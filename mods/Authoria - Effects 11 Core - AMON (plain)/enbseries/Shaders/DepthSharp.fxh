//=======================//
// Depth Sharp by Prod80 //
//=======================//

float4 PS_ProcessGaussianH(VS_OUTPUT_POST IN)  : SV_Target
{
	float4 color		= TextureColor.Sample(Sampler0, IN.txcoord0.xy);
	float Depth			= TextureDepth.Sample(Sampler0, IN.txcoord0.xy ).x;
	
	if ( shader_off==true ) return color;
	float px 			= ScreenSize.y; 
	float linDepth		= linearDepth( Depth, 0.5f, farDepth );
	
	float SigmaSum		= 0.0f;
	float sampleOffset	= 1.0f;
	
	//Gaussian
	float BlurSigma		= lerp( BlurSigmaE, BlurSigmaI, EInteriorFactor );
	BlurSigma			= max( BlurSigma * ( 1.0f - linDepth ), 0.3f );
	float3 Sigma;
	Sigma.x				= 1.0f / ( sqrt( 2.0f * PI ) * BlurSigma );
	Sigma.y				= exp( -0.5f / ( BlurSigma * BlurSigma ));
	Sigma.z				= Sigma.y * Sigma.y;
	
	//Center weight
	color				*= Sigma.x;
	SigmaSum			+= Sigma.x;
	Sigma.xy			*= Sigma.yz;

	for(int i = 0; i < 7; ++i) {
		color 			+= TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(sampleOffset*px, 0.0)) * Sigma.x;
		color 			+= TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(sampleOffset*px, 0.0)) * Sigma.x;
		SigmaSum		+= ( 2.0f * Sigma.x );
		sampleOffset	= sampleOffset + 1.0f;
		Sigma.xy		*= Sigma.yz;
		}
		
	color.xyz			/= SigmaSum;
	color.w				= 1.0f;
	return color;
}

float4 PS_ProcessGaussianV(VS_OUTPUT_POST IN) : SV_Target
{
	if ( shader_off==true ) return float4( TextureOriginal.Sample(Sampler0, IN.txcoord0.xy ));
	
	float sHeight		= ScreenSize.x * ScreenSize.w;
	float py 			= 1.0 / sHeight;
	float4 color		= 0.0;
	float Depth			= TextureDepth.Sample(Sampler0, IN.txcoord0.xy ).x;
	float linDepth		= linearDepth( Depth, 0.5f, farDepth );
	
	float SigmaSum		= 0.0f;
	float sampleOffset	= 1.0f;
	
	//Gaussian
	float BlurSigma		= lerp( BlurSigmaE, BlurSigmaI, EInteriorFactor );
	BlurSigma			= max( BlurSigma * ( 1.0f - linDepth ), 0.3f );
	float3 Sigma;
	Sigma.x				= 1.0f / ( sqrt( 2.0f * PI ) * BlurSigma );
	Sigma.y				= exp( -0.5f / ( BlurSigma * BlurSigma ));
	Sigma.z				= Sigma.y * Sigma.y;
	
	//Center weight
	color				= TextureColor.Sample(Sampler0, IN.txcoord0.xy);
	color				*= Sigma.x;
	SigmaSum			+= Sigma.x;
	Sigma.xy			*= Sigma.yz;

	for(int i = 0; i < 7; ++i) {
		color 			+= TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(0.0, sampleOffset*py)) * Sigma.x;
		color 			+= TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(0.0, sampleOffset*py)) * Sigma.x;
		SigmaSum		+= ( 2.0f * Sigma.x );
		sampleOffset	= sampleOffset + 1.0f;
		Sigma.xy		*= Sigma.yz;
		}
	
	color.xyz			/= SigmaSum;
	color.w				= 1.0f;
	return color;
}

float4 PS_ProcessEdges(VS_OUTPUT_POST IN) : SV_Target
{
	if ( shader_off==true ) return float4( TextureOriginal.Sample(Sampler0, IN.txcoord0.xy ));
	
	float Sharpening	= lerp( SharpeningE, SharpeningI, EInteriorFactor );
	float Threshold		= lerp( ThresholdE, ThresholdI, EInteriorFactor ) / 255;
	
	float4 color;
	float4 orig			= TextureOriginal.Sample(Sampler0, IN.txcoord0.xy);
	float4 blurred		= TextureColor.Sample(Sampler0, IN.txcoord0.xy);
	
	//Find edges
	orig.xyz			= saturate( orig.xyz );
	blurred.xyz			= saturate( blurred.xyz );
	float3 Edges		= max( saturate( orig.xyz - blurred.xyz ) - Threshold, 0.0f );
	float3 invBlur		= saturate( 1.0f - blurred.xyz );
	float3 originvBlur	= saturate( orig.xyz + invBlur.xyz );
	float3 invOrigBlur	= max( saturate( 1.0f - originvBlur.xyz ) - Threshold, 0.0f );
	
	float3 edges		= max(( saturate( Sharpening * Edges.xyz )) - ( saturate( Sharpening * invOrigBlur.xyz )), 0.0f );
	
	color.xyz			= edges.xyz;
	color.w				= 1.0f;
	return color;
}

float4 PS_ProcessSharpen1(VS_OUTPUT_POST IN) : SV_Target
{
	if ( shader_off==true ) return float4( TextureOriginal.Sample(Sampler0, IN.txcoord0.xy ));
	
	//Smooth out edges with extremely light gaussian
	float4 edges		= TextureColor.Sample(Sampler0, IN.txcoord0.xy);
	
	if (smooth_edges==false) return edges;
	
	float px 			= ScreenSize.y; 
	float4 color		= 0.0;
	
	float SigmaSum		= 0.0f;
	float sampleOffset	= 1.0f;
	
	//Gaussian
	float BlurSigma		= smooth;
	float3 Sigma;
	Sigma.x				= 1.0f / ( sqrt( 2.0f * PI ) * BlurSigma );
	Sigma.y				= exp( -0.5f / ( BlurSigma * BlurSigma ));
	Sigma.z				= Sigma.y * Sigma.y;
	
	//Center weight
	edges				*= Sigma.x;
	SigmaSum			+= Sigma.x;
	Sigma.xy			*= Sigma.yz;

	for(int i = 0; i < 5; ++i) {
		edges 			+= TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(sampleOffset*px, 0.0)) * Sigma.x;
		edges 			+= TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(sampleOffset*px, 0.0)) * Sigma.x;
		SigmaSum		+= ( 2.0f * Sigma.x );
		sampleOffset	= sampleOffset + 1.0f;
		Sigma.xy		*= Sigma.yz;
		}
		
	color.xyz			= edges.xyz / SigmaSum;
	color.w				= 1.0f;
	return color;

}

float4 PS_ProcessSharpen2(VS_OUTPUT_POST IN) : SV_Target
{
	if ( shader_off==true ) return float4( TextureOriginal.Sample(Sampler0, IN.txcoord0.xy ));
	
	float4 orig			= TextureOriginal.Sample(Sampler0, IN.txcoord0.xy);
	float4 edges		= TextureColor.Sample(Sampler0, IN.txcoord0.xy);
	float limiter		= lerp( limiterE, limiterI, EInteriorFactor );
	
	//Smooth out edges (reduce aliasing) - expensive, likely
	float sHeight		= ScreenSize.x * ScreenSize.w;
	float py 			= 1.0 / sHeight;
	float4 color		= 0.0;
	
	if (smooth_edges==true) {
	
		float SigmaSum		= 0.0f;
		float sampleOffset	= 1.0f;
		
		//Gaussian
		float BlurSigma		= smooth;
		float3 Sigma;
		Sigma.x				= 1.0f / ( sqrt( 2.0f * PI ) * BlurSigma );
		Sigma.y				= exp( -0.5f / ( BlurSigma * BlurSigma ));
		Sigma.z				= Sigma.y * Sigma.y;
		
		//Center weight
		edges				*= Sigma.x;
		SigmaSum			+= Sigma.x;
		Sigma.xy			*= Sigma.yz;

		for(int i = 0; i < 5; ++i) {
			edges 			+= TextureColor.Sample(Sampler0, IN.txcoord0.xy + float2(0.0, sampleOffset*py)) * Sigma.x;
			edges 			+= TextureColor.Sample(Sampler0, IN.txcoord0.xy - float2(0.0, sampleOffset*py)) * Sigma.x;
			SigmaSum		+= ( 2.0f * Sigma.x );
			sampleOffset	= sampleOffset + 1.0f;
			Sigma.xy		*= Sigma.yz;
			}
		
		edges.xyz			/= SigmaSum;
	}
	
	if (show_edges==true) {
		color.w 		= 1.0f;
		if(luma_sharpen==true) {
			color.xyz 	= min( dot( edges.xyz, float3( 0.2126, 0.7152, 0.0722 )), limiter );
			} else {
			color.xyz 	= edges.xyz * limiter;
			}
		return color;
	}
	
	if (luma_sharpen==true) {
		float3 blend	= saturate( orig.xyz + min( dot( edges.xyz, float3( 0.2126, 0.7152, 0.0722 )), limiter ));
		color.xyz		= BlendLuma( orig.xyz, blend.xyz );
		} else {
		color.xyz		= saturate( orig.xyz + ( edges.xyz * limiter ));
	}

	color.w				= 1.0f;
	return color;

}