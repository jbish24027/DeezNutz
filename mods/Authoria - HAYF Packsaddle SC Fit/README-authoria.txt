Authoria - HAYF Packsaddle SC Fit                        built 2026-10-17

PROBLEM
  Horses Are Your Friends' packsaddle is modelled on the vanilla Skyrim horse.
  SC Horses (with Equestrian) has a slimmer barrel, a higher back and a
  higher belly. Measured on the bind pose:
                       vanilla    SC
    barrel half-width   24-25.5   21-22     (mid-barrel, under the saddle)
    back at the seat    121-122   124       (about 2-3 units higher)
    belly at the girth  64.5      70.5-71   (about 6 units higher)
  Result on SC: the saddle flaps stand about 5.6 units off the sides and the
  girth band hangs 6 to 9 units below the belly.

FIX
  The 'NordicSaddle' shape in each mesh is scaled by 0.821 in X and 0.946 in Z
  about the line X=0, Z=122.5 (the horse's back), then raised by 2.85.
  Y is untouched, so it stays lined up with the bags, belts and baskets.
  The X scale and the lift are the ones Equestrian used when it refitted the
  same vanilla saddle onto the SC horse (its saddle.nif). The Z scale is a
  little gentler than Equestrian's 0.930 so HAYF's girth band, which
  Equestrian's saddle does not have, rests on the SC belly instead of
  sinking 0.9 into it. Standoff on the SC body now:
                       side gap           girth band vs belly
                       (median / low 10%) (edges / centre)
    Equestrian saddle  +2.2 / +0.9        top -0.5..-0.8, bottom -1.6..-1.9
    HAYF before        +5.6 / +3.3        -6.0..-6.7 / -8.2..-9.0
    HAYF after         +2.4 / +0.4        +0.0..-0.7 / -2.1..-2.7
  (negative girth numbers = below the belly; HAYF's own design on the vanilla
  horse is edges 0.0, centre -1.9..-2.4)

FILES
  meshes/hayfmeshes/hayfpacksaddlelav.nif    (HAYFHorsePackSaddle01AA)
  meshes/hayfmeshes/hayfpacksaddlecot.nif    (HAYFHorsePackSaddle02AA)
  meshes/hayfmeshes/hayfflowersaddle.nif     (HAYFHorseFlowerSaddleAA)

  Built from the originals in HorsesAreYourFriends_Lite.bsa, not from the
  Witcher fit. Only the NordicSaddle shape was touched: its vertex X/Z, its
  bounding sphere and its per-bone bounding spheres. Every other shape in
  those files is byte-identical to the originals. File sizes are unchanged.
  The flower saddle's NordicSaddle is a trimmed copy of the packsaddle one
  (783 of 894 vertices); it got the same transform.
  No plugin, no records. Loose files beat the BSA, so no load order concerns.
  Replaces 'Authoria - HAYF Packsaddle WHE Fit' (Witcher body); keep only one
  of the two enabled.
  Not fixed here: the bridle sinking into the head and the flower clusters
  sinking into the rump. The bags and basket also sink up to about 3 units
  into the SC back, and the raised saddle top now covers their contact
  points by about 2 units, because those shapes were left alone.
  To revert: disable or delete this mod.
