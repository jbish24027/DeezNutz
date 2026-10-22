#include "Settings.h"

namespace ACD
{
	namespace
	{
		std::string Lower(std::string_view a_s)
		{
			std::string out(a_s);
			std::transform(out.begin(), out.end(), out.begin(), [](unsigned char c) { return static_cast<char>(std::tolower(c)); });
			return out;
		}

		std::string Trim(std::string_view a_s)
		{
			const auto first = a_s.find_first_not_of(" \t\r\n");
			if (first == std::string_view::npos) {
				return {};
			}
			const auto last = a_s.find_last_not_of(" \t\r\n");
			return std::string(a_s.substr(first, last - first + 1));
		}

		std::string Key(std::string_view a_section, std::string_view a_key)
		{
			return Lower(a_section) + '\x1f' + Lower(a_key);
		}

		std::optional<long long> ParseInteger(const std::string& a_value)
		{
			try {
				std::size_t idx = 0;
				long long   v = 0;
				if (a_value.size() > 2 && a_value[0] == '0' && (a_value[1] == 'x' || a_value[1] == 'X')) {
					v = std::stoll(a_value.substr(2), &idx, 16);
				} else {
					v = static_cast<long long>(std::stod(a_value, &idx));
				}
				return v;
			} catch (...) {
				return std::nullopt;
			}
		}
	}

	bool Ini::Load(const std::filesystem::path& a_path)
	{
		_values.clear();
		_loaded = false;
		std::ifstream in(a_path, std::ios::binary);
		if (!in) {
			return false;
		}
		std::string section;
		std::string line;
		bool        first = true;
		while (std::getline(in, line)) {
			if (first) {
				first = false;
				if (line.size() >= 3 && static_cast<unsigned char>(line[0]) == 0xEF && static_cast<unsigned char>(line[1]) == 0xBB && static_cast<unsigned char>(line[2]) == 0xBF) {
					line.erase(0, 3);
				}
			}
			auto t = Trim(line);
			if (t.empty() || t[0] == ';' || t[0] == '#') {
				continue;
			}
			if (t.front() == '[') {
				const auto close = t.find(']');
				section = Trim(t.substr(1, close == std::string::npos ? std::string::npos : close - 1));
				continue;
			}
			const auto eq = t.find('=');
			if (eq == std::string::npos) {
				continue;
			}
			auto key = Trim(t.substr(0, eq));
			auto value = t.substr(eq + 1);
			// strip a trailing inline comment (" ; ...")
			if (const auto sc = value.find(" ;"); sc != std::string::npos) {
				value.erase(sc);
			}
			value = Trim(value);
			if (value.size() >= 2 && value.front() == '"' && value.back() == '"') {
				value = value.substr(1, value.size() - 2);
			}
			_values[Key(section, key)] = value;
		}
		_loaded = true;
		return true;
	}

	std::optional<std::string> Ini::Get(std::string_view a_section, std::string_view a_key) const
	{
		if (const auto it = _values.find(Key(a_section, a_key)); it != _values.end()) {
			return it->second;
		}
		return std::nullopt;
	}

	std::optional<std::string> Ini::GetAny(std::string_view a_key) const
	{
		const auto suffix = '\x1f' + Lower(a_key);
		for (const auto& [k, v] : _values) {
			if (k.size() >= suffix.size() && k.compare(k.size() - suffix.size(), suffix.size(), suffix) == 0) {
				return v;
			}
		}
		return std::nullopt;
	}

	bool Ini::GetBool(std::string_view a_section, std::string_view a_key, bool a_default) const
	{
		const auto v = Get(a_section, a_key);
		if (!v || v->empty()) {
			return a_default;
		}
		const auto l = Lower(*v);
		if (l == "true" || l == "yes" || l == "on") {
			return true;
		}
		if (l == "false" || l == "no" || l == "off") {
			return false;
		}
		const auto n = ParseInteger(*v);
		return n ? *n != 0 : a_default;
	}

	float Ini::GetFloat(std::string_view a_section, std::string_view a_key, float a_default) const
	{
		const auto v = Get(a_section, a_key);
		if (!v || v->empty()) {
			return a_default;
		}
		try {
			return std::stof(*v);
		} catch (...) {
			return a_default;
		}
	}

	int Ini::GetInt(std::string_view a_section, std::string_view a_key, int a_default) const
	{
		const auto v = Get(a_section, a_key);
		if (!v || v->empty()) {
			return a_default;
		}
		const auto n = ParseInteger(*v);
		return n ? static_cast<int>(*n) : a_default;
	}

	void Settings::Load()
	{
		Ini own;
		if (!own.Load("Data/SKSE/Plugins/AutoCombatDodge.ini")) {
			logger::warn("AutoCombatDodge.ini not found - using built-in defaults");
		}
		enabled = own.GetBool("General", "Enabled", enabled);
		logLevel = std::clamp(own.GetInt("General", "LogLevel", logLevel), 0, 2);
		activationMode = std::clamp(own.GetInt("General", "ActivationMode", activationMode), 0, 2);
		requirePilot = own.GetBool("General", "RequireAutoPilot", requirePilot);
		mirrorHotkey = own.GetInt("General", "MirrorHotkey", mirrorHotkey);
		notifications = own.GetBool("General", "Notifications", notifications);

		chance = std::clamp(own.GetFloat("Dodge", "Chance", chance), 0.0f, 100.0f);
		cooldown = std::max(0.0f, own.GetFloat("Dodge", "Cooldown", cooldown));
		minStaminaPercent = std::clamp(own.GetFloat("Dodge", "MinStaminaPercent", minStaminaPercent), 0.0f, 100.0f);
		detectionRadius = std::max(0.0f, own.GetFloat("Dodge", "DetectionRadius", detectionRadius));
		facingCone = std::clamp(own.GetFloat("Dodge", "FacingConeDegrees", facingCone), 0.0f, 180.0f);
		reactionDelay = std::clamp(own.GetFloat("Dodge", "ReactionDelay", reactionDelay), 0.0f, 2.0f);
		sideDodgeChance = std::clamp(own.GetFloat("Dodge", "SideDodgeChance", sideDodgeChance), 0.0f, 100.0f);
		attackCancel = std::clamp(own.GetInt("Dodge", "AttackCancel", attackCancel), 0, 2);
		respectPerkLock = own.GetBool("Dodge", "RespectPerkLock", respectPerkLock);

		dodgeProjectiles = own.GetBool("Projectiles", "DodgeProjectiles", dodgeProjectiles);
		projectileRadius = std::max(0.0f, own.GetFloat("Projectiles", "ProjectileRadius", projectileRadius));
		projectileWarning = std::clamp(own.GetFloat("Projectiles", "WarningTime", projectileWarning), 0.05f, 3.0f);
		projectileHitRadius = std::max(10.0f, own.GetFloat("Projectiles", "HitRadius", projectileHitRadius));

		// TK Dodge RE.ini - the copy MO2's VFS resolves is the one TK_Dodge_RE.dll reads too.
		Ini tk;
		if (tk.Load("Data/SKSE/Plugins/TK Dodge RE.ini")) {
			tkStepDodge = tk.GetBool("Main", "StepDodge", tkStepDodge);
			tkIFrame = std::max(0.0f, tk.GetFloat("Main", "iFrameDuration", tkIFrame));
			tkSneakDodge = tk.GetBool("Main", "EnableSneakDodge", tkSneakDodge);
			tkPerkPlugin = tk.Get("Perk", "sPerkModFileName").value_or("");
			tkPerkID = static_cast<RE::FormID>(tk.GetInt("Perk", "PerkLockFormID", 0));
		} else {
			logger::warn("TK Dodge RE.ini not found - TK Dodge RE may not be installed; using its defaults");
		}

		// TK Dodge RE Addon MCM values: user/override file first, then the shipped defaults.
		Ini mcmUser;
		Ini mcmDefault;
		mcmUser.Load("Data/MCM/Settings/TKDodgeAddon.ini");
		mcmDefault.Load("Data/MCM/Config/TKDodgeAddon/settings.ini");
		auto pickF = [&](std::string_view sec, std::string_view key, float def) {
			return mcmUser.Get(sec, key) ? mcmUser.GetFloat(sec, key, def) : mcmDefault.GetFloat(sec, key, def);
		};
		auto pickB = [&](std::string_view sec, std::string_view key, bool def) {
			return mcmUser.Get(sec, key) ? mcmUser.GetBool(sec, key, def) : mcmDefault.GetBool(sec, key, def);
		};
		tkDodgeCost = std::max(0.0f, pickF("General", "fDodgeCost", tkDodgeCost));
		tkUsePercentages = pickB("General", "bUsePercentages", tkUsePercentages);
		tkUsePerkLock = pickB("Perk", "bUsePerkLock", tkUsePerkLock);
		tkUseMCORecovery = pickB("General", "bUseMCORecovery", tkUseMCORecovery);

		// AutoCombat.ini (no sections). Hotkey is a DirectInput scan code (K = 37).
		Ini ac;
		if (ac.Load("Data/SKSE/Plugins/AutoCombat.ini")) {
			if (auto v = ac.GetAny("Hotkey")) {
				try {
					acHotkey = std::stoi(*v);
				} catch (...) {
				}
			}
			if (auto v = ac.GetAny("Enabled")) {
				acEnabledAtStart = (*v == "1" || Lower(*v) == "true");
			}
		} else {
			logger::warn("AutoCombat.ini not found");
		}
	}

	void Settings::LogSummary() const
	{
		logger::info("settings: enabled={} activationMode={} requireAutoPilot={} chance={}% cooldown={}s minStamina={}% radius={} cone={} delay={}s side={}% attackCancel={} perkLock={} projectiles={} (r={} t={}s hit={})",
			enabled, activationMode, requirePilot, chance, cooldown, minStaminaPercent, detectionRadius, facingCone, reactionDelay,
			sideDodgeChance, attackCancel, respectPerkLock, dodgeProjectiles, projectileRadius, projectileWarning, projectileHitRadius);
		logger::info("TK Dodge RE: StepDodge={} iFrame={}s SneakDodge={} perk='{}'|{:X}; Addon: cost={}{} perkLock={} mcoRecovery={}",
			tkStepDodge, tkIFrame, tkSneakDodge, tkPerkPlugin, tkPerkID, tkDodgeCost, tkUsePercentages ? "%" : "", tkUsePerkLock, tkUseMCORecovery);
		logger::info("AutoCombat.ini: Hotkey={} Enabled={}", acHotkey, acEnabledAtStart);
	}
}
