"""Full banter voice run. Resumable: skips lines already done. Stops cleanly when D:\\BANTER VOICE\\STOP exists.
Output: D:\\BANTER VOICE\\<Speaker>\\<TALKID>_<nn>.wav  (nn = line number inside the talk, all speakers counted)
Log:    D:\\BANTER VOICE\\<Speaker>\\done.jsonl  (one row per line: id, text, spoken, ref, seed, speed, QA)
Usage:  run_full.py [--limit N] [Speaker ...]"""
import os, sys, json, re, glob, time
os.environ.setdefault("HF_HOME", r"D:\OmniVoice\.hf")
S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)

OUT = r"D:\BANTER VOICE"
STOP = os.path.join(OUT, "STOP")
FILES = glob.glob(r"C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER SCRIPTS\*.txt") + glob.glob(r"C:\1. AUTHORIA\Notes and Files\FOLLOWER BANTER - SCRIPT*.txt")
NAMES = {"KAIDAN": "Kaidan", "LUNA": "Luna", "GORE": "Gore", "VAL": "Val Serano", "LUCIEN": "Lucien", "REMI": "Remiel",
         "INIGO": "Inigo", "XELZAZ": "Xelzaz", "REDCAP": "Redcap", "SERANA": "Serana", "ASHE": "Ashe"}
ORDER = ["Kaidan", "Luna", "Gore", "Val Serano", "Lucien", "Remiel", "Inigo", "Xelzaz", "Redcap", "Serana", "Ashe"]
SEED_STEP = [0, 1, 2, 3]
HDR = re.compile(r"^([A-Z]{1,4}\d{1,4}[a-z]?)\.\s+(.+)$")
SPK = re.compile(r"^([A-Z][A-Z ]{1,12}):\s+(.+)$")
BOW = re.compile(r"\b(the|a|my|his|her|your|their|our|that|this|short|long|hunting|elven|glass|ebony|daedric|dwarven|orcish|steel|iron|imperial|nord|war|good|old|new|own)\s+(bow)(s?)\b", re.I)


def parse():
    rows = []
    for f in sorted(FILES):
        cur, n = None, 0
        for ln in open(f, encoding="utf-8", errors="replace"):
            ln = ln.rstrip()
            m = HDR.match(ln)
            if m:
                cur, n = m.group(1), 0
                continue
            m = SPK.match(ln)
            if m and cur:
                n += 1
                rows.append({"id": "%s_%02d" % (cur, n), "speaker": NAMES[m.group(1).strip()], "text": m.group(2).strip(), "file": os.path.basename(f)})
    return rows


def spoken(t):
    t = re.sub(r"\*\s*sighs?\s*\*", " [sigh] ", t, flags=re.I)
    t = re.sub(r"\*[^*]+\*|\([^)]*\)", " ", t)
    t = t.replace("...", ", ").replace('"', "").replace("“", "").replace("”", "")
    t = re.sub(r"\b([A-Z]{3,})\b", lambda m: m.group(1).capitalize(), t)
    t = BOW.sub(lambda m: "%s [B OW1]%s" % (m.group(1), m.group(3)), t)   # the weapon, not "bough"
    t = re.sub(r"^[\s,]*(\[sigh\])[\s,]*", r"\1 ", t)
    t = re.sub(r"\s+", " ", t).strip(" ,")
    return t


def plain(t):   # what Whisper should hear
    return re.sub(r"\s+", " ", t.replace("[sigh]", "").replace("[B OW1]", "bow")).strip(" ,")


def main():
    a = sys.argv[1:]
    limit = None
    if "--limit" in a:
        i = a.index("--limit"); limit = int(a[i + 1]); del a[i:i + 2]
    only = a or ORDER
    import torch, soundfile as sf
    from voiceqa import VoiceQA
    from omnivoice import OmniVoice
    REFS = json.load(open(os.path.join(S, "chosen_refs.json"), encoding="utf-8"))
    SET = REFS["_settings"]
    rows = parse()
    model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16)
    qa = VoiceQA()
    t0, made = time.time(), 0
    for sp in [s for s in ORDER if s in only]:
        od = os.path.join(OUT, sp); os.makedirs(od, exist_ok=True)
        logp = os.path.join(od, "done.jsonl")
        done = set()
        if os.path.exists(logp):
            for ln in open(logp, encoding="utf-8"):
                try:
                    done.add(json.loads(ln)["id"])
                except Exception:
                    pass
        st = SET[sp]
        prefs = st["prefer_refs"]
        todo = [r for r in rows if r["speaker"] == sp and r["id"] not in done]
        print("==", sp, len(todo), "to do", flush=True)
        with open(logp, "a", encoding="utf-8") as log:
            for r in todo:
                if os.path.exists(STOP):
                    print("STOP file found - stopping cleanly", flush=True); return
                if limit is not None and made >= limit:
                    print("limit reached", flush=True); return
                say = spoken(r["text"])
                rec = dict(r, spoken=say)
                if not plain(say):
                    rec.update(skipped="no words after removing stage directions")
                    log.write(json.dumps(rec, ensure_ascii=False) + "\n"); log.flush(); continue
                dst = os.path.join(od, r["id"] + ".wav")
                best = None
                for k, step in enumerate(SEED_STEP):
                    ri = prefs[k % len(prefs)]
                    seed = st["seed"] + step * 100
                    ref = REFS[sp][ri - 1]
                    torch.manual_seed(seed)
                    kw = {"speed": st["speed"]} if st["speed"] != 1.0 else {}
                    try:
                        audio = model.generate(text=say, language="English", ref_audio=ref["wav"], ref_text=ref["text"], **kw)
                    except Exception as e:
                        print("generate error", r["id"], e, flush=True); continue
                    tmp = dst[:-4] + ".try%d.wav" % k
                    sf.write(tmp, audio[0], 24000)
                    q = qa.check(tmp, plain(say)); q.update(ref=ri, seed=seed, speed=st["speed"], tmp=tmp)
                    if best is None or (len(q["flags"]), q["wer"]) < (len(best["flags"]), best["wer"]):
                        if best:
                            os.remove(best["tmp"])
                        best = q
                    else:
                        os.remove(tmp)
                    if q["ok"]:
                        break
                if best is None:
                    rec.update(skipped="generate failed")
                else:
                    os.replace(best["tmp"], dst)
                    for x in ("tmp", "wav"):
                        best.pop(x, None)
                    rec.update(best)
                    made += 1
                log.write(json.dumps(rec, ensure_ascii=False) + "\n"); log.flush()
                if made % 200 == 0 and made:
                    el = time.time() - t0
                    print("%s %d made, %.2f s/line, %s" % (sp, made, el / made, time.strftime("%H:%M")), flush=True)
    print("ALL DONE", made, "lines in %.1f h" % ((time.time() - t0) / 3600), flush=True)


if __name__ == "__main__":
    main()
