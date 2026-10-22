#include "Camera.h"
#include "Config.h"

#ifndef WIN32_LEAN_AND_MEAN
#	define WIN32_LEAN_AND_MEAN
#endif
#ifndef NOMINMAX
#	define NOMINMAX
#endif
#include <Windows.h>

#if __has_include(<detours/detours.h>)
#	include <detours/detours.h>
#else
#	include <detours.h>
#endif

#include <atomic>

namespace OPad::Camera
{
	namespace
	{
		using ForceFirstPerson_t = void(RE::PlayerCamera*);
		using SetState_t = void(RE::TESCamera*, RE::TESCameraState*);
		using ProcessButton_t = void(RE::TogglePOVHandler*, RE::ButtonEvent*, RE::PlayerControlsData*);
		using Update_t = void(RE::PlayerCamera*);

		// Detours targets: the pointer is rewritten to the trampoline on commit.
		ForceFirstPerson_t* g_origForceFirstPerson{ nullptr };
		SetState_t*         g_origSetState{ nullptr };

		// vtable hooks
		REL::Relocation<ProcessButton_t*> g_origProcessButton;
		REL::Relocation<Update_t*>        g_origUpdate;

		// Set while the vanilla Toggle POV handler runs, so layers 1-2 can tell a
		// manual switch from a forced one when camera.allowManualToggle is on.
		thread_local bool t_manualToggle{ false };

		std::atomic<std::uint32_t> g_blockedForce{ 0 };
		std::atomic<std::uint32_t> g_blockedState{ 0 };
		std::atomic<std::uint32_t> g_corrected{ 0 };

		[[nodiscard]] bool Blocking()
		{
			const auto& cfg = Config::Get();
			return cfg.cameraBlockFirstPerson && !(cfg.cameraAllowManualToggle && t_manualToggle);
		}

		// A script stuck in a loop could call ForceFirstPerson every frame; log the
		// first few and then a heartbeat.
		[[nodiscard]] bool ShouldLog(std::uint32_t a_n)
		{
			return a_n <= 20 || (a_n % 500) == 0;
		}

		[[nodiscard]] RE::TESCameraState* StateOf(RE::PlayerCamera* a_camera, RE::CameraState a_state)
		{
			return a_camera ? a_camera->GetRuntimeData().cameraStates[a_state].get() : nullptr;
		}

		// Layer 1
		void Hook_ForceFirstPerson(RE::PlayerCamera* a_this)
		{
			if (Blocking()) {
				const auto n = ++g_blockedForce;
				if (ShouldLog(n)) {
					logger::info("camera: ForceFirstPerson blocked (#{})", n);
				}
				return;
			}
			g_origForceFirstPerson(a_this);
		}

		// Layer 2
		void Hook_SetState(RE::TESCamera* a_this, RE::TESCameraState* a_state)
		{
			if (a_state && Blocking()) {
				auto* camera = RE::PlayerCamera::GetSingleton();
				if (camera && a_this == camera && a_state == StateOf(camera, RE::CameraState::kFirstPerson)) {
					auto*      third = StateOf(camera, RE::CameraState::kThirdPerson);
					const auto n = ++g_blockedState;
					if (!third || camera->currentState.get() == third) {
						if (ShouldLog(n)) {
							logger::info("camera: first-person state request dropped (#{})", n);
						}
						return;
					}
					if (ShouldLog(n)) {
						logger::info("camera: first-person state request redirected to third person (#{})", n);
					}
					a_state = third;
				}
			}
			g_origSetState(a_this, a_state);
		}

		// Layer 3
		void Hook_ProcessButton(RE::TogglePOVHandler* a_this, RE::ButtonEvent* a_event, RE::PlayerControlsData* a_data)
		{
			const auto& cfg = Config::Get();
			if (cfg.cameraBlockFirstPerson && !cfg.cameraAllowManualToggle) {
				// Nothing to toggle to. The vanilla hold-to-rotate rides the same
				// control and goes with it; the free camera rotate on the right stick
				// is untouched.
				return;
			}
			t_manualToggle = true;
			g_origProcessButton(a_this, a_event, a_data);
			t_manualToggle = false;
		}

		// Layer 4
		void Hook_Update(RE::PlayerCamera* a_this)
		{
			const auto& cfg = Config::Get();
			if (cfg.cameraBlockFirstPerson && !cfg.cameraAllowManualToggle && a_this && a_this->IsInFirstPerson()) {
				const auto n = ++g_corrected;
				if (ShouldLog(n)) {
					logger::info("camera: camera found in first person, forcing third person (#{})", n);
				}
				a_this->ForceThirdPerson();
			}
			g_origUpdate(a_this);
		}
	}

	void Install()
	{
		const auto& cfg = Config::Get();
		if (!cfg.cameraBlockFirstPerson) {
			logger::info("camera: first-person block is off (camera.blockFirstPerson = false)");
			return;
		}
		if (REL::Module::IsVR()) {
			logger::warn("camera: VR runtime, first-person block not installed");
			return;
		}

		const REL::Relocation<std::uintptr_t> forceFirst{ REL::RelocationID(49858, 50790) };
		const REL::Relocation<std::uintptr_t> setState{ REL::RelocationID(32290, 33026) };
		g_origForceFirstPerson = reinterpret_cast<ForceFirstPerson_t*>(forceFirst.address());
		g_origSetState = reinterpret_cast<SetState_t*>(setState.address());

		DetourTransactionBegin();
		DetourUpdateThread(GetCurrentThread());
		DetourAttach(reinterpret_cast<PVOID*>(&g_origForceFirstPerson), reinterpret_cast<PVOID>(&Hook_ForceFirstPerson));
		DetourAttach(reinterpret_cast<PVOID*>(&g_origSetState), reinterpret_cast<PVOID>(&Hook_SetState));
		if (const auto err = DetourTransactionCommit(); err != NO_ERROR) {
			logger::error("camera: Detours commit failed ({}), first-person block NOT installed", err);
			return;
		}

		REL::Relocation<std::uintptr_t> povVtbl{ RE::VTABLE_TogglePOVHandler[0] };
		g_origProcessButton = povVtbl.write_vfunc(0x4, Hook_ProcessButton);

		REL::Relocation<std::uintptr_t> cameraVtbl{ RE::VTABLE_PlayerCamera[0] };
		g_origUpdate = cameraVtbl.write_vfunc(0x2, Hook_Update);

		logger::info("camera: first-person block installed - ForceFirstPerson no-op, SetState redirect, Toggle POV {}, per-frame watchdog",
			cfg.cameraAllowManualToggle ? "passed through (manual toggle allowed)" : "swallowed");
	}
}
