"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/daily-cross-task-board/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/daily-cross-task-board/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスのロゴは scripts/logos/）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。

矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow() だけ。
左＝読まれる側、中央＝AI、右＝書かれる側。ラベルは動くデータの名詞、動詞は AI の札の下。
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


def chat_bubble(x, y, w=64, h=44, c=fk.BLUE):
    """会話の印：吹き出し（文字なし）。左下に尾。"""
    fk.d.polygon([(x + 12, y + h - 2), (x + 6, y + h + 16), (x + 30, y + h - 2)], fill='white', outline=c)
    fk.rr((x, y, x + w, y + h), 'white', c, 3, 12)
    fk.d.line((x + 10, y + h - 6, x + 28, y + h - 6), fill='white', width=4)
    for k in range(3):
        fk.d.ellipse((x + 14 + k * 15, y + h / 2 - 4, x + 22 + k * 15, y + h / 2 + 4), fill=c)


def row(x, y, tag, c, line_w, done=False, tag_w=96):
    """ボードの1行。左に札（幅 tag_w・高さ 30）、右にチェック欄。"""
    fk.rr((x, y, x + tag_w, y + 30), '#eef3f8' if c == fk.BLUE else '#eaf3f1', c, 2, 8)
    fk.centered(x + tag_w / 2, y + 1, tag, 19, c)
    fk.d.line((x + tag_w + 20, y + 15, x + tag_w + 20 + line_w, y + 15), fill=fk.LINE, width=7)
    bx = x + 400
    fk.d.rectangle((bx, y + 4, bx + 22, y + 26), outline=c, width=3)
    if done:
        fk.d.line([(bx + 4, y + 14), (bx + 10, y + 21), (bx + 20, y + 7)], fill=fk.AMBER, width=4, joint='curve')


fk.begin()

# 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。ラベルは動くデータの名詞。
# 左＝読まれる側（Todoist・カレンダー・各リポジトリ）、中央＝Claude Code、
# 右＝書かれる側（ボード・Todoist の完了と日付・別フォルダの会話への依頼文）。
# Todoist は読み書き両方の相手なので、左（読まれる側）と右（書かれる側）に 2 回置く。
# 本人は依頼を出し、ボードを受け取るので、ボードの真上に置く（ボード→本人は上向き、本人→Claude Code は下向き）。
# 自動実行はしないので時計（きっかけ）は付けない。
# 書いたあとの読み直し（検算）は、ボードとの逆向きの線を並べないため、札の下の動詞に入れる。
CX, CY = 600, 480
fk.service('claude', CX, CY, 'Claude Code', tile=160)
fk.centered(CX, CY + 80 + 46, '組んで検算', 22, fk.GRAY)

# 左：読まれる側
LX, ELB, ELB2 = 140, 430, 480
fk.service('todoist', LX, 290, 'Todoist')
fk.flow([(LX + 72, 290), (ELB, 290), (ELB, CY - 50), (CX - 84, CY - 50)], 'タスク', at=((LX + 72 + ELB) / 2, 290 - 37))
fk.service('googlecalendar', LX, CY, 'カレンダー')
fk.flow([(LX + 72, CY), (CX - 84, CY)], '予定表', at=((LX + 72 + ELB) / 2, CY - 37))
folder(LX - 92, 636, 100, 70)
folder(LX - 32, 654, 100, 70, fk.BLUE)
fk.centered(LX - 22, 738, 'リポジトリ', 25)
fk.flow([(LX + 78, 680), (ELB2, 680), (ELB2, CY + 50), (CX - 84, CY + 50)], '計画・進捗・人間待ち',
        at=((LX + 78 + ELB2) / 2, 680 - 37))

# 右上：横断タスクボード（時刻の枠・配分の枠）
bx0, by0, bx1 = 860, 300, 1390
by1 = by0 + 276
BCX = (bx0 + bx1) // 2
fk.flow([(CX + 84, CY - 40), (bx0 - 4, CY - 40)], '時間割')
fk.rr((bx0, by0, bx1, by1), 'white', fk.BLUE, 3, 14)
for k, (name, on) in enumerate([('予定', True), ('AIに任せる', False), ('開発状況', False)]):
    tx = bx0 + 22 + k * 160
    fk.rr((tx, by0 + 12, tx + 148, by0 + 46), fk.BLUE if on else '#eef3f8', fk.BLUE, 2, 9)
    fk.centered(tx + 74, by0 + 14, name, 20, 'white' if on else fk.BLUE)
row(bx0 + 30, by0 + 60, '5:30', fk.BLUE, 230, True)
row(bx0 + 30, by0 + 98, '20:30', fk.BLUE, 190)
row(bx0 + 30, by0 + 136, '21:45', fk.BLUE, 150)
fk.d.line((bx0 + 24, by0 + 180, bx1 - 24, by0 + 180), fill=fk.LINE, width=2)
row(bx0 + 30, by0 + 192, '声で 2分', fk.TEAL, 200, tag_w=112)
row(bx0 + 30, by0 + 230, 'AIへ 10分', fk.TEAL, 170, tag_w=112)
fk.centered(BCX, by1 + 10, '横断タスクボード', 27, fk.BLUE)

# 右下：Todoist（書かれる側。本人の指示による完了・日付変更・削除）
TX, TY = 1320, 680
fk.flow([(CX + 84, CY + 10), (790, CY + 10), (790, TY), (TX - 59, TY)], '完了・日付・削除',
        at=(900, TY - 37))
fk.service('todoist', TX, TY, 'Todoist', tile=110)

# 右下：別のフォルダの会話へ渡す依頼文（フォルダに吹き出しを重ね、リポジトリと見分ける）
FY = 760
fk.flow([(CX + 84, CY + 60), (740, CY + 60), (740, FY), (896, FY)], '依頼文', at=(812, FY - 37))
folder(900, FY - 40, 100, 70)
folder(960, FY - 22, 100, 70, fk.BLUE)
chat_bubble(1030, FY - 58)
fk.centered(990, FY + 64, '別フォルダの会話', 25)

# 上：本人（ボードの真上）。ボードの時間割を受け取り（上向き）、依頼を出す（左へ出て下向き）
PX, PY, PS = BCX, 100, .72
fk.person(PX, PY, PS)
fk.centered(PX, PY + 93, '本人', 24)
fk.flow([(PX, by0 - 4), (PX, PY + 136)], '今日と明日の時間割', color=fk.BLUE,
        at=(PX + 14 + fk.width('今日と明日の時間割', 23) / 2, (by0 + PY + 136) / 2 - 16))
fk.flow([(PX - 68 * PS - 8, PY + 40), (CX, PY + 40), (CX, CY - 84)], '依頼と完了の指示', color=fk.AMBER,
        at=((CX + PX - 68 * PS) / 2, PY + 40 - 37))

fk.save(HERE / 'cover.png')
