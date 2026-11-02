"""このケースの score.png（棚卸しと点数で優先度を決める）を生成する。他の画像には触れない。

再生成：リポジトリの root で
    python3 cases/allowance-shopping-plan/score.py --font /absolute/path/日本語フォント
（Python 3 / Pillow。部品は scripts/figkit.py、ロゴは scripts/logos/）

買い物計画の最初の作業（2026-11-02 の本人の指摘で、点数をつける作業を切り出した）。左から 1 本の鎖：
本人 →（押した答え）→ 計画画面の棚卸しのタブ →（棚卸しの結果）→ Claude Code（Notion に反映）→（要否・5つの答え）→ Notion の欲しいもの
（数式で点数を出す）→（点数）→ 点数順の一覧。
棚卸しのタブには、上に「要る・要らない」、下に 5 つの質問（困りごと・代わり・使う頻度・良くなる度・待つと損）を描き、
点数の中身が絵で読めるようにする。待つと損は点数を 2 倍にする（このケースの README）。
Notion の右には短い矢印（点数）で点数の列で並んだ一覧をつなぎ、下に「点数順の欲しい物」と書く
（旧版は一覧が Notion の横に離れて置かれ、別物に見えた。2026-11-02 点検）。cover.png（値段とセールから買う月を決める）の
左上は同じ絵・同じ言葉なので、2 枚がつながって読める。
Claude Code の前後の線は、同じ言葉だと何が渡るかが読めないので分ける。画面から Claude へは「棚卸しの結果」、
Claude から Notion へはその中身の「要否・5つの答え」（2026-11-02 点検）。

事実の出どころはこのケースの README（「いる／いらない」と質問の答えを画面で押すと保存され、Claude がまとめて Notion に反映する。
点数は Notion の数式の列）。本人が Notion に直接答えを入れる流れもあるが、並んで走る矢印を増やさないため、
この図では画面から入る流れだけを描く。

描き方の決まりは AGENTS.md「見せ方と図」。生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
import figkit as fk  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('--font', required=True)
fk.init(ap.parse_args().font)
fk.begin()
d = fk.d

LS = 22
Y = 400                       # 鎖の高さ
PX, PS = 64, .6               # 本人
SX0, SX1 = 276, 542           # 棚卸しのタブ（左右）。本人との間は 170px 以上（線のラベル「押した答え」を矢じりから離す）
CC = 774                      # Claude Code
NX = 1088                     # Notion
LX, LW = 1228, 176            # 点数順の一覧（左の辺・幅）
TILE = 100                    # 線のラベルの場所を空けるため、札は小さめ
H = TILE / 2
GAP = 4

QUESTIONS = ['困りごと', '代わり', '使う頻度', '良くなる度', '待つと損']


def line(x0, x1, label):
    """線（x0 → x1）のラベルの場所。文字の下端は矢じりの上端より下に来るので、横で矢じりを避ける：
    根元から 8px、矢じりの付け根（先端から 18px）からさらに 8px 空けた間の中央に置く。
    間が足りなければ止める（2026-11-02 点検で「押した答え」「点数」が矢じりに重なった）。"""
    w = fk.width(label, LS)
    lo, hi = x0 + 8, x1 - 26
    assert hi - lo >= w, f'{label}: 線が短い（{hi - lo:.0f} < {w:.0f}）'
    return ((lo + hi) / 2, Y - LS - 14)


def review_tab(x0, x1, cy):
    """計画画面の棚卸しのタブ：上に「要る・要らない」のボタン、下に 5 つの質問（選ぶ丸 3 つ）。下に名前。"""
    rows, rh = len(QUESTIONS), 40
    h = 30 + 72 + rows * rh + 16
    y0 = cy - h / 2
    fk.rr((x0, y0, x1, y0 + h), 'white', fk.TEAL, 3, 14)
    d.rounded_rectangle((x0 + 2, y0 + 2, x1 - 2, y0 + 28), radius=12, fill='#e7eef6')
    # 要る・要らない
    by = y0 + 46
    fk.rr((x0 + 22, by, x0 + 108, by + 40), fk.TEAL, fk.TEAL, 2, 20)
    fk.centered(x0 + 65, by + 5, '要る', 22, 'white')
    fk.rr((x0 + 120, by, x0 + 236, by + 40), 'white', fk.LINE, 3, 20)
    fk.centered(x0 + 178, by + 5, '要らない', 22, fk.GRAY)
    d.line((x0 + 20, y0 + 102, x1 - 20, y0 + 102), fill=fk.LINE, width=2)
    # 5 つの質問
    for k, q in enumerate(QUESTIONS):
        ry = y0 + 118 + k * rh
        fk.text(x0 + 24, ry, q, 21)
        for j in range(3):
            cx = x0 + 152 + j * 28
            fill = fk.AMBER if j == (2, 1, 2, 1, 2)[k] else 'white'
            d.ellipse((cx - 9, ry + 6, cx + 9, ry + 24), fill=fill, outline=fk.AMBER, width=3)
        if k == rows - 1:
            fk.text(x0 + 226, ry - 1, '×2', 22, fk.AMBER)
    fk.centered((x0 + x1) / 2, y0 + h + 12, '計画画面の棚卸し', 25)


def scored_list(x0, cy, w):
    """Notion の欲しいものの一覧（点数の列で並ぶ）：画像の四角・名前の行・点数の棒（長い順）。"""
    rows, rh = 4, 44
    h = 40 + rows * rh + 8
    y0 = cy - h / 2
    fk.rr((x0, y0, x0 + w, y0 + h), 'white', fk.INK, 3, 12)
    bx = x0 + w - 80              # 点数の棒の左端
    fk.text(bx, y0 + 8, '点数', 21, fk.AMBER)
    for k in range(rows):
        ry = y0 + 40 + k * rh
        fk.rr((x0 + 16, ry, x0 + 50, ry + 32), '#e7eef6', fk.BLUE, 2, 6)
        d.line((x0 + 62, ry + 16, bx - 14, ry + 16), fill=fk.LINE, width=6)
        d.rounded_rectangle((bx, ry + 8, bx + (64, 50, 36, 22)[k], ry + 24), radius=6, fill=fk.AMBER)
    fk.centered(x0 + w / 2, y0 + h + 12, '点数順の欲しい物', 25)


# 本人 → 棚卸しのタブ
fk.person(PX, Y - 20, PS)
fk.centered(PX, Y - 20 + 118 * PS + 10, '本人', 25)
fk.flow([(PX + 68 * PS + 8, Y), (SX0 - GAP, Y)], '押した答え', at=line(PX + 68 * PS + 8, SX0 - GAP, '押した答え'), size=LS)
review_tab(SX0, SX1, Y)

# 棚卸しのタブ → Claude Code（Notion に反映）
fk.flow([(SX1 + 6, Y), (CC - H - GAP, Y)], '棚卸しの結果', at=line(SX1 + 6, CC - H - GAP, '棚卸しの結果'), size=LS)
fk.service('claude', CC, Y, 'Claude Code', tile=TILE)
fk.verb(CC, Y + H + 12 + 36, 'Notion に反映')

# Claude Code → Notion（数式で点数を出す）→ 点数順の一覧
fk.flow([(CC + H + 6, Y), (NX - H - GAP, Y)], '要否・5つの答え', at=line(CC + H + 6, NX - H - GAP, '要否・5つの答え'), size=LS)
fk.service('notion', NX, Y, '欲しいもの', tile=TILE)
fk.verb(NX, Y + H + 12 + 36, '数式で点数を出す')
fk.flow([(NX + H + 6, Y), (LX - GAP, Y)], '点数', at=line(NX + H + 6, LX - GAP, '点数'), size=LS)
scored_list(LX, Y, LW)

fk.save(HERE / 'score.png')
