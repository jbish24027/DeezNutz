#pragma once

#include "PCH.h"

namespace OPad::Camera
{
	// The first-person block (Padborn 2.1.0). Keeps the player camera out of the
	// first-person state no matter who asks: Game.ForceFirstPerson() from any
	// script (First Person Interactions ends every lever pull with one), the
	// vanilla Toggle POV control, zoom-in, camera restores on load, other SKSE
	// plugins. Four layers, cheapest first:
	//
	//   1. PlayerCamera::ForceFirstPerson  - detoured to a no-op.
	//   2. TESCamera::SetState             - a request for the player camera's
	//                                        FirstPersonState is redirected to
	//                                        ThirdPersonState (dropped when the
	//                                        camera is already there).
	//   3. TogglePOVHandler::ProcessButton - swallowed, unless camera.allowManualToggle
	//                                        lets the vanilla POV control through
	//                                        (its switch then passes layers 1-2).
	//   4. PlayerCamera::Update            - per-frame watchdog: first person found
	//                                        anyway -> ForceThirdPerson before the
	//                                        camera updates.
	//
	// Config: Padborn.json "camera": { "blockFirstPerson", "allowManualToggle" }.
	// Installed once at plugin load; nothing is written to disk.
	void Install();
}
