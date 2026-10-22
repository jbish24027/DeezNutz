# Bottled Shaders: Effects 11 and Silent Horizons 2 cores (request draft, revised 2026-09-25 late)

Draft for the Bottled Shaders Nexus page (mod 192816) or its Discord. Plain facts from this install. Revised twice: the Community Shaders team removed encrypted-core support on purpose, so this does not ask for the old key path back; and the Extender author has since shipped an API that makes a clean route possible.

---

**Title:** Effects 11: ENB Extender 1.6.0 now exports a compiler API that could handle KIEFX cores

**Setup:** Bottled Shaders 1.0.0 and 1.0.1, Skyrim SE 1.6.1170, Effects 11 preset = Soul Core ENB 2.1 (Nexus 162892) on Silent Horizons 2 Shader Core 1.10 (Nexus 101696).

**Symptom:** every launch shows `ERROR: 4 effect(s) failed to compile` for enbbloom.fx, enbadaptation.fx, enbeffect.fx and enbeffectpostpass.fx:

```
enbeffect.fx(2,1-5): error X3000: unrecognized identifier 'KIEFX'
[EFFECTS11] No preset in use: '...\enbseries\enbeffect.fx' failed to load
```

The four files start with the bytes `KIEFX`; the compiler is handed the encoded text. I know the CS sticky of 2026-08-26 says Extender and SH2 support was removed, and the Effects 11 page says encrypted presets are unsupported. I am not asking for the old key-reading code back.

**What changed on the Extender side:** ENB Extender and Helper 1.6.0 (2026-09-20, Nexus 99406) exports three new functions from KiENBExtender.dll:

- `ENBExt_Compile(CompileFileIndex FileIndex, ID3DBlob** ppCode, ID3DBlob** ppErrorMsgs)` with the index enum None, PreProcessing, DepthOfField, Bloom, Lens, Adaptation, MainProcessing, PostProcessing, SunSprite, Underwater
- `ENBExt_RegisterForENBCompileCallback` / `ENBExt_UnregisterFromENBCompileCallback`

The author's "Compiler API Example" file (Nexus 99406, misc files) links them with `GetModuleHandleW(L"KiENBExtender")` plus `GetProcAddress`, and its comment says to do that "after the Extender has been loaded (e.g. in the SKSE PostLoad callback)". The DLL also carries a "Running standalone initialization" path, so it initialises without ENB present. In other words the Shader Core author now provides a way for a renderer to receive compiled bytecode for a locked core without ever seeing the key.

**Request:** would you consider an optional path in Effects 11 that, when KiENBExtender.dll 1.6.0 or newer is loaded and an effect file starts with `KIEFX`, asks the Extender for the compiled effect through `ENBExt_Compile` instead of compiling the text itself? If that is out of scope for Bottled, a note saying so would let Silent Horizons users rebase now.

---

Local reference for us: the old build is kept as `mods\[NoDelete] Community Shaders AIO` (disabled). The Extender 1.6.0 archive, its example and Bottled 1.0.1 are in Downloads (2026-09-25 17:35). The third-party "CS 1.8.4 KIEFX Decoder Patch" on Dwemer Mods is a rebuilt official 1.8.4 DLL and cannot be used with Bottled.
