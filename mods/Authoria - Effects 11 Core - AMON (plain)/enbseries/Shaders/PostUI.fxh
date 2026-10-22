
// Ady: i found it more clean to have all the UI in an external file

float empty62 < string UIName = "|==== Global Settings ====|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

#if (USE_LUTweel==1)
float LUTSelect           <string UIName= weelname ;                              string UIWidget="Spinner";  float UIMin=0.0;  float UIMax=LUTcounter;   float UIStep=1;   > = {0.0};
#endif

float ExposureGOB         <string UIName="Global Brightness";                     string UIWidget="Spinner";  float UIMin=-3.0;  float UIMax=4.0;   float UIStep=0.1;   > = {0.0};
float GlobalTemperature   <string UIName="Global Temperature";		              string UIWidget="Spinner";  float UIMin=-0.15; float UIMax=0.15;	float UIStep=0.01;  > = {0.0};
bool  LIFTNAO             <string UIName="Lift Shadows";                                                                                                                > = {false};
bool  DROPNAO             <string UIName="Drop Shadows";                                                                                                                > = {false};



#if (INC_FishEye==1)
bool USE_FISH < string UIName = "Use Fisheye"; > = {false}; 

float	iFisheyeMod
<
	string UIName="Fisheye Mode";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=3.0;
	float UIStep=1.0;
> = {0.0};

float	fFisheyeZoom
<
	string UIName="Fisheye Zoom";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=1.0;
> = {0.55};

float	fFisheyeDistortion
<
	string UIName="Fisheye Distortion";
	string UIWidget="spinner";
	float UIMin=-0.300;
	float UIMax=0.300;
	float UIStep=0.01;
> = {0.01};

float	fFisheyeDistortionCubic
<
	string UIName="Fisheye Distortion Cube";
	string UIWidget="spinner";
	float UIMin=-0.300;
	float UIMax=0.300;
	float UIStep=0.01;
> = {0.7};

float	fFisheyeColorshift
<
	string UIName="Fisheye Colorshift";
	string UIWidget="spinner";
	float UIMin=-0.10;
	float UIMax=0.10;
	float UIStep=0.01;
> = {0.002};
#endif

#if (INC_Emboss==1)
bool USE_Emboss < string UIName = "Use Emboss"; > = {false}; 

float	fEmbossPower
<
	string UIName="Emboss Power";
	string UIWidget="spinner";
	float UIMin=0.01;
	float UIMax=2.0;
> = {0.150};

float	fEmbossOffset
<
	string UIName="Emboss Offset";
	string UIWidget="spinner";
	float UIMin=0.1;
	float UIMax=5.0;
> = {1.00};

float	iEmbossAngle
<
	string UIName="Emboss Angle";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=360.0;
	float UIStep=1.0;
> = {90.0};
#endif

#if (INC_Letterbox==1)
bool ENABLE_LETTERBOX        < string UIName = "|=== Toggle Letterbox ===|";> = {false};

float2	border_width
<
	string UIName="Letterbox Position - ";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.0, 1.0};

#define	border_ratio 1 // Supposed to be in UI but not working

float3	border_color
<
	string UIName = "Letterbox Color";
	string UIWidget = "color";
> = {0.0, 0.0, 0.0};
#endif



float empty2 < string UIName = "|=======Toggles=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
#if (INC_HDR==1)
bool USE_HDR < string UIName = "Use HDR"; > = {false};
#endif
#if (INC_Vibrance==1)
bool USE_Vibrance < string UIName = "Use Vibrance"; > = {false};
#endif
#if (INC_DPX==1)
bool USE_DPX < string UIName = "Use DPX"; > = {false};
#endif
#if (INC_Curves==1)
bool USE_Curves < string UIName = "Use Curves"; > = {false};
#endif
#if (INC_Reinhard==1)
bool USE_Reinhard < string UIName = "Use Reinhard"; > = {false};
#endif
#if (INC_Reinhard==2)
bool USE_Reinhard < string UIName = "Use Reinhard"; > = {false};
#endif
#if (INC_Filmpass==1)
bool USE_Filmpass < string UIName = "Use Filmpass"; > = {false};
#endif
#if (INC_Spherical==1)
bool USE_Spherical < string UIName="Use Spherical "; > = {false};
#endif
#if (INC_Tint==1)
bool use_tinting < string UIName = "Use Tinting"; > = {false};
#endif
#if (INC_Technicolor==1)
bool use_technicolor < string UIName="Use Technicolor"; > = {false};
#endif
#if (INC_Technicolor2==1)
bool use_t2s < string UIName="Use Technicolor 2 Strip"; > = {false};
#endif
#if (INC_Lightroom==1)
bool USE_Lightroom < string UIName="Use Lightroom "; > = {false};
#endif
#if (INC_LumaSHARP==1)
bool USE_LumaSharp < string UIName = "Use Luma Sharp"; > = {false};
#endif
#if (INC_Shadow==1)
bool USE_Shadows < string UIName = "Use Shadow Adjustments"; > = {false};
#endif
#if (INC_SBloom==1)
bool  USE_SBloom             <string UIName="Sweet Bloom"; > = {false};
#endif

bool ENABLE_DITHER < string UIName = "Enable Dither";   > = {false};


#if (INC_GaussBloom==1)
bool  USE_GaussBloom      <string UIName="Gaussian Bloom"; > = {false};

bool lumabloom <
   string UIName="Luma based Bloom";
> = {true};


float lumasource <
   string UIName="Luma Src 1_orig | 2_softlight | 3_blend";
   string UIWidget="Spinner";
   float UIMin=1;
   float UIMax=3;
   float UIStep=1;
> = {2};
float gauss_blur <
   string UIName="Gaussian Blur Strength";
   string UIWidget="Spinner";
   float UIMin=1;
   float UIMax=3;
   float UIStep=1;
> = {2};
#endif


float empty6 < string UIName = "|===== Sharp Settings =====|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
#if (INC_LumaSHARP==1)
float	LSharpStrength
<
	string UIName="LS: Sharp Strength";
	string UIWidget="spinner";
	float UIMin=0.10;
	float UIMax=3.00;
> = {0.70};

float	LSharpClamp
<
	string UIName="LS: Sharp Clamp";
	string UIWidget="spinner";
	float UIMin=0.000;
	float UIMax=1.000;
> = {0.035};

int		LSharpPattern
<
	string UIName="LS: Sharp Pattern";
	string UIWidget="spinner";
	float UIMin=0;
	float UIMax=3;
> = {2};

float	LSharpOffsetBias
<
	string UIName="LS: Offset Bias";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=6.0;
> = {1.0};
#endif
/*
bool shader_off <
	string UIName="Show Original";
> = {false};
bool show_edges <
	string UIName="Show Edges";
> = {false};
bool smooth_edges <
	string UIName="Use Edge Smoothing";
> = {true};
float smooth <
	string UIName="Edge Smoothing Intensity";
	string UIWidget="Spinner";
	float UIMin=0.3;
	float UIMax=1;
	float UIStep=0.001;
> = {0.52};
float farDepth <
	string UIName="Depth Sharpening: Far Depth";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=100000.0;
	float UIStep=0.1;
> = {100.0};
float limiterE <
	string UIName="Sharpening HL Limiter Exterior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=1;
	float UIStep=0.001;
> = {0.1};
float limiterI <
	string UIName="Sharpening HL Limiter Interior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=1;
	float UIStep=0.001;
> = {0.1};
bool luma_sharpen <
	string UIName="Use Luma Sharpen";
> = {true};
float BlurSigmaE <
	string UIName="Blur Sigma Exterior";
	string UIWidget="Spinner";
	float UIMin=0.3;
	float UIMax=2;
	float UIStep=0.001;
> = {0.87};
float BlurSigmaI <
	string UIName="Blur Sigma Interior";
	string UIWidget="Spinner";
	float UIMin=0.3;
	float UIMax=2;
	float UIStep=0.001;
> = {0.98};
float SharpeningE <
	string UIName="Sharpening Strength Exterior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=5;
	float UIStep=0.001;
> = {1.67};
float SharpeningI <
	string UIName="Sharpening Strength Interior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=5;
	float UIStep=0.001;
> = {1.87};
float ThresholdE <
	string UIName="Sharpening Threshold Exterior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=255;
	float UIStep=1;
> = {1};
float ThresholdI <
	string UIName="Sharpening Threshold Interior";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=255;
	float UIStep=1;
> = {0};
*/

#if (INC_FilmicAnamorphSharp==1)
float FASStrength <
	string UIName="Sharpen strength";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=3.0;
	float UIStep=0.005;
> = {1.0};

float FASClamp <
	string UIName="Sharpen clamping";
	string UIWidget="Spinner";
	float UIMin=0.5;
	float UIMax=1.0;
	float UIStep=0.001;
> = {1.0};

float FASOffset <
	string UIName="High-pass cross offset in pixels";
	string UIWidget="Spinner";
	float UIMin=0;
	float UIMax=2;
	float UIStep=1;
> = {1};

float FASContrast <
	string UIName="Depth high-pass mask amount";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=2000.0;
	float UIStep=1.0;
> = {128.0};
#endif

#if (INC_BasicSharp==1)
float	ESharpAmount
<
	string UIName="Sharp:: amount";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=4.0;
> = {1.0};

float	ESharpRange
<
	string UIName="Sharp:: range";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};
#endif

float empty7 < string UIName = "|===== Day =====|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
#if (INC_DPX==1)
float empty8 < string UIName = "|===== DPX Day =====|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	RGB_Curve_Day
<
	string UIName="DPX: RGB Curve Day";
	string UIWidget="Slider";
	float UIMin=0.0;
	float UIMax=16.0;
> = {8.0};

float	RGB_C_Day
<
	string UIName="DPX: RGB C Day";
	string UIWidget="Slider";
	float UIMin=0.2;
	float UIMax=0.5;
> = {0.36};

float	ContrastDPX_Day
<
	string UIName="DPX: Contrast Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.1};

float	SaturationDPX_Day
<
	string UIName="DPX: Saturation Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {3.0};

float	ColorfulnessDPX_Day
<
	string UIName="DPX: Colorfulness Day";
	string UIWidget="spinner";
	float UIMin=0.1;
	float UIMax=2.5;
> = {2.5};

float	StrengthDPX_Day
<
	string UIName="DPX: Strength Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.20};
#endif

#if (INC_Reinhard==1)
float empty9 < string UIName = "|=======Linear Reinhard Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	ReinhardLinearSlope_Day
<
	string UIName="RH: Linear Slope Day";
	string UIWidget="spinner";
	float UIMin=1.0;
	float UIMax=5.0;
> = {1.25};

float	ReinhardLinearWhitepoint_Day
<
	string UIName="RH: White Point Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=20.0;
> = {7.25};

float	ReinhardLinearPoint_Day
<
	string UIName="RH: Linear Point Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.15};
#endif
#if (INC_Reinhard==2)
float empty46 < string UIName = "|=======Reinhard Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	ReinhardWhitepoint_Day
<
	string UIName="RH: White Point Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=10.0;
> = {1.25};

float	ReinhardScale_Day
<
	string UIName="RH: Scale Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=3.0;
> = {0.5};
#endif


#if (INC_Vibrance==1)
float empty11 < string UIName = "|=======Vibrance Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Vibrance_Day <
   string UIName="Vibrance Day";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.15};

float3	VibranceRGBBalance_Day
<
	string UIName = "RGB Vibrance Day";
	string UIWidget = "color";
    float UIMin=-10.0;
    float UIMax=10.0;
> = {1.0, 1.0, 1.0};
#endif

#if (INC_Curves==1)
float empty12 < string UIName = "|=======Curves Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Mode_Day <
   string UIName="Curve Mode Day";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=2.0;
   float UIStep=1.0;
> = {0.0};

float Formula_Day <
   string UIName="Curve Formula Day";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=10.0;
   float UIStep=1.0;
> = {4.0};

float Contrast_Day <
   string UIName="Curves Blend Day";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.65};
#endif

#if (INC_HDR==1)
float empty13 < string UIName = "|=======HDR Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float HDRPower_Day <
   string UIName="HDR Power Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {1.3};

float radius1_Day <
   string UIName="Radius 1 Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.79};

float radius2_Day <
   string UIName="Radius 2 Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.87};
#endif

#if (INC_Filmpass==1)
float empty14 < string UIName = "|=======Filmpass Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	FPStrength_Day
<
	string UIName="FP: Strength Day";
	string UIWidget="spinner";
	float UIMin=0.05;
	float UIMax=1.5;
> = {0.85};

float	FPFade_Day
<
	string UIName="FP: Fade Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=0.6;
> = {0.4};

float	FPContrast_Day
<
	string UIName="FP: Contrast Day";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {1.0};

float	Linearization_Day
<
	string UIName="FP: Linearization Day";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {0.5};

float	FPBleach_Day
<
	string UIName="FP: Bleach Day";
	string UIWidget="spinner";
	float UIMin=-0.5;
	float UIMax=1.0;
> = {0.0};

float	FPSaturation_Day
<
	string UIName="FP: Saturation Day";
	string UIWidget="spinner";
	float UIMin=-1.0;
	float UIMax=1.0;
> = {-0.15};

float	RedCurve_Day
<
	string UIName="FP: Red Curve Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	GreenCurve_Day
<
	string UIName="FP: Green Curve Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BlueCurve_Day
<
	string UIName="FP: Blue Curve Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BaseCurve_Day
<
	string UIName="FP: Base Curve Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.5};

float	BaseGamma_Day
<
	string UIName="FP: Base Gamma Day";
	string UIWidget="spinner";
	float UIMin=0.7;
	float UIMax=2.0;
> = {1.0};

float	EffectGamma_Day
<
	string UIName="FP: Effect Gamma Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.65};

float	EffectGammaR_Day
<
	string UIName="FP Effect Gamma Red Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaG_Day
<
	string UIName="FP Effect Gamma Green Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaB_Day
<
	string UIName="FP Effect Gamma Blue Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};
#endif

#if (INC_Spherical==1)
float empty15 < string UIName = "|=======Spherical Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	sphericalAmount_Day
<
	string UIName="Spherical Amount Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.5};
#endif

#if (INC_Tint==1)
float empty35 < string UIName = "|=======Tinting Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 RGB_TintD <
   string UIName="Tint Color Day";
   string UIWidget="Color";
> = {0.725, 0.431, 0.118};
float HighlightPowerD <
   string UIName="Highlight Color Power Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float TintPowerD <
   string UIName="Tint Color Power Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowPowerD <
   string UIName="Shadow Color Power Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowStrD <
   string UIName="Add Shadow Color Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float SHueAdjustD <
   string UIName="Shift Shadow Hue Day";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatShadowsD <
   string UIName="Desaturate Shadows Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatMidsD <
   string UIName="Desaturate Midtones Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatOrigD <
   string UIName="Desaturate Original Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float3 TonedD <
   string UIName="Effect Strength Day";
   string UIWidget="Color";
> = {0.314, 0.314, 0.314};
#endif

#if (INC_Technicolor==1)
float empty38 < string UIName = "|=======Techicolor Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 colStrengthD <
   string UIName="Technicolor Color Strength Day";
   string UIWidget="Color";
> = {0.5, 0.5, 0.5};
float brightnessD <
   string UIName="Technicolor Brightness Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrengthD <
   string UIName="Technicolor Amount Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Technicolor2==1)
float empty43 < string UIName = "|=======Techicolor 2 Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 rChannelD <
   string UIName="Technicolor 2s Red Day";
   string UIWidget="Color";
> = {1, 0.165, 0};
float3 gChannelD <
   string UIName="Technicolor 2s Green Day";
   string UIWidget="Color";
> = {0.294, 1, 0};
float3 bChannelD <
   string UIName="Technicolor 2s Blue Day";
   string UIWidget="Color";
> = {0.0588, 0.902, 0};
float strip2vibD <
   string UIName="Technicolor 2s Saturation Boost Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrength2D <
   string UIName="Technicolor 2s Amount Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Shadow==1)
float empty54 < string UIName = "|=======Shadows Day=======<"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ECCGamma_Day
<
	string UIName="Gamma Day";
	string UIWidget="Spinner";
	float UIMin=0.2;
	float UIMax=5.0;
> = {1.0};

float	ECCInBlack_Day
<
	string UIName="In black Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCInWhite_Day
<
	string UIName="In white Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCOutBlack_Day
<
	string UIName="Out black Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCOutWhite_Day
<
	string UIName="Out white Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCDesaturateShadows_Day
<
	string UIName="Desaturate shadows Day";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	LightnessD <		string UIName="Highlights Day";							string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};
float	ShadowsD <			string UIName="Shadows Day";								string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};

#endif

#if (INC_SBloom==1)
float empty56 < string UIName = "|=======Sweet Bloom Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	BloomThreshold_Day
<
	string UIName="SBloom Threshold Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=50.0;
> = {20.25};

float	BloomPower_Day
<
	string UIName="SBloom Power Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {1.44};

float	BloomWidth_Day
<
	string UIName="SBloom Width Day";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
	float UIStep=0.0001;
> = {0.0142};
#endif


#if (INC_GaussBloom==1)
float empty59 < string UIName = "|=======Gaussian Bloom Day=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float sl_mix_set_Day <
   string UIName="Soft Light Intensity Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.275};

float gauss_bloom_Day <
   string UIName="Gaussian Bloom Intensity Day";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.550};
#endif

float empty16 < string UIName = "|=========NIGHT=========|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
#if (INC_DPX==1)
float empty17 < string UIName = "|=======DPX Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	RGB_Curve_Night
<
	string UIName="DPX: RGB Curve Night";
	string UIWidget="Slider";
	float UIMin=0.0;
	float UIMax=16.0;
> = {8.0};

float	RGB_C_Night
<
	string UIName="DPX: RGB C Night";
	string UIWidget="Slider";
	float UIMin=0.2;
	float UIMax=0.5;
> = {0.36};

float	ContrastDPX_Night
<
	string UIName="DPX: Contrast Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.1};

float	SaturationDPX_Night
<
	string UIName="DPX: Saturation Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {3.0};

float	ColorfulnessDPX_Night
<
	string UIName="DPX: Colorfulness Night";
	string UIWidget="spinner";
	float UIMin=0.1;
	float UIMax=2.5;
> = {2.5};

float	StrengthDPX_Night
<
	string UIName="DPX: Strength Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.20};
#endif


#if (INC_Reinhard==1)
float empty18 < string UIName = "|=======Reinhard Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ReinhardLinearSlope_Night
<
	string UIName="RH: Linear Slope Night";
	string UIWidget="spinner";
	float UIMin=1.0;
	float UIMax=5.0;
> = {1.25};

float	ReinhardLinearWhitepoint_Night
<
	string UIName="RH: White Point Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=20.0;
> = {7.25};

float	ReinhardLinearPoint_Night
<
	string UIName="RH: Linear Point Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.15};
#endif

#if (INC_Reinhard==2)
float empty47 < string UIName = "|=======Reinhard Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ReinhardWhitepoint_Night
<
	string UIName="RH: White Point Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=10.0;
> = {1.25};

float	ReinhardScale_Night
<
	string UIName="RH: Scale Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=3.0;
> = {0.5};
#endif


#if (INC_Vibrance==1)
float empty20 < string UIName = "|=======Vibrance Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Vibrance_Night <
   string UIName="Vibrance Night";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.15};

float3	VibranceRGBBalance_Night
<
	string UIName = "RGB Vibrance Night";
	string UIWidget = "color";
    float UIMin=-10.0;
    float UIMax=10.0;
> = {1.0, 1.0, 1.0};
#endif

#if (INC_Curves==1)
float empty21 < string UIName = "|=======Curves Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Mode_Night <
   string UIName="Curve Mode Night";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=2.0;
   float UIStep=1.0;
> = {0.0};

float Formula_Night <
   string UIName="Curve Formula Night";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=10.0;
   float UIStep=1.0;
> = {4.0};

float Contrast_Night <
   string UIName="Curves Blend Night";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.65};
#endif

#if (INC_HDR==1)
float empty22 < string UIName = "|=======HDR Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float HDRPower_Night <
   string UIName="HDR Power Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {1.3};

float radius1_Night <
   string UIName="Radius 1 Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.79};

float radius2_Night <
   string UIName="Radius 2 Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.87};
#endif

#if (INC_Filmpass==1)
float empty23 < string UIName = "|=======Filmpass Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	FPStrength_Night
<
	string UIName="FP: Strength Night";
	string UIWidget="spinner";
	float UIMin=0.05;
	float UIMax=1.5;
> = {0.85};

float	FPFade_Night
<
	string UIName="FP: Fade Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=0.6;
> = {0.4};

float	FPContrast_Night
<
	string UIName="FP: Contrast Night";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {1.0};

float	Linearization_Night
<
	string UIName="FP: Linearization Night";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {0.5};

float	FPBleach_Night
<
	string UIName="FP: Bleach Night";
	string UIWidget="spinner";
	float UIMin=-0.5;
	float UIMax=1.0;
> = {0.0};

float	FPSaturation_Night
<
	string UIName="FP Saturation Night";
	string UIWidget="spinner";
	float UIMin=-1.0;
	float UIMax=1.0;
> = {-0.15};

float	RedCurve_Night
<
	string UIName="FP: Red Curve Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	GreenCurve_Night
<
	string UIName="FP: Green Curve Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BlueCurve_Night
<
	string UIName="FP: Blue Curve Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BaseCurve_Night
<
	string UIName="FP: Base Curve Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.5};

float	BaseGamma_Night
<
	string UIName="FP: Base Gamma Night";
	string UIWidget="spinner";
	float UIMin=0.7;
	float UIMax=2.0;
> = {1.0};

float	EffectGamma_Night
<
	string UIName="FP: Effect Gamma Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.65};

float	EffectGammaR_Night
<
	string UIName="FP Effect Gamma Red Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaG_Night
<
	string UIName="FP Effect Gamma Green Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaB_Night
<
	string UIName="FP Effect Gamma Blue Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};
#endif

#if (INC_Spherical==1)
float empty24 < string UIName = "|=======Spherical Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	sphericalAmount_Night
<
	string UIName="Spherical Amount Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.5};
#endif

#if (INC_Tint==1)
float empty36 < string UIName = "|=======Tinting Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 RGB_TintN <
   string UIName="Tint Color Night";
   string UIWidget="Color";
> = {0.725, 0.431, 0.118};
float HighlightPowerN <
   string UIName="Highlight Color Power Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float TintPowerN <
   string UIName="Tint Color Power Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowPowerN <
   string UIName="Shadow Color Power Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowStrN <
   string UIName="Add Shadow Color Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float SHueAdjustN <
   string UIName="Shift Shadow Hue Night";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatShadowsN <
   string UIName="Desaturate Shadows Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatMidsN <
   string UIName="Desaturate Midtones Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatOrigN <
   string UIName="Desaturate Original Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float3 TonedN <
   string UIName="Effect Strength Night";
   string UIWidget="Color";
> = {0.314, 0.314, 0.314};
#endif

#if (INC_Technicolor==1)
float empty26 < string UIName = "|=======Techicolor Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 colStrengthN <
   string UIName="Technicolor Color Strength Night";
   string UIWidget="Color";
> = {0.5, 0.5, 0.5};
float brightnessN <
   string UIName="Technicolor Brightness Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrengthN <
   string UIName="Technicolor Amount Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Technicolor2==1)
float empty44 < string UIName = "|=======Techicolor 2 Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 rChannelN <
   string UIName="Technicolor 2s Red Night";
   string UIWidget="Color";
> = {1, 0.165, 0};
float3 gChannelN <
   string UIName="Technicolor 2s Green Night";
   string UIWidget="Color";
> = {0.294, 1, 0};
float3 bChannelN <
   string UIName="Technicolor 2s Blue Night";
   string UIWidget="Color";
> = {0.0588, 0.902, 0};
float strip2vibN <
   string UIName="Technicolor 2s Saturation Boost Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrength2N <
   string UIName="Technicolor 2s Amount Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Shadow==1)
float empty53 < string UIName = "|=======Shadows Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ECCGamma_Night
<
	string UIName="Gamma Night";
	string UIWidget="Spinner";
	float UIMin=0.2;
	float UIMax=5.0;
> = {1.0};

float	ECCInBlack_Night
<
	string UIName="In black Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCInWhite_Night
<
	string UIName="In white Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCOutBlack_Night
<
	string UIName="Out black Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCOutWhite_Night
<
	string UIName="Out white Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCDesaturateShadows_Night
<
	string UIName="Desaturate shadows Night";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	LightnessN <		string UIName="Highlights Night";							string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};
float	ShadowsN <			string UIName="Shadows Night";								string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};

#endif

#if (INC_SBloom==1)
float empty57 < string UIName = "|=======Sweet Bloom Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	BloomThreshold_Night
<
	string UIName="SBloom Threshold Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=50.0;
> = {20.25};

float	BloomPower_Night
<
	string UIName="SBloom Power Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {1.44};

float	BloomWidth_Night
<
	string UIName="SBloom Width Night";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
	float UIStep=0.0001;
> = {0.0142};
#endif

#if (INC_GaussBloom==1)
float empty60 < string UIName = "|=======Gaussian Bloom Night=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float sl_mix_set_Night <
   string UIName="Soft Light Intensity Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.275};

float gauss_bloom_Night <
   string UIName="Gaussian Bloom Intensity Night";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.550};
#endif

float empty25 < string UIName = "|=========INTERIOR=========|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

#if (INC_DPX==1)
float empty42 < string UIName = "|=======DPX Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	RGB_Curve_Interior
<
	string UIName="DPX: RGB Curve Interior";
	string UIWidget="Slider";
	float UIMin=0.0;
	float UIMax=16.0;
> = {8.0};

float	RGB_C_Interior
<
	string UIName="DPX: RGB C Interior";
	string UIWidget="Slider";
	float UIMin=0.2;
	float UIMax=0.5;
> = {0.36};

float	ContrastDPX_Interior
<
	string UIName="DPX: Contrast Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.1};

float	SaturationDPX_Interior
<
	string UIName="DPX: Saturation Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {3.0};

float	ColorfulnessDPX_Interior
<
	string UIName="DPX: Colorfulness Interior";
	string UIWidget="spinner";
	float UIMin=0.1;
	float UIMax=2.5;
> = {2.5};

float	StrengthDPX_Interior
<
	string UIName="DPX: Strength Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.20};
#endif
#if (INC_Reinhard==1)
float empty41 < string UIName = "|=======Linear Reinhard Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	ReinhardLinearSlope_Interior
<
	string UIName="RH: Linear Slope Interior";
	string UIWidget="spinner";
	float UIMin=1.0;
	float UIMax=5.0;
> = {1.25};

float	ReinhardLinearWhitepoint_Interior
<
	string UIName="RH: White Point Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=20.0;
> = {7.25};

float	ReinhardLinearPoint_Interior
<
	string UIName="RH: Linear Point Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.15};
#endif
#if (INC_Reinhard==2)
float empty48 < string UIName = "|======Reinhard Interior======="; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ReinhardWhitepoint_Interior
<
	string UIName="RH: White Point Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=10.0;
> = {1.25};

float	ReinhardScale_Interior
<
	string UIName="RH: Scale Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=3.0;
> = {0.5};
#endif


#if (INC_Vibrance==1)
float empty29 < string UIName = "|======Vibrance Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Vibrance_Interior <
   string UIName="Vibrance Interior";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.15};

float3	VibranceRGBBalance_Interior
<
	string UIName = "RGB Vibrance Interior";
	string UIWidget = "color";
    float UIMin=-10.0;
    float UIMax=10.0;
> = {1.0, 1.0, 1.0};
#endif

#if (INC_Curves==1)
float empty30 < string UIName = "|======Curves Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float Mode_Interior <
   string UIName="Curve Mode Interior";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=2.0;
   float UIStep=1.0;
> = {0.0};

float Formula_Interior <
   string UIName="Curve Formula Interior";
   string UIWidget="Spinner";
   float UIMin=-0.0;
   float UIMax=10.0;
   float UIStep=1.0;
> = {4.0};

float Contrast_Interior <
   string UIName="Curves Interior";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
> = {0.65};
#endif

#if (INC_HDR==1)
float empty31 < string UIName = "|======HDR Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float HDRPower_Interior <
   string UIName="HDR Power Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {1.3};

float radius1_Interior <
   string UIName="Radius 1 Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.79};

float radius2_Interior <
   string UIName="Radius 2 Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=8.0;
> = {0.87};
#endif

#if (INC_Filmpass==1)
float empty32 < string UIName = "|=======Filmpass Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	FPStrength_Interior
<
	string UIName="FP: Strength Interior";
	string UIWidget="spinner";
	float UIMin=0.05;
	float UIMax=1.5;
> = {0.85};

float	FPFade_Interior
<
	string UIName="FP: Fade Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=0.6;
> = {0.4};

float	FPContrast_Interior
<
	string UIName="FP: Contrast Interior";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {1.0};

float	Linearization_Interior
<
	string UIName="FP: Linearization Interior";
	string UIWidget="spinner";
	float UIMin=0.5;
	float UIMax=2.0;
> = {0.5};

float	FPBleach_Interior
<
	string UIName="FP: Bleach Interior";
	string UIWidget="spinner";
	float UIMin=-0.5;
	float UIMax=1.0;
> = {0.0};

float	FPSaturation_Interior
<
	string UIName="FP: Saturation Interior";
	string UIWidget="spinner";
	float UIMin=-1.0;
	float UIMax=1.0;
> = {-0.15};

float	RedCurve_Interior
<
	string UIName="FP: Red Curve Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	GreenCurve_Interior
<
	string UIName="FP: Green Curve Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BlueCurve_Interior
<
	string UIName="FP: Blue Curve Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	BaseCurve_Interior
<
	string UIName="FP: Base Curve Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.5};

float	BaseGamma_Interior
<
	string UIName="FP: Base Gamma Interior";
	string UIWidget="spinner";
	float UIMin=0.7;
	float UIMax=2.0;
> = {1.0};

float	EffectGamma_Interior
<
	string UIName="FP: Effect Gamma Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.65};

float	EffectGammaR_Interior
<
	string UIName="FP Effect Gamma Red Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaG_Interior
<
	string UIName="FP Effect Gamma Green Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};

float	EffectGammaB_Interior
<
	string UIName="FP Effect Gamma Blue Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {1.0};
#endif

#if (INC_Spherical==1)
float empty34 < string UIName = "|=======Spherical Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	sphericalAmount_Interior
<
	string UIName="Spherical Amount Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=2.0;
> = {0.5};
#endif

#if (INC_Tint==1)
float empty37 < string UIName = "|======Tinting Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 RGB_TintI <
   string UIName="Tint Color Interior";
   string UIWidget="Color";
> = {0.725, 0.431, 0.118};
float HighlightPowerI <
   string UIName="Highlight Color Power Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float TintPowerI <
   string UIName="Tint Color Power Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowPowerI <
   string UIName="Shadow Color Power Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=100.0;
   float UIStep=0.001;
> = {1};
float ShadowStrI <
   string UIName="Add Shadow Color Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float SHueAdjustI <
   string UIName="Shift Shadow Hue Interior";
   string UIWidget="Spinner";
   float UIMin=-1.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatShadowsI <
   string UIName="Desaturate Shadows Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatMidsI <
   string UIName="Desaturate Midtones Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float DesatOrigI <
   string UIName="Desaturate Original Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.0};
float3 TonedI <
   string UIName="Effect Strength Interior";
   string UIWidget="Color";
> = {0.314, 0.314, 0.314};
#endif

#if (INC_Technicolor==1)
float empty40 < string UIName = "|=======Techicolor Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 colStrengthI <
   string UIName="Technicolor Color Strength Interior";
   string UIWidget="Color";
> = {0.5, 0.5, 0.5};
float brightnessI <
   string UIName="Technicolor Brightness Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
float techStrengthI <
   string UIName="Technicolor Amount Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Technicolor2==1)
float empty45 < string UIName = "|======Techicolor 2 Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float3 rChannelI <
   string UIName="Technicolor 2s Red Interior";
   string UIWidget="Color";
> = {1, 0.165, 0};
float3 gChannelI <
   string UIName="Technicolor 2s Green Interior";
   string UIWidget="Color";
> = {0.294, 1, 0};
float3 bChannelI <
   string UIName="Technicolor 2s Blue Interior";
   string UIWidget="Color";
> = {0.0588, 0.902, 0};
float strip2vibI <
   string UIName="Technicolor 2s Saturation Boost Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.3};
float techStrength2I <
   string UIName="Technicolor 2s Amount Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {1.0};
#endif

#if (INC_Shadow==1)
float empty55 < string UIName = "|=======Shadows Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};
float	ECCGamma_Interior
<
	string UIName="Gamma Interior";
	string UIWidget="Spinner";
	float UIMin=0.2;
	float UIMax=5.0;
> = {1.0};

float	ECCInBlack_Interior
<
	string UIName="In black Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCInWhite_Interior
<
	string UIName="In white Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCOutBlack_Interior
<
	string UIName="Out black Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	ECCOutWhite_Interior
<
	string UIName="Out white Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {1.0};

float	ECCDesaturateShadows_Interior
<
	string UIName="Desaturate shadows Interior";
	string UIWidget="Spinner";
	float UIMin=0.0;
	float UIMax=1.0;
> = {0.0};

float	LightnessI <		string UIName="Highlights Interior";						string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};
float	ShadowsI <			string UIName="Shadows Interior";							string UIWidget="Spinner";	float UIMin=0.0;	float UIMax=1.0;	float UIStep=0.001;	> = {0.0};
#endif

#if (INC_SBloom==1)
float empty58 < string UIName = "|======Sweet Bloom Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float	BloomThreshold_Interior
<
	string UIName="SBloom Threshold Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=50.0;
> = {20.25};

float	BloomPower_Interior
<
	string UIName="SBloom Power Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=8.0;
> = {1.44};

float	BloomWidth_Interior
<
	string UIName="SBloom Width Interior";
	string UIWidget="spinner";
	float UIMin=0.0;
	float UIMax=1.0;
	float UIStep=0.0001;
> = {0.0142};
#endif

#if (INC_GaussBloom==1)
float empty61 < string UIName = "|======Gaussian Bloom Interior=======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};

float sl_mix_set_Interior <
   string UIName="Soft Light Intensity Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.275};

float gauss_bloom_Interior <
   string UIName="Gaussian Bloom Intensity Interior";
   string UIWidget="Spinner";
   float UIMin=0.0;
   float UIMax=1.0;
   float UIStep=0.001;
> = {0.550};
#endif

#if (INC_Lightroom==1)
float empty63 < string UIName = "|====== Lightroom Settings =======|"; string UIWidget = "Slider"; float UIMin = 0.0; float UIMax = 0.0; > = {0.0};


bool    bShowClippingWhite		 < string UIName="Show white clipping";			> = {false};
bool    bShowClippingBlack	 	 < string UIName="Show black clipping";			> = {false};
float	fLightroom_Red_Hueshift		 < string UIName="Hue: Red";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Orange_Hueshift	 < string UIName="Hue: Orange";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Yellow_Hueshift	 < string UIName="Hue: Yellow";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Green_Hueshift	 < string UIName="Hue: Green";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Aqua_Hueshift	 < string UIName="Hue: Aqua";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Blue_Hueshift	 < string UIName="Hue: Blue";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Magenta_Hueshift	 < string UIName="Hue: Magenta";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Red_Exposure		 < string UIName="Exposure: Red";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Orange_Exposure	 < string UIName="Exposure: Orange";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Yellow_Exposure	 < string UIName="Exposure: Yellow";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Green_Exposure	 < string UIName="Exposure: Green";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Aqua_Exposure	 < string UIName="Exposure: Aqua";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Blue_Exposure	 < string UIName="Exposure: Blue";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Magenta_Exposure	 < string UIName="Exposure: Magenta";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Red_Saturation	 < string UIName="Saturation: Red";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Orange_Saturation	 < string UIName="Saturation: Orange";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Yellow_Saturation	 < string UIName="Saturation: Yellow";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Green_Saturation	 < string UIName="Saturation: Green";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Aqua_Saturation	 < string UIName="Saturation: Aqua";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Blue_Saturation	 < string UIName="Saturation: Blue";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_Magenta_Saturation	 < string UIName="Saturation: Magenta";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalBlackLevel	 < string UIName="Global Black Level";		string UIWidget="Spinner";	float UIStep=1.0;	float UIMin=0.0;	float UIMax=512.0;	> = {0.0};
float	fLightroom_GlobalWhiteLevel	 < string UIName="Global White Level";		string UIWidget="Spinner";	float UIStep=1.0;	float UIMin=0.0;	float UIMax=512.0;	> = {255.0};
float	fLightroom_GlobalExposure	 < string UIName="Global Exposure";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalGamma		 < string UIName="Global Gamma";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalBlacksCurve	 < string UIName="Global Blacks Curve";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalShadowsCurve	 < string UIName="Global Shadows Curve";	string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalMidtonesCurve	 < string UIName="Global Midtones Curve";	string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalHighlightsCurve < string UIName="Global Highlights Curve";	string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalWhitesCurve 	 < string UIName="Global Whites Curve";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalContrast 	 < string UIName="Global Contrast";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalSaturation 	 < string UIName="Global Saturation";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalVibrance 	 < string UIName="Global Vibrance";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalTemperature 	 < string UIName="Global Temperature";		string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
float	fLightroom_GlobalTint 		 < string UIName="Global Tint";			string UIWidget="Spinner";	float UIStep=0.01;	float UIMin=-1.00;	float UIMax=1.0;	> = {0.0};
#endif