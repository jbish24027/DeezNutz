# Follower Banter - writing rules (every writer must follow these)

Goal: ~3,500 short scenes (user target 3,000-4,000) that make the party feel like a D&D adventuring party that lives in the world: they react to places, quests, Luna's choices, each other, the weather, the date, and they have running jokes and grudges that build over time.

Character sheets: `research\bibles\*.md` (read the ones for the speakers you write). Mod/quest facts: `research\content\*.md`. Gate vocabulary: `TRIGGERS.md` section 4. Already-written scripts (do not repeat their jokes or topics): the `FOLLOWER BANTER - SCRIPT *.txt` files on `C:\Users\User\Desktop\`.

## The player: LUNA (she speaks now)
- She is **Luna**. Followers call her **Luna** (Redcap calls her **Friend**). She/her.
- **Never "the Dragonborn"** unless the talk is gated `DB` (after she really killed the Western Watchtower dragon) — and even then prefer "Luna".
- **Luna speaks in about ONE THIRD of talks**, speaker label `LUNA`, voiced by Eleonora (a Nord woman's voice). Usually 1-2 short lines, often the last word. In the other two thirds the party talks about or around her.
- **Who she is (user's words):** a bit nerdy and scholarly — a **mage**; **dry and sarcastic**; **warm and playful** underneath. She reads, corrects people's lore, knows spell theory, has opinions about books. Quick deadpan comebacks, then a kind beat. She is NOT cruel.
- **Kaidan's crush: Luna is OBLIVIOUS at first.** During `K_CRUSH` she never notices or flirts back; her lines in his crush talks miss the point completely (e.g. thinks he's staring at a wolf behind her). From `K_TOG` on she's openly fond of him and teases him back.
- She is NOT the one doing the flirting in rivalry talks. Luna never commits to a romance choice, never says "I love you", never decides quest outcomes, never contradicts what the player chose in game. Keep her lines reactive and branch-neutral.
- She's bad at navigating (running joke she denies: "I'm taking the scenic route."). She loves sweet rolls (Redcap's info).

## Romance rules (user's direct instructions)
- The user almost always romances **Kaidan**. Kaidan/Luna material gets the most weight.
- Early romance stages are NOT really romantic yet: early Kaidan (`K_CRUSH`) = a huge crush. He thinks she's beautiful, sexy, awe-inspiring; he's flustered, hides it badly, tells himself "Focus, Kaidan." / "Bad Kaidan."
- **FIVE rivals for Luna: Kaidan, Gore, Val, Serana, Ashe** (user 10-18). Rivalry grows with romance; each rival's romance progress comes from their own mod (Serana: SDA romance quest chain + its on/off setting, see serana.md; Ashe: her romance, see ashe.md). Serana: dry vampire wit, centuries old, teases the boys. Ashe: denies jealousy as 'data' ('rivalry is inefficient'), then admits she's 'competitive'. Kaidan, Gore and Val are rivals for her too; rivalry grows with romance (STEP0 sizing up -> jealousy -> grudging respect). Gore: "I'm not the jealous type" (he is). Val: secure, charming, competes with wit. Kaidan: protective, jealous, glares.
- **Redcap has NO crush on Luna.** To him she's family/tribe. **Xelzaz, Inigo and Lucien have no romance with Luna** either (Xelzaz still loves Seryne; Inigo and Lucien are friends).
- Remi has her own romance in her mod but in banter she's the gossip/sister, not a rival.
- Serana's voice: the SDA recordings (Kerstyn Unger) are the clone source, by the user's personal-use decision. Ashe: Anna Rust's lines. Ashe's mod has an orphan boy named Remy: never confuse him with our Remi.
- Never invent scripted romance events that Kaidan's own mod plays (first date, first kiss, proposal content, wedding content). Banter can be about them AFTER (gated), in general terms.

## Character facts you must not break
- **Kaidan:** no beard. Geordie-flavoured English ("aye", "lad", "pet", "me" for "my", "bloody", "haway"). Swears. Horker sandwiches, bad puns. Can't sneak. Favourite season autumn, colour blue, time just before sunrise. Raised by Brynjar (only mention Brynjar after gate `BRYNJAR`). **His Dagon-cult past is LATE content — never mention the cult, Rosalind, Blooded Dawn or Dagon worship unless gated after KMDQuest completes.** His tattoo: he deflects ("a bad time"). He was the Thalmor's prisoner (fine to mention). Wanted a dog as a boy. Kyne.
- **Gore:** ~19, lanky Nord/half-Imperial, raised by the Band of the Raven mercenaries, calls people "blood", "tusk yourself", "Mara's tits", "milk drinker". Fishing, mead, hates bards. Learning to read. Sincere underneath. Mother Heide (from Helgen). Father Jo-Lee (only after `GORE_FATHER`). Not religious.
- **Val Serano:** HE/him. Half-Nord half-Dunmer, over thirty, "relic hunter, not a pirate", hates the name Valerius, "By Mephala", sweetrolls, coffee, strawberry danishes from his mum, hates hats, vain about hair, ex-Imperial Navy, crossbow he built. Served Hermaeus Mora once (say "Mora and I have history" until Val005 done). Brother Fathis (after `VAL_FATHIS` they're reconciled).
- **Remi (Remiel):** Breton thief from Wayrest, Dwemer fanatic, Scrap the spider, crossbow, "By Sheor", "Rude.", stammers when nervous, moon sugar baking, terrible cook (chaurus pie), calls Luna "adventurer" in her own mod but in OUR banter use "Luna". Hates necromancy. Fears caves collapsing.
- **Xelzaz:** Argonian, Telvanni Lawman, alchemist and food snob, dry, "*Sigh*", Jel words (beeko, beek-ojel, Xuth, Kaoc), hates Daedra worship and paid assassins, fine with necromancy, cold-blooded (hates snow), Seryne (private; he deflects), Roovi the drone, wants a tower.
- **Inigo:** blue Khajiit, first person, few contractions ("I am", "do not"), "my friend", "He he", smells things, Mr Dragonfly in a jar, spiders (loves killing them), sweetrolls, ex-skooma (handle with care), brother Fergus (dead), raised by assassins Leah and Da Vinci (Argonian). Langley. Not a romance.
- **Lucien:** young Imperial scholar, chatty British register ("marvelous", "splendid", "I say"), nervous, limericks, sweetrolls, packhorse jokes, Clive the telepathic horse (after `LUC_ADMIT`), loves Dwemer, scared of crypts/Falmer. Val stole his lunch money at school.
- **Redcap:** Riekling (NOT a goblin, hates being called one), yellow (was blue; witch Anise). One word per sentence with full stops: "Redcap. Want. Sweet roll." "fa-ka" names creatures (Dead fa-ka = draugr). Dizzydrink = alcohol. Calls Luna "Friend". Bigpig. Hates witches, cages. Big Ash Rock = Solstheim.

## Format (exactly like the existing files)
```
------------------------------------------------------------
<ID>. <SHORT TITLE IN CAPS> (<Speaker> and <Speaker>)
When: <plain words: place/moment + any gate in plain words>
------------------------------------------------------------
NAME:   line
NAME:   line
```
- Speaker labels: KAIDAN, GORE, VAL, REMI, XELZAZ, INIGO, LUCIEN, REDCAP, SERANA, ASHE, LUNA. Pad to align as in existing files.
- 2-3 speakers per talk. 4-12 lines. Most talks 5-9 lines.
- Each line is one breath for a voice actor: short sentences, under ~25 words.
- Stage directions only as "*Sigh*" (Xelzaz) or "..." pauses. No other action text.
- End on a button: a punchline or a quiet beat. Not a moral.
- Mix of tones across a file: ~50% funny, ~30% warm/character, ~20% serious/lore. Short combat barks (2-4 lines) are allowed in combat sections.
- Make it about THIS world: name the real place, NPC, quest object. The party has opinions, inside jokes and callbacks.

## Trigger line
After each talk's block, the writer also gives a table row (in a separate section at the end of the file, or a separate .md) in the TRIGGERS.md format: `| ID | speakers | T or E <event> | gates |`, using the gate codes. Event talks fire on the moment (arrival, after a fight, quest stage set). Story-dependent talks MUST carry the right "done" gate so nothing spoils or fires early.

## Don't
- Don't repeat topics already covered (see the bibles' existing-banter lists and the Desktop scripts).
- Don't have anyone say "Dragonborn" ungated, mention Kaidan's cult early, give Kaidan a beard, give Redcap a crush, or make Val "she".
- Don't give Luna romance commitments, quest decisions, or noticing Kaidan's crush before K_TOG.
- Don't write anything that contradicts a quest's actual outcome; when a quest has branches, gate per branch or keep the line branch-neutral.

## Cast additions
- **Serana** and **Ashe** join the cast. Read `research\bibles\serana.md` and `ashe.md` before writing them; until those files exist, do not write them.

## IDs and files (large-scale production)
- Each writer gets an ID prefix and a file name from `MANIFEST.md`. IDs are `<PREFIX><number>` from 1, never reused.
- Write the script file to `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\<file>.txt` and trigger rows to `C:\1. AUTHORIA\_tools\follower-banter\triggers\<file>.md`.
- Spread speakers: every follower in your scope should appear; Kaidan most; Luna in about 1/3 of talks.
- No two talks in a file on the same joke. List your topics first, then write.

## Expansion rule (8,500 target)
- Before finishing, also run `python "C:. AUTHORIA\_toolsollower-banter\dup_scan.py"` and rewrite any of YOUR talks that repeat a 6+ word line from another file (catchphrases used sparingly are OK).
- Part-2 writers: read your part-1 file in full first. New angles only.
