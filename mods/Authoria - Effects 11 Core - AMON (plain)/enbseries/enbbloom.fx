//----------------------------------------------------------------------------------------------//
//								    DYNAMIC GAUSSIAN BLOOM 2.2									//
//----------------------------------------------------------------------------------------------//
//																								//
//						 enbbloom.fx file by LonelyKitsuune aka Skratzer						//
//						      for ENB (DirectX 11 Shader Model 5)								//
//																								//
//				Copyright (c) 2018-2020 LoneKitsuune / T.Thanner - CC BY-NC-ND 4.0				//
//																								//
//-------------------------------------------CREDITS--------------------------------------------//
//																								//
//								  Boris Vorontsov for ENBSeries									//
//																								//
//------------------------------------------THANKS TO-------------------------------------------//
//																								//
//				prod80, Sonic Ether, Sandvich Maker and Marty McFly for inspiration				//
//																								//
//----------------------------------------------------------------------------------------------//
//								==================================								//
//								//     Silent Horizons ENB      //								//
//								//								//								//
//								//		by LonelyKitsuune		//								//
//								==================================								//
//----------------------------------------------------------------------------------------------//


/*¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\
|												Multipass Bloom Flow Chart:														|
|																																|
|																																|
|PREPASS ---> Horizontal Gaussian Blur	|-------> Horizontal Gaussian Blur		|-------> Horizontal Gaussian Blur				|
|				       \ /				|				   \ /					|				   \ /							|
|		      Vertical Gaussian Blur	|		   Vertical Gaussian Blur		|		   Vertical Gaussian Blur				|
|				       \ /				|				   \ /					|				   \ /							|
|				RenderTarget1024 -------|		     RenderTarget512 -----------|		      RenderTarget256 ------- ...		|
|						|								    |						    		    |							|
|						|								    |						    		    |							|
|						|								    |						    		    |							|
|						¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯Load in all RenderTargets¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯ ...		|
|														   | |																	|
|														   | |																	|
|														   \ /																	|
|														   MIX																	|
|														   \ /																	|
|												       BLOOM OUTPUT																|
\______________________________________________________________________________________________________________________________*/

//Boris' comment on ENB bloom files:
//Works with hdr input and output
//Bloom texture is always forced to 1024*1024 resolution


//This file needs my helper and UI files to work!
//Some options could be made UI tweakable instead


//--------------------------------------------------------------------------------
//Enables full local control over this shader file
#define LOCAL_OVERRIDE							0	//[0-1]


//--------------------------------------------------------------------------------
//GENERAL OPTIONS
//--------------------------------------------------------------------------------
//Enable additional debugging tools
#define ENABLE_TOOLS							0	//[0-1]


//--------------------------------------------------------------------------------
//PREPASS OPTIONS
//--------------------------------------------------------------------------------
//Switch the prepass variant
#define BLOOM_PREPASS_STYLE						2	//[1-2]
// 1 = Levels
// 2 = Thresholds


//UI seperation mode for the prepass
#define UI_SEP_MODE_PRE							1	//[1-2]
// 1 = TODIE seperated UI
// 2 = DNI seperated UI


//--------------------------------------------------------------------------------
//MAIN BLOOM OPTIONS
//--------------------------------------------------------------------------------
//UI seperation mode for the main pass
#define UI_SEP_MODE_MAIN						1	//[1-2]
// 1 = TODIE seperated UI
// 2 = DNI seperated UI


//Enables a more agressive correction method that gets rid of
//bright bloom flares at screen borders.
// -> Can produces small visual artifacts!
#define ENABLE_AGRESSIVE_BORDER_CORRECTION		0	//[0-1]


//Enables depth based bloom width/intensity manipulation
#define ENABLE_DEPTH_TESTING					0	//[0-1]-G


//--------------------------------------------------------------------------------
//BLOOM MIX OPTIONS
//--------------------------------------------------------------------------------
//Use automatic pass weighting
#define ENABLE_AUTOMATIC_WEIGHTING				0	//[0-1]


//Use bicubic filtering to upsample bloom pass textures
#define USE_BICUBIC_FILTERING					0	//[0-1]


//Activate per pass Bloom tinting
#define ENBALE_BLOOM_TINTING					0	//[0-1]


//Enables a additional small scale bloom for very bright objects
#define ENABLE_TINYBLOOM						0	//[0-1]


//Enables the option to mask out the bloom source
#define ENABLE_SOURCE_MASKING					0	//[0-1]-G


//Enable lens-dirt bloom reflections
#define ENABLE_DIRT_REFLECTION					0	//[0-1]-G


//Enable graining of the bloom output to reduce possible banding visiblity
// -> If you dither after mixing in the bloom texture you probably don't need it
#define ENABLE_BLOOM_GRAIN						0	//[0-1]


//UI seperation mode for the mix pass
#define UI_SEP_MODE_MIX							1	//[1-2]
// 1 = TODIE seperated UI
// 2 = DNI seperated UI


//----------------------------------------------------------------------------------------------//
//										 Global Parameters										//
//----------------------------------------------------------------------------------------------//

#if !LOCAL_OVERRIDE
#undef ENABLE_DEPTH_TESTING
#undef ENABLE_SOURCE_MASKING
#undef ENABLE_DIRT_REFLECTION
// ---- begin include enbglobals.fxh ----
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


// ---- end include enbglobals.fxh ----

#endif //LOCAL_OVERRIDE


//----------------------------------------------------------------------------------------------//
//										Internal Parameters										//
//----------------------------------------------------------------------------------------------//

// ---- begin include UI/enbUI_Primer.fxh ----
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

// ---- end include UI/enbUI_Primer.fxh ----


//Tools
#define SHADERGROUP 0
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

#undef SHADERGROUP
UI_WHITESPACE(7)

//--------------------------------------------Prepass-------------------------------------------//

#if BLOOM_PREPASS_STYLE != 0
#if UI_SEP_MODE_PRE == 1 //Prepass (TODIE)
#define SHADERGROUP 1
#define TODIE Dawn
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(7)

#define TODIE Sunrise
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(8)

#define TODIE Day
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(9)

#define TODIE Sunset
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(10)

#define TODIE Dusk
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(11)

#define TODIE Night
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(12)

#define TODIE Interior
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


UI_WHITESPACE(8)
UI_WHITESPACE(9)

#undef SHADERGROUP
#undef NOTFIRSTTIME


#elif UI_SEP_MODE_PRE == 2 //Prepass (DNI)
#define SHADERGROUP 1

#define TODIE Day
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(7)

#define TODIE Night
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(8)

#define TODIE Interior
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


UI_WHITESPACE(8)
UI_WHITESPACE(9)

#undef SHADERGROUP
#undef NOTFIRSTTIME

#endif //UI_SEP_MODE_PRE
#endif //BLOOM_PREPASS_STYLE

//---------------------------------------------Main---------------------------------------------//

#if UI_SEP_MODE_MAIN == 1 //Main Bloom (TODIE)
#define SHADERGROUP 2
#define TODIE Dawn
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(13)

#define TODIE Sunrise
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(14)

#define TODIE Day
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(15)

#define TODIE Sunset
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(16)

#define TODIE Dusk
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(17)

#define TODIE Night
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(18)

#define LASTTIME
#define TODIE Interior
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


UI_WHITESPACE(10)
UI_WHITESPACE(11)

#undef SHADERGROUP
#undef NOTFIRSTTIME


#elif UI_SEP_MODE_MAIN == 2 //Main Bloom (DNI)
#define SHADERGROUP 2
#define TODIE Day
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(13)

#define TODIE Night
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(14)

#define LASTTIME
#define TODIE Interior
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


UI_WHITESPACE(10)
UI_WHITESPACE(11)

#undef SHADERGROUP
#undef NOTFIRSTTIME

#endif //UI_SEP_MODE_MAIN

//----------------------------------------------Mix---------------------------------------------//

#if !ENABLE_AUTOMATIC_WEIGHTING
#if UI_SEP_MODE_MIX == 1 //Bloom Mix (TODIE)
#define SHADERGROUP 3
#define TODIE Dawn
#define SWSN 19
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(28)

#define TODIE Sunrise
#define SWSN 20
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(29)

#define TODIE Day
#define SWSN 21
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(30)

#define TODIE Sunset
#define SWSN 24
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(31)

#define TODIE Dusk
#define SWSN 25
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(32)

#define TODIE Night
#define SWSN 26
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(33)

#define TODIE Interior
#define SWSN 27
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


//UI_WHITESPACE(12)
//UI_WHITESPACE(13)

#undef SHADERGROUP
#undef NOTFIRSTTIME


#elif UI_SEP_MODE_MIX == 2 //Bloom Mix (DNI)
#define SHADERGROUP 3
#define TODIE Day
#define SWSN 19
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(28)

#define TODIE Night
#define SWSN 20
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----

UI_SPECIAL_WHITESPACE(29)

#define TODIE Interior
#define SWSN 21
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


//UI_WHITESPACE(12)
//UI_WHITESPACE(13)

#undef SHADERGROUP
#undef NOTFIRSTTIME

#endif //UI_SEP_MODE_MIX

#else

#if UI_SEP_MODE_MIX == 1 //Bloom Mix (TODIE)
#define SHADERGROUP 3
#define TODIE Dawn
#define SWSN 19
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#define TODIE Sunrise
#define SWSN 20
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#define TODIE Day
#define SWSN 21
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#define TODIE Sunset
#define SWSN 24
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#define TODIE Dusk
#define SWSN 25
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#define TODIE Night
#define SWSN 26
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#define TODIE Interior
#define SWSN 27
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#undef SHADERGROUP
#undef NOTFIRSTTIME


#elif UI_SEP_MODE_MIX == 2 //Bloom Mix (DNI)
#define SHADERGROUP 3
#define TODIE Day
#define SWSN 19
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#define TODIE Night
#define SWSN 20
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#define TODIE Interior
#define SWSN 21
// ---- begin include UI/enbUI_Bloom.fxh ----
//----------------------------------------------------------------------------------------------//
//																								//
//								  Main ENB Bloom UI file										//
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

UI_FileHeaderLong(">>>      Dynamic Bloom 2.2 for ENB       <<<",
				  ">>>              by LonelyKitsuune              <<<")

#if ENABLE_TOOLS
UI_WHITESPACE(1)
UI_ELEMENT(_Tools_Header,"               >>>>>>TOOLS<<<<<<")
UI_WHITESPACE(2)
int  UI_PASSOUTPUT		<string UIName="Show Pass Output"; int UIMin=0; int UIMax=7;> = {0};
#if ENABLE_DEPTH_TESTING
bool UI_Visualize_Depth <string UIName="Visualize Depth";> = {false};
#endif //ENABLE_DEPTH_TESTING
UI_WHITESPACE(3)
#endif //ENABLE_TOOLS

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 1

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Prepass_Header,"             >>>>>>PREPASS<<<<<<")
UI_WHITESPACE(4)
#if BLOOM_PREPASS_STYLE == 2
bool UI_Smooth_Threshold <string UIName="|---- Use Smooth Threshold"; > = {true};
UI_SPECIAL_WHITESPACE(1)
#endif //BLOOM_PREPASS_STYLE
#endif //NOTFIRSTTIME

#if BLOOM_PREPASS_STYLE == 1
float SEPARATE_VAR(UI_InBlack)			<string UIName=TO_STRING(|- TODIE - In Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_InWhite)			<string UIName=TO_STRING(|- TODIE - In White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_OutBlack)			<string UIName=TO_STRING(|- TODIE - Out Black);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {0.0};
float SEPARATE_VAR(UI_OutWhite)			<string UIName=TO_STRING(|- TODIE - Out White);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#elif BLOOM_PREPASS_STYLE == 2
float SEPARATE_VAR(UI_Brightness)		<string UIName=TO_STRING(|- TODIE - Brightness);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Contrast)			<string UIName=TO_STRING(|- TODIE - Contrast);			float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_Saturation)		<string UIName=TO_STRING(|- TODIE - Saturation);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
float SEPARATE_VAR(UI_ThresholdLower)	<string UIName=TO_STRING(|- TODIE - Lower Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {0.0};
float SEPARATE_VAR(UI_ThresholdUpper)	<string UIName=TO_STRING(|- TODIE - Upper Threshold);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.0001; > = {1.0};
#endif //BLOOM_PREPASS_STYLE

#if ENABLE_SKIN_ATTENUATION
float SEPARATE_VAR(UI_SkinAttenu)		<string UIName=TO_STRING(|- TODIE - Skin Attenuation);	float UIMin=0.0; float UIMax=10.0; float UIStep=0.001;  > = {1.0};
#endif


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 2

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Main_Header,"               >>>>>>BLOOM<<<<<<")
UI_WHITESPACE(5)
int UI_Quality <string UIName="|---- Bloom Quality"; string UIWidget="Quality"; > = {0};
UI_SPECIAL_WHITESPACE(2)
#endif //NOTFIRSTTIME

float  SEPARATE_VAR(UI_Sigma)				  <string UIName=TO_STRING(|- TODIE - Bloom Sigma (Width));				float UIMin=0.5; float UIMax=20.0; float UIStep=0.001; > = {3.0};
float  SEPARATE_VAR(UI_HoriIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Horizontal);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};
float  SEPARATE_VAR(UI_VertIntensity)		  <string UIName=TO_STRING(|- TODIE - Bloom Intensity Vertical);		float UIMin=0.0; float UIMax=10.0; float UIStep=0.001; > = {1.0};


#ifdef LASTTIME
#if ENABLE_DEPTH_TESTING
UI_SPECIAL_WHITESPACE(3)
UI_SPECIAL_WHITESPACE(4)
bool  UI_Depth_Calc		  <string UIName="|---- Exterior - Activate Depth Testing";														  > = {false};
bool  UI_DepthInvert	  <string UIName="|- Exterior - Invert Depth";																	  > = {false};
float UI_FarDepth		  <string UIName="|- Exterior - Depthfade";				float UIMin=0.0; float UIMax=5000.0; float UIStep=1.0;   > = {3500.0};
float UI_DepthWidth		  <string UIName="|- Exterior - Bloom Depth Width";		float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.5};
float UI_DepthInt		  <string UIName="|- Exterior - Bloom Depth Intensity";	float UIMin=0.0; float UIMax=2.0;    float UIStep=0.001; > = {0.2};
#endif //ENABLE_DEPTH_TESTING
#undef LASTTIME
#endif //LASTTIME


//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------//
#elif SHADERGROUP == 3

#ifndef NOTFIRSTTIME
#define NOTFIRSTTIME
UI_ELEMENT(_Mix_Header,"            >>>>>>BLOOM MIX<<<<<<")
UI_WHITESPACE(6)
bool  UI_Normalize_BloomSum		  <string UIName="|---- Normalize Bloom after Mixing";					    > = {true};

#if ENABLE_TINYBLOOM
bool  UI_TinyBloom				  <string UIName="|---- Enable TinyBloom";								    > = {true};
#endif //ENABLE_TINYBLOOM

#if ENABLE_SOURCE_MASKING
UI_SPECIAL_WHITESPACE(34)
bool  UI_Mask_BloomSource		  <string UIName="|---- Mask Bloom Source";								    > = {false};
float UI_Mask_Weight			  <string UIName="|- Masking Strength";   float UIMin=0.0; float UIMax=1.0; > = {1.0};
#endif //ENABLE_SOURCE_MASKING

#if ENABLE_BLOOM_GRAIN
UI_SPECIAL_WHITESPACE(35)
bool  UI_Enable_Grain			  <string UIName="|---- Enable Grain";									    > = {false};
float UI_GrainIntensity			  <string UIName="|- Grain Intensity";	  float UIMin=0.0; float UIMax=1.0; > = {0.2};
float UI_GrainSaturation		  <string UIName="|- Grain Saturation";   float UIMin=0.0; float UIMax=3.0; > = {0.0};
float UI_GrainMotion			  <string UIName="|- Grain Motion";		  float UIMin=0.0; float UIMax=0.5; > = {0.2};
#endif //ENABLE_BLOOM_GRAIN

#if ENABLE_DIRT_REFLECTION
UI_SPECIAL_WHITESPACE(36)
bool  UI_EnableDirtRef			  <string UIName="|---- Enable Dirt Reflection";								    > = {false};
float UI_DirtRef				  <string UIName="|- Dirt Reflection";			 float UIMin=0.0; float UIMax=10.0; > = {0.8};
float UI_DirtRefThresh			  <string UIName="|- Dirt Reflection Threshold"; float UIMin=0.0; float UIMax=10.0; > = {1.5};
float UI_DirtRefCurve			  <string UIName="|- Dirt Reflection Curve";	 float UIMin=0.1; float UIMax=10.0; > = {1.5};
int   UI_DirtSelect				  <string UIName="|- Select Dirt Texture";		 int   UIMin=1;   int   UIMax=4;    > = {1};
#endif //ENABLE_DIRT_REFLECTION

UI_SPECIAL_WHITESPACE(6)
#endif //NOTFIRSTTIME

#if ENABLE_AUTOMATIC_WEIGHTING
float SEPARATE_VAR(UI_AutoWeight_Bias)			<string UIName=TO_STRING(|- AutoWeighting Bias TODIE);   float UIMin=0.1; float UIMax=20.0; float UIStep=0.01; > = {3.0};
#else
float SEPARATE_VAR(UI_RenderTargetStrength1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Strength); float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Strength);  float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
float SEPARATE_VAR(UI_RenderTargetStrength16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Strength);   float UIMin=0.0; float UIMax=10.0; float UIStep=0.01; > = {1.0};
#endif

#if ENBALE_BLOOM_TINTING
UI_SPECIAL_WHITESPACE(SWSN)
float3 SEPARATE_VAR(UI_RenderTargetTint1024) <string UIName=TO_STRING(|- TODIE - 1024 Pass Tint); string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint512)  <string UIName=TO_STRING(|- TODIE - 512 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint256)  <string UIName=TO_STRING(|- TODIE - 256 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint128)  <string UIName=TO_STRING(|- TODIE - 128 Pass Tint);  string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint64)   <string UIName=TO_STRING(|- TODIE - 64 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint32)   <string UIName=TO_STRING(|- TODIE - 32 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
float3 SEPARATE_VAR(UI_RenderTargetTint16)   <string UIName=TO_STRING(|- TODIE - 16 Pass Tint);   string UIWidget="Color"; > = {1.0,1.0,1.0};
#endif //ENBALE_BLOOM_TINTING


#endif //SHADERGROUP

#undef TODIE











// ---- end include UI/enbUI_Bloom.fxh ----


#undef SHADERGROUP
#undef NOTFIRSTTIME

#endif //UI_SEP_MODE_MIX
#endif //ENABLE_AUTOMATIC_WEIGHTING

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
//						     Game and mod parameters, do not modify								//
//																								//
//----------------------------------------------------------------------------------------------//

Texture2D TextureDownsampled;	//color R16B16G16A16 64 bit or R11G11B10 32 bit hdr format. 1024*1024 size
Texture2D TextureColor;			//color which is output of previous technique (except when drawed to temporary render target), R16B16G16A16 64 bit hdr format. 1024*1024 size
Texture2D TextureOriginal;		//color R16B16G16A16 64 bit or R11G11B10 32 bit hdr format, screen size. PLEASE AVOID USING IT BECAUSE OF ALIASING ARTIFACTS, UNLESS YOU FIX THEM
Texture2D TextureDepth;			//scene depth R32F 32 bit hdr format, screen size. PLEASE AVOID USING IT BECAUSE OF ALIASING ARTIFACTS, UNLESS YOU FIX THEM
Texture2D TextureAperture;		//this frame aperture 1*1 R32F hdr red channel only. computed in PS_Aperture of enbdepthoffield.fx

//temporary textures which can be set as render target for techniques via annotations like <string RenderTarget="RenderTargetRGBA32";>
Texture2D RenderTarget1024;		//R16B16G16A16F 64 bit hdr format, 1024*1024 size		-- Used as bloom texture
Texture2D RenderTarget512;		//R16B16G16A16F 64 bit hdr format, 512*512 size				-- Used as bloom texture
Texture2D RenderTarget256;		//R16B16G16A16F 64 bit hdr format, 256*256 size				-- Used as bloom texture
Texture2D RenderTarget128;		//R16B16G16A16F 64 bit hdr format, 128*128 size				-- Used as bloom texture
Texture2D RenderTarget64;		//R16B16G16A16F 64 bit hdr format, 64*64 size				-- Used as bloom texture
Texture2D RenderTarget32;		//R16B16G16A16F 64 bit hdr format, 32*32 size				-- Used as bloom texture
Texture2D RenderTarget16;		//R16B16G16A16F 64 bit hdr format, 16*16 size				-- Used as bloom texture
Texture2D RenderTargetRGBA32;	//R8G8B8A8		32 bit ldr format, screen size
Texture2D RenderTargetRGBA64F;	//R16B16G16A16F 64 bit hdr format, screen size				-- 1/4 Used as source passthrough if activated

#if ENABLE_DIRT_REFLECTION
//Atlas with 4 different lensdirt textures
Texture2D LensDirtAtlas <string ResourceName="Textures/LensDirtTexAtlas.png";>;
#endif

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
// ---- begin include Helper/enbHelper_Common.fxh ----
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

// ---- end include Helper/enbHelper_Common.fxh ----



//----------------------------------------------------------------------------------------------//
//										   Structs												//
//																								//
//----------------------------------------------------------------------------------------------//

struct VertexShaderInput
{
   float3 pos     : POSITION;
   float2 txcoord : TEXCOORD0;
};

struct VertexShaderOutputBasic
{
   float4 pos      : SV_POSITION;
   float2 texcoord : TEXCOORD;
};

struct VertexShaderOutputPrePass
{
   float4 pos               : SV_POSITION;
   float2 texcoord          : TEXCOORD0;
#if BLOOM_PREPASS_STYLE == 1
NI float  UI_InBlack        : TODIE0;
NI float  UI_InWhite        : TODIE1;
NI float  UI_OutBlack       : TODIE2;
NI float  UI_OutWhite       : TODIE3;
NI float  UI_Saturation     : TODIE4;
NI float  UI_SkinAttenu     : TODIE5;
#elif BLOOM_PREPASS_STYLE == 2
NI float  UI_Brightness     : TODIE0;
NI float  UI_Contrast       : TODIE1;
NI float  UI_Saturation     : TODIE2;
NI float  UI_ThresholdLower : TODIE3;
NI float  UI_ThresholdUpper : TODIE4;
NI float  UI_SkinAttenu     : TODIE5;
#endif
};

struct VertexShaderOutputMain
{
   float4 pos             : SV_POSITION;
   float2 texcoord        : TEXCOORD0;
#if ENABLE_DEPTH_TESTING
   float2 origtexcoord    : TEXCOORD1;
#endif
NI bool   Hori            : PRECALC0;
NI bool   SkipPS          : PRECALC1;
NI float2 ScaledPixelSize : PRECALC2;
NI float4 NewScreenSize	  : PRECALC3;
NI float  Intensity       : PRECALC4;
NI float  Sigma           : PRECALC5;
NI float  WeightFactor    : PRECALC6;
NI float  LoopCount       : PRECALC7;
};

struct VertexShaderOutputMix
{
   float4 pos                        : SV_POSITION;
   float2 texcoord                   : TEXCOORD0;
#if ENABLE_DIRT_REFLECTION
   float2 DirtCoords                 : TEXCOORD1;
#endif
NI float UI_RenderTargetStrength1024 : BSTRE0;
NI float UI_RenderTargetStrength512  : BSTRE1;
NI float UI_RenderTargetStrength256  : BSTRE2;
NI float UI_RenderTargetStrength128  : BSTRE3;
NI float UI_RenderTargetStrength64   : BSTRE4;
NI float UI_RenderTargetStrength32   : BSTRE5;
NI float UI_RenderTargetStrength16   : BSTRE6;
#if ENBALE_BLOOM_TINTING
NI float3 UI_RenderTargetTint1024    : BTINT0;
NI float3 UI_RenderTargetTint512     : BTINT1;
NI float3 UI_RenderTargetTint256     : BTINT2;
NI float3 UI_RenderTargetTint128     : BTINT3;
NI float3 UI_RenderTargetTint64      : BTINT4;
NI float3 UI_RenderTargetTint32      : BTINT5;
NI float3 UI_RenderTargetTint16      : BTINT6;
#endif
};


//----------------------------------------------------------------------------------------------//
//								      Variables and Macros										//
//																								//
//----------------------------------------------------------------------------------------------//

//Maximum allowed output HDR brightness
#define MAXHDR 16384.0

//Hardcoded resolutions for bicubic filtering and render scaling - DON'T CHANGE!
#define MAX_BLOOM_RENDER_RES 1024.0
#define OUTPUTRES float2(1024, 1024)

//Maximum loop limit per pass (only change it if you know what you're doing)
#define MAXLOOP 30

//Global variable for gaussian weight calculation
static const float SqrtTwoPI = sqrt(2.0 * PI);

//Array for the different quality level multipliers [VERYHIGH, HIGH, MEDIUM, LOW]
static const float QualityLevel[4] = {1.8, 1.6, 1.2, 1.0};


//----------------------------------------------------------------------------------------------//
//										      Shaders											//
//																								//
//----------------------------------------------------------------------------------------------//

//--------------------------------------------Prepass-------------------------------------------//

VertexShaderOutputPrePass VS_BloomPrePass(VertexShaderInput IN)
{
	VertexShaderOutputPrePass OUT;
	OUT.pos				= float4(IN.pos.xyz,1.0);
	OUT.texcoord.xy = IN.txcoord.xy;
	
	#if UI_SEP_MODE_PRE == 1
	
	#if BLOOM_PREPASS_STYLE == 1
	OUT.UI_InBlack		  = TODIE_SEPARATION(UI_InBlack);
	OUT.UI_InWhite		  = TODIE_SEPARATION(UI_InWhite);
	OUT.UI_OutBlack		  = TODIE_SEPARATION(UI_OutBlack);
	OUT.UI_OutWhite		  = TODIE_SEPARATION(UI_OutWhite);
	OUT.UI_Saturation = TODIE_SEPARATION(UI_Saturation);
	
	#elif BLOOM_PREPASS_STYLE == 2
	OUT.UI_Brightness     = TODIE_SEPARATION(UI_Brightness);
	OUT.UI_Contrast       = TODIE_SEPARATION(UI_Contrast);
	OUT.UI_Saturation     = TODIE_SEPARATION(UI_Saturation);
	OUT.UI_ThresholdLower = TODIE_SEPARATION(UI_ThresholdLower);
	OUT.UI_ThresholdUpper = TODIE_SEPARATION(UI_ThresholdUpper);
	#endif //BLOOM_PREPASS_STYLE
	
	#if ENABLE_SKIN_ATTENUATION
	OUT.UI_SkinAttenu = TODIE_SEPARATION(UI_SkinAttenu);
	#endif
	
	#elif UI_SEP_MODE_PRE == 2
	
	#if BLOOM_PREPASS_STYLE == 1
	OUT.UI_InBlack		  = DNI_SEPARATION(UI_InBlack);
	OUT.UI_InWhite		  = DNI_SEPARATION(UI_InWhite);
	OUT.UI_OutBlack		  = DNI_SEPARATION(UI_OutBlack);
	OUT.UI_OutWhite		  = DNI_SEPARATION(UI_OutWhite);
	OUT.UI_Saturation = DNI_SEPARATION(UI_Saturation);
	
	#elif BLOOM_PREPASS_STYLE == 2
	OUT.UI_Brightness     = DNI_SEPARATION(UI_Brightness);
	OUT.UI_Contrast       = DNI_SEPARATION(UI_Contrast);
	OUT.UI_Saturation     = DNI_SEPARATION(UI_Saturation);
	OUT.UI_ThresholdLower = DNI_SEPARATION(UI_ThresholdLower);
	OUT.UI_ThresholdUpper = DNI_SEPARATION(UI_ThresholdUpper);
	#endif //BLOOM_PREPASS_STYLE
	
	#if ENABLE_SKIN_ATTENUATION
	OUT.UI_SkinAttenu = DNI_SEPARATION(UI_SkinAttenu);
	#endif
	
	#endif //UI_SEP_MODE_PRE
	
	return OUT;
}

float4 PS_BloomPrePass(VertexShaderOutputPrePass IN) : SV_Target
{
	float3 Bloom = TextureDownsampled.Sample(Linear_Sampler, IN.texcoord);
	
	//Use prepass alpha mask to attenuate bloom from skins
	#if ENABLE_SKIN_ATTENUATION
			float SkinMask = TextureOriginal.Sample(Linear_Sampler, IN.texcoord).a;
				  Bloom   *= lerp(1.0, IN.UI_SkinAttenu, saturate(1.0 - SkinMask));
	#endif
	
	//Seperate luma and chroma to prevent hue/saturation shifting
	float  BloomLuma   = dot(Bloom.rgb, K_LUM);
	float3 BloomChroma = Bloom.rgb / BloomLuma;
	
	#if BLOOM_PREPASS_STYLE == 1 //Levels prepass variant
		BloomLuma = zerolim(BloomLuma - IN.UI_InBlack) / deltalim(IN.UI_InWhite - IN.UI_InBlack);
		BloomLuma = mad(deltalim(IN.UI_OutWhite - IN.UI_OutBlack), BloomLuma, IN.UI_OutBlack);
		Bloom.rgb = zerolim(lerp(BloomLuma, BloomLuma * BloomChroma, IN.UI_Saturation));
	
	#elif BLOOM_PREPASS_STYLE == 2 //Thresholds prepass variant
		BloomLuma = mad(BloomLuma, IN.UI_Brightness, 0.18) - 0.18 * IN.UI_Contrast;
		Bloom.rgb = zerolim(lerp(BloomLuma, BloomLuma * BloomChroma, IN.UI_Saturation));
		
		[branch]
		if(UI_Smooth_Threshold) Bloom.rgb *= smoothstep(IN.UI_ThresholdLower, IN.UI_ThresholdUpper, BloomLuma);
		else						Bloom.rgb *= LinearStep(IN.UI_ThresholdLower, IN.UI_ThresholdUpper, BloomLuma);
	#endif //BLOOM_PREPASS_STYLE
	
	#if ENABLE_SOURCE_MASKING
		return float4(Bloom.rgb, dot(Bloom, K_LUM));
	#else
		return float4(Bloom.rgb, 1.0);
	#endif
}


//-----------------------------------Main Bloom Pass - Dynamic------------------------------------//

VertexShaderOutputMain VS_GaussBloomMainDynamic(VertexShaderInput IN, uniform float TexSize,
																      uniform bool  Hori,
																      uniform float MaxLoop)
{
	VertexShaderOutputMain OUT;
	
	//Horizontal mode: Scales down the entire screen to the resolution of the next rendertarget
	//Vertical mode: Scales texture coordinates to the new screen size
	// -> without scaling, lower res rendertargets will have a fullres
	//    horizontal blur and waste performance that way
	
	float2 Transform; Transform.x = MAX_BLOOM_RENDER_RES / TexSize;
					  Transform.y = (Transform.x - 1.0) / Transform.x;
	
	//Screen quad and texcoord scaling
	OUT.pos.xy = Hori ? IN.pos.xy / Transform.x + float2(-Transform.y, Transform.y) : IN.pos.xy;
	OUT.pos.zw = float2(IN.pos.z, 1.0);
	OUT.texcoord.xy = Hori ? IN.txcoord.xy : IN.txcoord.xy / Transform.x;
	
	//Pixelsize scaling and screen boundary computation
	OUT.ScaledPixelSize  = rcp(TexSize) * (Hori ? float2(1.0, 0.0) : float2(0.0, ScreenSize.z / Transform.x));
	OUT.NewScreenSize    = (Hori ? 1.0 : rcp(Transform.x)) + float4(-OUT.ScaledPixelSize, OUT.ScaledPixelSize);
	OUT.ScaledPixelSize *= min(Transform.x / 4.0, 2.0);
	
	#if UI_SEP_MODE_MAIN == 1
		  OUT.Sigma		       = TODIE_SEPARATION(UI_Sigma);
	float UI_HoriIntensity = TODIE_SEPARATION(UI_HoriIntensity);
	float UI_VertIntensity = TODIE_SEPARATION(UI_VertIntensity);
	
	#elif UI_SEP_MODE_MAIN == 2
		  OUT.Sigma		       = DNI_SEPARATION(UI_Sigma);
	float UI_HoriIntensity = DNI_SEPARATION(UI_HoriIntensity);
	float UI_VertIntensity = DNI_SEPARATION(UI_VertIntensity);
	#endif //UI_SEP_MODE_MAIN
	
	//Skips pixel shader of low res rendertargets when bloom sigma is too small
	// -> saves performance and helps against aliasing artifacts
	OUT.SkipPS = 0.0 > (max(OUT.Sigma, 1.0) - pow(Transform.x, 0.2));
	
	if(!OUT.SkipPS)
	{
		OUT.Sigma     = min(OUT.Sigma, MaxLoop - 1.5);
		OUT.Intensity = Hori ? UI_HoriIntensity : UI_VertIntensity;
		OUT.Hori      = Hori;
		
		#if ENABLE_DEPTH_TESTING
			OUT.origtexcoord = IN.txcoord.xy;
		#else
			OUT.WeightFactor =  rcp(OUT.Sigma * SqrtTwoPI);
			OUT.LoopCount    = ceil(OUT.Sigma * QualityLevel[UI_Quality+1]);
			OUT.LoopCount    =  min(OUT.LoopCount, MAXLOOP);
			OUT.Sigma		 = -rcp(OUT.Sigma * OUT.Sigma);
		#endif
	}
	
	return OUT;
}

float4 PS_GaussBloomMainDynamic(VertexShaderOutputMain IN, uniform Texture2D InputTex, uniform bool HQ_Pass) : SV_Target
{
	if(IN.SkipPS) return 0.0; //Don't use clip operation!
	
	#if ENABLE_DEPTH_TESTING
		bool  EnableDepthTesting = UI_Depth_Calc && !EInteriorFactor && HQ_Pass;
		float Depth				 = 1.0;

		//Simple depth test to manipulate bloom sigma and intensity
		[branch] if(EnableDepthTesting)
		{
			Depth		 = TextureDepth.Sample(Linear_Sampler, IN.origtexcoord).x;
			Depth		 = FastLinDepth(Depth, UI_FarDepth);
			Depth		 = abs(UI_DepthInvert - Depth) + 1.0;
			IN.Sigma = lerp(IN.Sigma, IN.Sigma * Depth, UI_DepthWidth);
		}

		IN.WeightFactor =  rcp(IN.Sigma * SqrtTwoPI);
		IN.LoopCount    = ceil(IN.Sigma * QualityLevel[UI_Quality+1]);
		IN.LoopCount    =  min(IN.LoopCount, MAXLOOP);
		IN.Sigma		= -rcp(IN.Sigma * IN.Sigma);
	#endif
	
	//Gaussian based bloom/blur with realtime adjustable kernel
	float3 Bloom		 = IN.WeightFactor * InputTex.Sample(Linear_Sampler, IN.texcoord).rgb;
	float  WeightSum = IN.WeightFactor;
	
	[loop] for(float i=1.0; i <= IN.LoopCount; i++)
	{
		float4 Offset = IN.texcoord.xyxy + IN.ScaledPixelSize.xyxy * float4(i.xx, -i.xx);
		
		#if ENABLE_AGRESSIVE_BORDER_CORRECTION
		//Fixes wrongly weighted pixels at screen borders by ignoring out of bound samples
		float2 GaussWeight  = IN.WeightFactor * exp(i*i*IN.Sigma);
		float2 OffsetTest   = IN.Hori ? Offset.xz : Offset.yw;
			   GaussWeight *= ceil(OffsetTest - DELTA) * abs(floor(OffsetTest - IN.NewScreenSize.yw));
			   Bloom	   += GaussWeight.x * InputTex.SampleLevel(Linear_Sampler, Offset.xy, 0).rgb;
			   Bloom	   += GaussWeight.y * InputTex.SampleLevel(Linear_Sampler, Offset.zw, 0).rgb;
			   WeightSum   += GaussWeight.x + GaussWeight.y;
		#else
		//Fixes pixels at the new screen borders by clamping offset coords to the new size
		float GaussWeight = IN.WeightFactor * exp(i*i*IN.Sigma);
			  Offset	  = saturate(min(Offset, IN.NewScreenSize));
			  Bloom		 += GaussWeight * InputTex.SampleLevel(Linear_Sampler, Offset.xy, 0).rgb;
			  Bloom		 += GaussWeight * InputTex.SampleLevel(Linear_Sampler, Offset.zw, 0).rgb;
			  WeightSum  += GaussWeight * 2.0;
		#endif
	}
	
	Bloom /= WeightSum;
	
	#if ENABLE_DEPTH_TESTING
	[branch] if(EnableDepthTesting)
		Bloom *= lerp(IN.Intensity, IN.Intensity * Depth, UI_DepthInt); else
	#endif
		Bloom *= IN.Intensity;
	
	return float4(Bloom, 1.0);
}


//----------------------------------------SourceGrab Pass---------------------------------------//

#if ENABLE_SOURCE_MASKING
//Grab and write bloomsource at half screen res to the rendertarget
VertexShaderOutputBasic VS_GrabSource (VertexShaderInput IN)
{
	VertexShaderOutputBasic OUT;
	OUT.pos.xy		= IN.pos.xy * 0.5 + float2(-0.5, 0.5);
	OUT.pos.zw		= float2(IN.pos.z, 1.0);
	OUT.texcoord.xy = IN.txcoord.xy;
	return OUT;
}

float4 PS_GrabSource(VertexShaderOutputBasic IN) : SV_Target
{
	if(UI_Mask_BloomSource) return TextureColor.Sample(Linear_Sampler, IN.texcoord);
	else					return 0.0;
}
#endif


//----------------------------------------Bloom Mix Pass----------------------------------------//

VertexShaderOutputMix VS_BloomMix(VertexShaderInput IN)
{
	VertexShaderOutputMix OUT;
	OUT.pos				= float4(IN.pos.xyz,1.0);
	OUT.texcoord.xy = IN.txcoord.xy;
	
	#if ENABLE_DIRT_REFLECTION
	OUT.DirtCoords = AtlasFetch_4(IN.txcoord, UI_DirtSelect);
	#endif
	
	#if ENABLE_AUTOMATIC_WEIGHTING
	#if UI_SEP_MODE_MIX == 1
	float UI_AutoWeight_Bias = TODIE_SEPARATION(UI_AutoWeight_Bias);
	#elif UI_SEP_MODE_MIX == 2
	float UI_AutoWeight_Bias = DNI_SEPARATION(UI_AutoWeight_Bias);
	#endif
	
	float PassStrength[7];
	
	float WeightFactor = rcp(UI_AutoWeight_Bias * SqrtTwoPI);
	float Sigma		   = rcp(UI_AutoWeight_Bias * UI_AutoWeight_Bias);
	
	[unroll] for(int i=0; i<7; i++)
			PassStrength[i] = WeightFactor * exp(i*i*-Sigma);
	
	OUT.UI_RenderTargetStrength1024 = PassStrength[0];
	OUT.UI_RenderTargetStrength512		= PassStrength[1];
	OUT.UI_RenderTargetStrength256		= PassStrength[2];
	OUT.UI_RenderTargetStrength128		= PassStrength[3];
	OUT.UI_RenderTargetStrength64		= PassStrength[4];
	OUT.UI_RenderTargetStrength32		= PassStrength[5];
	OUT.UI_RenderTargetStrength16		= PassStrength[6];
	
	#else
	
	#if UI_SEP_MODE_MIX == 1
	OUT.UI_RenderTargetStrength1024 = TODIE_SEPARATION(UI_RenderTargetStrength1024);
	OUT.UI_RenderTargetStrength512  = TODIE_SEPARATION(UI_RenderTargetStrength512);
	OUT.UI_RenderTargetStrength256  = TODIE_SEPARATION(UI_RenderTargetStrength256);
	OUT.UI_RenderTargetStrength128  = TODIE_SEPARATION(UI_RenderTargetStrength128);
	OUT.UI_RenderTargetStrength64   = TODIE_SEPARATION(UI_RenderTargetStrength64);
	OUT.UI_RenderTargetStrength32   = TODIE_SEPARATION(UI_RenderTargetStrength32);
	OUT.UI_RenderTargetStrength16   = TODIE_SEPARATION(UI_RenderTargetStrength16);
	
	#elif UI_SEP_MODE_MIX == 2
	OUT.UI_RenderTargetStrength1024 = DNI_SEPARATION(UI_RenderTargetStrength1024);
	OUT.UI_RenderTargetStrength512  = DNI_SEPARATION(UI_RenderTargetStrength512);
	OUT.UI_RenderTargetStrength256  = DNI_SEPARATION(UI_RenderTargetStrength256);
	OUT.UI_RenderTargetStrength128  = DNI_SEPARATION(UI_RenderTargetStrength128);
	OUT.UI_RenderTargetStrength64   = DNI_SEPARATION(UI_RenderTargetStrength64);
	OUT.UI_RenderTargetStrength32   = DNI_SEPARATION(UI_RenderTargetStrength32);
	OUT.UI_RenderTargetStrength16   = DNI_SEPARATION(UI_RenderTargetStrength16);
	#endif //UI_SEP_MODE_MIX
	#endif //ENABLE_AUTOMATIC_WEIGHTING
	
	
	#if ENBALE_BLOOM_TINTING
	#if UI_SEP_MODE_MIX == 1
	OUT.UI_RenderTargetTint1024 = TODIE_SEPARATION(UI_RenderTargetTint1024);
	OUT.UI_RenderTargetTint512  = TODIE_SEPARATION(UI_RenderTargetTint512);
	OUT.UI_RenderTargetTint256  = TODIE_SEPARATION(UI_RenderTargetTint256);
	OUT.UI_RenderTargetTint128  = TODIE_SEPARATION(UI_RenderTargetTint128);
	OUT.UI_RenderTargetTint64   = TODIE_SEPARATION(UI_RenderTargetTint64);
	OUT.UI_RenderTargetTint32   = TODIE_SEPARATION(UI_RenderTargetTint32);
	OUT.UI_RenderTargetTint16   = TODIE_SEPARATION(UI_RenderTargetTint16);
	
	#elif UI_SEP_MODE_MIX == 2
	OUT.UI_RenderTargetTint1024 = DNI_SEPARATION(UI_RenderTargetTint1024);
	OUT.UI_RenderTargetTint512  = DNI_SEPARATION(UI_RenderTargetTint512);
	OUT.UI_RenderTargetTint256  = DNI_SEPARATION(UI_RenderTargetTint256);
	OUT.UI_RenderTargetTint128  = DNI_SEPARATION(UI_RenderTargetTint128);
	OUT.UI_RenderTargetTint64   = DNI_SEPARATION(UI_RenderTargetTint64);
	OUT.UI_RenderTargetTint32   = DNI_SEPARATION(UI_RenderTargetTint32);
	OUT.UI_RenderTargetTint16   = DNI_SEPARATION(UI_RenderTargetTint16);
	#endif //UI_SEP_MODE_MIX
	
	OUT.UI_RenderTargetTint1024 = ColorToChroma(OUT.UI_RenderTargetTint1024);
	OUT.UI_RenderTargetTint512  = ColorToChroma(OUT.UI_RenderTargetTint512);
	OUT.UI_RenderTargetTint256  = ColorToChroma(OUT.UI_RenderTargetTint256);
	OUT.UI_RenderTargetTint128  = ColorToChroma(OUT.UI_RenderTargetTint128);
	OUT.UI_RenderTargetTint64   = ColorToChroma(OUT.UI_RenderTargetTint64);
	OUT.UI_RenderTargetTint32   = ColorToChroma(OUT.UI_RenderTargetTint32);
	OUT.UI_RenderTargetTint16   = ColorToChroma(OUT.UI_RenderTargetTint16);
	#endif //ENBALE_BLOOM_TINTING
	
	//Check if RenderTarget got skipped (helps with normalization later)
	OUT.UI_RenderTargetStrength1024 *= RenderTarget1024.Load(0).a;
	OUT.UI_RenderTargetStrength512  *= RenderTarget512. Load(0).a;
	OUT.UI_RenderTargetStrength256  *= RenderTarget256. Load(0).a;
	OUT.UI_RenderTargetStrength128  *= RenderTarget128. Load(0).a;
	OUT.UI_RenderTargetStrength64   *= RenderTarget64.  Load(0).a;
	OUT.UI_RenderTargetStrength32   *= RenderTarget32.  Load(0).a;
	OUT.UI_RenderTargetStrength16   *= RenderTarget16.  Load(0).a;
	
	return OUT;
}


float4 PS_BloomMix(VertexShaderOutputMix IN) : SV_Target
{
	float3 Bloom, Bloom1024, Bloom512, Bloom256, Bloom128, Bloom64, Bloom32, Bloom16;
	
	#if USE_BICUBIC_FILTERING
		Bloom1024 =   RenderTarget1024.Sample(Linear_Sampler, IN.texcoord).rgb * IN.UI_RenderTargetStrength1024;
		Bloom512  = BicubicFilter(RenderTarget512, IN.texcoord, OUTPUTRES).rgb * IN.UI_RenderTargetStrength512;
		Bloom256  = BicubicFilter(RenderTarget256, IN.texcoord, OUTPUTRES).rgb * IN.UI_RenderTargetStrength256;
		Bloom128  = BicubicFilter(RenderTarget128, IN.texcoord, OUTPUTRES).rgb * IN.UI_RenderTargetStrength128;
		Bloom64   = BicubicFilter(RenderTarget64,  IN.texcoord, OUTPUTRES).rgb * IN.UI_RenderTargetStrength64;
		Bloom32   = BicubicFilter(RenderTarget32,  IN.texcoord, OUTPUTRES).rgb * IN.UI_RenderTargetStrength32;
		Bloom16   = BicubicFilter(RenderTarget16,  IN.texcoord, OUTPUTRES).rgb * IN.UI_RenderTargetStrength16;
	#else
		Bloom1024 = RenderTarget1024.Sample(Linear_Sampler, IN.texcoord).rgb   * IN.UI_RenderTargetStrength1024;
		Bloom512  = RenderTarget512. Sample(Linear_Sampler, IN.texcoord).rgb   * IN.UI_RenderTargetStrength512;
		Bloom256  = RenderTarget256. Sample(Linear_Sampler, IN.texcoord).rgb   * IN.UI_RenderTargetStrength256;
		Bloom128  = RenderTarget128. Sample(Linear_Sampler, IN.texcoord).rgb   * IN.UI_RenderTargetStrength128;
		Bloom64   = RenderTarget64.  Sample(Linear_Sampler, IN.texcoord).rgb   * IN.UI_RenderTargetStrength64;
		Bloom32   = RenderTarget32.  Sample(Linear_Sampler, IN.texcoord).rgb   * IN.UI_RenderTargetStrength32;
		Bloom16   = RenderTarget16.  Sample(Linear_Sampler, IN.texcoord).rgb   * IN.UI_RenderTargetStrength16;
	#endif
	
	#if ENBALE_BLOOM_TINTING
		Bloom1024 *= IN.UI_RenderTargetTint1024;
		Bloom512  *= IN.UI_RenderTargetTint512;
		Bloom256  *= IN.UI_RenderTargetTint256;
		Bloom128  *= IN.UI_RenderTargetTint128;
		Bloom64   *= IN.UI_RenderTargetTint64;
		Bloom32   *= IN.UI_RenderTargetTint32;
		Bloom16   *= IN.UI_RenderTargetTint16;
	#endif
	
	#if ENABLE_TOOLS
	[branch] switch (UI_PASSOUTPUT)
	{
		case 1: return float4(clamp(Bloom1024,0.0,MAXHDR),1.0);
		case 2: return float4(clamp(Bloom512, 0.0,MAXHDR),1.0);
		case 3: return float4(clamp(Bloom256, 0.0,MAXHDR),1.0);
		case 4: return float4(clamp(Bloom128, 0.0,MAXHDR),1.0);
		case 5: return float4(clamp(Bloom64,  0.0,MAXHDR),1.0);
		case 6: return float4(clamp(Bloom32,  0.0,MAXHDR),1.0);
		case 7: return float4(clamp(Bloom16,  0.0,MAXHDR),1.0);
		default: break; //case 0
	}
	
	#if ENABLE_DEPTH_TESTING
	[branch] if (UI_Visualize_Depth)
	{
		float Depth = TextureDepth.Sample(Linear_Sampler, IN.texcoord).x;
			  Depth = FastLinDepth(Depth, UI_FarDepth);
		return abs(UI_DepthInvert - Depth) + 1.0;
	}
	#endif //ENABLE_DEPTH_TESTING
	#endif //ENABLE_TOOLS
	
	Bloom = Bloom1024 + Bloom512 + Bloom256 + Bloom128 + Bloom64 + Bloom32 + Bloom16;
	
	if(UI_Normalize_BloomSum)
	Bloom /= IN.UI_RenderTargetStrength1024 + IN.UI_RenderTargetStrength512 +
			 IN.UI_RenderTargetStrength256  + IN.UI_RenderTargetStrength128 +
			 IN.UI_RenderTargetStrength64   + IN.UI_RenderTargetStrength32  +
			 IN.UI_RenderTargetStrength16;
	
	#if ENABLE_TINYBLOOM
	if(UI_TinyBloom) Bloom += pow(dot(zerolim(Bloom512 - Bloom1024 * 0.5), K_LUM) * 0.5, 1.5);
	#endif
	
	#if ENABLE_SOURCE_MASKING
	[branch] if (UI_Mask_BloomSource)
	{
		float4 Source = RenderTargetRGBA64F.Sample(Linear_Sampler, IN.texcoord*0.5);
			   Bloom  = lerp (Bloom, Bloom - Source.rgb, Source.a * UI_Mask_Weight);
	}
	#endif
	
	#if ENABLE_DIRT_REFLECTION
	[branch] if (UI_EnableDirtRef)
	{
		float2 RefCoords = 1.0 - IN.texcoord;
		float3 DirtRef		 = 0.5 * (RenderTarget32.Sample(Linear_Sampler, RefCoords).rgb +
								  RenderTarget16.Sample(Linear_Sampler, RefCoords).rgb);
			   DirtRef		+= DirtRef * LensDirtAtlas.Sample(Linear_Sampler, IN.DirtCoords).rgb;
			   DirtRef  *= smoothstep(0.0, UI_DirtRefThresh * 30.0, dot(DirtRef, K_LUM));
			   Bloom		+= DirtRef * UI_DirtRef * pow(length(IN.texcoord * 2.0 - 1.0), UI_DirtRefCurve);
	}
	#endif
	
	#if ENABLE_BLOOM_GRAIN //Simple bloom restricted grain
	[branch] if(UI_Enable_Grain)
	{
		//Grain is here to obscure banding a bit, but if you want to get rid of it more effectively
		//add dithering after mixing in the bloom texture
		float3 Grain;
		float3 TimerSeed = Timer.x * UI_GrainMotion + float3(0.01, 0.02, 0.03);
		
		Grain.r = RandomGauss(IN.texcoord + float2(0.0, TimerSeed.x));
		Grain.g = RandomGauss(IN.texcoord + float2(TimerSeed.y, 0.0));
		Grain.b = RandomGauss(IN.texcoord + TimerSeed.z);
		Grain		= lerp(dot(Grain, N_LUM), Grain, UI_GrainSaturation);
		
		float GrainInt = saturate(max3(Bloom) * 4.0) * UI_GrainIntensity;
			  Bloom   += Grain * GrainInt - GrainInt * 0.5;
	}
	#endif
	
	return float4(clamp(Bloom, 0.0, MAXHDR), 1.0);
}


//----------------------------------------------------------------------------------------------//
//										     Techniques											//
//																								//
//----------------------------------------------------------------------------------------------//

#define BLOOMTECH11(NAME, VS_VALUES, PS_VALUES) technique11 NAME { pass p0 { \
SetVertexShader(CompileShader(vs_5_0, VS_GaussBloomMainDynamic##VS_VALUES));\
SetPixelShader(CompileShader(ps_5_0, PS_GaussBloomMainDynamic##PS_VALUES)); } }


#if !ENABLE_SOURCE_MASKING
TECH11	    (KitsuuneGaussianBloom   <string UIName="Dynamic Multipass Bloom - Kitsuune";>, VS_BloomPrePass(), PS_BloomPrePass())
BLOOMTECH11 (KitsuuneGaussianBloom1,												(1024.0, true,  256.0), (TextureColor,     true))
BLOOMTECH11 (KitsuuneGaussianBloom2  <string RenderTarget="RenderTarget1024";>,		(1024.0, false, 256.0), (TextureColor,     true))
BLOOMTECH11 (KitsuuneGaussianBloom3,												(512.0,  true,  128.0), (RenderTarget1024, true))
BLOOMTECH11 (KitsuuneGaussianBloom4  <string RenderTarget="RenderTarget512";>,		(512.0,  false, 128.0), (TextureColor,     true))
BLOOMTECH11 (KitsuuneGaussianBloom5,												(256.0,  true,  64.0),  (RenderTarget512,  false))
BLOOMTECH11 (KitsuuneGaussianBloom6  <string RenderTarget="RenderTarget256";>,		(256.0,  false, 64.0),  (TextureColor,     false))
BLOOMTECH11 (KitsuuneGaussianBloom7,												(128.0,  true,  32.0),  (RenderTarget256,  false))
BLOOMTECH11 (KitsuuneGaussianBloom8  <string RenderTarget="RenderTarget128";>,		(128.0,  false, 32.0),  (TextureColor,     false))
BLOOMTECH11 (KitsuuneGaussianBloom9,												(64.0,   true,  16.0),  (RenderTarget128,  false))
BLOOMTECH11 (KitsuuneGaussianBloom10 <string RenderTarget="RenderTarget64";>,		(64.0,   false, 16.0),  (TextureColor,     false))
BLOOMTECH11 (KitsuuneGaussianBloom11,												(32.0,   true,  8.0),   (RenderTarget64,   false))
BLOOMTECH11 (KitsuuneGaussianBloom12 <string RenderTarget="RenderTarget32";>,		(32.0,   false, 8.0),   (TextureColor,     false))
BLOOMTECH11 (KitsuuneGaussianBloom13,												(16.0,   true,  4.0),   (RenderTarget32,   false))
BLOOMTECH11 (KitsuuneGaussianBloom14 <string RenderTarget="RenderTarget16";>,		(16.0,   false, 4.0),   (TextureColor,     false))
TECH11	    (KitsuuneGaussianBloom15, VS_BloomMix(), PS_BloomMix())

#else

TECH11	    (KitsuuneGaussianBloom   <string UIName="Dynamic Multipass Bloom - Kitsuune";>, VS_BloomPrePass(), PS_BloomPrePass())
TECH11	    (KitsuuneGaussianBloom1  <string RenderTarget="RenderTargetRGBA64F";>,		  VS_GrabSource(),   PS_GrabSource())
BLOOMTECH11 (KitsuuneGaussianBloom2,												(1024.0, true,  256.0), (TextureColor,     true))
BLOOMTECH11 (KitsuuneGaussianBloom3  <string RenderTarget="RenderTarget1024";>,		(1024.0, false, 256.0), (TextureColor,     true))
BLOOMTECH11 (KitsuuneGaussianBloom4,												(512.0,  true,  128.0), (RenderTarget1024, true))
BLOOMTECH11 (KitsuuneGaussianBloom5  <string RenderTarget="RenderTarget512";>,		(512.0,  false, 128.0), (TextureColor,     true))
BLOOMTECH11 (KitsuuneGaussianBloom6,												(256.0,  true,  64.0),  (RenderTarget512,  false))
BLOOMTECH11 (KitsuuneGaussianBloom7  <string RenderTarget="RenderTarget256";>,		(256.0,  false, 64.0),  (TextureColor,     false))
BLOOMTECH11 (KitsuuneGaussianBloom8,												(128.0,  true,  32.0),  (RenderTarget256,  false))
BLOOMTECH11 (KitsuuneGaussianBloom9  <string RenderTarget="RenderTarget128";>,		(128.0,  false, 32.0),  (TextureColor,     false))
BLOOMTECH11 (KitsuuneGaussianBloom10,												(64.0,   true,  16.0),  (RenderTarget128,  false))
BLOOMTECH11 (KitsuuneGaussianBloom11 <string RenderTarget="RenderTarget64";>,		(64.0,   false, 16.0),  (TextureColor,     false))
BLOOMTECH11 (KitsuuneGaussianBloom12,												(32.0,   true,  8.0),   (RenderTarget64,   false))
BLOOMTECH11 (KitsuuneGaussianBloom13 <string RenderTarget="RenderTarget32";>,		(32.0,   false, 8.0),   (TextureColor,     false))
BLOOMTECH11 (KitsuuneGaussianBloom14,												(16.0,   true,  4.0),   (RenderTarget32,   false))
BLOOMTECH11 (KitsuuneGaussianBloom15 <string RenderTarget="RenderTarget16";>,		(16.0,   false, 4.0),   (TextureColor,     false))
TECH11	    (KitsuuneGaussianBloom16, VS_BloomMix(), PS_BloomMix())
#endif

