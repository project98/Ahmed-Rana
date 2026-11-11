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
 (13.1, 19.0, "दूसरा क़दम: क्लॉड से कहें, ये चार मुफ़्त टूल्स ख़ुद इंस्टॉल करे।"),
 (19.1, 22.75, "एफ एफ एम्पेग: वीडियो का इंजन। कट, जोड़, और फ़ाइनल रेंडर।"),
 (22.85, 26.5, "विस्पर: आपकी आवाज़ सुन कर ख़ुद कैप्शन लिखता है।"),
 (26.6, 30.25, "वाई टी डी एल पी: रेफ़रेंस रील्स डाउनलोड करता है।"),
 (30.35, 34.0, "हाइपर फ्रेम्स: एनिमेटेड टेक्स्ट और मोशन ग्राफ़िक्स बनाता है।"),
 (34.1, 39.6, "तीसरा क़दम: अपनी पसंदीदा रील्स दें। क्लॉड आपका पूरा अंदाज़ सीख लेगा।"),
 (39.7, 44.4, "चौथा क़दम: फ़ुटेज डालें, एक प्रॉम्प्ट दें, और रील तैयार।"),
 (44.5, 49.0, "पूरा प्रॉम्प्ट चाहिए? कमेंट करें बिल्ड। और फ़ॉलो करें, बिल्ड विद अहमद।"),
]
track = np.zeros(int(49.0 * SR), dtype=np.float32)
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
