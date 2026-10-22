"""Redo one Beeing Female Eleonora line with more seeds until it ends flat. Usage: redo_line.py <number>"""
import json, os, sys
os.environ.setdefault("HF_HOME", r"D:\OmniVoice\.hf")
import torch, soundfile as sf
sys.path.insert(0, r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\34437703-a598-4855-8cfe-ed31b2a62c51\scratchpad")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from voiceqa import VoiceQA
from omnivoice import OmniVoice
from make_bf_voice_refs import REF, OUT

n = int(sys.argv[1])
man_p = os.path.join(OUT, "manifest.json")
man = json.load(open(man_p, encoding="utf-8"))
m = next(x for x in man if x["number"] == n)
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
qa = VoiceQA()
best = None
for i, (ref, seed) in enumerate([(r, s) for s in (5, 7, 31, 42, 57, 77) for r in ("clip3", "clip1")]):
    torch.manual_seed(seed)
    wav, rtext = REF[ref]
    audio = model.generate(text=m["spoken"], language="English", ref_audio=wav, ref_text=rtext)
    p = os.path.join(OUT, "other takes", "%02d redo %s %d.wav" % (n, ref, seed))
    sf.write(p, audio[0], 24000)
    q = qa.check(p, m["spoken"]); q.update(ref=ref, seed=seed)
    print(ref, seed, q["flags"], q["end_rise_st"], flush=True)
    if not q["flags"]:
        best = q; break
if best:
    os.replace(best["wav"], m["best_file"])
    m["best_take"] = "redo %s %d" % (best["ref"], best["seed"]); m["qa"].append(best)
    json.dump(man, open(man_p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("REPLACED with", m["best_take"])
else:
    print("NO CLEAN TAKE")
