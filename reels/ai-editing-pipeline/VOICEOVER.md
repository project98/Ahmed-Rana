# Build with Ahmed — "₹0 AI Video Editor" reel

**Video:** `build-with-ahmed-ai-editing-reel.mp4` (1080×1920, 34s, 30fps, silent track)

## Voiceover script (Hinglish), timed to the on-screen captions

| Time | Line |
|---|---|
| 0.0–3.6 | Video editor ki fees? Ab zero. Seriously. |
| 3.6–7.4 | Ek free AI pipeline — raw clip andar, reel bahar. |
| 7.4–13.0 | Step 1: Claude Desktop install karo, aur ek project folder banao — raw, style, aur output. |
| 13.0–19.0 | Step 2: Claude ko bolo free tools khud install kare — FFmpeg, Whisper, yt-dlp aur HyperFrames. |
| 19.0–24.6 | Step 3: apni favourite reels style folder mein daalo — Claude fonts, cuts, captions, sab seekh lega. |
| 24.6–29.4 | Step 4: footage drop karo, ek prompt do — aur reel ready. |
| 29.4–34.0 | Full prompt chahiye? Comment "BUILD" — aur follow karo Build with Ahmed. |

## Recording the AI voice
- **ElevenLabs:** pick a Hindi/Hinglish male voice (or clone your own). Settings: Stability ~35%, Similarity ~75%, Style ~30%, speed slightly fast (1.05–1.1×).
- Generate each row separately so you can line it up with the caption times, or do one take and trim it to 34s.
- Export as `voice.mp3`.

## Add the voice (and optional music)
```bash
# voice only
ffmpeg -i build-with-ahmed-ai-editing-reel.mp4 -i voice.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -shortest final.mp4

# voice + background music at 12% volume
ffmpeg -i build-with-ahmed-ai-editing-reel.mp4 -i voice.mp3 -i music.mp3 \
  -filter_complex "[2:a]volume=0.12[m];[1:a][m]amix=inputs=2:duration=first[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac final.mp4
```

## Editing the video
To change text or timing, edit `reel.html`: `CAPS` holds the captions and `SC` the scene timings. Then re-render:
```bash
mkdir frames && node render.js reel.html frames 30 34
ffmpeg -framerate 30 -i frames/%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 18 out.mp4
```

## Caption to post with it
> ₹0 mein apna AI video editor 🤖🎬 Claude + free tools = raw footage se ready reel, ek prompt mein.
> Comment **BUILD** aur main full prompt DM karunga.
> #BuildWithAhmed #ClaudeAI #AIVideoEditing #AITools #ContentCreation #FFmpeg #Whisper

## Free AI voice (already added)
`build-with-ahmed-ai-editing-reel-voiced.mp4` is the ready-to-post version. Its voice is Kokoro (free, open-source, Apache-2.0), using the Hindi male voice `hm_omega`. The voice track alone is in `voice.mp3`.
To regenerate it with a different voice (`hm_psi` male, `hf_alpha`/`hf_beta` female), download `kokoro-v1.0.onnx` and `voices-v1.0.bin` from github.com/thewh1teagle/kokoro-onnx releases into a folder, then:
```bash
pip install kokoro-onnx soundfile
python3 vo.py <model-folder> hm_psi voice.wav
```

## Urdu version
`build-with-ahmed-ai-editing-reel-urdu.mp4` has Urdu wording (muft, qadam, tayyar, pasandeeda, andaaz), Roman Urdu captions, "Rs 0" instead of ₹0, and the Kokoro male voice `hm_psi`. The source files are `reel-urdu.html`, `build_urdu.py` and `timeline.js`, and the voice track alone is `voice-urdu.mp3`.
Urdu caption to post with it:
> Rs 0 mein apna AI video editor 🤖🎬 Claude + muft tools = raw footage se tayyar reel, sirf ek prompt mein.
> Comment **BUILD** karein, main poora prompt DM karunga.
> #BuildWithAhmed #ClaudeAI #AIVideoEditing #AITools #PakistanTech #ContentCreation

### Urdu version, ~73s, young male voice (current)
The voice is Kokoro `hm_psi` with the pitch raised slightly (×1.08) so it sounds younger. The video's timing follows the voice: `build_urdu.py` generates the voice and writes `timeline.js`, and `reel-urdu.html` reads it.
```bash
python3 build_urdu.py <kokoro-model-dir> work            # optional: voice name, pitch e.g. hm_omega 1.1
mkdir frames && node render.js reel-urdu.html frames 30 <total from timeline.js>
ffmpeg -framerate 30 -i frames/%05d.jpg -i work/voice.wav -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -shortest out.mp4
```

Script for recording in your own voice. Pause 1–2 seconds after each line.
1. Video editor ki fees? Ab bilkul muft.
2. Ek muft AI pipeline. Raw clip andar, tayyar reel bahar.
3. Step ek: Claude Desktop install karein, aur ek project folder banayein.
4. Step do: Claude ko chaar muft tools dein.
5. FFmpeg: video ka engine. Cut, join, aur final render.
6. Whisper: awaz sun kar khud captions likhta hai.
7. yt-dlp: reels download kar ke study karne ke liye.
8. HyperFrames: animated text aur motion graphics.
9. Yeh chaar tools Claude ko super powerful bana dein ge.
10. Bas in ke links prompt ke saath paste karein, aur Claude inhein khud install kar le ga.
11. Step teen hai style.
12. Apne favourite creator ki teen se paanch reels Claude ko dein.
13. Yeh un ki editing style ko, font se le kar sound design tak, poora breakdown kar de ga.
14. Phir yeh prompt dein, aur Claude ek reusable style sheet bana de ga,
15. jo har baar perfection ke saath kaam karti hai.
16. Step chaar: footage daalein, ek prompt dein, aur reel tayyar.
17. Poora prompt chahiye? Comment karein BUILD. Aur follow karein, Build with Ahmed.

## Final: Ahmed's own voice (YouTube Short)
`build-with-ahmed-ai-editing-short-own-voice.mp4` (72.3s) uses Ahmed's own recording, which has been cleaned (high-pass filter, noise reduction, compression, loudness at -14 LUFS). Removed: the false start "bas in ke…", the first take of "Apne favourite creator ki…", and the mispronounced "FFmpeg" (~18s). The voice track alone is `voice-own.mp3`.
`build_own_voice.py` lists which part of the recording goes with which line. For a new recording, update those times and run:
```bash
python3 build_own_voice.py recording.m4a work
mkdir frames && node render.js reel-urdu.html frames 30 <total from timeline.js>
ffmpeg -framerate 30 -i frames/%05d.jpg -i work/voice.wav -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -af loudnorm=I=-14:TP=-1.5 -shortest out.mp4
```

### Background music
`bg-music-original.mp3` is an original lo-fi track made from scratch by `gen_music.py` (pure synthesis, no samples), so it can't get a copyright strike or a Content ID claim. It sits ~12 dB under the voice and ducks automatically (sidechain) while you speak:
```bash
python3 gen_music.py <seconds> music.wav
ffmpeg -i voice.wav -i music.wav -filter_complex "[0:a]aresample=44100,aformat=channel_layouts=stereo,asplit[v1][v2];[1:a]volume=0.22[m];[m][v2]sidechaincompress=threshold=0.02:ratio=5:attack=30:release=500[md];[v1][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5[a]" -map "[a]" mixed.wav
```
