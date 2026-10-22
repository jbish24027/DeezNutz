#pragma once

#include "Config.h"
#include "PCH.h"

#include "ostim/Threading/ThreadInterface.h"

namespace OPad
{
	// Everything OPad needs to know about OStim: whether the player is in a scene,
	// and which keycode each OStim action currently listens on.
	//
	// Scene state comes from OStim's own plugin interface (thread start/stop
	// listeners), not from guessing at menu visibility — OStim's scene menu is
	// registered kAlwaysOpen, so RE::UI::IsMenuOpen would read true forever.
	class OStimBridge : public OStim::ThreadEventListener
	{
	public:
		static OStimBridge& Get();

		// Called on kDataLoaded: resolves OStim.esp's key globals.
		void ResolveGlobals();

		// Called on kPostLoadGame: hands OStim our listeners. Safe to call again.
		void Connect();

		[[nodiscard]] bool SceneActive() const { return _sceneActive; }
		[[nodiscard]] bool Connected() const { return _threadInterface != nullptr; }

		// The DIK scancode OStim is currently listening on for this action, or 0 if
		// the action has no binding / the global could not be resolved.
		[[nodiscard]] std::uint32_t KeyFor(Action a_action) const;

		// OStim ships Search on K (37) and Alignment on L (38). On this load order L
		// is Lights On, so an injected L would toggle the lantern mid-scene. Move
		// both onto free numpad codes that nothing else claims.
		void ReserveKeys();

		// OStim::ThreadEventListener
		void listen(OStim::Thread* a_thread) override;

	private:
		OStimBridge() = default;

		struct StopListener : OStim::ThreadEventListener
		{
			void listen(OStim::Thread* a_thread) override;
		};

		std::unordered_map<Action, RE::TESGlobal*> _globals;
		OStim::ThreadInterface*                    _threadInterface{ nullptr };
		StopListener                               _stopListener;
		bool                                       _sceneActive{ false };

		friend struct StopListener;
		void SetSceneActive(bool a_active);
	};
}
