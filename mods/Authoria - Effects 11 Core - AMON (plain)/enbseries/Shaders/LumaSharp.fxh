//========================//
// LumaSharp by Ceejay.dk //
// ENB port by Sonnhy     //
//========================//
float4	LumaSharp(float4 ori, float2 coord)
{
	// float4 TextureOriginal.Sample(Sampler0, IN.txcoord0.xy) = float3 tex2D(ReShade::BackBuffer, tex).rgb
	//float4 ori = TextureOriginal.Sample(Sampler0, IN.txcoord0.xy); // ori = original pixel
	if (USE_LumaSharp==true)
	{

	// pixelsize = ReShade::PixelSize
	float2 pixelsize = ScreenSize.y;
	pixelsize.y *= ScreenSize.z;

	// Combining the strength and luma multipliers
	float3 sharp_strength_luma = (CoefLuma * LSharpStrength);

	// Sampling patterns
	float4 blur_ori;
	
	// Pattern 1 -- A (fast) 7 tap gaussian using only 2+1 texture fetches.
	if (LSharpPattern == 0) {
		// -- Gaussian filter --
		//   [ 1/9, 2/9,    ]     [ 1 , 2 ,   ]
		//   [ 2/9, 8/9, 2/9]  =  [ 2 , 8 , 2 ]
		//   [    , 2/9, 1/9]     [   , 2 , 1 ]

		// tex = IN.txcoord0.xy
		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + (pixelsize / 3.0) * LSharpOffsetBias);  // North West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + (-pixelsize / 3.0) * LSharpOffsetBias); // South East

		blur_ori /= 2;  //Divide by the number of texture fetches

		sharp_strength_luma *= 1.5; // Adjust strength to aproximate the strength of pattern 2
	}

	// Pattern 2 -- A 9 tap gaussian using 4+1 texture fetches.
	if (LSharpPattern == 1)
	{
		// -- Gaussian filter --
		//   [ .25, .50, .25]     [ 1 , 2 , 1 ]
		//   [ .50,   1, .50]  =  [ 2 , 4 , 2 ]
		//   [ .25, .50, .25]     [ 1 , 2 , 1 ]

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + float2(pixelsize.x, -pixelsize.y) * 0.5 * LSharpOffsetBias); // South East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy - pixelsize * 0.5 * LSharpOffsetBias);  // South West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * 0.5 * LSharpOffsetBias); // North East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy - float2(pixelsize.x, -pixelsize.y) * 0.5 * LSharpOffsetBias); // North West

		blur_ori *= 0.25;  // ( /= 4) Divide by the number of texture fetches
	}

	// Pattern 3 -- An experimental 17 tap gaussian using 4+1 texture fetches.
	if (LSharpPattern == 2)
	{
		// -- Gaussian filter --
		//   [   , 4 , 6 ,   ,   ]
		//   [   ,16 ,24 ,16 , 4 ]
		//   [ 6 ,24 ,   ,24 , 6 ]
		//   [ 4 ,16 ,24 ,16 ,   ]
		//   [   ,   , 6 , 4 ,   ]

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * float2(0.4, -1.2) * LSharpOffsetBias);  // South South East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * float2(1.2, 0.4) * LSharpOffsetBias); // West South West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * float2(1.2, 0.4) * LSharpOffsetBias); // East North East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * float2(0.4, -1.2) * LSharpOffsetBias); // North North West

		blur_ori *= 0.25;  // ( /= 4) Divide by the number of texture fetches

		sharp_strength_luma *= 0.51;
	}

	// Pattern 4 -- A 9 tap high pass (pyramid filter) using 4+1 texture fetches.
	if (LSharpPattern == 3)
	{
		// -- Gaussian filter --
		//   [ .50, .50, .50]     [ 1 , 1 , 1 ]
		//   [ .50,    , .50]  =  [ 1 ,   , 1 ]
		//   [ .50, .50, .50]     [ 1 , 1 , 1 ]

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + float2(0.5 * pixelsize.x, -pixelsize.y * LSharpOffsetBias));  // South South East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + float2(LSharpOffsetBias * -pixelsize.x, 0.5 * -pixelsize.y)); // West South West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + float2(LSharpOffsetBias * pixelsize.x, 0.5 * pixelsize.y)); // East North East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + float2(0.5 * -pixelsize.x, pixelsize.y * LSharpOffsetBias)); // North North West

		//blur_ori += (2 * ori); // Probably not needed. Only serves to lessen the effect.

		blur_ori /= 4.0;  //Divide by the number of texture fetches

		sharp_strength_luma *= 0.666; // Adjust strength to aproximate the strength of pattern 2
	}

	// Calculate the sharpening
	float4 sharp = ori - blur_ori;  //Subtracting the blurred image from the original image

	// OLD CODE (working too)
	// float sharp_luma = dot(sharp, sharp_strength_luma); //Calculate the luma and adjust the strength
	// sharp_luma = clamp(sharp_luma, -LSharpClamp, LSharpClamp);

	// NEW CODE
	// Adjust strength of the sharpening and clamp it
	float4 sharp_strength_luma_clamp = float4(sharp_strength_luma * (0.5 / LSharpClamp), 0.5);
	// Calculate the luma, adjust the strength, scale up and clamp
	sharp.w = 1.0; // HACK: because orginal LumaSharpen.fx uses float3 for color and something may change
	float sharp_luma = saturate( dot(sharp, sharp_strength_luma_clamp) );
	// Scale down
	sharp_luma = (LSharpClamp * 2.0) * sharp_luma - LSharpClamp;

	// Combining the values to get the final sharpened pixel
	// Add the sharpening to the the original.
	float4 outputcolor = ori + sharp_luma;

	return saturate(outputcolor);
	}
	else
	return ori;
}