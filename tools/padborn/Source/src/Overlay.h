#pragma once

#include "PCH.h"

namespace OPad::Overlay
{
	// ImGui glyph bar drawn over the game while an OStim player scene runs.
	// Replaces the vanilla ShowTutorialHintText toast (rejected: too big, timed out
	// mid-scene). Persistent for the whole scene, sized/positioned per config.

	// Writes the two render hooks (D3D init + DXGI present). Must run inside
	// SKSEPluginLoad, after SKSE::AllocTrampoline — the D3D init hook has to be in
	// place before the renderer comes up.
	void Install();

	// Scene lifecycle, called by OStimBridge on the OStim listener thread.
	void OnSceneStart();
	void OnSceneEnd();

	// The Back button's hideUI action also hides this bar, so "hide UI" means all of it.
	void NotifyHideUI();
}
