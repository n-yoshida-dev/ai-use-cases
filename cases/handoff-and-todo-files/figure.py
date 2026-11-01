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

# 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。ラベルは動くデータの名詞。線はすべて TEAL。
# 左＝会話の区切りで書く Claude Code、中央左＝2 つのファイル（読まれる側）、中央右＝次の会話の Claude Code、
# 右＝答えを書かれる TODO（読み書き両方の相手なので TODO を左右に 2 回置く）。
# 古さの点検は左の TODO を読み、指摘を次の会話の Claude Code へ渡す（会話の始めのフック）ので、TODO の真下に置く。
# 本人は問いを受け取り答えを返すので、次の会話の Claude Code の右上に置く（問い＝札の右の辺から上向き、答え＝札の上の辺へ下向き）。
# 横断タスクボードは右の TODO を読むので、その下に置く。定期実行はしないので時計は付けない。
OX = 45                              # 全体を右へ寄せて左右の余白をそろえる

# 中央右：次の会話の Claude Code（ほかの位置の基準）
CX, CY = 930 + OX, 470

# 左：会話の区切りで書く Claude Code
AX, AY = 150 + OX, CY - 140
fk.service('claude', AX, AY, 'Claude Code', tile=150)
fk.centered(AX, AY + 75 + 46, '会話の区切りで書く', 22, fk.GRAY)

# 中央左：2 つのファイル
DX, HY, TY = 470 + OX, AY, CY + 120  # 書類の左端、HANDOFF と TODO の中心
fk.centered(DX + 70, HY - 79 - 42, 'HANDOFF', 28, fk.BLUE)
fk.doc(DX, HY - 79, c=fk.BLUE)
fk.centered(DX + 70, TY - 79 - 42, 'TODO', 28, fk.AMBER)
fk.doc(DX, TY - 79, c=fk.AMBER)

fk.flow([(AX + 79, HY), (DX - 4, HY)], '現在地')
VX = 290 + OX
fk.flow([(AX + 79, AY + 55), (VX, AY + 55), (VX, TY), (DX - 4, TY)], '確認待ち・保留',
        at=((VX + DX - 4) / 2, TY - 37))

# 次の会話の Claude Code：左の辺に 3 本（現在地・確認待ち・古さの指摘）を 50px 間隔で受ける
fk.service('claude', CX, CY, 'Claude Code', tile=160)
fk.centered(CX, CY + 80 + 46, '読んで聞いて書く', 22, fk.GRAY)
IN = CX - 84
E1, E2, E3 = 690 + OX, 730 + OX, 780 + OX
fk.flow([(DX + 144, HY), (E1, HY), (E1, CY - 50), (IN, CY - 50)], '現在地', at=((E1 + IN) / 2, CY - 50 - 37))
fk.flow([(DX + 144, TY), (E2, TY), (E2, CY), (IN, CY)], '確認待ち', at=((DX + 144 + E2) / 2, TY - 37))

# TODO の真下：古さの点検。TODO を読み、指摘を次の会話の Claude Code へ渡す
KX, KY = DX + 70 - 52, TY + 79 + 46  # 点検の左端と上端
fk.flow([(DX + 70, TY + 83), (DX + 70, KY - 6)], '確認待ち・保留')
fk.checklist(KX, KY)
fk.centered(KX + 52, KY + 126, '古さの点検', 24, fk.TEAL)
KM = KY + 58
fk.flow([(KX + 108, KM), (E3, KM), (E3, CY + 50), (IN, CY + 50)], '古さの指摘',
        at=((KX + 108 + E3) / 2, KM - 37))

# 右上：本人。問いを受け取り、答えを返す
PS = .8
PX, PY = CX + 80, CY - 260
fk.person(PX, PY, PS)
fk.centered(PX, PY + 118 * PS + 10, '本人', 24)
QX, AX2 = PX + 46, PX - 48           # 問いが入る x、答えが出る x
fk.flow([(CX + 84, CY - 40), (QX, CY - 40), (QX, PY + 118 * PS + 4)], '問い',
        at=(QX + 14 + 23, (CY - 40 + PY + 118 * PS) / 2 - 16))
fk.flow([(AX2, PY + 118 * PS + 4), (AX2, CY - 84)], '答え',
        at=(AX2 - 14 - 23, (CY - 84 + PY + 118 * PS) / 2 - 16))

# 右：答えを書かれる TODO
RX, RY = 1130 + OX, CY + 30          # 書類の左端と中心
fk.centered(RX + 70, RY - 79 - 42, 'TODO', 28, fk.AMBER)
fk.doc(RX, RY - 79, c=fk.AMBER)
fk.flow([(CX + 84, RY), (RX - 4, RY)], '答え')

# 右下：TODO を読む横断タスクボード
BOT = RY + 79 + 92
BX0, BX1 = RX + 70 - 85, RX + 70 + 85
fk.flow([(RX + 70, RY + 83), (RX + 70, BOT - 6)], '確認待ち')
fk.rr((BX0, BOT, BX1, BOT + 116), 'white', fk.BLUE, 3, 14)
for k, w in enumerate([80, 56, 70]):
    ry = BOT + 16 + k * 32
    fk.rr((BX0 + 18, ry, BX0 + 58, ry + 22), '#eef3f8', fk.BLUE, 2, 6)
    fk.d.line((BX0 + 72, ry + 11, BX0 + 72 + w, ry + 11), fill=fk.LINE, width=6)
fk.centered((BX0 + BX1) / 2, BOT + 126, '横断タスクボード', 24, fk.BLUE)

fk.save(Path(args.out))
