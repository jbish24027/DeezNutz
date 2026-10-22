#pragma once

#include "PCH.h"

namespace OPad::Sprint
{
	// The Padborn sprint rescue, folded in from PadbornSprint 1.2.1-diag.
	//
	// Classic Sprinting Redone makes sprint hold-to-run and is deliberately
	// LEVEL-triggered — its SprintHandler vtable hook re-fires sprint on every held
	// frame, so a hold "catches up" once the player is actually moving. TK Dodge RE
	// Addon re-hooks the same handler at save load, forwards only the press-down
	// frame, and eats the held frames — which turns sprint into an accidentally
	// EDGE-triggered control: a press that lands before the stick is at running
	// speed is lost for the whole hold.
	//
	// This sink restores the catch-up from outside the contested vtable slot,
	// re-setting the sprint flag while the sprint control has been held long enough.
	// It tracks hold duration itself, because on the pad the sprint ButtonEvent
	// arrives as a fresh DOWN nearly every frame (HeldDuration useless).
	//
	// Registers at kInputLoaded when config sprint.enabled is true. Not device
	// filtered: any sprint press whose held frames get eaten is rescued, keyboard
	// included.
	void Register();

	// Moves the gamepad Sprint control to the configured button (sprint.button:
	// b / lb / ls) by swapping mappings inside the live ControlMap — the event that
	// held the target button gets Sprint's old button. Nothing is written to disk,
	// so no controlmap file and no CCS reinstall is involved; reapplied every load.
	// Call at kDataLoaded and on kPostLoadGame.
	void ApplyButton();
}
