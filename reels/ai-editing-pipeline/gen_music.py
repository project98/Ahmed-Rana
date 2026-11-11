"""Generate an original, royalty-free lo-fi background bed (no samples, pure synthesis).

usage: python3 gen_music.py <seconds> <out.wav>
Everything here is synthesized from scratch, so there is no third-party copyright
and nothing for Content ID to match.
"""
import sys, numpy as np, soundfile as sf

DUR, OUT = float(sys.argv[1]), sys.argv[2]
SR, BPM = 44100, 84
beat = 60 / BPM; bar = 4 * beat
N = int(DUR * SR); t = np.arange(N) / SR
rng = np.random.default_rng(7)
mix = np.zeros((N, 2), np.float32)

def note(f): return 440 * 2 ** ((f - 69) / 12)
def env(n, a, r):
    e = np.ones(n, np.float32); ai = min(n, int(a * SR)); ri = min(n, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[n - ri:] *= np.linspace(1, 0, ri); return e
def lowpass(x, cutoff):
    a = np.exp(-2 * np.pi * cutoff / SR); y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s = (1 - a) * x[i] + a * s; y[i] = s
    return y
def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR); j = min(N, i + len(sig))
    if i >= N: return
    s = sig[: j - i] * gain
    mix[i:j, 0] += s * (1 - pan) / 2 * 2 ** .5; mix[i:j, 1] += s * (1 + pan) / 2 * 2 ** .5

# warm 7th chords: Fmaj7 - Em7 - Dm7 - Cmaj7 (a generic progression)
CHORDS = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]
BASS = [41, 40, 38, 36]
nbars = int(np.ceil(DUR / bar))
for b in range(nbars):
    st = b * bar; ch = CHORDS[b % 4]; n = int(bar * SR) + int(0.6 * SR)
    tt = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * note(m) * tt + 0.3 * np.sin(2 * np.pi * 0.25 * tt)) * 0.6 +
              np.sin(2 * np.pi * note(m) * 2.003 * tt) * 0.12 for m in ch)
    add((pad * env(n, 0.5, 0.8)).astype(np.float32), st, pan=0.0, gain=0.045)
    # soft keys arpeggio on 8th notes
    for k in range(8):
        m = ch[[0, 2, 1, 3, 2, 1, 3, 2][k]] + 12; ln = int(beat * 0.9 * SR); kt = np.arange(ln) / SR
        key = (np.sin(2 * np.pi * note(m) * kt) + 0.25 * np.sin(4 * np.pi * note(m) * kt)) * np.exp(-kt * 5)
        add(key.astype(np.float32), st + k * beat / 2 + rng.uniform(0, 0.012), pan=(-.4 if k % 2 else .4), gain=0.03)
    # sub bass
    ln = int(bar * SR); bt = np.arange(ln) / SR
    add((np.sin(2 * np.pi * note(BASS[b % 4]) * bt) * env(ln, 0.05, 0.3)).astype(np.float32), st, gain=0.09)
    # drums (enter after the first bar): soft kick 1 & 3, snare-ish rim 2 & 4, hats on 8ths
    if b >= 1:
        for q in range(4):
            if q in (0, 2):
                ln = int(0.35 * SR); kt = np.arange(ln) / SR
                kick = np.sin(2 * np.pi * (45 + 70 * np.exp(-kt * 30)) * kt) * np.exp(-kt * 9)
                add(kick.astype(np.float32), st + q * beat, gain=0.22)
            else:
                ln = int(0.18 * SR); kt = np.arange(ln) / SR
                sn = lowpass(rng.standard_normal(ln).astype(np.float32), 2500) * np.exp(-kt * 22)
                add(sn, st + q * beat + 0.01, gain=0.10)
        for h in range(8):
            ln = int(0.05 * SR); kt = np.arange(ln) / SR
            hat = np.diff(rng.standard_normal(ln + 1)).astype(np.float32) * np.exp(-kt * 70)
            add(hat, st + h * beat / 2 + (0.03 if h % 2 else 0), pan=0.3, gain=0.022 if h % 2 else 0.03)
# gentle tape hiss for warmth
mix += (lowpass(rng.standard_normal(N).astype(np.float32), 3000) * 0.004)[:, None]
fade = np.ones(N, np.float32); fi, fo = int(1.0 * SR), int(2.0 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
mix *= fade[:, None]
mix /= np.abs(mix).max() / 0.8
sf.write(OUT, mix, SR)
print("wrote", OUT, DUR, "s")
