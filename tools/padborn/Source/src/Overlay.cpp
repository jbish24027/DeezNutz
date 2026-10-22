#include "Overlay.h"

#include "Config.h"

#ifndef NOMINMAX
#	define NOMINMAX
#endif
#include <d3d11.h>
#include <dxgi.h>

#include <imgui.h>
#include <imgui_impl_dx11.h>
#include <imgui_impl_win32.h>

#include <atomic>
#include <mutex>

namespace OPad::Overlay
{
	namespace
	{
		enum class Glyph : std::uint8_t
		{
			kNone = 0,
			kA,
			kB,
			kX,
			kY,
			kLB,
			kRB,
			kLT,
			kRT,
			kLTRT,  // the speed pair rendered as one pill
			kStart,
			kBack,
			kL3,
			kR3,
		};

		struct Item
		{
			Glyph       glyph{ Glyph::kNone };
			std::string label;
		};

		std::atomic<bool> g_ready{ false };
		std::atomic<bool> g_visible{ false };
		std::atomic<bool> g_hiddenByUser{ false };

		std::mutex        g_itemsMutex;
		std::vector<Item> g_items;

		ImFont* g_fontRegular = nullptr;
		ImFont* g_fontBold = nullptr;

		Glyph KeyCodeToGlyph(std::uint32_t a_keyCode)
		{
			switch (a_keyCode) {
			case 270: return Glyph::kStart;
			case 271: return Glyph::kBack;
			case 272: return Glyph::kL3;
			case 273: return Glyph::kR3;
			case 274: return Glyph::kLB;
			case 275: return Glyph::kRB;
			case 276: return Glyph::kA;
			case 277: return Glyph::kB;
			case 278: return Glyph::kX;
			case 279: return Glyph::kY;
			case 280: return Glyph::kLT;
			case 281: return Glyph::kRT;
			default: return Glyph::kNone;
			}
		}

		// Finds the button a given action currently sits on. Returns 0 if unbound.
		std::uint32_t FindButton(Action a_action, bool* a_isHold = nullptr)
		{
			for (const auto& [code, binding] : Config::Get().bindings) {
				if (binding.press == a_action || binding.hold == a_action) {
					if (a_isHold) {
						*a_isHold = binding.hold == a_action;
					}
					return code;
				}
			}
			return 0;
		}

		// PlayStation pad? The engine's own device object answers: Skyrim SE on PC
		// drives a DualShock through BSPCOrbisGamepadDevice (HID) and everything
		// XInput-shaped (Xbox pads, Steam Input translation) through
		// BSWin32GamepadDevice. Config can override with "glyphs": "xbox" / "ps".
		bool UsePSGlyphs()
		{
			const auto& config = Config::Get();
			if (config.hintGlyphs == 1) {
				return false;
			}
			if (config.hintGlyphs == 2) {
				return true;
			}
			// the same signal the engine's own button art follows
			auto* controlMap = RE::ControlMap::GetSingleton();
			return controlMap && controlMap->GetGamePadType() == RE::PC_GAMEPAD_TYPE::kOrbis;
		}

		void BuildItems()
		{
			struct Entry
			{
				Action           action;
				std::string_view label;
			};
			// Same set the approved mockup showed. D-pad omitted (navigation reads as
			// intuitive without help); Start/Back/L3 omitted for compactness.
			constexpr std::array kEntries{
				Entry{ Action::kYes, "OK"sv },
				Entry{ Action::kToggle, "Menu"sv },
				Entry{ Action::kAlignment, "Align"sv },
				Entry{ Action::kSearch, "Search"sv },
				Entry{ Action::kPullOut, "Pull out"sv },
			};

			std::vector<Item> items;

			for (const auto& entry : kEntries) {
				if (const auto code = FindButton(entry.action); code != 0) {
					items.push_back({ KeyCodeToGlyph(code), std::string{ entry.label } });
				}
			}

			// Speed pair: one "LT/RT Speed" pill when it sits on the triggers, two
			// separate items otherwise.
			const auto upCode = FindButton(Action::kSpeedUp);
			const auto downCode = FindButton(Action::kSpeedDown);
			if ((upCode == 281 && downCode == 280) || (upCode == 280 && downCode == 281)) {
				items.push_back({ Glyph::kLTRT, "Speed" });
			} else {
				if (downCode != 0) {
					items.push_back({ KeyCodeToGlyph(downCode), "Slower" });
				}
				if (upCode != 0) {
					items.push_back({ KeyCodeToGlyph(upCode), "Faster" });
				}
			}

			bool endIsHold = false;
			if (const auto code = FindButton(Action::kEnd, &endIsHold); code != 0) {
				items.push_back({ KeyCodeToGlyph(code), endIsHold ? "End (hold)" : "End" });
			}

			std::scoped_lock lock{ g_itemsMutex };
			g_items = std::move(items);
		}

		// ---- drawing ----------------------------------------------------------

		struct GlyphStyle
		{
			bool        pill;         // rounded rectangle with text, vs a face button
			const char* pillText;     // for pills
			char        letter;       // for Xbox face buttons
			ImU32       color;        // ring / letter / symbol color
			int         psShape;      // 0 none, 1 cross, 2 circle, 3 square, 4 triangle
		};

		GlyphStyle StyleFor(Glyph a_glyph, bool a_ps)
		{
			constexpr ImU32 xbGreen = IM_COL32(110, 180, 60, 255);
			constexpr ImU32 xbRed = IM_COL32(224, 68, 60, 255);
			constexpr ImU32 xbBlue = IM_COL32(62, 141, 221, 255);
			constexpr ImU32 xbYellow = IM_COL32(235, 190, 30, 255);
			constexpr ImU32 psBlue = IM_COL32(124, 156, 233, 255);
			constexpr ImU32 psRed = IM_COL32(229, 68, 60, 255);
			constexpr ImU32 psPink = IM_COL32(224, 129, 195, 255);
			constexpr ImU32 psGreen = IM_COL32(64, 196, 160, 255);
			constexpr ImU32 none = IM_COL32(255, 255, 255, 255);

			switch (a_glyph) {
			case Glyph::kA: return a_ps ? GlyphStyle{ false, "", 0, psBlue, 1 } : GlyphStyle{ false, "", 'A', xbGreen, 0 };
			case Glyph::kB: return a_ps ? GlyphStyle{ false, "", 0, psRed, 2 } : GlyphStyle{ false, "", 'B', xbRed, 0 };
			case Glyph::kX: return a_ps ? GlyphStyle{ false, "", 0, psPink, 3 } : GlyphStyle{ false, "", 'X', xbBlue, 0 };
			case Glyph::kY: return a_ps ? GlyphStyle{ false, "", 0, psGreen, 4 } : GlyphStyle{ false, "", 'Y', xbYellow, 0 };
			case Glyph::kLB: return { true, a_ps ? "L1" : "LB", 0, none, 0 };
			case Glyph::kRB: return { true, a_ps ? "R1" : "RB", 0, none, 0 };
			case Glyph::kLT: return { true, a_ps ? "L2" : "LT", 0, none, 0 };
			case Glyph::kRT: return { true, a_ps ? "R2" : "RT", 0, none, 0 };
			case Glyph::kLTRT: return { true, a_ps ? "L2/R2" : "LT/RT", 0, none, 0 };
			case Glyph::kStart: return { true, a_ps ? "Options" : "Start", 0, none, 0 };
			case Glyph::kBack: return { true, a_ps ? "Touch" : "Back", 0, none, 0 };
			case Glyph::kL3: return { true, "L3", 0, none, 0 };
			case Glyph::kR3: return { true, "R3", 0, none, 0 };
			default: return { true, "?", 0, none, 0 };
			}
		}

		void Draw()
		{
			const auto& config = Config::Get();
			const auto& io = ImGui::GetIO();
			const float W = io.DisplaySize.x;
			const float H = io.DisplaySize.y;
			if (W <= 0.0f || H <= 0.0f) {
				return;
			}

			// All metrics are the approved 2160p mockup values, scaled.
			const float s = (H / 2160.0f) * config.hintScale;
			const float circleD = 46.0f * s;
			const float pillH = 40.0f * s;
			const float gapGlyphLabel = 10.0f * s;
			const float gapItem = 34.0f * s;
			const float padX = 28.0f * s;
			const float barH = 74.0f * s;
			const float labelSize = 32.0f * s;
			const float letterSize = 30.0f * s;
			const float pillTextSize = 26.0f * s;

			ImFont* labelFont = g_fontRegular ? g_fontRegular : ImGui::GetFont();
			ImFont* boldFont = g_fontBold ? g_fontBold : labelFont;

			const bool ps = UsePSGlyphs();

			std::scoped_lock lock{ g_itemsMutex };
			if (g_items.empty()) {
				return;
			}

			// measure
			struct Measured
			{
				float      glyphW;
				float      labelW;
				GlyphStyle style;
			};
			std::vector<Measured> measured;
			measured.reserve(g_items.size());
			float total = padX * 2.0f + gapItem * static_cast<float>(g_items.size() - 1);
			for (const auto& item : g_items) {
				auto  style = StyleFor(item.glyph, ps);
				float glyphW = circleD;
				if (style.pill) {
					glyphW = boldFont->CalcTextSizeA(pillTextSize, FLT_MAX, 0.0f, style.pillText).x + 28.0f * s;
				}
				const float labelW = labelFont->CalcTextSizeA(labelSize, FLT_MAX, 0.0f, item.label.c_str()).x;
				measured.push_back({ glyphW, labelW, style });
				total += glyphW + gapGlyphLabel + labelW;
			}

			const float right = config.hintAnchorX * W;
			const float bottom = config.hintAnchorY * H;
			float       x = (std::max)(0.0f, right - total);
			const float y0 = bottom - barH;
			const float cy = y0 + barH / 2.0f;

			auto* draw = ImGui::GetForegroundDrawList();

			draw->AddRectFilled({ x, y0 }, { x + total, y0 + barH }, IM_COL32(8, 8, 10, 150), 18.0f * s);
			draw->AddRect({ x, y0 }, { x + total, y0 + barH }, IM_COL32(255, 255, 255, 60), 18.0f * s, 0, 2.0f * s);

			x += padX;
			const ImU32 labelColor = IM_COL32(232, 228, 216, 235);
			const ImU32 glyphFill = IM_COL32(20, 20, 24, 200);

			for (std::size_t i = 0; i < g_items.size(); ++i) {
				const auto& item = g_items[i];
				const auto& m = measured[i];

				if (m.style.pill) {
					const ImVec2 p0{ x, cy - pillH / 2.0f };
					const ImVec2 p1{ x + m.glyphW, cy + pillH / 2.0f };
					draw->AddRectFilled(p0, p1, glyphFill, 12.0f * s);
					draw->AddRect(p0, p1, IM_COL32(170, 170, 175, 220), 12.0f * s, 0, 3.0f * s);
					const ImVec2 ts = boldFont->CalcTextSizeA(pillTextSize, FLT_MAX, 0.0f, m.style.pillText);
					draw->AddText(boldFont, pillTextSize,
						{ x + (m.glyphW - ts.x) / 2.0f, cy - ts.y / 2.0f },
						IM_COL32(255, 255, 255, 255), m.style.pillText);
				} else {
					const ImVec2 center{ x + circleD / 2.0f, cy };
					const float  r = circleD / 2.0f;
					draw->AddCircleFilled(center, r, glyphFill);
					draw->AddCircle(center, r, m.style.color, 0, 3.5f * s);
					if (m.style.psShape != 0) {
						const float e = r * 0.45f;  // symbol extent
						const float t = 3.0f * s;   // symbol stroke
						switch (m.style.psShape) {
						case 1:  // cross
							draw->AddLine({ center.x - e, center.y - e }, { center.x + e, center.y + e }, m.style.color, t);
							draw->AddLine({ center.x - e, center.y + e }, { center.x + e, center.y - e }, m.style.color, t);
							break;
						case 2:  // circle
							draw->AddCircle(center, e, m.style.color, 0, t);
							break;
						case 3:  // square
							draw->AddRect({ center.x - e, center.y - e }, { center.x + e, center.y + e }, m.style.color, 0.0f, 0, t);
							break;
						case 4:  // triangle
							draw->AddTriangle(
								{ center.x, center.y - e * 1.15f },
								{ center.x + e * 1.1f, center.y + e * 0.85f },
								{ center.x - e * 1.1f, center.y + e * 0.85f },
								m.style.color, t);
							break;
						}
					} else {
						const char   letter[2]{ m.style.letter, '\0' };
						const ImVec2 ts = boldFont->CalcTextSizeA(letterSize, FLT_MAX, 0.0f, letter);
						draw->AddText(boldFont, letterSize,
							{ center.x - ts.x / 2.0f, center.y - ts.y / 2.0f - 1.0f * s },
							m.style.color, letter);
					}
				}

				const float lx = x + m.glyphW + gapGlyphLabel;
				const ImVec2 ts = labelFont->CalcTextSizeA(labelSize, FLT_MAX, 0.0f, item.label.c_str());
				draw->AddText(labelFont, labelSize, { lx, cy - ts.y / 2.0f }, labelColor, item.label.c_str());

				x += m.glyphW + gapGlyphLabel + m.labelW + gapItem;
			}
		}

		// ---- hooks ------------------------------------------------------------

		void LoadFonts()
		{
			auto& io = ImGui::GetIO();

			char winDir[MAX_PATH]{};
			if (GetWindowsDirectoryA(winDir, MAX_PATH) != 0) {
				const std::string fonts = std::string{ winDir } + "\\Fonts\\";
				const std::string regular = fonts + "segoeui.ttf";
				const std::string bold = fonts + "seguisb.ttf";
				g_fontRegular = io.Fonts->AddFontFromFileTTF(regular.c_str(), 64.0f);
				g_fontBold = io.Fonts->AddFontFromFileTTF(bold.c_str(), 64.0f);
			}
			if (!g_fontRegular) {
				g_fontRegular = io.Fonts->AddFontDefault();
			}
			if (!g_fontBold) {
				g_fontBold = g_fontRegular;
			}
		}

		struct D3DInitHook
		{
			static void thunk()
			{
				func();

				auto* renderer = RE::BSGraphics::Renderer::GetSingleton();
				if (!renderer) {
					logger::error("overlay: no renderer singleton, glyph bar disabled");
					return;
				}
				// CommonLibSSE-NG 7.x moved the renderer state behind a runtime-offset accessor.
				auto& data = renderer->GetRuntimeData();

				auto* swapChain = reinterpret_cast<IDXGISwapChain*>(data.renderWindows[0].swapChain);
				if (!swapChain) {
					logger::error("overlay: no swap chain, glyph bar disabled");
					return;
				}

				DXGI_SWAP_CHAIN_DESC sd{};
				if (FAILED(swapChain->GetDesc(&sd))) {
					logger::error("overlay: IDXGISwapChain::GetDesc failed, glyph bar disabled");
					return;
				}

				auto* device = reinterpret_cast<ID3D11Device*>(data.forwarder);
				auto* context = reinterpret_cast<ID3D11DeviceContext*>(data.context);
				if (!device || !context) {
					logger::error("overlay: no d3d device/context, glyph bar disabled");
					return;
				}

				ImGui::CreateContext();
				ImGui::GetIO().IniFilename = nullptr;  // no imgui.ini
				if (!ImGui_ImplWin32_Init(sd.OutputWindow)) {
					logger::error("overlay: ImGui Win32 init failed, glyph bar disabled");
					return;
				}
				if (!ImGui_ImplDX11_Init(device, context)) {
					logger::error("overlay: ImGui DX11 init failed, glyph bar disabled");
					return;
				}

				LoadFonts();

				g_ready.store(true);
				logger::info("overlay: ImGui initialized on the game's swap chain");
			}

			static inline REL::Relocation<decltype(thunk)> func;

			static constexpr auto id = REL::RelocationID(75595, 77226);
			static constexpr auto offset = REL::VariantOffset(0x9, 0x275, 0x00);
		};

		struct PresentHook
		{
			static void thunk(std::uint32_t a_p1)
			{
				func(a_p1);

				if (!g_ready.load() || !g_visible.load() || g_hiddenByUser.load()) {
					return;
				}

				ImGui_ImplDX11_NewFrame();
				ImGui_ImplWin32_NewFrame();
				ImGui::NewFrame();

				Draw();

				ImGui::EndFrame();
				ImGui::Render();
				ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
			}

			static inline REL::Relocation<decltype(thunk)> func;

			static constexpr auto id = REL::RelocationID(75461, 77246);
			static constexpr auto offset = REL::Offset(0x9);
		};

		template <class T>
		void WriteThunkCall()
		{
			auto&                                 trampoline = SKSE::GetTrampoline();
			const REL::Relocation<std::uintptr_t> hook{ T::id, T::offset };
			T::func = trampoline.write_call<5>(hook.address(), T::thunk);
		}
	}

	void Install()
	{
		WriteThunkCall<D3DInitHook>();
		WriteThunkCall<PresentHook>();
		logger::info("overlay: render hooks installed");
	}

	void OnSceneStart()
	{
		if (!Config::Get().hintEnabled) {
			return;
		}
		BuildItems();
		g_hiddenByUser.store(false);
		g_visible.store(true);
	}

	void OnSceneEnd()
	{
		g_visible.store(false);
	}

	void NotifyHideUI()
	{
		g_hiddenByUser.store(!g_hiddenByUser.load());
	}
}
