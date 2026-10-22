"""One-shot edits that turn the shipped Padborn 2.0.0 source into 2.1.0 (first-person block).
Idempotent: refuses to run twice (each anchor must occur exactly once)."""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Source")


def edit(rel, pairs):
    path = os.path.join(ROOT, rel)
    raw = open(path, "rb").read()
    crlf = b"\r\n" in raw
    s = raw.decode("utf-8")
    if crlf:
        s = s.replace("\r\n", "\n")
    for old, new in pairs:
        n = s.count(old)
        assert n == 1, (rel, old[:60], n)
        s = s.replace(old, new)
    if crlf:
        s = s.replace("\n", "\r\n")
    open(path, "wb").write(s.encode("utf-8"))
    print("edited", rel, "(crlf)" if crlf else "(lf)")


edit("src/Config.h", [(
    "\t\tbool logInput{ false };\n",
    "\t\tbool logInput{ false };\n"
    "\n"
    "\t\t// First-person block (2.1.0): keep the player camera out of first person no\n"
    "\t\t// matter who asks - scripts (First Person Interactions ends every lever\n"
    "\t\t// pull with Game.ForceFirstPerson), the vanilla Toggle POV control, zoom-in,\n"
    "\t\t// camera restores on load, other plugins. See Camera.cpp for the layers.\n"
    "\t\tbool cameraBlockFirstPerson{ true };\n"
    "\n"
    "\t\t// Let the vanilla Toggle POV control (keyboard F by default) still switch;\n"
    "\t\t// only forced/automatic switches are blocked then, and the per-frame\n"
    "\t\t// watchdog stands down. Off = the control does nothing.\n"
    "\t\tbool cameraAllowManualToggle{ false };\n",
)])

edit("src/Config.cpp", [
    (
        '\t\tif (json.contains("hint") && json["hint"].is_object()) {',
        '\t\tif (json.contains("camera") && json["camera"].is_object()) {\n'
        '\t\t\tconst auto& camera = json["camera"];\n'
        '\t\t\tcameraBlockFirstPerson = camera.value("blockFirstPerson", cameraBlockFirstPerson);\n'
        '\t\t\tcameraAllowManualToggle = camera.value("allowManualToggle", cameraAllowManualToggle);\n'
        "\t\t}\n"
        "\n"
        '\t\tif (json.contains("hint") && json["hint"].is_object()) {',
    ),
    (
        '\t\tlogger::info("OPad.json loaded: {} bindings, hold {:.2f}s, fullLockout {}",\n'
        "\t\t\tbindings.size(), holdSeconds, fullLockout);",
        '\t\tlogger::info("OPad.json loaded: {} bindings, hold {:.2f}s, fullLockout {}, blockFirstPerson {} (manual toggle {})",\n'
        '\t\t\tbindings.size(), holdSeconds, fullLockout, cameraBlockFirstPerson, cameraAllowManualToggle ? "allowed" : "blocked");',
    ),
])

edit("src/plugin.cpp", [
    (
        '#include "Config.h"\n#include "InputRouter.h"',
        '#include "Camera.h"\n#include "Config.h"\n#include "InputRouter.h"',
    ),
    (
        "\t.Version = REL::Version{ 2, 0, 0, 0 },",
        "\t.Version = REL::Version{ 2, 1, 0, 0 },",
    ),
    (
        '\tlogger::info("Padborn 2.0.0 loading (sprint rescue + OStim pad layer + glyph bar)");',
        '\tlogger::info("Padborn 2.1.0 loading (sprint rescue + OStim pad layer + glyph bar + first-person block)");',
    ),
    (
        "\tOPad::Overlay::Install();\n",
        "\tOPad::Overlay::Install();\n"
        "\n"
        "\t// Engine-function detours + two vtable writes; needs no trampoline space and\n"
        "\t// no game data, so it goes in at load like the render hooks.\n"
        "\tOPad::Camera::Install();\n",
    ),
])

edit("CMakeLists.txt", [
    (
        "project(OPad VERSION 2.0.0 LANGUAGES CXX)",
        "project(OPad VERSION 2.1.0 LANGUAGES CXX)",
    ),
    (
        'set(ENABLE_SKYRIM_VR OFF CACHE BOOL "" FORCE)\nadd_subdirectory(extern/CommonLibSSE-NG)',
        'set(ENABLE_SKYRIM_VR OFF CACHE BOOL "" FORCE)\n'
        "# LTCG (/GL) crashes cl.exe on the build machine; keep IPO off.\n"
        'set(COMMONLIB_ENABLE_IPO OFF CACHE BOOL "" FORCE)\n'
        "add_subdirectory(extern/CommonLibSSE-NG)",
    ),
    (
        "find_package(imgui CONFIG REQUIRED)\n",
        "find_package(imgui CONFIG REQUIRED)\n"
        "\n"
        "# Microsoft Detours: function-entry hooks that still call the original\n"
        '# (Camera.cpp). vcpkg port "detours".\n'
        "find_path(DETOURS_INCLUDE_DIR NAMES detours/detours.h detours.h REQUIRED)\n"
        "find_library(DETOURS_LIBRARY NAMES detours REQUIRED)\n",
    ),
    (
        "    src/Sprint.cpp\n)",
        "    src/Sprint.cpp\n    src/Camera.cpp\n)",
    ),
    (
        "target_include_directories(OPad PRIVATE\n    ${CMAKE_CURRENT_SOURCE_DIR}/src\n)",
        "target_include_directories(OPad PRIVATE\n    ${CMAKE_CURRENT_SOURCE_DIR}/src\n    ${DETOURS_INCLUDE_DIR}\n)",
    ),
    (
        "    imgui::imgui\n    d3d11\n)",
        "    imgui::imgui\n    ${DETOURS_LIBRARY}\n    d3d11\n)",
    ),
    (
        "    /wd4100  # unreferenced formal parameter\n)",
        "    /wd4100  # unreferenced formal parameter\n"
        "    /Zi      # always ship a PDB - the only reason a lost-source DLL stays diagnosable\n"
        ")\n"
        "\n"
        "target_link_options(OPad PRIVATE /DEBUG:FULL /OPT:REF /OPT:ICF)",
    ),
])
print("all edits applied")
