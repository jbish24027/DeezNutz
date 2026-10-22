//======================================//
// SweetFX Bloom by CeeJay.dk (I guess) //
//======================================//

float4 BloomPass(float4 color, float2 coord)
{
    if (USE_SBloom==true) {
	
	// DNI seperation
	float BloomThreshold   =lerp( lerp(BloomThreshold_Night,   BloomThreshold_Day,   ENightDayFactor), BloomThreshold_Interior,   EInteriorFactor );
	float BloomPower       =lerp( lerp(BloomPower_Night,       BloomPower_Day,       ENightDayFactor), BloomPower_Interior,       EInteriorFactor );
	float BloomWidth       =lerp( lerp(BloomWidth_Night,       BloomWidth_Day,       ENightDayFactor), BloomWidth_Interior,       EInteriorFactor );
	
	float3 BlurColor2 = 0;
	float3 Blurtemp = 0;
	float MaxDistance = 8*BloomWidth; //removed sqrt
	float CurDistance = 0;
	
	float Samplecount = 25.0;
	
	float2 pixelsize = ScreenSize.y;
	pixelsize.y *= ScreenSize.z;
	
	float2 blurtempvalue = coord * pixelsize * BloomWidth;
	
	
	float2 BloomSample = float2(2.5,-2.5);
	float2 BloomSampleValue; // = BloomSample;
	
	for(BloomSample.x = (2.5); BloomSample.x > -2.0; BloomSample.x = BloomSample.x - 1.0) // runs 5 times
	{
        BloomSampleValue.x = BloomSample.x * blurtempvalue.x;
        float2 distancetemp = BloomSample.x * BloomSample.x * BloomWidth;
        
		for(BloomSample.y = (- 2.5); BloomSample.y < 2.0; BloomSample.y = BloomSample.y + 1.0) // runs 5 ( * 5) times
		{
            distancetemp.y = BloomSample.y * BloomSample.y;
			CurDistance = (distancetemp.y * BloomWidth) + distancetemp.x; //removed sqrt
			
			BloomSampleValue.y = BloomSample.y * blurtempvalue.y;
			Blurtemp.rgb = TextureColor.Sample(Sampler0, float2(coord + BloomSampleValue)).rgb; //same result - same speed.
			
			BlurColor2.rgb += lerp(Blurtemp.rgb,color.rgb, sqrt(CurDistance / MaxDistance)); //reduced number of sqrts needed
		}
	}
	BlurColor2.rgb = (BlurColor2.rgb / (Samplecount - (BloomPower - BloomThreshold*5))); //check if using MAD
	float Bloomamount = (dot(color.rgb,float3(0.299f, 0.587f, 0.114f))) ; //try BT 709
	float3 BlurColor = BlurColor2.rgb * (BloomPower + 4.0); //check if calculated offline and combine with line 24 (the blurcolor2 calculation)

	color.rgb = lerp(color.rgb,BlurColor.rgb, Bloomamount);	

	return saturate(color);
	}
	else
	return color; //do i need an else here??
}
