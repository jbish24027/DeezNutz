Removes default powers, adds new power that automatically checks for followers, adds hotkey to bathe.

Authoria - DnB Wig Exclusions_FLM.ini
  Stops bathing from stripping wigs, hair armors and beards. Dirt and Blood's
  bathing routine unequips every worn item in biped slots 30-62 and re-equips
  it after the animation; wigs sit in slot 31 (Hair) / 41 (LongHair), so they
  pop off every bath and are lost outright if the actor unloads or the script
  is interrupted mid-animation. FLM adds all 296 wig/hair/beard armors in the
  load order to Dirt and Blood's own Dirty_ListofIgnoredItems FormList
  (0xDEA~Dirt and Blood - Dynamic Visuals.esp), which the strip loop skips.
  Helmets, hoods, hats, circlets and hair-slot masks are deliberately left out
  so they still come off for a bath.
  Requires: FormList Manipulator (FLM).

Soap AnimObject for the Malignis bathing animation
  The Malignis animations were shipped without an AnimObject, so the actor
  scrubbed with an empty hand. Restores Bathing in Skyrim's behaviour:
    - Meshes\mzin\Bathe\AnimObjectSoap.nif + Textures\mzin\Bathe\Soap_*.dds
      (from Bathing in Skyrim - Renewed; the mesh carries Prn='AnimObjectR',
      the skeleton's right-hand AnimObject node)
    - ANIO record Authoria_AnimObjectSoap, 000809 in this mod's esp. BiS's own
      mzinAnimObjectSoap is unavailable - Bathing in Skyrim.esp is not enabled
      in ARR - so the list gets its own.
    - Meshes\Actors\Character\Animations\Bathing_in_Skyrim_Malignis\
      FNIS_Bathing_in_Skyrim_Malignis_List.txt overrides the Malignis - BiSR -
      Dirt and Blood Patch list, adding the "o" option, the AnimObject name and
      a TAnimObjectR trigger to mzinBatheA5_T1..T4.
    - Dirty_BathingQuest.DryCustom sends AnimObjectUnequip so an early-ending
      bath can't leave the soap stuck in the actor's hand.
  REQUIRES A PANDORA RE-RUN. The behaviour is generated, so nothing changes
  in game until Pandora is run again.
