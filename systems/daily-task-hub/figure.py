"""全体概念図（daily-task-hub）。ブックマーク・音声・手入力・メールを Todoist に集め、
ChatGPT が毎朝整理して、本人が今日のタスクを受け取るまでの流れ。

矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。読まれる側を左、AI を中央、書かれる側を右に置く。
- 本人は入力も受け取りもするので上に 1 回だけ置く。左の辺から音声メモ（頼んだときの ChatGPT へ）と
  手入力のタスク（Todoist の Inbox へ）を出し、右の辺で今日のタスク（右の Todoist から）を受ける
- 頼んだときの ChatGPT（時計なし）：ブックマークの保存した投稿と音声メモを読み、
  音声のタスクを Inbox（左の Todoist）へ、買い物タスクを別の Todoist（買い物プロジェクト）へ書く。
  買い物の Todoist からは線を出さない（毎朝の整理の対象外）
- 毎朝の ChatGPT（毎朝6時）：Gmail の新着メールと Inbox の未整理タスクを読み、
  右の Todoist へ要対応タスクと整理済みタスク、右の Gmail へ仕分けラベルを書く
- 読み書き両方の相手（Gmail・Todoist）は左右に 2 回置き、左右の Todoist は同じ高さにそろえる

再生成:
    cd <ai-use-cases のルート>
    python3 systems/daily-task-hub/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
（フォントは位置引数でも渡せる: python3 systems/daily-task-hub/figure.py /path/to/font.ttf）
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import figkit as fk

ap = argparse.ArgumentParser()
ap.add_argument('font_pos', nargs='?')
ap.add_argument('--font')
a = ap.parse_args()
fk.init(a.font or a.font_pos)
fk.begin()

T = 84; H = T / 2        # サービスの札
AT = 104; AH = AT / 2    # ChatGPT の札（2 つとも同じ大きさ）
LS = 21                  # 線のラベルの文字の大きさ（全部そろえる）
GAP = 6                  # 札の辺と線の端のすき間


def above(x0, x1, y, head=True):
    """横の区間 x0〜x1（高さ y）の上に置くラベルの位置。区間が矢じりで終わるときは矢じりを除いた部分の中央。"""
    return ((x0 + 4 + x1 - (24 if head else 4)) / 2, y - LS - 14)


def ai(cx, cy, verb):
    bottom = fk.service('openai', cx, cy, 'ChatGPT', tile=AT)
    fk.centered(cx, bottom + 46, verb, 25, fk.TEAL)


# ── 列の位置 ──────────────────────────────────────────────
C1 = 95      # ブックマーク
J1 = 200     # 音声メモが下りる縦の線
C2 = 355     # 頼んだときの ChatGPT
CS = 560     # 買い物の Todoist
C3 = 710     # 読まれる側（Inbox の Todoist・Gmail）
C4 = 990     # 毎朝の ChatGPT・本人
C5 = 1320    # 書かれる側（Todoist・Gmail）

# ── 行の位置 ──────────────────────────────────────────────
A = 395      # 毎朝の ChatGPT の中心
M = A - 20   # 左右の Todoist の行（毎朝の ChatGPT の辺の上寄りに真っすぐ入る・出る）
GB = 600     # Gmail の行（下）
SY = 240     # 買い物の Todoist の行
PS = .7      # 本人の大きさ
PY = 120     # 本人の中心
VY = PY + 44  # 音声メモが本人を出る高さ
HY = PY + 78  # 手入力のタスクが本人を出る高さ
TY = PY + 60  # 今日のタスクが本人に入る高さ

# ── 本人（上に 1 回だけ） ─────────────────────────────────────
fk.person(C4, PY, PS)
fk.centered(C4, PY + 118 * PS + 10, '本人', 25)
pl, pr = C4 - 68 * PS - GAP, C4 + 68 * PS + GAP

# ── 頼んだときの ChatGPT ─────────────────────────────────────
ai(C2, M, '頼まれて登録')
a2l, a2r, a2t = C2 - AH, C2 + AH, M - AH

fk.flow([(pl, VY), (J1, VY), (J1, M - 28), (a2l - GAP, M - 28)], '音声メモ', size=LS,
        at=((J1 + C2) / 2 + 10, VY - LS - 14))

XY = M + 28
fk.service('x', C1, XY, 'ブックマーク', tile=T)
fk.flow([(C1 + H + GAP, XY), (a2l - GAP, XY)], '保存した投稿', size=LS,
        at=((C1 + H + GAP + a2l - GAP - 20) / 2, XY + 10))

fk.service('todoist', CS, SY, 'Todoist', tile=T)
fk.flow([(C2, a2t - GAP), (C2, SY), (CS - H - GAP, SY)], '買い物タスク', size=LS,
        at=above(C2, CS - H - GAP, SY))

# ── 読まれる側：Inbox の Todoist と Gmail ─────────────────────────
fk.service('todoist', C3, M, 'Todoist', tile=T)
fk.flow([(a2r + GAP, M), (C3 - H - GAP, M)], '音声のタスク', size=LS,
        at=above(a2r + GAP, C3 - H - GAP, M))
fk.flow([(pl, HY), (C3, HY), (C3, M - H - GAP)], '手入力のタスク', size=LS,
        at=(C3 + 14 + fk.width('手入力のタスク', LS) / 2, (HY + M - H) / 2 - LS / 2 - 4))

fk.service('gmail', C3, GB, 'Gmail', tile=T)

# ── 毎朝の ChatGPT ───────────────────────────────────────────
ai(C4, A, '仕分けて整理')
a1l, a1r, a1t = C4 - AH, C4 + AH, A - AH
fk.trigger(C4, a1t, '毎朝6時')

fk.flow([(C3 + H + GAP, M), (a1l - GAP, M)], '未整理タスク', size=LS,
        at=above(C3 + H + GAP, a1l - GAP, M))
J3 = a1l - 50
fk.flow([(C3 + H + GAP, GB), (J3, GB), (J3, A + 40), (a1l - GAP, A + 40)], '新着メール', size=LS,
        at=above(C3 + H + GAP, J3, GB, head=False))

# ── 書かれる側：Todoist と Gmail ─────────────────────────────────
TRl = C5 - H
fk.service('todoist', C5, M, 'Todoist', tile=T)
fk.service('gmail', C5, GB, 'Gmail', tile=T)

fk.flow([(a1r + GAP, A - 40), (TRl - GAP, A - 40)], '要対応タスク', size=LS,
        at=above(a1r + GAP, TRl - GAP, A - 40))
J4 = a1r + 43
fk.flow([(a1r + GAP, A), (TRl - GAP, A)], '整理済みタスク', size=LS,
        at=((J4 + 14 + TRl - GAP - 24) / 2, A + 8))
fk.flow([(a1r + GAP, A + 40), (J4, A + 40), (J4, GB), (TRl - GAP, GB)], '仕分けラベル', size=LS,
        at=above(J4, TRl - GAP, GB))

# ── 本人へ：今日のタスク ─────────────────────────────────────
fk.flow([(C5, M - H - GAP), (C5, TY), (pr, TY)], '今日のタスク', size=LS,
        at=above(pr, C5, TY, head=False))

fk.save(Path(__file__).with_name('cover.png'))
