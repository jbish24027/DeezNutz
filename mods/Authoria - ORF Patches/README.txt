Authoria - ORF Patches
======================
Built 2026-08-19 for the DEEZ CS NUTZ profile.

WHAT THIS IS
162 keyword files that tell Outfit Recognition Framework what every piece of
modded clothing and armour in this load order looks like. 6,210 keyword
assignments across 2,821 wearable records.

Install it as a normal mod. The files must sit flat in the mod's root folder,
which is where they are. Keyword Item Distributor only reads Data root, so do
not move them into a subfolder.

THE RULE THESE FILES FOLLOW
ORF decides what an NPC says by asking "is this person wearing ANYTHING with
this tag". It pools every equipped piece. So:

  Colour and character  -> only on slot-32 outer garments.
  Shape and coverage    -> on whichever piece actually is that thing, any slot.

That is why you will not find a colour on a boot, a glove, a helmet or a cape
in here. A black boot worn with a red dress would otherwise make you register
as both black and red.

WHERE THE COLOURS CAME FROM
Not from the mod authors' assumptions. Each colour was read off the texture
this load order actually loads, resolved through the mod order including BSAs.
That matters: the mage robes here come from Robes Retexture SE, so they are
blue-grey, teal and dark red rather than the vanilla colours a patch author
would have assumed.

Colours were assigned by eye from contact sheets. A script was tried first and
measured wrong three times in four on dark textures, so it was used only for
unambiguous black, white and grey.

ADDRESSING
Every line uses FormIDs, not EditorIDs, because the Reqtificator renames
EditorIDs on Requiem-touched gear. Zero-padded FormIDs are used, matching the
DynamicFurMorph files already in this setup, and confirmed working in the
Keyword Item Distributor log.

DO NOT ALSO INSTALL
FIBBI, ORF more keywords, MEG ORF, the Ninirim ORF patch and the Cosplay Pack
ORF file are all superseded by this mod. Of their 264 files only 34 target a
mod present here, and 23 percent of their colour lines sit on helmets, boots
and capes, which pollutes the outfit reading. Install the ORF main mod and
this, nothing else.

CHECKING IT WORKED
Launch to the main menu and quit, then open
  Documents\My Games\Skyrim Special Edition\SKSE\po3_KeywordItemDistributor.log
Search for ORF_. Each keyword should report a non-zero "added to N" count.

REBUILDING
The toolchain lives in C:\1. AUTHORIA\_tools\orf. emit_patches.py regenerates
every file from the recorded colour decisions. Re-run it if you add armour
mods or change a retexture.
