#include "AutoCombatLink.h"
#include "Dodge.h"
#include "Settings.h"

#include <spdlog/sinks/basic_file_sink.h>

namespace
{
	void InitLogging()
	{
		auto path = SKSE::log::log_directory();
		if (!path) {
			return;
		}
		*path /= "AutoCombatDodge.log";
		auto sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(path->string(), true);
		auto log = std::make_shared<spdlog::logger>("global", std::move(sink));
		log->set_level(spdlog::level::info);
		log->flush_on(spdlog::level::debug);
		spdlog::set_default_logger(std::move(log));
		spdlog::set_pattern("[%H:%M:%S.%e] [%l] %v");
	}

	void ApplyLogLevel()
	{
		switch (ACD::Settings::Get().logLevel) {
		case 0:
			spdlog::set_level(spdlog::level::warn);
			break;
		case 2:
			spdlog::set_level(spdlog::level::debug);
			break;
		default:
			spdlog::set_level(spdlog::level::info);
			break;
		}
	}

	void MessageHandler(SKSE::MessagingInterface::Message* a_msg)
	{
		switch (a_msg->type) {
		case SKSE::MessagingInterface::kPostLoad:
			ACD::AutoCombat::Init();
			break;
		case SKSE::MessagingInterface::kInputLoaded:
			ACD::AutoCombat::RegisterInputSink();
			break;
		case SKSE::MessagingInterface::kDataLoaded:
			ACD::Dodge::OnDataLoaded();
			break;
		case SKSE::MessagingInterface::kNewGame:
		case SKSE::MessagingInterface::kPostLoadGame:
			ACD::Dodge::Reset();
			ACD::AutoCombat::ResetMirror();
			break;
		default:
			break;
		}
	}
}

SKSEPluginInfo(
	.Version = REL::Version{ 1, 0, 0, 0 },
	.Name = "AutoCombatDodge"sv,
	.Author = "Authoria"sv,
	.StructCompatibility = SKSE::StructCompatibility::Independent,
	.RuntimeCompatibility = SKSE::VersionIndependence::AddressLibrary)

SKSEPluginLoad(const SKSE::LoadInterface* a_skse)
{
	InitLogging();
	SKSE::Init(a_skse, false);

	logger::info("AutoCombatDodge 1.0.0 loading");

	if (REL::Module::IsVR()) {
		logger::error("Skyrim VR is not supported (the PlayerCharacter::Update slot differs) - not loading");
		return false;
	}

	auto& cfg = ACD::Settings::Get();
	cfg.Load();
	ApplyLogLevel();
	cfg.LogSummary();

	if (!cfg.enabled) {
		logger::info("Enabled=0 in AutoCombatDodge.ini - nothing installed");
		return true;
	}

	ACD::Dodge::InstallHook();

	if (!SKSE::GetMessagingInterface()->RegisterListener(MessageHandler)) {
		logger::error("could not register the SKSE message listener");
		return false;
	}
	return true;
}
