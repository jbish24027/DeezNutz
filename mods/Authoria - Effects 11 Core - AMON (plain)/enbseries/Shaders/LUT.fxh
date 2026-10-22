//==========================//
// LUT code by kingeric1992 //
//==========================//

static const float2 Lut_Size256 = float2(256.0, 16.0);

float3 Lut256( float3 colorIN, Texture2D lutTexIn ) {
    float2 CLut_pSize = 1.0 / Lut_Size256;
    float4 CLut_UV;
    colorIN    = saturate(colorIN) * ( Lut_Size256.y - 1.0);
    CLut_UV.w  = floor(colorIN.b);
    CLut_UV.xy = (colorIN.rg + 0.5) * CLut_pSize;
    CLut_UV.x += CLut_UV.w * CLut_pSize.y;
    CLut_UV.z  = CLut_UV.x + CLut_pSize.y;
    return       lerp (lutTexIn.SampleLevel(Sampler1, CLut_UV.xy, 0).rgb, 
                       lutTexIn.SampleLevel(Sampler1, CLut_UV.zy, 0).rgb, colorIN.b - CLut_UV.w);
}


static const float2 Lut_Size1024 = float2(1024.0, 32.0);

float3 Lut1024( float3 colorIN, Texture2D lutTexIn ) {
    float2 CLut_pSize = 1.0 / Lut_Size1024;
    float4 CLut_UV;
    colorIN    = saturate(colorIN) * ( Lut_Size1024.y - 1.0);
    CLut_UV.w  = floor(colorIN.b);
    CLut_UV.xy = (colorIN.rg + 0.5) * CLut_pSize;
    CLut_UV.x += CLut_UV.w * CLut_pSize.y;
    CLut_UV.z  = CLut_UV.x + CLut_pSize.y;
    return       lerp (lutTexIn.SampleLevel(Sampler1, CLut_UV.xy, 0).rgb, 
                       lutTexIn.SampleLevel(Sampler1, CLut_UV.zy, 0).rgb, colorIN.b - CLut_UV.w);
}


static const float2 Lut_Size4096 = float2(4096.0, 64.0);

float3 Lut4096( float3 colorIN, Texture2D lutTexIn ) {
    float2 CLut_pSize = 1.0 / Lut_Size4096;
    float4 CLut_UV;
    colorIN    = saturate(colorIN) * ( Lut_Size4096.y - 1.0);
    CLut_UV.w  = floor(colorIN.b);
    CLut_UV.xy = (colorIN.rg + 0.5) * CLut_pSize;
    CLut_UV.x += CLut_UV.w * CLut_pSize.y;
    CLut_UV.z  = CLut_UV.x + CLut_pSize.y;
    return       lerp (lutTexIn.SampleLevel(Sampler1, CLut_UV.xy, 0).rgb, 
                       lutTexIn.SampleLevel(Sampler1, CLut_UV.zy, 0).rgb, colorIN.b - CLut_UV.w);
}