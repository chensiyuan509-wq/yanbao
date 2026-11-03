"""场景顺序与转场表。

转场都按电影的方式做：眨眼（第一视角）、强光过曝、形状匹配剪辑、纸面燃烧、书页飞过遮挡、
蒸汽遮挡、电光闪白、虚焦切换——没有 PPT 式的翻页。
"""
from . import (s00_prologue, s01_fire, s02_writing, s03_reason, s04_relay, s05_revolution, s06_industry,
               s07_invisible, s08_compute, s09_epilogue)

ORDER = [s00_prologue, s01_fire, s02_writing, s03_reason, s04_relay, s05_revolution, s06_industry, s07_invisible,
         s08_compute, s09_epilogue]

# (种类, 时长, 参数)；第 i 个转场位于 ORDER[i] 与 ORDER[i+1] 之间（以交界为中心）
TRANSITIONS = [
    ("blink", 1.3, {"sound": "hush", "gain": 0.3}),                                   # 序章 → 火与石：睁眼
    ("flare", 1.4, {"x": 960, "y": 540, "sound": "swell", "gain": 0.35}),             # 巨石阵的日出 → 古地图
    ("match", 1.2, {"a": (960, 540), "b": (960, 540), "ra": 300, "rb": 300,
                    "sound": "whoosh_short", "gain": 0.25}),                            # 节气轮盘 → 沙地上的圆
    ("burn", 1.8, {"seed": 11, "sound": "ignite", "gain": 0.45}),                     # 亚历山大图书馆 → 巴格达
    ("pages", 1.4, {"seed": 5, "sound": "pages_flurry", "gain": 0.5}),                # 印刷的书页 → 哥白尼
    ("smoke", 1.6, {"seed": 3, "sound": "steam", "gain": 0.45}),                      # 牛顿 → 蒸汽机
    ("flash", 1.0, {"sound": "crackle", "gain": 0.4}),                                # 电灯 → X 射线
    ("defocus", 1.6, {"max": 16, "sound": "hush", "gain": 0.3}),                      # 月面 → 分析机
    ("blink", 1.6, {"sound": "hush", "gain": 0.35, "double": False}),                 # Claude 闭眼 → 星图
]
