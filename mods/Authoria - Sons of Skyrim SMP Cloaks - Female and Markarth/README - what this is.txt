Authoria - Sons of Skyrim SMP Cloaks - Female and Markarth
==========================================================
Made 2026-08-16 by Claude for the Authoria list (profile DEEZ CS NUTZ).

WHAT
  HDT-SMP versions of the Sons of Skyrim v2.0 hold cloaks that no mod ships as SMP:
    - all 12 FEMALE hold cloaks (Cloack\CloackF, CloackOfficerF, CloackPauldronF,
      Dawnstar, Falkreath, Markarth, Morthal, Riften, Solitude, Whiterun, Whiterun\CloackLightF,
      Winterhold), weights _0 and _1
    - the MALE Markarth cloak (Markarth\CloackM_0/_1), which the Nexus SMP patch never covered
  The 11 other male cloaks come from "Sons of Skyrim - HDT Physics for Cloaks Patch" (Nexus 114690).

HOW (geometry transplant, no Outfit Studio)
  container  = the male SMP donor nif from Nexus 114690 (same hold; Markarth uses the Dawnstar donor)
               -> keeps its CB 01/02/03 bone chains, skin weights, Virtual* collision shapes,
                  the root NiStringExtraData "HDT Skinned Mesh Physics Object" ->
                  SKSE\Plugins\hdtSkinnedMeshConfigs\capeM_SoS.xml, and its shader.
  geometry   = the static BodySlide build of the same cloak (Authoria - Bodyslide Output - 3BA
               for female, - HIMBO for Markarth male): per-vertex position / bitangent / uv /
               normal / tangent copied by vertex index. Both meshes share the same topology
               (verified: identical triangle lists and identical UVs, 997 or 1055 verts).
               Positions were moved into the donor's frame (pure translation (0, 1.886, -62.935)
               derived from the shared bones' skin-to-bone transforms; Whiterun\CloackF = identity).
  extras     = BSTriShape bounding sphere and NiSkinData per-bone bounds recomputed;
               Markarth texture set rewritten to markarthcloak.dds / _n / clouddwemerpipes cubemap.
  Script: "_source - transplant script\transplant.py" (+ niflib.py). Re-runnable.

CAVEATS
  - The collision proxy (VirtualBody) is the donor's MALE body shape, because Nexus 114690 ships
    capeF_SoS.xml but no female collision meshes. Expect the cape to hang a hair further off a
    female back than a purpose-built female rig would.
  - Skin weights are the donor's (vanilla-male fit). Fine for a cape; the geometry itself is the
    3BA / HIMBO preset build.
  - No .tri files: these capes are not OBody/RaceMenu-morphed (same as the male Nexus patch).

ADDED 2026-08-27 - cape swing retune (SKSE\Plugins\hdtSkinnedMeshConfigs\capeM_SoS.xml)
  The cloaks were SMP-live but did not look it. Every one of them (male Nexus patch + the
  female/Markarth meshes above) points at capeM_SoS.xml, and the Nexus v1.1 copy of that file
  pinned the cape down:
    - each chain CB 01/02/03 has bone rows 1-6; rows 2-5 carry the cape's vertex weights
    - joints 1-2 and 2-3 had angular limits of exactly 0 rad -> the upper half was rigid
    - joints 3-4 and 4-5 allowed only +-0.1 / 0.2 / 0.1 rad (about 6 / 11 / 6 degrees)
    - the moving bones ran linearDamping and angularDamping 0.8, killing what little swing was left
  This mod now ships a tuned capeM_SoS.xml that wins over the Nexus copy (it sits 4 lines above
  the patch in all five profiles). Angular limits widen down the chain instead of being locked:
      joint 2<-1   +-0.12 / 0.18 / 0.12 rad
      joint 3<-2   +-0.22 / 0.30 / 0.22
      joint 4<-3   +-0.32 / 0.42 / 0.32
      joint 5<-4   +-0.42 / 0.55 / 0.42
  and the mass template's damping drops 0.8 -> 0.55. Nothing else changed: same bones, same
  templates, same six collision shapes (Cape / VirtualBody / VirtualHead / VirtualHands /
  VirtualFeet / VirtualGround), same masses, same collision tags. Diffed line by line.

  TO DIAL IT: edit that one file. Stiffer = shrink the four angularLower/UpperLimit pairs
  and/or raise the mass template damping back toward 0.8. Looser = the reverse.
  REVERT that part only: delete SKSE\ from this mod folder; the Nexus patch's own copy takes over.

REVERT
  Delete this mod folder and restore the static builds from
  _backups\2026-08-16 - Sons static cloaks (3BA female + HIMBO Markarth) into
  Authoria - Bodyslide Output - 3BA / - HIMBO.
