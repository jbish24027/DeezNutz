# Authoria clothing audit and proposed revision

19 October 2026 · profile **DEEZ CS NUTZ - PICTA** · read-only audit. No outfit installations, builds or distribution changes were made.

## Result: Ysolda remains the only identified race/model-support failure

Checked all **126 explicitly targeted Northern Folk NPCs**, their **49 assigned outfits**, **74 clothing items** and **103 armor addons**, using the load-order winners after the supported SkyPatcher layer. Checked **234 required male/female weight-endpoint mesh paths** through MO2's virtual filesystem: **all present**, no archive-read failures.

- **125 recipients pass the explicit race, sex-specific model and file-presence checks.** This includes their assigned accessories, not only their torso clothing.
- **Ysolda fails:** her UBE race has no supported addon for the assigned Blue Nordland bunad or white-blue stockings/boots. Her separate Helga SPID assignment also requires the previously identified UBE repair.
- Six recipients have templates, but their template flags do not inherit traits or inventory; no additional inheritance ambiguity was identified for this check.
- Mesh winners: 228 paths from Northern Folk, two from Ophelia Accessories and four from Pelts 'o' Plenty.

**This does not prove the other 125 are clothed in the running save.** The audit verifies records and asset presence, not actual equipped inventory, full NIF rendering integrity, clipping or every runtime distributor. SPID and saved outfit state can change the effective clothing. Treat this as a completed static audit with an in-game acceptance check outstanding.

## Existing outfit conflicts to resolve deliberately

The current SkyPatcher post-state assigns Northern Folk to all 126. The following existing rules also target members of that set:

| NPC | Existing assignment | Proposed decision |
|---|---|---|
| Ysolda | Helga SPID plus Northern Folk | Repair and use UBE Helga temporarily; only switch to Northern Folk after its UBE conversion passes. |
| Kerah | Kreiste Merchantress SPID | Preserve Merchantress; enrich with a compatible accessory rather than replacing her outfit. |
| Orgnar, Thoring, Dagur | Kreiste Publican SPID | Preserve Publican and add individually suitable accessories. |
| Camilla Valerius | Authoria Haberdashery SkyPatcher | Protect the authored outfit by default; compare it with the regional option before deliberately changing her. |
| Muiri | Authoria's specific Muiri outfit patch | Protect the authored outfit by default. Preserve the face you confirmed good independently of this clothing choice. |
| Nenya, Aslfur, Jorleif | Stewards of Skyrim SkyPatcher | Preserve their professional steward outfits; use accessories for regional detail. |

These are **assignment conflicts, not additional confirmed nudity cases**. The SPID choices are potential runtime overrides; the tool's SkyPatcher post-state does not establish which outfit a spawned actor wears after SPID processing.

Reviewed winning root SPID configuration files from 100 active filenames and the 29 files under the NPC SkyPatcher directory. The local script saved 185 candidate distribution lines for review. This is a targeted rule review, not a full SPID emulator. Other named/faction outfit rules reviewed mainly target bandits, witches, Khajiit caravans or mod-specific actors. The latest SPID log did not provide per-NPC evidence for the relevant Publican/Merchantress/Helga assignments.

The outfit-overlay read also reported unrelated, unrecognized NPC keys in an outfit-folder New Leather Armor INI. Their application is unresolved; they were not repaired or used as evidence of a clean global distribution layer.

## Proposed distribution design

**Keep the cultural variety. Protect deliberate unique outfits. Add detail without replacing the whole wardrobe.**

1. **Named exceptions first.** Keep a manifest for each curated NPC: base outfit, body type, accessories, distributor and reason. Remove competing assignments for that NPC rather than relying on accidental rule precedence.
2. **Occupations next.** Publican for the appropriate barkeepers, Merchantress and other existing merchant sets for merchants, Stewards for stewards, Cultural Bards for bards. Retain unique follower/quest outfits and custom NPC resources unless explicitly replaced.
3. **Regional Northern Folk elsewhere.** Preserve the combinations you like. Replace only the disliked male pointed-collar jacket combinations in the Rift, Falkreath and Reach after identifying the exact meshes visually; do not remove the whole mod or all men's regional clothing.
4. **Accessories last.** Build intentional combinations suited to the individual and job. Keep existing hair, hats, circlets, cloaks and unique equipment. Check slots, body/race support, silhouette and clipping before adding anything. NPCs already adequately accessorized remain as they are.
5. **Test one small group before expansion.** Ysolda, Hulda, Valga, one Publican wearer, Kerah, one bard, and one replacement male regional look. The existing Fralia SMP prototype remains a separate prerequisite for expanding Northern Folk cloth physics.

### Accessory palette already available

- Northern Folk headscarves/bonnets commonly occupy **31 and 42**; headbands and the Ophelia pieces inspected occupy **42**. Do not stack these onto an occupied circlet/headwear slot or hide a deliberately chosen hairstyle unintentionally.
- The wolf pelt cloak used by this distribution occupies **57**. Check existing cloak/back equipment before assigning it, and inspect actual physics before advertising it as SMP.
- Cultural Bards provides fur cloaks, a Redguard cape and other accessories. Its author says fur cloaks/cape can be mixed, while wanderer gear is specially fitted to the wanderer outfit. Armlets and bracelets use **58/59**. Reuse only combinations that fit; no blanket backpack or cape assignment.
- Indoor barkeepers: favor small accents, apron/belt detail or jewelry over a long cape that intersects the counter. Outdoor merchants/travelers: consider a short cape/pelt where compatible. These are design proposals, not new installed assignments.

### Replacing the pointed-collar men's looks

Prepare a small visual comparison of the current relevant male meshes against existing Publican, suitable merchant/Steward and Northern Folk tunic alternatives. Known current examples to include in the Falkreath review are Solaf (Beltestakk Blue), Dengeir (Hardanger Green/Black) and Aslfur (Romerike Raven). **Their exact collar appearance has not yet been visually verified; these are review candidates, not confirmed offending meshes.** Keep status/occupation distinctions and avoid giving every man a barkeeper uniform. Final named assignments follow the visual identification step.

## Hulda and Falkreath: Bell Wild West

**Named targets: Hulda and Valga Vinicia**, the Falkreath innkeeper. Narri is a separate inn worker and is not included in this requested assignment. Local records confirm Hulda is Nord and Valga Imperial; neither currently requires a UBE build.

- Candidate base: **Bell Wild West 3BA v1.1**, not the BHUNP or SOM alternatives. A separate UBE conversion exists for required compatible coverage.
- **Compatibility gate:** the source page specifically requires FSMP **2.5.1 or lower for the skirt**, whereas the earlier Authoria runtime check reported **3.5.0**. Test the source rig/XML against the current runtime and repair locally if necessary. Do not downgrade the shared FSMP installation for one outfit.
- Use a deliberate complete combination, provisionally the opaque shirt and a skirt colour suited to each NPC. Include a final preview; the pack also contains transparent/optional pieces that should not be selected accidentally by a batch outfit rule.
- Valga currently appears in the existing Merchantress SPID rule with Carlotta, Haelga, Sayma and Kerah. Exempt **Valga only** when implementing Bell. Preserve the other four merchant assignments.
- Do not install the broad Tavern Workers SPID add-on: the requested scope is two named NPCs. Provide morph-enabled SMP outputs and applicable Requiem/UBE integration. The base is female-only; HIMBO is inapplicable unless a male adaptation is deliberately added.

Sources: [Bell Wild West](https://www.nexusmods.com/skyrimspecialedition/mods/151612), [UBE conversion](https://www.nexusmods.com/skyrimspecialedition/mods/153469).

## Cultural Bards

- Use the original **v2.0 plus v2.0 hotfix**, with one texture-resolution choice. Half resolution is the proposed default for a large everyday gameplay list; full resolution is an optional visual preference, not a compatibility requirement.
- The original supplies CBBE/HIMBO meshes and a named bard distribution. The **3BA v1.5 conversion describes body physics**, not confirmed loose cloth SMP. Check the conversion against the v2.0 source/hotfix before building.
- **Do not mark this complete on the strength of “3BA physics.”** Inspect skirt/cape rigs and author the missing cloth SMP. Preserve the mod's distinct bard combinations, applicable HIMBO support and add UBE coverage where required.
- Check required Creation Club assets and existing Bards Reborn clothing/quest rewards before enabling any distribution. Do not automatically use the expanded distribution labelled for runtime 1.6.1170 without verifying the game's runtime and need for it.

Sources: [Cultural Bards](https://www.nexusmods.com/skyrimspecialedition/mods/133000), [3BA conversion](https://www.nexusmods.com/skyrimspecialedition/mods/133265).

## Files, validation and next implementation batch

Machine-readable results and source exports are in `_staging/`: `cnf-compatibility-audit.json`, `cnf-recipients-post.jsonl`, `cnf-assigned-outfits-post.jsonl`, `cnf-assigned-armor-post.jsonl`, `cnf-assigned-addons-post.jsonl`, `cnf-mesh-winners.jsonl`, and `cnf-distribution-candidates.json`. The reusable local analyzer is `audit_cnf.py` beside this report. Older exports without `assigned`/`post` are source-only inventories; do not mistake them for current runtime values.

**Suggested next batch:** prepare Ysolda's narrow UBE repair and a reviewed exception manifest protecting the existing professional/unique outfits. In parallel with that batch's planning (not additional agents), prepare the Bell compatibility trial and one Cultural Bards cloth prototype. Obtain a scoped estimate/approval before substantial implementation, as required by your usage rules.

All additions retain applicable Requiem, HIMBO, UBE and Seasons integration. Clothing-only changes introduce no spoken lines, so new Eleonora DBReV audio is inapplicable unless dialogue is added. Verify MO2/game closed before protected writes, preserve fixed order and terminal Outputs block, and keep Synthesis/Reqtificator manual. **Every final 3BA output must retain SMP and OBody morphs.**
