"""Voices for Authoria - Kaidan Holds Baby (2026-10-22).
Kaidan's 6 responses (cloned from his own recordings) and Luna's 2 prompts (Eleonora, DBReV).
3 OmniVoice takes per line, Whisper/pitch QA picks the best. Writes listenable wavs to
Notes and Files\\KAIDAN HOLDS BABY VOICE; encodes .fuz with lips and installs them only with --go.
Run with D:\\OmniVoice\\.venv\\Scripts\\python.exe."""
import json, os, re, shutil, subprocess, sys, hashlib
os.environ.setdefault("HF_HOME", r"D:\OmniVoice\.hf")
sys.path.insert(0, r"C:\1. AUTHORIA\_tools\follower-banter\voice-refs\scripts")
import torch, soundfile as sf
from voiceqa import VoiceQA
from omnivoice import OmniVoice

GO = "--go" in sys.argv
PLUGIN = "Authoria - Kaidan Holds Baby.esp"
OUT = r"C:\1. AUTHORIA\Notes and Files\KAIDAN HOLDS BABY VOICE"
MOD = r"C:\1. AUTHORIA\mods\houseCARL - Authoria - Kaidan Holds Baby"
KAI_DIR = os.path.join(MOD, "Sound", "Voice", PLUGIN, "kaivoice")
PACK = r"C:\1. AUTHORIA\mods\Eleonora DBReV\Sound\DBReV\eleonora"
BIN = r"D:\1. MOD STUFF\1. SKYRIM FILES\- 1 TOOLS\- DBReV crap\- DBReV\DBVReV\bin"
FFMPEG, XWMA, FACEFX, BMLFUZ, FONIX = (os.path.join(BIN, n) for n in
    ("ffmpeg.exe", "xWMAEncode.exe", "FaceFXWrapper.exe", "BmlFuzEncode.exe", "FonixData.cdf"))
ENC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "enc")

refs = json.load(open(r"C:\1. AUTHORIA\_tools\follower-banter\voice-refs\chosen_refs.json", encoding="utf-8"))
KAI = [(r["wav"], r["text"]) for r in refs["Kaidan"]]
T = "C:/1. AUTHORIA/_staging/omnivoice-test-20261017/reference"
ELE = [(T + "/eleonora-ref1 - And, it sounds to me like you need a.wav",
        "And, it sounds to me like you need a friend. You said you're an outcast, so it seems like a new face is the best thing for you."),
       (T + "/eleonora-ref3 - I've seen firsthand how much death a.wav",
        "I've seen firsthand how much death and destruction vampires can cause. I joined the Dawnguard to stop them.")]

# (who, file key, text). Kaidan voice files: <quest[:10]>_<topic[:15]>_<INFO id>_1.fuz
LINES = [
    ("kaidan", "authkbs_qu_authkbs_givetop_00000806_1", "Come here, little one. I've got you."),
    ("kaidan", "authkbs_qu_authkbs_givetop_00000807_1", "Hand them over, love. Go on, I'll keep them safe."),
    ("kaidan", "authkbs_qu_authkbs_givetop_00000808_1", "Look at that face. Aye, I've got them. Take a breath, lass."),
    ("kaidan", "authkbs_qu_authkbs_taketop_0000080A_1", "Here you go, back to your mama. No trouble at all."),
    ("kaidan", "authkbs_qu_authkbs_taketop_0000080B_1", "Already? They like me better, you know."),
    ("kaidan", "authkbs_qu_authkbs_taketop_0000080C_1", "Careful now. They only just dozed off."),
    ("luna", "dbrev_line_00000805", "Can you hold the baby for a while?"),
    ("luna", "dbrev_line_00000809", "I'll take the baby back now."),
]


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
    rc2, _ = run([FACEFX, "Skyrim", "USEnglish", FONIX, w16, lip, text], timeout=90)
    lip_ok = rc2 == 0 and os.path.exists(lip) and os.path.getsize(lip) > 0
    rc, out = run([BMLFUZ, fuz, xwm, lip] if lip_ok else [BMLFUZ, "-nolip", fuz, xwm])
    if rc or not os.path.exists(fuz): raise RuntimeError("BmlFuzEncode failed: " + out)
    return fuz, lip_ok


os.makedirs(os.path.join(OUT, "other takes"), exist_ok=True)
man_path = os.path.join(OUT, "manifest.json")
if not GO:
    model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
    qa = VoiceQA()
    man = []
    for n, (who, key, text) in enumerate(LINES, 1):
        refset = KAI if who == "kaidan" else ELE
        results = []
        for take, (ri, seed) in enumerate(((0, 11), (1, 23), (2 % len(refset), 7))):
            torch.manual_seed(seed)
            wav, rtext = refset[ri]
            audio = model.generate(text=text, language="English", ref_audio=wav, ref_text=rtext)
            p = os.path.join(OUT, "other takes", "%02d %s %s - take %d.wav" % (n, who, re.sub(r"[^\w ]", "", text)[:40], take + 1))
            sf.write(p, audio[0], 24000)
            q = qa.check(p, text); q.update(ref=ri, seed=seed); results.append(q)
        good = [r for r in results if "words" not in r["flags"]] or results
        best = sorted(good, key=lambda r: ("rises" in r["flags"], r["wer"], r["end_rise_st"]))[0]
        final = os.path.join(OUT, "%02d - %s - %s.wav" % (n, "Kaidan" if who == "kaidan" else "Luna", re.sub(r"[^\w ]", "", text)[:45]))
        shutil.copy2(best["wav"], final)
        man.append({"n": n, "who": who, "key": key, "text": text, "file": final, "qa": {k: best[k] for k in ("heard", "wer", "flags")}})
        print(n, who, best["wer"], best["flags"], text, flush=True)
    json.dump(man, open(man_path, "w", encoding="utf-8"), indent=1)
    print("wavs ready in", OUT)
else:
    out = subprocess.run(["tasklist"], stdout=subprocess.PIPE).stdout.decode("utf-8", "replace").lower()
    if any(x in out for x in ("modorganizer.exe", "skyrimse.exe", "skse64_loader.exe")):
        sys.exit("MO2 or the game is running - stopped")
    man = json.load(open(man_path, encoding="utf-8"))
    refs_out = []
    for m in man:
        fuz, lip_ok = encode(m["file"], m["text"])
        if m["who"] == "kaidan":
            dest = os.path.join(KAI_DIR, m["key"] + ".fuz")
        else:
            dest = os.path.join(PACK, PLUGIN, m["key"] + ".fuz")
            refs_out.append("%s | %s | %s" % (PLUGIN, m["key"][-8:], m["text"]))
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(fuz, dest)
        print("installed", os.path.basename(dest), "lips=%s" % lip_ok)
    ref = os.path.join(PACK, "dialogue_ref.txt")
    raw = open(ref, "rb").read()
    nl = "\r\n" if b"\r\n" in raw else "\n"
    with open(ref, "ab") as f:
        if raw and not raw.endswith(nl.encode()): f.write(nl.encode())
        f.write((nl.join(refs_out) + nl).encode("utf-8"))
