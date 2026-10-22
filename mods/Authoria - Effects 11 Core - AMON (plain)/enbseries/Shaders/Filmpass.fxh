//=============================================================//
// FilmPass by Reshade Team (There is no name in the Credits?) //
// ENB port and DNI by Adyss                                   //
//=============================================================//
// FilmPass Shader //
//=================//
float3	filmpass(float3 color)
{
	if (USE_Filmpass==true)
	{
	float3 B = color;
	float3 G = B;
	float3 H = 0.01;
	
  // DNI Seperation by Adyss
  float FPStrength     =lerp( lerp(FPStrength_Night,     FPStrength_Day,     ENightDayFactor), FPStrength_Interior,     EInteriorFactor );
  float FPFade         =lerp( lerp(FPFade_Night,         FPFade_Day,         ENightDayFactor), FPFade_Interior,         EInteriorFactor );
  float FPContrast     =lerp( lerp(FPContrast_Night,     FPContrast_Day,     ENightDayFactor), FPContrast_Interior,     EInteriorFactor );
  float Linearization  =lerp( lerp(Linearization_Night,  Linearization_Day,  ENightDayFactor), Linearization_Interior,  EInteriorFactor );
  float FPBleach       =lerp( lerp(FPBleach_Night,       FPBleach_Day,       ENightDayFactor), FPBleach_Interior,       EInteriorFactor );
  float FPSaturation   =lerp( lerp(FPSaturation_Night,   FPSaturation_Day,   ENightDayFactor), FPSaturation_Interior,   EInteriorFactor );
  float BaseCurve      =lerp( lerp(BaseCurve_Night,      BaseCurve_Day,      ENightDayFactor), BaseCurve_Interior,      EInteriorFactor );
  float RedCurve       =lerp( lerp(RedCurve_Night,       RedCurve_Day,       ENightDayFactor), RedCurve_Interior,       EInteriorFactor );
  float GreenCurve     =lerp( lerp(GreenCurve_Night,     GreenCurve_Day,     ENightDayFactor), GreenCurve_Interior,     EInteriorFactor );
  float BlueCurve      =lerp( lerp(BlueCurve_Night,      BlueCurve_Day,      ENightDayFactor), BlueCurve_Interior,      EInteriorFactor );
  float BaseGamma      =lerp( lerp(BaseGamma_Night,      BaseGamma_Day,      ENightDayFactor), BaseGamma_Interior,      EInteriorFactor );
  float EffectGamma    =lerp( lerp(EffectGamma_Night,    EffectGamma_Day,    ENightDayFactor), EffectGamma_Interior,    EInteriorFactor );
  float EffectGammaR   =lerp( lerp(EffectGammaR_Night,   EffectGammaR_Day,   ENightDayFactor), EffectGammaR_Interior,   EInteriorFactor );
  float EffectGammaG   =lerp( lerp(EffectGammaG_Night,   EffectGammaG_Day,   ENightDayFactor), EffectGammaG_Interior,   EInteriorFactor );
  float EffectGammaB   =lerp( lerp(EffectGammaB_Night,   EffectGammaB_Day,   ENightDayFactor), EffectGammaB_Interior,   EInteriorFactor );
 
	B = saturate(B);
	B = pow(B, Linearization);
	B = lerp(H, B, FPContrast);
 
	float A = dot(B.rgb, CoefLuma);
	float3 D = A;
 
	B = pow(B, 1.0 / BaseGamma);
 
	float a = RedCurve;
	float b = GreenCurve;
	float c = BlueCurve;
	float d = BaseCurve;
 
	float y = 1.0 / (1.0 + exp(a / 2.0));
	float z = 1.0 / (1.0 + exp(b / 2.0));
	float w = 1.0 / (1.0 + exp(c / 2.0));
	float v = 1.0 / (1.0 + exp(d / 2.0));
 
	float3 C = B;
 
	D.r = (1.0 / (1.0 + exp(-a * (D.r - 0.5))) - y) / (1.0 - 2.0 * y);
	D.g = (1.0 / (1.0 + exp(-b * (D.g - 0.5))) - z) / (1.0 - 2.0 * z);
	D.b = (1.0 / (1.0 + exp(-c * (D.b - 0.5))) - w) / (1.0 - 2.0 * w);
 
	D = pow(D, 1.0 / EffectGamma);
 
	float3 Di = 1.0 - D;
 
	D = lerp(D, Di, FPBleach);
 
	D.r = pow(abs(D.r), 1.0 / EffectGammaR);
	D.g = pow(abs(D.g), 1.0 / EffectGammaG);
	D.b = pow(abs(D.b), 1.0 / EffectGammaB);
 
	if (D.r < 0.5)
		C.r = (2.0 * D.r - 1.0) * (B.r - B.r * B.r) + B.r;
	else
		C.r = (2.0 * D.r - 1.0) * (sqrt(B.r) - B.r) + B.r;
 
	if (D.g < 0.5)
		C.g = (2.0 * D.g - 1.0) * (B.g - B.g * B.g) + B.g;
	else
		C.g = (2.0 * D.g - 1.0) * (sqrt(B.g) - B.g) + B.g;

	if (D.b < 0.5)
		C.b = (2.0 * D.b - 1.0) * (B.b - B.b * B.b) + B.b;
	else
		C.b = (2.0 * D.b - 1.0) * (sqrt(B.b) - B.b) + B.b;
 
	float3 F = lerp(B, C, FPStrength);
 
	F = (1.0 / (1.0 + exp(-d * (F - 0.5))) - v) / (1.0 - 2.0 * v);
 
	float r2R = 1.0 - FPSaturation;
	float g2R = 0.0 + FPSaturation;
	float b2R = 0.0 + FPSaturation;
 
	float r2G = 0.0 + FPSaturation;
	float g2G = (1.0 - FPFade) - FPSaturation;
	float b2G = (0.0 + FPFade) + FPSaturation;
 
	float r2B = 0.0 + FPSaturation;
	float g2B = (0.0 + FPFade) + FPSaturation;
	float b2B = (1.0 - FPFade) - FPSaturation;
 
	float3 iF = F;
 
	F.r = (iF.r * r2R + iF.g * g2R + iF.b * b2R);
	F.g = (iF.r * r2G + iF.g * g2G + iF.b * b2G);
	F.b = (iF.r * r2B + iF.g * g2B + iF.b * b2B);
 
	float N = dot(F.rgb, CoefLuma);
	float3 Cn = F;
 
	if (N < 0.5)
		Cn = (2.0 * N - 1.0) * (F - F * F) + F;
	else
		Cn = (2.0 * N - 1.0) * (sqrt(F) - F) + F;
 
	Cn = pow(max(Cn,0), 1.0 / Linearization);
 
	float3 Fn = lerp(B, Cn, FPStrength);
	return Fn;
	}
	else
	return color;
}