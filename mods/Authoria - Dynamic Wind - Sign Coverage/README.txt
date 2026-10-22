Authoria - Dynamic Wind - Sign Coverage
Built 2026-08-28 by houseCARL.

WHAT THIS IS
------------
Push-module configs for Dynamic Wind Framework, covering hanging signs the upstream
"Dynamic Wind - Skyrim" pack leaves out. The Push handler shoves Havok objects in the
wind direction; a sign only responds if its mesh carries a bhkLimitedHingeConstraint
rig, so every entry below was checked for one before it was written.

No plugin. No scripts. Config JSON only. Safe to add or remove at any time.

Requires: Dynamic Wind Framework (bPushHandlerEnabled=true in DynamicWind.ini).

23 signs at windSensitivity 1.0 to match the upstream pack, plus 4 blacksmith signs
raised to 3.0 - see the last section.

VANILLA GAPS (6) - Skyrim.esm signs the upstream pack missed
  0x101BD5  SignTG03BlackBriarMeadery   Riften, Black-Briar Meadery
  0x0FF297  SignRTRaggedFlagon01        Riften, Ragged Flagon
  0x0EA621  SignRTStables01             Riften stables
  0x0EA620  SignRTAlchemyShop01         Riften, Elgrim's Elixirs
  0x10EAC3  SignFrostfruitInn01         Rorikstead, Frostfruit Inn
  0x0EA696  SignWHStables01             Windhelm stables

SOLSTHEIM (1)
  0x03BD5E~Dragonborn.esm  DLC2SignRRBlacksmith01   Raven Rock, Glover Mallory

BEYOND SKYRIM - BRUMA (7)
  0x003BAB / 003BAD / 003BAE / 003BAF / 003BB1 / 003BB3 / 003BB5 ~BSHeartland.esm
  Restful Watchman, Jerall View Inn, Icewind Traders, A Cut Above,
  Northern Arms, Fighters Guild, Synod Conclave

MOD-ADDED (9)
  0x015BC5~Gray Fox Cowl.esm                 Three Peaks store
  0x283D0C~SnozzResources.esp                Stumbling Sabrecat inn
  0x0F0C7E~LegacyoftheDragonborn.esm         museum gift shop
  0x27A6D7~LegacyoftheDragonborn.esm         Dragonborn Gallery
  0x4CE333~Skyrim Extended Cut - Saints and Seducers.esp   corgi shop
  0x000241~Ivy Riften Docks Overhaul.esp     Riften fishery
  0x00053C~Ivy Riverwood Overhaul.esp        Riverwood magic shop
  0x3F7CEB~Morskom.esp                       Morskom home sign
  0x322F6B~Morskom.esp                       Morskom docks sign

DELIBERATELY NOT INCLUDED
-------------------------
  SignRTOrphanage01 (0x0EA631)  - no havok rig at all in the winning mesh. Fixed board.
  _mag_ForSaleSign  (MagpieManor.esp)  - rigid body but no hinge. Planted, not hung.
  _RMP_PurchaseSign (Mirele)    - Markarth wall sign, no hinge.
  CYRSignSnowStoneRest (0x003AB2~BSHeartland.esm) - Skyking Signs - Bruma.esp repoints it
        at bscyrodiil\Clutter\Signage\Inns\SignWindpeakInn01.nif, which NOTHING in the load
        order provides, loose or in any BSA. That sign has no mesh to push. Separate bug.

NOTES
-----
The two Morskom entries key on Morskom.esp even though PG_1.esp currently wins those
records. Push matches the base FormID, not the load-order winner, so this stays correct
across ParallaxGen re-runs.

Several of these signs hang indoors (Ragged Flagon, LOTD gift shop). The framework fixes
vanilla's interior-wind bug, so wind reads as zero in interiors and those configs are
simply inert there. They cost nothing and start working if the sign is ever moved outside.

BLACKSMITH SIGN STRENGTH OVERRIDES (added 2026-08-28)
-----------------------------------------------------
WiZkiD Diverse Blacksmith Signs replaced the four blacksmith sign meshes. The new rigs
still carry the 4x bhkLimitedHingeConstraint pendulum, so Push works on them - but at the
upstream windSensitivity of 1.0 they barely move. These four are raised to 3.0.

Three of them are OVERRIDES of the upstream Dynamic Wind - Skyrim pack, so they use that
pack's exact filenames (8-hex FormID) to win the MO2 VFS. Do not rename them, or both
copies load for the same FormID and the winner is undefined.

  0009624C.json                          0x09624C~Skyrim.esm       SignWRBlacksmith01
                                           Whiterun, Warmaidens          overrides upstream
  00038228.json                          0x038228~Skyrim.esm       SignRiverwoodBlacksmith01
                                           Riverwood, Alvor              overrides upstream
  000EA623.json                          0x0EA623~Skyrim.esm       SignRTBlacksmith01
                                           Riften, Scorched Hammer       overrides upstream
  0x03BD5E-DLC2SignRRBlacksmith01.json   0x03BD5E~Dragonborn.esm   Raven Rock, Glover Mallory
                                           (ours already - raised 1.0 to 3.0)

Raven Rock is on the list because its record points at the Riften mesh, so WiZkiD replaced
it too.

There is no Windhelm blacksmith sign. WiZkiD ships the mesh
meshes\clutter\signage\windhelm\SignWHBlacksmith01.nif and vanilla has it in Meshes0.bsa,
but NO record in the load order references that path - checked every MSTT and STAT. Nothing to configure.

To retune: windSensitivity scales the push force linearly. The hinge constraint caps the
swing, so past a point the sign just rides its stop. Upstream's own range is 0.1 to 2.0.
