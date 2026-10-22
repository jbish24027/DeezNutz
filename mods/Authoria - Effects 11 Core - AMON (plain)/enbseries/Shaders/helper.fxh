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

