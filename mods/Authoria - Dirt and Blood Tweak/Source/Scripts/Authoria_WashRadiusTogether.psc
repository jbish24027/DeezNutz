Scriptname Authoria_WashRadiusTogether extends ActiveMagicEffect

; Authoria - Wash Together (Player + Followers)
; Radius-based follower washing + player self-wash using Dirt and Blood spells
; Requires: Dirt and Blood, PO3 Papyrus Extender

import PO3_SKSEFunctions

Event OnEffectStart(Actor akTarget, Actor akCaster)
    Actor player = Game.GetPlayer()
    Faction FollowerFaction = Game.GetFormFromFile(0x0005C84E, "Skyrim.esm") as Faction
    Spell washNPC = Game.GetFormFromFile(0x00000860, "Dirt and Blood - Dynamic Visuals.esp") as Spell
    Spell washPlayer = Game.GetFormFromFile(0x0000082F, "Dirt and Blood - Dynamic Visuals.esp") as Spell

    if !washNPC || !washPlayer
        Debug.Notification("[Authoria] Dirt and Blood not found!")
        return
    endIf

    if !FollowerFaction
        Debug.Notification("[Authoria] Could not resolve follower faction!")
        return
    endIf

    if !CanPlayerBathe(player)
        return
    endIf

    Keyword ActorTypeNPC = Game.GetFormFromFile(0x00013794, "Skyrim.esm") as Keyword
    ObjectReference[] actors = FindAllReferencesWithKeyword(player, ActorTypeNPC, 512.0, true)

    int count = 0
    int i = actors.Length
    while i > 0
        i -= 1
        Actor follower = actors[i] as Actor
        if IsEligibleFollower(follower, FollowerFaction)
            washNPC.Cast(player, follower)
            count += 1
        endIf
    endWhile

    washPlayer.Cast(player)

    if count > 0
        Debug.Notification("Washed you and " + count + " follower(s)")
    else
        Debug.Notification("Washed you (no eligible followers nearby)")
    endIf
EndEvent

bool Function CanPlayerBathe(Actor player)
    if player.IsInCombat()
        ShowDirtAndBloodMessage(0x00000851)
        return false
    endIf

    if player.IsWeaponDrawn()
        ShowDirtAndBloodMessage(0x00000850)
        return false
    endIf

    GlobalVariable soapRequired = Game.GetFormFromFile(0x0000082D, "Dirt and Blood - Dynamic Visuals.esp") as GlobalVariable
    if soapRequired && soapRequired.GetValue() == 1
        FormList soaps = Game.GetFormFromFile(0x0000085B, "Dirt and Blood - Dynamic Visuals.esp") as FormList
        if !soaps || !FindFirstItemInList(player, soaps)
            ShowDirtAndBloodMessage(0x00000852)
            return false
        endIf
    endIf

    GlobalVariable waterRequired = Game.GetFormFromFile(0x0000086A, "Dirt and Blood - Dynamic Visuals.esp") as GlobalVariable
    if waterRequired && waterRequired.GetValue() == 1 && !HasValidBathingWater(player)
        ShowDirtAndBloodMessage(0x0000086B)
        return false
    endIf

    return true
EndFunction

bool Function HasValidBathingWater(Actor player)
    Spell wadeInWater1 = Game.GetFormFromFile(0x00000D64, "WadeInWater.esp") as Spell
    Spell wadeInWater2 = Game.GetFormFromFile(0x00000D65, "WadeInWater.esp") as Spell

    if (wadeInWater1 && player.HasSpell(wadeInWater1)) || (wadeInWater2 && player.HasSpell(wadeInWater2))
        return true
    endIf

    ObjectReference staticItem
    FormList waterfalls = Game.GetFormFromFile(0x0000086C, "Dirt and Blood - Dynamic Visuals.esp") as FormList
    if waterfalls
        staticItem = Game.FindClosestReferenceOfAnyTypeInList(waterfalls, player.GetPositionX(), player.GetPositionY(), player.GetPositionZ() + 256, 312.0)
    endIf

    if !staticItem
        waterfalls = Game.GetFormFromFile(0x0000086D, "Dirt and Blood - Dynamic Visuals.esp") as FormList
        if waterfalls
            staticItem = Game.FindClosestReferenceOfAnyTypeInList(waterfalls, player.GetPositionX(), player.GetPositionY(), player.GetPositionZ() + 512, 512.0)
        endIf
    endIf

    if !staticItem
        waterfalls = Game.GetFormFromFile(0x0000086E, "Dirt and Blood - Dynamic Visuals.esp") as FormList
        if waterfalls
            staticItem = Game.FindClosestReferenceOfAnyTypeInList(waterfalls, player.GetPositionX(), player.GetPositionY(), player.GetPositionZ() + 2048, 1000.0)
        endIf
    endIf

    if !staticItem
        waterfalls = Game.GetFormFromFile(0x0000086F, "Dirt and Blood - Dynamic Visuals.esp") as FormList
        if waterfalls
            staticItem = Game.FindClosestReferenceOfAnyTypeInList(waterfalls, player.GetPositionX(), player.GetPositionY(), player.GetPositionZ() + 4096, 1000.0)
        endIf
    endIf

    return staticItem != None
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
