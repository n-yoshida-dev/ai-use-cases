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
# 右＝書かれる側（ボード・Todoist の完了とリスケ）。
# Todoist は読み書き両方の相手なので、左（読まれる側）と右（書かれる側）に 2 回置く。
# 本人はボードの真上に 1 回だけ置く。ボードから時間割と依頼文を受け取り（上向き）、依頼・完了の指示を Claude Code へ出し（左へ出て下向き）、
# 依頼文をほかの作業の会話（そのリポジトリで開く新しい会話）に貼る（右向き）。Claude Code からその会話へは線を引かない
# （Claude Code は依頼文を作るだけで、貼るのは本人。自動で送っているように見えるため。2026-11-02）。
# 自動実行はしないので時計（きっかけ）は付けない。
# 書いたあとの読み直し（検算）は、ボードとの逆向きの線を並べないため、札の下の動詞に入れる。
CX, CY = 640, 480
fk.service('claude', CX, CY, 'Claude Code', tile=160)
fk.verb(CX, CY + 80 + 12 + 36, '組んで検算')

# 左：読まれる側
LX, ELB, ELB2 = 170, 460, 520
fk.service('todoist', LX, 290, 'Todoist')
fk.flow([(LX + 72, 290), (ELB, 290), (ELB, CY - 50), (CX - 84, CY - 50)], 'タスク', at=((LX + 72 + ELB) / 2, 290 - 37))
fk.service('googlecalendar', LX, CY, 'カレンダー')
fk.flow([(LX + 72, CY), (CX - 84, CY)], '今日・明日の予定', at=((LX + 72 + ELB) / 2, CY - 37))
folder(LX - 82, 636, 100, 70)
folder(LX - 18, 654, 100, 70, fk.BLUE)
fk.centered(LX, 738, '作業中のリポジトリ', 24)
fk.flow([(LX + 94, 680), (ELB2, 680), (ELB2, CY + 50), (CX - 84, CY + 50)], '計画・進捗・本人待ち',
        at=((LX + 94 + ELB2) / 2, 680 - 37))

# 右：横断タスクボード（時刻の枠・配分の枠。「AIに任せる」の欄に依頼文が付く）
bx0, by0, bx1 = 920, 300, 1390
by1 = by0 + 316
BCX = (bx0 + bx1) // 2
fk.flow([(CX + 84, CY - 40), (bx0 - 4, CY - 40)], '時間割・依頼文', at=((CX + 84 + bx0) / 2 - 16, CY - 40 - 37))
fk.rr((bx0, by0, bx1, by1), 'white', fk.BLUE, 3, 14)
# タブは画面と同じ 6 つ（2026-11-08 に日付、2026-11-10 に目標と確認待ちを足し、分野ごとのタブを外した）。
# 画面の並びのまま 3 つずつ 2 段。字は 18、段ごとに枠の中央にそろえる
TABS = [[('スケジュール', True), ('目標', False), ('日付', False)],
        [('確認待ち', False), ('開発状況', False), ('AIに任せる', False)]]
for k, tabs in enumerate(TABS):
    ty = by0 + 12 + k * 40
    tx = BCX - (sum(fk.width(n, 18) + 18 for n, _ in tabs) + 8 * (len(tabs) - 1)) / 2
    for name, on in tabs:
        tw = fk.width(name, 18) + 18
        fk.rr((tx, ty, tx + tw, ty + 34), fk.BLUE if on else '#eef3f8', fk.BLUE, 2, 9)
        fk.centered(tx + tw / 2, ty + 3, name, 18, 'white' if on else fk.BLUE)
        tx += tw + 8
RY0 = by0 + 40  # タブを 2 段にした分、行を下げる
row(bx0 + 30, RY0 + 60, '5:30', fk.BLUE, 230, True)
row(bx0 + 30, RY0 + 98, '20:30', fk.BLUE, 190)
row(bx0 + 30, RY0 + 136, '21:45', fk.BLUE, 150)
fk.d.line((bx0 + 24, RY0 + 180, bx1 - 24, RY0 + 180), fill=fk.LINE, width=2)
row(bx0 + 30, RY0 + 192, '声で 2分', fk.TEAL, 200, tag_w=112)
row(bx0 + 30, RY0 + 230, 'AIへ 10分', fk.TEAL, 170, tag_w=112)
fk.centered(BCX, by1 + 10, '横断タスクボード', 27, fk.BLUE)

# 右下：Todoist（書かれる側。本人の指示による完了・リスケ）
TX, TY = BCX, 760
fk.flow([(CX + 84, CY + 40), (790, CY + 40), (790, TY), (TX - 59, TY)], '完了・リスケ',
        at=((790 + TX - 59) / 2, TY - 37))
fk.service('todoist', TX, TY, 'Todoist', tile=110)

# 上：本人（ボードの上）。ボードの時間割と依頼文を受け取り（上向き）、依頼を出し（左へ出て下向き）、
# 依頼文をほかの作業の会話に貼る（右向き）
PX, PY, PS = 1010, 100, .72
PL, PR = PX - 68 * PS - 8, PX + 68 * PS + 8
fk.person(PX, PY, PS)
fk.centered(PX, PY + 93, '本人', 24)
fk.flow([(PX, by0 - 4), (PX, PY + 136)], '時間割・依頼文',
        at=(PX + 14 + fk.width('時間割・依頼文', 23) / 2, (by0 + PY + 136) / 2 - 16))
fk.flow([(PL, PY + 40), (CX, PY + 40), (CX, CY - 84)], '依頼・完了の指示',
        at=((CX + PL) / 2, PY + 40 - 37))

# 右上：ほかの作業の会話（そのリポジトリで開く新しい会話。フォルダに吹き出しを重ね、左のリポジトリと見分ける）。本人が依頼文を貼る
FX, FY = 1190, PY + 40
fk.flow([(PR, FY), (FX - 4, FY)], '依頼文')
folder(FX, FY - 40, 100, 70)
folder(FX + 60, FY - 22, 100, 70, fk.BLUE)
chat_bubble(FX + 130, FY - 58)
fk.centered(FX + 90, FY + 64, 'ほかの作業の会話', 25)

fk.save(HERE / 'cover.png')
