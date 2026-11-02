"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/allowance-shopping-plan/figure.py --font /absolute/path/日本語フォント

Python 3 / Pillow。部品は scripts/figkit.py（サービスはロゴの札 fk.service で示す）。
矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow()（1 色）、ラベルは動くデータの名詞。

この図は「値段とセールから買う月を決める」作業だけを描く（2026-11-02 の本人の指摘で、作業ごとに図を分けた）。
- 左（同じ AI に同時に入る入力を 3 本まで）：Notion の欲しいもの（点数順の一覧）・Keepa（値段の履歴）・Amazon（セール日程）
- 上：本人（今あるお小遣い。チャットで伝える）。左の 3 本と並べないよう、Claude Code の真上から入れる
- 中央：Claude Code（お小遣いで買う月を決める。買い物の全体像の図と同じ動詞にそろえる）
- 右：計画画面（買う時期のまとまり「今すぐ」「セール」「◯月」に商品が並ぶ）
棚卸しと 5 つの質問で点数をつける作業、Notion への状態の書き戻し、ChatGPT が Notion に登録する流れは別の図に任せる。
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
fk.begin()
d = fk.d

LS = 22
CX, CY, TILE = 770, 470, 140         # Claude Code の札
HALF = TILE / 2
L, R, T = CX - HALF, CX + HALF, CY - HALF
GAP = 4
SX = 130                             # 左の列（読まれる側）の中心
STILE = 112
SH = STILE / 2
BEND = 600                           # 左の入力が Claude Code へ曲がる位置
YN, YK, YA = 280, 470, 660           # 行：Notion・Keepa・Amazon


def scored_list(x0, cy, w=200):
    """Notion の欲しいものの一覧（点数の列で並ぶ）：画像の四角・名前の行・点数の棒（長い順）。右の辺の x を返す。"""
    rows, rh = 3, 40
    h = 34 + rows * rh + 6
    y0 = cy - h / 2
    fk.rr((x0, y0, x0 + w, y0 + h), 'white', fk.INK, 3, 12)
    fk.text(x0 + w - 82, y0 + 4, '点数', 20, fk.AMBER)
    for k in range(rows):
        ry = y0 + 34 + k * rh
        fk.rr((x0 + 14, ry, x0 + 44, ry + 28), '#e7eef6', fk.BLUE, 2, 6)
        d.line((x0 + 56, ry + 14, x0 + 104, ry + 14), fill=fk.LINE, width=6)
        d.rounded_rectangle((x0 + w - 82, ry + 7, x0 + w - 82 + (68, 50, 32)[k], ry + 21), radius=6, fill=fk.AMBER)
    return x0 + w


def plan_screen(x0, y0, x1, y1):
    """計画画面：買う時期のまとまり（今すぐ・セール・◯月）ごとに商品の四角が並ぶ。下に名前。"""
    fk.rr((x0, y0, x1, y1), 'white', fk.TEAL, 3, 14)
    d.rounded_rectangle((x0 + 2, y0 + 2, x1 - 2, y0 + 30), radius=12, fill='#e7eef6')
    cols = ['今すぐ', 'セール', '◯月']
    cw = (x1 - x0 - 32) / 3
    for k, (name, n) in enumerate(zip(cols, (2, 3, 2))):
        cx0 = x0 + 16 + k * cw
        fk.rr((cx0 + 4, y0 + 46, cx0 + cw - 4, y1 - 18), '#f4f7f6', fk.LINE, 2, 10)
        fk.centered(cx0 + cw / 2, y0 + 54, name, 22, fk.TEAL)
        for r in range(n):
            ry = y0 + 96 + r * 48
            fk.rr((cx0 + 18, ry, cx0 + cw - 18, ry + 36), fk.NOTE, fk.AMBER, 2, 7)
    fk.centered((x0 + x1) / 2, y1 + 12, '計画画面', 25)


# ── 左：読まれる側（3 本）──────────────────────────────
fk.service('notion', SX, YN, '欲しいもの', tile=STILE)
N_R = scored_list(SX + SH + 12, YN)
fk.flow([(N_R + 6, YN), (BEND, YN), (BEND, CY - 44), (L - GAP, CY - 44)], '点数順の欲しい物',
        at=((N_R + BEND) / 2 + 4, YN - LS - 14), size=LS)

fk.service('keepa', SX, YK, 'Keepa', tile=STILE)
fk.flow([(SX + SH + 6, YK), (L - GAP, YK)], '値段の履歴', at=((SX + SH + BEND) / 2, YK - LS - 14), size=LS)

fk.service('amazon', SX, YA, 'Amazon', tile=STILE)
fk.flow([(SX + SH + 6, YA), (BEND, YA), (BEND, CY + 44), (L - GAP, CY + 44)], 'セール日程',
        at=((SX + SH + BEND) / 2, YA - LS - 14), size=LS)

# ── 上：本人（今あるお小遣い）→ Claude Code の真上から ──────────────
PY, PS = 120, .6
fk.person(CX, PY, PS)
fk.centered(CX, PY + 118 * PS + 8, '本人', 25)
DOWN0 = PY + 118 * PS + 52
fk.flow([(CX, DOWN0), (CX, T - GAP)])
fk.text(CX + 16, (DOWN0 + T) / 2 - LS / 2 - 4, '今あるお小遣い', LS, fk.TEAL)

# ── 中央：Claude Code ──────────────────────────────────
fk.service('claude', CX, CY, 'Claude Code', tile=TILE)
fk.verb(CX, CY + HALF + 12 + 36, 'お小遣いで買う月を決める')

# ── 右：計画画面 ──────────────────────────────────────
SX0, SY0, SX1, SY1 = 1032, CY - 140, 1388, CY + 140
fk.flow([(R + 6, CY), (SX0 - GAP, CY)], 'いつ何を買うか', size=LS)
plan_screen(SX0, SY0, SX1, SY1)

fk.save(HERE / 'cover.png')
