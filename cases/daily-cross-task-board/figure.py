"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/daily-cross-task-board/figure.py --font /absolute/path/日本語フォント

Python 3 / Pillow。部品は scripts/figkit.py。生成後は欠字・はみ出し・重なりを目視確認する。
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
    """作業するフォルダ（別のリポジトリ）。"""
    fk.rr((x, y, x + 46, y + 18), c, c, 1, 6)
    fk.rr((x, y + 10, x + w, y + h), 'white', c, 3, 10)
    fk.d.line((x + 18, y + 40, x + w - 22, y + 40), fill=fk.LINE, width=6)
    fk.d.line((x + 18, y + 60, x + w - 48, y + 60), fill=fk.LINE, width=6)


def row(x, y, tag, c, line_w, done=False):
    """ボードの1行。左に札、右にチェック欄。"""
    fk.rr((x, y, x + 96, y + 34), '#eef3f8' if c == fk.BLUE else '#eaf3f1', c, 2, 8)
    fk.centered(x + 48, y + 2, tag, 20, c)
    fk.d.line((x + 116, y + 17, x + 116 + line_w, y + 17), fill=fk.LINE, width=7)
    bx = x + 400
    fk.d.rectangle((bx, y + 6, bx + 22, y + 28), outline=c, width=3)
    if done:
        fk.d.line([(bx + 4, y + 16), (bx + 10, y + 23), (bx + 20, y + 9)], fill=fk.AMBER, width=4, joint='curve')


fk.begin('横断タスクボードで今日と明日を組む', 'AIが時刻つきの予定と隙間の配分を書き、本人は見て決める・やる')

# 中央左：Claude Code（PCで読んで組む・検算する）
fk.laptop(330, 270)
fk.centered(440, 466, 'Claude Code', 30, fk.TEAL)
fk.centered(440, 506, '組む・検算する', 23, fk.GRAY)
fk.checklist(588, 238, 84, 96)
fk.centered(630, 340, '件数を検算', 20, fk.TEAL)

# 右：横断タスクボード（データベースつきのページ）
fk.arrow([(600, 380), (790, 380)])
fk.centered(695, 392, '書き込む', 22, fk.TEAL)
bx0, by0, bx1, by1 = 810, 222, 1376, 612
fk.rr((bx0, by0, bx1, by1), 'white', fk.BLUE, 3, 14)
for k, (name, on) in enumerate([('予定', True), ('AIに任せる', False), ('開発状況', False)]):
    tx = bx0 + 22 + k * 160
    fk.rr((tx, by0 + 18, tx + 148, by0 + 56), fk.BLUE if on else '#eef3f8', fk.BLUE, 2, 9)
    fk.centered(tx + 74, by0 + 22, name, 20, 'white' if on else fk.BLUE)
fk.clock(bx0 + 40, by0 + 108, 18, fk.BLUE)
fk.text(bx0 + 68, by0 + 92, '朝・夜は時刻で', 22, fk.BLUE)
row(bx0 + 30, by0 + 128, '5:30', fk.BLUE, 230, True)
row(bx0 + 30, by0 + 170, '20:30', fk.BLUE, 190)
row(bx0 + 30, by0 + 212, '21:45', fk.BLUE, 150)
fk.d.line((bx0 + 24, by0 + 260, bx1 - 24, by0 + 260), fill=fk.LINE, width=2)
fk.text(bx0 + 30, by0 + 270, '平日の日中は配分で上から', 22, fk.TEAL)
row(bx0 + 30, by0 + 306, '声で 2分', fk.TEAL, 200)
row(bx0 + 30, by0 + 348, 'AIへ 10分', fk.TEAL, 170)
fk.centered((bx0 + bx1) / 2, by1 + 10, '横断タスクボード', 27, fk.BLUE)
fk.centered((bx0 + bx1) / 2, by1 + 48, 'アーティファクト＋DB', 21, fk.GRAY)

# 左下：本人。声で頼む・チェックする
fk.person(170, 500, .72)
fk.centered(170, 608, '本人が決める', 24)
fk.arrow([(220, 455), (300, 395)], fk.AMBER, 5)
fk.text(160, 330, '声で頼む', 22, fk.AMBER)
fk.arrow([(1093, 700), (1093, 772), (170, 772), (170, 652)], fk.BLUE, 5)
fk.centered(900, 736, "見てチェック", 22, fk.BLUE)

# 下中央：別のフォルダの会話へ依頼文を渡す
fk.arrow([(440, 545), (440, 590)], fk.TEAL, 5)
fk.rr((360, 598, 520, 656), fk.NOTE, fk.AMBER, 3, 10)
fk.centered(440, 610, '依頼文', 24, fk.AMBER)
fk.arrow([(530, 627), (585, 627)], fk.TEAL, 5)
folder(600, 590, 100, 70)
folder(712, 590, 100, 70, fk.BLUE)
fk.centered(706, 676, '別フォルダの会話', 22, fk.GRAY)

fk.footer('2026-10-21から使用（作業記録は8日分）／ 自動実行はしない ／ 効果は未測定')
fk.save(HERE / 'cover.png')
