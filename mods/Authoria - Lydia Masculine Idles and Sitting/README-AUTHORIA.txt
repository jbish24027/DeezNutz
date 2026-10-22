Authoria - Lydia Masculine Idles and Sitting (built 2026-10-12)

Why: vanilla gives Lydia male animations via the "opposite gender anims" flag.
No Opposite Gender Animations NG strips that flag from everyone at runtime, so she
reads the female set and every IsFemale OAR mod (SVFI, Modern Female Sitting, HSF
Cross Legged, Dynamic Female Ledge Sitting) applies to her.

What: OAR submods gated on IsActorBase Skyrim.esm A2C8E (HousecarlWhiterun) that
give her exactly what a male NPC plays:
  900100        vanilla male standing idles + all chair idles on her female path,
                vanilla barstool and throne idle
  900101-104    Improved Table Sit twins (unisex mod)
  889888115-170 Male Furniture Animation Pack chairs + Jarl Sit twins
  998889000     vanilla cross-legged + ledge sit
  998889001-006 Take a Seat twins
  998889128-169 Male Furniture Animation Pack cross-legged twins
Twins copy the source conditions verbatim minus the "not female" gate.
Situational mods (drunk, wounds, RaySense, torch/lantern) still sit above.
Not covered: walking/running, talk gestures, table leaning, hand warming.
Rebuild: _tools\lydia-masculine\build_lydia.py (rescan with oar_scan.py first).
