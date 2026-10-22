# 60 BEEING FEMALE FAMILY - trigger rows (prefix BF, BF1-BF100, 100 talks)

Script: `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\60 BEEING FEMALE FAMILY.txt`.
Sources: `STYLE-GUIDE.md`, `TRIGGERS.md` sections 2-4 and 8, `triggers\47b KAIDAN AND LUNA DEEP 2.md` (K04 steps), `triggers\53 RIVALRY.md` (`G_PAST`, `V_PAST`, `S_PAST`, `A_PAST`), `triggers\20 DAWNGUARD.md` (Serana/Ashe Free rows, `SERANA`, `SER_VAMP`, `ASHE_REVEAL`), `triggers\21 HEARTHFIRE AND HOME.md` (`HOUSE`, `HOUSE_LEAVE`), `Notes and Files\BEEING FEMALE PLAN.txt` sections 6b, 9 and 10.
Everything also obeys TRIGGERS.md section 2 (`WorldQuiet`), Kaidan's set pieces (kaidan_block.md §2b items 1-11, KaiSTFUQuest / STFUVarNPCGeneral), and section 3 (`Free`). Marks: **[UNC]** = unconfirmed, check at build.

Speakers: K Kaidan, G Gore, V Val, R Remi, X Xelzaz, I Inigo, L Lucien, C Redcap, S Serana, A Ashe, P Luna (the player; no Free check, but a talk with P lines still needs the player not in dialogue).
Type: T = timer, E = event (fires on the moment).
Every row with S also needs `SERANA` and Serana Free; every row with A also needs `ASHE_HIRED` and Ashe Free (20 DAWNGUARD.md §1).

## 1. The base gate on every row: `BF_ON`

`BF_ON` = all of:
- `K04 (06D900:0Kaidan.esp) >= 75` (committed lovers, engaged or married) OR `KaidanRef GetInFaction PlayerMarriedFaction == 1`. A romance pause (K04 reset) fails it.
- `GetStageDone K01 30 == 1` and Kaidan not dead. Rows where Kaidan speaks also need Kaidan Free; rows without him do not.
- **HARD RULE (user 10-21):** if Luna is pregnant or in labour and the recorded father is NOT Kaidan, every BF row is blocked, including the child rows. Only Kaidan's pregnancies and Kaidan's children ever produce a BF talk.

## 2. New gate codes (all kept by the banter controller from Beeing Female NG)

The controller listens to BF's conception / labour / birth events (plan §9) and keeps its own flags. Kaidan = his ActorBase from `0Kaidan.esp` **[UNC: FormID; compare by ActorBase, not ref]**.

| Code | Meaning | Source |
|---|---|---|
| `BF_KF` | the current pregnancy's recorded father is Kaidan (built into every pregnancy code below) | BF father record on the pregnancy |
| `BF_T1` | 1st trimester, `BF_KF` | BF pregnancy faction on the player, rank 4 |
| `BF_T2` | 2nd trimester, `BF_KF` | rank 5 |
| `BF_T3` | 3rd trimester, `BF_KF` | rank 6 |
| `BF_T2+` | `BF_T2` or `BF_T3` (belly showing; P.A.I.A hand-on-belly idle from here) | ranks 5-6 |
| `BF_PREG` | any of `BF_T1/T2/T3` | ranks 4-6 |
| `BF_T1NEW` | `BF_T1` and the controller's own count of game days since it first saw rank 4 is 0..10 ("just found out") | controller float `FB_BFConceiveDay` set when rank 4 first appears **[UNC: BF may expose a "player knows" state; if so, use it instead]** |
| `BF_LABOUR` | in labour, `BF_KF` | rank 7 (or BF labour event) |
| `BF_BIRTH` | event: a child is born and its recorded father is Kaidan | BF birth event (father + child) |
| `BF_KIDS n` | number of living BF children whose recorded father is Kaidan (`2+` = two or more) | controller int, +1 on each `BF_BIRTH` |
| `BF_DAYS a..b` | game days since the most recent Kaidan `BF_BIRTH` | controller float `FB_BFLastBirthDay` |
| `BF_NEWBORN` | `BF_DAYS 0..2` | |
| `BF_BABY` | youngest Kaidan child is 0..29 days old (small, growing a little each day) | `BF_DAYS 0..29` |
| `BF_CHILD` | at least one Kaidan child is 30+ days old (full child size) | birth day of the eldest Kaidan child |
| `BF_SECOND` | `BF_PREG` and `BF_KIDS 1+` (expecting again) | |
| `BF_KIDNEAR` | a Kaidan BF child actor is loaded, in the player's cell and within 1500 units | child ref from the birth event, stored by the controller **[UNC: BF child ref persistence / RS Children actor]** |
| `BF_KIDAWAY` | no Kaidan BF child actor in the player's cell or worldspace | |
| `K_AKAVIRI` | Kaidan has learned of his mother and the Akaviri (his "All of this Past" relic quest `KINV` completed) | **[UNC: KINV EditorID/stage; plan says the cache quest ends with his mother's letter]** |

Other codes reused unchanged: `G_PAST`, `V_PAST`, `S_PAST`, `A_PAST` (53 RIVALRY.md), `G_TOG+`, `V_TOG+`, `A_LOVE`, `V_BOAT` (47b), `SERANA`, `SER_VAMP`, `ASHE_HIRED`, `ASHE_REVEAL`, `LUC_ADMIT`, `ARCH`, `INN`, `CAMP`, `NIGHT`, `MORNING`, `SNOW`, `RAIN`, `STORM`, `CRYPT`, `WILD`, `HOUSE`, `HOUSE_LEAVE`, `AFTERFIGHT`, `AFTERFIGHT:bandit`, `after:X` (including `after:KL346`, `after:KL347` from 47b).

New event hooks:
- `AFTERFIGHT:mudcrab` = last combat target was MudcrabRace **[UNC]**; fallback plain `AFTERFIGHT`.
- `player casts a Restoration heal on self` = player spell cast event with a RestoreHealth effect on self **[UNC hook]**; fallback timer.

## 3. Per-talk table

| ID | Speakers | Type | Gates |
|---|---|---|---|
| BF1 | P K | E first tick of BF_T1NEW | BF_ON; BF_T1NEW; first pregnancy (BF_KIDS 0) |
| BF2 | G K | T | BF_ON; BF_T1; after:BF1 |
| BF3 | I K | T | BF_ON; BF_T1; after:BF1 |
| BF4 | K P | T | BF_ON; BF_T1; WILD; after:BF1 |
| BF5 | V K | E AFTERFIGHT:mudcrab (fallback AFTERFIGHT) | BF_ON; BF_PREG; after:BF1 |
| BF6 | K P | T | BF_ON; BF_T1; after:BF1 |
| BF7 | K L | T | BF_ON; BF_T1; after:BF1 |
| BF8 | X P | E MORNING | BF_ON; BF_T1; after:BF1 |
| BF9 | S K | E CAMP or INN | BF_ON; BF_T1; SERANA; after:BF1 |
| BF10 | K P | T | BF_ON; BF_PREG; K_AKAVIRI |
| BF11 | K I | T | BF_ON; BF_T1; after:BF3 |
| BF12 | P K | T | BF_ON; BF_PREG; after:KL346; after:BF1 |
| BF13 | K C | T | BF_ON; BF_T1; after:BF1 |
| BF14 | A K | E SNOW | BF_ON; BF_PREG; ASHE_HIRED; after:BF1 |
| BF15 | G K | E CRYPT | BF_ON; BF_PREG; after:BF2 |
| BF16 | R K | T | BF_ON; BF_T1; after:BF1 |
| BF17 | K P | T | BF_ON; BF_T1; after:BF1 |
| BF18 | K X | T | BF_ON; BF_PREG; after:BF1 |
| BF19 | L K | T | BF_ON; BF_PREG; after:BF7 |
| BF20 | P K | E first tick of BF_T2 | BF_ON; BF_T2; first pregnancy (BF_KIDS 0) |
| BF21 | C P | T | BF_ON; BF_PREG; after:BF13 |
| BF22 | K C | E CAMP | BF_ON; BF_PREG; after:BF13 |
| BF23 | R X | T | BF_ON; BF_PREG; after:BF2 |
| BF24 | L P | T | BF_ON; BF_PREG; after:BF1 |
| BF25 | I P | T | BF_ON; BF_T2+; after:BF3 |
| BF26 | G K | T | BF_ON; BF_PREG; G_PAST; not G_TOG+; after:BF2 |
| BF27 | G P | E CAMP or INN | BF_ON; BF_PREG; after:BF2 |
| BF28 | V P | T | BF_ON; BF_PREG; after:KL347 |
| BF29 | V K | T | BF_ON; BF_PREG; V_PAST; not V_TOG+; V_BOAT |
| BF30 | S P | T | BF_ON; BF_PREG; S_PAST; SERANA |
| BF31 | S K | T | BF_ON; BF_PREG; SERANA |
| BF32 | A K | T | BF_ON; BF_PREG; ASHE_HIRED; after:BF6 |
| BF33 | A P | T | BF_ON; BF_PREG; A_PAST; not A_LOVE; ASHE_REVEAL |
| BF34 | S A | E CAMP+NIGHT | BF_ON; BF_PREG; SERANA; ASHE_REVEAL |
| BF35 | L X | T | BF_ON; BF_PREG; after:BF18 |
| BF36 | K R | E HOUSE or INN | BF_ON; BF_PREG; after:BF16 |
| BF37 | L K | T | BF_ON; BF_PREG; LUC_ADMIT |
| BF38 | G R | E CAMP+NIGHT | BF_ON; BF_PREG; after:BF2 |
| BF39 | I K | T | BF_ON; BF_T2+; exterior, no RAIN/STORM; after:BF3 |
| BF40 | G C | E CAMP+NIGHT | BF_ON; BF_PREG; after:BF13 |
| BF41 | V G | E INN | BF_ON; BF_PREG; after:BF2 |
| BF42 | R X | T | BF_ON; BF_PREG; after:BF23; Remi/Xelzaz not fallen out |
| BF43 | A C | E CAMP+NIGHT | BF_ON; BF_PREG; ASHE_REVEAL; after:BF13 |
| BF44 | V P | T | BF_ON; BF_PREG; after:BF5 |
| BF45 | L R | T | BF_ON; BF_PREG; after:BF23; after:BF24 |
| BF46 | K P | E player casts a Restoration heal on self (fallback T) | BF_ON; BF_PREG; after:BF1 |
| BF47 | L P | T | BF_ON; BF_T2+; not ARCH |
| BF48 | P K | T | BF_ON; BF_PREG; after:BF1 |
| BF49 | A P | T | BF_ON; BF_T2+; after:BF32 |
| BF50 | P K | T | BF_ON; BF_T2+; after:BF6 |
| BF51 | I P | E CAMP or HOUSE | BF_ON; BF_T2+; after:BF1 |
| BF52 | G P | T | BF_ON; BF_T2+; WILD; after:BF20 |
| BF53 | P X | T | BF_ON; BF_PREG; after:BF18 |
| BF54 | K P | E AFTERFIGHT:bandit | BF_ON; BF_T2+; after:BF20 |
| BF55 | S P | E INN or HOUSE | BF_ON; BF_T2+; SERANA |
| BF56 | P L | T | BF_ON; BF_T2+; after:BF24 |
| BF57 | P K | E HOUSE or INN | BF_ON; BF_T2+; K_AKAVIRI; after:BF10 |
| BF58 | R P | T | BF_ON; BF_T2+; after:BF16 |
| BF59 | K P | T | BF_ON; BF_T3; after:BF1 |
| BF60 | G K | T | BF_ON; BF_T3; after:BF2 |
| BF61 | P K | E BF_LABOUR start | BF_ON; BF_LABOUR |
| BF62 | G X | E BF_LABOUR (second talk, if labour is still going) | BF_ON; BF_LABOUR; after:BF61 |
| BF63 | A K | E BF_LABOUR (second talk, if labour is still going) | BF_ON; BF_LABOUR; ASHE_HIRED; after:BF61 |
| BF64 | K P | E BF_LABOUR (second talk, if labour is still going) | BF_ON; BF_LABOUR; after:BF61 |
| BF65 | K P | E BF_BIRTH | BF_ON; BF_NEWBORN; BF_KIDS 1 |
| BF66 | K P | T | BF_ON; BF_BABY; BF_DAYS 0..5; after:BF12 |
| BF67 | C P | E BF_KIDNEAR | BF_ON; BF_BABY; BF_DAYS 0..3; after:BF13 |
| BF68 | L I | T | BF_ON; BF_BABY; BF_DAYS 0..7; after:BF24; after:BF35 |
| BF69 | I K | E NIGHT + BF_KIDNEAR | BF_ON; BF_BABY; BF_DAYS 0..3 |
| BF70 | V K | T | BF_ON; BF_BABY; BF_DAYS 0..7; after:BF44 |
| BF71 | A L | E HOUSE + BF_KIDNEAR | BF_ON; BF_BABY; BF_DAYS 3..25; ASHE_HIRED |
| BF72 | P K | E HOUSE | BF_ON; BF_BABY or BF_CHILD; after:BF19 |
| BF73 | I P | E HOUSE + BF_KIDNEAR | BF_ON; BF_BABY or BF_CHILD |
| BF74 | K C | T | BF_ON; BF_BABY (BF_DAYS 5+) or BF_CHILD; after:BF67 |
| BF75 | G K | T | BF_ON; BF_BABY; BF_DAYS 5..29 |
| BF76 | A K | E HOUSE, first tick at BF_DAYS 30+ | BF_ON; BF_CHILD; BF_DAYS 30..35; after:BF71 |
| BF77 | L K | T | BF_ON; BF_BABY or BF_CHILD |
| BF78 | S P | E HOUSE + BF_KIDNEAR | BF_ON; BF_BABY or BF_CHILD; SER_VAMP |
| BF79 | V K | E HOUSE_LEAVE | BF_ON; BF_BABY or BF_CHILD |
| BF80 | X K | E CAMP+NIGHT + BF_KIDAWAY | BF_ON; BF_BABY or BF_CHILD |
| BF81 | R P | T | BF_ON; BF_CHILD; after:BF53 |
| BF82 | R K | E HOUSE + BF_KIDNEAR | BF_ON; BF_BABY or BF_CHILD; after:BF23 |
| BF83 | G K | T | BF_ON; BF_BABY or BF_CHILD; after:BF9 |
| BF84 | K G | E HOUSE + BF_KIDNEAR | BF_ON; BF_CHILD; after:BF27 |
| BF85 | V I | E SNOW | BF_ON; BF_CHILD |
| BF86 | K P | E HOUSE+NIGHT + BF_KIDNEAR | BF_ON; BF_BABY or BF_CHILD |
| BF87 | I X | E HOUSE | BF_ON; BF_BABY or BF_CHILD |
| BF88 | A K | E HOUSE | BF_ON; BF_CHILD; ASHE_HIRED |
| BF89 | L C | T | BF_ON; BF_BABY or BF_CHILD |
| BF90 | K I | T | BF_ON; BF_CHILD |
| BF91 | P K | E first tick of BF_T1NEW | BF_ON; BF_SECOND; BF_T1NEW; after:BF1 |
| BF92 | G K | T | BF_ON; BF_SECOND; after:BF91 |
| BF93 | R P | E HOUSE | BF_ON; BF_SECOND |
| BF94 | V A | T | BF_ON; BF_SECOND; ASHE_HIRED; after:BF28 |
| BF95 | A P | T | BF_ON; BF_SECOND; after:BF32 |
| BF96 | C K | T | BF_ON; BF_SECOND; after:BF21 |
| BF97 | X K | T | BF_ON; BF_SECOND; after:BF50 |
| BF98 | K P | E BF_BIRTH | BF_ON; BF_NEWBORN; BF_KIDS 2+ |
| BF99 | G V | E HOUSE + BF_KIDNEAR | BF_ON; BF_KIDS 2+; BF_BABY |
| BF100 | K P C | E HOUSE | BF_ON; BF_KIDS 2+; after:BF98 |

## 4. Notes for the build
- Labour (BF61-BF64): BF61 fires first on the labour event and skips the 300 s cooldown; at most ONE of BF62/BF63/BF64 follows, and only if labour is still running after the cooldown. If BF's labour or birth locks the controls or plays an animation, `WorldQuiet` blocks them, which is fine. **[UNC: BF labour length and control lock]**
- Births: BF65 plays only for the first Kaidan child (`BF_KIDS 1`), BF98 for the second or later (`BF_KIDS 2+`). Only one birth talk per birth.
- Day 30: BF76 is the "full size" moment; it should fire on the first HOUSE visit with `BF_DAYS 30..35`, only if BF71 (the doorframe) played.
- First pregnancy vs later: BF1 and BF20 need `BF_KIDS 0`; BF91-BF97 need `BF_SECOND`. Part 1-3 rows may also play in a later pregnancy if they never played in the first one (they're written so they still make sense), except BF1 and BF20.
- Rival rows BF26, BF29, BF30, BF33 need the rival's romance to have started (`*_PAST`) and the rival NOT currently together with Luna. Luna never chooses anyone in them.
- Nothing here retells Kaidan's scripted beats. No cult, Rosalind, tattoo or Brynjar. His mother's people only in BF10 and BF57 (`K_AKAVIRI`).
- Nobody names the child or says boy or girl; BF and the player decide those. The child is "they", "the bairn", "the little one", "the sprog".
- Same-event priority at HOUSE: only one BF HOUSE talk per visit.
- Existing coverage avoided: 47/47b married rows (KL346 names list and KL347 betting book are only paid off here), 21/21b Hearthfire (adopted kids, uncle Gore, wooden sword, hide and seek, tiny centurion). `dup_scan.py` shows no repeated 6+ word line and no repeated title involving BF1-BF100. `qa_check.py`: 0 flags.


## Confirmed 2026-10-21 (from the BF install)
- Father check: compare BF's stored father with Kaidan's base NPC `002F9A:0Kaidan.esp` (editorid 00Kaidan). Kaidan's race in this load order is VorstagRace (Akaviri, `HSFVorstag.esp:FA1`).
- Labour length: BF setting Global_Duration_09_LaborPains = 0.18 days (about 4 in-game hours).
- Baby -> full child: 30 in-game days (BF default 50 x MatureTimeScale 0.6); children never grow up (GrowUpToAdult off).
- Children are protected (Global_ProtectedChildActor = true).
