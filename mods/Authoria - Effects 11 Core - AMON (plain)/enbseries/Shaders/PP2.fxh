//=================================//
// PP2 by Boris without Adaptation //
//=================================//

float4 PP2(float4 color)
{

float   timeweight;
float   timevalue;

timeweight=0.000001;
timevalue=0.0;

timevalue+=TimeOfDay1.x * EBrightnessV2Dawn;
timevalue+=TimeOfDay1.y * EBrightnessV2Sunrise;
timevalue+=TimeOfDay1.z * EBrightnessV2Day;
timevalue+=TimeOfDay1.w * EBrightnessV2Sunset;
timevalue+=TimeOfDay2.x * EBrightnessV2Dusk;
timevalue+=TimeOfDay2.y * EBrightnessV2Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float newEBrightnessV2;
	newEBrightnessV2=lerp((timevalue / timeweight), EBrightnessV2Interior, EInteriorFactor );

timeweight=0.000001;
timevalue=0.0;

	
timevalue+=TimeOfDay1.x * EColorSaturationV2Dawn;
timevalue+=TimeOfDay1.y * EColorSaturationV2Sunrise;
timevalue+=TimeOfDay1.z * EColorSaturationV2Day;
timevalue+=TimeOfDay1.w * EColorSaturationV2Sunset;
timevalue+=TimeOfDay2.x * EColorSaturationV2Dusk;
timevalue+=TimeOfDay2.y * EColorSaturationV2Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float newEColorSaturationV2;
	newEColorSaturationV2=lerp((timevalue / timeweight), EColorSaturationV2Interior, EInteriorFactor );

timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * EToneMappingCurveV2Dawn;
timevalue+=TimeOfDay1.y * EToneMappingCurveV2Sunrise;
timevalue+=TimeOfDay1.z * EToneMappingCurveV2Day;
timevalue+=TimeOfDay1.w * EToneMappingCurveV2Sunset;
timevalue+=TimeOfDay2.x * EToneMappingCurveV2Dusk;
timevalue+=TimeOfDay2.y * EToneMappingCurveV2Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float newEToneMappingCurve;
	newEToneMappingCurve=lerp( (timevalue / timeweight), EToneMappingCurveV2Interior, EInteriorFactor );

timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * EIntensityContrastV2Dawn;
timevalue+=TimeOfDay1.y * EIntensityContrastV2Sunrise;
timevalue+=TimeOfDay1.z * EIntensityContrastV2Day;
timevalue+=TimeOfDay1.w * EIntensityContrastV2Sunset;
timevalue+=TimeOfDay2.x * EIntensityContrastV2Dusk;
timevalue+=TimeOfDay2.y * EIntensityContrastV2Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
	
	float newEIntensityContrastV2;
	newEIntensityContrastV2=lerp( (timevalue / timeweight), EIntensityContrastV2Interior, EInteriorFactor );

timeweight=0.000001;
timevalue=0.0;
	
timevalue+=TimeOfDay1.x * EToneMappingOversaturationV2Dawn;
timevalue+=TimeOfDay1.y * EToneMappingOversaturationV2Sunrise;
timevalue+=TimeOfDay1.z * EToneMappingOversaturationV2Day;
timevalue+=TimeOfDay1.w * EToneMappingOversaturationV2Sunset;
timevalue+=TimeOfDay2.x * EToneMappingOversaturationV2Dusk;
timevalue+=TimeOfDay2.y * EToneMappingOversaturationV2Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;

	float newEToneMappingOversaturationV2;
	newEToneMappingOversaturationV2=lerp( (timevalue / timeweight), EToneMappingOversaturationV2Interior, EInteriorFactor );
	
	// Actual Shader
    if (USE_PP2==true) {
	color.xyz*=(newEBrightnessV2);
	color.xyz+=0.000001;
	float3 xncol=normalize(color.xyz);
	float3 scl=color.xyz/xncol.xyz;
	scl=pow(scl, newEIntensityContrastV2);
	xncol.xyz=pow(xncol.xyz, newEColorSaturationV2);
	color.xyz=scl*xncol.xyz;

	float	lumamax=newEToneMappingOversaturationV2;
	color.xyz=(color.xyz * (1.0 + color.xyz/lumamax))/(color.xyz + newEToneMappingCurve);
	}
	return color;
}