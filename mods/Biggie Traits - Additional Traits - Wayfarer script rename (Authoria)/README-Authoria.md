# Wayfarer script rename (Authoria, 2026-09-30)

Walk With Me 0.2.5 ships `Scripts\Wayfarer.pex` (the native class its SKSE DLL binds to). Additional Traits for Biggie Traits also ships a `Scripts\Wayfarer.pex` (the Wayfarer trait: disables fast travel while the map is open). Walk With Me wins the file conflict, which would break the trait.

This mod renames the trait script to `WayfarBT` (same length, so the plugin was byte-patched in place: one VMAD on MGEF `Traits_Wayfarer`, no properties) and ships the renamed pex and source. Load it above (higher priority than) Additional Traits for Biggie Traits. The original Wayfarer.pex in the trait mod is now unreferenced and harmless.
