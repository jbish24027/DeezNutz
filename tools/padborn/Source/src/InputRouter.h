#pragma once

#include "Config.h"
#include "PCH.h"

namespace OPad
{
	// Sits on the call BSInputDeviceManager::PollInputDevices makes to the input
	// event dispatcher, which runs before every BSTEventSink<InputEvent*> in the
	// game — OStim's, Wheeler's, TK Dodge's, TDM's, and SKSE's Papyrus bridge that
	// feeds Gamepad++. Being upstream of all of them is what makes the lockout total.
	//
	// While a player scene is running, each gamepad button event is rewritten in
	// place into a keyboard event carrying the keycode OStim listens on, with its
	// userEvent blanked so vanilla controls (favorites hotkeys, jump, activate)
	// don't fire either. Buttons with no binding are rewritten to an inert keycode.
	// Everything is restored after the dispatch, so the engine's own event objects
	// come back untouched.
	class InputRouter
	{
	public:
		static InputRouter& Get();

		void Install();

	private:
		InputRouter() = default;

		struct DispatchHook
		{
			static void thunk(RE::BSTEventSource<RE::InputEvent*>* a_dispatcher, RE::InputEvent* const* a_events);

			static inline REL::Relocation<decltype(thunk)> func;

			// BSInputDeviceManager::PollInputDevices -> the dispatch call
			static inline constexpr auto id = REL::RelocationID(67315, 68617);
			static inline constexpr auto offset = REL::VariantOffset(0x7B, 0x7B, 0x7B);
		};

		struct SavedEvent
		{
			RE::ButtonEvent*  event;
			RE::INPUT_DEVICE  device;
			std::uint32_t     idCode;
			RE::BSFixedString userEvent;
		};

		struct ButtonState
		{
			bool holdFired{ false };
			bool pressPending{ false };
		};

		void Route(RE::BSTEventSource<RE::InputEvent*>* a_dispatcher, RE::InputEvent* const* a_events);

		// Grabs a reusable ButtonEvent we own for the lifetime of the process, so the
		// game never frees an event it did not allocate.
		RE::ButtonEvent* BorrowSynthetic(std::uint32_t a_keyCode);
		void             ReleaseSynthetics();

		std::unordered_map<std::uint32_t, ButtonState> _buttons;
		std::vector<SavedEvent>                        _saved;
		std::vector<RE::ButtonEvent*>                  _pending;
		std::vector<RE::ButtonEvent*>                  _pool;
		std::size_t                                    _poolInUse{ 0 };
		bool                                           _installed{ false };
	};

	// OStim's own mask -> keycode table, mirrored so OPad reads gamepad buttons the
	// same way OStim does. See OStimNG skse/src/Util.cpp gamepadMaskToKeyCode.
	[[nodiscard]] std::uint32_t GamepadMaskToKeyCode(std::uint32_t a_mask);
}
