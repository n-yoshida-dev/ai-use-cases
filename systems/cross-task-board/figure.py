"""全体概念図（cover.png）。

再生成（リポジトリの根から）:
    python3 systems/cross-task-board/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
（フォントの道は位置引数でも受け付ける）

矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は flow() の 1 種類。
左＝Claude Code が読む 5 つ、中央＝Claude Code、右＝書く先（ボードと Todoist）。
Todoist は読む相手でも書く相手でもあるので、左と右に 2 回置く。
本人はボードを見て、声で Claude Code に指示するので、AI の札の上に置く。
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


def folder(x, y, w=78, h=62, c=f.TEAL):
    f.rr((x, y, x + w * .5, y + 18), c, c, 1, 5)
    f.rr((x, y + 10, x + w, y + h), 'white', c, 3, 7)
    f.d.line((x + 14, y + 32, x + w - 14, y + 32), fill=f.LINE, width=5)
    f.d.line((x + 14, y + 46, x + w - 28, y + 46), fill=f.LINE, width=5)


def todo_page(x, y, s=68):
    """各リポジトリのTODO.md（チェックボックスのある文書）"""
    f.d.polygon([(x, y), (x + s - 16, y), (x + s, y + 16), (x + s, y + s), (x, y + s)],
                fill='white', outline=f.AMBER)
    f.d.line([(x, y), (x + s - 16, y), (x + s, y + 16), (x + s, y + s), (x, y + s), (x, y)],
             fill=f.AMBER, width=3, joint='curve')
    for k in range(2):
        by = y + 18 + k * 22
        f.d.rectangle((x + 10, by, x + 22, by + 12), outline=f.AMBER, width=3)
        f.d.line((x + 30, by + 6, x + s - 12 - k * 12, by + 6), fill=f.AMBER, width=5)


def bars(x, y, w=78, h=64):
    f.rr((x, y, x + w, y + h), 'white', f.BLUE, 3, 8)
    for k, bh in enumerate([22, 38, 30]):
        f.d.rectangle((x + 14 + k * 20, y + h - 10 - bh, x + 26 + k * 20, y + h - 10),
                      fill=[f.TEAL, f.BLUE, f.AMBER][k])


def board(x, y, w=380, h=290):
    """横断タスクボード：タブ（予定・分野別・開発状況）と、朝・夜の時刻つきの行"""
    f.rr((x, y, x + w, y + h), 'white', f.BLUE, 3, 14)
    for k, name in enumerate(['予定', '分野別', '開発状況']):
        fill = '#e7eef6' if k else f.BLUE
        f.rr((x + 18 + k * 118, y + 16, x + 124 + k * 118, y + 52), fill, f.BLUE, 2, 9)
        f.centered(x + 71 + k * 118, y + 18, name, 20, 'white' if k == 0 else f.BLUE)
    for k, (t, c) in enumerate([('朝', f.TEAL), ('朝', f.TEAL), ('夜', f.BLUE), ('夜', f.BLUE)]):
        ry = y + 76 + k * 52
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
AX, AY, AT = 680, 450, 200
AL, AR, ATOP = AX - AT / 2, AX + AT / 2, AY - AT / 2
f.service('claude', AX, AY, 'Claude Code', tile=AT)
f.verb(AX, AY + AT / 2 + 12 + 36, '集めて時刻で組む')

# 左：Claude Code が読む 5 つ。各行から札の左辺へ 40px 間隔で入る
IX, X0 = 120, 190
rows = [210, 330, 450, 570, 690]
f.service('todoist', IX, rows[0], tile=96)
f.service('googlecalendar', IX, rows[1], tile=96)
folder(IX - 39, rows[2] - 36)
todo_page(IX - 34, rows[3] - 34)
bars(IX - 39, rows[4] - 32)
entry = [AY - 80, AY - 40, AY, AY + 40, AY + 80]
bend = [500, 460, None, 460, 500]
labels = ['タスク', '今日・明日の予定', '計画と引き継ぎ', '人間待ち', '開発状況']
for ry, ey, bx, label in zip(rows, entry, bend, labels):
    if bx is None:
        pts = [(X0, ry), (AL - 4, ry)]
    else:
        pts = [(X0, ry), (bx, ry), (bx, ey), (AL - 4, ey)]
    f.flow(pts, label, at=((X0 + (bx or AL)) / 2, ry - 37))

# 右：横断タスクボード（アーティファクトとデータベース）
BX, BY = 1010, 290
f.centered(BX + 160, BY - 44, '横断タスクボード', 27, f.BLUE)
board(BX, BY)
f.flow([(AR + 4, AY - 50), (BX - 6, AY - 50)], 'タスクと時間枠')

# 右下：Todoist への反映（本人が指示した分）
TX, TY = 1195, 720
f.service('todoist', TX, TY, tile=110)
f.flow([(AR + 4, AY + 30), (890, AY + 30), (890, TY), (TX - 61, TY)], '完了・リスケ')

# 上：本人がボードを見て実行し、声で指示する
PY = 150
f.person(AX, PY, .7)
f.text(AX - 140, PY - 4, '本人', 26)
f.flow([(BX + 340, BY - 6), (BX + 340, PY), (AX + 58, PY)], '時刻つきの予定',
       at=((AX + 58 + BX + 340) / 2, PY - 37))
f.flow([(AX, PY + 96), (AX, ATOP - 6)], '声の指示')

f.save(Path(__file__).with_name('cover.png'))
