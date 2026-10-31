"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/handoff-and-todo-files/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/handoff-and-todo-files/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

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
parser.add_argument('--out', default=str(HERE / 'cover.png'), help='出力先（既定はこのフォルダの cover.png）')
args = parser.parse_args()
fk.init(args.font)

fk.begin()

# 左：会話の区切りで書く Claude Code
LX, RY = 200, 330
fk.centered(LX, 212, '会話の区切り', 24, fk.GRAY)
fk.service('claude', LX, RY, 'Claude Code', tile=150)

# 右：次の会話で読む Claude Code
RX = 1230
fk.centered(RX, 212, '次の会話', 24, fk.GRAY)
fk.service('claude', RX, RY, 'Claude Code', tile=150)

# 中央：2 つのファイル
DX = 650
fk.centered(DX + 70, 62, 'HANDOFF', 28, fk.BLUE)
fk.centered(DX + 70, 98, '今どこまで', 22, fk.BLUE)
fk.doc(DX, 132, c=fk.BLUE)
fk.centered(DX + 70, 326, 'TODO', 28, fk.AMBER)
fk.centered(DX + 70, 362, '確認待ち（本人）', 22, fk.AMBER)
fk.doc(DX, 398, c=fk.AMBER)

# 書く（左の Claude → 2 つのファイル）
fk.arrow([(LX + 85, 300), (DX - 10, 212)])
fk.centered(455, 222, '書く', 22, fk.TEAL)
fk.arrow([(LX + 85, 360), (DX - 10, 470)])
fk.centered(455, 428, '問いを書く', 22, fk.TEAL)

# 読む（2 つのファイル → 右の Claude）
fk.arrow([(DX + 150, 212), (RX - 85, 300)])
fk.centered(975, 222, '読む', 22, fk.TEAL)
fk.arrow([(DX + 150, 470), (RX - 85, 360)])
fk.centered(960, 366, '読む', 22, fk.TEAL)

# 答えを書く（右の Claude → TODO。本人の答えを本人の言葉で残す）
fk.arrow([(RX - 85, 410), (DX + 152, 530)], fk.AMBER, 5)
fk.centered(1000, 480, '答えを書く', 22, fk.AMBER)

# 右下：本人。Claude が会話で中身を聞き、本人が答える
PX, PY = RX, 700
fk.person(PX, PY, .8)
fk.centered(PX, 806, '本人', 24)
fk.arrow([(PX - 22, RY + 125), (PX - 22, PY - 85)], fk.AMBER, 5)
fk.text(PX - 118, 520, '聞く', 22, fk.AMBER)
fk.arrow([(PX + 22, PY - 85), (PX + 22, RY + 125)], fk.AMBER, 5)
fk.text(PX + 40, 520, '答える', 22, fk.AMBER)

# 左下：点検（古さ・書式）が TODO を見る
fk.checklist(320, 640)
fk.centered(372, 766, '点検', 24, fk.TEAL)
fk.arrow([(424, 650), (DX + 18, 568)], fk.TEAL, 5)
fk.centered(600, 642, '古さを見つける', 22, fk.TEAL)

# 右下中央：横断タスクボードが TODO を読む
BX0, BY0, BX1, BY1 = 830, 640, 1090, 790
fk.rr((BX0, BY0, BX1, BY1), 'white', fk.BLUE, 3, 14)
for k, w in enumerate([150, 110, 130]):
    ry = BY0 + 26 + k * 40
    fk.rr((BX0 + 22, ry, BX0 + 70, ry + 26), '#eef3f8', fk.BLUE, 2, 7)
    fk.d.line((BX0 + 86, ry + 13, BX0 + 86 + w, ry + 13), fill=fk.LINE, width=6)
fk.centered((BX0 + BX1) / 2, 800, '横断タスクボード', 24, fk.BLUE)
fk.arrow([(DX + 122, 568), (BX0 + 30, BY0 - 8)], fk.BLUE, 5)
fk.centered(848, 578, '読む', 22, fk.BLUE)

fk.save(Path(args.out))
