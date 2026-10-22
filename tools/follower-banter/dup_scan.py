"""Find repeated lines and repeated titles across all banter scripts."""
import glob, os, re, collections
DESK = r"C:\Users\User\Desktop"
files = glob.glob(os.path.join(DESK, "FOLLOWER BANTER - SCRIPT*.txt")) + glob.glob(os.path.join(DESK, "FOLLOWER BANTER SCRIPTS", "*.txt"))
lines = collections.defaultdict(list); titles = collections.defaultdict(list)
head = re.compile(r"^([A-Z]{1,3}\d+)\. (.+?) \(")
spk = re.compile(r"^([A-Z]+):\s+(.*)$")
cur = None
for f in files:
    b = os.path.basename(f)
    for s in open(f, encoding="utf-8"):
        s = s.strip()
        m = head.match(s)
        if m: cur = m.group(1); titles[m.group(2).strip().upper()].append(f"{cur}@{b[:20]}"); continue
        m = spk.match(s)
        if m and cur:
            t = re.sub(r"[^a-z ]", "", m.group(2).lower()).strip()
            if len(t.split()) >= 6: lines[(m.group(1), t)].append(f"{cur}@{b[:20]}")
dl = [(k, v) for k, v in lines.items() if len({x.split('@')[0] for x in v}) > 1]
dt = [(k, v) for k, v in titles.items() if len(v) > 1]
print("repeated lines (6+ words, same speaker):", len(dl))
for k, v in dl[:40]: print(" ", k[0], "|", k[1][:70], "|", v)
print("repeated titles:", len(dt))
for k, v in dt[:40]: print(" ", k, v)
