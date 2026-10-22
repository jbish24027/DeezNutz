r"""Measure the Wanderer's Fair arrival burst from the game's own logs.

Usage:  python -I measure.py [--docs "<Documents\\My Games\\Skyrim Special Edition>"] [--label before|after]

Reads:  Logs\Script\Papyrus.0.log, SKSE\Walk With Me.log, SKSE\OBody.log, SKSE\SchlongsOfSkyrim.log
Arrival = the first Walk With Me scan whose high-process actor count jumps to >= 120 (the fair cell load).
Window  = arrival .. arrival + 70 s (the length of the bad minute on 2026-10-14).
Prints the numbers the before/after comparison is defined on:
  1. Papyrus stack dumps inside the window, and which script sat on top of each dumped stack
  2. the VM 'Frequency' counts logged for the three burst scripts in the window
  3. seconds from arrival to the cull's 'SkyrimFairCrowdCull: ... switched' line
  4. OBody 'apply preset to' calls for fair NPCs and SOS per-actor lines for 7B-prefixed (SkyrimFair.esp) actors
"""
import argparse, collections, datetime as dt, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("--docs", default=os.path.join(os.path.expanduser("~"), "Documents", "My Games", "Skyrim Special Edition"))
ap.add_argument("--label", default="")
ap.add_argument("--window", type=int, default=70, help="seconds after arrival to count (default 70)")
ap.add_argument("--jump", type=int, default=120, help="high-actor count that marks the fair arrival (default 120)")
a = ap.parse_args()

papy = os.path.join(a.docs, "Logs", "Script", "Papyrus.0.log")
wwm = os.path.join(a.docs, "SKSE", "Walk With Me.log")
obody = os.path.join(a.docs, "SKSE", "OBody.log")
sos = os.path.join(a.docs, "SKSE", "SchlongsOfSkyrim.log")

def wwm_arrival():
    """Return (datetime, actors) of the first scan with high actors >= jump, else None."""
    rx = re.compile(r"^\[(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)\.\d+\].*high actors=(\d+)")
    with open(wwm, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = rx.match(line)
            if m and int(m.group(2)) >= a.jump:
                return dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S"), int(m.group(2))
    return None

def papy_ts(line, day):
    m = re.match(r"^\[(\d\d)/(\d\d)/(\d{4}) - (\d\d):(\d\d):(\d\d)(AM|PM)\]", line)
    if not m: return None
    mo, d, y, h, mi, s, ap_ = m.groups()
    h = int(h) % 12 + (12 if ap_ == "PM" else 0)
    return dt.datetime(int(y), int(mo), int(d), h, int(mi), int(s))

arr = wwm_arrival()
if not arr:
    print("no Walk With Me scan reached", a.jump, "high actors - is the log from a fair visit?"); sys.exit(1)
t0, actors0 = arr
t1 = t0 + dt.timedelta(seconds=a.window)
print(f"== fair arrival {a.label} ==")
print(f"arrival (Walk With Me): {t0:%Y-%m-%d %H:%M:%S}  high actors={actors0}")
print(f"window: {t0:%H:%M:%S} .. {t1:%H:%M:%S} ({a.window} s)")

# 1 + 2 + 3: Papyrus
dumps = 0; top = collections.Counter(); freq = {}; cull_t = None; errs = collections.Counter()
frame_rx = re.compile(r"\]\.(\w+)\.(\w+)\(\)")
in_dump = False; first = False; cur = None
with open(papy, encoding="utf-8", errors="replace") as f:
    for line in f:
        ts = papy_ts(line, t0.date())
        if ts: cur = ts
        if cur is None or cur < t0: continue
        if "SkyrimFairCrowdCull:" in line and "switched" in line and cull_t is None and cur >= t0:
            cull_t = cur
        if cur > t1 + dt.timedelta(seconds=120): break   # cull line may be past the window; stop 2 min after
        if cur > t1: continue
        if "Dumping stack" in line:
            dumps += 1; in_dump = True; first = False; continue
        if in_dump and line.startswith("[") and "\t" not in line and "Frame count" not in line and "stack" not in line.lower():
            in_dump = False
        if in_dump and not first:
            m = frame_rx.search(line)
            if m: top[m.group(1)] += 1; first = True
        m = re.search(r"Event: (\w+)\.(\w+), Frequency: (\d+)", line)
        if m:
            key = f"{m.group(1)}.{m.group(2)}"
            freq[key] = max(freq.get(key, 0), int(m.group(3)))
        if " error: " in line:
            errs[re.sub(r"\(\w{8}\)", "(id)", line.split("] ", 1)[1].strip())[:90]] += 1

print(f"\n1. Papyrus stack dumps in window: {dumps}")
for s, n in top.most_common(8): print(f"     {n:5d}  {s}")
print("\n2. VM event frequency peaks in window (one line per burst script):")
for k in ("REQ_PersistentSpellRescaling.OnEffectStart", "obodyngscript.OnActorGenerated",
          "SOS_ActorMagicEffect_Script.OnEffectStart", "REQ_MassEffectArmor.OnEffectFinish", "SkyrimFairKeeper.OnUpdate"):
    print(f"     {freq.get(k, 0):5d}  {k}")
print("\n3. cull: " + (f"'switched' logged at {cull_t:%H:%M:%S} = {(cull_t - t0).total_seconds():.0f} s after arrival" if cull_t else "no 'switched' line found after arrival"))
print("\n   top errors in window:")
for s, n in errs.most_common(4): print(f"     {n:5d}  {s}")

# 4: OBody + SOS
def count_between(path, rx_ts, fmt, pred):
    n = 0
    if not os.path.exists(path): return None
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = re.match(rx_ts, line)
            if not m: continue
            ts = dt.datetime.strptime(m.group(1), fmt)
            if t0 - dt.timedelta(seconds=10) <= ts <= t1 and pred(line): n += 1
    return n
ob = count_between(obody, r"^\[(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)", "%Y-%m-%d %H:%M:%S", lambda l: "apply preset to Fair" in l)
sos_n = count_between(sos, r"^\[(\d\d:\d\d:\d\d)", "%H:%M:%S", lambda l: "actor 7B" in l) if os.path.exists(sos) else None
# the SOS log has no date: rebase its times onto the arrival day
if os.path.exists(sos):
    n = 0
    with open(sos, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = re.match(r"^\[(\d\d):(\d\d):(\d\d)", line)
            if not m: continue
            ts = t0.replace(hour=int(m.group(1)), minute=int(m.group(2)), second=int(m.group(3)))
            if t0 - dt.timedelta(seconds=10) <= ts <= t1 and "actor 7B" in line: n += 1
    sos_n = n
print(f"\n4. OBody 'apply preset to Fair ...' calls in window: {ob}")
print(f"   SOS per-actor lines for SkyrimFair.esp actors in window: {sos_n}")
