Authoria - Balgruuf Beard Fix (22 Oct 2026)

Balgruuf's face mesh (FaceGen 00013BBD.nif) copied from True Sons of Skyrim Refined with two fixes:
- Shape HumanBeardMedium04 had a near-white hair tint (0.99, 0.95, 0.86) baked in, while every other hair/beard
  shape had (0.65, 0.63, 0.56), and it used Hvergelmir's vanilla-path beardshort06. Now: the bake's own tint and
  TSOS's own textures\0TSOS\!COR\beard\beardshort06(_n).dds.
- Shape 0BalgruufBeardHL pointed at beardshort05_hd(_n).dds, which no mod provides. Now: TSOS beardshort05(_n).dds.
Everything else is byte-identical. The face tint .dds still comes from TSOS (same bake), so houseCARL's
"split bake" flag here is expected.

Placed directly above True Sons of Skyrim Refined. On in PICTA, PICTA x Astralite, Preset Studio HPH; off elsewhere.
Script: C:\1. AUTHORIA\_tools\fix-list-20261022\balgruuf_beard.py <TSOS nif> <out nif>
If TSOS updates Balgruuf's face, rebuild with the script or delete this mod.
