"""Generate banter voice tests. Reads test_lines.json + chosen_refs.json, writes Notes and Files\BANTER VOICE TESTS\<Speaker>\.
3 takes per line (one per reference clip, different seeds). A take that fails auto-QA is retried with other seeds/clips.
Usage: gen_tests.py [Speaker ...]"""
import os, sys, json, re, shutil
os.environ.setdefault("HF_HOME", r"D:\OmniVoice\.hf")
S = os.path.dirname(os.path.abspath(__file__))
import torch, soundfile as sf
sys.path.insert(0, S)
from voiceqa import VoiceQA
from omnivoice import OmniVoice

DESK = r"C:\1. AUTHORIA\Notes and Files\BANTER VOICE TESTS"
LINES = json.load(open(os.path.join(S, "test_lines.json"), encoding="utf-8"))
REFS = json.load(open(os.path.join(S, "chosen_refs.json"), encoding="utf-8"))
only = sys.argv[1:]
SEEDS = [7, 31, 42, 57, 77, 101, 123, 202]


def spoken(t):
    t = t.lstrip(". ").replace("...", ", ").replace('"', "")
    return re.sub(r"\b([A-Z]{3,})\b", lambda m: m.group(1).capitalize(), t)


def fname(t):
    t = re.sub(r'[\\/:*?"<>|]', "", t).strip(". ")
    return t[:60].rstrip(" ,.")


def score(q):
    return (len(q["flags"]), q["wer"] + max(0, q["end_rise_st"]) * 0.05)


model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
qa = VoiceQA()
for sp, lines in LINES.items():
    if only and sp not in only:
        continue
    refs = REFS[sp]
    od = os.path.join(DESK, sp); os.makedirs(od, exist_ok=True)
    tmp = os.path.join(od, "_tmp"); os.makedirs(tmp, exist_ok=True)
    for i, r in enumerate(refs, 1):
        dst = os.path.join(od, "0 - real voice %d - %s.wav" % (i, fname(r["text"])[:40]))
        if not os.path.exists(dst):
            shutil.copyfile(r["wav"], dst)
        r["desktop_file"] = os.path.basename(dst)
    man = {"speaker": sp, "references": refs, "lines": []}
    for n, (mood, text) in enumerate(lines, 1):
        say = spoken(text)
        entry = {"number": n, "mood": mood, "script_text": text, "spoken_text": say, "takes": []}
        for k in range(3):
            best = None
            tries = [(k % len(refs), SEEDS[k])] + [((k + j) % len(refs), SEEDS[(k * 3 + j + 3) % len(SEEDS)]) for j in range(1, 5)]
            for ri, seed in tries:
                torch.manual_seed(seed)
                ref = refs[ri]
                audio = model.generate(text=say, language="English", ref_audio=ref["wav"], ref_text=ref["text"])
                p = os.path.join(tmp, "%02d_%d_%d_%d.wav" % (n, k, ri, seed))
                sf.write(p, audio[0], 24000)
                q = qa.check(p, say); q.update(ref=ri + 1, seed=seed)
                if best is None or score(q) < score(best):
                    best = q
                if q["ok"]:
                    break
            dst = os.path.join(od, "%02d - %s - take %d.wav" % (n, fname(text), k + 1))
            os.replace(best["wav"], dst)
            best["file"] = os.path.basename(dst); best.pop("wav", None)
            entry["takes"].append(best)
            print(sp, n, k + 1, "ref", best["ref"], "seed", best["seed"], best["flags"] or "ok", "rise", best["end_rise_st"], "|", best["heard"][:70], flush=True)
        man["lines"].append(entry)
    shutil.rmtree(tmp, ignore_errors=True)
    json.dump(man, open(os.path.join(od, "manifest.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("DONE")
