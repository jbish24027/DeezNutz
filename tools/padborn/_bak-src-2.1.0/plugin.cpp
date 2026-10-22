#include "Camera.h"
#include "Config.h"
#include "InputRouter.h"
#include "OStimBridge.h"
#include "Overlay.h"
#include "PCH.h"
#include "Sprint.h"

#include <spdlog/sinks/basic_file_sink.h>

namespace
{
	// True once kDataLoaded has confirmed OStim.esp is in the load order. On a
	// profile without OStim the whole scene layer (input lockout, key reservation,
	// glyph bar) stays dormant: no hooksite traffic, no warnings, nothing drawn.
	bool g_ostimPresent = false;

	void InitLogging()
	{
		auto path = SKSE::log::log_directory();
		if (!path) {
			return;
		}

		*path /= "Padborn.log";

		auto sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(path->string(), true);
		auto log = std::make_shared<spdlog::logger>("global", std::move(sink));
		log->set_level(spdlog::level::info);
		log->flush_on(spdlog::level::info);

		spdlog::set_default_logger(std::move(log));
		spdlog::set_pattern("[%H:%M:%S.%e] [%l] %v");
	}

	void MessageHandler(SKSE::MessagingInterface::Message* a_message)
	{
		switch (a_message->type) {
		case SKSE::MessagingInterface::kInputLoaded:
			OPad::Sprint::Register();
			break;

		case SKSE::MessagingInterface::kDataLoaded:
			OPad::Sprint::ApplyButton();
			{
				auto* handler = RE::TESDataHandler::GetSingleton();
				g_ostimPresent = handler && handler->LookupModByName("OStim.esp") != nullptr;
			}
			if (g_ostimPresent) {
				OPad::OStimBridge::Get().ResolveGlobals();
				OPad::OStimBridge::Get().Connect();
				OPad::InputRouter::Get().Install();
			} else {
				logger::info("OStim.esp not in the load order - scene layer dormant");
			}
			break;

		case SKSE::MessagingInterface::kPostLoadGame:
		case SKSE::MessagingInterface::kNewGame:
			// the engine can rebuild mappings from the controlmap files on load
			OPad::Sprint::ApplyButton();
			if (!g_ostimPresent) {
				break;
			}
			// OStim rebuilds its interface map per session; reconnecting is a no-op if
			// the listeners are already registered.
			OPad::OStimBridge::Get().Connect();
			if (OPad::Config::Get().reserveCollidingKeys) {
				OPad::OStimBridge::Get().ReserveKeys();
			}
			break;

		default:
			break;
		}
	}
}

SKSEPluginInfo(
	.Version = REL::Version{ 2, 1, 0, 0 },
	.Name = "Padborn"sv,
	.Author = "Authoria"sv,
	.StructCompatibility = SKSE::StructCompatibility::Independent,
	.RuntimeCompatibility = SKSE::VersionIndependence::AddressLibrary)

SKSEPluginLoad(const SKSE::LoadInterface* a_skse)
{
	InitLogging();
	SKSE::Init(a_skse);

	logger::info("Padborn 2.1.0 loading (sprint rescue + OStim pad layer + glyph bar + first-person block)");

	// Config is pure file I/O, and the sprint module needs it at kInputLoaded,
	// which fires before kDataLoaded — so load it here.
	OPad::Config::Get().Load();

	// One pool for every hook Padborn writes: the input dispatch call (14) plus the
	// two render hooks (2 x 14). A second AllocTrampoline REPLACES the pool, so the
	// per-installer allocs were consolidated here.
	SKSE::AllocTrampoline(64);

	// Render hooks must exist before the renderer initializes, so this cannot wait
	// for kDataLoaded. Drawing still only happens while an OStim scene runs.
	OPad::Overlay::Install();

	// Engine-function detours + two vtable writes; needs no trampoline space and
	// no game data, so it goes in at load like the render hooks.
	OPad::Camera::Install();

	if (!SKSE::GetMessagingInterface()->RegisterListener(MessageHandler)) {
		logger::error("could not register the SKSE message listener");
		return false;
	}

	return true;
}
