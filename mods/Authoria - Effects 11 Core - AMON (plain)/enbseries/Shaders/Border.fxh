//=====================//
// Border by Ceejay.dk //
//=====================//
float3 Border(float3 color, float2 coord)
{	
	if (ENABLE_LETTERBOX==true)
	{
	float2 pixelSize=ScreenSize.y;
	pixelSize.y*=ScreenSize.z;

	// -- calculate the right border_width for a given border_ratio --
	float2 border_width_variable = border_width;
	if (border_width.x == -border_width.y) // If width is not used
		if (ScreenSize.z < border_ratio)
			border_width_variable = float2(0.0, (ScreenSize.y - (ScreenSize.x / border_ratio)) * 0.5);
		else
			border_width_variable = float2((ScreenSize.x - (ScreenSize.y * border_ratio)) * 0.5, 0.0);

	float2 border = (ScreenSize.w * border_width_variable); // This is supposed to be pixelSize but dosnt work with it so i use ScreenSize.w
	float2 within_border = saturate((-coord * coord + coord) - (-border * border + border)); // Becomes positive when inside the border and zero when outside

	return all(within_border) ? color : border_color;
	}
	else
	return color;
}