/**********************************************************************
 *
 *  Device Curves
 *
 *  s-Log3, sLog3 Gamut3 Cine, sLog3 Gamut3
 *      https://pro.sony.com/bbsccms/assets/files/micro/dmpc/training/TechnicalSummary_for_S-Gamut3Cine_S-Gamut3_S-Log3_V1_01.pdf
 *  s-Log2
 *      https://pro.sony.com/bbsccms/assets/files/micro/dmpc/training/S-Log2_Technical_PaperV1_0.pdf
 *  s-Log
 *      https://pro.sony.com/bbsccms/assets/files/mkt/cinema/solutions/slog_manual.pdf
 *  Cineon
 *      https://github.com/mymei/UE4/blob/master/Engine/Shaders/PostProcessTonemap.usf
 *
 *  input struct:
 *      float3 white;
 *
 *  Function prototype:
 *      float3 TM_sLog3(       float3 linearColor, opt float3 white);
 *      float3 TM_sLog2(       float3 linearColor, opt float3 white);
 *      float3 TM_sLog(        float3 linearColor, opt float3 white);
 *      float3 TM_sGamut3Cine( float3 linearColor, opt float3 white);
 *      float3 TM_sGamut3(     float3 linearColor, opt float3 white);
 *      float3 TM_Cineon(      float3 linearColor, opt float3 white);
 *
 *  Ported to HLSL by kingeric1992 for ENBseries
 *      forum:
 *                                                  update: July.4.2017
 *
 **********************************************************************/
 
#ifndef _TM_DEVICE_FXH_
#define _TM_DEVICE_FXH_

static const float3x3 rec709_2_sGamut3_Cine = {
    0.6456794776, 0.2591145470, 0.0952059754,
    0.0875299915, 0.7596995626, 0.1527704459,
    0.0369574199, 0.1292809048, 0.8337616753 
};
    
static const float3x3 rec709_2_sGamut3 = {
    0.5660490800, 0.3427630873, 0.0911878326,
    0.0769613789, 0.7990545001, 0.1239841210,
    0.0223509133, 0.1086120512, 0.8690370355 
};

struct TM_Device_struct {
    float a, b, c, d;
};

static const TM_Device_struct TM_Device_sLog2 = {
    0.432699, 155.0/219.0, 0.037584, 0.616596
};

static const TM_Device_struct TM_Device_sLog = {
    0.432699, 1.0, 0.037584, 0.616596
};

static const TM_Device_struct TM_Device_Cineon = {
    300.0/1023.0, 1.0-0.0108, 0.0108, 685.0/1023.0
};

static const TM_Device_struct TM_Device_sLog3 = {
    261.5/1023.0, 1.0/0.19, 1.0/19.0, 420.0/1023.0
};

float3 TM_DeviceLog(float3 c, const TM_Device_struct i) {
    return i.a*log10(c*i.b+i.c)+i.d;
}

float3 TM_sLog3( float3 c ) {
    return ( c >= 0.01125000)? TM_DeviceLog(c, TM_Device_sLog3):
           ( c * ( 171.2102946929 - 95.0) + 95.0 / 0.01125000) / 1023.0;
}

float3 TM_sLog2( float3 c ) { 
    return TM_DeviceLog(c, TM_Device_sLog2);
}

float3 TM_sLog( float3 c ) {
    return TM_DeviceLog(c, TM_Device_sLog);
}

float3 TM_sGamut3Cine( float3 c ) { 
    return TM_sLog3( mul(rec709_2_sGamut3_Cine, c));
}

float3 TM_sGamut3( float3 c ) { 
    return TM_sLog3( mul(rec709_2_sGamut3, c));
}

float3 TM_Cineon( float3 c ) {
    return TM_DeviceLog(c, TM_Device_Cineon);
}


/**********************************************************************
 *
 *  Function Overload
 *
 **********************************************************************/

float3 TM_sLog3( float3 c, const float3 w ) {
    return (( c/w >= 0.01125000)? TM_DeviceLog(c, TM_Device_sLog3):
            ( c * ( 171.2102946929 - 95.0) + 95.0 / 0.01125000) / 1023.0 ) /
                                  TM_DeviceLog(w, TM_Device_sLog3);
}

float3 TM_sLog2( float3 c, const float3 w ) { 
    return TM_DeviceLog(c, TM_Device_sLog2)/TM_DeviceLog(w, TM_Device_sLog2);
}

float3 TM_sLog( float3 c, const float3 w )  {
    return TM_DeviceLog(c, TM_Device_sLog)/TM_DeviceLog(w, TM_Device_sLog);
}

float3 TM_sGamut3Cine( float3 c, const float3 w ) { 
    return TM_sLog3( mul(rec709_2_sGamut3_Cine, c), w);
}

float3 TM_sGamut3( float3 c, const float3 w ) { 
    return TM_sLog3( mul(rec709_2_sGamut3, c), w);
}

float3 TM_Cineon( float3 c, const float3 w ) {
    return TM_DeviceLog(c, TM_Device_Cineon)/TM_DeviceLog(w, TM_Device_Cineon);
}

#endif //_TM_DEVICE_FXH_