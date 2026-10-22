"""Automatic QA for generated voice lines.
- words: Whisper (openai/whisper-large-v3-turbo) transcript vs the intended text -> word error rate
- ending: pitch slope over the last voiced ~0.5 s (semitones); a statement that rises > RISE_ST reads as a question
Usage as a module: qa = VoiceQA(); qa.check(wav_path, text) -> dict
CLI: python voiceqa.py <wav> "<text>" [<wav> "<text>" ...]"""
import re, sys
from difflib import SequenceMatcher
import numpy as np, librosa, torch
from transformers import pipeline

RISE_ST = 2.0


def norm(s):
    s = s.lower().replace('’', "'")
    s = re.sub(r"[^a-z0-9' ]+", ' ', s)
    return s.split()


def wer(ref, hyp):
    r, h = norm(ref), norm(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            same = r[i - 1] == h[j - 1] or (len(r[i - 1]) > 4 and SequenceMatcher(None, r[i - 1], h[j - 1]).ratio() >= 0.6)
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (not same))
            prev, d[j] = d[j], cur
    return d[len(h)] / max(1, len(r))


class VoiceQA:
    def __init__(self, device='cuda:0'):
        self.asr = pipeline('automatic-speech-recognition', model='openai/whisper-large-v3-turbo',
                            torch_dtype=torch.float16, device=device)

    def ending_slope(self, y, sr):
        f0, voiced, _ = librosa.pyin(y, fmin=80, fmax=500, sr=sr, frame_length=1024)
        idx = np.where(voiced & ~np.isnan(f0))[0]
        if len(idx) < 8:
            return 0.0, 0.0
        hop = 256
        last_t = idx[-1] * hop / sr
        sel = idx[idx * hop / sr >= last_t - 0.5]
        if len(sel) < 5:
            sel = idx[-8:]
        st = 12 * np.log2(f0[sel] / np.median(f0[idx]))
        t = sel * hop / sr
        slope = np.polyfit(t, st, 1)[0] * (t[-1] - t[0])   # semitone change across the window
        tail = idx[idx * hop / sr >= last_t - 0.25]
        level = float(np.median(st[-len(tail):])) if len(tail) else 0.0  # end pitch vs the line's median
        return float(slope), level

    def check(self, wav, text):
        y, sr = librosa.load(wav, sr=16000, mono=True)
        hyp = self.asr({'raw': y, 'sampling_rate': sr}, generate_kwargs={'language': 'english'})['text'].strip()
        w = wer(text, hyp)
        rise, level = self.ending_slope(y, sr)
        is_q = text.rstrip().rstrip('"\'').endswith('?')
        flags = []
        if w > 0.15:
            flags.append('words')
        if not is_q and rise > RISE_ST:
            flags.append('rises')
        return {'wav': wav, 'heard': hyp, 'wer': round(w, 3), 'end_rise_st': round(rise, 2), 'end_level_st': round(level, 2),
                'question': is_q, 'flags': flags, 'ok': not flags}


if __name__ == '__main__':
    qa = VoiceQA()
    a = sys.argv[1:]
    for i in range(0, len(a), 2):
        print(qa.check(a[i], a[i + 1]))
