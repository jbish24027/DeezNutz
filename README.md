# DeezNutz — Authoria custom work

Our own stuff for the Authoria Skyrim setup, with history. Private.

## What's where

| Folder | What it holds | Source |
|---|---|---|
| `notes/installs-and-updates` | Install plans, "mods added" ledgers, update notes, batch plans | **Moved** from `C:\1. AUTHORIA` root |
| `notes/visuals-and-performance` | Picta / CS / Bottled / PBR / grass / lighting / water / FPS notes | Moved |
| `notes/characters-and-voice` | Eleonora DBVO, Lydia, Serana, Kaidan, SMP hair, UBE skin/dirt notes | Moved |
| `notes/gameplay-and-mods` | Everything else: Requiem, MCM, stances, quivers, homes, misc plans | Moved |
| `tools/` | Helper scripts and project folders | **Copy** of `C:\1. AUTHORIA\_tools` |
| `mods/` | Hand-authored mod folders (`Authoria - …`, `houseCARL - Authoria - …`) | **Copy** of `C:\1. AUTHORIA\mods` — MO2 is untouched |

`notes/MOVED-FROM-MO2-ROOT-20261022.csv` lists every note that was moved and where it went.

## What is deliberately left out

- **Generated output** (DynDOLOD, xLODGen, TexGen, PG, Pandora, Synthesis, xEdit, BodySlide, UBE Converter output, RFTI) — the tools rebuild it.
- **Grass caches, NPC / 3DNPC merges, BodySlide projects, Vanilla Bodyslides, SMP Hair Grafts** — bulk, regenerable.
- **Third-party binaries**: dlss-unlocked / OptiScaler, main menu videos, the built Reqtificator `app` and its backups (its `Source` is kept).
- Any single file over 50 MB, `bin/`, `obj/`, `build/`, `__pycache__`, `.pdb`, `.mohidden`, `.bak*`.

## Updating

`tools/` and `mods/` are snapshots. To refresh them, ask Claude to "sync the repo" — it re-copies from the MO2 instance with the same rules, then commits and pushes.

Files are stored byte-for-byte (`.gitattributes: * -text`), so CRLF line endings in game files are never changed.
