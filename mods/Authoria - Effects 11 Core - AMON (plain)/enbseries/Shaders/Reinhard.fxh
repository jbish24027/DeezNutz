//==============================//
// Original code by Marty McFly //
// Reshade3 port by Insomnia    //
//==============================//

float3 ReinhardPass(float3 color)
{
    if (USE_Reinhard==true) {

    float ReinhardWhitepoint   =lerp( lerp(ReinhardWhitepoint_Night,   ReinhardWhitepoint_Day,   ENightDayFactor), ReinhardWhitepoint_Interior,   EInteriorFactor );
    float ReinhardScale         =lerp( lerp(ReinhardScale_Night,        ReinhardScale_Day,        ENightDayFactor), ReinhardScale_Interior,        EInteriorFactor );
	
	float3 x = color;
	const float W =  ReinhardWhitepoint;	// Linear White Point Value
    const float K =  ReinhardScale;         // Scale

    	// gamma space or not?
    	return (1 + K * x / (W * W)) * x / (x + K);
	}
	else
	return color;
}