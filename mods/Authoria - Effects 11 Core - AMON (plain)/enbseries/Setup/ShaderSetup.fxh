//================================= Credits =====================================//
// Kingeric1992: Countless Shaders and code in mutiple files                     //
// Prod80: Many Shaders for his oldrim ENB,s that i reused                       //
// JawZ: Autor of MSL                                                            //
// Aiyen: Autor of Skylight ENB                                                  //
// Tapikos: TOD seperation code that got applied to many shaders here            //
// CeeJay.dk: Orginal Autor of SweetFX and its Shaders                           //
// Marty McFly: Autor of Mastereffect and many other Shaders                     //
// Insomnia: Quite a few Reshade 3.x ports that were really helpful              //
// Crosire: Orginal Autor of Reshade                                             //
// TreyM: A big inspiration and also a great help with questions                 //
// L00: Also a very big inspiration for me                                       //
// Evok: Being a big help, motivation, friend and tweaker for me                 //
// Adyss: Autor of this ENB setup                                                //
//===============================================================================//
// How to use: switch the 1/0 out to enable shaders. Some of them need a pass    //
// implementation (read in TechniquesSetup.fxh) Choose only what you need. Blind //
// toggle of all effects will kill fps and also wont look good at all ;)         //


//===============================================================================//
//                         enbeffectpostpass.fx settings                         //
//===============================================================================//

#define postpassname             "Post FX"

//========================== Active Postpass Shaders ============================//
#define INC_Vibrance            1
#define INC_DPX                 1
#define INC_Filmpass            1
#define INC_Spherical           1
#define INC_Reinhard            2     // 1 = Linear   2 = Normal
#define INC_Curves              1
#define INC_Technicolor         1
#define INC_Technicolor2        1
#define INC_Tint                1
#define INC_Letterbox           1
#define INC_HDR                 0
#define INC_Lightroom           0
#define INC_Shadow              1      // Shadow Adjustments
#define INC_FishEye             1
#define INC_Emboss              0
#define INC_SBloom              1      // Bloom from SweetFX
#define INC_GaussBloom          0      // Gaussian Bloom (needs Pass implementation)
#define INC_LumaSHARP           0      // needs Pass implementation
#define INC_FilmicAnamorphSharp 1      // needs Pass implementation
#define INC_BasicSharp          0      // needs Pass implementation

//===============================================================================//
//                             enbeffect.fx settings                             //
//===============================================================================//

#define enbeffectname              "Daycycle"

//========================== Active Enbeffect Shaders ===========================//
#define INC_EYEAdaptation   1 
#define INC_FilmicTonemap   1
#define INC_AGCC            1 // Applies some Weather defined color Values that also can be tweaked ingame
#define INC_BloomControl    1 // Adds Tweakable values to the bloom
#define INC_AGCC_Tone       1 // AGCC Tonemapper (currently not really working :/ )