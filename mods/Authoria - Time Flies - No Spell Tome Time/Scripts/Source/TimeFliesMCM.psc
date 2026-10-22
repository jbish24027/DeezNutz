Scriptname TimeFliesMCM extends SKI_ConfigBase

TimeFliesMain Property main Auto
TimeFliesMods Property mods Auto

bool debug_mode = True
Function _debug(string str)
    if debug_mode
        Debug.Trace("Time Flies MCM: " + str)
    endif
EndFunction

Event OnConfigInit()
    mods.prepare_pages()
    main.is_enabled = False
    load_defaults()
    initialize()
    _debug("Initialized for the first time")
EndEvent

int Function GetVersion()
    return 8 ;; increases version number if new mod(s) support added
EndFunction

Event OnVersionUpdate(int version)
    ;; if added support for new mods, things needed to do:
    ;; 1. re-prepare menu pages;
    ;; 2. initialize related settings for mods recently supported;
    mods.prepare_pages()
    mods.update(version)
	mods.initialize()
	_debug("OnVersionUpdate initaialize")
	showVersionMessage()
EndEvent

Function showVersionMessage()
	Utility.Wait(1.0)
	Debug.Notification("Time Flies updated to version " + GetVersion())
	_debug("Updated to version" + GetVersion())
EndFunction

Function initialize()
    _debug("Initializing...")
    if main.is_enabled
        ;; always tracks those menus because related options were removed
        registerForMenu("Book Menu")
		registerForMenu("Lockpicking Menu")
		registerForMenu("InventoryMenu")
        registerForMenu("Training Menu")
        registerForMenu("ContainerMenu")
		registerForMenu("BarterMenu")
		registerForMenu("GiftMenu")
		registerForMenu("Sleep/Wait Menu")
		registerForMenu("MessageBoxMenu")
		registerForMenu("Dialogue Menu")
		registerForMenu("Loading Menu")
		
        if main.crafting_takes_time
            registerForMenu("Crafting Menu")
        else
            unregisterForMenu("Crafting Menu")
        endif
				
        ;; initialize other mods
		mods.prepare_pages()
		mods.initialize()
		
		;; final initialization
		main.is_paused = False
		register_hotkey()
		registerForKey(18)	;; listener for key that may activate crafting menu
		registerForKey(276)
		_debug("Initialized")
    else
        unregisterForAllMenus()
    endif
	
	;; Baseline iron crafting items
	helm = Game.getFormFromFile(0x12e4d, "Skyrim.esm")
	cuirass = Game.getFormFromFile(0x12e49, "Skyrim.esm")
	gauntlets = Game.getFormFromFile(0x12e46, "Skyrim.esm")
	boots = Game.getFormFromFile(0x12e4b, "Skyrim.esm")
	shield = Game.getFormFromFile(0x12eb6, "Skyrim.esm")
	bow = Game.getFormFromFile(0x13985, "Skyrim.esm")	
	dagger = Game.getFormFromFile(0x1397e, "Skyrim.esm")
	sword = Game.getFormFromFile(0x12eb7, "Skyrim.esm")
	greatsword = Game.getFormFromFile(0x1359d, "Skyrim.esm")
	waraxe = Game.getFormFromFile(0x13790, "Skyrim.esm")
	battleaxe = Game.getFormFromFile(0x13980, "Skyrim.esm")
	mace = Game.getFormFromFile(0x13982, "Skyrim.esm")
	warhammer = Game.getFormFromFile(0x13981, "Skyrim.esm")		
	arrow = Game.getFormFromFile(0x1397d, "Skyrim.esm")

	;; Baseline deadric crafting items
	helm_d = Game.getFormFromFile(0x1396d, "Skyrim.esm")
	cuirass_d = Game.getFormFromFile(0x1396b, "Skyrim.esm")
	gauntlets_d = Game.getFormFromFile(0x1396c, "Skyrim.esm")
	boots_d = Game.getFormFromFile(0x1396a, "Skyrim.esm")
	shield_d = Game.getFormFromFile(0x1396e, "Skyrim.esm")
	bow_d = Game.getFormFromFile(0x139b5, "Skyrim.esm")	
	dagger_d = Game.getFormFromFile(0x139b6, "Skyrim.esm")
	sword_d = Game.getFormFromFile(0x139b9, "Skyrim.esm")
	greatsword_d = Game.getFormFromFile(0x139b7, "Skyrim.esm")
	waraxe_d = Game.getFormFromFile(0x139b3, "Skyrim.esm")
	battleaxe_d = Game.getFormFromFile(0x139b4, "Skyrim.esm")
	mace_d = Game.getFormFromFile(0x139b8, "Skyrim.esm")
	warhammer_d = Game.getFormFromFile(0x139ba, "Skyrim.esm")		
	arrow_d = Game.getFormFromFile(0x139c0, "Skyrim.esm")
	
	;; Populate iron item gold values
	main.helm_ival = helm.getGoldValue()
	main.cuirass_ival = cuirass.getGoldValue()
	main.gauntlets_ival = gauntlets.getGoldValue()
	main.boots_ival = boots.getGoldValue()
	main.shield_ival = shield.getGoldValue()
	main.bow_ival = bow.getGoldValue()	
	main.dagger_ival = dagger.getGoldValue()
	main.sword_ival = sword.getGoldValue()
	main.greatsword_ival = greatsword.getGoldValue()
	main.waraxe_ival = waraxe.getGoldValue()
	main.battleaxe_ival = battleaxe.getGoldValue()
	main.mace_ival = mace.getGoldValue()
	main.warhammer_ival = warhammer.getGoldValue()
	main.ammo_ival = arrow.getGoldValue()
	
	;; Populate baseline daedric item gold values
	main.helm_dval = helm_d.getGoldValue()
	main.cuirass_dval = cuirass_d.getGoldValue()
	main.gauntlets_dval = gauntlets_d.getGoldValue()
	main.boots_dval = boots_d.getGoldValue()
	main.shield_dval = shield_d.getGoldValue()
	main.bow_dval = bow_d.getGoldValue()	
	main.dagger_dval = dagger_d.getGoldValue()
	main.sword_dval = sword_d.getGoldValue()
	main.greatsword_dval = greatsword_d.getGoldValue()
	main.waraxe_dval = waraxe_d.getGoldValue()
	main.battleaxe_dval = battleaxe_d.getGoldValue()
	main.mace_dval = mace_d.getGoldValue()
	main.warhammer_dval = warhammer_d.getGoldValue()
	main.ammo_dval = arrow_d.getGoldValue()
	
	;; Modded action items
	shovel_list = new Form[2]
	shovel_list[0] = Game.getFormFromFile(0xF5D05, "Skyrim.esm")
	shovel_list[1] = Game.getFormFromFile(0xF5D06, "Skyrim.esm")
	
	pray = new Form[2]
	pray[0] = Game.getFormFromFile(0x3A9AF6, "Pilgrim.esp")
	pray[1] = Game.getFormFromFile(0xF945, "Wintersun - Faiths of Skyrim.esp")
		
	frostbite = new Form[4]
	frostbite[0] = Game.getFormFromFile(0x62FEC, "Frostfall.esp")
	frostbite[1] = Game.getFormFromFile(0x68121, "Frostfall.esp")
	frostbite[2] = Game.getFormFromFile(0x68123, "Frostfall.esp")
	frostbite[3] = Game.getFormFromFile(0x68125, "Frostfall.esp")
	
	caco_ws = new Form[49]	
	;;waterskins
    caco_ws[0] = Game.getFormFromFile(0x4DE9AD, "SunHelmSurvival.esp")
    caco_ws[1] = Game.getFormFromFile(0x4DE9AE, "SunHelmSurvival.esp")
    caco_ws[2] = Game.getFormFromFile(0x4DE9AF, "SunHelmSurvival.esp")
	caco_ws[3] = Game.getFormFromFile(0x4DE9B0, "SunHelmSurvival.esp")
	caco_ws[4] = Game.getFormFromFile(0x4EDCC1, "SunHelmSurvival.esp")
	caco_ws[5] = Game.getFormFromFile(0x4E3ABC, "SunHelmSurvival.esp")
	caco_ws[6] = Game.getFormFromFile(0x534AC3, "SunHelmSurvival.esp")
	caco_ws[7] = Game.getFormFromFile(0x438C, "iNeed.esp")
    caco_ws[8] = Game.getFormFromFile(0x587B6, "iNeed.esp")
    caco_ws[9] = Game.getFormFromFile(0x4376, "iNeed.esp")
	caco_ws[10] = Game.getFormFromFile(0x437D, "iNeed.esp")
	caco_ws[11] = Game.getFormFromFile(0x437F, "iNeed.esp")
	caco_ws[12] = Game.getFormFromFile(0x3B2C5, "iNeed.esp")
	caco_ws[13] = Game.getFormFromFile(0x3B2C8, "iNeed.esp")
	caco_ws[14] = Game.getFormFromFile(0x3B2CC, "iNeed.esp")
	caco_ws[15] = Game.getFormFromFile(0x4E63, "iNeed.esp")
	caco_ws[16] = Game.getFormFromFile(0x4E64, "iNeed.esp")
	caco_ws[17] = Game.getFormFromFile(0x387B1, "iNeed.esp")
	caco_ws[18] = Game.getFormFromFile(0x3B2CF, "iNeed.esp")
	caco_ws[19] = Game.getFormFromFile(0x3B2D0, "iNeed.esp")
	caco_ws[20] = Game.getFormFromFile(0x3B2D1, "iNeed.esp")
	caco_ws[21] = Game.getFormFromFile(0x587B8, "iNeed.esp")
	caco_ws[22] = Game.getFormFromFile(0x20EA1, "iNeed - Extended.esp")
	caco_ws[23] = Game.getFormFromFile(0x20EA2, "iNeed - Extended.esp")
	caco_ws[24] = Game.getFormFromFile(0x20EA3, "iNeed - Extended.esp")	
	caco_ws[25] = Game.getFormFromFile(0x20EA4, "iNeed - Extended.esp")
	caco_ws[26] = Game.getFormFromFile(0x20EA5, "iNeed - Extended.esp")
	caco_ws[27] = Game.getFormFromFile(0x10895, "LastSeed.esp")
    caco_ws[28] = Game.getFormFromFile(0x1088F, "LastSeed.esp")
    caco_ws[29] = Game.getFormFromFile(0x10891, "LastSeed.esp")
	caco_ws[30] = Game.getFormFromFile(0x10893, "LastSeed.esp")
	caco_ws[31] = Game.getFormFromFile(0x10894, "LastSeed.esp")
	caco_ws[32] = Game.getFormFromFile(0x1088E, "LastSeed.esp")
	caco_ws[33] = Game.getFormFromFile(0x10890, "LastSeed.esp")
	caco_ws[34] = Game.getFormFromFile(0x10892, "LastSeed.esp")
	caco_ws[35] = Game.getFormFromFile(0x2FCDA9, "LastSeed.esp")
	caco_ws[36] = Game.getFormFromFile(0x10897, "LastSeed.esp")
	caco_ws[37] = Game.getFormFromFile(0x10898, "LastSeed.esp")
	caco_ws[38] = Game.getFormFromFile(0x1089D, "LastSeed.esp")
	caco_ws[39] = Game.getFormFromFile(0x1089E, "LastSeed.esp")
	caco_ws[40] = Game.getFormFromFile(0x2D9662, "LastSeed.esp")
	caco_ws[41] = Game.getFormFromFile(0x2D9663, "LastSeed.esp")
	caco_ws[42] = Game.getFormFromFile(0x2D9664, "LastSeed.esp")
	caco_ws[43] = Game.getFormFromFile(0x2D9665, "LastSeed.esp")
	caco_ws[44] = Game.getFormFromFile(0x2D9666, "LastSeed.esp")
	caco_ws[45] = Game.getFormFromFile(0x2D9667, "LastSeed.esp")
	caco_ws[46] = Game.getFormFromFile(0x2D9668, "LastSeed.esp")
	caco_ws[47] = Game.getFormFromFile(0xFCDAB, "LastSeed.esp")
	caco_ws[48] = Game.getFormFromFile(0x2FCDAC, "LastSeed.esp")
	
	caco_tokens = new Form[90]
	;;salt
	caco_tokens[0] = Game.getFormFromFile(0x34CDF, "Skyrim.esm")	
	caco_tokens[1] = Game.getFormFromFile(0xCCA101, "Update.esm")	
	caco_tokens[2] = Game.getFormFromFile(0x4B633B, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[3] = Game.getFormFromFile(0x50750A, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[4] = Game.getFormFromFile(0x50750B, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[5] = Game.getFormFromFile(0x50750D, "Complete Alchemy & Cooking Overhaul.esp")
	;;water
	caco_tokens[6] = Game.getFormFromFile(0xCCA100, "Update.esm")
	caco_tokens[7] = Game.getFormFromFile(0xCCA111, "Update.esm")
	caco_tokens[8] = Game.getFormFromFile(0x4E3D21, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[9] = Game.getFormFromFile(0x4E3D23, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[10] = Game.getFormFromFile(0x4E3D25, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[11] = Game.getFormFromFile(0x4E3D27, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[12] = Game.getFormFromFile(0x4E3D29, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[12] = Game.getFormFromFile(0x4E3D2B, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[14] = Game.getFormFromFile(0x4E3D2D, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[15] = Game.getFormFromFile(0x97AFB6, "Complete Alchemy & Cooking Overhaul.esp")
	;;wine(villagered)
	caco_tokens[16] = Game.getFormFromFile(0x3133C, "Skyrim.esm")
	caco_tokens[17] = Game.getFormFromFile(0xCCA105, "Update.esm")
	caco_tokens[18] = Game.getFormFromFile(0x2EE529, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[19] = Game.getFormFromFile(0x2EE52B, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[20] = Game.getFormFromFile(0x2EE52D, "Complete Alchemy & Cooking Overhaul.esp")
	;;wine(villagewhite)
	caco_tokens[21] = Game.getFormFromFile(0xC5348, "Skyrim.esm")
	caco_tokens[22] = Game.getFormFromFile(0xCCA104, "Update.esm")
	caco_tokens[23] = Game.getFormFromFile(0x2EE52F, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[24] = Game.getFormFromFile(0x2EE531, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[25] = Game.getFormFromFile(0x2EE533, "Complete Alchemy & Cooking Overhaul.esp")
	;;wine(altonoir)
	caco_tokens[26] = Game.getFormFromFile(0x3133B, "Skyrim.esm")
	caco_tokens[27] = Game.getFormFromFile(0xCCA107, "Update.esm")
	caco_tokens[28] = Game.getFormFromFile(0x2BBAC6, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[29] = Game.getFormFromFile(0x2BBAC7, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[30] = Game.getFormFromFile(0x2BBAC9, "Complete Alchemy & Cooking Overhaul.esp")
	;;wine(altoblanc)
	caco_tokens[31] = Game.getFormFromFile(0xC5349, "Skyrim.esm")
	caco_tokens[32] = Game.getFormFromFile(0xCCA106, "Update.esm")
	caco_tokens[33] = Game.getFormFromFile(0x2EE520, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[34] = Game.getFormFromFile(0x2EE522, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[35] = Game.getFormFromFile(0x2EE524, "Complete Alchemy & Cooking Overhaul.esp")
	;;oil
	caco_tokens[36] = Game.getFormFromFile(0xCCA124, "Update.esm")
	caco_tokens[37] = Game.getFormFromFile(0x9E0567, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[38] = Game.getFormFromFile(0x9E056A, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[39] = Game.getFormFromFile(0x9E056C, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[40] = Game.getFormFromFile(0x9E056E, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[41] = Game.getFormFromFile(0x9E0584, "Complete Alchemy & Cooking Overhaul.esp")
	;;vinegar
	caco_tokens[42] = Game.getFormFromFile(0xCCA125, "Update.esm")
	caco_tokens[43] = Game.getFormFromFile(0x9E0568, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[44] = Game.getFormFromFile(0x9E0570, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[45] = Game.getFormFromFile(0x9E0572, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[46] = Game.getFormFromFile(0x9E0574, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[47] = Game.getFormFromFile(0x9E0583, "Complete Alchemy & Cooking Overhaul.esp")
	;;barleyflour
	caco_tokens[48] = Game.getFormFromFile(0xCCA103, "Update.esm")
	caco_tokens[49] = Game.getFormFromFile(0x52ACD4, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[50] = Game.getFormFromFile(0x52ACD6, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[51] = Game.getFormFromFile(0x52ACD8, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[52] = Game.getFormFromFile(0x52ACDA, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[53] = Game.getFormFromFile(0x52ACDC, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[54] = Game.getFormFromFile(0x52ACDE, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[55] = Game.getFormFromFile(0x52ACE0, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[56] = Game.getFormFromFile(0x52ACE2, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[57] = Game.getFormFromFile(0x52ACE4, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[58] = Game.getFormFromFile(0x52ACE6, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[59] = Game.getFormFromFile(0x52ACE8, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[60] = Game.getFormFromFile(0x52ACEA, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[61] = Game.getFormFromFile(0x52ACEC, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[62] = Game.getFormFromFile(0x52ACEE, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[63] = Game.getFormFromFile(0x52ACF0, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[64] = Game.getFormFromFile(0x52ACF2, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[65] = Game.getFormFromFile(0x52ACF4, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[66] = Game.getFormFromFile(0x52ACF6, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[67] = Game.getFormFromFile(0x52ACF8, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[68] = Game.getFormFromFile(0xA10116, "Complete Alchemy & Cooking Overhaul.esp")
	;;wheatflour
	caco_tokens[69] = Game.getFormFromFile(0xCCA102, "Update.esm")
	caco_tokens[70] = Game.getFormFromFile(0x3538, "HearthFires.esm")
	caco_tokens[71] = Game.getFormFromFile(0x5023C9, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[72] = Game.getFormFromFile(0x5023CB, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[73] = Game.getFormFromFile(0x5023CD, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[74] = Game.getFormFromFile(0x5023CF, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[75] = Game.getFormFromFile(0x5023D1, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[76] = Game.getFormFromFile(0x5023D3, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[77] = Game.getFormFromFile(0x5023D5, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[78] = Game.getFormFromFile(0x5023D7, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[79] = Game.getFormFromFile(0x5023D9, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[80] = Game.getFormFromFile(0x5023DB, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[81] = Game.getFormFromFile(0x5023DD, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[82] = Game.getFormFromFile(0x5023DF, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[83] = Game.getFormFromFile(0x5023E1, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[84] = Game.getFormFromFile(0x5023E3, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[85] = Game.getFormFromFile(0x5023E5, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[86] = Game.getFormFromFile(0x5023E7, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[87] = Game.getFormFromFile(0x5023E9, "Complete Alchemy & Cooking Overhaul.esp")
	caco_tokens[88] = Game.getFormFromFile(0x5023EA, "Complete Alchemy & Cooking Overhaul.esp")	
	caco_tokens[89] = Game.getFormFromFile(0x5023ED, "Complete Alchemy & Cooking Overhaul.esp")
	
	milk = Game.getFormFromFile(0x3534, "HearthFires.esm")
	butter = Game.getFormFromFile(0x353C, "HearthFires.esm")
	flour = Game.getFormFromFile(0x3538, "HearthFires.esm")
	leather = Game.getFormFromFile(0xDB5D2, "Skyrim.esm")
	firewood_campsite = Game.getFormFromFile(0x6F993, "Campsite.esp")
	
	;; Populate modded action items
	main.shovel_list = shovel_list
	main.pray = pray
	main.frostbite = frostbite
	main.caco_ws = caco_ws
	main.caco_tokens = caco_tokens
	main.milk = milk
	main.butter = butter
	main.flour = flour

	main.leather = leather
	main.firewood_campsite = firewood_campsite
			
EndFunction

Function load_defaults()
    ;; General
	main.expertise_reduces_time = True
	main.item_value_time = True
    main.random_crafting_time = True
    main.random_time_multiplier_min = 0.67
    main.random_time_multiplier_max = 1.0
	main.show_day_notification = True
    main.show_notification = True
    main.notification_threshold = 30.0
	main.show_transition = False
	main.show_fullscreen_transition = False
	main.transition_threshold = 2.0
	main.transition_duration = 5.0
	main.skinning_enabled = False
    main.hotkey = 0
	
	;; Combat
	main.block_controls = False
	main.combat_warning = False
	main.block_menus = False
	main.block_objects = False
	main.block_journal = False
	
    ;; Reading
    main.reading_time_multiplier = 1.0
    main.reading_increases_speech_multiplier = 1.0
    main.spell_learning_hour = 0.0    ;; Authoria: spell tomes take no time (was 2.0)

    ;; Training & Eating & Looting & Lockpicking & Trading
	main.scaled_training = False
    main.training_hour = 2.0
    main.eating_minute = 5.0
    main.lockpicking_time_multiplier = 1.0
    main.trading_time_multiplier = 1.0
    main.looting_time_multiplier = 1.0
	main.inventory_loot = False

    ;; Crafting
    main.crafting_takes_time = True
    main.helmet_crafting_hour = 3.0
    main.armor_crafting_hour = 6.0
    main.gauntlets_crafting_hour = 3.0
    main.boots_crafting_hour = 3.0
    main.shield_crafting_hour = 4.0
    main.clothes_crafting_hour = 2.0
    main.jewelry_crafting_hour = 2.5
	main.tool_crafting_hour = 1.0
	main.clutter_crafting_hour = 1.0
    main.staff_crafting_hour = 4.0
    main.bow_crafting_hour = 4.0
    main.ammo_crafting_hour = 1.5
    main.dagger_crafting_hour = 3.0
    main.sword_crafting_hour = 4.0
    main.waraxe_crafting_hour = 4.0
    main.mace_crafting_hour = 4.0
    main.greatsword_crafting_hour = 5.0
    main.battleaxe_crafting_hour = 5.0
    main.warhammer_crafting_hour = 5.0
    main.smelting_hour = 2.0
    main.leather_crafting_hour = 1.0
    main.armor_improving_minute = 15.0
    main.weapon_improving_minute = 15.0
    main.enchanting_hour = 1.0
    main.alchemy_minute = 30.0
    main.cooking_minute = 15.0
	main.harvesting_minute = 10.0
	main.lumbering_minute = 10.0
	main.milling_minute = 15.0
	main.mining_minute = 30.0
	main.skinning_minute = 10.0
	
	;; Modded Actions
	main.bury_hour = 2.0
	main.prayer_minute = 15.0
	
    ;; Other Mods
    mods.load_defaults()
EndFunction

Function register_hotkey()
    if main.hotkey
        registerForKey(main.hotkey)
    else
        unregisterForAllKeys()
    endif
EndFunction

Event OnOptionKeyMapChange(int option, int keycode, \
        string conflict_ctrl, string conflict_name)
    if conflict_ctrl != ""
        if conflict_name != ""
            showMessage("$key_already_mapped_to{" + conflict_ctrl \
                + "}{" + conflict_name + "}")
        else
            showMessage("$key_already_mapped_to{" + conflict_ctrl + "}")
        endif
        return
    endif

    if option == hotkey_id
        main.hotkey = keycode
        register_hotkey()
        forcePageReset()
    endif
EndEvent

Event OnKeyUp(int keycode, float hold_time)
    ;; hotkey only works in "normal" state
    if UI.isMenuOpen("Console") || Utility.isInMenuMode() \
            || Game.getPlayer().getSitState() != 0
        return
    elseif keycode == main.hotkey
        if !main.is_enabled
            Debug.notification("$mod_not_enabled")
            return
        endif

        if main.is_paused
            Debug.notification("$mod_resumed")
            main.is_paused = False
        else
            Debug.notification("$mod_paused")
            main.is_paused = True
        endif
    endif
EndEvent


import FISSFactory
FISSInterface Property fiss Auto
Function save_settings()
    fiss = FISSFactory.getFISS()
    if !fiss
        return
    endif

    _debug("Saving basic settings...")
    fiss.beginSave("TimeFlies.xml", "Time Flies")

    ;; General
	fiss.saveBool("expertise_reduces_time", main.expertise_reduces_time)
	fiss.saveBool("item_value_time", main.item_value_time)
    fiss.saveBool("random_crafting_time", main.random_crafting_time)
    fiss.saveFloat("random_time_multiplier_min", main.random_time_multiplier_min)
    fiss.saveFloat("random_time_multiplier_max", main.random_time_multiplier_max)
	fiss.saveBool("show_day_notification", main.show_day_notification)
    fiss.saveBool("show_notification", main.show_notification)
    fiss.saveFloat("notification_threshold", main.notification_threshold)
	fiss.saveBool("show_transition", main.show_transition)
	fiss.saveBool("show_fullscreen_transition", main.show_fullscreen_transition)
	fiss.saveFloat("transition_threshold", main.transition_threshold)
	fiss.saveFloat("transition_duration", main.transition_duration)
    fiss.saveInt("hotkey", main.hotkey)
	
	;; Combat
	fiss.saveBool("block_controls", main.block_controls)
	fiss.saveBool("block_menus", main.block_menus)
	fiss.saveBool("block_objects", main.block_objects)
	fiss.saveBool("block_journal", main.block_journal)
    
    ;; Reading
    fiss.saveFloat("reading_time_multiplier", main.reading_time_multiplier)
    fiss.saveFloat("reading_increases_speech_multiplier", main.reading_increases_speech_multiplier)
    fiss.saveFloat("spell_learning_hour", main.spell_learning_hour)

    ;; Training & Eating & Looting & Lockpicking & Trading
    fiss.saveFloat("training_hour", main.training_hour)
	fiss.saveBool("scaled_training", main.scaled_training)
    fiss.saveFloat("eating_minute", main.eating_minute)
    fiss.saveFloat("lockpicking_time_multiplier", main.lockpicking_time_multiplier)
    fiss.saveFloat("trading_time_multiplier", main.trading_time_multiplier)
	fiss.saveFloat("looting_time_multiplier", main.looting_time_multiplier)
	fiss.saveBool("inventory_loot", main.inventory_loot)

    ;; Crafting
    fiss.saveBool("crafting_takes_time", main.crafting_takes_time)
    fiss.saveFloat("helmet_crafting_hour", main.helmet_crafting_hour)
    fiss.saveFloat("armor_crafting_hour", main.armor_crafting_hour)
    fiss.saveFloat("gauntlets_crafting_hour", main.gauntlets_crafting_hour)
    fiss.saveFloat("boots_crafting_hour", main.boots_crafting_hour)
    fiss.saveFloat("shield_crafting_hour", main.shield_crafting_hour)
    fiss.saveFloat("clothes_crafting_hour", main.clothes_crafting_hour)
    fiss.saveFloat("jewelry_crafting_hour", main.jewelry_crafting_hour)
	fiss.saveFloat("tool_crafting_hour", main.tool_crafting_hour)
	fiss.saveFloat("clutter_crafting_hour", main.clutter_crafting_hour)
    fiss.saveFloat("staff_crafting_hour", main.staff_crafting_hour)
    fiss.saveFloat("bow_crafting_hour", main.bow_crafting_hour)
    fiss.saveFloat("ammo_crafting_hour", main.ammo_crafting_hour)
    fiss.saveFloat("dagger_crafting_hour", main.dagger_crafting_hour)
    fiss.saveFloat("sword_crafting_hour", main.sword_crafting_hour)
    fiss.saveFloat("waraxe_crafting_hour", main.waraxe_crafting_hour)
    fiss.saveFloat("mace_crafting_hour", main.mace_crafting_hour)
    fiss.saveFloat("greatsword_crafting_hour", main.greatsword_crafting_hour)
    fiss.saveFloat("battleaxe_crafting_hour", main.battleaxe_crafting_hour)
    fiss.saveFloat("warhammer_crafting_hour", main.warhammer_crafting_hour)
    fiss.saveFloat("smelting_hour", main.smelting_hour)
    fiss.saveFloat("leather_crafting_hour", main.leather_crafting_hour)
    fiss.saveFloat("armor_improving_minute", main.armor_improving_minute)
    fiss.saveFloat("weapon_improving_minute", main.weapon_improving_minute)
    fiss.saveFloat("enchanting_hour", main.enchanting_hour)
    fiss.saveFloat("alchemy_minute", main.alchemy_minute)
    fiss.saveFloat("cooking_minute", main.cooking_minute)
	fiss.saveFloat("harvesting_minute", main.harvesting_minute)
	fiss.saveFloat("lumbering_minute", main.lumbering_minute)
	fiss.saveFloat("milling_minute", main.milling_minute)
	fiss.saveFloat("mining_minute", main.mining_minute)
	fiss.saveBool("skinning_enabled", main.skinning_enabled)
	fiss.saveFloat("skinning_minute", main.skinning_minute)
	
	;; Modded Actions
	fiss.saveFloat("bury_hour", main.bury_hour)
	fiss.saveFloat("prayer_minute", main.prayer_minute)
	
    ;; Other Mods
    mods.save_settings()

    string result = fiss.endSave()
    if result != ""
        _debug("Saving finished with result - " + result)
    endif
EndFunction

Function load_settings()
    fiss = FISSFactory.getFISS()
    if !fiss
        return
    endif
    
    _debug("Loading settings...")
    fiss.beginLoad("TimeFlies.xml")

    ;; General
	main.expertise_reduces_time = fiss.loadBool("expertise_reduces_time")
	main.item_value_time = fiss.loadBool("item_value_time")
    main.random_crafting_time = fiss.loadBool("random_crafting_time")
    main.random_time_multiplier_min = fiss.loadFloat("random_time_multiplier_min")
    main.random_time_multiplier_max = fiss.loadFloat("random_time_multiplier_max")
    main.show_day_notification = fiss.loadBool("show_day_notification")
	main.show_notification = fiss.loadBool("show_notification")
    main.notification_threshold = fiss.loadFloat("notification_threshold")
	main.show_transition = fiss.loadBool("show_transition")
	main.show_fullscreen_transition = fiss.loadBool("show_fullscreen_transition")
	main.transition_threshold = fiss.loadFloat("transition_threshold")
	main.transition_duration = fiss.loadFloat("transition_duration")
    main.hotkey = fiss.loadInt("hotkey")
	
	;; Combat
	main.block_controls = fiss.loadBool("block_controls")
	main.block_menus = fiss.loadBool("block_menus")
	main.block_objects = fiss.loadBool("block_objects")
	main.block_journal = fiss.loadBool("block_journal")
	
    ;; Reading
    main.reading_time_multiplier = fiss.loadFloat("reading_time_multiplier")
    main.reading_increases_speech_multiplier = fiss.loadFloat("reading_increases_speech_multiplier")
    main.spell_learning_hour = fiss.loadFloat("spell_learning_hour")

    ;; Training & Eating & Looting & Lockpicking & Trading
    main.training_hour = fiss.loadFloat("training_hour")
	main.scaled_training = fiss.loadBool("scaled_training")
    main.eating_minute = fiss.loadFloat("eating_minute")
    main.lockpicking_time_multiplier = fiss.loadFloat("lockpicking_time_multiplier")
    main.trading_time_multiplier = fiss.loadFloat("trading_time_multiplier")
    main.looting_time_multiplier = fiss.loadFloat("looting_time_multiplier")
	main.inventory_loot = fiss.loadBool("inventory_loot")	

    ;; Crafting
    main.crafting_takes_time = fiss.loadBool("crafting_takes_time")
    main.helmet_crafting_hour = fiss.loadFloat("helmet_crafting_hour")
    main.armor_crafting_hour = fiss.loadFloat("armor_crafting_hour")
    main.gauntlets_crafting_hour = fiss.loadFloat("gauntlets_crafting_hour")
    main.boots_crafting_hour = fiss.loadFloat("boots_crafting_hour")
    main.shield_crafting_hour = fiss.loadFloat("shield_crafting_hour")
    main.clothes_crafting_hour = fiss.loadFloat("clothes_crafting_hour")
    main.jewelry_crafting_hour = fiss.loadFloat("jewelry_crafting_hour")
	main.tool_crafting_hour = fiss.loadFloat("tool_crafting_hour")
	main.clutter_crafting_hour = fiss.loadFloat("clutter_crafting_hour")
    main.staff_crafting_hour = fiss.loadFloat("staff_crafting_hour")
    main.bow_crafting_hour = fiss.loadFloat("bow_crafting_hour")
    main.ammo_crafting_hour = fiss.loadFloat("ammo_crafting_hour")
    main.dagger_crafting_hour = fiss.loadFloat("dagger_crafting_hour")
    main.sword_crafting_hour = fiss.loadFloat("sword_crafting_hour")
    main.waraxe_crafting_hour = fiss.loadFloat("waraxe_crafting_hour")
    main.mace_crafting_hour = fiss.loadFloat("mace_crafting_hour")
    main.greatsword_crafting_hour = fiss.loadFloat("greatsword_crafting_hour")
    main.battleaxe_crafting_hour = fiss.loadFloat("battleaxe_crafting_hour")
    main.warhammer_crafting_hour = fiss.loadFloat("warhammer_crafting_hour")
    main.smelting_hour = fiss.loadFloat("smelting_hour")
    main.leather_crafting_hour = fiss.loadFloat("leather_crafting_hour")
    main.armor_improving_minute = fiss.loadFloat("armor_improving_minute")
    main.weapon_improving_minute = fiss.loadFloat("weapon_improving_minute")
    main.enchanting_hour = fiss.loadFloat("enchanting_hour")
    main.alchemy_minute = fiss.loadFloat("alchemy_minute")
    main.cooking_minute = fiss.loadFloat("cooking_minute")
	main.harvesting_minute = fiss.loadFloat("harvesting_minute")
	main.lumbering_minute = fiss.loadFloat("lumbering_minute")
	main.milling_minute = fiss.loadFloat("milling_minute")
	main.mining_minute = fiss.loadFloat("mining_minute")
	main.skinning_enabled = fiss.loadFloat("skinning_enabled")
	main.skinning_minute = fiss.loadFloat("skinning_minute")
	
	;; Modded Actions
	main.bury_hour = fiss.loadFloat("bury_hour")
	main.prayer_minute = fiss.loadFloat("prayer_minute")

    ;; Other Mods
    mods.load_settings()

    string result = fiss.endLoad()
    if result != ""
        _debug("Loading finished with result - " + result)
    endif
    initialize()
EndFunction


;; General
int is_enabled_id
int expertise_reduces_time_id
int item_value_time_id
int random_crafting_time_id
int random_time_multiplier_min_id
int random_time_multiplier_max_id
int show_day_notification_id
int show_notification_id
int notification_threshold_id
int show_transition_id
int show_fullscreen_transition_id
int transition_threshold_id
int transition_duration_id
int save_id
int load_id
int load_defaults_id
int hotkey_id
int reinitialize_id
bool option_flag_enabled

;; Reading
int reading_time_multiplier_id
int reading_increases_speech_multiplier_id
int spell_learning_hour_id

;; Training & Eating & Looting & Trading
int scaled_training_id
int training_hour_id
int eating_minute_id
int lockpicking_time_multiplier_id
int trading_time_multiplier_id
int looting_time_multiplier_id
int inventory_loot_id

;; Crafting
int crafting_takes_time_id
int helmet_crafting_hour_id
int armor_crafting_hour_id
int gauntlets_crafting_hour_id
int boots_crafting_hour_id
int shield_crafting_hour_id
int leather_crafting_hour_id
int clothes_crafting_hour_id
int jewelry_crafting_hour_id
int tool_crafting_hour_id
int clutter_crafting_hour_id
int staff_crafting_hour_id
int bow_crafting_hour_id
int ammo_crafting_hour_id
int dagger_crafting_hour_id
int sword_crafting_hour_id
int waraxe_crafting_hour_id
int mace_crafting_hour_id
int greatsword_crafting_hour_id
int battleaxe_crafting_hour_id
int warhammer_crafting_hour_id
int smelting_hour_id
int armor_improving_minute_id
int weapon_improving_minute_id
int enchanting_hour_id
int alchemy_minute_id
int cooking_minute_id
int harvesting_minute_id
int lumbering_minute_id
int milling_minute_id
int mining_minute_id
int skinning_enabled_id
int skinning_minute_id

;; Crafted Items
Form dagger
Form dagger_d
Form sword
Form sword_d
Form greatsword
Form greatsword_d
Form waraxe
Form waraxe_d
Form battleaxe
Form battleaxe_d
Form mace
Form mace_d
Form warhammer
Form warhammer_d
Form bow
Form bow_d
Form arrow
Form arrow_d
Form helm
Form helm_d
Form cuirass
Form cuirass_d
Form gauntlets
Form gauntlets_d
Form boots
Form boots_d
Form shield
Form shield_d

;; Combat
int block_controls_id
int combat_warning_id
int block_menus_id
int block_objects_id
int block_journal_id

;; Modded Actions
int bury_hour_id
int prayer_minute_id
Form[] shovel_list
Form[] pray
Form[] frostbite
Form[] caco_ws
Form[] caco_tokens
Form milk
Form butter
Form flour
Form leather
Form firewood_campsite


Event OnPageReset(string page)
    if page == ""
        loadCustomContent("TimeFlies/TimeFlies.dds", 180, 120)
        return
    else
        unloadCustomContent()
    endif
		
    if page == "$general"
        setCursorFillMode(TOP_TO_BOTTOM)
        addHeaderOption("$header_options")
        is_enabled_id = addToggleOption("$enable?", main.is_enabled)
        
        show_notification_id = addToggleOption("$show_notification", \
            main.show_notification)
		if main.show_notification
			notification_threshold_id = addSliderOption( \
				"$notification_threshold", \
				main.notification_threshold, \
				"${0}min", OPTION_FLAG_NONE)
		else
			notification_threshold_id = addSliderOption( \
				"$notification_threshold", \
				main.notification_threshold, \
				"${0}min", OPTION_FLAG_DISABLED)
		endif
	
		show_day_notification_id = addToggleOption("$show_day_notification", \
            main.show_day_notification)
			
		addHeaderOption("$transitions")
		show_transition_id = addToggleOption("$show_transition", \
            main.show_transition)
		if main.show_transition 
			show_fullscreen_transition_id = addToggleOption("$show_fullscreen_transition", \
				main.show_fullscreen_transition, OPTION_FLAG_NONE)		
			transition_threshold_id = addSliderOption( \
				"$transition_threshold", \
				main.transition_threshold, \
				"${2}hour", OPTION_FLAG_NONE)
			transition_duration_id = addSliderOption( \
				"$transition_duration", \
				main.transition_duration, \
				"${0}sec", OPTION_FLAG_NONE)	
		else
			show_fullscreen_transition_id = addToggleOption("$show_fullscreen_transition", \
				main.show_fullscreen_transition, OPTION_FLAG_DISABLED)		
			transition_threshold_id = addSliderOption( \
				"$transition_threshold", \
				main.transition_threshold, \
				"${2}hour", OPTION_FLAG_DISABLED)
			transition_duration_id = addSliderOption( \
				"$transition_duration", \
				main.transition_duration, \
				"${0}sec", OPTION_FLAG_DISABLED)
		endif

		setCursorPosition(1)
		addHeaderOption("$hotkeys")
		hotkey_id = addKeyMapOption("$pause", main.hotkey)
		
        if main.is_paused
            addTextOption("", "$mod_paused")
        endif
		
        addHeaderOption("$save_and_load")
        fiss = FISSFactory.getFISS()
        int save_flag = OPTION_FLAG_NONE
        int load_flag = OPTION_FLAG_NONE

        if !fiss
            save_flag = OPTION_FLAG_DISABLED
            load_flag = OPTION_FLAG_DISABLED
        else
            fiss.beginLoad("TimeFlies.xml")
            if fiss.endLoad() != ""
                load_flag = OPTION_FLAG_DISABLED
            endif
        endif
        save_id = addTextOption("$save_current", "", save_flag)
        load_id = addTextOption("$load_saved", "", load_flag)
		load_defaults_id = addTextOption("$load_defaults", "", OPTION_FLAG_NONE)
        
        addHeaderOption("$maintenance")		
        reinitialize_id = addTextOption("$reinitialize", "", OPTION_FLAG_NONE)
				
	elseif page == "$crafting_config"
		setCursorFillMode(TOP_TO_BOTTOM)
        addHeaderOption("$header_options")
        crafting_takes_time_id = addToggleOption("$crafting_takes_time", \
            main.crafting_takes_time)
			
		expertise_reduces_time_id = addToggleOption( \
            "$expertise_reduces_time", main.expertise_reduces_time)
			
		item_value_time_id = addToggleOption( \
            "$item_value_time", main.item_value_time)
			
		setCursorPosition(1)
		addHeaderOption("$random")
		random_crafting_time_id = addToggleOption( \
            "$random_crafting_time", main.random_crafting_time)
		if main.random_crafting_time
			random_time_multiplier_min_id = addSliderOption( \
				"$random_time_multiplier_min", \
				main.random_time_multiplier_min, \
				"$x{2}", OPTION_FLAG_NONE)
			random_time_multiplier_max_id = addSliderOption( \
				"$random_time_multiplier_max", \
				main.random_time_multiplier_max, \
				"$x{2}", OPTION_FLAG_NONE)	
		else
			random_time_multiplier_min_id = addSliderOption( \
				"$random_time_multiplier_min", \
				main.random_time_multiplier_min, \
				"$x{2}", OPTION_FLAG_DISABLED)
			random_time_multiplier_max_id = addSliderOption( \
				"$random_time_multiplier_max", \
				main.random_time_multiplier_max, \
				"$x{2}", OPTION_FLAG_DISABLED)
		endif

    elseif page == "$crafting_times"
		setCursorFillMode(TOP_TO_BOTTOM)
        addHeaderOption("$armors")
        armor_improving_minute_id = addSliderOption( \
            "$armor_improving", main.armor_improving_minute, \
            "${0}min")
        boots_crafting_hour_id = addSliderOption( \
            "$boots", main.boots_crafting_hour, "${2}hour")
        armor_crafting_hour_id = addSliderOption( \
            "$cuirass", main.armor_crafting_hour, "${2}hour")			
        gauntlets_crafting_hour_id = addSliderOption( \
            "$gauntlets", main.gauntlets_crafting_hour, \
            "${2}hour")			
		helmet_crafting_hour_id = addSliderOption( \
            "$helmet", main.helmet_crafting_hour, "${2}hour")
        shield_crafting_hour_id = addSliderOption( \
            "$shield", main.shield_crafting_hour, "${2}hour")

        addHeaderOption("$others")
        alchemy_minute_id = addSliderOption( \
            "$alchemy", main.alchemy_minute, "${0}min")		
        clothes_crafting_hour_id = addSliderOption( \
            "$clothes", main.clothes_crafting_hour, \
            "${2}hour")
		clutter_crafting_hour_id = addSliderOption( \
            "$clutter", main.clutter_crafting_hour, \
            "${2}hour")			
        cooking_minute_id = addSliderOption( \
            "$cooking", main.cooking_minute, "${0}min")
		enchanting_hour_id = addSliderOption( \
            "$enchanting", main.enchanting_hour, "${2}hour")			
        jewelry_crafting_hour_id = addSliderOption( \
            "$jewelry", main.jewelry_crafting_hour, \
            "${2}hour")
		tool_crafting_hour_id = addSliderOption( \
            "$tool", main.tool_crafting_hour, \
            "${2}hour")

        setCursorPosition(1)
        addHeaderOption("$weapons")

		weapon_improving_minute_id = addSliderOption( \
            "$weapon_improving", main.weapon_improving_minute, \
            "${0}min")			
        ammo_crafting_hour_id = addSliderOption( \
            "$ammo", main.ammo_crafting_hour, "${2}hour")
        battleaxe_crafting_hour_id = addSliderOption( \
            "$battleaxe", main.battleaxe_crafting_hour, \
            "${2}hour")
		bow_crafting_hour_id = addSliderOption( \
            "$bow", main.bow_crafting_hour, "${2}hour")
        dagger_crafting_hour_id = addSliderOption( \
            "$dagger", main.dagger_crafting_hour, "${2}hour")
        greatsword_crafting_hour_id = addSliderOption( \
            "$greatsword", main.greatsword_crafting_hour, \
            "${2}hour")			
        mace_crafting_hour_id = addSliderOption( \
            "$mace", main.mace_crafting_hour, "${2}hour")
        staff_crafting_hour_id = addSliderOption( \
            "$staff", main.staff_crafting_hour, "${2}hour")			
        sword_crafting_hour_id = addSliderOption( \
            "$sword", main.sword_crafting_hour, "${2}hour")
        waraxe_crafting_hour_id = addSliderOption( \
            "$waraxe", main.waraxe_crafting_hour, "${2}hour")
        warhammer_crafting_hour_id = addSliderOption( \
            "$warhammer", main.warhammer_crafting_hour, \
            "${2}hour")
			
        addHeaderOption("$smelting_and_tanning")
        smelting_hour_id = addSliderOption( \
            "$smelting", main.smelting_hour, "${2}hour")
        leather_crafting_hour_id = addSliderOption( \
            "$tanning", main.leather_crafting_hour, \
            "${2}hour")

    elseif page == "$activities"
        setCursorFillMode(TOP_TO_BOTTOM)
        addHeaderOption("$multipliers")

        reading_time_multiplier_id = addSliderOption( \
            "$reading", main.reading_time_multiplier, \
            "$x{2}")
        reading_increases_speech_multiplier_id = addSliderOption( \
            "$reading_increases_speech", \
            main.reading_increases_speech_multiplier, "$x{2}")	
        lockpicking_time_multiplier_id = addSliderOption( \
            "$lockpicking", \
            main.lockpicking_time_multiplier, "$x{2}")			
        trading_time_multiplier_id = addSliderOption( \
            "$trading", main.trading_time_multiplier, \
            "$x{2}")
        looting_time_multiplier_id = addSliderOption( \
            "$looting", main.looting_time_multiplier, \
            "$x{2}")	
		inventory_loot_id = addToggleOption("$inventory_loot", \
            main.inventory_loot)			

        addHeaderOption("$improvement")
		spell_learning_hour_id = addSliderOption( \
            "$spell_learning", main.spell_learning_hour, "${2}hour")
        training_hour_id = addSliderOption( \
            "$training", main.training_hour, "${2}hour")
		scaled_training_id = addToggleOption("$scaled_training", \
            main.scaled_training)	
			
		setCursorPosition(1)
		addHeaderOption("$other_actions")
        eating_minute_id = addSliderOption("$eating", \
            main.eating_minute, "${0}min")
		harvesting_minute_id = addSliderOption( \
            "$harvesting", main.harvesting_minute, "${0}min")
		lumbering_minute_id = addSliderOption( \
            "$lumbering", main.lumbering_minute, "${0}min")	
		milling_minute_id = addSliderOption( \
            "$milling", main.milling_minute, "${0}min")				
		mining_minute_id = addSliderOption( \
            "$mining", main.mining_minute, "${0}min")
			
		addHeaderOption("$skinning")
		skinning_enabled_id = addToggleOption("$skinning_enabled", \
            main.skinning_enabled)
		if main.skinning_enabled
			skinning_minute_id = addSliderOption( \
				"$skinning", main.skinning_minute, "${0}min", OPTION_FLAG_NONE)
		else 
			skinning_minute_id = addSliderOption( \
				"$skinning", main.skinning_minute, "${0}min", OPTION_FLAG_DISABLED)
		endif
		
		addHeaderOption("$modded_actions")
		bury_hour_id = addSliderOption( \
            "$bury", main.bury_hour, "${2}hour")
		prayer_minute_id = addSliderOption( \
            "$prayer", main.prayer_minute, "${0}min")
		
	elseif page == "$combat"
		setCursorFillMode(TOP_TO_BOTTOM)
        addHeaderOption("$header_options")
		block_controls_id = addToggleOption("$block_controls", \
            main.block_controls)
		if main.block_controls
			combat_warning_id = addToggleOption("$combat_warning", \
			main.combat_warning, OPTION_FLAG_NONE)
		else
			combat_warning_id = addToggleOption("$combat_warning", \
			main.combat_warning, OPTION_FLAG_DISABLED)
		endif
			
		setCursorPosition(1)
		addHeaderOption("$header_controls")
		if main.block_controls				
			block_menus_id = addToggleOption("$block_menus", \
				main.block_menus, OPTION_FLAG_NONE)
			block_journal_id = addToggleOption("$block_journal", \
				main.block_journal, OPTION_FLAG_NONE)
			block_objects_id = addToggleOption("$block_objects", \
				main.block_objects, OPTION_FLAG_NONE)
		else
			block_menus_id = addToggleOption("$block_menus", \
				main.block_menus, OPTION_FLAG_DISABLED)
			block_journal_id = addToggleOption("$block_journal", \
				main.block_journal, OPTION_FLAG_DISABLED)
			block_objects_id = addToggleOption("$block_objects", \
				main.block_objects, OPTION_FLAG_DISABLED)
		endif	

    else
        mods.handle_page(page)
    endif
EndEvent

Event OnOptionSelect(int option)
    if option == is_enabled_id
        main.is_enabled = !main.is_enabled
        setToggleOptionValue(is_enabled_id, main.is_enabled)
        initialize()

    elseif option == reinitialize_id
        initialize()
        showMessage("$reinitialized", False)
		showVersionMessage()

    elseif option == save_id
        bool choice = showMessage("$save_current?", True, "$save_current", "$cancel")
        if choice
            save_settings()
            forcePageReset()
        endif

    elseif option == load_id
        bool choice = showMessage("$load_saved?", True, "$load_saved", "$cancel")
        if choice
            load_settings()
            forcePageReset()
        endif

    elseif option == load_defaults_id
        bool choice = showMessage("$load_defaults?", True, "$load_defaults", "$cancel")
		if choice
			load_defaults()
			initialize()
			forcePageReset()
		endif
		
	elseif option == expertise_reduces_time_id
        main.expertise_reduces_time = !main.expertise_reduces_time
        setToggleOptionValue(expertise_reduces_time_id, \
            main.expertise_reduces_time)
			
	elseif option == item_value_time_id
        main.item_value_time = !main.item_value_time
        setToggleOptionValue(item_value_time_id, \
            main.item_value_time)

    elseif option == random_crafting_time_id
        main.random_crafting_time = !main.random_crafting_time
        setToggleOptionValue(random_crafting_time_id, \
            main.random_crafting_time)
		if main.random_crafting_time
			setOptionFlags(random_time_multiplier_min_id, OPTION_FLAG_NONE)
			setOptionFlags(random_time_multiplier_max_id, OPTION_FLAG_NONE)
		else
			setOptionFlags(random_time_multiplier_min_id, OPTION_FLAG_DISABLED)
			setOptionFlags(random_time_multiplier_max_id, OPTION_FLAG_DISABLED)
		endif

	elseif option == show_day_notification_id
        main.show_day_notification = !main.show_day_notification
        setToggleOptionValue(show_day_notification_id, main.show_day_notification)
					
    elseif option == show_notification_id
        main.show_notification = !main.show_notification
        setToggleOptionValue(show_notification_id, main.show_notification)
		if main.show_notification
			setOptionFlags(notification_threshold_id, OPTION_FLAG_NONE)
		else
			setOptionFlags(notification_threshold_id, OPTION_FLAG_DISABLED)
		endif
		
    elseif option == show_transition_id
        main.show_transition = !main.show_transition
        setToggleOptionValue(show_transition_id, main.show_transition)
		if main.show_transition 
			setOptionFlags(show_fullscreen_transition_id, OPTION_FLAG_NONE)
			setOptionFlags(transition_threshold_id, OPTION_FLAG_NONE)
			setOptionFlags(transition_duration_id, OPTION_FLAG_NONE)
		else
			setOptionFlags(show_fullscreen_transition_id, OPTION_FLAG_DISABLED)
			setOptionFlags(transition_threshold_id, OPTION_FLAG_DISABLED)
			setOptionFlags(transition_duration_id, OPTION_FLAG_DISABLED)
		endif

	elseif option == show_fullscreen_transition_id
        main.show_fullscreen_transition = !main.show_fullscreen_transition
        setToggleOptionValue(show_fullscreen_transition_id, main.show_fullscreen_transition)

	elseif option == block_controls_id
        main.block_controls = !main.block_controls
        setToggleOptionValue(block_controls_id, main.block_controls)
		if main.block_controls
			setOptionFlags(combat_warning_id, OPTION_FLAG_NONE)
			setOptionFlags(block_menus_id, OPTION_FLAG_NONE)
			setOptionFlags(block_objects_id, OPTION_FLAG_NONE)
			setOptionFlags(block_journal_id, OPTION_FLAG_NONE)
			registerForSingleUpdate(5.0)

		else	
			setOptionFlags(combat_warning_id, OPTION_FLAG_DISABLED)
			setOptionFlags(block_menus_id, OPTION_FLAG_DISABLED)
			setOptionFlags(block_objects_id, OPTION_FLAG_DISABLED)
			setOptionFlags(block_journal_id, OPTION_FLAG_DISABLED)
			unregisterForUpdate()
		endif
		
	elseif option == combat_warning_id
        main.combat_warning = !main.combat_warning
        setToggleOptionValue(combat_warning_id, main.combat_warning)
		
	elseif option == block_menus_id
        main.block_menus = !main.block_menus
        setToggleOptionValue(block_menus_id, main.block_menus)
		
	elseif option == block_objects_id
        main.block_objects = !main.block_objects
        setToggleOptionValue(block_objects_id, main.block_objects)
		
	elseif option == block_journal_id
        main.block_journal = !main.block_journal
        setToggleOptionValue(block_journal_id, main.block_journal)
		
	elseif option == crafting_takes_time_id
        main.crafting_takes_time = !main.crafting_takes_time
        setToggleOptionValue(crafting_takes_time_id, main.crafting_takes_time)
		
	elseif option == inventory_loot_id
        main.inventory_loot = !main.inventory_loot
        setToggleOptionValue(inventory_loot_id, main.inventory_loot)
		
	elseif option == scaled_training_id
        main.scaled_training = !main.scaled_training
        setToggleOptionValue(scaled_training_id, main.scaled_training)
		
	elseif option == skinning_enabled_id
        main.skinning_enabled = !main.skinning_enabled
        setToggleOptionValue(skinning_enabled_id, main.skinning_enabled)
		if main.skinning_enabled
			setOptionFlags(skinning_minute_id, OPTION_FLAG_NONE)
		else
			setOptionFlags(skinning_minute_id, OPTION_FLAG_DISABLED)
		endif
		
    else
        mods.handle_option_selected(option)
    endif
EndEvent

Event OnOptionSliderOpen(int option)
    if option == random_time_multiplier_min_id
        setSliderDialogStartValue(main.random_time_multiplier_min)
        setSliderDialogDefaultValue(0.67)
        setSliderDialogRange(0.50, 1.00)
        setSliderDialogInterval(0.01)

    elseif option == random_time_multiplier_max_id
        setSliderDialogStartValue(main.random_time_multiplier_max)
        setSliderDialogDefaultValue(1.00)
        setSliderDialogRange(1.00, 2.00)
        setSliderDialogInterval(0.01)

    elseif option == notification_threshold_id
        setSliderDialogStartValue(main.notification_threshold)
        setSliderDialogDefaultValue(30.0)
        setSliderDialogRange(1.0, 60.0)
        setSliderDialogInterval(1.0)

    elseif option == transition_threshold_id
        setSliderDialogStartValue(main.transition_threshold)
        setSliderDialogDefaultValue(2.0)
        setSliderDialogRange(1.0, 8.0)
        setSliderDialogInterval(1.0)
		
	elseif option == transition_duration_id
        setSliderDialogStartValue(main.transition_duration)
        setSliderDialogDefaultValue(2.0)
        setSliderDialogRange(1.0, 60.0)
        setSliderDialogInterval(1.0)
		
    elseif option == reading_time_multiplier_id
        setSliderDialogStartValue(main.reading_time_multiplier)
        setSliderDialogDefaultValue(3.0)
        setSliderDialogRange(0.00, 5.00)
        setSliderDialogInterval(0.05)

    elseif option == reading_increases_speech_multiplier_id
        setSliderDialogStartValue( \
            main.reading_increases_speech_multiplier)
        setSliderDialogDefaultValue(1.0)
        setSliderDialogRange(0.00, 5.00)
        setSliderDialogInterval(0.05)

    elseif option == spell_learning_hour_id
        setSliderDialogStartValue(main.spell_learning_hour)
        setSliderDialogDefaultValue(2.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == training_hour_id
        setSliderDialogStartValue(main.training_hour)
        setSliderDialogDefaultValue(2.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == eating_minute_id
        setSliderDialogStartValue(main.eating_minute)
        setSliderDialogDefaultValue(5.0)
        setSliderDialogRange(0.0, 30.0)
        setSliderDialogInterval(1.0)

    elseif option == looting_time_multiplier_id
        setSliderDialogStartValue(main.looting_time_multiplier)
        setSliderDialogDefaultValue(1.0)
        setSliderDialogRange(0.0, 5.0)
        setSliderDialogInterval(0.05)

    elseif option == lockpicking_time_multiplier_id
        setSliderDialogStartValue(main.lockpicking_time_multiplier)
        setSliderDialogDefaultValue(1.0)
        setSliderDialogRange(0.0, 5.0)
        setSliderDialogInterval(0.05)

    elseif option == trading_time_multiplier_id
        setSliderDialogStartValue(main.trading_time_multiplier)
        setSliderDialogDefaultValue(1.0)
        setSliderDialogRange(0.0, 5.0)
        setSliderDialogInterval(0.05)

    elseif option == helmet_crafting_hour_id
        setSliderDialogStartValue(main.helmet_crafting_hour)
        setSliderDialogDefaultValue(3.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == armor_crafting_hour_id
        setSliderDialogStartValue(main.armor_crafting_hour)
        setSliderDialogDefaultValue(6.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == gauntlets_crafting_hour_id
        setSliderDialogStartValue(main.gauntlets_crafting_hour)
        setSliderDialogDefaultValue(3.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == boots_crafting_hour_id
        setSliderDialogStartValue(main.boots_crafting_hour)
        setSliderDialogDefaultValue(3.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == shield_crafting_hour_id
        setSliderDialogStartValue(main.shield_crafting_hour)
        setSliderDialogDefaultValue(4.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == clothes_crafting_hour_id
        setSliderDialogStartValue(main.clothes_crafting_hour)
        setSliderDialogDefaultValue(2.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == jewelry_crafting_hour_id
        setSliderDialogStartValue(main.jewelry_crafting_hour)
        setSliderDialogDefaultValue(2.5)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)
		
	elseif option == tool_crafting_hour_id
        setSliderDialogStartValue(main.tool_crafting_hour)
        setSliderDialogDefaultValue(100)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)
		
	elseif option == clutter_crafting_hour_id
        setSliderDialogStartValue(main.clutter_crafting_hour)
        setSliderDialogDefaultValue(1.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == staff_crafting_hour_id
        setSliderDialogStartValue(main.staff_crafting_hour)
        setSliderDialogDefaultValue(4.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == bow_crafting_hour_id
        setSliderDialogStartValue(main.bow_crafting_hour)
        setSliderDialogDefaultValue(4.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == ammo_crafting_hour_id
        setSliderDialogStartValue(main.ammo_crafting_hour)
        setSliderDialogDefaultValue(1.5)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == dagger_crafting_hour_id
        setSliderDialogStartValue(main.dagger_crafting_hour)
        setSliderDialogDefaultValue(3.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == sword_crafting_hour_id
        setSliderDialogStartValue(main.sword_crafting_hour)
        setSliderDialogDefaultValue(4.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == waraxe_crafting_hour_id
        setSliderDialogStartValue(main.waraxe_crafting_hour)
        setSliderDialogDefaultValue(4.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == mace_crafting_hour_id
        setSliderDialogStartValue(main.mace_crafting_hour)
        setSliderDialogDefaultValue(4.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == greatsword_crafting_hour_id
        setSliderDialogStartValue(main.greatsword_crafting_hour)
        setSliderDialogDefaultValue(5.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == battleaxe_crafting_hour_id
        setSliderDialogStartValue(main.battleaxe_crafting_hour)
        setSliderDialogDefaultValue(5.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == warhammer_crafting_hour_id
        setSliderDialogStartValue(main.waraxe_crafting_hour)
        setSliderDialogDefaultValue(5.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == smelting_hour_id
        setSliderDialogStartValue(main.smelting_hour)
        setSliderDialogDefaultValue(2.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == leather_crafting_hour_id
        setSliderDialogStartValue(main.leather_crafting_hour)
        setSliderDialogDefaultValue(1.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == armor_improving_minute_id
        setSliderDialogStartValue(main.armor_improving_minute)
        setSliderDialogDefaultValue(15.0)
        setSliderDialogRange(0.0, 60.0)
        setSliderDialogInterval(1.0)

    elseif option == weapon_improving_minute_id
        setSliderDialogStartValue(main.weapon_improving_minute)
        setSliderDialogDefaultValue(15.0)
        setSliderDialogRange(0.0, 60.0)
        setSliderDialogInterval(1.0)

    elseif option == enchanting_hour_id
        setSliderDialogStartValue(main.enchanting_hour)
        setSliderDialogDefaultValue(1.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)

    elseif option == alchemy_minute_id
        setSliderDialogStartValue(main.alchemy_minute)
        setSliderDialogDefaultValue(30.0)
        setSliderDialogRange(0.0, 60.0)
        setSliderDialogInterval(1.0)

    elseif option == cooking_minute_id
        setSliderDialogStartValue(main.cooking_minute)
        setSliderDialogDefaultValue(15.0)
        setSliderDialogRange(0.0, 60.0)
        setSliderDialogInterval(1.0)
				
	elseif option == harvesting_minute_id
        setSliderDialogStartValue(main.harvesting_minute)
        setSliderDialogDefaultValue(10.0)
        setSliderDialogRange(0.0, 30.0)
        setSliderDialogInterval(1.0)	

	elseif option == mining_minute_id
        setSliderDialogStartValue(main.mining_minute)
        setSliderDialogDefaultValue(30.0)
        setSliderDialogRange(0.0, 60.0)
        setSliderDialogInterval(1.0)
		
	elseif option == lumbering_minute_id
        setSliderDialogStartValue(main.lumbering_minute)
        setSliderDialogDefaultValue(10.0)
        setSliderDialogRange(0.0, 30.0)
        setSliderDialogInterval(1.0)
		
	elseif option == milling_minute_id
        setSliderDialogStartValue(main.milling_minute)
        setSliderDialogDefaultValue(15.0)
        setSliderDialogRange(0.0, 60.0)
        setSliderDialogInterval(1.0)
				
	elseif option == skinning_minute_id
        setSliderDialogStartValue(main.skinning_minute)
        setSliderDialogDefaultValue(10.0)
        setSliderDialogRange(0.0, 30.0)
        setSliderDialogInterval(1.0)
		
	elseif option == bury_hour_id
        setSliderDialogStartValue(main.bury_hour)
        setSliderDialogDefaultValue(2.0)
        setSliderDialogRange(0.0, 8.0)
        setSliderDialogInterval(0.25)
		
	elseif option == prayer_minute_id
        setSliderDialogStartValue(main.prayer_minute)
        setSliderDialogDefaultValue(15.0)
        setSliderDialogRange(0.0, 60.0)
        setSliderDialogInterval(1.0)

    else
        mods.handle_slider_opened(option)
    endif
EndEvent

Event OnOptionSliderAccept(int option, float value)
    if option == random_time_multiplier_min_id
        main.random_time_multiplier_min = value
        setSliderOptionValue(random_time_multiplier_min_id, value, "$x{2}")

    elseif option == random_time_multiplier_max_id
        main.random_time_multiplier_max = value
        setSliderOptionValue(random_time_multiplier_max_id, value, "$x{2}")

    elseif option == notification_threshold_id
        main.notification_threshold = value
        setSliderOptionValue(notification_threshold_id, value, "${0}min")
		
    elseif option == transition_threshold_id
        main.transition_threshold = value
        setSliderOptionValue(transition_threshold_id, value, "${2}hour")
		
    elseif option == transition_duration_id
        main.transition_duration = value
        setSliderOptionValue(transition_duration_id, value, "${0}sec")

    elseif option == reading_time_multiplier_id
        main.reading_time_multiplier = value
        setSliderOptionValue(reading_time_multiplier_id, value, "$x{2}")

    elseif option == reading_increases_speech_multiplier_id
        main.reading_increases_speech_multiplier = value
        setSliderOptionValue(reading_increases_speech_multiplier_id, value, \
            "$x{2}")

    elseif option == spell_learning_hour_id
        main.spell_learning_hour = value
        setSliderOptionValue(spell_learning_hour_id, value, "${2}hour")

    elseif option == training_hour_id
        main.training_hour = value
        setSliderOptionValue(training_hour_id, value, "${2}hour")

    elseif option == eating_minute_id
        main.eating_minute = value
        setSliderOptionValue(eating_minute_id, value, "${0}min")

    elseif option == looting_time_multiplier_id
        main.looting_time_multiplier = value
        setSliderOptionValue(looting_time_multiplier_id, value, "$x{2}")

    elseif option == lockpicking_time_multiplier_id
        main.lockpicking_time_multiplier = value
        setSliderOptionValue(lockpicking_time_multiplier_id, value, "$x{2}")

    elseif option == trading_time_multiplier_id
        main.trading_time_multiplier = value
        setSliderOptionValue(trading_time_multiplier_id, value, "$x{2}")

    elseif option == helmet_crafting_hour_id
        main.helmet_crafting_hour = value
        setSliderOptionValue(helmet_crafting_hour_id, value, "${2}hour")

    elseif option == armor_crafting_hour_id
        main.armor_crafting_hour = value
        setSliderOptionValue(armor_crafting_hour_id, value, "${2}hour")

    elseif option == gauntlets_crafting_hour_id
        main.gauntlets_crafting_hour = value
        setSliderOptionValue(gauntlets_crafting_hour_id, value, "${2}hour")

    elseif option == boots_crafting_hour_id
        main.boots_crafting_hour = value
        setSliderOptionValue(boots_crafting_hour_id, value, "${2}hour")

    elseif option == shield_crafting_hour_id
        main.shield_crafting_hour = value
        setSliderOptionValue(shield_crafting_hour_id, value, "${2}hour")

    elseif option == clothes_crafting_hour_id
        main.clothes_crafting_hour = value
        setSliderOptionValue(clothes_crafting_hour_id, value, "${2}hour")

    elseif option == jewelry_crafting_hour_id
        main.jewelry_crafting_hour = value
        setSliderOptionValue(jewelry_crafting_hour_id, value, "${2}hour")
		
	elseif option == tool_crafting_hour_id
        main.tool_crafting_hour = value
        setSliderOptionValue(tool_crafting_hour_id, value, "${2}hour")
		
	elseif option == clutter_crafting_hour_id
        main.clutter_crafting_hour = value
        setSliderOptionValue(clutter_crafting_hour_id, value, "${2}hour")

    elseif option == staff_crafting_hour_id
        main.staff_crafting_hour = value
        setSliderOptionValue(staff_crafting_hour_id, value, "${2}hour")

    elseif option == bow_crafting_hour_id
        main.bow_crafting_hour = value
        setSliderOptionValue(bow_crafting_hour_id, value, "${2}hour")

    elseif option == ammo_crafting_hour_id
        main.ammo_crafting_hour = value
        setSliderOptionValue(ammo_crafting_hour_id, value, "${2}hour")

    elseif option == dagger_crafting_hour_id
        main.dagger_crafting_hour = value
        setSliderOptionValue(dagger_crafting_hour_id, value, "${2}hour")

    elseif option == sword_crafting_hour_id
        main.sword_crafting_hour = value
        setSliderOptionValue(sword_crafting_hour_id, value, "${2}hour")

    elseif option == waraxe_crafting_hour_id
        main.waraxe_crafting_hour = value
        setSliderOptionValue(waraxe_crafting_hour_id, value, "${2}hour")

    elseif option == mace_crafting_hour_id
        main.mace_crafting_hour = value
        setSliderOptionValue(mace_crafting_hour_id, value, "${2}hour")

    elseif option == greatsword_crafting_hour_id
        main.greatsword_crafting_hour = value
        setSliderOptionValue(greatsword_crafting_hour_id, value, "${2}hour")

    elseif option == battleaxe_crafting_hour_id
        main.battleaxe_crafting_hour = value
        setSliderOptionValue(battleaxe_crafting_hour_id, value, "${2}hour")

    elseif option == warhammer_crafting_hour_id
        main.warhammer_crafting_hour = value
        setSliderOptionValue(warhammer_crafting_hour_id, value, "${2}hour")

    elseif option == smelting_hour_id
        main.smelting_hour = value
        setSliderOptionValue(smelting_hour_id, value, "${2}hour")

    elseif option == leather_crafting_hour_id
        main.leather_crafting_hour = value
        setSliderOptionValue(leather_crafting_hour_id, value, "${2}hour")

    elseif option == armor_improving_minute_id
        main.armor_improving_minute = value
        setSliderOptionValue(armor_improving_minute_id, value, "${0}min")

    elseif option == weapon_improving_minute_id
        main.weapon_improving_minute = value
        setSliderOptionValue(weapon_improving_minute_id, value, "${0}min")

    elseif option == enchanting_hour_id
        main.enchanting_hour = value
        setSliderOptionValue(enchanting_hour_id, value, "${2}hour")

    elseif option == alchemy_minute_id
        main.alchemy_minute = value
        setSliderOptionValue(alchemy_minute_id, value, "${0}min")

    elseif option == cooking_minute_id
        main.cooking_minute = value
        setSliderOptionValue(cooking_minute_id, value, "${0}min")
		
	elseif option == harvesting_minute_id
        main.harvesting_minute = value
        setSliderOptionValue(harvesting_minute_id, value, "${0}min") 

	elseif option == mining_minute_id
        main.mining_minute = value
        setSliderOptionValue(mining_minute_id, value, "${0}min") 
		
	elseif option == lumbering_minute_id
        main.lumbering_minute = value
        setSliderOptionValue(lumbering_minute_id, value, "${0}min") 
		
	elseif option == milling_minute_id
        main.milling_minute = value
        setSliderOptionValue(milling_minute_id, value, "${0}min") 
		
	elseif option == skinning_minute_id
        main.skinning_minute = value
        setSliderOptionValue(skinning_minute_id, value, "${0}min")
		
	elseif option == bury_hour_id
        main.bury_hour = value
        setSliderOptionValue(bury_hour_id, value, "${2}hour")
		
	elseif option == prayer_minute_id
        main.prayer_minute = value
        setSliderOptionValue(prayer_minute_id, value, "${0}min")
		
    else
        mods.handle_slider_accepted(option, value)
    endif
EndEvent

Event OnOptionDefault(int option)
    if option == is_enabled_id
        main.is_enabled = True
        setToggleOptionValue(is_enabled_id, True)
        initialize()

    elseif option == random_crafting_time_id
        main.random_crafting_time = True
        setToggleOptionValue(random_crafting_time_id, True)
		
	elseif option == item_value_time_id
        main.item_value_time = True
        setToggleOptionValue(item_value_time_id, True)

	elseif option == show_day_notification_id
        main.show_day_notification = True
        setToggleOptionValue(show_day_notification_id, True)	
		
    elseif option == show_notification_id
        main.show_notification = True
        setToggleOptionValue(show_notification_id, True)
		
	elseif option == show_transition_id
        main.show_transition = True
        setToggleOptionValue(show_transition_id, True)
		
	elseif option == show_fullscreen_transition_id
        main.show_fullscreen_transition = True
        setToggleOptionValue(show_fullscreen_transition_id, True)
	
	elseif option == combat_warning_id
        main.combat_warning = True
        setToggleOptionValue(combat_warning_id, True)
	
	elseif option == block_controls_id
        main.block_controls = True
        setToggleOptionValue(block_controls_id, True)
		
	elseif option == block_menus_id
        main.block_menus = True
        setToggleOptionValue(block_menus_id, True)
		
	elseif option == block_objects_id
        main.block_objects = True
        setToggleOptionValue(block_objects_id, True)
		
	elseif option == block_journal_id
        main.block_journal = True
        setToggleOptionValue(block_journal_id, True)
		
	elseif option == inventory_loot_id
        main.inventory_loot = True
        setToggleOptionValue(inventory_loot_id, True)

    elseif option == crafting_takes_time_id
        main.crafting_takes_time = True
        setToggleOptionValue(crafting_takes_time_id, True)
        registerForMenu("Crafting Menu")
		
	elseif option == scaled_training_id
        main.scaled_training = True
        setToggleOptionValue(scaled_training_id, True)
		
	elseif option == skinning_enabled_id
        main.show_notification = True
        setToggleOptionValue(skinning_enabled_id, True)

    elseif option == hotkey_id
        unregisterForAllKeys()
        main.hotkey = 0
        setKeyMapOptionValue(hotkey_id, 0)

    else
        mods.handle_option_set_default(option)
    endif
EndEvent

Event OnOptionHighlight(int option)
    if option == is_enabled_id
        setInfoText("$enable_or_disable")
    elseif option == crafting_takes_time_id
        setInfoText("$crafting_takes_time_info")
    elseif option == reading_time_multiplier_id \
            || option == looting_time_multiplier_id \
            || option == lockpicking_time_multiplier_id
        setInfoText("$multiplier_used_to_calculate_passed_time")
	elseif option == trading_time_multiplier_id
        setInfoText("$multiplier_used_to_calculate_passed_time_trading")
    elseif option == spell_learning_hour_id \
            || option == training_hour_id \
            || option == eating_minute_id \
            || option == helmet_crafting_hour_id \
            || option == armor_crafting_hour_id \
            || option == gauntlets_crafting_hour_id \
            || option == boots_crafting_hour_id \
            || option == shield_crafting_hour_id \
            || option == leather_crafting_hour_id \
            || option == clothes_crafting_hour_id \
            || option == jewelry_crafting_hour_id \
			|| option == tool_crafting_hour_id \
			|| option == clutter_crafting_hour_id \
            || option == staff_crafting_hour_id \
            || option == bow_crafting_hour_id \
            || option == ammo_crafting_hour_id \
            || option == dagger_crafting_hour_id \
            || option == sword_crafting_hour_id \
            || option == waraxe_crafting_hour_id \
            || option == mace_crafting_hour_id \
            || option == greatsword_crafting_hour_id \
            || option == battleaxe_crafting_hour_id \
            || option == warhammer_crafting_hour_id \
            || option == smelting_hour_id \
            || option == armor_improving_minute_id \
            || option == weapon_improving_minute_id \
            || option == enchanting_hour_id \
            || option == alchemy_minute_id \
            || option == cooking_minute_id \
			|| option == harvesting_minute_id \
			|| option == mining_minute_id \
			|| option == lumbering_minute_id \
			|| option == milling_minute_id \
			|| option == skinning_minute_id 
        setInfoText("$time_passed_performing_this_action")
	elseif option == expertise_reduces_time_id
        setInfoText("$expertise_reduces_time_info")
	elseif option == item_value_time_id
        setInfoText("$item_value_time_info")
	elseif option == random_crafting_time_id
        setInfoText("$use_random_multiplier_calculating_crafting_time")
    elseif option == random_time_multiplier_min_id
        setInfoText("$random_multiplier_minimum")
    elseif option == random_time_multiplier_max_id
        setInfoText("$random_multiplier_maximum")
    elseif option == show_day_notification_id
        setInfoText("$show_day_notification_info")
	elseif option == show_notification_id
        setInfoText("$show_notification_when_time_passed")
    elseif option == notification_threshold_id
        setInfoText("$show_notification_only_when_pass_the_threshold")
	elseif option == show_transition_id
        setInfoText("$show_transition_when_time_passed")
	elseif option == show_fullscreen_transition_id
        setInfoText("$show_fullscreen_transition_when_time_passed")
    elseif option == transition_threshold_id
        setInfoText("$show_transition_only_when_pass_the_threshold")
    elseif option == transition_duration_id
        setInfoText("$transition_duration_info")
	elseif option == block_controls_id
        setInfoText("$block_controls_info")
	elseif option == combat_warning_id
        setInfoText("$combat_warning_info")
	elseif option == block_menus_id
        setInfoText("$block_menus_info")
	elseif option == block_objects_id
        setInfoText("$block_objects_info")
	elseif option == block_journal_id
        setInfoText("$block_journal_info")
    elseif option == hotkey_id
        setInfoText("$hotkey_info")
    elseif option == save_id
        setInfoText("$save_current_info")
    elseif option == load_id
        setInfoText("$load_saved_info")
    elseif option == load_defaults_id
        setInfoText("$load_defaults_info")
    elseif option == reinitialize_id
        setInfoText("$reinitialize_info")
    elseif option == reading_increases_speech_multiplier_id
        setInfoText("$multiplier_used_calculating_speech_skill_increasing")
	elseif option == inventory_loot_id
        setInfoText("$inventory_loot_info")
	elseif option == scaled_training_id
        setInfoText("$scaled_training_info")
	elseif option == skinning_enabled_id
        setInfoText("$skinning_enabled_info")
	elseif option == bury_hour_id
        setInfoText("$bury_info")
	elseif option == prayer_minute_id
        setInfoText("$prayer_info")
    else
        mods.handle_option_highlighted(option)
    endif
EndEvent
