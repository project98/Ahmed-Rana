import sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
d = sys.argv[1]; voice = sys.argv[2]; out = sys.argv[3]
k = Kokoro(f"{d}/kokoro.onnx", f"{d}/voices.bin")
SR = 24000
# (start, end, text) — matches scene timing in reel.html
LINES = [
 (0.15, 3.6,  "वीडियो एडिटर की फ़ीस? अब बिल्कुल मुफ़्त।"),
 (3.7,  7.4,  "एक मुफ़्त ए आई पाइपलाइन। रॉ क्लिप अंदर, तैयार रील बाहर।"),
 (7.5,  13.0, "पहला क़दम: क्लॉड डेस्कटॉप इंस्टॉल करें, और एक प्रोजेक्ट फ़ोल्डर बनाएँ।"),
 (13.1, 19.0, "दूसरा क़दम: क्लॉड से कहें, मुफ़्त टूल्स ख़ुद इंस्टॉल करे। एफ एफ एम्पेग, विस्पर, और हाइपर फ्रेम्स।"),
 (19.1, 24.6, "तीसरा क़दम: अपनी पसंदीदा रील्स दें। क्लॉड आपका पूरा अंदाज़ सीख लेगा।"),
 (24.7, 29.4, "चौथा क़दम: फ़ुटेज डालें, एक प्रॉम्प्ट दें, और रील तैयार।"),
 (29.5, 34.0, "पूरा प्रॉम्प्ट चाहिए? कमेंट करें बिल्ड। और फ़ॉलो करें, बिल्ड विद अहमद।"),
]
track = np.zeros(int(34.0 * SR), dtype=np.float32)
for a, b, text in LINES:
    slot = (b - a) - 0.15
    speed = 1.1
    for _ in range(6):
        audio, sr = k.create(text, voice=voice, speed=speed, lang="hi")
        if len(audio) / sr <= slot: break
        speed = min(1.6, speed * (len(audio) / sr) / slot * 1.02)
    print(f"{a:5.1f}s  len={len(audio)/sr:.2f}s slot={slot:.2f}s speed={speed:.2f}")
    s = int(a * SR); audio = audio[: len(track) - s]
    track[s:s + len(audio)] += audio
track /= max(1e-6, np.abs(track).max()) / 0.9
sf.write(out, track, SR)
