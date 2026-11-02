"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/allowance-shopping-plan/figure.py --font /absolute/path/日本語フォント

Python 3 / Pillow。部品は scripts/figkit.py（サービスはロゴの札 fk.service で示す）。
矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow()（1 色）、ラベルは動くデータの名詞。
この図は Claude Code の部分だけを描く（ChatGPT が Notion に登録する流れは別の図）。
左＝読まれる側（Notion の欲しいもの・Amazon と Keepa の値段とセール日程）、中央＝Claude Code、
右＝書かれる側（計画画面・Notion の状態と棚卸しの結果）。本人は上に 1 回：買った物と今ある分をチャットで渡し、計画画面を見る。
棚卸しの答えは本人が画面のボタンで押し、画面の保存先（db）から Claude Code が読む。画面は読み書き両方の相手なので左上にもう 1 回置く（名前は「棚卸しの画面」。右の大きな枠は「計画画面」）。
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

CX, CY, HALF = 760, 460, 75          # Claude Code の札
L, R, T, B = CX - HALF, CX + HALF, CY - HALF, CY + HALF
GAP = 4                              # 矢じりと札のすき間

# 左上：Notion の欲しいもの（正本）→ Claude Code
ROW = CY - 40
NLX = 150                            # 左の Notion の中心
fk.service('notion', NLX, ROW, 'Notion', tile=120)
wish_db(NLX + 76, ROW - 66, w=155)
fk.flow([(NLX + 231, ROW), (L - GAP, ROW)], '欲しいもの一覧', size=22)

# 左下：Keepa の値段の履歴と Amazon のセール日程 → Claude Code
AY = 640
fk.rr((90, AY - 75, 390, AY + 75), 'white', fk.BLUE, 3, 18)
fk.service('amazon', 175, AY, 'Amazon', tile=110)
fk.service('keepa', 305, AY, 'Keepa', tile=110)
BEND = 610
fk.flow([(390, AY), (BEND, AY), (BEND, CY + 40), (L - GAP, CY + 40)], '値段とセール日程', size=22)

# 中央：Claude Code
fk.service('claude', CX, CY, 'Claude Code', tile=150)
fk.verb(CX, B + 12 + 36, '点数とセールで並べる')

# 右上：計画の画面（積立はひとつ。高すぎる物は保留）
SX0, SY0, SX1, SY1 = 1015, CY - 155, 1365, CY + 155
fk.flow([(R, CY - 40), (SX0 - GAP, CY - 40)], '買う順と月', size=22)
fk.rr((SX0, SY0, SX1, SY1), 'white', fk.BLUE, 3, 14)
fk.d.rounded_rectangle((SX0 + 2, SY0 + 2, SX1 - 2, SY0 + 34), radius=12, fill='#e7eef6')
jar(SX0 + 35, SY0 + 50, .55, fk.TEAL)
fk.centered(SX0 + 90, SY0 + 190, '積立', 24)
fk.rr((SX0 + 210, SY0 + 62, SX0 + 310, SY0 + 180), 'white', fk.FAINT, 3, 18)
fk.centered(SX0 + 260, SY0 + 104, '保留', 26, fk.GRAY)
for k in range(3):
    ry = SY0 + 234 + k * 26
    fk.d.ellipse((SX0 + 31, ry - 9, SX0 + 49, ry + 9), fill=fk.TEAL)
    fk.d.line((SX0 + 63, ry, SX0 + 310 - k * 40, ry), fill=fk.LINE, width=6)
fk.centered((SX0 + SX1) / 2, SY1 + 12, '計画画面', 25)

# 右下：状態と棚卸しの結果を Notion へ書き戻す（README「Claudeがまとめて Notion に反映する」）
NX, NY = 1250, 740                   # 計画画面の名前の下にずらす
fk.flow([(R, CY + 40), (900, CY + 40), (900, NY), (NX - 60 - GAP, NY)], '状態・棚卸しの結果', size=22)
fk.service('notion', NX, NY, 'Notion', tile=120)

# 上：本人（1 回）。買った物と今ある分をチャットで Claude Code へ渡し、計画画面を見る
PX, PY, PS = CX, 140, .6
fk.person(PX, PY, PS)
fk.centered(PX, PY + 118 * PS + 6, '本人', 24)
DOWN0 = PY + 118 * PS + 50
fk.flow([(PX, DOWN0), (PX, T - GAP)])
fk.text(PX + 16, (DOWN0 + T) / 2 - 16, '買った物・今ある分', 22, fk.TEAL)
SIDE = PY + 30
fk.flow([(SX0 + 70, SY0 - 8), (SX0 + 70, SIDE), (PX + 68 * PS + 14, SIDE)], '買う順と月', size=22)

# 左上：計画画面の保存先（棚卸しの答え）。本人がボタンで押し、Claude Code が読む
QX0, QY0, QX1, QY1 = 120, 206, 360, 290   # 下に名前を入れるぶん上へ（Notion の札とあける）
fk.flow([(PX - 68 * PS - 14, SIDE), (QX0 + 120, SIDE), (QX0 + 120, QY0 - GAP)], '棚卸しの答え', size=22)
fk.rr((QX0, QY0, QX1, QY1), 'white', fk.BLUE, 3, 14)
fk.d.rounded_rectangle((QX0 + 2, QY0 + 2, QX1 - 2, QY0 + 26), radius=12, fill='#e7eef6')
for k in range(2):
    ry = QY0 + 44 + k * 26
    fk.d.ellipse((QX0 + 22, ry - 9, QX0 + 40, ry + 9), fill=fk.TEAL)
    fk.d.line((QX0 + 54, ry, QX1 - 70 - k * 30, ry), fill=fk.LINE, width=6)
fk.centered((QX0 + QX1) / 2, QY1 + 4, '棚卸しの画面', 24)   # 計画画面の棚卸しのタブ
QIN = 715                            # Claude Code の上端に入る位置（本人の矢印の左）
fk.flow([(QX1, (QY0 + QY1) / 2 + 10), (QIN, (QY0 + QY1) / 2 + 10), (QIN, T - GAP)], '棚卸しの答え', size=22)

fk.save(HERE / 'cover.png')
