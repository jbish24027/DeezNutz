"""Retest batch 22 Oct: Val slower, Gore new clips/seeds, Kaidan clip 3 slowed. Writes Notes and Files\BANTER VOICE TESTS\RETEST\<Speaker>\."""
import os, sys, json, re, shutil
os.environ.setdefault("HF_HOME", r"D:\OmniVoice\.hf")
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import torch, soundfile as sf
from voiceqa import VoiceQA
from omnivoice import OmniVoice

DESK = r"C:\1. AUTHORIA\Notes and Files\BANTER VOICE TESTS\RETEST"
LINES = json.load(open(os.path.join(S, "test_lines.json"), encoding="utf-8"))
REFS = json.load(open(os.path.join(S, "chosen_refs.json"), encoding="utf-8"))
SCRATCH = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\f4941a5e-f3b7-4567-9232-2db3d3adf5f4\scratchpad"
cands = json.load(open(SCRATCH + r"\refs\candidates.json", encoding="utf-8"))

# two extra Gore clips (candidates 13 and 6), saved beside the others as ref4/ref5
for n, i in ((4, 13), (5, 6)):
    c = cands["Gore"]["cands"][i]
    dst = r"C:\1. AUTHORIA\_tools\follower-banter\voice-refs\Gore\ref%d.wav" % n
    shutil.copyfile(c["wav"], dst)
    if len(REFS["Gore"]) < n:
        REFS["Gore"].append({"wav": dst, "text": c["text"], "dur": c["dur"], "source_file": c["src"], "transcript_from": "Whisper large-v3-turbo"})
json.dump(REFS, open(os.path.join(S, "chosen_refs.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# (speaker, label, ref number, seed, speed)
JOBS = {
    "Val Serano": [("clip 1 speed 0.92", 1, 7, 0.92), ("clip 1 speed 0.85", 1, 7, 0.85)],
    "Gore": [("clip 3 seed 42", 3, 42, 1.0), ("clip 3 seed 77", 3, 77, 1.0), ("new clip 4", 4, 7, 1.0), ("new clip 5", 5, 7, 1.0)],
    "Kaidan": [("clip 3 speed 0.88", 3, 42, 0.88), ("clip 3 speed 0.82", 3, 42, 0.82)],
}


def spoken(t):
    t = t.lstrip(". ").replace("...", ", ").replace('"', "")
    return re.sub(r"\b([A-Z]{3,})\b", lambda m: m.group(1).capitalize(), t)


def fname(t):
    return re.sub(r'[\\/:*?"<>|]', "", t).strip(". ")[:60].rstrip(" ,.")


model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
qa = VoiceQA()
for sp, jobs in JOBS.items():
    od = os.path.join(DESK, sp); os.makedirs(od, exist_ok=True)
    if sp == "Gore":
        for n in (4, 5):
            shutil.copyfile(REFS["Gore"][n - 1]["wav"], os.path.join(od, "0 - real voice %d (new) - %s.wav" % (n, fname(REFS["Gore"][n - 1]["text"])[:40])))
    man = []
    for n, (mood, text) in enumerate(LINES[sp], 1):
        say = spoken(text)
        for label, ri, seed, speed in jobs:
            ref = REFS[sp][ri - 1]
            best = None
            for s in (seed, seed + 100, seed + 200):
                torch.manual_seed(s)
                kw = {"speed": speed} if speed != 1.0 else {}
                audio = model.generate(text=say, language="English", ref_audio=ref["wav"], ref_text=ref["text"], **kw)
                p = os.path.join(od, "%02d - %s - %s.wav" % (n, fname(text), label))
                sf.write(p, audio[0], 24000)
                q = qa.check(p, say); q.update(label=label, ref=ri, seed=s, speed=speed, line=n, file=os.path.basename(p))
                if best is None or len(q["flags"]) < len(best["flags"]):
                    best = q
                if "rises" not in q["flags"]:
                    break
            q.pop("wav", None); man.append(q)
            print(sp, n, label, "seed", q["seed"], q["flags"] or "ok", "rise", q["end_rise_st"], flush=True)
    json.dump(man, open(os.path.join(od, "manifest.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("DONE")
