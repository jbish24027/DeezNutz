//==================================//
// Spherical Tonemap by Marty McFly //
//==================================//
float3 Spherical(float3 color)
{
    float3 x =color;
if (USE_Spherical==true)
{
    float sphericalAmount   =lerp( lerp(sphericalAmount_Night,   sphericalAmount_Day,   ENightDayFactor), sphericalAmount_Interior,   EInteriorFactor );
    float3 signedColor = x * 2.0 - 1.0;
    float3 sphericalColor = sqrt(1.0 - signedColor.rgb * signedColor.rgb);
    sphericalColor = sphericalColor * 0.5 + 0.5;
    sphericalColor *= x;
    x += sphericalColor.rgb * sphericalAmount;
}
    return x;
}