"""Place the PCHT All Eleonora Clips patch next to PC Head Tracking in every profile.
modlist: mod line directly before (= higher priority than) '+PC Head Tracking - MCM', same enabled state.
plugins.txt / loadorder.txt: plugin directly after 'PC Head Tracking - MCM.esp', same enabled state.
plugingroups.txt: same group as PC Head Tracking - MCM.esp, kept alphabetical.
Backups: <file>.bak-pre-pcht-eleonora-20261018. CRLF/LF preserved. Refuses if MO2 or the game runs."""
import os, shutil, subprocess, sys

ROOT = r"C:\1. AUTHORIA\profiles"
MOD = "houseCARL - Authoria - Patch - PCHT All Eleonora Clips"
ANCHOR_MOD = "PC Head Tracking - MCM"
PLUG = "Authoria - Patch - PCHT All Eleonora Clips.esp"
ANCHOR_PLUG = "PC Head Tracking - MCM.esp"
TAG = ".bak-pre-pcht-eleonora-20261018"

out = subprocess.run(["tasklist"], capture_output=True, text=True).stdout.lower()
if "modorganizer" in out or "skyrimse" in out or "skse64" in out:
    sys.exit("MO2 or the game is running - refusing")

def rd(p):
    b = open(p, "rb").read()
    nl = "\r\n" if b"\r\n" in b else "\n"
    return b.decode("utf-8"), nl

def wr(p, lines, nl, had_trailing):
    if not os.path.exists(p + TAG):
        shutil.copy2(p, p + TAG)
    txt = nl.join(lines) + (nl if had_trailing else "")
    open(p, "wb").write(txt.encode("utf-8"))

for prof in sorted(os.listdir(ROOT)):
    d = os.path.join(ROOT, prof)
    ml = os.path.join(d, "modlist.txt")
    if not os.path.isfile(ml):
        continue
    report = [prof]
    t, nl = rd(ml); trail = t.endswith(nl); L = t.split(nl)
    if trail: L = L[:-1]
    names = [x[1:] for x in L]
    if MOD in names:
        report.append("modlist: already there")
    elif ANCHOR_MOD in names:
        i = names.index(ANCHOR_MOD)
        state = L[i][0]
        L.insert(i, state + MOD)
        wr(ml, L, nl, trail)
        report.append(f"modlist: inserted {state} above {ANCHOR_MOD} (line {i+1})")
    else:
        report.append("modlist: anchor absent, skipped")
        print(" | ".join(report)); continue


    for fn in ("plugins.txt", "loadorder.txt"):
        p = os.path.join(d, fn)
        if not os.path.isfile(p):
            report.append(f"{fn}: missing"); continue
        t, nl2 = rd(p); trail2 = t.endswith(nl2); P = t.split(nl2)
        if trail2: P = P[:-1]
        bare = [x.lstrip("*") for x in P]
        if PLUG in bare:
            report.append(f"{fn}: already there"); continue
        if ANCHOR_PLUG not in bare:
            report.append(f"{fn}: anchor absent, skipped"); continue
        i = bare.index(ANCHOR_PLUG)
        if fn == "plugins.txt":
            anchor_on = P[i].startswith("*")
            line = ("*" if anchor_on else "") + PLUG
        else:
            line = PLUG
        P.insert(i + 1, line)
        wr(p, P, nl2, trail2)
        report.append(f"{fn}: after anchor (line {i+2})")

    pg = os.path.join(d, "plugingroups.txt")
    if os.path.isfile(pg):
        t, nl3 = rd(pg); trail3 = t.endswith(nl3); G = t.split(nl3)
        if trail3: G = G[:-1]
        head = [x for x in G if "|" not in x]
        body = [x for x in G if "|" in x]
        keys = [x.split("|", 1)[0] for x in body]
        if PLUG in keys:
            report.append("groups: already there")
        elif ANCHOR_PLUG in keys:
            grp = body[keys.index(ANCHOR_PLUG)].split("|", 1)[1]
            # insert at its alphabetical spot without re-sorting anyone else
            j = next((k for k, x in enumerate(G) if "|" in x and x.split("|", 1)[0].lower() > PLUG.lower()), len(G))
            G.insert(j, PLUG + "|" + grp)
            wr(pg, G, nl3, trail3)
            report.append(f"groups: '{grp}'")
        else:
            report.append("groups: anchor has no group, skipped")
    print(" | ".join(report))
