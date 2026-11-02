"""このフォルダの part-context.png・part-record.png・part-review.png（中で動く 3 つの仕組みの図）を生成する。cover.png には触れない。

再生成：リポジトリの root で
    python3 systems/context-reading-loop/parts.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
（Python 3 / Pillow。フォントは任意の日本語フォント。部品は scripts/figkit.py、ロゴは scripts/logos/）

1 枚に 1 つの仕組み（cover.png は 3 段の全体像。こちらは仕組みごとに分けた図。2026-11-02 本人「図が差し込まれてないように見えます」）。
- part-context.png：会話を文脈として溜める。毎週日曜 22:00 に ChatGPT がその週の会話と正本を比べ、変わった目標・今の状況だけを
  personal-ai-context（非公開）に書く。矢印のラベルは part-review.png の「目標・今の状況」と同じ言葉にし、1 枚目が書いた物を 3 枚目が読むとつなぐ
- part-record.png：読書を記録する。本人が話しかけたとき ChatGPT が聞いて、reading-log の本ごとのファイルに書く。本棚サイトに出る
- part-review.png：週 1 回の振り返り。毎週日曜 20:30 に ChatGPT が 3 つを読み、候補の本を 5 項目 100 点で採点して
  reading-log に本ごとの点数を書く。本棚サイトで本人が次の 1 冊を見る。5 項目の中身は README と meta.yaml の deck に書く
  （点数のような独自の言葉は中身を見せる）

置き場として読まれる ChatGPT（会話の履歴）は、中身を札の上に書く（動詞と同じ札の下に置くと、作業に見えるため）。

矢印 1 本＝データが動く向き。読まれる側を左、ChatGPT を中央、書かれる側を右に置き、左から右への 1 本の鎖で順番を読ませる。
座標・錠の印・本棚サイトの絵は figure.py に合わせた。
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
import figkit as fk  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('--font', required=True)
fk.init(ap.parse_args().font)

HALF = 58
TILE = 2 * HALF
GAP = 4                  # 矢じりと札のすき間
PS = .8                  # 本人の大きさ


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
        k = 0
        while True:
            bw = 16 + (k * 7 + row * 5) % 9
            if bx + bw > x + w - 14:
                break
            bh = 30 + (k * 11 + row * 7) % 15
            fk.d.rectangle((bx, base - bh, bx + bw, base), fill=colors[(k + row * 3) % len(colors)])
            bx += bw + 5
            k += 1
        fk.d.line((x + 10, base + 2, x + w - 10, base + 2), fill=fk.INK, width=4)


def site(cx, cy, w=200, h=150):
    """本棚サイト（中心 cx, cy）。名前は下。左右の辺の x を返す。"""
    bookshelf(cx - w / 2, cy - h / 2, w, h)
    fk.centered(cx, cy + h / 2 + 12, '本棚サイト', 25)
    return cx - w / 2, cx + w / 2


def chatgpt(x, y, verb=None, when=None, holds=None):
    """ChatGPT の札。きっかけ（定期実行のときだけ）は真上、名前と動詞は下。
    置き場として読まれるときは、中身（holds）を store() の名前と同じく札の上に書く。"""
    fk.service('openai', x, y, 'ChatGPT', tile=TILE)
    if holds:
        fk.centered(x, y - HALF - 44, holds, 25)
    if when:
        fk.trigger(x, y - HALF, when)
    if verb:
        fk.verb(x, y + HALF + 12 + 36, verb)


def me(x, cy):
    """本人（体の中ほどが cy）。左右の辺の x を返す。"""
    py = cy - 20 * PS
    fk.person(x, py, PS)
    fk.centered(x, py + 118 * PS + 10, '本人', 25)
    return x - 68 * PS, x + 68 * PS


def context():
    """1 会話を文脈として溜める：本人 → 会話の履歴 → 日曜 22:00 に差分を整理 → personal-ai-context（非公開）。"""
    fk.SIZE = (1440, 700)
    fk.begin()
    PX, IX, GX, RX = 130, 480, 860, 1250
    CY = 300
    _, pr = me(PX, CY)
    chatgpt(IX, CY, holds='会話の履歴')
    chatgpt(GX, CY, '差分を整理', '日曜22:00')
    store('personal-ai-context', RX, CY, True)
    fk.flow([(pr + 12, CY), (IX - HALF - GAP, CY)], '会話', size=22)
    fk.flow([(IX + HALF, CY), (GX - HALF - GAP, CY)], '今週の会話', size=22)
    fk.flow([(GX + HALF, CY), (RX - HALF - GAP, CY)], '目標・今の状況の更新', size=22)
    fk.save(HERE / 'part-context.png')


def record():
    """2 読書を記録する：本人 → ChatGPT（聞いて記録）→ reading-log → 本棚サイト。"""
    fk.SIZE = (1440, 700)
    fk.begin()
    PX, GX, RX, SX = 130, 500, 880, 1220
    CY = 300
    _, pr = me(PX, CY)
    chatgpt(GX, CY, '聞いて記録')
    store('reading-log', RX, CY)
    sl, _ = site(SX, CY)
    fk.flow([(pr + 12, CY), (GX - HALF - GAP, CY)], '進捗・感想')
    fk.flow([(GX + HALF, CY), (RX - HALF - GAP, CY)], '本ごとの記録')
    fk.flow([(RX + HALF, CY), (sl - GAP, CY)])
    fk.save(HERE / 'part-record.png')


def review():
    """3 週 1 回の振り返り：3 つを読む → 日曜 20:30 に採点 → reading-log → 本棚サイト → 本人。"""
    fk.SIZE = (1440, 900)
    fk.begin()
    IX, BEND, GX, RX, SX, PX = 150, 420, 556, 866, 1052, 1340
    CY = 420
    ROW = 200
    TOP, BOT = CY - ROW, CY + ROW
    store('reading-log', IX, TOP)
    store('personal-ai-context', IX, CY, True)
    chatgpt(IX, BOT, holds='会話の履歴')
    chatgpt(GX, CY, '5項目100点で採点', '日曜20:30')
    store('reading-log', RX, CY)
    sl, sr = site(SX, CY, w=160, h=160)
    pl, _ = me(PX, CY)
    seg = (IX + HALF + BEND) / 2
    fk.flow([(IX + HALF, TOP), (BEND, TOP), (BEND, CY - 34), (GX - HALF - GAP, CY - 34)], '本・前回の振り返り',
            at=(seg, TOP - 37), size=22)
    fk.flow([(IX + HALF, CY), (GX - HALF - GAP, CY)], '目標・今の状況', size=22)
    fk.flow([(IX + HALF, BOT), (BEND, BOT), (BEND, CY + 34), (GX - HALF - GAP, CY + 34)], '今週の会話',
            at=(seg, BOT - 37), size=22)
    fk.flow([(GX + HALF, CY), (RX - HALF - GAP, CY)], '本ごとの点数', size=22)
    fk.flow([(RX + HALF, CY), (sl - GAP, CY)])
    fk.flow([(sr + GAP, CY), (pl - 12, CY)], '次の1冊', size=22)
    fk.save(HERE / 'part-review.png')


context()
record()
review()
