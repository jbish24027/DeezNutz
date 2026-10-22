#include "Sprint.h"

#include "Config.h"

#include <chrono>

namespace OPad::Sprint
{
	namespace
	{
		// The hold floor stays above TK Dodge's SprintingPressDuration (0.25 s) so its
		// stop-window (tap-from-sprint = dodge) is never contested: below the floor we
		// do nothing.
		constexpr float kHoldFloorSecs = 0.3f;
		constexpr float kPressGapResetSecs = 0.25f;
		constexpr float kHeldLogStepSecs = 0.5f;

		class SprintRetrigger : public RE::BSTEventSink<RE::InputEvent*>
		{
		public:
			static SprintRetrigger* GetSingleton()
			{
				static SprintRetrigger instance;
				return &instance;
			}

			RE::BSEventNotifyControl ProcessEvent(RE::InputEvent* const* a_event, RE::BSTEventSource<RE::InputEvent*>*) override
			{
				if (!a_event || !*a_event) {
					return RE::BSEventNotifyControl::kContinue;
				}

				auto* ui = RE::UI::GetSingleton();
				if (!ui || ui->GameIsPaused()) {
					return RE::BSEventNotifyControl::kContinue;
				}

				const auto* userEvents = RE::UserEvents::GetSingleton();
				if (!userEvents) {
					return RE::BSEventNotifyControl::kContinue;
				}

				const bool logInput = Config::Get().sprintLog;

				for (const RE::InputEvent* event = *a_event; event; event = event->next) {
					if (event->GetEventType() != RE::INPUT_EVENT_TYPE::kButton) {
						continue;
					}
					const auto* button = event->AsButtonEvent();
					if (!button) {
						continue;
					}
					if (logInput) {
						LogButton(*event, *button);
					}
					if (button->QUserEvent() != userEvents->sprint) {
						continue;
					}

					const auto now = std::chrono::steady_clock::now();
					auto&      press = _press[HeldKey(static_cast<int>(event->GetDevice()), button->GetIDCode())];

					if (button->IsUp()) {
						if (press.active && logInput) {
							LogPressEnd(press, now, "up");
						}
						press.active = false;
						continue;
					}
					if (button->Value() == 0.0f) {
						continue;
					}

					if (!press.active || Secs(now - press.lastSeen) > kPressGapResetSecs) {
						if (press.active && logInput) {
							LogPressEnd(press, press.lastSeen, "gap");
						}
						press.firstDown = now;
						press.logged = false;
						press.flips = 0;
						press.active = true;
					}
					press.lastSeen = now;

					const float heldSecs = Secs(now - press.firstDown);
					if (heldSecs < kHoldFloorSecs) {
						continue;
					}

					auto* player = RE::PlayerCharacter::GetSingleton();
					if (!player) {
						continue;
					}

					auto& flags = player->GetPlayerRuntimeData().playerFlags;
					if (flags.isSprinting) {
						continue;
					}

					// Same gate CSR itself uses: only stamina. Movement is the engine's
					// business — setting the flag while below running speed just gets
					// cleared again next frame, which is exactly the retry loop we want back.
					auto* avOwner = player->AsActorValueOwner();
					if (!avOwner || avOwner->GetActorValue(RE::ActorValue::kStamina) <= 0.0f) {
						continue;
					}

					flags.isSprinting = true;
					++press.flips;
					if (!press.logged) {
						press.logged = true;
						if (logInput) {
							logger::info("sprint retriggered at held {:.2f}s (sink-tracked)", heldSecs);
						}
					}
				}

				return RE::BSEventNotifyControl::kContinue;
			}

		private:
			struct PressState
			{
				std::chrono::steady_clock::time_point firstDown{};
				std::chrono::steady_clock::time_point lastSeen{};
				bool                                  active{ false };
				bool                                  logged{ false };
				int                                   flips{ 0 };
			};

			static float Secs(std::chrono::steady_clock::duration a_dur)
			{
				return std::chrono::duration_cast<std::chrono::duration<float>>(a_dur).count();
			}

			// One line per finished press, format shared with the 1.2.1-diag routing
			// table: was sprint actually ON at release, how hard did the rescue have to
			// fight (flips), and which POV.
			static void LogPressEnd(const PressState& a_press, std::chrono::steady_clock::time_point a_end, const char* a_how)
			{
				const float held = Secs(a_end - a_press.firstDown);

				bool  sprinting = false;
				float stamina = -1.0f;
				if (auto* player = RE::PlayerCharacter::GetSingleton()) {
					sprinting = player->GetPlayerRuntimeData().playerFlags.isSprinting;
					if (auto* avOwner = player->AsActorValueOwner()) {
						stamina = avOwner->GetActorValue(RE::ActorValue::kStamina);
					}
				}

				const char* pov = "??";
				if (auto* cam = RE::PlayerCamera::GetSingleton(); cam && cam->currentState) {
					pov = cam->currentState->id == RE::CameraState::kFirstPerson ? "1p" : "3p";
				}

				logger::info("[press] end={} pov={} held={:.2f}s flips={} sprint@end={} stam={:.0f}",
					a_how, pov, held, a_press.flips, sprinting ? 1 : 0, stamina);
			}

			void LogButton(const RE::InputEvent& a_event, const RE::ButtonEvent& a_button)
			{
				const int   device = static_cast<int>(a_event.GetDevice());
				const auto  id = a_button.GetIDCode();
				const char* userEvent = a_button.QUserEvent().c_str();

				if (a_button.IsDown()) {
					_lastHeldLog[HeldKey(device, id)] = 0.0f;
					logger::info("[in] dev={} id={} ue='{}' DOWN val={:.2f}", device, id, userEvent, a_button.Value());
				} else if (a_button.IsUp()) {
					logger::info("[in] dev={} id={} ue='{}' UP after {:.2f}s", device, id, userEvent, a_button.HeldDuration());
				} else if (a_button.IsHeld()) {
					auto [it, inserted] = _lastHeldLog.try_emplace(HeldKey(device, id), 0.0f);
					const float held = a_button.HeldDuration();
					if (inserted || held - it->second >= kHeldLogStepSecs || held < it->second) {
						it->second = held;
						logger::info("[in] dev={} id={} ue='{}' HELD {:.2f}s val={:.2f}", device, id, userEvent, held, a_button.Value());
					}
				}
			}

			static std::uint64_t HeldKey(int a_device, std::uint32_t a_id)
			{
				return (static_cast<std::uint64_t>(a_device) << 32) | a_id;
			}

			std::unordered_map<std::uint64_t, float>      _lastHeldLog;
			std::unordered_map<std::uint64_t, PressState> _press;
		};
	}

	void ApplyButton()
	{
		const int choice = Config::Get().sprintButton;
		if (choice == 0) {
			return;  // keep the controlmap's own layout
		}

		std::uint16_t targetMask = 0;
		const char*   targetName = "?";
		switch (choice) {
		case 1: targetMask = 0x2000; targetName = "B"; break;
		case 2: targetMask = 0x100; targetName = "LB"; break;
		case 3: targetMask = 0x40; targetName = "LS"; break;
		default: return;
		}

		auto* controlMap = RE::ControlMap::GetSingleton();
		const auto* userEvents = RE::UserEvents::GetSingleton();
		if (!controlMap || !userEvents) {
			logger::error("sprint button: no ControlMap/UserEvents singleton");
			return;
		}
		auto* context = controlMap->controlMap[RE::ControlMap::InputContextID::kGameplay];
		if (!context) {
			logger::error("sprint button: no gameplay input context");
			return;
		}

		auto& mappings = context->deviceMappings[RE::INPUT_DEVICE::kGamepad];
		RE::ControlMap::UserEventMapping* sprint = nullptr;
		RE::ControlMap::UserEventMapping* occupant = nullptr;
		for (auto& mapping : mappings) {
			if (mapping.eventID == userEvents->sprint) {
				sprint = &mapping;
			} else if (mapping.inputKey == targetMask) {
				occupant = &mapping;
			}
		}
		if (!sprint) {
			logger::error("sprint button: no gamepad Sprint mapping in the gameplay context");
			return;
		}
		if (sprint->inputKey == targetMask) {
			return;  // already there
		}

		const auto oldKey = sprint->inputKey;
		sprint->inputKey = targetMask;
		if (occupant) {
			// classic swap: whatever sat on the target button takes Sprint's old one,
			// so no button carries two events and nothing is lost.
			occupant->inputKey = oldKey;
			logger::info("sprint moved to {} (0x{:X}); '{}' took its old button 0x{:X}",
				targetName, targetMask, occupant->eventID.c_str(), oldKey);
		} else {
			logger::info("sprint moved to {} (0x{:X}); old button 0x{:X} left free",
				targetName, targetMask, oldKey);
		}
	}

	void Register()
	{
		if (!Config::Get().sprintEnabled) {
			logger::info("sprint rescue disabled by config");
			return;
		}
		if (auto* manager = RE::BSInputDeviceManager::GetSingleton()) {
			manager->AddEventSink(SprintRetrigger::GetSingleton());
			logger::info("sprint rescue registered, hold floor {:.2f}s, sink-tracked press timing", kHoldFloorSecs);
		} else {
			logger::error("no BSInputDeviceManager - sprint rescue not registered");
		}
	}
}
