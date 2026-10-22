Authoria - Carriage PBR Wood Fix (2026-10-12)

Source: Authoria - PG Output - PBR (PG Patcher 1.2.0 run of 2026-08-28).
Change: in each mesh below, every shape whose base texture is textures\architecture\farmhouse\woodwall01.dds (Parallax) or
textures\architecture\riften\riftencanalplanks01.dds (EnvMap) now carries a byte copy of the same mesh's PrisonerCarriage:2 material
(textures\pbr\architecture\markarth\mrkwood01 + _n/_p/_rmaos, SLSF2 PBR flag, PBR glossiness), vertex-colour flag kept per shape.
Block count and indices unchanged; only those shader-property and texture-set blocks differ from the PG output.
Why: no PBR version of those two textures exists in the instance, so PG Patcher left them non-PBR next to PBR panels.
Remove when: PG Patcher is rerun with PBR farmhouse / Riften wood sources installed (then the output itself is right).
Script: session scratchpad s15_carriage_fix.py (nifrw.py toolkit).

Files:
  meshes\clutter\vicn\cart\carriage01.nif
  meshes\clutter\vicn\cart\carriage01_shadow.nif
  meshes\clutter\vicn\cart\carriage02.nif
  meshes\clutter\vicn\cart\carriage02_shadow.nif
  meshes\clutter\vicn\cart\carriageb01.nif
  meshes\clutter\vicn\cart\carriageb01_shadow.nif
  meshes\clutter\vicn\cart\carriageb02.nif
  meshes\clutter\vicn\cart\carriageb02_shadow.nif
  meshes\furniture\prisonercarriage\prisonercarriage01.nif
  meshes\furniture\prisonercarriage\prisonercarriage01static.nif
  meshes\furniture\prisonercarriage\prisonercarriagefurniture01.nif
  meshes\_pgpatcher_dups\1\furniture\prisonercarriage\prisonercarriage01static.nif
