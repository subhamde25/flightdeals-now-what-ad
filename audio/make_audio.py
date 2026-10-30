"""Synthesize BGM + SFX for the FlightDeals "Now what?" ad, mix with the Fish Audio VO.
Writes build/mix.wav (pre-master) and build/stems/{vo,music,sfx}.wav (stems at mix level, for QA).
All events are on the same timeline as h169/index.html (VO at +0.25 s, drop at 3.25 s, 120 BPM)."""
import wave, sys, os
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1')  # keeps BLAS start-up memory low on 8 GB machines
import numpy as np
from scipy import signal

SR = 48000
DUR = 21.2
N = int(SR * DUR)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(REPO, 'build')
rng = np.random.default_rng(7)

def t_arr(d): return np.arange(int(SR * d)) / SR
def midi(m): return 440.0 * 2 ** ((m - 69) / 12)
def put(buf, x, t0, gain=1.0, pan=0.0):
    """add mono x (or stereo Nx2) into stereo buf at time t0 with constant-power pan"""
    i0 = int(round(t0 * SR))
    if x.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        x = np.stack([x * l, x * r], 1) * np.sqrt(2)
    if i0 < 0: x = x[-i0:]; i0 = 0
    n = min(len(x), len(buf) - i0)
    if n > 0: buf[i0:i0 + n] += x[:n] * gain

def lp(x, fc, order=2): return signal.sosfilt(signal.butter(order, fc, 'low', fs=SR, output='sos'), x, axis=0)
def hp(x, fc, order=2): return signal.sosfilt(signal.butter(order, fc, 'high', fs=SR, output='sos'), x, axis=0)
def bp(x, lo, hi, order=2): return signal.sosfilt(signal.butter(order, [lo, hi], 'band', fs=SR, output='sos'), x, axis=0)

def svf(x, fc, q=0.8, mode='bp'):
    """TPT state-variable filter with per-sample cutoff (for sweeps)"""
    g = np.tan(np.pi * np.clip(fc, 30, SR * 0.45) / SR); k = 1 / q
    y = np.zeros_like(x); ic1 = ic2 = 0.0
    for n in range(len(x)):
        G = g[n]; a1 = 1 / (1 + G * (G + k)); a2 = G * a1; a3 = G * a2
        v3 = x[n] - ic2; v1 = a1 * ic1 + a2 * v3; v2 = ic2 + a2 * ic1 + a3 * v3
        ic1 = 2 * v1 - ic1; ic2 = 2 * v2 - ic2
        y[n] = v1 if mode == 'bp' else v2
    return y

def reverb_ir(d=2.2, decay=3.2, bright=6000):
    t = t_arr(d)
    ir = rng.standard_normal((len(t), 2)) * np.exp(-decay * t)[:, None]
    ir = lp(ir, bright); ir[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))[:, None]
    return ir / np.sqrt((ir ** 2).sum(0)).max() * 0.9
IR = reverb_ir()
def reverb(x, wet=0.3):
    out = np.zeros_like(x)
    for c in range(2): out[:, c] = signal.fftconvolve(x[:, c], IR[:, c])[:len(x)]
    return x * (1 - wet) + out * wet

# ---------------------------------------------------------------- music
BEAT = 0.5; DROP = 3.25; END = 18.25
CH = {'D': [50, 57, 61, 64, 69], 'Bm': [47, 54, 57, 61, 66], 'G': [55, 59, 62, 66, 69], 'A': [57, 62, 64, 69, 71]}
ROOT = {'D': 38, 'Bm': 35, 'G': 31, 'A': 33}
PROG = [(0.0, 'D'), (1.97, 'G'), (3.25, 'D'), (5.25, 'Bm'), (7.25, 'G'), (9.25, 'A'), (11.25, 'D'), (13.25, 'Bm'), (15.25, 'G'), (17.25, 'A'), (18.25, 'D')]
def chord_at(t):
    c = PROG[0][1]
    for t0, n in PROG:
        if t >= t0: c = n
    return c

def saw(f, t):
    ph = (f * t) % 1.0
    return 2 * ph - 1

pad_dark = np.zeros((N, 2)); pad = np.zeros((N, 2))
for i, (t0, name) in enumerate(PROG):
    t1 = PROG[i + 1][0] if i + 1 < len(PROG) else DUR
    d = t1 - t0 + 0.6
    t = t_arr(d)
    env = np.minimum(1, t / 0.25) * np.minimum(1, np.maximum(0, (d - t) / 0.6))
    s = np.zeros((len(t), 2))
    for m in CH[name]:
        for det, pn in ((-0.07, -0.6), (0.0, 0.0), (0.07, 0.6)):
            f = midi(m + det)
            v = saw(f, t + rng.random())
            s[:, 0] += v * (1 - pn) * 0.5; s[:, 1] += v * (1 + pn) * 0.5
    s *= env[:, None] / 12
    put(pad, lp(s, 2600), t0); put(pad_dark, lp(s, 520), t0)
# intro: dark -> bright across the hook, dark again for "Now what?", bright on drop
tt = np.arange(N) / SR
mixb = np.interp(tt, [0, 1.2, 1.9, 2.1, 3.2, 3.25, END, END + 0.05], [0.1, 0.55, 0.55, 0.0, 0.25, 1.0, 1.0, 1.0])
pad_bus = pad * mixb[:, None] + pad_dark * (1 - mixb[:, None])

# pluck arpeggio (16ths) with ping-pong delay
pl = np.zeros((N, 2))
pat = [0, 2, 4, 2, 1, 3, 4, 3]
step = BEAT / 4
k0 = int(np.ceil((0.5 - DROP) / step))
k = k0
while True:
    t0 = DROP + k * step
    if t0 >= END: break
    if t0 >= 0.45 and not (2.05 <= t0 < 3.25):
        name = chord_at(t0 + 0.01)
        m = CH[name][pat[k % 8]] + 12
        t = t_arr(0.45)
        f = midi(m)
        v = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t + 0.3) + 0.12 * np.sin(6 * np.pi * f * t)) * np.exp(-t / 0.11)
        v *= np.minimum(1, t / 0.003)
        g = 0.5 if t0 < DROP else 0.8
        acc = 1.0 if k % 4 == 0 else 0.7
        put(pl, v * 0.09 * g * acc, t0, pan=0.25 * np.sin(k * 0.7))
    k += 1
d1, d2 = int(0.375 * SR), int(0.75 * SR)
dl = np.zeros_like(pl)
dl[d1:, 1] += pl[:-d1, 0] * 0.38 + pl[:-d1, 1] * 0.1
dl[d2:, 0] += pl[:-d2, 1] * 0.22 + pl[:-d2, 0] * 0.05
pl_bus = lp(pl + lp(dl, 3500), 7000)

# drums
dr = np.zeros((N, 2)); kick_times = []
def kick():
    t = t_arr(0.42)
    f = 48 + 100 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    v = np.sin(ph) * np.exp(-t / 0.22) + 0.25 * rng.standard_normal(len(t)) * np.exp(-t / 0.004)
    return np.tanh(v * 1.4) * 0.8
def clap():
    t = t_arr(0.3); n = rng.standard_normal(len(t))
    e = np.zeros(len(t))
    for o in (0, 0.011, 0.022): e += (t >= o) * np.exp(-np.maximum(0, t - o) / (0.008 if o < 0.02 else 0.12))
    return bp(n * e, 900, 4200) * 0.55
def hat(dec=0.035):
    t = t_arr(0.12); return hp(rng.standard_normal(len(t)) * np.exp(-t / dec), 7500) * 0.32
def crash(d=1.6):
    t = t_arr(d); return hp(rng.standard_normal(len(t)) * np.exp(-t / 0.5), 5000) * 0.22
b = 0
while DROP + b * BEAT < END - 1e-6:
    t0 = DROP + b * BEAT
    kick_times.append(t0); put(dr, kick(), t0, 0.9)
    if b % 2 == 1: put(dr, clap(), t0, 0.55, pan=0.05)
    put(dr, hat(), t0 + BEAT / 2, 0.55, pan=0.3)
    put(dr, hat(0.018), t0 + BEAT / 4, 0.18, pan=-0.3); put(dr, hat(0.018), t0 + 3 * BEAT / 4, 0.22, pan=0.35)
    b += 1
for tc in (DROP, 6.25, 9.75, 13.25, 17.25):
    put(dr, crash(), tc, 0.8 if tc == DROP else 0.5, pan=-0.2)
# snare build before drop
for i in range(8):
    tb = 2.25 + i * 0.125
    put(dr, clap(), tb, 0.08 + 0.05 * i, pan=0.1 * ((-1) ** i))

# sidechain pump from kicks
pump = np.ones(N)
for tk in kick_times:
    i0 = int(tk * SR); L = int(0.3 * SR); n = min(L, N - i0)
    pump[i0:i0 + n] = np.minimum(pump[i0:i0 + n], 1 - 0.55 * np.exp(-np.arange(n) / SR / 0.09))
pump = lp(pump, 40)

# sub bass on 8ths after drop
bs = np.zeros(N)
b = 0
while DROP + b * BEAT / 2 < END - 1e-6:
    t0 = DROP + b * BEAT / 2
    f = midi(ROOT[chord_at(t0 + 0.01)] + 12)
    t = t_arr(0.24)
    v = np.sin(2 * np.pi * f * t) + 0.2 * np.sin(4 * np.pi * f * t)
    v *= np.minimum(1, t / 0.005) * np.exp(-t / 0.2)
    i0 = int(t0 * SR); n = min(len(v), N - i0); bs[i0:i0 + n] += v[:n] * 0.32
    b += 1
bass_bus = np.stack([bs, bs], 1) * pump[:, None]

# end: big D chord + bells
endc = np.zeros((N, 2))
t = t_arr(DUR - END)
for m, a in zip([38, 50, 57, 62, 66, 69, 74], [0.5, 0.35, 0.3, 0.3, 0.25, 0.22, 0.18]):
    f = midi(m); v = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t / 2.2) * np.minimum(1, t / 0.01)
    put(endc, v * a * 0.22, END, pan=(m - 60) / 40)
for i, m in enumerate([74, 78, 81, 86]):
    tt0 = 19.64 + i * 0.07; tb = t_arr(1.6); f = midi(m)
    v = (np.sin(2 * np.pi * f * tb) + 0.4 * np.sin(2 * np.pi * f * 2.76 * tb) * np.exp(-tb / 0.2)) * np.exp(-tb / 0.6)
    put(endc, v * 0.08, tt0, pan=-0.4 + 0.27 * i)

music = (pad_bus * 0.75 * (0.55 + 0.45 * pump[:, None]) + pl_bus * 1.0)
music = reverb(music, 0.32) + dr + bass_bus + reverb(endc, 0.4)

# ---------------------------------------------------------------- SFX
sfx = np.zeros((N, 2))
def whoosh(d, f0, f1, peak=0.8, q=1.2, pan0=0.0, pan1=0.0):
    t = t_arr(d); x = rng.standard_normal(len(t))
    fc = f0 * (f1 / f0) ** (t / d)
    y = svf(x, fc, q, 'bp')
    pk = peak * d
    env = np.where(t < pk, (t / pk) ** 2.2, np.exp(-(t - pk) / (0.06 + 0.15 * (d - pk))))
    y = y * env; y /= np.abs(y).max() + 1e-9
    p = np.linspace(pan0, pan1, len(t))
    return np.stack([y * np.cos((p + 1) * np.pi / 4), y * np.sin((p + 1) * np.pi / 4)], 1) * np.sqrt(2)
def click(f=2300):
    t = t_arr(0.06)
    v = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.006) + 0.5 * np.sin(2 * np.pi * 180 * t) * np.exp(-t / 0.015)
    v += 0.3 * hp(rng.standard_normal(len(t)), 3000) * np.exp(-t / 0.003)
    return v * 0.6
def chime(notes=(88, 95), gap=0.075, dec=0.5):
    out = np.zeros(int(SR * (gap * len(notes) + dec * 3)))
    for i, m in enumerate(notes):
        t = t_arr(dec * 3); f = midi(m)
        v = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / 0.1)) * np.exp(-t / dec) * np.minimum(1, t / 0.002)
        i0 = int(i * gap * SR); out[i0:i0 + len(v)] += v[:len(out) - i0]
    return out * 0.3
def pop(f=900):
    t = t_arr(0.12); fr = f * (1 + 0.8 * np.exp(-t / 0.012))
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.035) * 0.5
def boom(f=46, d=1.6, noise=0.4):
    t = t_arr(d); fr = f + 70 * np.exp(-t / 0.05)
    v = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.55)
    v += noise * lp(rng.standard_normal(len(t)), 1800) * np.exp(-t / 0.12)
    return np.tanh(v * 1.3) * 0.7
def shimmer(d=1.4, base=2600):
    t = t_arr(d); v = np.zeros(len(t))
    for i, r in enumerate([1, 1.5, 2.0, 2.52, 3.01]):
        v += np.sin(2 * np.pi * base * r * t + i) * (0.5 + 0.5 * np.sin(2 * np.pi * (7 + i * 1.3) * t)) / (1 + i)
    return v * np.minimum(1, t / 0.05) * np.exp(-t / (d / 3)) * 0.12
def riser(d, f0, f1):
    t = t_arr(d); fr = f0 * (f1 / f0) ** (t / d)
    tone = np.sin(2 * np.pi * np.cumsum(fr) / SR) * 0.25
    nz = svf(rng.standard_normal(len(t)), fr * 4, 1.5, 'bp')
    v = (tone + nz / (np.abs(nz).max() + 1e-9) * 0.6) * (t / d) ** 2
    return v * 0.5
def thump(f=70):
    t = t_arr(0.5); fr = f + 60 * np.exp(-t / 0.03)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t / 0.16) * 0.8

def whoosh_into(tc, d=0.35, g=0.5, f0=300, f1=5000, p0=0, p1=0):
    put(sfx, whoosh(d + 0.12, f0, f1, peak=d / (d + 0.12), pan0=p0, pan1=p1), tc - d, g)

# hook
put(sfx, whoosh(0.9, 200, 1800, peak=0.45), 0.0, 0.25)
put(sfx, click(), 0.93, 0.5, pan=-0.3)
put(sfx, chime((88, 95)), 1.0, 0.55, pan=-0.2)
put(sfx, pop(1300), 1.08, 0.3, pan=0.4)
for i, f in enumerate((620, 560, 500)): put(sfx, pop(f), 1.42 + 0.08 * i, 0.25, pan=0.5)
put(sfx, thump(60), 1.96, 0.9); put(sfx, boom(55, 0.6, 0.5), 1.96, 0.35)
put(sfx, thump(75), 2.25, 0.75); put(sfx, boom(60, 0.5, 0.4), 2.25, 0.25)
put(sfx, riser(1.0, 180, 1400), 2.25, 0.5)
whoosh_into(3.25, 0.4, 0.55, 250, 6000)
# drop / brand
put(sfx, boom(44, 1.8, 0.5), 3.25, 0.55); put(sfx, shimmer(1.6, 2900), 3.25, 0.6)
put(sfx, whoosh(0.8, 500, 2500, peak=0.35, pan0=0.8, pan1=-0.8), 3.28, 0.28)
put(sfx, pop(700), 4.07, 0.3)
for i, f in enumerate((820, 980, 1180)): put(sfx, pop(f), 4.61 + 0.18 * i, 0.35, pan=-0.4 + 0.4 * i)
put(sfx, shimmer(0.9, 3300), 5.55, 0.5)
whoosh_into(6.25, 0.38, 0.6, 300, 7000)
put(sfx, boom(52, 0.7, 0.6), 6.25, 0.35)
# experiences
put(sfx, whoosh(0.6, 1800, 400, peak=0.3), 6.27, 0.2)
put(sfx, whoosh(0.5, 900, 300, peak=0.5), 7.1, 0.18)
put(sfx, whoosh(0.5, 700, 2400, peak=0.5, pan0=-0.6, pan1=0.0), 7.25, 0.12)
put(sfx, click(), 9.21, 0.55, pan=0.15)
put(sfx, chime((86, 93)), 9.24, 0.5, pan=0.1)
put(sfx, whoosh(0.35, 1500, 3500, peak=0.4), 9.25, 0.15)
whoosh_into(9.75, 0.28, 0.55, 400, 6000, 0.6, -0.8)
put(sfx, boom(55, 0.6, 0.5), 9.75, 0.3)
# transfers
put(sfx, whoosh(0.55, 2000, 500, peak=0.25, pan0=0.8, pan1=0.0), 9.76, 0.22)
put(sfx, whoosh(0.55, 500, 2200, peak=0.45), 11.15, 0.18)
put(sfx, riser(1.1, 300, 900), 11.45, 0.18)
put(sfx, pop(950), 11.8, 0.3, pan=0.4)
put(sfx, chime((81, 88, 93), gap=0.09, dec=0.4), 12.75, 0.55)
put(sfx, whoosh(0.35, 1500, 3500, peak=0.4), 12.79, 0.14)
whoosh_into(13.25, 0.32, 0.55, 300, 6500)
put(sfx, boom(50, 0.7, 0.6), 13.25, 0.32)
# rent a car
put(sfx, whoosh(0.6, 1800, 400, peak=0.3), 13.27, 0.2)
put(sfx, whoosh(0.5, 900, 300, peak=0.5), 14.15, 0.16)
put(sfx, click(), 15.31, 0.55, pan=0.15)
put(sfx, chime((86, 93)), 15.34, 0.45, pan=0.1)
put(sfx, whoosh(0.6, 400, 2200, peak=0.45), 15.5, 0.25)
for i in range(4): put(sfx, click(5200 + 700 * i), 15.72 + 0.045 * i, 0.12, pan=-0.3 + 0.2 * i)  # key jingle
whoosh_into(17.25, 0.32, 0.55, 300, 6500, 0, 0)
put(sfx, boom(52, 0.6, 0.5), 17.25, 0.3)
# resolve + end
for i, m in enumerate((84, 88, 91, 96)): put(sfx, chime((m,), dec=0.25), 17.45 + 0.11 * i, 0.45, pan=-0.3 + 0.2 * i)
whoosh_into(18.25, 0.3, 0.6, 400, 8000)
put(sfx, boom(40, 2.4, 0.7), 18.25, 0.5); put(sfx, shimmer(2.2, 2400), 18.27, 0.5)
put(sfx, pop(1100), 19.64, 0.35); put(sfx, shimmer(1.2, 3600), 19.66, 0.45)
put(sfx, click(), 20.55, 0.5, pan=0.1); put(sfx, shimmer(0.8, 4200), 20.57, 0.3)
sfx = reverb(sfx, 0.18)

# ---------------------------------------------------------------- VO + mix
def read_wav(p):
    w = wave.open(p); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if w.getnchannels() == 2: x = x.reshape(-1, 2).mean(1)
    assert w.getframerate() == SR
    return x
vo = read_wav(os.path.join(REPO, 'assets', 'audio', 'vo.wav'))
vo_bus = np.zeros((N, 2)); put(vo_bus, vo, 0.25, 1.0)
vo_bus = vo_bus / (np.abs(vo_bus).max() + 1e-9) * 0.75
vo_bus = reverb(vo_bus, 0.06)

env = np.abs(vo_bus[:, 0])
env = signal.sosfilt(signal.butter(1, 6, 'low', fs=SR, output='sos'), env)
duck = 1 - 0.55 * np.clip(env / 0.05, 0, 1)
duck = lp(duck, 4)
mus_gain = np.interp(tt, [0, 3.2, 3.25, END - 0.05, END, DUR], [2.0, 2.0, 1.0, 1.0, 1.6, 1.6])
music *= (duck * mus_gain)[:, None] / (np.abs(music).max() + 1e-9) * 0.24

mix = vo_bus + music + sfx * 0.42
_sc = 1/(np.abs(mix).max() + 1e-9)
mix *= _sc
mix = np.tanh(mix * 1.15) / np.tanh(1.15) * 0.95
fade = int(0.06 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]

def write(p, x):
    y = (np.clip(x, -1, 1) * 32767).astype(np.int16)
    w = wave.open(p, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(y.tobytes()); w.close()
os.makedirs(os.path.join(BUILD, 'stems'), exist_ok=True)
write(os.path.join(BUILD, 'mix.wav'), mix)
for nm, x in (('vo', vo_bus), ('music', music), ('sfx', sfx * 0.42)): write(os.path.join(BUILD, 'stems', nm + '.wav'), x * _sc)
print('wrote build/mix.wav', mix.shape[0] / SR, 's')
