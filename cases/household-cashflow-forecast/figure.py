"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/household-cashflow-forecast/figure.py --font /absolute/path/日本語フォント

Python 3 / Pillow。部品は scripts/figkit.py（サービスはロゴの札 fk.service で示す）。
矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow()（1 色）、ラベルは動くデータの名詞。

- 左（同じ AI に同時に入る入力 2 本）：家計簿アプリ（先月の明細）・計画のファイル（これからの出入り）
- 上：本人（計画の直し。会話で伝える）。左の 2 本と並べないよう、Claude Code の真上から入れる
- 中央：Claude Code（目標に届く月を予測）
- 右：画面「家計の見通し」（上に 3 つの切り替え「今・この1年・その先」。目標額の線に向かって上がる月末の線と届く月の丸。
  下に費目ごとの実際と予算の棒。予算を超えた費目だけ色を変える。2026-11-10 の組み直しに合わせた）
家計簿アプリは特定のサービスを指さない絵にした（明細の一覧）。金額・費目の名前は描かない。
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
CX, CY, TILE = 740, 470, 140         # Claude Code の札
HALF = TILE / 2
L, R, T = CX - HALF, CX + HALF, CY - HALF
GAP = 4
SX = 150                             # 左の列（読まれる側）の中心
BEND = 560                           # 左の入力が Claude Code へ曲がる位置
YA, YP = 340, 600                    # 行：家計簿アプリ・計画


def ledger(cx, cy, w=150, h=150):
    """家計簿アプリの明細の一覧：日付の点・内容の線・金額の棒が 4 行。右の辺の x を返す。"""
    x0, y0 = cx - w / 2, cy - h / 2
    fk.rr((x0, y0, x0 + w, y0 + h), 'white', fk.BLUE, 3, 14)
    d.rounded_rectangle((x0 + 2, y0 + 2, x0 + w - 2, y0 + 28), radius=12, fill='#e7eef6')
    for k in range(4):
        ry = y0 + 44 + k * 26
        d.ellipse((x0 + 14, ry, x0 + 26, ry + 12), fill=fk.BLUE)
        d.line((x0 + 36, ry + 6, x0 + 80, ry + 6), fill=fk.LINE, width=6)
        d.rounded_rectangle((x0 + w - 16 - (40, 26, 48, 32)[k], ry, x0 + w - 16, ry + 12), radius=5, fill=fk.AMBER)
    fk.centered(cx, y0 + h + 12, '家計簿アプリ', 25)
    return x0 + w


def outlook_screen(x0, y0, x1, y1):
    """画面「家計の見通し」：3 つの切り替え、目標額の線へ上がる月末の線と届く月の丸、費目ごとの実際と予算の棒。下に名前。"""
    fk.rr((x0, y0, x1, y1), 'white', fk.TEAL, 3, 14)
    # 切り替え（今・この1年・その先）。開いているのは「今」
    tabs = ['今', 'この1年', 'その先']
    tw = (x1 - x0 - 40) / 3
    for k, name in enumerate(tabs):
        tx0 = x0 + 20 + k * tw
        on = k == 0
        fk.rr((tx0 + 4, y0 + 16, tx0 + tw - 4, y0 + 54), fk.TEAL if on else '#f4f7f6', fk.TEAL if on else fk.LINE, 2, 10)
        fk.centered(tx0 + tw / 2, y0 + 20, name, 21, 'white' if on else fk.GRAY)
    # 月末の線：賞与の月に段が付きながら上がり、目標額の線（点線）に届く月に丸
    gx0, gx1, base, top = x0 + 34, x1 - 34, y0 + 196, y0 + 82
    fk.rr((x0 + 20, y0 + 68, x1 - 20, y0 + 210), '#f4f7f6', fk.LINE, 2, 10)
    goal = top + 22
    x = gx0
    while x < gx1:
        d.line((x, goal, min(x + 12, gx1), goal), fill=fk.AMBER, width=3)
        x += 20
    levels = [.10, .18, .16, .34, .42, .40, .50, .70, .78, .86, .92]
    span = base - goal
    pts = [(gx0 + k * (gx1 - gx0) / (len(levels) - 1), base - lv / .78 * span) for k, lv in enumerate(levels)]
    d.line(pts, fill=fk.BLUE, width=4, joint='curve')
    hx, hy = pts[8]
    d.ellipse((hx - 11, hy - 11, hx + 11, hy + 11), fill=fk.NOTE, outline=fk.AMBER, width=4)
    # 費目ごとの実際と予算：灰色の枠が予算、中の棒が実際。超えた費目は色を変える
    for k, (act, over) in enumerate(((.62, False), (1.18, True), (.84, False))):
        ry = y0 + 232 + k * 40
        bx0, bw = x0 + 70, x1 - x0 - 150
        d.ellipse((x0 + 34, ry + 4, x0 + 54, ry + 24), fill='#e7eef6', outline=fk.BLUE, width=2)
        fk.rr((bx0, ry, bx0 + bw, ry + 28), '#f4f7f6', fk.LINE, 2, 8)
        d.rounded_rectangle((bx0 + 3, ry + 3, bx0 + bw * act - 3, ry + 25), radius=6, fill=fk.AMBER if over else fk.TEAL)
    fk.centered((x0 + x1) / 2, y1 + 12, '家計の見通し', 25)


# ── 左：読まれる側（2 本）──────────────────────────────
A_R = ledger(SX, YA)
fk.flow([(A_R + 6, YA), (BEND, YA), (BEND, CY - 36), (L - GAP, CY - 36)], '先月の明細',
        at=((A_R + BEND) / 2, YA - LS - 14), size=LS)

DW, DH = 124, 140
fk.doc(SX - DW / 2, YP - DH / 2, DW, DH)
fk.centered(SX, YP + DH / 2 + 12, '計画', 25)
P_R = SX + DW / 2
fk.flow([(P_R + 6, YP), (BEND, YP), (BEND, CY + 36), (L - GAP, CY + 36)], 'これからの出入り',
        at=((P_R + BEND) / 2, YP - LS - 14), size=LS)

# ── 上：本人（計画の直し）→ Claude Code の真上から ──────────────
PY, PS = 120, .6
fk.person(CX, PY, PS)
fk.centered(CX, PY + 118 * PS + 8, '本人', 25)
DOWN0 = PY + 118 * PS + 52
fk.flow([(CX, DOWN0), (CX, T - GAP)])
fk.text(CX + 16, (DOWN0 + T) / 2 - LS / 2 - 4, '計画の直し', LS, fk.TEAL)

# ── 中央：Claude Code ──────────────────────────────────
fk.service('claude', CX, CY, 'Claude Code', tile=TILE)
fk.verb(CX, CY + HALF + 12 + 36, '目標に届く月を予測')

# ── 右：画面「家計の見通し」──────────────────────────────
SX0, SY0, SX1, SY1 = 1020, CY - 186, 1388, CY + 186
fk.flow([(R + 6, CY), (SX0 - GAP, CY)], '届く月・見直す所', size=LS)
outlook_screen(SX0, SY0, SX1, SY1)

fk.save(HERE / 'cover.png')
