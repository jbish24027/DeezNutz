// AuthoriaReShadeBeforeUI - SKSE plugin + ReShade add-on.
// Renders ReShade's effects right before Skyrim draws its menus and HUD, so depth of field and
// blur never touch the UI. Same technique as SSE ReShade Helper (PureDark / doodlum): wrap the call
// MenuManagerDrawInterfaceStart (ID 82084) makes at +0x17A and call effect_runtime::render_effects
// after it. ReShade then skips its own pass at Present for that frame.
// Built for SkyrimSE 1.6.1170 only; refuses to patch if the exe or the call site does not match.

#define WIN32_LEAN_AND_MEAN
#define NOMINMAX
#include <Windows.h>
#include <ShlObj.h>
#include <cstdarg>
#include <cstdint>
#include <cstdio>
#include <cstring>

#include "reshade.hpp"

using namespace reshade::api;

namespace
{
	HMODULE g_self = nullptr;
	FILE* g_log = nullptr;

	effect_runtime* g_runtime = nullptr;
	command_list* g_cmd = nullptr;
	resource_view g_rtv = {};
	resource_view g_rtv_srgb = {};
	bool g_registered = false;
	uint32_t g_tries = 0;
	uint64_t g_passes = 0;

	using DrawFn = uint64_t (*)(uint64_t, uint64_t, uint64_t, uint64_t);
	DrawFn g_orig = nullptr;

	// SkyrimSE 1.6.1170: ID 82084 = RVA 0xFA4F00; the wrapped call sits at +0x17A
	constexpr uint32_t kSiteRva = 0xFA4F00 + 0x17A;
	constexpr uint8_t kBefore[9] = { 0x33, 0xD2, 0x48, 0x8D, 0x0D, 0x46, 0x37, 0x2E, 0x02 };  // xor edx,edx; lea rcx,[rip+..]
	constexpr uint32_t kVanillaTargetRva = 0xE44850;                                          // ID 77247

	void log(const char* fmt, ...)
	{
		if (!g_log)
			return;
		SYSTEMTIME t;
		GetLocalTime(&t);
		std::fprintf(g_log, "%02u:%02u:%02u.%03u ", t.wHour, t.wMinute, t.wSecond, t.wMilliseconds);
		va_list a;
		va_start(a, fmt);
		std::vfprintf(g_log, fmt, a);
		va_end(a);
		std::fputc('\n', g_log);
		std::fflush(g_log);
	}

	void open_log()
	{
		PWSTR docs = nullptr;
		if (SUCCEEDED(SHGetKnownFolderPath(FOLDERID_Documents, 0, nullptr, &docs))) {
			wchar_t path[MAX_PATH * 2];
			_snwprintf_s(path, _TRUNCATE, L"%s\\My Games\\Skyrim Special Edition\\SKSE\\AuthoriaReShadeBeforeUI.log", docs);
			_wfopen_s(&g_log, path, L"w");
			CoTaskMemFree(docs);
		}
	}

	void on_begin_effects(effect_runtime* rt, command_list* cmd, resource_view rtv, resource_view rtv_srgb)
	{
		// Only ever drive a D3D11 runtime from the game's render thread (a frame-generation proxy puts
		// ReShade on a D3D12 swap chain; that one is left alone and renders at Present as usual).
		if (rt->get_device()->get_api() != device_api::d3d11)
			return;
		if (g_runtime != rt || g_rtv.handle != rtv.handle)
			log("captured D3D11 runtime %p, back buffer view %llx", static_cast<void*>(rt), static_cast<unsigned long long>(rtv.handle));
		g_runtime = rt;
		g_cmd = cmd;
		g_rtv = rtv;
		g_rtv_srgb = rtv_srgb;
	}

	void on_destroy_runtime(effect_runtime* rt)
	{
		if (rt == g_runtime) {
			g_runtime = nullptr;
			g_cmd = nullptr;
			g_rtv = {};
			g_rtv_srgb = {};
			log("runtime %p destroyed (resize or shutdown) - waiting for the next capture", static_cast<void*>(rt));
		}
	}

	void try_register()
	{
		if (g_registered)
			return;
		if (reshade::register_addon(g_self)) {
			g_registered = true;
			reshade::register_event<reshade::addon_event::reshade_begin_effects>(on_begin_effects);
			reshade::register_event<reshade::addon_event::destroy_effect_runtime>(on_destroy_runtime);
			log("registered with ReShade (API %u)", static_cast<unsigned>(RESHADE_API_VERSION));
		}
	}

	uint64_t draw_thunk(uint64_t a, uint64_t b, uint64_t c, uint64_t d)
	{
		const uint64_t r = g_orig(a, b, c, d);
		if (!g_registered) {
			if ((g_tries++ % 300) == 0)
				try_register();
		} else if (g_runtime && g_cmd && g_rtv.handle) {
			g_runtime->render_effects(g_cmd, g_rtv, g_rtv_srgb);
			if (g_passes++ == 0)
				log("first pre-UI effect pass done");
		}
		return r;
	}

	bool exe_is_1170()
	{
		wchar_t exe[MAX_PATH];
		GetModuleFileNameW(nullptr, exe, MAX_PATH);
		DWORD h = 0, n = GetFileVersionInfoSizeW(exe, &h);
		if (!n)
			return false;
		static unsigned char buf[16384];
		if (n > sizeof(buf) || !GetFileVersionInfoW(exe, 0, n, buf))
			return false;
		VS_FIXEDFILEINFO* fi = nullptr;
		UINT len = 0;
		if (!VerQueryValueW(buf, L"\\", reinterpret_cast<void**>(&fi), &len) || !fi)
			return false;
		log("game exe version %u.%u.%u.%u", HIWORD(fi->dwFileVersionMS), LOWORD(fi->dwFileVersionMS), HIWORD(fi->dwFileVersionLS), LOWORD(fi->dwFileVersionLS));
		return fi->dwFileVersionMS == ((1u << 16) | 6u) && HIWORD(fi->dwFileVersionLS) == 1170;
	}

	void* alloc_near(uintptr_t addr)
	{
		SYSTEM_INFO si;
		GetSystemInfo(&si);
		const uintptr_t gran = si.dwAllocationGranularity;
		const uintptr_t start = addr & ~(gran - 1);
		for (uintptr_t delta = gran; delta < 0x70000000; delta += gran) {
			for (int dir = 0; dir < 2; ++dir) {
				const uintptr_t p = dir ? start + delta : start - delta;
				if (void* m = VirtualAlloc(reinterpret_cast<void*>(p), 64, MEM_RESERVE | MEM_COMMIT, PAGE_EXECUTE_READWRITE))
					return m;
			}
		}
		return nullptr;
	}

	void install()
	{
		if (!exe_is_1170()) {
			log("not SkyrimSE 1.6.1170 - hook NOT installed, ReShade keeps rendering at Present");
			return;
		}
		auto* const base = reinterpret_cast<uint8_t*>(GetModuleHandleW(nullptr));
		uint8_t* const site = base + kSiteRva;
		if (std::memcmp(site - sizeof(kBefore), kBefore, sizeof(kBefore)) != 0 || site[0] != 0xE8) {
			log("call site bytes do not match - hook NOT installed");
			return;
		}
		int32_t rel;
		std::memcpy(&rel, site + 1, 4);
		uint8_t* const target = site + 5 + rel;
		if (target != base + kVanillaTargetRva)
			log("call site already wrapped by another plugin (target RVA %llx) - chaining", static_cast<unsigned long long>(target - base));
		g_orig = reinterpret_cast<DrawFn>(target);

		auto* const tramp = static_cast<uint8_t*>(alloc_near(reinterpret_cast<uintptr_t>(site)));
		if (!tramp) {
			log("no trampoline memory near the exe - hook NOT installed");
			return;
		}
		const uint8_t jmp[6] = { 0xFF, 0x25, 0, 0, 0, 0 };  // jmp [rip+0]
		std::memcpy(tramp, jmp, 6);
		const uint64_t dst = reinterpret_cast<uint64_t>(&draw_thunk);
		std::memcpy(tramp + 6, &dst, 8);
		FlushInstructionCache(GetCurrentProcess(), tramp, 14);

		const int64_t newRel = reinterpret_cast<int64_t>(tramp) - reinterpret_cast<int64_t>(site + 5);
		if (newRel < INT32_MIN || newRel > INT32_MAX) {
			log("trampoline out of rel32 range - hook NOT installed");
			return;
		}
		const int32_t rel32 = static_cast<int32_t>(newRel);
		DWORD old;
		VirtualProtect(site + 1, 4, PAGE_EXECUTE_READWRITE, &old);
		std::memcpy(site + 1, &rel32, 4);
		VirtualProtect(site + 1, 4, old, &old);
		FlushInstructionCache(GetCurrentProcess(), site, 5);
		log("pre-UI hook installed at RVA %x", kSiteRva);

		try_register();
		if (!g_registered)
			log("ReShade not loaded yet - will retry from the render thread");
	}
}

struct SKSEPluginVersionData
{
	uint32_t dataVersion;
	uint32_t pluginVersion;
	char name[256];
	char author[256];
	char supportEmail[252];
	uint32_t versionIndependenceEx;
	uint32_t versionIndependence;
	uint32_t compatibleVersions[16];
	uint32_t seVersionRequired;
};

extern "C" __declspec(dllexport) SKSEPluginVersionData SKSEPlugin_Version = {
	1,                                  // dataVersion
	(1u << 24) | (0u << 16) | (0u << 4),  // 1.0.0
	"AuthoriaReShadeBeforeUI",
	"Authoria",
	"",
	1,  // kVersionIndependentEx_NoStructUse
	0,
	{ (1u << 24) | (6u << 16) | (1170u << 4), 0 },  // RUNTIME_VERSION_1_6_1170
	0
};

extern "C" __declspec(dllexport) bool SKSEPlugin_Load(const void*)
{
	open_log();
	log("AuthoriaReShadeBeforeUI 1.0.0 loaded");
	install();
	return true;
}

BOOL APIENTRY DllMain(HMODULE h, DWORD reason, LPVOID)
{
	if (reason == DLL_PROCESS_ATTACH) {
		g_self = h;
		DisableThreadLibraryCalls(h);
	}
	return TRUE;
}
