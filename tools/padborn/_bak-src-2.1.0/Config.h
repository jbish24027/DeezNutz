#pragma once

#include "PCH.h"

namespace OPad
{
	// Every OStim action OPad can drive. Each one maps to a keycode OStim already
	// listens on, read live from OStim.esp's globals — see OStimBridge.
	enum class Action : std::uint8_t
	{
		kNone = 0,
		kUp,
		kDown,
		kLeft,
		kRight,
		kToggle,
		kYes,
		kEnd,
		kSpeedUp,
		kSpeedDown,
		kPullOut,
		kAutoMode,
		kFreeCam,
		kSearch,
		kAlignment,
		kHideUI,
		kSceneStart,
	};

	[[nodiscard]] std::string_view ActionName(Action a_action);
	[[nodiscard]] Action ActionFromName(std::string_view a_name);

	// One gamepad button's bindings. A button with no hold binding fires its press
	// action on button-down (zero added latency); a button that also carries a hold
	// binding has to wait for release to know which one the user meant.
	struct ButtonBinding
	{
		Action press{ Action::kNone };
		Action hold{ Action::kNone };
	};

	struct Config
	{
		// keyed by the SKSE gamepad keycode, 266..281
		std::unordered_map<std::uint32_t, ButtonBinding> bindings;

		float holdSeconds{ 0.6f };

		// Swallow every gamepad button while a scene runs, so Wheeler / TK Dodge /
		// TDM / Gamepad++ never see the press. Off = translate but let them through.
		bool fullLockout{ true };

		// Rewrite OStim's own Search and Alignment keys off K and L, which collide
		// with other mods on this load order. See OStimBridge::ReserveKeys.
		bool reserveCollidingKeys{ true };

		bool  hintEnabled{ true };
		float hintSeconds{ 10.0f };  // legacy toast timing; the bar ignores it (persistent)

		// Glyph bar geometry, as fractions of the screen (right edge / bottom edge)
		// plus a size multiplier. Defaults replicate the approved 2160p mockup.
		float hintScale{ 1.0f };
		float hintAnchorX{ 0.786f };
		float hintAnchorY{ 0.9815f };

		// 0 = auto (ask the engine's gamepad device), 1 = force Xbox, 2 = force PS.
		int hintGlyphs{ 0 };

		// Padborn sprint rescue (device-agnostic input sink). OFF by default — the
		// bug it fixes is specific to one mod mix (Classic Sprinting Redone + TK
		// Dodge RE Addon) and is not confirmed on other rigs (user ruling
		// 2026-08-24: test-build feature). log=true also writes the per-press diag
		// verdict lines.
		bool sprintEnabled{ false };
		bool sprintLog{ false };

		// Where the gamepad's Sprint control sits. 0 = keep whatever the current
		// controlmap says (default); 1 = B, 2 = LB, 3 = LS click — applied at
		// runtime as a swap with whatever event held the target button, so no
		// controlmap file is touched and no CCS reinstall is needed.
		int sprintButton{ 0 };

		bool logInput{ false };

		// First-person block (2.1.0): keep the player camera out of first person no
		// matter who asks - scripts (First Person Interactions ends every lever
		// pull with Game.ForceFirstPerson), the vanilla Toggle POV control, zoom-in,
		// camera restores on load, other plugins. See Camera.cpp for the layers.
		bool cameraBlockFirstPerson{ true };

		// Let the vanilla Toggle POV control (keyboard F by default) still switch;
		// only forced/automatic switches are blocked then, and the per-frame
		// watchdog stands down. Off = the control does nothing.
		bool cameraAllowManualToggle{ false };

		static Config& Get();

		// Reads SKSE/Plugins/OPad.json if present, otherwise keeps the defaults below.
		void Load();
		void ApplyDefaults();
	};
}
