"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/daily-cross-task-board/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/daily-cross-task-board/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

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


def folder(x, y, w=120, h=84, c=fk.TEAL):
    """作業するフォルダ（リポジトリ）。"""
    fk.rr((x, y, x + 46, y + 18), c, c, 1, 6)
    fk.rr((x, y + 10, x + w, y + h), 'white', c, 3, 10)
    fk.d.line((x + 18, y + 40, x + w - 22, y + 40), fill=fk.LINE, width=6)
    fk.d.line((x + 18, y + 60, x + w - 48, y + 60), fill=fk.LINE, width=6)


def row(x, y, tag, c, line_w, done=False, tag_w=96):
    """ボードの1行。左に札（幅 tag_w）、右にチェック欄。"""
    fk.rr((x, y, x + tag_w, y + 34), '#eef3f8' if c == fk.BLUE else '#eaf3f1', c, 2, 8)
    fk.centered(x + tag_w / 2, y + 2, tag, 20, c)
    fk.d.line((x + tag_w + 20, y + 17, x + tag_w + 20 + line_w, y + 17), fill=fk.LINE, width=7)
    bx = x + 400
    fk.d.rectangle((bx, y + 6, bx + 22, y + 28), outline=c, width=3)
    if done:
        fk.d.line([(bx + 4, y + 16), (bx + 10, y + 23), (bx + 20, y + 9)], fill=fk.AMBER, width=4, joint='curve')


fk.begin()

# 上段：読む先（Todoist・Google カレンダー・各リポジトリ）
fk.service('todoist', 330, 150, 'Todoist')
fk.service('googlecalendar', 510, 150, 'カレンダー')
folder(595, 112, 100, 70)
folder(655, 130, 100, 70, fk.BLUE)
fk.centered(675, 228, 'リポジトリ', 25)

# 中央：Claude Code が読んで組む
CX, CY = 510, 430
fk.service('claude', CX, CY, 'Claude Code', tile=160)
fk.arrow([(345, 262), (CX - 60, CY - 90)])
fk.arrow([(510, 262), (CX, CY - 90)])
fk.arrow([(655, 262), (CX + 60, CY - 90)])
fk.centered(455, 282, '読む', 22, fk.TEAL)

# 右：横断タスクボード（時刻の枠・配分の枠）
fk.arrow([(CX + 90, CY), (795, CY)])
fk.centered(697, CY - 36, '書く', 22, fk.TEAL)
bx0, by0, bx1, by1 = 810, 150, 1376, 540

# 検算：書いたあとにボードから戻って確かめる（件数・時刻の重なり）
fk.checklist(640, 468, 76, 100)
fk.arrow([(bx0, 518), (728, 518)], fk.TEAL, 5)
fk.centered(769, 486, '検算', 20, fk.TEAL)
fk.rr((bx0, by0, bx1, by1), 'white', fk.BLUE, 3, 14)
for k, (name, on) in enumerate([('予定', True), ('AIに任せる', False), ('開発状況', False)]):
    tx = bx0 + 22 + k * 160
    fk.rr((tx, by0 + 18, tx + 148, by0 + 56), fk.BLUE if on else '#eef3f8', fk.BLUE, 2, 9)
    fk.centered(tx + 74, by0 + 22, name, 20, 'white' if on else fk.BLUE)
fk.clock(bx0 + 40, by0 + 108, 18, fk.BLUE)
fk.text(bx0 + 68, by0 + 92, '朝・夜は時刻', 22, fk.BLUE)
row(bx0 + 30, by0 + 128, '5:30', fk.BLUE, 230, True)
row(bx0 + 30, by0 + 170, '20:30', fk.BLUE, 190)
row(bx0 + 30, by0 + 212, '21:45', fk.BLUE, 150)
fk.d.line((bx0 + 24, by0 + 260, bx1 - 24, by0 + 260), fill=fk.LINE, width=2)
fk.text(bx0 + 30, by0 + 270, '日中は配分', 22, fk.TEAL)
row(bx0 + 30, by0 + 306, '声で 2分', fk.TEAL, 200, tag_w=112)
row(bx0 + 30, by0 + 348, 'AIへ 10分', fk.TEAL, 170, tag_w=112)
fk.centered((bx0 + bx1) / 2, by1 + 10, '横断タスクボード', 27, fk.BLUE)

# 左：本人。声で頼み、ボードを見てチェックする
PX, PY = 150, 440
fk.person(PX, PY, .8)
fk.centered(PX, PY + 108, '本人', 24)
fk.arrow([(PX + 65, CY), (CX - 100, CY)], fk.AMBER, 5)
fk.centered((PX + 65 + CX - 100) / 2, CY - 36, '声で頼む', 22, fk.AMBER)
fk.arrow([(1340, by1), (1340, 760), (PX, 760), (PX, PY + 148)], fk.BLUE, 5)
fk.centered(1000, 724, '見てチェック', 22, fk.BLUE)

# 下中央：別のフォルダの会話へ依頼文を渡す
fk.arrow([(CX, CY + 125), (CX, CY + 170)], fk.TEAL, 5)
fk.rr((CX - 80, 608, CX + 80, 666), fk.NOTE, fk.AMBER, 3, 10)
fk.centered(CX, 620, '依頼文', 24, fk.AMBER)
fk.arrow([(CX + 90, 637), (CX + 145, 637)], fk.TEAL, 5)
folder(CX + 160, 600, 100, 70)
folder(CX + 272, 600, 100, 70, fk.BLUE)
fk.centered(CX + 266, 686, '別フォルダへ', 22, fk.GRAY)

fk.save(HERE / 'cover.png')
