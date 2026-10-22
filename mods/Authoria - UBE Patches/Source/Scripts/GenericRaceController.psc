Scriptname GenericRaceController extends Quest
{ RCS-compat shim (Authoria, 2026-06-29).

  UBE was built for TMPhoenix's Papyrus RaceCompatibility, whose GenericRaceController
  did the per-race runtime FormList injection (PlayableRaceList / HeadParts* sharing /
  RacesHuman|Beast|Elf). ARR replaced that framework with Race Compatibility SKSE (RCS),
  which does NOT ship GenericRaceController -> UBE's 8 *RaceController quests (+ Register-
  CustomRaceScript) call into a missing class, spamming the Papyrus log every load
  ("Cannot open store for class GenericRaceController" -> raceController == None ->
  "Cannot call NewNord()/proxyRaces() on a None object").

  This shim restores the class so those bindings resolve and the spam stops. It declares
  every property the original did (so the quest VMADs bind with no "property no longer
  exists" warnings) and makes proxyRaces() a NO-OP: under RCS the work it used to do is
  already handled (proxy + vampirism via ActorProxy keywords + RCS JSON; PlayableRaceList
  via UBE's own records) or is DELIBERATELY omitted (vanilla head-part sharing, which on a
  UBE body produces a head<->body seam). Do not reinstate the injection here. }

; --- Race Compatibility framework lists (set by the quest VMADs; many point at the old
;     RaceCompatibility.esm and resolve to None under the RCS dummy esm - harmless) ---
FormList Property PlayableRaceList Auto
FormList Property PlayableVampireList Auto

FormList Property RacesHuman Auto
FormList Property RacesBeast Auto
FormList Property RacesElf Auto

FormList Property HeadPartsAllRacesMinusBeast Auto
FormList Property HeadPartsAllRacesMinusBeastVampires Auto

FormList Property HeadPartsHuman Auto
FormList Property HeadPartsHumanVampires Auto
FormList Property HeadPartsHumansandVampires Auto
FormList Property HeadPartsHumansOrcsandVampires Auto
FormList Property HeadPartsHumanoidVampire Auto
FormList Property HeadPartsBretsNordsImpsandVampires Auto

FormList Property HeadPartsArgonianVampire Auto
FormList Property HeadPartsKhajiitVampire Auto

FormList Property HeadPartsElves Auto
FormList Property HeadPartsElvesandVampires Auto

FormList Property HeadPartsArgonian Auto
FormList Property HeadPartsBreton Auto
FormList Property HeadPartsDarkElf Auto
FormList Property HeadPartsHighElf Auto
FormList Property HeadPartsImperial Auto
FormList Property HeadPartsKhajiit Auto
FormList Property HeadPartsNord Auto
FormList Property HeadPartsOrc Auto
FormList Property HeadPartsRedguard Auto
FormList Property HeadPartsWoodElf Auto

FormList Property HeadPartsArgonianandVampire Auto
FormList Property HeadPartsBretonandVampire Auto
FormList Property HeadPartsDarkElfandVampire Auto
FormList Property HeadPartsHighElfandVampire Auto
FormList Property HeadPartsImperialandVampire Auto
FormList Property HeadPartsKhajiitandVampire Auto
FormList Property HeadPartsNordandVampire Auto
FormList Property HeadPartsOrcandVampire Auto
FormList Property HeadPartsRedguardandVampire Auto
FormList Property HeadPartsWoodElfandVampire Auto

; --- "New" custom-race lists (set at runtime by UBE_*RaceController / RegisterCustomRaceScript
;     OnInit, e.g. raceController.NewNord = HeadPartsNord_UBE) ---
FormList Property NewArgonian Auto
FormList Property NewBreton Auto
FormList Property NewDarkElf Auto
FormList Property NewHighElf Auto
FormList Property NewImperial Auto
FormList Property NewKhajiit Auto
FormList Property NewNord Auto
FormList Property NewOrc Auto
FormList Property NewRedguard Auto
FormList Property NewWoodElf Auto

FormList Property NewArgonianVampire Auto
FormList Property NewBretonVampire Auto
FormList Property NewDarkElfVampire Auto
FormList Property NewHighElfVampire Auto
FormList Property NewImperialVampire Auto
FormList Property NewKhajiitVampire Auto
FormList Property NewNordVampire Auto
FormList Property NewOrcVampire Auto
FormList Property NewRedguardVampire Auto
FormList Property NewWoodElfVampire Auto

Function proxyRaces()
	; No-op under RCS. The original injected the custom races into the vanilla head-part
	; FormLists + RacesHuman/Beast/Elf + PlayableRaceList via RaceCompatibility.esm's
	; RaceDispatcherScript. RCS handles proxy/vampirism natively, UBE adds its races to
	; PlayableRaceList at the record level, and the vanilla head-part sharing is omitted on
	; purpose (it causes a head<->body seam on the UBE body). So there is nothing to do.
EndFunction
