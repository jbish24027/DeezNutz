//============================== V1.0 ===============================//
//   ______   ______     ______     ______      ______   __  __      //
//  /\  == \ /\  __ \   /\  ___\   /\__  _\    /\  ___\ /\_\_\_\     //
//  \ \  _-/ \ \ \/\ \  \ \___  \  \/_/\ \/    \ \  __\ \/_/\_\/_    //
//   \ \_\    \ \_____\  \/\_____\    \ \_\     \ \_\     /\_\/\_\   //
//    \/_/     \/_____/   \/_____/     \/_/      \/_/     \/_/\/_/   //
//                                                                   //
//===================================================================//

//========================================//
// external enb parameters, do not modify //
//========================================//
float4	Timer;
float4	ScreenSize;
float	AdaptiveQuality;
float4	Weather;
float4	TimeOfDay1;
float4	TimeOfDay2;
float	ENightDayFactor;
float	EInteriorFactor;

float4	tempF1; //0,1,2,3
float4	tempF2; //5,6,7,8
float4	tempF3; //9,0

float4	tempInfo1;
float4	tempInfo2;

//=============================//
// Mod Parameters and Textures //
//=============================//
Texture2D			TextureOriginal;
Texture2D			TextureColor;
Texture2D			TextureDepth;

Texture2D			RenderTargetRGBA32;
Texture2D			RenderTargetRGBA64;
Texture2D			RenderTargetRGBA64F;
Texture2D			RenderTargetR16F;
Texture2D			RenderTargetR32F;
Texture2D			RenderTargetRGB32F;

//==========//
// SAMPLERS //
//==========//
SamplerState		Sampler0
{
	Filter = MIN_MAG_MIP_POINT;
	AddressU = Clamp;
	AddressV = Clamp;
};

SamplerState		Sampler1
{
	Filter = MIN_MAG_MIP_LINEAR;
	AddressU = Clamp;
	AddressV = Clamp;
};

//================//
// DATA STRUCTURE //
//================//
struct VS_INPUT_POST
{
	float3 pos		: POSITION;
	float2 txcoord	: TEXCOORD0;
};
struct VS_OUTPUT_POST
{
	float4 pos		: SV_POSITION;
	float2 txcoord0	: TEXCOORD0;
};


//======================================================//
// ---- begin include Shaders/helper.fxh ----
//==========================================//
// Based of parts from msHelper.fxh by JawZ //
//==========================================//

#define PixelSize 		float2(ScreenSize.y,ScreenSize.y*ScreenSize.z)

#define TAU 6.28318

float3 HUEToRGB(in float H)
{
   float R = abs(H * 6 - 3) - 1;
   float G = 2 - abs(H * 6 - 2);
   float B = 2 - abs(H * 6 - 4);
   return saturate(float3(R,G,B));
}

float Epsilon = 1e-10;

float3 RGBToHCV(in float3 RGB)
{
   // Based on work by Sam Hocevar and Emil Persson
   float4 P = (RGB.g < RGB.b) ? float4(RGB.bg, -1.0, 2.0/3.0) : float4(RGB.gb, 0.0, -1.0/3.0);
   float4 Q = (RGB.r < P.x) ? float4(P.xyw, RGB.r) : float4(RGB.r, P.yzx);
   float C = Q.x - min(Q.w, Q.y);
   float H = abs((Q.w - Q.y) / (6 * C + Epsilon) + Q.z);
   return float3(H, C, Q.x);
}

float3 RGBToHSL(in float3 RGB)
{
   float3 HCV = RGBToHCV(RGB);
   float L = HCV.z - HCV.y * 0.5;
   float S = HCV.y / (1 - abs(L * 2 - 1) + Epsilon);
   return float3(HCV.x, S, L);
}

float3 HSLToRGB(in float3 HSL)
{
   float3 RGB = HUEToRGB(HSL.x);
   float C = (1 - abs(2 * HSL.z - 1)) * HSL.y;
   return (RGB - 0.5) * C + HSL.z;
}

float grayValue(float3 gv)
{
   return dot( gv, float3(0.2125, 0.7154, 0.0721) );
}

float Luminance( float3 c )
{
	return dot( c, float3(0.22, 0.707, 0.071) );
}

float3 HUEtoRGB(in float H)
{
   float R = abs(H * 6.0 - 3.0) - 1.0;
   float G = 2.0 - abs(H * 6.0 - 2.0);
   float B = 2.0 - abs(H * 6.0 - 4.0);
   return saturate(float3(R,G,B));
}

float RGBCVtoHUE(in float3 RGB, in float C, in float V)
{
     float3 Delta = (V - RGB) / C;
     Delta.rgb -= Delta.brg;
     Delta.rgb += float3(2.0,4.0,6.0);
     Delta.brg = step(V, RGB) * Delta.brg;
     float H;
     H = max(Delta.r, max(Delta.g, Delta.b));
     return frac(H / 6.0);
}

float3 HSVtoRGB(in float3 HSV)
{
   float3 RGB = HUEtoRGB(HSV.x);
   return ((RGB - 1) * HSV.y + 1) * HSV.z;
}
 
float3 RGBtoHSV(in float3 RGB)
{
   float3 HSV = 0.0;
   HSV.z = max(RGB.r, max(RGB.g, RGB.b));
   float M = min(RGB.r, min(RGB.g, RGB.b));
   float C = HSV.z - M;
   if (C != 0.0)
   {
     HSV.x = RGBCVtoHUE(RGB, C, HSV.z);
     HSV.y = C / HSV.z;
   }
   return HSV;
}


// Define CoefLuma for Reshade ports
#define CoefLuma float3(0.2126, 0.7152, 0.0722)      // BT.709 & sRBG luma coefficient (Monitors and HD Television)

float smootherstep(float edge0, float edge1, float x)
{
   x = clamp((x - edge0)/(edge1 - edge0), 0.0, 1.0);
   return x*x*x*(x*(x*6 - 15) + 10);
}

float3 RGBtoXYZ(float3 color) {
  static const float3x3 RGB2XYZ = {0.412453f, 0.357580f, 0.180423f,
                                   0.212671f,  0.715160f, 0.072169f,
                                   0.019334f, 0.119193f,  0.950227f};
  return mul(RGB2XYZ, color.rgb);
}

// XYZ to Yxy conversion
float3 XYZtoYxy(float3 XYZ) {

   float4 Yxy = 0.0f;

   Yxy.r = XYZ.g;                                  /// Copy luminance Y
   Yxy.g = XYZ.r / (XYZ.r + XYZ.g + XYZ.b ); /// x = X / (X + Y + Z)
   Yxy.b = XYZ.g / (XYZ.r + XYZ.g + XYZ.b ); /// y = Y / (X + Y + Z)

  return Yxy.rgb;
}

// Define LUM_709 for Use in Pixel Shader... uhm ya again
#define LUM_709  float3(0.2125, 0.7154, 0.0721)

// RGB to Yxy conversion
float3 RGBtoYxy(float3 color) {
/// Implementation example;
///   float3 Yxy = RGBtoYxy(color.rgb);

  /// RGB to XYZ conversion
    static const float3x3 RGB2XYZ = {0.412453f, 0.357580f, 0.180423f,
                                     0.212671f,  0.715160f, 0.072169f,
                                     0.019334f, 0.119193f,  0.950227f};

    float3 XYZ = mul(RGB2XYZ, color.rgb);

 /// XYZ to Yxy conversion
   float4 Yxy = 0.0f;

   Yxy.r = XYZ.y;                                  /// Copy luminance Y
   Yxy.g = XYZ.x / (XYZ.x + XYZ.y + XYZ.z ); /// x = X / (X + Y + Z)
   Yxy.b = XYZ.y / (XYZ.x + XYZ.y + XYZ.z ); /// y = Y / (X + Y + Z)

  return Yxy.rgb;
}

// Yxy to RGB conversion
float3 YxytoRGB(float3 Yxy) {
/// Implementation example;
///   color.rgb = YxytoRGB(Yxy.rgb);

  /// Yxy to XYZ conversion
   float3 XYZ = 0.0f;

    XYZ.r = Yxy.r * Yxy.g / Yxy. b;              /// X = Y * x / y
    XYZ.g = Yxy.r;                               /// Copy luminance Y
    XYZ.b = Yxy.r * (1 - Yxy.g - Yxy.b) / Yxy.b; /// Z = Y * (1-x-y) / y

  /// XYZ to RGB conversion
    static const float3x3 XYZ2RGB = {3.240479f, -1.537150f, -0.498535f,
                                     -0.969256f, 1.875992f, 0.041556f, 
                                     0.055648f, -0.204043f, 1.057311f};

  return mul(XYZ2RGB, XYZ);
}

float4 AvgLuma(float3 color) {
/// Implementation example;
///   color.rgb = AvgLuma(color.rgb).x // or .y or ,z or .w never ever .xyzw!;

  return float4(dot(color, float3(0.2125f, 0.7154f, 0.0721f)),                 /// Perform a weighted average
                max(color.r, max(color.g, color.b)),                       /// Take the maximum value of the incoming value
                max(max(color.x, color.y), color.z),                       /// Compute the luminance component as per the HSL colour space
                sqrt((color.x*color.x*0.2125f)+(color.y*color.y*0.7154f)+(color.z*color.z*0.0721f)));
}

float3 RGB2HCV(in float3 RGB)
{
	RGB = saturate(RGB);
	float Epsilon = 1e-10;
    	// Based on work by Sam Hocevar and Emil Persson
    	float4 P = (RGB.g < RGB.b) ? float4(RGB.bg, -1.0, 2.0/3.0) : float4(RGB.gb, 0.0, -1.0/3.0);
    	float4 Q = (RGB.r < P.x) ? float4(P.xyw, RGB.r) : float4(RGB.r, P.yzx);
    	float C = Q.x - min(Q.w, Q.y);
    	float H = abs((Q.w - Q.y) / (6 * C + Epsilon) + Q.z);
    	return float3(H, C, Q.x);
}

float3 RGB2HSL(in float3 RGB)
{
    	float3 HCV = RGB2HCV(RGB);
    	float L = HCV.z - HCV.y * 0.5;
    	float S = HCV.y / (1.0000001 - abs(L * 2 - 1));
    	return float3(HCV.x, S, L);
}

float3 HSL2RGB(in float3 HSL)
{
	HSL = saturate(HSL);
	//HSL.z *= 0.99;
    	float3 RGB = saturate(float3(abs(HSL.x * 6.0 - 3.0) - 1.0,2.0 - abs(HSL.x * 6.0 - 2.0),2.0 - abs(HSL.x * 6.0 - 4.0)));
    	float C = (1 - abs(2 * HSL.z - 1)) * HSL.y;
    	return (RGB - 0.5) * C + HSL.z;
}

float linearstep(float lower, float upper, float value)
{
    	return saturate((value-lower)/(upper-lower));
}


// and as it wasnt enought... again

float3 RGBToHSL2(float3 color)
{
	float3 hsl; // init to 0 to avoid warnings ? (and reverse if + remove first part)
	
	float fmin = min(min(color.r, color.g), color.b);
	float fmax = max(max(color.r, color.g), color.b);
	float delta = fmax - fmin;

	hsl.z = (fmax + fmin) / 2.0;

	if (delta == 0.0) //No chroma
	{
		hsl.x = 0.0;	// Hue
		hsl.y = 0.0;	// Saturation
	}
	else //Chromatic data
	{
		if (hsl.z < 0.5)
			hsl.y = delta / (fmax + fmin); // Saturation
		else
			hsl.y = delta / (2.0 - fmax - fmin); // Saturation
		
		float deltaR = (((fmax - color.r) / 6.0) + (delta / 2.0)) / delta;
		float deltaG = (((fmax - color.g) / 6.0) + (delta / 2.0)) / delta;
		float deltaB = (((fmax - color.b) / 6.0) + (delta / 2.0)) / delta;

		if (color.r == fmax )
			hsl.x = deltaB - deltaG; // Hue
		else if (color.g == fmax)
			hsl.x = (1.0 / 3.0) + deltaR - deltaB; // Hue
		else if (color.b == fmax)
			hsl.x = (2.0 / 3.0) + deltaG - deltaR; // Hue

		if (hsl.x < 0.0)
			hsl.x += 1.0; // Hue
		else if (hsl.x > 1.0)
			hsl.x -= 1.0; // Hue
	}

	return hsl;
}

float HueToRGB2(float f1, float f2, float hue)
{
	if (hue < 0.0)
		hue += 1.0;
	else if (hue > 1.0)
		hue -= 1.0;
	float res;
	if ((6.0 * hue) < 1.0)
		res = f1 + (f2 - f1) * 6.0 * hue;
	else if ((2.0 * hue) < 1.0)
		res = f2;
	else if ((3.0 * hue) < 2.0)
		res = f1 + (f2 - f1) * ((2.0 / 3.0) - hue) * 6.0;
	else
		res = f1;
	return res;
}

float3 HSLToRGB2(float3 hsl)
{
	float3 rgb;
	
	if (hsl.y == 0.0)
		rgb = float3(hsl.z, hsl.z, hsl.z); // Luminance
	else
	{
		float f2;
		
		if (hsl.z < 0.5)
			f2 = hsl.z * (1.0 + hsl.y);
		else
			f2 = (hsl.z + hsl.y) - (hsl.y * hsl.z);
			
		float f1 = 2.0 * hsl.z - f2;
		
		rgb.r = HueToRGB2(f1, f2, hsl.x + (1.0/3.0));
		rgb.g = HueToRGB2(f1, f2, hsl.x);
		rgb.b= HueToRGB2(f1, f2, hsl.x - (1.0/3.0));
	}
	
	return rgb;
}

// PI, required to calculate weight
static const float PI = 3.1415926535897932384626433832795;

// Luminance Blend
float3 BlendLuma( float3 base, float3 blend )
{
	float3 HSLBase 	= RGBToHSL2( base );
	float3 HSLBlend	= RGBToHSL2( blend );
	return HSLToRGB2( float3( HSLBase.x, HSLBase.y, HSLBlend.z ));
}

// Pseudo Random Number generator. 
float random(in float2 uv)
{
float2 noise = (frac(sin(dot(uv , float2(12.9898,78.233) * 2.0)) * 43758.5453));
return abs(noise.x + noise.y) * 0.5;
}

// Linear depth
float linearDepth(float d, float n, float f)
{
	return (2.0 * n)/(f + n - d * (f - n));
}

//GAUSSIAN WEIGHTS - Linear sampled for high performance
//9 tap reduced to 3 weights ( 17 pixels wide )
static const float sampleOffsets_1[3]   = { 0.0,         1.137453814668,      3.013581103919   };
static const float sampleWeights_1[3]   = { 0.441440131387,   0.277468870531,      0.001811063775   };

//17 tap reduced to 5 weights ( 33 pixels wide )
static const float sampleOffsets_2[5]   = { 0.0,         1.263686497497,      3.083471450524,      5.022636787155,      7.005855649638   };
static const float sampleWeights_2[5]   = { 0.330086281980,   0.318351147970,      0.016540813281,      0.000064880504,      0.000000017255   };

//21 tap reduced to 6 weights ( 41 pixels wide )
static const float sampleOffsets_3[6]   = { 0.0,         1.452313744966,      3.390210239952,      5.331472958797,      7.277552900121,      9.229394260785   };
static const float sampleWeights_3[6]   = { 0.142479385858,   0.244115579374,      0.131636577371,      0.043283482080,      0.008668409765,      0.001056258481   };

float3 softlight(float3 a, float3 b, float s)
{
   float3 ret;
   float3 b_x2 = 2.0 * b;
   float3 a_b_x2 = a * b_x2;
   float3 c1 = a_b_x2 + a * a - a * a_b_x2;
   float3 c2 = sqrt(a) * ( b_x2 - 1.0 ) + 2.0 * a - a_b_x2;
   ret = ( b >= 0.5 ) ? c1 : c2;
   return lerp( a, ret, s );
}

float3 screen(float3 a, float3 b)
{
   return (1.0f - (1.0f - a) * (1.0f - b));
}

float Overlay(float LayerA, float LayerB)
{
	float MinA = min(LayerA, 0.5);
	float MinB = min(LayerB, 0.5);
	float MaxA = max(LayerA, 0.5);
	float MaxB = max(LayerB, 0.5);
	return 2 * (MinA * MinB + MaxA + MaxB - MaxA * MaxB) - 1.5;
}


// ---- end include Shaders/helper.fxh ----
 // Includes Shader Helper //
//======================================================//

//===============//
// VERTEX SHADER //
//===============//
VS_OUTPUT_POST	VS_PostProcess(VS_INPUT_POST IN)
{
	VS_OUTPUT_POST	OUT;
	float4	pos;
	pos.xyz = IN.pos.xyz;
	pos.w = 1.0;
	OUT.pos = pos;
	OUT.txcoord0.xy = IN.txcoord.xy;
	return OUT;
}

// ---- begin include Setup/ShaderSetup.fxh ----
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
// ---- end include Setup/ShaderSetup.fxh ----

// ---- begin include Shaders/TM_Device.fxh ----
/**********************************************************************
 *
 *  Device Curves
 *
 *  s-Log3, sLog3 Gamut3 Cine, sLog3 Gamut3
 *      https://pro.sony.com/bbsccms/assets/files/micro/dmpc/training/TechnicalSummary_for_S-Gamut3Cine_S-Gamut3_S-Log3_V1_01.pdf
 *  s-Log2
 *      https://pro.sony.com/bbsccms/assets/files/micro/dmpc/training/S-Log2_Technical_PaperV1_0.pdf
 *  s-Log
 *      https://pro.sony.com/bbsccms/assets/files/mkt/cinema/solutions/slog_manual.pdf
 *  Cineon
 *      https://github.com/mymei/UE4/blob/master/Engine/Shaders/PostProcessTonemap.usf
 *
 *  input struct:
 *      float3 white;
 *
 *  Function prototype:
 *      float3 TM_sLog3(       float3 linearColor, opt float3 white);
 *      float3 TM_sLog2(       float3 linearColor, opt float3 white);
 *      float3 TM_sLog(        float3 linearColor, opt float3 white);
 *      float3 TM_sGamut3Cine( float3 linearColor, opt float3 white);
 *      float3 TM_sGamut3(     float3 linearColor, opt float3 white);
 *      float3 TM_Cineon(      float3 linearColor, opt float3 white);
 *
 *  Ported to HLSL by kingeric1992 for ENBseries
 *      forum:
 *                                                  update: July.4.2017
 *
 **********************************************************************/
 
#ifndef _TM_DEVICE_FXH_
#define _TM_DEVICE_FXH_

static const float3x3 rec709_2_sGamut3_Cine = {
    0.6456794776, 0.2591145470, 0.0952059754,
    0.0875299915, 0.7596995626, 0.1527704459,
    0.0369574199, 0.1292809048, 0.8337616753 
};
    
static const float3x3 rec709_2_sGamut3 = {
    0.5660490800, 0.3427630873, 0.0911878326,
    0.0769613789, 0.7990545001, 0.1239841210,
    0.0223509133, 0.1086120512, 0.8690370355 
};

struct TM_Device_struct {
    float a, b, c, d;
};

static const TM_Device_struct TM_Device_sLog2 = {
    0.432699, 155.0/219.0, 0.037584, 0.616596
};

static const TM_Device_struct TM_Device_sLog = {
    0.432699, 1.0, 0.037584, 0.616596
};

static const TM_Device_struct TM_Device_Cineon = {
    300.0/1023.0, 1.0-0.0108, 0.0108, 685.0/1023.0
};

static const TM_Device_struct TM_Device_sLog3 = {
    261.5/1023.0, 1.0/0.19, 1.0/19.0, 420.0/1023.0
};

float3 TM_DeviceLog(float3 c, const TM_Device_struct i) {
    return i.a*log10(c*i.b+i.c)+i.d;
}

float3 TM_sLog3( float3 c ) {
    return ( c >= 0.01125000)? TM_DeviceLog(c, TM_Device_sLog3):
           ( c * ( 171.2102946929 - 95.0) + 95.0 / 0.01125000) / 1023.0;
}

float3 TM_sLog2( float3 c ) { 
    return TM_DeviceLog(c, TM_Device_sLog2);
}

float3 TM_sLog( float3 c ) {
    return TM_DeviceLog(c, TM_Device_sLog);
}

float3 TM_sGamut3Cine( float3 c ) { 
    return TM_sLog3( mul(rec709_2_sGamut3_Cine, c));
}

float3 TM_sGamut3( float3 c ) { 
    return TM_sLog3( mul(rec709_2_sGamut3, c));
}

float3 TM_Cineon( float3 c ) {
    return TM_DeviceLog(c, TM_Device_Cineon);
}


/**********************************************************************
 *
 *  Function Overload
 *
 **********************************************************************/

float3 TM_sLog3( float3 c, const float3 w ) {
    return (( c/w >= 0.01125000)? TM_DeviceLog(c, TM_Device_sLog3):
            ( c * ( 171.2102946929 - 95.0) + 95.0 / 0.01125000) / 1023.0 ) /
                                  TM_DeviceLog(w, TM_Device_sLog3);
}

float3 TM_sLog2( float3 c, const float3 w ) { 
    return TM_DeviceLog(c, TM_Device_sLog2)/TM_DeviceLog(w, TM_Device_sLog2);
}

float3 TM_sLog( float3 c, const float3 w )  {
    return TM_DeviceLog(c, TM_Device_sLog)/TM_DeviceLog(w, TM_Device_sLog);
}

float3 TM_sGamut3Cine( float3 c, const float3 w ) { 
    return TM_sLog3( mul(rec709_2_sGamut3_Cine, c), w);
}

float3 TM_sGamut3( float3 c, const float3 w ) { 
    return TM_sLog3( mul(rec709_2_sGamut3, c), w);
}

float3 TM_Cineon( float3 c, const float3 w ) {
    return TM_DeviceLog(c, TM_Device_Cineon)/TM_DeviceLog(w, TM_Device_Cineon);
}

#endif //_TM_DEVICE_FXH_
// ---- end include Shaders/TM_Device.fxh ----

// ---- begin include Shaders/TM_Lin2Log.fxh ----
/**********************************************************************
 *
 *  Linear to Log 
 *
 *  https://github.com/mymei/UE4/blob/master/Engine/Shaders/PostProcessTonemap.usf
 *
 *  input struct:
 *      struct TM_Lin2Log_struct {
 *          float range;
 *          float grey;
 *          float exposureGrey;
 *  };
 *
 *  Function prototype:
 *      float3 res = TM_Lin2Log( float3 linearColor, 
 *                                TM_Lin2Log_struct params = TM_Lin2Log_Default);
 *
 *  Ported to HLSL by kingeric1992 for ENBseries
 *      forum:
 *                                                  update: July.4.2017
 *
 **********************************************************************/ 

#ifndef _TM_LIN2LOG_FXH_
#define _TM_LIN2LOG_FXH_ 

struct TM_Lin2Log_struct {
    float range, grey, exposureGrey;
};
 
static const TM_Lin2Log_struct TM_Lin2Log_Default = {
    14.0, 0.18, 444.0
};
 
float3 TM_Lin2Log( float3 c, const TM_Lin2Log_struct i = TM_Lin2Log_Default ) {
	return log2( c / i.grey ) / i.range + i.exposureGrey / 1023.0;
}

#endif //_TM_LIN2LOG_FXH_ 
// ---- end include Shaders/TM_Lin2Log.fxh ----

// ---- begin include Shaders/LUT.fxh ----
//==========================//
// LUT code by kingeric1992 //
//==========================//

static const float2 Lut_Size256 = float2(256.0, 16.0);

float3 Lut256( float3 colorIN, Texture2D lutTexIn ) {
    float2 CLut_pSize = 1.0 / Lut_Size256;
    float4 CLut_UV;
    colorIN    = saturate(colorIN) * ( Lut_Size256.y - 1.0);
    CLut_UV.w  = floor(colorIN.b);
    CLut_UV.xy = (colorIN.rg + 0.5) * CLut_pSize;
    CLut_UV.x += CLut_UV.w * CLut_pSize.y;
    CLut_UV.z  = CLut_UV.x + CLut_pSize.y;
    return       lerp (lutTexIn.SampleLevel(Sampler1, CLut_UV.xy, 0).rgb, 
                       lutTexIn.SampleLevel(Sampler1, CLut_UV.zy, 0).rgb, colorIN.b - CLut_UV.w);
}


static const float2 Lut_Size1024 = float2(1024.0, 32.0);

float3 Lut1024( float3 colorIN, Texture2D lutTexIn ) {
    float2 CLut_pSize = 1.0 / Lut_Size1024;
    float4 CLut_UV;
    colorIN    = saturate(colorIN) * ( Lut_Size1024.y - 1.0);
    CLut_UV.w  = floor(colorIN.b);
    CLut_UV.xy = (colorIN.rg + 0.5) * CLut_pSize;
    CLut_UV.x += CLut_UV.w * CLut_pSize.y;
    CLut_UV.z  = CLut_UV.x + CLut_pSize.y;
    return       lerp (lutTexIn.SampleLevel(Sampler1, CLut_UV.xy, 0).rgb, 
                       lutTexIn.SampleLevel(Sampler1, CLut_UV.zy, 0).rgb, colorIN.b - CLut_UV.w);
}


static const float2 Lut_Size4096 = float2(4096.0, 64.0);

float3 Lut4096( float3 colorIN, Texture2D lutTexIn ) {
    float2 CLut_pSize = 1.0 / Lut_Size4096;
    float4 CLut_UV;
    colorIN    = saturate(colorIN) * ( Lut_Size4096.y - 1.0);
    CLut_UV.w  = floor(colorIN.b);
    CLut_UV.xy = (colorIN.rg + 0.5) * CLut_pSize;
    CLut_UV.x += CLut_UV.w * CLut_pSize.y;
    CLut_UV.z  = CLut_UV.x + CLut_pSize.y;
    return       lerp (lutTexIn.SampleLevel(Sampler1, CLut_UV.xy, 0).rgb, 
                       lutTexIn.SampleLevel(Sampler1, CLut_UV.zy, 0).rgb, colorIN.b - CLut_UV.w);
}
// ---- end include Shaders/LUT.fxh ----

// ---- begin include Setup/LUTSetup.fxh ----
//===============================================================================================//
// Based on kingeric1992,s work here: http://enbseries.enbdev.com/forum/viewtopic.php?f=7&t=4394 //
// Description and Presetup by Adyss                                                             //
//===============================================================================================//

/*
What is a LUT?
A LUT (Lookup Table) is basically a color palette that tells colors what to do. Neutral LUTs in diffrent sizes can be found in LUT folder.

How do i use a LUT?
Basically you take a screenshot and alter it in Photoshop or any other programm (i use Magic Bullet) to your likeing.
You can only change colors on it. No grain or else
After you have your screenshot set you take the LUT.bmp (or .png) and load it into your ENB (look below) The changes you made will now appear ingame.


=============================================== Load LUTs in your ENB =======================================================

 | First annonce that its a texture |     | Give your lut a codename |        |   Give the path to your LUT file         |
 |            Texture2D             |     |          LUTxy           |        |  <string ResourceName="LUT/LUT.bmp"; >;  |
 
	example:
	Texture2D LOGtoREC          <string ResourceName="LUT/LOGtoREC.bmp"; >;  

=============================================== Apply your loaded LUTs ======================================================
 
Depending on the size of the lut you loaded you will need a diffrent function to apply it
available lut sizes are:       256x16      1024x32      4096x64
functions for these are:       Lut256      Lut1024      Lut4096

| what you alter with lut (don't change) |    | Size of your LUT |   | necessary step for the code |    | Name you gave the lut you loaded and want to apply |
|            color.rgb =                 |    |      Lut256      |   |         (color.rgb,         |    |                     LUTxy);                        |

	example:
	color.rgb = Lut4096(color.rgb, LOGtoREC);
	
	In case you want seperate luts for each daytime you will need to load 3 luts. Apply them by doing:
    color.rgb = lerp(lerp(Lut256(color.rgb, LUTxy_Night), 
                          Lut256(color.rgb, LUTxy_Day),      ENightDayFactor),
                          Lut256(color.rgb, LUTxy_Interior), EInteriorFactor);
|

	Usefull Info:
	it doesnt matter what format the luts are in. Tho i only tested .bmp and .png yet.
	The bigger the LUT the more precise will your colorchanges be applied. 1024 should be enough in most cases. (4096 is a bit overkill lol)
	You  cant have the same LUTname twice without getting a compiler error.

	
=============================================== Integrade Switchweel ======================================================== 

This little tool makes it possible to switch LUTs ingame on the fly. 
Baically you do: 


| and if statement with the nr you have to chose ingame to apply it |   | Your lut function (and log if wanted)  |   | another  } to end the if statement |
|                       if (LUTSelect==1) {                         |   | color.rgb = Lut4096(color.rgb, LUTxy); |   |                }                   |

	example:
	if (LUTSelect==1) { color.rgb = Lut4096(color.rgb, LUTxy); }
	
	if (LUTSelect==2) { color.rgb = TM_Lin2Log(color.rgb);     color.rgb = Lut4096(color.rgb, LOGtoREC);  }


*/

#define USE_LUTweel  1                 // Set to 0 if you dont want to have selectable luts
#define weelname     "Select LUT"      // Decide what the weel shall be called. Dont remove the "  "
#define LUTcounter   3                 // Select the Nr. of LUTs that you want to have selectable

// ---- begin include Shaders/PostUI.fxh ----

// Ady: i found it more clean to have all the UI in an external file

float empty62 < string UIName = "|==== Global Settings ====|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

#if (USE_LUTweel==1)
float LUTSelect           <string UIName= weelname ;                              string UIWidget="Spinner";  float UIMin=0.0;  float UIMax=LUTcounter;   float UIStep=1;   > = {0.0};
#endif

float ExposureGOB         <string UIName="Global Brightness";                     string UIWidget="Spinner";  float UIMin=-3.0;  float UIMax=4.0;   float UIStep=0.1;   > = {0.0};
float GlobalTemperature   <string UIName="Global Temperature";		              string UIWidget="Spinner";  float UIMin=-0.15; float UIMax=0.15;	float UIStep=0.01;  > = {0.0};
bool  LIFTNAO             <string UIName="Lift Shadows";                                                                                                                > = {false};
bool  DROPNAO             <string UIName="Drop Shadows";                                                                                                                > = {false};



#if (INC_FishEye==1)
bool USE_FISH < string UIName = "Use Fisheye"; > = {false}; 

float	iFisheyeMod
<
	string UIName="Fisheye Mode";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=3.0;
	float UIStep=1.0;
> = {0.0};

float	fFisheyeZoom
<
	string UIName="Fisheye Zoom";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=1.0;
> = {0.55};

float	fFisheyeDistortion
<
	string UIName="Fisheye Distortion";
	string UIWidget="spinner";
	float UIMin=-0.300;
	float UIMax=0.300;
	float UIStep=0.01;
> = {0.01};

float	fFisheyeDistortionCubic
<
	string UIName="Fisheye Distortion Cube";
	string UIWidget="spinner";
	float UIMin=-0.300;
	float UIMax=0.300;
	float UIStep=0.01;
> = {0.7};

float	fFisheyeColorshift
<
	string UIName="Fisheye Colorshift";
	string UIWidget="spinner";
	float UIMin=-0.10;
	float UIMax=0.10;
	float UIStep=0.01;
> = {0.002};
#endif

#if (INC_Emboss==1)
bool USE_Emboss < string UIName = "Use Emboss"; > = {false}; 

float	fEmbossPower
<
	string UIName="Emboss Power";
	string UIWidget="spinner";
	float UIMin=0.01;
	float UIMax=2.0;
> = {0.150};

float	fEmbossOffset
<
	string UIName="Emboss Offset";
	string UIWidget="spinner";
	float UIMin=0.1;
	float UIMax=5.0;
> = {1.00};

float	iEmbossAngle
<
	string UIName="Emboss Angle";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=360.0;
	float UIStep=1.0;
> = {90.0};
#endif

#if (INC_Letterbox==1)
bool ENABLE_LETTERBOX        < string UIName = "|=== Toggle Letterbox ===|";> = {false};

float2	border_width
<
	string UIName="Letterbox Position - ";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.0, 1.0};

#define	border_ratio 1 // Supposed to be in UI but not working

float3	border_color
<
	string UIName = "Letterbox Color";
	string UIWidget = "color";
> = {0.0, 0.0, 0.0};
#endif



float empty2 < string UIName = "|=======Toggles=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
#if (INC_HDR==1)
bool USE_HDR < string UIName = "Use HDR"; > = {false};
#endif
#if (INC_Vibrance==1)
bool USE_Vibrance < string UIName = "Use Vibrance"; > = {false};
#endif
#if (INC_DPX==1)
bool USE_DPX < string UIName = "Use DPX"; > = {false};
#endif
#if (INC_Curves==1)
bool USE_Curves < string UIName = "Use Curves"; > = {false};
#endif
#if (INC_Reinhard==1)
bool USE_Reinhard < string UIName = "Use Reinhard"; > = {false};
#endif
#if (INC_Reinhard==2)
bool USE_Reinhard < string UIName = "Use Reinhard"; > = {false};
#endif
#if (INC_Filmpass==1)
bool USE_Filmpass < string UIName = "Use Filmpass"; > = {false};
#endif
#if (INC_Spherical==1)
bool USE_Spherical < string UIName="Use Spherical "; > = {false};
#endif
#if (INC_Tint==1)
bool use_tinting < string UIName = "Use Tinting"; > = {false};
#endif
#if (INC_Technicolor==1)
bool use_technicolor < string UIName="Use Technicolor"; > = {false};
#endif
#if (INC_Technicolor2==1)
bool use_t2s < string UIName="Use Technicolor 2 Strip"; > = {false};
#endif
#if (INC_Lightroom==1)
bool USE_Lightroom < string UIName="Use Lightroom "; > = {false};
#endif
#if (INC_LumaSHARP==1)
bool USE_LumaSharp < string UIName = "Use Luma Sharp"; > = {false};
#endif
#if (INC_Shadow==1)
bool USE_Shadows < string UIName = "Use Shadow Adjustments"; > = {false};
#endif
#if (INC_SBloom==1)
bool  USE_SBloom             <string UIName="Sweet Bloom"; > = {false};
#endif

bool ENABLE_DITHER < string UIName = "Enable Dither";   > = {false};


#if (INC_GaussBloom==1)
bool  USE_GaussBloom      <string UIName="Gaussian Bloom"; > = {false};

bool lumabloom <
   string UIName="Luma based Bloom";
> = {true};


float lumasource <
   string UIName="Luma Src 1_orig | 2_softlight | 3_blend";
   string UIWidget="Spinner";
   float UIMin=1;
   float UIMax=3;
   float UIStep=1;
> = {2};
float gauss_blur <
   string UIName="Gaussian Blur Strength";
   string UIWidget="Spinner";
   float UIMin=1;
   float UIMax=3;
   float UIStep=1;
> = {2};
#endif


float empty6 < string UIName = "|===== Sharp Settings =====|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
#if (INC_LumaSHARP==1)
float	LSharpStrength
<
	string UIName="LS: Sharp Strength";
	string UIWidget="spinner";
	float UIMin=0.10;
	float UIMax=3.00;
> = {0.70};

float	LSharpClamp
<
	string UIName="LS: Sharp Clamp";
	string UIWidget="spinner";
	float UIMin=0.000;
	float UIMax=1.000;
> = {0.035};

int		LSharpPattern
<
	string UIName="LS: Sharp Pattern";
	string UIWidget="spinner";
	float UIMin=0;
	float UIMax=3;
> = {2};

float	LSharpOffsetBias
<
	string UIName="LS: Offset Bias";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=6.0;
> = {1.0};
#endif
/*
bool shader_off <
	string UIName="Show Original";
> = {false};
bool show_edges <
	string UIName="Show Edges";
> = {false};
bool smooth_edges <
	string UIName="Use Edge Smoothing";
> = {true};
float smooth <
	string UIName="Edge Smoothing Intensity";
	string UIWidget="Spinner";
	float UIMin=0.3;
	float UIMax=1;
	float UIStep=0.001;
> = {0.52};
float farDepth <
	string UIName="Depth Sharpening: Far Depth";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=100000.0;
	float UIStep=0.1;
> = {100.0};
float limiterE <
	string UIName="Sharpening HL Limiter Exterior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=1;
	float UIStep=0.001;
> = {0.1};
float limiterI <
	string UIName="Sharpening HL Limiter Interior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=1;
	float UIStep=0.001;
> = {0.1};
bool luma_sharpen <
	string UIName="Use Luma Sharpen";
> = {true};
float BlurSigmaE <
	string UIName="Blur Sigma Exterior";
	string UIWidget="Spinner";
	float UIMin=0.3;
	float UIMax=2;
	float UIStep=0.001;
> = {0.87};
float BlurSigmaI <
	string UIName="Blur Sigma Interior";
	string UIWidget="Spinner";
	float UIMin=0.3;
	float UIMax=2;
	float UIStep=0.001;
> = {0.98};
float SharpeningE <
	string UIName="Sharpening Strength Exterior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=5;
	float UIStep=0.001;
> = {1.67};
float SharpeningI <
	string UIName="Sharpening Strength Interior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=5;
	float UIStep=0.001;
> = {1.87};
float ThresholdE <
	string UIName="Sharpening Threshold Exterior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=255;
	float UIStep=1;
> = {1};
float ThresholdI <
	string UIName="Sharpening Threshold Interior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=255;
	float UIStep=1;
> = {0};
*/

#if (INC_FilmicAnamorphSharp==1)
float FASStrength <
	string UIName="Sharpen strength";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=3.0;
	float UIStep=0.005;
> = {1.0};

float FASClamp <
	string UIName="Sharpen clamping";
	string UIWidget="Spinner";
	float UIMin=0.5;
	float UIMax=1.0;
	float UIStep=0.001;
> = {1.0};

float FASOffset <
	string UIName="High-pass cross offset in pixels";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=2;
	float UIStep=1;
> = {1};

float FASContrast <
	string UIName="Depth high-pass mask amount";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=2000.0;
	float UIStep=1.0;
> = {128.0};
#endif

#if (INC_BasicSharp==1)
float	ESharpAmount
<
	string UIName="Sharp:: amount";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=4.0;
> = {1.0};

float	ESharpRange
<
	string UIName="Sharp:: range";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};
#endif

float empty7 < string UIName = "|===== Day =====|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
#if (INC_DPX==1)
float empty8 < string UIName = "|===== DPX Day =====|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	RGB_Curve_Day
<
	string UIName="DPX: RGB Curve Day";
	string UIWidget="Slider";
	float UIMin=0.0;
	float UIMax=16.0;
> = {8.0};

float	RGB_C_Day
<
	string UIName="DPX: RGB C Day";
	string UIWidget="Slider";
	float UIMin=0.2;
	float UIMax=0.5;
> = {0.36};

float	ContrastDPX_Day
<
	string UIName="DPX: Contrast Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.1};

float	SaturationDPX_Day
<
	string UIName="DPX: Saturation Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {3.0};

float	ColorfulnessDPX_Day
<
	string UIName="DPX: Colorfulness Day";
	string UIWidget="spinner";
	float UIMin=0.1;
	float UIMax=2.5;
> = {2.5};

float	StrengthDPX_Day
<
	string UIName="DPX: Strength Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.20};
#endif

#if (INC_Reinhard==1)
float empty9 < string UIName = "|=======Linear Reinhard Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	ReinhardLinearSlope_Day
<
	string UIName="RH: Linear Slope Day";
	string UIWidget="spinner";
	float UIMin=1.0;
	float UIMax=5.0;
> = {1.25};

float	ReinhardLinearWhitepoint_Day
<
	string UIName="RH: White Point Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=20.0;
> = {7.25};

float	ReinhardLinearPoint_Day
<
	string UIName="RH: Linear Point Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.15};
#endif
#if (INC_Reinhard==2)
float empty46 < string UIName = "|=======Reinhard Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	ReinhardWhitepoint_Day
<
	string UIName="RH: White Point Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=10.0;
> = {1.25};

float	ReinhardScale_Day
<
	string UIName="RH: Scale Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=3.0;
> = {0.5};
#endif


#if (INC_Vibrance==1)
float empty11 < string UIName = "|=======Vibrance Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Vibrance_Day <
   string UIName="Vibrance Day";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.15};

float3	VibranceRGBBalance_Day
<
	string UIName = "RGB Vibrance Day";
	string UIWidget = "color";
    float UIMin=-10.0;
    float UIMax=10.0;
> = {1.0, 1.0, 1.0};
#endif

#if (INC_Curves==1)
float empty12 < string UIName = "|=======Curves Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Mode_Day <
   string UIName="Curve Mode Day";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=2.0;
   float UIStep=1.0;
> = {0.0};

float Formula_Day <
   string UIName="Curve Formula Day";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=10.0;
   float UIStep=1.0;
> = {4.0};

float Contrast_Day <
   string UIName="Curves Blend Day";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.65};
#endif

#if (INC_HDR==1)
float empty13 < string UIName = "|=======HDR Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float HDRPower_Day <
   string UIName="HDR Power Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {1.3};

float radius1_Day <
   string UIName="Radius 1 Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.79};

float radius2_Day <
   string UIName="Radius 2 Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.87};
#endif

#if (INC_Filmpass==1)
float empty14 < string UIName = "|=======Filmpass Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	FPStrength_Day
<
	string UIName="FP: Strength Day";
	string UIWidget="spinner";
	float UIMin=0.05;
	float UIMax=1.5;
> = {0.85};

float	FPFade_Day
<
	string UIName="FP: Fade Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=0.6;
> = {0.4};

float	FPContrast_Day
<
	string UIName="FP: Contrast Day";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {1.0};

float	Linearization_Day
<
	string UIName="FP: Linearization Day";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {0.5};

float	FPBleach_Day
<
	string UIName="FP: Bleach Day";
	string UIWidget="spinner";
	float UIMin=-0.5;
	float UIMax=1.0;
> = {0.0};

float	FPSaturation_Day
<
	string UIName="FP: Saturation Day";
	string UIWidget="spinner";
	float UIMin=-1.0;
	float UIMax=1.0;
> = {-0.15};

float	RedCurve_Day
<
	string UIName="FP: Red Curve Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	GreenCurve_Day
<
	string UIName="FP: Green Curve Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BlueCurve_Day
<
	string UIName="FP: Blue Curve Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BaseCurve_Day
<
	string UIName="FP: Base Curve Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.5};

float	BaseGamma_Day
<
	string UIName="FP: Base Gamma Day";
	string UIWidget="spinner";
	float UIMin=0.7;
	float UIMax=2.0;
> = {1.0};

float	EffectGamma_Day
<
	string UIName="FP: Effect Gamma Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.65};

float	EffectGammaR_Day
<
	string UIName="FP Effect Gamma Red Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaG_Day
<
	string UIName="FP Effect Gamma Green Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaB_Day
<
	string UIName="FP Effect Gamma Blue Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};
#endif

#if (INC_Spherical==1)
float empty15 < string UIName = "|=======Spherical Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	sphericalAmount_Day
<
	string UIName="Spherical Amount Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.5};
#endif

#if (INC_Tint==1)
float empty35 < string UIName = "|=======Tinting Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 RGB_TintD <
   string UIName="Tint Color Day";
   string UIWidget="Color";
> = {0.725, 0.431, 0.118};
float HighlightPowerD <
   string UIName="Highlight Color Power Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float TintPowerD <
   string UIName="Tint Color Power Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowPowerD <
   string UIName="Shadow Color Power Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowStrD <
   string UIName="Add Shadow Color Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float SHueAdjustD <
   string UIName="Shift Shadow Hue Day";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatShadowsD <
   string UIName="Desaturate Shadows Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatMidsD <
   string UIName="Desaturate Midtones Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatOrigD <
   string UIName="Desaturate Original Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float3 TonedD <
   string UIName="Effect Strength Day";
   string UIWidget="Color";
> = {0.314, 0.314, 0.314};
#endif

#if (INC_Technicolor==1)
float empty38 < string UIName = "|=======Techicolor Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 colStrengthD <
   string UIName="Technicolor Color Strength Day";
   string UIWidget="Color";
> = {0.5, 0.5, 0.5};
float brightnessD <
   string UIName="Technicolor Brightness Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrengthD <
   string UIName="Technicolor Amount Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Technicolor2==1)
float empty43 < string UIName = "|=======Techicolor 2 Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 rChannelD <
   string UIName="Technicolor 2s Red Day";
   string UIWidget="Color";
> = {1, 0.165, 0};
float3 gChannelD <
   string UIName="Technicolor 2s Green Day";
   string UIWidget="Color";
> = {0.294, 1, 0};
float3 bChannelD <
   string UIName="Technicolor 2s Blue Day";
   string UIWidget="Color";
> = {0.0588, 0.902, 0};
float strip2vibD <
   string UIName="Technicolor 2s Saturation Boost Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrength2D <
   string UIName="Technicolor 2s Amount Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Shadow==1)
float empty54 < string UIName = "|=======Shadows Day=======<"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ECCGamma_Day
<
	string UIName="Gamma Day";
	string UIWidget="Spinner";
	float UIMin=0.2;
	float UIMax=5.0;
> = {1.0};

float	ECCInBlack_Day
<
	string UIName="In black Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCInWhite_Day
<
	string UIName="In white Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCOutBlack_Day
<
	string UIName="Out black Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCOutWhite_Day
<
	string UIName="Out white Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCDesaturateShadows_Day
<
	string UIName="Desaturate shadows Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	LightnessD <		string UIName="Highlights Day";							string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};
float	ShadowsD <			string UIName="Shadows Day";								string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};

#endif

#if (INC_SBloom==1)
float empty56 < string UIName = "|=======Sweet Bloom Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	BloomThreshold_Day
<
	string UIName="SBloom Threshold Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=50.0;
> = {20.25};

float	BloomPower_Day
<
	string UIName="SBloom Power Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {1.44};

float	BloomWidth_Day
<
	string UIName="SBloom Width Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
	float UIStep=0.0001;
> = {0.0142};
#endif


#if (INC_GaussBloom==1)
float empty59 < string UIName = "|=======Gaussian Bloom Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float sl_mix_set_Day <
   string UIName="Soft Light Intensity Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.275};

float gauss_bloom_Day <
   string UIName="Gaussian Bloom Intensity Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.550};
#endif

float empty16 < string UIName = "|=========NIGHT=========|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
#if (INC_DPX==1)
float empty17 < string UIName = "|=======DPX Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	RGB_Curve_Night
<
	string UIName="DPX: RGB Curve Night";
	string UIWidget="Slider";
	float UIMin=0.0;
	float UIMax=16.0;
> = {8.0};

float	RGB_C_Night
<
	string UIName="DPX: RGB C Night";
	string UIWidget="Slider";
	float UIMin=0.2;
	float UIMax=0.5;
> = {0.36};

float	ContrastDPX_Night
<
	string UIName="DPX: Contrast Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.1};

float	SaturationDPX_Night
<
	string UIName="DPX: Saturation Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {3.0};

float	ColorfulnessDPX_Night
<
	string UIName="DPX: Colorfulness Night";
	string UIWidget="spinner";
	float UIMin=0.1;
	float UIMax=2.5;
> = {2.5};

float	StrengthDPX_Night
<
	string UIName="DPX: Strength Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.20};
#endif


#if (INC_Reinhard==1)
float empty18 < string UIName = "|=======Reinhard Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ReinhardLinearSlope_Night
<
	string UIName="RH: Linear Slope Night";
	string UIWidget="spinner";
	float UIMin=1.0;
	float UIMax=5.0;
> = {1.25};

float	ReinhardLinearWhitepoint_Night
<
	string UIName="RH: White Point Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=20.0;
> = {7.25};

float	ReinhardLinearPoint_Night
<
	string UIName="RH: Linear Point Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.15};
#endif

#if (INC_Reinhard==2)
float empty47 < string UIName = "|=======Reinhard Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ReinhardWhitepoint_Night
<
	string UIName="RH: White Point Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=10.0;
> = {1.25};

float	ReinhardScale_Night
<
	string UIName="RH: Scale Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=3.0;
> = {0.5};
#endif


#if (INC_Vibrance==1)
float empty20 < string UIName = "|=======Vibrance Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Vibrance_Night <
   string UIName="Vibrance Night";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.15};

float3	VibranceRGBBalance_Night
<
	string UIName = "RGB Vibrance Night";
	string UIWidget = "color";
    float UIMin=-10.0;
    float UIMax=10.0;
> = {1.0, 1.0, 1.0};
#endif

#if (INC_Curves==1)
float empty21 < string UIName = "|=======Curves Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Mode_Night <
   string UIName="Curve Mode Night";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=2.0;
   float UIStep=1.0;
> = {0.0};

float Formula_Night <
   string UIName="Curve Formula Night";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=10.0;
   float UIStep=1.0;
> = {4.0};

float Contrast_Night <
   string UIName="Curves Blend Night";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.65};
#endif

#if (INC_HDR==1)
float empty22 < string UIName = "|=======HDR Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float HDRPower_Night <
   string UIName="HDR Power Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {1.3};

float radius1_Night <
   string UIName="Radius 1 Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.79};

float radius2_Night <
   string UIName="Radius 2 Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.87};
#endif

#if (INC_Filmpass==1)
float empty23 < string UIName = "|=======Filmpass Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	FPStrength_Night
<
	string UIName="FP: Strength Night";
	string UIWidget="spinner";
	float UIMin=0.05;
	float UIMax=1.5;
> = {0.85};

float	FPFade_Night
<
	string UIName="FP: Fade Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=0.6;
> = {0.4};

float	FPContrast_Night
<
	string UIName="FP: Contrast Night";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {1.0};

float	Linearization_Night
<
	string UIName="FP: Linearization Night";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {0.5};

float	FPBleach_Night
<
	string UIName="FP: Bleach Night";
	string UIWidget="spinner";
	float UIMin=-0.5;
	float UIMax=1.0;
> = {0.0};

float	FPSaturation_Night
<
	string UIName="FP Saturation Night";
	string UIWidget="spinner";
	float UIMin=-1.0;
	float UIMax=1.0;
> = {-0.15};

float	RedCurve_Night
<
	string UIName="FP: Red Curve Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	GreenCurve_Night
<
	string UIName="FP: Green Curve Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BlueCurve_Night
<
	string UIName="FP: Blue Curve Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BaseCurve_Night
<
	string UIName="FP: Base Curve Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.5};

float	BaseGamma_Night
<
	string UIName="FP: Base Gamma Night";
	string UIWidget="spinner";
	float UIMin=0.7;
	float UIMax=2.0;
> = {1.0};

float	EffectGamma_Night
<
	string UIName="FP: Effect Gamma Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.65};

float	EffectGammaR_Night
<
	string UIName="FP Effect Gamma Red Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaG_Night
<
	string UIName="FP Effect Gamma Green Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaB_Night
<
	string UIName="FP Effect Gamma Blue Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};
#endif

#if (INC_Spherical==1)
float empty24 < string UIName = "|=======Spherical Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	sphericalAmount_Night
<
	string UIName="Spherical Amount Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.5};
#endif

#if (INC_Tint==1)
float empty36 < string UIName = "|=======Tinting Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 RGB_TintN <
   string UIName="Tint Color Night";
   string UIWidget="Color";
> = {0.725, 0.431, 0.118};
float HighlightPowerN <
   string UIName="Highlight Color Power Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float TintPowerN <
   string UIName="Tint Color Power Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowPowerN <
   string UIName="Shadow Color Power Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowStrN <
   string UIName="Add Shadow Color Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float SHueAdjustN <
   string UIName="Shift Shadow Hue Night";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatShadowsN <
   string UIName="Desaturate Shadows Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatMidsN <
   string UIName="Desaturate Midtones Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatOrigN <
   string UIName="Desaturate Original Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float3 TonedN <
   string UIName="Effect Strength Night";
   string UIWidget="Color";
> = {0.314, 0.314, 0.314};
#endif

#if (INC_Technicolor==1)
float empty26 < string UIName = "|=======Techicolor Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 colStrengthN <
   string UIName="Technicolor Color Strength Night";
   string UIWidget="Color";
> = {0.5, 0.5, 0.5};
float brightnessN <
   string UIName="Technicolor Brightness Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrengthN <
   string UIName="Technicolor Amount Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Technicolor2==1)
float empty44 < string UIName = "|=======Techicolor 2 Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 rChannelN <
   string UIName="Technicolor 2s Red Night";
   string UIWidget="Color";
> = {1, 0.165, 0};
float3 gChannelN <
   string UIName="Technicolor 2s Green Night";
   string UIWidget="Color";
> = {0.294, 1, 0};
float3 bChannelN <
   string UIName="Technicolor 2s Blue Night";
   string UIWidget="Color";
> = {0.0588, 0.902, 0};
float strip2vibN <
   string UIName="Technicolor 2s Saturation Boost Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrength2N <
   string UIName="Technicolor 2s Amount Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Shadow==1)
float empty53 < string UIName = "|=======Shadows Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ECCGamma_Night
<
	string UIName="Gamma Night";
	string UIWidget="Spinner";
	float UIMin=0.2;
	float UIMax=5.0;
> = {1.0};

float	ECCInBlack_Night
<
	string UIName="In black Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCInWhite_Night
<
	string UIName="In white Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCOutBlack_Night
<
	string UIName="Out black Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCOutWhite_Night
<
	string UIName="Out white Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCDesaturateShadows_Night
<
	string UIName="Desaturate shadows Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	LightnessN <		string UIName="Highlights Night";							string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};
float	ShadowsN <			string UIName="Shadows Night";								string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};

#endif

#if (INC_SBloom==1)
float empty57 < string UIName = "|=======Sweet Bloom Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	BloomThreshold_Night
<
	string UIName="SBloom Threshold Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=50.0;
> = {20.25};

float	BloomPower_Night
<
	string UIName="SBloom Power Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {1.44};

float	BloomWidth_Night
<
	string UIName="SBloom Width Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
	float UIStep=0.0001;
> = {0.0142};
#endif

#if (INC_GaussBloom==1)
float empty60 < string UIName = "|=======Gaussian Bloom Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float sl_mix_set_Night <
   string UIName="Soft Light Intensity Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.275};

float gauss_bloom_Night <
   string UIName="Gaussian Bloom Intensity Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.550};
#endif

float empty25 < string UIName = "|=========INTERIOR=========|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

#if (INC_DPX==1)
float empty42 < string UIName = "|=======DPX Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	RGB_Curve_Interior
<
	string UIName="DPX: RGB Curve Interior";
	string UIWidget="Slider";
	float UIMin=0.0;
	float UIMax=16.0;
> = {8.0};

float	RGB_C_Interior
<
	string UIName="DPX: RGB C Interior";
	string UIWidget="Slider";
	float UIMin=0.2;
	float UIMax=0.5;
> = {0.36};

float	ContrastDPX_Interior
<
	string UIName="DPX: Contrast Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.1};

float	SaturationDPX_Interior
<
	string UIName="DPX: Saturation Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {3.0};

float	ColorfulnessDPX_Interior
<
	string UIName="DPX: Colorfulness Interior";
	string UIWidget="spinner";
	float UIMin=0.1;
	float UIMax=2.5;
> = {2.5};

float	StrengthDPX_Interior
<
	string UIName="DPX: Strength Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.20};
#endif
#if (INC_Reinhard==1)
float empty41 < string UIName = "|=======Linear Reinhard Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	ReinhardLinearSlope_Interior
<
	string UIName="RH: Linear Slope Interior";
	string UIWidget="spinner";
	float UIMin=1.0;
	float UIMax=5.0;
> = {1.25};

float	ReinhardLinearWhitepoint_Interior
<
	string UIName="RH: White Point Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=20.0;
> = {7.25};

float	ReinhardLinearPoint_Interior
<
	string UIName="RH: Linear Point Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.15};
#endif
#if (INC_Reinhard==2)
float empty48 < string UIName = "|======Reinhard Interior======="; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ReinhardWhitepoint_Interior
<
	string UIName="RH: White Point Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=10.0;
> = {1.25};

float	ReinhardScale_Interior
<
	string UIName="RH: Scale Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=3.0;
> = {0.5};
#endif


#if (INC_Vibrance==1)
float empty29 < string UIName = "|======Vibrance Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Vibrance_Interior <
   string UIName="Vibrance Interior";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.15};

float3	VibranceRGBBalance_Interior
<
	string UIName = "RGB Vibrance Interior";
	string UIWidget = "color";
    float UIMin=-10.0;
    float UIMax=10.0;
> = {1.0, 1.0, 1.0};
#endif

#if (INC_Curves==1)
float empty30 < string UIName = "|======Curves Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Mode_Interior <
   string UIName="Curve Mode Interior";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=2.0;
   float UIStep=1.0;
> = {0.0};

float Formula_Interior <
   string UIName="Curve Formula Interior";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=10.0;
   float UIStep=1.0;
> = {4.0};

float Contrast_Interior <
   string UIName="Curves Interior";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.65};
#endif

#if (INC_HDR==1)
float empty31 < string UIName = "|======HDR Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float HDRPower_Interior <
   string UIName="HDR Power Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {1.3};

float radius1_Interior <
   string UIName="Radius 1 Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.79};

float radius2_Interior <
   string UIName="Radius 2 Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.87};
#endif

#if (INC_Filmpass==1)
float empty32 < string UIName = "|=======Filmpass Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	FPStrength_Interior
<
	string UIName="FP: Strength Interior";
	string UIWidget="spinner";
	float UIMin=0.05;
	float UIMax=1.5;
> = {0.85};

float	FPFade_Interior
<
	string UIName="FP: Fade Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=0.6;
> = {0.4};

float	FPContrast_Interior
<
	string UIName="FP: Contrast Interior";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {1.0};

float	Linearization_Interior
<
	string UIName="FP: Linearization Interior";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {0.5};

float	FPBleach_Interior
<
	string UIName="FP: Bleach Interior";
	string UIWidget="spinner";
	float UIMin=-0.5;
	float UIMax=1.0;
> = {0.0};

float	FPSaturation_Interior
<
	string UIName="FP: Saturation Interior";
	string UIWidget="spinner";
	float UIMin=-1.0;
	float UIMax=1.0;
> = {-0.15};

float	RedCurve_Interior
<
	string UIName="FP: Red Curve Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	GreenCurve_Interior
<
	string UIName="FP: Green Curve Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BlueCurve_Interior
<
	string UIName="FP: Blue Curve Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BaseCurve_Interior
<
	string UIName="FP: Base Curve Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.5};

float	BaseGamma_Interior
<
	string UIName="FP: Base Gamma Interior";
	string UIWidget="spinner";
	float UIMin=0.7;
	float UIMax=2.0;
> = {1.0};

float	EffectGamma_Interior
<
	string UIName="FP: Effect Gamma Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.65};

float	EffectGammaR_Interior
<
	string UIName="FP Effect Gamma Red Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaG_Interior
<
	string UIName="FP Effect Gamma Green Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaB_Interior
<
	string UIName="FP Effect Gamma Blue Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};
#endif

#if (INC_Spherical==1)
float empty34 < string UIName = "|=======Spherical Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	sphericalAmount_Interior
<
	string UIName="Spherical Amount Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.5};
#endif

#if (INC_Tint==1)
float empty37 < string UIName = "|======Tinting Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 RGB_TintI <
   string UIName="Tint Color Interior";
   string UIWidget="Color";
> = {0.725, 0.431, 0.118};
float HighlightPowerI <
   string UIName="Highlight Color Power Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float TintPowerI <
   string UIName="Tint Color Power Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowPowerI <
   string UIName="Shadow Color Power Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowStrI <
   string UIName="Add Shadow Color Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float SHueAdjustI <
   string UIName="Shift Shadow Hue Interior";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatShadowsI <
   string UIName="Desaturate Shadows Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatMidsI <
   string UIName="Desaturate Midtones Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatOrigI <
   string UIName="Desaturate Original Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float3 TonedI <
   string UIName="Effect Strength Interior";
   string UIWidget="Color";
> = {0.314, 0.314, 0.314};
#endif

#if (INC_Technicolor==1)
float empty40 < string UIName = "|=======Techicolor Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 colStrengthI <
   string UIName="Technicolor Color Strength Interior";
   string UIWidget="Color";
> = {0.5, 0.5, 0.5};
float brightnessI <
   string UIName="Technicolor Brightness Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrengthI <
   string UIName="Technicolor Amount Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Technicolor2==1)
float empty45 < string UIName = "|======Techicolor 2 Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 rChannelI <
   string UIName="Technicolor 2s Red Interior";
   string UIWidget="Color";
> = {1, 0.165, 0};
float3 gChannelI <
   string UIName="Technicolor 2s Green Interior";
   string UIWidget="Color";
> = {0.294, 1, 0};
float3 bChannelI <
   string UIName="Technicolor 2s Blue Interior";
   string UIWidget="Color";
> = {0.0588, 0.902, 0};
float strip2vibI <
   string UIName="Technicolor 2s Saturation Boost Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.3};
float techStrength2I <
   string UIName="Technicolor 2s Amount Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Shadow==1)
float empty55 < string UIName = "|=======Shadows Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ECCGamma_Interior
<
	string UIName="Gamma Interior";
	string UIWidget="Spinner";
	float UIMin=0.2;
	float UIMax=5.0;
> = {1.0};

float	ECCInBlack_Interior
<
	string UIName="In black Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCInWhite_Interior
<
	string UIName="In white Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCOutBlack_Interior
<
	string UIName="Out black Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCOutWhite_Interior
<
	string UIName="Out white Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCDesaturateShadows_Interior
<
	string UIName="Desaturate shadows Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	LightnessI <		string UIName="Highlights Interior";						string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};
float	ShadowsI <			string UIName="Shadows Interior";							string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};
#endif

#if (INC_SBloom==1)
float empty58 < string UIName = "|======Sweet Bloom Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	BloomThreshold_Interior
<
	string UIName="SBloom Threshold Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=50.0;
> = {20.25};

float	BloomPower_Interior
<
	string UIName="SBloom Power Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {1.44};

float	BloomWidth_Interior
<
	string UIName="SBloom Width Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
	float UIStep=0.0001;
> = {0.0142};
#endif

#if (INC_GaussBloom==1)
float empty61 < string UIName = "|======Gaussian Bloom Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float sl_mix_set_Interior <
   string UIName="Soft Light Intensity Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.275};

float gauss_bloom_Interior <
   string UIName="Gaussian Bloom Intensity Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.550};
#endif

#if (INC_Lightroom==1)
float empty63 < string UIName = "|====== Lightroom Settings =======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};


bool    bShowClippingWhite		 < string UIName="Show white clipping";			> = {false};
bool    bShowClippingBlack	 	 < string UIName="Show black clipping";			> = {false};
float	fLightroom_Red_Hueshift		 < string UIName="Hue: Red";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Orange_Hueshift	 < string UIName="Hue: Orange";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Yellow_Hueshift	 < string UIName="Hue: Yellow";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Green_Hueshift	 < string UIName="Hue: Green";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Aqua_Hueshift	 < string UIName="Hue: Aqua";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Blue_Hueshift	 < string UIName="Hue: Blue";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Magenta_Hueshift	 < string UIName="Hue: Magenta";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Red_Exposure		 < string UIName="Exposure: Red";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Orange_Exposure	 < string UIName="Exposure: Orange";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Yellow_Exposure	 < string UIName="Exposure: Yellow";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Green_Exposure	 < string UIName="Exposure: Green";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Aqua_Exposure	 < string UIName="Exposure: Aqua";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Blue_Exposure	 < string UIName="Exposure: Blue";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Magenta_Exposure	 < string UIName="Exposure: Magenta";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Red_Saturation	 < string UIName="Saturation: Red";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Orange_Saturation	 < string UIName="Saturation: Orange";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Yellow_Saturation	 < string UIName="Saturation: Yellow";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Green_Saturation	 < string UIName="Saturation: Green";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Aqua_Saturation	 < string UIName="Saturation: Aqua";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Blue_Saturation	 < string UIName="Saturation: Blue";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Magenta_Saturation	 < string UIName="Saturation: Magenta";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalBlackLevel	 < string UIName="Global Black Level";		string UIWidget="Spinner";	float UIStep=1.0;	float UIMin=0.0;	float UIMax=512.0;	> = {0.0};
float	fLightroom_GlobalWhiteLevel	 < string UIName="Global White Level";		string UIWidget="Spinner";	float UIStep=1.0;	float UIMin=0.0;	float UIMax=512.0;	> = {255.0};
float	fLightroom_GlobalExposure	 < string UIName="Global Exposure";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalGamma		 < string UIName="Global Gamma";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalBlacksCurve	 < string UIName="Global Blacks Curve";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalShadowsCurve	 < string UIName="Global Shadows Curve";	string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalMidtonesCurve	 < string UIName="Global Midtones Curve";	string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalHighlightsCurve < string UIName="Global Highlights Curve";	string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalWhitesCurve 	 < string UIName="Global Whites Curve";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalContrast 	 < string UIName="Global Contrast";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalSaturation 	 < string UIName="Global Saturation";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalVibrance 	 < string UIName="Global Vibrance";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalTemperature 	 < string UIName="Global Temperature";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalTint 		 < string UIName="Global Tint";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
#endif
// ---- end include Shaders/PostUI.fxh ----
          // LEAVE THIS!!!
 
/*
=============================================== Convert Image Color to Grade ================================================
	
	In case you want to grade on LOG fotage i added these functions (code by kingeric1992)
	Place them before your LUT comes in. This way you can use diffrent log methods to grade ontop
	Or incase you have no idea what all that is look up on it here: https://www.rocketstock.com/blog/tips-for-log-color-space-compositing/
	
	Avalible LOG Functions are:
	
    color.rgb = TM_Lin2Log(color.rgb);

    color.rgb = TM_sLog3(color.rgb);

	color.rgb = TM_sLog2(color.rgb);

	color.rgb = TM_sLog(color.rgb);

	color.rgb = TM_sGamut3Cine(color.rgb);

	color.rgb = TM_sGamut3(color.rgb);

	color.rgb = TM_Cineon(color.rgb);
	
	
	implementation example:
	color.rgb = TM_Lin2Log(color.rgb);
	color.rgb = Lut4096(color.rgb, MyLogLUT);
	
	
	might be useful: https://luts.iwltbap.com/free-lut-log-to-rec709-and-rec709-to-log-conversion/


===================================================== Implementation ========================================================

Basically do what has been written above inbetween the {      }    (not the texture loading tho)

	example:
	Texture2D LOGtoREC          <string ResourceName="LUT/LOGtoREC.bmp"; >; 
	Texture2D sLOG_LUT          <string ResourceName="LUT/MySLogLUT.bmp"; >; 
	Texture2D LUTxy_Night       <string ResourceName="LUT/VibrantNight.bmp"; >; 
	Texture2D LUTxy_Interior    <string ResourceName="LUT/VibrantInterior.bmp"; >; 
	Texture2D LUTxy_Day         <string ResourceName="LUT/VibrantDay.bmp"; >; 
	
	
    float3 LUTApply(float3 color)        // Leave this!
    {                                    // Leave this!
	
	if (LUTSelect==1) {
	color.rgb = TM_Lin2Log(color.rgb);
    color.rgb = Lut4096(color.rgb, LOGtoREC);
	}
	
	if (LUTSelect==2) {
	color.rgb = TM_sLog(color.rgb);
	color.rgb = Lut1024(color.rgb, sLOG_LUT);
	}
	
	if {LUTSelect==3) {
    color.rgb = lerp(lerp(Lut256(color.rgb, LUTxy_Night), 
                          Lut256(color.rgb, LUTxy_Day),      ENightDayFactor),
                          Lut256(color.rgb, LUTxy_Interior), EInteriorFactor);
	}
		return color;                    // Leave this!
    }                                    // Leave this!

*/


float3 LUTApply(float3 color)        // Leave this!
{                                    // Leave this!
	

	
	
	return color;                    // Leave this!
}                                    // Leave this!


// ---- end include Setup/LUTSetup.fxh ----



#if (INC_Lightroom==1)
// ---- begin include Shaders/Lightroom.fxh ----
//==========================//
// Lightroom by Marty McFly //
//==========================//

void VS_Lightroom(in  	float3 inpos  		: POSITION,
	          out 	float4 outpos 		: SV_POSITION,
		  inout float2 txcoord0 	: TEXCOORD0,
		  out 	float huefactors[7] 	: TEXCOORD1)
{
	outpos = float4(inpos.xyz,1.0);

	static const float originalHue[8] = {0.0,0.0833333333333,0.1666666666666,0.3333333333333,0.5,0.6666666666666,0.8333333333333,1.0};

	huefactors[0] 	= (fLightroom_Red_Hueshift     > 0.0) ? lerp(originalHue[0], originalHue[1], fLightroom_Red_Hueshift) 	  : lerp(originalHue[7], originalHue[6], -fLightroom_Red_Hueshift);
	huefactors[1] 	= (fLightroom_Orange_Hueshift  > 0.0) ? lerp(originalHue[1], originalHue[2], fLightroom_Orange_Hueshift)  : lerp(originalHue[1], originalHue[0], -fLightroom_Orange_Hueshift);
	huefactors[2]	= (fLightroom_Yellow_Hueshift  > 0.0) ? lerp(originalHue[2], originalHue[3], fLightroom_Yellow_Hueshift)  : lerp(originalHue[2], originalHue[1], -fLightroom_Yellow_Hueshift);
	huefactors[3] 	= (fLightroom_Green_Hueshift   > 0.0) ? lerp(originalHue[3], originalHue[4], fLightroom_Green_Hueshift)   : lerp(originalHue[3], originalHue[2], -fLightroom_Green_Hueshift);
	huefactors[4] 	= (fLightroom_Aqua_Hueshift    > 0.0) ? lerp(originalHue[4], originalHue[5], fLightroom_Aqua_Hueshift) 	  : lerp(originalHue[4], originalHue[3], -fLightroom_Aqua_Hueshift);
	huefactors[5] 	= (fLightroom_Blue_Hueshift    > 0.0) ? lerp(originalHue[5], originalHue[6], fLightroom_Blue_Hueshift) 	  : lerp(originalHue[5], originalHue[4], -fLightroom_Blue_Hueshift);
	huefactors[6]	= (fLightroom_Magenta_Hueshift > 0.0) ? lerp(originalHue[6], originalHue[7], fLightroom_Magenta_Hueshift) : lerp(originalHue[6], originalHue[5], -fLightroom_Magenta_Hueshift);
}


float GetLumaGradient(float x)
{
	x = linearstep(fLightroom_GlobalBlackLevel / 255.0, fLightroom_GlobalWhiteLevel / 255.0, x);
	x = saturate(x * exp2(fLightroom_GlobalExposure));
	x = pow(x, exp2(-fLightroom_GlobalGamma));

	//derp, could add more nodes here
	float BlacksMult   	= smoothstep(0.25,0.00,x);
	float ShadowsMult  	= smoothstep(0.00,0.25,x) * smoothstep(0.50,0.25,x);
	float MidtonesMult 	= smoothstep(0.25,0.50,x) * smoothstep(0.75,0.50,x);
	float HighlightsMult  	= smoothstep(0.50,0.75,x) * smoothstep(1.00,0.75,x);
	float WhitesMult  	= smoothstep(0.75,1.00,x);

	float BlacksCurve 	= fLightroom_GlobalBlacksCurve;
	float ShadowsCurve 	= fLightroom_GlobalShadowsCurve;
	float MidtonesCurve 	= fLightroom_GlobalMidtonesCurve;
	float HighlightsCurve 	= fLightroom_GlobalHighlightsCurve;
	float WhitesCurve 	= fLightroom_GlobalWhitesCurve;

	//I'm not proud of that one :V
	x = pow(saturate(x), exp2(BlacksMult	 *exp2(-BlacksCurve)
	                        + ShadowsMult	 *exp2(-ShadowsCurve)
			        + MidtonesMult	 *exp2(-MidtonesCurve)
			        + HighlightsMult *exp2(-HighlightsCurve)
			        + WhitesMult	 *exp2(-WhitesCurve) - 1));
	x = lerp(x,smoothstep(0.0,1.0,x),fLightroom_GlobalContrast); //faster than Dpeasant3's sin based contrast
	return x;
}


float4	PS_Lightroom(float4 vpos : SV_POSITION, float2 texcoord : TEXCOORD0, float huefactors[7] : TEXCOORD1) : SV_Target
{
	float4 color = TextureColor.Sample(Sampler1, texcoord.xy);
	if (USE_Lightroom==true)
	{
	color.xyz = saturate(color.xyz); //we did tonemapping in enbeffect.fx so we force LDR here.

	//TEMPERATURE AND TINT - looking for better alternatives ..
	float3 ColdKelvinColor = HSL2RGB(float3(0.56111,1.0,0.5));
	float3 WarmKelvinColor = HSL2RGB(float3(0.06111,1.0,0.5));

	float3 TempKelvinColor = lerp(ColdKelvinColor, WarmKelvinColor, fLightroom_GlobalTemperature*0.5+0.5);

	float oldLuma = RGB2HSL(color.xyz).z;
	float3 tintedColor = color.xyz * TempKelvinColor / dot(TempKelvinColor,float3(0.299,0.587,0.114)); //just using old luma does not work for some reason and weirds out colors.
	color.xyz = HSL2RGB(float3(RGB2HSL(tintedColor.xyz).xy,oldLuma));

	float3 TintColorGreen  = HSL2RGB(float3(0.31111,1.0,0.5));
	float3 TintColorPurple = HSL2RGB(float3(0.81111,1.0,0.5));

	float3 TempTintColor = lerp(TintColorGreen, TintColorPurple, fLightroom_GlobalTint*0.5+0.5);

	tintedColor = color.xyz * TempTintColor / dot(TempTintColor,float3(0.299,0.587,0.114)); //just using old luma does not work for some reason and weirds out colors.
	color.xyz = HSL2RGB(float3(RGB2HSL(tintedColor.xyz).xy,oldLuma));

	//GLOBAL ADJUSTMENTS
	float3 HSL = RGB2HSL(color.xyz);
	HSL.z = GetLumaGradient(HSL.z);
	HSL.y = saturate(HSL.y + HSL.y*fLightroom_GlobalSaturation);
	HSL.y = pow(HSL.y,1.0 / exp2(fLightroom_GlobalVibrance)); //Preprocessor makes -f[..] to --f[..] so we need 1 / x
	HSL.xyz = saturate(HSL.xyz); //EXTREMELY IMPORTANT! FIXES BLACK PIXELS

	//HUE ADJUSTMENTS
	float huemults[7] =
	{
	/*red*/	max(saturate(1.0 - abs(HSL.x*12.0)), saturate(1.0 - abs((HSL.x-12.0/12)* 6.0))),
     /*orange*/ saturate(1.0 - abs((HSL.x-1.0/12)*12.0)),
     /*yellow*/	max(saturate(1.0 - abs((HSL.x-2.0/12)*12.0))*step(HSL.x,2.0/12.0), saturate(1.0 - abs((HSL.x-2.0/12)* 6.0))*step(2.0/12.0,HSL.x)),
      /*green*/ saturate(1.0 - abs((HSL.x-4.0/12)* 6.0)),
       /*aqua*/ saturate(1.0 - abs((HSL.x-6.0/12)* 6.0)),
       /*blue*/ saturate(1.0 - abs((HSL.x-8.0/12)* 6.0)),
    /*magenta*/ saturate(1.0 - abs((HSL.x-10.0/12)* 6.0))
	};

	//could use exp2 for saturation as well but then grayscale would require -inf as saturation setting. sqrt(sat) to make exposure changes more intense as it'd only apply fully on max saturated pixels.
	color.xyz = 0.0;
	color.xyz += huemults[0] * HSL2RGB(float3(huefactors[0],saturate(HSL.y + HSL.y * fLightroom_Red_Saturation), 	 HSL.z * exp2(sqrt(HSL.y)*fLightroom_Red_Exposure)	));
	color.xyz += huemults[1] * HSL2RGB(float3(huefactors[1],saturate(HSL.y + HSL.y * fLightroom_Orange_Saturation),  HSL.z * exp2(sqrt(HSL.y)*fLightroom_Orange_Exposure)	));
	color.xyz += huemults[2] * HSL2RGB(float3(huefactors[2],saturate(HSL.y + HSL.y * fLightroom_Yellow_Saturation),  HSL.z * exp2(sqrt(HSL.y)*fLightroom_Yellow_Exposure)	));
	color.xyz += huemults[3] * HSL2RGB(float3(huefactors[3],saturate(HSL.y + HSL.y * fLightroom_Green_Saturation), 	 HSL.z * exp2(sqrt(HSL.y)*fLightroom_Green_Exposure)	));
	color.xyz += huemults[4] * HSL2RGB(float3(huefactors[4],saturate(HSL.y + HSL.y * fLightroom_Aqua_Saturation), 	 HSL.z * exp2(sqrt(HSL.y)*fLightroom_Aqua_Exposure)	));
	color.xyz += huemults[5] * HSL2RGB(float3(huefactors[5],saturate(HSL.y + HSL.y * fLightroom_Blue_Saturation), 	 HSL.z * exp2(sqrt(HSL.y)*fLightroom_Blue_Exposure)	));
	color.xyz += huemults[6] * HSL2RGB(float3(huefactors[6],saturate(HSL.y + HSL.y * fLightroom_Magenta_Saturation), HSL.z * exp2(sqrt(HSL.y)*fLightroom_Magenta_Exposure)	));

	//CLIP MASK
	color.xyz = (bShowClippingWhite && dot(color.xyz,1.0) >= 3.0) ? float3(1.0,0.0,0.0) : color.xyz;
	color.xyz = (bShowClippingBlack && dot(color.xyz,1.0) <= 0.0) ? float3(0.0,0.0,1.0) : color.xyz; //"<=0" when we just saturate()'ed, am I drunk?

	color.w = 1.0;
	}
	return color;

}
// ---- end include Shaders/Lightroom.fxh ----

#endif
#if (INC_Vibrance==1)
// ---- begin include Shaders/Vibrance.fxh ----
//=======================//
// Vibrance by Ceejay.dk //
//=======================//

float3 Vibrance(float3 color)
{

	if (USE_Vibrance==true)
	{
    float Vibrance              =lerp( lerp(Vibrance_Night,             Vibrance_Day,             ENightDayFactor), Vibrance_Interior,             EInteriorFactor );
    float3 VibranceRGBBalance   =lerp( lerp(VibranceRGBBalance_Night,   VibranceRGBBalance_Day,   ENightDayFactor), VibranceRGBBalance_Interior,   EInteriorFactor );
  
	const float3 coefLuma = float3(0.212656, 0.715158, 0.072186);
	float luma = dot(coefLuma, color);

	float max_color = max(color.r, max(color.g, color.b)); // Find the strongest color
	float min_color = min(color.r, min(color.g, color.b)); // Find the weakest color

	float color_saturation = max_color - min_color; // The difference between the two is the saturation

	// Extrapolate between luma and original by 1 + (1-saturation) - current
	float3 coeffVibrance = float3(VibranceRGBBalance * Vibrance);
	color = lerp(luma, color, 1.0 + (coeffVibrance * (1.0 - (sign(coeffVibrance) * color_saturation))));
    }
	return color;
}

// ---- end include Shaders/Vibrance.fxh ----

#endif
#if (INC_DPX==1)
// ---- begin include Shaders/DPX.fxh ----
//=============================//
// DPX Cineon shader by Loadus //
//=============================//

static const float3x3 RGB = float3x3(
	 2.6714711726599600, -1.2672360578624100, -0.4109956021722270,
	-1.0251070293466400,  1.9840911624108900,  0.0439502493584124,
	 0.0610009456429445, -0.2236707508128630,  1.1590210416706100
);
static const float3x3 XYZ = float3x3(
	 0.5003033835433160,  0.3380975732227390,  0.1645897795458570,
	 0.2579688942747580,  0.6761952591447060,  0.0658358459823868,
	 0.0234517888692628,  0.1126992737203000,  0.8668396731242010
);

float3	DPX(float3 color)
{
	if (USE_DPX==true)
	{
	
  float RGB_Curve        =lerp( lerp(RGB_Curve_Night,   RGB_Curve_Day,   ENightDayFactor), RGB_Curve_Interior,   EInteriorFactor );
  float RGB_C            =lerp( lerp(RGB_C_Night,   RGB_C_Day,   ENightDayFactor), RGB_C_Interior,   EInteriorFactor );
  float ContrastDPX      =lerp( lerp(ContrastDPX_Night,   ContrastDPX_Day,   ENightDayFactor), ContrastDPX_Interior,   EInteriorFactor );
  float SaturationDPX    =lerp( lerp(SaturationDPX_Night,   SaturationDPX_Day,   ENightDayFactor), SaturationDPX_Interior,   EInteriorFactor );
  float ColorfulnessDPX  =lerp( lerp(ColorfulnessDPX_Night,   ColorfulnessDPX_Day,   ENightDayFactor), ColorfulnessDPX_Interior,   EInteriorFactor );
  float StrengthDPX      =lerp( lerp(StrengthDPX_Night,   StrengthDPX_Day,   ENightDayFactor), StrengthDPX_Interior,   EInteriorFactor );

	float3 B = color;
	B = B * (1.0 - ContrastDPX) + (0.5 * ContrastDPX);
	float3 Btemp = (1.0 / (1.0 + exp(RGB_Curve / 2.0)));
	B = ((1.0 / (1.0 + exp(-RGB_Curve * (B - RGB_C)))) / (-2.0 * Btemp + 1.0)) + (-Btemp / (-2.0 * Btemp + 1.0));

	float value = max(max(B.r, B.g), B.b);
	float3 input = B / value;
	input = pow(abs(input), 1.0 / ColorfulnessDPX);

	float3 c0 = input * value;
	c0 = mul(XYZ, c0);
	float luma = dot(c0, float3(0.30, 0.59, 0.11));
	c0 = (1.0 - SaturationDPX) * luma + SaturationDPX * c0;
	c0 = mul(RGB, c0);

	return lerp(color, c0, StrengthDPX);
	}
	else
	return color;
}
// ---- end include Shaders/DPX.fxh ----

#endif
#if (INC_Filmpass==1)
// ---- begin include Shaders/Filmpass.fxh ----
//=============================================================//
// FilmPass by Reshade Team (There is no name in the Credits?) //
// ENB port and DNI by Adyss                                   //
//=============================================================//
// FilmPass Shader //
//=================//
float3	filmpass(float3 color)
{
	if (USE_Filmpass==true)
	{
	float3 B = color;
	float3 G = B;
	float3 H = 0.01;
	
  // DNI Seperation by Adyss
  float FPStrength     =lerp( lerp(FPStrength_Night,     FPStrength_Day,     ENightDayFactor), FPStrength_Interior,     EInteriorFactor );
  float FPFade         =lerp( lerp(FPFade_Night,         FPFade_Day,         ENightDayFactor), FPFade_Interior,         EInteriorFactor );
  float FPContrast     =lerp( lerp(FPContrast_Night,     FPContrast_Day,     ENightDayFactor), FPContrast_Interior,     EInteriorFactor );
  float Linearization  =lerp( lerp(Linearization_Night,  Linearization_Day,  ENightDayFactor), Linearization_Interior,  EInteriorFactor );
  float FPBleach       =lerp( lerp(FPBleach_Night,       FPBleach_Day,       ENightDayFactor), FPBleach_Interior,       EInteriorFactor );
  float FPSaturation   =lerp( lerp(FPSaturation_Night,   FPSaturation_Day,   ENightDayFactor), FPSaturation_Interior,   EInteriorFactor );
  float BaseCurve      =lerp( lerp(BaseCurve_Night,      BaseCurve_Day,      ENightDayFactor), BaseCurve_Interior,      EInteriorFactor );
  float RedCurve       =lerp( lerp(RedCurve_Night,       RedCurve_Day,       ENightDayFactor), RedCurve_Interior,       EInteriorFactor );
  float GreenCurve     =lerp( lerp(GreenCurve_Night,     GreenCurve_Day,     ENightDayFactor), GreenCurve_Interior,     EInteriorFactor );
  float BlueCurve      =lerp( lerp(BlueCurve_Night,      BlueCurve_Day,      ENightDayFactor), BlueCurve_Interior,      EInteriorFactor );
  float BaseGamma      =lerp( lerp(BaseGamma_Night,      BaseGamma_Day,      ENightDayFactor), BaseGamma_Interior,      EInteriorFactor );
  float EffectGamma    =lerp( lerp(EffectGamma_Night,    EffectGamma_Day,    ENightDayFactor), EffectGamma_Interior,    EInteriorFactor );
  float EffectGammaR   =lerp( lerp(EffectGammaR_Night,   EffectGammaR_Day,   ENightDayFactor), EffectGammaR_Interior,   EInteriorFactor );
  float EffectGammaG   =lerp( lerp(EffectGammaG_Night,   EffectGammaG_Day,   ENightDayFactor), EffectGammaG_Interior,   EInteriorFactor );
  float EffectGammaB   =lerp( lerp(EffectGammaB_Night,   EffectGammaB_Day,   ENightDayFactor), EffectGammaB_Interior,   EInteriorFactor );
 
	B = saturate(B);
	B = pow(B, Linearization);
	B = lerp(H, B, FPContrast);
 
	float A = dot(B.rgb, CoefLuma);
	float3 D = A;
 
	B = pow(B, 1.0 / BaseGamma);
 
	float a = RedCurve;
	float b = GreenCurve;
	float c = BlueCurve;
	float d = BaseCurve;
 
	float y = 1.0 / (1.0 + exp(a / 2.0));
	float z = 1.0 / (1.0 + exp(b / 2.0));
	float w = 1.0 / (1.0 + exp(c / 2.0));
	float v = 1.0 / (1.0 + exp(d / 2.0));
 
	float3 C = B;
 
	D.r = (1.0 / (1.0 + exp(-a * (D.r - 0.5))) - y) / (1.0 - 2.0 * y);
	D.g = (1.0 / (1.0 + exp(-b * (D.g - 0.5))) - z) / (1.0 - 2.0 * z);
	D.b = (1.0 / (1.0 + exp(-c * (D.b - 0.5))) - w) / (1.0 - 2.0 * w);
 
	D = pow(D, 1.0 / EffectGamma);
 
	float3 Di = 1.0 - D;
 
	D = lerp(D, Di, FPBleach);
 
	D.r = pow(abs(D.r), 1.0 / EffectGammaR);
	D.g = pow(abs(D.g), 1.0 / EffectGammaG);
	D.b = pow(abs(D.b), 1.0 / EffectGammaB);
 
	if (D.r < 0.5)
		C.r = (2.0 * D.r - 1.0) * (B.r - B.r * B.r) + B.r;
	else
		C.r = (2.0 * D.r - 1.0) * (sqrt(B.r) - B.r) + B.r;
 
	if (D.g < 0.5)
		C.g = (2.0 * D.g - 1.0) * (B.g - B.g * B.g) + B.g;
	else
		C.g = (2.0 * D.g - 1.0) * (sqrt(B.g) - B.g) + B.g;

	if (D.b < 0.5)
		C.b = (2.0 * D.b - 1.0) * (B.b - B.b * B.b) + B.b;
	else
		C.b = (2.0 * D.b - 1.0) * (sqrt(B.b) - B.b) + B.b;
 
	float3 F = lerp(B, C, FPStrength);
 
	F = (1.0 / (1.0 + exp(-d * (F - 0.5))) - v) / (1.0 - 2.0 * v);
 
	float r2R = 1.0 - FPSaturation;
	float g2R = 0.0 + FPSaturation;
	float b2R = 0.0 + FPSaturation;
 
	float r2G = 0.0 + FPSaturation;
	float g2G = (1.0 - FPFade) - FPSaturation;
	float b2G = (0.0 + FPFade) + FPSaturation;
 
	float r2B = 0.0 + FPSaturation;
	float g2B = (0.0 + FPFade) + FPSaturation;
	float b2B = (1.0 - FPFade) - FPSaturation;
 
	float3 iF = F;
 
	F.r = (iF.r * r2R + iF.g * g2R + iF.b * b2R);
	F.g = (iF.r * r2G + iF.g * g2G + iF.b * b2G);
	F.b = (iF.r * r2B + iF.g * g2B + iF.b * b2B);
 
	float N = dot(F.rgb, CoefLuma);
	float3 Cn = F;
 
	if (N < 0.5)
		Cn = (2.0 * N - 1.0) * (F - F * F) + F;
	else
		Cn = (2.0 * N - 1.0) * (sqrt(F) - F) + F;
 
	Cn = pow(max(Cn,0), 1.0 / Linearization);
 
	float3 Fn = lerp(B, Cn, FPStrength);
	return Fn;
	}
	else
	return color;
}
// ---- end include Shaders/Filmpass.fxh ----

#endif
#if (INC_Spherical==1)
// ---- begin include Shaders/Spherical.fxh ----
//==================================//
// Spherical Tonemap by Marty McFly //
//==================================//
float3 Spherical(float3 color)
{
    float3 x =color;
if (USE_Spherical==true)
{
    float sphericalAmount   =lerp( lerp(sphericalAmount_Night,   sphericalAmount_Day,   ENightDayFactor), sphericalAmount_Interior,   EInteriorFactor );
    float3 signedColor = x * 2.0 - 1.0;
    float3 sphericalColor = sqrt(1.0 - signedColor.rgb * signedColor.rgb);
    sphericalColor = sphericalColor * 0.5 + 0.5;
    sphericalColor *= x;
    x += sphericalColor.rgb * sphericalAmount;
}
    return x;
}
// ---- end include Shaders/Spherical.fxh ----

#endif
#if (INC_Reinhard==1)
// ---- begin include Shaders/LinReinhard.fxh ----
//===============================================================================//
// Reinhard Shader form Mastereffect by Marty McFly. Reshade 3 port by Insomnia  //
//===============================================================================//
float3 Reinhard(float3 color)
{
	if (USE_Reinhard==true)
	{
  float ReinhardLinearSlope        =lerp( lerp(ReinhardLinearSlope_Night,   ReinhardLinearSlope_Day,   ENightDayFactor), ReinhardLinearSlope_Interior,   EInteriorFactor );
  float ReinhardLinearWhitepoint   =lerp( lerp(ReinhardLinearWhitepoint_Night,   ReinhardLinearWhitepoint_Day,   ENightDayFactor), ReinhardLinearWhitepoint_Interior,   EInteriorFactor );
  float ReinhardLinearPoint        =lerp( lerp(ReinhardLinearPoint_Night,   ReinhardLinearPoint_Day,   ENightDayFactor), ReinhardLinearPoint_Interior,   EInteriorFactor );
	
	float3 x = color.rgb;

    	const float W = ReinhardLinearWhitepoint;	   // Linear White Point Value
    	const float L = ReinhardLinearPoint;           // Linear point
    	const float C = ReinhardLinearSlope;           // Slope of the linear section
    	const float K = (1 - L * C) / C;               // Scale (fixed so that the derivatives of the Reinhard and linear functions are the same at x = L)
    	float3 reinhard = L * C + (1 - L * C) * (1 + K * (x - L) / ((W - L) * (W - L))) * (x - L) / (x - L + K);

    	// gamma space or not?
    	color.rgb = (x > L) ? reinhard : C * x;
	}
	return color;
}
// ---- end include Shaders/LinReinhard.fxh ----

#endif
#if (INC_Reinhard==2)
// ---- begin include Shaders/Reinhard.fxh ----
//==============================//
// Original code by Marty McFly //
// Reshade3 port by Insomnia    //
//==============================//

float3 ReinhardPass(float3 color)
{
    if (USE_Reinhard==true) {

    float ReinhardWhitepoint   =lerp( lerp(ReinhardWhitepoint_Night,   ReinhardWhitepoint_Day,   ENightDayFactor), ReinhardWhitepoint_Interior,   EInteriorFactor );
    float ReinhardScale         =lerp( lerp(ReinhardScale_Night,        ReinhardScale_Day,        ENightDayFactor), ReinhardScale_Interior,        EInteriorFactor );
	
	float3 x = color;
	const float W =  ReinhardWhitepoint;	// Linear White Point Value
    const float K =  ReinhardScale;         // Scale

    	// gamma space or not?
    	return (1 + K * x / (W * W)) * x / (x + K);
	}
	else
	return color;
}
// ---- end include Shaders/Reinhard.fxh ----

#endif
#if (INC_Curves==1)
// ---- begin include Shaders/Curves.fxh ----
//=====================//
// Curves by Ceejay.dk //
//=====================//

float4 Curves(float4 color)
{
    float4 colorInput;
    colorInput = color;
	if (USE_Curves==true)
	{
	// DNI Separation by Adyss
    float Formula   =lerp( lerp(Formula_Night,   Formula_Day,   ENightDayFactor), Formula_Interior,   EInteriorFactor );
    float Mode   =lerp( lerp(Mode_Night,   Mode_Day,   ENightDayFactor), Mode_Interior,   EInteriorFactor );
    float Contrast   =lerp( lerp(Contrast_Night,   Contrast_Day,   ENightDayFactor), Contrast_Interior,   EInteriorFactor );
	
	float3 lumCoeff = float3(0.2126, 0.7152, 0.0722);  //Values to calculate luma with
	float Contrast_blend = Contrast; 
	const float PI = 3.1415927;

	/*-----------------------------------------------------------.
	/               Separation of Luma and Chroma                 /
	'-----------------------------------------------------------*/

	// -- Calculate Luma and Chroma if needed --
	//calculate luma (grey)
	float luma = dot(lumCoeff, colorInput.rgb);
	//calculate chroma
	float3 chroma = colorInput.rgb - luma;

	// -- Which value to put through the contrast formula? --
	// I name it x because makes it easier to copy-paste to Graphtoy or Wolfram Alpha or another graphing program
	float3 x;
	if (Mode == 0)
		x = luma; //if the curve should be applied to Luma
	else if (Mode == 1)
		x = chroma, //if the curve should be applied to Chroma
		x = x * 0.5 + 0.5; //adjust range of Chroma from -1 -> 1 to 0 -> 1
	else
		x = colorInput.rgb; //if the curve should be applied to both Luma and Chroma

	/*-----------------------------------------------------------.
	/                     Contrast formulas                       /
	'-----------------------------------------------------------*/

	// -- Curve 1 --
	if (Formula == 0)
	{
		x = sin(PI * 0.5 * x); // Sin - 721 amd fps, +vign 536 nv
		x *= x;

		//x = 0.5 - 0.5*cos(PI*x);
		//x = 0.5 * -sin(PI * -x + (PI*0.5)) + 0.5;
	}

	// -- Curve 2 --
	if (Formula == 1)
	{
		x = x - 0.5;
		x = (x / (0.5 + abs(x))) + 0.5;

		//x = ( (x - 0.5) / (0.5 + abs(x-0.5)) ) + 0.5;
	}

	// -- Curve 3 --
	if (Formula == 2)
	{
		//x = smoothstep(0.0,1.0,x); //smoothstep
		x = x*x*(3.0 - 2.0*x); //faster smoothstep alternative - 776 amd fps, +vign 536 nv
		//x = x - 2.0 * (x - 1.0) * x* (x- 0.5);  //2.0 is contrast. Range is 0.0 to 2.0
	}

	// -- Curve 4 --
	if (Formula == 3)
	{
		x = (1.0524 * exp(6.0 * x) - 1.05248) / (exp(6.0 * x) + 20.0855); //exp formula
	}

	// -- Curve 5 --
	if (Formula == 4)
	{
		//x = 0.5 * (x + 3.0 * x * x - 2.0 * x * x * x); //a simplified catmull-rom (0,0,1,1) - btw smoothstep can also be expressed as a simplified catmull-rom using (1,0,1,0)
		//x = (0.5 * x) + (1.5 -x) * x*x; //estrin form - faster version
		x = x * (x * (1.5 - x) + 0.5); //horner form - fastest version

		Contrast_blend = Contrast * 2.0; //I multiply by two to give it a strength closer to the other curves.
	}

	// -- Curve 6 --
	if (Formula == 5)
	{
		x = x*x*x*(x*(x*6.0 - 15.0) + 10.0); //Perlins smootherstep
	}

	// -- Curve 7 --
	if (Formula == 6)
	{
		//x = ((x-0.5) / ((0.5/(4.0/3.0)) + abs((x-0.5)*1.25))) + 0.5;
		x = x - 0.5;
		x = x / ((abs(x)*1.25) + 0.375) + 0.5;
		//x = ( (x-0.5) / ((abs(x-0.5)*1.25) + (0.5/(4.0/3.0))) ) + 0.5;
	}

	// -- Curve 8 --
	if (Formula == 7)
	{
		x = (x * (x * (x * (x * (x * (x * (1.6 * x - 7.2) + 10.8) - 4.2) - 3.6) + 2.7) - 1.8) + 2.7) * x * x; //Techicolor Cinestyle - almost identical to curve 1
	}

	// -- Curve 9 --
	if (Formula == 8)
	{
		x = -0.5 * (x*2.0 - 1.0) * (abs(x*2.0 - 1.0) - 2.0) + 0.5; //parabola
	}

	// -- Curve 10 --
	if (Formula == 9)
	{
		float3 xstep = step(x, 0.5); //tenary might be faster here
		float3 xstep_shift = (xstep - 0.5);
		float3 shifted_x = x + xstep_shift;

		x = abs(xstep - sqrt(-shifted_x * shifted_x + shifted_x)) - xstep_shift;

		//x = abs(step(x,0.5)-sqrt(-(x+step(x,0.5)-0.5)*(x+step(x,0.5)-0.5)+(x+step(x,0.5)-0.5)))-(step(x,0.5)-0.5); //single line version of the above

		//x = 0.5 + (sign(x-0.5)) * sqrt(0.25-(x-trunc(x*2))*(x-trunc(x*2))); //worse

		/* // if/else - even worse
		if (x-0.5)
		x = 0.5-sqrt(0.25-x*x);
		else
		x = 0.5+sqrt(0.25-(x-1)*(x-1));
		*/

		//x = (abs(step(0.5,x)-clamp( 1-sqrt(1-abs(step(0.5,x)- frac(x*2%1)) * abs(step(0.5,x)- frac(x*2%1))),0 ,1))+ step(0.5,x) )*0.5; //worst so far

		//TODO: Check if I could use an abs split instead of step. It might be more efficient

		Contrast_blend = Contrast * 0.5; //I divide by two to give it a strength closer to the other curves.
	}
  
	// -- Curve 11 --
	if (Formula == 10)
	{
		float3 a = float3(0.0, 0.0, 0.0);
		float3 b = float3(0.0, 0.0, 0.0);

		a = x * x * 2.0;
		b = (2.0 * -x + 4.0) * x - 1.0;
		x = (x < 0.5) ? a : b;
	}

	/*-----------------------------------------------------------.
	/                 Joining of Luma and Chroma                  /
	'-----------------------------------------------------------*/

	if (Mode == 0) // Only Luma
	{
		x = lerp(luma, x, Contrast_blend); //Blend by Contrast
		colorInput.rgb = x + chroma; //Luma + Chroma
	}
	else if (Mode == 1) // Only Chroma
	{
		x = x * 2.0 - 1.0; //adjust the Chroma range back to -1 -> 1
		float3 color = luma + x; //Luma + Chroma
		colorInput.rgb = lerp(colorInput.rgb, color, Contrast_blend); //Blend by Contrast
	}
	else // Both Luma and Chroma
	{
		float3 color = x;  //if the curve should be applied to both Luma and Chroma
		colorInput.rgb = lerp(colorInput.rgb, color, Contrast_blend); //Blend by Contrast
	}
    }
	return colorInput;
}
// ---- end include Shaders/Curves.fxh ----

#endif
#if (INC_Technicolor==1)
// ---- begin include Shaders/Technicolor.fxh ----
//=======================//
// Technicolor by Prod80 //
//=======================//
float4 Technicolor(float4 color)
{
    float4 res;
	
if (use_technicolor==true)
{
   float3 colStrength   = lerp( lerp( colStrengthN, colStrengthD, ENightDayFactor ), colStrengthI, EInteriorFactor );
   float brightness   = lerp( lerp( brightnessN, brightnessD, ENightDayFactor ), brightnessI, EInteriorFactor );
   float techStrength   = lerp( lerp( techStrengthN, techStrengthD, ENightDayFactor ), techStrengthI, EInteriorFactor );

   float3 source      = saturate( color.rgb );
   float3 temp       = 1-source.rgb;
   float3 target       = temp.grg;
   float3 target2      = temp.bbr;
   float3 temp2       = source.rgb * target.rgb;
   temp2.rgb         *= target2.rgb;
   
   temp.rgb          = temp2.rgb * colStrength.rgb;
   temp2.rgb          *= brightness;
   
   target.rgb          = temp.grg;
   target2.rgb       = temp.bbr;
   
   temp.rgb          = source.rgb - target.rgb;
   temp.rgb          += temp2.rgb;
   temp2.rgb          = temp.rgb - target2.rgb;
   
   color.rgb          = lerp( source.rgb, temp2.rgb, techStrength );
}
  	res.xyz=saturate(color);
	res.w=1.0;
	return res;
}
// ---- end include Shaders/Technicolor.fxh ----

#endif
#if (INC_Technicolor2==1)
// ---- begin include Shaders/Technicolor2.fxh ----
//=========================//
// Technicolor 2 by Prod80 //
//=========================//
float4 Technicolor2(float4 color)
{
    float4 res;
if ( use_t2s == true ) 
{
   float3 rChannel      = lerp( lerp( rChannelN, rChannelD, ENightDayFactor ), rChannelI, EInteriorFactor );
   float3 gChannel      = lerp( lerp( gChannelN, gChannelD, ENightDayFactor ), gChannelI, EInteriorFactor );
   float3 bChannel      = lerp( lerp( bChannelN, bChannelD, ENightDayFactor ), bChannelI, EInteriorFactor );
   float strip2vib      = lerp( lerp( strip2vibN, strip2vibD, ENightDayFactor ), strip2vibI, EInteriorFactor );
   float techStrength2   = lerp( lerp( techStrength2N, techStrength2D, ENightDayFactor ), techStrength2I, EInteriorFactor );
   
   color.rgb         = saturate( color.rgb );
   float t2stripRed   = dot( color.rgb, rChannel.rgb / dot( rChannel.rgb, 1 ));
   float t2stripGreen   = dot( color.rgb, gChannel.rgb / dot( gChannel.rgb, 1 ));
   float t2stripBlue   = dot( color.rgb, bChannel.rgb / dot( bChannel.rgb, 1 ));
   
   float3 t2scolor      = float3( t2stripRed, t2stripGreen, t2stripBlue );
   
   t2scolor.rgb      = saturate( t2scolor.rgb );
   t2scolor.rgb      = RGBToHSL( t2scolor.rgb );
   t2scolor.g         = t2scolor.g + (( 1.0f - t2scolor.g ) * ( strip2vib * t2scolor.g ));
   t2scolor.rgb      = HSLToRGB( t2scolor.rgb );
   color.rgb         = lerp( color.rgb, t2scolor.rgb, techStrength2 );
}
  	res.xyz=saturate(color);
	res.w=1.0;
	return res;
}
// ---- end include Shaders/Technicolor2.fxh ----

#endif
#if (INC_Tint==1)
// ---- begin include Shaders/Tint.fxh ----
//================//
// Tint by Prod80 //
//================//
float4 Tint(float4 color)
{
    float4 res;
if (use_tinting==true)
{
   float3   RGB_Tint      = lerp( lerp( RGB_TintN, RGB_TintD,   ENightDayFactor ), RGB_TintI, EInteriorFactor );
   float    DesatMids      = lerp( lerp( DesatMidsN, DesatMidsD, ENightDayFactor ), DesatMidsI, EInteriorFactor );
   float   DesatShadows   = lerp( lerp( DesatShadowsN, DesatShadowsD, ENightDayFactor ), DesatShadowsI, EInteriorFactor );
   float   DesatOrig      = lerp( lerp( DesatOrigN, DesatOrigD, ENightDayFactor ), DesatOrigI, EInteriorFactor );
   float3    Toned          = lerp( lerp( TonedN, TonedD, ENightDayFactor ), TonedI, EInteriorFactor );
   float    ShadowStr      = lerp( lerp( ShadowStrN, ShadowStrD, ENightDayFactor ), ShadowStrI, EInteriorFactor );
   float   TintPower      = lerp( lerp( TintPowerN,   TintPowerD, ENightDayFactor ), TintPowerI, EInteriorFactor );
   float   ShadowPower      = lerp( lerp( ShadowPowerN, ShadowPowerD, ENightDayFactor ), ShadowPowerI, EInteriorFactor );
   float   HighlightPower   = lerp( lerp( HighlightPowerN, HighlightPowerD, ENightDayFactor ), HighlightPowerI, EInteriorFactor );
   float   SHueAdjust      = lerp( lerp( SHueAdjustN, SHueAdjustD, ENightDayFactor ), SHueAdjustI, EInteriorFactor );
   
   color.rgb            = saturate( color.rgb );
   
   float gray            = dot( color.rgb, 0.33333333 );
   float shadows         = pow( 1 - gray, TintPower + ShadowPower );
   float highlights      = pow( gray, TintPower + HighlightPower );
   float midtones         = saturate( 1 - shadows - highlights );
   
   float3 RGB_Shadows      = RGBToHSL( RGB_Tint.rgb );
   RGB_Shadows.r         += 0.5 + SHueAdjust;
      if ( RGB_Shadows.r > 1.0 ) RGB_Shadows.r -= 1.0;
      if ( RGB_Shadows.r < 0.0 ) RGB_Shadows.r += 1.0;
   
   RGB_Shadows.rgb         = saturate( RGB_Shadows.rgb );
   float3 temp_shadows      = RGB_Shadows.rgb;
   RGB_Shadows.rgb         = HSLToRGB( RGB_Shadows.rgb );
   
   //Create gradient
   float3 cg            = saturate( midtones * RGB_Tint.rgb + shadows * RGB_Shadows.rgb + highlights );

   //Mix back with gray 0.33333333, other 'luma' values are INACCURATE in this effect at this stage!
   cg.rgb                = RGBToHSL( cg.rgb );
   cg.rgb                = HSLToRGB( float3( cg.rg, gray ));

   //Shadow color, saturation and final mixing
   temp_shadows.b         = max( temp_shadows.b - ( temp_shadows.b - ShadowStr ), 0.0 );
   temp_shadows.rgb      = HSLToRGB( temp_shadows.rgb );
   cg.rgb                = max( temp_shadows.rgb, cg.rgb );
   cg.rgb               = lerp( cg.rgb, lerp( cg.rgb, grayValue( cg.rgb ), shadows ), DesatShadows );
   cg.rgb                = lerp( cg.rgb, lerp( cg.rgb, grayValue( cg.rgb ), midtones ), DesatMids );
   color.rgb             = lerp( color.rgb, grayValue( color.rgb ), DesatOrig );
   color.rgb             = lerp( color.rgb, cg.rgb, Toned.rgb );
   }
  res.xyz=saturate(color);
  res.w=1.0;
  return res;

}
// ---- end include Shaders/Tint.fxh ----

#endif
#if (INC_Letterbox==1)
// ---- begin include Shaders/Border.fxh ----
//=====================//
// Border by Ceejay.dk //
//=====================//
float3 Border(float3 color, float2 coord)
{	
	if (ENABLE_LETTERBOX==true)
	{
	float2 pixelSize=ScreenSize.y;
	pixelSize.y*=ScreenSize.z;

	// -- calculate the right border_width for a given border_ratio --
	float2 border_width_variable = border_width;
	if (border_width.x == -border_width.y) // If width is not used
		if (ScreenSize.z < border_ratio)
			border_width_variable = float2(0.0, (ScreenSize.y - (ScreenSize.x / border_ratio)) * 0.5);
		else
			border_width_variable = float2((ScreenSize.x - (ScreenSize.y * border_ratio)) * 0.5, 0.0);

	float2 border = (ScreenSize.w * border_width_variable); // This is supposed to be pixelSize but dosnt work with it so i use ScreenSize.w
	float2 within_border = saturate((-coord * coord + coord) - (-border * border + border)); // Becomes positive when inside the border and zero when outside

	return all(within_border) ? color : border_color;
	}
	else
	return color;
}
// ---- end include Shaders/Border.fxh ----

#endif
#if (INC_HDR==1)
// ---- begin include Shaders/fakeHDR.fxh ----
//=======================//
// Fake HDR by Ceejay.dk //
// ENB port by Adyss     //
//=======================//
float3 HDR(float3 color, float2 coord)
{	
	if (USE_HDR==true)
	{
	
	float2 pixelsize=ScreenSize.y;
	pixelsize.y*=ScreenSize.z;
	
	float HDRPower  =lerp( lerp(HDRPower_Night,  HDRPower_Day,  ENightDayFactor), HDRPower_Interior,  EInteriorFactor );
    float radius1   =lerp( lerp(radius1_Night,   radius1_Day,   ENightDayFactor), radius1_Interior,   EInteriorFactor );
    float radius2   =lerp( lerp(radius2_Night,   radius2_Day,   ENightDayFactor), radius2_Interior,   EInteriorFactor );

	float3 bloom_sum1 = TextureColor.Sample(Sampler0, coord + float2(1.5, -1.5) * radius1 * pixelsize);
	bloom_sum1 += TextureColor.Sample(Sampler0, coord + float2(-1.5, -1.5) * radius1 * pixelsize);
	bloom_sum1 += TextureColor.Sample(Sampler0, coord + float2( 1.5,  1.5) * radius1 * pixelsize);
	bloom_sum1 += TextureColor.Sample(Sampler0, coord + float2(-1.5,  1.5) * radius1 * pixelsize);
	bloom_sum1 += TextureColor.Sample(Sampler0, coord + float2( 0.0, -2.5) * radius1 * pixelsize);
	bloom_sum1 += TextureColor.Sample(Sampler0, coord + float2( 0.0,  2.5) * radius1 * pixelsize);
	bloom_sum1 += TextureColor.Sample(Sampler0, coord + float2(-2.5,  0.0) * radius1 * pixelsize);
	bloom_sum1 += TextureColor.Sample(Sampler0, coord + float2( 2.5,  0.0) * radius1 * pixelsize);

	bloom_sum1 *= 0.005;

	float3 bloom_sum2 = TextureColor.Sample(Sampler0, coord + float2(1.5, -1.5) * radius2 * pixelsize);
	bloom_sum2 += TextureColor.Sample(Sampler0, coord + float2(-1.5, -1.5) * radius2 * pixelsize);
	bloom_sum2 += TextureColor.Sample(Sampler0, coord + float2( 1.5,  1.5) * radius2 * pixelsize);
	bloom_sum2 += TextureColor.Sample(Sampler0, coord + float2(-1.5,  1.5) * radius2 * pixelsize);
	bloom_sum2 += TextureColor.Sample(Sampler0, coord + float2( 0.0, -2.5) * radius2 * pixelsize);	
	bloom_sum2 += TextureColor.Sample(Sampler0, coord + float2( 0.0,  2.5) * radius2 * pixelsize);
	bloom_sum2 += TextureColor.Sample(Sampler0, coord + float2(-2.5,  0.0) * radius2 * pixelsize);
	bloom_sum2 += TextureColor.Sample(Sampler0, coord + float2( 2.5,  0.0) * radius2 * pixelsize);

	bloom_sum2 *= 0.010;

	float dist = radius2 - radius1;
	float3 HDR = (color + (bloom_sum2 - bloom_sum1)) * dist;
	float3 blend = HDR + color;
	color = pow(abs(blend), abs(HDRPower)) + HDR; // pow - don't use fractions for HDRpower
	
	return saturate(color);
	}
	else
	return color;
}
// ---- end include Shaders/fakeHDR.fxh ----

#endif
#if (INC_Shadow==1)
// ---- begin include Shaders/Shadows.fxh ----
//=======================//
// Based on ECC by Boris //
// Lightness by Prod80   //
//=======================//

float4 Shadows(float4 color)
{
    if (USE_Shadows==true)
	{
	float	tempgray;
	float4	tempvar;
	
	//DNI Seperation
	float  ECCGamma                  =lerp( lerp(ECCGamma_Night,                  ECCGamma_Day,                  ENightDayFactor), ECCGamma_Interior,                  EInteriorFactor );
	float  ECCInBlack                =lerp( lerp(ECCInBlack_Night,                ECCInBlack_Day,                ENightDayFactor), ECCInBlack_Interior,                EInteriorFactor );
	float  ECCInWhite                =lerp( lerp(ECCInWhite_Night,                ECCInWhite_Day,                ENightDayFactor), ECCInWhite_Interior,                EInteriorFactor );
	float  ECCOutBlack               =lerp( lerp(ECCOutBlack_Night,               ECCOutBlack_Day,               ENightDayFactor), ECCOutBlack_Interior,               EInteriorFactor );
	float  ECCOutWhite               =lerp( lerp(ECCOutWhite_Night,               ECCOutWhite_Day,               ENightDayFactor), ECCOutWhite_Interior,               EInteriorFactor );
	float  ECCDesaturateShadows      =lerp( lerp(ECCDesaturateShadows_Night,      ECCDesaturateShadows_Day,      ENightDayFactor), ECCDesaturateShadows_Interior,      EInteriorFactor );
	float2 Lightness		         =lerp( lerp(float2(LightnessN, ShadowsN), float2(LightnessD, ShadowsD),     ENightDayFactor ), float2(LightnessI, ShadowsI),      EInteriorFactor );
	
	color=max(color-ECCInBlack, 0.0) / max(ECCInWhite-ECCInBlack, 0.0001);
	if (ECCGamma!=1.0) color=pow(color, ECCGamma);
	color=color*(ECCOutWhite-ECCOutBlack) + ECCOutBlack;
	
	// desaturate shadows
	tempgray=dot(color.xyz, 0.3333);
	tempvar.x=saturate(1.0-tempgray);
	tempvar.x*=tempvar.x;
	tempvar.x*=tempvar.x;
	color=lerp(color, tempgray, ECCDesaturateShadows*tempvar.x);

	color.xyz		= saturate( color.xyz );
	color.xyz		= RGBToHSL( color.xyz );
	color.z			= color.z + (( 1 - color.z ) * ( Lightness.x * color.z ));
	color.z			= color.z + (( 1 - color.z ) * ( Lightness.y * ( 1 - color.z )));
	color.xyz		= HSLToRGB( color.xyz );
	
	}
	return color;
}
// ---- end include Shaders/Shadows.fxh ----

#endif
#if (INC_FishEye==1)
// ---- begin include Shaders/FishEye.fxh ----
//=============================================================//
// icelaglace, a.o => (ported from some blog, author unknown)  //
// mastereffect by Marty McFly                                 //
// ReShade 3 port by Insomnia                                  //
// Iddqd combined Horizontal and Vertical Fisheye (Switchable) //
// ENB port by Adyss                                           //
//=============================================================//

float3 FISHEYE(float3 color, float2 coord)
{
 
    if (USE_FISH==true)
	{
/*	
    float4 coord=0.0;
    coord.xy=IN.txcoord0.xy;
    coord.w=0.0;
*/
    color.rgb = 0.0;
     
    float3 eta = float3(1.0+fFisheyeColorshift*0.9,1.0+fFisheyeColorshift*0.6,1.0+fFisheyeColorshift*0.3);
    float2 center;
    center.x = coord.x-0.5;
    center.y = coord.y-0.5;
    float LensZoom = 1.0/fFisheyeZoom;
 
    float r2;// + (coord.y-0.5) * (coord.y-0.5);
 
    if(iFisheyeMod == 0)
    {
         r2 = (coord.y-0.5) * (coord.y-0.5);
    }
    else if (iFisheyeMod == 1)
    {
        r2 = (coord.x-0.5) * (coord.x-0.5);
    }
    else
    {
        r2 = (coord.y-0.5) * (coord.y-0.5) + (coord.y-0.5) * (coord.y-0.5);
    }
 
 
    float f = 0;
 
    if( fFisheyeDistortionCubic == 0.0){
        f = 1 + r2 * fFisheyeDistortion;
    }else{
                f = 1 + r2 * (fFisheyeDistortion + fFisheyeDistortionCubic * sqrt(r2));
    };
 
    float x = f*LensZoom*(coord.x-0.5)+0.5;
    float y = f*LensZoom*(coord.y-0.5)+0.5;
    float2 rCoords = (f*eta.r)*LensZoom*(center.xy*0.5)+0.5;
    float2 gCoords = (f*eta.g)*LensZoom*(center.xy*0.5)+0.5;
    float2 bCoords = (f*eta.b)*LensZoom*(center.xy*0.5)+0.5;
   
    color.x = TextureColor.Sample(Sampler0,rCoords).r;
    color.y = TextureColor.Sample(Sampler0,gCoords).g;
    color.z = TextureColor.Sample(Sampler0,bCoords).b;
   
    }   
    return color.rgb;
 
}
// ---- end include Shaders/FishEye.fxh ----

#endif
#if (INC_Emboss==1)
// ---- begin include Shaders/Emboss.fxh ----
//==================================//
// Full credits to the ReShade team //
// ReShade 3 port by Insomnia       //
//==================================//

float3 Emboss(float3 color, float2 coord)
{
    if (USE_Emboss==true)
	{
    float2 offset;
	sincos(radians( iEmbossAngle), offset.y, offset.x);
	float3 col1 = TextureColor.Sample(Sampler0, coord - PixelSize*fEmbossOffset*offset).rgb;
	float3 col2 = color.rgb;
	float3 col3 = TextureColor.Sample(Sampler0, coord + PixelSize*fEmbossOffset*offset).rgb;
	
	float3 colEmboss = col1 * 2.0 - col2 - col3;

	float colDot = max(0,dot(colEmboss, 0.333))*fEmbossPower;

	float3 colFinal = col2 - colDot;

	float luminance = dot( col2, float3( 0.6, 0.2, 0.2 ) );

	color.xyz = lerp( colFinal, col2, luminance * luminance ).xyz;
	
	}
	return color;
}


// ---- end include Shaders/Emboss.fxh ----

#endif
#if (INC_SBloom==1)
// ---- begin include Shaders/SweetBloom.fxh ----
//======================================//
// SweetFX Bloom by CeeJay.dk (I guess) //
//======================================//

float4 BloomPass(float4 color, float2 coord)
{
    if (USE_SBloom==true) {
	
	// DNI seperation
	float BloomThreshold   =lerp( lerp(BloomThreshold_Night,   BloomThreshold_Day,   ENightDayFactor), BloomThreshold_Interior,   EInteriorFactor );
	float BloomPower       =lerp( lerp(BloomPower_Night,       BloomPower_Day,       ENightDayFactor), BloomPower_Interior,       EInteriorFactor );
	float BloomWidth       =lerp( lerp(BloomWidth_Night,       BloomWidth_Day,       ENightDayFactor), BloomWidth_Interior,       EInteriorFactor );
	
	float3 BlurColor2 = 0;
	float3 Blurtemp = 0;
	float MaxDistance = 8*BloomWidth; //removed sqrt
	float CurDistance = 0;
	
	float Samplecount = 25.0;
	
	float2 pixelsize = ScreenSize.y;
	pixelsize.y *= ScreenSize.z;
	
	float2 blurtempvalue = coord * pixelsize * BloomWidth;
	
	
	float2 BloomSample = float2(2.5,-2.5);
	float2 BloomSampleValue; // = BloomSample;
	
	for(BloomSample.x = (2.5); BloomSample.x > -2.0; BloomSample.x = BloomSample.x - 1.0) // runs 5 times
	{
        BloomSampleValue.x = BloomSample.x * blurtempvalue.x;
        float2 distancetemp = BloomSample.x * BloomSample.x * BloomWidth;
        
		for(BloomSample.y = (- 2.5); BloomSample.y < 2.0; BloomSample.y = BloomSample.y + 1.0) // runs 5 ( * 5) times
		{
            distancetemp.y = BloomSample.y * BloomSample.y;
			CurDistance = (distancetemp.y * BloomWidth) + distancetemp.x; //removed sqrt
			
			BloomSampleValue.y = BloomSample.y * blurtempvalue.y;
			Blurtemp.rgb = TextureColor.Sample(Sampler0, float2(coord + BloomSampleValue)).rgb; //same result - same speed.
			
			BlurColor2.rgb += lerp(Blurtemp.rgb,color.rgb, sqrt(CurDistance / MaxDistance)); //reduced number of sqrts needed
		}
	}
	BlurColor2.rgb = (BlurColor2.rgb / (Samplecount - (BloomPower - BloomThreshold*5))); //check if using MAD
	float Bloomamount = (dot(color.rgb,float3(0.299f, 0.587f, 0.114f))) ; //try BT 709
	float3 BlurColor = BlurColor2.rgb * (BloomPower + 4.0); //check if calculated offline and combine with line 24 (the blurcolor2 calculation)

	color.rgb = lerp(color.rgb,BlurColor.rgb, Bloomamount);	

	return saturate(color);
	}
	else
	return color; //do i need an else here??
}

// ---- end include Shaders/SweetBloom.fxh ----

#endif

// ---- begin include Shaders/Dither.fxh ----
// JawZ: Author and developer of MSL //


float3 msDither(float3 color, float2 txcoord0) {
  if (ENABLE_DITHER==true) {  /// Activates if ENABLE_DITHER = true
    float dither_bit = 8.0;  /// Number of bits per channel. Should be 8 for most monitors.

    /// Calculate grid position
      float grid_position = frac(dot(txcoord0, (ScreenSize.x) * float2(0.75, 0.5) + (0.00025)));  // (0.6,0.8) is good too - TODO : experiment with values

    /// Calculate how big the shift should be
      float dither_shift = (0.25) * (1.0 / (pow(2, dither_bit) - 1.0));              /// 0.25 seems good both when using math and when eyeballing it. So does 0.75 btw.
      dither_shift = lerp(2.0 * dither_shift, -2.0 * dither_shift, grid_position);  /// Shift according to grid position.

    /// Shift the color by dither_shift
      color.rgb += float3(dither_shift, -dither_shift, dither_shift);  /// Subpixel dithering


    }

  return color;
}
// ---- end include Shaders/Dither.fxh ----

// ---- begin include Shaders/TempAdjust.fxh ----
//=========================================//
// Ripped of from Lightroom by Marty McFly //
//=========================================//
float4 TEMP(float4 color)
{
	color.xyz = saturate(color.xyz);
	
	//TEMPERATURE AND TINT - looking for better alternatives ..
	float3 ColdKelvinColor = HSL2RGB(float3(0.56111,1.0,0.5));
	float3 WarmKelvinColor = HSL2RGB(float3(0.06111,1.0,0.5));

	float3 TempKelvinColor = lerp(ColdKelvinColor, WarmKelvinColor, GlobalTemperature*0.5+0.5);

	float oldLuma = RGB2HSL(color.xyz).z;
	float3 tintedColor = color.xyz * TempKelvinColor / dot(TempKelvinColor,float3(0.299,0.587,0.114)); //just using old luma does not work for some reason and weirds out colors.
	color.xyz = HSL2RGB(float3(RGB2HSL(tintedColor.xyz).xy,oldLuma));

	return color;
}
// ---- end include Shaders/TempAdjust.fxh ----

// ---- begin include Shaders/Lift.fxh ----
// These adjust what the Drop/Lift Checkmarks ingame do

#define LIFTGamma    1
#define LIFTInBlack  0
#define LIFTInWhite  1
#define LIFTOutBlack 0.06
#define LIFTOutWhite 1

#define DROPGamma    1
#define DROPInBlack  0.06
#define DROPInWhite  1
#define DROPOutBlack 0
#define DROPOutWhite 1


float4 Lift(float4 color)
{
    if (LIFTNAO==true)
	{
	color=max(color-LIFTInBlack, 0.0) / max(LIFTInWhite-LIFTInBlack, 0.0001);
	if (LIFTGamma!=1.0) color=pow(color, LIFTGamma);
	color=color*(LIFTOutWhite-LIFTOutBlack) + LIFTOutBlack;
	}
	if (DROPNAO==true)
	{
	color=max(color-DROPInBlack, 0.0) / max(DROPInWhite-DROPInBlack, 0.0001);
	if (DROPGamma!=1.0) color=pow(color, DROPGamma);
	color=color*(DROPOutWhite-DROPOutBlack) + DROPOutBlack;
	}
	return color;
}
// ---- end include Shaders/Lift.fxh ----





//=======================Start of Color Pixel Shader============================//
float4	PS_Colors(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{

	float2 coord = IN.txcoord0;
	float4 color = TextureColor.Sample(Sampler0, coord.xy);

#if (INC_Reinhard==1)
	color.rgb = Reinhard(color.rgb);         // Linear Reinhard tone
#endif
#if (INC_Reinhard==2)
	color.rgb = ReinhardPass(color.rgb);     // Basic Reinhard tone
#endif
#if (INC_Spherical==1)
	color.rgb = Spherical(color.rgb);        // Spherical tone
#endif
#if (INC_Curves==1)
	color.rgb = Curves(color);               // Curves
#endif
#if (INC_Shadow==1)
	color.rgb = Shadows(color);              // Shadow Adjustments
#endif
#if (INC_DPX==1)
	color.rgb = DPX(color.rgb);              // DPX
#endif
#if (INC_Filmpass==1)
	color.rgb = filmpass(color.rgb);         // Filmpass
#endif	
#if (INC_Vibrance==1)
	color.rgb = Vibrance(color.rgb);         // Vibrance
#endif
#if (INC_Technicolor==1)
	color.rgb = Technicolor(color);          // Techicolor
#endif
#if (INC_Technicolor2==1)
	color.rgb = Technicolor2(color);         // Techicolor 2 Strip
#endif
#if (INC_Tint==1)
	color.rgb = Tint(color);                 // Tint
#endif
#if (INC_HDR==1)
	color.rgb = HDR(color, coord.xy);        // Fake HDR
#endif
#if (INC_SBloom==1)
    color.rgb = BloomPass(color, coord);
#endif

    // Global Adjustments
    color.rgb = TEMP(color);                 // Global Temperature Adjustments
	color.rgb = Lift(color);                 // Drop/Lift of Shadows
	color *= pow(2.0f, ExposureGOB);

	return color;
}


//=============Last Pass=============//
float4	PS_Image(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	float2 coord = IN.txcoord0;
	float4 color = TextureColor.Sample(Sampler0, coord.xy);
	
	color.rgb = LUTApply(color.rgb);
	
#if (INC_Emboss==1)
	color.rgb = Emboss(color, coord);
#endif
	
#if (INC_FishEye==1)
	color.rgb = FISHEYE(color, coord); //Degrades colors for some reason...
#endif

    color.rgb = msDither(color, coord);
	
#if (INC_Letterbox==1)
    color.rgb = Border(color.rgb, coord.xy); // Letterbox
#endif
	
	return color;
}



// ---- begin include Shaders/Sharps.fxh ----
//========================//
// LumaSharp by Ceejay.dk //
// ENB port by Sonnhy     //
//========================//

#if (INC_LumaSHARP==1)
float4	PS_LumaSharp(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	// float4 TextureOriginal.Sample(Sampler0, IN.txcoord0.xy) = float3 tex2D(ReShade::BackBuffer, tex).rgb
	float4 ori = TextureOriginal.Sample(Sampler0, IN.txcoord0.xy); // ori = original pixel
	float2 coord = IN.txcoord0;
	if (USE_LumaSharp==true)
	{

	float2 pixelsize = ScreenSize.y;
	pixelsize.y *= ScreenSize.z;

	float3 sharp_strength_luma = (CoefLuma * LSharpStrength);

	float4 blur_ori;
	
	// Pattern 1 -- A (fast) 7 tap gaussian using only 2+1 texture fetches.
	if (LSharpPattern == 0) {

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + (pixelsize / 3.0) * LSharpOffsetBias);  // North West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + (-pixelsize / 3.0) * LSharpOffsetBias); // South East

		blur_ori /= 2;  //Divide by the number of texture fetches

		sharp_strength_luma *= 1.5; // Adjust strength to aproximate the strength of pattern 2
	}

	// Pattern 2 -- A 9 tap gaussian using 4+1 texture fetches.
	if (LSharpPattern == 1)
	{

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + float2(pixelsize.x, -pixelsize.y) * 0.5 * LSharpOffsetBias); // South East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy - pixelsize * 0.5 * LSharpOffsetBias);  // South West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * 0.5 * LSharpOffsetBias); // North East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy - float2(pixelsize.x, -pixelsize.y) * 0.5 * LSharpOffsetBias); // North West

		blur_ori *= 0.25;  // ( /= 4) Divide by the number of texture fetches
	}

	// Pattern 3 -- An experimental 17 tap gaussian using 4+1 texture fetches.
	if (LSharpPattern == 2)
	{

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * float2(0.4, -1.2) * LSharpOffsetBias);  // South South East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * float2(1.2, 0.4) * LSharpOffsetBias); // West South West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * float2(1.2, 0.4) * LSharpOffsetBias); // East North East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * float2(0.4, -1.2) * LSharpOffsetBias); // North North West

		blur_ori *= 0.25;  // ( /= 4) Divide by the number of texture fetches

		sharp_strength_luma *= 0.51;
	}

	// Pattern 4 -- A 9 tap high pass (pyramid filter) using 4+1 texture fetches.
	if (LSharpPattern == 3)
	{

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + float2(0.5 * pixelsize.x, -pixelsize.y * LSharpOffsetBias));  // South South East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + float2(LSharpOffsetBias * -pixelsize.x, 0.5 * -pixelsize.y)); // West South West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + float2(LSharpOffsetBias * pixelsize.x, 0.5 * pixelsize.y)); // East North East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + float2(0.5 * -pixelsize.x, pixelsize.y * LSharpOffsetBias)); // North North West

		//blur_ori += (2 * ori); // Probably not needed. Only serves to lessen the effect.

		blur_ori /= 4.0;  //Divide by the number of texture fetches

		sharp_strength_luma *= 0.666; // Adjust strength to aproximate the strength of pattern 2
	}

	// Calculate the sharpening
	float4 sharp = ori - blur_ori;  //Subtracting the blurred image from the original image

	float4 sharp_strength_luma_clamp = float4(sharp_strength_luma * (0.5 / LSharpClamp), 0.5);
	sharp.w = 1.0;
	float sharp_luma = saturate( dot(sharp, sharp_strength_luma_clamp) );
	sharp_luma = (LSharpClamp * 2.0) * sharp_luma - LSharpClamp;


	float4 outputcolor = ori + sharp_luma;

	return saturate(outputcolor);
	}
	else
	return ori;
}
#endif

//===================================================================//
// Filmic Anamorph Sharpen PS v1.1.5 (c) 2018 Jacob Maximilian Fober //
// This work is licensed under the Creative Commons                  //
// Attribution-ShareAlike 4.0 International License.                 //
// To view a copy of this license, visit                             //
// http://creativecommons.org/licenses/by-sa/4.0/.                   //
//===================================================================//
// Not sure about the Depth part :/ halp plis
#if (INC_FilmicAnamorphSharp==1)
float3	PS_FilmicAnamorphSharp(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	float2 Pixel = PixelSize;
	float2 UvCoord = IN.txcoord0;

	float2 DepthPixel = Pixel * float(FASOffset + 1);
	Pixel *= float(FASOffset);
	// Sample display image
	float3 Source = TextureColor.Sample(Sampler0, UvCoord).rgb;
	// Sample display depth image
	float SourceDepth = TextureDepth.Sample(Sampler1, UvCoord);

	float2 NorSouWesEst[4] = {
		float2(UvCoord.x, UvCoord.y + Pixel.y),
		float2(UvCoord.x, UvCoord.y - Pixel.y),
		float2(UvCoord.x + Pixel.x, UvCoord.y),
		float2(UvCoord.x - Pixel.x, UvCoord.y)
	};

	float2 DepthNorSouWesEst[4] = {
		float2(UvCoord.x, UvCoord.y + DepthPixel.y),
		float2(UvCoord.x, UvCoord.y - DepthPixel.y),
		float2(UvCoord.x + DepthPixel.x, UvCoord.y),
		float2(UvCoord.x - DepthPixel.x, UvCoord.y)
	};

	// Choose luma coefficient, if True BT.709 Luma, else BT.601 Luma
	float3 LumaCoefficient = float3( 0.2126,  0.7152,  0.0722);

	// Luma high-pass color
	float HighPassColor =
	   dot(TextureColor.Sample(Sampler0, NorSouWesEst[0]).rgb, LumaCoefficient)
	 + dot(TextureColor.Sample(Sampler0, NorSouWesEst[1]).rgb, LumaCoefficient)
	 + dot(TextureColor.Sample(Sampler0, NorSouWesEst[2]).rgb, LumaCoefficient)
	 + dot(TextureColor.Sample(Sampler0, NorSouWesEst[3]).rgb, LumaCoefficient);
	HighPassColor = 0.5 - 0.5 * (HighPassColor * 0.25 - dot(Source, LumaCoefficient));
	
	// Luma high-pass depth
	float DepthMask =
	   TextureDepth.Sample(Sampler1, DepthNorSouWesEst[0])
	 + TextureDepth.Sample(Sampler1, DepthNorSouWesEst[1])
	 + TextureDepth.Sample(Sampler1, DepthNorSouWesEst[2])
	 + TextureDepth.Sample(Sampler1, DepthNorSouWesEst[3])
	 + TextureDepth.Sample(Sampler1, NorSouWesEst[0])
	 + TextureDepth.Sample(Sampler1, NorSouWesEst[1])
	 + TextureDepth.Sample(Sampler1, NorSouWesEst[2])
	 + TextureDepth.Sample(Sampler1, NorSouWesEst[3]);
	DepthMask = 1.0 - DepthMask * 0.125 + SourceDepth;
	DepthMask = min(1.0, DepthMask) + 1.0 - max(1.0, DepthMask);
	DepthMask = saturate(FASContrast * DepthMask + 1.0 - FASContrast);

	// Sharpen strength
	HighPassColor = lerp(0.5, HighPassColor, FASStrength * DepthMask);

	// Clamping sharpen
	HighPassColor = max(min(HighPassColor, FASClamp), 1 - FASClamp);

	float3 Sharpen = float3(
		Overlay(Source.r, HighPassColor),
		Overlay(Source.g, HighPassColor),
		Overlay(Source.b, HighPassColor)
	);

	return Sharpen;
}
#endif

//======================//
// Basic Sharp by Boris //
//======================//
#if (INC_BasicSharp==1)
float4	PS_BSharp(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	float4	res;
	float4	color;
	float4	centercolor;
	float2	pixeloffset=ScreenSize.y;
	pixeloffset.y*=ScreenSize.z;

	centercolor=TextureColor.Sample(Sampler0, IN.txcoord0.xy);
	color=0.0;
	float2	offsets[4]=
	{
		float2(-1.0,-1.0),
		float2(-1.0, 1.0),
		float2( 1.0,-1.0),
		float2( 1.0, 1.0),
	};
	for (int i=0; i<4; i++)
	{
		float2	coord=offsets[i].xy * pixeloffset.xy * ESharpRange + IN.txcoord0.xy;
		color.xyz+=TextureColor.Sample(Sampler1, coord.xy);
	}
	color.xyz *= 0.25;

	float	diffgray=dot((centercolor.xyz-color.xyz), 0.3333);
	res.xyz=ESharpAmount * centercolor.xyz*diffgray + centercolor.xyz;

	res.w=1.0;
	return res;
}
#endif
/*
//=============================//
// UnSharp Mask by Marty McFly //
//=============================//
// Dosnt compile (i suck lol)
float4	UNSharp(float4 color, float2 coord)
{
	float4 blurred = 0.0;

	int iStepcount = iSharpStepCount;
	float deviation = (float)iStepcount * 0.4;
	float norm = -rcp(2.0*deviation*deviation);

	float2 offset;
	float3 sample;

	float2 stepsize = PixelSize.xy * fSharpStepSize;

	[loop]
	for(int iStepsX=-iStepcount; iStepsX<=iStepcount; iStepsX++)
	{
		[loop]
		for(int iStepsY=-iStepcount; iStepsY<=iStepcount; iStepsY++)
		{
			float2 cOffset = float2(iStepsX,iStepsY);
			sample = (color, coord.xy + cOffset * stepsize,0);
			float weight = exp(dot(cOffset,cOffset)*norm);
			blurred.xyz += sample * weight;
			blurred.w += weight;
		}
	}

	blurred.xyz /= blurred.w;

	float4 res =  (color, coord.xy);
	float3 sharp = res.xyz - blurred.xyz;
	float sharp_luma = dot(sharp,fSharpAmount);

	sharp_luma = clamp(sharp_luma, -fSharpClamp, fSharpClamp);

	res.xyz = bSharpVisualize ? saturate(0.5 + 4*sharp_luma) : saturate(res.xyz + sharp_luma);

	return res;
}
*/
// ---- end include Shaders/Sharps.fxh ----
 

#if (INC_GaussBloom==1)
// ---- begin include Shaders/GaussBloom.fxh ----
//===================================//
// Gaussian Postpass Bloom by Prod80 //
//===================================//

float4 PS_ProcessGaussianH(VS_OUTPUT_POST IN) : SV_Target
{

   float4 dis_out = TextureColor.Sample(Sampler0, IN.txcoord0.xy);
   if (USE_GaussBloom==true) {
   float4 color      =   0.0;
   float sHeight      =   ScreenSize.x * ScreenSize.w;
   float2 fvTexelSize    =    float2(ScreenSize.y, 1.0 / sHeight);
   float px          =    fvTexelSize.x; 
   float py          =    fvTexelSize.y; 
   
   if ( gauss_blur==1 )
   {
   color       = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_1[0];
   for(int i = 1; i < 3; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(sampleOffsets_1[i]*px, 0.0)) * sampleWeights_1[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(sampleOffsets_1[i]*px, 0.0)) * sampleWeights_1[i];
      }
   }
   if ( gauss_blur==2 )
   {
   color       = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_2[0];
   for(int i = 1; i < 5; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(sampleOffsets_2[i]*px, 0.0)) * sampleWeights_2[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(sampleOffsets_2[i]*px, 0.0)) * sampleWeights_2[i];
      }
   }
   if ( gauss_blur==3 )
   {
   color       = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_3[0];
   for(int i = 1; i < 6; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(sampleOffsets_3[i]*px, 0.0)) * sampleWeights_3[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(sampleOffsets_3[i]*px, 0.0)) * sampleWeights_3[i];
      }
   }
   color.w            = 1.0f;
   return color;
   }
   else
   return dis_out;
}

float4 PS_ProcessGaussianV(VS_OUTPUT_POST IN) : SV_Target
{
   float4 dis_out = TextureColor.Sample(Sampler0, IN.txcoord0.xy);
   if (USE_GaussBloom==true) {
   float4 color      =   0.0;
   float sHeight      =   ScreenSize.x * ScreenSize.w;
   float2 fvTexelSize    =    float2(ScreenSize.y, 1.0 / sHeight);
   float px          =    fvTexelSize.x; 
   float py          =    fvTexelSize.y; 
   
   if ( gauss_blur==1 )
   {
   color = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_1[0];
   for(int i = 1; i < 3; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(0.0, sampleOffsets_1[i]*py)) * sampleWeights_1[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(0.0, sampleOffsets_1[i]*py)) * sampleWeights_1[i];
      }
   }
   if ( gauss_blur==2 )
   {
   color = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_2[0];
   for(int i = 1; i < 5; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(0.0, sampleOffsets_2[i]*py)) * sampleWeights_2[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(0.0, sampleOffsets_2[i]*py)) * sampleWeights_2[i];
      }
   }
   if ( gauss_blur==3 )
   {
   color = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_3[0];
   for(int i = 1; i < 6; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(0.0, sampleOffsets_3[i]*py)) * sampleWeights_3[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(0.0, sampleOffsets_3[i]*py)) * sampleWeights_3[i];
      }
   }
   color.w            = 1.0f;
   return color;
   }
   else
   return dis_out;
   
}

float4 PS_ProcessSoftLight(VS_OUTPUT_POST IN) : SV_Target
{
   float4 blendC   = TextureColor.Sample(Sampler0, IN.txcoord0.xy);
   if (USE_GaussBloom==true) {
   float4 color      =   0.0;
   float4 baseC   = TextureOriginal.Sample(Sampler0, IN.txcoord0.xy);
   
   float3 base      = baseC.xyz;
   float3 blend   = blendC.xyz;
   
   float sl_mix_set   =lerp( lerp(sl_mix_set_Night,   sl_mix_set_Day,   ENightDayFactor), sl_mix_set_Interior,   EInteriorFactor );
   
   color.xyz      = softlight( base, blend, sl_mix_set );
   color.w         = 1.0f;

   return color;
   }
   else
   return blendC;
}

float4 PS_ProcessGaussBloom(VS_OUTPUT_POST IN) : SV_Target
{
   float4 blendC   = TextureColor.Sample(Sampler0, IN.txcoord0.xy);
   if (USE_GaussBloom==true) {
   float4 scrcolor   = 0.0;
   float3 luma    = float3(0.2125, 0.7154, 0.0721);
   float pixluma   = 0.0;
   float4 baseC   = TextureOriginal.Sample(Sampler0, IN.txcoord0.xy);
   float4 color   = 0.0;
   
   float3 base      = baseC.xyz;
   float3 blend   = blendC.xyz;
   
   scrcolor.xyz   = screen( base, blend );
   
   float gauss_bloom   =lerp( lerp(gauss_bloom_Night,   gauss_bloom_Day,   ENightDayFactor), gauss_bloom_Interior,   EInteriorFactor );
   
   //Bloom on luma
   if (lumabloom==true)
   {
      if (lumasource==1) pixluma = dot( base, luma );
      if (lumasource==2) pixluma = dot( blend, luma );
      if (lumasource==3) pixluma = dot( scrcolor, luma );
   color.xyz      = lerp( base.xyz, scrcolor.xyz, gauss_bloom * pixluma );
   };
   if (lumabloom==false)
   {
   color.xyz      = lerp( base.xyz, scrcolor.xyz, gauss_bloom );
   };
   
   float3   lumCoeff = float3(0.212656, 0.715158, 0.072186);     
   color.a = dot(lumCoeff, color.rgb);
   
   color.w         = 1.0f;
   return color;
   }
   else
   return blendC;
}
// ---- end include Shaders/GaussBloom.fxh ----
 
#endif

//============//
// Techniques //
//============//

// ---- begin include Setup/TechniquesSetup.fxh ----
/*
A postpass can have multiple passes after each other. This can be really tricky to do. So feel free to ask on the forum or on my discord: https://discord.gg/sWunDwj
Basically here you arrange what passes and when. After a pass happend the next one works with the result of the last one.
Some passes like sharp (in some cases) can conflict with others and should come before the others.
Also some passes need the imput of one of the previous ones (like bloom in this case. 

the first pass has a few infos that is important for all the others

            | gives your postpass a codename. passes that come after that one need to be named MyPostPass1 ... 2 ... 3  and so on | | only witten at the fist pass. (Gives it the ingame name. Change in Shadersetup and not here |
technique11 |                                                     MyPostPass                                                      | |                                <string UIName= postpassname;>                               |
{
  pass p0
    {                  | Here it sets what this pass does. VS = Vertex shader   PS = Pixel Shader (important for you) these two get comiled here |
       SetVertexShader |                                 (CompileShader(vs_5_0, VS_PostProcess()));                                              |
       SetPixelShader  |                                 (CompileShader(ps_5_0, PS_Colors()));                                                   |
    }
}

in the end it should look like this:

technique11 MyPostPass <string UIName= postpassname;>
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Colors()));
    }
}


technique11 MyPostPass1
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Image()));
    }
}


=============== Here comes a list of Possible passes: ====================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Colors()));
    }
}

PS_Colors is were most of the Coloring Shaders are in. I reccoment setting it almost at the end of your passes
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Image()));
    }
}
ALWAYS should be the last of all passes. Otherwise there can be conflicting.
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_LumaSharp()));
    }
}
Place really early. Needs "#define INC_LumaSHARP" to be 1
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_FilmicAnamorphSharp()));
    }
}
 Needs "#define INC_FilmicAnamorphSharp" to be 1
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_BSharp()));
    }
}
 Needs "#define INC_BasicSharp" to be 1
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_Lightroom()));
       SetPixelShader (CompileShader(ps_5_0, PS_Lightroom()));
    }
}
 Needs "#define INC_Lightroom" to be 1
==========================================================================


==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianH()));
    }
}


technique11 post1
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianV()));
    }
}

technique11 post2
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessSoftLight()));
    }
}

technique11 post3
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianH()));
    }
}

technique11 post4
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianV()));
    }
}

technique11 post5
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussBloom()));
    }
}

 Needs "#define INC_GaussBloom" to be 1
 Always should look like that as a process. I reccoment setting these passes first

==========================================================================


======================DRAW YOUR TECHNIQUES HERE===========================
*/

technique11 MyPostPass <string UIName= postpassname;>
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Colors()));
    }
}


technique11 MyPostPass1
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Image()));
    }
}


technique11 MyPostPass2
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_FilmicAnamorphSharp()));
    }
}










































/* Example config of mine i used on screenshots like: https://www.flickr.com/photos/157466996@N07/27211402927/in/dateposted-public/
technique11 gallery <string UIName= postpassname;>
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianH()));
    }
}


technique11 gallery1
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianV()));
    }
}

technique11 gallery2
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessSoftLight()));
    }
}

technique11 gallery3
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianH()));
    }
}

technique11 gallery4
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianV()));
    }
}

technique11 gallery5
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussBloom()));
    }
}

technique11 gallery6
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_FilmicAnamorphSharp()));
    }
}

technique11 gallery7
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_VSharp()));
    }
}

technique11 gallery8
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Colors()));
    }
}

technique11 gallery10
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Image()));
    }
}
*/
// ---- end include Setup/TechniquesSetup.fxh ----

