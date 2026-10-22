//========================================================//
// Tonemapping by Matt J.P used for Skylight ENB by Aiyen //
//========================================================//

	float3 ToneFunc(float3 x)
	{
float   timeweight;
float   timevalue;	

timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * ShoulderStrengthDawn;
timevalue+=TimeOfDay1.y * ShoulderStrengthSunrise;
timevalue+=TimeOfDay1.z * ShoulderStrengthDay;
timevalue+=TimeOfDay1.w * ShoulderStrengthSunset;
timevalue+=TimeOfDay2.x * ShoulderStrengthDusk;
timevalue+=TimeOfDay2.y * ShoulderStrengthNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float ShoulderStrength;
   ShoulderStrength=lerp( (timevalue / timeweight), ShoulderStrengthInterior, EInteriorFactor );

timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * LinearStrengthDawn;
timevalue+=TimeOfDay1.y * LinearStrengthSunrise;
timevalue+=TimeOfDay1.z * LinearStrengthDay;
timevalue+=TimeOfDay1.w * LinearStrengthSunset;
timevalue+=TimeOfDay2.x * LinearStrengthDusk;
timevalue+=TimeOfDay2.y * LinearStrengthNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float LinearStrength;
   LinearStrength=lerp( (timevalue / timeweight), LinearStrengthInterior, EInteriorFactor );  
   
timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * LinearAngleDawn;
timevalue+=TimeOfDay1.y * LinearAngleSunrise;
timevalue+=TimeOfDay1.z * LinearAngleDay;
timevalue+=TimeOfDay1.w * LinearAngleSunset;
timevalue+=TimeOfDay2.x * LinearAngleDusk;
timevalue+=TimeOfDay2.y * LinearAngleNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float LinearAngle;
   LinearAngle=lerp( (timevalue / timeweight), LinearAngleInterior, EInteriorFactor );  
   
timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * ToeStrengthDawn;
timevalue+=TimeOfDay1.y * ToeStrengthSunrise;
timevalue+=TimeOfDay1.z * ToeStrengthDay;
timevalue+=TimeOfDay1.w * ToeStrengthSunset;
timevalue+=TimeOfDay2.x * ToeStrengthDusk;
timevalue+=TimeOfDay2.y * ToeStrengthNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float ToeStrength;
   ToeStrength=lerp( (timevalue / timeweight), ToeStrengthInterior, EInteriorFactor );  
   
timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * ToeNumeratorDawn;
timevalue+=TimeOfDay1.y * ToeNumeratorSunrise;
timevalue+=TimeOfDay1.z * ToeNumeratorDay;
timevalue+=TimeOfDay1.w * ToeNumeratorSunset;
timevalue+=TimeOfDay2.x * ToeNumeratorDusk;
timevalue+=TimeOfDay2.y * ToeNumeratorNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float ToeNumerator;
   ToeNumerator=lerp( (timevalue / timeweight), ToeNumeratorInterior, EInteriorFactor );  
   
timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * ToeDenominatorDawn;
timevalue+=TimeOfDay1.y * ToeDenominatorSunrise;
timevalue+=TimeOfDay1.z * ToeDenominatorDay;
timevalue+=TimeOfDay1.w * ToeDenominatorSunset;
timevalue+=TimeOfDay2.x * ToeDenominatorDusk;
timevalue+=TimeOfDay2.y * ToeDenominatorNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float ToeDenominator;
   ToeDenominator=lerp( (timevalue / timeweight), ToeDenominatorInterior, EInteriorFactor );  


		float A = ShoulderStrength;
		float B = LinearStrength;
		float C = LinearAngle;
		float D = ToeStrength;
		float E = ToeNumerator;
		float F = ToeDenominator;
		return ((x*(A*x+C*B)+D*E)/(x*(A*x+B)+D*F)) - E/F;
	}

	float3 ToneMapFilmic(float3 color)
	{
float   timeweight;
float   timevalue;

timeweight=0.000001;
timevalue=0.0;
   
timevalue+=TimeOfDay1.x * LinearWhiteDawn;
timevalue+=TimeOfDay1.y * LinearWhiteSunrise;
timevalue+=TimeOfDay1.z * LinearWhiteDay;
timevalue+=TimeOfDay1.w * LinearWhiteSunset;
timevalue+=TimeOfDay2.x * LinearWhiteDusk;
timevalue+=TimeOfDay2.y * LinearWhiteNight;

timeweight+=TimeOfDay1.x;
timeweight+=TimeOfDay1.y;
timeweight+=TimeOfDay1.z;
timeweight+=TimeOfDay1.w;
timeweight+=TimeOfDay2.x;
timeweight+=TimeOfDay2.y;
   
   float LinearWhite;
   LinearWhite=lerp( (timevalue / timeweight), LinearWhiteInterior, EInteriorFactor );  

		float3 numerator = ToneFunc(color);        
		float3 denominator = ToneFunc(LinearWhite);
		return numerator / denominator;
	}