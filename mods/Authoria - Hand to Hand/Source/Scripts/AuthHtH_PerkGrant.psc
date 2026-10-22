Scriptname AuthHtH_PerkGrant extends Quest
{Start-game init for Hand to Hand (Authoria). Grants the hidden XP-driver perk (0x822) to the player
 (idempotent), and on a NEW game sets the starting skill level: 15, or 25 for Khajiit-family races
 (the +10 racial bonus). "New game" is detected by the driver perk being ABSENT the first time OnInit
 runs; existing saves already carry the perk (OnInit does not re-fire on them), so a trained skill is
 never reset and no retroactive racial bonus is applied. The racial level is set only after character
 creation menus close, so the player's chosen race is read (not the pre-chargen default).}

int Property iBaseStart    = 10  Auto
int Property iKhajiitStart  = 20  Auto

Event OnInit()
    Actor pl = Game.GetPlayer()
    Perk driver = Game.GetFormFromFile(0x822, "Authoria - Hand to Hand.esp") as Perk
    ; New game iff the driver perk is not yet present (existing saves already have it).
    bool bNewGame = (driver != None && pl != None && pl.HasPerk(driver) == false)

    GrantDriverPerk()

    if bNewGame
        ; Seed the damage-scaling tracker to an exact 0 for a fresh character.
        GlobalVariable dmg = Game.GetFormFromFile(0x825, "Authoria - Hand to Hand.esp") as GlobalVariable
        if dmg
            dmg.SetValue(0.0)
        endif
        ; Apply the racial starting level once chargen is done.
        RegisterForSingleUpdate(2.0)
    endif
EndEvent

Event OnUpdate()
    ; Wait out character-creation menus so GetRace() returns the CHOSEN race, then set the start level once.
    if Utility.IsInMenuMode()
        RegisterForSingleUpdate(2.0)
        return
    endif
    ApplyStartingLevel()
EndEvent

Function GrantDriverPerk()
    Perk p = Game.GetFormFromFile(0x822, "Authoria - Hand to Hand.esp") as Perk
    Actor pl = Game.GetPlayer()
    if p && pl && pl.HasPerk(p) == false
        pl.AddPerk(p)
    endif
EndFunction

Function ApplyStartingLevel()
    GlobalVariable LevelGlob = Game.GetFormFromFile(0x800, "Authoria - Hand to Hand.esp") as GlobalVariable
    Actor pl = Game.GetPlayer()
    if LevelGlob == None || pl == None
        return
    endif
    int startLevel = iBaseStart
    if IsKhajiitFamily(pl.GetRace())
        startLevel = iKhajiitStart
    endif
    LevelGlob.SetValue(startLevel as float)
EndFunction

bool Function IsKhajiitFamily(Race r)
    if r == None
        return false
    endif
    Race khajiit       = Game.GetFormFromFile(0x013745, "Skyrim.esm") as Race
    Race khajiitVamp    = Game.GetFormFromFile(0x088845, "Skyrim.esm") as Race
    Race halfKhajiit    = Game.GetFormFromFile(0x03322B, "HalfKhajiit.esp") as Race
    Race halfKhajiitVamp = Game.GetFormFromFile(0x05693A, "HalfKhajiit.esp") as Race
    return r == khajiit || r == khajiitVamp || r == halfKhajiit || r == halfKhajiitVamp
EndFunction
