//==================================//
// Full credits to the ReShade team //
// ReShade 3 port by Insomnia       //
//==================================//

float3 Emboss(float3 color, float2 coord)
{
    if (USE_Emboss==true)
	{
    float2 offset;
	sincos(radians( iEmbossAngle), offset.y, offset.x);
	float3 col1 = TextureColor.Sample(Sampler0, coord - PixelSize*fEmbossOffset*offset).rgb;
	float3 col2 = color.rgb;
	float3 col3 = TextureColor.Sample(Sampler0, coord + PixelSize*fEmbossOffset*offset).rgb;
	
	float3 colEmboss = col1 * 2.0 - col2 - col3;

	float colDot = max(0,dot(colEmboss, 0.333))*fEmbossPower;

	float3 colFinal = col2 - colDot;

	float luminance = dot( col2, float3( 0.6, 0.2, 0.2 ) );

	color.xyz = lerp( colFinal, col2, luminance * luminance ).xyz;
	
	}
	return color;
}

