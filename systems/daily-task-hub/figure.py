"""全体概念図（daily-task-hub）。音声・手入力・メールを Todoist に集め、
ChatGPT が毎朝整理して、本人が今日のタスクを受け取るまでの流れ。

矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。読まれる側を左、AI を中央、書かれる側を右に置く。
- 本人は入力も受け取りもするので上に 1 回だけ置く。左の辺から音声メモ（頼んだときの ChatGPT へ）と
  手入力のタスク（Todoist の Inbox へ）を出し、右の辺で今日のタスク（右の Todoist から）を受ける
- 頼んだときの ChatGPT（時計なし）：音声メモを読み、音声のタスクを左の Todoist へ書く
- 毎朝の ChatGPT（毎朝6時）：Gmail の新着メールと Inbox の未整理タスクを読み、
  右の Todoist へ整理済みタスク、右の Gmail へ仕分けラベルを書く
- 同じ行き先へは 1 本だけ引く（2026-11-02 の点検で、平行な 2 本は順番が読みにくいと指摘）。メール由来のタスクも
  同じ朝の整理に乗るので「整理済みタスク」1 本にまとめ、内訳はメール仕分けと Todoist 整理の図に任せる
- ブックマークの振り分け（買い物タスクの入口）は、2026-10-30 から定期では回さない休止中なので描かない
  （図には今動いている流れだけを描く）
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
    fk.verb(cx, bottom + 12 + 36, verb)


# ── 列の位置 ──────────────────────────────────────────────
C2 = 230     # 頼んだときの ChatGPT
C3 = 560     # 読まれる側（Inbox の Todoist・Gmail）
C4 = 880     # 毎朝の ChatGPT・本人
C5 = 1210    # 書かれる側（Todoist・Gmail）

# ── 行の位置 ──────────────────────────────────────────────
A = 395      # 毎朝の ChatGPT の中心
M = A - 20   # Todoist の行（頼んだときの ChatGPT → 左の Todoist → 毎朝の ChatGPT → 右の Todoist を 1 本の鎖にする）
GB = 600     # Gmail の行（下）
PS = .7      # 本人の大きさ
PY = 120     # 本人の中心
VY = PY + 44  # 音声メモが本人を出る高さ
HY = PY + 78  # 手入力のタスクが本人を出る高さ
TY = PY + 60  # 今日のタスクが本人に入る高さ

# ── 本人（上に 1 回だけ） ─────────────────────────────────────
fk.person(C4, PY, PS)
fk.centered(C4, PY + 118 * PS + 10, '本人', 25)
pl, pr = C4 - 68 * PS - GAP, C4 + 68 * PS + GAP

# ── 頼んだときの ChatGPT：音声メモを受けて Todoist へ ──────────────────
ai(C2, M, '頼まれて登録')
a2l, a2r, a2t = C2 - AH, C2 + AH, M - AH

fk.flow([(pl, VY), (C2, VY), (C2, a2t - GAP)], '音声メモ', size=LS,
        at=above(C2, pl, VY, head=False))

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

fk.flow([(a1r + GAP, M), (TRl - GAP, M)], '整理済みタスク', size=LS,
        at=above(a1r + GAP, TRl - GAP, M))
J4 = a1r + 50
fk.flow([(a1r + GAP, A + 40), (J4, A + 40), (J4, GB), (TRl - GAP, GB)], '仕分けラベル', size=LS,
        at=above(J4, TRl - GAP, GB))

# ── 本人へ：今日のタスク ─────────────────────────────────────
fk.flow([(C5, M - H - GAP), (C5, TY), (pr, TY)], '今日のタスク', size=LS,
        at=above(pr, C5, TY, head=False))

fk.save(Path(__file__).with_name('cover.png'))
