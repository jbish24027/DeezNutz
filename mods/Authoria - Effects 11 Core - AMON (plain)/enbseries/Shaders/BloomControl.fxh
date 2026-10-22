//===========================//
// Bloom Control by soulwynd //
// From oldrim MSL by JawZ   //
// Bloom Layer code by Prod80//
// Addtions by Adyss         //
//===========================//
/* going to be implemented soon as i got time to put this into TOD
	float bconD <
		string UIName="Bloom Curve Day";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.3};
	float bconN <
		string UIName="Bloom Curve Night";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.24};
	float bconI <
		string UIName="Bloom Curve Interior";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.24};
	float bloom_L1T_D <
		string UIName="Bloom L1 Threshold Day";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.0};
	float bloom_L1T_N <
		string UIName="Bloom L1 Threshold Night";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.0};
	float bloom_L1T_I <
		string UIName="Bloom L1 Threshold Interior";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.0};
	float bloom_L2T_D <
		string UIName="Bloom L2 Threshold Day";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.125};
	float bloom_L2T_N <
		string UIName="Bloom L2 Threshold Night";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.06};
	float bloom_L2T_I <
		string UIName="Bloom L2 Threshold Interior";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.06};
	float bloom_L3T_D <
		string UIName="Bloom L3 Threshold Day";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.0};
	float bloom_L3T_N <
		string UIName="Bloom L3 Threshold Night";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.0};
	float bloom_L3T_I <
		string UIName="Bloom L3 Threshold Interior";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=1.0;
		float UIStep=0.001;
	> = {0.0};
	float bloom_L1I_D <
		string UIName="Bloom L1 Intensity Day";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {1.0};
	float bloom_L1I_N <
		string UIName="Bloom L1 Intensity Night";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {1.0};
	float bloom_L1I_I <
		string UIName="Bloom L1 Intensity Interior";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {1.0};
	float bloom_L2I_D <
		string UIName="Bloom L2 Intensity Day";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {0.7};
	float bloom_L2I_N <
		string UIName="Bloom L2 Intensity Night";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {1.0};
	float bloom_L2I_I <
		string UIName="Bloom L2 Intensity Interior";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {1.0};	
	float bloom_L3I_D <
		string UIName="Bloom L3 Intensity Day";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {0.33};
	float bloom_L3I_N <
		string UIName="Bloom L3 Intensity Night";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {0.7};
	float bloom_L3I_I <
		string UIName="Bloom L3 Intensity Interior";
		string UIWidget="Spinner";
		float UIMin=0.0;
		float UIMax=2.0;
		float UIStep=0.001;
	> = {0.7}; */

float3 BloomControl(float3 Bloom, float2 coord)
{
float   timeweight;
float   timevalue;		

timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * BInBlackDawn;
timevalue+=TimeOfDay1.y * BInBlackSunrise;
timevalue+=TimeOfDay1.z * BInBlackDay;
timevalue+=TimeOfDay1.w * BInBlackSunset;
timevalue+=TimeOfDay2.x * BInBlackDusk;
timevalue+=TimeOfDay2.y * BInBlackNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float BInBlack;
	BInBlack=lerp( (timevalue / timeweight), BInBlackInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * BInWhiteDawn;
timevalue+=TimeOfDay1.y * BInWhiteSunrise;
timevalue+=TimeOfDay1.z * BInWhiteDay;
timevalue+=TimeOfDay1.w * BInWhiteSunset;
timevalue+=TimeOfDay2.x * BInWhiteDusk;
timevalue+=TimeOfDay2.y * BInWhiteNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float BInWhite;
	BInWhite=lerp( (timevalue / timeweight), BInWhiteInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * BOutWhiteDawn;
timevalue+=TimeOfDay1.y * BOutWhiteSunrise;
timevalue+=TimeOfDay1.z * BOutWhiteDay;
timevalue+=TimeOfDay1.w * BOutWhiteSunset;
timevalue+=TimeOfDay2.x * BOutWhiteDusk;
timevalue+=TimeOfDay2.y * BOutWhiteNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float BOutWhite;
	BOutWhite=lerp( (timevalue / timeweight), BOutWhiteInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * BOutBlackDawn;
timevalue+=TimeOfDay1.y * BOutBlackSunrise;
timevalue+=TimeOfDay1.z * BOutBlackDay;
timevalue+=TimeOfDay1.w * BOutBlackSunset;
timevalue+=TimeOfDay2.x * BOutBlackDusk;
timevalue+=TimeOfDay2.y * BOutBlackNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float BOutBlack;
	BOutBlack=lerp( (timevalue / timeweight), BOutBlackInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * fLightSpreadThresholdDawn;
timevalue+=TimeOfDay1.y * fLightSpreadThresholdSunrise;
timevalue+=TimeOfDay1.z * fLightSpreadThresholdDay;
timevalue+=TimeOfDay1.w * fLightSpreadThresholdSunset;
timevalue+=TimeOfDay2.x * fLightSpreadThresholdDusk;
timevalue+=TimeOfDay2.y * fLightSpreadThresholdNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float fLightSpreadThreshold;
	fLightSpreadThreshold=lerp( (timevalue / timeweight), fLightSpreadThresholdInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * fLightSpreadPowerDawn;
timevalue+=TimeOfDay1.y * fLightSpreadPowerSunrise;
timevalue+=TimeOfDay1.z * fLightSpreadPowerDay;
timevalue+=TimeOfDay1.w * fLightSpreadPowerSunset;
timevalue+=TimeOfDay2.x * fLightSpreadPowerDusk;
timevalue+=TimeOfDay2.y * fLightSpreadPowerNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float fLightSpreadPower;
	fLightSpreadPower=lerp( (timevalue / timeweight), fLightSpreadPowerInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * fGlowThresholdDawn;
timevalue+=TimeOfDay1.y * fGlowThresholdSunrise;
timevalue+=TimeOfDay1.z * fGlowThresholdDay;
timevalue+=TimeOfDay1.w * fGlowThresholdSunset;
timevalue+=TimeOfDay2.x * fGlowThresholdDusk;
timevalue+=TimeOfDay2.y * fGlowThresholdNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float fGlowThreshold;
	fGlowThreshold=lerp( (timevalue / timeweight), fGlowThresholdInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * fGlowPowerDawn;
timevalue+=TimeOfDay1.y * fGlowPowerSunrise;
timevalue+=TimeOfDay1.z * fGlowPowerDay;
timevalue+=TimeOfDay1.w * fGlowPowerSunset;
timevalue+=TimeOfDay2.x * fGlowPowerDusk;
timevalue+=TimeOfDay2.y * fGlowPowerNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float fGlowPower;
	fGlowPower=lerp( (timevalue / timeweight), fGlowPowerInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * fBloomMaxWhiteDawn;
timevalue+=TimeOfDay1.y * fBloomMaxWhiteSunrise;
timevalue+=TimeOfDay1.z * fBloomMaxWhiteDay;
timevalue+=TimeOfDay1.w * fBloomMaxWhiteSunset;
timevalue+=TimeOfDay2.x * fBloomMaxWhiteDusk;
timevalue+=TimeOfDay2.y * fBloomMaxWhiteNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float fBloomMaxWhite;
	fBloomMaxWhite=lerp( (timevalue / timeweight), fBloomMaxWhiteInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * fBSaturationDawn;
timevalue+=TimeOfDay1.y * fBSaturationSunrise;
timevalue+=TimeOfDay1.z * fBSaturationDay;
timevalue+=TimeOfDay1.w * fBSaturationSunset;
timevalue+=TimeOfDay2.x * fBSaturationDusk;
timevalue+=TimeOfDay2.y * fBSaturationNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float fBSaturation;
	fBSaturation=lerp( (timevalue / timeweight), fBSaturationInterior, EInteriorFactor );
	
timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * fBLumRGBDawn;
timevalue+=TimeOfDay1.y * fBLumRGBSunrise;
timevalue+=TimeOfDay1.z * fBLumRGBDay;
timevalue+=TimeOfDay1.w * fBLumRGBSunset;
timevalue+=TimeOfDay2.x * fBLumRGBDusk;
timevalue+=TimeOfDay2.y * fBLumRGBNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float3 fBLumRGB;
	fBLumRGB=lerp( (timevalue / timeweight), fBLumRGBInterior, EInteriorFactor );
	
	/*
	float bloom_L1T		= lerp( lerp( bloom_L1T_N, bloom_L1T_D, ENightDayFactor ), bloom_L1T_I, EInteriorFactor );
	float bloom_L1I		= lerp( lerp( bloom_L1I_N, bloom_L1I_D, ENightDayFactor ), bloom_L1I_I, EInteriorFactor ) * ENBParams01.x;
	float bloom_L2T		= lerp( lerp( bloom_L2T_N, bloom_L2T_D, ENightDayFactor ), bloom_L2T_I, EInteriorFactor );
	float bloom_L2I		= lerp( lerp( bloom_L2I_N, bloom_L2I_D, ENightDayFactor ), bloom_L2I_I, EInteriorFactor ) * ENBParams01.x;
	float bloom_L3T		= lerp( lerp( bloom_L3T_N, bloom_L3T_D, ENightDayFactor ), bloom_L3T_I, EInteriorFactor );
	float bloom_L3I		= lerp( lerp( bloom_L3I_N, bloom_L3I_D, ENightDayFactor ), bloom_L3I_I, EInteriorFactor ) * ENBParams01.x;
	float bcontrast		= lerp( lerp( bconN, bconD, ENightDayFactor ), bconI, EInteriorFactor );
	
	//Layers
	float3 bloom_L1		= max( Bloom.xyz - bloom_L1T, 0.0f ) * bloom_L1I;
	float3 bloom_L2		= max( Bloom.xyz - bloom_L2T, 0.0f ) * bloom_L2I;
	float3 bloom_L3		= max( Bloom.xyz - bloom_L3T, 0.0f ) * bloom_L3I;
	Bloom.xyz		    = bloom_L1.xyz + bloom_L2.xyz + bloom_L3.xyz;
	
	// Bloom Contrast
	Bloom.xyz		= lerp( Bloom.xyz, Bloom.xyz * Bloom.xyz, bcontrast );
	*/
	
	// Bloom Cutoff
	Bloom=max(Bloom-BInBlack, 0.0) / max(BInWhite-BInBlack, 0.0001);
	Bloom=Bloom*(BOutWhite-BOutBlack) + BOutBlack;
	
	// Bloom Lightspread
    Bloom.xyz += max(0.0, (Bloom.xyz - fLightSpreadThreshold * 0.1) * fLightSpreadPower * (1.0 - TextureBloom.Sample(Sampler1, coord.xy)));

    // Bloom Glow
    Bloom.xyz += max(0.0, (Bloom.xyz - fGlowThreshold * 0.1) * fGlowPower);

    // Compress and scale bloom
    Bloom = (Bloom * (1.0f + Bloom / (fBloomMaxWhite * fBloomMaxWhite))) / (1.0f + Bloom); /// Scale bloom luminance within a displayable range of 0 to 1

    // Luminance Saturation
    float3 avgBloomLuma = AvgLuma(Bloom.xyz).w;  /// Average the scene bloom luminance
    Bloom.xyz = lerp(avgBloomLuma.xyz, Bloom.xyz, fBSaturation * float3(fBLumRGB.x, fBLumRGB.y, fBLumRGB.z));
	
	return Bloom;
}