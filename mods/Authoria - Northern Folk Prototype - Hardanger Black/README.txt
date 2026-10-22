Authoria - Northern Folk Prototype - Hardanger Black (built 22 Oct 2026)

Prototype for converting Clothes of the Northern Folk (CNF): Fralia's outfit CNFVikingHardangerBlack.
  - Black Hardanger Viking attire (dress / men's tunic)
  - Knitted black stockings and boots
  - Black Hardanger headscarf (head item: unchanged mesh, UBE races added)

What is in here
  Women, vanilla races (CBBE 3BA):  meshes\clothes\MaidenDressesofNorway\...\*_f_0/_1.nif + *_f.tri
     dress and boots fitted to the 3BA body ('- Zeroed Sliders -', hidden sliders at project defaults), 3BA skin
     only where the CNF author showed skin, weights from the 3BA body (breast/butt/belly bones follow), every 3BA
     slider as a .tri morph (OBody / RaceMenu body shapes). The dress has Helga-style cloth physics.
  Women, UBE races:  meshes\!UBE\clothes\MaidenDressesofNorway\...  same, fitted to the in-game UBE body with
     DayOnly's own 3BA->UBE move (sampled from Authoria - UBE Converter Output), UBE sliders as .tri; dress has cloth physics.
     Records: Authoria - CNF Prototype - UBE.esp (ESL, 3 UBE armor addons) + SkyPatcher armorAddonsToAdd INI.
  Men (HIMBO):  *_m_0/_1.nif + *_m.tri  fitted with HIMBO's own Vanilla-to-HIMBO reference, HIMBO skin piece,
     HIMBO slider morphs. No cloth physics on the men's tunic in this prototype.
  Physics: meshes\authoria cnf smp\hardanger dress f.xml (12 x 8 cloth grid under the pelvis, invisible
     thigh/calf colliders, Helga numbers - same recipe as the 18 Oct robe physics).

Not changed: first-person sleeves (vanilla arms), ground models, other colours.
Requiem / Eleonora / Seasons: mesh-only change plus visual-only UBE addons; no balance, dialogue or seasonal
content, so none apply.

Placement: directly above "Clothes of the Northern Folk" in MO2; plugin directly after CNFDistribution.esp.
Enabled in DEEZ CS NUTZ - PICTA and Authoria - Preset Studio - HPH. Backups: profiles\*\*.bak-pre-cnfproto-20261022.

Rebuild (scripts in C:\1. AUTHORIA\_tools\cnf-convert):
  convert_f3ba.py <CNF _1.nif> <out dir> <tri path> [f3ba|mhimbo]   (women 3BA / men HIMBO)
  build_ube_field.py (once) then convert_ube.py <3BA _1.nif> <out dir> <!UBE tri path>
  rig_dress.py <staged mods root> <out root>  (cloth physics; positions untouched, .tri stays valid)
  render.py / poke.py / morphcheck.py  (pictures and clipping checks)
