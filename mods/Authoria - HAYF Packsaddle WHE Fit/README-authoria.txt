Authoria - HAYF Packsaddle WHE Fit                       built 2026-08-23

PROBLEM
  Horses Are Your Friends' packsaddle is modelled on the vanilla Skyrim horse.
  Witcher Horse Expansion replaces the horse body with a slimmer barrel.
  Result: the saddle stands about 3 units proud on each side and the girth
  band hangs about 6 units clear of the belly, so the band appears to stop in
  mid-air instead of wrapping the horse.

FIX
  The 'NordicSaddle' shape in each mesh is scaled by 0.915 in X and Z about
  the line X=0, Z=122.5 (the horse's back), leaving Y untouched.
  That keeps the saddle top where it was, pulls the flaps in, and lifts the
  girth loop up onto the belly. Standoff now matches Witcher Horse Expansion's
  own saddle.nif:
                       side gap        girth under belly
    WHE own saddle     +1.9 .. +2.8    -0.7 .. -1.2
    HAYF before        +5.2 .. +6.2    -5.6 .. -6.5
    HAYF after         +2.6 .. +3.6    -0.6 .. -1.4

FILES
  meshes/hayfmeshes/hayfpacksaddlelav.nif    (HAYFHorsePackSaddle01AA)
  meshes/hayfmeshes/hayfpacksaddlecot.nif    (HAYFHorsePackSaddle02AA)
  meshes/hayfmeshes/hayfflowersaddle.nif     (HAYFHorseFlowerSaddleAA)

  Only the NordicSaddle shape was touched. Every other shape in those files is
  byte-identical to the originals in HorsesAreYourFriends_Lite.bsa.
  No plugin, no records. Loose files beat the BSA, so no load order concerns.
  To revert: disable or delete this mod.
