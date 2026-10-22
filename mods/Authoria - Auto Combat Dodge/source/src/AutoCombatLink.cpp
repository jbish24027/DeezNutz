#include "AutoCombatLink.h"
#include "Settings.h"

namespace ACD::AutoCombat
{
	namespace
	{
		struct Section
		{
			std::uintptr_t begin;
			std::uintptr_t end;
			DWORD          flags;
		};

		struct Module
		{
			std::uintptr_t       base{ 0 };
			std::vector<Section> sections;

			[[nodiscard]] const Section* SectionOf(std::uintptr_t a_addr) const
			{
				for (const auto& s : sections) {
					if (a_addr >= s.begin && a_addr < s.end) {
						return &s;
					}
				}
				return nullptr;
			}
			[[nodiscard]] bool IsWritableData(std::uintptr_t a_addr) const
			{
				const auto* s = SectionOf(a_addr);
				return s && (s->flags & IMAGE_SCN_MEM_WRITE) && !(s->flags & IMAGE_SCN_MEM_EXECUTE);
			}
		};

		Link                     g_link{ Link::kNone };
		const volatile std::uint8_t* g_enabledFlag{ nullptr };
		const volatile std::uint8_t* g_pilotFlag{ nullptr };
		std::atomic<bool>        g_mirrorEnabled{ false };

		bool ReadModule(HMODULE a_handle, Module& a_out)
		{
			const auto base = reinterpret_cast<std::uintptr_t>(a_handle);
			const auto dos = reinterpret_cast<const IMAGE_DOS_HEADER*>(base);
			if (dos->e_magic != IMAGE_DOS_SIGNATURE) {
				return false;
			}
			const auto nt = reinterpret_cast<const IMAGE_NT_HEADERS64*>(base + dos->e_lfanew);
			if (nt->Signature != IMAGE_NT_SIGNATURE || nt->OptionalHeader.Magic != IMAGE_NT_OPTIONAL_HDR64_MAGIC) {
				return false;
			}
			a_out.base = base;
			const auto* sec = IMAGE_FIRST_SECTION(nt);
			for (WORD i = 0; i < nt->FileHeader.NumberOfSections; ++i, ++sec) {
				const auto size = std::max<std::uintptr_t>(sec->Misc.VirtualSize, sec->SizeOfRawData);
				a_out.sections.push_back({ base + sec->VirtualAddress, base + sec->VirtualAddress + size, sec->Characteristics });
			}
			return !a_out.sections.empty();
		}

		std::int32_t Disp(std::uintptr_t a_at) { return *reinterpret_cast<const std::int32_t*>(a_at); }
		std::uint8_t Byte(std::uintptr_t a_at) { return *reinterpret_cast<const std::uint8_t*>(a_at); }
		bool         IsRipModRM(std::uint8_t a_modrm) { return (a_modrm & 0xC7) == 0x05; }

		// Every occurrence of a NUL-terminated string inside the module's non-code sections.
		std::vector<std::uintptr_t> FindString(const Module& a_mod, std::string_view a_text)
		{
			std::vector<std::uintptr_t> hits;
			std::string                 needle(a_text);
			needle.push_back('\0');
			for (const auto& s : a_mod.sections) {
				if (s.flags & IMAGE_SCN_MEM_EXECUTE) {
					continue;
				}
				const auto* first = reinterpret_cast<const char*>(s.begin);
				const auto* last = reinterpret_cast<const char*>(s.end);
				for (const auto* p = std::search(first, last, needle.begin(), needle.end()); p != last;
					 p = std::search(p + 1, last, needle.begin(), needle.end())) {
					hits.push_back(reinterpret_cast<std::uintptr_t>(p));
				}
			}
			return hits;
		}

		// "lea r64, [rip+disp32]" (REX.W 8D /r) instructions whose target is a_target.
		std::vector<std::uintptr_t> FindLeaRefs(const Module& a_mod, std::uintptr_t a_target)
		{
			std::vector<std::uintptr_t> hits;
			for (const auto& s : a_mod.sections) {
				if (!(s.flags & IMAGE_SCN_MEM_EXECUTE) || s.end - s.begin < 8) {
					continue;
				}
				for (auto p = s.begin; p + 7 <= s.end; ++p) {
					const auto rex = Byte(p);
					if ((rex != 0x48 && rex != 0x4C) || Byte(p + 1) != 0x8D || !IsRipModRM(Byte(p + 2))) {
						continue;
					}
					if (p + 7 + static_cast<std::intptr_t>(Disp(p + 3)) == a_target) {
						hits.push_back(p);
					}
				}
			}
			return hits;
		}

		// "movzx r32, byte ptr [rip+disp32]" (0F B6 /r) at a_at -> its target, if it is one.
		std::optional<std::uintptr_t> MovzxRipTarget(const Module& a_mod, std::uintptr_t a_at)
		{
			if (!a_mod.SectionOf(a_at) || !a_mod.SectionOf(a_at + 6)) {
				return std::nullopt;
			}
			if (Byte(a_at) != 0x0F || Byte(a_at + 1) != 0xB6 || !IsRipModRM(Byte(a_at + 2))) {
				return std::nullopt;
			}
			const auto target = a_at + 7 + static_cast<std::intptr_t>(Disp(a_at + 3));
			if (!a_mod.IsWritableData(target)) {
				return std::nullopt;
			}
			return target;
		}

		// Nearest byte-flag load in the a_window bytes before a_from.
		std::optional<std::uintptr_t> FlagLoadedBefore(const Module& a_mod, std::uintptr_t a_from, std::size_t a_window)
		{
			for (std::size_t back = 7; back <= a_window; ++back) {
				if (auto t = MovzxRipTarget(a_mod, a_from - back)) {
					return t;
				}
			}
			return std::nullopt;
		}

		// First flag in the window after a_from that is loaded (movzx), negated (sete) and swapped
		// back (xchg) - the "flag = !flag" toggle of AutoCombat's hotkey handler. The sete
		// requirement skips the neighbouring "capture a new hotkey" flags, which are cleared, not negated.
		std::optional<std::uintptr_t> ToggledFlagAfter(const Module& a_mod, std::uintptr_t a_from, std::size_t a_window)
		{
			for (std::size_t fwd = 0; fwd < a_window; ++fwd) {
				const auto at = a_from + fwd;
				const auto target = MovzxRipTarget(a_mod, at);
				if (!target) {
					continue;
				}
				bool sawSete = false;
				for (std::size_t k = 7; k < 0x30; ++k) {
					const auto x = at + k;
					if (!a_mod.SectionOf(x + 5)) {
						break;
					}
					if (Byte(x) == 0x0F && Byte(x + 1) == 0x94) {
						sawSete = true;
					}
					if (Byte(x) == 0x86 && IsRipModRM(Byte(x + 1)) && x + 6 + static_cast<std::intptr_t>(Disp(x + 2)) == *target) {
						if (sawSete) {
							return target;
						}
						break;
					}
				}
			}
			return std::nullopt;
		}

		std::optional<std::uintptr_t> FlagNearString(const Module& a_mod, std::string_view a_text, bool a_toggleAfter)
		{
			for (const auto str : FindString(a_mod, a_text)) {
				for (const auto lea : FindLeaRefs(a_mod, str)) {
					auto t = a_toggleAfter ? ToggledFlagAfter(a_mod, lea, 0x200) : FlagLoadedBefore(a_mod, lea, 0x40);
					if (t) {
						return t;
					}
				}
			}
			return std::nullopt;
		}

		bool ScanModule(HMODULE a_handle)
		{
			Module mod;
			if (!ReadModule(a_handle, mod)) {
				logger::warn("AutoCombat.dll: could not read its PE headers");
				return false;
			}
			const auto pilotA = FlagNearString(mod, "Auto-pilot is active.", false);
			const auto pilotB = FlagNearString(mod, "auto-pilot turned off", false);
			const auto enabled = FlagNearString(mod, "Auto Combat: ON", true);

			auto rva = [&](const std::optional<std::uintptr_t>& p) { return p ? *p - mod.base : 0; };
			logger::info("AutoCombat.dll scan: pilot(menu)=+{:X} pilot(stop)=+{:X} enabled(hotkey)=+{:X}", rva(pilotA), rva(pilotB), rva(enabled));

			if (!pilotA || !enabled) {
				logger::warn("AutoCombat.dll: flag signatures not found (different build?)");
				return false;
			}
			if (pilotB && *pilotB != *pilotA) {
				logger::warn("AutoCombat.dll: the two auto-pilot references disagree - not trusting the scan");
				return false;
			}
			if (*pilotA == *enabled) {
				logger::warn("AutoCombat.dll: auto-pilot and enabled flags resolved to the same byte - not trusting the scan");
				return false;
			}
			const auto pv = *reinterpret_cast<const std::uint8_t*>(*pilotA);
			const auto ev = *reinterpret_cast<const std::uint8_t*>(*enabled);
			if (pv > 1 || ev > 1) {
				logger::warn("AutoCombat.dll: flag bytes are not booleans (pilot={} enabled={}) - not trusting the scan", pv, ev);
				return false;
			}
			g_pilotFlag = reinterpret_cast<const volatile std::uint8_t*>(*pilotA);
			g_enabledFlag = reinterpret_cast<const volatile std::uint8_t*>(*enabled);
			return true;
		}

		class InputSink final : public RE::BSTEventSink<RE::InputEvent*>
		{
		public:
			static InputSink* Get()
			{
				static InputSink s;
				return &s;
			}

			RE::BSEventNotifyControl ProcessEvent(RE::InputEvent* const* a_event, RE::BSTEventSource<RE::InputEvent*>*) override
			{
				if (!a_event || g_link != Link::kMirror) {
					return RE::BSEventNotifyControl::kContinue;
				}
				const auto& cfg = Settings::Get();
				const int   hotkey = cfg.mirrorHotkey > 0 ? cfg.mirrorHotkey : cfg.acHotkey;
				if (hotkey <= 0) {
					return RE::BSEventNotifyControl::kContinue;
				}
				for (auto* e = *a_event; e; e = e->next) {
					if (e->GetEventType() != RE::INPUT_EVENT_TYPE::kButton || e->GetDevice() != RE::INPUT_DEVICE::kKeyboard) {
						continue;
					}
					const auto* button = e->AsButtonEvent();
					if (!button || !button->IsDown() || static_cast<int>(button->GetIDCode()) != hotkey) {
						continue;
					}
					// Auto Combat ignores its key while the game is paused by a menu; do the same.
					if (const auto ui = RE::UI::GetSingleton(); ui && ui->GameIsPaused()) {
						continue;
					}
					const bool now = !g_mirrorEnabled.load();
					g_mirrorEnabled.store(now);
					logger::info("hotkey mirror: Auto Combat now assumed {}", now ? "ON" : "OFF");
				}
				return RE::BSEventNotifyControl::kContinue;
			}
		};
	}

	void Init()
	{
		const auto handle = GetModuleHandleW(L"AutoCombat.dll");
		if (!handle) {
			g_link = Link::kNone;
			logger::warn("AutoCombat.dll is not loaded - auto-dodge stays idle unless ActivationMode=2");
			return;
		}
		const auto& cfg = Settings::Get();
		if (cfg.activationMode == 0 && ScanModule(handle)) {
			g_link = Link::kMemory;
			logger::info("linked to Auto Combat's live state (memory read)");
		} else {
			g_link = Link::kMirror;
			g_mirrorEnabled.store(cfg.acEnabledAtStart);
			logger::info("following Auto Combat through its hotkey (scan code {}), starting {}", cfg.mirrorHotkey > 0 ? cfg.mirrorHotkey : cfg.acHotkey,
				cfg.acEnabledAtStart ? "ON" : "OFF");
		}
	}

	void RegisterInputSink()
	{
		if (auto* mgr = RE::BSInputDeviceManager::GetSingleton()) {
			mgr->AddEventSink(InputSink::Get());
			logger::info("input sink registered (used only by the hotkey mirror)");
		}
	}

	void ResetMirror()
	{
		if (g_link != Link::kMirror) {
			return;
		}
		// Auto Combat saves its settings (Enabled= included) back to its ini, so re-read it.
		Ini ac;
		if (ac.Load("Data/SKSE/Plugins/AutoCombat.ini")) {
			if (auto v = ac.GetAny("Enabled")) {
				g_mirrorEnabled.store(*v == "1" || *v == "true");
			}
		}
		logger::info("hotkey mirror reset from AutoCombat.ini: {}", g_mirrorEnabled.load() ? "ON" : "OFF");
	}

	Link LinkType() { return g_link; }

	bool IsEnabled()
	{
		switch (g_link) {
		case Link::kMemory:
			return g_enabledFlag && *g_enabledFlag != 0;
		case Link::kMirror:
			return g_mirrorEnabled.load();
		default:
			return false;
		}
	}

	bool IsPilotActive()
	{
		return g_link == Link::kMemory && g_pilotFlag && *g_pilotFlag != 0;
	}

	const char* LinkName()
	{
		switch (g_link) {
		case Link::kMemory:
			return "memory";
		case Link::kMirror:
			return "hotkey mirror";
		default:
			return "none";
		}
	}
}
