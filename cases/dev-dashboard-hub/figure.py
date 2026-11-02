"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/dev-dashboard-hub/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/dev-dashboard-hub/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスのロゴは scripts/logos/）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。

矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow() だけで、ラベルは動くデータの名詞。
読まれる側（リポジトリ・GitHub）を左、常に動くプログラム（ハブ）を中央、書かれる側（1 枚の画面と本人）を右に置く。
Claude Code がリポジトリに読み取るプログラムと画面を書く流れは、主な流れと直角（下から上）に逃がす。
言葉は開発をしない人に分かるものにする（CI→自動テスト、HANDOFF→作業メモ、確認待ち→本人待ち）。
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


def card(x, y, w, h, fill_ratio, waiting, c=fk.TEAL):
    """ハブの 1 枚のカード（1 リポジトリ）：題名の線、進捗バー、本人待ちの件数、自動テストの印。"""
    fk.rr((x, y, x + w, y + h), 'white', fk.LINE, 2, 10)
    fk.d.line((x + 12, y + 16, x + w * .55, y + 16), fill=fk.LINE, width=6)
    # 進捗バー
    bx0, bx1, by = x + 12, x + w - 12, y + 32
    fk.d.rounded_rectangle((bx0, by, bx1, by + 12), radius=6, fill='#e6ecee')
    fk.d.rounded_rectangle((bx0, by, bx0 + (bx1 - bx0) * fill_ratio, by + 12), radius=6, fill=c)
    # 本人待ちの件数（色は件数の数字にだけ。番号の丸と紛れないよう角丸の札にする）
    fk.d.rounded_rectangle((x + 10, y + h - 40, x + 50, y + h - 8), radius=7, fill=fk.NOTE, outline=fk.AMBER, width=3)
    fk.centered(x + 30, y + h - 40, str(waiting), 22, fk.AMBER)
    # 自動テストの印（正常は灰色のチェック）
    cx, cy = x + w - 26, y + h - 24
    fk.d.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), fill='#eef1f2')
    fk.d.line([(cx - 7, cy), (cx - 2, cy + 6), (cx + 8, cy - 6)], fill=fk.GRAY, width=4, joint='curve')


def hub(cx, cy, w=170, h=140, c=fk.TEAL):
    """常に動くプログラム（ハブ）：箱の中に 2 段のサーバーの板と、点いている印。"""
    fk.rr((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), 'white', c, 3, 18)
    for k in range(2):
        sy = cy - 44 + k * 48
        fk.rr((cx - 60, sy, cx + 60, sy + 36), '#eaf3f1', c, 2, 8)
        fk.d.ellipse((cx - 46, sy + 12, cx - 34, sy + 24), fill=c)
        fk.d.line((cx - 22, sy + 18, cx + 44, sy + 18), fill=fk.LINE, width=6)


fk.begin()

CY = 370                       # 主な流れの高さ
CX, HW, HH = 645, 150, 140     # 中央：常に動くプログラム（ハブ）
HL = CX - HW / 2 - 12          # ハブの左の辺（入る線の先端）

# 左上：GitHub（自動テストの結果）
GX, GY = 150, CY - 160
fk.service('github', GX, GY, 'GitHub')

# 左：各リポジトリ（やること・作業メモ・変更履歴）
FW, FH = 120, 96
fk.folder(140, CY - 10, FW, FH, fk.TEAL)
fk.folder(90, CY + 38, FW, FH, fk.BLUE)
fk.folder(40, CY + 86, FW, FH, fk.TEAL)
fk.centered(100, CY + 194, 'リポジトリ', 25)

# 中央：常に動くプログラムが 30 分ごとに集めて 1 枚にする
hub(CX, CY, HW, HH)
fk.trigger(CX, CY - HH / 2, '30分ごと')
fk.centered(CX, CY + HH / 2 + 10, '常に動くプログラム', 25)
fk.verb(CX, CY + HH / 2 + 10 + 36, '集めて1枚に')

# 入る線（ハブの左の辺に 60px あけて 2 本）
# 自動テストの縦の区間はハブの上の時計「30分ごと」から離すため、左（x=440）に寄せる
fk.flow([(GX + 66 + 12, GY), (440, GY), (440, CY - 30), (HL, CY - 30)], '自動テストの結果')
# 2 本の線の間を空けておくため、ラベルは自分の線の真下に置く（矢じりから離すため少し左に寄せる）
fk.flow([(140 + FW + 14, CY + 30), (HL, CY + 30)], 'やること・作業メモ・履歴', at=((140 + FW + 14 + HL) / 2 - 4, CY + 30 + 12))

# 左下：Claude Code がリポジトリごとの読み取るプログラムと画面を書く（主な流れと直角に、下から上へ）
AX, AY = 226, CY + 330
fk.service('claude', AX, AY, 'Claude Code')
fk.verb(AX, AY + 66 + 12 + 36, '作る')
fk.flow([(AX, AY - 66 - 12), (AX, CY - 10 + FH + 12)], '読み取るプログラム・画面')

# 右：1 枚の画面（進捗・本人待ち・自動テストが並ぶ）
SX, SW, SH = 1068, 256, 240
SY = CY - SH / 2
fk.flow([(CX + HW / 2 + 12, CY), (SX - 14, CY)], '進捗・本人待ち・テスト', at=((CX + HW / 2 + 12 + SX - 14) / 2 - 10, CY - 37))
fk.laptop(SX, SY, SW, SH)
fk.d.rectangle((SX + 6, SY + 6, SX + SW - 6, SY + SH - 6), fill='#eaf3f1')
GW, GH, GAP = 108, 92, 12
gx0 = SX + (SW - 2 * GW - GAP) / 2
gy0 = SY + (SH - 2 * GH - GAP) / 2
card(gx0, gy0, GW, GH, .72, 2)
card(gx0 + GW + GAP, gy0, GW, GH, .45, 1, fk.BLUE)
card(gx0, gy0 + GH + GAP, GW, GH, .9, 0, fk.BLUE)
card(gx0 + GW + GAP, gy0 + GH + GAP, GW, GH, .3, 3)
fk.centered(SX + SW / 2, SY + SH + 37 + 12, '開発ダッシュボード', 25)   # 全体図・紹介資料と同じ呼び名（台の下に置く）

# 右端：本人は画面を見るだけ（書き込む線は無い）
PX, PY = 1387, CY - 10
fk.person(PX, PY, .72)
fk.centered(PX, PY + 118 * .72 + 14, '本人', 24)

fk.save(HERE / 'cover.png')
