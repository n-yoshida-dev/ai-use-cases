"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/allowance-shopping-plan/figure.py --font /absolute/path/日本語フォント

Python 3 / Pillow。部品は scripts/figkit.py（サービスはロゴの札 fk.service で示す）。
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


def wish_db(x, y, w=200, h=132):
    """画像つきの欲しいものの一覧（Notion のデータベース）。"""
    fk.rr((x, y, x + w, y + h), 'white', fk.INK, 3, 12)
    for k, c in enumerate([fk.AMBER, fk.BLUE, fk.TEAL]):
        ry = y + 14 + k * 38
        fk.rr((x + 16, ry, x + 52, ry + 32), c, c, 1, 6)
        fk.d.ellipse((x + 23, ry + 7, x + 32, ry + 16), fill='white')
        fk.d.line((x + 66, ry + 9, x + w - 24 - (k % 2) * 34, ry + 9), fill=fk.LINE, width=6)
        fk.d.line((x + 66, ry + 24, x + 124, ry + 24), fill=fk.LINE, width=5)


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


fk.begin()

# 左上：ChatGPT が候補を調べ、Notion の商品メモに書く
fk.service('openai', 210, 150, 'ChatGPT')
fk.arrow([(210, 268), (210, 342)], fk.TEAL, 5)
fk.text(232, 288, '調べてメモ', 22, fk.TEAL)

# 左：欲しいもの（Notion が正本）
fk.service('notion', 210, 420, 'Notion')
wish_db(300, 354)

# 中央：Claude Code が読んで計算し、画面を作る
fk.arrow([(515, 400), (638, 400)])
fk.centered(576, 362, '読む', 22, fk.TEAL)
fk.dashed_arrow([(638, 445), (515, 445)], fk.FAINT, 4)
fk.centered(576, 456, '反映', 22, fk.GRAY)
fk.service('claude', 720, 420, 'Claude Code', tile=150)

# 上：Amazon の値段の履歴（Keepa）を Claude が読む
fk.service('amazon', 660, 150, 'Amazon', tile=118)
fk.service('keepa', 792, 150, 'Keepa', tile=118)
fk.arrow([(660, 215), (660, 338)], fk.BLUE, 5)
fk.arrow([(790, 215), (790, 338)], fk.BLUE, 5)
fk.centered(725, 258, '値段の履歴', 20, fk.BLUE)

# 右：計画の画面（積立はひとつ。高すぎる物は保留）
fk.arrow([(800, 420), (945, 420)])
fk.centered(872, 380, '画面を作る', 22, fk.TEAL)
fk.rr((960, 250, 1370, 610), 'white', fk.BLUE, 3, 14)
fk.d.rounded_rectangle((962, 252, 1368, 290), radius=12, fill='#e7eef6')
fk.text(984, 256, '買う順番の計画', 22, fk.BLUE)
jar(1010, 330, .55, fk.TEAL)
fk.centered(1065, 470, '積立', 24)
fk.rr((1200, 342, 1310, 460), 'white', fk.FAINT, 3, 18)
fk.centered(1255, 384, '保留', 26, fk.GRAY)
for k in range(3):
    ry = 526 + k * 30
    fk.d.ellipse((1000, ry - 10, 1020, ry + 10), fill=fk.TEAL)
    fk.d.line((1034, ry, 1300 - k * 40, ry), fill=fk.LINE, width=6)

# 下：本人。入力は Notion、見るのは画面、相談は Claude
fk.person(720, 700, .6)
fk.centered(720, 782, '本人', 24)
fk.arrow([(645, 710), (210, 710), (210, 545)], fk.AMBER, 5)
fk.centered(430, 672, '画像つきで入力', 22, fk.AMBER)
fk.arrow([(795, 710), (1010, 710), (1010, 625)], fk.BLUE, 5)
fk.centered(900, 720, '見る', 22, fk.BLUE)
fk.arrow([(720, 638), (720, 556)], fk.AMBER, 5)
fk.text(738, 585, '相談', 22, fk.AMBER)

fk.save(HERE / 'cover.png')
