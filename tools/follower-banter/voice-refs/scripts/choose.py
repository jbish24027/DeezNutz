import json, os, shutil
S = os.path.dirname(os.path.abspath(__file__))
R = r"C:\1. AUTHORIA\_tools\follower-banter\voice-refs"
c = json.load(open(S + r"\refs\candidates.json", encoding="utf-8"))
PICK = {"Kaidan": [15, 12, 1], "Gore": [11, 5, 4], "Val Serano": [0, 10, 12], "Remiel": [11, 9, 14],
        "Xelzaz": [4, 6, 1], "Inigo": [2, 4, 9], "Lucien": [4, 10, 16], "Redcap": [13, 36, 12],
        "Serana": [15, 2, 21], "Ashe": [14, 9, 7]}
FIX = {"Red Cap": "Redcap"}
out = {}
for sp, idx in PICK.items():
    od = os.path.join(R, sp); os.makedirs(od, exist_ok=True)
    out[sp] = []
    for n, i in enumerate(idx, 1):
        r = c[sp]["cands"][i]
        t = r["text"]
        for a, b in FIX.items():
            t = t.replace(a, b)
        dst = os.path.join(od, "ref%d.wav" % n)
        shutil.copyfile(r["wav"], dst)
        out[sp].append({"wav": dst, "text": t, "dur": r["dur"], "source_file": r["src"], "transcript_from": "Whisper large-v3-turbo"})
L = "C:/1. AUTHORIA/_staging/omnivoice-test-20261017/reference"
out["Luna"] = [
    {"wav": L + "/eleonora-ref1 - And, it sounds to me like you need a.wav", "text": "And, it sounds to me like you need a friend. You said you're an outcast, so it seems like a new face is the best thing for you.", "source_file": "Eleonora setup 10-17"},
    {"wav": L + "/eleonora-ref3 - I've seen firsthand how much death a.wav", "text": "I've seen firsthand how much death and destruction vampires can cause. I joined the Dawnguard to stop them.", "source_file": "Eleonora setup 10-17"}]
json.dump(out, open(S + r"\chosen_refs.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
json.dump(out, open(os.path.join(R, "chosen_refs.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
for sp, v in out.items():
    print(sp, [x["text"][:50] for x in v])
