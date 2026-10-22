// Authoria 2026-10-13: AMON ENB REBORN enbdepthoffield.fx (ADOF Kitsuune Edition, LonelyKitsuune, CC BY-NC-ND 4.0)
// with its #include files inlined for Bottled Effects 11 in the Picta lane. Local use only - do not redistribute.
//----------------------------------------------------------------------------------------------//
//							ADVANCED DEPTH OF FIELD KITSUUNE EDITION							//
//----------------------------------------------------------------------------------------------//
//																								//
//				     enbdepthoffield.fx file by LonelyKitsuune aka Skratzer						//
//						      for ENB (DirectX 11 Shader Model 5)								//
//																								//
//			   Copyright (c) 2019-2020 LonelyKitsuune / T.Thanner - CC BY-NC-ND 4.0				//
//																								//
//-------------------------------------------CREDITS--------------------------------------------//
//																								//
//				 Marty McFly for his Advanced Depth of Field 3.0 shader which					//
//								 served as a basis for this file								//
//		       BY-NC-ND 3.0 Copyright (c) 2008-2018 Marty McFly / Pascal Gilcher				//
//																								//
//----------------------------------------------------------------------------------------------//
//								==================================								//
//								//     Silent Horizons ENB      //								//
//								//								//								//
//								//		by LonelyKitsuune		//								//
//								==================================								//
//----------------------------------------------------------------------------------------------//

//This file needs my helper and UI files to work!


//--------------------------------------------------------------------------------
//Enables full local control over this shader file
#define LOCAL_OVERRIDE					0	//[0-1]


//--------------------------------------------------------------------------------
//DOF OPTIONS
//--------------------------------------------------------------------------------
//Enables partial occlusion of bokeh discs at screen corners
#define ENABLE_OPTICAL_VIGNETTE			1	//[0-1]-G


//Enables bokeh specific chromatic aberration
#define ENABLE_CHROMATIC_ABERRATION		1	//[0-1]-G


//Enables uneven weighting of the bokeh discs
#define ENABLE_SPHERICAL_ABERRATION		1	//[0-1]-G


//Enables bokeh shape diffraction
#define ENABLE_DIFFRACTION				1	//[0-1]-G


//Enables DoF limited graining
// 1 - Individual bokeh shape grain
// 2 - Full screen grain
#define ENABLE_GRAINING					2	//[0-2]-G


//Enables the option to visualize the focusing area
#define ENABLE_FOCUSING_TOOL			1	//[0-1]-G


//Enables custom texture-based bokeh shapes
#define ENABLE_STYLIZED_BOKEHSHAPES		0	//[0-1]-G


//EXPERIMENTAL - Enables the option to freezes the
//current background bokeh blur
#define ENABLE_FAR_BOKEH_FREEZING		0	//[0-1]


//Enable bilateral filtering to get sharper bokeh shapes while
//still being able to use higher "gaussian width" values
#define ENABLE_BILATERAL_GAUSSIAN_BLUR	0	//[0-1]


//----------------------------------------------------------------------------------------------//
//										 Global Parameters										//
//----------------------------------------------------------------------------------------------//

#if !LOCAL_OVERRIDE
#undef ENABLE_OPTICAL_VIGNETTE
#undef ENABLE_CHROMATIC_ABERRATION
#undef ENABLE_FOCUSING_TOOL
#undef ENABLE_STYLIZED_BOKEHSHAPES
#undef ENABLE_SPHERICAL_ABERRATION
#undef ENABLE_DIFFRACTION
#undef ENABLE_GRAINING
//>>> Authoria: inlined "enbglobals.fxh"
//----------------------------------------------------------------------------------------------//
//										GLOBAL OPTIONS FILE										//
//----------------------------------------------------------------------------------------------//
//								==================================								//
//								//     Silent Horizons ENB      //								//
//								//								//								//
//								//		by LonelyKitsuune		//								//
//								==================================								//
//----------------------------------------------------------------------------------------------//


//Simplified version of the most important settings for tweakers
// -> Everything that beginns with #define in this file is a global setting
// -> The values inside the brackets "[]" behind the main variable are the possible inputs


//For more experience users:
//If you want more control over the shaders go into the .fx files and
//enable LOCAL_OVERRIDE to tune each setting manually



//--------------------------------------------------------------------------------
//LENS OPTIONS
//--------------------------------------------------------------------------------
//Enables individual per droplet light dispersion
#define RAINFX_ENABLE_DISPERSION				1 //[0-1]


//Switches to a single layer frost texture with approximated refractions
#define FROSTFX_USE_REFRACTION_METHOD			1 //[0-1]


//Use only the brightest burst when more than one intersect
#define STARBURST_USE_MAX_COLOR					0 //[0-1]



//--------------------------------------------------------------------------------
//BLOOM OPTIONS
//--------------------------------------------------------------------------------
//Enable lens-dirt bloom reflections
#define ENABLE_DIRT_REFLECTION		1 //[0-1]


//Enables the option to mask out the bloom source
#define ENABLE_SOURCE_MASKING		1 //[0-1]


//Enables depth based bloom width/intensity manipulation
#define ENABLE_DEPTH_TESTING		1 //[0-1]


//Enables the option to limit bloom from skin (requires an active prepass!)
#define ENABLE_SKIN_ATTENUATION		1 //[0-1]



//--------------------------------------------------------------------------------
//POSTPASS OPTIONS
//--------------------------------------------------------------------------------
//Note: Disabling an AA method via the UI isn't the same as disabling it in here!
//      Doing it here safes you additional performance in most cases (especially
//      FXAA & SMAA), so make sure to choose your support preset accordingly!

//Makes different antialiasing methods available ingame
#define AA_SUPPORT_PRESET		0 //[0-5]-G
// 0 - No AA support
// 1 - Only SMAA
// 2 - Only FXAA
// 3 - SMAA and FXAA
// 4 - SMAA and CREAA
// 5 - SMAA, FXAA and CREAA


//Choose the SMAA quality level
#define SMAA_PRESET				3 //[0-3]
//0 = low,  1 = medium
//2 = high, 3 = ultra


//Choose the FXAA quality level
#define FXAA_PRESET				4 //[0-4]
// 0 = low,  1 = medium
// 2 = high, 3 = very high
// 4 = ultra


//Enables an optional blur pass (features full screen, radial and depth based controls)
#define ENABLE_BLUR_SUITE		1 //[0-1]



//--------------------------------------------------------------------------------
//DEPTH OF FIELD OPTIONS
//--------------------------------------------------------------------------------
//Enables partial occlusion of bokeh discs at screen corners
#define ENABLE_OPTICAL_VIGNETTE			1 //[0-1]


//Enables bokeh specific chromatic aberration
#define ENABLE_CHROMATIC_ABERRATION		1 //[0-1]


//Enables custom texture-based bokeh shapes
#define ENABLE_STYLIZED_BOKEHSHAPES		1 //[0-1]


//Enables uneven weighting of bokeh discs
#define ENABLE_SPHERICAL_ABERRATION		1 //[0-1]


//Enables bokeh shape diffraction
#define ENABLE_DIFFRACTION				1 //[0-1]


//Enables DoF limited graining
// 1 - Individual bokeh shape grain
// 2 - Full screen grain
#define ENABLE_GRAINING					2 //[0-2]


//Enables the option to visualize the focusing area
#define ENABLE_FOCUSING_TOOL			1 //[0-1]
//<<< end "enbglobals.fxh"
#endif //LOCAL_OVERRIDE


//----------------------------------------------------------------------------------------------//
//										Internal Parameters										//
//----------------------------------------------------------------------------------------------//

//Gives the option to visualize the different CoC textures
#define ENABLE_COC_DEBUGGING 0

//>>> Authoria: inlined "UI/enbUI_Primer.fxh"
//----------------------------------------------------------------------------------------------//
//																								//
//				       UI Primer - header file for Silent Horizons ENB							//
//																								//
//----------------------------------------------------------------------------------------------//

#ifndef _UI_PRIMER_
#define _UI_PRIMER_

//Little macro collection for the UI

#define SEPARATE_VAR(x) COMBINE(COMBINE(TODIE,_),x)
#define COMBINE(a,b) a##b
#define TO_STRING(x) #x

#define UI_ELEMENT(a,b) int COMBINE(TODIE,a) <string UIName = ##b; int UIMin = 0; int UIMax = 0; > = {0};
#define UI_WHITESPACE(a) int Whitespace_##a <string UIName = WHITESPACE_##a; int UIMin = 0; int UIMax = 0; > = {0};
#define UI_SPECIAL_WHITESPACE(a) int Special_Whitespace_##a <string UIName = SPECIAL_WHITESPACE_##a; int UIMin = 0; int UIMax = 0; > = {0};

#define UI_FileHeader(a) int FileHeader1 <string UIName="_________________________________________"; int UIMin=0;int UIMax=0;> ={0}; \
int FileHeader2 <string UIName=##a; int UIMin=0;int UIMax=0;> ={0}; \
int FileHeader3 <string UIName="\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF"; int UIMin=0;int UIMax=0;> ={0};

#define UI_FileHeaderLong(a,b) int FileHeader1 <string UIName="_________________________________________"; int UIMin=0;int UIMax=0;> ={0}; \
int FileHeader2 <string UIName=##a; int UIMin=0;int UIMax=0;> ={0}; \
int FileHeader3 <string UIName=##b; int UIMin=0;int UIMax=0;> ={0}; \
int FileHeader4 <string UIName="\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF\xAF"; int UIMin=0;int UIMax=0;> ={0};

//---------------------------------------------------------//
//WHITESPACE COLLECTION from "ReforgedUI" by SANDVICH MAKER//
//---------------------------------------------------------//
#define WHITESPACE_1   " "
#define WHITESPACE_2   "  "
#define WHITESPACE_3   "   "
#define WHITESPACE_4   "    "
#define WHITESPACE_5   "     "
#define WHITESPACE_6   "      "
#define WHITESPACE_7   "       "
#define WHITESPACE_8   "        "
#define WHITESPACE_9   "         "
#define WHITESPACE_10  "          "
#define WHITESPACE_11  "           "
#define WHITESPACE_12  "            "
#define WHITESPACE_13  "             "
#define WHITESPACE_14  "              "
#define WHITESPACE_15  "               "
#define WHITESPACE_16  "                "
#define WHITESPACE_17  "                 "
#define WHITESPACE_18  "                  "
#define WHITESPACE_19  "                   "
#define WHITESPACE_20  "                    "
#define WHITESPACE_21  "                     "
#define WHITESPACE_22  "                      "
#define WHITESPACE_23  "                       "
#define WHITESPACE_24  "                        "
#define WHITESPACE_25  "                         "
#define WHITESPACE_26  "                          "
#define WHITESPACE_27  "                           "
#define WHITESPACE_28  "                            "
#define WHITESPACE_29  "                             "
#define WHITESPACE_30  "                              "
#define WHITESPACE_31  "                               "
#define WHITESPACE_32  "                                "
#define WHITESPACE_33  "                                 "
#define WHITESPACE_34  "                                  "
#define WHITESPACE_35  "                                   "
#define WHITESPACE_36  "                                    "
#define WHITESPACE_37  "                                     "
#define WHITESPACE_38  "                                      "
#define WHITESPACE_39  "                                       "
#define WHITESPACE_40  "                                        "
#define WHITESPACE_41  "                                         "
#define WHITESPACE_42  "                                          "
#define WHITESPACE_43  "                                           "
#define WHITESPACE_44  "                                            "
#define WHITESPACE_45  "                                             "
#define WHITESPACE_46  "                                              "
#define WHITESPACE_47  "                                               "
#define WHITESPACE_48  "                                                "
#define WHITESPACE_49  "                                                 "
#define WHITESPACE_50  "                                                  "
#define WHITESPACE_51  "                                                   "
#define WHITESPACE_52  "                                                    "
#define WHITESPACE_53  "                                                     "
#define WHITESPACE_54  "                                                      "
#define WHITESPACE_55  "                                                       "
#define WHITESPACE_56  "                                                        "
#define WHITESPACE_57  "                                                         "
#define WHITESPACE_58  "                                                          "
#define WHITESPACE_59  "                                                           "
#define WHITESPACE_60  "                                                            "
#define WHITESPACE_61  "                                                             "
#define WHITESPACE_62  "                                                              "
#define WHITESPACE_63  "                                                               "
#define WHITESPACE_64  "                                                                "
#define WHITESPACE_65  "                                                                 "
#define WHITESPACE_66  "                                                                  "
#define WHITESPACE_67  "                                                                   "
#define WHITESPACE_68  "                                                                    "
#define WHITESPACE_69  "                                                                     "
#define WHITESPACE_70  "                                                                      "
#define WHITESPACE_71  "                                                                       "
#define WHITESPACE_72  "                                                                        "
#define WHITESPACE_73  "                                                                         "
#define WHITESPACE_74  "                                                                          "
#define WHITESPACE_75  "                                                                           "
#define WHITESPACE_76  "                                                                            "
#define WHITESPACE_77  "                                                                             "
#define WHITESPACE_78  "                                                                              "
#define WHITESPACE_79  "                                                                               "
#define WHITESPACE_80  "                                                                                "
#define WHITESPACE_81  "                                                                                 "
#define WHITESPACE_82  "                                                                                  "
#define WHITESPACE_83  "                                                                                   "
#define WHITESPACE_84  "                                                                                    "
#define WHITESPACE_85  "                                                                                     "
#define WHITESPACE_86  "                                                                                      "
#define WHITESPACE_87  "                                                                                       "
#define WHITESPACE_88  "                                                                                        "
#define WHITESPACE_89  "                                                                                         "
#define WHITESPACE_90  "                                                                                          "
#define WHITESPACE_91  "                                                                                           "
#define WHITESPACE_92  "                                                                                            "
#define WHITESPACE_93  "                                                                                             "
#define WHITESPACE_94  "                                                                                              "
#define WHITESPACE_95  "                                                                                               "
#define WHITESPACE_96  "                                                                                                "
#define WHITESPACE_97  "                                                                                                 "
#define WHITESPACE_98  "                                                                                                  "
#define WHITESPACE_99  "                                                                                                   "
#define WHITESPACE_100 "                                                                                                    "
#define WHITESPACE_101 "                                                                                                     "
#define WHITESPACE_102 "                                                                                                      "
#define WHITESPACE_103 "                                                                                                       "
#define WHITESPACE_104 "                                                                                                        "
#define WHITESPACE_105 "                                                                                                         "
#define WHITESPACE_106 "                                                                                                          "
#define WHITESPACE_107 "                                                                                                           "
#define WHITESPACE_108 "                                                                                                            "
#define WHITESPACE_109 "                                                                                                             "
#define WHITESPACE_110 "                                                                                                              "
#define WHITESPACE_111 "                                                                                                               "
#define WHITESPACE_112 "                                                                                                                "
#define WHITESPACE_113 "                                                                                                                 "
#define WHITESPACE_114 "                                                                                                                  "
#define WHITESPACE_115 "                                                                                                                   "
#define WHITESPACE_116 "                                                                                                                    "
#define WHITESPACE_117 "                                                                                                                     "
#define WHITESPACE_118 "                                                                                                                      "
#define WHITESPACE_119 "                                                                                                                       "
#define WHITESPACE_120 "                                                                                                                        "
#define WHITESPACE_121 "                                                                                                                         "
#define WHITESPACE_122 "                                                                                                                          "
#define WHITESPACE_123 "                                                                                                                           "
#define WHITESPACE_124 "                                                                                                                            "
#define WHITESPACE_125 "                                                                                                                             "
#define WHITESPACE_126 "                                                                                                                              "
#define WHITESPACE_127 "                                                                                                                               "
#define WHITESPACE_128 "                                                                                                                                "


//------------------------------------------------//
//And my own little SPECIAL WHITESPACE COLLECTION //
//------------------------------------------------//
#define SPECIAL_WHITESPACE_0   "|"
#define SPECIAL_WHITESPACE_1   "| "
#define SPECIAL_WHITESPACE_2   "|  "
#define SPECIAL_WHITESPACE_3   "|   "
#define SPECIAL_WHITESPACE_4   "|    "
#define SPECIAL_WHITESPACE_5   "|     "
#define SPECIAL_WHITESPACE_6   "|      "
#define SPECIAL_WHITESPACE_7   "|       "
#define SPECIAL_WHITESPACE_8   "|        "
#define SPECIAL_WHITESPACE_9   "|         "
#define SPECIAL_WHITESPACE_10  "|          "
#define SPECIAL_WHITESPACE_11  "|           "
#define SPECIAL_WHITESPACE_12  "|            "
#define SPECIAL_WHITESPACE_13  "|             "
#define SPECIAL_WHITESPACE_14  "|              "
#define SPECIAL_WHITESPACE_15  "|               "
#define SPECIAL_WHITESPACE_16  "|                "
#define SPECIAL_WHITESPACE_17  "|                 "
#define SPECIAL_WHITESPACE_18  "|                  "
#define SPECIAL_WHITESPACE_19  "|                   "
#define SPECIAL_WHITESPACE_20  "|                    "
#define SPECIAL_WHITESPACE_21  "|                     "
#define SPECIAL_WHITESPACE_22  "|                      "
#define SPECIAL_WHITESPACE_23  "|                       "
#define SPECIAL_WHITESPACE_24  "|                        "
#define SPECIAL_WHITESPACE_25  "|                         "
#define SPECIAL_WHITESPACE_26  "|                          "
#define SPECIAL_WHITESPACE_27  "|                           "
#define SPECIAL_WHITESPACE_28  "|                            "
#define SPECIAL_WHITESPACE_29  "|                             "
#define SPECIAL_WHITESPACE_30  "|                              "
#define SPECIAL_WHITESPACE_31  "|                               "
#define SPECIAL_WHITESPACE_32  "|                                "
#define SPECIAL_WHITESPACE_33  "|                                 "
#define SPECIAL_WHITESPACE_34  "|                                  "
#define SPECIAL_WHITESPACE_35  "|                                   "
#define SPECIAL_WHITESPACE_36  "|                                    "
#define SPECIAL_WHITESPACE_37  "|                                     "
#define SPECIAL_WHITESPACE_38  "|                                      "
#define SPECIAL_WHITESPACE_39  "|                                       "
#define SPECIAL_WHITESPACE_40  "|                                        "
#define SPECIAL_WHITESPACE_41  "|                                         "
#define SPECIAL_WHITESPACE_42  "|                                          "
#define SPECIAL_WHITESPACE_43  "|                                           "
#define SPECIAL_WHITESPACE_44  "|                                            "
#define SPECIAL_WHITESPACE_45  "|                                             "
#define SPECIAL_WHITESPACE_46  "|                                              "
#define SPECIAL_WHITESPACE_47  "|                                               "
#define SPECIAL_WHITESPACE_48  "|                                                "
#define SPECIAL_WHITESPACE_49  "|                                                 "
#define SPECIAL_WHITESPACE_50  "|                                                  "
#define SPECIAL_WHITESPACE_51  "|                                                   "
#define SPECIAL_WHITESPACE_52  "|                                                    "
#define SPECIAL_WHITESPACE_53  "|                                                     "
#define SPECIAL_WHITESPACE_54  "|                                                      "
#define SPECIAL_WHITESPACE_55  "|                                                       "
#define SPECIAL_WHITESPACE_56  "|                                                        "
#define SPECIAL_WHITESPACE_57  "|                                                         "
#define SPECIAL_WHITESPACE_58  "|                                                          "
#define SPECIAL_WHITESPACE_59  "|                                                           "
#define SPECIAL_WHITESPACE_60  "|                                                            "
#define SPECIAL_WHITESPACE_61  "|                                                             "
#define SPECIAL_WHITESPACE_62  "|                                                              "
#define SPECIAL_WHITESPACE_63  "|                                                               "
#define SPECIAL_WHITESPACE_64  "|                                                                "
#define SPECIAL_WHITESPACE_65  "|                                                                 "
#define SPECIAL_WHITESPACE_66  "|                                                                  "
#define SPECIAL_WHITESPACE_67  "|                                                                   "
#define SPECIAL_WHITESPACE_68  "|                                                                    "
#define SPECIAL_WHITESPACE_69  "|                                                                     "
#define SPECIAL_WHITESPACE_70  "|                                                                      "
#define SPECIAL_WHITESPACE_71  "|                                                                       "
#define SPECIAL_WHITESPACE_72  "|                                                                        "
#define SPECIAL_WHITESPACE_73  "|                                                                         "
#define SPECIAL_WHITESPACE_74  "|                                                                          "
#define SPECIAL_WHITESPACE_75  "|                                                                           "
#define SPECIAL_WHITESPACE_76  "|                                                                            "
#define SPECIAL_WHITESPACE_77  "|                                                                             "
#define SPECIAL_WHITESPACE_78  "|                                                                              "
#define SPECIAL_WHITESPACE_79  "|                                                                               "
#define SPECIAL_WHITESPACE_80  "|                                                                                "
#define SPECIAL_WHITESPACE_81  "|                                                                                 "
#define SPECIAL_WHITESPACE_82  "|                                                                                  "
#define SPECIAL_WHITESPACE_83  "|                                                                                   "
#define SPECIAL_WHITESPACE_84  "|                                                                                    "
#define SPECIAL_WHITESPACE_85  "|                                                                                     "
#define SPECIAL_WHITESPACE_86  "|                                                                                      "
#define SPECIAL_WHITESPACE_87  "|                                                                                       "
#define SPECIAL_WHITESPACE_88  "|                                                                                        "
#define SPECIAL_WHITESPACE_89  "|                                                                                         "
#define SPECIAL_WHITESPACE_90  "|                                                                                          "
#define SPECIAL_WHITESPACE_91  "|                                                                                           "
#define SPECIAL_WHITESPACE_92  "|                                                                                            "
#define SPECIAL_WHITESPACE_93  "|                                                                                             "
#define SPECIAL_WHITESPACE_94  "|                                                                                              "
#define SPECIAL_WHITESPACE_95  "|                                                                                               "
#define SPECIAL_WHITESPACE_96  "|                                                                                                "
#define SPECIAL_WHITESPACE_97  "|                                                                                                 "
#define SPECIAL_WHITESPACE_98  "|                                                                                                  "
#define SPECIAL_WHITESPACE_99  "|                                                                                                   "
#define SPECIAL_WHITESPACE_100 "|                                                                                                    "
#define SPECIAL_WHITESPACE_101 "|                                                                                                     "
#define SPECIAL_WHITESPACE_102 "|                                                                                                      "
#define SPECIAL_WHITESPACE_103 "|                                                                                                       "
#define SPECIAL_WHITESPACE_104 "|                                                                                                        "
#define SPECIAL_WHITESPACE_105 "|                                                                                                         "
#define SPECIAL_WHITESPACE_106 "|                                                                                                          "
#define SPECIAL_WHITESPACE_107 "|                                                                                                           "
#define SPECIAL_WHITESPACE_108 "|                                                                                                            "
#define SPECIAL_WHITESPACE_109 "|                                                                                                             "
#define SPECIAL_WHITESPACE_110 "|                                                                                                              "
#define SPECIAL_WHITESPACE_111 "|                                                                                                               "
#define SPECIAL_WHITESPACE_112 "|                                                                                                                "
#define SPECIAL_WHITESPACE_113 "|                                                                                                                 "
#define SPECIAL_WHITESPACE_114 "|                                                                                                                  "
#define SPECIAL_WHITESPACE_115 "|                                                                                                                   "
#define SPECIAL_WHITESPACE_116 "|                                                                                                                    "
#define SPECIAL_WHITESPACE_117 "|                                                                                                                     "
#define SPECIAL_WHITESPACE_118 "|                                                                                                                      "
#define SPECIAL_WHITESPACE_119 "|                                                                                                                       "
#define SPECIAL_WHITESPACE_120 "|                                                                                                                        "
#define SPECIAL_WHITESPACE_121 "|                                                                                                                         "
#define SPECIAL_WHITESPACE_122 "|                                                                                                                          "
#define SPECIAL_WHITESPACE_123 "|                                                                                                                           "
#define SPECIAL_WHITESPACE_124 "|                                                                                                                            "
#define SPECIAL_WHITESPACE_125 "|                                                                                                                             "
#define SPECIAL_WHITESPACE_126 "|                                                                                                                              "
#define SPECIAL_WHITESPACE_127 "|                                                                                                                               "
#define SPECIAL_WHITESPACE_128 "|                                                                                                                                "

#endif //_UI_PRIMER_
//<<< end "UI/enbUI_Primer.fxh"

#define SHADERGROUP 0
//>>> Authoria: inlined "UI/enbUI_DepthOfField.fxh"
//----------------------------------------------------------------------------------------------//
//																								//
//						      Main ENB Depth of Field UI file									//
//						      by LonelyKitsuune aka Skratzer									//
//																								//
//----------------------------------------------------------------------------------------------//

//This file requires my UI Primer header to work!
#ifndef _UI_PRIMER_
#error UI_Primer couldnt be found!
#endif

//----------------------------------------------------------------------------------------------//
//								  User Interface Parameters										//
//																								//
//----------------------------------------------------------------------------------------------//


#if SHADERGROUP == 0

UI_FileHeaderLong(">>>          Avanced Depth of Field          <<<",
				  ">>>                Kitsuune Edition               <<<")
UI_WHITESPACE(1)


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

UI_ELEMENT(_Focus_Header,"               >>>>>>FOCUS<<<<<<")
UI_WHITESPACE(2)
int   UI_FocusType				<string UIName="|- Focus Type (1-Auto, 2-Mouse, 3-Manual)";				 int   UIMin=1;    int   UIMax=3;   > = {1};
#if ENABLE_FOCUSING_TOOL
bool  UI_VisualizeFocus			<string UIName="|- Visualize Focus";																	    > = {false};
#endif
UI_SPECIAL_WHITESPACE(1)
UI_ELEMENT(_DOF_FocusInfo1,				       "|- 1 - Autofocus")
float2 UI_AutofocusCenter		<string UIName="|- Autofocus Sample Center";							 float UIMin=0.00; float UIMax=1.0; > = {0.5,0.5};
float  UI_AutofocusRadius		<string UIName="|- Autofocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(2)
UI_ELEMENT(_DOF_FocusInfo2,				       "|- 2 - Mousefocus (right click to focus)")
float  UI_MousefocusRadius		<string UIName="|- Mousefocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(3)
UI_ELEMENT(_DOF_FocusInfo3,				       "|- 3 - Manual Focus")
float  UI_ManualfocusDepth		<string UIName="|- Manual Focus Depth";			    float UIStep=0.0001; float UIMin=0.0;  float UIMax=1.0; > = {0.05};
UI_WHITESPACE(3)
UI_WHITESPACE(4)
UI_ELEMENT(_DOF_Header,"        >>>>>>DEPTH OF FIELD<<<<<<")
UI_WHITESPACE(5)
UI_ELEMENT(_DOF_DoFInfo,				       "|------- DOF")
float  UI_NearBlurCurve			<string UIName="|- DOF - Near Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.0};
float  UI_NearBlurBleed			<string UIName="|- DOF - Near Blur Bleeding";							 float UIMin=0.0;   float UIMax= 2.0;  > = {1.0};
float  UI_FarBlurCurve			<string UIName="|- DOF - Far Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.4};
#if ENABLE_FAR_BOKEH_FREEZING
bool   UI_FreezeFarBokeh		<string UIName="|- DOF - Freeze Far Bokeh";																       > = {false};
#endif
float  UI_HyperFocus			<string UIName="|- DOF - Hyperfocal Depth Distance"; float UIStep=0.001; float UIMin=0.0;   float UIMax=1.0;   > = {0.015};
bool   UI_RemoveFPSObjects      <string UIName="|- DOF - Remove FPS Objects";															       > = {true};
float  UI_RenderResMult			<string UIName="|- DOF - Blur Render Res mult";							 float UIMin=0.5;   float UIMax=1.0;   > = {0.5};
float  UI_SmootheningAmount		<string UIName="|- DOF - Gaussian PostBlur Width";						 float UIMin=0.0;   float UIMax=20.0;  > = {4.0};
int    UI_GaussQuality			<string UIName="|- DOF - Gaussian Quality";   string UIWidget="Quality"; int   UIMin=0;     int   UIMax=2;     > = {  1};
#if ENABLE_COC_DEBUGGING
int    UI_CoCDebug				<string UIName="|- DOF - CoC Debug";									 int   UIMin=0;     int   UIMax=4;     > = {  0};
#endif
UI_SPECIAL_WHITESPACE(4)
UI_ELEMENT(_DOF_BokehInfo,				       "|------- BOKEH")
float  UI_BokehIntensity		<string UIName="|- Bokeh - Intensity";									 float UIMin=0.0;   float UIMax=1.0;   > = {0.5};
float  UI_BokehCurve			<string UIName="|- Bokeh - Curve";										 float UIMin=0.0;   float UIMax=20.0;  > = {1.0};
float  UI_ShapeRadius			<string UIName="|- Bokeh - Shape Max Size";		     float UIStep=0.1;	 float UIMin=0.0;   float UIMax=100.0; > = {15.0};
int    UI_ShapeVertices			<string UIName="|- Bokeh - Shape Vertices";								 int   UIMin=3;     int   UIMax=9;     > = {6};
int    UI_ShapeQuality			<string UIName="|- Bokeh - Shape Quality";								 int   UIMin=2;     int   UIMax=50;    > = {5};
float  UI_ShapeCurvatureAmount	<string UIName="|- Bokeh - Shape Roundness";							 float UIMin=-1.0;  float UIMax=1.0;   > = {1.0};
float  UI_ShapeRotation			<string UIName="|- Bokeh - Shape Rotation (\xB0)";   float UIStep=1;	 float UIMin=0;     float UIMax=360;   > = {15};
float  UI_ShapeAnamorphRatio	<string UIName="|- Bokeh - Shape Aspect Ratio";							 float UIMin=0.0;   float UIMax=2.0;   > = {1.0};
bool   UI_ShapeCut				<string UIName="|- Bokeh - Cut Shape in Half";															       > = {false};

#if ENABLE_STYLIZED_BOKEHSHAPES
UI_SPECIAL_WHITESPACE(5)
UI_ELEMENT(_DOF_StyleInfo,				       "|------- STYLIZED BOKEH SHAPES")
bool   UI_EnableStyle			<string UIName="|- Style - Override Bokeh Shape";														    > = {false};
float  UI_StyleTex				<string UIName="|- Style - Choose Shape Texture";   float UIStep=1;		float UIMin=1.0; float UIMax=9.0;   > = {1.0};
float  UI_StyleIntensity		<string UIName="|- Style - Intensity";									float UIMin=0.0; float UIMax=1.0;   > = {1.0};
float  UI_StyleRadius			<string UIName="|- Style - Shape Max Size";		    float UIStep=0.1;	float UIMin=0.0; float UIMax=100.0; > = {15.0};
float  UI_StyleQualityLevel		<string UIName="|- Style - Shape Quality Level";    float UIStep=1;		float UIMin=1.0; float UIMax=4.0;   > = {2.0};
float  UI_StyleRotation			<string UIName="|- Style - Shape Rotation (\xB0)";  float UIStep=1;		float UIMin=0.0; float UIMax=359.0; > = {0.0};
float  UI_StyleSmoothening		<string UIName="|- Style - Gaussian Blur Override";						float UIMin=0.0; float UIMax=20.0;  > = {2.0};
#endif //ENABLE_STYLIZED_BOKEHSHAPES

#if ENABLE_SPHERICAL_ABERRATION
UI_SPECIAL_WHITESPACE(6)
UI_ELEMENT(_DOF_SAInfo,						       "|------- SPHERICAL ABERRATION")
float  UI_SphericalAmount		<string UIName="|- Bokeh - Shape SA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.1};
float  UI_SphericalCurve		<string UIName="|- Bokeh - Shape SA Curve";  float UIMin= 0.0; float UIMax=3.0; > = {0.25};
#endif //ENABLE_SPHERICAL_ABERRATION

#if ENABLE_DIFFRACTION
UI_SPECIAL_WHITESPACE(7)
UI_ELEMENT(_DOF_DiInfo,						       "|------- DIFFRACTION")
float  UI_DiffractionAmount		<string UIName="|- Bokeh - Diffraction Amount";    float UIMin=0.0;  float UIMax= 1.0; > = {0.25};
float  UI_DiffractionFreq		<string UIName="|- Bokeh - Diffraction Frequency"; float UIMin=0.01; float UIMax=20.0; > = {8.0};
#endif //ENABLE_DIFFRACTION

#if ENABLE_OPTICAL_VIGNETTE
UI_SPECIAL_WHITESPACE(9)
UI_ELEMENT(_DOF_OVInfo,						       "|------- OPTICAL VIGNETTE")
float  UI_ShapeVignetteCurve		<string UIName="|- Bokeh - Shape Vignette Curve";  float UIMin=0.5; float UIMax=2.5; > = {0.75};
float  UI_ShapeVignetteAmount		<string UIName="|- Bokeh - Shape Vignette Amount"; float UIMin=0.0; float UIMax=2.0; > = {1.0};
#endif //ENABLE_OPTICAL_VIGNETTE

#if ENABLE_CHROMATIC_ABERRATION
UI_SPECIAL_WHITESPACE(10)
UI_ELEMENT(_DOF_CAInfo,						       "|------- CHROMATIC ABERRATION")
float  UI_LongitudChromaAmount		<string UIName="|- Bokeh - Longitudinal CA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.3};
float  UI_LateralChromaAmount		<string UIName="|- Bokeh - Lateral CA Amount";      float UIMin=-1.0; float UIMax=1.0; > = {0.2};
float  UI_LateralChromaCurve		<string UIName="|- Bokeh - Lateral CA Curve";       float UIMin= 0.0; float UIMax=8.0; > = {1.3};
int    UI_ChromaMode				<string UIName="|- Bokeh - CA Type";                int   UIMin=   0; int   UIMax=  2; > = {2};
#endif

#if ENABLE_GRAINING == 1
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainAmount			<string UIName="|- Bokeh - Grain Amount"; float UIMin=0.0; float UIMax= 1.0; > = {0.1};
float UI_GrainSeed				<string UIName="|- Bokeh - Grain Seed";   float UIMin=0.0; float UIMax=10.0; > = {0.23};
#elif ENABLE_GRAINING == 2
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainInt				<string UIName="|- DOF - Grain Intensity";  float UIMin= 0.0; float UIMax=0.5; > = {0.05};
float UI_GrainSaturation		<string UIName="|- DOF - Grain Saturation"; float UIMin= 0.0; float UIMax=1.0; > = {0.5};
float UI_GrainMotion			<string UIName="|- DOF - Grain Motion";     float UIMin=-2.0; float UIMax=2.0; > = {0.1};
#endif //ENABLE_GRAINING


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_DOFCC_Header,"   >>>>>>DOF COLOR GRADING<<<<<<")
UI_WHITESPACE(9)
bool  UICG_Enable		<string UIName="|---- Enable DOF Color Grading";										> = {true};
int   UICG_Mask			<string UIName="|- DOFCG - CC Mask (1-Bokeh, 2-CoC)"; int   UIMin=1;   int   UIMax=2;   > = {1};
float UICG_ConGrayLvl	<string UIName="|- DOFCG - Contrast Gray Level";      float UIMin=0.0; float UIMax=1.0; > = {0.5};
UI_SPECIAL_WHITESPACE(11)
#endif //NOTFIRSTTIME

float SEPARATE_VAR(UICG_Saturation) <string UIName=TO_STRING(|- DOFCG - TODIE - Saturation); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Brightness) <string UIName=TO_STRING(|- DOFCG - TODIE - Brightness); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Contrast)   <string UIName=TO_STRING(|- DOFCG - TODIE - Contrast);   float UIMin=0.0; float UIMax=10.0; > = {1.0};


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

UI_ELEMENT(_DOFK_Header,"           >>>>>>DOF KEYING<<<<<<")
UI_WHITESPACE(10)
bool   UIK_Enable <string UIName="|---- Enable DOF Keying";										  > = {false};
int    UIK_Mask   <string UIName="|- DOFK - Key Mask (1-Bokeh, 2-DOF)"; int UIMin=1; int UIMax=2; > = {2};
float3 UIK_Color  <string UIName="|- DOFK - Keycolor";						string UIWidget="Color";  > = {0,1,0};

#endif //SHADERGROUP

#undef TODIE
//<<< end "UI/enbUI_DepthOfField.fxh"
#undef SHADERGROUP

//Focus, DOF and Bokeh
#define SHADERGROUP 1
//>>> Authoria: inlined "UI/enbUI_DepthOfField.fxh"
//----------------------------------------------------------------------------------------------//
//																								//
//						      Main ENB Depth of Field UI file									//
//						      by LonelyKitsuune aka Skratzer									//
//																								//
//----------------------------------------------------------------------------------------------//

//This file requires my UI Primer header to work!
#ifndef _UI_PRIMER_
#error UI_Primer couldnt be found!
#endif

//----------------------------------------------------------------------------------------------//
//								  User Interface Parameters										//
//																								//
//----------------------------------------------------------------------------------------------//


#if SHADERGROUP == 0

UI_FileHeaderLong(">>>          Avanced Depth of Field          <<<",
				  ">>>                Kitsuune Edition               <<<")
UI_WHITESPACE(1)


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

UI_ELEMENT(_Focus_Header,"               >>>>>>FOCUS<<<<<<")
UI_WHITESPACE(2)
int   UI_FocusType				<string UIName="|- Focus Type (1-Auto, 2-Mouse, 3-Manual)";				 int   UIMin=1;    int   UIMax=3;   > = {1};
#if ENABLE_FOCUSING_TOOL
bool  UI_VisualizeFocus			<string UIName="|- Visualize Focus";																	    > = {false};
#endif
UI_SPECIAL_WHITESPACE(1)
UI_ELEMENT(_DOF_FocusInfo1,				       "|- 1 - Autofocus")
float2 UI_AutofocusCenter		<string UIName="|- Autofocus Sample Center";							 float UIMin=0.00; float UIMax=1.0; > = {0.5,0.5};
float  UI_AutofocusRadius		<string UIName="|- Autofocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(2)
UI_ELEMENT(_DOF_FocusInfo2,				       "|- 2 - Mousefocus (right click to focus)")
float  UI_MousefocusRadius		<string UIName="|- Mousefocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(3)
UI_ELEMENT(_DOF_FocusInfo3,				       "|- 3 - Manual Focus")
float  UI_ManualfocusDepth		<string UIName="|- Manual Focus Depth";			    float UIStep=0.0001; float UIMin=0.0;  float UIMax=1.0; > = {0.05};
UI_WHITESPACE(3)
UI_WHITESPACE(4)
UI_ELEMENT(_DOF_Header,"        >>>>>>DEPTH OF FIELD<<<<<<")
UI_WHITESPACE(5)
UI_ELEMENT(_DOF_DoFInfo,				       "|------- DOF")
float  UI_NearBlurCurve			<string UIName="|- DOF - Near Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.0};
float  UI_NearBlurBleed			<string UIName="|- DOF - Near Blur Bleeding";							 float UIMin=0.0;   float UIMax= 2.0;  > = {1.0};
float  UI_FarBlurCurve			<string UIName="|- DOF - Far Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.4};
#if ENABLE_FAR_BOKEH_FREEZING
bool   UI_FreezeFarBokeh		<string UIName="|- DOF - Freeze Far Bokeh";																       > = {false};
#endif
float  UI_HyperFocus			<string UIName="|- DOF - Hyperfocal Depth Distance"; float UIStep=0.001; float UIMin=0.0;   float UIMax=1.0;   > = {0.015};
bool   UI_RemoveFPSObjects      <string UIName="|- DOF - Remove FPS Objects";															       > = {true};
float  UI_RenderResMult			<string UIName="|- DOF - Blur Render Res mult";							 float UIMin=0.5;   float UIMax=1.0;   > = {0.5};
float  UI_SmootheningAmount		<string UIName="|- DOF - Gaussian PostBlur Width";						 float UIMin=0.0;   float UIMax=20.0;  > = {4.0};
int    UI_GaussQuality			<string UIName="|- DOF - Gaussian Quality";   string UIWidget="Quality"; int   UIMin=0;     int   UIMax=2;     > = {  1};
#if ENABLE_COC_DEBUGGING
int    UI_CoCDebug				<string UIName="|- DOF - CoC Debug";									 int   UIMin=0;     int   UIMax=4;     > = {  0};
#endif
UI_SPECIAL_WHITESPACE(4)
UI_ELEMENT(_DOF_BokehInfo,				       "|------- BOKEH")
float  UI_BokehIntensity		<string UIName="|- Bokeh - Intensity";									 float UIMin=0.0;   float UIMax=1.0;   > = {0.5};
float  UI_BokehCurve			<string UIName="|- Bokeh - Curve";										 float UIMin=0.0;   float UIMax=20.0;  > = {1.0};
float  UI_ShapeRadius			<string UIName="|- Bokeh - Shape Max Size";		     float UIStep=0.1;	 float UIMin=0.0;   float UIMax=100.0; > = {15.0};
int    UI_ShapeVertices			<string UIName="|- Bokeh - Shape Vertices";								 int   UIMin=3;     int   UIMax=9;     > = {6};
int    UI_ShapeQuality			<string UIName="|- Bokeh - Shape Quality";								 int   UIMin=2;     int   UIMax=50;    > = {5};
float  UI_ShapeCurvatureAmount	<string UIName="|- Bokeh - Shape Roundness";							 float UIMin=-1.0;  float UIMax=1.0;   > = {1.0};
float  UI_ShapeRotation			<string UIName="|- Bokeh - Shape Rotation (\xB0)";   float UIStep=1;	 float UIMin=0;     float UIMax=360;   > = {15};
float  UI_ShapeAnamorphRatio	<string UIName="|- Bokeh - Shape Aspect Ratio";							 float UIMin=0.0;   float UIMax=2.0;   > = {1.0};
bool   UI_ShapeCut				<string UIName="|- Bokeh - Cut Shape in Half";															       > = {false};

#if ENABLE_STYLIZED_BOKEHSHAPES
UI_SPECIAL_WHITESPACE(5)
UI_ELEMENT(_DOF_StyleInfo,				       "|------- STYLIZED BOKEH SHAPES")
bool   UI_EnableStyle			<string UIName="|- Style - Override Bokeh Shape";														    > = {false};
float  UI_StyleTex				<string UIName="|- Style - Choose Shape Texture";   float UIStep=1;		float UIMin=1.0; float UIMax=9.0;   > = {1.0};
float  UI_StyleIntensity		<string UIName="|- Style - Intensity";									float UIMin=0.0; float UIMax=1.0;   > = {1.0};
float  UI_StyleRadius			<string UIName="|- Style - Shape Max Size";		    float UIStep=0.1;	float UIMin=0.0; float UIMax=100.0; > = {15.0};
float  UI_StyleQualityLevel		<string UIName="|- Style - Shape Quality Level";    float UIStep=1;		float UIMin=1.0; float UIMax=4.0;   > = {2.0};
float  UI_StyleRotation			<string UIName="|- Style - Shape Rotation (\xB0)";  float UIStep=1;		float UIMin=0.0; float UIMax=359.0; > = {0.0};
float  UI_StyleSmoothening		<string UIName="|- Style - Gaussian Blur Override";						float UIMin=0.0; float UIMax=20.0;  > = {2.0};
#endif //ENABLE_STYLIZED_BOKEHSHAPES

#if ENABLE_SPHERICAL_ABERRATION
UI_SPECIAL_WHITESPACE(6)
UI_ELEMENT(_DOF_SAInfo,						       "|------- SPHERICAL ABERRATION")
float  UI_SphericalAmount		<string UIName="|- Bokeh - Shape SA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.1};
float  UI_SphericalCurve		<string UIName="|- Bokeh - Shape SA Curve";  float UIMin= 0.0; float UIMax=3.0; > = {0.25};
#endif //ENABLE_SPHERICAL_ABERRATION

#if ENABLE_DIFFRACTION
UI_SPECIAL_WHITESPACE(7)
UI_ELEMENT(_DOF_DiInfo,						       "|------- DIFFRACTION")
float  UI_DiffractionAmount		<string UIName="|- Bokeh - Diffraction Amount";    float UIMin=0.0;  float UIMax= 1.0; > = {0.25};
float  UI_DiffractionFreq		<string UIName="|- Bokeh - Diffraction Frequency"; float UIMin=0.01; float UIMax=20.0; > = {8.0};
#endif //ENABLE_DIFFRACTION

#if ENABLE_OPTICAL_VIGNETTE
UI_SPECIAL_WHITESPACE(9)
UI_ELEMENT(_DOF_OVInfo,						       "|------- OPTICAL VIGNETTE")
float  UI_ShapeVignetteCurve		<string UIName="|- Bokeh - Shape Vignette Curve";  float UIMin=0.5; float UIMax=2.5; > = {0.75};
float  UI_ShapeVignetteAmount		<string UIName="|- Bokeh - Shape Vignette Amount"; float UIMin=0.0; float UIMax=2.0; > = {1.0};
#endif //ENABLE_OPTICAL_VIGNETTE

#if ENABLE_CHROMATIC_ABERRATION
UI_SPECIAL_WHITESPACE(10)
UI_ELEMENT(_DOF_CAInfo,						       "|------- CHROMATIC ABERRATION")
float  UI_LongitudChromaAmount		<string UIName="|- Bokeh - Longitudinal CA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.3};
float  UI_LateralChromaAmount		<string UIName="|- Bokeh - Lateral CA Amount";      float UIMin=-1.0; float UIMax=1.0; > = {0.2};
float  UI_LateralChromaCurve		<string UIName="|- Bokeh - Lateral CA Curve";       float UIMin= 0.0; float UIMax=8.0; > = {1.3};
int    UI_ChromaMode				<string UIName="|- Bokeh - CA Type";                int   UIMin=   0; int   UIMax=  2; > = {2};
#endif

#if ENABLE_GRAINING == 1
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainAmount			<string UIName="|- Bokeh - Grain Amount"; float UIMin=0.0; float UIMax= 1.0; > = {0.1};
float UI_GrainSeed				<string UIName="|- Bokeh - Grain Seed";   float UIMin=0.0; float UIMax=10.0; > = {0.23};
#elif ENABLE_GRAINING == 2
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainInt				<string UIName="|- DOF - Grain Intensity";  float UIMin= 0.0; float UIMax=0.5; > = {0.05};
float UI_GrainSaturation		<string UIName="|- DOF - Grain Saturation"; float UIMin= 0.0; float UIMax=1.0; > = {0.5};
float UI_GrainMotion			<string UIName="|- DOF - Grain Motion";     float UIMin=-2.0; float UIMax=2.0; > = {0.1};
#endif //ENABLE_GRAINING


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_DOFCC_Header,"   >>>>>>DOF COLOR GRADING<<<<<<")
UI_WHITESPACE(9)
bool  UICG_Enable		<string UIName="|---- Enable DOF Color Grading";										> = {true};
int   UICG_Mask			<string UIName="|- DOFCG - CC Mask (1-Bokeh, 2-CoC)"; int   UIMin=1;   int   UIMax=2;   > = {1};
float UICG_ConGrayLvl	<string UIName="|- DOFCG - Contrast Gray Level";      float UIMin=0.0; float UIMax=1.0; > = {0.5};
UI_SPECIAL_WHITESPACE(11)
#endif //NOTFIRSTTIME

float SEPARATE_VAR(UICG_Saturation) <string UIName=TO_STRING(|- DOFCG - TODIE - Saturation); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Brightness) <string UIName=TO_STRING(|- DOFCG - TODIE - Brightness); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Contrast)   <string UIName=TO_STRING(|- DOFCG - TODIE - Contrast);   float UIMin=0.0; float UIMax=10.0; > = {1.0};


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

UI_ELEMENT(_DOFK_Header,"           >>>>>>DOF KEYING<<<<<<")
UI_WHITESPACE(10)
bool   UIK_Enable <string UIName="|---- Enable DOF Keying";										  > = {false};
int    UIK_Mask   <string UIName="|- DOFK - Key Mask (1-Bokeh, 2-DOF)"; int UIMin=1; int UIMax=2; > = {2};
float3 UIK_Color  <string UIName="|- DOFK - Keycolor";						string UIWidget="Color";  > = {0,1,0};

#endif //SHADERGROUP

#undef TODIE
//<<< end "UI/enbUI_DepthOfField.fxh"
#undef SHADERGROUP

//DOF Color Correction
UI_WHITESPACE(11)
UI_WHITESPACE(12)
#define SHADERGROUP 2
#define TODIE Day
//>>> Authoria: inlined "UI/enbUI_DepthOfField.fxh"
//----------------------------------------------------------------------------------------------//
//																								//
//						      Main ENB Depth of Field UI file									//
//						      by LonelyKitsuune aka Skratzer									//
//																								//
//----------------------------------------------------------------------------------------------//

//This file requires my UI Primer header to work!
#ifndef _UI_PRIMER_
#error UI_Primer couldnt be found!
#endif

//----------------------------------------------------------------------------------------------//
//								  User Interface Parameters										//
//																								//
//----------------------------------------------------------------------------------------------//


#if SHADERGROUP == 0

UI_FileHeaderLong(">>>          Avanced Depth of Field          <<<",
				  ">>>                Kitsuune Edition               <<<")
UI_WHITESPACE(1)


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

UI_ELEMENT(_Focus_Header,"               >>>>>>FOCUS<<<<<<")
UI_WHITESPACE(2)
int   UI_FocusType				<string UIName="|- Focus Type (1-Auto, 2-Mouse, 3-Manual)";				 int   UIMin=1;    int   UIMax=3;   > = {1};
#if ENABLE_FOCUSING_TOOL
bool  UI_VisualizeFocus			<string UIName="|- Visualize Focus";																	    > = {false};
#endif
UI_SPECIAL_WHITESPACE(1)
UI_ELEMENT(_DOF_FocusInfo1,				       "|- 1 - Autofocus")
float2 UI_AutofocusCenter		<string UIName="|- Autofocus Sample Center";							 float UIMin=0.00; float UIMax=1.0; > = {0.5,0.5};
float  UI_AutofocusRadius		<string UIName="|- Autofocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(2)
UI_ELEMENT(_DOF_FocusInfo2,				       "|- 2 - Mousefocus (right click to focus)")
float  UI_MousefocusRadius		<string UIName="|- Mousefocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(3)
UI_ELEMENT(_DOF_FocusInfo3,				       "|- 3 - Manual Focus")
float  UI_ManualfocusDepth		<string UIName="|- Manual Focus Depth";			    float UIStep=0.0001; float UIMin=0.0;  float UIMax=1.0; > = {0.05};
UI_WHITESPACE(3)
UI_WHITESPACE(4)
UI_ELEMENT(_DOF_Header,"        >>>>>>DEPTH OF FIELD<<<<<<")
UI_WHITESPACE(5)
UI_ELEMENT(_DOF_DoFInfo,				       "|------- DOF")
float  UI_NearBlurCurve			<string UIName="|- DOF - Near Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.0};
float  UI_NearBlurBleed			<string UIName="|- DOF - Near Blur Bleeding";							 float UIMin=0.0;   float UIMax= 2.0;  > = {1.0};
float  UI_FarBlurCurve			<string UIName="|- DOF - Far Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.4};
#if ENABLE_FAR_BOKEH_FREEZING
bool   UI_FreezeFarBokeh		<string UIName="|- DOF - Freeze Far Bokeh";																       > = {false};
#endif
float  UI_HyperFocus			<string UIName="|- DOF - Hyperfocal Depth Distance"; float UIStep=0.001; float UIMin=0.0;   float UIMax=1.0;   > = {0.015};
bool   UI_RemoveFPSObjects      <string UIName="|- DOF - Remove FPS Objects";															       > = {true};
float  UI_RenderResMult			<string UIName="|- DOF - Blur Render Res mult";							 float UIMin=0.5;   float UIMax=1.0;   > = {0.5};
float  UI_SmootheningAmount		<string UIName="|- DOF - Gaussian PostBlur Width";						 float UIMin=0.0;   float UIMax=20.0;  > = {4.0};
int    UI_GaussQuality			<string UIName="|- DOF - Gaussian Quality";   string UIWidget="Quality"; int   UIMin=0;     int   UIMax=2;     > = {  1};
#if ENABLE_COC_DEBUGGING
int    UI_CoCDebug				<string UIName="|- DOF - CoC Debug";									 int   UIMin=0;     int   UIMax=4;     > = {  0};
#endif
UI_SPECIAL_WHITESPACE(4)
UI_ELEMENT(_DOF_BokehInfo,				       "|------- BOKEH")
float  UI_BokehIntensity		<string UIName="|- Bokeh - Intensity";									 float UIMin=0.0;   float UIMax=1.0;   > = {0.5};
float  UI_BokehCurve			<string UIName="|- Bokeh - Curve";										 float UIMin=0.0;   float UIMax=20.0;  > = {1.0};
float  UI_ShapeRadius			<string UIName="|- Bokeh - Shape Max Size";		     float UIStep=0.1;	 float UIMin=0.0;   float UIMax=100.0; > = {15.0};
int    UI_ShapeVertices			<string UIName="|- Bokeh - Shape Vertices";								 int   UIMin=3;     int   UIMax=9;     > = {6};
int    UI_ShapeQuality			<string UIName="|- Bokeh - Shape Quality";								 int   UIMin=2;     int   UIMax=50;    > = {5};
float  UI_ShapeCurvatureAmount	<string UIName="|- Bokeh - Shape Roundness";							 float UIMin=-1.0;  float UIMax=1.0;   > = {1.0};
float  UI_ShapeRotation			<string UIName="|- Bokeh - Shape Rotation (\xB0)";   float UIStep=1;	 float UIMin=0;     float UIMax=360;   > = {15};
float  UI_ShapeAnamorphRatio	<string UIName="|- Bokeh - Shape Aspect Ratio";							 float UIMin=0.0;   float UIMax=2.0;   > = {1.0};
bool   UI_ShapeCut				<string UIName="|- Bokeh - Cut Shape in Half";															       > = {false};

#if ENABLE_STYLIZED_BOKEHSHAPES
UI_SPECIAL_WHITESPACE(5)
UI_ELEMENT(_DOF_StyleInfo,				       "|------- STYLIZED BOKEH SHAPES")
bool   UI_EnableStyle			<string UIName="|- Style - Override Bokeh Shape";														    > = {false};
float  UI_StyleTex				<string UIName="|- Style - Choose Shape Texture";   float UIStep=1;		float UIMin=1.0; float UIMax=9.0;   > = {1.0};
float  UI_StyleIntensity		<string UIName="|- Style - Intensity";									float UIMin=0.0; float UIMax=1.0;   > = {1.0};
float  UI_StyleRadius			<string UIName="|- Style - Shape Max Size";		    float UIStep=0.1;	float UIMin=0.0; float UIMax=100.0; > = {15.0};
float  UI_StyleQualityLevel		<string UIName="|- Style - Shape Quality Level";    float UIStep=1;		float UIMin=1.0; float UIMax=4.0;   > = {2.0};
float  UI_StyleRotation			<string UIName="|- Style - Shape Rotation (\xB0)";  float UIStep=1;		float UIMin=0.0; float UIMax=359.0; > = {0.0};
float  UI_StyleSmoothening		<string UIName="|- Style - Gaussian Blur Override";						float UIMin=0.0; float UIMax=20.0;  > = {2.0};
#endif //ENABLE_STYLIZED_BOKEHSHAPES

#if ENABLE_SPHERICAL_ABERRATION
UI_SPECIAL_WHITESPACE(6)
UI_ELEMENT(_DOF_SAInfo,						       "|------- SPHERICAL ABERRATION")
float  UI_SphericalAmount		<string UIName="|- Bokeh - Shape SA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.1};
float  UI_SphericalCurve		<string UIName="|- Bokeh - Shape SA Curve";  float UIMin= 0.0; float UIMax=3.0; > = {0.25};
#endif //ENABLE_SPHERICAL_ABERRATION

#if ENABLE_DIFFRACTION
UI_SPECIAL_WHITESPACE(7)
UI_ELEMENT(_DOF_DiInfo,						       "|------- DIFFRACTION")
float  UI_DiffractionAmount		<string UIName="|- Bokeh - Diffraction Amount";    float UIMin=0.0;  float UIMax= 1.0; > = {0.25};
float  UI_DiffractionFreq		<string UIName="|- Bokeh - Diffraction Frequency"; float UIMin=0.01; float UIMax=20.0; > = {8.0};
#endif //ENABLE_DIFFRACTION

#if ENABLE_OPTICAL_VIGNETTE
UI_SPECIAL_WHITESPACE(9)
UI_ELEMENT(_DOF_OVInfo,						       "|------- OPTICAL VIGNETTE")
float  UI_ShapeVignetteCurve		<string UIName="|- Bokeh - Shape Vignette Curve";  float UIMin=0.5; float UIMax=2.5; > = {0.75};
float  UI_ShapeVignetteAmount		<string UIName="|- Bokeh - Shape Vignette Amount"; float UIMin=0.0; float UIMax=2.0; > = {1.0};
#endif //ENABLE_OPTICAL_VIGNETTE

#if ENABLE_CHROMATIC_ABERRATION
UI_SPECIAL_WHITESPACE(10)
UI_ELEMENT(_DOF_CAInfo,						       "|------- CHROMATIC ABERRATION")
float  UI_LongitudChromaAmount		<string UIName="|- Bokeh - Longitudinal CA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.3};
float  UI_LateralChromaAmount		<string UIName="|- Bokeh - Lateral CA Amount";      float UIMin=-1.0; float UIMax=1.0; > = {0.2};
float  UI_LateralChromaCurve		<string UIName="|- Bokeh - Lateral CA Curve";       float UIMin= 0.0; float UIMax=8.0; > = {1.3};
int    UI_ChromaMode				<string UIName="|- Bokeh - CA Type";                int   UIMin=   0; int   UIMax=  2; > = {2};
#endif

#if ENABLE_GRAINING == 1
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainAmount			<string UIName="|- Bokeh - Grain Amount"; float UIMin=0.0; float UIMax= 1.0; > = {0.1};
float UI_GrainSeed				<string UIName="|- Bokeh - Grain Seed";   float UIMin=0.0; float UIMax=10.0; > = {0.23};
#elif ENABLE_GRAINING == 2
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainInt				<string UIName="|- DOF - Grain Intensity";  float UIMin= 0.0; float UIMax=0.5; > = {0.05};
float UI_GrainSaturation		<string UIName="|- DOF - Grain Saturation"; float UIMin= 0.0; float UIMax=1.0; > = {0.5};
float UI_GrainMotion			<string UIName="|- DOF - Grain Motion";     float UIMin=-2.0; float UIMax=2.0; > = {0.1};
#endif //ENABLE_GRAINING


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_DOFCC_Header,"   >>>>>>DOF COLOR GRADING<<<<<<")
UI_WHITESPACE(9)
bool  UICG_Enable		<string UIName="|---- Enable DOF Color Grading";										> = {true};
int   UICG_Mask			<string UIName="|- DOFCG - CC Mask (1-Bokeh, 2-CoC)"; int   UIMin=1;   int   UIMax=2;   > = {1};
float UICG_ConGrayLvl	<string UIName="|- DOFCG - Contrast Gray Level";      float UIMin=0.0; float UIMax=1.0; > = {0.5};
UI_SPECIAL_WHITESPACE(11)
#endif //NOTFIRSTTIME

float SEPARATE_VAR(UICG_Saturation) <string UIName=TO_STRING(|- DOFCG - TODIE - Saturation); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Brightness) <string UIName=TO_STRING(|- DOFCG - TODIE - Brightness); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Contrast)   <string UIName=TO_STRING(|- DOFCG - TODIE - Contrast);   float UIMin=0.0; float UIMax=10.0; > = {1.0};


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

UI_ELEMENT(_DOFK_Header,"           >>>>>>DOF KEYING<<<<<<")
UI_WHITESPACE(10)
bool   UIK_Enable <string UIName="|---- Enable DOF Keying";										  > = {false};
int    UIK_Mask   <string UIName="|- DOFK - Key Mask (1-Bokeh, 2-DOF)"; int UIMin=1; int UIMax=2; > = {2};
float3 UIK_Color  <string UIName="|- DOFK - Keycolor";						string UIWidget="Color";  > = {0,1,0};

#endif //SHADERGROUP

#undef TODIE
//<<< end "UI/enbUI_DepthOfField.fxh"
UI_SPECIAL_WHITESPACE(12)

#define TODIE Night
//>>> Authoria: inlined "UI/enbUI_DepthOfField.fxh"
//----------------------------------------------------------------------------------------------//
//																								//
//						      Main ENB Depth of Field UI file									//
//						      by LonelyKitsuune aka Skratzer									//
//																								//
//----------------------------------------------------------------------------------------------//

//This file requires my UI Primer header to work!
#ifndef _UI_PRIMER_
#error UI_Primer couldnt be found!
#endif

//----------------------------------------------------------------------------------------------//
//								  User Interface Parameters										//
//																								//
//----------------------------------------------------------------------------------------------//


#if SHADERGROUP == 0

UI_FileHeaderLong(">>>          Avanced Depth of Field          <<<",
				  ">>>                Kitsuune Edition               <<<")
UI_WHITESPACE(1)


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

UI_ELEMENT(_Focus_Header,"               >>>>>>FOCUS<<<<<<")
UI_WHITESPACE(2)
int   UI_FocusType				<string UIName="|- Focus Type (1-Auto, 2-Mouse, 3-Manual)";				 int   UIMin=1;    int   UIMax=3;   > = {1};
#if ENABLE_FOCUSING_TOOL
bool  UI_VisualizeFocus			<string UIName="|- Visualize Focus";																	    > = {false};
#endif
UI_SPECIAL_WHITESPACE(1)
UI_ELEMENT(_DOF_FocusInfo1,				       "|- 1 - Autofocus")
float2 UI_AutofocusCenter		<string UIName="|- Autofocus Sample Center";							 float UIMin=0.00; float UIMax=1.0; > = {0.5,0.5};
float  UI_AutofocusRadius		<string UIName="|- Autofocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(2)
UI_ELEMENT(_DOF_FocusInfo2,				       "|- 2 - Mousefocus (right click to focus)")
float  UI_MousefocusRadius		<string UIName="|- Mousefocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(3)
UI_ELEMENT(_DOF_FocusInfo3,				       "|- 3 - Manual Focus")
float  UI_ManualfocusDepth		<string UIName="|- Manual Focus Depth";			    float UIStep=0.0001; float UIMin=0.0;  float UIMax=1.0; > = {0.05};
UI_WHITESPACE(3)
UI_WHITESPACE(4)
UI_ELEMENT(_DOF_Header,"        >>>>>>DEPTH OF FIELD<<<<<<")
UI_WHITESPACE(5)
UI_ELEMENT(_DOF_DoFInfo,				       "|------- DOF")
float  UI_NearBlurCurve			<string UIName="|- DOF - Near Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.0};
float  UI_NearBlurBleed			<string UIName="|- DOF - Near Blur Bleeding";							 float UIMin=0.0;   float UIMax= 2.0;  > = {1.0};
float  UI_FarBlurCurve			<string UIName="|- DOF - Far Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.4};
#if ENABLE_FAR_BOKEH_FREEZING
bool   UI_FreezeFarBokeh		<string UIName="|- DOF - Freeze Far Bokeh";																       > = {false};
#endif
float  UI_HyperFocus			<string UIName="|- DOF - Hyperfocal Depth Distance"; float UIStep=0.001; float UIMin=0.0;   float UIMax=1.0;   > = {0.015};
bool   UI_RemoveFPSObjects      <string UIName="|- DOF - Remove FPS Objects";															       > = {true};
float  UI_RenderResMult			<string UIName="|- DOF - Blur Render Res mult";							 float UIMin=0.5;   float UIMax=1.0;   > = {0.5};
float  UI_SmootheningAmount		<string UIName="|- DOF - Gaussian PostBlur Width";						 float UIMin=0.0;   float UIMax=20.0;  > = {4.0};
int    UI_GaussQuality			<string UIName="|- DOF - Gaussian Quality";   string UIWidget="Quality"; int   UIMin=0;     int   UIMax=2;     > = {  1};
#if ENABLE_COC_DEBUGGING
int    UI_CoCDebug				<string UIName="|- DOF - CoC Debug";									 int   UIMin=0;     int   UIMax=4;     > = {  0};
#endif
UI_SPECIAL_WHITESPACE(4)
UI_ELEMENT(_DOF_BokehInfo,				       "|------- BOKEH")
float  UI_BokehIntensity		<string UIName="|- Bokeh - Intensity";									 float UIMin=0.0;   float UIMax=1.0;   > = {0.5};
float  UI_BokehCurve			<string UIName="|- Bokeh - Curve";										 float UIMin=0.0;   float UIMax=20.0;  > = {1.0};
float  UI_ShapeRadius			<string UIName="|- Bokeh - Shape Max Size";		     float UIStep=0.1;	 float UIMin=0.0;   float UIMax=100.0; > = {15.0};
int    UI_ShapeVertices			<string UIName="|- Bokeh - Shape Vertices";								 int   UIMin=3;     int   UIMax=9;     > = {6};
int    UI_ShapeQuality			<string UIName="|- Bokeh - Shape Quality";								 int   UIMin=2;     int   UIMax=50;    > = {5};
float  UI_ShapeCurvatureAmount	<string UIName="|- Bokeh - Shape Roundness";							 float UIMin=-1.0;  float UIMax=1.0;   > = {1.0};
float  UI_ShapeRotation			<string UIName="|- Bokeh - Shape Rotation (\xB0)";   float UIStep=1;	 float UIMin=0;     float UIMax=360;   > = {15};
float  UI_ShapeAnamorphRatio	<string UIName="|- Bokeh - Shape Aspect Ratio";							 float UIMin=0.0;   float UIMax=2.0;   > = {1.0};
bool   UI_ShapeCut				<string UIName="|- Bokeh - Cut Shape in Half";															       > = {false};

#if ENABLE_STYLIZED_BOKEHSHAPES
UI_SPECIAL_WHITESPACE(5)
UI_ELEMENT(_DOF_StyleInfo,				       "|------- STYLIZED BOKEH SHAPES")
bool   UI_EnableStyle			<string UIName="|- Style - Override Bokeh Shape";														    > = {false};
float  UI_StyleTex				<string UIName="|- Style - Choose Shape Texture";   float UIStep=1;		float UIMin=1.0; float UIMax=9.0;   > = {1.0};
float  UI_StyleIntensity		<string UIName="|- Style - Intensity";									float UIMin=0.0; float UIMax=1.0;   > = {1.0};
float  UI_StyleRadius			<string UIName="|- Style - Shape Max Size";		    float UIStep=0.1;	float UIMin=0.0; float UIMax=100.0; > = {15.0};
float  UI_StyleQualityLevel		<string UIName="|- Style - Shape Quality Level";    float UIStep=1;		float UIMin=1.0; float UIMax=4.0;   > = {2.0};
float  UI_StyleRotation			<string UIName="|- Style - Shape Rotation (\xB0)";  float UIStep=1;		float UIMin=0.0; float UIMax=359.0; > = {0.0};
float  UI_StyleSmoothening		<string UIName="|- Style - Gaussian Blur Override";						float UIMin=0.0; float UIMax=20.0;  > = {2.0};
#endif //ENABLE_STYLIZED_BOKEHSHAPES

#if ENABLE_SPHERICAL_ABERRATION
UI_SPECIAL_WHITESPACE(6)
UI_ELEMENT(_DOF_SAInfo,						       "|------- SPHERICAL ABERRATION")
float  UI_SphericalAmount		<string UIName="|- Bokeh - Shape SA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.1};
float  UI_SphericalCurve		<string UIName="|- Bokeh - Shape SA Curve";  float UIMin= 0.0; float UIMax=3.0; > = {0.25};
#endif //ENABLE_SPHERICAL_ABERRATION

#if ENABLE_DIFFRACTION
UI_SPECIAL_WHITESPACE(7)
UI_ELEMENT(_DOF_DiInfo,						       "|------- DIFFRACTION")
float  UI_DiffractionAmount		<string UIName="|- Bokeh - Diffraction Amount";    float UIMin=0.0;  float UIMax= 1.0; > = {0.25};
float  UI_DiffractionFreq		<string UIName="|- Bokeh - Diffraction Frequency"; float UIMin=0.01; float UIMax=20.0; > = {8.0};
#endif //ENABLE_DIFFRACTION

#if ENABLE_OPTICAL_VIGNETTE
UI_SPECIAL_WHITESPACE(9)
UI_ELEMENT(_DOF_OVInfo,						       "|------- OPTICAL VIGNETTE")
float  UI_ShapeVignetteCurve		<string UIName="|- Bokeh - Shape Vignette Curve";  float UIMin=0.5; float UIMax=2.5; > = {0.75};
float  UI_ShapeVignetteAmount		<string UIName="|- Bokeh - Shape Vignette Amount"; float UIMin=0.0; float UIMax=2.0; > = {1.0};
#endif //ENABLE_OPTICAL_VIGNETTE

#if ENABLE_CHROMATIC_ABERRATION
UI_SPECIAL_WHITESPACE(10)
UI_ELEMENT(_DOF_CAInfo,						       "|------- CHROMATIC ABERRATION")
float  UI_LongitudChromaAmount		<string UIName="|- Bokeh - Longitudinal CA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.3};
float  UI_LateralChromaAmount		<string UIName="|- Bokeh - Lateral CA Amount";      float UIMin=-1.0; float UIMax=1.0; > = {0.2};
float  UI_LateralChromaCurve		<string UIName="|- Bokeh - Lateral CA Curve";       float UIMin= 0.0; float UIMax=8.0; > = {1.3};
int    UI_ChromaMode				<string UIName="|- Bokeh - CA Type";                int   UIMin=   0; int   UIMax=  2; > = {2};
#endif

#if ENABLE_GRAINING == 1
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainAmount			<string UIName="|- Bokeh - Grain Amount"; float UIMin=0.0; float UIMax= 1.0; > = {0.1};
float UI_GrainSeed				<string UIName="|- Bokeh - Grain Seed";   float UIMin=0.0; float UIMax=10.0; > = {0.23};
#elif ENABLE_GRAINING == 2
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainInt				<string UIName="|- DOF - Grain Intensity";  float UIMin= 0.0; float UIMax=0.5; > = {0.05};
float UI_GrainSaturation		<string UIName="|- DOF - Grain Saturation"; float UIMin= 0.0; float UIMax=1.0; > = {0.5};
float UI_GrainMotion			<string UIName="|- DOF - Grain Motion";     float UIMin=-2.0; float UIMax=2.0; > = {0.1};
#endif //ENABLE_GRAINING


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_DOFCC_Header,"   >>>>>>DOF COLOR GRADING<<<<<<")
UI_WHITESPACE(9)
bool  UICG_Enable		<string UIName="|---- Enable DOF Color Grading";										> = {true};
int   UICG_Mask			<string UIName="|- DOFCG - CC Mask (1-Bokeh, 2-CoC)"; int   UIMin=1;   int   UIMax=2;   > = {1};
float UICG_ConGrayLvl	<string UIName="|- DOFCG - Contrast Gray Level";      float UIMin=0.0; float UIMax=1.0; > = {0.5};
UI_SPECIAL_WHITESPACE(11)
#endif //NOTFIRSTTIME

float SEPARATE_VAR(UICG_Saturation) <string UIName=TO_STRING(|- DOFCG - TODIE - Saturation); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Brightness) <string UIName=TO_STRING(|- DOFCG - TODIE - Brightness); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Contrast)   <string UIName=TO_STRING(|- DOFCG - TODIE - Contrast);   float UIMin=0.0; float UIMax=10.0; > = {1.0};


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

UI_ELEMENT(_DOFK_Header,"           >>>>>>DOF KEYING<<<<<<")
UI_WHITESPACE(10)
bool   UIK_Enable <string UIName="|---- Enable DOF Keying";										  > = {false};
int    UIK_Mask   <string UIName="|- DOFK - Key Mask (1-Bokeh, 2-DOF)"; int UIMin=1; int UIMax=2; > = {2};
float3 UIK_Color  <string UIName="|- DOFK - Keycolor";						string UIWidget="Color";  > = {0,1,0};

#endif //SHADERGROUP

#undef TODIE
//<<< end "UI/enbUI_DepthOfField.fxh"
UI_SPECIAL_WHITESPACE(13)

#define TODIE Interior
//>>> Authoria: inlined "UI/enbUI_DepthOfField.fxh"
//----------------------------------------------------------------------------------------------//
//																								//
//						      Main ENB Depth of Field UI file									//
//						      by LonelyKitsuune aka Skratzer									//
//																								//
//----------------------------------------------------------------------------------------------//

//This file requires my UI Primer header to work!
#ifndef _UI_PRIMER_
#error UI_Primer couldnt be found!
#endif

//----------------------------------------------------------------------------------------------//
//								  User Interface Parameters										//
//																								//
//----------------------------------------------------------------------------------------------//


#if SHADERGROUP == 0

UI_FileHeaderLong(">>>          Avanced Depth of Field          <<<",
				  ">>>                Kitsuune Edition               <<<")
UI_WHITESPACE(1)


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

UI_ELEMENT(_Focus_Header,"               >>>>>>FOCUS<<<<<<")
UI_WHITESPACE(2)
int   UI_FocusType				<string UIName="|- Focus Type (1-Auto, 2-Mouse, 3-Manual)";				 int   UIMin=1;    int   UIMax=3;   > = {1};
#if ENABLE_FOCUSING_TOOL
bool  UI_VisualizeFocus			<string UIName="|- Visualize Focus";																	    > = {false};
#endif
UI_SPECIAL_WHITESPACE(1)
UI_ELEMENT(_DOF_FocusInfo1,				       "|- 1 - Autofocus")
float2 UI_AutofocusCenter		<string UIName="|- Autofocus Sample Center";							 float UIMin=0.00; float UIMax=1.0; > = {0.5,0.5};
float  UI_AutofocusRadius		<string UIName="|- Autofocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(2)
UI_ELEMENT(_DOF_FocusInfo2,				       "|- 2 - Mousefocus (right click to focus)")
float  UI_MousefocusRadius		<string UIName="|- Mousefocus Sample Radius";							 float UIMin=0.01; float UIMax=1.0; > = {0.05};
UI_SPECIAL_WHITESPACE(3)
UI_ELEMENT(_DOF_FocusInfo3,				       "|- 3 - Manual Focus")
float  UI_ManualfocusDepth		<string UIName="|- Manual Focus Depth";			    float UIStep=0.0001; float UIMin=0.0;  float UIMax=1.0; > = {0.05};
UI_WHITESPACE(3)
UI_WHITESPACE(4)
UI_ELEMENT(_DOF_Header,"        >>>>>>DEPTH OF FIELD<<<<<<")
UI_WHITESPACE(5)
UI_ELEMENT(_DOF_DoFInfo,				       "|------- DOF")
float  UI_NearBlurCurve			<string UIName="|- DOF - Near Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.0};
float  UI_NearBlurBleed			<string UIName="|- DOF - Near Blur Bleeding";							 float UIMin=0.0;   float UIMax= 2.0;  > = {1.0};
float  UI_FarBlurCurve			<string UIName="|- DOF - Far Blur Curve";								 float UIMin=0.01;  float UIMax=20.0;  > = {1.4};
#if ENABLE_FAR_BOKEH_FREEZING
bool   UI_FreezeFarBokeh		<string UIName="|- DOF - Freeze Far Bokeh";																       > = {false};
#endif
float  UI_HyperFocus			<string UIName="|- DOF - Hyperfocal Depth Distance"; float UIStep=0.001; float UIMin=0.0;   float UIMax=1.0;   > = {0.015};
bool   UI_RemoveFPSObjects      <string UIName="|- DOF - Remove FPS Objects";															       > = {true};
float  UI_RenderResMult			<string UIName="|- DOF - Blur Render Res mult";							 float UIMin=0.5;   float UIMax=1.0;   > = {0.5};
float  UI_SmootheningAmount		<string UIName="|- DOF - Gaussian PostBlur Width";						 float UIMin=0.0;   float UIMax=20.0;  > = {4.0};
int    UI_GaussQuality			<string UIName="|- DOF - Gaussian Quality";   string UIWidget="Quality"; int   UIMin=0;     int   UIMax=2;     > = {  1};
#if ENABLE_COC_DEBUGGING
int    UI_CoCDebug				<string UIName="|- DOF - CoC Debug";									 int   UIMin=0;     int   UIMax=4;     > = {  0};
#endif
UI_SPECIAL_WHITESPACE(4)
UI_ELEMENT(_DOF_BokehInfo,				       "|------- BOKEH")
float  UI_BokehIntensity		<string UIName="|- Bokeh - Intensity";									 float UIMin=0.0;   float UIMax=1.0;   > = {0.5};
float  UI_BokehCurve			<string UIName="|- Bokeh - Curve";										 float UIMin=0.0;   float UIMax=20.0;  > = {1.0};
float  UI_ShapeRadius			<string UIName="|- Bokeh - Shape Max Size";		     float UIStep=0.1;	 float UIMin=0.0;   float UIMax=100.0; > = {15.0};
int    UI_ShapeVertices			<string UIName="|- Bokeh - Shape Vertices";								 int   UIMin=3;     int   UIMax=9;     > = {6};
int    UI_ShapeQuality			<string UIName="|- Bokeh - Shape Quality";								 int   UIMin=2;     int   UIMax=50;    > = {5};
float  UI_ShapeCurvatureAmount	<string UIName="|- Bokeh - Shape Roundness";							 float UIMin=-1.0;  float UIMax=1.0;   > = {1.0};
float  UI_ShapeRotation			<string UIName="|- Bokeh - Shape Rotation (\xB0)";   float UIStep=1;	 float UIMin=0;     float UIMax=360;   > = {15};
float  UI_ShapeAnamorphRatio	<string UIName="|- Bokeh - Shape Aspect Ratio";							 float UIMin=0.0;   float UIMax=2.0;   > = {1.0};
bool   UI_ShapeCut				<string UIName="|- Bokeh - Cut Shape in Half";															       > = {false};

#if ENABLE_STYLIZED_BOKEHSHAPES
UI_SPECIAL_WHITESPACE(5)
UI_ELEMENT(_DOF_StyleInfo,				       "|------- STYLIZED BOKEH SHAPES")
bool   UI_EnableStyle			<string UIName="|- Style - Override Bokeh Shape";														    > = {false};
float  UI_StyleTex				<string UIName="|- Style - Choose Shape Texture";   float UIStep=1;		float UIMin=1.0; float UIMax=9.0;   > = {1.0};
float  UI_StyleIntensity		<string UIName="|- Style - Intensity";									float UIMin=0.0; float UIMax=1.0;   > = {1.0};
float  UI_StyleRadius			<string UIName="|- Style - Shape Max Size";		    float UIStep=0.1;	float UIMin=0.0; float UIMax=100.0; > = {15.0};
float  UI_StyleQualityLevel		<string UIName="|- Style - Shape Quality Level";    float UIStep=1;		float UIMin=1.0; float UIMax=4.0;   > = {2.0};
float  UI_StyleRotation			<string UIName="|- Style - Shape Rotation (\xB0)";  float UIStep=1;		float UIMin=0.0; float UIMax=359.0; > = {0.0};
float  UI_StyleSmoothening		<string UIName="|- Style - Gaussian Blur Override";						float UIMin=0.0; float UIMax=20.0;  > = {2.0};
#endif //ENABLE_STYLIZED_BOKEHSHAPES

#if ENABLE_SPHERICAL_ABERRATION
UI_SPECIAL_WHITESPACE(6)
UI_ELEMENT(_DOF_SAInfo,						       "|------- SPHERICAL ABERRATION")
float  UI_SphericalAmount		<string UIName="|- Bokeh - Shape SA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.1};
float  UI_SphericalCurve		<string UIName="|- Bokeh - Shape SA Curve";  float UIMin= 0.0; float UIMax=3.0; > = {0.25};
#endif //ENABLE_SPHERICAL_ABERRATION

#if ENABLE_DIFFRACTION
UI_SPECIAL_WHITESPACE(7)
UI_ELEMENT(_DOF_DiInfo,						       "|------- DIFFRACTION")
float  UI_DiffractionAmount		<string UIName="|- Bokeh - Diffraction Amount";    float UIMin=0.0;  float UIMax= 1.0; > = {0.25};
float  UI_DiffractionFreq		<string UIName="|- Bokeh - Diffraction Frequency"; float UIMin=0.01; float UIMax=20.0; > = {8.0};
#endif //ENABLE_DIFFRACTION

#if ENABLE_OPTICAL_VIGNETTE
UI_SPECIAL_WHITESPACE(9)
UI_ELEMENT(_DOF_OVInfo,						       "|------- OPTICAL VIGNETTE")
float  UI_ShapeVignetteCurve		<string UIName="|- Bokeh - Shape Vignette Curve";  float UIMin=0.5; float UIMax=2.5; > = {0.75};
float  UI_ShapeVignetteAmount		<string UIName="|- Bokeh - Shape Vignette Amount"; float UIMin=0.0; float UIMax=2.0; > = {1.0};
#endif //ENABLE_OPTICAL_VIGNETTE

#if ENABLE_CHROMATIC_ABERRATION
UI_SPECIAL_WHITESPACE(10)
UI_ELEMENT(_DOF_CAInfo,						       "|------- CHROMATIC ABERRATION")
float  UI_LongitudChromaAmount		<string UIName="|- Bokeh - Longitudinal CA Amount"; float UIMin=-1.0; float UIMax=1.0; > = {0.3};
float  UI_LateralChromaAmount		<string UIName="|- Bokeh - Lateral CA Amount";      float UIMin=-1.0; float UIMax=1.0; > = {0.2};
float  UI_LateralChromaCurve		<string UIName="|- Bokeh - Lateral CA Curve";       float UIMin= 0.0; float UIMax=8.0; > = {1.3};
int    UI_ChromaMode				<string UIName="|- Bokeh - CA Type";                int   UIMin=   0; int   UIMax=  2; > = {2};
#endif

#if ENABLE_GRAINING == 1
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainAmount			<string UIName="|- Bokeh - Grain Amount"; float UIMin=0.0; float UIMax= 1.0; > = {0.1};
float UI_GrainSeed				<string UIName="|- Bokeh - Grain Seed";   float UIMin=0.0; float UIMax=10.0; > = {0.23};
#elif ENABLE_GRAINING == 2
UI_SPECIAL_WHITESPACE(8)
UI_ELEMENT(_DOF_GInfo,						       "|------- GRAINING")
float UI_GrainInt				<string UIName="|- DOF - Grain Intensity";  float UIMin= 0.0; float UIMax=0.5; > = {0.05};
float UI_GrainSaturation		<string UIName="|- DOF - Grain Saturation"; float UIMin= 0.0; float UIMax=1.0; > = {0.5};
float UI_GrainMotion			<string UIName="|- DOF - Grain Motion";     float UIMin=-2.0; float UIMax=2.0; > = {0.1};
#endif //ENABLE_GRAINING


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_DOFCC_Header,"   >>>>>>DOF COLOR GRADING<<<<<<")
UI_WHITESPACE(9)
bool  UICG_Enable		<string UIName="|---- Enable DOF Color Grading";										> = {true};
int   UICG_Mask			<string UIName="|- DOFCG - CC Mask (1-Bokeh, 2-CoC)"; int   UIMin=1;   int   UIMax=2;   > = {1};
float UICG_ConGrayLvl	<string UIName="|- DOFCG - Contrast Gray Level";      float UIMin=0.0; float UIMax=1.0; > = {0.5};
UI_SPECIAL_WHITESPACE(11)
#endif //NOTFIRSTTIME

float SEPARATE_VAR(UICG_Saturation) <string UIName=TO_STRING(|- DOFCG - TODIE - Saturation); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Brightness) <string UIName=TO_STRING(|- DOFCG - TODIE - Brightness); float UIMin=0.0; float UIMax=10.0; > = {1.0};
float SEPARATE_VAR(UICG_Contrast)   <string UIName=TO_STRING(|- DOFCG - TODIE - Contrast);   float UIMin=0.0; float UIMax=10.0; > = {1.0};


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

UI_ELEMENT(_DOFK_Header,"           >>>>>>DOF KEYING<<<<<<")
UI_WHITESPACE(10)
bool   UIK_Enable <string UIName="|---- Enable DOF Keying";										  > = {false};
int    UIK_Mask   <string UIName="|- DOFK - Key Mask (1-Bokeh, 2-DOF)"; int UIMin=1; int UIMax=2; > = {2};
float3 UIK_Color  <string UIName="|- DOFK - Keycolor";						string UIWidget="Color";  > = {0,1,0};

#endif //SHADERGROUP

#undef TODIE
//<<< end "UI/enbUI_DepthOfField.fxh"
UI_WHITESPACE(13)
UI_WHITESPACE(14)
#undef SHADERGROUP
#undef NOTFIRSTTIME


//----------------------------------------------------------------------------------------------//
//						     External enb parameters, do not modify								//
//																								//
//----------------------------------------------------------------------------------------------//
float4 Timer;			// x = generic timer in range 0..1, period of 16777216 ms (4.6 hours), y = average fps,
						// z = frame number (cyclically wraps to 0 after 9999 frames passed), w = frame time elapsed (in seconds)
float4 ScreenSize;		// x = Width, y = 1/Width, z = aspect, w = 1/aspect, aspect is Width/Height
float  AdaptiveQuality;	// changes in range 0..1, 0 means full quality, 1 lowest dynamic quality (0.33, 0.66 are limits for quality levels)
float4 TimeOfDay1;		// x = dawn, y = sunrise, z = day, w = sunset. Interpolators range from 0..1
float4 TimeOfDay2;		// x = dusk, y = night. Interpolators range from 0..1
float  ENightDayFactor;	// changes in range 0..1, 0 means that night time, 1 - day time
float  EInteriorFactor;	// changes 0 or 1. 0 means that exterior, 1 - interior
float  FieldOfView;		// FOV in degrees
float4 Weather;			// x = current weather index, y = outgoing weather index, z = weather transition, w = time of the day in 24 standard hours.
						// Weather index is value from weather ini file, for example WEATHER002 means index==2, but index==0 means that weather not captured.
						// -> Needs ENB Helper skse64 plugin to work correctly!
float4 DofParameters;	// z = ApertureTime multiplied by time elapsed, w = FocusingTime multiplied by time elapsed


//----------------------------------------------------------------------------------------------//
//						       External enb debugging parameters for							//
//								 shader programmers, do not modify								//
//----------------------------------------------------------------------------------------------//
float4 tempF1; //0,1,2,3
float4 tempF2; //5,6,7,8
float4 tempF3; //9,0
//keyboard controlled temporary variables. Press and hold key 1,2,3...8 together with PageUp or PageDown to modify.
//By default all set to 1.0

float4 tempInfo1;
// xy = cursor position in range 0..1 of screen;
// z = is shader editor window active;
// w = mouse buttons with values 0..7 as follows:
//    0 = none
//    1 = left
//    2 = right
//    3 = left+right
//    4 = middle
//    5 = left+middle
//    6 = right+middle
//    7 = left+right+middle (or rather cat is sitting on your mouse)

float4 tempInfo2;
// xy = cursor position of previous left mouse button click
// zw = cursor position of previous right mouse button click


//----------------------------------------------------------------------------------------------//
//						      Game and mod parameters, do not modify							//
//																								//
//----------------------------------------------------------------------------------------------//

Texture2D TextureCurrent; 		//current frame focus depth or aperture. unused in dof computation
Texture2D TexturePrevious; 		//previous frame focus depth or aperture. unused in dof computation
Texture2D TextureOriginal; 		//color R16B16G16A16 64 bit hdr format
Texture2D TextureColor; 		//color which is output of previous technique (except when drawed to temporary render target), R16B16G16A16 64 bit hdr format
Texture2D TextureDepth; 		//scene depth R32F 32 bit hdr format
Texture2D TextureFocus; 		//this frame focus 1*1 R32F hdr red channel only. computed in PS_Focus
Texture2D TextureAperture; 		//this frame aperture 1*1 R32F hdr red channel only. computed in PS_Aperture
Texture2D TextureAdaptation;	//previous frame vanilla or enb adaptation 1*1 R32F hdr red channel only (computed after depth of field)

//temporary textures which can be set as render target for techniques via annotations like <string RenderTarget="RenderTargetRGBA32";>
Texture2D RenderTargetRGBA32; 		//R8G8B8A8		32 bit ldr format
Texture2D RenderTargetRGBA64; 		//R16B16G16A16	64 bit ldr format
Texture2D RenderTargetRGBA64F; 		//R16B16G16A16F 64 bit hdr format
Texture2D RenderTargetR16F; 		//R16F			16 bit hdr format with red channel only
Texture2D RenderTargetR32F; 		//R32F			32 bit hdr format with red channel only
Texture2D RenderTargetRGB32F; 		//R8G8B8F		32 bit hdr format without alpha

SamplerState Point_Sampler
{
	Filter = MIN_MAG_MIP_POINT;
	AddressU = Clamp;
	AddressV = Clamp;
};

SamplerState Linear_Sampler
{
	Filter = MIN_MAG_MIP_LINEAR;
	AddressU = Clamp;
	AddressV = Clamp;
};

//Helper with some useful macros, variables and functions
//>>> Authoria: inlined "Helper/enbHelper_Common.fxh"
//----------------------------------------------------------------------------------------------//
//																								//
//					   Common helper library by LonelyKitsuune aka Skratzer						//
//								 for ENB (DirectX 11 Shader Model 5)							//
//																								//
//			   Copyright (c) 2019-2020 LonelyKitsuune / T.Thanner - CC BY-NC-ND 4.0				//
//																								//
//----------------------------------------------------------------------------------------------//

//Include debugging helper if needed
//#include "Helper/enbHelper_Debug.fxh"


//----------------------------------------------------------------------------------------------//

//Some useful variable macros
#define LUM_709	float3(0.2125, 0.7154, 0.0721)
#define LUM_601	float3(0.2989, 0.5870, 0.1140)
#define K_LUM	float3(0.25,   0.60,   0.15)
#define ALT_LUM	float3(0.25,   0.50,   0.25)
#define N_LUM	0.333333
#define DELTA	1e-6//1e-8
#define PI		3.1415926535897932384626433832795

//And some useful variables
static const float2 PixelSize = float2(ScreenSize.y, ScreenSize.y * ScreenSize.z);
static const float2 ScreenRes = float2(ScreenSize.x, ScreenSize.x * ScreenSize.w); //(Width,Height)

//Shorter syntax
#define NI nointerpolation


//----------------------------------------------------------------------------------------------//
//Macros for basic technique setups
#define TECH11(NAME, VS, PS) \
technique11 NAME {pass p0 {SetVertexShader(CompileShader(vs_5_0, VS));\
						   SetPixelShader (CompileShader(ps_5_0, PS));}}

#define TWOPASSTECH11(NAME, VS1, PS1, VS2, PS2) \
technique11 NAME {pass p0 {SetVertexShader(CompileShader(vs_5_0, VS1));\
						   SetPixelShader (CompileShader(ps_5_0, PS1));}\
				  pass p1 {SetVertexShader(CompileShader(vs_5_0, VS2));\
						   SetPixelShader (CompileShader(ps_5_0, PS2));}}


//Technique macros for pre-compiled shaders
#define TECH11_COMP(NAME, VS, PS) \
technique11 NAME {pass p0 {SetVertexShader(VS);  SetPixelShader(PS);}}

#define TWOPASSTECH11_COMP(NAME, VS1, PS1, VS2, PS2) \
technique11 NAME {pass p0 {SetVertexShader(VS1); SetPixelShader(PS1);}\
				  pass p1 {SetVertexShader(VS2); SetPixelShader(PS2);}}


//Basic vertex shader and blank pixel shader to clear out rendertargets if needed
void   VS_Basic(inout float4 pos : SV_POSITION, inout float4 txcoord : TEXCOORD0) { pos.w= 1.0; }
float4 PS_Blank(float4 pos : SV_POSITION, float4 txcoord : TEXCOORD0) : SV_Target { return 0.0; }


//----------------------------------------------------------------------------------------------//

//TODIE Separations
float  TODIESep(float  Dawn, float  Sunrise, float  Day, float  Sunset, float  Dusk, float  Night, float  Interior)
{ return lerp(TimeOfDay1.x * Dawn   + TimeOfDay1.y * Sunrise + TimeOfDay1.z * Day +
		      TimeOfDay1.w * Sunset + TimeOfDay2.x * Dusk    + TimeOfDay2.y * Night, Interior, EInteriorFactor); }

float3 TODIESep(float3 Dawn, float3 Sunrise, float3 Day, float3 Sunset, float3 Dusk, float3 Night, float3 Interior)
{ return lerp(TimeOfDay1.x * Dawn   + TimeOfDay1.y * Sunrise + TimeOfDay1.z * Day +
		      TimeOfDay1.w * Sunset + TimeOfDay2.x * Dusk    + TimeOfDay2.y * Night, Interior, EInteriorFactor); }

#define TODIE_SEPARATION(x) TODIESep(Dawn_##x, Sunrise_##x, Day_##x, Sunset_##x, Dusk_##x, Night_##x, Interior_##x)


//TODIE Separations (Dawn and Dusk to Twilight)
float  TODIETLSep(float  Twilight, float  Sunrise, float  Day, float  Sunset, float  Night, float  Interior)
{ return lerp(TimeOfDay1.x * Twilight + TimeOfDay1.y * Sunrise  + TimeOfDay1.z * Day +
		      TimeOfDay1.w * Sunset   + TimeOfDay2.x * Twilight + TimeOfDay2.y * Night, Interior, EInteriorFactor); }

float3 TODIETLSep(float3 Twilight, float3 Sunrise, float3 Day, float3 Sunset, float3 Night, float3 Interior)
{ return lerp(TimeOfDay1.x * Twilight + TimeOfDay1.y * Sunrise  + TimeOfDay1.z * Day +
		      TimeOfDay1.w * Sunset   + TimeOfDay2.x * Twilight + TimeOfDay2.y * Night, Interior, EInteriorFactor); }

#define TODIETL_SEPARATION(x) TODIETLSep(Twilight_##x, Sunrise_##x, Day_##x, Sunset_##x, Night_##x, Interior_##x)


//DNI Separations
float  DNISep(float  Day, float  Night, float  Interior)
{ return lerp(lerp(Night, Day, ENightDayFactor), Interior, EInteriorFactor); }

float3 DNISep(float3 Day, float3 Night, float3 Interior)
{ return lerp(lerp(Night, Day, ENightDayFactor), Interior, EInteriorFactor); }

#define DNI_SEPARATION(x) DNISep(Day_##x, Night_##x, Interior_##x)


//DNIE Separations
float  DNIESep(float  Day, float  Night, float  IDay, float  INight)
{ return lerp(lerp(Night, Day, ENightDayFactor), lerp(INight, IDay, ENightDayFactor), EInteriorFactor); }

float3 DNIESep(float3 Day, float3 Night, float3 IDay, float3 INight)
{ return lerp(lerp(Night, Day, ENightDayFactor), lerp(INight, IDay, ENightDayFactor), EInteriorFactor); }

#define DNIE_SEPARATION(x) DNIESep(Day_##x, Night_##x, InteriorDay_##x, InteriorNight_##x)


//IE Separations
float  IESep(float  Exterior, float  Interior)
{ return lerp(Exterior, Interior, EInteriorFactor); }

float3 IESep(float3 Exterior, float3 Interior)
{ return lerp(Exterior, Interior, EInteriorFactor); }

#define IE_SEPARATION(x) IESep(Exterior_##x, Interior_##x)


//----------------------------------------------------------------------------------------------//
//Various functions

//Returns scaled texcoords for a four-tile texture atlas
float2 AtlasFetch_4(float2 Coord, uint TexSelect)
{ static const float2 TexPos[4] = {0.0,0.0, 0.5,0.0, 0.0,0.5, 0.5,0.5};
  return mad(Coord, 0.5, TexPos[TexSelect-1]); }


//Highpass filter with limiting shoulder
float LimitedHighPass(float x, float Thresh, float Curve, float Shoulder)
{
		x = pow(x / Thresh, Thresh * Curve * 2.0);
		x = min(x, pow(Curve,4) * Shoulder);
		return (x * Shoulder) / (x + Thresh);
}


//Maps x [0,1] to specific range
float MapToRange(float x, float Min, float Max)
{ return x * (Max - Min) + Min; }
//MapToRange(LinearStep(IMin, IMax, x), OMin, OMax);


//Simplified diffraction
float Diffraction(float x, float freq, float phase, float ampli)
{
	float  sinc = PI * (x * freq - phase) + DELTA;
		   sinc = sin(sinc) / sinc;
	return sinc * sinc * ampli;
}


#define INITIALIZE_ARRAY(Array, Size)\
[unroll] for(int i=0; i<Size; i++) Array[i] = 0.0


float GetTempUIVar(int Index)
{
	float TempArray[10] = { tempF1, tempF2, tempF3.xy };
	return TempArray[Index];
}


//----------------------------------------------------------------------------------------------//
//Functions for angle/vector direction manipulation

//Get 2D direction vector (+overload)
float2 GetDirVec(float Deg)
{ float2 Vec; sincos(radians(Deg), Vec.y, Vec.x); return Vec; }

float4 GetDirVec(float2 Deg) //Deg.x -> xy, Deg.y -> zw
{ float4 Vec; sincos(radians(Deg), Vec.yw, Vec.xz); return Vec; }


//Polar/Cartesian transforms (arctangent intrinsics generate tons of instructions, use carefully!)
float2 CartToPolar(float2 CartCoords)
{
	float2 PolarCoords = { length(CartCoords), atan2(CartCoords.y, CartCoords.x) };
		   PolarCoords.y = (PolarCoords.x == 0.0) ? 0.0 : PolarCoords.y;
	return PolarCoords; //[Radius,Theta(Radians)]
}

float2 PolarToCart(float2 PolarCoords)
{
	float2 CartCoords; sincos(PolarCoords.y, CartCoords.y, CartCoords.x);
	return CartCoords * PolarCoords.x;
}


//Simpler and faster rotation function (CCW -> counter clock wise)
float2 MatrixRotate(float2 Coords, float Deg, bool CCW)
{
	float4 RotDir = CCW ? float4(1.0,  1.0, -1.0, 1.0):
						  float4(1.0, -1.0,  1.0, 1.0);
	return mul(float2x2(RotDir * GetDirVec(Deg).xyyx), Coords);
}


//----------------------------------------------------------------------------------------------//
//Scale fullscreen quad through vertex shader (via multiplier or target resolution)

void ScaleScreenQuad_Mult(inout float2 Pos, float2 Scale)
{
	Pos  = Pos * Scale + float2(-1.0, 1.0);
	Pos += float2(Scale.x, -Scale.y);
}

void ScaleScreenQuad_Res(inout float2 Pos, float2 TargetRes)
{ ScaleScreenQuad_Mult(Pos, TargetRes / ScreenRes); }


//----------------------------------------------------------------------------------------------//
//Quick max & min functions

float max2(float2 a)
{ return max(a.x, a.y); }

float min2(float2 a)
{ return min(a.x, a.y); }


float max3(float3 a)
{ return max(a.x, max(a.y, a.z)); }

float min3(float3 a)
{ return min(a.x, min(a.y, a.z)); }


float max4(float4 a)
{ return max(a.x, max(a.y, max(a.z, a.w))); }

float min4(float4 a)
{ return min(a.x, min(a.y, min(a.z, a.w))); }


//----------------------------------------------------------------------------------------------//
//Extract nth root

float  nRoot(float  x, float  n)
{ return pow(x, rcp(n)); }

float2 nRoot(float2 x, float2 n)
{ return pow(x, rcp(n)); }

float3 nRoot(float3 x, float3 n)
{ return pow(x, rcp(n)); }

float4 nRoot(float4 x, float4 n)
{ return pow(x, rcp(n)); }


//nth Root like curve for n>4 and x[0,1]
// -> Can also be used as a faster but very rough nRoot() approximation
float nRootCurve(float x, float n)
{
	float Power    = rcp(n);
	float Inverter = Power + 1.0;
	
	float2 ZeroCorrection;
	ZeroCorrection    = float2(Power, Inverter);
	ZeroCorrection   *= ZeroCorrection;
	ZeroCorrection.x /= ZeroCorrection.y;
	
	return saturate(Inverter - Power * rsqrt(x + ZeroCorrection.x));
}


//----------------------------------------------------------------------------------------------//
//Zero and delta limit macros

#define zerolim(a)  max(a, 0.0)
#define deltalim(a) max(a, DELTA)


//----------------------------------------------------------------------------------------------//
//Color to Chroma functions

float3 ColorToChroma(float3 Color, float3 LumaWeight)
{ return Color / deltalim(dot(Color, LumaWeight)); }

float3 ColorToChroma(float3 Color)
{ return ColorToChroma(Color, N_LUM); }


//----------------------------------------------------------------------------------------------//
//Depth linearization

float LinearDepth(float Depth, float Near, float Far)
{ return (2.0 * Near)/(Far + Near - Depth * (Far - Near)); }

float  FastLinDepth(float  Depth, float Far)
{ return Depth / mad(-Depth, Far, Far + 1.0); }

float2 FastLinDepth(float2 Depth, float Far)
{ return Depth / mad(-Depth, Far, Far + 1.0); }

float3 FastLinDepth(float3 Depth, float Far)
{ return Depth / mad(-Depth, Far, Far + 1.0); }

float4 FastLinDepth(float4 Depth, float Far)
{ return Depth / mad(-Depth, Far, Far + 1.0); }


//----------------------------------------------------------------------------------------------//
//Noise/random number algorithms

//Pseudo Random number generator
float Random(float2 coord)
{ return abs(frac(sin(dot(coord, float2(25.9796, 156.466))) * 43758.5453)); }


//Modified Pseudo-RNG
float4 RandomF4(float4 seed)
{ return abs(frac(sin(seed * float4(25.9796, 156.466, 78.233, 51.9592)) * 43758.5453)); }

float RandomF1(float seed)
{ return abs(frac(sin(seed * 78.233) * 43758.5453)); }


//Pseudo-RNG with gaussian-like distribution
float RandomGauss(float2 Coords)
{
	float4 Noise  = { 0.0, 0.25, 0.5, 0.75 };
		   Noise += dot(Coords, Random(Coords));
	return dot(RandomF4(Noise), 0.25);
}

//ALU noise in Next-gen post processing in COD:AW
float InterleavedGradientNoise(float2 coord)
{ return frac(52.9829189 * frac(dot(coord, float2 (0.06711056, 0.00583715)))); }


//----------------------------------------------------------------------------------------------//
//Additional interpolations and curves

float  LinearStep(float  Low, float  Up, float  x)
{ return saturate((x - Low) / (Up - Low)); }

float2 LinearStep(float2 Low, float2 Up, float2 x)
{ return saturate((x - Low) / (Up - Low)); }

float3 LinearStep(float3 Low, float3 Up, float3 x)
{ return saturate((x - Low) / (Up - Low)); }


//Optimized linearstep for constant input
// -> gets compiled into a single mad_sat instruction
float ConstOptLinStep(uniform float Low, uniform float Up, float x)
{
	const float Denominator = rcp(Up - Low);
	
	float Mul = Denominator;
	float Add = -Low * Denominator;
	
	return saturate(x * Mul + Add);
}


float smootherstep(float Low, float Up, float x)
{
	x = LinearStep(Low, Up, x);
	return x * x * x * (x * (x * 6.0 - 15.0) + 10.0);
}

//Catmull-Rom
float CatmullRom(float x, float CP1, float CP2, float CP3, float CP4)
{
	float x2 = x*x;
	return		0.5 * ((2.0 * CP2) + (-CP1 + CP3) * x +
		   (2.0 * CP1 - 5.0 * CP2 + 4.0 * CP3 - CP4) * x2 +
		   (     -CP1 + 3.0 * CP2 - 3.0 * CP3 + CP4) * x2 * x);
}

float2 CatmullRom(float2 x, float2 CP1, float2 CP2, float2 CP3, float2 CP4)
{
	float2 x2 = x*x;
	return		0.5 * ((2.0 * CP2) + (-CP1 + CP3) * x +
		   (2.0 * CP1 - 5.0 * CP2 + 4.0 * CP3 - CP4) * x2 +
		   (     -CP1 + 3.0 * CP2 - 3.0 * CP3 + CP4) * x2 * x);
}


//----------------------------------------------------------------------------------------------//
//Conversion from linear RGB to sRGB (gamma space) and vice versa

//Accurate conversions
float3 Lin2sRGB(float3 Color)
{ return Color > 0.0031308 ? 1.055 * pow(Color, 1.0/2.4) - 0.055 : 12.92 * Color; }

float3 sRGB2Lin(float3 Color)
{ return Color > 0.04045 ? pow(Color / 1.055 + 0.055 / 1.055, 2.4) : Color / 12.92; }


//Approximation by Ian Taylor
float3 sRGB2Lin_Approx(float3 Color)
{ return Color * (Color * (Color * 0.305306011 + 0.682171111) + 0.012522878); }


//Inaccurate but cheap approximations
float3 Lin2sRGB_Fast(float3 Color)
{ return pow(Color, 1.0/2.2); }

float3 sRGB2Lin_Fast(float3 Color)
{ return pow(Color, 2.2); }


//Fastest but even more inaccurate approximations
//-> Should be avoided for color sensitive work! (e.g. color grading)
float3 Lin2sRGB_Fastest(float3 Color)
{ return sqrt(Color); }

float3 sRGB2Lin_Fastest(float3 Color)
{ return Color * Color; }


//----------------------------------------------------------------------------------------------//
//CIE color space conversions (XYZ, Lab and LCh)


//D65, 2° Observer (normalized to Y = 1.0)
static const float3 TristimulusValues = { 0.95047, 1.0, 1.08883 };

static const float3x3 LinRGB2XYZMat = //D65
{ 0.4124564,  0.3575761,  0.1804375,
  0.2126729,  0.7151522,  0.0721750,
  0.0193339,  0.1191920,  0.9503041 };

static const float3x3 XYZ2LinRGBMat = //D65
{ 3.2404542, -1.5371385, -0.4985314,
 -0.9692660,  1.8760108,  0.0415560,
  0.0556434, -0.2040259,  1.0572252 };


float3 sRGB2XYZ(float3 RGB)
{ return mul(LinRGB2XYZMat, sRGB2Lin(RGB)); }

float3 XYZ2sRGB(float3 XYZ)
{ return Lin2sRGB(mul(XYZ2LinRGBMat, XYZ)); }


float3 XYZ2Lab(float3 XYZ)
{
	XYZ /= TristimulusValues;
	XYZ  = XYZ > 0.008856 ? pow(XYZ, 1.0/3.0) : 7.787037 * XYZ + 16.0/116.0;
	
	float L = 116.0 *  XYZ.y - 16.0; //[0,100]
	float a = 500.0 * (XYZ.x - XYZ.y);
	float b = 200.0 * (XYZ.y - XYZ.z);
	return float3(L, a, b);
}

float3 Lab2XYZ(float3 Lab)
{
	//Lab.yz = clamp(Lab.yz, -128.0, 127.0);
	float3 XYZ;
	XYZ.y = 16.0/116.0 + Lab.x / 116.0;
	XYZ.x = XYZ.y + Lab.y / 500.0;
	XYZ.z = XYZ.y - Lab.z / 200.0;
	
	XYZ  = XYZ > 0.206897 ? pow(XYZ,3) : XYZ / 7.787037 - (16.0/116.0) / 7.787037;
	XYZ *= TristimulusValues;
	return XYZ;
}


float3 Lab2LCh(float3 Lab) //h in radians!
{ return float3(Lab.x, CartToPolar(Lab.yz)); }

float3 LCh2Lab(float3 LCh)
{ return float3(LCh.x, PolarToCart(LCh.yz)); }


float3 sRGB2LCh(float3 RGB)
{ return Lab2LCh(XYZ2Lab(sRGB2XYZ(RGB))); }

float3 LCh2sRGB(float3 LCh)
{ return XYZ2sRGB(Lab2XYZ(LCh2Lab(LCh))); }


//----------------------------------------------------------------------------------------------//
//RGB - HSL/HCV conversion by Ian Taylor

float3 RGB2HCV(float3 RGB)
{
	//Based on work by Sam Hocevar and Emil Persson
	RGB		 = saturate(RGB);
	float4 P = (RGB.g < RGB.b) ? float4(RGB.bg, -1.0, 2.0/3.0) : float4(RGB.gb, 0.0, -1.0/3.0);
	float4 Q = (RGB.r < P.x) ? float4(P.xyw, RGB.r) : float4(RGB.r, P.yzx);
	float  C = Q.x - min(Q.w, Q.y);
	float  H = abs((Q.w - Q.y) / (6.0 * C + DELTA) + Q.z);
	return float3(H, C, Q.x);
}

float3 RGB2HSL(float3 RGB)
{
	float3 HCV = RGB2HCV(RGB);
	float  L   = HCV.z - HCV.y * 0.5;
	float  S   = HCV.y / ((1.0 + DELTA) - abs(L * 2.0 - 1.0));
	return float3(HCV.x, S, L);
}

float3 HSL2RGB(float3 HSL)
{
		   HSL = saturate(HSL);
	float3 RGB = saturate(float3(abs(HSL.x * 6.0 - 3.0) - 1.0,
						   2.0 - abs(HSL.x * 6.0 - 2.0),
						   2.0 - abs(HSL.x * 6.0 - 4.0)));
	float C = (1.0 - abs(2.0 * HSL.z - 1.0)) * HSL.y;
	return (RGB - 0.5) * C + HSL.z;
}


//----------------------------------------------------------------------------------------------//
//Alternative Texture filtering modes


//----------------------------------------------------------------------------------------------//
//						    More accurate, manual bilinear filtering							//
//																								//
//										  Reference:											//
//		      https://iquilezles.org/www/articles/hwinterpolation/hwinterpolation.htm			//
//----------------------------------------------------------------------------------------------//

/*float4 Acc_BilinearFilter(Texture2D Tex, float2 Coords)
{
	float2 TexRes;
	Tex.GetDimensions(TexRes.x, TexRes.y);
	
	float2 Step       = Coords * TexRes - 0.5;
	float2 IntCoords  = floor(Step);
	float2 FracCoords = frac (Step);
	
	float4 a = Tex.Sample(Point_Sampler, (IntCoords + float2(0.5, 0.5)) / TexRes);
	float4 b = Tex.Sample(Point_Sampler, (IntCoords + float2(1.5, 0.5)) / TexRes);
	float4 c = Tex.Sample(Point_Sampler, (IntCoords + float2(0.5, 1.5)) / TexRes);
	float4 d = Tex.Sample(Point_Sampler, (IntCoords + float2(1.5, 1.5)) / TexRes);
	
	return lerp(lerp(a, b, FracCoords.x), lerp(c, d, FracCoords.x), FracCoords.y);
}

float4 Acc_BilinearFilter(Texture2D Tex, float2 Coords, uint Level)
{
	float2 TexRes;
	Tex.GetDimensions(TexRes.x, TexRes.y);
	
	float2 Step       = Coords * TexRes - 0.5;
	float2 IntCoords  = floor(Step);
	float2 FracCoords = frac (Step);
	
	float4 a = Tex.SampleLevel(Point_Sampler, (IntCoords + float2(0.5, 0.5)) / TexRes, Level);
	float4 b = Tex.SampleLevel(Point_Sampler, (IntCoords + float2(1.5, 0.5)) / TexRes, Level);
	float4 c = Tex.SampleLevel(Point_Sampler, (IntCoords + float2(0.5, 1.5)) / TexRes, Level);
	float4 d = Tex.SampleLevel(Point_Sampler, (IntCoords + float2(1.5, 1.5)) / TexRes, Level);
	
	return lerp(lerp(a, b, FracCoords.x), lerp(c, d, FracCoords.x), FracCoords.y);
}*/


//----------------------------------------------------------------------------------------------//
//				 B-Spline bicubic filtering function for ENB by kingeric1992					//
//				  http://enbseries.enbdev.com/forum/viewtopic.php?f=7&t=4714					//
//																								//
//										  Reference:											//
//		      https://developer.nvidia.com/gpugems/GPUGems2/gpugems2_chapter20.html				//
//						http://vec3.ca/bicubic-filtering-in-fewer-taps/							//
//----------------------------------------------------------------------------------------------//

float4 BicubicFilter(Texture2D InputTex, float2 texcoord, float2 texsize)
{
	float4 uv;
	uv.xy = texcoord * texsize;
	
	//distant to nearest center    
	float2 center  = floor(uv - 0.5) + 0.5;
	float2 dist1st = uv - center;
	float2 dist2nd = dist1st * dist1st;
	float2 dist3rd = dist2nd * dist1st;
	
	//B-Spline weights
	float2 weight0 =     -dist3rd + 3 * dist2nd - 3 * dist1st + 1;
	float2 weight1 =  3 * dist3rd - 6 * dist2nd               + 4;
	float2 weight2 = -3 * dist3rd + 3 * dist2nd + 3 * dist1st + 1;  
	float2 weight3 =      dist3rd;    
	
	weight0 += weight1;
	weight2 += weight3;
	
	//sample point to utilize bilinear filtering interpolation
	uv.xy  = center - 1 + weight1 / weight0;
	uv.zw  = center + 1 + weight3 / weight2;
	uv    /= texsize.xyxy;
	
	//Sample and blend
	return (weight0.y * (InputTex.Sample(Linear_Sampler, uv.xy) * weight0.x  +
						 InputTex.Sample(Linear_Sampler, uv.zy) * weight2.x) +
			weight2.y * (InputTex.Sample(Linear_Sampler, uv.xw) * weight0.x  +
						 InputTex.Sample(Linear_Sampler, uv.zw) * weight2.x)) / 36;
}

//Use screen resolution as default if texture size isn't provided
float4 BicubicFilter(Texture2D InputTex, float2 texcoord)
{ return BicubicFilter(InputTex, texcoord, ScreenRes); }


//----------------------------------------------------------------------------------------------//
//						     Alternative bicubic filtering function								//
//																								//
//										  Reference:											//
//						     https://www.shadertoy.com/view/lstSRS								//
//----------------------------------------------------------------------------------------------//

/*float4 cubic(float x)
{
	float x2 = x * x;
	float x3 = x2 * x;
	float4 w;
	
	w.x =     -x3 + 3.0*x2 - 3.0*x + 1.0;
	w.y =  3.0*x3 - 6.0*x2         + 4.0;
	w.z = -3.0*x3 + 3.0*x2 + 3.0*x + 1.0;
	w.w =      x3;
	return w / 6.0;
}

float4 BicubicFilter(Texture2D InputTex, float2 texcoord, float2 texsize)
{
	texcoord *= texsize;
	
	float fx = frac(texcoord.x);
	float fy = frac(texcoord.y);
	texcoord.x -= fx;
	texcoord.y -= fy;
	
	float4 xcubic = cubic(fx - 0.5);
	float4 ycubic = cubic(fy - 0.5);
	
	float4 fcubic  = float4(xcubic.xz + xcubic.yw, ycubic.xz + ycubic.yw);
	float4 offset  = texcoord.xxyy + float4(-0.5, 1.5, -0.5, 1.5);
		   offset += xcubic.ywyw / fcubic;
		   offset /= texsize;
	
	float4 sample0 = InputTex.Sample(Linear_Sampler, offset.xz);
	float4 sample1 = InputTex.Sample(Linear_Sampler, offset.yz);
	float4 sample2 = InputTex.Sample(Linear_Sampler, offset.xw);
	float4 sample3 = InputTex.Sample(Linear_Sampler, offset.yw);
	
	float2 interp = fcubic.xz / (fcubic.xz + fcubic.yw);
	
	return lerp(lerp(sample3, sample2, interp.x),
				lerp(sample1, sample0, interp.x), interp.y);
}*/


/*BlendState BlendTest
{ //non-zero backbuffer blending ops
  //behave weird in some DX11 ENB fx files
BlendEnable[0]  =TRUE;
SrcBlend        =SRC_ALPHA; //Current Pixel * pre blend op
DestBlend       =ZERO; //Backbuffer/RT Pixel * pre blend op
BlendOp         =ADD;
};*/

//----------------------------------------------------------------------------------------------//
//										  FIELD STYLE 1											//
//----------------------------------------------------------------------------------------------//

/*‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\
|										  FIELD STYLE 2											|
\______________________________________________________________________________________________*/
//<<< end "Helper/enbHelper_Common.fxh"


//----------------------------------------------------------------------------------------------//

#if ENABLE_STYLIZED_BOKEHSHAPES
//Mask atlas texture for stylized bokeh shapes (greyscale image)
Texture2D BokehMaskAtlas <string ResourceName="Textures/BokehMaskAtlas.png";>;

//Atlas grid size and maximum mipmap level (higher max LOD = lower possible res)
#define BOKEHMASK_GRID_SIZE 3
#define BOKEHMASK_MAX_LOD   4
#endif

static const float BlurQuality[3]      = { 1.9, 1.5, 1.2 };
static const float SqrtTwoPI           = sqrt(2.0 * PI);
static const float GaussBleedReduction = 0.5;


//----------------------------------------------------------------------------------------------//

#define DISCRADIUS_RESOLUTION_BOUNDARY_LOWER_FAR 0.25   // Used for blending blurred scene
#define DISCRADIUS_RESOLUTION_BOUNDARY_UPPER_FAR 1.0    // Used for blending blurred scene
#define DISCRADIUS_RESOLUTION_BOUNDARY_CURVE_FAR 0.5    // Used for blending blurred scene

#define BOKEH_CURVE_DISCARD_BOUNDARY_FAR		 3.6    // Skip far  bokeh computation if far  blur curve parameter >= x
#define BOKEH_CURVE_DISCARD_BOUNDARY_NEAR 		 2.4    // Skip near bokeh computation if near blur curve parameter >= x

#define ENABLE_AGRESSIVE_FPS_WEAPON_FIX			 1		// [0-1] Ignore autofocus samples even if they are only partially occluded by fps hands or weapons
#define FPS_HAND_BLUR_CUTOFF_DIST				 0.3468 // FPS hand depth (x10.000), change if you perceive blurred fps weapons
#define FPS_HAND_BLUR_CUTOFF_CHECK				 0      // [0-1] blur = max if depth > hand depth, else 0, useful for tweaking above param

#define GAUSSIAN_BUILDUP_MULT					 4.0    // Value of x -> gaussian blur        reaches max radius   at |CoC| == 1/x
#define CHROMA_BUILUP_MULT						 2.0    // Value of x -> chromatic aberration reaches max strength at |CoC| == 1/x


//----------------------------------------------------------------------------------------------//

//Alpha passthrough for prepass skin mask
#if ENABLE_SKIN_ATTENUATION
		#define ALPHAOUT TextureOriginal.Sample(Point_Sampler, IN.texcoord).a
#else
		#define ALPHAOUT 1.0
#endif


//----------------------------------------------------------------------------------------------//
//										      Structs											//
//																								//
//----------------------------------------------------------------------------------------------//

struct VertexShaderInput
{
   float3 pos     : POSITION;
   float2 txcoord : TEXCOORD0;
};

struct VertexShaderOutput
{
   float4 pos      : SV_POSITION;
   float2 texcoord : TEXCOORD0;
};

struct VertexShaderOutputDrawCoC
{
   float4 pos      : SV_POSITION;
   float2 texcoord : TEXCOORD0;
NI float  Focus    : TEXCOORD1;
};

struct VertexShaderOutputNearCoC
{
   float4 pos          : SV_POSITION;
   float2 texcoord     : TEXCOORD0;
NI float  BlurSteps    : TEXCOORD1;
NI float  Sigma        : TEXCOORD2;
NI float  WeightFactor : PSINFO0;
NI float4 StepSize     : PSINFO1;
};

struct VertexShaderOutputCombineCoC
{
   float4 pos          : SV_POSITION;
   float4 texcoord     : TEXCOORD0;
NI float  BlurSteps    : PSINFO0;
NI float  Sigma        : PSINFO1;
NI float  WeightFactor : PSINFO2;
NI float4 StepSize     : PSINFO3;
};

struct VertexShaderOutputDOF
{
   float4 pos          : SV_POSITION;
   float2 texcoord     : TEXCOORD0;
#if ENABLE_STYLIZED_BOKEHSHAPES
NI float2 AtlasSelect  : TEXCOORD1;
NI float2x2 RotMat     : TEXCOORD2;
NI float2 AtlasTileRes : TEXCOORD4;
#endif
NI float2 vertices[10] : VERTICES0;
};

struct VertexShaderOutputCombine
{
   float4 pos             : SV_POSITION;
   float4 texcoord        : TEXCOORD;
NI float DOFCG_Saturation : DNI0;
NI float DOFCG_Brightness : DNI1;
NI float DOFCG_Contrast   : DNI2;
};

struct BokehUIParams
{
   float ShapeQuality;
   float VertexCount;
   float Curvature;
   float Intensity;
   float SphericalAmount;
   float GrainAmount;
   float DiffractionAmount;
   float ShapeVignetteAmount;
};


//----------------------------------------------------------------------------------------------//
//										    Functions											//
//																								//
//----------------------------------------------------------------------------------------------//

float4 GetCircleOfConfusion(float2 Coords)
{
	float4 CoC   = RenderTargetRGBA32.Sample(Point_Sampler, Coords);
		   CoC.y = CoC.y * 2.0 - 1.0;
	return CoC;
}


float4 DebugCircleOfConfusion(float2 Coords)
{ return RenderTargetRGBA32.Sample(Point_Sampler, Coords); }


//----------------------------------------------------------------------------------------------//

float GetLinearAndMinDepth_Precise(float2 Coords, out float MinDepth)
{
	//Early depth linearization and manual bilinear filtering
	float4 DepthSamples = TextureDepth.Gather(Linear_Sampler, Coords);
		   DepthSamples = FastLinDepth(DepthSamples, 2999.0);
		   MinDepth     = min4(DepthSamples);
	
	float2 FracPos = frac(Coords * ScreenRes - 0.5);
	float2 LinearX = lerp(DepthSamples.wx, DepthSamples.zy, FracPos.x);
	float  LinearY = lerp(LinearX.x, LinearX.y, FracPos.y);
	
	return LinearY;
}


//----------------------------------------------------------------------------------------------//

void ShapeRoundness(inout float2 sampleOffset, in float roundness)
{ sampleOffset *= (1.0 - roundness) + roundness * rsqrt(dot(sampleOffset, sampleOffset)); }

void OpticalVignette(in float2 sampleOffset, in float2 centerVec, inout float sampleWeight)
{
	sampleOffset -= centerVec; //scaled by vignette intensity
	sampleWeight *= saturate(3.33 - dot(sampleOffset, sampleOffset) * 1.666); //notsosmoothstep to avoid aliasing
}


float2 CoC2BlurRadius(float CoC)
{
	float ShapeRadius   = UI_ShapeRadius;
	float AnamorphRatio = UI_ShapeAnamorphRatio;
	
	#if ENABLE_STYLIZED_BOKEHSHAPES
	if(UI_EnableStyle)
	{
		ShapeRadius   = UI_StyleRadius;
		AnamorphRatio = 1.0;
	}
	#endif
	
	return float2(AnamorphRatio, ScreenSize.z) * CoC * ShapeRadius * 6e-4;
}


//----------------------------------------------------------------------------------------------//

void GetGaussianWeight(out float CurrWeight, float BaseWeight, float4 CurrTap, float4 CentTap, float Iterator)
{
	//CurrWeight = BaseWeight * saturate(CurrTap.a - CentTap.a * 0.25);
	CurrWeight = BaseWeight * saturate(1.0 - (CentTap.a - CurrTap.a * GaussBleedReduction) * Iterator);
	
	#if ENABLE_BILATERAL_GAUSSIAN_BLUR
	CurrWeight *= saturate(1.0 - sqrt(distance(CentTap.rgb, CurrTap.rgb) * 1.5));
	#endif
}


void ApplyDoFPostGraining(inout float3 Color, float2 Coords, float GrainInt)
{
	[branch] if(GrainInt > 0.01)
	{
		float3 Grain;
		float3 TimerSeed = Timer.x * UI_GrainMotion + float3(0.01, 0.02, 0.03);
		
		Grain.r = RandomGauss(Coords + float2(0.0, TimerSeed.x));
		Grain.g = RandomGauss(Coords + float2(TimerSeed.y, 0.0));
		Grain.b = RandomGauss(Coords + TimerSeed.z);
		Grain	= lerp(dot(Grain, N_LUM), Grain, UI_GrainSaturation);
		
		Color = zerolim(Color + Grain * GrainInt - GrainInt * 0.5);
	}
}


//----------------------------------------------------------------------------------------------//

#if ENABLE_STYLIZED_BOKEHSHAPES
float2 GetBokehAtlasTileRes()
{
	float2 Res;
	BokehMaskAtlas.GetDimensions(Res.x, Res.y);
	return Res / BOKEHMASK_GRID_SIZE;
}


void MaskBokehShape(float2 MaskCoords, float2 AtlasSelect, float LOD, inout float sampleWeight)
{    
	MaskCoords    = MaskCoords * -0.75 + 0.5;
	sampleWeight *= all(saturate(MaskCoords - MaskCoords * MaskCoords));
	MaskCoords    = (AtlasSelect + MaskCoords) / BOKEHMASK_GRID_SIZE;
	sampleWeight *= BokehMaskAtlas.SampleLevel(Linear_Sampler, MaskCoords, LOD).x;
}


float2 VecMatrixMul2x2(float2 Vec, float2x2 Matrix)
{ return float2(dot(Vec, Matrix._11_12), dot(Vec, Matrix._21_22)); }
#endif


float GetSmootheningAmount(float SampleWeight)
{
	float SmootheningAmount =
	#if ENABLE_STYLIZED_BOKEHSHAPES
		UI_EnableStyle ? UI_StyleSmoothening :
	#endif
	UI_SmootheningAmount;
	
	return SampleWeight * SmootheningAmount + DELTA;
}


BokehUIParams GetUIBokehParams()
{
	BokehUIParams UI;
	#if ENABLE_STYLIZED_BOKEHSHAPES
	if(UI_EnableStyle)
	{
		UI.ShapeQuality = UI_StyleRadius * 0.2 * UI_StyleQualityLevel;
		UI.VertexCount  = 4.0;
		UI.Curvature    = 0.0;
		UI.Intensity    = UI_StyleIntensity;
		
		#if ENABLE_SPHERICAL_ABERRATION
			UI.SphericalAmount     = 0.0;
		#endif
		#if ENABLE_GRAINING == 1
			UI.GrainAmount         = 0.0;
		#endif
		#if ENABLE_DIFFRACTION
			UI.DiffractionAmount   = 0.0;
		#endif
		#if ENABLE_OPTICAL_VIGNETTE
			UI.ShapeVignetteAmount = 0.0;
		#endif
	}
	else
	#endif
	{
		UI.ShapeQuality = UI_ShapeQuality;
		UI.VertexCount  = UI_ShapeVertices;
		UI.VertexCount -= UI_ShapeCut ? ceil(UI.VertexCount * 0.5) : 0.0;
		UI.Curvature    = UI_ShapeCurvatureAmount;
		UI.Intensity    = UI_BokehIntensity;
		
		#if ENABLE_SPHERICAL_ABERRATION
			UI.SphericalAmount     = UI_SphericalAmount;
		#endif
		#if ENABLE_GRAINING == 1
			UI.GrainAmount         = UI_GrainAmount;
		#endif
		#if ENABLE_DIFFRACTION
			UI.DiffractionAmount   = UI_DiffractionAmount;
		#endif
		#if ENABLE_OPTICAL_VIGNETTE
			UI.ShapeVignetteAmount = UI_ShapeVignetteAmount;
		#endif
	}
	return UI;
}


//----------------------------------------------------------------------------------------------//
//										      Shaders											//
//																								//
//----------------------------------------------------------------------------------------------//

//------------------------------------Generic Vertex Shader-------------------------------------//

VertexShaderOutput VS_DoF(VertexShaderInput IN)
{
	VertexShaderOutput OUT;
	OUT.pos			= float4(IN.pos.xyz, 1.0);
	OUT.texcoord.xy	= IN.txcoord.xy;
	return OUT;
}

//----------------------------------------Focusing Pass-----------------------------------------//

//Kitsuune - Optimized focus pass by scaling down screen quad, improved depth
//			 sample accuracy and vastly improved FPS weapon cut out

VertexShaderOutput VS_ReadFocus(VertexShaderInput IN)
{
	VertexShaderOutput OUT;
	OUT.pos			= float4(IN.pos.xy * 0.0625 + float2(-0.9375, 0.9375), IN.pos.z, 1.0);
	OUT.texcoord.xy	= IN.txcoord.xy;
	return OUT;
}


//fullres -> 16x16 R32F (scaled down to 1x1 through VS)
float4 PS_ReadFocus(VertexShaderOutput IN) : SV_Target
{
	float scenefocus = 0.0;
	
	[branch] if(UI_FocusType != 3)
	{
		float weightsum = 1e-6;
		
		for(float xcoord = 0.0; xcoord < 10.0; xcoord++)
		for(float ycoord = 0.0; ycoord < 10.0; ycoord++)
		{
			float2 sampleOffset;
			sampleOffset  = float2(xcoord, ycoord) + 0.5;
			sampleOffset  = sampleOffset * 0.2 - 1.0;
			sampleOffset *=  (UI_FocusType == 1) ? UI_AutofocusRadius : UI_MousefocusRadius;
			sampleOffset += ((UI_FocusType == 1) ? UI_AutofocusCenter : tempInfo2.zw) - 0.5;
			
			float MinDepth, SampleWeight, TempFocus;
			SampleWeight  = saturate(1.2 * exp2(dot(sampleOffset, sampleOffset) * -4.0));
			TempFocus     = GetLinearAndMinDepth_Precise(sampleOffset + 0.5, MinDepth);
			SampleWeight /= TempFocus + DELTA;
			
			//Remove fps hands and weapons from focus calculations
			#if ENABLE_AGRESSIVE_FPS_WEAPON_FIX
				SampleWeight *= MinDepth  > FPS_HAND_BLUR_CUTOFF_DIST * 1e-4;
			#else
				SampleWeight *= TempFocus > FPS_HAND_BLUR_CUTOFF_DIST * 1e-4;
			#endif
			
			scenefocus += TempFocus * SampleWeight;
			weightsum  += SampleWeight;
		}
		
		scenefocus /= weightsum;
		
		#if ENABLE_AGRESSIVE_FPS_WEAPON_FIX
			scenefocus = (weightsum > 1e-6) ? scenefocus : -1.0;
		#endif
	}
	else	scenefocus = UI_ManualfocusDepth;
	return	scenefocus;
}


//---------------------------------------Focus Transition---------------------------------------//

//16x16 (now 1x1 at [0,0]) -> 1x1 R32F
float4 PS_Focus(VertexShaderOutput IN) : SV_Target
{
	//Kitsuune - Optimized focus sampling
	float prevFocus = TexturePrevious.Load(0).x;
	float currFocus = TextureCurrent. Load(0).x;
	
	float Interpolator = DofParameters.w;
	
	#if ENABLE_AGRESSIVE_FPS_WEAPON_FIX
		//Freeze focus transition when sampling area is blocked by FPS weapons or hand
		Interpolator *= currFocus > -DELTA;
	#endif
	
	return (UI_FocusType == 3) ? currFocus :
	lerp(prevFocus, currFocus, Interpolator);
}


//------------------------------------- Circle of Confusion ------------------------------------//

//Kitsuune - Complete CoC rework for better performance and near CoC bleeding
// -> Bleeding is still not nearly as good as I want it to be, but its a start

VertexShaderOutputDrawCoC VS_DrawCoC(VertexShaderInput IN)
{
	VertexShaderOutputDrawCoC OUT;
	OUT.pos			= float4(IN.pos.xyz, 1.0);
	OUT.texcoord.xy	= IN.txcoord.xy;
	OUT.Focus       = TextureFocus.Load(0).x;
	
	return OUT;
}

float4 PS_DrawCoC(VertexShaderOutputDrawCoC IN) : SV_Target
{
	float3 DepthData; //xy - linear scene depth, z - linear scene focus
	float2 SceneCoC;  //Circle of confusion signed by position relative to focus plane
	
	float2 GatheringCoords = IN.texcoord - PixelSize * 0.5;
	float4 DepthGather[2]  = { TextureDepth.Gather(Point_Sampler, GatheringCoords  ),
							   TextureDepth.Gather(Point_Sampler, GatheringCoords,1) };
	
	DepthGather[0] = FastLinDepth(DepthGather[0], 2999.0);
	DepthGather[1] = FastLinDepth(DepthGather[1], 2999.0);
	
	DepthData.x = min(min(min(DepthGather[0].x, DepthGather[0].z), min(DepthGather[1].x, DepthGather[1].z)), DepthGather[0].y);
	
	DepthData.x = lerp(DepthData.x, DepthGather[0].y, 0.001);
	DepthData.y = DepthGather[0].y;
	DepthData.z = IN.Focus;
	
	float2 handdepth  = DepthData.xy;
	float  HyperFocus = saturate(UI_HyperFocus + (UI_FocusType > 1.0));
		   DepthData  = saturate(DepthData / HyperFocus);
	
	SceneCoC = (DepthData.xy < DepthData.z) ?
			   ldexp(DepthData.xy / DepthData.z - 1.0, -0.5 * UI_NearBlurCurve * UI_NearBlurCurve):
			   saturate((DepthData.xy - DepthData.z) / (ldexp(DepthData.z, UI_FarBlurCurve * UI_FarBlurCurve) - DepthData.z));
	
	#if FPS_HAND_BLUR_CUTOFF_CHECK
		SceneCoC = (handdepth < FPS_HAND_BLUR_CUTOFF_DIST * 1e-4 && UI_RemoveFPSObjects) ? 0.0 : 1.0;
	#else
		SceneCoC = (handdepth < FPS_HAND_BLUR_CUTOFF_DIST * 1e-4 && UI_RemoveFPSObjects) ? 0.0 : SceneCoC;
	#endif
	
	float4 SeparatedCoC;
	SeparatedCoC    = saturate(float4(SceneCoC, -SceneCoC));
	SeparatedCoC.zw = SeparatedCoC.zw * SeparatedCoC.zw * (3.0 - 2.0 * SeparatedCoC.zw);
	
	return SeparatedCoC;
}


VertexShaderOutputNearCoC VS_NearCoC(VertexShaderInput IN)
{
	VertexShaderOutputNearCoC OUT;
	OUT.pos			= float4(IN.pos.xyz, 1.0);
	OUT.texcoord.xy	= IN.txcoord.xy;
	
	ScaleScreenQuad_Mult(OUT.pos.xy, 0.5);
	
	OUT.BlurSteps    = UI_ShapeRadius * 0.5 * UI_NearBlurBleed + DELTA;
	OUT.Sigma        = OUT.BlurSteps / 1.5;
	OUT.WeightFactor =  rcp(OUT.Sigma * SqrtTwoPI);
	OUT.Sigma        = -rcp(OUT.Sigma * OUT.Sigma);
	
	OUT.StepSize = PixelSize.xyxy * float4(1.0, 0.0, -1.0, 0.0);
	
	return OUT;
}

float PS_DownsampleNearCoC(VertexShaderOutputNearCoC IN) : SV_Target
{
	//Downsampling + horizontal gaussian blur
	float WeightSum      = IN.WeightFactor;
	float BlurredNearCoC = IN.WeightFactor * TextureColor.Sample(Linear_Sampler, IN.texcoord).w;
	
	[loop] for(float i=1.0; i <= IN.BlurSteps; i++)
	{
		float  GaussWeight = IN.WeightFactor * exp(i*i*IN.Sigma);
		float4 CurrOffset  = IN.texcoord.xyxy + i * IN.StepSize;
		
		BlurredNearCoC += GaussWeight * TextureColor.Sample(Linear_Sampler, CurrOffset.xy).w;
		BlurredNearCoC += GaussWeight * TextureColor.Sample(Linear_Sampler, CurrOffset.zw).w;
		WeightSum      += GaussWeight * 2.0;
	}
	
	return BlurredNearCoC / WeightSum;
}


VertexShaderOutputCombineCoC VS_CombineCoC(VertexShaderInput IN)
{
	VertexShaderOutputCombineCoC OUT;
	OUT.pos			= float4(IN.pos.xyz, 1.0);
	OUT.texcoord.xy	= IN.txcoord.xy;
	OUT.texcoord.zw = IN.txcoord.xy * 0.5;
	
	OUT.BlurSteps    = UI_ShapeRadius * 0.25 * UI_NearBlurBleed + DELTA;
	OUT.Sigma        = OUT.BlurSteps / 1.5;
	OUT.WeightFactor =  rcp(OUT.Sigma * SqrtTwoPI);
	OUT.Sigma        = -rcp(OUT.Sigma * OUT.Sigma);
	
	OUT.StepSize  = PixelSize.xyxy * float4(0.0, 1.0, 0.0, -1.0);
	
	return OUT;
}

float4 PS_CombineCoC(VertexShaderOutputCombineCoC IN) : SV_Target
{
	float4 SceneCoC = TextureColor.Sample(Point_Sampler, IN.texcoord);
	
	//Upsampling + vertical gaussian blur
	float WeightSum      = IN.WeightFactor;
	float BlurredNearCoC = IN.WeightFactor * RenderTargetR16F.Sample(Linear_Sampler, IN.texcoord.zw).x;
	
	[loop] for(float i=1.0; i <= IN.BlurSteps; i++)
	{
		float  GaussWeight = IN.WeightFactor * exp(i*i*IN.Sigma);
		float4 CurrOffset  = min(IN.texcoord.zwzw + i * IN.StepSize, 0.5);
		
		BlurredNearCoC += GaussWeight * RenderTargetR16F.Sample(Linear_Sampler, CurrOffset.xy).x;
		BlurredNearCoC += GaussWeight * RenderTargetR16F.Sample(Linear_Sampler, CurrOffset.zw).x;
		WeightSum      += GaussWeight * 2.0;
	}
	
	BlurredNearCoC /= WeightSum;
	
	
	float  MinCoCSampleRadius = CoC2BlurRadius(max(BlurredNearCoC, SceneCoC.w)).x * 300.0;
	float  MinNearCoC         = SceneCoC.w;
	float2 MinCoCOffsetScale  = saturate(MinCoCSampleRadius * float2(2.0, 1.0));
	
	float2 InnerOffsets[4] = { 0.5,-1.5,  1.5,0.5,  -0.5,1.5,  -1.5,-0.5 };
	float2 OuterOffsets[8] = { 0.5,-3.5,  1.5,2.5,  -0.5,3.5,  -1.5,-2.5,
							   2.5,-1.5,  3.5,0.5,  -2.5,1.5,  -3.5,-0.5 };
	
	[unroll] for(int j=0; j<4; j++)
	{
		InnerOffsets[  j] *= MinCoCOffsetScale.x;
		OuterOffsets[  j] *= MinCoCOffsetScale.y;
		OuterOffsets[7-j] *= MinCoCOffsetScale.y;
	}
	
	float4 InnerSamples[4];
	
	[unroll] for(int k=0; k<4; k++)
		InnerSamples[k] = TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * InnerOffsets[k]);
	
	[branch] if(MinCoCOffsetScale.x < 1.0)
	{
		MinNearCoC = min(MinNearCoC, min3(InnerSamples[0].xyw));
		MinNearCoC = min(MinNearCoC, min3(InnerSamples[1].xzw));
		MinNearCoC = min(MinNearCoC, min3(InnerSamples[2].yzw));
		MinNearCoC = min(MinNearCoC, min3(InnerSamples[3].xyz));
	}
	else
	{
		[unroll] for(int l=0; l<4; l++)
			MinNearCoC = min(MinNearCoC, min4(InnerSamples[l]));
		
		MinNearCoC = min(MinNearCoC, min3(TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * OuterOffsets[0]).xyw));
		MinNearCoC = min(MinNearCoC, min3(TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * OuterOffsets[4]).xyw));
		
		MinNearCoC = min(MinNearCoC, min3(TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * OuterOffsets[1]).xzw));
		MinNearCoC = min(MinNearCoC, min3(TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * OuterOffsets[5]).xzw));
		
		MinNearCoC = min(MinNearCoC, min3(TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * OuterOffsets[2]).yzw));
		MinNearCoC = min(MinNearCoC, min3(TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * OuterOffsets[6]).yzw));
		
		MinNearCoC = min(MinNearCoC, min3(TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * OuterOffsets[3]).xyz));
		MinNearCoC = min(MinNearCoC, min3(TextureColor.GatherBlue(Linear_Sampler, IN.texcoord + PixelSize * OuterOffsets[7]).xyz));
	}
	
	MinNearCoC = lerp(SceneCoC.w, MinNearCoC, saturate(MinCoCSampleRadius * 8.0));
	
	float NearBleed = max(SceneCoC.w, nRootCurve(BlurredNearCoC, 10.0));
	
	float4 CoC;
	CoC.x = SceneCoC.x;				  // Far (aggressive leak reduction)
	CoC.y = MinNearCoC - SceneCoC.y;  // + == Near min, - == Far (without agressive leak reduction)
	CoC.z = NearBleed;				  // Near bleeding
	CoC.w = BlurredNearCoC;			  // Near blurred
	
	CoC.y = CoC.y * 0.5 + 0.5;
	return CoC;
}


//---------------------------------------- DoF Prepass -----------------------------------------//

float4 PS_DoF_PrePass(VertexShaderOutput IN, uniform uint CoCIndex, uniform bool SkipPass) : SV_Target
{
	if(SkipPass) discard;
	
	float3 color = TextureOriginal.Sample(Linear_Sampler, IN.texcoord.xy).rgb;
	
	static const float2 sampleOffsets[4] = { float2( 1.5, 0.5) * PixelSize,
											 float2( 0.5,-1.5) * PixelSize,
											 float2(-1.5,-0.5) * PixelSize,
											 float2(-0.5, 1.5) * PixelSize };
	
	float4 compColor   = 0.0;
	float  centerDepth = TextureDepth.Sample(Linear_Sampler, IN.texcoord.xy).x;
		   centerDepth = rcp(FastLinDepth(centerDepth, 2999.0));
	
	[unroll] for (int i=0; i<4; i++)
	{
		float2 sampleCoord  = IN.texcoord.xy + sampleOffsets[i];
		float3 sampleColor  = TextureOriginal.SampleLevel(Linear_Sampler, sampleCoord,0).rgb;
		float4 sampleDepths = TextureDepth.Gather(Linear_Sampler, sampleCoord);
		
			  sampleColor   /= max3(sampleColor) + 1.0;
		float sampleDepthMin = FastLinDepth(min4(sampleDepths), 2999.0);
		
		float sampleWeight = saturate(sampleDepthMin * centerDepth + 1e-3);
			  compColor   += float4(sampleColor.rgb * sampleWeight, sampleWeight);
	}
	
	compColor.rgb /= compColor.a;
	compColor.rgb /= 1.0 - max3(compColor.rgb);
	color	       = lerp(color, compColor.rgb, saturate(compColor.w * 8.0));
	
	return float4(color, saturate(GetCircleOfConfusion(IN.texcoord)[CoCIndex]));
}


//--------------------------------------- Main DOF Pass ----------------------------------------//

//Kitsuune - Added support for custom texture-based bokeh shapes, spherical aberration,
//           diffraction, graining and half shapes + a few micro-optimizations
VertexShaderOutputDOF VS_DoF_Main(VertexShaderInput IN)
{
	VertexShaderOutputDOF OUT;
	OUT.pos				= float4(IN.pos.xyz, 1.0);
	OUT.texcoord.xy		= IN.txcoord.xy;
	
	ScaleScreenQuad_Mult(OUT.pos.xy, UI_RenderResMult);
	
	float VertexCount = UI_ShapeVertices;
	float Rotation    = UI_ShapeRotation;
	
	#if ENABLE_STYLIZED_BOKEHSHAPES
	if(UI_EnableStyle)
	{
		float UISelection = UI_StyleTex - 1.0;
		float AtlasColumn = floor(UISelection / BOKEHMASK_GRID_SIZE);
		float AtlasRow    = UISelection - AtlasColumn * BOKEHMASK_GRID_SIZE;
		OUT.AtlasSelect   = float2(AtlasRow, AtlasColumn);
		OUT.RotMat        = GetDirVec(UI_StyleRotation).xyyx * float4(1.0, -1.0, 1.0, 1.0);
		OUT.AtlasTileRes  = GetBokehAtlasTileRes();
		VertexCount       = 4.0;
		Rotation          = 45.0;
	}
	#endif
	
	[unroll] for(int i=0; i<10; i++)
		sincos(i * 6.2831853 / VertexCount + radians(Rotation), OUT.vertices[i].y, OUT.vertices[i].x);
	
	return OUT;
}

float4 PS_DoF_Main(VertexShaderOutputDOF IN, uniform uint CoCIndex, uniform bool SkipPass) : SV_Target
{
	if(SkipPass) discard;
	
	float4 CenterBokeh = TextureColor.Sample(Linear_Sampler, IN.texcoord);
	float  CoC         = GetCircleOfConfusion(IN.texcoord)[CoCIndex];
	float  WeightSum   = saturate(1e6 * (CenterBokeh.a - CoC) + 9e5) + DELTA;
	float2 BokehRadius = CoC2BlurRadius(CoC);
	
	if(BokehRadius.x < DISCRADIUS_RESOLUTION_BOUNDARY_LOWER_FAR * ScreenSize.y) return CenterBokeh;
	
	#if ENABLE_STYLIZED_BOKEHSHAPES
		float2 ShapeRes, rMaxRadius; float MaskLOD;
		
		[branch] if(UI_EnableStyle)
		{
			ShapeRes   = (BokehRadius * 2.0) / PixelSize;
			MaskLOD    = max(dot(IN.AtlasTileRes / ShapeRes, 0.5), 1.0);
			MaskLOD    = min(log2(MaskLOD), BOKEHMASK_MAX_LOD);
			rMaxRadius = rcp(BokehRadius);
			
			float2 MaskCenterCoords = (IN.AtlasSelect + 0.5) / BOKEHMASK_GRID_SIZE;
			WeightSum *= BokehMaskAtlas.SampleLevel(Linear_Sampler, MaskCenterCoords, MaskLOD).x;
		}
	#endif
	
	BokehUIParams UI = GetUIBokehParams();
	float nRings  = lerp(1.0, UI.ShapeQuality, saturate(CoC));
		  nRings += fmod(IN.pos.x + IN.pos.y, 2.0) * 0.5;
	
	#if ENABLE_SPHERICAL_ABERRATION
		float SphericalType = UI.SphericalAmount < 0.0;
		UI.SphericalAmount *= saturate(CoC * 0.9 + SphericalType);
		WeightSum          *= saturate(1.0 - UI.SphericalAmount);
		UI.SphericalAmount  = rcp(UI.SphericalAmount * nRings + DELTA);
		
		float SphericalCorrection = UI.SphericalAmount * (nRings + 0.1) * SphericalType;
	#endif
	
	#if ENABLE_DIFFRACTION
		float DiffractionAmount   = (1.0 - UI.DiffractionAmount) * 0.25 + 0.75;
		float CenterDiffracWeight = Diffraction(1.0, UI_DiffractionFreq, 0.0, 1.0);
			  WeightSum          *= saturate(CenterDiffracWeight + DiffractionAmount);
	#endif
	
	#if ENABLE_GRAINING == 1
		float GrainAmount = (1.0 - UI.GrainAmount) * 0.5 + 0.5;
			  WeightSum  *= saturate(Random(UI_GrainSeed) * 0.5 + GrainAmount);
	#endif
	
	#if ENABLE_OPTICAL_VIGNETTE
		float2 centerVec  = IN.texcoord.xy - 0.5;
		float  centerDist = sqrt(dot(centerVec, centerVec));
		float  vignette		  = pow(centerDist, UI_ShapeVignetteCurve) * UI.ShapeVignetteAmount;
			   centerVec  = centerVec / centerDist * vignette;
			   WeightSum *= saturate(3.33 - vignette * 2.0);
	#endif
	
	BokehRadius /= nRings;
	CoC         /= nRings;
	
	//float3 BokehCenterDistance = 0.0;
	float3 BokehSum, BokehMax;
	BokehSum.rgb = BokehMax.rgb = WeightSum * CenterBokeh.rgb;
	
	[loop] for(float iRings = 1; iRings <= nRings; iRings++)
	{
		float2 RingOffsetScale  = BokehRadius * iRings;
		float  RingSampleWeight = 1.0;
		
		#if ENABLE_DIFFRACTION || ENABLE_OPTICAL_VIGNETTE
			float rnRings = rcp(nRings);
		#endif
		
		#if ENABLE_DIFFRACTION
			float DiffractionWeight = Diffraction(1.0 - iRings * rnRings, UI_DiffractionFreq, 0.0, 1.0);
				  RingSampleWeight *= saturate(DiffractionWeight + DiffractionAmount);
		#endif
		
		#if ENABLE_SPHERICAL_ABERRATION
			float SphericalWeight   = SphericalCorrection - iRings * UI.SphericalAmount;
				  RingSampleWeight *= saturate(pow(abs(SphericalWeight), UI_SphericalCurve));
		#endif
		
		[loop] for(float iSamplesPerRing = 0; iSamplesPerRing < iRings; iSamplesPerRing++)
		[loop] for(int   iVertices       = 0; iVertices       < UI.VertexCount; )
		{
			float2 OffsetVec = lerp(IN.vertices[iVertices], IN.vertices[++iVertices], iSamplesPerRing / iRings);
			ShapeRoundness(OffsetVec, UI.Curvature);
			
			float2 SampleOffset = OffsetVec * RingOffsetScale;
			float  SampleWeight = RingSampleWeight;
			
			#if ENABLE_STYLIZED_BOKEHSHAPES
			[branch] if(UI_EnableStyle)
			{
				//Manual matrix multiplication to avoid weird compiler "optimizations"
				float2 MaskSampleOffset = VecMatrixMul2x2(SampleOffset * rMaxRadius, IN.RotMat);
				MaskBokehShape(MaskSampleOffset, IN.AtlasSelect, MaskLOD, SampleWeight);
				if(SampleWeight < 0.01) continue;
			}
			#endif
			
			float4 sampleBokeh;
			sampleBokeh   = TextureColor.SampleLevel(Linear_Sampler, IN.texcoord + SampleOffset,0);
			SampleWeight *= saturate(1e6 * (sampleBokeh.a - CoC * iRings) + 1.0);
			
			#if ENABLE_GRAINING == 1
				SampleWeight *= saturate(Random(OffsetVec + UI_GrainSeed) * 0.5 + GrainAmount);
			#endif
			
			#if ENABLE_OPTICAL_VIGNETTE
				OpticalVignette(OffsetVec * iRings * rnRings, centerVec, SampleWeight);
			#endif
			
			sampleBokeh.rgb *= SampleWeight;
			
			WeightSum += SampleWeight;
			BokehSum  += sampleBokeh.rgb;
			BokehMax   = max(BokehMax, sampleBokeh.rgb);
			//BokehCenterDistance = (BokehMax == sampleBokeh.rgb) ? iRings : BokehCenterDistance;
		}
	}
	
	BokehSum     /= WeightSum;
	UI.Intensity  = saturate(UI.Intensity * pow(dot(BokehMax, N_LUM), UI_BokehCurve));
	UI.Intensity *= saturate(CoC * nRings * 4.0);
	BokehMax      = max(BokehMax, BokehSum);
	
	//float AvgCenterDist = dot(BokehCenterDistance, rcp(nRings * 3.0));
	
	return float4(lerp(BokehSum, BokehMax, UI.Intensity), 1.0);
}


//-------------------------------------DOF Combine/PostPass-------------------------------------//

VertexShaderOutputCombine VS_DoF_Combine(VertexShaderInput IN)
{
	VertexShaderOutputCombine OUT;
	OUT.pos				= float4(IN.pos.xyz, 1.0);
	OUT.texcoord.xy		= IN.txcoord.xy;
	OUT.texcoord.zw = IN.txcoord.xy * UI_RenderResMult;
	
	OUT.DOFCG_Saturation = DNI_SEPARATION(UICG_Saturation);
	OUT.DOFCG_Brightness = DNI_SEPARATION(UICG_Brightness);
	OUT.DOFCG_Contrast   = DNI_SEPARATION(UICG_Contrast);
	
	return OUT;
}

float4 PS_DoF_Combine(VertexShaderOutputCombine IN) : SV_Target
{
	float3 NearBokeh     = TextureColor.       Sample(Linear_Sampler, IN.texcoord.zw).rgb;
	float3 FarBokeh      = RenderTargetRGBA64F.Sample(Linear_Sampler, IN.texcoord.zw).rgb;
	float3 originalColor = TextureOriginal.    Sample(Point_Sampler,  IN.texcoord.xy).rgb;
	float4 CoC           = GetCircleOfConfusion(IN.texcoord);
	float  AbsCoC        = max(CoC.w, saturate(-CoC.y));
	
	float blendWeightFar = LinearStep(DISCRADIUS_RESOLUTION_BOUNDARY_LOWER_FAR,
									  DISCRADIUS_RESOLUTION_BOUNDARY_UPPER_FAR,
									  abs(CoC2BlurRadius(CoC.x).x * ScreenSize.x));
	
		  blendWeightFar  = pow(blendWeightFar, DISCRADIUS_RESOLUTION_BOUNDARY_CURVE_FAR);
	float blendWeightNear = saturate(sqrt(CoC.w) * 1.5);
	
	blendWeightFar  *= UI_FarBlurCurve  < BOKEH_CURVE_DISCARD_BOUNDARY_FAR;
	blendWeightNear *= UI_NearBlurCurve < BOKEH_CURVE_DISCARD_BOUNDARY_NEAR;
	
	float4 BokehSum;
	BokehSum.rgb = lerp(originalColor, FarBokeh, blendWeightFar);
	BokehSum.rgb = lerp(BokehSum.rgb, NearBokeh, blendWeightNear);
	BokehSum.a   = saturate(AbsCoC * GAUSSIAN_BUILDUP_MULT);
	
	[branch] if(UICG_Enable) //Depth of Field Color Grading
	{
		float3 DoFCol;
		DoFCol = log2(mad(BokehSum.rgb, IN.DOFCG_Brightness, DELTA));
		DoFCol = exp2(lerp(UICG_ConGrayLvl, DoFCol, IN.DOFCG_Contrast));
		DoFCol = zerolim(lerp(dot(DoFCol - DELTA, K_LUM), DoFCol, IN.DOFCG_Saturation));
		
		float Mask   = (UICG_Mask == 1) ? AbsCoC : max(blendWeightFar, blendWeightNear);
		BokehSum.rgb = lerp(BokehSum.rgb, DoFCol, saturate(Mask));
	}
	
	return BokehSum;
}


//-----------------------------------Gaussian PostBlur Pass-------------------------------------//

float4 PS_DoF_Gauss(VertexShaderOutput IN, uniform float2 Axis, uniform bool OverrideAlpha) : SV_Target
{
	//Kitsuune - Replaced entire gaussian blur shader and added bilateral mode + grain
	float4 Color     = TextureColor.Sample(Linear_Sampler, IN.texcoord);
	float  OrigSigma = Color.a;
		   Color.a  *= GaussBleedReduction;
	
	float  Sigma       = GetSmootheningAmount(OrigSigma);
	float  OffsetScale = 1.0 - sqrt(saturate(Sigma / 3.0)) * 0.5;
	
	float4 StepSize     = PixelSize.xyxy * float4(Axis, -Axis);
	float4 HalfStepSize = StepSize * OffsetScale;
		   StepSize    *= 2.0;
	
	float WeightFactor =  rcp(Sigma * SqrtTwoPI);
	float LoopCount    = ceil(Sigma * BlurQuality[UI_GaussQuality] - 0.01);
		  Sigma        =  rcp(Sigma * Sigma);
	
	float  WeightSum  = WeightFactor * OffsetScale;
	float3 BlurredCol = WeightSum * Color.rgb;
	
	
	[loop] for(float i=1.0; i <= LoopCount; i++)
	{
		float  GaussWeight = WeightFactor * exp(i*i*-Sigma);
		float4 CurrOffset  = IN.texcoord.xyxy + i * StepSize - HalfStepSize;
		
		float4 CurrSample; float CurrWeight;
		CurrSample = TextureColor.SampleLevel(Linear_Sampler, CurrOffset.xy, 0);
		GetGaussianWeight(CurrWeight, GaussWeight, CurrSample, Color, i);
		
		BlurredCol += CurrWeight * CurrSample.rgb;
		WeightSum  += CurrWeight;
		
		CurrSample = TextureColor.SampleLevel(Linear_Sampler, CurrOffset.zw, 0);
		GetGaussianWeight(CurrWeight, GaussWeight, CurrSample, Color, i);
		
		BlurredCol += CurrWeight * CurrSample.rgb;
		WeightSum  += CurrWeight;
	}
	
	Color.a   = OrigSigma;
	Color.rgb = BlurredCol / WeightSum;
	
	#if ENABLE_CHROMATIC_ABERRATION
		if(OverrideAlpha)
		{
			float4 CoC = GetCircleOfConfusion(IN.texcoord);
			Color.a    = max(CoC.x, CoC.w);
		}
	#else
		if(OverrideAlpha)
		{
			#if ENABLE_GRAINING == 2
				ApplyDoFPostGraining(Color.rgb, IN.texcoord, Color.a * UI_GrainInt);
			#endif
			Color.a = ALPHAOUT;
		}
		
		#if ENABLE_COC_DEBUGGING
			if(UI_CoCDebug > 0)
				Color.rgb = DebugCircleOfConfusion(IN.texcoord)[UI_CoCDebug-1];
		#endif
	#endif
	
	return Color;
}


//-------------------------------------Chromatic Aberration-------------------------------------//

#if ENABLE_CHROMATIC_ABERRATION
float4 PS_DoF_CA(VertexShaderOutput IN) : SV_Target
{
	#if ENABLE_COC_DEBUGGING
		if(UI_CoCDebug > 0)
			return float4((DebugCircleOfConfusion(IN.texcoord)[UI_CoCDebug-1]).xxx, ALPHAOUT);
	#endif
	
	
	//Kitsuune - Added lateral chromatic aberration and a more aggressive leak reduction
	// -> mixing both CA types into one pass isn't ideal but saves performance and looks good enough
	
	float  Alpha = ALPHAOUT;
	float4 colorVals[5];
	colorVals[0] = TextureColor.Load(int3(IN.pos.x,   IN.pos.y,   0)); //C
	
	if(colorVals[0].w < DELTA) return float4(colorVals[0].rgb, Alpha);
	
	colorVals[1] = TextureColor.Load(int3(IN.pos.x-1, IN.pos.y,   0)); //L
	colorVals[2] = TextureColor.Load(int3(IN.pos.x,   IN.pos.y-1, 0)); //T
	colorVals[3] = TextureColor.Load(int3(IN.pos.x+1, IN.pos.y,   0)); //R
	colorVals[4] = TextureColor.Load(int3(IN.pos.x,   IN.pos.y+1, 0)); //B
	
	float2 bokehRadiusScaled = CoC2BlurRadius(colorVals[0].a);
	
	float4 vGradTwosided = float4(dot(colorVals[0].rgb - colorVals[1].rgb, 1),  //C - L
								  dot(colorVals[0].rgb - colorVals[2].rgb, 1),  //C - T
								  dot(colorVals[3].rgb - colorVals[0].rgb, 1),  //R - C
								  dot(colorVals[4].rgb - colorVals[0].rgb, 1)); //B - C
	
	float2 vGrad = min(vGradTwosided.xy, vGradTwosided.zw);
	
	float vGradLen = sqrt(dot(vGrad, vGrad)) + 1e-6;
	vGrad = vGrad / vGradLen * saturate(vGradLen * 32.0) * bokehRadiusScaled * 0.125 * UI_LongitudChromaAmount;
	
	
	float2 LateralVector   = IN.texcoord * 2.0 - 1.0;
	float  LateralGradient = length(LateralVector);
		   LateralVector  *= float2(ScreenSize.z, 1.0);
	
	float LateralShift  = LateralGradient / 1.15 + DELTA;
		  LateralShift  = pow(LateralShift, UI_LateralChromaCurve);
		  LateralShift *= UI_LateralChromaAmount * 5.0;
		  LateralShift *= saturate(CHROMA_BUILUP_MULT * colorVals[0].a);
	
	vGrad *= saturate(1.0 - LateralShift * 0.2);
	vGrad += LateralVector * PixelSize * (LateralShift / LateralGradient);
	
	
	float4 chromaVals[3];
	
	chromaVals[0] = colorVals[0];
	chromaVals[1] = TextureColor.Sample(Linear_Sampler, IN.texcoord + vGrad);
	chromaVals[2] = TextureColor.Sample(Linear_Sampler, IN.texcoord - vGrad);
	
	//Agressive leak reduction for CA
	float2 LeakScanScale = saturate(1.0 - bokehRadiusScaled) * 1.15;
	chromaVals[1].w = min(min4(TextureColor.GatherAlpha(Linear_Sampler, IN.texcoord + vGrad * LeakScanScale)), colorVals[0].w);
	chromaVals[2].w = min(min4(TextureColor.GatherAlpha(Linear_Sampler, IN.texcoord - vGrad * LeakScanScale)), colorVals[0].w);
	
	chromaVals[1].rgb = lerp(chromaVals[0].rgb, chromaVals[1].rgb, saturate(CHROMA_BUILUP_MULT * chromaVals[1].w));
	chromaVals[2].rgb = lerp(chromaVals[0].rgb, chromaVals[2].rgb, saturate(CHROMA_BUILUP_MULT * chromaVals[2].w));
	
	int3 ChromaMode = (int3(0,1,2) + UI_ChromaMode) % 3;
	
	float4 BokehSum;
	BokehSum = float4(chromaVals[ChromaMode.x].r,
					  chromaVals[ChromaMode.y].g,
					  chromaVals[ChromaMode.z].b, Alpha);
	
	
	#if ENABLE_GRAINING == 2
		ApplyDoFPostGraining(BokehSum.rgb, IN.texcoord, UI_GrainInt * chromaVals[0].w);
	#endif
	
	return BokehSum;
}
#endif


//--------------------------------------Focusing Visualizer-------------------------------------//

#if ENABLE_FOCUSING_TOOL

//Visualizer parameters
static const float  FocusingTool_LineSize    = 1.5;
static const float3 FocusingTool_LineColor   = { 1.0, 1.0, 1.0 };
static const float3 FocusingTool_CenterColor = { 1.0, 0.0, 0.0 };


//Clip functions
bool ANDTexcoordClip(float2 Coords, float4 Bound)
{ return all(Coords > Bound.xy && Coords < Bound.zw); }

bool ORTexcoordClip(float2 Coords, float4 Bound)
{ return any(Coords > Bound.xy && Coords < Bound.zw); }


float4 PS_DoF_Overlay(VertexShaderOutput IN) : SV_Target
{
	//Kitsuune - Added optional focusing visualizer to better see the actually sampled area and
	//focusing center (useful when adjusting autofocus offsets for third person gameplay)
	// -> Not the most efficient way of doing it but this will do for now
	//    And its turned off most of the time anyway, so it shouldn't really matter
	
	if(UI_FocusType == 3 || !UI_VisualizeFocus) discard;
	
	float4 PixelScale, FocusCoords; float FocusRadius;
	PixelScale  = float4(-PixelSize, PixelSize);
	PixelScale *= FocusingTool_LineSize;
	
	
	[flatten] if(UI_FocusType == 2)
	{ FocusCoords = tempInfo2.zwzw;
	  FocusRadius = UI_MousefocusRadius; }
	else
	{ FocusCoords = UI_AutofocusCenter.xyxy;
	  FocusRadius = UI_AutofocusRadius;  }
	
	float4 CrosshairCoords		= PixelScale + FocusCoords;
	float4 SampleAreaCoords = FocusCoords + float4(-FocusRadius.xx, FocusRadius.xx);
	
	bool DrawCrosshair  = ORTexcoordClip(IN.texcoord, CrosshairCoords);
	bool DrawSampleArea = ANDTexcoordClip(IN.texcoord, SampleAreaCoords);
		 DrawCrosshair  = DrawCrosshair && !DrawSampleArea;
	
	SampleAreaCoords = PixelScale * -2.0 + SampleAreaCoords;
	DrawSampleArea   = DrawSampleArea && !ANDTexcoordClip(IN.texcoord, SampleAreaCoords);
	
	bool DrawFocusCenter = ANDTexcoordClip(IN.texcoord, FocusCoords + PixelScale * 2.0);
	if(!(DrawSampleArea || DrawCrosshair || DrawFocusCenter)) discard;
	
	return float4(DrawFocusCenter ? FocusingTool_CenterColor : FocusingTool_LineColor, 0.0);
}

//Old visualization shader that shows each sample position separately
/*float4 PS_DoF_Debug_Overlay(VertexShaderOutput IN) : SV_Target
{
	#define PS_DoF_Overlay PS_DoF_Debug_Overlay
	float4 FocusCoords		   = 0.0;
	float  FocusRadius		   = 0.0;
	bool   ShowSamplePositions = true;
	
	if (UI_FocusType == 2)
	{ FocusCoords = tempInfo2.zwzw;
	  FocusRadius = UI_MousefocusRadius; }
	else
	{ FocusCoords = UI_AutofocusCenter.xyxy;
	  FocusRadius = UI_AutofocusRadius;  }
	
	float4 ClippingArea = FocusCoords.xyxy + float4(-FocusRadius.xx, FocusRadius.xx);
	clip(ANDTexcoordClip(IN.texcoord, ClippingArea) && UI_FocusType != 3 && UI_VisualizeFocus ? 1:-1);
	
	float4 OverlayPxlSize = float4(-PixelSize, PixelSize) * 2.0;
	float3 Color		      = TextureColor.Sample(Point_Sampler, IN.texcoord).rgb;
	
	[branch] if (ShowSamplePositions)
	[unroll] for(float xcoord = 0.0; xcoord < 5.0; xcoord++)
	[unroll] for(float ycoord = 0.0; ycoord < 5.0; ycoord++)
	{
		float4 SampleOffset; float SampleWeight;
		SampleOffset.xy = (float2(xcoord,ycoord) + 0.5) * 0.2;
		SampleOffset.xy = mad(SampleOffset.xy, 2.0, -1.0);
		SampleWeight    = 1.0; //saturate(1.2 * exp2(dot(sampleOffset, sampleOffset) * -4.0));
		
		SampleOffset.xy = mad(SampleOffset.xy, FocusRadius, FocusCoords.xy);
		SampleOffset    = SampleOffset.xyxy + OverlayPxlSize;
		
		Color = ANDTexcoordClip(IN.texcoord, SampleOffset) ? SampleWeight : Color;
	}
	else Color = ANDTexcoordClip(IN.texcoord, mad(OverlayPxlSize,-2.0, ClippingArea)) ? Color : 1.0;
		 Color = ANDTexcoordClip(IN.texcoord, mad(OverlayPxlSize, 2.0, FocusCoords)) ? float3(1.0, 0.0, 0.0) : Color;
	
	return float4(Color, 1.0);
}*/
#endif


//----------------------------------------------------------------------------------------------//
//										   Techniques												//
//																								//
//----------------------------------------------------------------------------------------------//

//--------------------------------------------Focus---------------------------------------------//

TECH11(ReadFocus, VS_ReadFocus(), PS_ReadFocus())
TECH11(Focus,     VS_DoF(),       PS_Focus())


//---------------------------------------------DOF----------------------------------------------//

#if ENABLE_FAR_BOKEH_FREEZING
	static bool SkipFarBokehPass  = UI_FarBlurCurve  >= BOKEH_CURVE_DISCARD_BOUNDARY_FAR || UI_FreezeFarBokeh;
#else
	static bool SkipFarBokehPass  = UI_FarBlurCurve  >= BOKEH_CURVE_DISCARD_BOUNDARY_FAR;
#endif
	static bool SkipNearBokehPass = UI_NearBlurCurve >= BOKEH_CURVE_DISCARD_BOUNDARY_NEAR;


TECH11       (DOF  <string UIName="ADoF - Kitsuune - McFly";>,   VS_DrawCoC(),     PS_DrawCoC())
TWOPASSTECH11(DOF1 <string RenderTarget="RenderTargetR16F";>,    VS_Basic(),       PS_Blank(),
																 VS_NearCoC(),     PS_DownsampleNearCoC())
TECH11       (DOF2 <string RenderTarget="RenderTargetRGBA32";>,  VS_CombineCoC(),  PS_CombineCoC())
TECH11       (DOF3,												 VS_DoF(),         PS_DoF_PrePass(0, SkipFarBokehPass))
TECH11       (DOF4 <string RenderTarget="RenderTargetRGBA64F";>, VS_DoF_Main(),    PS_DoF_Main(0, SkipFarBokehPass))
TECH11       (DOF5,												 VS_DoF(),         PS_DoF_PrePass(1, SkipNearBokehPass))
TWOPASSTECH11(DOF6,												 VS_Basic(),       PS_Blank(),
																 VS_DoF_Main(),    PS_DoF_Main(2, SkipNearBokehPass))
TECH11       (DOF7,												 VS_DoF_Combine(), PS_DoF_Combine())
TECH11       (DOF8,												 VS_DoF(),         PS_DoF_Gauss(float2(0.0,1.0), false))

#if ENABLE_FOCUSING_TOOL
	TWOPASSTECH11(DOF9, VS_DoF(), PS_DoF_Gauss(float2(1.0,0.0), true),
					    VS_DoF(), PS_DoF_Overlay())
#else
	TECH11       (DOF9, VS_DoF(), PS_DoF_Gauss(float2(1.0,0.0), true))
#endif

#if ENABLE_CHROMATIC_ABERRATION
	TECH11       (DOF10, VS_DoF(), PS_DoF_CA())
#endif

