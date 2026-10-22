p = r"C:\1. AUTHORIA\_tools\follower-banter\STYLE-GUIDE.md"
s = open(p, encoding="utf-8").read()
s = s.replace("Goal: ~1000 short scenes", "Goal: ~3,500 short scenes (user target 3,000-4,000)")
s = s.replace("- Speaker labels: KAIDAN, GORE, VAL, REMI, XELZAZ, INIGO, LUCIEN, REDCAP. Pad to align as in existing files.",
              "- Speaker labels: KAIDAN, GORE, VAL, REMI, XELZAZ, INIGO, LUCIEN, REDCAP, SERANA, ASHE, LUNA. Pad to align as in existing files.")
s = s.replace("- Don't put Luna's words in her mouth.",
              "- Don't give Luna romance commitments, quest decisions, or noticing Kaidan's crush before K_TOG.")
if "## Cast additions" not in s:
    s += r"""
## Cast additions
- **Serana** and **Ashe** join the cast. Read `research\bibles\serana.md` and `ashe.md` before writing them; until those files exist, do not write them.

## IDs and files (large-scale production)
- Each writer gets an ID prefix and a file name from `MANIFEST.md`. IDs are `<PREFIX><number>` from 1, never reused.
- Write the script file to `C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\<file>.txt` and trigger rows to `C:\1. AUTHORIA\_tools\follower-banter\triggers\<file>.md`.
- Spread speakers: every follower in your scope should appear; Kaidan most; Luna in about 1/3 of talks.
- No two talks in a file on the same joke. List your topics first, then write.
"""
open(p, "w", encoding="utf-8").write(s)
print("ok")
