cmake_minimum_required(VERSION 3.21)

project(OPad VERSION 2.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# CommonLibSSE-NG: runtime-agnostic (SE + AE), no unit tests, no xbyak.
set(BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(SKSE_SUPPORT_XBYAK OFF CACHE BOOL "" FORCE)
set(ENABLE_SKYRIM_SE ON CACHE BOOL "" FORCE)
set(ENABLE_SKYRIM_AE ON CACHE BOOL "" FORCE)
set(ENABLE_SKYRIM_VR OFF CACHE BOOL "" FORCE)
# LTCG (/GL) crashes cl.exe on the build machine; keep IPO off.
set(COMMONLIB_ENABLE_IPO OFF CACHE BOOL "" FORCE)
add_subdirectory(extern/CommonLibSSE-NG)

find_package(nlohmann_json CONFIG REQUIRED)
find_package(imgui CONFIG REQUIRED)

# Microsoft Detours: function-entry hooks that still call the original
# (Camera.cpp). vcpkg port "detours".
find_path(DETOURS_INCLUDE_DIR NAMES detours/detours.h detours.h REQUIRED)
find_library(DETOURS_LIBRARY NAMES detours REQUIRED)

set(SOURCES
    src/plugin.cpp
    src/Config.cpp
    src/OStimBridge.cpp
    src/InputRouter.cpp
    src/Overlay.cpp
    src/Sprint.cpp
    src/Camera.cpp
)

add_library(OPad SHARED ${SOURCES})

target_include_directories(OPad PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${DETOURS_INCLUDE_DIR}
)

target_precompile_headers(OPad PRIVATE src/PCH.h)

target_link_libraries(OPad PRIVATE
    CommonLibSSE::CommonLibSSE
    nlohmann_json::nlohmann_json
    imgui::imgui
    ${DETOURS_LIBRARY}
    d3d11
)

target_compile_options(OPad PRIVATE
    /utf-8
    /permissive-
    /Zc:preprocessor
    /W4
    /wd4100  # unreferenced formal parameter
    /Zi      # always ship a PDB - the only reason a lost-source DLL stays diagnosable
)

target_link_options(OPad PRIVATE /DEBUG:FULL /OPT:REF /OPT:ICF)

# SKSE expects the DLL flat, no "lib" prefix. Output renamed at the 2.0 merge:
# OPad + PadbornSprint are one suite now, shipped as Padborn.dll.
set_target_properties(OPad PROPERTIES PREFIX "" OUTPUT_NAME "Padborn")
