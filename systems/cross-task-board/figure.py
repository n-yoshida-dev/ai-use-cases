"""全体概念図（cover.png）。

再生成（リポジトリの根から）:
    python3 systems/cross-task-board/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
（フォントの道は位置引数でも受け付ける）

矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は flow() の 1 種類。
左＝Claude Code が読む 3 つ（Todoist・カレンダー・作業中のリポジトリ）、中央＝Claude Code、
右＝書く先（ボードと Todoist）。並ぶ入力は 3 本まで（計画・進捗・本人待ちはリポジトリ 1 本にまとめる）。
Todoist は読む相手でも書く相手でもあるので、左と右に 2 回置く。
本人はボードを見て、声で Claude Code に指示するので、左の入力とは別の向き（AI の札の上）に置く。
ボードのタブの名前は実際の画面と同じ（スケジュール・目標・日付・確認待ち・開発状況・AIに任せる）。
自動実行はしない（本人の依頼で作る）ので、時計は付けない。
"""
import argparse
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import figkit as f

ap = argparse.ArgumentParser()
ap.add_argument('font_pos', nargs='?')
ap.add_argument('--font')
args = ap.parse_args()
f.init(args.font or args.font_pos)


def folder(x, y, w=100, h=70, c=f.TEAL):
    """作業するフォルダ（リポジトリ）。"""
    f.rr((x, y, x + 44, y + 18), c, c, 1, 6)
    f.rr((x, y + 10, x + w, y + h), 'white', c, 3, 10)
    f.d.line((x + 16, y + 36, x + w - 18, y + 36), fill=f.LINE, width=6)
    f.d.line((x + 16, y + 54, x + w - 40, y + 54), fill=f.LINE, width=6)


def board(x, y, w=380, h=330):
    """横断タスクボード：画面と同じ 6 つのタブ（2026-11-08 に日付、2026-11-10 に目標と確認待ちを足し、
    分野ごとのタブを外した）を画面の並びのまま 3 つずつ 2 段にし、その下に朝・夜の時刻つきの行"""
    f.rr((x, y, x + w, y + h), 'white', f.BLUE, 3, 14)
    rows = [['スケジュール', '目標', '日付'], ['確認待ち', '開発状況', 'AIに任せる']]
    for r, tabs in enumerate(rows):
        ty = y + 16 + r * 40
        tx = x + (w - sum(f.width(n, 16) + 16 for n in tabs) - 6 * (len(tabs) - 1)) / 2  # 左右の余白をそろえる
        for k, name in enumerate(tabs):
            tw = f.width(name, 16) + 16
            on = r == 0 and k == 0
            f.rr((tx, ty, tx + tw, ty + 34), f.BLUE if on else '#e7eef6', f.BLUE, 2, 9)
            f.centered(tx + tw / 2, ty + 4, name, 16, 'white' if on else f.BLUE)
            tx += tw + 6
    for k, (t, c) in enumerate([('朝', f.TEAL), ('朝', f.TEAL), ('夜', f.BLUE), ('夜', f.BLUE)]):
        ry = y + 116 + k * 52
        f.rr((x + 18, ry, x + 100, ry + 36), '#eef3f3', c, 2, 8)
        f.centered(x + 59, ry + 3, t, 20, c)
        f.d.line((x + 118, ry + 18, x + w - 80 - (k % 2) * 60, ry + 18), fill=f.LINE, width=6)
        f.d.rectangle((x + w - 52, ry + 6, x + w - 28, ry + 30), outline=f.TEAL, width=3)
        if k < 2:
            f.d.line([(x + w - 48, ry + 18), (x + w - 41, ry + 25), (x + w - 30, ry + 9)],
                     fill=f.AMBER, width=4, joint='curve')
    f.d.line((x + 18, y + h - 20, x + w - 18, y + h - 20), fill=f.LINE, width=2)


f.begin()

# 中央：PCのClaude Code（本人の依頼で動く。時計は付けない）
AX, AY, AT = 700, 460, 200
AL, AR, ATOP = AX - AT / 2, AX + AT / 2, AY - AT / 2
f.service('claude', AX, AY, 'Claude Code', tile=AT)
f.verb(AX, AY + AT / 2 + 12 + 36, '集めて時刻で組む')

# 左：Claude Code が読む 3 つ。上下の 2 本は x=BEND で折れて札の左辺へ 60px 間隔で入る
IX, X0, BEND = 150, 222, 500
f.service('todoist', IX, 240, 'Todoist', tile=110)
f.flow([(X0, 240), (BEND, 240), (BEND, AY - 60), (AL - 4, AY - 60)], 'タスク',
       at=((X0 + BEND) / 2, 240 - 37))
f.service('googlecalendar', IX, AY, 'カレンダー', tile=110)
f.flow([(X0, AY), (AL - 4, AY)], '今日・明日の予定', at=((X0 + AL) / 2, AY - 37))
RY = 690
folder(IX - 82, RY - 46)
folder(IX - 18, RY - 26, c=f.BLUE)
f.centered(IX, RY + 58, '作業中のリポジトリ', 24)
RX0 = IX + 82 + 12
f.flow([(RX0, RY), (BEND, RY), (BEND, AY + 60), (AL - 4, AY + 60)], '計画・進捗・本人待ち',
       at=((RX0 + BEND) / 2, RY - 37))

# 右：横断タスクボード（アーティファクトとデータベース）
BX, BY, BW = 1000, 300, 380
f.centered(BX + BW / 2, BY - 44, '横断タスクボード', 27, f.BLUE)
board(BX, BY, BW)
f.flow([(AR + 4, AY - 50), (BX - 6, AY - 50)], '時間割・依頼文', at=((AR + BX) / 2 - 14, AY - 50 - 44))

# 右下：Todoist への反映（本人が指示した分）
TX, TY = BX + BW / 2, 770
f.service('todoist', TX, TY, 'Todoist', tile=110)
f.flow([(AR + 4, AY + 30), (870, AY + 30), (870, TY), (TX - 61, TY)], '完了・リスケ')

# 上：本人がボードを見て実行し、声で指示する
PY = 150
f.person(AX, PY, .7)
f.text(AX - 140, PY - 4, '本人', 26)
f.flow([(BX + BW - 40, BY - 6), (BX + BW - 40, PY), (AX + 58, PY)], '時間割・依頼文',
       at=((AX + 58 + BX + BW - 40) / 2, PY - 37))
f.flow([(AX, PY + 96), (AX, ATOP - 6)], '声の指示')

f.save(Path(__file__).with_name('cover.png'))
