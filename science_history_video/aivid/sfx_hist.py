"""历史题材的音效与环境声（全部用 numpy 合成；没有任何旋律性的背景音乐）。

由 audio.py 在建立音效表之前导入，函数名 s_xxx 即音效名 xxx；ambience_ 开头的进入环境声总线。
"""
import math

import numpy as np

from .audio import (SR, TWO_PI, _rng, _t, bandpass, bell, env_ad, fade_edges, highpass, lowpass, noise, norm,
                    sweep_noise, tone)


def _fade(x, fin, fout):
    n = len(x)
    a, b = min(n, int(fin * SR)), min(n, int(fout * SR))
    if a > 1:
        x[:a] *= np.linspace(0, 1, a) ** 1.5
    if b > 1:
        x[-b:] *= np.linspace(1, 0, b) ** 1.5
    return x


def _place(out, sig, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= len(out) or i < 0:
        return
    n = min(len(sig), len(out) - i)
    out[i:i + n] += sig[:n] * gain


# ---------------------------------------------------------------- 石器 / 火


def s_knap(pitch=1.0, seed=0, **_):
    """打制石器：清脆的石头撞击 + 碎屑。"""
    d = 0.35
    t = _t(d)
    r = _rng(seed)
    s = bandpass(noise(d, seed), 1800 * pitch, 7000) * env_ad(len(t), 0.0005, 70)
    for f in (2300, 3700, 5200):
        s += 0.35 * np.sin(TWO_PI * f * pitch * r.uniform(0.95, 1.05) * t) * env_ad(len(t), 0.0003, 45)
    s += 0.6 * lowpass(noise(d, seed + 1), 300) * env_ad(len(t), 0.001, 30)
    for k in range(5):
        _place(s, bandpass(noise(0.03, seed + 9 + k), 3000, 9000) * env_ad(int(0.03 * SR), 0.0005, 120),
               r.uniform(0.04, 0.22), 0.25)
    return norm(fade_edges(s, 0.0003, 0.02))


def s_flint(seed=0, **_):
    """燧石打火：金属感的擦击 + 一串火花噼啪。"""
    d = 0.6
    t = _t(d)
    s = bandpass(noise(d, seed), 3000, 12000) * env_ad(len(t), 0.0004, 40)
    s += 0.4 * np.sin(TWO_PI * 4100 * t) * env_ad(len(t), 0.0003, 60)
    r = _rng(seed + 2)
    for k in range(14):
        c = highpass(noise(0.012, seed + k), 4000) * env_ad(int(0.012 * SR), 0.0002, 300)
        _place(s, c, r.uniform(0.02, 0.5), r.uniform(0.15, 0.5))
    return norm(fade_edges(s, 0.0003, 0.05))


def s_ignite(seed=0, **_):
    """火苗被吹旺：低沉的呼一声 + 噼啪。"""
    d = 1.6
    t = _t(d)
    u = t / d
    s = lowpass(noise(d, seed), 500) * (np.sin(np.clip(u * 1.6, 0, 1) * math.pi / 2) ** 2) * np.exp(-u * 1.5)
    s += 0.5 * bandpass(noise(d, seed + 1), 800, 3000) * np.clip(u * 3, 0, 1) * np.exp(-u * 2)
    r = _rng(seed + 3)
    for k in range(20):
        c = bandpass(noise(0.01, seed + 20 + k), 2000, 9000) * env_ad(int(0.01 * SR), 0.0002, 260)
        _place(s, c, r.uniform(0.3, d - 0.05), r.uniform(0.1, 0.35))
    return norm(_fade(s, 0.01, 0.3))


def s_ambience_fire(dur=10.0, seed=0, **_):
    """篝火：低沉的火焰呼呼声 + 随机噼啪。"""
    t = _t(dur)
    roar = lowpass(noise(dur, seed), 320) * (0.7 + 0.3 * np.sin(TWO_PI * 0.23 * t))
    s = norm(roar) * 0.55
    r = _rng(seed + 1)
    for k in range(int(dur * 9)):
        L = r.uniform(0.004, 0.02)
        c = bandpass(noise(L, seed + 100 + k), r.uniform(1200, 3000), 9000) * env_ad(int(L * SR), 0.0002, r.uniform(150, 400))
        _place(s, c, r.uniform(0, dur - 0.05), r.uniform(0.08, 0.6) ** 2 * 2)
    return norm(_fade(s, 1.0, 1.5)) * 0.4


def s_ambience_wind(dur=10.0, seed=0, **_):
    """旷野的风：慢慢起伏的阵风。"""
    t = _t(dur)
    g = 0.55 + 0.45 * np.sin(TWO_PI * 0.07 * t + 1) * np.sin(TWO_PI * 0.13 * t)
    s = lowpass(noise(dur, seed), 700) * g
    s += 0.35 * bandpass(noise(dur, seed + 1), 900, 2400) * g ** 2
    return norm(_fade(highpass(s, 60), 1.2, 1.5)) * 0.4


def s_ambience_cave(dur=10.0, seed=0, **_):
    """山洞：低沉的空洞感 + 偶尔的滴水。"""
    t = _t(dur)
    s = lowpass(noise(dur, seed), 160) * 0.8
    r = _rng(seed + 4)
    for k in range(int(dur / 1.6)):
        _place(s, s_drip(pitch=r.uniform(0.8, 1.3), seed=seed + k), r.uniform(0.3, dur - 0.5), r.uniform(0.15, 0.4))
    return norm(_fade(s, 1.0, 1.0)) * 0.35


def s_drip(pitch=1.0, seed=0, **_):
    d = 0.25
    t = _t(d)
    f = (900 + 1400 * (1 - np.exp(-t * 60))) * pitch
    s = tone(f, d) * env_ad(len(t), 0.001, 30)
    return norm(fade_edges(s))


def s_carve(dur=0.5, seed=0, **_):
    """在骨头 / 石头上刻划：粗糙的刮擦。"""
    t = _t(dur)
    jit = np.abs(lowpass(noise(dur, seed + 5), 40)) * 3
    s = bandpass(noise(dur, seed), 1500, 6000) * np.clip(jit, 0, 1.5) * np.sin(np.pi * t / dur) ** 0.6
    return norm(fade_edges(s, 0.005, 0.03))


def s_wedge(seed=0, **_):
    """芦苇笔压进湿泥板：闷闷的一下。"""
    d = 0.22
    t = _t(d)
    s = lowpass(noise(d, seed), 900) * env_ad(len(t), 0.002, 28)
    s += 0.5 * np.sin(TWO_PI * 140 * t) * env_ad(len(t), 0.001, 35)
    return norm(fade_edges(s))


def s_ambience_river(dur=10.0, seed=0, **_):
    """河水流淌：宽带水声 + 冒泡。"""
    t = _t(dur)
    s = bandpass(noise(dur, seed), 300, 2500) * (0.8 + 0.2 * np.sin(TWO_PI * 0.3 * t))
    r = _rng(seed + 7)
    for k in range(int(dur * 6)):
        d = r.uniform(0.03, 0.08)
        tt = _t(d)
        f = r.uniform(500, 1500) * (1 + 0.6 * tt / d)
        _place(s, np.sin(TWO_PI * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * 0.3, r.uniform(0, dur - 0.1),
               r.uniform(0.05, 0.25))
    return norm(_fade(s, 1.0, 1.2)) * 0.35


def s_ambience_birds(dur=10.0, seed=0, **_):
    """清晨的鸟鸣（远处、零星）+ 微风。"""
    t = _t(dur)
    s = norm(highpass(lowpass(noise(dur, seed), 600), 80)) * 0.5
    r = _rng(seed + 3)
    for k in range(int(dur * 0.9)):
        st = r.uniform(0.3, dur - 0.6)
        base = r.uniform(2600, 4200)
        for j in range(r.integers(2, 5)):
            d = r.uniform(0.05, 0.11)
            tt = _t(d)
            f = base * (1 + 0.22 * np.sin(np.pi * tt / d)) * r.uniform(0.95, 1.05)
            _place(s, np.sin(TWO_PI * np.cumsum(f) / SR) * np.sin(np.pi * tt / d) * 0.25, st + j * 0.13)
    return norm(_fade(s, 1.0, 1.5)) * 0.32


def s_sand(dur=1.0, seed=0, **_):
    """木棍在沙地上画线。"""
    t = _t(dur)
    s = bandpass(noise(dur, seed), 2500, 9000) * (0.6 + 0.4 * np.abs(lowpass(noise(dur, seed + 1), 20)) * 3)
    s *= np.sin(np.pi * t / dur) ** 0.4
    return norm(fade_edges(s, 0.01, 0.05))


# ---------------------------------------------------------------- 纸 / 书 / 写字


def s_page(seed=0, **_):
    """翻书页：快速的纸张掠过声。"""
    d = 0.42
    s = sweep_noise(d, 1800, 6000, seed, bands=5, width=0.5)
    u = np.linspace(0, 1, len(s))
    s *= np.sin(u * math.pi) ** 1.5 * (1 + 0.5 * np.sin(u * 40))
    return norm(s)


def s_pages_flurry(dur=1.6, seed=0, **_):
    out = np.zeros(int(dur * SR))
    r = _rng(seed)
    for k in range(int(dur * 9)):
        _place(out, s_page(seed=seed + k), r.uniform(0, dur - 0.4), r.uniform(0.3, 0.8))
    return norm(_fade(out, 0.1, 0.3))


def s_quill(dur=1.5, seed=0, **_):
    """羽毛笔书写：一笔一笔的细刮。"""
    out = np.zeros(int(dur * SR))
    r = _rng(seed)
    tt = 0.0
    while tt < dur - 0.2:
        L = r.uniform(0.06, 0.22)
        n = int(L * SR)
        st = bandpass(noise(L, seed + int(tt * 100)), 3500, 10000) * np.sin(np.linspace(0, np.pi, n)) ** 0.5
        _place(out, st, tt, r.uniform(0.4, 1.0))
        tt += L + r.uniform(0.02, 0.12)
    return norm(_fade(out, 0.01, 0.05))


def s_chalk(dur=1.2, seed=0, **_):
    """粉笔在黑板上写字：嗒嗒 + 粗糙的刮擦。"""
    out = np.zeros(int(dur * SR))
    r = _rng(seed)
    tt = 0.0
    while tt < dur - 0.15:
        L = r.uniform(0.05, 0.16)
        n = int(L * SR)
        st = bandpass(noise(L, seed + int(tt * 97)), 1200, 5000) * np.sin(np.linspace(0, np.pi, n)) ** 0.3
        _place(out, st, tt, 0.6)
        tap = lowpass(noise(0.02, seed + 3), 2500) * env_ad(int(0.02 * SR), 0.0003, 200)
        _place(out, tap, tt, 0.8)
        tt += L + r.uniform(0.03, 0.1)
    return norm(_fade(out, 0.005, 0.03))


def s_press(seed=0, **_):
    """木制印刷机：螺杆吱呀 + 沉重的压板声。"""
    d = 1.2
    t = _t(d)
    out = np.zeros(len(t))
    cr = np.zeros(int(0.5 * SR))
    tt = _t(0.5)
    f = 220 + 80 * np.sin(TWO_PI * 3 * tt)
    cr += np.sign(np.sin(TWO_PI * np.cumsum(f) / SR)) * 0.15 * np.sin(np.pi * tt / 0.5)
    cr = bandpass(cr, 300, 2500)
    _place(out, cr, 0.0, 0.6)
    th = lowpass(noise(0.5, seed), 260) * env_ad(int(0.5 * SR), 0.002, 9)
    th += np.sin(TWO_PI * 70 * _t(0.5)) * env_ad(int(0.5 * SR), 0.002, 11)
    _place(out, th, 0.52, 1.0)
    return norm(fade_edges(out, 0.005, 0.05))


# ---------------------------------------------------------------- 钟声 / 时间


def s_bell_toll(pitch=1.0, seed=0, **_):
    """远处的大钟：非谐泛音、长长的余音。"""
    d = 5.0
    t = _t(d)
    f0 = 110 * pitch
    s = np.zeros(len(t))
    for ratio, amp, dec in ((0.5, 0.6, 0.5), (1.0, 1.0, 0.7), (1.19, 0.5, 0.9), (1.5, 0.45, 1.1), (2.0, 0.4, 1.3),
                            (2.51, 0.3, 1.8), (3.0, 0.2, 2.2), (4.07, 0.12, 3.0)):
        s += amp * np.sin(TWO_PI * f0 * ratio * t + ratio) * np.exp(-t * dec)
    s += 0.3 * lowpass(noise(d, seed), 2000) * env_ad(len(t), 0.001, 30)
    return norm(_fade(s, 0.002, 0.8))


def s_ticks(dur=2.0, rate=2.0, seed=0, **_):
    """钟表滴答（rate 每秒次数）。"""
    out = np.zeros(int(dur * SR))
    n = int(dur * rate)
    for k in range(n):
        d = 0.04
        tt = _t(d)
        c = bandpass(noise(d, seed + k), 2500, 8000) * env_ad(len(tt), 0.0003, 150)
        c += 0.5 * np.sin(TWO_PI * (2200 if k % 2 == 0 else 1800) * tt) * env_ad(len(tt), 0.0003, 120)
        _place(out, c, k / rate)
    return norm(out)


def s_rewind(dur=2.5, seed=0, **_):
    """时间倒流：越来越快的滴答 + 倒放的嗖声。"""
    out = np.zeros(int(dur * SR))
    tt = 0.0
    k = 0
    while tt < dur - 0.05:
        rate = 3 + 40 * (tt / dur) ** 1.6
        c = bandpass(noise(0.02, seed + k), 2000, 7000) * env_ad(int(0.02 * SR), 0.0003, 180)
        _place(out, c, tt, 0.5)
        tt += 1 / rate
        k += 1
    w = sweep_noise(dur, 4000, 300, seed + 1, bands=6)
    u = np.linspace(0, 1, len(w))
    out[:len(w)] += norm(w) * (u ** 2) * 0.8
    return norm(_fade(out, 0.05, 0.1))


# ---------------------------------------------------------------- 电影化的冲击 / 起势


def s_boom(seed=0, **_):
    """低频重击：亚低频下坠 + 撞击噪声 + 长尾。"""
    d = 3.0
    t = _t(d)
    f = 58 * np.exp(-t * 0.5) + 30
    s = tone(f, d) * np.exp(-t * 1.4)
    s += 0.5 * lowpass(noise(d, seed), 400) * env_ad(len(t), 0.001, 6)
    s += 0.3 * bandpass(noise(d, seed + 1), 800, 4000) * env_ad(len(t), 0.0005, 25)
    return norm(_fade(s, 0.001, 0.8))


def s_riser(dur=3.0, seed=0, **_):
    """紧张感起势：噪声带由低到高 + 渐强，在结尾突然停止。"""
    s = sweep_noise(dur, 200, 6000, seed, bands=8, curve=lambda u: u ** 1.6)
    u = np.linspace(0, 1, len(s))
    s = s * u ** 2.2
    s += 0.4 * lowpass(noise(dur, seed + 3), 120) * u ** 1.5
    return norm(fade_edges(s, 0.05, 0.02))


def s_heartbeat(n=2, seed=0, **_):
    out = np.zeros(int((n * 0.85 + 0.4) * SR))
    for k in range(n):
        for off, g in ((0.0, 1.0), (0.22, 0.7)):
            d = 0.25
            tt = _t(d)
            th = np.sin(TWO_PI * 52 * tt) * env_ad(len(tt), 0.004, 16)
            _place(out, th, k * 0.85 + off, g)
    return norm(out)


def s_hush(dur=3.0, seed=0, **_):
    """吸气般的空气声（重要时刻前的寂静）。"""
    s = lowpass(noise(dur, seed), 1200)
    u = np.linspace(0, 1, len(s))
    s *= np.sin(u * math.pi) ** 2
    return norm(s)


# ---------------------------------------------------------------- 器械


def s_brass(seed=0, **_):
    """黄铜器械的咔嗒（望远镜调焦、仪器）。"""
    d = 0.3
    t = _t(d)
    s = bandpass(noise(d, seed), 2000, 8000) * env_ad(len(t), 0.0003, 90)
    for f in (1850, 3300, 5100):
        s += 0.3 * np.sin(TWO_PI * f * t) * env_ad(len(t), 0.0003, 22)
    return norm(fade_edges(s))


def s_thump(pitch=1.0, seed=0, **_):
    """软的落地（苹果落到草地上）。"""
    d = 0.35
    t = _t(d)
    s = np.sin(TWO_PI * 95 * pitch * t) * env_ad(len(t), 0.002, 22)
    s += 0.6 * lowpass(noise(d, seed), 700) * env_ad(len(t), 0.001, 30)
    return norm(fade_edges(s))


def s_steam(dur=1.5, seed=0, **_):
    """蒸汽喷出：嘶——"""
    s = highpass(noise(dur, seed), 1500)
    t = _t(dur)
    e = np.minimum(1, t / 0.06) * np.exp(-t * 1.2)
    return norm(_fade(s * e, 0.005, 0.2))


def s_ambience_engine(dur=8.0, rate=1.6, seed=0, **_):
    """蒸汽机：有节奏的活塞 + 低沉的机械轰鸣。"""
    t = _t(dur)
    s = lowpass(noise(dur, seed), 120) * 0.6
    n = int(dur * rate * 2)
    for k in range(n):
        d = 0.22
        tt = _t(d)
        ch = lowpass(noise(d, seed + k), 600 if k % 2 else 450) * env_ad(len(tt), 0.004, 14)
        ch += 0.4 * highpass(noise(d, seed + 50 + k), 2500) * env_ad(len(tt), 0.002, 25)
        _place(s, ch, k / (rate * 2), 1.0 if k % 2 == 0 else 0.7)
    return norm(_fade(s, 0.6, 1.0)) * 0.45


def s_hum(dur=4.0, seed=0, **_):
    """电流嗡嗡声（50 Hz 及谐波）。"""
    t = _t(dur)
    s = sum(a * np.sin(TWO_PI * 50 * h * t) for h, a in ((1, 1.0), (2, 0.6), (3, 0.35), (4, 0.2), (6, 0.1)))
    s *= 0.8 + 0.2 * np.sin(TWO_PI * 0.7 * t)
    s += 0.05 * highpass(noise(dur, seed), 3000)
    return norm(_fade(s, 0.3, 0.5))


def s_crackle(dur=1.0, seed=0, **_):
    """电火花噼啪。"""
    out = np.zeros(int(dur * SR))
    r = _rng(seed)
    for k in range(int(dur * 30)):
        L = r.uniform(0.003, 0.02)
        c = highpass(noise(L, seed + k), 1800) * env_ad(int(L * SR), 0.0001, 200)
        _place(out, c, r.uniform(0, dur - 0.02), r.uniform(0.2, 1.0))
    out += 0.3 * np.sin(TWO_PI * 100 * _t(dur)) * np.exp(-_t(dur) * 3)
    return norm(_fade(out, 0.002, 0.05))


def s_telegraph(dur=2.0, seed=0, **_):
    """电报：嘀嘀嗒嗒的电键声。"""
    out = np.zeros(int(dur * SR))
    r = _rng(seed)
    tt = 0.0
    while tt < dur - 0.3:
        L = 0.06 if r.random() < 0.6 else 0.18
        for edge, g in ((0.0, 1.0), (L, 0.6)):
            c = bandpass(noise(0.015, seed + int(tt * 1000)), 1500, 6000) * env_ad(int(0.015 * SR), 0.0002, 260)
            c += 0.6 * np.sin(TWO_PI * 900 * _t(0.015)) * env_ad(int(0.015 * SR), 0.0002, 200)
            _place(out, c, tt + edge, g)
        tt += L + r.choice([0.07, 0.07, 0.2])
    return norm(out)


def s_geiger(dur=2.0, rate=12.0, seed=0, **_):
    """盖革计数器：随机的咔嗒。"""
    out = np.zeros(int(dur * SR))
    r = _rng(seed)
    tt = r.exponential(1 / rate)
    while tt < dur - 0.01:
        c = highpass(noise(0.004, seed + int(tt * 1e4)), 2000) * env_ad(int(0.004 * SR), 0.0001, 900)
        _place(out, c, tt, r.uniform(0.6, 1.0))
        tt += r.exponential(1 / rate)
    return norm(out)


def s_whine(dur=2.0, seed=0, **_):
    """真空管 / X 光管的高频嗡鸣。"""
    t = _t(dur)
    f = 7200 + 60 * np.sin(TWO_PI * 5 * t)
    s = np.sin(TWO_PI * np.cumsum(f) / SR) * 0.5 + 0.5 * np.sin(TWO_PI * 120 * t)
    return norm(_fade(s, 0.2, 0.4))


def s_rocket(dur=6.0, seed=0, **_):
    """火箭发射：持续的低频轰鸣 + 噼啪的爆裂。"""
    t = _t(dur)
    u = t / dur
    s = lowpass(noise(dur, seed), 180) * 1.0 + 0.5 * bandpass(noise(dur, seed + 1), 200, 900)
    r = _rng(seed + 2)
    for k in range(int(dur * 40)):
        L = r.uniform(0.005, 0.03)
        c = bandpass(noise(L, seed + 10 + k), 600, 4000) * env_ad(int(L * SR), 0.0002, 150)
        _place(s, c, r.uniform(0, dur - 0.05), r.uniform(0.2, 0.7))
    s *= np.minimum(1, u * 4) * np.minimum(1, (1 - u) * 2.5)
    return norm(s)


def s_relays(dur=2.0, seed=0, **_):
    """老式计算机：一片继电器咔嗒声。"""
    out = np.zeros(int(dur * SR))
    r = _rng(seed)
    for k in range(int(dur * 40)):
        c = bandpass(noise(0.01, seed + k), 1500, 7000) * env_ad(int(0.01 * SR), 0.0002, 300)
        _place(out, c, r.uniform(0, dur - 0.02), r.uniform(0.2, 1.0))
    out += 0.15 * s_hum(dur, seed)[:len(out)]
    return norm(_fade(out, 0.05, 0.1))


def s_ambience_data(dur=10.0, seed=0, **_):
    """机房：风扇的低鸣 + 零星的数据声。"""
    t = _t(dur)
    s = lowpass(noise(dur, seed), 400) * 0.6 + 0.25 * bandpass(noise(dur, seed + 1), 2000, 5000)
    s += 0.15 * np.sin(TWO_PI * 120 * t)
    r = _rng(seed + 2)
    for k in range(int(dur * 3)):
        d = 0.03
        _place(s, np.sin(TWO_PI * r.uniform(1500, 3500) * _t(d)) * env_ad(int(d * SR), 0.001, 80) * 0.15,
               r.uniform(0, dur - 0.05))
    return norm(_fade(s, 1.0, 1.0)) * 0.3


def s_ambience_space(dur=10.0, seed=0, **_):
    """太空 / 宇宙：极低的空气感（不是音乐，只是低频的"空"）。"""
    t = _t(dur)
    s = lowpass(noise(dur, seed), 90) * (0.8 + 0.2 * np.sin(TWO_PI * 0.05 * t))
    s += 0.2 * bandpass(noise(dur, seed + 1), 300, 900) * (0.5 + 0.5 * np.sin(TWO_PI * 0.03 * t))
    return norm(_fade(s, 1.5, 2.0)) * 0.35


def s_ambience_room(dur=10.0, seed=0, **_):
    """安静的室内（书房 / 图书馆）：很轻的底噪 + 偶尔的木头吱呀。"""
    t = _t(dur)
    s = lowpass(noise(dur, seed), 300) * 0.5
    r = _rng(seed + 6)
    for k in range(int(dur / 4)):
        d = 0.3
        tt = _t(d)
        f = r.uniform(300, 600) * (1 + 0.3 * np.sin(TWO_PI * 6 * tt))
        cr = bandpass(np.sign(np.sin(TWO_PI * np.cumsum(f) / SR)), 300, 2000) * np.sin(np.pi * tt / d) * 0.08
        _place(s, cr, r.uniform(0.5, dur - 0.5))
    return norm(_fade(s, 1.0, 1.0)) * 0.25


def s_ambience_city(dur=10.0, seed=0, **_):
    """夜晚的工业城市：远处的轰鸣与偶尔的金属声。"""
    t = _t(dur)
    s = lowpass(noise(dur, seed), 250) * 0.7 + 0.2 * bandpass(noise(dur, seed + 1), 500, 1500)
    r = _rng(seed + 9)
    for k in range(int(dur / 2)):
        _place(s, bell(r.uniform(400, 900), 0.8, 6, 2.5, 2.7) * 0.15, r.uniform(0, dur - 1))
    return norm(_fade(s, 1.0, 1.0)) * 0.3


def s_stone_click(pitch=1.0, seed=0, **_):
    """棋子落盘：木头与石头的一声脆响。"""
    d = 0.2
    t = _t(d)
    s = bandpass(noise(d, seed), 1500, 6000) * env_ad(len(t), 0.0003, 90)
    s += 0.6 * np.sin(TWO_PI * 1200 * pitch * t) * env_ad(len(t), 0.0003, 50)
    s += 0.4 * np.sin(TWO_PI * 260 * pitch * t) * env_ad(len(t), 0.001, 35)
    return norm(fade_edges(s))


def s_shutter(seed=0, **_):
    """老相机快门 / 底片曝光。"""
    out = np.zeros(int(0.35 * SR))
    for off, g in ((0.0, 1.0), (0.09, 0.7)):
        c = bandpass(noise(0.03, seed + int(off * 100)), 1000, 6000) * env_ad(int(0.03 * SR), 0.0002, 150)
        _place(out, c, off, g)
    return norm(out)


def s_caravan(dur=8.0, seed=0, **_):
    """驼队：风沙 + 远处零星的驼铃。"""
    t = _t(dur)
    s = norm(lowpass(noise(dur, seed), 500)) * 0.5
    r = _rng(seed + 4)
    for k in range(int(dur * 1.2)):
        f = r.choice([620, 700, 780, 930])
        _place(s, bell(f, 1.0, 5, 1.2, 2.76) * 0.12, r.uniform(0, dur - 1.0))
    return norm(_fade(s, 0.8, 1.2)) * 0.35
