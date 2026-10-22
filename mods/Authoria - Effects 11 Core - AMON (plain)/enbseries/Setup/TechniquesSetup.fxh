/*
A postpass can have multiple passes after each other. This can be really tricky to do. So feel free to ask on the forum or on my discord: https://discord.gg/sWunDwj
Basically here you arrange what passes and when. After a pass happend the next one works with the result of the last one.
Some passes like sharp (in some cases) can conflict with others and should come before the others.
Also some passes need the imput of one of the previous ones (like bloom in this case. 

the first pass has a few infos that is important for all the others

            | gives your postpass a codename. passes that come after that one need to be named MyPostPass1 ... 2 ... 3  and so on | | only witten at the fist pass. (Gives it the ingame name. Change in Shadersetup and not here |
technique11 |                                                     MyPostPass                                                      | |                                <string UIName= postpassname;>                               |
{
  pass p0
    {                  | Here it sets what this pass does. VS = Vertex shader   PS = Pixel Shader (important for you) these two get comiled here |
       SetVertexShader |                                 (CompileShader(vs_5_0, VS_PostProcess()));                                              |
       SetPixelShader  |                                 (CompileShader(ps_5_0, PS_Colors()));                                                   |
    }
}

in the end it should look like this:

technique11 MyPostPass <string UIName= postpassname;>
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Colors()));
    }
}


technique11 MyPostPass1
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Image()));
    }
}


=============== Here comes a list of Possible passes: ====================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Colors()));
    }
}

PS_Colors is were most of the Coloring Shaders are in. I reccoment setting it almost at the end of your passes
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Image()));
    }
}
ALWAYS should be the last of all passes. Otherwise there can be conflicting.
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_LumaSharp()));
    }
}
Place really early. Needs "#define INC_LumaSHARP" to be 1
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_FilmicAnamorphSharp()));
    }
}
 Needs "#define INC_FilmicAnamorphSharp" to be 1
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_BSharp()));
    }
}
 Needs "#define INC_BasicSharp" to be 1
==========================================================================

==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_Lightroom()));
       SetPixelShader (CompileShader(ps_5_0, PS_Lightroom()));
    }
}
 Needs "#define INC_Lightroom" to be 1
==========================================================================


==========================================================================
technique11 post
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianH()));
    }
}


technique11 post1
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianV()));
    }
}

technique11 post2
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessSoftLight()));
    }
}

technique11 post3
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianH()));
    }
}

technique11 post4
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianV()));
    }
}

technique11 post5
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussBloom()));
    }
}

 Needs "#define INC_GaussBloom" to be 1
 Always should look like that as a process. I reccoment setting these passes first

==========================================================================


======================DRAW YOUR TECHNIQUES HERE===========================
*/

technique11 MyPostPass <string UIName= postpassname;>
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Colors()));
    }
}


technique11 MyPostPass1
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Image()));
    }
}


technique11 MyPostPass2
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_FilmicAnamorphSharp()));
    }
}










































/* Example config of mine i used on screenshots like: https://www.flickr.com/photos/157466996@N07/27211402927/in/dateposted-public/
technique11 gallery <string UIName= postpassname;>
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianH()));
    }
}


technique11 gallery1
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianV()));
    }
}

technique11 gallery2
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessSoftLight()));
    }
}

technique11 gallery3
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianH()));
    }
}

technique11 gallery4
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussianV()));
    }
}

technique11 gallery5
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_ProcessGaussBloom()));
    }
}

technique11 gallery6
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_FilmicAnamorphSharp()));
    }
}

technique11 gallery7
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_VSharp()));
    }
}

technique11 gallery8
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Colors()));
    }
}

technique11 gallery10
{
  pass p0
    {
       SetVertexShader(CompileShader(vs_5_0, VS_PostProcess()));
       SetPixelShader (CompileShader(ps_5_0, PS_Image()));
    }
}
*/