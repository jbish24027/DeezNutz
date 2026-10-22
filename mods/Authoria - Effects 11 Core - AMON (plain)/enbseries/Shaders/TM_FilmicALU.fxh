/**********************************************************************
 * 
 * Flimic ALU [HEJL] @https://twitter.com/jimhejl
 * 
 * http://filmicworlds.com/blog/filmic-tonemapping-operators/
 *
 *  input struct:
 *      TM_FilmicALU_struct {
 *          float a;
 *          float b;
 *          float c;
 *          float d;
 *          float e;
 *          float f; //gamma decoder
 *          float g; //input offset
 *          float w; //white
 *      };
 *  
 *  Preset:
 *      TM_FilmicALU_struct TM_FilmicALU_ACES;
 *          ACES curve fitted by Krzysztof Narkowicz, color * 0.6 for original ACES curve
 *          https://knarkowicz.wordpress.com/2016/01/06/aces-filmic-tone-mapping-curve/
 *      
 *      TM_FilmicALU_struct TM_FilmicALU_Default;
 *          http://filmicworlds.com/blog/filmic-tonemapping-operators/
 *              Skyrim SSE with slightly modified version
 *          http://enbseries.enbdev.com/forum/viewtopic.php?f=7&t=5278&p=73675
 *
 *  Function prototype:
 *      float3 res = TM_FilmicALU( float3 linearColor, 
 *                                 TM_FilmicALU_struct params = TM_FilmicALU_Default );
 *
 *  Ported to HLSL by kingeric1992 for ENBseries
 *      forum:
 *                                                  update: July.4.2017
 *
 **********************************************************************/

#ifndef _TM_FILMICALU_FXH_
#define _TM_FILMICALU_FXH_
 
struct TM_FilmicALU_struct { 
    float a, b, c, d, e, f, g, w; 
};

static const TM_FilmicALU_struct TM_FilmicALU_ACES = {
    0.9, 0.018, 0.875, 0.354, 0.14, 1.0, 0.0, 4.0
};

static const TM_FilmicALU_struct TM_FilmicALU_Default  = {
    6.2, 0.5, 6.2, 1.7, 0.06, 2.2, 0.004, 4.0
};

float4 TM_FlimicALU_func(float4 color, const TM_FilmicALU_struct i) {
    float4 l = max(color - i.g, 0.0);
    return pow(saturate( l*(i.a*l+i.b) / 
                       ( l*(i.c*l+i.d) + i.e)), i.f);
}

float3 TM_FilmicALU( float3 color, const TM_FilmicALU_struct i = TM_FilmicALU_Default ) { 
     float4 res = TM_FlimicALU_func(float4(color, i.w), i);
     return res.rgb/res.a;
}

#endif //_TM_FILMICALU_FXH_