#pragma once

// Knowing whether Auto Combat (Nexus 195681, AutoCombat.dll) is currently fighting
// for the player. AutoCombat.dll exports nothing but the SKSE triad and registers no
// Papyrus API or mod event, so there are two ways in:
//
//  1. Memory (preferred, exact): AutoCombat keeps two atomic bool flags in its .data
//     section - "Enabled" (flipped by its hotkey / menu checkbox) and "auto-pilot
//     active" (set while it is driving the player at a target, cleared by
//     Manager::ReleaseControl). Their addresses are located at runtime by following
//     the code that references Auto Combat's own UI strings ("Auto-pilot is active.",
//     "auto-pilot turned off", "Auto Combat: ON"), so no build-specific offset is
//     hard-coded. The flags are only ever READ.
//  2. Hotkey mirror (fallback when the scan does not validate): watch the same key
//     through the game's own input event sink (BSInputDeviceManager), starting from
//     AutoCombat.ini's Enabled= value. Can drift if Auto Combat is toggled from its
//     SKSE Menu Framework page instead of the key.
namespace ACD::AutoCombat
{
	enum class Link
	{
		kNone,     // AutoCombat.dll not loaded
		kMemory,   // flags located
		kMirror    // hotkey mirror
	};

	void Init();                 // kPostLoad: find the module and scan it
	void RegisterInputSink();    // kInputLoaded: mirror sink (always registered; cheap)
	void ResetMirror();          // on game load: mirror back to the ini's Enabled=

	[[nodiscard]] Link LinkType();
	[[nodiscard]] bool IsEnabled();       // Auto Combat switched on
	[[nodiscard]] bool IsPilotActive();   // Auto Combat is currently driving the player (memory link only)
	[[nodiscard]] const char* LinkName();
}
