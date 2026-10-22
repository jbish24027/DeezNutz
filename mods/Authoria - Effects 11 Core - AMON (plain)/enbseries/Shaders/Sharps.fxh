//========================//
// LumaSharp by Ceejay.dk //
// ENB port by Sonnhy     //
//========================//

#if (INC_LumaSHARP==1)
float4	PS_LumaSharp(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	// float4 TextureOriginal.Sample(Sampler0, IN.txcoord0.xy) = float3 tex2D(ReShade::BackBuffer, tex).rgb
	float4 ori = TextureOriginal.Sample(Sampler0, IN.txcoord0.xy); // ori = original pixel
	float2 coord = IN.txcoord0;
	if (USE_LumaSharp==true)
	{

	float2 pixelsize = ScreenSize.y;
	pixelsize.y *= ScreenSize.z;

	float3 sharp_strength_luma = (CoefLuma * LSharpStrength);

	float4 blur_ori;
	
	// Pattern 1 -- A (fast) 7 tap gaussian using only 2+1 texture fetches.
	if (LSharpPattern == 0) {

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + (pixelsize / 3.0) * LSharpOffsetBias);  // North West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + (-pixelsize / 3.0) * LSharpOffsetBias); // South East

		blur_ori /= 2;  //Divide by the number of texture fetches

		sharp_strength_luma *= 1.5; // Adjust strength to aproximate the strength of pattern 2
	}

	// Pattern 2 -- A 9 tap gaussian using 4+1 texture fetches.
	if (LSharpPattern == 1)
	{

		blur_ori  = TextureOriginal.Sample(Sampler0, coord.xy + float2(pixelsize.x, -pixelsize.y) * 0.5 * LSharpOffsetBias); // South East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy - pixelsize * 0.5 * LSharpOffsetBias);  // South West
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy + pixelsize * 0.5 * LSharpOffsetBias); // North East
		blur_ori += TextureOriginal.Sample(Sampler0, coord.xy - float2(pixelsize.x, -pixelsize.y) * 0.5 * LSharpOffsetBias); // North West

		blur_ori *= 0.25;  // ( /= 4) Divide by the number of texture fetches
	}

	// Pattern 3 -- An experimental 17 tap gaussian using 4+1 texture fetches.
	if (LSharpPattern == 2)
	{

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

	float4 sharp_strength_luma_clamp = float4(sharp_strength_luma * (0.5 / LSharpClamp), 0.5);
	sharp.w = 1.0;
	float sharp_luma = saturate( dot(sharp, sharp_strength_luma_clamp) );
	sharp_luma = (LSharpClamp * 2.0) * sharp_luma - LSharpClamp;


	float4 outputcolor = ori + sharp_luma;

	return saturate(outputcolor);
	}
	else
	return ori;
}
#endif

//===================================================================//
// Filmic Anamorph Sharpen PS v1.1.5 (c) 2018 Jacob Maximilian Fober //
// This work is licensed under the Creative Commons                  //
// Attribution-ShareAlike 4.0 International License.                 //
// To view a copy of this license, visit                             //
// http://creativecommons.org/licenses/by-sa/4.0/.                   //
//===================================================================//
// Not sure about the Depth part :/ halp plis
#if (INC_FilmicAnamorphSharp==1)
float3	PS_FilmicAnamorphSharp(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	float2 Pixel = PixelSize;
	float2 UvCoord = IN.txcoord0;

	float2 DepthPixel = Pixel * float(FASOffset + 1);
	Pixel *= float(FASOffset);
	// Sample display image
	float3 Source = TextureColor.Sample(Sampler0, UvCoord).rgb;
	// Sample display depth image
	float SourceDepth = TextureDepth.Sample(Sampler1, UvCoord);

	float2 NorSouWesEst[4] = {
		float2(UvCoord.x, UvCoord.y + Pixel.y),
		float2(UvCoord.x, UvCoord.y - Pixel.y),
		float2(UvCoord.x + Pixel.x, UvCoord.y),
		float2(UvCoord.x - Pixel.x, UvCoord.y)
	};

	float2 DepthNorSouWesEst[4] = {
		float2(UvCoord.x, UvCoord.y + DepthPixel.y),
		float2(UvCoord.x, UvCoord.y - DepthPixel.y),
		float2(UvCoord.x + DepthPixel.x, UvCoord.y),
		float2(UvCoord.x - DepthPixel.x, UvCoord.y)
	};

	// Choose luma coefficient, if True BT.709 Luma, else BT.601 Luma
	float3 LumaCoefficient = float3( 0.2126,  0.7152,  0.0722);

	// Luma high-pass color
	float HighPassColor =
	   dot(TextureColor.Sample(Sampler0, NorSouWesEst[0]).rgb, LumaCoefficient)
	 + dot(TextureColor.Sample(Sampler0, NorSouWesEst[1]).rgb, LumaCoefficient)
	 + dot(TextureColor.Sample(Sampler0, NorSouWesEst[2]).rgb, LumaCoefficient)
	 + dot(TextureColor.Sample(Sampler0, NorSouWesEst[3]).rgb, LumaCoefficient);
	HighPassColor = 0.5 - 0.5 * (HighPassColor * 0.25 - dot(Source, LumaCoefficient));
	
	// Luma high-pass depth
	float DepthMask =
	   TextureDepth.Sample(Sampler1, DepthNorSouWesEst[0])
	 + TextureDepth.Sample(Sampler1, DepthNorSouWesEst[1])
	 + TextureDepth.Sample(Sampler1, DepthNorSouWesEst[2])
	 + TextureDepth.Sample(Sampler1, DepthNorSouWesEst[3])
	 + TextureDepth.Sample(Sampler1, NorSouWesEst[0])
	 + TextureDepth.Sample(Sampler1, NorSouWesEst[1])
	 + TextureDepth.Sample(Sampler1, NorSouWesEst[2])
	 + TextureDepth.Sample(Sampler1, NorSouWesEst[3]);
	DepthMask = 1.0 - DepthMask * 0.125 + SourceDepth;
	DepthMask = min(1.0, DepthMask) + 1.0 - max(1.0, DepthMask);
	DepthMask = saturate(FASContrast * DepthMask + 1.0 - FASContrast);

	// Sharpen strength
	HighPassColor = lerp(0.5, HighPassColor, FASStrength * DepthMask);

	// Clamping sharpen
	HighPassColor = max(min(HighPassColor, FASClamp), 1 - FASClamp);

	float3 Sharpen = float3(
		Overlay(Source.r, HighPassColor),
		Overlay(Source.g, HighPassColor),
		Overlay(Source.b, HighPassColor)
	);

	return Sharpen;
}
#endif

//======================//
// Basic Sharp by Boris //
//======================//
#if (INC_BasicSharp==1)
float4	PS_BSharp(VS_OUTPUT_POST IN, float4 v0 : SV_Position0) : SV_Target
{
	float4	res;
	float4	color;
	float4	centercolor;
	float2	pixeloffset=ScreenSize.y;
	pixeloffset.y*=ScreenSize.z;

	centercolor=TextureColor.Sample(Sampler0, IN.txcoord0.xy);
	color=0.0;
	float2	offsets[4]=
	{
		float2(-1.0,-1.0),
		float2(-1.0, 1.0),
		float2( 1.0,-1.0),
		float2( 1.0, 1.0),
	};
	for (int i=0; i<4; i++)
	{
		float2	coord=offsets[i].xy * pixeloffset.xy * ESharpRange + IN.txcoord0.xy;
		color.xyz+=TextureColor.Sample(Sampler1, coord.xy);
	}
	color.xyz *= 0.25;

	float	diffgray=dot((centercolor.xyz-color.xyz), 0.3333);
	res.xyz=ESharpAmount * centercolor.xyz*diffgray + centercolor.xyz;

	res.w=1.0;
	return res;
}
#endif
/*
//=============================//
// UnSharp Mask by Marty McFly //
//=============================//
// Dosnt compile (i suck lol)
float4	UNSharp(float4 color, float2 coord)
{
	float4 blurred = 0.0;

	int iStepcount = iSharpStepCount;
	float deviation = (float)iStepcount * 0.4;
	float norm = -rcp(2.0*deviation*deviation);

	float2 offset;
	float3 sample;

	float2 stepsize = PixelSize.xy * fSharpStepSize;

	[loop]
	for(int iStepsX=-iStepcount; iStepsX<=iStepcount; iStepsX++)
	{
		[loop]
		for(int iStepsY=-iStepcount; iStepsY<=iStepcount; iStepsY++)
		{
			float2 cOffset = float2(iStepsX,iStepsY);
			sample = (color, coord.xy + cOffset * stepsize,0);
			float weight = exp(dot(cOffset,cOffset)*norm);
			blurred.xyz += sample * weight;
			blurred.w += weight;
		}
	}

	blurred.xyz /= blurred.w;

	float4 res =  (color, coord.xy);
	float3 sharp = res.xyz - blurred.xyz;
	float sharp_luma = dot(sharp,fSharpAmount);

	sharp_luma = clamp(sharp_luma, -fSharpClamp, fSharpClamp);

	res.xyz = bSharpVisualize ? saturate(0.5 + 4*sharp_luma) : saturate(res.xyz + sharp_luma);

	return res;
}
*/