//=================================//
// Eye Adaptation Shader by Prod80 //
// Based on work by Rim van Wersch //
//=================================//

float4 eyeadapt(float4 color)
{

float   timeweight;
float   timevalue;

timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * minAdaptDawn;
timevalue+=TimeOfDay1.y * minAdaptSunrise;
timevalue+=TimeOfDay1.z * minAdaptDay;
timevalue+=TimeOfDay1.w * minAdaptSunset;
timevalue+=TimeOfDay2.x * minAdaptDusk;
timevalue+=TimeOfDay2.y * minAdaptNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float minAdapt;
   minAdapt=lerp( (timevalue / timeweight), minAdaptInterior, EInteriorFactor );

timeweight=0.000001;
timevalue=0.0;   

timevalue+=TimeOfDay1.x * maxAdaptDawn;
timevalue+=TimeOfDay1.y * maxAdaptSunrise;
timevalue+=TimeOfDay1.z * maxAdaptDay;
timevalue+=TimeOfDay1.w * maxAdaptSunset;
timevalue+=TimeOfDay2.x * maxAdaptDusk;
timevalue+=TimeOfDay2.y * maxAdaptNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float maxAdapt;
   maxAdapt=lerp( (timevalue / timeweight), maxAdaptInterior, EInteriorFactor );

timeweight=0.000001;
timevalue=0.0;   
   
timevalue+=TimeOfDay1.x * middleGrayDawn;
timevalue+=TimeOfDay1.y * middleGraySunrise;
timevalue+=TimeOfDay1.z * middleGrayDay;
timevalue+=TimeOfDay1.w * middleGraySunset;
timevalue+=TimeOfDay2.x * middleGrayDusk;
timevalue+=TimeOfDay2.y * middleGrayNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float middleGray;
   middleGray=lerp( (timevalue / timeweight), middleGrayInterior, EInteriorFactor );
   
timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * maxLumaDawn;
timevalue+=TimeOfDay1.y * maxLumaSunrise;
timevalue+=TimeOfDay1.z * maxLumaDay;
timevalue+=TimeOfDay1.w * maxLumaSunset;
timevalue+=TimeOfDay2.x * maxLumaDusk;
timevalue+=TimeOfDay2.y * maxLumaNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float maxLuma;
   maxLuma=lerp( (timevalue / timeweight), maxLumaInterior, EInteriorFactor );
   

    float EyeAdapt      = grayValue( TextureAdaptation.Sample(Sampler1, 0.5 ).xyz );
    float pixelLuma     = grayValue( color.xyz );
    EyeAdapt            = clamp( EyeAdapt, minAdapt, maxAdapt );
   
    float scaledLuma    = ( pixelLuma * middleGray ) / EyeAdapt;
    float compLuma      = ( scaledLuma * ( 1.0f + ( scaledLuma / ( maxLuma * maxLuma )))) / ( 1.0f + scaledLuma );
   
    color.xyz          *= compLuma;
	return color;
}