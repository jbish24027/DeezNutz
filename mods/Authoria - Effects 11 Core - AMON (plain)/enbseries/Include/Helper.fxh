/////////////////////////////////////////////////////////
//        ____       __    __   ________   __    __    //
//       /    \     |  \  /  | |  ___   | |  \  |  |   //
//      /  /\  \    |   \/   | |  |  |  | |   \ |  |   //
//     /  ____  \   |        | |  |  |  | |    \|  |   //
//    /  /    \  \  |  |\/|  | |  |__|  | |  |\    |   //
//   /__/      \__\ |__|  |__| |________| |__| \___|   //
//   ENB   FOR   OBSIDIAN   WEATHERS   AND   SEASONS   //
//                                                     //
/////////////////////////////////////////////////////////
//         _   _  ____  __    ____  ____  ____         //
//        ( )_( )( ___)(  )  (  _ \( ___)(  _ \        //
//         ) _ (  )__)  )(__  )___/ )__)  )   /        //
//        (_) (_)(____)(____)(__)  (____)(_)\_)        //
//                                                     //
/////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
//  ____  _  _  ____  ____  ____  _  _    __    __      ____   __    ____    __    __  __  ____  ____  ____  ____  ___  //
// ( ___)( \/ )(_  _)( ___)(  _ \( \( )  /__\  (  )    (  _ \ /__\  (  _ \  /__\  (  \/  )( ___)(_  _)( ___)(  _ \/ __) //
//  )__)  )  (   )(   )__)  )   / )  (  /(__)\  )(__    )___//(__)\  )   / /(__)\  )    (  )__)   )(   )__)  )   /\__ \ //
// (____)(_/\_) (__) (____)(_)\_)(_)\_)(__)(__)(____)  (__) (__)(__)(_)\_)(__)(__)(_/\/\_)(____) (__) (____)(_)\_)(___/ //
//                                                                                                                      //
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

float4  Timer;                  // x = generic timer in range 0..1, period of 16777216 ms (4.6 hours), y = average fps, w = frame time elapsed (in seconds)
float4  ScreenSize;             // x = Width, y = 1/Width, z = Width/Height, w = Height/Width
float   AdaptiveQuality;        // changes in range 0..1, 0 means full quality, 1 lowest dynamic quality (0.33, 0.66 are limits for quality levels)
float4  Weather;                // x = current weather index, y = outgoing weather index, z = weather transition, w = time of the day in 24 standart hours.
float4  TimeOfDay1;             // x = dawn, y = sunrise, z = day, w = sunset. Interpolators range from 0..1
float4  TimeOfDay2;             // x = dusk, y = night. Interpolators range from 0..1
float   ENightDayFactor;        // changes in range 0..1, 0 means that night time, 1 - day time
float   EInteriorFactor;        // changes 0 or 1. 0 means that exterior, 1 - interior
float4  SunDirection;           // Prepass exclusive. Refrence here: https://cdn.discordapp.com/attachments/335788870849265675/532859588203249666/unknown.png
float4  Params01[7];            // skyrimse parameters
float4  ENBParams01;            // x - bloom amount, y - lens amount
float4  DofParameters;          // z = ApertureTime multiplied by time elapsed, w = FocusingTime multiplied by time elapsed
float4  LightParameters;        // xy = sun position on screen, w = visibility

float4  tempF1, tempF2, tempF3; // 0,1,2,3,4,5,6,7,8,9
float4  tempInfo1;
float4  tempInfo2;              // xy = cursor position of previous left click, zw = cursor position of previous right click

static const float2 PixelSize  = float2(ScreenSize.y, ScreenSize.y * ScreenSize.z); // As in Reshade
static const float2 Resolution = float2(ScreenSize.x, ScreenSize.x * ScreenSize.w); // Display Resolution


/////////////////////////////////////////////////////////
//   ____  ____  _  _  ____  __  __  ____  ____  ___   //
//  (_  _)( ___)( \/ )(_  _)(  )(  )(  _ \( ___)/ __)  //
//    )(   )__)  )  (   )(   )(__)(  )   / )__) \__ \  //
//   (__) (____)(_/\_) (__) (______)(_)\_)(____)(___/  //
//                                                     //
/////////////////////////////////////////////////////////

Texture2D           TextureOriginal;        // color R16B16G16A16 64 bit or R11G11B10 32 bit hdr format, screen size. PLEASE AVOID USING IT BECAUSE OF ALIASING ARTIFACTS, UNLESS YOU FIX THEM
Texture2D           TextureColor;           // color which is output of previous technique (except when drawed to temporary render target), R16B16G16A16 64 bit hdr format. screen size
Texture2D           TextureDownsampled;     // color R16B16G16A16 64 bit or R11G11B10 32 bit hdr format. 1024*1024 size
Texture2D           TextureDepth;           // scene depth R32F 32 bit hdr format, screen size. PLEASE AVOID USING IT BECAUSE OF ALIASING ARTIFACTS, UNLESS YOU FIX THEM
Texture2D           TextureFocus;           // this frame focus 1*1 R32F hdr red channel only. computed in PS_Focus
Texture2D           TextureAperture;        // this frame aperture 1*1 R32F hdr red channel only. computed in PS_Aperture of enbdepthoffield.fx
Texture2D           TextureMask;            // mask of underwater area of screen
Texture2D           TextureBloom;           // vanilla or enb bloom
Texture2D           TextureLens;            // enb lens fx
Texture2D           TextureAdaptation;      // vanilla or enb adaptation
Texture2D           TextureCurrent;
Texture2D           TexturePrevious;
Texture2D           TexturePalette;         //enbpalette texture, if loaded and enabled in [colorcorrection].

// temporary textures which can be set as render target for techniques via annotations like <string RenderTarget="RenderTargetRGBA32";>
Texture2D           RenderTarget1024;       // R16B16G16A16F 64 bit hdr format, 1024*1024 size
Texture2D           RenderTarget512;        // R16B16G16A16F 64 bit hdr format, 512*512 size
Texture2D           RenderTarget256;        // R16B16G16A16F 64 bit hdr format, 256*256 size
Texture2D           RenderTarget128;        // R16B16G16A16F 64 bit hdr format, 128*128 size
Texture2D           RenderTarget64;         // R16B16G16A16F 64 bit hdr format, 64*64 size
Texture2D           RenderTarget32;         // R16B16G16A16F 64 bit hdr format, 32*32 size
Texture2D           RenderTarget16;         // R16B16G16A16F 64 bit hdr format, 16*16 size
Texture2D           RenderTargetRGBA32;     // R8G8B8A8 32 bit ldr format
Texture2D           RenderTargetRGBA64;     // R16B16G16A16 64 bit ldr format
Texture2D           RenderTargetRGBA64F;    // R16B16G16A16F 64 bit hdr format
Texture2D           RenderTargetR16F;       // R16F 16 bit hdr format with red channel only
Texture2D           RenderTargetR32F;       // R32F 32 bit hdr format with red channel only
Texture2D           RenderTargetRGB32F;     // 32 bit hdr format without alpha


////////////////////////////////////////////////////////
//  ___    __    __  __  ____  __    ____  ____  ___  //
// / __)  /__\  (  \/  )(  _ \(  )  ( ___)(  _ \/ __) //
// \__ \ /(__)\  )    (  )___/ )(__  )__)  )   /\__ \ //
// (___/(__)(__)(_/\/\_)(__)  (____)(____)(_)\_)(___/ //
//                                                    //
////////////////////////////////////////////////////////

SamplerState        PointSampler            // Sampler0
{
    Filter = MIN_MAG_MIP_POINT;
    AddressU = Clamp;
    AddressV = Clamp;
};
SamplerState        LinearSampler           // Sampler1
{
    Filter = MIN_MAG_MIP_LINEAR;
    AddressU = Clamp;
    AddressV = Clamp;
};
SamplerState        WrapSampler
{
    Filter = MIN_MAG_MIP_LINEAR;
    AddressU = Wrap;
    AddressV = Wrap;
};
SamplerState        MirrorSampler
{
    Filter = MIN_MAG_MIP_LINEAR;
    AddressU = Mirror;
    AddressV = Mirror;
};
SamplerState        BorderSampler
{
    Filter = MIN_MAG_MIP_LINEAR;
    AddressU = Border;
    AddressV = Border;
};
SamplerState        Sampler0 
{
    Filter = MIN_MAG_MIP_POINT;
    AddressU = Clamp;   
    AddressV = Clamp;
};
SamplerState        Sampler1 
{
    Filter = MIN_MAG_MIP_LINEAR;
    AddressU = Clamp;   
    AddressV = Clamp;
};


//////////////////////////////////////////////////////////////
//  ___  ____  ____  __  __  ___  ____  __  __  ____  ____  //
// / __)(_  _)(  _ \(  )(  )/ __)(_  _)(  )(  )(  _ \( ___) //
// \__ \  )(   )   / )(__)(( (__   )(   )(__)(  )   / )__)  //
// (___/ (__) (_)\_)(______)\___) (__) (______)(_)\_)(____) //
//                                                          //
//////////////////////////////////////////////////////////////

struct VS_INPUT_POST
{
    float3 pos     : POSITION;
    float2 txcoord : TEXCOORD0;
};

struct VS_INPUT
{
    float3 pos     : POSITION;
    float2 txcoord : TEXCOORD0;
};

struct VS_OUTPUT_POST
{
    float4 pos     : SV_POSITION;
    float2 txcoord : TEXCOORD0;
};

struct VS_OUTPUT_DOF
{
    float4 pos      : SV_POSITION;
    float2 txcoord      : TEXCOORD0;
    float2 vertices[10]     : TEXCOORD1;
};

struct VS_OUTPUT
{
    float4 pos     : SV_POSITION;
    float2 txcoord : TEXCOORD0;
};


//////////////////////////////////////////////////////////////////////////////////
//  _  _  ____  ____  ____  ____  _  _    ___  _   _    __    ____  ____  ____  //
// ( \/ )( ___)(  _ \(_  _)( ___)( \/ )  / __)( )_( )  /__\  (  _ \( ___)(  _ \ //
//  \  /  )__)  )   /  )(   )__)  )  (   \__ \ ) _ (  /(__)\  )(_) ))__)  )   / //
//   \/  (____)(_)\_) (__) (____)(_/\_)  (___/(_) (_)(__)(__)(____/(____)(_)\_) //
//                                                                              //
//////////////////////////////////////////////////////////////////////////////////

void VS_Quad( inout float4 pos : SV_POSITION, inout float2 txcoord0 : TEXCOORD0)
{
    pos.w     = 1.0;
    txcoord0 -= 7.0 / 256.0;
}

VS_OUTPUT_POST  VS_Draw(VS_INPUT_POST IN)
{
    VS_OUTPUT_POST OUT;
    OUT.pos = float4(IN.pos.xyz, 1.0);
    OUT.txcoord.xy = IN.txcoord.xy;
    return OUT;
}

VS_OUTPUT_POST  VS_PostProcess(VS_INPUT_POST IN)
{
    VS_OUTPUT_POST  OUT;
    float4  pos;
    pos.xyz=IN.pos.xyz;
    pos.w=1.0;
    OUT.pos=pos;
    OUT.txcoord.xy=IN.txcoord.xy;
    return OUT;
}


/////////////////////////////////////////////////////////////
//  ____  __  __  _  _  ___  ____  ____  _____  _  _  ___  //
// ( ___)(  )(  )( \( )/ __)(_  _)(_  _)(  _  )( \( )/ __) //
//  )__)  )(__)(  )  (( (__   )(   _)(_  )(_)(  )  ( \__ \ //
// (__)  (______)(_)\_)\___) (__) (____)(_____)(_)\_)(___/ //
//                                                         //
/////////////////////////////////////////////////////////////

////////////////////////////////////////////////////
// Depth Linearization (Thanks to Marty and Trey) //
////////////////////////////////////////////////////

float GetLinearizedDepth(float2 coord)
{
    float depth = TextureDepth.Sample(PointSampler, coord);
    depth *= rcp(mad(depth,-2999.0,3000.0));
    return depth;
}

////////////////////////////////
// Get Luma function by TreyM //
////////////////////////////////

// Luma Coefficients
#define Rec709      0
#define Rec709_5    1
#define Rec601      2
#define Rec2020     3
#define Lum333      4

// Calculate perceived luminance color by using the ITU-R BT standards
float GetLuma(in float3 color, int btspec)
{
    static const float3 LumaCoeff[5] =
    {
        // 0: HD TV - Rec.709
        float3(0.2126, 0.7152f, 0.0722),
        // 1: HD TV - Rec.709-5
        float3(0.212395, 0.701049, 0.086556),
        // 2: CRT TV - Rec.601
        float3(0.299, 0.587, 0.114),
        // 3: HDR Spec - Rec.2020
        float3(0.2627, 0.6780, 0.0593),
        // 4: Incorrect Equal Weighting
        float3(0.3333, 0.3333, 0.3333)
    };

    //return sqrt(dot(color.rgb * color.rgb, LumaCoeff[btspec])); // Requires sRGB input
    return dot(color.rgb, LumaCoeff[btspec]);
}


/////////////////
// CONVERSIONS //
/////////////////

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

/////////////////////////////////////////////

float3 RGB2HSL(in float3 RGB)
{
    float3 HCV = RGB2HCV(RGB);
    float L = HCV.z - HCV.y * 0.5;
    float S = HCV.y / (1.0000001 - abs(L * 2 - 1));
    
    return float3(HCV.x, S, L);
}

/////////////////////////////////////////////

float3 HSL2RGB(in float3 HSL)
{
    HSL = saturate(HSL);
    //HSL.z *= 0.99;
    float3 RGB = saturate(float3(abs(HSL.x * 6.0 - 3.0) - 1.0,2.0 - abs(HSL.x * 6.0 - 2.0),2.0 - abs(HSL.x * 6.0 - 4.0)));
    float C = (1 - abs(2 * HSL.z - 1)) * HSL.y;
    
    return (RGB - 0.5) * C + HSL.z;
}