//===============================================================================================//
// Based on kingeric1992,s work here: http://enbseries.enbdev.com/forum/viewtopic.php?f=7&t=4394 //
// Description and Presetup by Adyss                                                             //
//===============================================================================================//

/*
What is a LUT?
A LUT (Lookup Table) is basically a color palette that tells colors what to do. Neutral LUTs in diffrent sizes can be found in LUT folder.

How do i use a LUT?
Basically you take a screenshot and alter it in Photoshop or any other programm (i use Magic Bullet) to your likeing.
You can only change colors on it. No grain or else
After you have your screenshot set you take the LUT.bmp (or .png) and load it into your ENB (look below) The changes you made will now appear ingame.


=============================================== Load LUTs in your ENB =======================================================

 | First annonce that its a texture |     | Give your lut a codename |        |   Give the path to your LUT file         |
 |            Texture2D             |     |          LUTxy           |        |  <string ResourceName="LUT/LUT.bmp"; >;  |
 
	example:
	Texture2D LOGtoREC          <string ResourceName="LUT/LOGtoREC.bmp"; >;  

=============================================== Apply your loaded LUTs ======================================================
 
Depending on the size of the lut you loaded you will need a diffrent function to apply it
available lut sizes are:       256x16      1024x32      4096x64
functions for these are:       Lut256      Lut1024      Lut4096

| what you alter with lut (don't change) |    | Size of your LUT |   | necessary step for the code |    | Name you gave the lut you loaded and want to apply |
|            color.rgb =                 |    |      Lut256      |   |         (color.rgb,         |    |                     LUTxy);                        |

	example:
	color.rgb = Lut4096(color.rgb, LOGtoREC);
	
	In case you want seperate luts for each daytime you will need to load 3 luts. Apply them by doing:
    color.rgb = lerp(lerp(Lut256(color.rgb, LUTxy_Night), 
                          Lut256(color.rgb, LUTxy_Day),      ENightDayFactor),
                          Lut256(color.rgb, LUTxy_Interior), EInteriorFactor);
|

	Usefull Info:
	it doesnt matter what format the luts are in. Tho i only tested .bmp and .png yet.
	The bigger the LUT the more precise will your colorchanges be applied. 1024 should be enough in most cases. (4096 is a bit overkill lol)
	You  cant have the same LUTname twice without getting a compiler error.

	
=============================================== Integrade Switchweel ======================================================== 

This little tool makes it possible to switch LUTs ingame on the fly. 
Baically you do: 


| and if statement with the nr you have to chose ingame to apply it |   | Your lut function (and log if wanted)  |   | another  } to end the if statement |
|                       if (LUTSelect==1) {                         |   | color.rgb = Lut4096(color.rgb, LUTxy); |   |                }                   |

	example:
	if (LUTSelect==1) { color.rgb = Lut4096(color.rgb, LUTxy); }
	
	if (LUTSelect==2) { color.rgb = TM_Lin2Log(color.rgb);     color.rgb = Lut4096(color.rgb, LOGtoREC);  }


*/

#define USE_LUTweel  1                 // Set to 0 if you dont want to have selectable luts
#define weelname     "Select LUT"      // Decide what the weel shall be called. Dont remove the "  "
#define LUTcounter   3                 // Select the Nr. of LUTs that you want to have selectable

#include "Shaders/PostUI.fxh"          // LEAVE THIS!!!
 
/*
=============================================== Convert Image Color to Grade ================================================
	
	In case you want to grade on LOG fotage i added these functions (code by kingeric1992)
	Place them before your LUT comes in. This way you can use diffrent log methods to grade ontop
	Or incase you have no idea what all that is look up on it here: https://www.rocketstock.com/blog/tips-for-log-color-space-compositing/
	
	Avalible LOG Functions are:
	
    color.rgb = TM_Lin2Log(color.rgb);

    color.rgb = TM_sLog3(color.rgb);

	color.rgb = TM_sLog2(color.rgb);

	color.rgb = TM_sLog(color.rgb);

	color.rgb = TM_sGamut3Cine(color.rgb);

	color.rgb = TM_sGamut3(color.rgb);

	color.rgb = TM_Cineon(color.rgb);
	
	
	implementation example:
	color.rgb = TM_Lin2Log(color.rgb);
	color.rgb = Lut4096(color.rgb, MyLogLUT);
	
	
	might be useful: https://luts.iwltbap.com/free-lut-log-to-rec709-and-rec709-to-log-conversion/


===================================================== Implementation ========================================================

Basically do what has been written above inbetween the {      }    (not the texture loading tho)

	example:
	Texture2D LOGtoREC          <string ResourceName="LUT/LOGtoREC.bmp"; >; 
	Texture2D sLOG_LUT          <string ResourceName="LUT/MySLogLUT.bmp"; >; 
	Texture2D LUTxy_Night       <string ResourceName="LUT/VibrantNight.bmp"; >; 
	Texture2D LUTxy_Interior    <string ResourceName="LUT/VibrantInterior.bmp"; >; 
	Texture2D LUTxy_Day         <string ResourceName="LUT/VibrantDay.bmp"; >; 
	
	
    float3 LUTApply(float3 color)        // Leave this!
    {                                    // Leave this!
	
	if (LUTSelect==1) {
	color.rgb = TM_Lin2Log(color.rgb);
    color.rgb = Lut4096(color.rgb, LOGtoREC);
	}
	
	if (LUTSelect==2) {
	color.rgb = TM_sLog(color.rgb);
	color.rgb = Lut1024(color.rgb, sLOG_LUT);
	}
	
	if {LUTSelect==3) {
    color.rgb = lerp(lerp(Lut256(color.rgb, LUTxy_Night), 
                          Lut256(color.rgb, LUTxy_Day),      ENightDayFactor),
                          Lut256(color.rgb, LUTxy_Interior), EInteriorFactor);
	}
		return color;                    // Leave this!
    }                                    // Leave this!

*/


float3 LUTApply(float3 color)        // Leave this!
{                                    // Leave this!
	

	
	
	return color;                    // Leave this!
}                                    // Leave this!

