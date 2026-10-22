Scriptname Authoria_SeranaFaceFix extends ActiveMagicEffect
{UBE NPC head probe + tint safety net (Serana AND Lydia; SPID-distributed).
 Writes every probe line to console AND to Data\Authoria_FaceProbe.txt (PapyrusUtil), so the
 report can be read from the overwrite folder after the session - no screenshots needed.
 PROBE: race, weight, which head shapes exist on the loaded 3D, the head shape's diffuse and
 facetint texture paths (baked facegen embeds a FaceGenData\FaceTint path; a runtime-generated
 head does not), the base record's current head-part list, and the head ShaderTintColor (key 7).
 NO WRITES: this script is a probe only (the former key-7 tint write crashed the renderer on baked
 heads - see crash logs 2026-08-17 11:48 and 14:24).}

Int Property TintVampire = 0xA0B1B1 Auto   ; Serana vampire form skin tone
Int Property TintCured   = 0xA6A098 Auto   ; Serana cured form skin tone
Int Property TintLydia   = 0xCECDCC Auto   ; Lydia HumanFemaleSkinWhite02
String Property HeadShape = "00UBE_FemaleHead" Auto
String Property LogFile = "Data\\Authoria_FaceProbe.txt" Auto

Actor kTarget
Int   iTries = 0
Int   iPass  = 0

String Function Col(Int c)
    Int r = Math.LogicalAnd(Math.RightShift(c, 16), 255)
    Int g = Math.LogicalAnd(Math.RightShift(c, 8), 255)
    Int b = Math.LogicalAnd(c, 255)
    Return r + "," + g + "," + b
EndFunction

String Function Who()
    ActorBase b = kTarget.GetActorBase()
    If b
        Return b.GetName()
    EndIf
    Return "?"
EndFunction

Function Say(String s)
    String line = "[FaceProbe][" + Who() + "] " + s
    ConsoleUtil.PrintMessage(line)
    Debug.Trace(line)
    MiscUtil.WriteToFile(LogFile, line + "\n", true, true)
EndFunction

Int Function LocalID(Form f)
    ; low 6 hex digits of the FormID (strips load-order/ESL prefix)
    Return Math.LogicalAnd(f.GetFormID(), 0xFFFFFF)
EndFunction

Bool Function IsSerana()
    Return LocalID(kTarget.GetActorBase()) == 0x002B6C
EndFunction

Bool Function IsCured()
    Keyword kUndead = Game.GetFormFromFile(0x00013795, "Skyrim.esm") as Keyword
    If kUndead == None
        Return False
    EndIf
    Return !kTarget.HasKeyword(kUndead)
EndFunction

Event OnEffectStart(Actor akTarget, Actor akCaster)
    kTarget = akTarget
    iPass = 0
    RegisterForSingleUpdate(2.0)
EndEvent

Event OnCellLoad()
    ; 3D rebuilt (e.g. Serana Multiform NG applies a form + resets 3D) - probe again
    iTries = 0
    iPass = 0
    RegisterForSingleUpdate(2.0)
EndEvent

Event OnUpdate()
    If kTarget == None || kTarget.IsDead()
        Return
    EndIf
    iTries += 1
    If !kTarget.Is3DLoaded()
        If iTries < 30
            RegisterForSingleUpdate(1.0)
        EndIf
        Return
    EndIf
    iPass += 1
    Probe(iPass)
    If iPass == 1
        ; second pass after runtime appearance systems (Multiform NG etc.) have settled
        RegisterForSingleUpdate(8.0)
    EndIf
EndEvent

Function Probe(Int pass)
    ActorBase kBase = kTarget.GetActorBase()
    Race kRace = kTarget.GetRace()
    String sRace = "?"
    If kRace
        sRace = kRace.GetName()
    EndIf
    Say("pass " + pass + " base=" + LocalID(kBase) + " race=" + sRace + " weight=" + kBase.GetWeight() + " cured=" + IsCured())

    Bool bHead = NetImmerse.HasNode(kTarget, HeadShape, False)
    Say("shapes: UBEhead=" + bHead + " OriHair=" + NetImmerse.HasNode(kTarget, "_OriSeranaUBE_Hair", False) + " OriHL=" + NetImmerse.HasNode(kTarget, "_OriSeranaUBE_HL", False) + " OriEyes=" + NetImmerse.HasNode(kTarget, "_OriSeranaUBE_Eyes", False) + " OriBrows=" + NetImmerse.HasNode(kTarget, "_OriSeranaUBE_Brows", False) + " LydiaHair=" + NetImmerse.HasNode(kTarget, "00UBE_LydiaHair", False) + " LydiaHairRT=" + NetImmerse.HasNode(kTarget, "hair 11", False) + " vanillaSeranaHair=" + NetImmerse.HasNode(kTarget, "DLC1HairFemaleSerana", False) + " vanillaHead=" + NetImmerse.HasNode(kTarget, "FemaleHeadNord", False))
    If bHead
        ; key 9 = ShaderTexture by slot: 0 diffuse, 6 facetint. A BAKED head's slot-6 path
        ; contains "FaceGenData\FaceTint\<plugin>\<id>.dds"; a runtime head does not.
        Say("head tex0 = " + NiOverride.GetNodePropertyString(kTarget, False, HeadShape, 9, 0))
        Say("head tex6 = " + NiOverride.GetNodePropertyString(kTarget, False, HeadShape, 9, 6))
    EndIf

    Int n = kBase.GetNumHeadParts()
    String sParts = ""
    Int i = 0
    While i < n
        HeadPart hp = kBase.GetNthHeadPart(i)
        If hp
            sParts += "[" + hp.GetType() + "]" + hp.GetPartName() + " "
        EndIf
        i += 1
    EndWhile
    Say("record headparts(" + n + "): " + sParts)

    ; CLEANUP (2026-08-17 14:30): the former key-7 ShaderTintColor writes (this script's first
    ; versions + the Lydia Weight Runtime fix) were PERSISTENT NiOverrides. On a BAKED facegen head
    ; that override converts the FaceGen material to the RGB-tint type and the renderer then reads a
    ; colour as a texture pointer -> CTD (crash-2026-08-17-11-48-11 / -14-24-34, Serana's
    ; 00UBE_FemaleHead). RaceMenu re-applies persistent overrides from the save on every load, so
    ; strip it here and rebuild the actor's 3D so the head comes back from the bake untouched.
    If NiOverride.HasNodeOverride(kTarget, True, HeadShape, 7, -1)
        NiOverride.RemoveNodeOverride(kTarget, True, HeadShape, 7, -1)
        Say("REMOVED stale persistent key-7 tint override on " + HeadShape + " - queueing 3D refresh")
        kTarget.QueueNiNodeUpdate()
    ElseIf bHead
        Say("tint key7=" + Col(NiOverride.GetNodePropertyInt(kTarget, False, HeadShape, 7, -1)) + " (read-only; no override present)")
    Else
        Say("no '" + HeadShape + "' shape - not a UBE head")
    EndIf
EndFunction
