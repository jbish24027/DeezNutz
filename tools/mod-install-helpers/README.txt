mod-install-helpers (2026-08-17)
- fomod_tool.py  : dump / match / providers / simulate a FOMOD (ModuleConfig.xml) against an installed MO2 folder.
                   simulate <archive_root> <choices.txt> --inst <installed dir> compares; --out <dir> writes the install.
                   Choice labels look like: S<step index> <step name> / <group> / <option>  (see veldun-choices\*.txt)
- pex_patch.py   : find PROPSET <prop> = <float> in a function of a Skyrim .pex and patch the float (big-endian PEX).
                   used for Time Flies: load_defaults spell_learning_hour 2.0 -> 0.0
- plugin_census.py : full vs light plugin count per profile (winner resolved by modlist rank; base + CC implicit counted).
- apply_profiles.py: the 2026-08-17 profile edit script (anchor-based inserts into modlist/plugins/loadorder/plugingroups, all 4 profiles). Reuse the pattern, not the hardcoded lists.
- veldun-choices\ : proven Vel'dun UI FOMOD choices (main / patches / overhauls) for the three installed folders.