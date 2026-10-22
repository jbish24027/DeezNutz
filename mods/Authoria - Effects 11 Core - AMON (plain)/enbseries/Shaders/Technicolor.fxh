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