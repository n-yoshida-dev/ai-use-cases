"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/dev-dashboard-hub/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/dev-dashboard-hub/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスのロゴは scripts/logos/）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
import figkit as fk  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument('--font', required=True, help='Noto Sans JP / Noto Sans CJK JP 等の日本語フォント')
fk.init(parser.parse_args().font)


def card(x, y, w, h, fill_ratio, waiting, c=fk.TEAL):
    """ハブの 1 枚のカード（1 リポジトリ）：題名の線、進捗バー、あなた待ちの件数、CI の印。"""
    fk.rr((x, y, x + w, y + h), 'white', fk.LINE, 2, 10)
    fk.d.line((x + 14, y + 20, x + w * .55, y + 20), fill=fk.LINE, width=6)
    # 進捗バー
    bx0, bx1, by = x + 14, x + w - 14, y + 44
    fk.d.rounded_rectangle((bx0, by, bx1, by + 14), radius=7, fill='#e6ecee')
    fk.d.rounded_rectangle((bx0, by, bx0 + (bx1 - bx0) * fill_ratio, by + 14), radius=7, fill=c)
    # あなた待ちの件数（色は件数の数字にだけ）
    fk.d.ellipse((x + 14, y + h - 44, x + 48, y + h - 10), fill=fk.NOTE, outline=fk.AMBER, width=3)
    fk.centered(x + 31, y + h - 43, str(waiting), 24, fk.AMBER)
    # CI の印（正常は灰色のチェック）
    cx, cy = x + w - 30, y + h - 27
    fk.d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill='#eef1f2')
    fk.d.line([(cx - 7, cy), (cx - 2, cy + 6), (cx + 8, cy - 6)], fill=fk.GRAY, width=4, joint='curve')


def hub(cx, cy, w=180, h=140, c=fk.TEAL):
    """常駐のハブ（Node のプロセス）：箱の中に 2 段のサーバーの板と、点いている印。"""
    fk.rr((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 'white', c, 3, 18)
    for k in range(2):
        sy = cy - 44 + k * 48
        fk.rr((cx - 60, sy, cx + 60, sy + 36), '#eaf3f1', c, 2, 8)
        fk.d.ellipse((cx - 46, sy + 12, cx - 34, sy + 24), fill=c)
        fk.d.line((cx - 22, sy + 18, cx + 44, sy + 18), fill=fk.LINE, width=6)


fk.begin()

# 中心線（ハブ・画面・本人を同じ高さに置き、左の列の上下と釣り合わせる）
CY = 380

# 左上：GitHub（PR・CI）も集める元
fk.service('github', 250, 130, 'GitHub')

# 左：各リポジトリ（TODO・引き継ぎメモ・git）
fk.folder(70, 250, 130, 100, fk.TEAL)
fk.folder(120, 300, 130, 100, fk.BLUE)
fk.folder(170, 350, 130, 100, fk.TEAL)
fk.centered(130, 466, 'リポジトリ', 25)

# 中央：常駐のハブが 30 分ごとに集める
CX = 600
HW, HH = 180, 140
hub(CX, CY, HW, HH)
fk.centered(CX, CY + HH / 2 + 10, '常駐のハブ', 25)
fk.clock(CX, CY - 250, 44, fk.BLUE)
fk.centered(CX, CY - 194, '30分ごと', 24, fk.BLUE)
fk.arrow([(CX, CY - 148), (CX, CY - HH / 2 - 12)], fk.BLUE, 5)
fk.arrow([(312, 395), (CX - HW / 2 - 12, CY + 8)])
fk.centered(405, 350, '集める', 22, fk.TEAL)
fk.arrow([(326, 150), (CX - HW / 2 - 12, CY - 25)])
fk.centered(455, 200, 'CI', 22, fk.GRAY)

# 左下：Claude Code は、リポジトリごとの集計スクリプトと画面を作る（集めるのはハブ）
fk.service('claude', 250, 651, 'Claude Code')
fk.arrow([(250, 651 - 66 - 10), (250, 462)], fk.AMBER, 5)
fk.text(266, 505, '作る', 22, fk.AMBER)

# 右：1 枚の画面（進捗・あなた待ち・CI が並ぶ）
SX, SW, SH = 790, 380, 270
SY = CY - SH / 2
fk.arrow([(CX + HW / 2 + 10, CY), (SX - 14, CY)])
fk.centered((CX + HW / 2 + 10 + SX - 14) / 2, CY - 42, '1枚に', 22, fk.TEAL)
fk.laptop(SX, SY, SW, SH)
fk.d.rectangle((SX + 6, SY + 6, SX + SW - 6, SY + SH - 6), fill='#eaf3f1')
GW, GH, GAP = 160, 100, 18
gx0 = SX + (SW - 2 * GW - GAP) / 2
gy0 = SY + (SH - 2 * GH - GAP) / 2
card(gx0, gy0, GW, GH, .72, 2)
card(gx0 + GW + GAP, gy0, GW, GH, .45, 1, fk.BLUE)
card(gx0, gy0 + GH + GAP, GW, GH, .9, 0, fk.BLUE)
card(gx0 + GW + GAP, gy0 + GH + GAP, GW, GH, .3, 3)
fk.centered(SX + SW / 2, SY + SH + 50, '進捗・あなた待ち・CI', 24, fk.TEAL)

# 右端：本人は見るだけ
PX, PY = 1330, CY + 10
fk.person(PX, PY, .85)
fk.centered(PX, PY + 112, '本人', 24)
fk.arrow([(SX + SW + 40, CY), (PX - 70, CY)], fk.BLUE, 5)
fk.centered((SX + SW + 40 + PX - 70) / 2, CY - 42, '見るだけ', 22, fk.BLUE)

fk.save(HERE / 'cover.png')
