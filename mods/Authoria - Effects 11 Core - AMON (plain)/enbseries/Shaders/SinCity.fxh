float3 SincityPass(float3 color)
{
	float sinlumi = dot(color.rgb, float3(0.30f,0.59f,0.11f));
	if(color.r > (color.g + 0.2f) && color.r > (color.b + 0.025f))
	{
		color.rgb = float3(sinlumi, 0, 0)*1.5;
	}
	else
	{
		color.rgb = sinlumi;
	}
	return color.rgb;
}