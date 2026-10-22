Scriptname Authoria_PlayerDirtDriver extends ReferenceAlias
{Authoria: paints Dirt and Blood's PLAYER dirt stage onto the player's skin as RaceMenu
overlays (the Zaki UBE set), by POLLING which dirt spell the player currently has.

Why a polling quest alias and not a magic effect: four in-game rounds proved the magic-effect
route silent-fails in this load order (see the mod's README). This driver depends on nothing
but Game.GetFormFromFile + Actor.HasSpell, and traces every decision, so its behaviour is
always visible in the Papyrus log. Mirrors Authoria_WashInit, which works in this same list.}

Float Property PollSeconds = 6.0 Auto
{Seconds between checks. Four HasSpell calls per poll - cheap.}

String Property BodyTextureFemale = "mzin\\Bathe\\Set1\\F\\DirtFXBody.DDS" Auto
String Property BodyTextureMale = "mzin\\Bathe\\Set1\\M\\DirtFXBody.DDS" Auto
String Property FaceTexture = "mzin\\Bathe\\Set1\\F\\DirtFXFace.DDS" Auto
String Property DefaultTexture = "actors\\character\\overlays\\default.dds" Auto

; skee override keys: 0 emissive colour, 1 emissive multiple, 2 glossiness, 3 specular,
; 7 tint colour, 8 alpha, 9 texture (index 0 = diffuse).
Int Property KEY_EMISSIVE_COLOR = 0 AutoReadOnly
Int Property KEY_EMISSIVE_MULT = 1 AutoReadOnly
Int Property KEY_GLOSSINESS = 2 AutoReadOnly
Int Property KEY_SPECULAR = 3 AutoReadOnly
Int Property KEY_TINT_COLOR = 7 AutoReadOnly
Int Property KEY_ALPHA = 8 AutoReadOnly
Int Property KEY_TEXTURE = 9 AutoReadOnly
Int Property TINT_WHITE = 16777215 AutoReadOnly

Int AppliedStage = -1
Bool Announced = False


Event OnInit()
	Startup()
EndEvent

Event OnPlayerLoadGame()
	Startup()
EndEvent

Function Startup()
	AppliedStage = -1
	Announced = False
	Debug.Trace("Authoria_PlayerDirtDriver: STARTUP - polling every " + PollSeconds + "s")
	RegisterForSingleUpdate(3.0)
EndFunction

Event OnUpdate()
	Poll()
	RegisterForSingleUpdate(PollSeconds)
EndEvent


Function Poll()
	Actor player = GetActorReference()
	If !player
		Debug.Trace("Authoria_PlayerDirtDriver: alias has no actor yet")
		Return
	EndIf

	Int stage = CurrentDirtStage(player)

	If !Announced
		Announced = True
		Race r = player.GetRace()
		String rn = "none"
		If r
			rn = r.GetName()
		EndIf
		Debug.Trace("Authoria_PlayerDirtDriver: FIRST POLL - race=" + rn + " isUBE=" + IsUbeRace(player) + " dirtStage=" + stage)
		Census(player)
	EndIf

	If stage == AppliedStage
		Return
	EndIf
	Debug.Trace("Authoria_PlayerDirtDriver: stage " + AppliedStage + " -> " + stage)
	Census(player)

	If !IsUbeRace(player)
		Debug.Trace("Authoria_PlayerDirtDriver: not a UBE race - leaving Dirt and Blood's own visuals alone")
		AppliedStage = stage
		Return
	EndIf

	Bool isFemale = player.GetLeveledActorBase().GetSex() == 1
	If stage == 0
		ClearAll(player, isFemale)
	Else
		String bodyTex = BodyTextureMale
		If isFemale
			bodyTex = BodyTextureFemale
		EndIf
		Float a = AlphaForStage(stage)
		ApplyPart(player, isFemale, "Body", NiOverride.GetNumBodyOverlays(), bodyTex, a)
		ApplyPart(player, isFemale, "Hands", NiOverride.GetNumHandOverlays(), bodyTex, a)
		ApplyPart(player, isFemale, "Feet", NiOverride.GetNumFeetOverlays(), bodyTex, a)
		ApplyPart(player, isFemale, "Face", NiOverride.GetNumFaceOverlays(), FaceTexture, a)
	EndIf
	NiOverride.ApplyNodeOverrides(player)
	AppliedStage = stage
EndFunction


; Names EVERY Dirt and Blood player spell currently held, so the log can identify anything still
; drawing on the player without another guessing round. Blood is deliberately not handled by this
; mod (Zaki Set A ships no blood texture) - if a blood spell shows here, that is the old visual.
Function Census(Actor player)
	Debug.Trace("Authoria_PlayerDirtDriver: SPELLS dirt1=" + Has(player, 0x00000806) \
		+ " dirt2=" + Has(player, 0x00000807) \
		+ " dirt3=" + Has(player, 0x00000808) \
		+ " dirt4=" + Has(player, 0x00000838) \
		+ " | blood1=" + Has(player, 0x00000809) \
		+ " blood2=" + Has(player, 0x0000080A) \
		+ " blood3=" + Has(player, 0x0000080B) \
		+ " blood4=" + Has(player, 0x00000839))
EndFunction

Bool Function Has(Actor player, Int formid)
	Spell s = Game.GetFormFromFile(formid, "Dirt and Blood - Dynamic Visuals.esp") as Spell
	If !s
		Return False
	EndIf
	Return player.HasSpell(s)
EndFunction


Int Function CurrentDirtStage(Actor player)
	Spell s4 = Game.GetFormFromFile(0x00000838, "Dirt and Blood - Dynamic Visuals.esp") as Spell
	If s4 && player.HasSpell(s4)
		Return 4
	EndIf
	Spell s3 = Game.GetFormFromFile(0x00000808, "Dirt and Blood - Dynamic Visuals.esp") as Spell
	If s3 && player.HasSpell(s3)
		Return 3
	EndIf
	Spell s2 = Game.GetFormFromFile(0x00000807, "Dirt and Blood - Dynamic Visuals.esp") as Spell
	If s2 && player.HasSpell(s2)
		Return 2
	EndIf
	Spell s1 = Game.GetFormFromFile(0x00000806, "Dirt and Blood - Dynamic Visuals.esp") as Spell
	If s1 && player.HasSpell(s1)
		Return 1
	EndIf
	Return 0
EndFunction


Float Function AlphaForStage(Int stage)
	If stage <= 1
		Return 0.5
	ElseIf stage == 2
		Return 0.65
	ElseIf stage == 3
		Return 0.8
	EndIf
	Return 1.0
EndFunction


Bool Function IsUbeRace(Actor player)
	Keyword kw = Game.GetFormFromFile(0x00000800, "Ultimate Body Enhancer - Dirt and Blood.esp") as Keyword
	Race r = player.GetRace()
	If !kw || !r
		Return False
	EndIf
	Return r.HasKeyword(kw)
EndFunction


Function ApplyPart(Actor player, Bool isFemale, String area, Int count, String texture, Float alpha)
	Int slot = FindSlot(player, isFemale, area, count)
	If slot < 0
		Debug.Trace("Authoria_PlayerDirtDriver: NO FREE OVERLAY SLOT for " + area + " (" + count + " slots)")
		Return
	EndIf
	String node = area + " [ovl" + slot + "]"
	NiOverride.AddNodeOverrideString(player, isFemale, node, KEY_TEXTURE, 0, texture, true)
	NiOverride.AddNodeOverrideInt(player, isFemale, node, KEY_TINT_COLOR, -1, TINT_WHITE, true)
	NiOverride.AddNodeOverrideInt(player, isFemale, node, KEY_EMISSIVE_COLOR, -1, 0, true)
	NiOverride.AddNodeOverrideFloat(player, isFemale, node, KEY_EMISSIVE_MULT, -1, 1.0, true)
	NiOverride.AddNodeOverrideFloat(player, isFemale, node, KEY_ALPHA, -1, alpha, true)
	NiOverride.AddNodeOverrideFloat(player, isFemale, node, KEY_GLOSSINESS, -1, 0.0, true)
	NiOverride.AddNodeOverrideFloat(player, isFemale, node, KEY_SPECULAR, -1, 0.0, true)
	Debug.Trace("Authoria_PlayerDirtDriver: " + node + " <- " + texture + " @" + alpha)
EndFunction


Function ClearAll(Actor player, Bool isFemale)
	ClearPart(player, isFemale, "Body", NiOverride.GetNumBodyOverlays())
	ClearPart(player, isFemale, "Hands", NiOverride.GetNumHandOverlays())
	ClearPart(player, isFemale, "Feet", NiOverride.GetNumFeetOverlays())
	ClearPart(player, isFemale, "Face", NiOverride.GetNumFaceOverlays())
	Debug.Trace("Authoria_PlayerDirtDriver: cleared (clean)")
EndFunction


Function ClearPart(Actor player, Bool isFemale, String area, Int count)
	Int i = 0
	While i < count
		String node = area + " [ovl" + i + "]"
		If IsOurTexture(NiOverride.GetNodeOverrideString(player, isFemale, node, KEY_TEXTURE, 0))
			NiOverride.AddNodeOverrideString(player, isFemale, node, KEY_TEXTURE, 0, DefaultTexture, true)
			NiOverride.RemoveNodeOverride(player, isFemale, node, KEY_TINT_COLOR, -1)
			NiOverride.RemoveNodeOverride(player, isFemale, node, KEY_EMISSIVE_COLOR, -1)
			NiOverride.RemoveNodeOverride(player, isFemale, node, KEY_EMISSIVE_MULT, -1)
			NiOverride.RemoveNodeOverride(player, isFemale, node, KEY_ALPHA, -1)
			NiOverride.RemoveNodeOverride(player, isFemale, node, KEY_GLOSSINESS, -1)
			NiOverride.RemoveNodeOverride(player, isFemale, node, KEY_SPECULAR, -1)
		EndIf
		i += 1
	EndWhile
EndFunction


; Our own slot wins (so a stage change reuses it); otherwise the highest free slot.
; "Free" = empty OR RaceMenu's blank default - on the player no slot is ever unset.
Int Function FindSlot(Actor player, Bool isFemale, String area, Int count)
	Int free = -1
	Int i = count
	While i > 0
		i -= 1
		String tex = NiOverride.GetNodeOverrideString(player, isFemale, area + " [ovl" + i + "]", KEY_TEXTURE, 0)
		If IsOurTexture(tex)
			Return i
		ElseIf free < 0 && (tex == "" || tex == DefaultTexture)
			free = i
		EndIf
	EndWhile
	Return free
EndFunction


Bool Function IsOurTexture(String texture)
	If texture == ""
		Return False
	EndIf
	Return texture == BodyTextureFemale || texture == BodyTextureMale || texture == FaceTexture
EndFunction
