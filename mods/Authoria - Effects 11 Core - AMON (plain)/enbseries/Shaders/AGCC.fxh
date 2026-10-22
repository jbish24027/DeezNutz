//===================================//
// Based on kingeric1992`s AGCC code //
//===================================//

float4 AGCC_Color(float4 INcolor, float2 INmiddlegray)
{
float   timeweight;
float   timevalue;

timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * TOD_Sat_Dawn;
timevalue+=TimeOfDay1.y * TOD_Sat_Sunrise;
timevalue+=TimeOfDay1.z * TOD_Sat_Day;
timevalue+=TimeOfDay1.w * TOD_Sat_Sunset;
timevalue+=TimeOfDay2.x * TOD_Sat_Dusk;
timevalue+=TimeOfDay2.y * TOD_Sat_Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float TOD_Sat;
   TOD_Sat=lerp( (timevalue / timeweight), TOD_Sat_Interior, EInteriorFactor );

timeweight=0.000001;   
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * TOD_Cont_Dawn;
timevalue+=TimeOfDay1.y * TOD_Cont_Sunrise;
timevalue+=TimeOfDay1.z * TOD_Cont_Day;
timevalue+=TimeOfDay1.w * TOD_Cont_Sunset;
timevalue+=TimeOfDay2.x * TOD_Cont_Dusk;
timevalue+=TimeOfDay2.y * TOD_Cont_Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float TOD_Cont;
   TOD_Cont=lerp( (timevalue / timeweight), TOD_Cont_Interior, EInteriorFactor );
   
timeweight=0.000001;   
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * TOD_Brig_Dawn;
timevalue+=TimeOfDay1.y * TOD_Brig_Sunrise;
timevalue+=TimeOfDay1.z * TOD_Brig_Day;
timevalue+=TimeOfDay1.w * TOD_Brig_Sunset;
timevalue+=TimeOfDay2.x * TOD_Brig_Dusk;
timevalue+=TimeOfDay2.y * TOD_Brig_Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float TOD_Brig;
   TOD_Brig=lerp( (timevalue / timeweight), TOD_Brig_Interior, EInteriorFactor );
   
timeweight=0.000001;   
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * TOD_Tint_Dawn;
timevalue+=TimeOfDay1.y * TOD_Tint_Sunrise;
timevalue+=TimeOfDay1.z * TOD_Tint_Day;
timevalue+=TimeOfDay1.w * TOD_Tint_Sunset;
timevalue+=TimeOfDay2.x * TOD_Tint_Dusk;
timevalue+=TimeOfDay2.y * TOD_Tint_Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float TOD_Tint;
   TOD_Tint=lerp( (timevalue / timeweight), TOD_Tint_Interior, EInteriorFactor );
   
timeweight=0.000001;   
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * TOD_Fade_Dawn;
timevalue+=TimeOfDay1.y * TOD_Fade_Sunrise;
timevalue+=TimeOfDay1.z * TOD_Fade_Day;
timevalue+=TimeOfDay1.w * TOD_Fade_Sunset;
timevalue+=TimeOfDay2.x * TOD_Fade_Dusk;
timevalue+=TimeOfDay2.y * TOD_Fade_Night;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float TOD_Fade;
   TOD_Fade=lerp( (timevalue / timeweight), TOD_Fade_Interior, EInteriorFactor );
   
    INmiddlegray.y = 1.0;
	
    float  saturation  = Params01[3].x + TOD_Sat ;   // 0 == gray scale
    float  contrast    = Params01[3].z + TOD_Cont;   // 0 == no contrast
    float  brightness  = Params01[3].w + TOD_Brig;   // intensity
    float3 tint_color  = Params01[4].rgb         ;   // tint color
    float  tint_weight = Params01[4].w + TOD_Tint;   // 0 == no tint
    float3 fade        = Params01[5].xyz         ;   // fade current scene to specified color, mostly used in special effects
    float  fade_weight = Params01[5].w + TOD_Fade;   // 0 == no fade
    
    INcolor.a   = dot (INcolor.rgb, LUM_709);
    INcolor.rgb = lerp(INcolor.a, INcolor.rgb, saturation);
    INcolor.rgb = lerp(INcolor.rgb, tint_color * INcolor.a , tint_weight);
    INcolor.rgb = lerp(INmiddlegray.x, INcolor.rgb * brightness, contrast);
    INcolor.rgb = lerp(INcolor.rgb, fade, fade_weight);
    INcolor.a = 1.0;
	
	return INcolor;
}