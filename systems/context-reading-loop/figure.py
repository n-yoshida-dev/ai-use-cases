"""全体概念図（会話の文脈から次に読む本へ）。

再生成：リポジトリの root で
    PYTHONPATH=<Pillow の場所> python3 systems/context-reading-loop/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
（フォントは任意の日本語フォント。部品は scripts/figkit.py、ロゴは scripts/logos/）
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import figkit as fk

ap = argparse.ArgumentParser()
ap.add_argument('--font', required=True)
fk.init(ap.parse_args().font)
fk.SIZE = (1440, 1500)           # 3 段あるので縦を伸ばす（save() が中身に合わせて切り詰める）
fk.begin()

# 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow() だけ。
# 上から 3 段：1 文脈を溜める／2 読書を記録する／3 週 1 回の振り返り。段どうしの線は交差させない。
# 列：本人（左に 1 回）｜読まれる側｜ChatGPT（定期実行はきっかけを真上に）｜書かれる正本。
# 同じ正本が別の段で読まれる・書かれるときは、段ごとにロゴを置き直す。
# 最後に、振り返りを書いた reading-log が本棚サイトになり、本人が見る（図の下を回って本人の足もとへ）。
PX, IX, GX, RX = 120, 400, 790, 1230     # 本人・読まれる側・ChatGPT・書かれる正本の列
Y1, Y2, Y3 = 170, 440, 925               # 段 1・段 2・段 3 の中心
HALF = 58
TILE = 2 * HALF
PY, PS = 360, .8                          # 本人
GAP = 4                                   # 矢じりと札のすき間


def lock(lx, ly, c=fk.BLUE):
    """非公開の印。札の角に付ける小さな錠。"""
    fk.d.arc((lx - 11, ly - 26, lx + 11, ly - 2), 180, 360, fill=c, width=5)
    fk.rr((lx - 16, ly - 10, lx + 16, ly + 16), 'white', c, 3, 6)
    fk.d.ellipse((lx - 4, ly - 1, lx + 4, ly + 7), fill=c)


def store(name, x, y, private=False):
    """正本の札（GitHub のロゴ）。名前は札の上。非公開なら右下の角に錠。"""
    fk.service('github', x, y, tile=TILE)
    fk.centered(x, y - HALF - 44, name, 25)
    if private:
        lock(x + HALF - 2, y + HALF - 12)


def bookshelf(x, y, w, h):
    """本棚サイトの画面：ブラウザの枠に、背表紙の並んだ棚が 2 段。"""
    fk.rr((x, y, x + w, y + h), 'white', fk.TEAL, 4, 14)
    fk.d.rounded_rectangle((x + 2, y + 2, x + w - 2, y + 30), radius=12, fill='#e3efed')
    for k in range(3):
        fk.d.ellipse((x + 14 + k * 18, y + 11, x + 24 + k * 18, y + 21), fill=fk.TEAL)
    colors = [fk.TEAL, fk.BLUE, fk.AMBER, fk.FAINT, fk.BLUE, fk.TEAL, fk.AMBER, fk.BLUE]
    for row in range(2):
        base = y + 34 + (row + 1) * (h - 50) / 2
        bx = x + 18
        for k in range(7):
            bw = 16 + (k * 7 + row * 5) % 9
            bh = 34 + (k * 11 + row * 7) % 16
            fk.d.rectangle((bx, base - bh, bx + bw, base), fill=colors[(k + row * 3) % len(colors)])
            bx += bw + 5
        fk.d.line((x + 10, base + 2, x + w - 10, base + 2), fill=fk.INK, width=4)


def chatgpt(x, y, verb=None, when=None):
    """ChatGPT の札。きっかけ（定期実行のときだけ）は真上、名前と動詞（置き場なら中身）は下。"""
    fk.service('openai', x, y, 'ChatGPT', tile=TILE)
    if when:
        fk.trigger(x, y - HALF, when)
    if verb:
        fk.verb(x, y + HALF + 12 + 36, verb)


# 本人（左に 1 回）
fk.person(PX, PY, PS)
HEAD = PY - 84 * PS                       # 頭のてっぺん
FOOT = PY + 118 * PS                      # 足もと
fk.centered(PX, FOOT + 8, '本人', 25)

# 段 1：文脈を溜める（本人 → ChatGPT の会話の履歴（置き場）→ 日曜 22:00 に差分 → personal-ai-context）
chatgpt(IX, Y1, '会話の履歴')
chatgpt(GX, Y1, '差分を整理', '日曜22:00')
store('personal-ai-context', RX, Y1, True)
fk.flow([(PX, HEAD - 14), (PX, Y1), (IX - HALF - GAP, Y1)], '会話')
fk.flow([(IX + HALF, Y1), (GX - HALF - GAP, Y1)], '今週の会話')
fk.flow([(GX + HALF, Y1), (RX - HALF - GAP, Y1)], '目標・今の状況の更新', size=22)   # 段 3 が読む物と同じ言葉

# 段 2：読書を記録する（本人 → ChatGPT → reading-log）
chatgpt(GX, Y2, '聞いて記録')
store('reading-log', RX, Y2)
fk.flow([(PX + 68 * PS + 14, Y2), (GX - HALF - GAP, Y2)], '進捗・感想')
fk.flow([(GX + HALF, Y2), (RX - HALF - GAP, Y2)], '本ごとの記録')

# 段 3：週 1 回の振り返り（3 つを読む → 日曜 20:30 に採点 → reading-log）
TOP, BOT = Y3 - 185, Y3 + 185             # 上と下の入力
BEND = 680                                # 上下の入力が曲がる x
store('reading-log', IX, TOP)
store('personal-ai-context', IX, Y3, True)
chatgpt(IX, BOT, '会話の履歴')              # 段 1 と同じ置き場（会話の履歴）
chatgpt(GX, Y3, '5項目100点で採点', '日曜20:30')
store('reading-log', RX, Y3)
fk.flow([(IX + HALF, TOP), (BEND, TOP), (BEND, Y3 - 36), (GX - HALF - GAP, Y3 - 36)], '本・前回の振り返り',
        at=((IX + HALF + BEND) / 2, TOP - 37), size=22)
fk.flow([(IX + HALF, Y3), (GX - HALF - GAP, Y3)], '目標・今の状況', size=22)
fk.flow([(IX + HALF, BOT), (BEND, BOT), (BEND, Y3 + 36), (GX - HALF - GAP, Y3 + 36)], '今週の会話',
        at=((IX + HALF + BEND) / 2, BOT - 37), size=22)
# 出力は 1 本（並んで走る線を増やさない。次の 1 冊は点数から本棚サイトで見る）
fk.flow([(GX + HALF, Y3), (RX - HALF - GAP, Y3)], '本ごとの点数')

# 本棚サイト：reading-log → 画面 → 本人（図の下を回って足もとへ）
LW, LH = 210, 160
LX0, LY0 = RX - LW / 2, BOT + 80
fk.flow([(RX, Y3 + HALF + 8), (RX, LY0 - GAP)])
bookshelf(LX0, LY0, LW, LH)
fk.centered(RX, LY0 + LH + 12, '本棚サイト', 25)
SY = LY0 + LH / 2 + 10
fk.flow([(LX0 - GAP, SY), (PX, SY), (PX, FOOT + 54)], '次の1冊', at=(GX, SY - 37))

fk.save(Path(__file__).with_name('cover.png'))
