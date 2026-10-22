//================//
// Tint by Prod80 //
//================//
float4 Tint(float4 color)
{
    float4 res;
if (use_tinting==true)
{
   float3   RGB_Tint      = lerp( lerp( RGB_TintN, RGB_TintD,   ENightDayFactor ), RGB_TintI, EInteriorFactor );
   float    DesatMids      = lerp( lerp( DesatMidsN, DesatMidsD, ENightDayFactor ), DesatMidsI, EInteriorFactor );
   float   DesatShadows   = lerp( lerp( DesatShadowsN, DesatShadowsD, ENightDayFactor ), DesatShadowsI, EInteriorFactor );
   float   DesatOrig      = lerp( lerp( DesatOrigN, DesatOrigD, ENightDayFactor ), DesatOrigI, EInteriorFactor );
   float3    Toned          = lerp( lerp( TonedN, TonedD, ENightDayFactor ), TonedI, EInteriorFactor );
   float    ShadowStr      = lerp( lerp( ShadowStrN, ShadowStrD, ENightDayFactor ), ShadowStrI, EInteriorFactor );
   float   TintPower      = lerp( lerp( TintPowerN,   TintPowerD, ENightDayFactor ), TintPowerI, EInteriorFactor );
   float   ShadowPower      = lerp( lerp( ShadowPowerN, ShadowPowerD, ENightDayFactor ), ShadowPowerI, EInteriorFactor );
   float   HighlightPower   = lerp( lerp( HighlightPowerN, HighlightPowerD, ENightDayFactor ), HighlightPowerI, EInteriorFactor );
   float   SHueAdjust      = lerp( lerp( SHueAdjustN, SHueAdjustD, ENightDayFactor ), SHueAdjustI, EInteriorFactor );
   
   color.rgb            = saturate( color.rgb );
   
   float gray            = dot( color.rgb, 0.33333333 );
   float shadows         = pow( 1 - gray, TintPower + ShadowPower );
   float highlights      = pow( gray, TintPower + HighlightPower );
   float midtones         = saturate( 1 - shadows - highlights );
   
   float3 RGB_Shadows      = RGBToHSL( RGB_Tint.rgb );
   RGB_Shadows.r         += 0.5 + SHueAdjust;
      if ( RGB_Shadows.r > 1.0 ) RGB_Shadows.r -= 1.0;
      if ( RGB_Shadows.r < 0.0 ) RGB_Shadows.r += 1.0;
   
   RGB_Shadows.rgb         = saturate( RGB_Shadows.rgb );
   float3 temp_shadows      = RGB_Shadows.rgb;
   RGB_Shadows.rgb         = HSLToRGB( RGB_Shadows.rgb );
   
   //Create gradient
   float3 cg            = saturate( midtones * RGB_Tint.rgb + shadows * RGB_Shadows.rgb + highlights );

   //Mix back with gray 0.33333333, other 'luma' values are INACCURATE in this effect at this stage!
   cg.rgb                = RGBToHSL( cg.rgb );
   cg.rgb                = HSLToRGB( float3( cg.rg, gray ));

   //Shadow color, saturation and final mixing
   temp_shadows.b         = max( temp_shadows.b - ( temp_shadows.b - ShadowStr ), 0.0 );
   temp_shadows.rgb      = HSLToRGB( temp_shadows.rgb );
   cg.rgb                = max( temp_shadows.rgb, cg.rgb );
   cg.rgb               = lerp( cg.rgb, lerp( cg.rgb, grayValue( cg.rgb ), shadows ), DesatShadows );
   cg.rgb                = lerp( cg.rgb, lerp( cg.rgb, grayValue( cg.rgb ), midtones ), DesatMids );
   color.rgb             = lerp( color.rgb, grayValue( color.rgb ), DesatOrig );
   color.rgb             = lerp( color.rgb, cg.rgb, Toned.rgb );
   }
  res.xyz=saturate(color);
  res.w=1.0;
  return res;

}