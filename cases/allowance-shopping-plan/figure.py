"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/allowance-shopping-plan/figure.py --font /absolute/path/日本語フォント

Python 3 / Pillow。部品は scripts/figkit.py（サービスはロゴの札 fk.service で示す）。
矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow()、ラベルは動くデータの名詞。
左＝読まれる側（ChatGPT・Notion・Amazon と Keepa）、中央＝Claude Code、右＝書かれる側（計画画面・Notion）。
本人は読み書き両方なので上に置く。棚卸しの結果の Notion への反映は README で動いている仕組みなので実線。
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


def wish_db(x, y, w=200, h=132):
    """画像つきの欲しいものの一覧（Notion のデータベース）。"""
    fk.rr((x, y, x + w, y + h), 'white', fk.INK, 3, 12)
    for k, c in enumerate([fk.AMBER, fk.BLUE, fk.TEAL]):
        ry = y + 14 + k * 38
        fk.rr((x + 16, ry, x + 52, ry + 32), c, c, 1, 6)
        fk.d.ellipse((x + 23, ry + 7, x + 32, ry + 16), fill='white')
        fk.d.line((x + 66, ry + 9, x + w - 24 - (k % 2) * 34, ry + 9), fill=fk.LINE, width=6)
        fk.d.line((x + 66, ry + 24, x + 124, ry + 24), fill=fk.LINE, width=5)


def jar(x, y, level, c):
    """積立の瓶。level は0〜1の貯まり具合（概念のみ）。"""
    w, h = 110, 132
    fk.rr((x + 14, y - 18, x + w - 14, y + 4), c, c, 1, 6)
    fk.rr((x, y, x + w, y + h), 'white', c, 4, 22)
    top = y + h - int((h - 16) * level)
    fk.d.rounded_rectangle((x + 8, top, x + w - 8, y + h - 8), radius=14, fill='#f4e3c4')
    for k in range(3):
        cx = x + 30 + k * 25
        cy = y + h - 24 - (k % 2) * 14
        fk.d.ellipse((cx - 11, cy - 11, cx + 11, cy + 11), fill=fk.AMBER, outline='#8f5a22', width=2)


fk.begin()

CX, CY, HALF = 810, 400, 75          # Claude Code の札
L, R, T, B = CX - HALF, CX + HALF, CY - HALF, CY + HALF
ROW = 380                            # 左の主な流れの高さ

# 左：ChatGPT が調べた商品メモ → Notion（欲しいものの正本）
NLX = 345                            # 左の Notion の中心
fk.service('openai', 90, ROW, 'ChatGPT', tile=110)
fk.flow([(145, ROW), (NLX - 64, ROW)], '商品メモ', at=(202, ROW - 36), size=22)
fk.service('notion', NLX, ROW, 'Notion', tile=120)
wish_db(NLX + 74, ROW - 66, w=155)
fk.flow([(NLX + 229, ROW), (L - 4, ROW)], '欲しいもの一覧', at=(653, ROW - 34), size=20)

# 左下：Amazon の値段の履歴（Keepa）→ Claude Code
fk.rr((300, 560, 600, 710), 'white', fk.BLUE, 3, 18)
fk.service('amazon', 385, 635, 'Amazon', tile=110)
fk.service('keepa', 515, 635, 'Keepa', tile=110)
fk.flow([(600, 635), (690, 635), (690, CY + 45), (L - 4, CY + 45)], '値段の履歴', at=(618, 494), size=22)

# 中央：Claude Code
fk.service('claude', CX, CY, 'Claude Code', tile=150)
fk.centered(CX, B + 48, '計算して画面に', 25)

# 右：計画の画面（積立はひとつ。高すぎる物は保留）
SX0, SY0, SX1, SY1 = 1035, 250, 1385, 560
fk.flow([(R, ROW), (SX0 - 4, ROW)], '買う順と月', at=(948, ROW - 36), size=22)
fk.rr((SX0, SY0, SX1, SY1), 'white', fk.BLUE, 3, 14)
fk.d.rounded_rectangle((SX0 + 2, SY0 + 2, SX1 - 2, SY0 + 34), radius=12, fill='#e7eef6')
jar(1070, 300, .55, fk.TEAL)
fk.centered(1125, 440, '積立', 24)
fk.rr((1245, 312, 1345, 430), 'white', fk.FAINT, 3, 18)
fk.centered(1295, 354, '保留', 26, fk.GRAY)
for k in range(3):
    ry = 484 + k * 26
    fk.d.ellipse((1066, ry - 9, 1084, ry + 9), fill=fk.TEAL)
    fk.d.line((1098, ry, 1345 - k * 40, ry), fill=fk.LINE, width=6)

# 右下：棚卸しの結果を Notion へ（README「Claudeがまとめて Notion に反映する」）
NX, NY = 1210, 720
fk.flow([(R, CY + 40), (960, CY + 40), (960, NY), (NX - 64, NY)], '棚卸しの結果', at=(1045, NY - 36), size=22)
fk.service('notion', NX, NY, 'Notion', tile=120)

# 上：本人。入力は Notion、相談と棚卸しの答えは Claude Code、見るのは計画画面。本人にかかわる線は琥珀色にそろえる
PX, PY, PS = CX, 150, .6
fk.person(PX, PY, PS)
fk.centered(PX, PY + 118 * PS + 6, '本人', 24)
SIDE = 185
fk.flow([(PX - 68 * PS - 8, SIDE), (NLX, SIDE), (NLX, ROW - 64)], '欲しいもの', size=22, color=fk.AMBER)
DOWN0 = PY + 118 * PS + 50           # 本人から Claude Code の上辺へ下りる 2 本の始まり（間隔 50px）
fk.flow([(PX - 25, DOWN0), (PX - 25, T - 4)], color=fk.AMBER)
fk.text(PX - 25 - 14 - fk.width('順番の相談', 22), (DOWN0 + T) / 2 - 15, '順番の相談', 22, fk.AMBER)
# README「本人が「いる／いらない」と質問の答えを押すと保存され、Claudeがまとめて Notion に反映する」
fk.flow([(PX + 25, DOWN0), (PX + 25, T - 4)], '棚卸しの答え', size=22, color=fk.AMBER)
fk.flow([(SX0 + 50, SY0 - 4), (SX0 + 50, SIDE), (PX + 68 * PS + 8, SIDE)], '計画画面', size=22, color=fk.AMBER)

fk.save(HERE / 'cover.png')
