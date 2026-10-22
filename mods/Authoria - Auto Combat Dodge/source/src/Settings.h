#pragma once

// All configuration: this plugin's own ini plus the values it mirrors from
// TK Dodge RE (+ Addon) and Auto Combat, so a dodge fired here obeys the same
// rules as a dodge the player triggers by hand.
namespace ACD
{
	// Minimal INI reader: [Section] / key = value, ';' and '#' comments, UTF-8 BOM tolerated.
	// Keys and sections are matched case-insensitively.
	class Ini
	{
	public:
		bool Load(const std::filesystem::path& a_path);
		[[nodiscard]] bool               Loaded() const noexcept { return _loaded; }
		[[nodiscard]] std::optional<std::string> Get(std::string_view a_section, std::string_view a_key) const;
		// Section-agnostic lookup (Auto Combat's ini has no sections).
		[[nodiscard]] std::optional<std::string> GetAny(std::string_view a_key) const;

		[[nodiscard]] bool  GetBool(std::string_view a_section, std::string_view a_key, bool a_default) const;
		[[nodiscard]] float GetFloat(std::string_view a_section, std::string_view a_key, float a_default) const;
		[[nodiscard]] int   GetInt(std::string_view a_section, std::string_view a_key, int a_default) const;

	private:
		std::map<std::string, std::string> _values;  // "section\x1fkey" (lower case) -> value
		bool                               _loaded{ false };
	};

	struct Settings
	{
		// [General]
		bool enabled{ true };
		int  logLevel{ 1 };          // 0 = warnings/errors, 1 = info, 2 = debug (every decision)
		int  activationMode{ 0 };    // 0 = follow Auto Combat (memory, else hotkey mirror), 1 = hotkey mirror only, 2 = always in combat (test)
		bool requirePilot{ true };   // dodge only while the auto-pilot is actually driving the player
		int  mirrorHotkey{ 0 };      // 0 = read Hotkey= from AutoCombat.ini
		bool notifications{ false };

		// [Dodge]
		float chance{ 60.0f };              // percent per detected attack
		float cooldown{ 1.2f };             // seconds between auto-dodges
		float minStaminaPercent{ 25.0f };   // keep this much stamina in reserve (Requiem)
		float detectionRadius{ 420.0f };    // game units, attacker to player
		float facingCone{ 60.0f };          // attacker must face the player within +/- this many degrees
		float reactionDelay{ 0.10f };       // seconds after the wind-up starts
		float sideDodgeChance{ 35.0f };     // percent of frontal attacks dodged sideways instead of back
		int   attackCancel{ 1 };            // 0 never while attacking, 1 only in the TK/MCO cancel window, 2 any normal attack
		bool  respectPerkLock{ true };      // honour TK Dodge Perk Lock when the Addon has bUsePerkLock on

		// [Projectiles]
		bool  dodgeProjectiles{ false };
		float projectileRadius{ 2500.0f };
		float projectileWarning{ 0.45f };   // seconds to impact at which we react
		float projectileHitRadius{ 110.0f };

		// Mirrored from TK Dodge RE.ini (winning copy through the VFS)
		bool        tkStepDodge{ true };
		float       tkIFrame{ 0.3f };
		bool        tkSneakDodge{ false };
		std::string tkPerkPlugin;
		RE::FormID  tkPerkID{ 0 };

		// Mirrored from the TK Dodge RE Addon MCM settings
		float tkDodgeCost{ 10.0f };
		bool  tkUsePercentages{ false };
		bool  tkUsePerkLock{ true };
		bool  tkUseMCORecovery{ true };

		// Mirrored from AutoCombat.ini
		int  acHotkey{ 0 };
		bool acEnabledAtStart{ false };

		void Load();
		void LogSummary() const;

		static Settings& Get()
		{
			static Settings s;
			return s;
		}
	};
}
