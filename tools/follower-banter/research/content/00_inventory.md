# Quest content inventory - follower banter research

Profile read: `DEEZ CS NUTZ - PICTA` (4,114 checked plugins + 60 implicit masters/CC). Read-only, via houseCARL `housecarl_records` (epoch e2-6f1c37c9b1e44807), 2026-10-18.

**How quests were counted.** A quest counts as a player-facing journal quest when it has at least one journal objective, or when it has a quest type set (Side, Daedric, Misc, guild etc.) and more than one stage (catches quest mods that only write journal log entries, e.g. the Walks-Distant-Sands family). Plain "Name exists" was not usable on its own: it returns 5,558 records, most of them internal (scene, dialogue, tracker, mechanic quests). Trackers, handlers, markers, tethers, test and scene quests were then dropped by name. Counts are by the plugin that DEFINES the quest; quest-expansion mods that only edit vanilla quests are listed with the vanilla quests they edit.

**Localized names.** HearthFires.esm and most Creation Club masters keep their text in .STRINGS files inside BSAs, which houseCARL could not resolve, so those quests show _(localized name, not resolved)_. The Creation title and what the quest is about are given from the Creation itself.

**Excluded on purpose:** our 8 followers (Kaidan: `0Kaidan.esp`, `Kaidan - Immersive Features.esp`, `Kaidan - Alternate Start Quest.esp`, `Kaidan pre Thalmor.esp`, `KaidanNSFW.esp`, BWB Kaidan files; Gore: `GORE.esp`, `Gore - Vigilant.esp`; Val Serano: `AX ValSerano.esp` (36 journal quests - his own pirate questline, already his content); Remiel: `HLIORemi.esp`, `HLIIRemiLOTD.esp`; Xelzaz: `BPUFXelzazFollower.esp`, `BPUFXelzazFollowerSirenroot.esp`; Inigo: `Inigo.esp`; Lucien: `Lucien.esp`; Redcap: `FA01RedcapFollower.esp`, `FARGRedcapCCGoblinsPatch.esp`), pure patches (DBM_*, LOTD_TCC_*, Authoria patches, DBVO fixes), and framework/utility quests (Shadow of Skyrim nemesis trackers, SunHelm, Requiem install/Hogithum notes, Paragliding intro, Honed Metal courier, Animated Carriage (222 named, 0 journal), Devotion, OStim, Frostfall, Apocalypse, Triumvirate, Immersive Dialogue Expansion, Wayfarer, Dreadbinder, Radiance, Sanguine's Trade tutorials, Curator's Companion storybook).


## 1. Vanilla Skyrim questlines (Skyrim.esm)

### Vanilla - Main quest (MQ)

- Plugin(s): `Skyrim.esm`
- What it is: Alduin, the Greybeards, Delphine and the Blades, Paarthurnax, Sovngarde.
- Named journal quests: **22** · Size: **L** · Suggested banter scenes: **50**

| EditorID | Name | FormID |
|---|---|---|
| `MQ101` | Unbound | `03372B:Skyrim.esm` |
| `MQ102` | Before the Storm | `04E50D:Skyrim.esm` |
| `MQ102A` | Season Unending | `02BF9C:Skyrim.esm` |
| `MQ102B` | Season Unending | `02610A:Skyrim.esm` |
| `MQ103` | Bleak Falls Barrow | `0D0800:Skyrim.esm` |
| `MQ104` | Dragon Rising | `02610C:Skyrim.esm` |
| `MQ105` | The Way of the Voice | `0242BA:Skyrim.esm` |
| `MQ105Ustengrav` | The Horn of Jurgen Windcaller | `0713DC:Skyrim.esm` |
| `MQ106` | A Blade in the Dark | `032926:Skyrim.esm` |
| `MQ201` | Diplomatic Immunity | `035D5F:Skyrim.esm` |
| `MQ201Party` | Quest to hold aliases and scenes for party | `063B57:Skyrim.esm` |
| `MQ202` | A Cornered Rat | `036191:Skyrim.esm` |
| `MQ203` | Alduin's Wall | `036192:Skyrim.esm` |
| `MQ204` | The Throat of the World | `02D515:Skyrim.esm` |
| `MQ205` | Elder Knowledge | `02D516:Skyrim.esm` |
| `MQ206` | Alduin's Bane | `036193:Skyrim.esm` |
| `MQ301` | The Fallen | `044C56:Skyrim.esm` |
| `MQ302` | Season Unending | `045923:Skyrim.esm` |
| `MQ303` | The World-Eater's Eyrie | `046EF0:Skyrim.esm` |
| `MQ304` | Sovngarde | `046EF1:Skyrim.esm` |
| `MQ305` | Dragonslayer | `046EF2:Skyrim.esm` |
| `MQPaarthurnax` | Paarthurnax | `03FA16:Skyrim.esm` |

### Vanilla - Civil War (CW)

- Plugin(s): `Skyrim.esm`
- What it is: Legion vs Stormcloaks, Jagged Crown, fort sieges, the capital battles.
- Named journal quests: **21** · Size: **L** · Suggested banter scenes: **35**

| EditorID | Name | FormID |
|---|---|---|
| `CW00A` | Imperial Introductions | `0D3C5F:Skyrim.esm` |
| `CW00B` | Stormcloak Introductions | `0E1B5A:Skyrim.esm` |
| `CW01A` | Joining the Legion | `0D517A:Skyrim.esm` |
| `CW01AOutfitImperial` | Get Outfitted | `0C349B:Skyrim.esm` |
| `CW01B` | Joining the Stormcloaks | `0E2D29:Skyrim.esm` |
| `CW02A` | The Jagged Crown | `02D75C:Skyrim.esm` |
| `CW02B` | The Jagged Crown | `02610B:Skyrim.esm` |
| `CW03` | Message to Whiterun | `0D661C:Skyrim.esm` |
| `CWCampaignObj` | Campaign for <Alias=CampaignHold> | `026F45:Skyrim.esm` |
| `CWFortObserver` | Player left fort, check if its been cleared of monsters | `0D5F08:Skyrim.esm` |
| `CWFortSiegeCapital` | The Battle for <Alias=Fort> | `087C21:Skyrim.esm` |
| `CWFortSiegeFort` | The Battle for <Alias=Fort> | `083042:Skyrim.esm` |
| `CWMission03` | A False Front | `03BCC4:Skyrim.esm` |
| `CWMission04` | Rescue from <Alias=AttackPoint> | `035A23:Skyrim.esm` |
| `CWMission07` | Compelling Tribute | `0504F0:Skyrim.esm` |
| `CWObj` | <Alias=QuestNameLocation> | `029940:Skyrim.esm` |
| `CWResolution01` | Attack <Alias=Capital> | `02B272:Skyrim.esm` |
| `CWResolution02` | Defend <Alias=Capital> | `01FA52:Skyrim.esm` |
| `CWSiegeAttackObj` | Battle of <Alias=City> | `04E857:Skyrim.esm` |
| `CWSiegeDefendObj` | Defense of <Alias=City> | `02FF95:Skyrim.esm` |
| `CWSiegeObj` | Battle for <Alias=City> | `096E71:Skyrim.esm` |

### Vanilla - Thieves Guild (TG)

- Plugin(s): `Skyrim.esm`
- What it is: Brynjolf, Mercer, the Ragged Flagon, Nocturnal, Nightingales, city influence jobs.
- Named journal quests: **33** · Size: **L** · Suggested banter scenes: **25**

| EditorID | Name | FormID |
|---|---|---|
| `TG00` | A Chance Arrangement | `021556:Skyrim.esm` |
| `TG00SP` | A Chance Arrangement Spectator Quest | `020BE7:Skyrim.esm` |
| `TG01` | Taking Care of Business | `01F326:Skyrim.esm` |
| `TG02` | Loud and Clear | `02154E:Skyrim.esm` |
| `TG02B` | Meet the Family | `084ABD:Skyrim.esm` |
| `TG02SP` | Loud and Clear Conversations | `07EB37:Skyrim.esm` |
| `TG03` | Dampened Spirits | `02154F:Skyrim.esm` |
| `TG04` | Scoundrel's Folly | `021550:Skyrim.esm` |
| `TG04Post` | Scoundrel's Folly Post | `0D3AC6:Skyrim.esm` |
| `TG05` | Speaking With Silence | `021551:Skyrim.esm` |
| `TG06` | Hard Answers | `021552:Skyrim.esm` |
| `TG07` | The Pursuit | `021553:Skyrim.esm` |
| `TG08A` | Trinity Restored | `057F99:Skyrim.esm` |
| `TG08B` | Blindsighted | `021554:Skyrim.esm` |
| `TG09` | Darkness Returns | `021555:Skyrim.esm` |
| `TG09Post` | Darkness Returns Post Quest | `0E1782:Skyrim.esm` |
| `TGBan` | Reparations | `0B03A2:Skyrim.esm` |
| `TGCrown` | No Stone Unturned | `09DD77:Skyrim.esm` |
| `TGFenceCaravan` | Thieves Guild Caravan Fence Quest | `0D8E40:Skyrim.esm` |
| `TGLarceny` | The Litany of Larceny | `04C6C2:Skyrim.esm` |
| `TGLeadership` | Under New Management | `0D7D69:Skyrim.esm` |
| `TGRBE` | The Burglary Job | `02893B:Skyrim.esm` |
| `TGRDU` | The Shill Job | `015D24:Skyrim.esm` |
| `TGRFO` | The Numbers Job | `06098E:Skyrim.esm` |
| `TGRGF` | The Fishing Job | `028922:Skyrim.esm` |
| `TGRHC` | The Sweep Job | `028936:Skyrim.esm` |
| `TGRNT` | The Bedlam Job | `060990:Skyrim.esm` |
| `TGRShell` | Thieves Guild Radiant Shell | `028923:Skyrim.esm` |
| `TGRSL` | The Heist Job | `02893E:Skyrim.esm` |
| `TGTQ01` | Silver Lining | `0799DF:Skyrim.esm` |
| `TGTQ02` | The Dainty Sload | `0799E0:Skyrim.esm` |
| `TGTQ03` | Imitation Amnesty | `0799E1:Skyrim.esm` |
| `TGTQ04` | Summerset Shadows | `0799E2:Skyrim.esm` |

### Vanilla - Dark Brotherhood (DB)

- Plugin(s): `Skyrim.esm`
- What it is: Astrid, Cicero, the Night Mother, killing the Emperor (or destroying the Brotherhood).
- Named journal quests: **30** · Size: **L** · Suggested banter scenes: **30**

| EditorID | Name | FormID |
|---|---|---|
| `DarkBrotherhoodSanctuaryRepair` | Where You Hang Your Enemy's Head... | `087BA2:Skyrim.esm` |
| `DB01` | Innocence Lost | `01EA50:Skyrim.esm` |
| `DB01Misc` | Delayed Burial | `01EA4F:Skyrim.esm` |
| `DB02` | With Friends Like These... | `01EA51:Skyrim.esm` |
| `DB02a` | Sanctuary | `022F47:Skyrim.esm` |
| `DB03` | Mourning Never Comes | `01EA52:Skyrim.esm` |
| `DB04` | Whispers in the Dark | `01EA53:Skyrim.esm` |
| `DB04a` | The Silence Has Been Broken | `02AD16:Skyrim.esm` |
| `DB05` | Bound Until Death | `01EA54:Skyrim.esm` |
| `DB06` | Breaching Security | `01EA55:Skyrim.esm` |
| `DB07` | The Cure for Madness | `01EA56:Skyrim.esm` |
| `DB08` | Recipe for Disaster | `01EA57:Skyrim.esm` |
| `DB09` | To Kill an Empire | `01EA58:Skyrim.esm` |
| `DB10` | Death Incarnate | `03CEDA:Skyrim.esm` |
| `DB11` | Hail Sithis! | `01EA59:Skyrim.esm` |
| `DBDestroy` | Destroy the Dark Brotherhood! | `0934FB:Skyrim.esm` |
| `DBEviction` | Honor Thy Family | `06F9A5:Skyrim.esm` |
| `DBrecurring` | The Dark Brotherhood Forever | `01EA5A:Skyrim.esm` |
| `DBSideContract01` | Contract: Kill Narfi | `01EA5B:Skyrim.esm` |
| `DBSideContract02` | Contract: Kill Ennodius Papius | `01EA5E:Skyrim.esm` |
| `DBSideContract03` | Contract: Kill Beitild | `01EA5F:Skyrim.esm` |
| `DBSideContract04` | Contract: Kill Hern | `01EA60:Skyrim.esm` |
| `DBSideContract05` | Contract: Kill Lurbuk | `01EA61:Skyrim.esm` |
| `DBSideContract06` | Contract: Kill Deekus | `01EA62:Skyrim.esm` |
| `DBSideContract07` | Contract: Kill Ma'randru-jo | `01EA63:Skyrim.esm` |
| `DBSideContract08` | Contract: Kill Anoriath | `01EA64:Skyrim.esm` |
| `DBSideContract09` | Contract: Kill Agnis | `01EA65:Skyrim.esm` |
| `DBSideContract10` | Contract: Kill Maluril | `01EA66:Skyrim.esm` |
| `DBSideContract11` | Contract: Kill Helvard | `01EA67:Skyrim.esm` |
| `DBSideContract12` | Contract: Kill Safia | `01EA68:Skyrim.esm` |

### Vanilla - Companions (C / CR)

- Plugin(s): `Skyrim.esm`
- What it is: Jorrvaskr, the Circle, lycanthropy, Silver Hand, Kodlak, Ysgramor's tomb. CR = radiant jobs.
- Named journal quests: **21** · Size: **L** · Suggested banter scenes: **22**

| EditorID | Name | FormID |
|---|---|---|
| `C00` | Take Up Arms | `04B2D9:Skyrim.esm` |
| `C01` | Proving Honor | `06E803:Skyrim.esm` |
| `C02` | Brotherhood | `06E804:Skyrim.esm` |
| `C03` | The Silver Hand | `01CEF4:Skyrim.esm` |
| `C04` | Blood's Honor | `01CEF5:Skyrim.esm` |
| `C05` | Purity of Revenge | `06E805:Skyrim.esm` |
| `C06` | Glory of the Dead | `01CEF6:Skyrim.esm` |
| `CR01` | Animal Extermination | `01CEEE:Skyrim.esm` |
| `CR02` | Animal Extermination | `025185:Skyrim.esm` |
| `CR03` | Animal Pelt Collection | `025230:Skyrim.esm` |
| `CR04` | Hired Muscle | `025231:Skyrim.esm` |
| `CR05` | Trouble in Skyrim | `02522F:Skyrim.esm` |
| `CR06` | Family Heirloom | `0C18E1:Skyrim.esm` |
| `CR07` | Escaped Criminal | `025250:Skyrim.esm` |
| `CR08` | Rescue Mission | `025251:Skyrim.esm` |
| `CR09` | Striking the Heart | `025252:Skyrim.esm` |
| `CR10` | Stealing Plans | `09D6FC:Skyrim.esm` |
| `CR11` | Retrieval | `09D700:Skyrim.esm` |
| `CR12` | Totems of Hircine | `0E3145:Skyrim.esm` |
| `CR13` | Purity | `0E3163:Skyrim.esm` |
| `CR14` | Dragon Seekers | `0E3156:Skyrim.esm` |

### Vanilla - College of Winterhold (MG / MGR)

- Plugin(s): `Skyrim.esm`
- What it is: Saarthal, the Eye of Magnus, Ancano and the Thalmor, Arniel's endeavor, ritual spells.
- Named journal quests: **32** · Size: **L** · Suggested banter scenes: **22**

| EditorID | Name | FormID |
|---|---|---|
| `MG01` | First Lessons | `01F251:Skyrim.esm` |
| `MG01Pointer` | College Objective Quest | `054D0A:Skyrim.esm` |
| `MG02` | Under Saarthal | `01F252:Skyrim.esm` |
| `MG03` | Hitting the Books | `01F253:Skyrim.esm` |
| `MG04` | Good Intentions | `01F254:Skyrim.esm` |
| `MG05` | Containment | `01F255:Skyrim.esm` |
| `mg06` | Revealing the Unseen | `01F256:Skyrim.esm` |
| `MG07` | The Staff of Magnus | `01F257:Skyrim.esm` |
| `MG08` | The Eye of Magnus | `01F258:Skyrim.esm` |
| `MGR01` | Tolfdir the Absent-Minded | `0266F1:Skyrim.esm` |
| `MGR02` | Out of Balance | `0266F2:Skyrim.esm` |
| `MGR10` | Enchanting Pick-Up | `028A13:Skyrim.esm` |
| `MGR11` | Restocking Soul Gems | `028A19:Skyrim.esm` |
| `MGR12` | Filling Soul Gems | `028A1E:Skyrim.esm` |
| `MGR20` | Fetch me that Book! | `028A24:Skyrim.esm` |
| `MGR20B` | Fetch me that Book! | `0BC096:Skyrim.esm` |
| `MGR21` | Shalidor's Insights | `0E0E04:Skyrim.esm` |
| `MGR30` | Aftershock | `0C1E72:Skyrim.esm` |
| `MGRAppBrelyna01` | Brelyna's Practice | `0C0416:Skyrim.esm` |
| `MGRAppJzargo01` | J'zargo's Experiment | `0958B3:Skyrim.esm` |
| `MGRAppOnmund01` | Onmund's Request | `06BC33:Skyrim.esm` |
| `MGRArniel01` | Arniel's Endeavor | `06A086:Skyrim.esm` |
| `MGRArniel02` | Arniel's Endeavor | `06A08D:Skyrim.esm` |
| `MGRArniel03` | Arniel's Endeavor | `06A097:Skyrim.esm` |
| `MGRArniel04` | Arniel's Endeavor | `06A119:Skyrim.esm` |
| `MGRejoinQuest` | Rejoining the College | `0C9A0E:Skyrim.esm` |
| `MGRitual01` | Destruction Ritual Spell | `0A4E82:Skyrim.esm` |
| `MGRitual02` | Illusion Ritual Spell | `0B3233:Skyrim.esm` |
| `MGRitual03` | Conjuration Ritual Spell | `099F27:Skyrim.esm` |
| `MGRitual04` | Restoration Ritual Spell | `0CD987:Skyrim.esm` |
| `MGRitual05` | Alteration Ritual Spell | `0D0755:Skyrim.esm` |
| `MGRRogue` | Rogue Wizard | `05A609:Skyrim.esm` |

### Vanilla - Daedric quests (DA)

- Plugin(s): `Skyrim.esm`
- What it is: 16 Daedric Prince quests: Azura, Boethiah, Clavicus Vile, Hermaeus Mora, Hircine, Malacath, Mehrunes Dagon, Mephala, Meridia, Molag Bal, Namira, Peryite, Sanguine, Sheogorath, Vaermina.
- Named journal quests: **18** · Size: **L** · Suggested banter scenes: **40**

| EditorID | Name | FormID |
|---|---|---|
| `DA01` | The Black Star | `028AD6:Skyrim.esm` |
| `DA02` | Boethiah's Calling | `04D8D6:Skyrim.esm` |
| `DA02KillObj` | Boethiah's Bidding | `052795:Skyrim.esm` |
| `DA03` | A Daedra's Best Friend | `01BFC4:Skyrim.esm` |
| `DA04` | Discerning the Transmundane | `02D512:Skyrim.esm` |
| `DA05` | Ill Met By Moonlight | `02A49A:Skyrim.esm` |
| `DA06` | The Cursed Tribe | `03B681:Skyrim.esm` |
| `DA07` | Pieces of the Past | `0240B8:Skyrim.esm` |
| `DA08` | The Whispering Door | `04A37B:Skyrim.esm` |
| `DA09` | The Break of Dawn | `04E4E1:Skyrim.esm` |
| `DA10` | The House of Horrors | `022F08:Skyrim.esm` |
| `DA11` | The Taste of Death | `02C358:Skyrim.esm` |
| `DA11Intro` | Investigate the Hall of the Dead | `07D949:Skyrim.esm` |
| `DA11IntroScene` | DA11IntroScene | `0AEC22:Skyrim.esm` |
| `DA13` | The Only Cure | `08998D:Skyrim.esm` |
| `DA14` | A Night To Remember | `01BB9B:Skyrim.esm` |
| `DA15` | The Mind of Madness | `02AC68:Skyrim.esm` |
| `DA16` | Waking Nightmare | `0242AF:Skyrim.esm` |

### Vanilla - Favors and thaneships (Favor)

- Plugin(s): `Skyrim.esm`
- What it is: Jarl and townsfolk favors, the eight thane titles, Orc stronghold intro.
- Named journal quests: **25** · Size: **M** · Suggested banter scenes: **10**

| EditorID | Name | FormID |
|---|---|---|
| `Favor001` | Delivery | `0403B0:Skyrim.esm` |
| `Favor013` | A Few Words with You | `0CA209:Skyrim.esm` |
| `Favor017` | Fight! Fight! | `0CA210:Skyrim.esm` |
| `Favor018` | Some Light Theft | `03F46A:Skyrim.esm` |
| `Favor019` | That Was Always There | `03F4EC:Skyrim.esm` |
| `Favor104` | Kill the Bandit Leader | `06FD35:Skyrim.esm` |
| `Favor109` | Kill the Vampire | `0940E0:Skyrim.esm` |
| `Favor110` | Rare Gifts | `0CA439:Skyrim.esm` |
| `Favor151` | Kill the Forsworn Leader (Jarl) | `06C824:Skyrim.esm` |
| `Favor153` | Kill the Giant (Jarl) | `090E36:Skyrim.esm` |
| `Favor154` | Kill the Bandit Leader (Jarl) | `07172A:Skyrim.esm` |
| `Favor157` | Dungeon Delving (Jarl - Hagravens) | `0A3504:Skyrim.esm` |
| `Favor158` | Dungeon Delving (Jarl - Caves) | `0940D0:Skyrim.esm` |
| `Favor204` | Dungeon Delving (Bandits) | `07105B:Skyrim.esm` |
| `Favor205` | Dungeon Delving (Caves) | `06FE37:Skyrim.esm` |
| `Favor250` | Thane of the Reach | `0A2C86:Skyrim.esm` |
| `Favor252` | Thane of Haafingar | `0A2C9B:Skyrim.esm` |
| `Favor253` | Thane of Whiterun | `0A2C9E:Skyrim.esm` |
| `Favor254` | Thane of Eastmarch | `0A2CA6:Skyrim.esm` |
| `Favor255` | Thane of Hjaalmarch | `0A34CE:Skyrim.esm` |
| `Favor256` | Thane of the Pale | `0A34D4:Skyrim.esm` |
| `Favor257` | Thane of Winterhold | `0A34D7:Skyrim.esm` |
| `Favor258` | Thane of Falkreath | `0A34DE:Skyrim.esm` |
| `FavorJarlsMakeFriends` | Making Friends and Influencing People | `087E24:Skyrim.esm` |
| `FavorOrcsIntro` | The Forgemaster's Fingers | `076335:Skyrim.esm` |

### Vanilla - Major side quests (MS / T / NN / VC / dun / Bards College)

- Plugin(s): `Skyrim.esm`
- What it is: Forsworn Conspiracy, Cidhna Mine, Blood on the Ice, Wolf Queen, Golden Claw, White Phial, Laid to Rest, Kyne's Sacred Trials, Forelhost, Gauldur, Lost Expedition, Heart of Dibella, Blessings of Nature, Bards College.
- Named journal quests: **46** · Size: **L** · Suggested banter scenes: **45**

| EditorID | Name | FormID |
|---|---|---|
| `BardsCollegeDrum` | Rjorn's Drum | `0D944F:Skyrim.esm` |
| `BardsCollegeFlute` | Pantea's Flute | `0D9431:Skyrim.esm` |
| `BardsCollegeLute` | Finn's Lute | `0D93FA:Skyrim.esm` |
| `BardsCollegePoeticEdda` | Collecting the Edda | `0E7814:Skyrim.esm` |
| `dunBlindCliffQST` | The Affairs of Hagravens | `039B3B:Skyrim.esm` |
| `dunDarklightQST` | Repentance | `03FA89:Skyrim.esm` |
| `dunForelhostQST` | Siege on the Dragon Cult | `035354:Skyrim.esm` |
| `dunFrostmereCryptQST` | The Pale Lady | `0CF915:Skyrim.esm` |
| `dunGauldursonQST` | Forbidden Legend | `0E4D31:Skyrim.esm` |
| `dunHighGateRuinsQST` | A Scroll For Anska | `0443F4:Skyrim.esm` |
| `dunHillgrundsTombQST` | Ancestral Worship | `03E897:Skyrim.esm` |
| `dunHunterQST` | Kyne's Sacred Trials | `018601:Skyrim.esm` |
| `dunIronbindQST` | Coming of Age | `06CD54:Skyrim.esm` |
| `dunLabyrinthian` | Labyrinthian | `091F1A:Skyrim.esm` |
| `dunMidden01QST` | Forgotten Names | `055977:Skyrim.esm` |
| `dunNchuandZelQst` | The Lost Expedition | `0C3709:Skyrim.esm` |
| `dunNilheimQST` | Telrav's Request | `01BAEC:Skyrim.esm` |
| `dunShipwreck04QST` | Trius' Trinket | `043BAB:Skyrim.esm` |
| `dunTrevasWatchQST` | Infiltration | `04B2A1:Skyrim.esm` |
| `dunValthumeQST` | Evil in Waiting | `03ED82:Skyrim.esm` |
| `dunVolunruudQST` | Silenced Tongues | `08ADFA:Skyrim.esm` |
| `dunYngolBarrowQST` | Yngol's Barrow | `0434A3:Skyrim.esm` |
| `MS01` | The Forsworn Conspiracy | `018B4B:Skyrim.esm` |
| `MS02` | No One Escapes Cidhna Mine | `040A5E:Skyrim.esm` |
| `MS03` | Promises to Keep | `01DA3C:Skyrim.esm` |
| `MS04` | Unfathomable Depths | `0209CA:Skyrim.esm` |
| `MS05` | Tending the Flames | `053511:Skyrim.esm` |
| `MS05KingOlafsFestival` | Tending the Flames | `06C0EA:Skyrim.esm` |
| `MS06` | The Wolf Queen Awakened | `026C4D:Skyrim.esm` |
| `MS06Start` | The Man Who Cried Wolf | `093807:Skyrim.esm` |
| `MS07` | Lights Out! | `023A64:Skyrim.esm` |
| `MS07_dunIcerunnerQST` | Icerunner | `0906D4:Skyrim.esm` |
| `MS08` | In My Time Of Need | `01CF25:Skyrim.esm` |
| `MS09` | Missing In Action | `01CF26:Skyrim.esm` |
| `MS10` | Rise in the East | `01DBFC:Skyrim.esm` |
| `MS11` | Blood on the Ice | `01F7A3:Skyrim.esm` |
| `MS11b` | Blood on the Ice | `020556:Skyrim.esm` |
| `MS12` | The White Phial | `02C258:Skyrim.esm` |
| `MS12b` | Repairing the Phial | `02499C:Skyrim.esm` |
| `MS13` | The Golden Claw | `039645:Skyrim.esm` |
| `MS14` | Laid to Rest | `025F3E:Skyrim.esm` |
| `NN01` | A Return To Your Roots | `0C9BA0:Skyrim.esm` |
| `T01` | The Heart of Dibella | `023B6C:Skyrim.esm` |
| `t02` | The Book of Love | `0211D5:Skyrim.esm` |
| `T03` | The Blessings of Nature | `01C48E:Skyrim.esm` |
| `VC01` | Seeking A Cure | `05C625:Skyrim.esm` |

### Vanilla - Town misc / freeform (Freeform, Solitude, Riften etc.)

- Plugin(s): `Skyrim.esm`
- What it is: One-step town errands, Riften's many small jobs, marriage, Skyhaven Temple tasks.
- Named journal quests: **80** · Size: **M** · Suggested banter scenes: **15**

| EditorID | Name | FormID |
|---|---|---|
| `DialogueSolitudeGuardIntro` | Recruitment Drive | `034B58:Skyrim.esm` |
| `FreeformCaravansA` | Amulet of the Moon | `0D9393:Skyrim.esm` |
| `FreeformCidhnaMineA` | Shiv | `0DB851:Skyrim.esm` |
| `FreeformDushnikhYalA` | Gharol's Message | `09976E:Skyrim.esm` |
| `FreeformFalkreathQuest01` | Lod's Lot | `093753:Skyrim.esm` |
| `FreeformFalkreathQuest02` | Runil's Dark Past | `09375A:Skyrim.esm` |
| `FreeformFalkreathQuest03` | Dark Ancestor | `0B83C3:Skyrim.esm` |
| `FreeformFalkreathQuest03B` | Dark Ancestor | `0D6986:Skyrim.esm` |
| `FreeformHeartwoodMill` | Flight or Fight | `0E3EA5:Skyrim.esm` |
| `FreeformHighHrothgarA` | The Words of Power | `0E76DE:Skyrim.esm` |
| `FreeformIvarstead01` | Lifting the Shroud | `0D9B63:Skyrim.esm` |
| `FreeformIvarstead02` | The Straw that Broke | `0D9B64:Skyrim.esm` |
| `FreeformIvarstead03` | Grin and Bear It | `0D9B65:Skyrim.esm` |
| `FreeformIvarstead04` | Climb the Steps | `0D9B66:Skyrim.esm` |
| `FreeformKarthwastenA` | Sanuarach Mine | `0622E8:Skyrim.esm` |
| `FreeformKolskeggrA` | Kolskeggr Mine | `01FD72:Skyrim.esm` |
| `FreeformKynesgroveA` | Dravynea's Frost Salts | `069043:Skyrim.esm` |
| `FreeformMarkarthD` | Delivery to Calcelmo | `075399:Skyrim.esm` |
| `FreeformMarkarthE` | Lisbet's Missing Shipment | `0753A1:Skyrim.esm` |
| `FreeformMarkarthJ` | Bothela's Discreet Delivery | `0790E1:Skyrim.esm` |
| `FreeformMarkarthL` | Skilled Apprenticeship | `06099C:Skyrim.esm` |
| `FreeformMarkarthM` | Search and Seizure | `064798:Skyrim.esm` |
| `FreeformMarkarthN` | Coated in Blood | `0647B3:Skyrim.esm` |
| `FreeformMarkarthO` | Nimhe, the Poisoned One | `053804:Skyrim.esm` |
| `FreeformMerryfairFarm` | Bow to the Master | `0E3E9B:Skyrim.esm` |
| `FreeformMorthalA` | Falion's Secret | `021891:Skyrim.esm` |
| `FreeformMorthalB` | For the Good of Morthal | `021896:Skyrim.esm` |
| `FreeformOldHroldanB` | The Ghost of Old Hroldan | `06819A:Skyrim.esm` |
| `FreeformRiften01` | Supply and Demand | `053305:Skyrim.esm` |
| `FreeformRiften02` | The Lover's Requital | `053306:Skyrim.esm` |
| `FreeformRiften03` | Under the Table | `053307:Skyrim.esm` |
| `FreeformRiften04` | Few and Far Between | `053308:Skyrim.esm` |
| `FreeformRiften05` | Spread the Love | `053309:Skyrim.esm` |
| `FreeformRiften06` | Sealing the Deal | `053318:Skyrim.esm` |
| `FreeformRiften07` | Ice Cold | `05331A:Skyrim.esm` |
| `FreeformRiften08` | Distant Memories | `05331B:Skyrim.esm` |
| `FreeformRiften09` | Grimsever's Return | `05331C:Skyrim.esm` |
| `FreeformRiften10` | Stoking the Flames | `05331D:Skyrim.esm` |
| `FreeformRiften11` | Caught Red Handed | `041F91:Skyrim.esm` |
| `FreeformRiften12` | Helping Hand | `041FD2:Skyrim.esm` |
| `FreeformRiften13` | Pilgrimage | `043E1A:Skyrim.esm` |
| `FreeformRiften14` | Hunt and Gather | `043E25:Skyrim.esm` |
| `FreeformRiften15` | Special Delivery | `0557E9:Skyrim.esm` |
| `FreeformRiften16` | Bring It! | `0557F3:Skyrim.esm` |
| `FreeformRiften17` | Truth Ore Consequences | `05B2DE:Skyrim.esm` |
| `FreeformRiften18` | Ringmaker | `05B3A5:Skyrim.esm` |
| `FreeformRiften19` | Bloody Nose | `065C30:Skyrim.esm` |
| `FreeformRiften20` | The Raid | `085D40:Skyrim.esm` |
| `FreeformRiften21` | Toying With The Dead | `09F179:Skyrim.esm` |
| `FreeformRiften22` | Stabilized | `0C1E07:Skyrim.esm` |
| `FreeformRiftenThane` | I Done Got Thaned! | `065BDF:Skyrim.esm` |
| `FreeformRiverwood01` | A Lovely Letter | `074A83:Skyrim.esm` |
| `FreeformSalviusFarmA` | Rogatus's Letter | `0931BF:Skyrim.esm` |
| `FreeformSarethiFarm` | Smooth Jazbay | `0E3308:Skyrim.esm` |
| `FreeformShipsDawnstar` | Salty Sea-Dogs | `094152:Skyrim.esm` |
| `FreeformShipsWindhelm` | Harsh Master | `094158:Skyrim.esm` |
| `FreeformShorsStone01` | Mine or Yours | `0E49E7:Skyrim.esm` |
| `FreeformShorsStone02` | Special Delivery | `0E49E8:Skyrim.esm` |
| `FreeformSkyhavenTempleA` | Rebuilding the Blades | `0E38C9:Skyrim.esm` |
| `FreeformSkyHavenTempleB` | Dragon Hunting | `0E3E67:Skyrim.esm` |
| `FreeformSkyHavenTempleD` | Dragon Research | `0E6DF1:Skyrim.esm` |
| `FreeformSoljundsSinkholeA` | Soljund's Sinkhole | `06136B:Skyrim.esm` |
| `FreeformStonehillsA` | Payment Delivery | `064958:Skyrim.esm` |
| `FreeformValdDebt` | Vald's Debt | `0C04BA:Skyrim.esm` |
| `FreeformWindhelmA` | Delivery | `0CD882:Skyrim.esm` |
| `FreeformWinterholdA` | A Bad Trade | `062F54:Skyrim.esm` |
| `FreeformWinterholdC` | Drowned Sorrows | `064EA8:Skyrim.esm` |
| `FreeformWinterholdCollegeA` | Research Thief | `05D2E9:Skyrim.esm` |
| `FreeformWinterholdCollegeB` | The Missing Apprentices | `0E357D:Skyrim.esm` |
| `RelationshipMarriage` | The Bonds of Matrimony | `074793:Skyrim.esm` |
| `RelationshipMarriageBreakUp` | Player Has Broken Up with the Love Interest | `07431B:Skyrim.esm` |
| `RelationshipMarriageWedding` | Wedding Ceremony Scene | `07404E:Skyrim.esm` |
| `RelationshipOrcs` | A Friend to the Orcs | `06819E:Skyrim.esm` |
| `SolitudeFreeform01` | No News is Good News | `0E8BD7:Skyrim.esm` |
| `SolitudeFreeform02` | Fit for a Jarl | `0C7D1C:Skyrim.esm` |
| `SolitudeFreeform03` | Return to Grace | `0C7D42:Skyrim.esm` |
| `SolitudeFreeform04` | Delivery | `0D055D:Skyrim.esm` |
| `SolitudeFreeform06` | The Spiced Wine | `0D69FB:Skyrim.esm` |
| `SolitudeFreeform07` | Elisif's Tribute | `0E77BA:Skyrim.esm` |
| `SolitudeOpening` | Solitude Dialogue | `0B2FD9:Skyrim.esm` |

### Vanilla - Bounties and radiant (BQ / WE / WI)

- Plugin(s): `Skyrim.esm`
- What it is: Jarl bounties, treasure maps, world-interaction errands.
- Named journal quests: **50** · Size: **S** · Suggested banter scenes: **6**

| EditorID | Name | FormID |
|---|---|---|
| `BQ01` | Bounty: Bandit Boss | `095125:Skyrim.esm` |
| `BQ02` | Bounty: Forsworn | `0BD77F:Skyrim.esm` |
| `BQ03` | Bounty: Giant | `0BD78C:Skyrim.esm` |
| `BQ04` | Bounty: Dragon | `0CBA9A:Skyrim.esm` |
| `WE100ObjA` | Treasure Hunter Objectives | `0A17AD:Skyrim.esm` |
| `WE100ObjB` | Treasure Hunter Objectives | `0A17B4:Skyrim.esm` |
| `WE100ObjC` | Treasure Hunter Objectives | `0A17B5:Skyrim.esm` |
| `WE100ObjD` | Treasure Hunter Objectives | `0A17B6:Skyrim.esm` |
| `WE100ObjE` | Treasure Hunter Objectives | `0A17B7:Skyrim.esm` |
| `WE100ObjF` | Treasure Hunter Objectives | `0A17B8:Skyrim.esm` |
| `WE100ObjG` | Treasure Hunter Objectives | `0A17B9:Skyrim.esm` |
| `WE100ObjH` | Treasure Hunter Objectives | `0A17BA:Skyrim.esm` |
| `WE100ObjI` | Treasure Hunter Objectives | `0A17BB:Skyrim.esm` |
| `WE100ObjJ` | Treasure Hunter Objectives | `0A17BC:Skyrim.esm` |
| `WE24` | A Good Death | `062119:Skyrim.esm` |
| `WE31` | College Application Denied | `0753CA:Skyrim.esm` |
| `WEBountyCollectorQST` | BountyCollector | `0F8A80:Skyrim.esm` |
| `WEDA02` | DA02 Hook | `04A602:Skyrim.esm` |
| `WEDL13` | Looking to join Imperials | `0BD757:Skyrim.esm` |
| `WEDL14` | Looking to join Stormcloaks | `0BD758:Skyrim.esm` |
| `WEJS02` | DB08- Finding the Gourmet | `0B5D41:Skyrim.esm` |
| `WEJS10` | DA01-Dark Elf on Pilgrimage to Azura's Shrine | `0B85B8:Skyrim.esm` |
| `WEJS11` | DA11-Namira Cultist Offers the First Bite | `0B85BD:Skyrim.esm` |
| `WEJS12` | DA01- Necromancers Attack Player | `0BA2FF:Skyrim.esm` |
| `WEJS13` | T03- Pilgrim visiting the tree in Whiterun | `0BC037:Skyrim.esm` |
| `WEJS14` | DA13 Hook, Afflicted Refugee Headed to High Rock | `0BED92:Skyrim.esm` |
| `WEJS15` | DA13- Afflicted Refugees Attack the Player | `0BEDAF:Skyrim.esm` |
| `WEJS16` | Spriggan aggravated by a hunter, now dead | `0E8921:Skyrim.esm` |
| `WEJS18` | Corpses in the aftermath of a dragon attack, Dog left behind | `0E8929:Skyrim.esm` |
| `WEJS20` | Spriggan and Hagraven Battling | `0E892D:Skyrim.esm` |
| `WEJS21` | Hunter and Dog in the Wilderness | `0E892E:Skyrim.esm` |
| `WEJS24` | Bandit Killed With Horse Left Behind | `0E8924:Skyrim.esm` |
| `WEJS25` | Wizard Duel | `0E8941:Skyrim.esm` |
| `WEJS26` | Aggressive Adventurer | `105D12:Skyrim.esm` |
| `WEJS28` | Dark Brotherhood Assassin Sent to Kill the Player | `105D19:Skyrim.esm` |
| `WERoad06` | Adventurer on the Way to Nearby Dungeon | `105D1D:Skyrim.esm` |
| `WERoad07` | Taunting Adventurer | `105D15:Skyrim.esm` |
| `WERoad09` | Skooma Dealer | `1065FA:Skyrim.esm` |
| `WIAddItem07` | Buy Dwarven artifact | `0A0F43:Skyrim.esm` |
| `WIAssault02` | Scare my Enemy | `039792:Skyrim.esm` |
| `WICastMagic01` | Invisible Child | `070217:Skyrim.esm` |
| `WICastMagic02` | Dangerous Magic | `0AB3FA:Skyrim.esm` |
| `WICastMagic03` | Shout - Guard says stop | `0167D3:Skyrim.esm` |
| `WICastMagic04` | Shout - learn about word wall | `023EE4:Skyrim.esm` |
| `WIChangeLocation03` | Wizard Duel | `06E028:Skyrim.esm` |
| `WIChangeLocation04` | Magic Student | `06F211:Skyrim.esm` |
| `WIChangeLocation05` | Gift from a friend | `070E30:Skyrim.esm` |
| `WIGamesHideAndSeek` | Hide and Seek | `04B869:Skyrim.esm` |
| `WIGamesTag` | Tag, you're it! | `0AE004:Skyrim.esm` |
| `WIKill04` | An enemy's gratitude | `071441:Skyrim.esm` |

_Other Skyrim.esm quests not grouped above (tutorials, jail, house purchase etc.) - 7, no scenes suggested: DialogueCidhnaMine, DialogueIvarsteadScriptedScene, DialogueRiftenSS01, DialogueRiftenSS02, DialogueTutorial, PerksQuest, weroad08_


## 2. DLC

### Dawnguard

- Plugin(s): `Dawnguard.esm`
- What it is: Serana, Harkon and Castle Volkihar vs Isran and Fort Dawnguard, Soul Cairn, Forgotten Vale, Auriel's Bow, Durnehviir.
- Named journal quests: **39** · Size: **L** · Suggested banter scenes: **45**

| EditorID | Name | FormID |
|---|---|---|
| `DLC01SoulCairnHorseQuest2` | Soul Cairn Horse Quest | `0163CD:Dawnguard.esm` |
| `DLC1HunterBaseIntro` | A New Order | `004E24:Dawnguard.esm` |
| `DLC1HunterBaseStage2` | Bolstering the Ranks | `013F1F:Dawnguard.esm` |
| `DLC1LD` | Lost to the Ages | `005817:Dawnguard.esm` |
| `DLC1Radiant` | "Parent" quest for Radiant Content | `004C1C:Dawnguard.esm` |
| `DLC1RH01` | Hide and Seek | `005E4A:Dawnguard.esm` |
| `DLC1RH02` | Cleansing Light | `005E53:Dawnguard.esm` |
| `DLC1RH03` | Preemptive Strike | `005E58:Dawnguard.esm` |
| `DLC1RH04` | Hunting the Monster | `006952:Dawnguard.esm` |
| `DLC1RH05` | Ancient Technology | `006BAC:Dawnguard.esm` |
| `DLC1RH06` | Rescue | `007201:Dawnguard.esm` |
| `DLC1RH07` | A Jarl's Justice | `007EC5:Dawnguard.esm` |
| `DLC1RH08` | Lost Relic | `015017:Dawnguard.esm` |
| `DLC1RV01` | The Hunt | `004C1B:Dawnguard.esm` |
| `DLC1RV02` | Culling the Beast | `0050B9:Dawnguard.esm` |
| `DLC1RV03` | Deceiving the Herd | `0050BD:Dawnguard.esm` |
| `DLC1RV04` | Protecting the Bloodline | `0056FD:Dawnguard.esm` |
| `DLC1RV05` | Ancient Power | `005702:Dawnguard.esm` |
| `DLC1RV06` | The Gift | `0058CA:Dawnguard.esm` |
| `DLC1RV07` | New Allegiances | `00A29C:Dawnguard.esm` |
| `DLC1RV08` | Rings of Blood Magic | `00CE06:Dawnguard.esm` |
| `DLC1RV09` | Amulets of Night Power | `00CE0B:Dawnguard.esm` |
| `DLC1RV10` | Destroying the Dawnguard | `019938:Dawnguard.esm` |
| `DLC1VampireBaseIntro` | The Bloodstone Chalice | `00594C:Dawnguard.esm` |
| `DLC1VampireTutorial` | Power of the Blood | `01909F:Dawnguard.esm` |
| `DLC1VQ01` | Awakening | `00352A:Dawnguard.esm` |
| `DLC1VQ01MiscObjective` | Dawnguard | `00D06C:Dawnguard.esm` |
| `DLC1VQ02` | Bloodline | `002F65:Dawnguard.esm` |
| `DLC1VQ03Hunter` | Prophet | `0098CB:Dawnguard.esm` |
| `DLC1VQ03Vampire` | Prophet | `004C3D:Dawnguard.esm` |
| `DLC1VQ04` | Chasing Echoes | `00284F:Dawnguard.esm` |
| `DLC1VQ05` | Beyond Death | `002850:Dawnguard.esm` |
| `DLC1VQ06` | Unseen Visions | `002852:Dawnguard.esm` |
| `DLC1VQ07` | Touching the Sky | `002853:Dawnguard.esm` |
| `DLC1VQ08` | Kindred Judgment | `007C25:Dawnguard.esm` |
| `DLC1VQDragon` | Durnehviir | `00C73A:Dawnguard.esm` |
| `DLC1VQElder` | Seeking Disclosure | `005DA9:Dawnguard.esm` |
| `DLC1VQFVBooks` | Forgotten Vale Books Quest | `01A3E4:Dawnguard.esm` |
| `DLC1VQSaint` | Impatience of a Saint | `01400B:Dawnguard.esm` |

### Dragonborn

- Plugin(s): `Dragonborn.esm`
- What it is: Solstheim: Miraak, Hermaeus Mora and Apocrypha, the Skaal, Raven Rock, Tel Mithryn (Neloth), Thirsk, Black Books, Ebony Warrior.
- Named journal quests: **57** · Size: **L** · Suggested banter scenes: **50**

| EditorID | Name | FormID |
|---|---|---|
| `DLC2BlackBook03Quest` | Black Book: Untold Legends | `03216C:Dragonborn.esm` |
| `DLC2BlackBook04Quest` | Black Book: The Winds of Change | `03216E:Dragonborn.esm` |
| `DLC2BlackBook05Quest` | Black Book: The Sallow Regent | `03216D:Dragonborn.esm` |
| `DLC2BlackBook06Quest` | Black Book: Filament and Filigree | `03216F:Dragonborn.esm` |
| `DLC2BlackBook07Quest` | Black Book: The Hidden Twilight | `032170:Dragonborn.esm` |
| `DLC2dunHaknirTreasureQST` | Deathbrand | `024002:Dragonborn.esm` |
| `DLC2dunKolbjornQST` | Unearthed | `01810B:Dragonborn.esm` |
| `DLC2EbonyWarriorQuest` | The Ebony Warrior | `02C49E:Dragonborn.esm` |
| `DLC2KagrumezQST` | The Kagrumez Gauntlet | `03166D:Dragonborn.esm` |
| `DLC2MH01` | Retaking Thirsk | `01A50B:Dragonborn.esm` |
| `DLC2MH02` | The Chief of Thirsk Hall | `01A50C:Dragonborn.esm` |
| `DLC2MQ01` | Dragonborn | `017F8E:Dragonborn.esm` |
| `DLC2MQ02` | The Temple of Miraak | `017F8F:Dragonborn.esm` |
| `DLC2MQ03` | The Fate of the Skaal | `017F90:Dragonborn.esm` |
| `DLC2MQ03B` | Cleansing the Stones | `035440:Dragonborn.esm` |
| `DLC2MQ04` | The Path of Knowledge | `016E1F:Dragonborn.esm` |
| `DLC2MQ05` | The Gardener of Men | `0179DE:Dragonborn.esm` |
| `DLC2MQ06` | At the Summit of Apocrypha | `0179D7:Dragonborn.esm` |
| `DLC2RR01` | March of the Dead | `018B13:Dragonborn.esm` |
| `DLC2RR02` | Served Cold | `018B14:Dragonborn.esm` |
| `DLC2RR03` | The Final Descent | `018B15:Dragonborn.esm` |
| `DLC2RR03Intro` | An Axe to Find | `020A1C:Dragonborn.esm` |
| `DLC2RR03Priest` | The Final Descent Priest | `03332A:Dragonborn.esm` |
| `DLC2RRFavor01` | Recipe for Distraction | `024DDE:Dragonborn.esm` |
| `DLC2RRFavor02` | Fetch the Netch | `024DE7:Dragonborn.esm` |
| `DLC2RRFavor03` | Clean Sweep | `024DFC:Dragonborn.esm` |
| `DLC2RRFavor04` | It's All In The Taste | `024E04:Dragonborn.esm` |
| `DLC2RRFavor05` | Pain in the Necklace | `024FA8:Dragonborn.esm` |
| `DLC2RRFavor06` | Feeding the Addiction | `024FAD:Dragonborn.esm` |
| `DLC2RRFavor07` | First Edition | `02BAC6:Dragonborn.esm` |
| `DLC2SkaalVillageFreeform1` | Skaal Village Dialogue | `02C8AA:Dragonborn.esm` |
| `DLC2SV01` | Lost Legacy | `019B4A:Dragonborn.esm` |
| `DLC2SV02` | A New Source of Stalhrim | `01CAF1:Dragonborn.esm` |
| `DLC2TGQuest` | Paid in Full | `02AD26:Dragonborn.esm` |
| `DLC2ThirskFFElmus` | Elmus Favor Quest | `038EBF:Dragonborn.esm` |
| `DLC2ThirskFFElmusBack` | Elmus Favor Quest | `038EC4:Dragonborn.esm` |
| `DLC2ThirskFFHalbarn` | Halbarn Favor Quest | `038FBC:Dragonborn.esm` |
| `DLC2ThirskFFHilund` | Hilund Favor Quest | `038FBB:Dragonborn.esm` |
| `DLC2TT1` | Reluctant Steward | `017E8D:Dragonborn.esm` |
| `DLC2TT1b` | A New Debt | `01844E:Dragonborn.esm` |
| `DLC2TT2` | Old Friends | `0195A1:Dragonborn.esm` |
| `DLC2TTF1` | From the Ashes | `01AAB0:Dragonborn.esm` |
| `DLC2TTF2` | Healing a House | `01AAC8:Dragonborn.esm` |
| `DLC2TTR1` | Lost Knowledge | `01B65F:Dragonborn.esm` |
| `DLC2TTR2` | Heart Stones | `01C06E:Dragonborn.esm` |
| `DLC2TTR3a` | Telvanni Research | `01B65D:Dragonborn.esm` |
| `DLC2TTR3b` | Wind and Sand | `01D8D1:Dragonborn.esm` |
| `DLC2TTR4a` | Experimental Subject | `01B664:Dragonborn.esm` |
| `DLC2TTR4b` | Experimental Subject | `01CDE1:Dragonborn.esm` |
| `DLC2TTR5` | Briarheart Necropsy | `01C05C:Dragonborn.esm` |
| `DLC2TTR7` | Azra's Staffs | `01BD18:Dragonborn.esm` |
| `DLC2TTR8` | Hunting and Gathering | `01F13B:Dragonborn.esm` |
| `DLC2WB01` | Filial Bonds | `0209AE:Dragonborn.esm` |
| `DLC2WE03` | Hunter and Dog in the Wilderness | `01F989:Dragonborn.esm` |
| `DLC2WE06` | Black Book | `027A14:Dragonborn.esm` |
| `DLC2WE09` | Cultists vs Player | `0331C0:Dragonborn.esm` |
| `DLC2WE12` | Frossel Bandit | `03923B:Dragonborn.esm` |

### Hearthfire

- Plugin(s): `HearthFires.esm`
- What it is: Building Lakeview Manor / Windstad Manor / Heljarchen Hall, adopting children, steward, bandit/giant/vampire attacks on the house.
- Named journal quests: **7** · Size: **M** · Suggested banter scenes: **12**
- Note: Quest names are localized; the BYOHHouse* quests are the three homesteads, BYOHRelationshipAdopt* is adoption.

| EditorID | Name | FormID |
|---|---|---|
| `BYOHHouseBanditAttack2` | _(localized or no journal name)_ | `0008A8:HearthFires.esm` |
| `BYOHHouseBuilding` | _(localized or no journal name)_ | `00305D:HearthFires.esm` |
| `BYOHHouseFalkreath` | _(localized or no journal name)_ | `00305E:HearthFires.esm` |
| `BYOHHouseHjaalmarch` | _(localized or no journal name)_ | `00BE09:HearthFires.esm` |
| `BYOHHousePale` | _(localized or no journal name)_ | `010BEE:HearthFires.esm` |
| `BYOHRelationshipAdoptable` | _(localized or no journal name)_ | `004291:HearthFires.esm` |
| `BYOHRelationshipAdoption` | _(localized or no journal name)_ | `0042B4:HearthFires.esm` |


## 3. Creation Club (all 54 CC plugins in the load order)

| CC plugin | Creation | Journal quests | Size | Scenes | What it is |
|---|---|---|---|---|---|
| `ccasvsse001-almsivi.esm` | Ghosts of the Tribunal | 6 | M | 8 | Ordinator ghosts hunt the Dragonborn; a Morrowind-themed questline through Tribunal history, Ordinator armor set. |
| `ccbgssse001-fish.esm` | Fishing | 24 | M | 5 | Fishing system plus a chain of fishing quests in every hold (Viriya / supply-run style jobs), Khajiit, Dwarven and crab chains. |
| `ccbgssse003-zombies.esl` | Plague of the Dead | 1 | S | 3 | Zombie outbreak encounters and a short investigation quest. |
| `ccbgssse004-ruinsedge.esl` | Ruin's Edge | 0 | S | 1 | Short quest for a Daedric-flavoured bow. |
| `ccbgssse006-stendarshammer.esl` | Stendarr's Hammer | 1 | S | 1 | "If I had a Hammer" - steal the hammer from a temple. |
| `ccbgssse011-hrsarmrelvn.esl` | Elven Horse Armor | 0 | - | 0 | Item only. |
| `ccbgssse012-hrsarmrstl.esl` | Steel Horse Armor | 0 | - | 0 | Item only. |
| `ccbgssse014-spellpack01.esl` | Arcane Accessories | 1 | S | 1 | "The Lost Library" - find a hidden library of spell tomes. |
| `ccbgssse019-staffofsheogorath.esl` | Staff of Sheogorath | 0 | S | 2 | "Put A Fork In It" - Sheogorath-flavoured staff hunt on Solstheim. |
| `ccbgssse021-lordsmail.esl` | Lord's Mail | 0 | S | 1 | "Gift of Kynareth" - the Emperor's letter leads to Lord's Mail. |
| `ccmtysse001-knightsofthenine.esl` | Divine Crusader | 2 | S | 3 | "Relics of the Crusader" + "The Pilgrim's Path" (pray at the nine shrines). |
| `ccqdrsse001-survivalmode.esl` | Survival Mode | 0 | - | 0 | System only. |
| `cctwbsse001-puzzledungeon.esm` | Forgotten Seasons | 3 | M | 4 | Dwemer puzzle dungeon Vardnknundr, seasonal vault, Dwarven horse and crown quests. |
| `cceejsse001-hstead.esm` | Tundra Homestead | 1 | S | 1 | Player home near Whiterun. |
| `ccbgssse018-shadowrend.esl` | Shadowrend | 1 | S | 1 | Short quest for the Shadowrend blade. |
| `ccedhsse001-norjewel.esl` | Nordic Jewelry | 1 | S | 1 | Craftsman encounter quest. |
| `ccbgssse037-curios.esl` | Rare Curios | 0 | - | 0 | Khajiit caravan ingredients, no journal quest. |
| `ccbgssse034-mntuni.esl` | Wild Horses | 9 | S | 2 | Tame wild horses across Skyrim and find the unicorn. |
| `ccbgssse045-hasedoki.esl` | Staff of Hasedoki | 1 | S | 1 | Staff quest through an ancient ruin. |
| `ccffbsse001-imperialdragon.esl` | Civil War Champions | 1 | S | 2 | Champion armor quest tied to the Civil War side you chose. |
| `ccmtysse002-ve.esl` | Vigil Enforcer Armor Set | 1 | S | 2 | Vigil of Stendarr questline for the Vigil Enforcer armor. |
| `ccbgssse043-crosselv.esl` | Elite Crossbows | 1 | S | 1 | Dawnguard vampire-hunter quest for crossbows. |
| `ccvsvsse001-winter.esl` | Saturalia Holiday Pack | 1 | S | 1 | "Saturalia Preparation" - find the Saturalia merchant. |
| `cceejsse003-hollow.esl` | Shadowfoot Sanctum | 1 | S | 1 | Thief home in the Riften Ratways. |
| `ccbgssse016-umbra.esm` | Umbra | 0 | S | 2 | The soul-stealing sword Umbra; Clavicus Vile flavour. |
| `ccbgssse040-advobgobs.esl` | Goblins | 1 | S | 2 | Goblin tribes, a goblin quest, tameable goblins. |
| `ccbgssse050-ba_daedric.esl` | Alt Armor: Daedric Plate | 2 | S | 1 | Short armor quest. |
| `ccbgssse051-ba_daedricmail.esl` | Alt Armor: Daedric Mail | 2 | S | 1 | Short armor quest. |
| `ccbgssse052-ba_iron.esl` | Alt Armor: Iron | 2 | S | 1 | "Brothers in Irons". |
| `ccbgssse053-ba_leather.esl` | Alt Armor: Leather | 2 | S | 1 | "Double-Edged". |
| `ccbgssse054-ba_orcish.esl` | Alt Armor: Orcish Plate | 2 | S | 1 | "Smith 'N Slash". |
| `ccbgssse055-ba_orcishscaled.esl` | Alt Armor: Orcish Scaled | 2 | S | 1 | "Gambler's Edge". |
| `ccbgssse056-ba_silver.esl` | Alt Armor: Silver | 2 | S | 1 | "When the Cat's Away". |
| `ccbgssse057-ba_stalhrim.esl` | Alt Armor: Stalhrim Fur | 2 | S | 1 | Short armor quest. |
| `ccbgssse058-ba_steel.esl` | Alt Armor: Steel Soldier | 2 | S | 1 | "Over the Edge". |
| `ccbgssse059-ba_dragonplate.esl` | Alt Armor: Dragonplate | 2 | S | 1 | Short armor quest. |
| `ccbgssse060-ba_dragonscale.esl` | Alt Armor: Dragonscale | 2 | S | 1 | Short armor quest. |
| `ccbgssse061-ba_dwarven.esl` | Alt Armor: Dwarven Plate | 2 | S | 1 | Short armor quest. |
| `ccbgssse062-ba_dwarvenmail.esl` | Alt Armor: Dwarven Mail | 2 | S | 1 | Short armor quest. |
| `ccbgssse063-ba_ebony.esl` | Alt Armor: Ebony Plate | 2 | S | 1 | "Heart of Crimson". |
| `ccbgssse064-ba_elven.esl` | Alt Armor: Elven Hunter | 2 | S | 1 | "Once a Hunter" - bounty on Aesrael. |
| `ccpewsse002-armsofchaos.esl` | Arms of Chaos | 1 | S | 3 | "The Arms of Chaos" - Skytemple Ruins, Sheogorath's cult weapons. |
| `ccbgssse041-netchleather.esl` | Netch Leather Armor | 2 | S | 2 | Netch-hunting questline on Solstheim with a Dunmer crafter. |
| `ccedhsse002-splkntset.esl` | Spell Knight Armor | 1 | S | 2 | Spell Knight questline (a Breton knight order). |
| `ccbgssse067-daedinv.esm` | The Cause | 2 | M | 8 | Daedric invasion: Mehrunes Dagon cult, an Oblivion gate world (Dead Lands style), Ayleid ruin, a big quest. |
| `ccbgssse069-contest.esl` | The Contest | 1 | S | 2 | "Caught in a Web" - Candlehearth Hall mystery, a prize fight contest. |
| `ccvsvsse003-necroarts.esl` | Necromantic Grimoire | 0 | S | 1 | Necromancy spells; journal quest is a tome pointer. |
| `ccvsvsse004-beafarmer.esl` | Farming | 3 | S | 3 | Goldenhills Plantation farm, haunting and restoring the farm. |
| `ccbgssse025-advdsgs.esm` | Saints & Seducers | 2 | M | 6 | Shivering Isles creatures; Saints vs Seducers, Elytra pets, Amber/Madness gear. Extended by SEC below. |
| `ccffbsse002-crossbowpack.esl` | Expanded Crossbow Pack | 0 | - | 0 | Items only (seeding quest). |
| `ccbgssse013-dawnfang.esl` | Dawnfang & Duskfang | 2 | S | 2 | "A Soul Divided" (Riften Ratway ghosts) + "Bloodthirst". |
| `ccedhsse003-redguard.esl` | Redguard Elite Armaments | 1 | S | 2 | Redguard elite armor questline (Alik'r warriors). |
| `cckrtsse001_altar.esl` | Bittercup | 3 | M | 5 | Sheogorath/Dream-themed quests: fortune, power, and a long dream quest; ferry system. |
| `cccbhsse001-gaunt.esl` | Rebel's Cairn | 0 | S | 2 | Rebel's Cairn: Red Eagle's tomb, a ghost and the Red Eagle armor. Quest has no journal objectives. |

**CC total suggested scenes: 99** (biggest: The Cause 8, Ghosts of the Tribunal 10, Fishing 6, Saints & Seducers 6 + SEC, Bittercup 5).

CC journal quests in detail:

| CC plugin | EditorID | Name | FormID |
|---|---|---|---|
| Ghosts of the Tribunal | `ccASVSSE001_Quest` | _(localized)_ | `000CC3:ccasvsse001-almsivi.esm` |
| Ghosts of the Tribunal | `ccASVSSE001_QuestA` | _(localized)_ | `000CA0:ccasvsse001-almsivi.esm` |
| Ghosts of the Tribunal | `ccASVSSE001_QuestB` | _(localized)_ | `000F19:ccasvsse001-almsivi.esm` |
| Ghosts of the Tribunal | `ccASVSSE001_QuestC` | _(localized)_ | `000F1A:ccasvsse001-almsivi.esm` |
| Ghosts of the Tribunal | `ccASVSSE001_QuestD` | _(localized)_ | `00117A:ccasvsse001-almsivi.esm` |
| Ghosts of the Tribunal | `ccASVSSE001_QuestE` | _(localized)_ | `0990EF:ccasvsse001-almsivi.esm` |
| Fishing | `ccBGSSSE001_Crab_MQ1` | _(localized)_ | `0009D4:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Crab_MQ2` | _(localized)_ | `0009DA:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Crab_MQ3` | _(localized)_ | `0009D6:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Crab_MQ4` | _(localized)_ | `0009E9:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Fish_MQ1` | _(localized)_ | `0009DE:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Fish_MQ2` | Caught in the Rain | `0009EB:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Fish_MQ3` | _(localized)_ | `0009E8:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Fish_MQ4` | _(localized)_ | `0009DD:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Fish_MQ5` | _(localized)_ | `0009DC:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_Dwarven` | Beneath Bronze Waters | `000AD6:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_Falkreath` | _(localized)_ | `0009EC:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_Khajiit` | Spirits Away | `0009E2:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_Markarth` | _(localized)_ | `0009DF:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_Morthal` | No Contest | `0009E4:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_Solitude` | _(localized)_ | `0009E3:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_WhiterunPartOne` | _(localized)_ | `000E5D:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_WhiterunPartTwo` | _(localized)_ | `0009D7:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Misc_Windhelm` | Tusked Terror | `0009D5:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_MiscQuests` | _(localized)_ | `0009E6:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Radiant_1` | _(localized)_ | `000B98:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Radiant_2` | Further Study | `000C2F:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Radiant_3` | _(localized)_ | `000C8C:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Start_MQ1` | _(localized)_ | `0009D3:ccBGSSSE001-Fish.esm` |
| Fishing | `ccBGSSSE001_Start_MQ2` | _(localized)_ | `0009DB:ccBGSSSE001-Fish.esm` |
| Plague of the Dead | `ccBGSSSE003_ZombieQuestStartEncounter` | _(localized)_ | `00083D:ccbgssse003-zombies.esl` |
| Stendarr's Hammer | `ccBGSSSE006_Quest` | If I had a Hammer | `000805:ccbgssse006-stendarshammer.esl` |
| Arcane Accessories | `ccBGSSSE014_SpellPack_StartupQuest` | The Lost Library | `00083C:ccbgssse014-spellpack01.esl` |
| Divine Crusader | `ccMTYSSE001_Quest` | The Pilgrim's Path | `000865:ccmtysse001-knightsofthenine.esl` |
| Divine Crusader | `ccMTYSSE001_StartupQuest_Alt` | Relics of the Crusader | `00083C:ccmtysse001-knightsofthenine.esl` |
| Forgotten Seasons | `DLCDwarvenPuzzleDungeonCrownQuest` | _(localized)_ | `0038DB:cctwbsse001-puzzledungeon.esm` |
| Forgotten Seasons | `DLCDwarvenPuzzleDungeonHorseQuest` | _(localized)_ | `0038DA:cctwbsse001-puzzledungeon.esm` |
| Forgotten Seasons | `DLCDwarvenPuzzleDungeonQuest01` | _(localized)_ | `0038D9:cctwbsse001-puzzledungeon.esm` |
| Tundra Homestead | `ccEEJSSE001_Quest` | _(localized)_ | `042D35:cceejsse001-hstead.esm` |
| Shadowrend | `BGSSSE018_ShadowrendQuest` | Through a Glass, Darkly | `00081C:ccbgssse018-shadowrend.esl` |
| Nordic Jewelry | `ccEDHSSE001_CraftsmanEncounterQuest` | _(localized)_ | `00082F:ccedhsse001-norjewel.esl` |
| Wild Horses | `ccBGSSSE034_Misc_Horse01_Chestnut` | _(localized)_ | `00086D:ccbgssse034-mntuni.esl` |
| Wild Horses | `ccBGSSSE034_Misc_Horse02_Black` | _(localized)_ | `000870:ccbgssse034-mntuni.esl` |
| Wild Horses | `ccBGSSSE034_Misc_Horse03_GreyBlack` | _(localized)_ | `000871:ccbgssse034-mntuni.esl` |
| Wild Horses | `ccBGSSSE034_Misc_Horse04_Pale` | _(localized)_ | `000872:ccbgssse034-mntuni.esl` |
| Wild Horses | `ccBGSSSE034_Misc_Horse05_RedBrown` | _(localized)_ | `000873:ccbgssse034-mntuni.esl` |
| Wild Horses | `ccBGSSSE034_Misc_Horse06_WhiteSpotted` | _(localized)_ | `000874:ccbgssse034-mntuni.esl` |
| Wild Horses | `ccBGSSSE034_Misc_Horse07_BrownSpotted` | _(localized)_ | `000875:ccbgssse034-mntuni.esl` |
| Wild Horses | `ccBGSSSE034_UnicornQuest` | _(localized)_ | `000DE8:ccbgssse034-mntuni.esl` |
| Wild Horses | `ccBGSSSE034_WildHorsesQuest` | Horse Whisperer | `000D65:ccbgssse034-mntuni.esl` |
| Staff of Hasedoki | `ccBGSSSE045_Quest` | _(localized)_ | `000823:ccbgssse045-hasedoki.esl` |
| Civil War Champions | `ccFFBSSE001_Quest` | Battle of the Champions | `000927:ccffbsse001-imperialdragon.esl` |
| Vigil Enforcer Armor Set | `ccMTYSSE002_Quest` | Unholy Vigil | `000926:ccmtysse002-ve.esl` |
| Elite Crossbows | `ccBGSSSE043_VampireHunterQuest` | Night Hunter | `00089E:ccbgssse043-crosselv.esl` |
| Saturalia Holiday Pack | `ccVSVSSE001_MainQuest` | Saturalia Preparation | `00082B:ccvsvsse001-winter.esl` |
| Shadowfoot Sanctum | `ccEEJSSE003_HouseQuest` | Shadowfoot Sanctum | `00082A:cceejsse003-hollow.esl` |
| Goblins | `ccBGSSSE040_Quest` | _(localized)_ | `0009B6:ccbgssse040-advobgobs.esl` |
| Alt Armor: Daedric Plate | `ccBGSSSE050_MiscQuest` | _(localized)_ | `00081D:ccbgssse050-ba_daedric.esl` |
| Alt Armor: Daedric Plate | `ccBGSSSE050_Quest` | _(localized)_ | `000822:ccbgssse050-ba_daedric.esl` |
| Alt Armor: Daedric Mail | `ccBGSSSE051_MiscQuest` | _(localized)_ | `00081A:ccbgssse051-ba_daedricmail.esl` |
| Alt Armor: Daedric Mail | `ccBGSSSE051_Quest` | _(localized)_ | `000819:ccbgssse051-ba_daedricmail.esl` |
| Alt Armor: Iron | `ccBGSSSE052_MiscQuest` | _(localized)_ | `00082F:ccbgssse052-ba_iron.esl` |
| Alt Armor: Iron | `ccBGSSSE052_Quest` | Brothers in Irons | `000822:ccbgssse052-ba_iron.esl` |
| Alt Armor: Leather | `ccBGSSSE053_MiscQuest` | _(localized)_ | `000828:ccbgssse053-ba_leather.esl` |
| Alt Armor: Leather | `ccBGSSSE053_Quest` | Double-Edged | `000826:ccbgssse053-ba_leather.esl` |
| Alt Armor: Orcish Plate | `ccBGSSSE054_MiscQuest` | _(localized)_ | `000823:ccbgssse054-ba_orcish.esl` |
| Alt Armor: Orcish Plate | `ccBGSSSE054_Quest` | Smith 'N Slash | `000822:ccbgssse054-ba_orcish.esl` |
| Alt Armor: Orcish Scaled | `ccBGSSSE055_MiscQuest` | _(localized)_ | `000833:ccbgssse055-ba_orcishscaled.esl` |
| Alt Armor: Orcish Scaled | `ccBGSSSE055_Quest` | Gambler's Edge | `000830:ccbgssse055-ba_orcishscaled.esl` |
| Alt Armor: Silver | `ccBGSSSE056_MiscQuest` | _(localized)_ | `000823:ccbgssse056-ba_silver.esl` |
| Alt Armor: Silver | `ccBGSSSE056_Quest` | When the Cat's Away | `000814:ccbgssse056-ba_silver.esl` |
| Alt Armor: Stalhrim Fur | `ccBGSSSE057_MiscQuest` | _(localized)_ | `00081B:ccbgssse057-ba_stalhrim.esl` |
| Alt Armor: Stalhrim Fur | `ccBGSSSE057_Quest` | _(localized)_ | `00081A:ccbgssse057-ba_stalhrim.esl` |
| Alt Armor: Steel Soldier | `ccBGSSSE058_MiscQuest` | _(localized)_ | `000819:ccbgssse058-ba_steel.esl` |
| Alt Armor: Steel Soldier | `ccBGSSSE058_Quest` | Over the Edge | `000823:ccbgssse058-ba_steel.esl` |
| Alt Armor: Dragonplate | `ccBGSSSE059_MiscQuest` | _(localized)_ | `00082B:ccbgssse059-ba_dragonplate.esl` |
| Alt Armor: Dragonplate | `ccBGSSSE059_Quest` | _(localized)_ | `000824:ccbgssse059-ba_dragonplate.esl` |
| Alt Armor: Dragonscale | `ccBGSSSE060_MiscQuest` | _(localized)_ | `00081A:ccbgssse060-ba_dragonscale.esl` |
| Alt Armor: Dragonscale | `ccBGSSSE060_Quest` | _(localized)_ | `00081B:ccbgssse060-ba_dragonscale.esl` |
| Alt Armor: Dwarven Plate | `ccBGSSSE061_MiscQuest` | _(localized)_ | `00082B:ccbgssse061-ba_dwarven.esl` |
| Alt Armor: Dwarven Plate | `ccBGSSSE061_Quest` | _(localized)_ | `000829:ccbgssse061-ba_dwarven.esl` |
| Alt Armor: Dwarven Mail | `ccBGSSSE062_MiscQuest` | _(localized)_ | `000819:ccbgssse062-ba_dwarvenmail.esl` |
| Alt Armor: Dwarven Mail | `ccBGSSSE062_Quest` | _(localized)_ | `00081A:ccbgssse062-ba_dwarvenmail.esl` |
| Alt Armor: Ebony Plate | `ccBGSSSE063_MiscQuest` | _(localized)_ | `000855:ccbgssse063-ba_ebony.esl` |
| Alt Armor: Ebony Plate | `ccBGSSSE063_Quest` | Heart of Crimson | `000840:ccbgssse063-ba_ebony.esl` |
| Alt Armor: Elven Hunter | `ccBGSSSE064_MiscQuest` | _(localized)_ | `00081A:ccbgssse064-ba_elven.esl` |
| Alt Armor: Elven Hunter | `ccBGSSSE064_Quest` | Once a Hunter | `000819:ccbgssse064-ba_elven.esl` |
| Arms of Chaos | `ccPEWSSE002_Quest` | The Arms of Chaos | `000819:ccpewsse002-armsofchaos.esl` |
| Netch Leather Armor | `ccBGSSSE041_MiscQuest` | _(localized)_ | `00094A:ccbgssse041-netchleather.esl` |
| Netch Leather Armor | `ccBGSSSE041_Quest` | More than you can Chew | `00081C:ccbgssse041-netchleather.esl` |
| Spell Knight Armor | `ccEDHSSE002_Quest` | Crypt of the Heart | `000800:ccedhsse002-splkntset.esl` |
| The Cause | `ccBGSSSE067_Quest` | The Cause | `06BFC1:ccbgssse067-daedinv.esm` |
| The Cause | `ccBGSSSE067_Quest2` | _(localized)_ | `19952A:ccbgssse067-daedinv.esm` |
| The Contest | `ccBGSSSE069_Quest` | Caught in a Web | `000805:ccbgssse069-contest.esl` |
| Farming | `ccVSVSSE004_IntroQuestMisc` | _(localized)_ | `000850:ccvsvsse004-beafarmer.esl` |
| Farming | `ccVSVSSE004_MainQuest` | The Unquiet Dead | `000D28:ccvsvsse004-beafarmer.esl` |
| Farming | `ccVSVSSE004_RestoreFarmQuest` | _(localized)_ | `000EB7:ccvsvsse004-beafarmer.esl` |
| Saints & Seducers | `EC_SS_ElytraPetAcquisition_Dementia` | My Pet Elytra (Dementia) | `0010C0:ccBGSSSE025-AdvDSGS.esm` |
| Saints & Seducers | `EC_SS_ElytraPetAcquisition_Mania` | My Pet Elytra (Mania) | `0010C3:ccBGSSSE025-AdvDSGS.esm` |
| Dawnfang & Duskfang | `ccBGSSSE013_AquisitionQuest` | A Soul Divided | `000F18:ccbgssse013-dawnfang.esl` |
| Dawnfang & Duskfang | `ccBGSSSE013_BloodthirstQuest` | Bloodthirst | `000CA6:ccbgssse013-dawnfang.esl` |
| Redguard Elite Armaments | `ccEDHSSE003_Quest` | Interception | `00088C:ccedhsse003-redguard.esl` |
| Bittercup | `ccKRTSSE001_QuestFortune` | Fortunate Son | `000A90:cckrtsse001_altar.esl` |
| Bittercup | `ccKRTSSE001_QuestPower` | _(localized)_ | `000A5E:cckrtsse001_altar.esl` |
| Bittercup | `ccKRTSSE001_zQuest` | _(localized)_ | `000D63:cckrtsse001_altar.esl` |


## 4. Big quest mods

### Legacy of the Dragonborn

- Plugin(s): `LegacyoftheDragonborn.esm`
- What it is: The Dragonborn Gallery museum in Solitude, the Explorers Society, Auryen Morellus, relic hunts, excavations, Deepholme, Gala, haunted museum, Snow Elves, Ayleid waystones.
- Named journal quests: **59** · Size: **L** · Suggested banter scenes: **45**

| EditorID | Name | FormID |
|---|---|---|
| `DBM_AMJournalQST01` | Auryen's Notes: Dagger of Symmachus | `148479:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST02` | Auryen's Notes: Cyrus' Saber | `14846F:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST03` | Auryen's Notes: Orgnum's Coffer | `14D594:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST04` | Auryen's Notes: Ice Blade of the Monarch | `14D595:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST05` | Auryen's Notes: Shalidor's Stone | `14D596:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST06` | Auryen's Notes: The Bloodworm Helm | `14D597:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST07` | Auryen's Notes: The Warlock's Ring | `14D598:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST08` | Auryen's Notes: The Dragonmail Cuirass | `14D599:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST09` | Auryen's Notes: The Fists of Randagulf | `14D59A:LegacyoftheDragonborn.esm` |
| `DBM_AMJournalQST10` | Auryen's Notes: The Tools of Kagrenac | `14D59B:LegacyoftheDragonborn.esm` |
| `DBM_ArtifactOrderQuest` | Rebuilding The Past | `0F0D35:LegacyoftheDragonborn.esm` |
| `DBM_DHQuest` | The Vaults of Deepholme | `9211FD:LegacyoftheDragonborn.esm` |
| `DBM_DwarvenTech` | Ancient Technology | `3F33E3:LegacyoftheDragonborn.esm` |
| `DBM_EchosOfMadness` | Echos of Madness | `4E0D3F:LegacyoftheDragonborn.esm` |
| `DBM_Excavation01` | The Excavation of Windcaller Pass | `4D1811:LegacyoftheDragonborn.esm` |
| `DBM_Excavation02` | The Excavation of the Ruins of Rkund | `58B96A:LegacyoftheDragonborn.esm` |
| `DBM_Excavation03A` | Trial of Trinimac | `2702EE:LegacyoftheDragonborn.esm` |
| `DBM_Excavation03Prelude` | The Visage | `2702DC:LegacyoftheDragonborn.esm` |
| `DBM_ExplorerFieldStation01` | Branching Out | `2AD9CD:LegacyoftheDragonborn.esm` |
| `DBM_ExplorerFieldStation02` | Branching Out... Again | `2D1170:LegacyoftheDragonborn.esm` |
| `DBM_ExplorerFieldStation03` | Branching Out... Ever More | `2D1178:LegacyoftheDragonborn.esm` |
| `DBM_ExplorerGuildHouse` | A Room with a View | `3431C3:LegacyoftheDragonborn.esm` |
| `DBM_ExplorerGuildmembers` | Digging Up Explorers | `34D50B:LegacyoftheDragonborn.esm` |
| `DBM_ExplorerRelicFindQST` | Tools of the Trade | `7BFED0:LegacyoftheDragonborn.esm` |
| `DBM_GhostChestQST` | The Phantom Cache | `2E566D:LegacyoftheDragonborn.esm` |
| `DBM_HandofGloryQuest` | The Hand of Glory | `42E8D4:LegacyoftheDragonborn.esm` |
| `DBM_hauntedMuseumQuest` | Night at the Museum | `7AC75C:LegacyoftheDragonborn.esm` |
| `DBM_HOGCleanseQuest` | Breaking the curse | `08F9D7:LegacyoftheDragonborn.esm` |
| `DBM_HOSDiscoveryQST` | Auryen Morellus and the Chamber of Secrets | `0A9247:LegacyoftheDragonborn.esm` |
| `DBM_HrormirStaffQuest` | Eternal Ice | `4F0624:LegacyoftheDragonborn.esm` |
| `DBM_ImbuningMachine` | Back to the Drawing Board | `16658A:LegacyoftheDragonborn.esm` |
| `DBM_JournalDungeon01QST` | Sanamia's Journals - Mzulft | `1D5C18:LegacyoftheDragonborn.esm` |
| `DBM_JournalDungeon02QST` | Sanamia's Journals - Valthume | `2703F9:LegacyoftheDragonborn.esm` |
| `DBM_JournalDungeon03QST` | Sanamia's Journals - Fort Frostmoth | `275562:LegacyoftheDragonborn.esm` |
| `DBM_JournalDungeon04QST` | Sanamia's Journals - Lake Ilinalta | `27FDB5:LegacyoftheDragonborn.esm` |
| `DBM_JournalDungeon05QST` | Sanamia's Journals - Burial Ruin | `27FDD3:LegacyoftheDragonborn.esm` |
| `DBM_KOTNQuest` | Guardians of the Zealots | `9211C7:LegacyoftheDragonborn.esm` |
| `DBM_LALStart` | Dragonborn Gallery | `3F14FC:LegacyoftheDragonborn.esm` |
| `DBM_LordsMailQuest` | Lord's Mail | `125B25:LegacyoftheDragonborn.esm` |
| `DBM_MalrusCodexQST` | The Book of Wonders | `79C613:LegacyoftheDragonborn.esm` |
| `DBM_MuchAdoAboutSnowElves` | Much Ado About Snow Elves | `5C7E75:LegacyoftheDragonborn.esm` |
| `DBM_MuseumCollect` | Adding to the Collection | `124FD8:LegacyoftheDragonborn.esm` |
| `DBM_MuseumGala` | Museum Gala | `0F0DC8:LegacyoftheDragonborn.esm` |
| `DBM_MuseumHeist` | Shadows of One's Past | `33D940:LegacyoftheDragonborn.esm` |
| `DBM_MuseumIndarysQuest` | It Belongs in a Museum | `371C28:LegacyoftheDragonborn.esm` |
| `DBM_MuseumIntro` | An Interesting Prospect | `17211B:LegacyoftheDragonborn.esm` |
| `DBM_OngarKegbreaker` | Ongar's Kegbreaker | `33D941:LegacyoftheDragonborn.esm` |
| `DBM_PhynasterRingQST` | Relic of Phynaster | `2A36E4:LegacyoftheDragonborn.esm` |
| `DBM_PlanetariumQuest` | A Path to the Heavens | `5867FC:LegacyoftheDragonborn.esm` |
| `DBM_RadiantFindersKeepers` | Finders Keepers | `06B90A:LegacyoftheDragonborn.esm` |
| `DBM_RadiantResearch` | Research Project | `740A17:LegacyoftheDragonborn.esm` |
| `DBM_RadiantRuinedBooks` | One Man's Junk | `5A94C3:LegacyoftheDragonborn.esm` |
| `DBM_ShatteredLegacy` | Shattered Legacy | `121573:LegacyoftheDragonborn.esm` |
| `DBM_SpearofthSnowPrinceQuest` | Legacy of the Snow Prince | `289BEA:LegacyoftheDragonborn.esm` |
| `DBM_SyrabaneRingQST` | Relic of Syrabane | `2A87EE:LegacyoftheDragonborn.esm` |
| `DBM_VampireParts` | Ancient Power | `0854C5:LegacyoftheDragonborn.esm` |
| `DBM_VigilantsQuest1` | The Price of Vigilants | `0F0D34:LegacyoftheDragonborn.esm` |
| `DBM_VigilantsQuest2` | Faltering Light | `0E1595:LegacyoftheDragonborn.esm` |
| `DBM_WaystoneQuest` | The Ayleid Crossroads | `16658E:LegacyoftheDragonborn.esm` |

### VIGILANT

- Plugin(s): `Vigilant.esm`
- What it is: Vigil of Stendarr questline: Molag Bal's Coldharbour, the Blood Matron, Bloodsucker, the Mad King memories, Mara and Stendarr, multiple endings.
- Named journal quests: **101** · Size: **L** · Suggested banter scenes: **40**

| EditorID | Name | FormID |
|---|---|---|
| `zzzAomBountyBook` | Bounty: Book | `4E1318:Vigilant.esm` |
| `zzzAomBountyChickTrader` | Bounty: Chick Trader | `4E372E:Vigilant.esm` |
| `zzzAoMBountyPiper` | Bounty: Piper | `4E0116:Vigilant.esm` |
| `zzzAomBountyRelic` | Bounty: Daedric Relic | `4E011B:Vigilant.esm` |
| `zzzAoMBountyRelicHorn` | Bounty: Horn | `4E0121:Vigilant.esm` |
| `zzzAomBountySummoner` | Bounty: Summoner | `4E0102:Vigilant.esm` |
| `zzzAomBountyVampire` | Bounty: Vampire | `4E0108:Vigilant.esm` |
| `zzzAomBountyWitch` | Bounty: Witch | `4E010E:Vigilant.esm` |
| `zzzAoMMq00` | Vigilant of Stendarr | `005CE2:Vigilant.esm` |
| `zzzAoMMq01` | Bloodsucker | `005CE3:Vigilant.esm` |
| `zzzAoMMq02` | He Who Cannot Be Touched | `006271:Vigilant.esm` |
| `zzzAoMMq03` | Lazy Afternoon | `00627F:Vigilant.esm` |
| `zzzAoMMq04` | The Eye of Madness | `0082EA:Vigilant.esm` |
| `zzzAoMMq05` | Dine and Dash | `0098C9:Vigilant.esm` |
| `zzzAoMMq06` | Thus Spoke Khajiit | `009E68:Vigilant.esm` |
| `zzzAoMMq06BadEnd` | Mar'so Suicide | `4CDF8D:Vigilant.esm` |
| `zzzAoMMq07` | Old Regrets | `00A3FE:Vigilant.esm` |
| `zzzAoMMq08` | No Mercy | `00EA8A:Vigilant.esm` |
| `zzzAoMMq09` | The Endless Fall | `00EFF7:Vigilant.esm` |
| `zzzAoMMq10` | The Landing | `011B75:Vigilant.esm` |
| `zzzAoMMqGoodEnd` | Art of Mercy | `4D0376:Vigilant.esm` |
| `zzzAomQVigilDawnstar` | Send the Vigil to Dawnstar | `4E2521:Vigilant.esm` |
| `zzzAomQVigilFalkreath` | Send the Vigil to Falkreath | `4E2530:Vigilant.esm` |
| `zzzAoMQVigilMarkarth` | Send the Vigil to Markarth | `4E252B:Vigilant.esm` |
| `zzzAoMQVigilMorthal` | Send the Vigil to Morthal | `4E2535:Vigilant.esm` |
| `zzzAoMQVigilRiften` | Send the Vigil to Riften | `4E2517:Vigilant.esm` |
| `zzzAomQVigilSolitude` | Send the Vigil to Solitude | `4E2526:Vigilant.esm` |
| `zzzAomQVigilWhiterun` | Send the Vigil to Whiterun | `4E250C:Vigilant.esm` |
| `zzzAoMQVigilWindhelm` | Send the Vigil to Windhelm | `4E2512:Vigilant.esm` |
| `zzzAoMQVigilWinterhold` | Send the Vigil to Winterhold | `4E251C:Vigilant.esm` |
| `zzzAoMRadDead` | Radiance in the Dead | `4EA3A8:Vigilant.esm` |
| `zzzAoMRadDoppler` | Radiance in the Duplicate | `4EA3D1:Vigilant.esm` |
| `zzzAoMRadMolag` | Radiance in the Spawn | `4EA3AC:Vigilant.esm` |
| `zzzAoMRadVampire` | Radiance in the Vampire | `4E91B0:Vigilant.esm` |
| `zzzAoMRadWitchHunter` | Radiance in the Witch Hunter | `4EA3C8:Vigilant.esm` |
| `zzzAoMRestoreTemple` | Restore the Temple | `4E00FF:Vigilant.esm` |
| `zzzAoMSubQ01` | The Witch of Ivarstead | `17576E:Vigilant.esm` |
| `zzzAoMSubQ02` | Sacred Anatomancer | `4D4C3D:Vigilant.esm` |
| `zzzAoMSubQ03` | Legacy of Belharza | `51EAC1:Vigilant.esm` |
| `zzzBMGuide` | Stendarr Guide | `43B81F:Vigilant.esm` |
| `zzzBMMq01` | Empty Cells | `038524:Vigilant.esm` |
| `zzzBMMq02` | Remnants | `038525:Vigilant.esm` |
| `zzzBMMq03` | The Blood Matron | `038526:Vigilant.esm` |
| `zzzCHBossQuestAbbot` | VS Abbot | `4F57B8:Vigilant.esm` |
| `zzzCHBossQuestBloodsucker` | VS Leech King | `4F57B9:Vigilant.esm` |
| `zzzCHBossQuestDeathbringer` | VS Deathbringer | `4F57BD:Vigilant.esm` |
| `zzzCHBossQuestGorieus` | VS Gorieus | `4F57C0:Vigilant.esm` |
| `zzzCHBossQuestGreyprince` | VS Grey Prince | `4F57C1:Vigilant.esm` |
| `zzzCHBossQuestJyggalag` | VS Jyggalag | `4F69B3:Vigilant.esm` |
| `zzzCHBossQuestLaza01` | VS Laza 01 | `4F69B4:Vigilant.esm` |
| `zzzCHBossQuestLaza02` | VS Laza 02 | `4F69B5:Vigilant.esm` |
| `zzzCHBossQuestMaraKnight` | VS Knight of Mara | `4F57B7:Vigilant.esm` |
| `zzzCHBossQuestMaram` | VS Maram | `4F45C6:Vigilant.esm` |
| `zzzCHBossQuestMentana` | VS Menta-Na | `4F69B6:Vigilant.esm` |
| `zzzCHBossQuestMorihaus` | VS Morihaus | `4F69B7:Vigilant.esm` |
| `zzzCHBossQuestPelinal` | VS Pelinal | `4F69B8:Vigilant.esm` |
| `zzzCHBossQuestRitho` | VS Ritho | `4F69BC:Vigilant.esm` |
| `zzzCHBossQuestSelector` | VS Selector | `4F69BE:Vigilant.esm` |
| `zzzCHBossQuestShoggothMam` | VS Shoggoth Mother | `4F69C0:Vigilant.esm` |
| `zzzCHBossQuestVarla` | VS Varla | `4F69C2:Vigilant.esm` |
| `zzzCHBossQuestWarden` | VS Warden | `4F7BB7:Vigilant.esm` |
| `zzzCHEpilogueQuest01` | A Million Cats | `2D35CE:Vigilant.esm` |
| `zzzCHGreymarchQuest` | Greymarch | `13AEE3:Vigilant.esm` |
| `zzzCHMemoryGuide` | Memory Guide | `42E0B1:Vigilant.esm` |
| `zzzCHMemoryQuest01` | The Grand Inquisitor | `12C4F4:Vigilant.esm` |
| `zzzCHMemoryQuest02` | The Mad King | `13712B:Vigilant.esm` |
| `zzzCHMemoryQuest03` | Knight of Hounds | `13965A:Vigilant.esm` |
| `zzzCHMemoryQuest04` | Johan the Fool | `140225:Vigilant.esm` |
| `zzzCHMemoryQuest05` | Adabal | `05AE03:Vigilant.esm` |
| `zzzCHMemoryQuest06` | Remains of the Miracle | `06A23B:Vigilant.esm` |
| `zzzCHMemoryQuest07` | Temptation of Marukh | `06F53C:Vigilant.esm` |
| `zzzCHMemoryQuest08` | The Nameless Bard | `080E91:Vigilant.esm` |
| `zzzCHMemoryQuest09` | Beyond the Shores of Madness | `2CAE30:Vigilant.esm` |
| `zzzCHMemoryQuest10` | Pelinal the Bloody | `2A532E:Vigilant.esm` |
| `zzzCHMemoryQuest11` | After the Storm | `2B9BAB:Vigilant.esm` |
| `zzzCHMemoryQuest12` | The Final Night | `2BC395:Vigilant.esm` |
| `zzzCHMemoryQuest13` | Paravania the Man-Bull | `51C038:Vigilant.esm` |
| `zzzCHMQ00` | Coldharbour | `12F24E:Vigilant.esm` |
| `zzzCHMQ01` | Aetherius | `1363DB:Vigilant.esm` |
| `zzzCHMQ02` | Exsultate Jubilate | `08F2F4:Vigilant.esm` |
| `zzzCHqSAExile` | Maggot | `4EC7F3:Vigilant.esm` |
| `zzzCHrqSoulShriven` | Feral Soul-Shriven | `51532C:Vigilant.esm` |
| `zzzCHSubQuest01` | More Skooma | `1273E0:Vigilant.esm` |
| `zzzCHSubQuest02` | Archer of Kyne | `1279A1:Vigilant.esm` |
| `zzzCHSubQuest03` | The Black Worm | `129061:Vigilant.esm` |
| `zzzCHSubQuest04` | Funeral | `129BCA:Vigilant.esm` |
| `zzzChSubQuest04GoodEnd` | Martha Becomes Follower | `55985A:Vigilant.esm` |
| `zzzCHSubQuest05` | Madness | `12AD04:Vigilant.esm` |
| `zzzCHSubQuest06` | Pitier | `052F4A:Vigilant.esm` |
| `zzzCHSubQuest07` | Knight of Julianos | `1265FB:Vigilant.esm` |
| `zzzCHSubQuest08` | Knight of Zenithar | `1306FA:Vigilant.esm` |
| `zzzCHSubQuest09` | Paladin Melus | `1C1EA1:Vigilant.esm` |
| `zzzCHSubQuest10` | Knight of Arkay | `1C31F2:Vigilant.esm` |
| `zzzCHSubQuest11` | Kyne's Dragon | `21ED0C:Vigilant.esm` |
| `zzzCHSubQuest12` | Knight of Kynareth | `334C8F:Vigilant.esm` |
| `zzzCHSubQuest13` | Broken Horns | `51ADBF:Vigilant.esm` |
| `zzzCHSubQuest14` | Bald Man-Ape | `51FD3E:Vigilant.esm` |
| `zzzChSubQuest15` | The Saint's Corpse | `55AA72:Vigilant.esm` |
| `zzzCOGuide` | Stendarr Guide | `43CBAE:Vigilant.esm` |
| `zzzCOMq01` | Child of Oblivion | `065932:Vigilant.esm` |
| `zzzCOSubQ01` | Successor | `324E7E:Vigilant.esm` |

### Glenmoril

- Plugin(s): `Glenmoril.esm`
- What it is: Same author as Vigilant. Hircine and Glenmoril witches: Hinnmon, Revenant hunts, lycanthropy, Ahzidal, the Pipers, Grand Hollow; very large, dark and strange.
- Named journal quests: **147** · Size: **L** · Suggested banter scenes: **35**

| EditorID | Name | FormID |
|---|---|---|
| `zzzGHBloodCurseProgress` | Blood Curse | `012C8A:Glenmoril.esm` |
| `zzzGHEndingOwl` | To Dust | `014DDD:Glenmoril.esm` |
| `zzzGHMq01` | The Blue Bird | `009B59:Glenmoril.esm` |
| `zzzGHMq01Captive` | Captive | `06EDB0:Glenmoril.esm` |
| `zzzGHMq01SideA` | Chaplain's Song 1 | `009B83:Glenmoril.esm` |
| `zzzGHMq02` | Ebonwall | `00E3EC:Glenmoril.esm` |
| `zzzGHMq02BO` | The Black Owl 02 | `012C78:Glenmoril.esm` |
| `zzzGHMq02GoodEnd` | Embers | `00EEFA:Glenmoril.esm` |
| `zzzGHMq02Nazeem` | Nazeem | `06EDAF:Glenmoril.esm` |
| `zzzGHMq02Sub01` | Percussive Maintenance | `00FD2C:Glenmoril.esm` |
| `zzzGHMq03` | Tainted Orphan | `01230D:Glenmoril.esm` |
| `zzzGHMq03BO` | The Black Owl 03 | `012C8D:Glenmoril.esm` |
| `zzzGHMq03Sub01` | A Thousand Daggers | `012962:Glenmoril.esm` |
| `zzzGHMq04` | The Bronze Key | `0147BD:Glenmoril.esm` |
| `zzzGHMq04BO` | The Black Owl 04 | `0149C9:Glenmoril.esm` |
| `zzzGHMq04Radio` | Thalmor Radio | `014E3F:Glenmoril.esm` |
| `zzzGHMq04Sub01` | Shop of Curiosities | `014C39:Glenmoril.esm` |
| `zzzGHMq05` | Oneiromancer | `01719C:Glenmoril.esm` |
| `zzzGHMq05Charm` | Charm | `0172FB:Glenmoril.esm` |
| `zzzGHMq05Joint` | Broken Egg | `017530:Glenmoril.esm` |
| `zzzGHMq05Sub01` | Dream Within a Dream | `00C946:Glenmoril.esm` |
| `zzzGHMq05Sub02` | The Last Chick Trader | `00C9D7:Glenmoril.esm` |
| `zzzGHMq05Sub03` | The Night of Tears | `014A42:Glenmoril.esm` |
| `zzzGHMq05Sub04` | Louse | `014AFA:Glenmoril.esm` |
| `zzzGHMq05Sub05` | The Owls | `014B4A:Glenmoril.esm` |
| `zzzGHMq05Sub06` | Confined | `017654:Glenmoril.esm` |
| `zzzGHMq05Sub07` | Lucid Dream | `06492E:Glenmoril.esm` |
| `zzzGHMq06` | Or the Gospel | `017733:Glenmoril.esm` |
| `zzzGHmq06Sub01` | St. Bazura | `02C265:Glenmoril.esm` |
| `zzzGHReplayMq02` | Ebonwall | `010323:Glenmoril.esm` |
| `zzzGHReplayMq03` | Tainted Orphan | `012587:Glenmoril.esm` |
| `zzzGHReplayMq04` | The Bronze Key | `014B78:Glenmoril.esm` |
| `zzzGHReplayMq05` | Oneiromancer | `0175E7:Glenmoril.esm` |
| `zzzGHReplayMq06` | Or the Gospel | `03B8F6:Glenmoril.esm` |
| `zzzGHReplayMq07` | The Pipers | `1763BA:Glenmoril.esm` |
| `zzzGHRqAssassination` | Assassinate the Thalmor Agent | `088786:Glenmoril.esm` |
| `zzzGHRqConfidential` | Confidential Document | `088768:Glenmoril.esm` |
| `zzzGHRqDweRuin` | Tonal Code | `083565:Glenmoril.esm` |
| `zzzGhRqEpitaph` | Inscription | `08878F:Glenmoril.esm` |
| `zzzGHRqHuntBeast` | Beast Hunt | `083570:Glenmoril.esm` |
| `zzzGHRqHuntDefector` | Hunter of Hunters | `088763:Glenmoril.esm` |
| `zzzGHRqHuntWitch` | Witch Hunt | `08877D:Glenmoril.esm` |
| `zzzGHRqIronDaggers` | Iron Daggers | `088774:Glenmoril.esm` |
| `zzzGHSkip` | Skip Ep02 | `010144:Glenmoril.esm` |
| `zzzGHSkit02` | Skit 2 | `01479D:Glenmoril.esm` |
| `zzzGHSkit03` | Skit 3 | `014749:Glenmoril.esm` |
| `zzzGHSkit04` | Skit 4 | `0146C0:Glenmoril.esm` |
| `zzzLaMMq01` | The Pipers | `0B1758:Glenmoril.esm` |
| `zzzLaMMq02` | In Plain Sight | `0E9E2A:Glenmoril.esm` |
| `zzzLaMMq03` | Falling Sky | `103B86:Glenmoril.esm` |
| `zzzLaMMq04` | Little Red | `11E085:Glenmoril.esm` |
| `zzzLaMMq05` | Lice and Maggots | `1329BD:Glenmoril.esm` |
| `zzzLaMMqAlt` | Skip Hinnmon | `4863FC:Glenmoril.esm` |
| `zzzLrhBypass` | Bypass | `012EAD:Glenmoril.esm` |
| `zzzLrhMq01` | The Way is Blocked | `007733:Glenmoril.esm` |
| `zzzLrhMq02` | The Chick Trader | `007835:Glenmoril.esm` |
| `zzzLrhMq03` | A Curious Animal | `00790A:Glenmoril.esm` |
| `zzzLrhMq04` | Weary of Waiting | `007E5E:Glenmoril.esm` |
| `zzzLrhMq05` | Ah, Apple Pie! | `007F1F:Glenmoril.esm` |
| `zzzLrhMq06` | Cleaning Up Falkreath | `0082EE:Glenmoril.esm` |
| `zzzLrhMq07` | The Blessing | `0083AC:Glenmoril.esm` |
| `zzzLrhMq08` | My Precious | `008431:Glenmoril.esm` |
| `zzzLrhMq09` | Ta Ta! | `0085BD:Glenmoril.esm` |
| `zzzLrhMq10` | The Cat and the Chick | `008685:Glenmoril.esm` |
| `zzzLrhQCheckDreamTorvesard` | Check Sleep | `474F10:Glenmoril.esm` |
| `zzzLrhqChickTraderRevenge` | The Chick Trader's Shadow | `0087DF:Glenmoril.esm` |
| `zzzLrhqItheliaCall01` | Jazel Call Ithelia 01 | `47AAEF:Glenmoril.esm` |
| `zzzLrhqItheliaCall02` | Grasping at Straws | `4806FD:Glenmoril.esm` |
| `zzzLrhQTorvesardContact` | Ghost in the Mirror | `474F0F:Glenmoril.esm` |
| `zzzLRHrqChicken` | Chicken Extermination | `092BA7:Glenmoril.esm` |
| `zzzLRHrqCookingRecipe` | Cooking Recipe | `092B9C:Glenmoril.esm` |
| `zzzLRHrqKanraRescue` | Kanra Rescue | `092BBC:Glenmoril.esm` |
| `zzzLRHrqMushroom` | Mushroom | `092BAC:Glenmoril.esm` |
| `zzzLRHrqNutrient` | Nutritional Potion | `092BA1:Glenmoril.esm` |
| `zzzLRHrqRogueHunt` | Ruffian Hunt | `092BB4:Glenmoril.esm` |
| `zzzLRHrqSweetroll` | Sweet Roll | `092B8C:Glenmoril.esm` |
| `zzzLrhSqRoadRoller` | Brain-Billy's Sting | `614517:Glenmoril.esm` |
| `zzzLRHSqRoadRollerStarter` | Starter: Rolls-On-Roads | `614513:Glenmoril.esm` |
| `zzzLrhSubQuest01` | The Black Owl | `007B93:Glenmoril.esm` |
| `zzzLrhSubQuest02` | Nostos G | `0176B8:Glenmoril.esm` |
| `zzzLrhSubQuest03` | The Black Owl Flies | `017A03:Glenmoril.esm` |
| `zzzRevBossQuest01` | Lycanthropy 01 | `1F73CC:Glenmoril.esm` |
| `zzzRevBossQuest02` | Lycanthropy 02 | `1F73E6:Glenmoril.esm` |
| `zzzRevBossQuest03` | Moonlit Hunt | `30EF7D:Glenmoril.esm` |
| `zzzRevBossQuest04` | Mark of the Hunter | `33DEE3:Glenmoril.esm` |
| `zzzRevBossQuest05` | Undead Beast | `36C620:Glenmoril.esm` |
| `zzzRevBossQuestAhzidal` | Ahzidal | `38F141:Glenmoril.esm` |
| `zzzRevBossQuestAradia` | Shadow of Aradia | `343BA7:Glenmoril.esm` |
| `zzzRevBossQuestAssassin` | Assassin | `360BC6:Glenmoril.esm` |
| `zzzRevBossQuestDagoth` | Will of Dagoth | `3CE9E4:Glenmoril.esm` |
| `zzzRevBossQuestLyg` | Lyg Caller | `37DBA1:Glenmoril.esm` |
| `zzzRevBossQuestPuppet` | Puppet | `366989:Glenmoril.esm` |
| `zzzRevCircusIntro` | Sanguine Circus | `33DF1A:Glenmoril.esm` |
| `zzzRevCqAhzidal` | Ahzidal's Remains | `38F17D:Glenmoril.esm` |
| `zzzRevCqAisha` | Snow Cat | `360BD2:Glenmoril.esm` |
| `zzzRevCqCitizen01` | The Pawnbroker | `016144:Glenmoril.esm` |
| `zzzRevCqCitizen02` | The Alchemist | `016172:Glenmoril.esm` |
| `zzzRevCqCitizen03` | The Innkeeper | `01619B:Glenmoril.esm` |
| `zzzRevCqCitizen04` | The Charlatan | `0161C6:Glenmoril.esm` |
| `zzzRevCqCitizen05` | The Blacksmith | `0161F1:Glenmoril.esm` |
| `zzzRevCqDragon01` | Farewell Gift | `343B60:Glenmoril.esm` |
| `zzzRevCqLeaper` | Words of Worlding | `5872E4:Glenmoril.esm` |
| `zzzRevCqLeaperSurgey` | Nymic Surgery | `58DF4C:Glenmoril.esm` |
| `zzzRevCqMothMan` | Song of Fjyron | `579C46:Glenmoril.esm` |
| `zzzRevCqPedlar` | Stray Cat | `3D45DE:Glenmoril.esm` |
| `zzzRevCqRobin` | Bad Company | `3B7828:Glenmoril.esm` |
| `zzzRevCqRuddyman` | Memory of the Deep Sea | `3B1B6D:Glenmoril.esm` |
| `zzzRevCqScab` | Stigmata Necrosis | `35AF3D:Glenmoril.esm` |
| `zzzRevDA01` | Clavicus Vile | `176373:Glenmoril.esm` |
| `zzzRevDAAzura` | Azura | `355287:Glenmoril.esm` |
| `zzzRevDANamira` | To Fishing Village | `355274:Glenmoril.esm` |
| `zzzRevMisc01` | Zealot of Meridia | `0160BA:Glenmoril.esm` |
| `zzzRevMisc02` | Musketeer's Hope | `016143:Glenmoril.esm` |
| `zzzRevMisc03` | Legless Friends | `016235:Glenmoril.esm` |
| `zzzRevMisc04` | Je'm'ath Brandy | `37226B:Glenmoril.esm` |
| `zzzRevMisc05` | Ahzidal's Ladder | `383800:Glenmoril.esm` |
| `zzzRevMisc06` | One-Finger | `54ACC6:Glenmoril.esm` |
| `zzzRevMq00` | Departure | `171135:Glenmoril.esm` |
| `zzzRevMq01` | Feast of Love | `60026B:Glenmoril.esm` |
| `zzzRevqKeyItem` | Key Items | `123349:Glenmoril.esm` |
| `zzzRevRq01A` | Child Beast | `3DA23B:Glenmoril.esm` |
| `zzzRevRq01B` | Musketeer Hunt | `3DA244:Glenmoril.esm` |
| `zzzRevRq01C` | Rioter Hunt | `3DA258:Glenmoril.esm` |
| `zzzRevRq01D` | Herma Cat | `3DA260:Glenmoril.esm` |
| `zzzRevRq01E` | Pale Sack | `3DFE17:Glenmoril.esm` |
| `zzzRevRq01F` | Infected Hunt | `3E59B9:Glenmoril.esm` |
| `zzzRevRq02A` | Beast Citizen | `3E59D4:Glenmoril.esm` |
| `zzzRevRq02B` | Boss Beast | `3E59EC:Glenmoril.esm` |
| `zzzRevRq02C` | Worshippers of Hircine | `3E59FE:Glenmoril.esm` |
| `zzzRevRq02D` | Outlander | `3E5A03:Glenmoril.esm` |
| `zzzRevRqAtatami` | Atatami | `3F1171:Glenmoril.esm` |
| `zzzRevRqDragon` | Dragon | `3EB5E6:Glenmoril.esm` |
| `zzzRevRqMiniBoss` | Kalpic Traveler | `5A8BC8:Glenmoril.esm` |
| `zzzRevRqScab` | Radiance | `3EB596:Glenmoril.esm` |
| `zzzRevSCq01` | Meat | `3F6D3A:Glenmoril.esm` |
| `zzzRevScq02` | Bone | `3F6DA7:Glenmoril.esm` |
| `zzzRevSCq03` | Scraps | `3F6DB2:Glenmoril.esm` |
| `zzzRevSqCheese` | Pale Cheese | `5D7AD9:Glenmoril.esm` |
| `zzzRevSub01` | Strange Fruit | `015B58:Glenmoril.esm` |
| `zzzRevSub01Jabal` | Communion: Ja'bal | `48BF99:Glenmoril.esm` |
| `zzzRevSub02` | Desiccated Embryo | `01710D:Glenmoril.esm` |
| `zzzRevSub03` | Baby of Nightmares | `34980C:Glenmoril.esm` |
| `zzzRevSub03Rush` | Rite of Cannibalism | `3ABF2B:Glenmoril.esm` |
| `zzzRevSub04` | Sacrament of Cat | `51525D:Glenmoril.esm` |
| `zzzRevSub04Jazel` | Jazel Phantom | `572FEC:Glenmoril.esm` |
| `zzzRevSub05Intro` | The Lost Storyteller | `5F2B94:Glenmoril.esm` |
| `zzzRevSub06Key01` | Yelem's Cord | `62F3BC:Glenmoril.esm` |

### Unslaad

- Plugin(s): `Unslaad.esm`
- What it is: Same author. A winter-and-dream questline (Falling Cat, Hoarfrost, Long Winter, Stairway to Llesw'er, Under the Elder Tree), Ysgramor and Magnar boss fights, many radiants.
- Named journal quests: **48** · Size: **L** · Suggested banter scenes: **25**

| EditorID | Name | FormID |
|---|---|---|
| `zzzCrbBqDreughKing` | VS Dreugh King | `407436:Unslaad.esm` |
| `zzzCrbBqJhunalPriest` | VS Jhunal Priest | `47F4A9:Unslaad.esm` |
| `zzzCrbBqMagnarIdol` | VS Idol of Magnar | `409CE1:Unslaad.esm` |
| `zzzCrbBqStuhnTsun` | Trial of the Gods | `3C8752:Unslaad.esm` |
| `zzzCrbBqYsgramor` | VS Ysgramor | `419232:Unslaad.esm` |
| `zzzCrbBqYsJhumalGiant` | VS Giant of Jhunal | `40C576:Unslaad.esm` |
| `zzzCrbBqYsJill01` | VS Jill 01 | `40C5F1:Unslaad.esm` |
| `zzzCrbBqYsJill02` | VS Jill 02 | `40EE61:Unslaad.esm` |
| `zzzCrbBqYsLeopard` | VS Leopard | `40C580:Unslaad.esm` |
| `zzzCrbBqYsSnake` | VS Snake | `40C58A:Unslaad.esm` |
| `zzzCrbEpilogue` | Epilogue Scenes | `1EC845:Unslaad.esm` |
| `zzzCrbMq01` | Falling Cat | `01D8FF:Unslaad.esm` |
| `zzzCrbMq02` | Hoarfrost | `02299D:Unslaad.esm` |
| `zzzCrbMq03` | When You Wish Upon a Star | `112A83:Unslaad.esm` |
| `zzzCrbMq04` | Long Winter | `117B3E:Unslaad.esm` |
| `zzzCrbMq05` | Lingering Snow | `117B3F:Unslaad.esm` |
| `zzzCrbMq05Rush` | Boss Rush | `18F113:Unslaad.esm` |
| `zzzCrbMq06` | Stairway to Llesw'er | `1DFDFA:Unslaad.esm` |
| `zzzCrbMq07` | The Owl Flies at Dusk | `1DFDFB:Unslaad.esm` |
| `zzzCrbMq08` | The Final Journey | `465EBF:Unslaad.esm` |
| `zzzCrbMq09` | Loveletter to the Fifth Era | `47A32B:Unslaad.esm` |
| `zzzCrbMq10` | Under the Elder Tree | `47A38C:Unslaad.esm` |
| `zzzCrbqLessonKhev` | Sermon of Khev | `4073F0:Unslaad.esm` |
| `zzzCrbRadiantAmarantos` | Amaranth Flower | `3533FE:Unslaad.esm` |
| `zzzCrbRadiantBrandy` | Briarheart Brandy | `3676B2:Unslaad.esm` |
| `zzzCrbRadiantCoin` | Rare Coin | `350B8B:Unslaad.esm` |
| `zzzCrbRadiantDragon` | Dregs of Alduin | `34E336:Unslaad.esm` |
| `zzzCrbRadiantEmber` | Ember of Atmora | `34BAD8:Unslaad.esm` |
| `zzzCrbRadiantHM` | Woodland Man Hunt | `48E803:Unslaad.esm` |
| `zzzCrbRadiantIceTree` | Ice Tree | `34926B:Unslaad.esm` |
| `zzzCrbRadiantKanra` | Lost Kanra | `3441D4:Unslaad.esm` |
| `zzzCrbRadiantLizz` | Picture Book | `350B7F:Unslaad.esm` |
| `zzzCrbRadiantMemory` | Memento Collection | `3719C1:Unslaad.esm` |
| `zzzCrbRadiantParasite` | Infected | `3676A3:Unslaad.esm` |
| `zzzCrbRadiantRagingPot` | Raging Pot | `3719D3:Unslaad.esm` |
| `zzzCrbRadiantRat` | Rogue Rat | `369EFB:Unslaad.esm` |
| `zzzCrbRadiantUnwanted` | Intruder | `350BA7:Unslaad.esm` |
| `zzzCrbSkip` | Act Skip | `2D6C97:Unslaad.esm` |
| `zzzCrbsq01` | Dragon Souls | `022986:Unslaad.esm` |
| `zzzCrbSq02` | Fluffy's Secret | `05268B:Unslaad.esm` |
| `zzzCrbSq03` | Arkved | `33F0E0:Unslaad.esm` |
| `zzzCrbSq04` | Snow Guardian | `364E2B:Unslaad.esm` |
| `zzzCrbSq05` | Liturgy of I | `376B99:Unslaad.esm` |
| `zzzCrbSqApoSafeRoom` | Saferoom Unlock: Frozen Abyss | `453AFA:Unslaad.esm` |
| `zzzCrbSqMankar` | Watcher from the Third Era | `411777:Unslaad.esm` |
| `zzzCrbSqReopen` | Reopen the Gate | `2904BE:Unslaad.esm` |
| `zzzCrbSqResurrection` | Revive | `11023D:Unslaad.esm` |
| `zzzCrbSqRoadAtmora` | Road to Amora | `3C0D01:Unslaad.esm` |

### DAc0da

- Plugin(s): `DAc0da.esm`
- What it is: Same author. Sea of Causality, the Sload city, Numidium Tertius, bosses Nchunak, Zurin Arctus, Dumac; Vivec-era lore and Tamrielic myth-war.
- Named journal quests: **36** · Size: **L** · Suggested banter scenes: **20**

| EditorID | Name | FormID |
|---|---|---|
| `zDcdEpiQAbnur` | Epi Abnur | `00CEE1:DAc0da.esm` |
| `zDcdEpiQSamon` | Epilogue Samon | `00CE94:DAc0da.esm` |
| `zDcdEpiQYngol` | Epilogue Yngol | `00CED0:DAc0da.esm` |
| `zDcdMq00` | The Call of Landfall | `00AA0C:DAc0da.esm` |
| `zDcdMq00Citizen` | Citizen Dialogue | `000D9F:DAc0da.esm` |
| `zDcdMq00CitizenPanic` | Panic Citizen | `004452:DAc0da.esm` |
| `zDcdMq01` | The Sea of Causality | `004475:DAc0da.esm` |
| `zDcdMq02` | Negative Legacy | `004931:DAc0da.esm` |
| `zDcdMq03` | Patchwork | `004981:DAc0da.esm` |
| `zDcdMq04` | Numidium Tertius | `00B21B:DAc0da.esm` |
| `zDcdMq05` | Censored Fate | `00CA1E:DAc0da.esm` |
| `zDcdMqAgent` | Agent Event | `004566:DAc0da.esm` |
| `zDcdMqArgoEnd` | Pan-Argonia | `00CA5B:DAc0da.esm` |
| `zDcdMqBoss01` | VS Nchunak | `00B265:DAc0da.esm` |
| `zDcdMqBoss02` | VS GC9 | `00B3A8:DAc0da.esm` |
| `zDcdMqBoss03` | VS Arcanist | `00B4F1:DAc0da.esm` |
| `zDcdMqBoss04` | VS Zurin Arctus | `00B5EE:DAc0da.esm` |
| `zDcdMqBoss05` | VS Dumac | `00B6DC:DAc0da.esm` |
| `zDcdMqCheeseEnd` | Rella Mozzarella | `00C9F1:DAc0da.esm` |
| `zDcdMqDragon` | Golden Dragon Flight | `004564:DAc0da.esm` |
| `zDcdQInit` | Init Quest | `000D9D:DAc0da.esm` |
| `zDcdQManagerNumidium` | Numidium Manager | `000D9C:DAc0da.esm` |
| `zDcdSqAbnur` | Abnur Tharn | `00525E:DAc0da.esm` |
| `zDcdSqAugur` | Augur of the Obscure | `0047E5:DAc0da.esm` |
| `zDcdSqGhostChoir` | Scene of Ghost Choir | `00B420:DAc0da.esm` |
| `zDcdSqHalfElf` | The End of All Wishes | `0050DC:DAc0da.esm` |
| `zDcdSqNumShotcut` | Numidium Shortcut | `00B1CE:DAc0da.esm` |
| `zDcdSqPrisoner` | In Grabbers' Hands | `00CEFE:DAc0da.esm` |
| `zDcdSqSheogorath` | Cheese Party | `00CDD9:DAc0da.esm` |
| `zDcdSqSloadRadio` | Sload Radio | `00CE40:DAc0da.esm` |
| `zDcdSqWorm` | Echoes of Mnemolichite | `0052C2:DAc0da.esm` |
| `zDcdSqWormSub01` | Option: Dreugh | `005303:DAc0da.esm` |
| `zDcdSqWormSub02` | Group Battle: The Sload City | `0056C4:DAc0da.esm` |
| `zDcdSqWormSub03` | Group Battle: The Revenant | `005FBE:DAc0da.esm` |
| `zDcdSqWormSub04` | The Sea of Radiance | `006134:DAc0da.esm` |
| `zDcdSqYngol` | Drowned Nighthawk | `004B1C:DAc0da.esm` |

### Wyrmstooth

- Plugin(s): `Wyrmstooth.esp`
- What it is: An island off Solstheim: hunt the dragon Vulthurmaar, bounties, Barrow of the Wyrm, a player home, favors for the Brinewater Grotto folk.
- Named journal quests: **23** · Size: **L** · Suggested banter scenes: **25**

| EditorID | Name | FormID |
|---|---|---|
| `WTAthirFavor` | Retrieving Embersunder | `3A1467:Wyrmstooth.esp` |
| `WTBarrowOfTheWyrm` | Barrow of the Wyrm | `028F01:Wyrmstooth.esp` |
| `WTBlindRobbersCache` | Blind Robber's Cache | `46DA2A:Wyrmstooth.esp` |
| `WTBountyAnimal` | Animal Bounty | `4B9DEE:Wyrmstooth.esp` |
| `WTBountyBandit` | Bandit Bounty | `4B9DED:Wyrmstooth.esp` |
| `WTBountyVampire` | Vampire Bounty | `4B9DF0:Wyrmstooth.esp` |
| `WTBountyWarlock` | Warlock Bounty | `4B9DEF:Wyrmstooth.esp` |
| `WTDaenlitFavor` | Robbed Blind | `3A1469:Wyrmstooth.esp` |
| `WTDragonHunt` | Wyrmstooth | `022528:Wyrmstooth.esp` |
| `WTElmeraFavor` | Stickler in the Mud | `3A146A:Wyrmstooth.esp` |
| `WTKillThalmor` | Unwanted Guests | `3943A0:Wyrmstooth.esp` |
| `WTNoticeboardPointer` | Noticeboard Pointer | `C92734:Wyrmstooth.esp` |
| `WTPlayerHome` | Reclaiming the Past | `28D0B5:Wyrmstooth.esp` |
| `WTPricelessCommodity` | A Priceless Commodity | `48F992:Wyrmstooth.esp` |
| `WTRandomEnc44Location` | Gjalrunn resting in an inn | `CAD2D3:Wyrmstooth.esp` |
| `WTRebuild` | Rebuilding Wyrmstooth | `11E1D3:Wyrmstooth.esp` |
| `WTShargamFavor` | Repaying a Debt | `3A1468:Wyrmstooth.esp` |
| `WTSignyFavor` | A Debt Unpaid | `B5DA18:Wyrmstooth.esp` |
| `WTTheNakedNord` | The Naked Nord | `C651DA:Wyrmstooth.esp` |
| `WTTheodynLocationEncounter` | Theodyn appears in a town or city | `B22004:Wyrmstooth.esp` |
| `WTUberEncounter` | Someone with Backbone | `2F1A74:Wyrmstooth.esp` |
| `WTWolfFollower` | A Howl Load of Trouble | `2E49AF:Wyrmstooth.esp` |
| `WTWrapMeUp` | Wrap Me Up | `3920D5:Wyrmstooth.esp` |

### SIRENROOT - Deluge of Deceit

- Plugin(s): `evgSIRENROOT.esm`
- What it is: One long 41-stage journey ("Deluge of Deceit", 27 objectives) into a flooded hidden land; mysterious, lore-heavy.
- Named journal quests: **1** · Size: **M** · Suggested banter scenes: **18**

| EditorID | Name | FormID |
|---|---|---|
| `EVGSirenrootQuest` | Deluge of Deceit | `026BC5:evgSIRENROOT.esm` |

### Beyond Skyrim - Bruma

- Plugin(s): `BSHeartland.esm`
- What it is: Whole Cyrodiil border region: city of Bruma, Cloud Ruler Temple, the Cutters, Underpall, Frostcrag Spire, dozens of town jobs.
- Named journal quests: **58** · Size: **L** · Suggested banter scenes: **35**

| EditorID | Name | FormID |
|---|---|---|
| `CYRAleswellFF01` | Studying | `0D2631:BSHeartland.esm` |
| `CYRApplewatchFF01` | The big, bad wolf | `072648:BSHeartland.esm` |
| `CYRApplewatchFF02` | Cider Delivery | `06E785:BSHeartland.esm` |
| `CYRApplewatchFF03` | Horse, Meet Troll | `07A9C6:BSHeartland.esm` |
| `CYRBQ01` | Bounty: Bandit Boss | `003A57:BSHeartland.esm` |
| `CYRBQ02` | Bounty: Goblin Chief | `0D3796:BSHeartland.esm` |
| `CYRBrumaFF00` | Visit Bruma | `0D6996:BSHeartland.esm` |
| `CYRBrumaFF01` | Collect ingredients for Ananril | `02DB52:BSHeartland.esm` |
| `CYRBrumaFF02` | Soulgem for Elintius | `0650C3:BSHeartland.esm` |
| `CYRBrumaFF03` | Payments for Razzada | `065163:BSHeartland.esm` |
| `CYRBrumaFF04` | Shipping request to Greenwood | `06516C:BSHeartland.esm` |
| `CYRBrumaFF05` | Dartaqto misc task | `0650BA:BSHeartland.esm` |
| `CYRBrumaFF06` | Horse, off course | `0723A2:BSHeartland.esm` |
| `CYRBrumaFF07` | Dartaqto bear pelts | `06E76F:BSHeartland.esm` |
| `CYRBrumaFF08` | Return Serulius' journal | `072639:BSHeartland.esm` |
| `CYRBrumaFF09` | Convince Cerendil to drop the charges against Bentior | `07F00A:BSHeartland.esm` |
| `CYRBrumaFF10` | Fighter's Guild Advertising | `06F999:BSHeartland.esm` |
| `CYRBrumaFF11` | Gort's Generic Fetch Quest | `08652B:BSHeartland.esm` |
| `CYRBrumaFF12` | Missing Dog | `086531:BSHeartland.esm` |
| `CYRBrumaFF13` | Nord Weapons | `06DB5F:BSHeartland.esm` |
| `CYRBrumaHaraldMuseumPointer` | Pointer to Harald museum tour | `0D3579:BSHeartland.esm` |
| `CYRBrumaMS01` | Alammu's Veil | `003A58:BSHeartland.esm` |
| `CYRBrumaMS02` | Upon My Honor | `0C7E4C:BSHeartland.esm` |
| `CYRBrumaMS03` | All the Wrong Places | `047FAA:BSHeartland.esm` |
| `CYRBrumaMS04` | The Screeching Songman | `067841:BSHeartland.esm` |
| `CYRBrumaMS05` | Ugly Love | `08AE84:BSHeartland.esm` |
| `CYRBrumaMS06` | Undeath at Underpall | `08BF0C:BSHeartland.esm` |
| `CYRBrumaMS07` | Absent Antiquity | `086207:BSHeartland.esm` |
| `CYRBrumaMS08` | A Delicate Situation | `086208:BSHeartland.esm` |
| `CYRBrumaMS09` | Against the Cutters | `08650F:BSHeartland.esm` |
| `CYRBrumaMS09MiscA` | Against the Cutters: Misc Tasks | `086509:BSHeartland.esm` |
| `CYRBrumaMS09UncutBackup` | Against the Cutters BACKUP BEFORE CUTS | `0D5682:BSHeartland.esm` |
| `CYRBrumaMS10` | Service Rewarded | `07F0FA:BSHeartland.esm` |
| `CYRBrumaMS11` | The Courier | `0C9BE1:BSHeartland.esm` |
| `CYRBrumaWatchtowersFF01` | Blade of the Cutpurse | `07CAAF:BSHeartland.esm` |
| `CYRCloudRulerFF01` | The Way Home | `06F9B8:BSHeartland.esm` |
| `CYRDialogueAleswell` | Aleswell dialogue | `0D2622:BSHeartland.esm` |
| `CYRDialogueBruma` | Bruma Dialogue | `003A54:BSHeartland.esm` |
| `CYRDragonclawRockFF01` | Aera the Devout's missing amulet | `07D7AC:BSHeartland.esm` |
| `CYRdunFrostfireQST` | Frostfire Unleashed | `06C0DE:BSHeartland.esm` |
| `CYRFortPalePassFF01` | Within the Ruins | `0C88E3:BSHeartland.esm` |
| `CYRFortPalePassMS01New` | A Stormcloak in Chains | `0CE0F1:BSHeartland.esm` |
| `CYRFrostcragFF01` | Kill the scamp for Ravil Fandrani | `083953:BSHeartland.esm` |
| `CYRFrostcragMS01` | Whispers of the Mountain | `083A17:BSHeartland.esm` |
| `CYRGreenwoodMeaderyFF01` | Water Run Dry | `06F9A1:BSHeartland.esm` |
| `CYRJerallsFF01` | A Cutter in Need | `06F938:BSHeartland.esm` |
| `CYRJerallsFF02` | Horseshoe for Terinius | `0723B3:BSHeartland.esm` |
| `CYRJerallsFF04` | Save the herbalist from Thorina's Cutters | `073C23:BSHeartland.esm` |
| `CYRMarriage` | Cyrodiil marriage quest | `06DEB5:BSHeartland.esm` |
| `CYRMountainWatchFF01` | Zurikki the Thief | `0D263D:BSHeartland.esm` |
| `CYRMountainWatchFF02` | Bargin Brunch from Bruma | `0E591F:BSHeartland.esm` |
| `CYRMountainWatchMS01` | Two of a Kind | `0E5911:BSHeartland.esm` |
| `CYRMountainWatchMS02` | The Deepiron Problem | `0E5912:BSHeartland.esm` |
| `CYRSkyrimBorderGateTopLevelQuest` | Welcome to Cyrodiil | `0D3F2C:BSHeartland.esm` |
| `CYRSnowstoneRestFF01` | Barnius tribute | `06E78C:BSHeartland.esm` |
| `CYRSnowstoneRestFF02` | Word to Bruma | `06F9A9:BSHeartland.esm` |
| `CYRWEBountyCollectorQST` | Bounty Collector | `0C8902:BSHeartland.esm` |
| `CYRWICourier` | Courier | `0C9A88:BSHeartland.esm` |

### Moonpath to Elsweyr

- Plugin(s): `moonpath.esp`
- What it is: A Khajiit-led trip to the Elsweyr desert (Riverhold region / Anvil) - sload dinner guest, moon sugar, rebuilding a ruin.
- Named journal quests: **6** · Size: **M** · Suggested banter scenes: **15**

| EditorID | Name | FormID |
|---|---|---|
| `Anvil_armorquest` | Desert Style | `0440C0:moonpath.esp` |
| `Anvil_buildquest` | Rebuilding the Past | `03C6E1:moonpath.esp` |
| `AnvilDenQuest` | Incursion | `01ED3C:moonpath.esp` |
| `AnvilMoonpathQuest` | By the Light of the Moon | `06A8CA:moonpath.esp` |
| `AnvilQuestameir` | The Sweet Taste of Elsweyr | `01EE82:moonpath.esp` |
| `AnvilSloadquest` | The Dinner Guest | `0589C5:moonpath.esp` |

### The Forgotten City

- Plugin(s): `ForgottenCity.esp`
- What it is: Time-loop mystery in a Dwemer-built Roman city: the Golden Rule, "one sins, all suffer".
- Named journal quests: **2** · Size: **L** · Suggested banter scenes: **20**
- Note: Only two journal quests but a dense, famous story. Status sub-quests dropped.

| EditorID | Name | FormID |
|---|---|---|
| `000FCQuest01` | The Forgotten City | `012BB9:ForgottenCity.esp` |
| `000FCQuest02` | Forget-me-not | `05965B:ForgottenCity.esp` |

### Skyrim Extended Cut - Saints and Seducers

- Plugin(s): `Skyrim Extended Cut - Saints and Seducers.esp`
- What it is: Expands the S&S CC into a Shivering Isles trip: The Route/Isle/Roots of Madness, merchant and lunatic side quests.
- Named journal quests: **5** · Size: **M** · Suggested banter scenes: **10**

| EditorID | Name | FormID |
|---|---|---|
| `EC_SS_LizardQuest` | The Lunatic's Treasure | `099D1B:Skyrim Extended Cut - Saints and Seducers.esp` |
| `EC_SS_MQ100Int` | The Route of Madness | `099D18:Skyrim Extended Cut - Saints and Seducers.esp` |
| `EC_SS_MQ101` | The Isle of Madness | `099D19:Skyrim Extended Cut - Saints and Seducers.esp` |
| `EC_SS_MQ102` | The Roots of Madness | `09EF5F:Skyrim Extended Cut - Saints and Seducers.esp` |
| `EC_SS_TheodorQuest` | The Merchant's Masterpiece | `099D1A:Skyrim Extended Cut - Saints and Seducers.esp` |

### The Gray Cowl of Nocturnal

- Plugin(s): `Gray Fox Cowl.esm`
- What it is: Gray Fox legend: the cowl, Coldharbour reward, Umbranox memories, the Hammerfell desert.
- Named journal quests: **8** · Size: **M** · Suggested banter scenes: **15**

| EditorID | Name | FormID |
|---|---|---|
| `manny_GF_Books` | Memories of the Umbranox | `0026F4:Gray Fox Cowl.esm` |
| `manny_GF_BuryValenDreth` | Bury Valen Dreth | `01E072:Gray Fox Cowl.esm` |
| `manny_GF_ColdharbourQuest` | Reward of Coldharbour | `01F56B:Gray Fox Cowl.esm` |
| `manny_GF_Farewell` | Time for the Farewells | `01CFA7:Gray Fox Cowl.esm` |
| `manny_GF_IrlavExperiment` | The Experiment | `03039F:Gray Fox Cowl.esm` |
| `manny_GF_MiscQuestShantaFilibb` | Claim Shanta Filibb | `050159:Gray Fox Cowl.esm` |
| `manny_GF_MQ` | The Call of Gray Cowl of Nocturnal | `001E61:Gray Fox Cowl.esm` |
| `manny_GF_Sadraaka` | The Curse of Sadraaka | `026AE8:Gray Fox Cowl.esm` |

### Missives (+ Voice and Quest Expansion + worldspace add-ons)

- Plugin(s): `Missives.esp`, `MissivesExpansion.esp`, `Missives - Solstheim.esp`, `Missives - Heartland.esp`, `Missives - Gray Cowl Patch.esp`, `Missives - Wyrmstooth.esp`
- What it is: Notice-board jobs in every hold: bandits, dragons, giants, fugitives, deliveries, fetch jobs. Radiant; repetitive.
- Named journal quests: **391** · Size: **M** · Suggested banter scenes: **10**
- Note: Generic radiant jobs: good for "another notice-board job?" style banter, not per-quest scenes. Headhunter - Bounties Redone + Requiem patches add to the same lane.

Quest names (type x count): Deliver a Potion Far x14, Deliver a Letter Distant x13, Deliver a Letter Near x13, Deliver a Letter Medium x13, Deliver a Potion Near x13, Deliver a Weapon Distant x13, Deliver a Weapon Near x13, Deliver a Weapon Medium x13, Gather Some Rare Ingredients x13, Gather Some Common Ingredients x13, Gather Some Uncommon Ingredients x13, Collect Some Food x13, Gather Rare Ore x13, Gather Common Ore x13, Gather Uncommon Ore x13, Gather Very Rare Ore x13, Find a Powerful Soul Gem x13, Collect Some Weak Soul Gems x13, Collect Some Standard Soul Gems x13, Kill Some Things x13, Kill a Dragon x13, Recover From a Hideout x13, Retrieve From a Ruin x13, Retrieve From the Wilderness x13, Kill Some Bandits x11, Deliver a Potion Medium x10, Track Fugitive x9, Track Thief x9, Track Vampire x9, Kill a Giant x4, Deliver a Potion Med x2, Kill an Ogre, Kill Forsworn, Kill Rieklings, Kill or Capture A Bandit Marauder, Catch Fish, Find Adept Spell Tome, Find Apprentice Spell Tome, Find Common Book, Find Rare Book, Find Uncommon Book, Find Common Accessory, Find Dwemer Rarity, Find Expert Spell Tome, Find Rare Accessory, Find The Missing Dog, Find The Missing Goat, Find Toy, Gather Firewood, Gather Nord Mead, Gather Steel Swords, Heal the Sick, Kill Pests, Kill The Draugr, Find Item From Solstheim

### Interesting NPCs (3DNPC)

- Plugin(s): `3DNPC.esp`
- What it is: Hundreds of voiced NPCs with personal quests, plus the "From the Blood of Kings" main line (Bloodsmith, Harbinger, Beast Who Cannot Be Slain).
- Named journal quests: **100** · Size: **L** · Suggested banter scenes: **30**

| EditorID | Name | FormID |
|---|---|---|
| `3DMCue` | Darkened Steel | `1D40F8:3DNPC.esp` |
| `3dmcue2` | A Daedra in the Dark | `1D96ED:3DNPC.esp` |
| `3DMCue3` | Cat and Mouse | `1E8C3C:3DNPC.esp` |
| `3DMCue4` | Deathbroker | `1F05C2:3DNPC.esp` |
| `3DMCue5` | A Path of Bones | `1F8527:3DNPC.esp` |
| `3dmcue6` | The Face of the Ghost | `203932:3DNPC.esp` |
| `3DNPCMQ1` | From the Blood of Kings | `196D2D:3DNPC.esp` |
| `3DNPCMQ2` | Faces and Names | `19B9CD:3DNPC.esp` |
| `3DNPCMQ3` | The Bloodsmith | `1A63C4:3DNPC.esp` |
| `3DNPCMQ4` | The Harbinger of Us All | `1A0BD4:3DNPC.esp` |
| `3DNPCMQ5` | Blood and Bones | `1ADAFB:3DNPC.esp` |
| `3DNPCMQ6` | The Beast Who Cannot Be Slain | `1B2911:3DNPC.esp` |
| `3DNPCMQ7` | An End to Keep | `1B462D:3DNPC.esp` |
| `3DNPCMQ9` | HummmmBaby | `1B4631:3DNPC.esp` |
| `AldiLeverQuest` | Lever Quest | `36F52B:3DNPC.esp` |
| `AmaleeQuest` | Bards, Beasts, and Beauties | `16E34D:3DNPC.esp` |
| `AmicusDialogue` | Idle Dreams | `1EDD76:3DNPC.esp` |
| `AnumLaQuest` | Honor's Calling | `1413D9:3DNPC.esp` |
| `Arielequest` | Children of the Dust | `306C12:3DNPC.esp` |
| `ArilwaenQuest` | The Immortal Coil | `2838D9:3DNPC.esp` |
| `AsteriaQuest` | The Raven of Anvil | `15E47E:3DNPC.esp` |
| `BeatriceQuest` | Mogo's Mead | `15A1BD:3DNPC.esp` |
| `blackrobesquest` | Black Robes | `242E87:3DNPC.esp` |
| `BookQuest3DNPC` | The Paper Mirror | `191004:3DNPC.esp` |
| `CarmellaSkjarnQuest` | Art and Sacrifice | `2A993F:3DNPC.esp` |
| `Cassockquest` | Spell It Out For Me | `23D691:3DNPC.esp` |
| `CWQQ2` | Forgotten Lore | `038120:3DNPC.esp` |
| `DarRakkiQuest` | Conspiracy of the Steps | `044B38:3DNPC.esp` |
| `DialogueAnumla` | The Swamp Knight | `0294CA:3DNPC.esp` |
| `DialogueAzzarian` | Azzarian's Gold | `29BB83:3DNPC.esp` |
| `DialogueBrakh` | A Hunter's Quarry | `0C2D72:3DNPC.esp` |
| `DialogueCassius` | The Good Inside | `28CDD8:3DNPC.esp` |
| `DialogueDaenlyn` | A Lute of Hollow Oak | `274031:3DNPC.esp` |
| `DialogueDarRakki` | The Conspiracy of the 7000 Steps | `002912:3DNPC.esp` |
| `DialogueDrobar` | Dialogue Drobar | `27DAFE:3DNPC.esp` |
| `DialogueFjona` | The Wolf of Greywater Grotto | `0958FC:3DNPC.esp` |
| `dialoguegorr` | Gorr the Wanderer | `02D6EA:3DNPC.esp` |
| `DialogueGriffith` | Runaways | `066092:3DNPC.esp` |
| `DialogueIorel` | The Queen of Mereth | `087EFD:3DNPC.esp` |
| `DialogueJasparGaerston` | The Loudest Whisper | `025759:3DNPC.esp` |
| `DialogueJilkmar` | The Milk-Drinker | `20EE6C:3DNPC.esp` |
| `DialogueLajjan` | Dialogue Lajjan | `2A4C9B:3DNPC.esp` |
| `DialogueMeresine` | Fire and Blood | `25EABA:3DNPC.esp` |
| `dialoguemisha` | The Bird's Eye | `1CD226:3DNPC.esp` |
| `DialogueMithrilan` | Tree Sprite | `2C904D:3DNPC.esp` |
| `dialoguemorviah` | The Winter Flower | `070058:3DNPC.esp` |
| `DialogueNair` | The Aldmeri Prisoner | `2CB19B:3DNPC.esp` |
| `DialogueOlivia` | A New Dawn | `036AD6:3DNPC.esp` |
| `DialogueOrenius` | Dialogue Orenius | `059F9D:3DNPC.esp` |
| `DialogueRaynes` | The Law Always Wins | `09F11B:3DNPC.esp` |
| `DialogueRinori` | Immortal Sin | `028404:3DNPC.esp` |
| `DialogueRumarin` | A Spell for Rumarin | `0AB6D8:3DNPC.esp` |
| `DialogueSalumEi` | Virtuous Blood | `09A517:3DNPC.esp` |
| `DialogueSkjel` | Tailor Made | `0D54B6:3DNPC.esp` |
| `dialoguesvashni` | The Hidden Blade | `054163:3DNPC.esp` |
| `DialogueTheRelic` | Relic's Revival | `044B3C:3DNPC.esp` |
| `DialogueThriceBitten` | Thrice Bitten, Once Shy | `27CF33:3DNPC.esp` |
| `DialogueTikrid` | The Bounty Hunter | `07A023:3DNPC.esp` |
| `DialogueTreads` | Treads the Ashes | `312F72:3DNPC.esp` |
| `dialoguetwotails` | A Warrior's Heart | `0671F5:3DNPC.esp` |
| `DialogueVinnius` | A New Dawn | `130796:3DNPC.esp` |
| `DialogueViranya` | Viranya Dialogue | `004991:3DNPC.esp` |
| `DialogueYtharil` | The Carver and The Collector | `0CB644:3DNPC.esp` |
| `DialogueZora` | A Field of Cotton | `03B254:3DNPC.esp` |
| `DJGQuest` | A Debt of Blood | `2CF3C0:3DNPC.esp` |
| `DJGQuest2` | As You Like It | `2CF48B:3DNPC.esp` |
| `ErevanQuest` | A Rose Without Thorns | `182E37:3DNPC.esp` |
| `GlathrielsBow` | Glathriel's Bow | `157064:3DNPC.esp` |
| `GorrQuest` | Pit Dogs | `171FD5:3DNPC.esp` |
| `HagCurseQuest` | The Curse | `2F282F:3DNPC.esp` |
| `hagquest` | Birds of a Feather | `1D094E:3DNPC.esp` |
| `Herranquest` | The Gales of Guilt | `24CEAA:3DNPC.esp` |
| `HorkerQuest` | The Way to a Big Oaf's Heart | `12E107:3DNPC.esp` |
| `hwsquest` | The House on the Hill | `219068:3DNPC.esp` |
| `KjoliQuest` | To Warm Sands | `1626B4:3DNPC.esp` |
| `LurgokQuest` | Bite the Hand That Feeds You | `1BD1F8:3DNPC.esp` |
| `MarlaDialogueArrest` | Arresting Marla | `2C2A67:3DNPC.esp` |
| `MorndasArgonianQuest` | Fenced In | `29844E:3DNPC.esp` |
| `Mzinchaleft3DNPC` | Mzinchaleft Quest | `2AB582:3DNPC.esp` |
| `Mzinchaleft3DNPC_2` | Mzinchaleft Quest | `2AC1DD:3DNPC.esp` |
| `Mzinchaleft3DNPC_3` | Mzinchaleft Quest | `2AD386:3DNPC.esp` |
| `Mzinchaleft3DNPC_4` | Mzinchaleft Quest | `2AD387:3DNPC.esp` |
| `Mzinchaleft3DNPC_5` | Mzinchaleft Quest | `2AD981:3DNPC.esp` |
| `Notice3DNPC` | Notice to Adventurers | `235909:3DNPC.esp` |
| `PaintingQuest` | A Thousand Words | `271DB3:3DNPC.esp` |
| `PaintingQuest_Post` | A Thousand Words - Post Quest | `272FA0:3DNPC.esp` |
| `RaynesGriffithQuest` | Brother and Keeper | `164D86:3DNPC.esp` |
| `RDQuest` | The Radiant Dark | `12A16A:3DNPC.esp` |
| `robbersrefuge3dnpc` | Robber's Refuge | `1F5362:3DNPC.esp` |
| `RumarinMeetObjective` | The Bladebinder | `237F97:3DNPC.esp` |
| `RumarinQuest` | A Spell for Rumarin | `145C24:3DNPC.esp` |
| `RumarinQuest2` | The Sleeping Giant | `185B23:3DNPC.esp` |
| `skjelquest` | A Good Fit | `2BB973:3DNPC.esp` |
| `SvashniMeetObjective` | The Bladebinder | `237F9D:3DNPC.esp` |
| `SvashniQuest` | The Way of the Nine | `14E08B:3DNPC.esp` |
| `TerynneQuest` | Transformation | `377D79:3DNPC.esp` |
| `VartheimQuest` | The Elven Sword | `18A9BD:3DNPC.esp` |
| `ViranyaQuest` | Vigilance and Virtue | `17A1F7:3DNPC.esp` |
| `warrensquest` | Stolen Property | `1C0F1E:3DNPC.esp` |
| `ZoraQuest` | The Children Fair | `147D05:3DNPC.esp` |

### Lunar Guard Integrated

- Plugin(s): `Lunar Guard Integrated - A Worldspace Addition.esp`
- What it is: New worldspace with the Lunar Guard order and Kharri; quests are dialogue-driven, no journal objectives.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **6**
- Note: Only one named quest ("Kharri Quest", 2 stages, 0 objectives). Treat it as a location to comment on.

| EditorID | Name | FormID |
|---|---|---|
| `LGIKharriQuest` | Kharri Quest | `000805:Lunar Guard Integrated - A Worldspace Addition.esp` |

### Olenveld

- Plugin(s): `Olenveld.esp`
- What it is: A frozen undead city: the dead should stay dead, sieges, renovating the city, a dead-trees blight, sewers.
- Named journal quests: **11** · Size: **M** · Suggested banter scenes: **12**

| EditorID | Name | FormID |
|---|---|---|
| `OlenveldAsAboveSoBelow` | As Above, So Below | `516251:Olenveld.esp` |
| `OlenveldBigWood` | Olenveld: Dead Trees | `516252:Olenveld.esp` |
| `OlenveldBOTE` | Beginning of the End | `50FC4D:Olenveld.esp` |
| `OlenveldCityRenovations` | Set in Stone | `516253:Olenveld.esp` |
| `OlenveldEtherealComplications` | Ethereal Complication | `5162B7:Olenveld.esp` |
| `OlenveldFromBelowWeGrow` | From the Depths we Grow | `516258:Olenveld.esp` |
| `OlenveldHarshWinds` | Harsh Winds | `5162C8:Olenveld.esp` |
| `OlenveldInsideOut` | Belly of the Beast | `51621B:Olenveld.esp` |
| `OlenveldPhase2` | Against Time | `51636C:Olenveld.esp` |
| `OlenveldSewerMaintenance` | The Lurking Fear | `516263:Olenveld.esp` |
| `OlenveldWarmWelcome` | Warm Welcome | `5162BC:Olenveld.esp` |

### M'rissi's Tails of Troubles

- Plugin(s): `MrissiTailOfTroubles.esp`
- What it is: A young Khajiit girl's nine-part story: memory loss, her clan, a ceremony.
- Named journal quests: **9** · Size: **M** · Suggested banter scenes: **8**

| EditorID | Name | FormID |
|---|---|---|
| `MRTstage1` | The Hunted Young One | `17229C:MrissiTailOfTroubles.esp` |
| `MRTstage2` | Total Recall | `1A9E06:MrissiTailOfTroubles.esp` |
| `MRTstage3` | Atonement | `260646:MrissiTailOfTroubles.esp` |
| `MRTstage3Bad` | The Taming of the Shrew | `554AD5:MrissiTailOfTroubles.esp` |
| `MRTstage4` | Echo from the Past | `2AD68D:MrissiTailOfTroubles.esp` |
| `MRTstage5` | Knowledge Is Power | `2CBD17:MrissiTailOfTroubles.esp` |
| `MRTstage6` | Feline Solidarity | `2D5F8D:MrissiTailOfTroubles.esp` |
| `MRTstage7` | Reconsolidation | `2F4705:MrissiTailOfTroubles.esp` |
| `MRTstage8` | Ceremonial Turmoil | `30DCA3:MrissiTailOfTroubles.esp` |

### Immersive World Encounters

- Plugin(s): `Immersive Encounters.esp`
- What it is: Roadside encounters with small quests: city raids, travelling bards, bounty hunts, the boy's endeavor, outbreaks.
- Named journal quests: **38** · Size: **M** · Suggested banter scenes: **15**

| EditorID | Name | FormID |
|---|---|---|
| `SetteAdventurer01` | Fellowship of Fighters | `77A9C3:Immersive Encounters.esp` |
| `SetteAdventurer02` | Show Me The Way | `5956AB:Immersive Encounters.esp` |
| `SetteAdventurer03` | Into the Deep | `692B80:Immersive Encounters.esp` |
| `SetteBard01` | We're Out of the Woods | `A970B4:Immersive Encounters.esp` |
| `SetteBard02Evelyna` | Beli Sut Salskap, En Sut Lo | `A970B9:Immersive Encounters.esp` |
| `SetteBard03Neddvir` | Yours Truly | `B9EA51:Immersive Encounters.esp` |
| `SetteBard04Roxelle` | Two Sisters | `06346F:Immersive Encounters.esp` |
| `SetteBard05` | The Touring Bard | `341AB6:Immersive Encounters.esp` |
| `SetteBladesDragonHunt` | Dragon Hunters | `9333F8:Immersive Encounters.esp` |
| `SetteBountyHunter01` | Suspect of Misfortune | `C0C928:Immersive Encounters.esp` |
| `SetteBoy00` | Boy's Endeavor | `6B51AC:Immersive Encounters.esp` |
| `SetteBoy01` | Bring Me Home | `6B51AD:Immersive Encounters.esp` |
| `SetteCitizen03` | A Fellow Traveler | `65B02E:Immersive Encounters.esp` |
| `SetteDA06` | Stronghold Celebration | `6DDA14:Immersive Encounters.esp` |
| `SetteGiftOfCharityFollowUp01` | O, Help Me Kind One | `E78043:Immersive Encounters.esp` |
| `SetteGiftOfCharityFollowUp02` | O, Help Me Kind One | `E7D14D:Immersive Encounters.esp` |
| `SetteGiftOfCharityFollowUp03` | O, Help Me Kind One | `1932FF:Immersive Encounters.esp` |
| `SetteGiftOfCharityFollowUp04` | O, Help Me Kind One | `6F9F38:Immersive Encounters.esp` |
| `SetteHusky01` | Without A Trace | `59055F:Immersive Encounters.esp` |
| `SetteHusky02` | The Pilgrim | `614103:Immersive Encounters.esp` |
| `SetteNord01` | When the Night Falls Down | `6140E8:Immersive Encounters.esp` |
| `SetteSoldiers01ImpObjA` | We Are the Imperial Legion | `F6E6A8:Immersive Encounters.esp` |
| `SetteSoldiers01ImpObjB` | We Are the Imperial Legion | `F788D9:Immersive Encounters.esp` |
| `SetteSoldiers01SonsObjA` | We Are the Children of Skyrim | `0A3649:Immersive Encounters.esp` |
| `SetteSoldiers01SonsObjB` | We Are the Children of Skyrim | `0A876E:Immersive Encounters.esp` |
| `SetteWERoad06Cont` | Bounty Hunt | `77FAC5:Immersive Encounters.esp` |
| `SetteWR01` | Outbreak | `49237A:Immersive Encounters.esp` |
| `SetteWR02` | Roadside Dispute | `9BBE88:Immersive Encounters.esp` |
| `WE_SetteDLC2Wilderness01` | Werewolf vs Werebear | `1866F4:Immersive Encounters.esp` |
| `WE_SetteQuestIntBoy00` | Boy's Endeavor | `5A8BAB:Immersive Encounters.esp` |
| `WEJS_SetteNecromancersForest` | Necromancers | `075013:Immersive Encounters.esp` |
| `WERJ_SetteMG01` | Wizards Gone Wild [Mis-Summoned Atronach] | `A9ABBC:Immersive Encounters.esp` |
| `WERJ_SetteMG03` | Wizards Gone Wild [Nelacar and Fantastic Beasts] | `37BBE3:Immersive Encounters.esp` |
| `WI_SetteCL02FollowUp` | Stolen Token | `111FC8:Immersive Encounters.esp` |
| `WI_SetteCLSiegeMarkarth` | The Raid of Markarth | `7BD9A3:Immersive Encounters.esp` |
| `WI_SetteCLSiegeSolitude` | The Raid of Solitude | `7E10E6:Immersive Encounters.esp` |
| `WI_SetteCLSiegeWhiterun` | The Raid of Whiterun | `6C04FC:Immersive Encounters.esp` |
| `WI_SetteCLSiegeWindhelm` | The Raid of Windhelm | `780D0B:Immersive Encounters.esp` |

### Penitus Oculatus

- Plugin(s): `Penitus_Oculatus.esp`
- What it is: Join the Emperor's guard after the Dark Brotherhood: Babette, Cicero, Amaund Motierre, radiant jobs.
- Named journal quests: **11** · Size: **M** · Suggested banter scenes: **10**

| EditorID | Name | FormID |
|---|---|---|
| `zzzPO00` | Penitus Oculatus | `0012D1:Penitus_Oculatus.esp` |
| `zzzPO01Informant` | Unfinished Business | `00A9C4:Penitus_Oculatus.esp` |
| `zzzPO02Babette` | Bad Blood | `004E19:Penitus_Oculatus.esp` |
| `zzzPO03Cicero` | Fool's Errand | `008968:Penitus_Oculatus.esp` |
| `zzzPO04Sanctuary` | A Nest of Vipers | `00CA4B:Penitus_Oculatus.esp` |
| `zzzPO05AmaundMotierre` | Loose Ends | `00DFE9:Penitus_Oculatus.esp` |
| `zzzPORadiant01` | Unfinished Business | `003884:Penitus_Oculatus.esp` |
| `zzzPORadiant02` | House Cleaning | `01B2C2:Penitus_Oculatus.esp` |
| `zzzPORadiant03` | Paperwork | `01B2CB:Penitus_Oculatus.esp` |
| `zzzPORadiant04` | Inquisition | `01BD9F:Penitus_Oculatus.esp` |
| `zzzPORadiant05` | Troubleshoot | `01CDD1:Penitus_Oculatus.esp` |

### Why I Came to Skyrim - Origin Stories (The Book of Origins)

- Plugin(s): `The Book of Origins.esp`
- What it is: Choose why your character came to Skyrim; 40 short origin quests (vampire crusade, silver hand, forsworn, path of the mage, etc.).
- Named journal quests: **40** · Size: **M** · Suggested banter scenes: **10**
- Note: Only one origin runs per playthrough; banter should be generic or keyed to the chosen origin.

| EditorID | Name | FormID |
|---|---|---|
| `Why_Bandit` | Left for Dead | `000017:The Book of Origins.esp` |
| `Why_DragonPriest` | Ashes of the Dragon Cult | `00001E:The Book of Origins.esp` |
| `Why_FindAdventurer` | Dark Trail | `000062:The Book of Origins.esp` |
| `Why_FindMageFriend` | The Best of Intentions | `00006A:The Book of Origins.esp` |
| `Why_FindVigilant` | The Last Vigil | `000069:The Book of Origins.esp` |
| `Why_Forsworn` | Blood of the Reach | `000018:The Book of Origins.esp` |
| `Why_GreatWarTraitor` | Blue Sapphire | `000B05:The Book of Origins.esp` |
| `Why_Guard` | Blind Justice | `000031:The Book of Origins.esp` |
| `Why_Hagraven` | The Price of Power | `00001D:The Book of Origins.esp` |
| `Why_Innocent` | No Questions Asked | `00002F:The Book of Origins.esp` |
| `Why_JoinBardQuest` | The Path of the Bard | `000083:The Book of Origins.esp` |
| `Why_JoinBrotherhoodQuest` | The Path of Shadows | `00007C:The Book of Origins.esp` |
| `Why_JoinCollegeQuest` | The Path of the Mage | `000074:The Book of Origins.esp` |
| `Why_JoinCompanionsQuest` | The Path of the Warrior | `00007B:The Book of Origins.esp` |
| `Why_JoinImperialQuest` | The Path of the Soldier | `000086:The Book of Origins.esp` |
| `Why_JoinMarriageQuest` | The Path of Love | `00008A:The Book of Origins.esp` |
| `Why_JoinStormcloaksQuest` | The Path of Freedom | `000088:The Book of Origins.esp` |
| `Why_JoinThievesQuest` | The Path of the Thief | `000080:The Book of Origins.esp` |
| `Why_Necromancer` | The Last Lesson | `000019:The Book of Origins.esp` |
| `Why_NPCsearch_BardSon` | Words Left Unspoken | `0000DF:The Book of Origins.esp` |
| `Why_NPCsearch_Knight` | Knight On The Road | `0000D2:The Book of Origins.esp` |
| `Why_RecoverFromBanditDungeon` | The Final Promise | `000056:The Book of Origins.esp` |
| `Why_RecoverFromDungeon` | Ash and Ancestry | `000052:The Book of Origins.esp` |
| `Why_RecoverFromDwemerDungeon` | Beneath the Brass | `000054:The Book of Origins.esp` |
| `Why_RecoverFromMerchant` | Trader's Folly | `000057:The Book of Origins.esp` |
| `Why_Sabrecat` | The Great Hunt | `00001A:The Book of Origins.esp` |
| `Why_SilverHand` | Hunter Becomes Hunted | `00001B:The Book of Origins.esp` |
| `Why_Vampire` | Vampire Crusade | `000008:The Book of Origins.esp` |
| `Why_VisitorQuest_Brawler` | Raise Those Fists | `0000C5:The Book of Origins.esp` |
| `Why_VisitorQuest_Chaos` | Chaos Incarnate | `0000C4:The Book of Origins.esp` |
| `Why_VisitorQuest_Gold` | Golden Touch | `0000B9:The Book of Origins.esp` |
| `Why_VisitorQuest_HighHrothgar` | Top of the World | `00009F:The Book of Origins.esp` |
| `Why_VisitorQuest_Home` | A Place To Call Home | `0000C0:The Book of Origins.esp` |
| `Why_VisitorQuest_Leap` | Chasing the Rush | `0000AE:The Book of Origins.esp` |
| `Why_VisitorQuest_Peak` | The Quiet Above | `0000AF:The Book of Origins.esp` |
| `Why_VisitorQuest_ShrineofAzura` | Sight to See | `00009A:The Book of Origins.esp` |
| `Why_VisitorQuest_Stones` | The Standing Stones | `0000AB:The Book of Origins.esp` |
| `Why_VisitorQuest_Thane` | Duty and Honor | `0000C9:The Book of Origins.esp` |
| `Why_VisitorQuest_Tourist` | Sightseeing | `0000A4:The Book of Origins.esp` |
| `Why_Werewolf` | Marked by the Moon | `00001C:The Book of Origins.esp` |

### The Tools of Kagrenac

- Plugin(s): `Tools of Kagrenac.esp`
- What it is: Find Kagrenac's Tools; Vivec's Trial of Wisdom, a labyrinth, Dwemer heritage.
- Named journal quests: **5** · Size: **M** · Suggested banter scenes: **8**

| EditorID | Name | FormID |
|---|---|---|
| `TOK_QUST_DialogueVonos` | Lost Heritage | `21F230:Tools of Kagrenac.esp` |
| `TOK_QUST_DialogueYassour` | My Precious | `21F231:Tools of Kagrenac.esp` |
| `TOK_QUST_KagrenacTools` | Kagrenac's Tools | `21F221:Tools of Kagrenac.esp` |
| `TOK_QUST_LabyrinthPuzzle` | Darkest Depths | `71C218:Tools of Kagrenac.esp` |
| `TOK_QUST_SunderVault` | Vivec's Trial of Wisdom | `24CBF6:Tools of Kagrenac.esp` |

### The Wanderer's Fair

- Plugin(s): `SkyrimFair.esp`
- What it is: A travelling fair with stalls, games and a passport stamp quest.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **6**

| EditorID | Name | FormID |
|---|---|---|
| `SkyrimFairPassport` | The Fair Passport | `0B0006:SkyrimFair.esp` |

### The Gift of Saturalia

- Plugin(s): `TheGiftofSaturalia.esp`
- What it is: Holiday quests in several towns: orphanage, Dawnstar joy, a lost dog, a song in the dark.
- Named journal quests: **6** · Size: **S** · Suggested banter scenes: **6**

| EditorID | Name | FormID |
|---|---|---|
| `Sat_Adoption` | Windhelm By The Sea | `000963:TheGiftofSaturalia.esp` |
| `Sat_Dog` | Lending a Paw | `0009A4:TheGiftofSaturalia.esp` |
| `Sat_Laugh` | The Joy of Dawnstar | `0008D3:TheGiftofSaturalia.esp` |
| `Sat_Music` | A Song in the Dark | `0009D2:TheGiftofSaturalia.esp` |
| `Sat_Orphanage` | Three Wise Men | `0008AA:TheGiftofSaturalia.esp` |
| `Sat_TheGiftofSaturalia` | The Gift of Saturalia | `000D61:TheGiftofSaturalia.esp` |

### Amorous Adventures (for OStim)

- Plugin(s): `SexLab-AmorousAdventures.esp`
- What it is: Romance quests with vanilla NPCs (Aela, Ysolda, Elisif, Serana's Mark ...). Adult content.
- Named journal quests: **35** · Size: **M** · Suggested banter scenes: **4**
- Note: NSFW. Keep banter teasing and non-explicit, or skip.

| EditorID | Name | FormID |
|---|---|---|
| `SexLabAmorousAdventuresAela` | The Huntress | `0376E9:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresAerin` | Love & Death | `060071:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresAnnekke` | Annekke's Release | `04C0EF:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresBear` | Loaded Bear | `59E183:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresBrelyna` | Spellbound | `366DAA:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresCamilla` | The Suitors | `000D62:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresCarlotta` | Her Heart | `32182D:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresCounseling` | [WIP] Dibellan Council | `20701B:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresDanica` | Passionate Priestess | `030041:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresDLC1_1` | Exquisite Corpse | `0BB119:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresDLC1_Arts` | Burning Inside | `16103F:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresDLC1_Main` | Crimson Love | `0F18AC:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresDLC1_Mark` | Serana's Mark | `29E32A:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresEbony` | Malacath Blues | `637A6F:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresElisif` | Widow's Rebirth | `07755B:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresElisif2` | Body Double | `6E77F6:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresFarkas` | Beast Within | `0376E7:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresGerdur` | Nordic Hospitality | `019C68:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresIdgrod` | Blinded Visions | `24EE2B:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresIrileth` | Private Desires | `01E7F1:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresJenassa` | Shadows & Scars | `1C19FA:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresLisette` | The Guile Song | `077556:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresMirabelle` | Strange Magic | `236198:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresNjada` | Njada's Secrets | `0376EA:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresOar` | Dead Bride's Curse | `097194:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresRikke` | Lost Battle | `6B104A:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresSenna` | Dibellan Arts | `0547E7:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresSteel` | Steel Angel | `2BBF62:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresSybille` | Fangs Of Desire | `077559:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresSylgja` | The Mark | `04E159:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresTailors` | Needles & Threads | `0935DF:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresTextiles` | Finest Materials | `09C31C:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresVilkas` | The Lone Wolf | `0376E8:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresWidow` | Widow's Sorrow | `077AC8:SexLab-AmorousAdventures.esp` |
| `SexLabAmorousAdventuresYsolda` | Tough Lessons | `057E2C:SexLab-AmorousAdventures.esp` |


## 5. Small quest mods

### The Frozen Heart

- Plugin(s): `ksws07_quest.esm`
- What it is: Book-collector Othriel and a frozen heart, shards to find.
- Named journal quests: **4** · Size: **S** · Suggested banter scenes: **5**

| EditorID | Name | FormID |
|---|---|---|
| `ksws07ArmorQuest` | Another Book for Othriel | `002444:ksws07_quest.esm` |
| `ksws07BookQuest` | A Book for Othriel | `000BBA:ksws07_quest.esm` |
| `ksws07MainQuest` | The Frozen Heart | `002086:ksws07_quest.esm` |
| `ksws07ShardsQuest` | Seeking Out Shards | `0024EF:ksws07_quest.esm` |

### Baba Yaga and the Labyrinth

- Plugin(s): `ksws03_quest.esp`
- What it is: Folk-tale witch Baba Yaga and her labyrinth.
- Named journal quests: **3** · Size: **S** · Suggested banter scenes: **4**

| EditorID | Name | FormID |
|---|---|---|
| `ksws03_house_quest` | The Walking Hut | `000949:ksws03_quest.esp` |
| `ksws03_main_quest` | The Wild Witch | `000AA2:ksws03_quest.esp` |
| `ksws03_tarot_quest` | Hagnes's Tarot Cards | `000AC8:ksws03_quest.esp` |

### Gravewind

- Plugin(s): `FalkreathShades.esp`
- What it is: Falkreath pines: lost in the woods, a realm lost to Oblivion.
- Named journal quests: **3** · Size: **S** · Suggested banter scenes: **4**

| EditorID | Name | FormID |
|---|---|---|
| `GRVEDestroyRealm01` | Lost to Oblivion | `4DCCF9:FalkreathShades.esp` |
| `GRVEMainQuest01` | In the Pines | `4CD9DA:FalkreathShades.esp` |
| `GRVEMainQuest02` | Lost in the Woods | `4D2AF7:FalkreathShades.esp` |

### Siege at Icemoth

- Plugin(s): `Siege at Icemoth.esp`
- What it is: Dragonborn-style Black Book and a siege at Icemoth, the Topaz Claw.
- Named journal quests: **4** · Size: **S** · Suggested banter scenes: **5**

| EditorID | Name | FormID |
|---|---|---|
| `HYORBlackBook08Quest` | Black Book: The Font of Memory | `59F97E:Siege at Icemoth.esp` |
| `HYORBookPointerMiscQST` | Caches of Skorjan Iron-Beard | `936795:Siege at Icemoth.esp` |
| `HYORdunIcemothQST` | Siege at Icemoth | `5A079F:Siege at Icemoth.esp` |
| `HYORdunWintershroudSanctumQST` | The Topaz Claw | `097057:Siege at Icemoth.esp` |

### Fists of Fury

- Plugin(s): `Fists of Fury - Skyrim.esp`
- What it is: Brawling circuit across Hjaalmarch, Eastmarch, the Rift.
- Named journal quests: **3** · Size: **S** · Suggested banter scenes: **4**

| EditorID | Name | FormID |
|---|---|---|
| `FOFMorthalBrawlerQuest` | Fists of Fury - Hjaalmarch | `149C95:Fists of Fury - Skyrim.esp` |
| `FOFRiftenBrawlerQuest` | Fists of Fury - The Rift | `04C991:Fists of Fury - Skyrim.esp` |
| `FOFWindhelmBrawlerQuest` | Fists of Fury - Eastmarch | `1D7962:Fists of Fury - Skyrim.esp` |

### College of Winterhold - Quest Expansion

- Plugin(s): `College Of Winterhold - Quest Expansion.esp`
- What it is: Real classes at the College: one quest per magic school plus curriculum.
- Named journal quests: **9** · Size: **S** · Suggested banter scenes: **5**

| EditorID | Name | FormID |
|---|---|---|
| `Cow_Breathing` | Rapture of the Deep | `000801:College Of Winterhold - Quest Expansion.esp` |
| `COW_CentralQuest` | College Curriculum | `00081D:College Of Winterhold - Quest Expansion.esp` |
| `Cow_Conjuration` | I Choose You, Familiar | `00086F:College Of Winterhold - Quest Expansion.esp` |
| `Cow_Conjuration_FightingScene` | Cow_Conjuration_Duplicate | `0009BF:College Of Winterhold - Quest Expansion.esp` |
| `Cow_Destruction` | A Test of Ice and Fire | `000873:College Of Winterhold - Quest Expansion.esp` |
| `Cow_enchantment` | Enchanted To Meet You | `000871:College Of Winterhold - Quest Expansion.esp` |
| `Cow_illusion` | Back-Stabbing Rodents | `000872:College Of Winterhold - Quest Expansion.esp` |
| `Cow_Reading` | Reading Comprehension 101 | `000870:College Of Winterhold - Quest Expansion.esp` |
| `Cow_restoration` | None Escape The Light | `00086E:College Of Winterhold - Quest Expansion.esp` |

### Forsworn Conspiracy - Quest Expansion

- Plugin(s): `Forsworn Conspiracy Quest Expansion.esp`
- What it is: Extra Markarth quests after the Forsworn Conspiracy.
- Named journal quests: **2** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `aaMS01New` | Blood for Blood, Silver for Silver | `000800:Forsworn Conspiracy Quest Expansion.esp` |
| `aaMS02New` | Forsworn But Not Forgotten | `000814:Forsworn Conspiracy Quest Expansion.esp` |

### Innocence Lost - Quest Expansion

- Plugin(s): `Innocence Lost - Quest Expansion.esp`
- What it is: Expands Aventus Aretino / Grelod.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `DB01_OptionalObjectives` | DB01_Opt | `000836:Innocence Lost - Quest Expansion.esp` |

### Caught Red Handed - Quest Expansion

- Plugin(s): `Caught Red Handed - Quest Expansion.esp`
- What it is: Expands the Riften Sapphire/Thieves misc quest.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `FreeformRiften11b` | A Strong Nord Woman | `000802:Caught Red Handed - Quest Expansion.esp` |

### Thieves Guild Alternative Endings

- Plugin(s): `TG Alternative Endings.esp`
- What it is: Choose other endings for the Guild line.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `TGAEDestroy` | Restore the Light | `00083D:TG Alternative Endings.esp` |

### Civil War Champions - Reduced Cut

- Plugin(s): `Civil War Champions - Reduced Cut.esp`
- What it is: Champion armor reward line.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `CWCRQuest` | Civil War Champion Armor | `000800:Civil War Champions - Reduced Cut.esp` |

### Mephala's Curse - Whispering Door addon

- Plugin(s): `EbonyBladeCurse.esp`
- What it is: The Ebony Blade curse after The Whispering Door.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `DA08MephalaHunt` | The Fate of the Ebony Blade | `000807:EbonyBladeCurse.esp` |

### The Taste of Death - Quest Addon

- Plugin(s): `TasteOfDeath_Addon_Dialogue.esp`
- What it is: Namira cannibal cult follow-ups: jail, extortion.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `madNamiraAddonQuest` | A Bitter Aftertaste | `000050:TasteOfDeath_Addon_Dialogue.esp` |

### The Rot Below

- Plugin(s): `CJ03Elroy.esp`
- What it is: A rot spreading under a village.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `CJ03RotBelowMQ` | The Rot Below | `02DA43:CJ03Elroy.esp` |

### Bark and Bite (Witcher-inspired)

- Plugin(s): `Tree Contract Mod.esp`
- What it is: A monster contract in the Witcher style.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `TCMSheoTreeQuest` | Bark and Bite | `000009:Tree Contract Mod.esp` |

### The Hunt for the Spectre (Elden Ring-inspired)

- Plugin(s): `Hunt for the Spectre.esp`
- What it is: Hunt a spectral boss.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `HSHuntForSpectreQuest` | _(localized or no journal name)_ | `000800:Hunt for the Spectre.esp` |

### Calling the Watchmaker (Lovecraftian)

- Plugin(s): `Sithis Mod - Lovecraftian Inspired Quest.esp`
- What it is: Cosmic horror quest about Sithis.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `SMQuest` | Calling the Watchmaker | `000892:Sithis Mod - Lovecraftian Inspired Quest.esp` |

### It Came from Akavir

- Plugin(s): `It Came from Akavir.esp`
- What it is: An Akaviri threat washes ashore.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `KMMKamalQuest` | It Came from Akavir | `000001:It Came from Akavir.esp` |

### Talos' Tease

- Plugin(s): `Talos' Tease - Starting Quest.esp`
- What it is: Starting quest around Talos worship.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `TT_TalosTease_QST` | Talos Tease | `000001:Talos' Tease - Starting Quest.esp` |

### Slays-Many-Beasts

- Plugin(s): `Slays-Many-Beasts Quest Mod.esp`
- What it is: Argonian beast-hunter quest (journal-log style).
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `SMBMainQuest` | _(localized or no journal name)_ | `000001:Slays-Many-Beasts Quest Mod.esp` |

### Walks-Distant-Sands

- Plugin(s): `Walks-Distant-Sands Quest Mod.esp`
- What it is: Argonian traveller quest, M'aiq cameo.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `WDSMainQuest` | Walks-Distant-Sands | `000003:Walks-Distant-Sands Quest Mod.esp` |

### Darbalag

- Plugin(s): `Darbalag - Quest Mod.esp`
- What it is: Orc quest (journal-log style).
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `DBQDarbalagQuest` | _(localized or no journal name)_ | `000002:Darbalag - Quest Mod.esp` |

### Once We Were Here

- Plugin(s): `Once We Were Here - Quest Mod.esp`
- What it is: Ruins-and-memories quest.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `OWWHMainQuest` | Once We Were Here | `000002:Once We Were Here - Quest Mod.esp` |

### Save the Icerunner

- Plugin(s): `SaveTheIcerunner.esp`
- What it is: Expands the Icerunner wreck: Jaree-Ra jail and revenge.
- Named journal quests: **2** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `STIJareeRaJailQuest` | Jaree-Ra goes to jail | `00082C:SaveTheIcerunner.esp` |
| `STIJareeRaRevengeQuest` | Jaree-Ra seeks revenge | `000836:SaveTheIcerunner.esp` |

### Prisoner Mod (Aradell)

- Plugin(s): `PrisonerMod.esp`
- What it is: A prisoner NPC quest.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `PMAradellQuest` | _(localized or no journal name)_ | `000007:PrisonerMod.esp` |

### Dungeon Delver (Pike)

- Plugin(s): `Dungeon Delver Mod.esp`
- What it is: Dungeon-delver NPC quest.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `DDPikeQuest` | _(localized or no journal name)_ | `000000:Dungeon Delver Mod.esp` |

### Morskom Estate

- Plugin(s): `Morskom.esp`
- What it is: "A Home Abandoned" - reclaim a ruined estate as a home (15 objectives).
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `MEQuestMain` | A Home Abandoned | `15A7F1:Morskom.esp` |

### An Evening With Angi

- Plugin(s): `An Evening With Angi.esp`
- What it is: Evening with Angi, the archer of Angi's Camp.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `RES_AngiQuest` | An Evening With Angi | `000800:An Evening With Angi.esp` |

### Become a Bard

- Plugin(s): `BecomeABard.esp`
- What it is: Perform at taverns and for jarls; spy jobs.
- Named journal quests: **4** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `_LP_BardJarlQuest` | _(localized or no journal name)_ | `027C1F:BecomeABard.esp` |
| `_LP_BardAudienceQuest` | _(localized or no journal name)_ | `030E67:BecomeABard.esp` |
| `_LP_BardTavernQuest` | _(localized or no journal name)_ | `027C20:BecomeABard.esp` |
| `_LP_BardSpyJobQuest` | _(localized or no journal name)_ | `034EB7:BecomeABard.esp` |

### Bards Reborn - Student of Song

- Plugin(s): `BardsRebornStudentofSong.esp`
- What it is: Bard college student path.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `BardsRebornBardsCollegeQuest` | Study at the Bards College | `06673B:BardsRebornStudentofSong.esp` |

### The City of Crossed Daggers - Riften Expansion

- Plugin(s): `Riften Expansion.esp`
- What it is: Expanded Riften with a vampire bear-clan quest.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `RTBearheartVampireQuest` | The Black Bear of the Clan | `37F320:Riften Expansion.esp` |

### Ivy's Riverwood Overhaul

- Plugin(s): `Ivy Riverwood Overhaul.esp`
- What it is: "Lights in the Dark" - missing Aelara.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `IvyAelaraMissingQuest` | Lights in the Dark | `000006:Ivy Riverwood Overhaul.esp` |

### Skybound Underhang Camp

- Plugin(s): `RiverwoodBandits.esp`
- What it is: "Riverwood Extortion" - bandits shake down Gerdur.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `RWBGerdurQuest01` | Riverwood Extortion | `00090D:RiverwoodBandits.esp` |

### Everdamned

- Plugin(s): `Everdamned.esp`
- What it is: Vampire overhaul; "Blue Blood" quest for vampire players.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `ED_Mechanics_BlueBlood_Quest` | Blue Blood | `47F5D9:Everdamned.esp` |

### Adventurer's Start (Alternate Perspective add-ons)

- Plugin(s): `AP - Missile Additional Starts.esp`, `AP - Missile Additional Bruma Starts.esp`, `AlternatePerspective.esp`
- What it is: Alternate-start openings: ambushed, bounty hunter, prisoner, Kawoosh.
- Named journal quests: **23** · Size: **S** · Suggested banter scenes: **3**

Quest names (type x count): Ambushed x9, Bounty Hunter x8, Prisoner x5, Kawoosh!

### Skyrim Realistic Conquering

- Plugin(s): `SRC - All In One.esp`
- What it is: Conquer dungeons; Ironbacked Traitor and Pinefrost Tower supply quests.
- Named journal quests: **2** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `SRC_IBH_SQ01` | The Ironbacked Traitor | `0A2982:SRC - All In One.esp` |
| `SRC_PFTSuppliesQuest` | Supplies for Pinefrost Tower | `0EEF45:SRC - All In One.esp` |

### Quest-expansion mods that only edit vanilla quests (no new quest records)

These change vanilla quests the party will already comment on; fold them into the vanilla scene counts (write lines that fit the expanded versions): The Cursed Tribe QE (DA06), The Whispering Door QE (DA08), The Only Cure QE (DA13), House of Horrors QE (DA10), The Heart of Dibella QE (T01), Infiltration QE (dunTrevasWatchQST), Rising at Dawn overhaul (VC01), Paarthurnax Quest Expansion (MQPaarthurnax + Skyhaven Temple), Nilheim Misc QE (dunNilheimQST), Headhunter - Bounties Redone (BQ01-04), At Your Own Pace (MQ / College / thanes pacing), Favor Quests Separated (vanilla favors split into journal quests), Miscellaneous Quests are Favors.


## 6. Other (non-party) follower quest mods

Not our 8 followers, but their quests are real content the party can witness. Keep these light (party reacting to that follower's drama).

### Ashe - Crystal Heart / Fire and Blood

- Plugin(s): `Ashe - Fire and Blood.esp`
- What it is: Ashe the ashen-haired mercenary: borrowed soul, oath echoes, shattered orphans, epilogue.
- Named journal quests: **14** · Size: **M** · Suggested banter scenes: **6**

| EditorID | Name | FormID |
|---|---|---|
| `MM_AMQ_01` | A Borrowed Soul | `756FEA:Ashe - Fire and Blood.esp` |
| `MM_AMQ_02` | All For One | `BB194C:Ashe - Fire and Blood.esp` |
| `MM_AMQ_03` | Oath Echoes | `BC5D8F:Ashe - Fire and Blood.esp` |
| `MM_AMQ_04` | Shadows of the Past | `00AA1A:Ashe - Fire and Blood.esp` |
| `MM_AMQ_05` | Through Hell and High Water | `056A66:Ashe - Fire and Blood.esp` |
| `MM_AMQ_06` | One For All | `C07BE5:Ashe - Fire and Blood.esp` |
| `MM_AMQ_06a` | Shattered Orphans | `C07BE9:Ashe - Fire and Blood.esp` |
| `MM_AMQ_06b` | Binding Blade | `C11E04:Ashe - Fire and Blood.esp` |
| `MM_AMQ_06c` | Beyond the Blade - OLD QUEST | `C11E05:Ashe - Fire and Blood.esp` |
| `MM_AMQ_06cNEW` | Beyond the Blade | `380306:Ashe - Fire and Blood.esp` |
| `MM_AMQ_07` | Go Beyond - Vestiges Reborn | `D6A70C:Ashe - Fire and Blood.esp` |
| `MM_AMQ_07Epilogue` | Bound by Flame and Crystal | `E5DA07:Ashe - Fire and Blood.esp` |
| `MM_AsheIntro` | The Ashen-Haired Mercenary | `0A7946:Ashe - Fire and Blood.esp` |
| `MM_FriendshipQuest` | Whispers of White Hair | `1A9DEE:Ashe - Fire and Blood.esp` |

### Heart of Ice - Astrid

- Plugin(s): `SM_Astrid.esp`
- What it is: Outlander Astrid: drink and brawl, the letter, wedding, back to Roscrea, several endings.
- Named journal quests: **10** · Size: **M** · Suggested banter scenes: **4**

| EditorID | Name | FormID |
|---|---|---|
| `SM_AstridDrinkQuest` | Drink and Brawl | `08443E:SM_Astrid.esp` |
| `SM_AstridEnding` | Back to Roscrea | `0A2BD0:SM_Astrid.esp` |
| `SM_AstridFinale` | Heart of Ice | `08443F:SM_Astrid.esp` |
| `SM_AstridLetterQuest` | The Letter | `08443D:SM_Astrid.esp` |
| `SM_AstridStart` | The Outlander | `084441:SM_Astrid.esp` |
| `SM_AstridStrollQuest` | A Stroll Around Skyrim | `08443C:SM_Astrid.esp` |
| `SM_AstridWedding` | Forever Together | `084440:SM_Astrid.esp` |
| `SM_DFAQuest` | Dye for Astrid | `07F2FF:SM_Astrid.esp` |
| `SM_GetToTavern` | A Time to Relax | `397910:SM_Astrid.esp` |
| `SM_WorstEnding` | No Way Back | `443BE3:SM_Astrid.esp` |

### Flint the Minotaur

- Plugin(s): `Flint9.esp`
- What it is: Minotaur follower: friendship or romance, Alessian ceremony.
- Named journal quests: **4** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `EGG1FlintFriendship` | Courting the Beast | `6A487E:Flint9.esp` |
| `EGG1FlintPlatonic` | An Unlikely Duo | `C6896C:Flint9.esp` |
| `EGG1FlintPostRomance` | An Alessian Ceremony | `89B8B8:Flint9.esp` |
| `EGG1FlintRelationshipIntro` | More Than a Monster | `C5C2A9:Flint9.esp` |

### Thogra gra-Mugur

- Plugin(s): `DK_Thogra.esp`
- What it is: Orc follower: Thogra's Revenge, marriage at Largashbur or Temple of Mara.
- Named journal quests: **3** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `dk_ThograMain` | Thogra's Revenge | `167FDE:DK_Thogra.esp` |
| `dk_ThograMarriageMara` | Marry Thogra - Temple of the Divines | `1F0E0E:DK_Thogra.esp` |
| `dk_ThograMarriageOrc` | Marry Thogra - Largashbur | `232B5A:DK_Thogra.esp` |

### Auri - Song of the Green

- Plugin(s): `018Auri.esp`
- What it is: Bosmer follower friend quest.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `018AuriFriendQuest` | Song of the Green | `03E4B1:018Auri.esp` |

### Serana Dialogue Add-On

- Plugin(s): `SeranaDialogAddon.esp`, `SDA Campfire Patch.esp`
- What it is: Serana romance / dates / trust conversations.
- Named journal quests: **12** · Size: **S** · Suggested banter scenes: **3**

| EditorID | Name | FormID |
|---|---|---|
| `SDA_CampfireSnuggle` | Snuggly Snuggle Time! | `005900:SDA Campfire Patch.esp` |
| `SDA_GetHorseQuest` | Get Serana a Horse! | `20DAC4:SeranaDialogAddon.esp` |
| `SDA_GiveYouQuest` | Serana Gives You Gifts! | `2BEE3F:SeranaDialogAddon.esp` |
| `SDA_OrderDrinks` | Serana Talking with Barkeep | `3293F2:SeranaDialogAddon.esp` |
| `SDA_SeranaRomance01` | An Unexpected Meeting | `A2D564:SeranaDialogAddon.esp` |
| `SDA_SeranaRomance08` | Determination | `B2A83E:SeranaDialogAddon.esp` |
| `SDA_SeranaRomance09` | A New Family | `B2A842:SeranaDialogAddon.esp` |
| `SDA_SeranaRomance10` | A New Covenant | `B2F967:SeranaDialogAddon.esp` |
| `SDA_SeranaRomance10Trust` | Trust Conversation | `46C3EC:SeranaDialogAddon.esp` |
| `SDA_SeranaRomance11` | A Date at the Bannered Mare | `C73A4A:SeranaDialogAddon.esp` |
| `SDA_SeranaRomance13` | Undying Love | `347A07:SeranaDialogAddon.esp` |
| `SDA_SneakQuest` | SDA_SneakQuest | `E22104:SeranaDialogAddon.esp` |

### Improved Follower Dialogue - Lydia

- Plugin(s): `ImprovedCompanionsBoogaloo.esp`
- What it is: "The King of Cowards" personal quest.
- Named journal quests: **1** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `0ICB_LydiaPersonalQuest` | The King of Cowards | `159008:ImprovedCompanionsBoogaloo.esp` |

### Follower Dialogue Expansion (Faralda, Jenassa, Erik, Mjoll, Aela)

- Plugin(s): `FDE Faralda.esp`, `FDE Jenassa.esp`, `FDE Erik.esp`, `FDE Mjoll.esp`, `FDE Aela Part 2.esp`
- What it is: Personal quests for vanilla followers.
- Named journal quests: **6** · Size: **S** · Suggested banter scenes: **2**

| EditorID | Name | FormID |
|---|---|---|
| `aaAela8ArnbjornJournalQuest` | _(localized or no journal name)_ | `0009F7:FDE Aela Part 2.esp` |
| `aaErikCompanionJoin` | Erik the Shield Brother | `0008E8:FDE Erik.esp` |
| `aaFaraldaQ1` | With Love, Eilonwy, Part 1 | `00096A:FDE Faralda.esp` |
| `aaFaraldaQ2` | With Love, Eilonwy, Part 2 | `000A40:FDE Faralda.esp` |
| `aaJenassaAmor5RomanceQuest` | Shadows of the Past | `000D03:FDE Jenassa.esp` |
| `aaMjollAerinQ` | Aerin the Man | `0008E0:FDE Mjoll.esp` |

### Yoana

- Plugin(s): `BB02YoanaFollower.esp`
- What it is: Custom voiced follower personal quest.
- Named journal quests: **2** · Size: **S** · Suggested banter scenes: **1**

| EditorID | Name | FormID |
|---|---|---|
| `BB02_YMQ` | The Man Who Cut Me in Half | `00092B:BB02YoanaFollower.esp` |
| `BB02YoanaFollowerQuest` | _(localized or no journal name)_ | `000813:BB02YoanaFollower.esp` |


## 7. Totals and top 20

**Suggested scenes, all sources: 1046.**

Creation Club is not ranked as one block (it is many small Creations); its combined total is 99.

| Rank | Source | Scenes |
|---|---|---|
| 1 | Vanilla - Main quest (MQ) | 50 |
| 2 | Dragonborn | 50 |
| 3 | Vanilla - Major side quests (MS / T / NN / VC / dun / Bards College) | 45 |
| 4 | Dawnguard | 45 |
| 5 | Legacy of the Dragonborn | 45 |
| 6 | Vanilla - Daedric quests (DA) | 40 |
| 7 | VIGILANT | 40 |
| 8 | Vanilla - Civil War (CW) | 35 |
| 9 | Glenmoril | 35 |
| 10 | Beyond Skyrim - Bruma | 35 |
| 11 | Vanilla - Dark Brotherhood (DB) | 30 |
| 12 | Interesting NPCs (3DNPC) | 30 |
| 13 | Vanilla - Thieves Guild (TG) | 25 |
| 14 | Unslaad | 25 |
| 15 | Wyrmstooth | 25 |
| 16 | Vanilla - Companions (C / CR) | 22 |
| 17 | Vanilla - College of Winterhold (MG / MGR) | 22 |
| 18 | DAc0da | 20 |
| 19 | The Forgotten City | 20 |
| 20 | SIRENROOT - Deluge of Deceit | 18 |
