//===============================================================================//
// Reinhard Shader form Mastereffect by Marty McFly. Reshade 3 port by Insomnia  //
//===============================================================================//
float3 Reinhard(float3 color)
{
	if (USE_Reinhard==true)
	{
  float ReinhardLinearSlope        =lerp( lerp(ReinhardLinearSlope_Night,   ReinhardLinearSlope_Day,   ENightDayFactor), ReinhardLinearSlope_Interior,   EInteriorFactor );
  float ReinhardLinearWhitepoint   =lerp( lerp(ReinhardLinearWhitepoint_Night,   ReinhardLinearWhitepoint_Day,   ENightDayFactor), ReinhardLinearWhitepoint_Interior,   EInteriorFactor );
  float ReinhardLinearPoint        =lerp( lerp(ReinhardLinearPoint_Night,   ReinhardLinearPoint_Day,   ENightDayFactor), ReinhardLinearPoint_Interior,   EInteriorFactor );
	
	float3 x = color.rgb;

    	const float W = ReinhardLinearWhitepoint;	   // Linear White Point Value
    	const float L = ReinhardLinearPoint;           // Linear point
    	const float C = ReinhardLinearSlope;           // Slope of the linear section
    	const float K = (1 - L * C) / C;               // Scale (fixed so that the derivatives of the Reinhard and linear functions are the same at x = L)
    	float3 reinhard = L * C + (1 - L * C) * (1 + K * (x - L) / ((W - L) * (W - L))) * (x - L) / (x - L + K);

    	// gamma space or not?
    	color.rgb = (x > L) ? reinhard : C * x;
	}
	return color;
}