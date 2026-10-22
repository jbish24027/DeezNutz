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