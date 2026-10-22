//====================================================================================//
// A additional switch for switching between Reinhard-modified and Filmic ALU by Heji //
// HLSL code by kingeric1992                                                          //
//====================================================================================//

float3 Filmic_AGCC(float3 color, float2 middlegray)
{
    bool   UseFilmic   = (0.5<Params01[2].z);
    float  WhiteFactor = Params01[2].y;
	
    float DELTA         = max(0,0.00000001);
    
    float  original_lum = max( dot(LUM_709, color.rgb), DELTA);
    float  lum_scaled   = original_lum * middlegray.y / middlegray.x;
           
    float  lum_filmic = max( lum_scaled - 0.004, 0.0); 
           lum_filmic = lum_filmic * (lum_filmic * 6.2 + 0.5)  / (lum_filmic * (lum_filmic * 6.2 + 1.7) + 0.06);
           lum_filmic = pow(lum_filmic, 2.2);          //de-gamma-correction for gamma-corrected tonemapper
           lum_filmic = lum_filmic * WhiteFactor;    //linear scale
    
    float lum_reinhard = lum_scaled * (lum_scaled * WhiteFactor + 1.0) / (lum_scaled + 1.0);
    
    float lum_mapped   = (UseFilmic)? lum_filmic : lum_reinhard; //if filmic
    
    color.rgb = color.rgb * lum_mapped / original_lum;
	
	return color;
}