"""全体概念図（cover.png）。

再生成（リポジトリの根から）:
    python3 systems/cross-task-board/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
（フォントの道は位置引数でも受け付ける）
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


f.begin()

# 左：入力（読むだけ）。サービスはロゴ、リポジトリ側の物は絵
CX = 150
rows = [(150, 'Todoist'), (290, 'カレンダー'), (430, '各リポジトリ'), (570, '人間待ちのTODO'), (710, 'アプリの開発状況')]
f.service('todoist', CX, rows[0][0], tile=110)
f.service('googlecalendar', CX, rows[1][0], tile=110)
folder(CX - 39, rows[2][0] - 36)
todo_page(CX - 34, rows[3][0] - 34)
bars(CX - 39, rows[4][0] - 32)
for cy, label in rows:
    f.text(240, cy - 17, label, 25)
    f.d.line((458, cy, 484, cy), fill=f.TEAL, width=5)
f.d.line((484, rows[0][0], 484, rows[-1][0]), fill=f.TEAL, width=5)
f.arrow([(484, 430), (570, 430)])
f.centered(527, 390, '読む', 22, f.TEAL)

# 中央：PCのClaude Code
f.service('claude', 660, 430, 'Claude Code', tile=160)

# 右：横断タスクボード（アーティファクト＋データベース）
BY = 275
f.centered(1135, BY - 44, '横断タスクボード', 27, f.BLUE)
f.rr((900, BY, 1370, BY + 314), 'white', f.BLUE, 3, 14)
for k, name in enumerate(['予定', '分野別', '開発状況']):
    fill = '#e7eef6' if k else f.BLUE
    f.rr((920 + k * 130, BY + 16, 1036 + k * 130, BY + 52), fill, f.BLUE, 2, 9)
    f.centered(978 + k * 130, BY + 18, name, 20, 'white' if k == 0 else f.BLUE)
for k, (t, c) in enumerate([('朝', f.TEAL), ('朝', f.TEAL), ('夜', f.BLUE), ('夜', f.BLUE)]):
    ry = BY + 80 + k * 54
    f.rr((920, ry, 1006, ry + 36), '#eef3f3', c, 2, 8)
    f.centered(963, ry + 3, t, 20, c)
    f.d.line((1024, ry + 18, 1290 - (k % 2) * 60, ry + 18), fill=f.LINE, width=6)
    f.d.rectangle((1318, ry + 6, 1342, ry + 30), outline=f.TEAL, width=3)
    if k < 2:
        f.d.line([(1322, ry + 18), (1329, ry + 25), (1340, ry + 9)], fill=f.AMBER, width=4, joint='curve')
f.d.line((920, BY + 294, 1350, BY + 294), fill=f.LINE, width=2)
f.arrow([(752, 430), (885, 430)])
f.centered(818, 390, '書き込む', 22, f.TEAL)

# 下：本人が見て実行し、声で指示する
f.arrow([(1135, BY + 320), (1135, 650)], f.BLUE, 5)
f.person(1135, 712, .55)
f.text(1205, 695, '見て実行する', 25)
f.arrow([(1068, 712), (660, 712), (660, 575)], f.AMBER, 5)
f.centered(860, 722, '声で指示', 22, f.AMBER)

# Todoistへの書き戻しは、本人が指示したときだけ（点線）
f.dashed_arrow([(620, 346), (620, 70), (CX, 70), (CX, 93)], f.FAINT, 4)
f.centered(385, 80, '指示分だけ反映', 21, f.GRAY)

f.save(Path(__file__).with_name('cover.png'))
