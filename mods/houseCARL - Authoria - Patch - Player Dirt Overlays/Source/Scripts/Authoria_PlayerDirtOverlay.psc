Scriptname Authoria_PlayerDirtOverlay extends ActiveMagicEffect
{Authoria bridge: shows Dirt and Blood's player dirt stage as RaceMenu skin overlays
(the Zaki UBE set) instead of the baked UBE effect shader. One instance per dirt stage,
attached to Authoria_Dirty_Effect_Dirt1..4_PlayerOvl. NPCs are never touched.

Node names, free-slot detection and the shader-key stack follow the two working overlay
implementations already in this load order (UBE Wounds, OCum Ascended): the overlay nodes
are lowercase "Body [ovl0]" style, and on the PLAYER every slot already carries
actors\character\overlays\default.dds - so a slot counts as free when its texture is
empty OR that default, never by "has no override".}

Int Property Stage = 1 Auto
{Dirt and Blood stage this effect represents (1-4).}

Float Property OverlayAlpha = 1.0 Auto
{Overlay opacity for this stage, 0.0 - 1.0.}

GlobalVariable Property StageGlobal Auto
{Authoria_PlayerDirtStage: the stage whose overlay is on the player right now (0 = none).}

String Property BodyTextureFemale = "mzin\\Bathe\\Set1\\F\\DirtFXBody.DDS" Auto
{Relative to Data\Textures. Used for Body, Hands and Feet (UBE shares one skin layout).}

String Property BodyTextureMale = "mzin\\Bathe\\Set1\\M\\DirtFXBody.DDS" Auto
{Relative to Data\Textures. Used for Body, Hands and Feet.}

String Property FaceTexture = "mzin\\Bathe\\Set1\\F\\DirtFXFace.DDS" Auto
{Relative to Data\Textures. Same file for both sexes.}

String Property DefaultTexture = "actors\\character\\overlays\\default.dds" Auto
{RaceMenu's blank overlay texture - what an unused slot carries, and what we restore.}

; skee override keys (RaceMenu): 0 emissive colour, 1 emissive multiple, 2 glossiness,
; 3 specular strength, 7 tint colour, 8 alpha, 9 texture (index 0 = diffuse).
Int Property KEY_EMISSIVE_COLOR = 0 AutoReadOnly
Int Property KEY_EMISSIVE_MULT = 1 AutoReadOnly
Int Property KEY_GLOSSINESS = 2 AutoReadOnly
Int Property KEY_SPECULAR = 3 AutoReadOnly
Int Property KEY_TINT_COLOR = 7 AutoReadOnly
Int Property KEY_ALPHA = 8 AutoReadOnly
Int Property KEY_TEXTURE = 9 AutoReadOnly
Int Property TINT_WHITE = 16777215 AutoReadOnly


Event OnEffectStart(Actor akTarget, Actor akCaster)
	; traced BEFORE the guard so the log always proves the effect fired at all
	Debug.Trace("Authoria_PlayerDirtOverlay: OnEffectStart stage " + Stage + " target=" + akTarget)
	If akTarget != Game.GetPlayer()
		Debug.Trace("Authoria_PlayerDirtOverlay: target is not the player - ignoring")
		Return
	EndIf
	Bool isFemale = akTarget.GetLeveledActorBase().GetSex() == 1
	String bodyTex = BodyTextureMale
	If isFemale
		bodyTex = BodyTextureFemale
	EndIf
	Debug.Trace("Authoria_PlayerDirtOverlay: applying stage " + Stage + " alpha " + OverlayAlpha + " female=" + isFemale)
	ApplyPart(akTarget, isFemale, "Body", NiOverride.GetNumBodyOverlays(), bodyTex)
	ApplyPart(akTarget, isFemale, "Hands", NiOverride.GetNumHandOverlays(), bodyTex)
	ApplyPart(akTarget, isFemale, "Feet", NiOverride.GetNumFeetOverlays(), bodyTex)
	ApplyPart(akTarget, isFemale, "Face", NiOverride.GetNumFaceOverlays(), FaceTexture)
	NiOverride.ApplyNodeOverrides(akTarget)
	If StageGlobal != None
		StageGlobal.SetValueInt(Stage)
	EndIf
EndEvent


Event OnEffectFinish(Actor akTarget, Actor akCaster)
	If akTarget != Game.GetPlayer()
		Return
	EndIf
	; Dirt and Blood adds the next stage BEFORE removing this one. If another stage has
	; already claimed the overlay, leave it alone.
	If StageGlobal != None && StageGlobal.GetValueInt() != Stage
		Debug.Trace("Authoria_PlayerDirtOverlay: stage " + Stage + " ending, stage " + StageGlobal.GetValueInt() + " owns the overlay - leaving it")
		Return
	EndIf
	Bool isFemale = akTarget.GetLeveledActorBase().GetSex() == 1
	Debug.Trace("Authoria_PlayerDirtOverlay: clearing stage " + Stage)
	ClearPart(akTarget, isFemale, "Body", NiOverride.GetNumBodyOverlays())
	ClearPart(akTarget, isFemale, "Hands", NiOverride.GetNumHandOverlays())
	ClearPart(akTarget, isFemale, "Feet", NiOverride.GetNumFeetOverlays())
	ClearPart(akTarget, isFemale, "Face", NiOverride.GetNumFaceOverlays())
	NiOverride.ApplyNodeOverrides(akTarget)
	If StageGlobal != None
		StageGlobal.SetValueInt(0)
	EndIf
EndEvent


; Put our texture on one slot of a part: reuse the slot already carrying one of our textures
; (stage change, game load), otherwise take the highest slot that is empty or still default.
Function ApplyPart(Actor akTarget, Bool isFemale, String area, Int count, String texture)
	Int slot = FindSlot(akTarget, isFemale, area, count)
	If slot < 0
		Debug.Trace("Authoria_PlayerDirtOverlay: NO FREE OVERLAY SLOT for " + area + " (" + count + " slots)")
		Return
	EndIf
	String node = area + " [ovl" + slot + "]"
	NiOverride.AddNodeOverrideString(akTarget, isFemale, node, KEY_TEXTURE, 0, texture, true)
	NiOverride.AddNodeOverrideInt(akTarget, isFemale, node, KEY_TINT_COLOR, -1, TINT_WHITE, true)
	NiOverride.AddNodeOverrideInt(akTarget, isFemale, node, KEY_EMISSIVE_COLOR, -1, 0, true)
	NiOverride.AddNodeOverrideFloat(akTarget, isFemale, node, KEY_EMISSIVE_MULT, -1, 1.0, true)
	NiOverride.AddNodeOverrideFloat(akTarget, isFemale, node, KEY_ALPHA, -1, OverlayAlpha, true)
	NiOverride.AddNodeOverrideFloat(akTarget, isFemale, node, KEY_GLOSSINESS, -1, 0.0, true)
	NiOverride.AddNodeOverrideFloat(akTarget, isFemale, node, KEY_SPECULAR, -1, 0.0, true)
	Debug.Trace("Authoria_PlayerDirtOverlay: " + node + " <- " + texture)
EndFunction


; Restore every slot of a part that carries one of our textures back to the blank default.
Function ClearPart(Actor akTarget, Bool isFemale, String area, Int count)
	Int i = 0
	While i < count
		String node = area + " [ovl" + i + "]"
		If IsOurTexture(NiOverride.GetNodeOverrideString(akTarget, isFemale, node, KEY_TEXTURE, 0))
			NiOverride.AddNodeOverrideString(akTarget, isFemale, node, KEY_TEXTURE, 0, DefaultTexture, true)
			NiOverride.RemoveNodeOverride(akTarget, isFemale, node, KEY_TINT_COLOR, -1)
			NiOverride.RemoveNodeOverride(akTarget, isFemale, node, KEY_EMISSIVE_COLOR, -1)
			NiOverride.RemoveNodeOverride(akTarget, isFemale, node, KEY_EMISSIVE_MULT, -1)
			NiOverride.RemoveNodeOverride(akTarget, isFemale, node, KEY_ALPHA, -1)
			NiOverride.RemoveNodeOverride(akTarget, isFemale, node, KEY_GLOSSINESS, -1)
			NiOverride.RemoveNodeOverride(akTarget, isFemale, node, KEY_SPECULAR, -1)
			Debug.Trace("Authoria_PlayerDirtOverlay: cleared " + node)
		EndIf
		i += 1
	EndWhile
EndFunction


; Our own slot wins (so a stage change reuses it); otherwise the highest free slot.
; "Free" means empty OR RaceMenu's blank default - on the player no slot is ever unset.
Int Function FindSlot(Actor akTarget, Bool isFemale, String area, Int count)
	Int free = -1
	Int i = count
	While i > 0
		i -= 1
		String tex = NiOverride.GetNodeOverrideString(akTarget, isFemale, area + " [ovl" + i + "]", KEY_TEXTURE, 0)
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
