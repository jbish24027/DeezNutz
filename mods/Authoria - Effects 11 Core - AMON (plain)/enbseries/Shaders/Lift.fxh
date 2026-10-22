// These adjust what the Drop/Lift Checkmarks ingame do

#define LIFTGamma    1
#define LIFTInBlack  0
#define LIFTInWhite  1
#define LIFTOutBlack 0.06
#define LIFTOutWhite 1

#define DROPGamma    1
#define DROPInBlack  0.06
#define DROPInWhite  1
#define DROPOutBlack 0
#define DROPOutWhite 1


float4 Lift(float4 color)
{
    if (LIFTNAO==true)
	{
	color=max(color-LIFTInBlack, 0.0) / max(LIFTInWhite-LIFTInBlack, 0.0001);
	if (LIFTGamma!=1.0) color=pow(color, LIFTGamma);
	color=color*(LIFTOutWhite-LIFTOutBlack) + LIFTOutBlack;
	}
	if (DROPNAO==true)
	{
	color=max(color-DROPInBlack, 0.0) / max(DROPInWhite-DROPInBlack, 0.0001);
	if (DROPGamma!=1.0) color=pow(color, DROPGamma);
	color=color*(DROPOutWhite-DROPOutBlack) + DROPOutBlack;
	}
	return color;
}