"""Pick reference clips per speaker: decode a size-filtered random sample, measure, Whisper-transcribe, score.
Writes refs/<speaker>/*.wav and refs/candidates.json"""
import os, sys, json, random, struct, subprocess, glob
os.environ.setdefault("HF_HOME", r"D:\OmniVoice\.hf")
import numpy as np, soundfile as sf, librosa, torch
from transformers import pipeline

S = r"C:\Users\User\AppData\Local\Temp\claude\C--1--AUTHORIA\f4941a5e-f3b7-4567-9232-2db3d3adf5f4\scratchpad"
X = S + r"\x"
M = r"C:\1. AUTHORIA\mods"
FF = r"D:\1. MOD STUFF\1. SKYRIM FILES\- 1 TOOLS\- DBReV crap\- DBReV\DBVReV\bin\ffmpeg.exe"
OUT = S + r"\refs"
SRC = {
    "Kaidan": X + r"\kaidan\sound\voice\0kaidan.esp\kaivoice",
    "Gore": M + r"\Gore\sound\voice\gore.esp\hd1gorevoice",
    "Val Serano": X + r"\val\sound\voice\ax valserano.esp\ax_valvoice",
    "Remiel": M + r"\Remiel - Cleaned Audio\sound\voice\hlioremi.esp\hlioremivoice",
    "Xelzaz": X + r"\xelzaz\sound\voice\bpufxelzazfollower.esp\bpufxelzazvoice",
    "Inigo": X + r"\inigo\sound\voice\inigo.esp\inigofollowervoice",
    "Lucien": X + r"\lucien\sound\voice\lucien.esp\jrlucienvoice",
    "Redcap": M + r"\Redcap\sound\voice\fa01redcapfollower.esp\fa01redcapvoice",
    "Serana": X + r"\serana\sound\voice\seranadialogaddon.esp\dlc1seranavoice",
    "Ashe": X + r"\ashe\sound\voice\ashe - fire and blood.esp\mm_ashevoice",
}
SAMPLE = int(sys.argv[1]) if len(sys.argv) > 1 else 45
only = sys.argv[2:]


def to_wav(src, dst):
    ext = os.path.splitext(src)[1].lower()
    tmp = dst + ".xwm"
    if ext == ".fuz":
        b = open(src, "rb").read()
        assert b[:4] == b"FUZE"
        lip = struct.unpack("<I", b[8:12])[0]
        open(tmp, "wb").write(b[12 + lip:])
        inp = tmp
    else:
        inp = src
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", inp, "-ac", "1", dst], check=True)
    if os.path.exists(tmp):
        os.remove(tmp)


def snr(y, sr):
    fr = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0] + 1e-6
    return float(20 * np.log10(np.percentile(fr, 95) / np.percentile(fr, 10)))


asr = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo", torch_dtype=torch.float16, device="cuda:0")
cand_p = OUT + r"\candidates.json"
allc = json.load(open(cand_p, encoding="utf-8")) if os.path.exists(cand_p) else {}
random.seed(11)
for sp, d in SRC.items():
    if only and sp not in only:
        continue
    files = [f for f in glob.glob(d + r"\*") if f.lower().endswith((".fuz", ".xwm", ".wav"))]
    # ~4-10 s of 48 kbps xWMA is about 24-70 KB (lip adds a little)
    sized = [f for f in files if 26000 <= os.path.getsize(f) <= 80000]
    pool = sized if len(sized) >= SAMPLE else files
    random.shuffle(pool)
    od = os.path.join(OUT, sp); os.makedirs(od, exist_ok=True)
    res = []
    for f in pool[:SAMPLE * 2]:
        if len(res) >= SAMPLE:
            break
        w = os.path.join(od, os.path.splitext(os.path.basename(f))[0] + ".wav")
        try:
            to_wav(f, w)
            y, sr = librosa.load(w, sr=None, mono=True)
        except Exception as e:
            print("decode fail", f, e); continue
        dur = len(y) / sr
        if not 3.5 <= dur <= 11:
            os.remove(w); continue
        y16 = librosa.resample(y, orig_sr=sr, target_sr=16000)
        text = asr({"raw": y16, "sampling_rate": 16000}, generate_kwargs={"language": "english"})["text"].strip()
        peak = float(np.max(np.abs(y)))
        res.append({"src": f, "wav": w, "dur": round(dur, 2), "sr": sr, "snr": round(snr(y, sr), 1), "peak": round(peak, 3),
                    "text": text, "words": len(text.split())})
    res.sort(key=lambda r: -r["snr"])
    allc[sp] = {"pool_files": len(files), "sized": len(sized), "cands": res}
    print(sp, len(files), "files;", len(res), "candidates", flush=True)
    for r in res[:8]:
        print("   %.1fs snr %.0f  %s" % (r["dur"], r["snr"], r["text"][:110]), flush=True)
    json.dump(allc, open(cand_p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("DONE")
