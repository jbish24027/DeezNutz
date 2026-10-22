/**********************************************************************
 *
 *  Uncharted 2 Filmic tonemapper[Hable10]
 *
 *  http://filmicworlds.com/blog/filmic-tonemapping-operators/
 *
 *  input struct:
 *      TM_Uncharted2_struct {
 *          float a; //Shoulder Strength 
 *          float b; //Linear Strength
 *          float c; //Linear Angle
 *          float d; //Toe Strength
 *          float e; //Toe Numerator
 *          float f; //Toe Denominator, E/F = Toe Angle
 *          float w; //White point 
 *      };
 *
 *  Preset:
 *      TM_Uncharted2_struct Uncharted2_Fallout4;
 *           http://enbseries.enbdev.com/forum/viewtopic.php?f=7&t=4695
 *      TM_Uncharted2_struct Uncharted2_Hejl2015;
 *           https://twitter.com/jimhejl/status/633777619998130176
 *      TM_Uncharted2_struct Uncharted2_Default;
 *           http://filmicworlds.com/blog/filmic-tonemapping-operators/
 * 
 *  Function prototype:
 *      float3 res = TM_Uncharted2( float3 linearColor, 
 *                                  TM_Uncharted2_struct params = Uncharted2_Default);
 *
 *  Ported to HLSL by kingeric1992 for ENBseries
 *      forum:
 *                                                  update: July.4.2017
 *
 **********************************************************************/

#ifndef _TM_UNCHARTED2_FXH_
#define _TM_UNCHARTED2_FXH_
 
struct TM_Uncharted2_struct {
    float a; //Shoulder Strength 
    float b; //Linear Strength
    float c; //Linear Angle
    float d; //Toe Strength
    float e; //Toe Numerator
    float f; //Toe Denominator, E/F = Toe Angle
    float w; //White point
};

static const TM_Uncharted2_struct Uncharted2_Fallout4 = { 
    0.15, 0.50, 0.10, 0.20, 0.02, 0.30, 4.0
};

static const TM_Uncharted2_struct Uncharted2_Default  = { 
    0.22, 0.3,  0.10, 0.20, 0.01, 0.30, 4.0
};

static const TM_Uncharted2_struct Uncharted2_Hejl2015 = {
    1.425, 0.6, 0.08333, 0.20, 0.02, 0.2455, 4.0
};

float3 TM_Uncharted2(float3 color, const TM_Uncharted2_struct i = Uncharted2_Default) {
    float4 l = float4(color, i.w);
           l = ( l * ( i.a * l + i.b * i.c) + i.d * i.e ) / 
               ( l * ( i.a * l + i.b) + i.d * i.f ) - i.e / i.f;
    return l.rgb / l.a; 
}

#endif //_TM_UNCHARTED2_FXH_