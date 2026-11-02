"""场景顺序与转场表。"""
from . import (s01_intro, s02_paper, s03_gpt, s04_cuda, s05_asic, s06_fab, s07_products, s08_coop,
               s09_capital, s10_flywheel, s11_china, s12_walls, s13_open, s14_work, s15_life, s16_ending)

ORDER = [s01_intro, s02_paper, s03_gpt, s04_cuda, s05_asic, s06_fab, s07_products, s08_coop, s09_capital,
         s10_flywheel, s11_china, s12_walls, s13_open, s14_work, s15_life, s16_ending]

# (种类, 时长, 参数)；第 i 个转场位于 ORDER[i] 与 ORDER[i+1] 之间（以交界为中心）
TRANSITIONS = [
    ("blob", 1.1, {"x": 960, "y": 560}),                      # 片头 → 01 一篇论文（Claude 身体形状开窗）
    ("whip", 0.75, {"dir": -1}),                              # 论文 → GPT（甩镜头去下一站）
    ("iris", 1.0, {"x": 960, "y": 600}),                      # → 02 算力接力
    ("wipe", 0.9, {"angle": 0.3, "edge": "#9FFFF0"}),         # CUDA → ASIC
    ("zoom", 1.0, {"x": 960, "y": 520}),                      # 光网 → 晶圆厂（推进）
    ("blob", 1.1, {"x": 960, "y": 560, "color": "#FFB27A"}),  # → 03 从聊天到智能体
    ("flash", 1.0, {"sound": "swell"}),                       # → 04 为什么是美国
    ("push_up", 0.8, {}),                                     # 竞合 → 耐心资本
    ("whip", 0.75, {"dir": 1}),                               # 资本 → 数据飞轮
    ("dip", 1.4, {"color": "#0B0F1E", "sound": "swell"}),     # → 05 孤岛（情绪转暗）
    ("zoom", 1.0, {"x": 960, "y": 560}),                      # 产品孤岛 → 围墙细节
    ("wipe", 0.9, {"angle": -0.3, "edge": "#FFE2A8"}),        # 围墙 → 付费与开源
    ("blob", 1.1, {"x": 960, "y": 560, "color": "#FFC08A"}),  # → 06 AI 与你
    ("push", 0.85, {"dir": -1}),                              # 工作 → 生活
    ("flash", 1.1, {"sound": "swell"}),                       # → 结语
]
