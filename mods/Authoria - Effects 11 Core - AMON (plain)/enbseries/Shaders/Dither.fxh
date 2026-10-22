// JawZ: Author and developer of MSL //


float3 msDither(float3 color, float2 txcoord0) {
  if (ENABLE_DITHER==true) {  /// Activates if ENABLE_DITHER = true
    float dither_bit = 8.0;  /// Number of bits per channel. Should be 8 for most monitors.

    /// Calculate grid position
      float grid_position = frac(dot(txcoord0, (ScreenSize.x) * float2(0.75, 0.5) + (0.00025)));  // (0.6,0.8) is good too - TODO : experiment with values

    /// Calculate how big the shift should be
      float dither_shift = (0.25) * (1.0 / (pow(2, dither_bit) - 1.0));              /// 0.25 seems good both when using math and when eyeballing it. So does 0.75 btw.
      dither_shift = lerp(2.0 * dither_shift, -2.0 * dither_shift, grid_position);  /// Shift according to grid position.

    /// Shift the color by dither_shift
      color.rgb += float3(dither_shift, -dither_shift, dither_shift);  /// Subpixel dithering


    }

  return color;
}