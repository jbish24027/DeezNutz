"""Encode the chosen Beeing Female Eleonora takes to .fuz (with lips) and add them to the
Eleonora DBReV pack. Refuses while MO2 or the game runs. Dry run unless --go."""
import json, os, shutil, subprocess, sys, hashlib

MAN = r"C:\1. AUTHORIA\Notes and Files\ELEONORA LINES\7 - BEEING FEMALE\manifest.json"
PACK = r"C:\1. AUTHORIA\mods\Eleonora DBReV\Sound\DBReV\eleonora"
BIN = r"D:\1. MOD STUFF\1. SKYRIM FILES\- 1 TOOLS\- DBReV crap\- DBReV\DBVReV\bin"
FFMPEG, XWMA, FACEFX, BMLFUZ, FONIX = (os.path.join(BIN, n) for n in
    ("ffmpeg.exe", "xWMAEncode.exe", "FaceFXWrapper.exe", "BmlFuzEncode.exe", "FonixData.cdf"))
ENC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "enc")
GO = "--go" in sys.argv


def run(cmd, timeout=120):
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout,
                       creationflags=subprocess.CREATE_NO_WINDOW)
    return p.returncode, p.stdout.decode("utf-8", "replace")


def encode(wav, text):
    os.makedirs(ENC, exist_ok=True)
    base = os.path.join(ENC, hashlib.md5((wav + "|" + text).encode()).hexdigest()[:12])
    fuz, xwm, lip, w16 = base + ".fuz", base + ".xwm", base + ".lip", base + "_16k.wav"
    for p in (fuz, xwm, lip, w16):
        if os.path.exists(p): os.remove(p)
    rc, out = run([XWMA, "/b", "48000", wav, xwm])
    if rc or not os.path.exists(xwm): raise RuntimeError("xWMAEncode failed: " + out)
    run([FFMPEG, "-y", "-i", wav, "-ar", "16000", "-ac", "1", "-sample_fmt", "s16", w16])
    rc2, _ = run([FACEFX, "Skyrim", "USEnglish", FONIX, w16, lip, " ".join(text.replace('"', "").split())], timeout=90)
    lip_ok = rc2 == 0 and os.path.exists(lip) and os.path.getsize(lip) > 0
    rc, out = run([BMLFUZ, fuz, xwm, lip] if lip_ok else [BMLFUZ, "-nolip", fuz, xwm])
    if rc or not os.path.exists(fuz): raise RuntimeError("BmlFuzEncode failed: " + out)
    return fuz, lip_ok


out = subprocess.run(["tasklist"], stdout=subprocess.PIPE).stdout.decode("utf-8", "replace").lower()
if any(x in out for x in ("modorganizer.exe", "skyrimse.exe", "skse64_loader.exe")):
    sys.exit("MO2 or the game is running - stopped")
man = json.load(open(MAN, encoding="utf-8"))
ref_lines, done = [], 0
for m in man:
    dest_dir = os.path.join(PACK, m["plugin"])
    dest = os.path.join(dest_dir, "dbrev_line_%s.fuz" % m["formid"])
    if os.path.exists(dest):
        print("EXISTS, skipped:", dest); continue
    fuz, lip_ok = encode(m["best_file"], m["spoken"])
    print(("GO " if GO else "DRY ") + "%s  lips=%s  %s" % (os.path.basename(dest), lip_ok, m["spoken"]))
    if GO:
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(fuz, dest)
        ref_lines.append("%s | %s | %s" % (m["plugin"], m["formid"], m["shown_text"]))
        done += 1
if GO and ref_lines:
    ref = os.path.join(PACK, "dialogue_ref.txt")
    raw = open(ref, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    with open(ref, "ab") as f:
        if raw and not raw.endswith(nl.encode()): f.write(nl.encode())
        f.write((nl.join(ref_lines) + nl).encode("utf-8"))
print("installed" if GO else "dry run", done, "of", len(man))
