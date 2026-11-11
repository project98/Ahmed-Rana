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
