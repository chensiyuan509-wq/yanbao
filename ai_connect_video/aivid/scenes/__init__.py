"""场景顺序与转场表。"""
from . import s01_intro, s02_chain, s03_data, s04_nohands, s05_agent, s06_history, s07_products, s08_corpus, s09_license, s10_stack, s11_muse, s12_coop, s13_islands, s14_ending

ORDER = [s01_intro, s02_chain, s03_data, s04_nohands, s05_agent, s06_history, s07_products, s08_corpus, s09_license, s10_stack, s11_muse, s12_coop, s13_islands, s14_ending]

# (种类, 时长, 参数)；第 i 个转场位于 ORDER[i] 与 ORDER[i+1] 之间
TRANSITIONS = [
    ("blob", 1.0, {"x": 960, "y": 640}),
    ("zoom", 0.9, {"x": 1000, "y": 380}),
    ("whip", 0.7, {"dir": -1}),
    ("iris", 0.9, {"x": 860, "y": 700}),
    ("push_up", 0.8, {}),
    ("wipe", 0.9, {"angle": 0.3}),
    ("blob", 1.0, {"x": 960, "y": 560, "color": "#FFB27A"}),
    ("whip", 0.7, {"dir": 1}),
    ("zoom", 0.9, {"x": 1560, "y": 480}),
    ("blinds", 0.9, {"n": 9}),
    ("iris", 0.9, {"x": 960, "y": 470}),
    ("glitch", 0.6, {"seed": 7, "sound": "glitch"}),
    ("flash", 1.0, {"sound": "swell"}),
]
