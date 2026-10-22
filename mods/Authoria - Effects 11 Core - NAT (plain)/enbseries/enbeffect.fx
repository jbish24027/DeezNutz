/* 
/////////////////////////////////////////////////////////
//                ENBSeries effect file                //
//         visit http://enbdev.com for updates         //
//       Copyright (c) 2007-2018 Boris Vorontsov       //
//----------------------ENB PRESET---------------------//
			
		 NATURAL LIGHTING & ATMOSPHERIC FOR ENB
				   - SPECIAL EDITION- 
					     3.1.1C
					RELEASE BUILD
//-----------------------CREDITS-----------------------//
// Boris: For ENBSeries and his knowledge and codes    //
// Prod80:	Author of original RGB correction shader   //
// 													   //
// L00 :  Shader Setup, Additional shaders,            //
// 		  Presets and Settings, Port,                  //
//        Modifications and author of this file        //
//                                                     //
//     Please do not redistribute without credits      //
///////////////////////////////////////////////////////// 
*/

int		Empty00							<string UIName=" NAT.ENB: 3.1.1C ";		string UIWidget="Spinner";float UIMin=0;float UIMax=0;> = {0};
int		Empty05						 	<string UIName=" Pick a render mode from TECHNIQUE ^ ";			string UIWidget="Spinner";float UIMin=0;float UIMax=0;> = {100};
int		Empty01						 	<string UIName=" ";						string UIWidget="Spinner";float UIMin=0;float UIMax=0;> = {0};
bool 	NoiseEnable 					<string UIName ="Grain";> = {true};
int		iSharpStyle 					<string UIName="Sharpening"; 			string UIWidget="dropdown";string UIList="Off, Soft, Sharp, Wide";int UIMin=0;int UIMax=3;>;
bool 	bUseLensDistortion 				<string UIName="Lens Distortion"; > = {true};
bool 	bUseVignette 					<string UIName="Vignette"; > = {true};
float 	border_ratio 					<string UIName="Letterbox ";			string UIWidget="Spinner";float UIMin=0.0;float UIMax=10.00;float UIStep=0.05;> = {2.35};
int		Empty02						 	<string UIName="  ";					string UIWidget="Spinner";float UIMin=0;float UIMax=0;> = {0};

//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
// EXTERNAL PARAMETERS BEGINS HERE, SHOULD NOT BE MODIFIED UNLESS YOU KNOW WHAT YOU ARE DOING
//++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
/* bool 	btest 		<string UIName="btest"; > = {true};
float 	ftest 		<string UIName="test"; string UIWidget="Spinner";  float UIMin=0.0;  float UIMax=10000000000.0;  float UIStep=0.001;> = {1.0};
//bool 	btest2 		<string UIName="btest2"; > = {true};
bool 	btest3 		<string UIName="btest3"; > = {true};
float 	ftest2 		<string UIName="test2"; string UIWidget="Spinner";  float UIMin=0.0;  float UIMax=10000000000.0;  float UIStep=0.001;> = {1.0};
float 	KeyValue 		<string UIName="KeyValue"; string UIWidget="Spinner";  float UIMin=-10000000000.0;  float UIMax=10000000000.0;  float UIStep=0.0001;> = {1.0};
float 	ftest3 		<string UIName="test3"; string UIWidget="Spinner";  float UIMin=0.0;  float UIMax=10000000000.0;  float UIStep=0.001;> = {1.0};
 */

//x = generic timer in range 0..1, period of 16777216 ms (4.6 hours), y = average fps, w = frame time elapsed (in seconds)
float4	Timer;
//x = Width, y = 1/Width, z = aspect, w = 1/aspect, aspect is Width/Height
float4	ScreenSize;
//changes in range 0..1, 0 means full quality, 1 lowest dynamic quality (0.33, 0.66 are limits for quality levels)
float	AdaptiveQuality;
//x = current weather index, y = outgoing weather index, z = weather transition, w = time of the day in 24 standart hours. Weather index is value from weather ini file, for example WEATHER002 means index==2, but index==0 means that weather not captured.
float4	Weather;
//x = dawn, y = sunrise, z = day, w = sunset. Interpolators range from 0..1
float4	TimeOfDay1;
//x = dusk, y = night. Interpolators range from 0..1
float4	TimeOfDay2;
//changes in range 0..1, 0 means that night time, 1 - day time
float	ENightDayFactor;
//changes 0 or 1. 0 means that exterior, 1 - interior
float	EInteriorFactor;

// External ENB debugging paramaters
float4 tempF1;     /// 0,1,2,3  // Keyboard controlled temporary variables.
float4 tempF2;     /// 5,6,7,8  // Press and hold key 1,2,3...8 together with PageUp or PageDown to modify.
float4 tempF3;     /// 9,0
float4 tempInfo1;  /// xy = cursor position in range 0..1 of screen, z = is shader editor window active, w = mouse buttons with values 0..7
/// tempInfo1 assigned mouse button values
///    0 = none
///    1 = left
///    2 = right
///    3 = left+right
///    4 = middle
///    5 = left+middle
///    6 = right+middle
///    7 = left+right+middle (or rather cat is sitting on your mouse)

float4 Params01[7];  /// MOD PARAMATER, DO NOT MODIFY!
float4 ENBParams01;  /// x - bloom amount; y - lens amount

// TEXTURES
Texture2D TextureColor;       /// HDR color
Texture2D TextureBloom;       /// Fallout4 or ENB bloom
Texture2D TextureLens;        /// ENB lens fx
Texture2D TextureAdaptation;  /// Fallout4 or ENB adaptation
Texture2D TextureDepth;       /// Scene depth
Texture2D TextureAperture;    /// This frame aperture 1*1 R32F hdr red channel only. computed in depth of field shader file

Texture2D TextureLUT_NAT 			<string ResourceName = "NATENB_nat.png";>; 			//index 0
Texture2D TextureLUT_natural 		<string ResourceName = "NATENB_natural.png";>; 		//index 1
Texture2D TextureLUT_atmospheric 	<string ResourceName = "NATENB_atmospheric.png";>;	//index 2
Texture2D TextureLUT_nightEye 		<string ResourceName = "NATENB_NightEye.png";>; 	//index 3

Texture2D TextureIMG_debug 			<string ResourceName = "NATENB_BadInstall.png";>;

// SAMPLERS
SamplerState SamplerPoint
{
  Filter=MIN_MAG_MIP_POINT;  AddressU=Clamp;  AddressV=Clamp;  /// MIN_MAG_MIP_LINEAR;
};
SamplerState SamplerLinear
{
  Filter=MIN_MAG_MIP_LINEAR;  AddressU=Clamp;  AddressV=Clamp;
};
SamplerState SamplerLut
{
   Filter=MIN_MAG_MIP_LINEAR;  AddressU=Clamp;  AddressV=Clamp;
};

// DATA STRUCTURE
struct VS_INPUT_POST
{
  float3 pos     : POSITION;
  float2 txcoord : TEXCOORD0;
};
struct VS_OUTPUT_POST
{
  float4 pos      : SV_POSITION;
  float2 txcoord0 : TEXCOORD0;
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
//CC
#define satLimit 0.1
// DITHER
#define remap(v, a, b) (((v) - (a)) / ((b) - (a)))

//LETTERBOX
#define border_width float2(0,0)
#define border_color float3(0, 0, 0)
#define screen_size float2(ScreenSize.x,ScreenSize.x*ScreenSize.w)
#define screen_ratio (screen_size.x / screen_size.y)
#define pixel float2(ScreenSize.y,ScreenSize.y*ScreenSize.z)
#define PixelSize 		 float2(ScreenSize.y, ScreenSize.y * ScreenSize.z)

//// GAME IMAGE SPACES
#define LUM_709 	float3(0.2125, 0.7154, 0.0721) 

static const float3 tint_color 			= Params01[4].rgb; 
static const float  tint_weight 		= Params01[4].w;
static const float3 fade        		= Params01[5].xyz; 
static const float  fade_weight 		= min(Params01[5].w,0.1f);
static const bool   isHavingGameFx 		= fade_weight > 0.0f;
static const float  fadeWeightFactor 	= fade_weight*5.0;
static const float  fadeWeightFactorHalf = fade_weight*2.0;

static const float 	GameSaturation 		= 0.9 + Params01[3].x;
static const float 	gameBrightness 		= saturate(Params01[3].w);
static const float 	gameContrast 		= min(Params01[3].z - 0.25f,2.0f);
static const float 	gameCurve  			= Params01[3].z;
//static const float rBloomThreshold  = Params01[2].x;

static const bool isBlackreach 			= Weather.x == 41;
static const bool isSoulCairn 			= Weather.x == 39;
static const bool isBroken 				= Weather.x < 1;

//// TODIE HELPER MACRO
static const float timeweight() {
    return TimeOfDay1.x +
           TimeOfDay1.y +
           TimeOfDay1.z +
           TimeOfDay1.w +
           TimeOfDay2.x +
           TimeOfDay2.y;
}

#define TOD(a) \
  ((TimeOfDay1.x * a##_Dawn    + \
    TimeOfDay1.y * a##_Sunrise + \
    TimeOfDay1.z * a##_Day     + \
    TimeOfDay1.w * a##_Sunset  + \
    TimeOfDay2.x * a##_Dusk    + \
    TimeOfDay2.y * a##_Night) / timeweight())

#define TODIE(a) lerp( TOD(a), a##_Interior, EInteriorFactor )

//// FUNCTIONS

float grayValue(float3 gv)
{
   return dot( gv, float3(0.2125, 0.7154, 0.0721) );
}

float smootherstep(float edge0, float edge1, float x)
{
   x = clamp((x - edge0)/(edge1 - edge0), 0.0, 1.0);
   return x*x*x*(x*(x*6 - 15) + 10);
}

float linearDepth(float nonLinDepth, float depthNearVar, float depthFarVar)
	{
	  return (2.0 * depthNearVar) / (depthFarVar + depthNearVar - nonLinDepth * (depthFarVar - depthNearVar));
	}

/// COLOR HELPERS
float Hue(float3 color)
{
   float hue = 0.0f;
   float fmin = min(min(color.r, color.g), color.b);
   float fmax = max(max(color.r, color.g), color.b);
   float delta = fmax - fmin;
   
   if (delta == 0.0)
      hue = 0.0;
   else
   {         
      float deltaR = (((fmax - color.r) / 6.0) + (delta / 2.0)) / delta;
      float deltaG = (((fmax - color.g) / 6.0) + (delta / 2.0)) / delta;
      float deltaB = (((fmax - color.b) / 6.0) + (delta / 2.0)) / delta;

      if (color.r == fmax )
         hue = deltaB - deltaG;
      else if (color.g == fmax)
         hue = (1.0 / 3.0) + deltaR - deltaB;
      else if (color.b == fmax)
         hue = (2.0 / 3.0) + deltaG - deltaR;
   }
      
   if (hue < 0.0)
      hue += 1.0f;
   else if (hue > 1.0)
      hue -= 1.0f;
   return hue;
}

float3 HUEToRGB( in float H )
{
    return saturate( float3( abs( H * 6.0f - 3.0f ) - 1.0f,
                                  2.0f - abs( H * 6.0f - 2.0f ),
                                  2.0f - abs( H * 6.0f - 4.0f )));
}

float3 RGBToHCV( in float3 RGB )
{
    // Based on work by Sam Hocevar and Emil Persson
    float4 P         = ( RGB.g < RGB.b ) ? float4( RGB.bg, -1.0f, 2.0f/3.0f ) : float4( RGB.gb, 0.0f, -1.0f/3.0f );
    float4 Q1        = ( RGB.r < P.x ) ? float4( P.xyw, RGB.r ) : float4( RGB.r, P.yzx );
    float C          = Q1.x - min( Q1.w, Q1.y );
    float H          = abs(( Q1.w - Q1.y ) / ( 6.0f * C + 0.000001f ) + Q1.z );
    return float3( H, C, Q1.x );
}

float3 RGBToHSL( in float3 RGB )
{
    RGB.xyz          = max( RGB.xyz, 0.000001f );
    float3 HCV       = RGBToHCV(RGB);
    float L          = HCV.z - HCV.y * 0.5f;
    float S          = HCV.y / ( 1.0f - abs( L * 2.0f - 1.0f ) + 0.000001f);
    return float3( HCV.x, S, L );
}

float3 HSLToRGB( in float3 HSL )
{
    float3 RGB       = HUEToRGB(HSL.x);
    float C          = (1.0f - abs(2.0f * HSL.z - 1.0f)) * HSL.y;
    return ( RGB - 0.5f ) * C + HSL.z;
}

/// SHADERS
float3 ChromaticAberration(float3 colorInput, float2 inTexCoords)
	{
		float3 color;

		color.r = TextureColor.Sample(SamplerPoint, inTexCoords + (PixelSize * 1.5)).r;
		color.g = colorInput.g;
		color.b = TextureColor.Sample(SamplerPoint, inTexCoords - (PixelSize * 1.5)).b;

		return lerp(colorInput, color, fadeWeightFactor*4.0);
	}
	
//LENS DISTORTION by Weaseltron
float2 barrelDistortion( float2 p, float2 amt )
{
    p = 2.0 * p - 1.0;
    float maxBarrelPower = sqrt(5.0);
    float radius = dot(p,p); 
    p *= pow(radius, maxBarrelPower * amt);
	

    return p * 0.5 + 0.5;
}

float2 brownConradyDistortion(float2 uv, float scalar)
{
    uv = (uv - 0.5 ) * 2.0;
    
    if( true )
    {
        float barrelDistortion1 = -0.02 * scalar;
        float barrelDistortion2 = 0.0 * scalar;

        float r2 = dot(uv,uv);
        uv *= 1.0 + barrelDistortion1 * r2 + barrelDistortion2 * r2 * r2;
       
    }
    
   return (uv / 2.0) + 0.5;
}

float3 LensCA( float2 uv )
{
	
    float maxDistort = fadeWeightFactor*8.0;
	if(bUseLensDistortion) maxDistort+=0.18;
	
    float scalar = 1.0 * maxDistort;
    float4 colourScalar = float4(700.0, 560.0, 490.0, 1.0);
    colourScalar /= max(max(colourScalar.x, colourScalar.y), colourScalar.z);
    colourScalar *= 2.0;
    
    colourScalar *= scalar;

    const float numTaps = 8.0;
    
    float3 fragColor = 0.0;
    for( float tap = 0.0; tap < numTaps; tap += 1.0 )
    {
        fragColor.r += TextureColor.Sample(SamplerLinear, brownConradyDistortion(uv, colourScalar.r)).r;
        fragColor.g += TextureColor.Sample(SamplerLinear, brownConradyDistortion(uv, colourScalar.g)).g;
        fragColor.b += TextureColor.Sample(SamplerLinear, brownConradyDistortion(uv, colourScalar.b)).b;
     
        colourScalar *= 0.95;
    }
    
    fragColor /= numTaps;
  
    return fragColor;
}	
	
//LETTERBOX
float4 BorderPass( float4 colorInput, float2 tex )
{
  if (border_ratio>0.0)
  {
	float3 border_color_float = border_color / 255.0;

	float2 border_width_variable = border_width;

	if (border_width.x == -border_width.y)
	if (screen_ratio < border_ratio)
		border_width_variable = float2(0.0, (screen_size.y - (screen_size.x / border_ratio)) * 0.5);
	else
		border_width_variable = float2((screen_size.x - (screen_size.y * border_ratio)) * 0.5, 0.0);

	float2 border = (pixel * border_width_variable);

	float2 within_border = saturate((-tex * tex + tex) - (-border * border + border));

	colorInput.rgb = all(within_border) ?  colorInput.rgb : border_color_float ;
	}
	return colorInput;
}

//VIGNETTE
float4 Vignette(float4 inColor, float2 inTexCoords, float ratio)
{
    float3 origcolor = inColor;
	float2 uv;

	
      if(ratio!=0.0)uv      = (inTexCoords.xy - 0.5f) * (ratio*0.25);
      else uv      = (inTexCoords.xy - 0.5f) * 0.45;
	  float vignette = saturate(dot(uv.xy, uv.xy));
      vignette       = pow(vignette, 1.5);
	  
      inColor.xyz    = lerp(origcolor.xyz, inColor.xyz*float3(0.0,0.0,0.0), vignette * 20);

	return inColor;
}

float4 VignetteFX(float4 inColor, float2 inTexCoords, float ratio)
{
    float3 origcolor = inColor;
	float2 uv;

	
      if(ratio!=0.0)uv      = (inTexCoords.xy - 0.5f) * (ratio*0.25);
      else uv      = (inTexCoords.xy - 0.5f) * 0.45;
	  float vignette = saturate(dot(uv.xy, uv.xy));
      vignette       = pow(vignette, 1.5);
	  
      inColor.xyz    = lerp(origcolor.xyz, inColor.xyz*float3(0.0,0.0,0.0), vignette * (fade_weight*200.0));

	return inColor;
}



//DITHERING BY SANDVICH MAKER
float rand21(float2 coord)
{
    float2 noise = frac(sin(dot(coord, float2(12.9898, 78.233) * 2.0)) * 43758.5453);
    return (noise.x + noise.y) * 0.5;
}

float rand11(float x)
{
    return frac(x * 0.024390243);
}

float permute(float x)
{
    return ((34.0 * x + 1.0) * x) % 289.0;
}

float3 Dither(float3 color, float2 uv, int depth)
{
    const float bitstep = exp2(depth) - 1.0; // pow(2.0, depth) - 1.0;
    const float lsb     = 1.0 / bitstep;
    const float lobit   = 0.5 / bitstep;
    const float hibit   = (bitstep - 0.5) / bitstep;

    float3 m   = float3(uv, rand21(uv + Timer.x)) + 1.0;
    float  h   = permute(permute(permute(m.x) + m.y) + m.z);

    float3 noise1, noise2;
    noise1.x   = rand11(h); h = permute(h);
    noise2.x   = rand11(h); h = permute(h);
    noise1.y   = rand11(h); h = permute(h);
    noise2.y   = rand11(h); h = permute(h);
    noise1.z   = rand11(h); h = permute(h);
    noise2.z   = rand11(h);

    float3 lo  = saturate(remap(color.xyz, 0.0, lobit));
    float3 hi  = saturate(remap(color.xyz, 1.0, hibit));
    float3 uni = noise1 - 0.5;
    float3 tri = noise1 - noise2;

    return float3(lerp(uni.x, tri.x, min(lo.x, hi.x)),
                  lerp(uni.y, tri.y, min(lo.y, hi.y)),
                  lerp(uni.z, tri.z, min(lo.z, hi.z))) * lsb;
}	

	
// 	Tetrahedral interpolated MultiLUT by kingeric (Nov 5th, 2022)

class Texture2DAtlas
{
    Texture2D tex;
    int slice;
    
    float4 Load(int3 pos, int3 size)
    {
        return tex.Load(int3(pos.x + size.x * pos.z, pos.y + size.y * slice, 0));
    }

    #define Texture2DAtlas(a,b) Texture2DAtlas::ctor((a),(b))
    static  Texture2DAtlas ctor(Texture2D t, int k)
    {
        Texture2DAtlas r = {t, k}; return r;
    }
};

#define _TETRATEX Texture2DAtlas
#define _TETRALOAD(a, b, c) (a).Load((b), (c))

float3 TetraLut(_TETRATEX texIn, float3 rgb, uint3 size)
{
    float3 d =  rgb * (size - 1);
    uint3  i =  d, p00, p11;
    uint2  j = {1,0};
    bool3  b = (d -= i) >= d.gbr;

    [flatten] // should flatten itself without annotation.
    if (b.x)  // x >= y
    {
        [flatten]
        if      (b.y) d = d.xyz, p00 = j.xyy, p11 = j.xxy; // xyz
        else if (b.z) d = d.zxy, p00 = j.yyx, p11 = j.xyx; // zxy
        else          d = d.xzy, p00 = j.xyy, p11 = j.xyx; // xzy
    }

    else // y > x
    {
        [flatten]
        if      (!b.y) d = d.zyx, p00 = j.yyx, p11 = j.yxx; // zyx
        else if (!b.z) d = d.yxz, p00 = j.yxy, p11 = j.xxy; // yxz
        else           d = d.yzx, p00 = j.yxy, p11 = j.yxx; // yzx
    }

    return mul(float4(1. - d.x, d.z, d.xy - d.yz),
               float4x3(_TETRALOAD(texIn, i + j.y, size).rgb,
                        _TETRALOAD(texIn, i + j.x, size).rgb,
                        _TETRALOAD(texIn, i + p00, size).rgb,
                        _TETRALOAD(texIn, i + p11, size).rgb));
}

// clean up
#undef _TETRATEX
#undef _TETRALOAD

float3 MultiLUT_T(float3 color, int index, int dni)
{
    class func_t
    {
        static float3 run(Texture2D t)
        {
            int2 tex_size;
            t.GetDimensions(tex_size.x, tex_size.y);

            return saturate(TetraLut(Texture2DAtlas(t, dni), color, sqrt(tex_size.x).xxx));
        }
    };

    switch(index)
    {
        case  0: return func_t::run(TextureLUT_NAT);
		case  1: return func_t::run(TextureLUT_natural);
		case  2: return func_t::run(TextureLUT_atmospheric);
		case  3: return func_t::run(TextureLUT_nightEye);

        default: return color;
    }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////////////

// VERTEX SHADER

VS_OUTPUT_POST	VS_Draw(VS_INPUT_POST IN)
{
	VS_OUTPUT_POST	OUT;
	float4	pos;
	pos.xyz=IN.pos.xyz;
	pos.w=1.0;
	OUT.pos=pos;
	OUT.txcoord0.xy=IN.txcoord.xy;
	return OUT;
}

// PIXEL SHADER
////////////////////////////////////////////////////////////////////////////// WARM Processed
float4 PS_NATENB(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	
	float4	res;
	float4	color;
	
	color=  TextureColor.Sample(SamplerPoint, IN.txcoord0.xy);
	float3	bloom=TextureBloom.Sample(SamplerLinear, IN.txcoord0.xy);
	float3	lens=TextureLens.Sample(SamplerLinear, IN.txcoord0.xy).xyz;
	float4	Adaptation=TextureAdaptation.Sample(SamplerPoint, IN.txcoord0.xy).x;
	
// GAME TINT
	if (!isHavingGameFx) {
		color.a   = dot(color.rgb, LUM_709);
		float fTintPercent_Dawn=0.75;
		float fTintPercent_Sunrise=0.45;
		float fTintPercent_Day=0.1;
			if (isSoulCairn) fTintPercent_Day*=2.0;
		float fTintPercent_Sunset=0.65;
		float fTintPercent_Dusk=0.7;
		float fTintPercent_Night=0.25;
		float fTintPercent_Interior=0.2;

		color.rgb = lerp(color.rgb, tint_color * color.a , tint_weight * TODIE(fTintPercent));	
		color.a = 1.0;
	}

/// ENB BLOOM & LENS
	bloom.xyz=pow(bloom,0.9);
	bloom.xyz=bloom-color;
	bloom.xyz=max(bloom, 0.0);
	bloom*=ENBParams01.x+fade_weight;
	color.xyz = color + bloom - color * bloom;
	
	if (isBlackreach) lens*=4.0;
	color.xyz+= (lens.xyz * ENBParams01.y * 0.85) / (1 + color);

/// ENB Adaptation
	float	grayadaptation=max(max(Adaptation.x, Adaptation.y), Adaptation.z);
	float 	greyscale = dot(color.xyz, float3(0.3, 0.59, 0.11));

/// PP2
/// SETUP
	float Gamma_Day = 1.4;
	float Gamma_Night = 1.2;
	float Gamma_Interior = 1.0;
	float Gamma_Dawn = (Gamma_Day+Gamma_Night)/2.0;
	float Gamma_Sunrise = Gamma_Day;
	float Gamma_Sunset = Gamma_Day;
	float Gamma_Dusk = (Gamma_Day+Gamma_Night)/2.0;
		
	float AdaptationMin_Day=0.001;
	float AdaptationMin_Night=0.002;
	float AdaptationMin_Interior=0.01;
	float AdaptationMin_Sunrise = (AdaptationMin_Day+AdaptationMin_Night)/2.0;//AdaptationMin_Day+0.0005;
	float AdaptationMin_Sunset = (AdaptationMin_Day+AdaptationMin_Night)/2.0;//AdaptationMin_Day+0.0005;
	float AdaptationMin_Dawn = AdaptationMin_Night;//(AdaptationMin_Sunrise+AdaptationMin_Night)/2.0;
	float AdaptationMin_Dusk = AdaptationMin_Night;//(AdaptationMin_Sunset+AdaptationMin_Night)/2.0;
	
	float AdaptationMax_Day=0.22;
	float AdaptationMax_Night=0.11;
	float AdaptationMax_Interior=0.15;
	float AdaptationMax_Dawn = (AdaptationMax_Day+AdaptationMax_Night)/2.0;
	float AdaptationMax_Sunrise = AdaptationMax_Day;
	float AdaptationMax_Sunset = AdaptationMax_Day;
	float AdaptationMax_Dusk = (AdaptationMax_Day+AdaptationMax_Night)/2.0;
	
	float Brightness_Day=1.0;
	float Brightness_Night=0.5;
	float Brightness_Interior=0.5;
	float Brightness_Dawn = (Brightness_Day+Brightness_Night)/2.0;
	float Brightness_Sunrise = Brightness_Day;
	float Brightness_Sunset = Brightness_Day;
	float Brightness_Dusk = (Brightness_Day+Brightness_Night)/2.0;
	if (isBlackreach) Brightness_Interior = 1.1;

	float Saturation_Day=2.6;
	float Saturation_Night=2.4;
	float Saturation_Interior= 2.6;	
	float Saturation_Dawn = (Saturation_Day+Saturation_Night)/2.0;
	float Saturation_Sunrise = Saturation_Day;
	float Saturation_Sunset = Saturation_Day;
	float Saturation_Dusk = (Saturation_Day+Saturation_Night)/2.0;
	
	float IntensityContrast_Day=1.2;
	float IntensityContrast_Night=1.2;
	float IntensityContrast_Interior=1.2;
	float IntensityContrast_Dawn = (IntensityContrast_Day+IntensityContrast_Night)/2.0;
	float IntensityContrast_Sunrise = IntensityContrast_Day;
	float IntensityContrast_Sunset = IntensityContrast_Day;
	float IntensityContrast_Dusk = (IntensityContrast_Day+IntensityContrast_Night)/2.0;
	
	float ToneMappingCurve_Day=0.9;
	float ToneMappingCurve_Night=1.0;
	float ToneMappingCurve_Interior=0.8;
	float ToneMappingCurve_Sunrise = ToneMappingCurve_Day-0.05;
	float ToneMappingCurve_Sunset = ToneMappingCurve_Day-0.05;
	float ToneMappingCurve_Dawn = (ToneMappingCurve_Sunrise+ToneMappingCurve_Night)/2.0;
	float ToneMappingCurve_Dusk = (ToneMappingCurve_Sunset+ToneMappingCurve_Night)/2.0;
	
	float RedFilter_Day=1.0;
	float RedFilter_Night=1.0;
	float RedFilter_Interior=1.0;
	float RedFilter_Dawn = (RedFilter_Day+RedFilter_Night)/2.0;
	float RedFilter_Sunrise = RedFilter_Day;
	float RedFilter_Sunset = RedFilter_Day;
	float RedFilter_Dusk = (RedFilter_Day+RedFilter_Night)/2.0;

	float BlueFilter_Day=1.0;
	float BlueFilter_Night=0.980;
	float BlueFilter_Interior=1.0;
	float BlueFilter_Dawn = (BlueFilter_Day+BlueFilter_Night)/2.0;
	float BlueFilter_Sunrise = BlueFilter_Day;
	float BlueFilter_Sunset = BlueFilter_Day;
	float BlueFilter_Dusk = (BlueFilter_Day+BlueFilter_Night)/2.0;
	
	float DesatG_Day= 0.12;
	float DesatG_Night=0.1;
	float DesatG_Interior=0.15;
	float DesatG_Dawn = (DesatG_Day+DesatG_Night)/2.0;
	float DesatG_Sunrise = DesatG_Day;//0.12;
	float DesatG_Sunset = DesatG_Day;//0.2;
	float DesatG_Dusk = (DesatG_Day+DesatG_Night)/2.0;
		
	float DesatB_Day=0.7;
	float DesatB_Night=0.65;
	float DesatB_Interior=0.7;
	float DesatB_Dawn = (DesatB_Day+DesatB_Night)/2.0;
	float DesatB_Sunrise = 0.6;
	float DesatB_Sunset = 0.6;
	float DesatB_Dusk = (DesatB_Day+DesatB_Night)/2.0;

//PP2------------------------------------------------------------------------------------------------------------------------------------------------------------------------

		color.g = lerp(greyscale, color.g, TODIE(DesatG));
		color.b = lerp(greyscale, color.b, TODIE(DesatB));	
			
		color = pow(color, TODIE(Gamma));
		
		color.r = pow(color.r, TODIE(RedFilter));
		color.b = pow(color.b, TODIE(BlueFilter)-(fade_weight*0.33));
	   
		grayadaptation=max(grayadaptation, 0.0); //0.0
		grayadaptation=min(grayadaptation, 50.0); //50.0
		
		color.xyz=color.xyz/(grayadaptation*TODIE(AdaptationMax)+TODIE(AdaptationMin));//*tempF1.x

		color.xyz*=(TODIE(Brightness)*max(gameBrightness,0.5f))+fadeWeightFactor;
			
		color.xyz+=0.000001;
		float3 xncol=normalize(color.xyz);
		float3 scl=color.xyz/xncol.xyz;
		scl=pow(scl, TODIE(IntensityContrast));
		xncol.xyz=pow(xncol.xyz, TODIE(Saturation)-fade_weight);
		color.xyz=scl*xncol.xyz;

		color.xyz=(color.xyz * (1.0 + color.xyz/333333))/(color.xyz + max(TODIE(ToneMappingCurve)-(fadeWeightFactor*0.5),0.01));

/// AGCC TINT & FADE FOR SFX
	color.xyz = lerp(color.xyz, fade, fade_weight);
	if (isHavingGameFx) {
		color.a   = dot(color.xyz, LUM_709);
		color.xyz = lerp(color.xyz, tint_color * color.a, tint_weight);
		color.xyz = lerp(color.xyz, fade, fade_weight);
		color.a = 1.0;
	}
	
/// PROD80 COLOR EQ	
   float3 fxcolor = saturate( color.xyz );
   float greyVal = grayValue( fxcolor.xyz );
   float colorHue = Hue( fxcolor.xyz );
   
   float colorSat = 0.0f;
   float minColor = min( min ( fxcolor.x, fxcolor.y ), fxcolor.z );
   float maxColor = max( max ( fxcolor.x, fxcolor.y ), fxcolor.z );
   float colorDelta = maxColor - minColor;
   float colorInt = ( maxColor + minColor ) * 0.5f;
   
   if ( colorDelta != 0.0f )
   {
      if ( colorInt < 0.5f )
         colorSat = colorDelta / ( maxColor + minColor );
      else
         colorSat = colorDelta / ( 2.0f - maxColor - minColor );
   }
   
	colorSat = 1.0f;
   
   float hueMin_1 = 0.0f;
   float hueMin_2 = 0.0f;
   float hueMax_1 = 0.0f;
   float hueMax_2 = 0.0f;
   
   if ( 0.5 > 0.45 )
   {
      hueMin_1 = 0.45 - 0.5;
      hueMin_2 = 1.0f + 0.45 - 0.5;
      hueMax_1 = 0.45 + 0.5;
      hueMax_2 = 1.0f + 0.45;
   
      if ( colorHue >= hueMin_1 && colorHue <= 0.45 )
         fxcolor.xyz = lerp( greyVal.xxx, fxcolor.xyz, smootherstep( hueMin_1, 0.45, colorHue ) * ( colorSat * satLimit ));
      else if ( colorHue > 0.45 && colorHue <= hueMax_1 )
         fxcolor.xyz = lerp( greyVal.xxx, fxcolor.xyz, ( 1.0f - smootherstep( 0.45, hueMax_1, colorHue )) * ( colorSat * satLimit ));
      else if ( colorHue >= hueMin_2 && colorHue <= hueMax_2 )
         fxcolor.xyz = lerp( greyVal.xxx, fxcolor.xyz, smootherstep( hueMin_2, hueMax_2, colorHue ) * ( colorSat * satLimit ));
      else
         fxcolor.xyz = greyVal.xxx;
   
   }
   else if ( 0.45 + 0.5 > 1.0f )
   {
      hueMin_1 = 0.45 - 0.5;
      hueMin_2 = 0.0f - ( 1.0f - 0.45 );
      hueMax_1 = 0.45 + 0.5;
      hueMax_2 = 0.45 + 0.5 - 1.0f;
   
      if ( colorHue >= hueMin_1 && colorHue <= 0.45 )
         fxcolor.xyz = lerp( greyVal.xxx, fxcolor.xyz, smootherstep( hueMin_1, 0.45, colorHue ) * ( colorSat * satLimit ));
      else if ( colorHue > 0.45 && colorHue <= hueMax_1 )
         fxcolor.xyz = lerp( greyVal.xxx, fxcolor.xyz, ( 1.0f - smootherstep( 0.45, hueMax_1, colorHue )) * ( colorSat * satLimit ));
      else if ( colorHue >= hueMin_2 && colorHue <= hueMax_2 )
         fxcolor.xyz = lerp( greyVal.xxx, fxcolor.xyz, smootherstep( hueMin_2, hueMax_2, colorHue) * ( colorSat * satLimit ));
      else
         fxcolor.xyz = greyVal.xxx;
      
   }
   else
   {
      hueMin_1 = 0.45 - 0.5;
      hueMax_1 = 0.45 + 0.5;
      
      if ( colorHue >= hueMin_1 && colorHue <= 0.45 )
         fxcolor.xyz = lerp( greyVal.xxx, fxcolor.xyz, smootherstep( hueMin_1, 0.45, colorHue ) * ( colorSat * satLimit ));
      else if ( colorHue > 0.45 && colorHue <= hueMax_1 )
         fxcolor.xyz = lerp( greyVal.xxx, fxcolor.xyz, ( 1.0f - smootherstep( 0.45, hueMax_1, colorHue )) * ( colorSat * satLimit ));
      else
         fxcolor.xyz = greyVal.xxx;
   
   }
   
	color.xyz = lerp( color.xyz, fxcolor.xyz, 0.25 );

/// GOING LDR
	res.xyz=saturate(color);

/// L U T S
/// COLOR CORRECTION NATURAL AND ATMOSPHERIC
	res.xyz = lerp(res.xyz, MultiLUT_T(res,0,0),lerp(lerp(0.5, 0.55, ENightDayFactor), 0.5, EInteriorFactor));

/// NIGHT EYE
	if (isHavingGameFx) {
		res.xyz = lerp(res.xyz, MultiLUT_T(res,3,0),saturate(fade_weight*5.0));
		res		= VignetteFX(res,IN.txcoord0.xy,border_ratio);
	}	

/// Saturation Limit 
	res.xyz = RGBToHSL( res.xyz );
	res.y = min( res.y, 0.720 );
	res.xyz = HSLToRGB( res.xyz );
	
/// Vignette
	if (bUseVignette) res = lerp(res, Vignette(res,IN.txcoord0.xy,border_ratio), 0.3);
	
	res.w=1.0;
	return float4(res + Dither(res, IN.txcoord0.xy, 10),1.0);
}

////////////////////////////////////////////////////////////////////////////// COLD
float4 PS_NATURAL(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	
	float4	res;
	float4	color;
	color = TextureColor.Sample(SamplerPoint, IN.txcoord0.xy);
	float3	lens=TextureLens.Sample(SamplerLinear, IN.txcoord0.xy).xyz;
	float3	bloom=TextureBloom.Sample(SamplerLinear, IN.txcoord0.xy);
	float4	Adaptation=TextureAdaptation.Sample(SamplerPoint, IN.txcoord0.xy).x;

/// ENB BLOOM & LENS
	color.xyz+= (pow(bloom,1.2) * (ENBParams01.x*0.8)) / (1 + color);
	lens *=0.7;
	if (isBlackreach) lens*=10.0;
	color.xyz+= (lens.xyz * ENBParams01.y) / (1 + color);

/// ENB Adaptation
    float4 middlegray=max(max(Adaptation.x, Adaptation.y), Adaptation.z);
	middlegray=max(middlegray, 0.0);
	middlegray=min(middlegray, 50.0);

/// PP2
	color.xyz = color.xyz / (middlegray * 0.28 + 0.05); 
	color.xyz  *= lerp(0.8*max(gameBrightness,0.75f), 1.8, EInteriorFactor) + fadeWeightFactor;
    color.xyz  += 0.000001;
    float3 xncol  = normalize(color.xyz);
    float3 scl    = color.xyz / xncol.xyz;
	//scl=pow(scl, lerp(lerp(1.0, 1.2, ENightDayFactor),1.0,EInteriorFactor));
	xncol.xyz=pow(xncol.xyz, lerp(1.1,1.2,EInteriorFactor));
    color.xyz   = scl * xncol.xyz;
    color.xyz   = (color.xyz * (1.0 + color.xyz / 200.0)) / (color.xyz + lerp(lerp(0.5-fadeWeightFactorHalf,0.8-fadeWeightFactor,ENightDayFactor),max(0.7-fadeWeightFactor,0.2), EInteriorFactor));

/// NIGHT EYE COLORS
	if (isHavingGameFx) {
		color.a   = dot(color.xyz, LUM_709);
		color.xyz = lerp(color.xyz, tint_color * color.a, tint_weight);
		color.xyz = lerp(color.xyz, fade, fade_weight);
		color.a = 1.0;
	}

/// GOING LDR
	res.xyz=saturate(color);

/// L U T S
/// NEUTRAL COLOR 
	res.xyz = lerp(res.xyz, MultiLUT_T(res,1,0),lerp(lerp(0.9, 1.0, ENightDayFactor), 0.8, EInteriorFactor));

/// NIGHT EYE
	if (isHavingGameFx) {
		res.xyz = lerp(res.xyz, MultiLUT_T(res,3,0),saturate(fade_weight*5.0));
		res		= VignetteFX(res,IN.txcoord0.xy,border_ratio);
	}	

/// Saturation Limit 
	res.xyz = RGBToHSL( res.xyz );
	res.y = min( res.y, 0.75 );
	res.xyz = HSLToRGB( res.xyz );

/// Vignette
	if (bUseVignette) res		= lerp(res, Vignette(res,IN.txcoord0.xy,border_ratio), 0.35);
	
	res.w=1.0;
	return float4(res + Dither(res, IN.txcoord0.xy, 10),1.0);
}

////////////////////////////////////////////////////////////////////////////// RDR2
float4 PS_ATMOSPHERIC(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	
	float4	res;
	float4	color;
	color=  TextureColor.Sample(SamplerPoint, IN.txcoord0.xy);
	float3	bloom=TextureBloom.Sample(SamplerLinear, IN.txcoord0.xy);
	float3	lens=TextureLens.Sample(SamplerLinear, IN.txcoord0.xy).xyz;
	float4	Adaptation=TextureAdaptation.Sample(SamplerPoint, IN.txcoord0.xy).x;
	
/// ENB BLOOM & LENS
	bloom.xyz=pow(bloom,0.8)-color;
	bloom.xyz=max(bloom, 0.0);
	
	color.xyz+=bloom*(ENBParams01.x+fade_weight);

	if (isBlackreach) lens*=5.0;
	color.xyz+= (lens.xyz * ENBParams01.y * 1.2) / (1 + color);

/// ENB Adaptation
    float4 middlegray=max(max(Adaptation.x, Adaptation.y), Adaptation.z);
	middlegray=max(middlegray, 0.0);
	middlegray=min(middlegray, 50.0);

// GAME TINT
	if (!isHavingGameFx) {
		color.a   = dot(color.rgb, LUM_709);
		float fTintPercent_Dawn=0.75;
		float fTintPercent_Sunrise=0.65;
		float fTintPercent_Day=0.35;
		float fTintPercent_Sunset=0.65;
		float fTintPercent_Dusk=0.75;
		float fTintPercent_Night=0.1;
		float fTintPercent_Interior=0.2;

		color.rgb = lerp(color.rgb, tint_color * color.a , tint_weight * TODIE(fTintPercent));	
		color.a = 1.0;
	}
/// GAMMA IN
	float Gamma=lerp(lerp(1.25, 1.45, ENightDayFactor), 1.15, EInteriorFactor);
	color = pow(color, Gamma);

/// PP2
	float adaptMin_Int;
	if (isBlackreach) adaptMin_Int = 0.0035;
	else adaptMin_Int = 0.015;
	float AdaptationMin=lerp(lerp(0.035, 0.005, ENightDayFactor), adaptMin_Int, EInteriorFactor);
	float AdaptationMax=lerp(lerp(0.025, 0.18, ENightDayFactor), 0.05, EInteriorFactor);

	float greyscale = dot(color.xyz, float3(0.3, 0.59, 0.11));
    float DesatG=lerp(lerp(0.1, 0.2, ENightDayFactor), 0.15, EInteriorFactor);
	float DesatB=lerp(lerp(0.65, 0.6, ENightDayFactor), 0.7, EInteriorFactor);

    color.g = lerp(greyscale, color.g, DesatG);
    color.b = lerp(greyscale, color.b, DesatB);	

    color.xyz = color.xyz / (middlegray * AdaptationMax + AdaptationMin); 

	color.xyz  *= 0.1+gameBrightness+fadeWeightFactor;

    color.xyz  += 0.000001;
    float3 xncol  = normalize(color.xyz);
    float3 scl    = color.xyz / xncol.xyz;
	
	if (gameContrast > 1.0f) scl = pow(scl, 1.0+(gameContrast/50));
	else scl = pow(scl, 1.1);

	xncol.xyz     = pow(xncol.xyz, lerp(lerp(1.8, 2.2, ENightDayFactor), 2.0, EInteriorFactor));
	
    color.xyz   = scl * xncol.xyz;
    color.xyz   = (color.xyz * (1.0 + color.xyz / 100.0)) / (color.xyz + (gameCurve-fadeWeightFactor));

/// AGCC TINT & FADE FOR SFX
	if (isHavingGameFx) {
		color.a   = dot(color.xyz, LUM_709);
		color.xyz = lerp(color.xyz, tint_color * color.a, tint_weight);
		color.xyz = lerp(color.xyz, fade, fade_weight);
		color.a = 1.0;
	}
	
/// GOING LDR
	res.xyz=saturate(color);

	// ATMOSPHERIC
	res.xyz = lerp(res.xyz, MultiLUT_T(res,2,0),lerp(lerp(0.5, 0.65, ENightDayFactor), 0.75, EInteriorFactor));

/// NIGHT EYE
	if (isHavingGameFx) {
		res.xyz = lerp(res.xyz, MultiLUT_T(res,3,0),saturate(fade_weight*5.0));
		res		= VignetteFX(res,IN.txcoord0.xy,border_ratio);
	}	

/// Saturation Limit 
	res.xyz = RGBToHSL( res.xyz );
	res.y = min( res.y, 0.7 );
	res.xyz = HSLToRGB( res.xyz );
		
/// Vignette
	if (bUseVignette) res		= lerp(res, Vignette(res,IN.txcoord0.xy,border_ratio), 0.75);
	
	res.w=1.0;
	return float4(res + Dither(res, IN.txcoord0.xy, 10),1.0);
}

////////////////////////////////////////////////////////////////////////////// POST PROCESS
float4	PS_DepthSharp(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	float4	res;
	float4	color;
	float4	centercolor;
	
	float Radius;
	float intExt;
	float intInt;
	
	float2	pixeloffset=ScreenSize.y;
	pixeloffset.y*=ScreenSize.z;

	/// SETUP
	//SOFT
	if (iSharpStyle == 1) {
		Radius=0.5;
		intExt=2.0;
		intInt=1.0;
	}
	//SHARP
	else if (iSharpStyle == 2) {
		Radius=0.25;
		intExt=8.0;
		intInt=4.0;
	}
	//WIDE
	else if (iSharpStyle == 3) {
		Radius=1.5;
		intExt=1.0;
		intInt=0.7;
	}
		//OFF
	else {
		Radius=0.0;
		intExt=0.0;
		intInt=0.0;
	}
	float Depth = TextureDepth.Sample(SamplerPoint, IN.txcoord0.xy ).x;
	float closeDepth = linearDepth(Depth, 0.5f, 500.0);

	centercolor=TextureColor.Sample(SamplerPoint, IN.txcoord0.xy);
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
		float2	coord=offsets[i].xy * pixeloffset.xy * (Radius - closeDepth) + IN.txcoord0.xy;
		color.xyz+=TextureColor.Sample(SamplerLinear, coord.xy);
	}
	color.xyz *= 0.25;

	float	diffgray = dot((centercolor.xyz-color.xyz), 0.333);
	
	res.xyz = lerp(lerp(intExt+(fadeWeightFactor*4.0),intInt+(fadeWeightFactor*4.0),EInteriorFactor), 0.0f, closeDepth) * centercolor.xyz * diffgray + centercolor.xyz;

	res.w=1.0;
	return res;
}

float4	PS_PFX(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	float4	res=TextureColor.Sample(SamplerPoint, IN.txcoord0.xy);
	
/// NIGHT EYE C.A
	if (isHavingGameFx) res.xyz = ChromaticAberration(res.rgb,IN.txcoord0.xy);
	res.xyz = LensCA(IN.txcoord0.xy);

/// GRAIN
	if (NoiseEnable){
		float NoiseAmount=lerp(lerp(0.06, 0.05, ENightDayFactor), 0.1, EInteriorFactor);

		float3 grain = 0.0;
		float4 uvs;
		uvs.xy = IN.txcoord0.xy + float2(Timer.x/Timer.y, Timer.x/Timer.y);
		uvs.zw = uvs.xy + float2(ScreenSize.y, ScreenSize.z);
		
		uvs = frac(uvs * float2(21.5932, 21.77156).xyxy);
		
		float origgray=max(res.x, res.y);
		origgray=max(origgray, res.z);
		
		float2 shift = float2(21.5351, 14.3137);
		float2 temp0 = uvs.xy + dot(uvs.yx, uvs.xy + shift);
		float2 temp1 = uvs.xw + dot(uvs.wx, uvs.xw + shift);
		float2 temp2 = uvs.zy + dot(uvs.yz, uvs.zy + shift);
		float2 temp3 = uvs.zw + dot(uvs.wz, uvs.zw + shift);

		float3 r = -2;
		r += frac(temp0.x * temp0.y * float3(95.4337, 96.4337, 97.4337));
		r += frac(temp1.x * temp1.y * float3(95.4337, 96.4337, 97.4337));
		r += frac(temp2.x * temp2.y * float3(95.4337, 96.4337, 97.4337));
		r += frac(temp3.x * temp3.y * float3(95.4337, 96.4337, 97.4337));

		r /= 2;

		r = lerp (r, r.x, 0.34);
		grain.xyz = r;
		grain.xyz = lerp(grain.x, grain, 0.0f);
		res.xyz=lerp(res, (grain.x+0.5)*res, NoiseAmount*saturate(1.0-origgray*0.5));
	}

/// LETTERBOX
	if (border_ratio>0.0)    	res		= BorderPass(res, IN.txcoord0.xy);

/// DEBUG MESSAGE
	if (!EInteriorFactor && isBroken) {
 
		float4 ImageColour;
		const float phiValue = ((1.0 + sqrt(5.0))/2.0);
		float aspectRatio = ScreenSize.z;

		float screenWidth = ScreenSize.x;
		float screenHeight = ScreenSize.x * ScreenSize.w;

		float idealWidth =  screenHeight * phiValue;
		float idealHeight = screenWidth / phiValue;

		float4 sourceCoordFactor = float4(1.0, 1.0, 1.0, 1.0);

		float2 coords = float2( (IN.txcoord0.x * sourceCoordFactor.x) - ((1.0-sourceCoordFactor.z)/2.0),
									(IN.txcoord0.y * sourceCoordFactor.y) - ((1.0-sourceCoordFactor.w)/2.0));

		ImageColour = TextureIMG_debug.Sample(SamplerLinear, coords);

		res.rgb= saturate(lerp(res, ImageColour.xyz*float3(1.0, 1.0, 1.0), ImageColour.w*1.0));

		}

	res.w=1.0;
	return res;
}
// VANILLA POST PROCESS, DO NOT MODIFY!
float4	PS_DrawOriginal(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	float4	res;
	float4	color;

	float2	scaleduv=Params01[6].xy*IN.txcoord0.xy;
	scaleduv=max(scaleduv, 0.0);
	scaleduv=min(scaleduv, Params01[6].zy);

	color=TextureColor.Sample(SamplerPoint, IN.txcoord0.xy); //hdr scene color

	float4	r0, r1, r2, r3;
	r1.xy=scaleduv;
	r0.xyz = color.xyz;
	if (0.5<=Params01[0].x) r1.xy=IN.txcoord0.xy;
	r1.xyz = TextureBloom.Sample(SamplerLinear, r1.xy).xyz;
	r2.xy = TextureAdaptation.Sample(SamplerLinear, IN.txcoord0.xy).xy; //in skyrimse it two component

	r0.w=dot(float3(2.125000e-001, 7.154000e-001, 7.210000e-002), r0.xyz);
	r0.w=max(r0.w, 1.000000e-005);
	r1.w=r2.y/r2.x;
	r2.y=r0.w * r1.w;
	if (0.5<Params01[2].z) r2.z=0xffffffff; else r2.z=0;
	r3.xy=r1.w * r0.w + float2(-4.000000e-003, 1.000000e+000);
	r1.w=max(r3.x, 0.0);
	r3.xz=r1.w * 6.2 + float2(5.000000e-001, 1.700000e+000);
	r2.w=r1.w * r3.x;
	r1.w=r1.w * r3.z + 6.000000e-002;
	r1.w=r2.w / r1.w;
	r1.w=pow(r1.w, 2.2);
	r1.w=r1.w * Params01[2].y;
	r2.w=r2.y * Params01[2].y + 1.0;
	r2.y=r2.w * r2.y;
	r2.y=r2.y / r3.y;
	if (r2.z==0) r1.w=r2.y; else r1.w=r1.w;
	r0.w=r1.w / r0.w;
	r1.w=saturate(Params01[2].x - r1.w);
	r1.xyz=r1 * r1.w;
	r0.xyz=r0 * r0.w + r1;
	r1.x=dot(r0.xyz, float3(2.125000e-001, 7.154000e-001, 7.210000e-002));
	r0.w=1.0;
	r0=r0 - r1.x;
	r0=Params01[3].x * r0 + r1.x;
	r1=Params01[4] * r1.x - r0;
	r0=Params01[4].w * r1 + r0;
	r0=Params01[3].w * r0 - r2.x;
	r0=Params01[3].z * r0 + r2.x;
	r0.xyz=saturate(r0);
	r1.xyz=pow(r1.xyz, Params01[6].w);
	//active only in certain modes, like khajiit vision, otherwise Params01[5].w=0
	r1=Params01[5] - r0;
	res=Params01[5].w * r1 + r0;

//	res.xyz = color.xyz;
//	res.w=1.0;
	return res;
}

///TECHNIQUES
//// COLD UNPPROC.
technique11 NATURAL <string UIName="NAT: Natural (Cold & Harsh)";>
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_NATURAL()));
	}
}
technique11 NATURAL1
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_DepthSharp()));
	}
}
technique11 NATURAL2
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_PFX()));
	}
}

/// RDR2
technique11 ATMOSPHERIC <string UIName="NAT: Atmospheric (Stylized & Cinematic)";>
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_ATMOSPHERIC()));
	}
}
technique11 ATMOSPHERIC1
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_DepthSharp()));
	}
}
technique11 ATMOSPHERIC2
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_PFX()));
	}
}

// WARM PROC.
technique11 NATENB <string UIName="NAT: Natural & Atmospheric (Balanced Mix)";>
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_NATENB()));
	}
}
technique11 NATENB1
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_DepthSharp()));
	}
}
technique11 NATENB2
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
		SetPixelShader(CompileShader(ps_5_0, PS_PFX()));
	}
}


//////////////////////////////////////////////////////////////////////////////////////////
technique11 ORIGINALPOSTPROCESS <string UIName="not a preset";> //do not modify this technique
{
  pass p0
  {
    SetVertexShader(CompileShader(vs_5_0, VS_Draw()));
    SetPixelShader(CompileShader(ps_5_0, PS_DrawOriginal()));
  }
}