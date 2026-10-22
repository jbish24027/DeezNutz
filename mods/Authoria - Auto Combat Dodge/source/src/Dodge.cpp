#include "Dodge.h"
#include "AutoCombatLink.h"
#include "Settings.h"

namespace ACD::Dodge
{
	namespace
	{
		using AS = RE::ATTACK_STATE_ENUM;

		constexpr auto kForward = "TKDodgeForward"sv;
		constexpr auto kBack = "TKDodgeBack"sv;
		constexpr auto kLeft = "TKDodgeLeft"sv;
		constexpr auto kRight = "TKDodgeRight"sv;

		struct Pending
		{
			RE::ActorHandle attacker;
			float           due{ 0.0f };
			bool            valid{ false };
		};

		float                                     g_clock{ 0.0f };        // seconds of game-frame time since load
		float                                     g_nextAllowed{ 0.0f };  // cooldown gate
		bool                                      g_wasActive{ false };
		Pending                                   g_pending;
		std::unordered_map<std::uint32_t, AS>     g_lastState;   // attacker handle -> last melee attack state
		std::unordered_map<std::uint32_t, float>  g_projSeen;    // projectile handle -> time first judged
		RE::BGSPerk*                              g_perk{ nullptr };
		std::mt19937                              g_rng{ std::random_device{}() };
		float                                     g_staminaCheckAt{ -1.0f };
		float                                     g_staminaAtFire{ 0.0f };
		std::uint32_t                             g_fired{ 0 };

		bool Roll(float a_percent)
		{
			if (a_percent >= 100.0f) {
				return true;
			}
			if (a_percent <= 0.0f) {
				return false;
			}
			return std::uniform_real_distribution<float>(0.0f, 100.0f)(g_rng) < a_percent;
		}

		bool IsMeleeWindup(AS a_state)
		{
			return a_state == AS::kDraw || a_state == AS::kSwing || a_state == AS::kBash;
		}

		bool GraphBool(RE::Actor* a_actor, std::string_view a_name, bool& a_out)
		{
			a_out = false;
			return a_actor->GetGraphVariableBool(RE::BSFixedString(a_name), a_out);
		}

		// Is Auto Combat fighting for the player right now?
		bool AutoPilotActive(RE::PlayerCharacter* a_pc)
		{
			const auto& cfg = Settings::Get();
			if (cfg.activationMode == 2) {
				return a_pc->IsInCombat();
			}
			switch (AutoCombat::LinkType()) {
			case AutoCombat::Link::kMemory:
				return cfg.requirePilot ? AutoCombat::IsPilotActive() : AutoCombat::IsEnabled();
			case AutoCombat::Link::kMirror:
				// No live pilot flag on this path: "switched on and in combat" stands in for it.
				return AutoCombat::IsEnabled() && a_pc->IsInCombat();
			default:
				return false;
			}
		}

		// The checks TK Dodge RE (and its Addon) make before a hand-triggered dodge,
		// plus this plugin's stamina reserve. nullptr = may dodge.
		const char* BlockReason(RE::PlayerCharacter* a_pc)
		{
			const auto& cfg = Settings::Get();
			const auto* st = a_pc->AsActorState();
			bool        b = false;

			if (a_pc->IsDead()) {
				return "dead";
			}
			if (!GraphBool(a_pc, "bIsDodging", b)) {
				return "TK Dodge behaviour not present on the player graph (bIsDodging missing)";
			}
			if (b) {
				return "already dodging";
			}
			if (a_pc->IsInKillMove()) {
				return "in a kill move";
			}
			if (st->GetSitSleepState() != RE::SIT_SLEEP_STATE::kNormal || st->GetKnockState() != RE::KNOCK_STATE_ENUM::kNormal ||
				st->GetFlyState() != RE::FLY_STATE::kNone) {
				return "sitting / knocked down / flying";
			}
			if (st->IsSwimming() || st->IsBleedingOut() || a_pc->IsOnMount()) {
				return "swimming / bleeding out / mounted";
			}
			if (GraphBool(a_pc, "bInJumpState", b) && b) {
				return "jumping";
			}
			if (a_pc->IsStaggering()) {
				return "staggered";
			}
			if (st->IsSneaking() && !cfg.tkSneakDodge) {
				return "sneaking (TK Dodge EnableSneakDodge is off)";
			}
			if (const auto cm = RE::ControlMap::GetSingleton(); cm && (!cm->IsMovementControlsEnabled() || !cm->IsFightingControlsEnabled())) {
				return "movement or fighting controls disabled";
			}
			if (st->GetAttackState() != AS::kNone) {
				if (a_pc->IsPowerAttacking()) {
					return "player is power attacking";
				}
				if (cfg.attackCancel == 0) {
					return "player is attacking (AttackCancel=0)";
				}
				if (cfg.attackCancel == 1) {
					bool ready = false;
					bool recovery = false;
					GraphBool(a_pc, "IsAttackReady", ready);
					if (cfg.tkUseMCORecovery) {
						GraphBool(a_pc, "MCO_IsInRecovery", recovery);
					}
					if (!ready && !recovery) {
						return "player is mid-swing (outside the TK/MCO cancel window)";
					}
				}
			}
			if (cfg.respectPerkLock && cfg.tkUsePerkLock && g_perk && !a_pc->HasPerk(g_perk)) {
				return "TK Dodge perk-lock perk not learned";
			}
			const float cur = a_pc->AsActorValueOwner()->GetActorValue(RE::ActorValue::kStamina);
			const float max = a_pc->GetActorValueMax(RE::ActorValue::kStamina);
			if (max > 0.0f && (cur / max) * 100.0f < cfg.minStaminaPercent) {
				return "stamina below the reserve (MinStaminaPercent)";
			}
			const float cost = cfg.tkUsePercentages ? max * cfg.tkDodgeCost / 100.0f : cfg.tkDodgeCost;
			if (cur < cost) {
				return "not enough stamina for TK Dodge's cost";
			}
			return nullptr;
		}

		// a_heading: where the threat is, relative to the player's facing, in degrees
		// (0 = straight ahead, positive = to the right, see TESObjectREFR::GetHeadingAngle).
		std::string_view EventForMelee(float a_heading)
		{
			const float abs = std::fabs(a_heading);
			if (abs <= 60.0f) {
				if (Roll(Settings::Get().sideDodgeChance)) {
					return Roll(50.0f) ? kLeft : kRight;
				}
				return kBack;
			}
			if (abs >= 120.0f) {
				return kForward;  // attacker behind: step forward, away from it
			}
			return a_heading > 0.0f ? kLeft : kRight;  // attacker on one side: step to the other
		}

		void Fire(RE::PlayerCharacter* a_pc, std::string_view a_event, std::string a_why)
		{
			const auto& cfg = Settings::Get();
			g_nextAllowed = g_clock + cfg.cooldown;
			g_staminaAtFire = a_pc->AsActorValueOwner()->GetActorValue(RE::ActorValue::kStamina);
			g_staminaCheckAt = g_clock + 0.6f;
			++g_fired;

			// Same sequence as TK Dodge RE's own dodge(): iStep for step dodge, the i-frame
			// length, then the direction event. Its Addon charges the stamina when the
			// behaviour raises TKDR_DodgeStart, exactly as for a hand-triggered dodge.
			// Queued through SKSE's task interface so it runs on the main thread's task pass.
			SKSE::GetTaskInterface()->AddTask([event = std::string(a_event), why = std::move(a_why), step = cfg.tkStepDodge, iframe = cfg.tkIFrame]() {
				auto* pc = RE::PlayerCharacter::GetSingleton();
				if (!pc) {
					return;
				}
				bool dodging = false;
				if (pc->GetGraphVariableBool("bIsDodging"sv, dodging) && dodging) {
					logger::debug("dodge dropped: a dodge started in the meantime");
					return;
				}
				if (step) {
					pc->SetGraphVariableInt("iStep"sv, 2);
				}
				pc->SetGraphVariableFloat("TKDR_IframeDuration"sv, iframe);
				const bool accepted = pc->NotifyAnimationGraph(RE::BSFixedString(event));
				logger::info("dodge {} -> {} ({})", event, accepted ? "accepted by the graph" : "REJECTED by the graph", why);
			});
		}

		void ScanMelee(RE::PlayerCharacter* a_pc)
		{
			const auto& cfg = Settings::Get();
			auto*       lists = RE::ProcessLists::GetSingleton();
			if (!lists) {
				return;
			}
			const auto ppos = a_pc->GetPosition();
			const float trackRadius = cfg.detectionRadius + 300.0f;

			std::unordered_map<std::uint32_t, AS> next;
			for (auto& handle : lists->highActorHandles) {
				const auto ptr = handle.get();
				auto*      actor = ptr.get();
				if (!actor || actor == a_pc || actor->IsDead() || !actor->Is3DLoaded()) {
					continue;
				}
				const float dist = actor->GetPosition().GetDistance(ppos);
				if (dist > trackRadius) {
					continue;
				}
				const auto key = handle.native_handle();
				const auto state = actor->AsActorState()->GetAttackState();
				next[key] = state;

				const auto prevIt = g_lastState.find(key);
				const AS   prev = prevIt != g_lastState.end() ? prevIt->second : AS::kNone;
				if (!IsMeleeWindup(state) || IsMeleeWindup(prev)) {
					continue;  // only the frame an attack starts
				}
				if (!actor->IsHostileToActor(a_pc)) {
					continue;
				}
				const auto target = actor->GetActorRuntimeData().currentCombatTarget.get();
				if (target.get() != a_pc) {
					logger::debug("{:08X} attacks, but not at the player", actor->GetFormID());
					continue;
				}
				if (dist > cfg.detectionRadius) {
					logger::debug("{:08X} attacks from {:.0f} units (radius {:.0f}) - ignored", actor->GetFormID(), dist, cfg.detectionRadius);
					continue;
				}
				const float facing = actor->GetHeadingAngle(ppos, true);
				if (facing > cfg.facingCone) {
					logger::debug("{:08X} attacks facing {:.0f} deg away - ignored", actor->GetFormID(), facing);
					continue;
				}
				if (!Roll(cfg.chance)) {
					logger::debug("{:08X} attack: chance roll failed", actor->GetFormID());
					continue;
				}
				if (!g_pending.valid) {
					g_pending = { handle, g_clock + cfg.reactionDelay, true };
					logger::debug("{:08X} winds up (state {}) at {:.0f} units - dodge queued in {:.2f}s", actor->GetFormID(), std::to_underlying(state), dist, cfg.reactionDelay);
				}
			}
			g_lastState.swap(next);
		}

		void ProcessPending(RE::PlayerCharacter* a_pc)
		{
			if (!g_pending.valid || g_clock < g_pending.due) {
				return;
			}
			const auto pending = g_pending;
			g_pending.valid = false;

			if (g_clock < g_nextAllowed) {
				logger::debug("dodge skipped: cooldown");
				return;
			}
			const auto ptr = pending.attacker.get();
			auto*      attacker = ptr.get();
			if (!attacker || attacker->IsDead()) {
				return;
			}
			if (!IsMeleeWindup(attacker->AsActorState()->GetAttackState())) {
				logger::debug("dodge skipped: {:08X}'s attack ended before the reaction", attacker->GetFormID());
				return;
			}
			if (const auto why = BlockReason(a_pc)) {
				logger::debug("dodge skipped: {}", why);
				return;
			}
			const float heading = a_pc->GetHeadingAngle(attacker->GetPosition(), false);
			Fire(a_pc, EventForMelee(heading), std::format("melee from {:08X}, {:.0f} deg", attacker->GetFormID(), heading));
		}

		void ScanProjectiles(RE::PlayerCharacter* a_pc)
		{
			const auto& cfg = Settings::Get();
			auto*       mgr = RE::Projectile::Manager::GetSingleton();
			if (!mgr) {
				return;
			}
			auto center = a_pc->GetPosition();
			center.z += 70.0f;

			bool          found = false;
			float         bestT = 1.0e9f;
			RE::NiPoint3  bestPoint;
			std::uint32_t bestKey = 0;
			RE::FormID    bestShooter = 0;

			{
				RE::BSSpinLockGuard guard(mgr->projectileLock);
				auto scan = [&](RE::BSTArray<RE::ProjectileHandle>& a_array) {
					for (auto& handle : a_array) {
						const auto key = handle.native_handle();
						if (g_projSeen.contains(key)) {
							continue;
						}
						const auto ptr = handle.get();
						auto*      proj = ptr.get();
						if (!proj) {
							continue;
						}
						const auto type = proj->GetFormType();
						if (type != RE::FormType::ProjectileArrow && type != RE::FormType::ProjectileMissile) {
							continue;  // flames, beams, cones, hazards: a step does not escape them
						}
						const auto  shooterRef = proj->GetProjectileRuntimeData().shooter.get();
						auto* const shooter = shooterRef ? shooterRef->As<RE::Actor>() : nullptr;
						if (!shooter || shooter == a_pc || !shooter->IsHostileToActor(a_pc)) {
							continue;
						}
						const auto pos = proj->GetPosition();
						if (pos.GetDistance(center) > cfg.projectileRadius) {
							continue;
						}
						RE::NiPoint3 vel;
						proj->GetLinearVelocity(vel);
						const float v2 = vel.x * vel.x + vel.y * vel.y + vel.z * vel.z;
						if (v2 < 100.0f) {
							continue;
						}
						const RE::NiPoint3 rel = center - pos;
						const float        t = (rel.x * vel.x + rel.y * vel.y + rel.z * vel.z) / v2;
						if (t <= 0.0f || t > cfg.projectileWarning) {
							continue;
						}
						const RE::NiPoint3 closest = pos + vel * t;
						if (closest.GetDistance(center) > cfg.projectileHitRadius) {
							continue;
						}
						if (t < bestT) {
							found = true;
							bestT = t;
							bestPoint = closest;
							bestKey = key;
							bestShooter = shooter->GetFormID();
						}
					}
				};
				scan(mgr->limited);
				scan(mgr->unlimited);
			}

			// forget projectiles judged more than 5 s ago
			std::erase_if(g_projSeen, [](const auto& kv) { return g_clock - kv.second > 5.0f; });

			if (!found) {
				return;
			}
			g_projSeen[bestKey] = g_clock;  // judge each projectile once
			if (!Roll(cfg.chance)) {
				logger::debug("projectile from {:08X}: chance roll failed", bestShooter);
				return;
			}
			if (g_clock < g_nextAllowed) {
				logger::debug("projectile dodge skipped: cooldown");
				return;
			}
			if (const auto why = BlockReason(a_pc)) {
				logger::debug("projectile dodge skipped: {}", why);
				return;
			}
			// Step sideways, away from the side the projectile passes on.
			const float heading = a_pc->GetHeadingAngle(bestPoint, false);
			std::string_view ev;
			if (std::fabs(heading) < 15.0f || std::fabs(heading) > 165.0f) {
				ev = Roll(50.0f) ? kLeft : kRight;
			} else {
				ev = heading > 0.0f ? kLeft : kRight;
			}
			Fire(a_pc, ev, std::format("projectile from {:08X}, impact in {:.2f}s", bestShooter, bestT));
		}

		void Tick(RE::PlayerCharacter* a_pc, float a_delta)
		{
			g_clock += std::clamp(a_delta, 0.0f, 0.5f);

			const auto& cfg = Settings::Get();
			if (!cfg.enabled || !a_pc || !a_pc->Is3DLoaded()) {
				return;
			}

			const bool active = AutoPilotActive(a_pc);
			if (active != g_wasActive) {
				g_wasActive = active;
				logger::info("auto-dodge {} (link: {}, Auto Combat enabled={}, auto-pilot={})", active ? "ARMED" : "idle",
					AutoCombat::LinkName(), AutoCombat::IsEnabled(), AutoCombat::IsPilotActive());
				if (cfg.notifications) {
					RE::SendHUDMessage::ShowHUDMessage(active ? "Auto Dodge: on" : "Auto Dodge: off");
				}
				if (!active) {
					g_pending.valid = false;
					g_lastState.clear();
				}
			}

			if (g_staminaCheckAt > 0.0f && g_clock >= g_staminaCheckAt) {
				g_staminaCheckAt = -1.0f;
				const float now = a_pc->AsActorValueOwner()->GetActorValue(RE::ActorValue::kStamina);
				logger::debug("stamina {:.1f} -> {:.1f} 0.6 s after the dodge (TK Dodge's own cost should show here)", g_staminaAtFire, now);
			}

			if (!active || a_pc->IsDead()) {
				return;
			}
			ScanMelee(a_pc);
			ProcessPending(a_pc);
			if (cfg.dodgeProjectiles) {
				ScanProjectiles(a_pc);
			}
		}

		struct PlayerUpdate
		{
			static void thunk(RE::PlayerCharacter* a_this, float a_delta)
			{
				func(a_this, a_delta);
				Tick(a_this, a_delta);
			}
			static inline void (*func)(RE::PlayerCharacter*, float) = nullptr;
		};
	}

	void InstallHook()
	{
		// PlayerCharacter::Update (Actor vtable slot 0xAD on SE and AE), primary vtable,
		// located through Address Library (VTABLE_PlayerCharacter = IDs 261916 / 208040).
		REL::Relocation<std::uintptr_t> vtbl{ RE::VTABLE_PlayerCharacter[0] };
		PlayerUpdate::func = reinterpret_cast<void (*)(RE::PlayerCharacter*, float)>(
			vtbl.write_vfunc(0xAD, reinterpret_cast<std::uintptr_t>(&PlayerUpdate::thunk)));
		logger::info("PlayerCharacter::Update hooked");
	}

	void OnDataLoaded()
	{
		const auto& cfg = Settings::Get();
		g_perk = nullptr;
		if (!cfg.tkPerkPlugin.empty() && cfg.tkPerkID != 0) {
			if (auto* dh = RE::TESDataHandler::GetSingleton()) {
				g_perk = dh->LookupForm<RE::BGSPerk>(cfg.tkPerkID & 0x00FFFFFF, cfg.tkPerkPlugin);
			}
			logger::info("TK Dodge perk lock: {} ({}|{:X})", g_perk ? "found" : "NOT found - not enforced", cfg.tkPerkPlugin, cfg.tkPerkID);
		}
	}

	void Reset()
	{
		g_pending.valid = false;
		g_lastState.clear();
		g_projSeen.clear();
		g_nextAllowed = 0.0f;
		g_clock = 0.0f;
		g_staminaCheckAt = -1.0f;
		g_wasActive = false;
	}
}
