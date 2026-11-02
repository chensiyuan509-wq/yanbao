"""音效：全部用 numpy 现场合成（无背景音乐、无外部素材）。

每个场景的 sfx() 给出 (时间, 音效名, 参数)，这里负责把它们合成为一条立体声音轨：
  1. 逐个生成音效（单声道），按增益 / 声像放进立体声总线；
  2. 加一点房间混响（分块 FFT 卷积，内存占用小）；
  3. 软限幅 + 归一化，输出 48kHz / 16bit WAV。
"""
import math
import wave

import numpy as np

SR = 48000
TWO_PI = 2 * np.pi


# ---------------------------------------------------------------- 基础工具


def _t(dur):
    return np.arange(max(1, int(dur * SR))) / SR


def _rng(seed):
    return np.random.default_rng(int(abs(seed)) % (2 ** 32))


def _fft_filter(x, fn):
    """频域滤波：fn(f) 返回各频率的增益。"""
    n = len(x)
    if n < 8:
        return x
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    return np.fft.irfft(X * fn(f), n)


def lowpass(x, fc, order=2):
    return _fft_filter(x, lambda f: 1 / np.sqrt(1 + (f / fc) ** (2 * order)))


def highpass(x, fc, order=2):
    return _fft_filter(x, lambda f: 1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** (2 * order)))


def bandpass(x, lo, hi, order=2):
    return _fft_filter(x, lambda f: (1 / np.sqrt(1 + (f / hi) ** (2 * order))) *
                       (1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** (2 * order))))


def env_ad(n, attack, decay_rate):
    """指数衰减包络（attack 秒的线性起音）。"""
    t = np.arange(n) / SR
    e = np.exp(-t * decay_rate)
    na = max(1, int(attack * SR))
    e[:na] *= np.linspace(0, 1, na)
    return e


def fade_edges(x, fin=0.003, fout=0.01):
    n = len(x)
    a, b = min(n, int(fin * SR)), min(n, int(fout * SR))
    if a > 1:
        x[:a] *= np.linspace(0, 1, a)
    if b > 1:
        x[-b:] *= np.linspace(1, 0, b)
    return x


def tone(freqs, dur, phase=0.0):
    """freqs 可为常数或逐样本数组（扫频）。"""
    n = max(1, int(dur * SR))
    f = np.broadcast_to(np.asarray(freqs, dtype=float), (n,))
    ph = TWO_PI * np.cumsum(f) / SR + phase
    return np.sin(ph)


def bell(freq, dur=1.0, decay=4.0, idx=1.6, ratio=3.5):
    t = _t(dur)
    mod = idx * np.exp(-t * decay * 1.8) * np.sin(TWO_PI * freq * ratio * t)
    s = np.sin(TWO_PI * freq * t + mod) * np.exp(-t * decay)
    s += 0.25 * np.sin(TWO_PI * freq * 2.0 * t) * np.exp(-t * decay * 1.6)
    return fade_edges(s, 0.002, 0.02)


def noise(dur, seed):
    return _rng(seed).standard_normal(max(1, int(dur * SR)))


def fit(x, n):
    """截断或补零到长度 n。"""
    if len(x) >= n:
        return x[:n]
    return np.concatenate([x, np.zeros(n - len(x))])


def norm(x, peak=1.0):
    m = np.max(np.abs(x)) if len(x) else 0
    return x * (peak / m) if m > 1e-9 else x


def sweep_noise(dur, f0, f1, seed, bands=7, width=0.55, curve=None):
    """移动频带的噪声（嗖嗖声）。curve(u) 给出 0..1 的扫频位置。"""
    n = max(8, int(dur * SR))
    base = noise(dur, seed)
    u = np.linspace(0, 1, n)
    pos = curve(u) if curve else u
    lf0, lf1 = math.log(f0), math.log(f1)
    centers = np.exp(np.linspace(min(lf0, lf1) - 0.3, max(lf0, lf1) + 0.3, bands))
    target = np.exp(lf0 + (lf1 - lf0) * pos)
    out = np.zeros(n)
    for c in centers:
        b = bandpass(base, c / 1.5, c * 1.5, 2)
        w = np.exp(-((np.log(target) - math.log(c)) ** 2) / (2 * width ** 2))
        out += b * w
    return out


# ---------------------------------------------------------------- 音效库
# 每个函数返回单声道数组（峰值约 1），参数里的 pitch 为音高倍率。


def s_pop(pitch=1.0, seed=0, **_):
    d = 0.16
    t = _t(d)
    f = (260 + 520 * (1 - np.exp(-t * 60))) * pitch
    s = tone(f, d) * env_ad(len(t), 0.002, 26)
    s += 0.3 * tone(f * 2, d) * env_ad(len(t), 0.002, 40)
    return norm(fade_edges(s))


def s_pop_big(pitch=1.0, seed=0, **_):
    d = 0.45
    t = _t(d)
    f = (150 + 420 * (1 - np.exp(-t * 30))) * pitch
    s = tone(f, d) * env_ad(len(t), 0.002, 10)
    s += 0.25 * highpass(noise(d, seed), 3000) * env_ad(len(t), 0.001, 40)
    sp = s_sparkle(dur=0.4, seed=seed + 1) * 0.25
    s[:len(sp)] += sp[:len(s)]
    return norm(fade_edges(s))


def s_tick(pitch=1.0, seed=0, **_):
    d = 0.06
    t = _t(d)
    s = bandpass(noise(d, seed), 2000, 7000) * env_ad(len(t), 0.0005, 160)
    s += 0.6 * tone(2100 * pitch, d) * env_ad(len(t), 0.0005, 90)
    return norm(fade_edges(s, 0.0005, 0.005))


def s_click(pitch=1.0, seed=0, **_):
    d = 0.08
    t = _t(d)
    s = bandpass(noise(d, seed), 2500, 9000) * env_ad(len(t), 0.0003, 220)
    s += 0.7 * tone(3200 * pitch, d) * env_ad(len(t), 0.0003, 120)
    s += 0.5 * tone(180, d) * env_ad(len(t), 0.001, 60)
    return norm(fade_edges(s, 0.0003, 0.005))


def s_blip(pitch=1.0, seed=0, **_):
    d = 0.1
    t = _t(d)
    f = 880 * pitch
    s = (np.sin(TWO_PI * f * t) + 0.3 * np.sin(TWO_PI * 3 * f * t)) * env_ad(len(t), 0.001, 35)
    return norm(fade_edges(s))


def s_whoosh(dur=0.9, seed=0, **_):
    def curve(u):
        return np.sin(np.clip(u, 0, 1) * math.pi / 2) ** 1.2
    s = sweep_noise(dur, 250, 3200, seed, curve=lambda u: np.where(u < 0.6, curve(u / 0.6), 1 - 0.6 * (u - 0.6) / 0.4))
    n = len(s)
    u = np.linspace(0, 1, n)
    env = np.where(u < 0.58, (u / 0.58) ** 2.2, ((1 - u) / 0.42) ** 1.6)
    return norm(s * env)


def s_whoosh_short(seed=0, **_):
    return s_whoosh(dur=0.38, seed=seed)


def s_swish(seed=0, **_):
    d = 0.28
    s = sweep_noise(d, 1500, 7000, seed, bands=5)
    u = np.linspace(0, 1, len(s))
    return norm(s * np.sin(u * math.pi) ** 2)


def s_swish_hi(seed=0, **_):
    d = 0.5
    s = sweep_noise(d, 3000, 10000, seed, bands=5)
    u = np.linspace(0, 1, len(s))
    return norm(s * np.sin(u * math.pi) ** 1.5)


def s_zip(pitch=1.0, seed=0, **_):
    d = 0.2
    s = sweep_noise(d, 900 * pitch, 6500 * pitch, seed, bands=5, width=0.4)
    u = np.linspace(0, 1, len(s))
    return norm(s * np.sin(u * math.pi) ** 1.2)


def s_hop(pitch=1.0, seed=0, **_):
    d = 0.18
    t = _t(d)
    f = (240 + 300 * t / d) * pitch
    s = tone(f, d) * np.sin(np.pi * t / d) ** 0.8
    return norm(fade_edges(s)) * 0.8


def s_boing(pitch=1.0, seed=0, **_):
    d = 0.5
    t = _t(d)
    f = (320 + 140 * np.sin(TWO_PI * 16 * t) * np.exp(-t * 7) + 160 * t) * pitch
    s = tone(f, d) * env_ad(len(t), 0.003, 6)
    s += 0.2 * tone(f * 2, d) * env_ad(len(t), 0.003, 10)
    return norm(fade_edges(s))


def s_key(seed=0, gain=1.0, **_):
    r = _rng(seed)
    d = 0.07
    t = _t(d)
    s = bandpass(noise(d, seed + 3), 1200, 5000) * env_ad(len(t), 0.0004, r.uniform(110, 160))
    s += 0.5 * tone(r.uniform(140, 200), d) * env_ad(len(t), 0.001, 70)
    return norm(fade_edges(s, 0.0004, 0.005))


def s_typing(dur=1.0, seed=0, **_):
    r = _rng(seed + 11)
    n = int(dur * SR)
    out = np.zeros(n + int(0.1 * SR))
    tt = 0.0
    k = 0
    while tt < dur:
        ks = s_key(seed=seed * 31 + k) * r.uniform(0.45, 1.0)
        i = int(tt * SR)
        out[i:i + len(ks)] += ks[:len(out) - i]
        tt += r.uniform(0.055, 0.12)
        k += 1
    return norm(out)


def s_check(pitch=1.0, seed=0, **_):
    a = bell(1318 * pitch, 0.35, 9, 0.8, 2.0)
    b = bell(1760 * pitch, 0.45, 8, 0.8, 2.0)
    out = np.zeros(int(0.55 * SR))
    out[:len(a)] += a
    i = int(0.075 * SR)
    out[i:i + len(b)] += b[:len(out) - i]
    return norm(out)


def s_thud(pitch=1.0, seed=0, **_):
    d = 0.3
    t = _t(d)
    f = (55 + 60 * np.exp(-t * 30)) * pitch
    s = tone(f, d) * env_ad(len(t), 0.002, 14)
    s += 0.35 * lowpass(noise(d, seed), 400) * env_ad(len(t), 0.001, 35)
    return norm(fade_edges(s))


def s_connect(pitch=1.0, seed=0, **_):
    d = 0.12
    t = _t(d)
    up = tone((500 + 900 * t / d) * pitch, d) * np.sin(np.pi * t / d)
    b = bell(1046 * pitch, 0.6, 6, 1.2, 2.0)
    out = np.zeros(len(up) + len(b))
    out[:len(up)] += up * 0.6
    out[len(up) - int(0.02 * SR):len(up) - int(0.02 * SR) + len(b)] += b
    return norm(out)


def s_clunk(pitch=1.0, seed=0, **_):
    d = 0.5
    t = _t(d)
    s = tone(70 * pitch, d) * env_ad(len(t), 0.002, 12)
    for f, dec, amp in ((420, 25, 0.5), (1130, 32, 0.35), (1870, 40, 0.25)):
        s += amp * np.sin(TWO_PI * f * pitch * t) * env_ad(len(t), 0.001, dec)
    s += 0.5 * bandpass(noise(d, seed), 200, 2000) * env_ad(len(t), 0.001, 45)
    return norm(fade_edges(s))


def s_rise(pitch=1.0, dur=0.6, seed=0, **_):
    t = _t(dur)
    f = (380 + 520 * (t / dur) ** 1.3) * pitch
    s = tone(f, dur) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.2
    s += 0.2 * tone(f * 2, dur) * np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return norm(fade_edges(s)) * 0.8


def s_impact_soft(seed=0, **_):
    d = 1.6
    t = _t(d)
    s = tone(48 + 30 * np.exp(-t * 6), d) * env_ad(len(t), 0.004, 3.2)
    s += 0.6 * lowpass(noise(d, seed), 300) * env_ad(len(t), 0.002, 6)
    sh = s_sparkle(dur=1.0, seed=seed + 2) * 0.18
    s[:len(sh)] += sh
    return norm(fade_edges(s))


def s_notify(pitch=1.0, seed=0, **_):
    a = bell(1318 * pitch, 0.6, 5, 1.0, 2.76)
    b = bell(1975 * pitch, 0.8, 4.5, 1.0, 2.76)
    out = np.zeros(int(1.0 * SR))
    out[:len(a)] += a
    i = int(0.11 * SR)
    out[i:i + len(b)] += b[:len(out) - i] * 0.9
    return norm(out)


def s_bubble(pitch=1.0, seed=0, **_):
    out = np.zeros(int(0.22 * SR))
    for k, (st, f0) in enumerate(((0.0, 380), (0.07, 520))):
        d = 0.08
        t = _t(d)
        s = tone((f0 + 900 * (t / d) ** 2) * pitch, d) * np.sin(np.pi * t / d)
        i = int(st * SR)
        out[i:i + len(s)] += s[:len(out) - i]
    return norm(out)


def s_coin(pitch=1.0, seed=0, **_):
    out = np.zeros(int(0.45 * SR))
    for st, f, d in ((0.0, 988, 0.07), (0.07, 1318, 0.35)):
        t = _t(d)
        s = (np.sin(TWO_PI * f * pitch * t) + 0.35 * np.sin(TWO_PI * 3 * f * pitch * t)) * env_ad(len(t), 0.001, 9)
        i = int(st * SR)
        out[i:i + len(s)] += s[:len(out) - i]
    return norm(fade_edges(out))


def s_ding(pitch=1.0, seed=0, **_):
    return norm(bell(1568 * pitch, 1.3, 3.5, 1.4, 3.0))


def s_fall(dur=1.0, seed=0, **_):
    t = _t(dur)
    f = 1100 * np.exp(-t / dur * 1.4)
    s = tone(f, dur) * np.sin(np.pi * np.clip(t / dur, 0, 1)) * 0.6
    s += 0.4 * sweep_noise(dur, 2500, 600, seed, bands=5) * np.sin(np.pi * np.clip(t / dur, 0, 1))
    return norm(fade_edges(s))


def s_surprise(seed=0, **_):
    d = 0.16
    t = _t(d)
    s = tone(320 + 700 * (t / d) ** 1.5, d) * np.sin(np.pi * t / d) ** 0.7
    return norm(fade_edges(s))


def s_sparkle(dur=1.0, seed=0, **_):
    r = _rng(seed + 5)
    out = np.zeros(int((dur + 0.4) * SR))
    n = max(4, int(dur * 14))
    for k in range(n):
        st = r.uniform(0, dur)
        f = r.choice([2637, 2960, 3136, 3520, 3951, 4186, 4699])
        b = bell(f, 0.35, 12, 0.6, 2.0) * r.uniform(0.3, 1.0)
        i = int(st * SR)
        out[i:i + len(b)] += b[:len(out) - i]
    return norm(out)


def s_shimmer(dur=1.2, seed=0, **_):
    r = _rng(seed + 9)
    out = np.zeros(int((dur + 0.8) * SR))
    notes = [1046, 1318, 1568, 2093, 2637, 3136, 4186]
    n = 12
    for k in range(n):
        st = dur * 0.75 * k / n + r.uniform(0, 0.03)
        f = notes[min(len(notes) - 1, int(k / n * len(notes)))] * r.choice([1.0, 1.0, 1.5])
        b = bell(f, 0.8, 5, 0.9, 2.0) * (0.5 + 0.5 * k / n)
        i = int(st * SR)
        out[i:i + len(b)] += b[:len(out) - i]
    return norm(out)


def s_success(pitch=1.0, seed=0, **_):
    out = np.zeros(int(1.2 * SR))
    for k, f in enumerate((1046, 1318, 1568, 2093)):
        b = bell(f * pitch, 0.9, 4.5, 1.0, 2.0)
        i = int(k * 0.075 * SR)
        out[i:i + len(b)] += b[:len(out) - i] * (0.7 + 0.1 * k)
    return norm(out)


def s_chime(seed=0, **_):
    out = np.zeros(int(1.4 * SR))
    for k, f in enumerate((1046, 1568)):
        b = bell(f, 1.3, 3.2, 1.1, 2.0)
        i = int(k * 0.05 * SR)
        out[i:i + len(b)] += b[:len(out) - i]
    return norm(out)


def s_pin(seed=0, **_):
    d = 0.22
    t = _t(d)
    s = np.sin(TWO_PI * 1750 * t) * env_ad(len(t), 0.0005, 45)
    s += 0.6 * np.sin(TWO_PI * 880 * t) * env_ad(len(t), 0.0005, 30)
    s += 0.5 * tone(120, d) * env_ad(len(t), 0.001, 40)
    return norm(fade_edges(s, 0.0005, 0.01))


def s_plug(pitch=1.0, seed=0, **_):
    d = 0.45
    t = _t(d)
    s = bandpass(noise(d, seed), 2000, 8000) * env_ad(len(t), 0.0003, 200)
    s += 0.8 * tone(130 * pitch, d) * env_ad(len(t), 0.001, 30)
    hum = (np.sin(TWO_PI * 100 * t) + 0.5 * np.sin(TWO_PI * 200 * t)) * env_ad(len(t), 0.02, 9) * 0.15
    s += hum
    return norm(fade_edges(s, 0.0003, 0.02))


def s_rumble(dur=0.8, seed=0, **_):
    t = _t(dur)
    s = lowpass(noise(dur, seed), 160, 3) * 3
    s += 0.3 * bandpass(noise(dur, seed + 1), 200, 900) * (0.5 + 0.5 * np.sin(TWO_PI * 13 * t))
    u = t / dur
    return norm(s * np.sin(np.pi * np.clip(u, 0, 1)) ** 0.6)


def s_gate(seed=0, **_):
    d = 0.7
    t = _t(d)
    s = np.zeros(len(t))
    for f, dec, amp in ((300, 8, 0.6), (845, 11, 0.45), (1520, 15, 0.3), (2380, 20, 0.2)):
        s += amp * np.sin(TWO_PI * f * t) * env_ad(len(t), 0.001, dec)
    s += 0.6 * tone(70, d) * env_ad(len(t), 0.002, 14)
    return norm(fade_edges(s))


def s_gear(dur=0.6, seed=0, **_):
    r = _rng(seed + 21)
    out = np.zeros(int((dur + 0.1) * SR))
    tt = 0.0
    while tt < dur:
        d = 0.03
        t = _t(d)
        c = bandpass(noise(d, int(tt * 1000) + seed), 1500, 6000) * env_ad(len(t), 0.0003, 250)
        c += 0.5 * np.sin(TWO_PI * r.uniform(1800, 2600) * t) * env_ad(len(t), 0.0003, 180)
        i = int(tt * SR)
        out[i:i + len(c)] += c[:len(out) - i] * r.uniform(0.5, 1.0)
        tt += r.uniform(0.035, 0.05)
    return norm(out)


def s_ratchet(dur=1.4, seed=0, **_):
    r = _rng(seed + 33)
    out = np.zeros(int((dur + 0.1) * SR))
    tt = 0.0
    while tt < dur:
        c = s_tick(pitch=r.uniform(0.8, 1.3), seed=int(tt * 997))
        i = int(tt * SR)
        out[i:i + len(c)] += c[:len(out) - i] * r.uniform(0.3, 0.9)
        tt += r.uniform(0.04, 0.11)
    return norm(out)


def s_gears_run(dur=5.0, seed=0, **_):
    t = _t(dur)
    g = fit(s_gear(dur=dur, seed=seed), len(t)) * 0.6
    hum = (np.sin(TWO_PI * 55 * t) + 0.4 * np.sin(TWO_PI * 110 * t)) * 0.25
    s = g + hum
    u = t / dur
    return norm(s * np.minimum(1, u * 5) * np.minimum(1, (1 - u) * 4))


def s_stamp(seed=0, **_):
    d = 0.4
    t = _t(d)
    s = tone(75 + 50 * np.exp(-t * 40), d) * env_ad(len(t), 0.001, 16)
    s += 0.9 * bandpass(noise(d, seed), 400, 3000) * env_ad(len(t), 0.0005, 55)
    return norm(fade_edges(s, 0.0005, 0.02))


def s_slide(seed=0, **_):
    d = 0.4
    s = bandpass(noise(d, seed), 700, 2200)
    u = np.linspace(0, 1, len(s))
    return norm(s * np.sin(u * math.pi) ** 1.5)


def s_lock(seed=0, **_):
    out = np.zeros(int(0.4 * SR))
    for st, p in ((0.0, 1.3), (0.06, 0.9)):
        c = s_click(pitch=p, seed=seed + int(st * 100))
        i = int(st * SR)
        out[i:i + len(c)] += c[:len(out) - i]
    th = s_thud(pitch=1.4, seed=seed) * 0.6
    i = int(0.05 * SR)
    out[i:i + len(th)] += th[:len(out) - i]
    return norm(out)


def s_bridge(pitch=1.0, seed=0, **_):
    out = np.zeros(int(1.2 * SR))
    for k, f in enumerate((784, 988, 1175)):
        b = bell(f * pitch, 0.9, 5, 0.9, 2.0)
        i = int(k * 0.09 * SR)
        out[i:i + len(b)] += b[:len(out) - i]
    sp = s_sparkle(dur=0.6, seed=seed) * 0.3
    out[:len(sp)] += sp[:len(out)]
    return norm(out)


def s_womp(seed=0, **_):
    d = 1.0
    t = _t(d)
    f = (330 - 120 * (t / d) ** 0.8) * (1 + 0.02 * np.sin(TWO_PI * 6 * t))
    s = sum(np.sin(TWO_PI * np.cumsum(f * h) / SR) / h ** 1.3 for h in range(1, 6))
    s = lowpass(s, 1200) * env_ad(len(t), 0.02, 2.2)
    return norm(fade_edges(s))


def s_powerup(seed=0, **_):
    d = 0.75
    t = _t(d)
    f = 180 + 1100 * (t / d) ** 1.6
    s = sum(np.sin(TWO_PI * np.cumsum(f * h) / SR) / h ** 1.5 for h in range(1, 5))
    s *= np.sin(np.pi * np.clip(t / d, 0, 1) * 0.5 + 0.1) ** 1.0 * np.minimum(1, (d - t) / 0.08 + 0.02)
    out = np.zeros(int(1.3 * SR))
    out[:len(s)] += s * 0.7
    sp = s_sparkle(dur=0.5, seed=seed + 4) * 0.5
    i = int(0.6 * SR)
    out[i:i + len(sp)] += sp[:len(out) - i]
    return norm(out)


def s_scan(dur=1.0, seed=0, **_):
    t = _t(dur)
    beeps = np.sin(TWO_PI * 1250 * t) * (np.sin(TWO_PI * 9 * t) > 0.6) * 0.5
    s = beeps + 0.25 * bandpass(noise(dur, seed), 3000, 7000)
    s = lowpass(s, 6000)
    u = t / dur
    return norm(s * np.minimum(1, u * 8) * np.minimum(1, (1 - u) * 8))


def s_chomp(seed=0, **_):
    out = np.zeros(int(0.35 * SR))
    for k, st in enumerate((0.0, 0.11)):
        d = 0.1
        t = _t(d)
        c = bandpass(noise(d, seed + k), 300, 2500) * env_ad(len(t), 0.002, 40)
        c += 0.6 * tone(110, d) * env_ad(len(t), 0.002, 45)
        i = int(st * SR)
        out[i:i + len(c)] += c[:len(out) - i]
    return norm(out)


def s_knock(seed=0, **_):
    d = 0.16
    t = _t(d)
    s = (np.sin(TWO_PI * 210 * t) + 0.6 * np.sin(TWO_PI * 470 * t)) * env_ad(len(t), 0.0005, 38)
    s += 0.4 * bandpass(noise(d, seed), 800, 4000) * env_ad(len(t), 0.0003, 120)
    return norm(fade_edges(s, 0.0005, 0.01))


def s_error(pitch=1.0, seed=0, **_):
    out = np.zeros(int(0.32 * SR))
    for st in (0.0, 0.14):
        d = 0.1
        t = _t(d)
        sq = np.sign(np.sin(TWO_PI * 196 * pitch * t)) * 0.6 + np.sin(TWO_PI * 392 * pitch * t) * 0.3
        c = lowpass(sq, 1800) * env_ad(len(t), 0.002, 8)
        i = int(st * SR)
        out[i:i + len(c)] += c[:len(out) - i]
    return norm(fade_edges(out))


def s_buzz(seed=0, **_):
    d = 0.35
    t = _t(d)
    sq = np.sign(np.sin(TWO_PI * 110 * t))
    return norm(fade_edges(lowpass(sq, 900) * env_ad(len(t), 0.005, 5), 0.005, 0.04))


def s_alert(seed=0, **_):
    out = np.zeros(int(0.4 * SR))
    for st in (0.0, 0.16):
        d = 0.11
        t = _t(d)
        c = (np.sin(TWO_PI * 880 * t) + 0.3 * np.sin(TWO_PI * 1760 * t)) * env_ad(len(t), 0.002, 10)
        i = int(st * SR)
        out[i:i + len(c)] += c[:len(out) - i]
    return norm(fade_edges(out))


def s_stream(dur=3.0, seed=0, **_):
    t = _t(dur)
    s = bandpass(noise(dur, seed), 900, 3500) * (0.6 + 0.4 * np.sin(TWO_PI * 0.9 * t + 1))
    r = _rng(seed + 2)
    for k in range(int(dur * 7)):
        st = r.uniform(0, dur)
        b = s_blip(pitch=r.uniform(1.2, 2.4)) * 0.25
        i = int(st * SR)
        s[i:i + len(b)] += b[:len(s) - i]
    u = t / dur
    return norm(s * np.minimum(1, u * 4) * np.minimum(1, (1 - u) * 4)) * 0.6


def s_stretch(dur=1.4, seed=0, **_):
    t = _t(dur)
    f = (190 + 230 * (t / dur)) * (1 + 0.05 * np.sin(TWO_PI * 13 * t))
    s = sum(np.sin(TWO_PI * np.cumsum(f * h) / SR) / h ** 1.6 for h in range(1, 4))
    u = t / dur
    return norm(fade_edges(lowpass(s, 1500) * np.minimum(1, u * 6) * np.minimum(1, (1 - u) * 5)))


def s_paper(seed=0, **_):
    r = _rng(seed + 8)
    d = 0.6
    out = np.zeros(int(d * SR))
    for k in range(9):
        st = r.uniform(0, d - 0.08)
        dd = r.uniform(0.02, 0.07)
        c = bandpass(noise(dd, seed + k), 1800, 7000) * np.sin(np.pi * np.linspace(0, 1, int(dd * SR)))
        i = int(st * SR)
        out[i:i + len(c)] += c[:len(out) - i] * r.uniform(0.4, 1.0)
    return norm(out)


def s_zap(dur=1.2, seed=0, **_):
    r = _rng(seed + 13)
    t = _t(dur)
    f = 90 + 300 * np.abs(lowpass(r.standard_normal(len(t)), 30)) * 6
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    crack = highpass(noise(dur, seed), 4000) * (r.random(len(t)) < 0.02) * 3
    s = lowpass(saw, 3000) * 0.6 + crack
    u = t / dur
    gate = (np.sin(TWO_PI * 7 * t + r.uniform(0, 6)) > -0.3).astype(float)
    return norm(s * gate * np.minimum(1, u * 10) * np.minimum(1, (1 - u) * 3))


def s_water(seed=0, **_):
    d = 0.9
    t = _t(d)
    s = lowpass(noise(d, seed), 900) * env_ad(len(t), 0.02, 4)
    r = _rng(seed + 3)
    for k in range(5):
        st = r.uniform(0.05, 0.6)
        bd = 0.06
        tt = _t(bd)
        b = tone(r.uniform(500, 900) + 1500 * tt / bd, bd) * np.sin(np.pi * tt / bd) * 0.4
        i = int(st * SR)
        s[i:i + len(b)] += b[:len(s) - i]
    return norm(fade_edges(s))


def s_snore_twitch(seed=0, **_):
    d = 0.35
    t = _t(d)
    s = tone(260 - 60 * t / d, d) * np.sin(np.pi * t / d) * 0.5
    s += 0.3 * lowpass(noise(d, seed), 800) * np.sin(np.pi * t / d)
    return norm(fade_edges(s))


def s_zoom_in(dur=1.6, seed=0, **_):
    t = _t(dur)
    u = t / dur
    s = sweep_noise(dur, 200, 5000, seed, curve=lambda v: v ** 1.5) * 0.8
    s += 0.35 * tone(150 + 1400 * u ** 2, dur)
    env = np.where(u < 0.85, (u / 0.85) ** 2, ((1 - u) / 0.15))
    return norm(fade_edges(s * env))


def s_wink(seed=0, **_):
    out = np.zeros(int(0.5 * SR))
    for st, f in ((0.0, 2093), (0.06, 3136)):
        b = bell(f, 0.4, 9, 0.6, 2.0)
        i = int(st * SR)
        out[i:i + len(b)] += b[:len(out) - i]
    return norm(out)


def s_shuffle(dur=1.2, seed=0, **_):
    r = _rng(seed + 17)
    out = np.zeros(int((dur + 0.2) * SR))
    tt = 0.0
    while tt < dur:
        c = s_slide(seed=int(tt * 1000) + seed)[:int(0.15 * SR)] * r.uniform(0.4, 1.0)
        i = int(tt * SR)
        out[i:i + len(c)] += c[:len(out) - i]
        tt += r.uniform(0.1, 0.2)
    return norm(out)


def s_door(seed=0, **_):
    d = 0.9
    t = _t(d)
    r = _rng(seed)
    f = 320 + 140 * np.abs(lowpass(r.standard_normal(len(t)), 20)) * 5
    s = np.sin(TWO_PI * np.cumsum(f) / SR) * 0.4 * (r.random(len(t)) < 0.3)
    s = bandpass(s, 300, 2500) + 0.4 * sweep_noise(d, 400, 1600, seed, bands=4)
    u = t / d
    return norm(s * np.sin(np.pi * u) ** 0.8)


def s_fan(dur=2.5, seed=0, **_):
    t = _t(dur)
    u = t / dur
    whirr = bandpass(noise(dur, seed), 300, 1600) * (0.3 + 0.7 * np.minimum(1, u * 2))
    motor = tone(90 + 120 * np.minimum(1, u * 1.5), dur) * 0.4
    s = whirr + motor
    return norm(s * np.minimum(1, u * 6) * np.minimum(1, (1 - u) * 3))


def s_think(dur=5.0, seed=0, **_):
    t = _t(dur)
    s = bandpass(noise(dur, seed), 500, 1800) * 0.4 * (0.6 + 0.4 * np.sin(TWO_PI * 2.5 * t))
    r = _rng(seed + 4)
    for k in range(int(dur * 5)):
        st = r.uniform(0, dur - 0.1)
        b = s_blip(pitch=r.choice([1.0, 1.26, 1.5, 1.68])) * 0.35
        i = int(st * SR)
        s[i:i + len(b)] += b[:len(s) - i]
    u = t / dur
    return norm(s * np.minimum(1, u * 6) * np.minimum(1, (1 - u) * 6))


def s_mail(seed=0, **_):
    sw = s_swish(seed=seed)
    b = bell(2093, 0.6, 6, 0.8, 2.0) * 0.6
    out = np.zeros(len(sw) + len(b))
    out[:len(sw)] += sw
    i = int(0.18 * SR)
    out[i:i + len(b)] += b[:len(out) - i]
    return norm(out)


def s_spinup(dur=5.0, seed=0, **_):
    t = _t(dur)
    u = t / dur
    rate = 1.2 + 9 * u ** 1.6                       # "呼呼"声的频率越来越快
    ph = TWO_PI * np.cumsum(rate) / SR
    whoom = 0.5 + 0.5 * np.sin(ph)
    body = bandpass(noise(dur, seed), 200, 1400) * whoom
    hum = tone(70 + 260 * u ** 1.4, dur) * 0.35
    s = body + hum
    return norm(s * np.minimum(1, u * 4) * np.minimum(1, (1 - u) * 5))


def s_glitch(dur=0.6, seed=0, **_):
    r = _rng(seed + 19)
    n = int(dur * SR)
    out = np.zeros(n)
    i = 0
    while i < n:
        seg = int(r.uniform(0.01, 0.05) * SR)
        kind = r.integers(0, 3)
        tt = np.arange(seg) / SR
        if kind == 0:
            c = np.sign(np.sin(TWO_PI * r.uniform(200, 1800) * tt))
        elif kind == 1:
            c = r.standard_normal(seg)
            c = np.round(c * 3) / 3
        else:
            c = np.zeros(seg)
        out[i:i + seg] = c[:n - i] * r.uniform(0.3, 1.0)
        i += seg
    return norm(lowpass(out, 7000))


def s_swell(dur=1.0, seed=0, **_):
    t = _t(dur)
    u = t / dur
    s = sweep_noise(dur, 300, 6000, seed, curve=lambda v: v ** 1.3) * 0.7
    s += 0.25 * fit(s_shimmer(dur=dur, seed=seed), len(t))
    return norm(s * np.where(u < 0.5, (u / 0.5) ** 2, (1 - u) / 0.5 * 0.9 + 0.1))


def s_grow(dur=2.8, seed=0, **_):
    t = _t(dur)
    u = t / dur
    f = 160 + 380 * u
    s = np.sin(TWO_PI * np.cumsum(f * (1 + 0.03 * np.sin(TWO_PI * 5 * t))) / SR) * 0.4
    s = lowpass(s, 900) + 0.3 * fit(s_sparkle(dur=dur * 0.8, seed=seed), len(t))
    return norm(s * np.minimum(1, u * 3) * np.minimum(1, (1 - u) * 3))


def s_finale(seed=0, **_):
    out = np.zeros(int(3.2 * SR))
    for k, f in enumerate((523, 659, 784, 1046, 1318, 1568, 2093)):
        b = bell(f, 2.4, 1.8, 1.0, 2.0) * (0.6 + 0.05 * k)
        i = int(k * 0.07 * SR)
        out[i:i + len(b)] += b[:len(out) - i]
    sh = s_shimmer(dur=1.6, seed=seed + 1) * 0.35
    i = int(0.5 * SR)
    out[i:i + len(sh)] += sh[:len(out) - i]
    im = s_impact_soft(seed=seed + 2) * 0.4
    out[:len(im)] += im[:len(out)]
    return norm(out)


# -- 环境声（长、轻） ----------------------------------------------------


def s_ambience_night(dur=17.0, seed=0, **_):
    t = _t(dur)
    wind = lowpass(noise(dur, seed), 500, 2) * (0.6 + 0.4 * np.sin(TWO_PI * 0.13 * t + 1))
    wind = highpass(wind, 80)
    r = _rng(seed + 7)
    crick = np.zeros(len(t))
    for k in range(int(dur * 0.9)):
        st = r.uniform(0, dur - 0.3)
        for j in range(3):
            d = 0.025
            tt = _t(d)
            c = np.sin(TWO_PI * 4400 * tt) * np.sin(np.pi * tt / d) * 0.25
            i = int((st + j * 0.05) * SR)
            crick[i:i + len(c)] += c[:len(crick) - i]
    s = norm(wind) * 0.8 + crick
    u = t / dur
    return norm(s * np.minimum(1, u * 6) * np.minimum(1, (1 - u) * 4)) * 0.35


def s_ambience_sea(dur=35.0, seed=0, **_):
    t = _t(dur)
    swell = 0.55 + 0.45 * np.sin(TWO_PI * t / 5.2 - 1) ** 2
    s = lowpass(noise(dur, seed), 700, 2) * swell
    s += 0.25 * bandpass(noise(dur, seed + 1), 2000, 6000) * swell ** 3
    u = t / dur
    return norm(s * np.minimum(1, u * 10) * np.minimum(1, (1 - u) * 8)) * 0.35


def s_ambience_dawn(dur=20.0, seed=0, **_):
    t = _t(dur)
    breeze = lowpass(noise(dur, seed), 600, 2) * (0.6 + 0.4 * np.sin(TWO_PI * 0.1 * t))
    s = norm(highpass(breeze, 100)) * 0.6
    r = _rng(seed + 3)
    for k in range(int(dur * 0.8)):
        st = r.uniform(0.5, dur - 0.5)
        n = r.integers(2, 5)
        base = r.uniform(2800, 4200)
        for j in range(n):
            d = r.uniform(0.05, 0.1)
            tt = _t(d)
            f = base * (1 + 0.25 * np.sin(np.pi * tt / d)) * r.uniform(0.95, 1.05)
            c = np.sin(TWO_PI * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * 0.3
            i = int((st + j * 0.13) * SR)
            s[i:i + len(c)] += c[:len(s) - i]
    u = t / dur
    return norm(s * np.minimum(1, u * 5) * np.minimum(1, (1 - u) * 3)) * 0.35


def s_room_tone(dur=300.0, seed=99, **_):
    """立体声房间底噪（棕噪声低通，非常轻）。"""
    out = []
    for ch in range(2):
        x = lowpass(noise(dur, seed + ch), 260, 2)
        x = highpass(x, 40)
        out.append((norm(x) * 0.5).astype(np.float32))
    return out


ROOM_TONE = 0.018

SOUNDS = {name[2:]: fn for name, fn in globals().items()
          if name.startswith("s_") and callable(fn) and name != "s_room_tone"}

# 默认声像：有些音效自带左右移动
AUTO_PAN = {"whoosh": "sweep", "whoosh_short": "sweep", "swish": "sweep", "zoom_in": "center",
            "fall": "center"}


# ---------------------------------------------------------------- 混音


def _add(bus, start, sig, gain, pan):
    i0 = int(round(start * SR))
    if i0 < 0:
        sig = sig[-i0:]
        i0 = 0
    if i0 >= bus.shape[1] or len(sig) == 0:
        return
    n = min(len(sig), bus.shape[1] - i0)
    s = sig[:n] * gain
    if isinstance(pan, np.ndarray):
        p = pan[:n]
        th = (p + 1) * np.pi / 4
        bus[0, i0:i0 + n] += s * np.cos(th)
        bus[1, i0:i0 + n] += s * np.sin(th)
    else:
        th = (pan + 1) * math.pi / 4
        bus[0, i0:i0 + n] += s * math.cos(th)
        bus[1, i0:i0 + n] += s * math.sin(th)


def _reverb_ir(seconds=1.4, seed=5):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    out = []
    for ch in range(2):
        r = _rng(seed + ch).standard_normal(n) * np.exp(-t * 4.2)
        r = lowpass(r, 4500)
        r[: int(0.012 * SR)] = 0           # 预延迟
        out.append(r / np.sqrt(np.sum(r ** 2)))
    return np.array(out)


def _convolve_ola(x, ir, block=1 << 17):
    """分块重叠相加卷积（内存友好）。"""
    m = len(ir)
    nfft = 1 << int(math.ceil(math.log2(block + m - 1)))
    H = np.fft.rfft(ir, nfft)
    y = np.zeros(len(x) + m - 1)
    for s in range(0, len(x), block):
        seg = x[s:s + block]
        Y = np.fft.irfft(np.fft.rfft(seg, nfft) * H, nfft)[:len(seg) + m - 1]
        y[s:s + len(Y)] += Y
    return y[:len(x)]


def build_audio(path, duration=None, cues=None, verbose=True):
    from .timeline import DURATION, all_sfx
    duration = duration or DURATION
    cues = cues if cues is not None else all_sfx()
    n = int(math.ceil(duration * SR))
    bus = np.zeros((2, n), dtype=np.float32)
    amb = np.zeros((2, n), dtype=np.float32)
    missing = set()
    for k, (t0, name, kw) in enumerate(cues):
        fn = SOUNDS.get(name)
        if fn is None:
            missing.add(name)
            continue
        params = dict(kw)
        gain = params.pop("gain", 0.5)
        pan = params.pop("pan", None)
        params.setdefault("seed", int(t0 * 1000) + k)
        sig = fn(**params)
        if pan is None:
            mode = AUTO_PAN.get(name)
            if mode == "sweep":
                d = 1 if (int(t0 * 10) % 2 == 0) else -1
                pan = np.linspace(-0.55 * d, 0.55 * d, len(sig))
            elif mode == "center":
                pan = 0.0
            else:
                pan = math.sin(t0 * 2.3 + k) * 0.25
        target = amb if name.startswith("ambience") else bus
        _add(target, t0, sig, gain, pan)
    if missing:
        raise KeyError(f"未定义的音效：{sorted(missing)}")
    if verbose:
        print(f"  合成 {len(cues)} 个音效，加混响 …")
    # 极轻的房间底噪，避免"死寂"
    room = s_room_tone(duration)
    amb[0] += room[0][:n] * ROOM_TONE
    amb[1] += room[1][:n] * ROOM_TONE
    ir = _reverb_ir()
    wet = np.stack([_convolve_ola(bus[c].astype(np.float64), ir[c]) for c in range(2)]).astype(np.float32)
    mix = bus * 0.9 + wet * 0.22 + amb
    del wet
    # 总线：边缘淡入淡出 + 软限幅
    t = np.arange(n) / SR
    mix *= np.minimum(1, t / 0.3) * np.clip((duration - t) / 1.2, 0, 1)
    peak = np.max(np.abs(mix))
    drive = 1.6
    mix = mix / max(peak, 1e-9) * drive
    mix = np.tanh(mix) / np.tanh(drive) * 0.9
    pcm = (np.clip(mix, -1, 1).T * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    if verbose:
        rms = 20 * math.log10(max(1e-9, float(np.sqrt(np.mean(mix ** 2)))))
        print(f"  音轨 → {path}（{duration:.1f}s，RMS {rms:.1f} dBFS）")
    return path


if __name__ == "__main__":
    import sys
    build_audio(sys.argv[1] if len(sys.argv) > 1 else "soundtrack.wav")
