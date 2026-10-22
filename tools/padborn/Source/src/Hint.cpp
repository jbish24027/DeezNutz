#include "Hint.h"

#include "Config.h"

#include <atomic>
#include <chrono>
#include <thread>

namespace OPad::Hint
{
	namespace
	{
		// Generation counter so a stale hide-timer from a previous scene can never
		// clobber a newer scene's hint.
		std::atomic<int> g_generation{ 0 };

		// keycode (266..281) -> the controlmap's gamepad button mask, the id
		// ControlMap::GetUserEventName wants. Inverse of GamepadMaskToKeyCode.
		std::uint32_t KeyCodeToGamepadMask(std::uint32_t a_keyCode)
		{
			switch (a_keyCode) {
			case 266: return 0x1;     // DPAD_UP
			case 267: return 0x2;     // DPAD_DOWN
			case 268: return 0x4;     // DPAD_LEFT
			case 269: return 0x8;     // DPAD_RIGHT
			case 270: return 0x10;    // Start
			case 271: return 0x20;    // Back
			case 272: return 0x40;    // L3
			case 273: return 0x80;    // R3
			case 274: return 0x100;   // LB
			case 275: return 0x200;   // RB
			case 276: return 0x1000;  // A
			case 277: return 0x2000;  // B
			case 278: return 0x4000;  // X
			case 279: return 0x8000;  // Y
			case 280: return 0x9;     // LT
			case 281: return 0xA;     // RT
			default: return 0;
			}
		}

		std::string_view ButtonFallbackName(std::uint32_t a_keyCode)
		{
			switch (a_keyCode) {
			case 270: return "Start"sv;
			case 271: return "Back"sv;
			case 272: return "L3"sv;
			case 273: return "R3"sv;
			case 274: return "LB"sv;
			case 275: return "RB"sv;
			case 276: return "A"sv;
			case 277: return "B"sv;
			case 278: return "X"sv;
			case 279: return "Y"sv;
			case 280: return "LT"sv;
			case 281: return "RT"sv;
			default: return ""sv;
			}
		}

		struct HintOrder
		{
			Action           action;
			std::string_view label;
		};

		// Priority order for the single hint line. Navigation is deliberately absent —
		// D-pad navigation reads as intuitive without help; buttons are what need naming.
		constexpr std::array kOrder{
			HintOrder{ Action::kYes, "Yes"sv },
			HintOrder{ Action::kToggle, "Toggle"sv },
			HintOrder{ Action::kSpeedUp, "Faster"sv },
			HintOrder{ Action::kSpeedDown, "Slower"sv },
			HintOrder{ Action::kPullOut, "Pull Out"sv },
			HintOrder{ Action::kEnd, "End"sv },
			HintOrder{ Action::kSearch, "Search"sv },
			HintOrder{ Action::kAlignment, "Align"sv },
			HintOrder{ Action::kAutoMode, "Auto"sv },
			HintOrder{ Action::kFreeCam, "Free Cam"sv },
			HintOrder{ Action::kHideUI, "Hide UI"sv },
		};

		// "[Activate] Yes" when the button carries a user event (the HUD swaps the token
		// for button art), "A Yes" as plain text when it does not.
		std::string TokenFor(std::uint32_t a_keyCode, bool a_hold)
		{
			std::string token;

			const auto mask = KeyCodeToGamepadMask(a_keyCode);
			std::string_view eventName;
			if (auto* controlMap = RE::ControlMap::GetSingleton(); controlMap && mask != 0) {
				eventName = controlMap->GetUserEventName(mask, RE::INPUT_DEVICE::kGamepad);
			}

			if (!eventName.empty()) {
				token = "[";
				token += eventName;
				token += "]";
			} else {
				token = ButtonFallbackName(a_keyCode);
			}

			if (a_hold) {
				token = "hold " + token;
			}
			return token;
		}

		std::string BuildHintText()
		{
			const auto& config = Config::Get();
			std::string text = "OPad:  ";
			bool        first = true;

			for (const auto& entry : kOrder) {
				for (const auto& [keyCode, binding] : config.bindings) {
					const bool asPress = binding.press == entry.action;
					const bool asHold = binding.hold == entry.action;
					if (!asPress && !asHold) {
						continue;
					}
					if (!first) {
						text += "   ";
					}
					text += TokenFor(keyCode, asHold);
					text += " ";
					text += entry.label;
					first = false;
					break;
				}
			}
			return text;
		}

		void InvokeTutorialText(const std::string& a_text, bool a_show)
		{
			auto* ui = RE::UI::GetSingleton();
			if (!ui) {
				return;
			}
			auto hud = ui->GetMenu(RE::HUDMenu::MENU_NAME);
			if (!hud || !hud->uiMovie) {
				return;
			}

			RE::GFxValue args[2];
			hud->uiMovie->CreateString(&args[0], a_text.c_str());
			args[1] = RE::GFxValue{ a_show };
			hud->uiMovie->Invoke("_root.HUDMovieBaseInstance.ShowTutorialHintText", nullptr, args, 2);
		}
	}

	void OnSceneStart()
	{
		const auto& config = Config::Get();
		if (!config.hintEnabled) {
			return;
		}

		const int generation = ++g_generation;
		const float seconds = config.hintSeconds;

		SKSE::GetTaskInterface()->AddUITask([]() {
			InvokeTutorialText(BuildHintText(), true);
		});

		std::thread([generation, seconds]() {
			std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<int>(seconds * 1000.0f)));
			if (generation == g_generation.load()) {
				SKSE::GetTaskInterface()->AddUITask([]() {
					InvokeTutorialText("", false);
				});
			}
		}).detach();
	}

	void OnSceneEnd()
	{
		++g_generation;
		SKSE::GetTaskInterface()->AddUITask([]() {
			InvokeTutorialText("", false);
		});
	}
}
