"""Eleonora (Luna) lines for Beeing Female's child dialogue, 2026-10-21.
3 OmniVoice takes per line (language English), Whisper/pitch auto-QA picks the best.
Writes wavs + manifest to Notes and Files\\ELEONORA LINES\\7 - BEEING FEMALE (nothing in mods)."""
import json, os, re, sys
os.environ.setdefault("HF_HOME", r"D:\OmniVoice\.hf")
import torch, soundfile as sf
sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\34437703-a598-4855-8cfe-ed31b2a62c51\scratchpad")
from voiceqa import VoiceQA
from omnivoice import OmniVoice

HERE = os.path.dirname(os.path.abspath(__file__))
T = "C:/1. AUTHORIA/_staging/omnivoice-test-20261017/reference"
OUT = r"C:\1. AUTHORIA\Notes and Files\ELEONORA LINES\7 - BEEING FEMALE"
REF = {
    "clip1": (T + "/eleonora-ref1 - And, it sounds to me like you need a.wav",
              "And, it sounds to me like you need a friend. You said you're an outcast, so it seems like a new face is the best thing for you."),
    "clip3": (T + "/eleonora-ref3 - I've seen firsthand how much death a.wav",
              "I've seen firsthand how much death and destruction vampires can cause. I joined the Dawnguard to stop them."),
}
TAKES = [("A", "clip1", 23), ("B", "clip3", 11), ("C", "clip1", 11)]
SPOKEN = {  # shown text -> what she says (typos fixed, statements end in a full stop)
    "Hey you": "Hey, you.",
    "Do you wan to hear something really strange?": "Do you want to hear something really strange?",
    "It's about a child. Nobody like it, everybody hate it!": "It's about a child. Nobody likes it, everybody hates it!",
    "Don't worry, it isn't you": "Don't worry, it isn't you.",
    "Show me what you're carrying": "Show me what you're carrying.",
    "Come with me": "Come with me.",
    "Go to daddy": "Go to Daddy.",
    "Go and find mummy": "Go and find Mummy.",
    "Wait here": "Wait here.",
    "No, just wait": "No, just wait.",
    "But don't run to far away!": "But don't run too far away!",
    "You'd better go home now": "You'd better go home now.",
    "Sorry, I did not mean so": "Sorry, I didn't mean it.",
    "This is our new meeting place": "This is our new meeting place.",
    "Run to our meeting point": "Run to our meeting point.",
}

lines = json.load(open(os.path.join(HERE, "bf_player_lines.json"), encoding="utf-8"))
os.makedirs(os.path.join(OUT, "other takes"), exist_ok=True)
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
qa = VoiceQA()
manifest = []
for n, (kind, formid, shown, *_) in enumerate(lines, 1):
    spoken = SPOKEN.get(shown, shown)
    short = re.sub(r'[\\/:*?"<>|]', "", spoken)[:45].strip().rstrip(".")
    results = []
    for take, ref, seed in TAKES:
        torch.manual_seed(seed)
        wav, rtext = REF[ref]
        audio = model.generate(text=spoken, language="English", ref_audio=wav, ref_text=rtext)
        p = os.path.join(OUT, "other takes", "%02d %s - take %s.wav" % (n, short, take))
        sf.write(p, audio[0], 24000)
        q = qa.check(p, spoken); q.update(take=take, ref=ref, seed=seed); results.append(q)
    good = [r for r in results if "words" not in r["flags"]] or results
    best = sorted(good, key=lambda r: ("rises" in r["flags"], r["end_rise_st"] + r["end_level_st"]))[0]
    final = os.path.join(OUT, "%02d - %s.wav" % (n, short))
    os.replace(best["wav"], final)
    fid, plugin = formid.split(":", 1)
    manifest.append({"number": n, "plugin": plugin, "formid": "00" + fid.upper(), "shown_text": shown, "spoken": spoken,
                     "best_take": best["take"], "best_file": final, "qa": results})
    print("%02d best %s %s | %s" % (n, best["take"], best["flags"], spoken), flush=True)
json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("ALL DONE", len(manifest))
