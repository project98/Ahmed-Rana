"""Build the Urdu reel's voice track and timeline.

usage: python3 build_urdu.py <kokoro-model-dir> <work-dir> [voice] [pitch]
Writes <work-dir>/voice.wav and timeline.js (next to this file). The video's
timing comes from the voice, so lines are never sped up to fit.
"""
import sys, os, json, subprocess, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

MODEL, WORK = sys.argv[1], sys.argv[2]
VOICE = sys.argv[3] if len(sys.argv) > 3 else "mix"  # "mix" = 50/50 hm_omega + hm_psi
PITCH = float(sys.argv[4]) if len(sys.argv) > 4 else 1.12   # 1.12 -> ~150 Hz, like the reference voice
SPEED = 1.15
HERE = os.path.dirname(os.path.abspath(__file__))
os.makedirs(WORK, exist_ok=True)

# scene -> list of (spoken Devanagari, [caption chunks in Roman Urdu])
SCENES = [
 ("hook", [("वीडियो एडिटर की फ़ीस? अब बिल्कुल मुफ़्त!", ["Video editor ki <b>fees?</b>", "Ab bilkul <b>muft.</b>"])]),
 ("pipe", [("एक मुफ़्त AI pipeline. Raw clip अंदर, तैयार reel बाहर।", ["Ek <b>muft AI pipeline</b>", "raw clip andar, <b>tayyar reel bahar.</b>"])]),
 ("s1",   [("Step one: Claude Desktop install करें, और एक project folder बनाएँ।", ["Step 1: <b>Claude Desktop</b> install karein", "aur ek <b>project folder</b> banayein."])]),
 ("s2",   [("Step two: Claude को चार मुफ़्त tools दें।", ["Step 2: Claude ko <b>4 muft tools</b> dein."])]),
 ("tools",[("F F M peg: वीडियो का engine. Cut, join, और final render.", ["<b>FFmpeg:</b> video ka engine", "cut, join aur <b>final render.</b>"]),
           ("Whisper: आवाज़ सुन कर ख़ुद captions लिखता है।", ["<b>Whisper:</b> awaz sun kar", "khud <b>captions likhta hai.</b>"]),
           ("Y T D L P: reels download कर के study करने के लिए।", ["<b>yt-dlp:</b> reels download kar ke", "<b>study karne ke liye.</b>"]),
           ("Hyper Frames: animated text और motion graphics.", ["<b>HyperFrames:</b> animated text", "aur <b>motion graphics.</b>"])]),
 ("power",[("ये चार tools Claude को super powerful बना देंगे।", ["Yeh 4 tools Claude ko", "<b>super powerful</b> bana dein ge."]),
           ("बस इनके links prompt के साथ paste करें, और Claude इन्हें ख़ुद install कर लेगा।", ["Bas in ke <b>links</b> prompt ke saath paste karein,", "aur Claude inhein <b>khud install</b> kar le ga."])]),
 ("s3",   [("Step three है style.", ["Step 3 hai <b>style.</b>"]),
           ("अपने favourite creator की तीन से पाँच reels Claude को दें।", ["Apne favourite creator ki", "<b>3 se 5 reels</b> Claude ko dein."]),
           ("ये उनकी editing style को, font से ले कर sound design तक, पूरा breakdown कर देगा।", ["Yeh un ki <b>editing style</b> ko", "font se le kar <b>sound design</b> tak", "poora <b>breakdown</b> kar de ga."])]),
 ("sheet",[("फिर ये prompt दें, और Claude एक reusable style sheet बना देगा,", ["Phir yeh prompt dein, aur Claude", "ek <b>reusable style sheet</b> bana de ga,"]),
           ("जो हर बार perfection के साथ काम करती है।", ["jo har baar <b>perfection</b> ke saath kaam karti hai."])]),
 ("s4",   [("Step four: footage डालें, एक prompt दें, और reel तैयार।", ["Step 4: footage daalein,", "ek prompt — <b>reel tayyar.</b>"])]),
 ("cta",  [("पूरा prompt चाहिए? Comment करें BUILD. और subscribe करें, Build Smarter with AI.", ["Poora prompt chahiye? Comment karein <b>BUILD</b>", "aur subscribe karein <b>Build Smarter with AI.</b>"])]),
]
MIN_SCENE = {"s2": 3.6, "s4": 4.2, "hook": 3.2}
LEAD, GAP, TAIL = 0.25, 0.3, 0.45

k = Kokoro(f"{MODEL}/kokoro.onnx", f"{MODEL}/voices.bin")
STYLE = (0.5 * k.get_voice_style("hm_omega") + 0.5 * k.get_voice_style("hm_psi")) if VOICE == "mix" else VOICE
import re
def phon(text):
    """Urdu/Hindi in Devanagari + English words in Latin: phonemize each part in its own language,
    so English tech words (install, prompt, Claude) are pronounced correctly."""
    parts = re.findall(r"[A-Za-z][A-Za-z\- ]*[A-Za-z]|[A-Za-z]|[^A-Za-z]+", text)
    out = (k.tokenizer.phonemize(p, "en-gb") if re.match(r"[A-Za-z]", p) else k.tokenizer.phonemize(p, "hi") for p in parts)
    return " ".join(x.strip() for x in out if x.strip())
SR = 24000
clips, scenes, caps, lines = [], [], [], []
t = 0.0
for name, items in SCENES:
    start = t; cur = t + LEAD
    for i, (text, chunks) in enumerate(items):
        a, sr = k.create(phon(text), voice=STYLE, speed=SPEED, is_phonemes=True)
        raw = f"{WORK}/l{len(clips)}.wav"; sf.write(raw, a, sr)
        out = f"{WORK}/p{len(clips)}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"rubberband=pitch={PITCH}", out], check=True)
        a, _ = sf.read(out, dtype="float32")
        d = len(a) / SR
        clips.append((cur, a)); lines.append([round(cur, 3), round(cur + d, 3)])
        w = [len(c) for c in chunks]; c0 = cur
        for c, n in zip(chunks, w):
            c1 = c0 + d * n / sum(w); caps.append([round(c0, 3), round(c1, 3), c]); c0 = c1
        cur += d + GAP
    end = max(cur - GAP + TAIL, start + MIN_SCENE.get(name, 0))
    scenes.append({"name": name, "a": round(start, 3), "b": round(end, 3),
                   "lines": lines[-len(items):]})
    t = end
TOTAL = round(t + 0.3, 2)
for c in caps: c[1] = min(c[1] + 0.25, TOTAL)  # let captions linger a bit
track = np.zeros(int(TOTAL * SR) + 1, dtype=np.float32)
for s, a in clips:
    i = int(s * SR); track[i:i + len(a)] += a[: len(track) - i]
track /= np.abs(track).max() / 0.9
sf.write(f"{WORK}/voice.wav", track, SR)
with open(f"{HERE}/timeline.js", "w") as f:
    f.write("window.TL=" + json.dumps({"total": TOTAL, "scenes": scenes, "caps": caps}, ensure_ascii=False) + ";\n")
for s in scenes: print(f'{s["name"]:6} {s["a"]:6.2f} -> {s["b"]:6.2f}')
print("TOTAL", TOTAL)
