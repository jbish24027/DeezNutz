#include "InputRouter.h"

#include "OStimBridge.h"
#include "Overlay.h"

namespace stl
{
	using namespace SKSE::stl;

	template <class T>
	void write_thunk_call()
	{
		auto&                                 trampoline = SKSE::GetTrampoline();
		const REL::Relocation<std::uintptr_t> hook{ T::id, T::offset };
		T::func = trampoline.write_call<5>(hook.address(), T::thunk);
	}
}

namespace OPad
{
	namespace
	{
		// OStim's guard rejects anything outside 2..281, so a button rewritten to this
		// reaches every sink downstream and moves nothing.
		constexpr std::uint32_t kInertKeyCode = 0;

		constexpr std::size_t kSyntheticPoolSize = 4;

		const RE::BSFixedString kNoUserEvent{ "" };
	}

	std::uint32_t GamepadMaskToKeyCode(std::uint32_t a_mask)
	{
		switch (a_mask) {
		case 0x1:
			return 266;  // DPAD_UP
		case 0x2:
			return 267;  // DPAD_DOWN
		case 0x4:
			return 268;  // DPAD_LEFT
		case 0x8:
			return 269;  // DPAD_RIGHT
		case 0x10:
			return 270;  // Start
		case 0x20:
			return 271;  // Back
		case 0x40:
			return 272;  // L3
		case 0x80:
			return 273;  // R3
		case 0x100:
			return 274;  // LB
		case 0x200:
			return 275;  // RB
		case 0x1000:
			return 276;  // A
		case 0x2000:
			return 277;  // B
		case 0x4000:
			return 278;  // X
		case 0x8000:
			return 279;  // Y
		case 0x9:
			return 280;  // LT
		case 0xA:
			return 281;  // RT
		default:
			return 282;  // invalid
		}
	}

	InputRouter& InputRouter::Get()
	{
		static InputRouter instance;
		return instance;
	}

	void InputRouter::Install()
	{
		if (_installed) {
			return;
		}

		// Trampoline pool is allocated once in SKSEPluginLoad (plugin.cpp) — a second
		// AllocTrampoline here would replace the pool the render hooks live in.
		stl::write_thunk_call<DispatchHook>();

		_pool.reserve(kSyntheticPoolSize);
		_pending.reserve(kSyntheticPoolSize);
		for (std::size_t i = 0; i < kSyntheticPoolSize; ++i) {
			auto* event = RE::ButtonEvent::Create(RE::INPUT_DEVICE::kKeyboard, kNoUserEvent, kInertKeyCode, 1.0f, 0.0f);
			if (!event) {
				logger::error("could not allocate synthetic button event {}", i);
				break;
			}
			_pool.push_back(event);
		}

		_installed = true;
		logger::info("input dispatch hook installed, {} synthetic events pooled", _pool.size());
	}

	RE::ButtonEvent* InputRouter::BorrowSynthetic(std::uint32_t a_keyCode)
	{
		if (_poolInUse >= _pool.size()) {
			return nullptr;
		}

		auto* event = _pool[_poolInUse++];
		event->device = RE::INPUT_DEVICE::kKeyboard;
		event->eventType = RE::INPUT_EVENT_TYPE::kButton;
		event->userEvent = kNoUserEvent;
		event->idCode = a_keyCode;
		event->value = 1.0f;
		event->heldDownSecs = 0.0f;  // OStim only reacts to IsDown()
		event->next = nullptr;
		return event;
	}

	void InputRouter::ReleaseSynthetics()
	{
		for (std::size_t i = 0; i < _poolInUse; ++i) {
			_pool[i]->next = nullptr;
		}
		_poolInUse = 0;
	}

	void InputRouter::DispatchHook::thunk(RE::BSTEventSource<RE::InputEvent*>* a_dispatcher, RE::InputEvent* const* a_events)
	{
		if (!a_events || !*a_events || !OStimBridge::Get().SceneActive()) {
			func(a_dispatcher, a_events);
			return;
		}

		InputRouter::Get().Route(a_dispatcher, a_events);
	}

	void InputRouter::Route(RE::BSTEventSource<RE::InputEvent*>* a_dispatcher, RE::InputEvent* const* a_events)
	{
		const auto& config = Config::Get();
		auto&       bridge = OStimBridge::Get();

		_saved.clear();
		ReleaseSynthetics();

		_pending.clear();
		RE::InputEvent*               engineTail = nullptr;

		// Pass 1 — rewrite the engine's own events in place. Nothing is linked yet, so
		// the walk only ever sees events the engine put there.
		for (RE::InputEvent* event = *a_events; event; event = event->next) {
			engineTail = event;

			if (event->GetEventType() != RE::INPUT_EVENT_TYPE::kButton ||
				event->GetDevice() != RE::INPUT_DEVICE::kGamepad) {
				continue;  // keyboard, mouse and thumbstick pass straight through
			}

			auto* button = event->AsButtonEvent();
			if (!button) {
				continue;
			}

			const auto code = GamepadMaskToKeyCode(button->GetIDCode());
			if (code > 281) {
				continue;
			}

			const auto bindingIt = config.bindings.find(code);
			const bool bound = bindingIt != config.bindings.end();

			if (!bound && !config.fullLockout) {
				continue;  // unbound button keeps behaving normally
			}

			_saved.push_back({ button, button->GetDevice(), button->GetIDCode(), button->QUserEvent() });

			// Whatever this button ends up meaning, no other mod sees a gamepad press,
			// and a blank userEvent keeps vanilla controls out of it too.
			button->device = RE::INPUT_DEVICE::kKeyboard;
			button->userEvent = kNoUserEvent;
			button->idCode = kInertKeyCode;

			if (!bound) {
				continue;
			}

			const auto& binding = bindingIt->second;
			auto&       state = _buttons[code];

			if (binding.hold == Action::kNone) {
				// Press-only button: rewritten in place, so it costs nothing in latency
				// and allocates nothing. The keycode is carried on the held and up
				// frames too, so downstream listeners see a complete key press rather
				// than a down with no matching up.
				if (binding.press != Action::kNone) {
					const auto key = bridge.KeyFor(binding.press);
					if (key != 0) {
						button->idCode = key;
						if (button->IsDown() && binding.press == Action::kHideUI) {
							// "hide UI" should hide the glyph bar too.
							Overlay::NotifyHideUI();
						}
						if (config.logInput && button->IsDown()) {
							logger::info("pad {} -> {} (key {})", code, ActionName(binding.press), key);
						}
					}
				}
				continue;
			}

			// The button also carries a hold action, so a press can only be resolved on
			// release — until then we don't know which the user meant.
			if (button->IsDown()) {
				state.holdFired = false;
				state.pressPending = binding.press != Action::kNone;
			} else if (button->IsHeld()) {
				if (!state.holdFired && button->HeldDuration() >= config.holdSeconds) {
					state.holdFired = true;
					state.pressPending = false;
					if (const auto key = bridge.KeyFor(binding.hold); key != 0) {
						if (auto* synthetic = BorrowSynthetic(key)) {
							_pending.push_back(synthetic);
							if (config.logInput) {
								logger::info("pad {} held -> {} (key {})", code, ActionName(binding.hold), key);
							}
						}
					}
				}
			} else if (button->IsUp()) {
				if (state.pressPending && !state.holdFired) {
					if (const auto key = bridge.KeyFor(binding.press); key != 0) {
						if (auto* synthetic = BorrowSynthetic(key)) {
							_pending.push_back(synthetic);
							if (config.logInput) {
								logger::info("pad {} tapped -> {} (key {})", code, ActionName(binding.press), key);
							}
						}
					}
				}
				state.pressPending = false;
				state.holdFired = false;
			}
		}

		// Pass 2 — append our own events, which OPad owns for the life of the process,
		// so the game never frees an event it did not allocate.
		RE::InputEvent* tailOriginalNext = nullptr;
		if (engineTail && !_pending.empty()) {
			tailOriginalNext = engineTail->next;
			RE::InputEvent* cursor = engineTail;
			for (auto* synthetic : _pending) {
				cursor->next = synthetic;
				cursor = synthetic;
			}
			cursor->next = nullptr;
		}

		DispatchHook::func(a_dispatcher, a_events);

		// Pass 3 — hand the engine back exactly the chain it gave us.
		if (engineTail && !_pending.empty()) {
			engineTail->next = tailOriginalNext;
		}

		for (const auto& saved : _saved) {
			saved.event->device = saved.device;
			saved.event->idCode = saved.idCode;
			saved.event->userEvent = saved.userEvent;
		}

		_saved.clear();
		ReleaseSynthetics();
	}
}
