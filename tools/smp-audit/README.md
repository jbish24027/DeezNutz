# SMP audit toolkit (Claude, 2026-08-16)

Finds SMP meshes that lose to a static copy in the MO2 VFS, plus SMP meshes whose xml is missing.
Read-only scripts. Python 3.12 + `lz4` (present in the user's Python).

| script | what it does |
|---|---|
| `smp_audit.py` | walks every ENABLED mod of profile `DEEZ CS NUTZ` (+ overwrite); for every nif path with 2+ loose providers, parses each copy's header and flags "winner static, lower copy SMP". Also lists xml-less SMP winners among contended paths. |
| `bsa_audit.py` | indexes every active mod BSA (profile `archives.txt`, vanilla/CC skipped), extracts BSA copies (lz4/zlib) and flags SMP-in-BSA buried by a loose static winner, and static-later-BSA over SMP-earlier-BSA. |
| `sweep2.py` | all 79k loose winners: SMP status + xml existence (loose or BSA); `meshes\!ube\<x>` twin check against `meshes\<x>`. |
| `pair_check.py` | for each buried pair: shapes, verts, topology equality, bones present in the static copy. |
| `nif_extradata.py` | adds / retargets the `HDT Skinned Mesh Physics Object` NiStringExtraData on a nif (rebuilds the header, links from the footer root). |
| `transplant.py` | Sons-of-Skyrim transplant (male SMP donor rig + female/Markarth static geometry). |
| `build_restores.py` | builds the prepared fixes into `restore_out\` (see below). |

Results of the 2026-08-16 run: `*_result.json`, `*_log.txt`.

## restore_out\ (prepared, NOT installed)
17 nifs, mod-layout paths:
- Velothi HIMBO/3BA builds (12): identical to the Bodyslide-output builds + physics link re-added
  (`indoril wayfarer\helmet*`, `helmetwithscarfm*`, `ashlander seer\bootsm*`/`bootsf*`, `camonnatong\steelglovesf*`, `ashlanderwarrior\steelbodyf*`).
- Falmer Slayer UBE (2): `!ube\falmerslayer\falmerslayerhelmet.nif`, `falmerslayerfaceguard.nif` + physics link (`meshes\falmerslayer\hood.xml`).
- volsCloaks UBE (3): `!ube\clothes\volscloaks\fluffycloak_f.nif`, `hoodedf_0/1.nif` = SMP source rig (with VirtualBody/VirtualFeet collision) + UBE geometry.
To install: new mod folder with these files, delete the static copies from the output mods (backup first),
add the modlist line in all four profiles, plus delete the 2 Einar backpack statics from Bodyslide Output - NSFW.
