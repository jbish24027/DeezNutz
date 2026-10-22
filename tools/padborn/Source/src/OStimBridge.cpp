#include "OStimBridge.h"

#include "Overlay.h"

#include "ostim/InterfaceExchangeMessage.h"

namespace OPad
{
	namespace
	{
		constexpr auto kOStimPlugin = "OStim.esp"sv;
		constexpr auto kOStimSKSEName = "OStim";

		// Local FormIDs of OStim.esp's key globals. OStim.esp is a full plugin, so
		// these are stable; the Papyrus properties are thin wrappers over exactly
		// these, which is why reading them gives the live MCM binding.
		struct GlobalEntry
		{
			Action           action;
			RE::FormID       localID;
			std::string_view editorID;  // for logging only
		};

		constexpr std::array kGlobals{
			GlobalEntry{ Action::kUp, 0x000E28, "OStimKeyUp"sv },
			GlobalEntry{ Action::kDown, 0x000E29, "OStimKeyDown"sv },
			GlobalEntry{ Action::kLeft, 0x000E2A, "OStimKeyLeft"sv },
			GlobalEntry{ Action::kRight, 0x000E2B, "OStimKeyRight"sv },
			GlobalEntry{ Action::kYes, 0x000E2C, "OStimKeyYes"sv },
			GlobalEntry{ Action::kEnd, 0x000E2D, "OStimKeyEnd"sv },
			GlobalEntry{ Action::kToggle, 0x000E2E, "OStimKeyToggle"sv },
			GlobalEntry{ Action::kSceneStart, 0x000DE7, "OStimKeySceneStart"sv },
			GlobalEntry{ Action::kSpeedUp, 0x000DE8, "OStimKeySpeedUp"sv },
			GlobalEntry{ Action::kSpeedDown, 0x000DE9, "OStimKeySpeedDown"sv },
			GlobalEntry{ Action::kPullOut, 0x000DEA, "OStimKeyPullOut"sv },
			GlobalEntry{ Action::kAutoMode, 0x000DEB, "OStimKeyAutoMode"sv },
			GlobalEntry{ Action::kFreeCam, 0x000DEC, "OStimKeyFreeCam"sv },
			GlobalEntry{ Action::kSearch, 0x000E41, "OStimKeySearch"sv },
			GlobalEntry{ Action::kAlignment, 0x000DE2, "OStimKeyAlignment"sv },
			GlobalEntry{ Action::kHideUI, 0x000EE9, "OStimKeyHideUI"sv },
		};

		// Free numpad scancodes: OStim's own defaults use every other numpad key, and
		// nothing else on this load order listens on 2/3.
		constexpr float kReservedSearch = 80.0f;     // NumPad2
		constexpr float kReservedAlignment = 81.0f;  // NumPad3
	}

	OStimBridge& OStimBridge::Get()
	{
		static OStimBridge instance;
		return instance;
	}

	void OStimBridge::ResolveGlobals()
	{
		auto* handler = RE::TESDataHandler::GetSingleton();
		if (!handler) {
			logger::error("no TESDataHandler, OPad cannot resolve OStim's keys");
			return;
		}

		_globals.clear();
		for (const auto& entry : kGlobals) {
			auto* global = handler->LookupForm<RE::TESGlobal>(entry.localID, kOStimPlugin);
			if (!global) {
				logger::warn("could not resolve {} ({:06X}:{})", entry.editorID, entry.localID, kOStimPlugin);
				continue;
			}
			_globals[entry.action] = global;
		}

		logger::info("resolved {}/{} OStim key globals", _globals.size(), kGlobals.size());

		if (Config::Get().reserveCollidingKeys) {
			ReserveKeys();
		}
	}

	void OStimBridge::ReserveKeys()
	{
		// OPad drives OStim by injecting the keyboard key OStim listens on. If that
		// key is one another mod also listens on, the other mod fires too — so the
		// two OStim keys that sit on letter keys get moved off them.
		if (auto it = _globals.find(Action::kSearch); it != _globals.end()) {
			if (it->second->value != kReservedSearch) {
				logger::info("moving OStim search key {} -> {} (NumPad2)", it->second->value, kReservedSearch);
				it->second->value = kReservedSearch;
			}
		}
		if (auto it = _globals.find(Action::kAlignment); it != _globals.end()) {
			if (it->second->value != kReservedAlignment) {
				logger::info("moving OStim alignment key {} -> {} (NumPad3)", it->second->value, kReservedAlignment);
				it->second->value = kReservedAlignment;
			}
		}
	}

	std::uint32_t OStimBridge::KeyFor(Action a_action) const
	{
		auto it = _globals.find(a_action);
		if (it == _globals.end() || !it->second) {
			return 0;
		}

		const auto value = it->second->value;
		if (value < 2.0f || value > 281.0f) {
			return 0;
		}
		return static_cast<std::uint32_t>(value);
	}

	void OStimBridge::Connect()
	{
		if (_threadInterface) {
			return;
		}

		OStim::InterfaceExchangeMessage message;
		auto*                           messaging = SKSE::GetMessagingInterface();
		if (!messaging) {
			return;
		}

		messaging->Dispatch(OStim::InterfaceExchangeMessage::MESSAGE_TYPE, &message,
			sizeof(OStim::InterfaceExchangeMessage), kOStimSKSEName);

		if (!message.interfaceMap) {
			logger::error("OStim did not answer the interface exchange — is OStim.dll installed?");
			return;
		}

		_threadInterface = static_cast<OStim::ThreadInterface*>(
			message.interfaceMap->queryInterface(OStim::ThreadInterface::NAME));

		if (!_threadInterface) {
			logger::error("OStim has no '{}' interface", OStim::ThreadInterface::NAME);
			return;
		}

		_threadInterface->registerThreadStartListener(this);
		_threadInterface->registerThreadStopListener(&_stopListener);

		logger::info("connected to OStim thread interface (version {})", _threadInterface->getVersion());
	}

	void OStimBridge::SetSceneActive(bool a_active)
	{
		if (_sceneActive == a_active) {
			return;
		}
		_sceneActive = a_active;
		logger::info("player scene {}", a_active ? "started" : "ended");
		if (a_active) {
			Overlay::OnSceneStart();
		} else {
			Overlay::OnSceneEnd();
		}
	}

	void OStimBridge::listen(OStim::Thread* a_thread)
	{
		if (a_thread && a_thread->isPlayerThread()) {
			Get().SetSceneActive(true);
		}
	}

	void OStimBridge::StopListener::listen(OStim::Thread* a_thread)
	{
		if (a_thread && a_thread->isPlayerThread()) {
			OStimBridge::Get().SetSceneActive(false);
		}
	}
}
