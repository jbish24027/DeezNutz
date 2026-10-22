//===================================//
// Gaussian Postpass Bloom by Prod80 //
//===================================//

float4 PS_ProcessGaussianH(VS_OUTPUT_POST IN) : SV_Target
{

   float4 dis_out = TextureColor.Sample(Sampler0, IN.txcoord0.xy);
   if (USE_GaussBloom==true) {
   float4 color      =   0.0;
   float sHeight      =   ScreenSize.x * ScreenSize.w;
   float2 fvTexelSize    =    float2(ScreenSize.y, 1.0 / sHeight);
   float px          =    fvTexelSize.x; 
   float py          =    fvTexelSize.y; 
   
   if ( gauss_blur==1 )
   {
   color       = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_1[0];
   for(int i = 1; i < 3; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(sampleOffsets_1[i]*px, 0.0)) * sampleWeights_1[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(sampleOffsets_1[i]*px, 0.0)) * sampleWeights_1[i];
      }
   }
   if ( gauss_blur==2 )
   {
   color       = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_2[0];
   for(int i = 1; i < 5; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(sampleOffsets_2[i]*px, 0.0)) * sampleWeights_2[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(sampleOffsets_2[i]*px, 0.0)) * sampleWeights_2[i];
      }
   }
   if ( gauss_blur==3 )
   {
   color       = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_3[0];
   for(int i = 1; i < 6; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(sampleOffsets_3[i]*px, 0.0)) * sampleWeights_3[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(sampleOffsets_3[i]*px, 0.0)) * sampleWeights_3[i];
      }
   }
   color.w            = 1.0f;
   return color;
   }
   else
   return dis_out;
}

float4 PS_ProcessGaussianV(VS_OUTPUT_POST IN) : SV_Target
{
   float4 dis_out = TextureColor.Sample(Sampler0, IN.txcoord0.xy);
   if (USE_GaussBloom==true) {
   float4 color      =   0.0;
   float sHeight      =   ScreenSize.x * ScreenSize.w;
   float2 fvTexelSize    =    float2(ScreenSize.y, 1.0 / sHeight);
   float px          =    fvTexelSize.x; 
   float py          =    fvTexelSize.y; 
   
   if ( gauss_blur==1 )
   {
   color = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_1[0];
   for(int i = 1; i < 3; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(0.0, sampleOffsets_1[i]*py)) * sampleWeights_1[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(0.0, sampleOffsets_1[i]*py)) * sampleWeights_1[i];
      }
   }
   if ( gauss_blur==2 )
   {
   color = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_2[0];
   for(int i = 1; i < 5; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(0.0, sampleOffsets_2[i]*py)) * sampleWeights_2[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(0.0, sampleOffsets_2[i]*py)) * sampleWeights_2[i];
      }
   }
   if ( gauss_blur==3 )
   {
   color = TextureColor.Sample(Sampler0, IN.txcoord0.xy) * sampleWeights_3[0];
   for(int i = 1; i < 6; ++i) {
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(0.0, sampleOffsets_3[i]*py)) * sampleWeights_3[i];
      color += TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(0.0, sampleOffsets_3[i]*py)) * sampleWeights_3[i];
      }
   }
   color.w            = 1.0f;
   return color;
   }
   else
   return dis_out;
   
}

float4 PS_ProcessSoftLight(VS_OUTPUT_POST IN) : SV_Target
{
   float4 blendC   = TextureColor.Sample(Sampler0, IN.txcoord0.xy);
   if (USE_GaussBloom==true) {
   float4 color      =   0.0;
   float4 baseC   = TextureOriginal.Sample(Sampler0, IN.txcoord0.xy);
   
   float3 base      = baseC.xyz;
   float3 blend   = blendC.xyz;
   
   float sl_mix_set   =lerp( lerp(sl_mix_set_Night,   sl_mix_set_Day,   ENightDayFactor), sl_mix_set_Interior,   EInteriorFactor );
   
   color.xyz      = softlight( base, blend, sl_mix_set );
   color.w         = 1.0f;

   return color;
   }
   else
   return blendC;
}

float4 PS_ProcessGaussBloom(VS_OUTPUT_POST IN) : SV_Target
{
   float4 blendC   = TextureColor.Sample(Sampler0, IN.txcoord0.xy);
   if (USE_GaussBloom==true) {
   float4 scrcolor   = 0.0;
   float3 luma    = float3(0.2125, 0.7154, 0.0721);
   float pixluma   = 0.0;
   float4 baseC   = TextureOriginal.Sample(Sampler0, IN.txcoord0.xy);
   float4 color   = 0.0;
   
   float3 base      = baseC.xyz;
   float3 blend   = blendC.xyz;
   
   scrcolor.xyz   = screen( base, blend );
   
   float gauss_bloom   =lerp( lerp(gauss_bloom_Night,   gauss_bloom_Day,   ENightDayFactor), gauss_bloom_Interior,   EInteriorFactor );
   
   //Bloom on luma
   if (lumabloom==true)
   {
      if (lumasource==1) pixluma = dot( base, luma );
      if (lumasource==2) pixluma = dot( blend, luma );
      if (lumasource==3) pixluma = dot( scrcolor, luma );
   color.xyz      = lerp( base.xyz, scrcolor.xyz, gauss_bloom * pixluma );
   };
   if (lumabloom==false)
   {
   color.xyz      = lerp( base.xyz, scrcolor.xyz, gauss_bloom );
   };
   
   float3   lumCoeff = float3(0.212656, 0.715158, 0.072186);     
   color.a = dot(lumCoeff, color.rgb);
   
   color.w         = 1.0f;
   return color;
   }
   else
   return blendC;
}