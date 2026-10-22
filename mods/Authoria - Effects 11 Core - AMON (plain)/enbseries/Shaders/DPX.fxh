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