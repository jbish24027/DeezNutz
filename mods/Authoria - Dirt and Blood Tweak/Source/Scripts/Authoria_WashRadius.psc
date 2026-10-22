Scriptname Authoria_WashRadius extends ActiveMagicEffect

; Authoria - Wash Followers
; Radius-based follower washing using Dirt and Blood spells
; Requires: Dirt and Blood, PO3 Papyrus Extender
;
; ARR gating rules:
;   - The PLAYER is the only one who must carry soap (when Dirt and Blood's
;     "Soap is Required for Baths" setting is on). Checked once, up front.
;   - Each FOLLOWER must individually be standing in water (when the
;     "Water Required For Bathing" setting is on). Checked per-follower in the loop.

import PO3_SKSEFunctions

Event OnEffectStart(Actor akTarget, Actor akCaster)
    Actor player = Game.GetPlayer()
    Faction FollowerFaction = Game.GetFormFromFile(0x0005C84E, "Skyrim.esm") as Faction
    Spell washNPC = Game.GetFormFromFile(0x00000860, "Dirt and Blood - Dynamic Visuals.esp") as Spell

    if !washNPC
        Debug.Notification("[Authoria] Dirt and Blood not found!")
        return
    endIf

    if !FollowerFaction
        Debug.Notification("[Authoria] Could not resolve follower faction!")
        return
    endIf

    ; Player is the only one who needs soap in their inventory.
    if !PlayerHasSoap(player)
        return
    endIf

    ; Is per-follower water required? (Dirt and Blood auto-disables this setting
    ; when Wade in Water isn't installed, so an off value means "no water needed".)
    GlobalVariable waterRequired = Game.GetFormFromFile(0x0000086A, "Dirt and Blood - Dynamic Visuals.esp") as GlobalVariable
    bool requireWater = waterRequired && waterRequired.GetValue() == 1

    Keyword ActorTypeNPC = Game.GetFormFromFile(0x00013794, "Skyrim.esm") as Keyword
    ObjectReference[] actors = FindAllReferencesWithKeyword(player, ActorTypeNPC, 512.0, true)

    int washed = 0
    int dry = 0
    int i = actors.Length
    while i > 0
        i -= 1
        Actor follower = actors[i] as Actor
        if IsEligibleFollower(follower, FollowerFaction)
            if requireWater && !IsActorInWater(follower)
                dry += 1
            else
                washNPC.Cast(player, follower)
                washed += 1
            endIf
        endIf
    endWhile

    if washed > 0
        Debug.Notification("Washed " + washed + " follower(s)")
    elseif dry > 0
        Debug.Notification("Followers must be standing in water to wash")
    else
        Debug.Notification("No eligible followers nearby to wash")
    endIf
EndEvent

bool Function PlayerHasSoap(Actor player)
    GlobalVariable soapRequired = Game.GetFormFromFile(0x0000082D, "Dirt and Blood - Dynamic Visuals.esp") as GlobalVariable
    if soapRequired && soapRequired.GetValue() == 1
        FormList soaps = Game.GetFormFromFile(0x0000085B, "Dirt and Blood - Dynamic Visuals.esp") as FormList
        if !soaps || !FindFirstItemInList(player, soaps)
            ShowDirtAndBloodMessage(0x00000852)
            return false
        endIf
    endIf
    return true
EndFunction

bool Function IsEligibleFollower(Actor follower, Faction followerFaction)
    if !follower
        return false
    endIf

    if follower.IsDead() || follower.IsInCombat() || follower.IsWeaponDrawn()
        return false
    endIf

    return follower.IsInFaction(followerFaction) || follower.IsPlayerTeammate()
EndFunction

Function ShowDirtAndBloodMessage(int localFormId)
    Message failureMessage = Game.GetFormFromFile(localFormId, "Dirt and Blood - Dynamic Visuals.esp") as Message
    if failureMessage
        failureMessage.Show()
    endIf
EndFunction
