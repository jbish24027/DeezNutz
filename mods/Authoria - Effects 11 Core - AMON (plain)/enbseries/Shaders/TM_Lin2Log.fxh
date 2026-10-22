/**********************************************************************
 *
 *  Linear to Log 
 *
 *  https://github.com/mymei/UE4/blob/master/Engine/Shaders/PostProcessTonemap.usf
 *
 *  input struct:
 *      struct TM_Lin2Log_struct {
 *          float range;
 *          float grey;
 *          float exposureGrey;
 *  };
 *
 *  Function prototype:
 *      float3 res = TM_Lin2Log( float3 linearColor, 
 *                                TM_Lin2Log_struct params = TM_Lin2Log_Default);
 *
 *  Ported to HLSL by kingeric1992 for ENBseries
 *      forum:
 *                                                  update: July.4.2017
 *
 **********************************************************************/ 

#ifndef _TM_LIN2LOG_FXH_
#define _TM_LIN2LOG_FXH_ 

struct TM_Lin2Log_struct {
    float range, grey, exposureGrey;
};
 
static const TM_Lin2Log_struct TM_Lin2Log_Default = {
    14.0, 0.18, 444.0
};
 
float3 TM_Lin2Log( float3 c, const TM_Lin2Log_struct i = TM_Lin2Log_Default ) {
	return log2( c / i.grey ) / i.range + i.exposureGrey / 1023.0;
}

#endif //_TM_LIN2LOG_FXH_ 