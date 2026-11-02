"""场景注册表与转场表。"""
from .core import H, W, bg_vertical, text
from .scenes_a import s_arrow, s_calendar, s_change, s_opening

try:
    from .scenes_b import s_clocks, s_perceive, s_spacetime
except ImportError:  # 开发过程中的占位
    s_clocks = s_perceive = s_spacetime = None
try:
    from .scenes_c import s_blackhole, s_ending, s_gravity, s_lightclock
except ImportError:
    s_blackhole = s_ending = s_gravity = s_lightclock = None


def _todo(name):
    def f(ctx, T):
        bg_vertical(ctx, "#202030", "#101018")
        text(ctx, f"TODO {name}  T={T:.1f}", W / 2, H / 2, 60, "#ffffff")
    return f


def _s(fn, name):
    return fn or _todo(name)


# (名称, 开始, 结束, 绘制函数)
SCENES = [
    ("opening", 0.0, 12.0, s_opening),
    ("change", 12.0, 30.0, s_change),
    ("calendar", 30.0, 51.0, s_calendar),
    ("arrow", 51.0, 63.0, s_arrow),
    ("clocks", 63.0, 80.0, _s(s_clocks, "clocks")),
    ("perceive", 80.0, 100.0, _s(s_perceive, "perceive")),
    ("spacetime", 100.0, 118.0, _s(s_spacetime, "spacetime")),
    ("lightclock", 118.0, 138.0, _s(s_lightclock, "lightclock")),
    ("gravity", 138.0, 155.0, _s(s_gravity, "gravity")),
    ("blackhole", 155.0, 165.0, _s(s_blackhole, "blackhole")),
    ("ending", 165.0, 180.0, _s(s_ending, "ending")),
]

# (边界时间, 转场类型, 时长)
TRANSITIONS = [
    (12.0, "iris", 1.1),
    (30.0, "wipe", 1.0),
    (51.0, "zoom", 1.0),
    (63.0, "iris", 1.1),
    (80.0, "push", 0.9),
    (100.0, "zoom", 1.0),
    (118.0, "fade", 1.0),
    (138.0, "iris", 1.1),
    (155.0, "zoomin", 1.2),
    (165.0, "flash", 1.2),
]
