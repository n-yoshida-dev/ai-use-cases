"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/allowance-shopping-plan/figure.py --font /absolute/path/日本語フォント

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


def wish_db(x, y, w=240, h=220):
    """画像つきの欲しいものの一覧（Notionのデータベース）。"""
    fk.rr((x, y, x + w, y + h), 'white', fk.INK, 3, 12)
    for k, c in enumerate([fk.AMBER, fk.BLUE, fk.TEAL, fk.AMBER]):
        ry = y + 20 + k * 49
        fk.rr((x + 18, ry, x + 58, ry + 36), c, c, 1, 6)
        fk.d.ellipse((x + 26, ry + 8, x + 36, ry + 18), fill='white')
        fk.d.line((x + 72, ry + 11, x + w - 30 - (k % 2) * 40, ry + 11), fill=fk.LINE, width=6)
        fk.d.line((x + 72, ry + 27, x + 140, ry + 27), fill=fk.LINE, width=5)


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


fk.begin('お小遣いの買い物計画をAIと組む', '欲しいものの入力はNotionのまま → AIが積立を分けた計画を画面にする')

# 左：本人が画像つきで入れる欲しいもの（正本）
wish_db(90, 262)
fk.centered(210, 498, '欲しいもの', 28)
fk.centered(210, 536, 'Notion（正本）', 23, fk.GRAY)

# 中央：Claude Code が読んで計算する
fk.arrow([(345, 352), (585, 352)])
fk.centered(465, 306, 'コネクタで読む', 22, fk.TEAL)
fk.laptop(610, 290)
fk.centered(720, 486, 'Claude Code', 30, fk.TEAL)
fk.centered(720, 526, '読む・計算する', 24, fk.GRAY)
fk.dashed_arrow([(585, 412), (345, 412)], fk.FAINT, 4)
fk.centered(465, 422, '決めたら反映', 22, fk.GRAY)

# 右：計画を見る画面（積立を2つに分ける）
fk.arrow([(860, 365), (945, 365)])
fk.centered(898, 320, '画面を作る', 21, fk.TEAL)
fk.rr((960, 236, 1370, 600), 'white', fk.BLUE, 3, 14)
fk.d.rounded_rectangle((962, 238, 1368, 276), radius=12, fill='#e7eef6')
fk.text(984, 242, '買う順番の計画', 22, fk.BLUE)
jar(1010, 316, .35, fk.TEAL)
fk.centered(1065, 458, '高いもの用', 23)
jar(1200, 316, .7, fk.BLUE)
fk.centered(1255, 458, '普段のもの用', 23)
for k in range(3):
    ry = 506 + k * 30
    fk.d.ellipse((1000, ry - 10, 1020, ry + 10), fill=fk.TEAL)
    fk.d.line((1034, ry, 1300 - k * 40, ry), fill=fk.LINE, width=6)
fk.centered(1165, 614, '計画の画面', 27, fk.BLUE)
fk.centered(1165, 652, 'アーティファクト', 21, fk.GRAY)

# 下：本人。入力は Notion、見るのは画面だけ、相談は隣のチャット
fk.person(720, 690, .6)
fk.centered(720, 770, '本人が決める', 24)
fk.arrow([(645, 700), (210, 700), (210, 575)], fk.AMBER, 5)
fk.centered(425, 660, '画像つきで入力', 22, fk.AMBER)
fk.arrow([(795, 700), (1000, 700), (1000, 612)], fk.BLUE, 5)
fk.centered(895, 712, '画面だけ見る', 22, fk.BLUE)
fk.arrow([(720, 626), (720, 566)], fk.AMBER, 5)
fk.text(738, 580, '順番を相談', 22, fk.AMBER)

fk.footer('試作・改善中（2026-10-22開始）／ 初回の画面を作成 ／ 効果は未測定')
fk.save(HERE / 'cover.png')
