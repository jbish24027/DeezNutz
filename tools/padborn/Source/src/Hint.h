#pragma once

#include "PCH.h"

namespace OPad::Hint
{
	// One-line button hint through the vanilla HUD's tutorial text, shown when a player
	// scene starts. The text carries [UserEvent] tokens; the HUD's own CreateButtonArt
	// resolves each one to the active device's button art (360_*/ps3_* PNGs), so the
	// glyphs always match the real controlmap and the real controller brand.
	void OnSceneStart();
	void OnSceneEnd();
}
