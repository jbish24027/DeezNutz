# Imperial Mail — install plan (dialogue only, no world edits)

Date: 2026-08-27
Archive: `Imperial Mail - Post and Banking Service Continued-21014-2-22-1541460203.7z`
Nexus 21014, v2.22 (2018-11-05). That is the current main file. Nothing newer exists.
Status: **PLAN ONLY. Nothing installed, nothing changed.**

Goal you set: keep the banking and parcel dialogue. Do not take the cell or world edits.

---

## 1. What the plugin actually touches

I parsed `ImperialMail.esp` record by record. It holds 552 records.

**535 of them are brand new.** They belong to the mod and collide with nothing.

**17 are overrides of vanilla records.** That is the entire footprint on Skyrim:

| Count | Type | What it is |
|---|---|---|
| 6 | Worldspace | Block headers only. Not real edits. Every exterior mod carries these. |
| 9 | Cell | Nine vanilla exterior cells. |
| 1 | Navmesh info map | Registers the mod's own new navmeshes. |
| 1 | Navmesh | **Blue Palace courtyard.** This one matters. See section 3. |

It does **not** override a single NPC, faction, dialogue line, container, leveled list,
quest, or keyword from the base game or any DLC. The postmaster dialogue is delivered
entirely by new records with conditions on faction + "offers services now" + voice type.
That is why it picks up modded innkeepers automatically.

### The nine cell overrides carry 33 new references

Not one vanilla reference is edited, moved, or deleted. The mod only *adds*:

- **20 service signs** on tavern exteriors, across Solitude, Windhelm, Riften, Markarth,
  Whiterun, and the Tamriel persistent cell.
- **2 sign brackets** (Windhelm's Candlehearth Hall and one other).
- **1 door** — the Central Office entrance, in a Solitude exterior cell.
- **10 statics** — the Central Office entrance facade, in the Blue Palace courtyard.

Three new interior cells are added: the Central Office, its basement, and a utility cell.
The utility cell is not optional — it holds the 19 parcel boxes and the vendor chest. It is
an interior the player never sees. It conflicts with nothing.

---

## 2. Full reference list to disable

33 references. All of them are records the mod defines, so a patch that masters
`ImperialMail.esp` can flag them without touching anything else.

**Cosmetic — the service signs and brackets (22):**

```
0200DA84  00ServiceSign          0200DA85  01ServiceSign
0200DA86  02ServiceSign          0200DA87  03ServiceSign
0200DA88  04ServiceSign          0200DA8C  05ServiceSign
0200DA8D  06ServiceSign          0200DA9F  07ServiceSign
0200DA8E  08ServiceSign          0200DA91  09ServiceSign
0200D520  10ServiceSign          0200DA92  10ServiceSignA
0200DA93  11ServiceSign          0200DA9C  12ServiceSign
0201BBA9  13ServiceSign          0200DAA3  14ServiceSign
0200DAA2  15ServiceSign          0200DAB7  16ServiceSign
0200DAB5  17ServiceSign          0200DAB9  18ServiceSign
0200DAB4  17ServiceSignBracket   0200DAB6  16ServiceSignBracket
```

**Structural — the Central Office entrance (11):**

```
0201B970  ImperialMailOfficeExtDoor   (the door)
0201009A  0201009D  02010090  02010098  0201009E
02010097  02013465  02013F57  020100A0  0201346A   (the facade)
```

All FormIDs above are `<id>:ImperialMail.esp`.

**Navmesh override, handled by load order instead:** `000B325A:Skyrim.esm`.

---

## 3. Why the Blue Palace courtyard is the real problem

The Central Office entrance sits in `SolitudeBluePalaceCourtyard`. That cell is the most
contested exterior in your load order.

- **30 plugins** touch the cell record.
- **8 plugins** touch the courtyard navmesh. The current winner is
  `JKs BPT - LOTD patch.esp`.

Imperial Mail overrides that same navmesh with a vanilla-derived version carrying its own
door cut. If it loaded after the Blue Palace chain it would throw away the navmesh work
that JK's Blue Palace, Blue Palace Terrace, and the LotD patches built, and NPCs in the
courtyard would path over geometry that mod stack replaced.

**The fix is load order, not surgery.** Put `ImperialMail.esp` *before* the city block. Its
navmesh and its nine cell headers then lose to the city mods and change nothing. Its new
references still get placed, because references from different plugins merge additively.
Then we disable those references separately.

This means the load-order position is load-bearing. Do not move the plugin later without
re-reading this section.

---

## 4. What you lose, and one live footgun

Disabling the Central Office entrance makes the office unreachable. That costs:

1. **Personal safe rental.** Gone.
2. **The Postmaster General courier job questline.** Gone.
3. **Central Office as a delivery destination.** This one does not disappear on its own.

Point 3 is a trap worth knowing about. The mod builds its destination menu by listing every
collection point whose postmaster is alive. The Central Office assistant stays alive in the
sealed office, so **"Central Office, Solitude" will appear in the send-parcel list, and
anything shipped there is unreachable.**

I checked whether the entry could be removed cleanly. It cannot, not cheaply: the MCM script
hardcodes 19 entries across six parallel arrays, so dropping one breaks the config menu.

Options, in order of how much I'd recommend them:

- **A.** Live with it. Never pick the Central Office in the destination list. Zero risk.
- **B.** Leave the office entrance enabled after all, keep all three features, and accept
  possible clipping in one courtyard corner. The navmesh problem is already solved by the
  load-order placement, so this is purely a visual gamble. It is one archway's worth of
  geometry against JK's + Blue Palace Terrace + Grand Solitude.

You asked for no world edits, so the plan below assumes A.

---

## 5. Compatibility checks I ran

| Check | Result |
|---|---|
| SkyUILib assets (`interface/uilib/*.swf`) | **Byte-identical** to the copies SSSO 3 already ships. No conflict either way. |
| SkyUILib script (`uilib_1.pex`) | Different build date, **identical API** (same 133 strings, same four Show* functions). Either copy works. Let SSSO 3's newer one win. |
| `Interface\Translate_ENGLISH.txt_` | Trailing underscore. Inert by design. Ignore. |
| Facegen for the 3 new NPCs | Shipped with the mod, matching filenames. No dark-face risk. |
| SEQ file | Present. Start-game-enabled quests will register. |
| Open Cities optional file | Open Cities is not installed. Skip it. |
| Gold weight MCM option | You run "Authoria - No Ammo and Septim Weight". **Leave the gold weight slider off.** |
| Vanilla courier / Dapper Deliveries | No overlap. Imperial Mail never touches the vanilla courier. |
| Requiem | Nothing needs a Requiem patch. Three new NPCs will be picked up on the next Reqtificator run — the one already pending from the weapons batch. |
| Plugin slots | 228 of 254 full used → **26 free**. 3792 light used → 304 free. |
| ESL flagging | **Do not.** Compacting would renumber the three NPCs and break their facegen filenames and the SEQ. Keep it a full ESP; you have the room. |
| MCM slots | About 122 of SkyUI's 128 in use (36 MCM Helper menus in today's log, ~86 native). This adds one. Tight but fine. It will not be in any MCM Recorder recording. |

---

## 6. The optional FOMOD patches

### Beyond Skyrim - Bruma — **install it**

6 records. Two dialogue topics and four responses. **Zero cell or world edits.** It just
extends the postmaster dialogue to Bruma's innkeeper. `BSHeartland.esm` is installed.
This is exactly the shape of thing you asked for.

### Legacy of the Dragonborn — **your call, leaning yes**

Adds Auryen as a postmaster and Dragonborn Hall as a 20th delivery destination.

- I verified Auryen's record still resolves at the same FormID under LotD V6. The 2018
  addon is not stale on that point.
- World footprint is **one** service sign at the museum exterior, plus an empty
  `SolitudeRow` cell override. The sign disables the same way as the other 20.
- It replaces the core MCM script with a 20-entry build and overrides the four core quests
  and the passbook. That is by design.

It is attractive because the museum is somewhere you actually go, so it is a destination
that works — unlike the Central Office. But it does add a world edit, so it is off by
default under your stated rule.

---

## 7. Install steps

Nothing here runs until you approve it. Steps 4 and 6 need MO2 closed.

1. **Install the FOMOD.** Main Mod = yes. Bruma = Support patch. LotD = "Not needed"
   unless you take section 6's recommendation.
2. **Mod name:** `Imperial Mail - Post and Banking Service`.
3. **Mod order (left pane):** above SSSO 3, so SSSO 3's `uilib_1.pex` wins. Everything else
   in the mod is uniquely named.
4. **Plugin order (right pane):** `ImperialMail.esp` immediately before
   `Grand Solitude - The Walls of High King Erling.esp` — that is the head of the city
   block, currently line 104. `ImperialMail - Bruma.esp` directly after it.
   Remember `plugingroups` needs the matching edit or MO2 shows duplicate group headers.
5. **Author the patch:** `Authoria - Imperial Mail - No World Edits.esp`, ESL-flagged,
   mastering `ImperialMail.esp`. It sets Initially Disabled on all 33 references in
   section 2. Loads directly after `ImperialMail.esp`.
   - Verified safe: the MCM's init reads each sign's *current* enabled state to seed its
     toggles. It never force-enables. Signs shipped disabled stay disabled and show as off
     in the menu.
   - Nothing in any script property points at the door or the facade, so nothing will try
     to re-enable them.
6. **Profiles:** decide whether this goes into all four profiles or only `DEEZ CS NUTZ`.
7. **Verify before launch:** re-read the 33 references through the load order and confirm
   every one resolves as disabled, and confirm the courtyard navmesh winner is still
   `JKs BPT - LOTD patch.esp`.

Rollback is two folders and four load-order lines.

---

## 8. What you will have in game

- Talk to any innkeeper who offers services and uses a vanilla voice. Register once.
- Deposit and withdraw gold at any of them.
- Ship parcels to 18 usable collection points across Skyrim (19 listed, minus the Central
  Office), plus Bruma's inn.
- An updating passbook with your balance and outstanding collections.
- An MCM for delivery prices, passbook and withdrawal costs, and pronoun style.
- No signs on any tavern. No new door in Solitude. No navmesh change anywhere.
