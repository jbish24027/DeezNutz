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