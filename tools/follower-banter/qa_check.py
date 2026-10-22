"""QA a banter script file (or all of them). Usage: python qa_check.py [file ...]
Flags rule breaks from STYLE-GUIDE.md. Prints a summary per file."""
import glob, os, re, sys

SPK = {"KAIDAN", "GORE", "VAL", "REMI", "XELZAZ", "INIGO", "LUCIEN", "REDCAP", "SERANA", "ASHE", "LUNA"}
DESK = r"C:\Users\User\Desktop"
files = sys.argv[1:] or (glob.glob(os.path.join(DESK, "FOLLOWER BANTER - SCRIPT*.txt")) +
                         glob.glob(os.path.join(DESK, "FOLLOWER BANTER SCRIPTS", "*.txt")))

head_re = re.compile(r"^([A-Z]{1,3}\d+)\. (.+)$")
line_re = re.compile(r"^([A-Z]+):\s+(.*)$")
all_ids = {}

def check(path):
    talks, cur, issues = [], None, []
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        s = raw.rstrip("\n")
        m = head_re.match(s)
        if m:
            cur = {"id": m.group(1), "title": m.group(2), "when": "", "lines": [], "n": n}
            talks.append(cur); continue
        if cur is None: continue
        if s.startswith("When:"):
            cur["when"] = s[5:].strip(); continue
        m = line_re.match(s)
        if m and m.group(1) in SPK:
            cur["lines"].append((m.group(1), m.group(2), n))
        elif m and m.group(1).isupper() and len(m.group(1)) > 2 and m.group(1) not in ("WHEN", "NOTE", "CHANGE", "LOVE", "CUT"):
            issues.append(f"{n}: unknown speaker {m.group(1)}")
    luna = 0
    for t in talks:
        tid = t["id"]
        if tid in all_ids: issues.append(f"{t['n']}: duplicate ID {tid} (also in {all_ids[tid]})")
        all_ids[tid] = os.path.basename(path)
        spk = [a for a, _, _ in t["lines"]]
        if not spk: issues.append(f"{t['n']}: {tid} has no lines"); continue
        if "LUNA" in spk: luna += 1
        if len(set(spk) - {"LUNA"}) < 1: issues.append(f"{t['n']}: {tid} has no follower")
        if len(t["lines"]) > 14: issues.append(f"{t['n']}: {tid} is long ({len(t['lines'])} lines)")
        when = t["when"].lower()
        for who, txt, ln in t["lines"]:
            low = txt.lower()
            if len(txt.split()) > 32: issues.append(f"{ln}: long line ({len(txt.split())} words)")
            if "dragonborn" in low and "dragonborn" not in when and "dragon" not in when:
                issues.append(f"{ln}: 'Dragonborn' said but When has no Dragonborn gate")
            if who == "KAIDAN" and "beard" in low and "my beard" in low or ("kaidan" in low and "beard" in low and "no beard" not in low):
                issues.append(f"{ln}: Kaidan beard?")
            if re.search(r"rosalind|blooded dawn|dagon cult|the cult", low) and "kaidan" in (when + " ".join(spk).lower()) and "cult" not in when and "blood and fire" not in when:
                issues.append(f"{ln}: Kaidan cult reference without late gate")
            if "goblin" in low and who != "REDCAP" and "not" not in low:
                issues.append(f"{ln}: someone calls Redcap a goblin?")
            if who == "REDCAP" and len(txt.split()) > 3 and not re.search(r"\w\.\s", txt):
                issues.append(f"{ln}: Redcap not in one-word style")
            if re.search(r"\bvalerius\b", low) and who not in ("REMI", "LUCIEN", "VAL"):
                pass
    print(f"\n== {os.path.basename(path)}: {len(talks)} talks, Luna in {luna} ({(100*luna//max(1,len(talks)))}%), {len(issues)} flags")
    for i in issues[:60]: print("   ", i)
    return len(talks)

total = sum(check(f) for f in files)
print(f"\nTOTAL talks: {total}")
