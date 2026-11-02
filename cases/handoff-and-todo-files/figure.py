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
# 左＝作業を終える前に書く Claude Code、中央左＝2 つのファイル（読まれる側）、中央＝本人、中央右＝次の会話の Claude Code、
# 右＝答えを書かれる TODO（読み書き両方の相手なので TODO を左右に 2 回置く）。
# 本人は TODO の本人待ちを受け取り、答えを次の会話の Claude Code へ渡す。Claude Code から本人への直接の線は引かない
# （問いと答えが同じ 2 つの間の往復になるため。2026-11-02）。本人は TODO と次の会話の Claude Code の間に 1 回だけ置く。
# 古さの点検は左の TODO を読み、指摘を次の会話の Claude Code へ渡す（会話の始めのフック）ので、TODO の真下に置く。
# 横断タスクボードは右の TODO を読むので、その下に置く。定期実行はしないので時計は付けない。
# 言葉（2026-11-02）：本人「会話の区切りで書くっていうのが全然意味わかんない」ので、場面が浮かぶ「作業を終える前に書く」にする。
# 左右の Claude Code の違いが見え、右の札から TODO へ答えを書くことも読めるよう、右の動詞は「次の会話で読んで書く」。HANDOFF の中身は「今の状況」、本人の確認待ちは「本人待ち」（資料全体の統一語）。

# 中央右：次の会話の Claude Code（ほかの位置の基準）
CX, CY, CT = 1030, 520, 180
IN = CX - CT // 2 - 4                         # 札の左の辺（入る線の先端）

# 中央左：2 つのファイル（左端 DX、幅 DW）。TODO は Claude Code の札と同じ高さ
DX, DW = 470, 130
HY, TY = CY - 270, CY                # HANDOFF と TODO の中心
DR = DX + DW + 4                     # 書類の右の辺（出る線の根元）
fk.centered(DX + DW / 2, HY - 79 - 42, 'HANDOFF', 28, fk.BLUE)
fk.doc(DX, HY - 79, DW, c=fk.BLUE)
fk.centered(DX + DW / 2, TY - 79 - 42, 'TODO', 28, fk.AMBER)
fk.doc(DX, TY - 79, DW, c=fk.AMBER)

# 左：作業を終える前に書く Claude Code
AX, AY = 135, (HY + TY) // 2           # 動詞「作業を終える前に書く」と縦の線の間をあける
fk.service('claude', AX, AY, 'Claude Code', tile=150)
fk.verb(AX, AY + 75 + 12 + 36, '作業を終える前に書く')
VX = 280
fk.flow([(AX + 79, AY - 40), (VX, AY - 40), (VX, HY), (DX - 4, HY)], '今の状況', at=((VX + DX - 4) / 2, HY - 37))
fk.flow([(AX + 79, AY + 40), (VX, AY + 40), (VX, TY), (DX - 4, TY)], '本人待ち・保留',
        at=((VX + DX - 4) / 2, TY - 37))

# 中央：本人。TODO の本人待ちを受け取り、答えを次の会話の Claude Code へ渡す
PS = .8
PX, PY = 780, TY - 44           # 胴の中ほどが TODO と同じ高さに来る
PL, PR = PX - 68 * PS, PX + 68 * PS
fk.person(PX, PY, PS)
fk.centered(PX, PY + 118 * PS + 10, '本人', 24)
fk.flow([(DR, TY), (PL - 8, TY)], '本人待ち', at=((DR + PL - 8) / 2 - 8, TY - 37))

# 次の会話の Claude Code：左の辺に 3 本（今の状況・答え・古さの指摘）を 60px 間隔で受ける
fk.service('claude', CX, CY, 'Claude Code', tile=CT)
fk.verb(CX, CY + CT // 2 + 12 + 36, '次の会話で読んで書く')
E1, E3 = 880, 870                             # E3 は右の動詞と縦の線の間をあけるため左へ
fk.flow([(DR, HY), (E1, HY), (E1, CY - 60), (IN, CY - 60)], '今の状況', at=((DR + E1) / 2, HY - 37))
fk.flow([(PR + 8, CY), (IN, CY)], '答え', at=((PR + 8 + IN) / 2 - 4, CY - 37))

# TODO の真下：古さの点検。TODO を読み、指摘を次の会話の Claude Code へ渡す
KX, KY = DX + DW / 2 - 52, TY + 79 + 46  # 点検の左端と上端
fk.flow([(DX + DW / 2, TY + 83), (DX + DW / 2, KY - 6)], '本人待ち・保留')
fk.checklist(KX, KY)
fk.centered(KX + 52, KY + 126, '古さの点検', 24, fk.TEAL)
KM = KY + 58
fk.flow([(KX + 108, KM), (E3, KM), (E3, CY + 60), (IN, CY + 60)], '古さの指摘',
        at=((KX + 108 + E3) / 2, KM - 37))

# 右：答えを書かれる TODO
RX, RY = 1220, CY + 30          # 書類の左端と中心
fk.centered(RX + DW / 2, RY - 79 - 42, 'TODO', 28, fk.AMBER)
fk.doc(RX, RY - 79, DW, c=fk.AMBER)
fk.flow([(CX + CT // 2 + 4, RY), (RX - 4, RY)], '答え', at=((CX + CT // 2 + RX) / 2 - 6, RY - 37))

# 右下：TODO を読む横断タスクボード
BOT = RY + 79 + 92
BC = RX + DW / 2
BX0, BX1 = BC - 85, BC + 85
fk.flow([(BC, RY + 83), (BC, BOT - 6)], '本人待ち')
fk.rr((BX0, BOT, BX1, BOT + 116), 'white', fk.BLUE, 3, 14)
for k, w in enumerate([80, 56, 70]):
    ry = BOT + 16 + k * 32
    fk.rr((BX0 + 18, ry, BX0 + 58, ry + 22), '#eef3f8', fk.BLUE, 2, 6)
    fk.d.line((BX0 + 72, ry + 11, BX0 + 72 + w, ry + 11), fill=fk.LINE, width=6)
fk.centered((BX0 + BX1) / 2, BOT + 126, '横断タスクボード', 24, fk.BLUE)

fk.save(Path(args.out))
