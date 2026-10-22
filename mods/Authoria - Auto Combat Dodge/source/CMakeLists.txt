cmake_minimum_required(VERSION 3.21)

project(AutoCombatDodge VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# CommonLibSSE-NG (alandtse/CommonLibVR, branch ng, tag v13.0.0): SE + AE, no VR, no tests.
set(BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(SKSE_SUPPORT_XBYAK OFF CACHE BOOL "" FORCE)
set(ENABLE_SKYRIM_SE ON CACHE BOOL "" FORCE)
set(ENABLE_SKYRIM_AE ON CACHE BOOL "" FORCE)
set(ENABLE_SKYRIM_VR OFF CACHE BOOL "" FORCE)
# The published prebuilt bundles are built with MSVC 19.51; this machine has 19.44, so
# CommonLib is compiled from source. /Brepro makes the output deterministic so two
# independent builds can be byte-compared (guards against a miscompile on unstable hardware).
add_compile_options(/Brepro)
add_link_options(/Brepro)
set(CMAKE_STATIC_LINKER_FLAGS "${CMAKE_STATIC_LINKER_FLAGS} /Brepro")
# LTCG (/GL) crashes cl.exe on this machine (Padborn build notes); keep IPO off.
set(COMMONLIB_ENABLE_IPO OFF CACHE BOOL "" FORCE)

if(NOT DEFINED COMMONLIB_DIR)
	set(COMMONLIB_DIR "${CMAKE_CURRENT_SOURCE_DIR}/../ext/CommonLibVR")
endif()
add_subdirectory("${COMMONLIB_DIR}" commonlib)

add_library(AutoCombatDodge SHARED
	src/main.cpp
	src/Settings.cpp
	src/AutoCombatLink.cpp
	src/Dodge.cpp
)

target_include_directories(AutoCombatDodge PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/src)
target_precompile_headers(AutoCombatDodge PRIVATE src/PCH.h)
target_link_libraries(AutoCombatDodge PRIVATE CommonLibSSE::CommonLibSSE)

target_compile_options(AutoCombatDodge PRIVATE
	/utf-8
	/permissive-
	/Zc:preprocessor
	/W4
	/wd4100
	/Zi
)
target_compile_definitions(AutoCombatDodge PRIVATE NOMINMAX WIN32_LEAN_AND_MEAN)
target_link_options(AutoCombatDodge PRIVATE /DEBUG:FULL /OPT:REF /OPT:ICF)

set_target_properties(AutoCombatDodge PROPERTIES PREFIX "" OUTPUT_NAME "AutoCombatDodge")
