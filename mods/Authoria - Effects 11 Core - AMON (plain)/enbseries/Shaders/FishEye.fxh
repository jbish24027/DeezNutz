//=============================================================//
// icelaglace, a.o => (ported from some blog, author unknown)  //
// mastereffect by Marty McFly                                 //
// ReShade 3 port by Insomnia                                  //
// Iddqd combined Horizontal and Vertical Fisheye (Switchable) //
// ENB port by Adyss                                           //
//=============================================================//

float3 FISHEYE(float3 color, float2 coord)
{
 
    if (USE_FISH==true)
	{
/*	
    float4 coord=0.0;
    coord.xy=IN.txcoord0.xy;
    coord.w=0.0;
*/
    color.rgb = 0.0;
     
    float3 eta = float3(1.0+fFisheyeColorshift*0.9,1.0+fFisheyeColorshift*0.6,1.0+fFisheyeColorshift*0.3);
    float2 center;
    center.x = coord.x-0.5;
    center.y = coord.y-0.5;
    float LensZoom = 1.0/fFisheyeZoom;
 
    float r2;// + (coord.y-0.5) * (coord.y-0.5);
 
    if(iFisheyeMod == 0)
    {
         r2 = (coord.y-0.5) * (coord.y-0.5);
    }
    else if (iFisheyeMod == 1)
    {
        r2 = (coord.x-0.5) * (coord.x-0.5);
    }
    else
    {
        r2 = (coord.y-0.5) * (coord.y-0.5) + (coord.y-0.5) * (coord.y-0.5);
    }
 
 
    float f = 0;
 
    if( fFisheyeDistortionCubic == 0.0){
        f = 1 + r2 * fFisheyeDistortion;
    }else{
                f = 1 + r2 * (fFisheyeDistortion + fFisheyeDistortionCubic * sqrt(r2));
    };
 
    float x = f*LensZoom*(coord.x-0.5)+0.5;
    float y = f*LensZoom*(coord.y-0.5)+0.5;
    float2 rCoords = (f*eta.r)*LensZoom*(center.xy*0.5)+0.5;
    float2 gCoords = (f*eta.g)*LensZoom*(center.xy*0.5)+0.5;
    float2 bCoords = (f*eta.b)*LensZoom*(center.xy*0.5)+0.5;
   
    color.x = TextureColor.Sample(Sampler0,rCoords).r;
    color.y = TextureColor.Sample(Sampler0,gCoords).g;
    color.z = TextureColor.Sample(Sampler0,bCoords).b;
   
    }   
    return color.rgb;
 
}