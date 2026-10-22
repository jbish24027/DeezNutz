#pragma once

// The dodge engine. Runs once per frame on the main thread from a PlayerCharacter::Update
// vtable hook (Address Library vtable ID, slot 0xAD), watches hostile actors around the
// player and fires TK Dodge RE's own animation events when one winds up an attack.
namespace ACD::Dodge
{
	void InstallHook();   // SKSEPlugin_Load
	void OnDataLoaded();  // resolve the TK Dodge perk-lock perk
	void Reset();         // new game / game loaded
}
