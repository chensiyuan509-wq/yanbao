"""Actor：用时间轴写角色动作。所有动作方法都返回 self，可以链式调用。

    a = (Actor(960, 820, 0.7, "sleep", hat="explorer")
         .expr(2.0, "surprised").hop(2.0)            # 2 秒被吵醒，吓得一跳
         .expr(2.6, "happy").wave(2.7, 4.5)           # 开心挥手
         .walk_to(5.0, 7.0, 1300, 820)                # 走过去
         .talk(7.2, 9.0))                             # 说话（口型）
    a.draw(ctx, t)

动作分三类：
1. 关键帧通道（位置、缩放、视线、倾斜、手臂、透明度、坐下……），在给定时间平滑过渡；
2. 阶梯通道（表情、特效、前置手臂姿势、道具、帽子、眼镜、朝向）；
3. 叠加事件（跳、点头、摇头、挥手、欢呼、拍手、打字、说话、发抖、转圈……），
   在求值时叠加到基础姿态上，所以可以同时发生（边走边说、边跳边挥手）。

另有"待机微动"（idle=True）：呼吸、重心轻摆、视线微漂，让角色站着也是活的；
说话时会自动加上轻微的点头节奏和手势。
"""
import math

from .body import draw_mascot
from .const import TOP
from .gfx import TAU, clamp, ease_back, ease_in, ease_io, ease_out, kf, lerp, noise, smooth

KEEP = object()


def _step(lst, t):
    """阶梯取值：返回 (当前值, 自切换以来的时间, 上一个值)。"""
    cur, since, prev = lst[0][1], t - lst[0][0], lst[0][1]
    for i, k in enumerate(lst):
        if t >= k[0]:
            prev = lst[i - 1][1] if i > 0 else k[1]
            cur, since = k[1], t - k[0]
        else:
            break
    return cur, since, prev


def _win(t, t0, t1, fin=0.2, fout=0.2):
    """窗口包络：t0..t1 内为 1，两端平滑。"""
    if t < t0 or t > t1:
        return 0.0
    return smooth(min((t - t0) / max(fin, 1e-3), (t1 - t) / max(fout, 1e-3), 1.0))


class Actor:
    def __init__(self, x, y, s=1.0, expr="neutral", seed=0.0, flip=False, hat=None, glasses=None,
                 idle=True):
        self.pos = [(-99.0, (float(x), float(y)))]
        self.sc = [(-99.0, s)]
        self.ex = [(-99.0, expr)]
        self.lk = [(-99.0, (0.0, 0.0))]
        self.tl = [(-99.0, 0.0)]
        self.al = [(-99.0, 0.0)]
        self.ar = [(-99.0, 0.0)]
        self.el = [(-99.0, 0.0)]
        self.er = [(-99.0, 0.0)]
        self.alpha_k = [(-99.0, 1.0)]
        self.sit_k = [(-99.0, 0.0)]
        self.fx_k = [(-99.0, None)]
        self.front_k = [(-99.0, None)]
        self.prop_k = [(-99.0, (None, "front", 0.0))]
        self.hat_k = [(-99.0, hat)]
        self.gl_k = [(-99.0, glasses)]
        self.flip_k = [(-99.0, flip)]
        self.walks = []           # (t0, t1, stride, run, inplace)
        self.ev = []              # (种类, t0, t1, 参数)
        self.blinks = []
        self.talks = []           # (t0, t1, smile)
        self.talk_fn = None       # 可选：fn(t) -> 0..1，用真实配音包络驱动口型
        self.seed = seed
        self.idle = idle

    # ================================================================ 关键帧通道
    def _add(self, lst, t, v, dur, ease):
        cur = kf(t, lst)
        lst.append((t, cur))
        lst.append((t + max(dur, 1e-3), v, ease))
        lst.sort(key=lambda k: k[0])
        return self

    def place(self, t, x, y):
        """瞬间移到 (x, y)。"""
        self.pos.append((t, (float(x), float(y)), lambda u: 1.0 if u > 0 else 0.0))
        self.pos.sort(key=lambda k: k[0])
        return self

    def move(self, t0, t1, x, y, ease=ease_io):
        """平移（不迈腿，用于漂浮 / 被拖走 / 镜头外进场）。"""
        cur = kf(t0, self.pos)
        self.pos += [(t0, cur), (t1, (float(x), float(y)), ease)]
        self.pos.sort(key=lambda k: k[0])
        return self

    def walk_to(self, t0, t1, x, y, stride=1.0, ease=ease_io):
        """走到 (x, y)：迈腿、上下起伏、身体前倾、视线看向前方。"""
        self.move(t0, t1, x, y, ease)
        self.walks.append((t0, t1, stride, False, False))
        return self

    def run_to(self, t0, t1, x, y):
        """跑到 (x, y)：步幅更大、前倾更多、脚下扬尘。"""
        self.move(t0, t1, x, y, lambda u: u)
        self.walks.append((t0, t1, 1.8, True, False))
        return self

    def march(self, t0, t1, stride=1.0):
        """原地踏步（推东西、等待时用）。"""
        self.walks.append((t0, t1, stride, False, True))
        return self

    def scale(self, t, s, dur=0.6, ease=ease_io):
        return self._add(self.sc, t, s, dur, ease)

    def look(self, t, lx, ly=0.0, dur=0.28):
        """视线（-1..1）。大幅转头时会自动眨一下眼（动画原则：转头眨眼）。"""
        cur = kf(t, self.lk)
        if math.hypot(lx - cur[0], ly - cur[1]) > 0.9:
            self.blinks.append(t + 0.03)
        return self._add(self.lk, t, (lx, ly), dur, ease_io)

    def look_at(self, t, wx, wy, dur=0.28):
        """看向世界坐标 (wx, wy)。"""
        x, y = kf(t, self.pos)
        s = kf(t, self.sc)
        hx, hy = x, y - 175 * s
        return self.look(t, clamp((wx - hx) / 420, -1, 1), clamp((wy - hy) / 300, -1, 1), dur)

    def tilt(self, t, ang, dur=0.4):
        return self._add(self.tl, t, ang, dur, ease_io)

    def arm(self, t, side, ang, dur=0.3, ease=ease_back):
        """侧臂抬起角度（弧度，0 为自然下垂，约 1.3 为高举）。side: 'l' / 'r'。"""
        for sd in ("l", "r") if side == "both" else (side,):
            self._add(self.al if sd == "l" else self.ar, t, ang, dur, ease)
        return self

    def ext(self, t, side, amount, dur=0.4, ease=ease_out):
        """侧臂伸长（像素，正值伸长）。"""
        for sd in ("l", "r") if side == "both" else (side,):
            self._add(self.el if sd == "l" else self.er, t, amount, dur, ease)
        return self

    def point(self, t, side="r", ang=0.35, reach=80, dur=0.35):
        """伸手指向某处。"""
        return self.arm(t, side, ang, dur).ext(t, side, reach, dur)

    def arms_down(self, t, dur=0.35):
        return (self.arm(t, "l", 0.0, dur, ease_io).arm(t, "r", 0.0, dur, ease_io)
                .ext(t, "l", 0, dur).ext(t, "r", 0, dur))

    def fade(self, t, a, dur=0.4):
        return self._add(self.alpha_k, t, a, dur, ease_io)

    def sit(self, t, k=1.0, dur=0.45):
        """坐下（k=1）/ 站起（k=0）。"""
        self._add(self.sit_k, t, k, dur, ease_out if k > 0.5 else ease_back)
        self.ev.append(("land", t + dur * 0.8, t + dur * 0.8 + 0.7, {"amp": 0.08}))
        return self

    def stand(self, t, dur=0.4):
        return self.sit(t, 0.0, dur)

    def pop_in(self, t, dur=0.55, s=None):
        """从无到有弹出来。"""
        target = s if s is not None else kf(t + dur, self.sc)
        self.sc += [(t, 0.001), (t + dur, target, lambda u: ease_back(u, 2.0))]
        self.sc.sort(key=lambda k: k[0])
        return self

    def pop_out(self, t, dur=0.35):
        cur = kf(t, self.sc)
        self.sc += [(t, cur), (t + dur, 0.001, ease_in)]
        self.sc.sort(key=lambda k: k[0])
        return self

    # ================================================================ 阶梯通道
    def expr(self, t, name, fx=KEEP):
        """切换表情（自动平滑过渡）。fx 可同时设定特效（None 为表情默认）。"""
        self.ex.append((t, name))
        self.ex.sort(key=lambda k: k[0])
        if fx is not KEEP:
            self.fx(t, fx)
        return self

    def fx(self, t, names):
        """特效（元组），None 表示用表情自带的默认特效，() 表示不要特效。"""
        self.fx_k.append((t, names))
        self.fx_k.sort(key=lambda k: k[0])
        return self

    def front(self, t, name):
        """前置手臂姿势：think / fists / cover / cross / hold / carry / clap / type /
        point_up / salute / chin；None 收回。"""
        self.front_k.append((t, name))
        self.front_k.sort(key=lambda k: k[0])
        return self

    def hold(self, t, prop, at="front", rot=0.0):
        """拿起道具。at: 'front'（双手捧在身前）/ 'over'（举过头顶）/ 'l' / 'r'（单手）。"""
        self.prop_k.append((t, (prop, at, rot)))
        self.prop_k.sort(key=lambda k: k[0])
        if at == "front":
            self.front(t, "hold")
        elif at == "over":
            self.front(t, "carry")
        return self

    def drop(self, t):
        """放下道具。"""
        cur = _step(self.prop_k, t)[0]
        self.prop_k.append((t, (None, cur[1], 0.0)))
        self.prop_k.sort(key=lambda k: k[0])
        if cur[1] in ("front", "over"):
            self.front(t, None)
        return self

    def hat(self, t, name):
        self.hat_k.append((t, name))
        self.hat_k.sort(key=lambda k: k[0])
        return self

    def glasses(self, t, name):
        self.gl_k.append((t, name))
        self.gl_k.sort(key=lambda k: k[0])
        return self

    def face(self, t, flip, dur=0.3):
        """转向（左右镜像），带"侧身"过渡。"""
        self.flip_k.append((t, flip))
        self.flip_k.sort(key=lambda k: k[0])
        self.ev.append(("turn", t - dur / 2, t + dur / 2, {}))
        return self

    def blink(self, t):
        self.blinks.append(t)
        return self

    # ================================================================ 叠加事件
    def _e(self, kind, t0, t1, **kw):
        self.ev.append((kind, t0, t1, kw))
        return self

    def hop(self, t, height=60, dur=0.48):
        """小跳：预备下蹲 → 腾空拉伸 → 落地挤压回弹。"""
        return self._e("hop", t, t + dur, h=height, d=dur)

    def jump(self, t, height=130, dur=0.75):
        """大跳（双臂上扬）。"""
        self._e("hop", t, t + dur, h=height, d=dur)
        return self._e("arms_up", t - 0.1, t + dur * 0.9, amp=1.1)

    def land(self, t, amp=0.16):
        return self._e("land", t, t + 0.7, amp=amp)

    def wave(self, t0, t1, side="r"):
        return self._e("wave", t0, t1, side=side)

    def cheer(self, t0, t1):
        """欢呼：双臂上下挥 + 小跳。"""
        self._e("cheer", t0, t1)
        n = max(1, int((t1 - t0) / 0.55))
        for i in range(n):
            self.hop(t0 + 0.05 + i * 0.55, 38, 0.42)
        return self

    def clap(self, t0, t1):
        self.front(t0, "clap").front(t1, None)
        return self._e("clap", t0, t1)

    def type(self, t0, t1):
        """敲键盘（前置手臂 + 身体微颤）。"""
        self.front(t0, "type").front(t1, None)
        return self._e("type", t0, t1)

    def talk(self, t0, t1, smile=0.0):
        """说话（口型）。若设置了 talk_fn，则口型跟随真实配音音量。"""
        self.talks.append((t0, t1, smile))
        return self

    def nod(self, t, n=1):
        for i in range(n):
            self._e("nod", t + i * 0.42, t + i * 0.42 + 0.5)
        return self

    def shake_head(self, t0, t1):
        return self._e("shake_head", t0, t1)

    def shake(self, t, dur=0.5, amp=0.05):
        """身体左右晃（受惊 / 被撞）。"""
        return self._e("shake", t, t + dur, amp=amp)

    def shiver(self, t0, t1, amp=1.0):
        """发抖。"""
        return self._e("shiver", t0, t1, amp=amp)

    def strain(self, t0, t1, side="r"):
        """使劲够 / 用力（手臂抖动 + 身体倾斜）。"""
        return self._e("strain", t0, t1, side=side)

    def shrug(self, t, dur=1.1):
        """耸肩摊手。"""
        return self._e("shrug", t, t + dur)

    def bounce(self, t0, t1, amp=0.05, freq=2.4):
        """开心地上下弹（原地）。"""
        return self._e("bounce", t0, t1, amp=amp, freq=freq)

    def dance(self, t0, t1):
        """跳舞：左右摇摆、双臂交替、轻弹，配音符特效。"""
        self.fx(t0, ("music",)).fx(t1, None)
        return self._e("dance", t0, t1)

    def float(self, t0, t1, height=40):
        """漂浮（悬空上下浮动）。"""
        return self._e("float", t0, t1, h=height)

    def spin(self, t, turns=1, dur=0.8):
        """原地转圈（背面不画脸）。"""
        return self._e("spin", t, t + dur, turns=turns)

    def sigh(self, t, dur=1.2):
        """叹气：慢慢瘪下去再恢复，嘴边一团气。"""
        self.fx(t, ("puff",)).fx(t + dur, None)
        return self._e("sigh", t, t + dur)

    def startle(self, t):
        """吓一跳：快速小跳 + 惊吓线。"""
        self.hop(t, 46, 0.36)
        self.fx(t, ("shock",)).fx(t + 0.9, None)
        return self.shake(t + 0.36, 0.4, 0.04)

    def push(self, t0, t1, side="r"):
        """推东西：身体前倾、手臂前伸、原地踏步、用力抖。"""
        sg = 1 if side == "r" else -1
        self.tilt(t0, 0.13 * sg, 0.3).tilt(t1, 0.0, 0.3)
        self.arm(t0, side, 0.12, 0.25).ext(t0, side, 26, 0.25).arm(t1, side, 0.0).ext(t1, side, 0)
        self.march(t0, t1, 0.8)
        return self.strain(t0, t1, side)

    def bonk(self, t, side="r"):
        """撞墙：被弹回 + 晃 + 冒星星。"""
        sg = 1 if side == "r" else -1
        self._e("bonk", t, t + 0.6, sg=sg)
        self.fx(t, ("dizzy",)).fx(t + 1.6, None)
        return self.shake(t + 0.1, 0.6, 0.06)

    def wobble(self, t0, t1, amp=0.05):
        """晕乎乎地左右摇。"""
        return self._e("wobble", t0, t1, amp=amp)

    # ================================================================ 求值
    def _walk_state(self, t, x, y, s):
        walk, stride, run, lean, look_dx = None, 1.0, False, 0.0, 0.0
        for (t0, t1, sd, rn, inplace) in self.walks:
            if t0 <= t <= t1:
                k = _win(t, t0, t1, 0.15, 0.15)
                if inplace:
                    walk = ((t - t0) * 1.6 * sd) % 1.0
                    stride = sd
                    continue
                x0, y0 = kf(t0, self.pos)
                x1, y1 = kf(t1, self.pos)
                dist = math.hypot(x - x0, y - y0)
                walk = (dist / (95.0 * max(s, 0.2) * (1.4 if rn else 1.0))) % 1.0
                stride = sd
                run = rn
                d = 1 if x1 >= x0 else -1
                lean += (0.09 if rn else 0.03) * d * k
                look_dx += 0.55 * d * k
        return walk, stride, run, lean, look_dx

    def _lift(self, t):
        lift, sq = 0.0, 0.0
        for (kind, t0, t1, kw) in self.ev:
            if kind == "hop":
                d, h = kw["d"], kw["h"]
                u = (t - t0) / d
                if -0.3 < u < 0:
                    sq += 0.09 * math.sin((u + 0.3) / 0.3 * math.pi / 2)
                elif 0 <= u <= 1:
                    lift += math.sin(u * math.pi) * h
                    sq += -0.07 * math.sin(u * math.pi) + (0.09 * (1 - u * 4) if u < 0.25 else 0)
                elif 1 < u < 1.9:
                    v = (u - 1) / 0.9
                    sq += 0.12 * math.sin(v * math.pi * 2.2) * math.exp(-v * 3.2)
            elif kind == "float" and t0 - 0.6 <= t <= t1 + 0.6:
                k = _win(t, t0, t1, 0.6, 0.6)
                lift += k * kw["h"] * (0.75 + 0.25 * math.sin((t - t0) * 2.4))
            elif kind == "bounce" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.2, 0.2)
                ph = (t - t0) * kw["freq"]
                lift += k * abs(math.sin(ph * math.pi)) * 14
                sq += k * kw["amp"] * math.cos(ph * TAU)
            elif kind == "dance" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.3, 0.3)
                lift += k * abs(math.sin((t - t0) * 2 * math.pi * 1.0)) * 12
        return lift, sq

    def state(self, t):
        x, y = kf(t, self.pos)
        s = kf(t, self.sc)
        expr, since, prev = _step(self.ex, t)
        lx, ly = kf(t, self.lk)
        tilt = kf(t, self.tl)
        arm_l, arm_r = kf(t, self.al), kf(t, self.ar)
        ext_l, ext_r = kf(t, self.el), kf(t, self.er)
        sit = kf(t, self.sit_k)
        lift, squash = self._lift(t)
        walk, stride, run, lean, look_dx = self._walk_state(t, x, y, s)
        tilt += lean
        lx = clamp(lx + look_dx, -1, 1)
        if walk is not None:
            tilt += math.sin(walk * TAU * 2) * 0.012
        if since < 0.6:                                 # 表情切换时的小弹跳
            squash += 0.05 * math.sin(since * 20) * math.exp(-since * 8)
        spin, flip_now = 0.0, _step(self.flip_k, t)[0]
        clap, brow_lift, fx_extra = 0.0, 0.0, None
        busy = walk is not None or lift > 0.5

        for (kind, t0, t1, kw) in self.ev:
            if not (t0 - 0.3 <= t <= t1 + 1.0):
                continue
            if kind == "land":
                v = (t - t0) / 0.7
                if 0 <= v <= 1:
                    squash += kw["amp"] * math.sin(v * math.pi * 2.4) * math.exp(-v * 3.5)
            elif kind == "wave" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.25, 0.25)
                side = kw["side"]
                if side in ("r", "both"):
                    arm_r = lerp(arm_r, 1.0 + 0.42 * math.sin((t - t0) * 11), k)
                if side in ("l", "both"):
                    arm_l = lerp(arm_l, 1.0 + 0.42 * math.sin((t - t0) * 11 + 1.3), k)
                tilt += 0.03 * math.sin((t - t0) * 5.5) * k
            elif kind == "arms_up" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.15, 0.3)
                arm_l = lerp(arm_l, kw["amp"], k)
                arm_r = lerp(arm_r, kw["amp"], k)
            elif kind == "cheer" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.2, 0.3)
                ph = (t - t0) * 2 * math.pi / 0.55
                arm_l = lerp(arm_l, 1.15 + 0.3 * math.sin(ph), k)
                arm_r = lerp(arm_r, 1.15 + 0.3 * math.sin(ph + 0.4), k)
            elif kind == "clap" and t0 <= t <= t1:
                clap = (t - t0) * 3.2
            elif kind == "type" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.2, 0.2)
                squash += 0.01 * math.sin((t - t0) * 30) * k
            elif kind == "nod":
                u = (t - t0) / 0.5
                if 0 <= u <= 1:
                    squash += 0.06 * math.sin(u * TAU) * (1 - u)
                    ly += 0.35 * math.sin(u * math.pi)
            elif kind == "shake_head" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.15, 0.15)
                lx = clamp(lx + 0.7 * math.sin((t - t0) * 13) * k, -1, 1)
                tilt += 0.025 * math.sin((t - t0) * 13) * k
            elif kind == "shake" and t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                tilt += kw["amp"] * math.sin(u * TAU * 3) * (1 - u)
            elif kind == "shiver" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.15, 0.15) * kw["amp"]
                tilt += 0.018 * math.sin(t * 61) * k
                squash += 0.012 * math.sin(t * 47) * k
            elif kind == "strain" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.3, 0.3)
                q = 0.08 * math.sin((t - t0) * 40) * k
                if kw["side"] in ("r", "both"):
                    arm_r += q
                    ext_r += 6 * math.sin((t - t0) * 33) * k
                if kw["side"] in ("l", "both"):
                    arm_l += q
                    ext_l += 6 * math.sin((t - t0) * 33) * k
                tilt += (0.05 if kw["side"] == "r" else -0.05) * k
            elif kind == "shrug" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.2, 0.35)
                arm_l = lerp(arm_l, 0.75, k)
                arm_r = lerp(arm_r, 0.75, k)
                ext_l += 10 * k
                ext_r += 10 * k
                tilt += 0.05 * k
                squash += 0.03 * k
                brow_lift += 8 * k
            elif kind == "dance" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.3, 0.3)
                ph = (t - t0) * 2 * math.pi * 1.0
                tilt += 0.09 * math.sin(ph) * k
                arm_l = lerp(arm_l, 0.6 + 0.6 * max(0, math.sin(ph)), k)
                arm_r = lerp(arm_r, 0.6 + 0.6 * max(0, -math.sin(ph)), k)
                lx = clamp(lx + 0.4 * math.sin(ph) * k, -1, 1)
            elif kind == "spin" and t0 <= t <= t1:
                u = ease_io((t - t0) / (t1 - t0))
                spin = u * TAU * kw["turns"]
            elif kind == "turn" and t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                spin = (u if u < 0.5 else 1 - u) * math.pi * 0.92
            elif kind == "sigh" and t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                squash += 0.07 * math.sin(u * math.pi)
                ly += 0.4 * math.sin(u * math.pi)
            elif kind == "bonk":
                u = (t - t0) / 0.6
                if 0 <= u <= 1:
                    tilt += -kw["sg"] * 0.22 * math.sin(u * math.pi) * (1 - u)
                    squash += 0.1 * math.sin(u * math.pi * 2) * (1 - u)
            elif kind == "wobble" and t0 <= t <= t1:
                k = _win(t, t0, t1, 0.3, 0.3)
                tilt += kw["amp"] * math.sin((t - t0) * 4.2) * k

        # 说话：口型 + 轻微点头节奏 + 句首扬眉 + 偶尔的手势
        talk, smile = 0.0, 0.0
        for (t0, t1, sm) in self.talks:
            if t0 - 0.05 <= t <= t1 + 0.05:
                k = _win(t, t0, t1, 0.08, 0.1)
                if self.talk_fn is not None:
                    o = self.talk_fn(t)
                else:
                    o = clamp(0.5 + 0.5 * noise(t * 9.0, self.seed + 2) + 0.3 * math.sin(t * 17))
                # 句中停顿时保持"闭着的说话嘴"，避免嘴型在说话 / 表情之间来回跳
                talk = max(talk, max(o, 0.04) * k)
                smile = sm
                squash += 0.012 * o * k
                tilt += 0.012 * noise(t * 1.7, self.seed + 9) * k
                brow_lift += 5 * math.exp(-(t - t0) * 2.5) * k
                if not busy and t1 - t0 > 1.8:
                    g = max(0.0, noise(t * 0.7, self.seed + 13)) * k
                    arm_r += 0.32 * g
                    arm_l += 0.18 * max(0.0, noise(t * 0.6, self.seed + 17)) * k

        # 待机微动：重心轻摆 + 视线微漂
        if self.idle and not busy:
            tilt += 0.010 * math.sin(t * 0.9 + self.seed * 2)
            lx = clamp(lx + 0.10 * noise(t * 0.35, self.seed + 21), -1, 1)
            ly = clamp(ly + 0.07 * noise(t * 0.3, self.seed + 23), -1, 1)

        eye_open = 1.0
        for tb in self.blinks:
            d = t - tb
            if 0 <= d < 0.17:
                eye_open = min(eye_open, 1 - math.sin(math.pi * d / 0.17) * 0.95)

        # 前置手臂姿势：新旧姿势交叉过渡
        fr_cur, fr_since, fr_prev = _step(self.front_k, t)
        front = {}
        if fr_cur:
            front[fr_cur] = clamp(fr_since / 0.22)
        if fr_prev and fr_prev != fr_cur and fr_since < 0.18:
            front[fr_prev] = max(front.get(fr_prev, 0.0), 1 - fr_since / 0.18)
        (prop, at, prot), p_since, p_prev = _step(self.prop_k, t)
        prop_k = clamp(p_since / 0.35) if prop is not None else 0.0
        if prop is None and p_prev and p_prev[0] is not None and p_since < 0.25:
            prop, at, prot = p_prev
            prop_k = 1 - p_since / 0.25

        fx, _, _ = _step(self.fx_k, t)
        hat = _step(self.hat_k, t)[0]
        glasses = _step(self.gl_k, t)[0]
        alpha = kf(t, self.alpha_k)
        return dict(x=x, y=y, s=s, expr=expr, since=since, prev=prev, look=(lx, ly), tilt=tilt,
                    arm_l=arm_l, arm_r=arm_r, ext_l=ext_l, ext_r=ext_r, squash=squash, lift=lift,
                    walk=walk, stride=stride, dust=1.0 if run else 0.0, talk=talk, talk_smile=smile,
                    fx=fx, front=front or None, clap=clap, flip=flip_now, spin=spin, sit=sit,
                    alpha=alpha, eye_open=eye_open, brow_lift=brow_lift, hat=hat, glasses=glasses,
                    prop=prop, prop_at=at, prop_k=prop_k, prop_rot=prot)

    def _hat_motion(self, t, st):
        """帽子的惯性：起跳时被压住，腾空时轻轻飘起，落地时一沉。"""
        if not st["hat"]:
            return 0.0, 0.0
        h = 1 / 30
        l0 = self._lift(t - h)[0]
        l2 = self._lift(t + h)[0]
        acc = (l2 - 2 * st["lift"] + l0) / (h * h)
        dy = clamp(acc * 0.004, -14, 9)
        t0 = kf(t - h, self.tl)
        t2 = kf(t + h, self.tl)
        rot = clamp(-(t2 - t0) / (2 * h) * 0.06, -0.12, 0.12)
        return dy, rot

    def head(self, t):
        """头顶位置（世界坐标），用来放气泡、道具、标签。"""
        st = self.state(t)
        return st["x"], st["y"] - (250 + st["lift"] - 41 * st["sit"]) * st["s"]

    def hand(self, t, side="r"):
        """侧臂手的位置（世界坐标，近似，忽略倾斜）。"""
        from .body import hand_point
        st = self.state(t)
        hx, hy, _ = hand_point(-1 if side == "l" else 1, st["arm_l" if side == "l" else "arm_r"],
                               st["ext_l" if side == "l" else "ext_r"])
        sg = -1 if st["flip"] else 1
        return st["x"] + hx * st["s"] * sg, st["y"] + (hy - st["lift"]) * st["s"]

    def draw(self, ctx, t, **override):
        st = self.state(t)
        st.update(override)
        dy, rot = self._hat_motion(t, st)
        kw = dict(st)
        x, y, s = kw.pop("x"), kw.pop("y"), kw.pop("s")
        draw_mascot(ctx, x, y, s, t=t, seed=self.seed, hat_dy=dy, hat_rot=rot, **kw)
        return st


# 动作清单（给文档 / 导出用）
ACTIONS = {
    "walk_to": "走到某处（迈腿、起伏、前倾、看向前方）",
    "run_to": "跑到某处（大步幅、更前倾、扬尘）",
    "march": "原地踏步",
    "move": "平移（不迈腿）",
    "hop": "小跳（预备—腾空—落地回弹）",
    "jump": "大跳（双臂上扬）",
    "wave": "挥手（左 / 右 / 双手）",
    "cheer": "欢呼（双臂挥动 + 连跳）",
    "clap": "拍手",
    "type": "敲键盘",
    "talk": "说话（口型，可接真实配音包络）",
    "nod": "点头",
    "shake_head": "摇头",
    "shake": "身体晃一下（受惊 / 被撞）",
    "shiver": "发抖",
    "strain": "使劲够 / 用力",
    "shrug": "耸肩摊手",
    "bounce": "原地开心地弹",
    "dance": "跳舞（摇摆 + 音符）",
    "float": "漂浮",
    "spin": "原地转圈",
    "face": "转身（左右朝向）",
    "sigh": "叹气",
    "startle": "吓一跳",
    "push": "推东西",
    "bonk": "撞墙被弹回",
    "wobble": "晕乎乎地摇",
    "sit / stand": "坐下 / 站起",
    "point": "伸手指向",
    "arm / ext": "单独控制手臂角度 / 伸长",
    "look / look_at": "视线（大幅转头自动眨眼）",
    "tilt": "倾斜",
    "hold / drop": "拿起 / 放下道具（身前捧、举过头顶、单手）",
    "front": "前置手臂姿势：think / fists / cover / cross / hold / carry / clap / type / "
             "point_up / salute / chin",
    "hat / glasses": "戴帽子 / 眼镜",
    "pop_in / pop_out": "弹出出现 / 缩小消失",
    "fade / scale": "透明度 / 缩放",
    "expr / fx": "表情 / 特效",
}
