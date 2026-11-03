"""造型常量（按 assets/image.jpg 的比例矢量重绘）。

坐标约定：原点 (0, 0) 是脚底中心（地面），y 向下为正。s=1 时身体宽 300、总高约 250。
"""
BW, BH = 300, 196            # 身体宽、高
LEG_H = 50                   # 腿长（身体底边到地面）
TOP = -(LEG_H + BH)          # 身体顶边 y = -246
EYE_X = 90                   # 眼睛到中线的距离
EYE_Y = TOP + 70             # 眼睛中心 y
BROW_Y = TOP + 20            # 眉毛 y
MOUTH_Y = TOP + 120          # 嘴巴 y
BLUSH_Y = TOP + 114          # 腮红 y
LEGS_X = (-117, -67, 63, 113)
ARM_Y = TOP + 120            # 侧臂根部 y
HEAD_TOP = TOP - 6           # 头顶（放帽子 / 气泡用）

# 配色
C_BODY_T = "#EE9669"
C_BODY_M = "#DE7C56"
C_BODY_B = "#C6664A"
C_RIM = "#FBE9BB"
C_LEG = "#A85B40"
C_LEG_D = "#6E3828"
C_LEG_L = "#F3C9A0"
C_EYE = "#24130E"
C_BROW = "#6B4436"
C_BLUSH = "#F8A396"
C_MOUTH = "#561918"
C_TONGUE = "#EF7E84"
C_TEETH = "#FFF8F0"
C_HL = "#FFF1DB"
C_OUT = "#8A452F"
C_TEAR = "#8FD3FF"

BLEND = 0.26                 # 表情过渡时长（秒）
