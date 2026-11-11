"""Build the Urdu reel's voice track + timeline from Ahmed's own recording.

usage: python3 build_own_voice.py <recording.m4a> <work-dir>
Cleans the recording, keeps only the good takes listed in SCENES (times in the
raw recording), tightens pauses, and writes <work-dir>/voice.wav and timeline.js
(next to this file), which reel-urdu.html reads.
"""
import sys, os, json, subprocess, numpy as np, soundfile as sf

REC, WORK = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(WORK, exist_ok=True)
SR = 48000

# scene -> lines; each line = (pieces [(start,end) in raw recording], caption chunks, split)
# split: optional list of fractions to cut one recorded take into several "lines"
SCENES = [
 ("hook", [([(0.10, 2.50)], ["Video editor ki <b>fees?</b>", "Ab bilkul <b>muft.</b>"])]),
 ("pipe", [([(2.52, 6.15)], ["Ek <b>muft AI pipeline</b>", "raw clip andar, <b>tayyar reel bahar.</b>"])]),
 ("s1",   [([(7.15, 8.10), (8.45, 12.90)], ["Step 1: <b>Claude Desktop</b> install karein", "aur ek <b>project folder</b> banayein."])]),
 ("s2",   [([(13.02, 15.95)], ["Claude ko <b>4 muft tools</b> dein."])]),
 ("tools",[([(16.53, 21.70)], ["<b>FFmpeg:</b> video ka engine", "cut, join aur <b>final render.</b>"]),
           ([(22.42, 25.40)], ["<b>Whisper:</b> awaz sun kar", "khud <b>captions likhta hai.</b>"]),
           ([(25.72, 29.95)], ["<b>yt-dlp:</b> reels download kar ke", "<b>study karne ke liye.</b>"]),
           ([(30.66, 35.20)], ["<b>HyperFrames:</b> animated text", "aur <b>motion graphics.</b>"])]),
 ("power",[([(35.68, 38.50)], ["Yeh 4 tools Claude ko", "<b>super powerful</b> bana dein ge."]),
           ([(41.56, 46.70)], ["Bas in ke <b>links</b> prompt ke saath paste karein,", "aur Claude inhein <b>khud install</b> kar le ga."])]),
 ("s3",   [([(47.27, 48.85)], ["Step 3 hai <b>style.</b>"]),
           ([(52.90, 56.20)], ["Apne favourite creator ki", "<b>3 se 5 reels</b> Claude ko dein."]),
           ([(56.50, 62.15)], ["Yeh un ki <b>editing style</b> ko", "font se le kar <b>sound design</b> tak", "poora <b>breakdown</b> kar de ga."])]),
 ("sheet",[([(62.95, 69.35)], ["Phir yeh prompt dein, aur Claude", "ek <b>reusable style sheet</b> bana de ga,", "jo har baar <b>perfection</b> ke saath kaam karti hai."], [0.66])]),
 ("s4",   [([(69.62, 73.60)], ["Step 4: footage daalein,", "ek prompt — <b>reel tayyar.</b>"])]),
 ("cta",  [([(74.22, 79.50)], ["Poora prompt chahiye? Comment kijiye <b>BUILD</b>", "aur subscribe kijiye <b>Build with Ahmed.</b>"])]),
]
MIN_SCENE = {"s2": 3.6, "s4": 4.2, "hook": 3.2}
LEAD, GAP, TAIL, PIECE_GAP = 0.2, 0.3, 0.45, 0.25

clean = f"{WORK}/clean.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", REC, "-ac", "1", "-ar", str(SR), "-af",
                "highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=80,volume=2",
                clean], check=True)
raw, _ = sf.read(clean, dtype="float32")

def cut(s, e):
    a = raw[int(s * SR):int(e * SR)].copy(); f = int(0.03 * SR)
    a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)  # click-free edges
    return a

out, scenes, caps = [], [], []
t = 0.0
for name, items in SCENES:
    start = t; cur = t + LEAD; spans = []
    for item in items:
        pieces, chunks = item[0], item[1]; splits = item[2] if len(item) > 2 else []
        a = np.concatenate([np.concatenate([cut(s, e), np.zeros(int(PIECE_GAP * SR), np.float32)]) for s, e in pieces])[:-int(PIECE_GAP * SR)]
        d = len(a) / SR; out.append((cur, a))
        bounds = [0] + splits + [1]
        spans += [[round(cur + d * bounds[i], 3), round(cur + d * bounds[i + 1], 3)] for i in range(len(bounds) - 1)]
        w = [len(c) for c in chunks]; c0 = cur
        for c, n in zip(chunks, w):
            c1 = c0 + d * n / sum(w); caps.append([round(c0, 3), round(c1, 3), c]); c0 = c1
        cur += d + GAP
    end = max(cur - GAP + TAIL, start + MIN_SCENE.get(name, 0))
    scenes.append({"name": name, "a": round(start, 3), "b": round(end, 3), "lines": spans})
    t = end
TOTAL = round(t + 0.3, 2)
for c in caps: c[1] = min(c[1] + 0.25, TOTAL)
track = np.zeros(int(TOTAL * SR) + 1, np.float32)
for s, a in out:
    i = int(s * SR); track[i:i + len(a)] += a[:len(track) - i]
track /= np.abs(track).max() / 0.9
sf.write(f"{WORK}/voice.wav", track, SR)
with open(f"{HERE}/timeline.js", "w") as f:
    f.write("window.TL=" + json.dumps({"total": TOTAL, "scenes": scenes, "caps": caps}, ensure_ascii=False) + ";\n")
for s in scenes: print(f'{s["name"]:6} {s["a"]:6.2f} -> {s["b"]:6.2f}')
print("TOTAL", TOTAL)
