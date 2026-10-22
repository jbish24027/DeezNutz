"""Padborn 3.1.0 documentation/config edits: README.md (installed mod), Padborn.json (installed mod),
fomod/info.xml + fomod/ModuleConfig.xml (extracted copies under _tools/padborn/fomod).
Each anchor must occur exactly once, so running it twice fails loudly instead of doubling text."""
import os

MOD = r"C:\1. AUTHORIA\mods\Authoria - Padborn"
TOOLS = os.path.dirname(os.path.abspath(__file__))


def edit(path, pairs):
    raw = open(path, "rb").read()
    crlf = b"\r\n" in raw
    s = raw.decode("utf-8")
    if crlf:
        s = s.replace("\r\n", "\n")
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, (path, old[:70], n)
        s = s.replace(old, new)
    if crlf:
        s = s.replace("\n", "\r\n")
    open(path, "wb").write(s.encode("utf-8"))
    print("edited", os.path.basename(path), "(crlf)" if crlf else "(lf)")


# ---------------------------------------------------------------- README.md
edit(os.path.join(MOD, "README.md"), [
    ("# Authoria — Padborn 3.0.0", "# Authoria — Padborn 3.1.0"),
    (
        "8. **Optional sprint-button move + experimental sprint rescue** — see \"The Padborn plugin\" below.\n",
        "8. **Optional sprint-button move + experimental sprint rescue** — see \"The Padborn plugin\" below.\n"
        "9. **First-person block (3.1.0)** — the game can no longer switch you to first person: not a script\n"
        "   (81 loose scripts on the list call `Game.ForceFirstPerson()`, First Person Interactions after\n"
        "   every lever pull among them), not the POV control, not zoom-in, not a save restore. On by default,\n"
        "   one json switch. Pairs with the layout change below that takes the vanilla POV toggle off R3, so\n"
        "   TDM's lock-on no longer drags the camera into first person.\n",
    ),
    (
        "text + **binary** controlmaps for 402, plus its MCM pictures and `Layout 402.jpg`. Exactly three\n"
        "rows differ from 406, and moving Sneak/Auto-Move is the CCS author's design for the B variant:\n",
        "text + **binary** controlmaps for 402, plus its MCM pictures and `Layout 402.jpg`. Three rows\n"
        "differ from 406 by the CCS author's design for the B variant, and 3.1.0 adds a fourth of its own:\n",
    ),
    (
        "| **Auto-Move** | L3 + R3 | **B + L3** |\n",
        "| **Auto-Move** | L3 + R3 | **B + L3** |\n"
        "| **Toggle POV** | R3 | **off the pad** (keyboard F only) — 3.1.0, in BOTH the text and the binary controlmap |\n"
        "\n"
        "Why Toggle POV moved: True Directional Movement's lock-on shares R3, and the engine reads the binary\n"
        "`ControlMap_Custom.txt` on top of the text one, so R3 fired lock-on AND the vanilla POV toggle on\n"
        "the same press — target lock = first person. With POV off the pad, R3 is lock-on only (TDM ini:\n"
        "`bTargetLockUsePOVSwitchGamepad = 0`, `uTargetLockKey = 273`). The first-person block in the DLL\n"
        "is the belt to these braces.\n",
    ),
    (
        "One DLL, three things, none of them touching the Gamepad++ half:\n",
        "One DLL, four things, none of them touching the Gamepad++ half:\n",
    ),
    (
        "`\"sprint\": { \"enabled\": true }` in the json.\n"
        "\n"
        "### Config (`SKSE\\Plugins\\Padborn.json`)\n",
        "`\"sprint\": { \"enabled\": true }` in the json.\n"
        "\n"
        "**First-person block (3.1.0, ON by default).** The player camera can no longer enter the first-person\n"
        "state, whoever asks. Four layers, all inside the DLL, nothing written to disk:\n"
        "\n"
        "1. `PlayerCamera::ForceFirstPerson` — the engine function behind Papyrus `Game.ForceFirstPerson()`\n"
        "   and most SKSE plugins — is detoured to a no-op.\n"
        "2. `TESCamera::SetState` — a request for the player camera's first-person state is redirected to\n"
        "   third person (dropped when already there). Catches zoom-in, load-game restores and anything\n"
        "   that bypasses layer 1.\n"
        "3. The vanilla **Toggle POV** control is swallowed (nothing to toggle to). Hold-to-rotate on that\n"
        "   key goes with it; the right stick still rotates the camera.\n"
        "4. A per-frame watchdog: camera found in first person anyway → `ForceThirdPerson` before the\n"
        "   camera updates, and a line in `Padborn.log`.\n"
        "\n"
        "Every blocked attempt is logged (`camera: ForceFirstPerson blocked (#n)` — first 20, then every\n"
        "500th), so a script that keeps trying shows up by name of its count, not by surprise. Switch it\n"
        "off with `\"camera\": { \"blockFirstPerson\": false }`; keep the block but let the keyboard POV key\n"
        "work with `\"allowManualToggle\": true` (then only forced/automatic switches are blocked and the\n"
        "watchdog stands down). Not built for VR.\n"
        "\n"
        "### Config (`SKSE\\Plugins\\Padborn.json`)\n",
    ),
    (
        "the full reference: sprint on/off + diagnostics, sprint button, per-button OStim bindings, hold\n"
        "timing, lockout behavior, and glyph-bar size/position/art style. Both installer answers are just\n"
        "json values — flip them any time without reinstalling.\n",
        "the full reference: first-person block, sprint on/off + diagnostics, sprint button, per-button OStim\n"
        "bindings, hold timing, lockout behavior, and glyph-bar size/position/art style. Both installer\n"
        "answers are just json values — flip them any time without reinstalling.\n",
    ),
    (
        "| `SKSE\\Plugins\\Padborn.dll` | the plugin: OStim controller layer, glyph bar, sprint button move, sprint rescue |\n",
        "| `SKSE\\Plugins\\Padborn.dll` (+ `.pdb`) | the plugin: first-person block, OStim controller layer, glyph bar, sprint button move, sprint rescue |\n",
    ),
    (
        "| `ControlMap_Custom.txt` + `Interface\\controls\\pc\\controlmap.txt` | CCS **LAYOUT 402** — the author's own binary + text controlmaps, unmodified |\n",
        "| `ControlMap_Custom.txt` + `Interface\\controls\\pc\\controlmap.txt` | CCS **LAYOUT 402** — the author's own binary + text controlmaps, one change in each: Toggle POV's gamepad column 0x0080 (R3) → unbound |\n",
    ),
    (
        "**The DLL.** C++ source for `Padborn.dll` ships in the archive under `Source\\` (not installed):\n"
        "`CMakeLists.txt` + `vcpkg.json` + `src\\`, CommonLibSSE-NG, CMake + vcpkg, MSVC x64 Release.\n",
        "**The DLL.** C++ source for `Padborn.dll` ships in the archive under `Source\\` (not installed):\n"
        "`CMakeLists.txt` + `vcpkg.json` + `src\\`, CommonLibSSE-NG (`extern\\CommonLibSSE-NG`, alandtse\n"
        "CommonLibVR branch `ng`), Microsoft Detours (vcpkg), CMake + vcpkg, MSVC x64 Release. Configure with\n"
        "`-DCOMMONLIB_ENABLE_IPO=OFF` if cl.exe crashes in \"Generating Code\". The build ships a PDB.\n",
    ),
    (
        "## Status\n"
        "\n"
        "- Gamepad++ menu + QuickLoot guard fixes, gesture map, dodge setup: confirmed in play.\n",
        "## Changelog\n"
        "\n"
        "**3.1.0 (2026-09-08)** — Padborn.dll 2.1.0: first-person block (on by default, `camera` json block).\n"
        "Layout 402 controlmaps: Toggle POV taken off the gamepad in the text AND the binary file (R3 was\n"
        "firing TDM lock-on and the vanilla POV toggle together). Source updated in `Source\\`.\n"
        "\n"
        "**3.0.0** — Gamepad++ fixes + gesture map + dodge setup + Padborn.dll 2.0.0 (OStim layer, glyph bar,\n"
        "sprint rescue) merged into one package.\n"
        "\n"
        "## Status\n"
        "\n"
        "- Gamepad++ menu + QuickLoot guard fixes, gesture map, dodge setup: confirmed in play.\n",
    ),
    (
        "- Glyph bar: freshly built, in-game pass pending.\n",
        "- Glyph bar: freshly built, in-game pass pending.\n"
        "- First-person block + POV off R3: built 2026-09-08, in-game pass pending.\n",
    ),
])

# ---------------------------------------------------------------- Padborn.json (installed)
edit(os.path.join(MOD, "SKSE", "Plugins", "Padborn.json"), [
    (
        "    \"Padborn - gamepad suite: sprint rescue + OStim controller layer + glyph bar.\",\n",
        "    \"Padborn - gamepad suite: first-person block + sprint rescue + OStim controller layer + glyph bar.\",\n",
    ),
    (
        "    \"sprint: EXPERIMENTAL hold-to-sprint rescue, OFF by default. Only enable it if\",\n",
        "    \"camera: blockFirstPerson true (default) keeps the player camera out of first\",\n"
        "    \"  person no matter who asks - Game.ForceFirstPerson from any script, the vanilla\",\n"
        "    \"  Toggle POV control, zoom-in, a save restore. Every blocked attempt is logged.\",\n"
        "    \"  allowManualToggle true lets the keyboard POV key still switch (only forced\",\n"
        "    \"  switches are blocked then); false (default) makes that key do nothing.\",\n"
        "    \"\",\n"
        "    \"sprint: EXPERIMENTAL hold-to-sprint rescue, OFF by default. Only enable it if\",\n",
    ),
    (
        "  \"sprint\": { \"enabled\": false, \"log\": false, \"button\": \"keep\" },\n",
        "  \"camera\": { \"blockFirstPerson\": true, \"allowManualToggle\": false },\n"
        "\n"
        "  \"sprint\": { \"enabled\": false, \"log\": false, \"button\": \"keep\" },\n",
    ),
])

# ---------------------------------------------------------------- fomod (extracted copies)
edit(os.path.join(TOOLS, "fomod", "info.xml"), [
    ("<Version>3.0.0</Version>", "<Version>3.1.0</Version>"),
    (
        "plus the Padborn SKSE plugin - OStim controller layer, glyph bar, optional sprint-button move and experimental sprint rescue.",
        "plus the Padborn SKSE plugin - first-person block (the game can no longer switch you to first person), OStim controller layer, glyph bar, optional sprint-button move and experimental sprint rescue. 3.1.0 also takes the vanilla POV toggle off R3 in the Layout 402 controlmaps, so TDM lock-on no longer flips the camera.",
    ),
])
edit(os.path.join(TOOLS, "fomod", "ModuleConfig.xml"), [
    (
        "Dodge: tap B = dodge, hold B = sprint, and the six B-combos (Favorites, Wait, Quick menus) can never fire a dodge. This is the variant the fix was built and play-tested on.</description>",
        "Dodge: tap B = dodge, hold B = sprint, and the six B-combos (Favorites, Wait, Quick menus) can never fire a dodge. This is the variant the fix was built and play-tested on.\n\n3.1.0: Toggle POV is taken off the gamepad in BOTH controlmap files (text and binary), so R3 is True Directional Movement's lock-on only and never the vanilla POV toggle. POV stays on keyboard F (and the DLL's first-person block swallows even that unless you allow it in Padborn.json).</description>",
    ),
])
print("all doc edits applied")
