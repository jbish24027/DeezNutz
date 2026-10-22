//=========================//
// Technicolor 2 by Prod80 //
//=========================//
float4 Technicolor2(float4 color)
{
    float4 res;
if ( use_t2s == true ) 
{
   float3 rChannel      = lerp( lerp( rChannelN, rChannelD, ENightDayFactor ), rChannelI, EInteriorFactor );
   float3 gChannel      = lerp( lerp( gChannelN, gChannelD, ENightDayFactor ), gChannelI, EInteriorFactor );
   float3 bChannel      = lerp( lerp( bChannelN, bChannelD, ENightDayFactor ), bChannelI, EInteriorFactor );
   float strip2vib      = lerp( lerp( strip2vibN, strip2vibD, ENightDayFactor ), strip2vibI, EInteriorFactor );
   float techStrength2   = lerp( lerp( techStrength2N, techStrength2D, ENightDayFactor ), techStrength2I, EInteriorFactor );
   
   color.rgb         = saturate( color.rgb );
   float t2stripRed   = dot( color.rgb, rChannel.rgb / dot( rChannel.rgb, 1 ));
   float t2stripGreen   = dot( color.rgb, gChannel.rgb / dot( gChannel.rgb, 1 ));
   float t2stripBlue   = dot( color.rgb, bChannel.rgb / dot( bChannel.rgb, 1 ));
   
   float3 t2scolor      = float3( t2stripRed, t2stripGreen, t2stripBlue );
   
   t2scolor.rgb      = saturate( t2scolor.rgb );
   t2scolor.rgb      = RGBToHSL( t2scolor.rgb );
   t2scolor.g         = t2scolor.g + (( 1.0f - t2scolor.g ) * ( strip2vib * t2scolor.g ));
   t2scolor.rgb      = HSLToRGB( t2scolor.rgb );
   color.rgb         = lerp( color.rgb, t2scolor.rgb, techStrength2 );
}
  	res.xyz=saturate(color);
	res.w=1.0;
	return res;
}