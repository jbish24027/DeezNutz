p=r"C:\1. AUTHORIA\_tools\follower-banter\STYLE-GUIDE.md"
s=open(p,encoding="utf-8").read()
s=s.replace("- Kaidan, Gore and Val are rivals for her; rivalry grows with romance",
"- **FIVE rivals for Luna: Kaidan, Gore, Val, Serana, Ashe** (user 10-18). Rivalry grows with romance; each rival's romance progress comes from their own mod (Serana: SDA romance quest chain + its on/off setting, see serana.md; Ashe: her romance, see ashe.md). Serana: dry vampire wit, centuries old, teases the boys. Ashe: denies jealousy as 'data' ('rivalry is inefficient'), then admits she's 'competitive'. Kaidan, Gore and Val are rivals for her too; rivalry grows with romance")
s=s.replace("- Remi has her own romance in her mod but in banter she's the gossip/sister, not a rival.",
"- Remi has her own romance in her mod but in banter she's the gossip/sister, not a rival.\n- Serana's voice: the SDA recordings (Kerstyn Unger) are the clone source, by the user's personal-use decision. Ashe: Anna Rust's lines. Ashe's mod has an orphan boy named Remy: never confuse him with our Remi.")
open(p,"w",encoding="utf-8").write(s); print("ok")
