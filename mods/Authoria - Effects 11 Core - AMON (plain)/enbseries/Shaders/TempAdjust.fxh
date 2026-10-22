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