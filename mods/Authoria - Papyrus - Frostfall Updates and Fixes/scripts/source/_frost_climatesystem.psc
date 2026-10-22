scriptname _Frost_ClimateSystem extends _Frost_BaseSystem

import CampUtil
import FrostUtil
import _FrostInternal
import Utility

Actor property PlayerRef auto

_Frost_Compatibility property Compatibility auto

GlobalVariable property GameHour auto
GlobalVariable property _Frost_CurrentTemperature auto
GlobalVariable property _Frost_CurrentWaterTemperature auto
GlobalVariable property _Frost_Setting_WeatherMessages auto
GlobalVariable property _Frost_RegionDetect_ForceUpdate auto
GlobalVariable property _Frost_Setting_DisplayTutorials auto
GlobalVariable property _Frost_HelpDone_Cold auto
GlobalVariable property FrostfallCurrentTemperatureReadOnly auto
GlobalVariable property _Frost_AttributeMeterTempLevel auto

GlobalVariable property GameMonth auto
GlobalVariable property SunriseStartHour auto
GlobalVariable property SunriseEndHour auto
GlobalVariable property SunsetStartHour auto
GlobalVariable property SunsetEndHour auto
GlobalVariable property TEMP_COLD auto 
GlobalVariable property TEMP_CHILL auto 
GlobalVariable property TEMP_BRISK auto 
GlobalVariable property TEMP_NONE auto 
GlobalVariable property TEMP_NICE auto 
GlobalVariable property TEMP_WARM auto 
GlobalVariable property TEMP_HOT auto 
GlobalVariable property REGION_CURRENTLY_IN auto
GlobalVariable property REGION_UNKNOWN_BASE_TEMP auto 
GlobalVariable property REGION_PINEFOREST_BASE_TEMP auto 
GlobalVariable property REGION_VOLCANICTUNDRA_BASE_TEMP auto 
GlobalVariable property REGION_FALLFOREST_BASE_TEMP auto 
GlobalVariable property REGION_REACH_BASE_TEMP auto 
GlobalVariable property REGION_TUNDRA_BASE_TEMP auto 
GlobalVariable property REGION_TUNDRAMARSH_BASE_TEMP auto 
GlobalVariable property REGION_COAST_BASE_TEMP auto 
GlobalVariable property REGION_SNOW_BASE_TEMP auto 
GlobalVariable property REGION_ASHWASTE_BASE_TEMP auto 
GlobalVariable Property DangerousMountainToggle Auto 

FormList property _Frost_WorldspacesExteriorPineForest auto
FormList property _Frost_WorldspacesExteriorVolcanicTundra auto
FormList property _Frost_WorldspacesExteriorFallForest auto
FormList property _Frost_WorldspacesExteriorWhiterun auto
FormList property _Frost_WorldspacesExteriorReach auto
FormList property _Frost_WorldspacesExteriorTundraMarsh auto
FormList property _Frost_WorldspacesExteriorCoast auto
FormList property _Frost_WorldspacesExteriorSnowy auto
FormList property _Frost_WorldspacesExteriorOblivion auto
FormList property _Frost_OvercastWeatherList auto

Message property _Frost_WeatherTransMsg_ClearToFog1 auto
Message property _Frost_WeatherTransMsg_ClearToFog2 auto
Message property _Frost_WeatherTransMsg_ClearToFog3 auto
Message property _Frost_WeatherTransMsg_ClearToFog4 auto
Message property _Frost_WeatherTransMsg_ClearToFog5 auto
Message property _Frost_WeatherTransMsg_ClearToFog6 auto
Message property _Frost_WeatherTransMsg_ClearToFog7 auto
Message property _Frost_WeatherTransMsg_RainToClear auto
Message property _Frost_WeatherTransMsg_StormToClear auto
Message property _Frost_WeatherTransMsg_SnowToClear auto
Message property _Frost_WeatherTransMsg_BlizzardToClear auto
Message property _Frost_WeatherTransMsg_RainToFog auto
Message property _Frost_WeatherTransMsg_ClearToRain auto
Message property _Frost_WeatherTransMsg_ClearToStorm auto
Message property _Frost_WeatherTransMsg_FogToRain auto
Message property _Frost_WeatherTransMsg_FogToStorm auto
Message property _Frost_WeatherTransMsg_SnowToRain auto
Message property _Frost_WeatherTransMsg_ClearToSnow auto
Message property _Frost_WeatherTransMsg_ClearToSnowMountain auto
Message property _Frost_WeatherTransMsg_ClearToSnowSevere auto
Message property _Frost_WeatherTransMsg_RainToSnow auto
Message property _Frost_WeatherTransMsg_RainToSnowSevere auto
Message property _Frost_CalmMsg auto
Message property _Frost_Calm2Msg auto
Message property _Frost_Help_Cold auto
Message property _Frost_Help_ColdSE auto

Worldspace property Tamriel auto
Worldspace property SolitudeWorld auto
Worldspace property WhiterunWorld auto
Worldspace property WindhelmWorld auto
Worldspace property WindhelmPitWorldspace auto

int property WEATHERCLASS_UNKNOWN           = -1    autoReadOnly
int property WEATHERCLASS_PLEASANT          = 0     autoReadOnly
int property WEATHERCLASS_CLOUDY_OR_FOGGY   = 1     autoReadOnly
int property WEATHERCLASS_RAIN              = 2     autoReadOnly
int property WEATHERCLASS_SNOW              = 3     autoReadOnly

int property REGION_UNKNOWN                 = -1    autoReadOnly
int property REGION_PINEFOREST              = 1     autoReadOnly
int property REGION_VOLCANICTUNDRA          = 2     autoReadOnly
int property REGION_FALLFOREST              = 3     autoReadOnly
int property REGION_REACH                   = 4     autoReadOnly
int property REGION_TUNDRA                  = 5     autoReadOnly
int property REGION_TUNDRAMARSH             = 6     autoReadOnly
int property REGION_COAST                   = 7     autoReadOnly
int property REGION_SNOW                    = 8     autoReadOnly
int property REGION_OBLIVION                = 9     autoReadOnly
int property REGION_FALMERVALLEY            = 10    autoReadOnly
int property REGION_SOLSTHEIM               = 11    autoReadOnly    ; no longer be used by the script, left for legacy reasons
int property REGION_ASHWASTE                = 12    autoReadOnly
int property REGION_WYRMSTOOTH              = 20    autoReadOnly    ; no longer be used by the script, left for legacy reasons
int property REGION_DARKEND                 = 21    autoReadOnly    ; no longer be used by the script, left for legacy reasons

bool first_update = true

int current_region = -1
int property currentRegion
    int function get()
        return current_region
    endFunction
    function set(int aiRegion)
        FrostDebug(1, "Now entering region " + aiRegion)
        current_region = aiRegion
    endFunction
endProperty

float pos_x
float pos_y
float pos_z
Worldspace ws
int current_max_temperature
int current_min_temperature
int last_max_temperature
int last_min_temperature
int last_region
int last_current_temperature
bool was_nighttime
bool was_twilight
bool is_nighttime
bool is_twilight
Weather last_incoming_weather
Weather last_current_weather
bool was_on_high_hrothgar_peak

float coast_minx
float coast_miny
float coast_maxx
float coast_maxy
float[] coast_polyx
float[] coast_polyy
float tundra_minx
float tundra_miny
float tundra_maxx
float tundra_maxy
float[] tundra_polyx
float[] tundra_polyy
float tundramarsh_minx
float tundramarsh_miny
float tundramarsh_maxx
float tundramarsh_maxy
float[] tundramarsh_polyx
float[] tundramarsh_polyy
float volcanictundra_minx
float volcanictundra_miny
float volcanictundra_maxx
float volcanictundra_maxy
float[] volcanictundra_polyx
float[] volcanictundra_polyy
float pineforestvolcanic_minx
float pineforestvolcanic_miny
float pineforestvolcanic_maxx
float pineforestvolcanic_maxy
float[] pineforestvolcanic_polyx
float[] pineforestvolcanic_polyy
float pineforestfalkreath_minx
float pineforestfalkreath_miny
float pineforestfalkreath_maxx
float pineforestfalkreath_maxy
float[] pineforestfalkreath_polyx
float[] pineforestfalkreath_polyy
float fallforest_minx
float fallforest_miny
float fallforest_maxx
float fallforest_maxy
float[] fallforest_polyx
float[] fallforest_polyy
float snow_minx
float snow_miny
float snow_maxx
float snow_maxy
float[] snow_polyx
float[] snow_polyy
float reach_minx
float reach_miny
float reach_maxx
float reach_maxy
float[] reach_polyx
float[] reach_polyy
float hrothgar_minx
float hrothgar_miny
float hrothgar_maxx
float hrothgar_maxy
float[] hrothgar_polyx
float[] hrothgar_polyy

; arrays to hold the base temps for each month for each region
int[] REGION_UNKNOWN_TEMPS
int[] REGION_PINEFOREST_TEMPS
int[] REGION_VOLCANICTUNDRA_TEMPS
int[] REGION_FALLFOREST_TEMPS
int[] REGION_REACH_TEMPS
int[] REGION_TUNDRA_TEMPS
int[] REGION_TUNDRAMARSH_TEMPS
int[] REGION_COAST_TEMPS
int[] REGION_SNOW_TEMPS
int[] REGION_ASHWASTE_TEMPS

; Public functions
bool function IsRaining()

endFunction

bool function IsSnowing()

endFunction

function StartUp()
    InitializeArrays()
    Compatibility.CheckIfModsAreLoaded()
endFunction

function InitializeArrays()
    tundramarsh_polyx = new float[12]
    tundramarsh_polyy = new float[12]
    tundra_polyx = new float[19]
    tundra_polyy = new float[19]
    fallforest_polyx = new float[20]
    fallforest_polyy = new float[20]
    pineforestvolcanic_polyx = new float[21]
    pineforestvolcanic_polyy = new float[21]
    pineforestfalkreath_polyx = new float[23]
    pineforestfalkreath_polyy = new float[23]
    volcanictundra_polyx = new float[24]
    volcanictundra_polyy = new float[24]
    reach_polyx = new float[33]
    reach_polyy = new float[33]
    coast_polyx = new float[40]
    coast_polyy = new float[40]
    snow_polyx = new float[56]
    snow_polyy = new float[56]
    hrothgar_polyx = new float[14]
    hrothgar_polyy = new float[14]

    REGION_UNKNOWN_TEMPS          = new int[12]
    REGION_PINEFOREST_TEMPS       = new int[12]
    REGION_VOLCANICTUNDRA_TEMPS   = new int[12]
    REGION_FALLFOREST_TEMPS       = new int[12]
    REGION_REACH_TEMPS            = new int[12]
    REGION_TUNDRA_TEMPS           = new int[12]
    REGION_TUNDRAMARSH_TEMPS      = new int[12]
    REGION_COAST_TEMPS            = new int[12]
    REGION_SNOW_TEMPS             = new int[12]
    REGION_ASHWASTE_TEMPS         = new int[12]

    ; coast
    coast_minx = -175270.000000
    coast_maxx = 195408.65625
    coast_miny = 52005.03125
    coast_maxy = 174914.296875
    coast_polyx[0] = -174782.250000
    coast_polyx[1] = -175270.000000
    coast_polyx[2] = -165759.156250
    coast_polyx[3] = -133080.906250
    coast_polyx[4] = -92111.156250
    coast_polyx[5] = -33826.863281
    coast_polyx[6] = 36650.851562
    coast_polyx[7] = 109323.375000
    coast_polyx[8] = 144440.359375
    coast_polyx[9] = 167120.046875
    coast_polyx[10] = 188336.515625
    coast_polyx[11] = 195408.656250
    coast_polyx[12] = 183703.000000
    coast_polyx[13] = 165900.656250
    coast_polyx[14] = 159316.218750
    coast_polyx[15] = 157121.406250
    coast_polyx[16] = 137368.156250
    coast_polyx[17] = 125906.375000
    coast_polyx[18] = 102007.359375
    coast_polyx[19] = 92496.523438
    coast_polyx[20] = 80303.140625
    coast_polyx[21] = 74938.062500
    coast_polyx[22] = 71523.914062
    coast_polyx[23] = 51282.914062
    coast_polyx[24] = 34622.210938
    coast_polyx[25] = 27058.289062
    coast_polyx[26] = 2790.679688
    coast_polyx[27] = -2251.929688
    coast_polyx[28] = -22107.242188
    coast_polyx[29] = -26519.523437
    coast_polyx[30] = -38810.906250
    coast_polyx[31] = -51102.265625
    coast_polyx[32] = -58351.031250
    coast_polyx[33] = -67175.609375
    coast_polyx[34] = -75369.867188
    coast_polyx[35] = -104832.445312
    coast_polyx[36] = -130019.718750
    coast_polyx[37] = -138675.531250
    coast_polyx[38] = -161404.750000
    coast_polyx[39] = -171157.734375
    
    coast_polyy[0] = 100046.921875
    coast_polyy[1] = 118824.726562
    coast_polyy[2] = 141504.421875
    coast_polyy[3] = 169549.203125
    coast_polyy[4] = 173938.812500
    coast_polyy[5] = 174914.296875
    coast_polyy[6] = 170524.687500
    coast_polyy[7] = 167110.515625
    coast_polyy[8] = 161501.593750
    coast_polyy[9] = 148820.468750
    coast_polyy[10] = 117361.546875
    coast_polyy[11] = 79318.203125
    coast_polyy[12] = 52005.031250
    coast_polyy[13] = 58589.417969
    coast_polyy[14] = 63222.906250
    coast_polyy[15] = 80537.507812
    coast_polyy[16] = 85170.992188
    coast_polyy[17] = 97852.109375
    coast_polyy[18] = 110045.492187
    coast_polyy[19] = 103948.804687
    coast_polyy[20] = 109070.023437
    coast_polyy[21] = 108338.421875
    coast_polyy[22] = 101022.390625
    coast_polyy[23] = 108826.156250
    coast_polyy[24] = 113803.140625
    coast_polyy[25] = 109706.015625
    coast_polyy[26] = 108760.515625
    coast_polyy[27] = 117269.937500
    coast_polyy[28] = 112227.328125
    coast_polyy[29] = 100566.265625
    coast_polyy[30] = 100251.101562
    coast_polyy[31] = 104663.390625
    coast_polyy[32] = 132712.968750
    coast_polyy[33] = 136179.765625
    coast_polyy[34] = 125779.359375
    coast_polyy[35] = 124424.843750
    coast_polyy[36] = 118514.054687
    coast_polyy[37] = 113835.234375
    coast_polyy[38] = 96138.687500
    coast_polyy[39] = 92357.500000
    
    ;fall forest
    fallforest_minx = 64327.582031
    fallforest_maxx = 206173.46875
    fallforest_miny = -134719.71875
    fallforest_maxy = -46029.882812
    fallforest_polyx[0] = 64327.585937
    fallforest_polyx[1] = 64327.582031
    fallforest_polyx[2] = 86507.125000
    fallforest_polyx[3] = 105849.742187
    fallforest_polyx[4] = 133961.015625
    fallforest_polyx[5] = 176772.687500
    fallforest_polyx[6] = 197662.718750
    fallforest_polyx[7] = 206173.468750
    fallforest_polyx[8] = 204368.187500
    fallforest_polyx[9] = 194567.906250
    fallforest_polyx[10] = 181005.984375
    fallforest_polyx[11] = 169027.765625
    fallforest_polyx[12] = 160396.406250
    fallforest_polyx[13] = 146656.656250
    fallforest_polyx[14] = 138377.593750
    fallforest_polyx[15] = 129922.390625
    fallforest_polyx[16] = 109540.390625
    fallforest_polyx[17] = 100240.953125
    fallforest_polyx[18] = 87913.765625
    fallforest_polyx[19] = 75370.320312
    
    fallforest_polyy[0] = -56833.308594
    fallforest_polyy[1] = -87523.625000
    fallforest_polyy[2] = -107897.867187
    fallforest_polyy[3] = -108671.609375
    fallforest_polyy[4] = -128787.976562
    fallforest_polyy[5] = -134719.718750
    fallforest_polyy[6] = -130077.484375
    fallforest_polyy[7] = -113571.773437
    fallforest_polyy[8] = -95518.648438
    fallforest_polyy[9] = -68181.062500
    fallforest_polyy[10] = -49210.347656
    fallforest_polyy[11] = -54318.710937
    fallforest_polyy[12] = -61717.023437
    fallforest_polyy[13] = -62245.476562
    fallforest_polyy[14] = -58370.164062
    fallforest_polyy[15] = -54142.558594
    fallforest_polyy[16] = -50138.945312
    fallforest_polyy[17] = -46029.882812
    fallforest_polyy[18] = -53382.941406
    fallforest_polyy[19] = -53815.472656
    
    ;tundra
    tundra_minx = -144434.625
    tundra_maxx = 85129.421875
    tundra_miny = -39139.832031
    tundra_maxy = 119573.3125
    tundra_polyx[0] = -47395.117188
    tundra_polyx[1] = -77053.171875
    tundra_polyx[2] = -99572.695312
    tundra_polyx[3] = -124630.742187
    tundra_polyx[4] = -122205.695312
    tundra_polyx[5] = -132309.750000
    tundra_polyx[6] = -144434.625000
    tundra_polyx[7] = -126247.320312
    tundra_polyx[8] = -56327.281250
    tundra_polyx[9] = -40564.953125
    tundra_polyx[10] = -63602.195312
    tundra_polyx[11] = -42585.773438
    tundra_polyx[12] = -43394.093750
    tundra_polyx[13] = -10656.953125
    tundra_polyx[14] = 32588.375000
    tundra_polyx[15] = 75833.703125
    tundra_polyx[16] = 85129.421875
    tundra_polyx[17] = 62092.187500
    tundra_polyx[18] = 28546.734375
    
    tundra_polyy[0] = -39139.832031
    tundra_polyy[1] = -32067.523437
    tundra_polyy[2] = -17033.484375
    tundra_polyy[3] = 20957.750000
    tundra_polyy[4] = 44803.320312
    tundra_polyy[5] = 67032.234375
    tundra_polyy[6] = 86432.015625
    tundra_polyy[7] = 106640.125000
    tundra_polyy[8] = 119573.312500
    tundra_polyy[9] = 106235.968750
    tundra_polyy[10] = 80369.593750
    tundra_polyy[11] = 62586.460937
    tundra_polyy[12] = 39549.214844
    tundra_polyy[13] = 32274.296875
    tundra_polyy[14] = 40357.539062
    tundra_polyy[15] = 18532.781250
    tundra_polyy[16] = -1271.167969
    tundra_polyy[17] = -24712.570312
    tundra_polyy[18] = -38858.250000
    
    
    ;tundramarsh
    tundramarsh_minx = -74266.148438
    tundramarsh_maxx = -9099.84375
    tundramarsh_miny = 59026.179687
    tundramarsh_maxy = 107806.765625
    tundramarsh_polyx[0] = -52606.828125
    tundramarsh_polyx[1] = -56938.695312
    tundramarsh_polyx[2] = -69180.921875
    tundramarsh_polyx[3] = -73889.468750
    tundramarsh_polyx[4] = -74266.148438
    tundramarsh_polyx[5] = -68615.890625
    tundramarsh_polyx[6] = -59952.167969
    tundramarsh_polyx[7] = -49405.023438
    tundramarsh_polyx[8] = -22283.789062
    tundramarsh_polyx[9] = -9099.843750
    tundramarsh_polyx[10] = -17951.921875
    tundramarsh_polyx[11] = -46579.898438
    
    tundramarsh_polyy[0] = 101591.468750
    tundramarsh_polyy[1] = 93681.109375
    tundramarsh_polyy[2] = 89725.921875
    tundramarsh_polyy[3] = 85959.085938
    tundramarsh_polyy[4] = 81815.562500
    tundramarsh_polyy[5] = 71268.406250
    tundramarsh_polyy[6] = 67124.882812
    tundramarsh_polyy[7] = 59026.179687
    tundramarsh_polyy[8] = 61286.285156
    tundramarsh_polyy[9] = 75788.617188
    tundramarsh_polyy[10] = 100838.109375
    tundramarsh_polyy[11] = 107806.765625
    
    ;volcanictundra
    volcanictundra_minx = 101112.1875
    volcanictundra_maxx = 160618.234375
    volcanictundra_miny = -37752.507812
    volcanictundra_maxy = 23902.558594
    volcanictundra_polyx[0] = 119000.125000
    volcanictundra_polyx[1] = 109382.218750
    volcanictundra_polyx[2] = 109382.218750
    volcanictundra_polyx[3] = 101324.234375
    volcanictundra_polyx[4] = 101112.187500
    volcanictundra_polyx[5] = 105565.265625
    volcanictundra_polyx[6] = 105493.648437
    volcanictundra_polyx[7] = 111289.703125
    volcanictundra_polyx[8] = 119488.359375
    volcanictundra_polyx[9] = 122904.453125
    volcanictundra_polyx[10] = 131786.312500
    volcanictundra_polyx[11] = 139438.406250
    volcanictundra_polyx[12] = 143947.671875
    volcanictundra_polyx[13] = 155835.687500
    volcanictundra_polyx[14] = 160618.234375
    volcanictundra_polyx[15] = 160481.593750
    volcanictundra_polyx[16] = 156245.625000
    volcanictundra_polyx[17] = 153512.734375
    volcanictundra_polyx[18] = 152282.937500
    volcanictundra_polyx[19] = 148183.609375
    volcanictundra_polyx[20] = 142034.625000
    volcanictundra_polyx[21] = 137525.375000
    volcanictundra_polyx[22] = 135612.359375
    volcanictundra_polyx[23] = 128732.359375
    
    volcanictundra_polyy[0] = 15282.574219
    volcanictundra_polyy[1] = 755.703125
    volcanictundra_polyy[2] = -6029.964844
    volcanictundra_polyy[3] = -7726.382812
    volcanictundra_polyy[4] = -15572.308594
    volcanictundra_polyy[5] = -21509.769531
    volcanictundra_polyy[6] = -33081.843750
    volcanictundra_polyy[7] = -33379.898437
    volcanictundra_polyy[8] = -33516.539062
    volcanictundra_polyy[9] = -37752.507812
    volcanictundra_polyy[10] = -37615.867188
    volcanictundra_polyy[11] = -33516.546875
    volcanictundra_polyy[12] = -33516.550781
    volcanictundra_polyy[13] = -29280.578125
    volcanictundra_polyy[14] = -24907.964844
    volcanictundra_polyy[15] = -15616.164062
    volcanictundra_polyy[16] = -11380.195312
    volcanictundra_polyy[17] = -9057.244141
    volcanictundra_polyy[18] = -3181.546875
    volcanictundra_polyy[19] = 5153.748047
    volcanictundra_polyy[20] = 10619.515625
    volcanictundra_polyy[21] = 15128.773437
    volcanictundra_polyy[22] = 21414.402344
    volcanictundra_polyy[23] = 23902.558594
    
    ;pineforestvolcanic
    pineforestvolcanic_minx = -16809.402344
    pineforestvolcanic_maxx = 182398.71875
    pineforestvolcanic_miny = -66468.242187
    pineforestvolcanic_maxy = 22512.25
    pineforestvolcanic_polyx[0] = 77366.929688
    pineforestvolcanic_polyx[1] = 72979.750000
    pineforestvolcanic_polyx[2] = 66724.117187
    pineforestvolcanic_polyx[3] = 67002.187500
    pineforestvolcanic_polyx[4] = 84798.281250
    pineforestvolcanic_polyx[5] = 102038.250000
    pineforestvolcanic_polyx[6] = 119000.140625
    pineforestvolcanic_polyx[7] = 144860.078125
    pineforestvolcanic_polyx[8] = 167105.187500
    pineforestvolcanic_polyx[9] = 182398.718750
    pineforestvolcanic_polyx[10] = 176837.421875
    pineforestvolcanic_polyx[11] = 166270.984375
    pineforestvolcanic_polyx[12] = 154314.250000
    pineforestvolcanic_polyx[13] = 147084.593750
    pineforestvolcanic_polyx[14] = 140967.171875
    pineforestvolcanic_polyx[15] = 130400.750000
    pineforestvolcanic_polyx[16] = 119278.203125
    pineforestvolcanic_polyx[17] = 105653.062500
    pineforestvolcanic_polyx[18] = 96476.953125
    pineforestvolcanic_polyx[19] = 87578.914062
    pineforestvolcanic_polyx[20] = -16809.402344
    
    pineforestvolcanic_polyy[0] = 760.457031
    pineforestvolcanic_polyy[1] = -3626.726562
    pineforestvolcanic_polyy[2] = -27817.378906
    pineforestvolcanic_polyy[3] = -58682.445312
    pineforestvolcanic_polyy[4] = -58404.382812
    pineforestvolcanic_polyy[5] = -53955.359375
    pineforestvolcanic_polyy[6] = -57014.062500
    pineforestvolcanic_polyy[7] = -66468.242187
    pineforestvolcanic_polyy[8] = -65355.984375
    pineforestvolcanic_polyy[9] = -52008.910156
    pineforestvolcanic_polyy[10] = -13636.117187
    pineforestvolcanic_polyy[11] = 4716.101562
    pineforestvolcanic_polyy[12] = 18063.179688
    pineforestvolcanic_polyy[13] = 18341.296875
    pineforestvolcanic_polyy[14] = 21956.125000
    pineforestvolcanic_polyy[15] = 22512.250000
    pineforestvolcanic_polyy[16] = 21956.125000
    pineforestvolcanic_polyy[17] = 13058.078125
    pineforestvolcanic_polyy[18] = 7774.863281
    pineforestvolcanic_polyy[19] = 6662.609375
    pineforestvolcanic_polyy[20] = -39490.996094
    
    ;pineforestfalkreath
    pineforestfalkreath_minx = -92197.570312
    pineforestfalkreath_maxx = 39772.664062
    pineforestfalkreath_miny = -107699.335937
    pineforestfalkreath_maxy = -24093.414062
    pineforestfalkreath_polyx[0] = -44976.421875
    pineforestfalkreath_polyx[1] = -73143.421875
    pineforestfalkreath_polyx[2] = -92197.570312
    pineforestfalkreath_polyx[3] = -79218.640625
    pineforestfalkreath_polyx[4] = -66792.023437
    pineforestfalkreath_polyx[5] = -35587.398438
    pineforestfalkreath_polyx[6] = -12114.898438
    pineforestfalkreath_polyx[7] = 22858.292969
    pineforestfalkreath_polyx[8] = 38787.363281
    pineforestfalkreath_polyx[9] = 39772.664062
    pineforestfalkreath_polyx[10] = 33172.605469
    pineforestfalkreath_polyx[11] = 33172.605469
    pineforestfalkreath_polyx[12] = 33172.605469
    pineforestfalkreath_polyx[13] = 37209.996094
    pineforestfalkreath_polyx[14] = 37447.488281
    pineforestfalkreath_polyx[15] = 33053.859375
    pineforestfalkreath_polyx[16] = 33172.605469
    pineforestfalkreath_polyx[17] = 19872.960938
    pineforestfalkreath_polyx[18] = 19872.960938
    pineforestfalkreath_polyx[19] = 19872.960938
    pineforestfalkreath_polyx[20] = 15835.570312
    pineforestfalkreath_polyx[21] = 15835.570312
    pineforestfalkreath_polyx[22] = 1467.205078
    
    pineforestfalkreath_polyy[0] = -36177.234375
    pineforestfalkreath_polyy[1] = -32311.171875
    pineforestfalkreath_polyy[2] = -43909.351562
    pineforestfalkreath_polyy[3] = -91958.953125
    pineforestfalkreath_polyy[4] = -104385.570312
    pineforestfalkreath_polyy[5] = -107699.335937
    pineforestfalkreath_polyy[6] = -95825.000000
    pineforestfalkreath_polyy[7] = -91726.898438
    pineforestfalkreath_polyy[8] = -71363.960938
    pineforestfalkreath_polyy[9] = -48373.468750
    pineforestfalkreath_polyy[10] = -38105.546875
    pineforestfalkreath_polyy[11] = -35849.355469
    pineforestfalkreath_polyy[12] = -33118.175781
    pineforestfalkreath_polyy[13] = -33118.175781
    pineforestfalkreath_polyy[14] = -27893.312500
    pineforestfalkreath_polyy[15] = -27893.312500
    pineforestfalkreath_polyy[16] = -24093.414062
    pineforestfalkreath_polyy[17] = -24093.414062
    pineforestfalkreath_polyy[18] = -25755.871094
    pineforestfalkreath_polyy[19] = -28130.806641
    pineforestfalkreath_polyy[20] = -28130.806641
    pineforestfalkreath_polyy[21] = -40361.738281
    pineforestfalkreath_polyy[22] = -40480.484375
    
    ;snow
    snow_minx = -58683.9375
    snow_maxx = 216672.0625
    snow_miny = -108435.3125
    snow_maxy = 116478.695312
    snow_polyx[0] = 202739.187500
    snow_polyx[1] = 198078.375000
    snow_polyx[2] = 189999.609375
    snow_polyx[3] = 184406.593750
    snow_polyx[4] = 180481.015625
    snow_polyx[5] = 178962.500000
    snow_polyx[6] = 174913.156250
    snow_polyx[7] = 170610.718750
    snow_polyx[8] = 162005.843750
    snow_polyx[9] = 148845.437500
    snow_polyx[10] = 135938.125000
    snow_polyx[11] = 123790.062500
    snow_polyx[12] = 112401.265625
    snow_polyx[13] = 108098.820312
    snow_polyx[14] = 95950.757812
    snow_polyx[15] = 78741.015625
    snow_polyx[16] = 72160.812500
    snow_polyx[17] = 62543.601562
    snow_polyx[18] = 53938.722656
    snow_polyx[19] = 46599.269531
    snow_polyx[20] = 34451.207031
    snow_polyx[21] = 22050.070312
    snow_polyx[22] = 5346.484375
    snow_polyx[23] = -14394.113281
    snow_polyx[24] = -31350.783203
    snow_polyx[25] = -36665.570312
    snow_polyx[26] = -40461.843750
    snow_polyx[27] = -58683.937500
    snow_polyx[28] = -48307.468750
    snow_polyx[29] = -51850.648437
    snow_polyx[30] = -42992.687500
    snow_polyx[31] = -38437.164062
    snow_polyx[32] = -23505.171875
    snow_polyx[33] = -18696.562500
    snow_polyx[34] = -11610.195312
    snow_polyx[35] = -14394.140625
    snow_polyx[36] = -20215.085938
    snow_polyx[37] = -25529.859375
    snow_polyx[38] = -16924.984375
    snow_polyx[39] = -3005.328125
    snow_polyx[40] = 4334.117188
    snow_polyx[41] = 29895.671875
    snow_polyx[42] = 45080.742188
    snow_polyx[43] = 58747.304687
    snow_polyx[44] = 74185.460938
    snow_polyx[45] = 92913.726562
    snow_polyx[46] = 117209.843750
    snow_polyx[47] = 137962.781250
    snow_polyx[48] = 158462.656250
    snow_polyx[49] = 161246.578125
    snow_polyx[50] = 174660.062500
    snow_polyx[51] = 182505.671875
    snow_polyx[52] = 207814.125000
    snow_polyx[53] = 208573.375000
    snow_polyx[54] = 216672.062500
    snow_polyx[55] = 215912.781250
    
    snow_polyy[0] = -108435.312500
    snow_polyy[1] = -87927.671875
    snow_polyy[2] = -75809.531250
    snow_polyy[3] = -59030.636719
    snow_polyy[4] = -56125.140625
    snow_polyy[5] = -46254.832031
    snow_polyy[6] = -43217.816406
    snow_polyy[7] = -16643.914062
    snow_polyy[8] = -1205.734375
    snow_polyy[9] = 14232.441406
    snow_polyy[10] = 15750.949219
    snow_polyy[11] = 18028.714844
    snow_polyy[12] = 10183.085938
    snow_polyy[13] = 5627.558594
    snow_polyy[14] = 312.777344
    snow_polyy[15] = 4868.304688
    snow_polyy[16] = 11195.425781
    snow_polyy[17] = 13220.105469
    snow_polyy[18] = 17269.460938
    snow_polyy[19] = 30176.785156
    snow_polyy[20] = 33973.058594
    snow_polyy[21] = 30176.785156
    snow_polyy[22] = 29923.699219
    snow_polyy[23] = 26886.683594
    snow_polyy[24] = 29923.699219
    snow_polyy[25] = 32960.718750
    snow_polyy[26] = 29417.531250
    snow_polyy[27] = 33719.972656
    snow_polyy[28] = 47386.558594
    snow_polyy[29] = 59534.621094
    snow_polyy[30] = 67380.250000
    snow_polyy[31] = 62571.644531
    snow_polyy[32] = 62571.644531
    snow_polyy[33] = 70923.437500
    snow_polyy[34] = 73201.203125
    snow_polyy[35] = 83577.671875
    snow_polyy[36] = 88386.281250
    snow_polyy[37] = 108379.984375
    snow_polyy[38] = 115972.531250
    snow_polyy[39] = 116478.695312
    snow_polyy[40] = 110151.578125
    snow_polyy[41] = 109392.328125
    snow_polyy[42] = 113441.671875
    snow_polyy[43] = 106102.210937
    snow_polyy[44] = 106102.210937
    snow_polyy[45] = 109645.406250
    snow_polyy[46] = 105849.132812
    snow_polyy[47] = 88386.281250
    snow_polyy[48] = 80540.648438
    snow_polyy[49] = 65608.648437
    snow_polyy[50] = 57509.933594
    snow_polyy[51] = 49917.375000
    snow_polyy[52] = -1458.845703
    snow_polyy[53] = -43724.007812
    snow_polyy[54] = -61946.109375
    snow_polyy[55] = -104970.531250
    
    ;reach
    reach_minx = -192608.6875
    reach_maxx = -71618.109375
    reach_miny = -59062.210937
    reach_maxy = 89516.859375
    reach_polyx[0] = -179900.562500
    reach_polyx[1] = -183180.093750
    reach_polyx[2] = -192608.687500
    reach_polyx[3] = -185116.718750
    reach_polyx[4] = -119254.226562
    reach_polyx[5] = -89177.406250
    reach_polyx[6] = -86743.445312
    reach_polyx[7] = -77007.593750
    reach_polyx[8] = -71618.109375
    reach_polyx[9] = -77355.304688
    reach_polyx[10] = -81527.812500
    reach_polyx[11] = -89351.242188
    reach_polyx[12] = -97522.406250
    reach_polyx[13] = -105519.726562
    reach_polyx[14] = -108649.132812
    reach_polyx[15] = -111430.796875
    reach_polyx[16] = -116298.695312
    reach_polyx[17] = -118037.242187
    reach_polyx[18] = -113690.875000
    reach_polyx[19] = -106215.140625
    reach_polyx[20] = -105801.609375
    reach_polyx[21] = -112092.703125
    reach_polyx[22] = -116811.015625
    reach_polyx[23] = -117709.750000
    reach_polyx[24] = -112766.750000
    reach_polyx[25] = -102431.382812
    reach_polyx[26] = -104228.835937
    reach_polyx[27] = -111643.335937
    reach_polyx[28] = -119956.562500
    reach_polyx[29] = -128943.828125
    reach_polyx[30] = -137032.375000
    reach_polyx[31] = -140627.281250
    reach_polyx[32] = -154557.546875
    
    reach_polyy[0] = 52700.894531
    reach_polyy[1] = 13756.593750
    reach_polyy[2] = -23957.882812
    reach_polyy[3] = -42954.066406
    reach_polyy[4] = -59062.210937
    reach_polyy[5] = -53151.156250
    reach_polyy[6] = -44284.578125
    reach_polyy[7] = -39242.796875
    reach_polyy[8] = -32114.759766
    reach_polyy[9] = -23769.748047
    reach_polyy[10] = -19771.093750
    reach_polyy[11] = -15424.737305
    reach_polyy[12] = -7253.576172
    reach_polyy[13] = 917.587891
    reach_polyy[14] = 5090.094727
    reach_polyy[15] = 11696.566406
    reach_polyy[16] = 19867.730469
    reach_polyy[17] = 31689.837891
    reach_polyy[18] = 36036.199219
    reach_polyy[19] = 38296.308594
    reach_polyy[20] = 48400.078125
    reach_polyy[21] = 52669.039062
    reach_polyy[22] = 54691.175781
    reach_polyy[23] = 60757.585937
    reach_polyy[24] = 67947.406250
    reach_polyy[25] = 70418.906250
    reach_polyy[26] = 78732.132812
    reach_polyy[27] = 81203.640625
    reach_polyy[28] = 78956.812500
    reach_polyy[29] = 71317.632812
    reach_polyy[30] = 75811.265625
    reach_polyy[31] = 89516.859375
    reach_polyy[32] = 87045.359375

    hrothgar_minx = 26624.000000
    hrothgar_maxx = 73731.000000
    hrothgar_miny = -79871.000000
    hrothgar_maxy = -20479.000000

    hrothgar_polyx[0] = 38910.00
    hrothgar_polyx[1] = 26625.00
    hrothgar_polyx[2] = 32800.00
    hrothgar_polyx[3] = 36865.00
    hrothgar_polyx[4] = 49150.00
    hrothgar_polyx[5] = 57345.00
    hrothgar_polyx[6] = 69630.00
    hrothgar_polyx[7] = 69630.00
    hrothgar_polyx[8] = 73730.00
    hrothgar_polyx[9] = 69630.00
    hrothgar_polyx[10] = 65535.00
    hrothgar_polyx[11] = 57345.00
    hrothgar_polyx[12] = 53250.00
    hrothgar_polyx[13] = 49150.00
    
    hrothgar_polyy[0] = -20480.00
    hrothgar_polyy[1] = -53250.00
    hrothgar_polyy[2] = -69630.00
    hrothgar_polyy[3] = -69630.00
    hrothgar_polyy[4] = -79870.00
    hrothgar_polyy[5] = -77825.00
    hrothgar_polyy[6] = -69630.00
    hrothgar_polyy[7] = -61440.00
    hrothgar_polyy[8] = -57345.00
    hrothgar_polyy[9] = -24575.00
    hrothgar_polyy[10] = -20480.00
    hrothgar_polyy[11] = -20480.00
    hrothgar_polyy[12] = -24575.00
    hrothgar_polyy[13] = -20480.00
    
endFunction

function Update()
    UpdateClimateState()
endFunction

function RegisterForEvents()
    FallbackEventEmitter emitter = GetEventEmitter_OnTamrielRegionChange()
    emitter.RegisterFormForModEventWithFallback("Frost_OnTamrielRegionChange", "OnTamrielRegionChange", self as Form)

    ; Force the region detect system to fire something on start-up.
    _Frost_RegionDetect_ForceUpdate.SetValueInt(0)
endFunction

int function UpdateCurrentRegion(float playerX, float playerY)
    if ws == Tamriel
        bool inTundraMarsh = IsPointInPolygonFast(tundramarsh_polyx, tundramarsh_polyy, tundramarsh_minx, tundramarsh_maxx, tundramarsh_miny, tundramarsh_maxy, playerX, playerY)
        bool inTundra = IsPointInPolygonFast(tundra_polyx, tundra_polyy, tundra_minx, tundra_maxx, tundra_miny, tundra_maxy, playerX, playerY)
        bool inFallForest = IsPointInPolygonFast(fallforest_polyx, fallforest_polyy, fallforest_minx, fallforest_maxx, fallforest_miny, fallforest_maxy, playerX, playerY)
        bool inVolcanicTundra = IsPointInPolygonFast(volcanictundra_polyx, volcanictundra_polyy, volcanictundra_minx, volcanictundra_maxx, volcanictundra_miny, volcanictundra_maxy, playerX, playerY)
        bool inPineForestVolcanic = IsPointInPolygonFast(pineforestvolcanic_polyx, pineforestvolcanic_polyy, pineforestvolcanic_minx, pineforestvolcanic_maxx, pineforestvolcanic_miny, pineforestvolcanic_maxy, playerX, playerY)
        bool inPineForestFalkreath = IsPointInPolygonFast(pineforestfalkreath_polyx, pineforestfalkreath_polyy, pineforestfalkreath_minx, pineforestfalkreath_maxx, pineforestfalkreath_miny, pineforestfalkreath_maxy, playerX, playerY)
        bool inPineForest = inPineForestVolcanic || inPineForestFalkreath
        bool inReach = IsPointInPolygonFast(reach_polyx, reach_polyy, reach_minx, reach_maxx, reach_miny, reach_maxy, playerX, playerY)
        bool inCoast = IsPointInPolygonFast(coast_polyx, coast_polyy, coast_minx, coast_maxx, coast_miny, coast_maxy, playerX, playerY)
        bool inSnow = IsPointInPolygonFast(snow_polyx, snow_polyy, snow_minx, snow_maxx, snow_miny, snow_maxy, playerX, playerY)
        bool inHrothgar = IsPointInPolygonFast(hrothgar_polyx, hrothgar_polyy, hrothgar_minx, hrothgar_maxx, hrothgar_miny, hrothgar_maxy, playerX, playerY)
        
        if inHrothgar && !inPineForest && !inTundra && !inFallForest
            return REGION_SNOW  ; treat the throat of the world mountain area as snow / arctic
        endif
        
        if inPineForest && !inVolcanicTundra
            return REGION_PINEFOREST
        endif

        if inVolcanicTundra && !inSnow
            return REGION_VOLCANICTUNDRA
        endif

        if inFallForest && !inPineForest && !inVolcanicTundra
            return REGION_FALLFOREST
        endif

        if inReach && !inTundraMarsh
            return REGION_REACH
        endif

        if inTundra && !inTundraMarsh && !inPineForest && !inCoast
            return REGION_TUNDRA
        endif

        if inTundraMarsh && !inCoast
            return REGION_TUNDRAMARSH
        endif

        if inCoast
            return REGION_COAST
        endif

        if inSnow && !inCoast && !inTundra && !inTundraMarsh
            return REGION_SNOW
        endif
        
        return REGION_UNKNOWN
    else
        if _Frost_WorldspacesExteriorPineForest.HasForm(ws)
            return REGION_PINEFOREST
        elseif _Frost_WorldspacesExteriorVolcanicTundra.HasForm(ws)
            return REGION_VOLCANICTUNDRA
        elseif _Frost_WorldspacesExteriorFallForest.HasForm(ws)
            return REGION_FALLFOREST
        elseif _Frost_WorldspacesExteriorWhiterun.HasForm(ws)
            return REGION_TUNDRA
        elseif _Frost_WorldspacesExteriorTundraMarsh.HasForm(ws)
            return REGION_TUNDRAMARSH
        elseif _Frost_WorldspacesExteriorReach.HasForm(ws)
            return REGION_REACH
        elseif _Frost_WorldspacesExteriorCoast.HasForm(ws)
            return REGION_COAST
        elseif _Frost_WorldspacesExteriorSnowy.HasForm(ws)
            return REGION_SNOW
        elseif _Frost_WorldspacesExteriorOblivion.HasForm(ws)
            return REGION_OBLIVION
        elseif Compatibility.isDLC1Loaded && ws == Compatibility.WS_FalmerValley
            return Compatibility.GetPlayerRegionTemp_FalmerValley(pos_x, pos_y)
        elseif Compatibility.isDLC2Loaded && ws == Compatibility.WS_Solstheim
            return Compatibility.GetPlayerRegionTemp_Solstheim(pos_x, pos_y)
        elseif Compatibility.WyrmstoothPresent && ws == Compatibility.WS_Wyrmstooth
            return Compatibility.GetPlayerRegionTemp_Wyrmstooth(pos_x, pos_y)
        elseif Compatibility.DarkendPresent && ws == Compatibility.WS_Darkend
            return Compatibility.GetPlayerRegionTemp_Darkend(pos_x, pos_y)
        else
            return REGION_UNKNOWN
        endif
    endif
endFunction


Function SetCurrentBiomeAndMonthlyValues()
    ; get the monthly variances in temperature
    int cold_month  = (TEMP_COLD.GetValue() as int)
    int chill_month = (TEMP_CHILL.GetValue() as int)
    int brisk_month = (TEMP_BRISK.GetValue() as int)
    int basic_month = (TEMP_NONE.GetValue() as int)
    int nice_month  = (TEMP_NICE.GetValue() as int)
    int warm_month  = (TEMP_WARM.GetValue() as int)
    int hot_month   = (TEMP_HOT.GetValue() as int)
    
    ; get the annual average temperature for each region
    int unknown_base_temp        = (REGION_UNKNOWN_BASE_TEMP.GetValue() as int)
    int pineforest_base_temp     = (REGION_PINEFOREST_BASE_TEMP.GetValue() as int)
    int volcanictundra_base_temp = (REGION_VOLCANICTUNDRA_BASE_TEMP.GetValue() as int)
    int fallforest_base_temp     = (REGION_FALLFOREST_BASE_TEMP.GetValue() as int)
    int reach_base_temp          = (REGION_REACH_BASE_TEMP.GetValue() as int)
    int tundrasteppe_base_temp   = (REGION_TUNDRA_BASE_TEMP.GetValue() as int)
    int tundramarsh_base_temp    = (REGION_TUNDRAMARSH_BASE_TEMP.GetValue() as int)
    int northcoast_base_temp     = (REGION_COAST_BASE_TEMP.GetValue() as int)
    int arcticsnow_base_temp     = (REGION_SNOW_BASE_TEMP.GetValue() as int)
    int ashwaste_base_temp       = (REGION_ASHWASTE_BASE_TEMP.GetValue() as int)

    ; now determine the monthly adjustments for each region
    
    ; for unknown regions
    REGION_UNKNOWN_TEMPS         [0]  = (unknown_base_temp + cold_month)
    REGION_UNKNOWN_TEMPS         [1]  = (unknown_base_temp + chill_month)
    REGION_UNKNOWN_TEMPS         [2]  = (unknown_base_temp + brisk_month)
    REGION_UNKNOWN_TEMPS         [3]  = (unknown_base_temp + basic_month)
    REGION_UNKNOWN_TEMPS         [4]  = (unknown_base_temp + nice_month)
    REGION_UNKNOWN_TEMPS         [5]  = (unknown_base_temp + warm_month)
    REGION_UNKNOWN_TEMPS         [6]  = (unknown_base_temp + hot_month)
    REGION_UNKNOWN_TEMPS         [7]  = (unknown_base_temp + warm_month)
    REGION_UNKNOWN_TEMPS         [8]  = (unknown_base_temp + nice_month)
    REGION_UNKNOWN_TEMPS         [9]  = (unknown_base_temp + basic_month)
    REGION_UNKNOWN_TEMPS         [10] = (unknown_base_temp + brisk_month)
    REGION_UNKNOWN_TEMPS         [11] = (unknown_base_temp + chill_month)
    
    ; for pine forest regions
    REGION_PINEFOREST_TEMPS      [0]  = (pineforest_base_temp + cold_month)
    REGION_PINEFOREST_TEMPS      [1]  = (pineforest_base_temp + chill_month)
    REGION_PINEFOREST_TEMPS      [2]  = (pineforest_base_temp + brisk_month)
    REGION_PINEFOREST_TEMPS      [3]  = (pineforest_base_temp + basic_month)
    REGION_PINEFOREST_TEMPS      [4]  = (pineforest_base_temp + nice_month)
    REGION_PINEFOREST_TEMPS      [5]  = (pineforest_base_temp + warm_month)
    REGION_PINEFOREST_TEMPS      [6]  = (pineforest_base_temp + hot_month)
    REGION_PINEFOREST_TEMPS      [7]  = (pineforest_base_temp + warm_month)
    REGION_PINEFOREST_TEMPS      [8]  = (pineforest_base_temp + nice_month)
    REGION_PINEFOREST_TEMPS      [9]  = (pineforest_base_temp + basic_month)
    REGION_PINEFOREST_TEMPS      [10] = (pineforest_base_temp + brisk_month)
    REGION_PINEFOREST_TEMPS      [11] = (pineforest_base_temp + chill_month)

    ; for volcanic tundra regions, where local hot springs and mudflats heat the otherwise chilly air
    REGION_VOLCANICTUNDRA_TEMPS  [0]  = (volcanictundra_base_temp + cold_month)
    REGION_VOLCANICTUNDRA_TEMPS  [1]  = (volcanictundra_base_temp + chill_month)
    REGION_VOLCANICTUNDRA_TEMPS  [2]  = (volcanictundra_base_temp + brisk_month)
    REGION_VOLCANICTUNDRA_TEMPS  [3]  = (volcanictundra_base_temp + basic_month)
    REGION_VOLCANICTUNDRA_TEMPS  [4]  = (volcanictundra_base_temp + nice_month)
    REGION_VOLCANICTUNDRA_TEMPS  [5]  = (volcanictundra_base_temp + warm_month)
    REGION_VOLCANICTUNDRA_TEMPS  [6]  = (volcanictundra_base_temp + hot_month)
    REGION_VOLCANICTUNDRA_TEMPS  [7]  = (volcanictundra_base_temp + warm_month)
    REGION_VOLCANICTUNDRA_TEMPS  [8]  = (volcanictundra_base_temp + nice_month)
    REGION_VOLCANICTUNDRA_TEMPS  [9]  = (volcanictundra_base_temp + basic_month)
    REGION_VOLCANICTUNDRA_TEMPS  [10] = (volcanictundra_base_temp + brisk_month)
    REGION_VOLCANICTUNDRA_TEMPS  [11] = (volcanictundra_base_temp + chill_month)
    
    ; for desciduous / fall forest regions
    REGION_FALLFOREST_TEMPS      [0]  = (fallforest_base_temp + cold_month)
    REGION_FALLFOREST_TEMPS      [1]  = (fallforest_base_temp + chill_month)
    REGION_FALLFOREST_TEMPS      [2]  = (fallforest_base_temp + brisk_month)
    REGION_FALLFOREST_TEMPS      [3]  = (fallforest_base_temp + basic_month)
    REGION_FALLFOREST_TEMPS      [4]  = (fallforest_base_temp + nice_month)
    REGION_FALLFOREST_TEMPS      [5]  = (fallforest_base_temp + warm_month)
    REGION_FALLFOREST_TEMPS      [6]  = (fallforest_base_temp + hot_month)
    REGION_FALLFOREST_TEMPS      [7]  = (fallforest_base_temp + warm_month)
    REGION_FALLFOREST_TEMPS      [8]  = (fallforest_base_temp + nice_month)
    REGION_FALLFOREST_TEMPS      [9]  = (fallforest_base_temp + basic_month)
    REGION_FALLFOREST_TEMPS      [10] = (fallforest_base_temp + brisk_month)
    REGION_FALLFOREST_TEMPS      [11] = (fallforest_base_temp + chill_month)
    
    ; for the reach and chilly canyon regions, where trees and canyon walls at least offer some cover from the wind
    REGION_REACH_TEMPS           [0]  = (reach_base_temp + cold_month)
    REGION_REACH_TEMPS           [1]  = (reach_base_temp + chill_month)
    REGION_REACH_TEMPS           [2]  = (reach_base_temp + brisk_month)
    REGION_REACH_TEMPS           [3]  = (reach_base_temp + basic_month)
    REGION_REACH_TEMPS           [4]  = (reach_base_temp + nice_month)
    REGION_REACH_TEMPS           [5]  = (reach_base_temp + warm_month)
    REGION_REACH_TEMPS           [6]  = (reach_base_temp + hot_month)
    REGION_REACH_TEMPS           [7]  = (reach_base_temp + warm_month)
    REGION_REACH_TEMPS           [8]  = (reach_base_temp + nice_month)
    REGION_REACH_TEMPS           [9]  = (reach_base_temp + basic_month)
    REGION_REACH_TEMPS           [10] = (reach_base_temp + brisk_month)
    REGION_REACH_TEMPS           [11] = (reach_base_temp + chill_month)
    
    ; for tundra / steppe regions - where there is no cover to shield the north wind from chilling you
    REGION_TUNDRA_TEMPS          [0]  = (tundrasteppe_base_temp + cold_month)
    REGION_TUNDRA_TEMPS          [1]  = (tundrasteppe_base_temp + chill_month)
    REGION_TUNDRA_TEMPS          [2]  = (tundrasteppe_base_temp + brisk_month)
    REGION_TUNDRA_TEMPS          [3]  = (tundrasteppe_base_temp + basic_month)
    REGION_TUNDRA_TEMPS          [4]  = (tundrasteppe_base_temp + nice_month)
    REGION_TUNDRA_TEMPS          [5]  = (tundrasteppe_base_temp + warm_month)
    REGION_TUNDRA_TEMPS          [6]  = (tundrasteppe_base_temp + hot_month)
    REGION_TUNDRA_TEMPS          [7]  = (tundrasteppe_base_temp + warm_month)
    REGION_TUNDRA_TEMPS          [8]  = (tundrasteppe_base_temp + nice_month)
    REGION_TUNDRA_TEMPS          [9]  = (tundrasteppe_base_temp + basic_month)
    REGION_TUNDRA_TEMPS          [10] = (tundrasteppe_base_temp + brisk_month)
    REGION_TUNDRA_TEMPS          [11] = (tundrasteppe_base_temp + chill_month)
    
    ; for marshy tundra regions - humid and cold even in summer
    REGION_TUNDRAMARSH_TEMPS     [0]  = (tundramarsh_base_temp + cold_month)
    REGION_TUNDRAMARSH_TEMPS     [1]  = (tundramarsh_base_temp + chill_month)
    REGION_TUNDRAMARSH_TEMPS     [2]  = (tundramarsh_base_temp + brisk_month)
    REGION_TUNDRAMARSH_TEMPS     [3]  = (tundramarsh_base_temp + basic_month)
    REGION_TUNDRAMARSH_TEMPS     [4]  = (tundramarsh_base_temp + nice_month)
    REGION_TUNDRAMARSH_TEMPS     [5]  = (tundramarsh_base_temp + warm_month)
    REGION_TUNDRAMARSH_TEMPS     [6]  = (tundramarsh_base_temp + hot_month)
    REGION_TUNDRAMARSH_TEMPS     [7]  = (tundramarsh_base_temp + warm_month)
    REGION_TUNDRAMARSH_TEMPS     [8]  = (tundramarsh_base_temp + nice_month)
    REGION_TUNDRAMARSH_TEMPS     [9]  = (tundramarsh_base_temp + basic_month)
    REGION_TUNDRAMARSH_TEMPS     [10] = (tundramarsh_base_temp + brisk_month)
    REGION_TUNDRAMARSH_TEMPS     [11] = (tundramarsh_base_temp + chill_month)
    
    ; for northern coastal regions, true tundra adjacent to glaciers
    REGION_COAST_TEMPS           [0]  = (northcoast_base_temp + cold_month)
    REGION_COAST_TEMPS           [1]  = (northcoast_base_temp + chill_month)
    REGION_COAST_TEMPS           [2]  = (northcoast_base_temp + brisk_month)
    REGION_COAST_TEMPS           [3]  = (northcoast_base_temp + basic_month)
    REGION_COAST_TEMPS           [4]  = (northcoast_base_temp + nice_month)
    REGION_COAST_TEMPS           [5]  = (northcoast_base_temp + warm_month)
    REGION_COAST_TEMPS           [6]  = (northcoast_base_temp + hot_month)
    REGION_COAST_TEMPS           [7]  = (northcoast_base_temp + warm_month)
    REGION_COAST_TEMPS           [8]  = (northcoast_base_temp + nice_month)
    REGION_COAST_TEMPS           [9]  = (northcoast_base_temp + basic_month)
    REGION_COAST_TEMPS           [10] = (northcoast_base_temp + brisk_month)
    REGION_COAST_TEMPS           [11] = (northcoast_base_temp + chill_month)
    
    ; for icy arctic regions always covered in snow and ice
    REGION_SNOW_TEMPS            [0]  = (arcticsnow_base_temp + cold_month)
    REGION_SNOW_TEMPS            [1]  = (arcticsnow_base_temp + chill_month)
    REGION_SNOW_TEMPS            [2]  = (arcticsnow_base_temp + brisk_month)
    REGION_SNOW_TEMPS            [3]  = (arcticsnow_base_temp + basic_month)
    REGION_SNOW_TEMPS            [4]  = (arcticsnow_base_temp + nice_month)
    REGION_SNOW_TEMPS            [5]  = (arcticsnow_base_temp + warm_month)
    REGION_SNOW_TEMPS            [6]  = (arcticsnow_base_temp + hot_month)
    REGION_SNOW_TEMPS            [7]  = (arcticsnow_base_temp + warm_month)
    REGION_SNOW_TEMPS            [8]  = (arcticsnow_base_temp + nice_month)
    REGION_SNOW_TEMPS            [9]  = (arcticsnow_base_temp + basic_month)
    REGION_SNOW_TEMPS            [10] = (arcticsnow_base_temp + brisk_month)
    REGION_SNOW_TEMPS            [11] = (arcticsnow_base_temp + chill_month)

    ; for Solstheim's ash-covered wastes
    REGION_ASHWASTE_TEMPS        [0]  = (ashwaste_base_temp + cold_month)
    REGION_ASHWASTE_TEMPS        [1]  = (ashwaste_base_temp + chill_month)
    REGION_ASHWASTE_TEMPS        [2]  = (ashwaste_base_temp + brisk_month)
    REGION_ASHWASTE_TEMPS        [3]  = (ashwaste_base_temp + basic_month)
    REGION_ASHWASTE_TEMPS        [4]  = (ashwaste_base_temp + nice_month)
    REGION_ASHWASTE_TEMPS        [5]  = (ashwaste_base_temp + warm_month)
    REGION_ASHWASTE_TEMPS        [6]  = (ashwaste_base_temp + hot_month)
    REGION_ASHWASTE_TEMPS        [7]  = (ashwaste_base_temp + warm_month)
    REGION_ASHWASTE_TEMPS        [8]  = (ashwaste_base_temp + nice_month)
    REGION_ASHWASTE_TEMPS        [9]  = (ashwaste_base_temp + basic_month)
    REGION_ASHWASTE_TEMPS        [10] = (ashwaste_base_temp + brisk_month)
    REGION_ASHWASTE_TEMPS        [11] = (ashwaste_base_temp + chill_month)
 EndFunction


function UpdateClimateState()
    Weather current_weather
    Weather incoming_weather
    int current_temperature

    SetCurrentBiomeAndMonthlyValues()
    
    _Frost_PlayerStateSystem stateSystem = GetPlayerStateSystem()

    ; Ensure that we get the complete state at the sample interval.
    while stateSystem.updateInProgress
        FrostDebug(0, "%%%% Climate ::: Waiting for Player State System to finish update.")
        Utility.Wait(0.2)
    endWhile

    pos_x = stateSystem.playerX
    pos_y = stateSystem.playerY
    pos_z = stateSystem.playerZ
    ws = stateSystem.thisWorldSpace
    int region = UpdateCurrentRegion(pos_x, pos_y)
    ; debug.trace("Region is now " + region)

    bool transitioning = IsWeatherTransitioning()
    if transitioning
        incoming_weather = Weather.GetCurrentWeather()
        current_weather = Weather.GetOutgoingWeather()
    else
        incoming_weather = none
        current_weather = Weather.GetCurrentWeather()
    endif

    ShowWeatherTransitionMessage(current_weather, incoming_weather, region)

    current_max_temperature = GetMaxTemperatureByLocation()
    current_min_temperature = GetMinTemperatureByLocation()

    ; To calculate temperature, always use the incoming weather if present.
    if transitioning
        current_temperature = GetCurrentTemperature(incoming_weather, region)
    else
        current_temperature = GetCurrentTemperature(current_weather, region)
    endif

    if !first_update && current_temperature <= 3
        ShowTutorial_Cold()
    endif

    FrostDebug(0, "%%%% Climate ::: Current Temp: " + current_temperature + ", Region: " + region)
    _Frost_CurrentTemperature.SetValueInt(current_temperature)
    _Frost_CurrentWaterTemperature.SetValueInt(current_temperature + 2)
    FrostfallCurrentTemperatureReadOnly.SetValueInt(current_temperature)
    SendEvent_UpdateWeathersenseMeter(current_temperature)

    ; Historical values
    last_current_weather = current_weather
    last_incoming_weather = incoming_weather
    last_current_temperature = current_temperature
    last_max_temperature = current_max_temperature
    last_min_temperature = current_min_temperature
    last_region = region
    first_update = false
endFunction

bool function IsWeatherTransitioning()
    return !(Weather.GetCurrentWeatherTransition() >= 1.0)
endFunction

Event OnTamrielRegionChange(int region, bool in_region)
    currentRegion = region
endEvent

int function GetCurrentTemperature(Weather this_weather, int region)
    ; Don't increase exposure when indoors.
    if CampUtil.IsRefInInterior(PlayerRef)
        return 10
    endif

    ; Don't increase exposure in Oblivion.
    if region == REGION_OBLIVION
        return 10
    endif

    ; set the global variable to the current biome
    REGION_CURRENTLY_IN.SetValue(region as int) 
    
    ; needed for seasonal base temp change
    int current_month = (GameMonth.GetValue() as int) 

    ; the mod Daylight Hours will soon switch to using SKSE and a dll, 
    ; allowing for day-length to change dynamically in-game from day to day
    ; in preparation for this the sunset / sunrise hours will be set to globals
    ; that will eventually receive that data
    
    ; until then the the globals will be set to the default values of Frostfall
    int sunrise_start = (SunriseStartHour.GetValue() as int) ;  5
    int sunrise_end   = (SunriseEndHour.GetValue() as int)   ;  8
    int sunset_start  = (SunsetStartHour.GetValue() as int)  ; 18
    int sunset_end    = (SunsetEndHour.GetValue() as int)    ; 21
    
    float hour = GameHour.GetValue()
    if (hour > sunset_end) || (hour < sunrise_start)
        is_nighttime = true
        is_twilight  = false
    elseif ((hour >= sunset_start) && (hour <= sunset_end)) || ((hour >= sunrise_start) && (hour <= sunrise_end))
        is_nighttime = false 
        is_twilight  = true 
    else
        is_nighttime = false
        is_twilight  = false 
    endif

    bool time_changed = false
    if (is_nighttime && !was_nighttime) || (!is_nighttime && was_nighttime)
        time_changed = true
    elseif (is_twilight && !was_twilight) || (!is_twilight && was_twilight)
        time_changed = true
    endif

    ; Don't recalculate if the weather, region or time hasn't changed.
    if last_max_temperature == current_max_temperature &&   \
       last_min_temperature == current_min_temperature &&   \
       this_weather == last_current_weather &&              \
       region == last_region && !time_changed
        return last_current_temperature
    endif

    int current_temperature = 10
    int base_temperature = GetRegionBaselineTemperature(region, current_month)
    int current_weather_class = GetWeatherClassificationActual(this_weather)

    if current_weather_class == WEATHERCLASS_UNKNOWN
        current_temperature = (base_temperature - 2) - RandomInt(-1, 1)

    elseif current_weather_class == WEATHERCLASS_PLEASANT
        current_temperature = base_temperature - RandomInt(-1, 2)

    elseif current_weather_class == WEATHERCLASS_CLOUDY_OR_FOGGY
        current_temperature = (base_temperature - 3) - RandomInt(-1, 1)

    elseif current_weather_class == WEATHERCLASS_RAIN
        if IsWeatherSevere(this_weather)
            current_temperature = (base_temperature - 7) - RandomInt(-1, 3)
        else
            current_temperature = (base_temperature - 5) - RandomInt(-1, 1)
        endif

    elseif current_weather_class == WEATHERCLASS_SNOW
        if IsWeatherSevere(this_weather)
            current_temperature = (base_temperature - 15) - RandomInt(-2, 2)
            if current_temperature > -10
                current_temperature = -10
            endif
        else
            current_temperature = (base_temperature - 5) - RandomInt(-2, 2)
            if current_temperature > -5
                current_temperature = -5
            endif
        endif
    endif

    if is_twilight
        current_temperature -= 2
    endif
    was_twilight = is_twilight
    
    if is_nighttime
        current_temperature -= 5
    endif
    was_nighttime = is_nighttime

    if current_temperature > current_max_temperature
        current_temperature = current_max_temperature
    endif
    if current_temperature < current_min_temperature
        current_temperature = current_min_temperature
    endif

    return current_temperature
endFunction

int function GetMinTemperatureByLocation()
    int min_temp = -100
    int returnVal
    
    ; statue of meridia area, when raised into the sky
    if (pos_x <= -93300 &&  pos_x >= -99200) && (pos_y <= 107400 && pos_y >= 97000) && pos_z >=13500
        min_temp = 10
        ; max_temp = 10     ; also found below, in the max temp function
        was_on_high_hrothgar_peak = false ; seems to be required for all min temp returns
    elseIf ws == WindhelmWorld || ws == WindhelmPitWorldspace || ws == WhiterunWorld || ws == SolitudeWorld
        was_on_high_hrothgar_peak = false
        ;    return 2
        ; why was this set to 2? setting this to 2 placed a minimum that Windhelm could never be less than, 
            ; even at night during a blizzard in the city; but Solitude and Whiterun use the same temp profile, 
            ; meaning it could be colder in either of these places than in Windhelm, since they are not limited.
            ; I'm guessing this was done as a bug-fix in case the PC fast-travelled to/from the peak and Windhelm?
            ; but then why was a similar minimum not set for other city world spaces?
            ; for now I am setting it to -15 as a minimum, and I am adding Whiterun and Solitude
        return -15
    elseif (pos_x <= 74340 && pos_x >= 32000) && (pos_y <= -21000 && pos_y >= -66600) && pos_z >= 35541
        if !was_on_high_hrothgar_peak
            was_on_high_hrothgar_peak = true
            ShowCalmMessage()
        endif
        return 10
    else
        was_on_high_hrothgar_peak = false
        return min_temp
    endif
endFunction

int function GetMaxTemperatureByLocation()
    int max_temp = 100
    if ws != Tamriel
        return max_temp
    endif

    int current_month = (GameMonth.GetValue() as int)

    ; High Hrothgar
    if (pos_x <= 74340 && pos_x >= 32000) && (pos_y <= -21000 && pos_y >= -66600) && (pos_z >15000)
        FrostDebug(0, "%%%% Climate ::: Override Area: High Hrothgar | Max Temp: " + max_temp)

        bool DangerousThroat = (DangerousMountainToggle.GetValue() as bool)
        if (DangerousThroat == FALSE)

            if pos_z >= 35541       ;Elevation 5            ~~~~    _  ~~~~
                max_temp = 10       ;                                                       (A strange calm at the peak.)
            elseif pos_z >= 34000   ;Elevation 4                ~~/~~\~~~~~~                ; shortly before the peak
                max_temp = -20      ;                        ~~~ /  ~~\~~~
            elseif pos_z >= 27500   ;Elevation 3               /   ??  \                    ; half-way along path from High Hrothgar to peak
                max_temp = -15      ;                        / . ~~   ?? \
            elseif pos_z >= 21300   ;Elevation 2           .  .  ~~~~   ??\                 <----High Hrothgar, the wide steps just before it
                max_temp = -10      ;                     /  .  .  ~~ ??   \
            elseif pos_z >= 15750   ;Elevation 1         / .   .    ??      \
                max_temp = -5       ;                   /########  ??########\              ; snow starts appearing on the path
            endif                   ;                           o    ))))FUS RO DAH))))
                                    ;                        [ ]|/={===>                    <----Dovahkiin
                                    ;                          / \
        ElseIf (DangerousThroat == TRUE)
            if pos_z >= 35541       ;Elevation 5    - at the peak, where a perpetual mild calm exists
                max_temp = 10       ;
            elseif pos_z >= 34000   ;Elevation 4    - shortly from the peak, not far before the narrow pass between two tall stones
                max_temp = -35      ;
            elseif pos_z >= 31000   ;Elevation 3,5  - ~2/3 along path, where a massive rock formation splits path in two
                max_temp = -30      ;
            elseif pos_z >= 27500   ;Elevation 3    - ~1/3 way long path, where the goat is located
                max_temp = -25      ;
            elseif pos_z >= 24500   ;Elevation 2,5  - not quite the top of the stairs just after High Hrothgar
                max_temp = -20      ; 
            elseif pos_z >= 21300   ;Elevation 2    - at the wide steps just before High Hrothgar
                max_temp = -15      ;
            elseif pos_z >= 18500   ;Elevation 1,5  - first curve in path after it is continuously snow-covered until the peak
                max_temp = -10      ;
            elseif pos_z >= 15750   ;Elevation 1    - snow starts appearing upon the path
                max_temp = -5       ;
            endif
        EndIf


    ; the areas below are all snow covered, so their max temp is set to -10 - the default in the non-season version
    ; but what if a summer overhaul is being used that removes the snow? such overhauls do not remove glaciers, 
    ; but some glacier areas (such as along the north coast) had a default temp of -5, not -10.
    ; based on this, I have added a current_month factor: during winter it will be a max = -15, 
    ; during spring / autumn it will be a max of -10, and during summer it will be a max of -5

    ; I considered doing the same for High Hrothgar, but it is already brutal enough, 
    ; and being the highest peak it should be exceptionally cold even during summer.


    ; The Rift
    elseif (pos_x <= 210000 &&  pos_x >= 53800) && (pos_y <= -66600 && pos_y >= -150000)
        if pos_z >= 16600
           if current_month <=1 || current_month == 11      ; winter
                max_temp = -15
           elseif current_month >= 5 || current_month <= 7  ; summer
                max_temp = -5
           else
                max_temp = -10
           endif
        endif
        FrostDebug(0, "%%%% Climate ::: Override Area: Rift | Max Temp: " + max_temp)
    ; Falkreath Hold
    elseif (pos_x <= 53800 &&  pos_x >= -42500) && (pos_y <= -66600 && pos_y >= -150000)
        if pos_z >= 7300
            if current_month <=1 || current_month == 11     ; winter
                max_temp = -15
           elseif current_month >= 5 || current_month <= 7  ; summer
                max_temp = -5
           else
                max_temp = -10
           endif
        endif
        FrostDebug(0, "%%%% Climate ::: Override Area: Falkreath Hold | Max Temp: " + max_temp)
    ; Bleak Falls Barrow
    elseif (pos_x <= 19400 &&  pos_x >= -42500) && (pos_y <= -15000 && pos_y >= -60900)
        if pos_z >= 1500
            if current_month <=1 || current_month == 11     ; winter
                max_temp = -15
           elseif current_month >= 5 || current_month <= 7  ; summer
                max_temp = -5
           else
                max_temp = -10
           endif
        endif
        FrostDebug(0, "%%%% Climate ::: Override Area: Bleak Falls Barrow | Max Temp: " + max_temp)
    ; Brittleshin Pass
    elseif (pos_x <= 15300 &&  pos_x >= -42500) && (pos_y <= -60900 && pos_y >= -80000)
        if pos_z >= 2000
            if current_month <=1 || current_month == 11     ; winter
                max_temp = -15
           elseif current_month >= 5 || current_month <= 7  ; summer
                max_temp = -5
           else
                max_temp = -10
           endif
        endif
        FrostDebug(0, "%%%% Climate ::: Override Area: Brittleshin Pass | Max Temp: " + max_temp)
    ; Haafingar (Dawnguard: catches Castle Volkihar)
    elseif (pos_x <= -71000 &&  pos_x >= -185000) && (pos_y <= 163000 && pos_y >= 78000)
        if pos_z >= -7000
            if current_month <=1 || current_month == 11     ; winter
                max_temp = -15
           elseif current_month >= 5 || current_month <= 7  ; summer
               max_temp = -5
           else
               max_temp = -10
           endif
        else
           if current_month <=1 || current_month == 11     ; winter
                max_temp = -10
           elseif current_month >= 5 || current_month <= 7  ; summer
                max_temp =  0
           else
                max_temp = -5
           endif
        endif
        FrostDebug(0, "%%%% Climate ::: Override Area: Haafingar | Max Temp: " + max_temp)
    ; Statue of Meridia, when raised into the sky (z > ~14000)
    elseIf (pos_x <= -93300 &&  pos_x >= -99200) && (pos_y <= 107400 && pos_y >= 97000) && pos_z >=13500
        ; min_temp = 10       ; also found above, in the min temp function
        max_temp = 10
        FrostDebug(0, "%%%% Climate ::: Override Area: Statue of Meridia elevated platform | Max Temp: " + max_temp)
    endif
    
    return max_temp
endFunction

int function GetRegionBaselineTemperature(int region, int month)

    if region == REGION_UNKNOWN
        return REGION_UNKNOWN_TEMPS[month]
    elseif region == REGION_PINEFOREST
        return REGION_PINEFOREST_TEMPS[month]
    elseif region == REGION_VOLCANICTUNDRA
        return REGION_VOLCANICTUNDRA_TEMPS[month]
    elseif region == REGION_FALLFOREST
        return REGION_FALLFOREST_TEMPS[month]
    elseif region == REGION_REACH  ; because steppe can be colder than a canyon, I have separated the Reach and Tundra regions
        return REGION_REACH_TEMPS[month]
    elseIf region == REGION_TUNDRA
        return REGION_TUNDRA_TEMPS[month]
    elseif region == REGION_TUNDRAMARSH
        return REGION_TUNDRAMARSH_TEMPS[month]
    elseif region == REGION_COAST
        return REGION_COAST_TEMPS[month]
    elseif region == REGION_SNOW
        return REGION_SNOW_TEMPS[month]
    elseif region == REGION_OBLIVION
        return 16  ; this is a separate plane of existence, so there is no need for it to have seasons
    elseif region == REGION_ASHWASTE
        return REGION_ASHWASTE_TEMPS[month]
 
    ;           ####Official DLC Compatibility####
    ;elseif region == REGION_FALMERVALLEY
    ;    return Compatibility.GetPlayerRegionTemp_FalmerValley(pos_x, pos_y)
    ;elseif region == REGION_SOLSTHEIM
    ;    return Compatibility.GetPlayerRegionTemp_Solstheim(pos_x, pos_y)

    ;           ####Landmass Mod Compatibility####
    ;elseif region == REGION_WYRMSTOOTH
    ;    return Compatibility.GetPlayerRegionTemp_Wyrmstooth(pos_x, pos_y)
    ;elseif region == REGION_DARKEND
    ;    return Compatibility.GetPlayerRegionTemp_Darkend(pos_x, pos_y)
    endif
endFunction

int function GetPlayerRegion()
    if ws == Tamriel
        if currentRegion == REGION_PINEFOREST
            return REGION_PINEFOREST
        elseif currentRegion == REGION_VOLCANICTUNDRA
            return REGION_VOLCANICTUNDRA
        elseif currentRegion == REGION_FALLFOREST
            return REGION_FALLFOREST
        elseif currentRegion == REGION_REACH
            return REGION_REACH
        elseif currentRegion == REGION_TUNDRA
            return REGION_TUNDRA
        elseif currentRegion == REGION_TUNDRAMARSH
            return REGION_TUNDRAMARSH
        elseif currentRegion == REGION_COAST
            return REGION_COAST
        elseif currentRegion == REGION_SNOW
            return REGION_SNOW
        else
            return REGION_UNKNOWN
        endif
    else
        if _Frost_WorldspacesExteriorPineForest.HasForm(ws)
            return REGION_PINEFOREST
        elseif _Frost_WorldspacesExteriorVolcanicTundra.HasForm(ws)
            return REGION_VOLCANICTUNDRA
        elseif _Frost_WorldspacesExteriorFallForest.HasForm(ws)
            return REGION_FALLFOREST
        elseif _Frost_WorldspacesExteriorWhiterun.HasForm(ws)
            return REGION_TUNDRA
        elseif _Frost_WorldspacesExteriorTundraMarsh.HasForm(ws)
            return REGION_TUNDRAMARSH
        elseif _Frost_WorldspacesExteriorCoast.HasForm(ws)
            return REGION_COAST
        elseif _Frost_WorldspacesExteriorSnowy.HasForm(ws)
            return REGION_SNOW
        elseif _Frost_WorldspacesExteriorOblivion.HasForm(ws)
            return REGION_OBLIVION
        elseif (Compatibility.isDLC1Loaded as bool) && ws == (Compatibility.WS_FalmerValley as Worldspace)
            return (Compatibility.GetPlayerRegionTemp_FalmerValley(pos_x, pos_y) as Int)
        elseif (Compatibility.isDLC2Loaded as bool) && ws == (Compatibility.WS_Solstheim as Worldspace)
            return (Compatibility.GetPlayerRegionTemp_Solstheim(pos_x, pos_y) as Int)
        elseif (Compatibility.WyrmstoothPresent as bool) && ws == (Compatibility.WS_Wyrmstooth as Worldspace)
            return (Compatibility.GetPlayerRegionTemp_Wyrmstooth(pos_x, pos_y) as Int)
        elseif (Compatibility.DarkendPresent as bool) && ws == (Compatibility.WS_Darkend as Worldspace)
            return (Compatibility.GetPlayerRegionTemp_Darkend(pos_x, pos_y) as Int)
        else
            return REGION_UNKNOWN
        endif
    endif
endFunction


int function GetWeatherClassificationActual(Weather akWeather)
    if !akWeather
        return -1
    endif

    if _Frost_OvercastWeatherList.HasForm(akWeather)
        return 0
    endif

    int weather_class = akWeather.GetClassification()
    if weather_class == 3
        if Compatibility.isDLC2Loaded && akWeather == Compatibility.DLC2AshStorm
            return 1
        else
            return 3
        endif
    else
        return weather_class
    endif
endFunction

function ShowWeatherTransitionMessage(Weather current_weather, Weather incoming_weather, int region)
    if IsRefInInterior(PlayerRef) || _Frost_Setting_WeatherMessages.GetValueInt() != 2
        return
    endif

    if incoming_weather == last_incoming_weather || incoming_weather == none
        return
    endif

    int current_weatherclass = GetWeatherClassificationActual(current_weather)
    int incoming_weatherclass = GetWeatherClassificationActual(incoming_weather)
    bool current_weather_severe = IsWeatherSevere(current_weather)
    bool incoming_weather_severe = IsWeatherSevere(incoming_weather)

    if incoming_weatherclass == WEATHERCLASS_UNKNOWN || incoming_weatherclass == WEATHERCLASS_PLEASANT
        if current_weatherclass == WEATHERCLASS_RAIN
            if current_weather_severe
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: CLEAR     OUTGOING: STORM")
                _Frost_WeatherTransMsg_StormToClear.Show()
            else
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: CLEAR     OUTGOING: RAIN")
                _Frost_WeatherTransMsg_RainToClear.Show()
            endif
        elseif current_weatherclass == WEATHERCLASS_SNOW
            if current_weather_severe
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: CLEAR     OUTGOING: BLIZZARD")
                _Frost_WeatherTransMsg_BlizzardToClear.Show()
            else
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: CLEAR     OUTGOING: SNOW")
                _Frost_WeatherTransMsg_SnowToClear.Show()
            endif
        endif

    elseif incoming_weatherclass == WEATHERCLASS_CLOUDY_OR_FOGGY
        if current_weatherclass == WEATHERCLASS_UNKNOWN || current_weatherclass == WEATHERCLASS_PLEASANT
            if region == REGION_UNKNOWN
                _Frost_WeatherTransMsg_ClearToFog1.Show()
            elseif region == REGION_PINEFOREST
                _Frost_WeatherTransMsg_ClearToFog2.Show()
            elseif region == REGION_VOLCANICTUNDRA
                _Frost_WeatherTransMsg_ClearToFog3.Show()
            elseif region == REGION_FALLFOREST
                _Frost_WeatherTransMsg_ClearToFog4.Show()
            elseif region == REGION_REACH
                _Frost_WeatherTransMsg_ClearToFog5.Show()
            elseif region == REGION_TUNDRAMARSH
                _Frost_WeatherTransMsg_ClearToFog6.Show()
            elseif region == REGION_COAST
                _Frost_WeatherTransMsg_ClearToFog7.Show()
            endif
            FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: FOG     OUTGOING: CLEAR")
        elseif current_weatherclass == WEATHERCLASS_RAIN
            _Frost_WeatherTransMsg_RainToFog.Show()
            FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: FOG     OUTGOING: RAIN")
        endif

    elseif incoming_weatherclass == WEATHERCLASS_RAIN
        if current_weatherclass == WEATHERCLASS_UNKNOWN || current_weatherclass == WEATHERCLASS_PLEASANT
            if incoming_weather_severe
                _Frost_WeatherTransMsg_ClearToStorm.Show()
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: STORM     OUTGOING: CLEAR")
            else
                _Frost_WeatherTransMsg_ClearToRain.Show()
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: RAIN     OUTGOING: CLEAR")
            endif
        elseif current_weatherclass == WEATHERCLASS_CLOUDY_OR_FOGGY
            if incoming_weather_severe
                _Frost_WeatherTransMsg_FogToStorm.Show()
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: STORM     OUTGOING: FOG")
            else
                _Frost_WeatherTransMsg_FogToRain.Show()
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: RAIN     OUTGOING: FOG")
            endif
        elseif current_weatherclass == WEATHERCLASS_SNOW
            _Frost_WeatherTransMsg_SnowToRain.Show()
            FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: RAIN     OUTGOING: SNOW")
        endif
    elseif incoming_weatherclass == WEATHERCLASS_SNOW
        if current_weatherclass == WEATHERCLASS_UNKNOWN || current_weatherclass == WEATHERCLASS_PLEASANT
            if incoming_weather_severe
                if current_max_temperature != 100
                    _Frost_WeatherTransMsg_ClearToSnowMountain.Show()
                    FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: MOUNTAIN BLIZZARD    OUTGOING: CLEAR")
                else
                    _Frost_WeatherTransMsg_ClearToSnowSevere.Show()
                    FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: BLIZZARD     OUTGOING: CLEAR")
                endif
            else
                _Frost_WeatherTransMsg_ClearToSnow.Show()
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: SNOW     OUTGOING: CLEAR")
            endif
        elseif current_weatherclass == WEATHERCLASS_SNOW
            if incoming_weather_severe
                _Frost_WeatherTransMsg_RainToSnowSevere.Show()
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: BLIZZARD     OUTGOING: RAIN")
            else
                _Frost_WeatherTransMsg_RainToSnow.Show()
                FrostDebug(1, "%%%% Climate ::: Weather Transition INCOMING: SNOW     OUTGOING: RAIN")
            endif
        endif
    endif
endFunction

function ShowCalmMessage()
    if _Frost_Setting_WeatherMessages.GetValueInt() == 2
        _Frost_CalmMsg.Show()
        Wait(2)
        _Frost_Calm2Msg.Show()
    endif
endFunction

function ShowTutorial_Cold()
    if _Frost_Setting_DisplayTutorials.GetValueInt() == 2 && _Frost_HelpDone_Cold.GetValueInt() == 1
        if CampUtil.GetSKSELoaded()
            _Frost_Help_Cold.Show()
        else
            _Frost_Help_ColdSE.Show()
        endif
        _Frost_HelpDone_Cold.SetValue(2)
    endif
endFunction

function SendEvent_UpdateWeathersenseMeter(int temp)
    if GetSKSELoaded()
        int temp_level
        if temp >= 18
            _Frost_AttributeMeterTempLevel.SetValueInt(10)
        elseif temp < 18 && temp >= 15
            _Frost_AttributeMeterTempLevel.SetValueInt(9)
        elseif temp < 15 && temp > 10
            _Frost_AttributeMeterTempLevel.SetValueInt(8)
        elseif temp == 10
            _Frost_AttributeMeterTempLevel.SetValueInt(7)
        elseif temp < 10 && temp >= 6
            _Frost_AttributeMeterTempLevel.SetValueInt(6)
        elseif temp < 6 && temp >= 1
            _Frost_AttributeMeterTempLevel.SetValueInt(5)
        elseif temp < 1 && temp >= -4
            _Frost_AttributeMeterTempLevel.SetValueInt(4)
        elseif temp < -4 && temp >= -9
            _Frost_AttributeMeterTempLevel.SetValueInt(3)
        elseif temp < -9 && temp >= -14
            _Frost_AttributeMeterTempLevel.SetValueInt(2)
        elseif temp < -14
            _Frost_AttributeMeterTempLevel.SetValueInt(1)
        endif
        int handle = ModEvent.Create("Frostfall_UpdateWeathersenseMeter")
        if handle
            ModEvent.Send(handle)
        endif
    endif
endFunction


bool function IsPointInPolygonFast(float[] polyX, float[] polyY, float minX, float maxX, float minY, float maxY, float x, float y)
    ; Attempts to determine if a given point (x, y) lies inside the bounds of a polygon described as a series
    ; of ordered pairs described in the polyX[] and polyY[] arrays.
    ; If (x, y) lies exactly on one of the line segments, this functiom may return True or False.
    ; From http://alienryderflex.com/polygon/, converted to Papyrus by Chesko
    ; Added bounding box check to increase speed
    
    ; Return Values
    ;     True  = Point is inside polygon
    ;     False = Point lies outside polygon OR polygon arrays are of different lengths

    ;float[] polyX = array that describes the polygon's x coordinates
    ;float[] polyY = array that describes the polygon's y coordinates
    ;float x           = the x coordinate under test
    ;float y           = the y coordinate under test
    
    ;debug.trace("Checking point in polygon.")
    if x < minX || x > maxX || y < minY || y > maxY
        ;debug.trace("    Escaped early, outside of bounding box!")
        return false
    endif
        
    int polySides = polyX.Length
    int i = 0
    int j = polySides - 1
    bool oddNodes = false

    while i < polySides
        if (((polyY[i] < y && polyY[j] >= y) || (polyY[j] < y && polyY[i] >= y)) && (polyX[i] <= x || polyX[j] <= x))
            if (polyX[i] + (y- polyY[i]) / (polyY[j] - polyY[i]) * (polyX[j] - polyX[i])) < x
                oddNodes = !oddNodes
            endif
        endif
        j = i
        i += 1
    endWhile
       
    ;debug.trace("    Check returning " + oddNodes)
    return oddNodes
endFunction

