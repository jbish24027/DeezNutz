# Redguard crash investigation — 2026-10-21

Scope approved: focused read-only diagnosis. No installed files, profiles, or build sources changed. User confirmed the crash profile was DEEZ CS NUTZ - PICTA.

Crash 05:47:10: SkyrimSE.exe+0D384DE, reading 0x3F800030. RDI identifies BSTriShape "Robe 2" on an Alik'r Warrior near RoriksteadEdge. RBP BSDismemberSkinInstance reports NumBones: 0. Parent identifies ARMA 07BC17:Skyrim.esm / ARMO 07BC19:Skyrim.esm.

houseCARL resolves the armor addon to USSEP and its male model to Clothes/Redguard/RedguardOutfit_1.nif. Both weight variants win from Authoria - SMP Vanilla Coats over HIMBO Vanilla Armors, USSEP BSA, and vanilla BSA. Skeleton winner is XPMSSE.

Both installed variants contain BSTriShape block 98 "Robe 2", skin block 99: zero vertices, zero triangles, zero skin-instance bones, zero NiSkinData bones. This exactly matches the log's shape and zero-bone finding. Strong evidence for the crash source, pending an in-game controlled retest after repair. Do not blame FreeClimb, Wayfarer, or Occlusion merely for appearing in the log.

houseCARL NiflySharp throws NullReferenceException on both SMP files. Independent local read-only niflib parsing confirms the empty shape; underlying HIMBO files parse normally and have 24 bones per shape. The staged copies are byte-identical to installed files.

SHA256 _0: 4343b16761d678ae15dd227b2f40717efea8468b1a32515eb7dd8eb7108d8d93
SHA256 _1: e923ef33514e24d86fdbdc13297c8a30f23c622ab699bb825de19457c10913cd

Build origin: designs/redguard_robe.py requests panels=2. skill/scripts/build_skirt_rig.py panel_split emits every sector without skipping empty sectors; its later-panel writer emits them. designs/out/RedguardRobe_build.log lines 15, 17, 18 explicitly record "Robe 2 0 pts" and zero bones. The prior STATE.md ALL OK is insufficient validation of this condition.

Also: ARG Skirt Side has nine partition vertices but zero triangles in both variants, and is referenced by RedguardRobeM.xml. Robe 2 is not referenced by that XML. Review the empty collider alongside the repair; do not assume it caused this crash.

Proposed next scope: preserve backups, repair only the Redguard pair and relevant XML as needed, prevent empty shape emission in the source builder, add a targeted empty-skinned-shape validation, and verify before installation. Keep the existing HIMBO fit and SMP rig. User must authorize repair scope; current permission was diagnosis only. Verify MO2 and game closed immediately before any mods/profiles writes. No Synthesis, Reqtificator, or sorting required.

Usage snapshot during investigation: 36% total weekly, 9% five-hour window. No daily baseline or numeric daily cap set; these are not daily usage figures.
