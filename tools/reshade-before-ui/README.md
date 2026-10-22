# AuthoriaReShadeBeforeUI (2026-10-13)

SKSE plugin + ReShade add-on that renders ReShade's effects right before Skyrim draws its menus and HUD,
so depth of field / blur never touch the UI (same method as doodlum + PureDark's SSE ReShade Helper,
github.com/doodlum/skyrim-reshade-helper, which Community Shaders lists as incompatible BY FILE NAME).

- Hook: the call at +0x17A inside ID 82084 (CS calls it MenuManagerDrawInterfaceStart; RVA 0xFA4F00 on
  1.6.1170, call target ID 77247 = RVA 0xE44850). After that call returns, `effect_runtime::render_effects`
  runs on the back buffer view captured from `reshade_begin_effects`. ReShade 6.7.3 then skips its Present
  pass for the frame (`_effects_rendered_this_frame`) and saves/restores the game's D3D11 state itself.
- Safety: exe must be 1.6.1170; the 9 bytes before the call and the E8 opcode must match; a different call
  target is chained, not overwritten. Only a D3D11 runtime is driven (a frame-generation proxy that moves
  ReShade to a D3D12 swap chain is left alone). Runtime destroy (resize) clears the cache.
- Code bytes were checked against a SteamStub-decrypted copy of the exe (session scratchpad s19_unstub.py
  + s19_addrlib.py; the exe on disk is encrypted, crash dumps do not hold code pages).
- Build: `build.cmd` (MSVC 2022 BuildTools, no other dependencies; headers = ReShade v6.7.3 include\).
  Install: `install.py --write` (mod `Authoria - ReShade Before UI`, + in PICTA / Preset Studio, - in the
  other profiles that carry the Picta-lane preset; also puts MagicDOF + GaussianBlur back in that preset).
- Logs: `Documents\My Games\Skyrim Special Edition\SKSE\AuthoriaReShadeBeforeUI.log` ("pre-UI hook installed",
  "registered with ReShade", "first pre-UI effect pass done"); ReShade.log lists the add-on.
- Re-check if: the game updates (RVA/bytes), ReShade updates (API version 18), CS upscaling/frame gen or
  HDR display is turned back on (effects then run before CS's present-time work - test).
