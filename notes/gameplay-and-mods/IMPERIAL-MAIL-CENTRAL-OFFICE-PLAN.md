# Imperial Mail — keeping the Central Office

Date: 2026-08-27
Companion to `IMPERIAL-MAIL-INSTALL-PLAN.md` (the approved base install).
Status (2026-08-28): **DONE and verified through the live load order.** See section 8.

You approved the base plan and chose to keep the Central Office. This file is the careful
part: exactly what the office collides with, and exactly how to fix it.

---

## 1. What I measured

Not eyeballed — computed, then attacked by four independent checkers.

- Extracted the true world position of all 33 exterior objects Imperial Mail adds.
- Box-scanned all 103 plugins that touch the Solitude worldspace, plus vanilla, for every
  object in the office zone. 152 unique objects came back; I resolved the live winner and
  on/off state of every one.
- Read the actual walk-map geometry out of three plugins and diffed it triangle by triangle.

**Four things I got wrong and corrected.** Recording them because each one would have caused
real damage:

1. Wall panels were in the wrong places — Skyrim stores a wall's pivot up to 191 units away
   from the wall itself. Recomputed all seven.
2. My walk-map read claimed two triangles 3,400 units apart were neighbours. Re-tested:
   420 of 426 links are genuine, the 6 odd ones are the cross-cell links.
3. My door-link reader used an 8-byte stride where the real record is 10. That mattered
   enormously — see the next section.
4. My first fix idea, and the red-team's own recommendation, would have **orphaned JK's
   palace side door**. Caught by testing it rather than reasoning about it.
5. I had the wrong idea of how a no-walking box works. I assumed it deleted a whole
   walk-map triangle. It does not — it **carves out only the shape it covers**. Proved
   it against 311 of the base game's own boxes: some of them cover half a percent of
   the triangle they sit on, which only makes sense if the game carves. This changed
   the size and position of the box completely.
6. One of the six backing panels turned out to be unnecessary and would have **sealed
   the office door shut**. See Part 3.

---

## 2. The problem

The Blue Palace courtyard has a covered arcade down its west side. Imperial Mail builds the
office by **walling that arcade off** — seven panels in a line with a door in the middle.
Behind the wall the arcade is still there, still walkable, and in your load order it holds
**JK's Blue Palace's side entrance to the palace**, two benches, two Immersive Laundry wash
lines, columns and a statue.

That strip meets the open courtyard at **exactly two places**, and Imperial Mail blocks both:

| Opening | Where | What blocks it |
|---|---|---|
| North-west | at the office entrance | **the office doorway itself** |
| South-east | far end of the arcade | **one plain wall panel** |

The walk-map still says both are open, so characters keep trying to walk through the new
wall. One does it on a schedule: a Grand Solitude character, Thorwyn Frost-Will, has a
standing errand to sit on a bench behind that wall every day from noon to 3pm.

---

## 3. The fix

### Part 1 — reopen the south-east end
Turn off **one** wall panel: the last one, at the far south-east end, ~1,200 units from the
office door. That reopens the arcade's other doorway, so everything behind the wall becomes
reachable the normal way again.

Cost: one open archway at the far end. The vanilla arcade has open arches anyway.

### Part 2 — one no-walking box, laid along the wall
Add a single invisible no-walking box across the north-west opening, so characters stop
routing through the office doorway.

It sits **on the line of the office wall itself**, running the width of the door bay:
260 long, 80 wide, centred on the one 199-unit seam where the courtyard walk-map meets
the arcade walk-map. Because the game carves rather than deleting, this leaves walkable
ground right up to 17 units from the wall on the courtyard side — close enough to stand
at the office door — and simply removes the strip that used to run through the wall.

I tested it by walking it. Shortest route from the courtyard, in front of the office
door, to the walled-in bench:

| | route length |
|---|---|
| today | **444** — straight through the new wall |
| with the box | **3,200** — round by the reopened south-east arch, as intended |

And nothing gets stranded: every door and both benches stay reachable. I re-ran that
check on five different box sizes and all five behaved the same, so the design is not
balanced on a knife edge.

The box is a standard Bethesda device, not a hack: 441 examples in the base game, one
official Creation Club file doing this exact job.

**Size it exactly.** The stored numbers are half-measures — a box spans twice what it says.
I proved this two independent ways: my own scan of 124 base-game examples came out at a
median of exactly 0.50, and a separate check confirmed it seven more ways. Getting it
backwards doubles the box in all three directions.

I also checked that nothing else is in the box's way: across all 30 plugins that touch
that cell, the courtyard walk-map is the **only** walk-map anywhere near it. No upper
terrace, no added path.

### Part 3 — make the wall visible from behind
The plain wall panels are one-sided sheets — literally one unit thick — so from the
arcade you would see straight through them. Three bays need a backing panel: the same
vanilla piece turned to face the other way, each landing 2 units behind its partner.

**Two bays that looked like they needed one do not:**

- The **door bay** must be left alone. Imperial Mail's arch there is not a flat sheet;
  it is a proper modelled archway, 33 units thick, five pieces, 347 faces, taken from
  the palace kit. It already reads correctly from behind. A backing panel there would
  have been a solid wall across the office doorway — it would have sealed the office.
- The bay by the **south corner** is already double-sided: Imperial Mail put its own
  custom wall back-to-back with a vanilla one there.

### Part 4 — the north-west bay (resolved 2026-08-27)
Turning off the **north-west** panel as well gives JK's palace side door a direct step into
the courtyard instead of a walk down the whole arcade.

I flagged a risk earlier that the bay might be blocked by a low wall, because the walk-map
has no ground spanning it. **That risk is disproven.** Two findings:

1. **Nothing is there.** Every object within 260 units of that panel is flora, a wash line,
   an invisible sit-marker, and clutter. No wall, no railing, no step. The ground is flat
   and at the same height on both sides.
2. **Vanilla has walkable ground sitting right on that line** — two patches 15 units off it.
   Your city mods (JK's Blue Palace Terrace and Blue Palace Terrace) re-drew the walk-map in
   that corner and stopped covering it. Imperial Mail's own map drops it too.

So the bay is open, unobstructed ground that simply is not mapped for walking any more.

**What that means:** turning the panel off helps the **player only**. Players walk anywhere;
characters need the map, and nothing can put map back at runtime. So it changes nothing for
anyone's schedule or pathing either way — it is purely a question of player convenience
versus one more visible gap.

**DECIDED 2026-08-27: turn it off. REVERSED 2026-08-28: put it back.**

I predicted the open bay would read as an ordinary arcade arch. It does not. In game it
reads as an odd sunken alcove with a bench sitting in it — the arcade is only about 190
units deep there before the palace's brick wall, so you get a niche, not a passage. My
prediction was wrong and you spotted it straight away.

Panel A is back on, and it now has a backing panel of its own so the arcade side is not
see-through. Nothing else changed: panel E stays off, and it is the one that matters —
it is the only navmesh-backed way in and out of the walled arcade. Closing A costs only
a longer walk from JK's palace side door, which no character uses for pathing anyway.

With only panel E off, four bays need a backing panel — A, B, C and D. See Part 3 for the
two that turned out not to need one.

---

## 4. What the patch contains

`Authoria - Imperial Mail - Courtyard.esp`, loading directly after `ImperialMail.esp`, both
early (ahead of the city mods, per the base plan).

**Written and checked — 42 records, 28.6 KB.**

| # | Content |
|---|---|
| 21 | Imperial Mail tavern sign/bracket objects turned off (approved base plan) |
| 1 | The south-east wall panel turned off |
| 4 | New backing panels |
| 1 | New no-walking box, along the office wall at the doorway |

That is 27 objects, carried by the 9 area records and 6 region records they sit in.
The count is 21 signs, not 22, because the office's own sign stays on — see section 5.

**Make it a full plugin, not a light one.** Two reasons. A light plugin saved with the wrong
extension gets hoisted above Imperial Mail and every override in it silently does nothing.
And a new light plugin shifts light-plugin indexes, which is the thing that gutted 11 Outfit
Wheeler outfits before. A full plugin sidesteps both, for one of your 26 free slots.

**Authoring note:** the 22 signs span nine different exterior cells, and the office sign and
door are in a different cell from the office facade. The patch needs the right parent for
each — easy to get wrong.

---

## 5. Checked so you do not have to

| Question | Answer |
|---|---|
| Does turning off Imperial Mail's panels break the mod? | No. Byte-scanned the whole plugin: the ten office shell pieces are referenced by nothing — no script, no quest, no link. |
| Does the office sign need to stay on? | Yes, and it will. It is entry 13 of the sign list and the config menu deliberately has no switch for entry 13, so its state is permanent. |
| Can the invisible fire hazards by the door burn you? | No. Radius 3 units, and they sit 340 units from the door. |
| Do the wash lines attract anyone? | No. Immersive Laundry adds no characters or behaviour at all. |
| Does the Blue Palace main entrance survive? | Yes — and this was a genuine near-miss. My earlier draft had a second box at the south-east end whose likely extent reached the main door's walk-map triangle. That would have cut Elisif's entire court off from their own front door. Part 1 removes that box completely. |
| Anything else pathing into the sealed strip? | No. Scans for quests, scenes, placed actors and link chains over all 14 objects in there came back clean apart from Thorwyn. |

---

## 6. After installing — four things

1. **Around noon**, watch Thorwyn Frost-Will. She should walk around to the bench behind the
   office. If she runs at a wall, tell me.
2. **Walk into the arcade** through the reopened south-east arch and look back at the office
   wall. Stone wall, not a window. If a backing panel faces the wrong way it is a one-line
   angle change.
3. **Step out of JK's palace side door** and check you walk straight into the courtyard
   through the reopened north-west bay.
4. **Reindex Outfit Wheeler before your first launch.** Inserting two plugins early shifts
   the index of everything after them, and Wheeler stores raw indexes.

---

## 7. Honest residuals

- Which way a wall panel faces comes from its mesh; I inferred it from the kit's convention
  rather than reading raw geometry. Item 2 above settles it in seconds.
- Imperial Mail's own office door carries a stale walk-map link pointing at an unrelated
  courtyard triangle, left over from the mod's own map losing to your city mods. Harmless —
  no character uses that door, and the player's use of it does not go through that link.
- The reopened arcade is a dead-end corridor. It already is one in your load order; the
  office does not make that worse.
- Occlusion and distant-object data predate this. The office pieces are interior-kit parts
  with no distant-object models, so nothing needs regenerating.

---

## 8. Build log — 2026-08-28

**Done:**

1. Backed up the load-order files in every profile (`.bak-imperialmail-20260828`).
2. Installed the mod as `Imperial Mail - Post and Banking Service`. Main mod plus the
   Bruma patch, no Legacy addon. Checked file by file against the archive: 148 files,
   all matching.
3. Wrote the patch to `Authoria - Imperial Mail - Courtyard`. Read it back with a
   separate reader and with houseCARL: structure sound, every one of the 23 objects
   reads back as off, all 4 new objects land in the courtyard, nothing points at
   anything missing.
4. Confirmed the load-order plan still holds. The courtyard walk-map's current owner
   is `JKs BPT - LOTD patch.esp` and every plugin that could take it from Imperial Mail
   sits after the insert point, so putting Imperial Mail there changes nothing.

5. Edited the load order in all six profiles, once MO2 was closed. Second backup taken
   first (`.bak-preinsert-20260828`), because your PG Patcher run had legitimately
   changed things since the first one — rollback lands after that run, not before it.
   Order is `ImperialMail.esp`, `ImperialMail - Bruma.esp`, then the patch, immediately
   before `Grand Solitude - The Walls of High King Erling.esp`.

**Verified afterwards, through the live load order:**

- All 23 objects read back as off. The office sign reads as on, as intended.
- All 4 new objects are there, in the courtyard, with the no-walking box carrying its
  box shape and the right collision layer.
- The courtyard walk-map still belongs to `JKs BPT - LOTD patch.esp`. Imperial Mail now
  sits in that chain and loses to it, which was the whole point of the placement.
- The courtyard area record still belongs to `Occlusion.esp`.
- No broken references and no missing masters across all three new plugins.

**Profiles: six, all of them.** `DEEZ CS NUTZ - PBR` was created 2026-08-28 and is now the
main profile (it is the one MO2 currently has selected). It is backed up and included.

Full plugin slots after this goes in — all six fit, tightest first:

| profile | after | free |
|---|---|---|
| PICTA EXPERIMENT | 245 | 9 |
| DEEZ CS NUTZ | 244 | 10 |
| DEEZ CS NUTZ - PBR | 242 | 12 |
| DEEEZ NUTTZZZ | 234 | 20 |
| Requiem Reforged - NSFW | 211 | 43 |
| Requiem Reforged - Main | 203 | 51 |

The base plan's "26 free" is stale — that was measured before the recent batches.

The load-order edit itself is written and dry-run clean on all six profiles. It is
idempotent: it strips MO2's own auto-added entries first (MO2 had already dropped a
disabled Imperial Mail line into the PBR profile) and preserves each file's line endings,
which are not uniform — `plugins.txt` is LF in two profiles and CRLF in four.
