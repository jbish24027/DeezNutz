# Authoria - Papyrus - Frostfall Updates and Fixes

- `scripts/_frost_main.pex`
  Updates Frostfall's SkyUI lookup to prefer `SkyUI_SE.esp` and only fall back to the old `SkyUI.esp` name if needed. It also guards startup, first-start, legacy config, tracking quest, and starter equipment properties that Authoria intentionally leaves unbound through the junk-disabler setup.

- `scripts/_frost_skyuiconfigpanelscript.pex`
  Uses the SSE SkyUI plugin name first and ignores out-of-window `OnOptionMenuOpen()` calls. That keeps the Frostfall MCM working normally while cutting down the SkyUI timing noise in the Papyrus log.

- `scripts/_frost_compatibility.pex`
  Adds safe `Game.IsPluginInstalled()` checks before optional compatibility lookups, including the old Immersive Armors path that logged false missing-plugin errors. It also guards DLC1/DLC2 worldspace form-list writes and keeps the `Frostfall_Loaded` event call from being assigned into a throwaway `None` variable.

- `scripts/_frost_sksetypesdelegate.pex`
  Uses the repaired SkyUI lookup path so Frostfall's SKSE/SkyUI bridge binds cleanly in an SSE load order.

- `scripts/_frost_climatesystem.pex`
  Carries forward the winning Frostfall - Seasons climate script and fixes the High Hrothgar polygon arrays to hold 14 entries, matching the existing index 13 assignments.