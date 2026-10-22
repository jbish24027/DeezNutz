#include "Config.h"

#include <nlohmann/json.hpp>

#include <filesystem>
#include <fstream>

namespace OPad
{
	namespace
	{
		// Padborn.json is the name since the 2.0 merge; OPad.json still read as the
		// fallback so an existing install keeps its settings.
		constexpr auto kConfigPath = "Data/SKSE/Plugins/Padborn.json"sv;
		constexpr auto kLegacyConfigPath = "Data/SKSE/Plugins/OPad.json"sv;

		struct NameEntry
		{
			Action           action;
			std::string_view name;
		};

		constexpr std::array kActionNames{
			NameEntry{ Action::kNone, "none"sv },
			NameEntry{ Action::kUp, "up"sv },
			NameEntry{ Action::kDown, "down"sv },
			NameEntry{ Action::kLeft, "left"sv },
			NameEntry{ Action::kRight, "right"sv },
			NameEntry{ Action::kToggle, "toggle"sv },
			NameEntry{ Action::kYes, "yes"sv },
			NameEntry{ Action::kEnd, "end"sv },
			NameEntry{ Action::kSpeedUp, "speedUp"sv },
			NameEntry{ Action::kSpeedDown, "speedDown"sv },
			NameEntry{ Action::kPullOut, "pullOut"sv },
			NameEntry{ Action::kAutoMode, "autoMode"sv },
			NameEntry{ Action::kFreeCam, "freeCam"sv },
			NameEntry{ Action::kSearch, "search"sv },
			NameEntry{ Action::kAlignment, "alignment"sv },
			NameEntry{ Action::kHideUI, "hideUI"sv },
			NameEntry{ Action::kSceneStart, "sceneStart"sv },
		};

		// SKSE gamepad keycodes, the same numbering OStim's scancode.json uses.
		constexpr std::uint32_t kDPadUp = 266;
		constexpr std::uint32_t kDPadDown = 267;
		constexpr std::uint32_t kDPadLeft = 268;
		constexpr std::uint32_t kDPadRight = 269;
		constexpr std::uint32_t kStart = 270;
		constexpr std::uint32_t kBack = 271;
		constexpr std::uint32_t kL3 = 272;
		constexpr std::uint32_t kR3 = 273;
		constexpr std::uint32_t kLB = 274;
		constexpr std::uint32_t kRB = 275;
		constexpr std::uint32_t kA = 276;
		constexpr std::uint32_t kB = 277;
		constexpr std::uint32_t kX = 278;
		constexpr std::uint32_t kY = 279;
		constexpr std::uint32_t kLT = 280;
		constexpr std::uint32_t kRT = 281;
	}

	std::string_view ActionName(Action a_action)
	{
		for (const auto& entry : kActionNames) {
			if (entry.action == a_action) {
				return entry.name;
			}
		}
		return "none"sv;
	}

	Action ActionFromName(std::string_view a_name)
	{
		for (const auto& entry : kActionNames) {
			if (entry.name == a_name) {
				return entry.action;
			}
		}
		return Action::kNone;
	}

	Config& Config::Get()
	{
		static Config instance;
		return instance;
	}

	void Config::ApplyDefaults()
	{
		bindings.clear();

		// Navigation and the two constant-use actions sit on plain presses so they
		// fire on button-down with no added latency.
		bindings[kDPadUp] = { Action::kUp, Action::kNone };
		bindings[kDPadDown] = { Action::kDown, Action::kNone };
		bindings[kDPadLeft] = { Action::kLeft, Action::kNone };
		bindings[kDPadRight] = { Action::kRight, Action::kNone };
		bindings[kA] = { Action::kYes, Action::kNone };
		bindings[kX] = { Action::kToggle, Action::kNone };
		bindings[kRT] = { Action::kSpeedUp, Action::kNone };
		bindings[kLT] = { Action::kSpeedDown, Action::kNone };
		bindings[kRB] = { Action::kPullOut, Action::kNone };
		bindings[kLB] = { Action::kSearch, Action::kNone };
		bindings[kY] = { Action::kAlignment, Action::kNone };
		bindings[kStart] = { Action::kAutoMode, Action::kNone };
		bindings[kL3] = { Action::kFreeCam, Action::kNone };
		bindings[kBack] = { Action::kHideUI, Action::kNone };

		// End scene is hold-only on purpose — a stray tap should not end the scene.
		bindings[kB] = { Action::kNone, Action::kEnd };

		// kR3 left free.
	}

	void Config::Load()
	{
		ApplyDefaults();

		std::filesystem::path configPath{ kConfigPath };

		std::error_code ec;
		if (!std::filesystem::exists(configPath, ec)) {
			configPath = kLegacyConfigPath;
			if (!std::filesystem::exists(configPath, ec)) {
				logger::info("no Padborn.json (or legacy OPad.json), using built-in defaults");
				return;
			}
			logger::info("using legacy OPad.json");
		}

		std::ifstream file{ configPath };
		if (!file.is_open()) {
			logger::warn("OPad.json exists but could not be opened, using defaults");
			return;
		}

		nlohmann::json json;
		try {
			file >> json;
		} catch (const std::exception& e) {
			logger::error("OPad.json is malformed ({}), using defaults", e.what());
			return;
		}

		holdSeconds = json.value("holdSeconds", holdSeconds);
		fullLockout = json.value("fullLockout", fullLockout);
		reserveCollidingKeys = json.value("reserveCollidingKeys", reserveCollidingKeys);
		logInput = json.value("logInput", logInput);

		if (json.contains("sprint") && json["sprint"].is_object()) {
			const auto& sprint = json["sprint"];
			sprintEnabled = sprint.value("enabled", sprintEnabled);
			sprintLog = sprint.value("log", sprintLog);
			if (const auto button = sprint.value("button", "keep"s); button == "b") {
				sprintButton = 1;
			} else if (button == "lb") {
				sprintButton = 2;
			} else if (button == "ls") {
				sprintButton = 3;
			} else {
				sprintButton = 0;
			}
		}

		if (json.contains("camera") && json["camera"].is_object()) {
			const auto& camera = json["camera"];
			cameraBlockFirstPerson = camera.value("blockFirstPerson", cameraBlockFirstPerson);
			cameraAllowManualToggle = camera.value("allowManualToggle", cameraAllowManualToggle);
		}

		if (json.contains("hint") && json["hint"].is_object()) {
			const auto& hint = json["hint"];
			hintEnabled = hint.value("enabled", hintEnabled);
			hintSeconds = hint.value("seconds", hintSeconds);
			hintScale = hint.value("scale", hintScale);
			hintAnchorX = hint.value("anchorX", hintAnchorX);
			hintAnchorY = hint.value("anchorY", hintAnchorY);
			if (const auto glyphs = hint.value("glyphs", "auto"s); glyphs == "xbox") {
				hintGlyphs = 1;
			} else if (glyphs == "ps") {
				hintGlyphs = 2;
			} else {
				hintGlyphs = 0;
			}
		}

		// A "bindings" object replaces the defaults outright rather than merging, so
		// a hand-written config is exactly what you get.
		if (json.contains("bindings") && json["bindings"].is_object()) {
			bindings.clear();
			for (const auto& [key, value] : json["bindings"].items()) {
				std::uint32_t code = 0;
				try {
					code = static_cast<std::uint32_t>(std::stoul(key));
				} catch (const std::exception&) {
					logger::warn("OPad.json: '{}' is not a gamepad keycode, skipped", key);
					continue;
				}

				if (code < 266 || code > 281) {
					logger::warn("OPad.json: keycode {} is not a gamepad button (266-281), skipped", code);
					continue;
				}

				ButtonBinding binding;
				if (value.is_string()) {
					binding.press = ActionFromName(value.get<std::string>());
				} else if (value.is_object()) {
					binding.press = ActionFromName(value.value("press", "none"s));
					binding.hold = ActionFromName(value.value("hold", "none"s));
				}
				bindings[code] = binding;
			}
		}

		logger::info("OPad.json loaded: {} bindings, hold {:.2f}s, fullLockout {}, blockFirstPerson {} (manual toggle {})",
			bindings.size(), holdSeconds, fullLockout, cameraBlockFirstPerson, cameraAllowManualToggle ? "allowed" : "blocked");
	}
}
