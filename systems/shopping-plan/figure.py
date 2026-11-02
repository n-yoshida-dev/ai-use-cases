"""全体概念図（欲しい物は Notion の 1 つ）。この全体構成の cover.png を生成する。他の画像には触れない。

再生成：リポジトリの root で
    python3 systems/shopping-plan/figure.py --font /absolute/path/日本語フォント
（Python 3 / Pillow。部品は scripts/figkit.py、ロゴは scripts/logos/）

買い物の 3 つの仕組みのつながりだけを描く全体像（2026-11-02 の本人の指摘で描き直し）。
左から 1 本の鎖：本人 →（用途と条件）→ ChatGPT（調べて比べる）→（登録する商品）→ Notion の欲しいもの。
Notion から 2 本に分かれる：
- 上：（点数順の欲しい物）→ Claude Code（お小遣いで買う月を決める）→ 計画画面（いつ何を買うか）
- 下：（定価つきの欲しい物）→ ChatGPT のメルカリプラグイン（お買い得を探す）→ 提案（お買い得の候補）
Notion の札の下に灰色の動詞「棚卸しして / 点数で並べる」（2 行）を置き、Notion の中で棚卸しと点数の段があることを
矢印を増やさずに見せる（旧版は Notion から急に「点数順の欲しい物」が出ていた。2026-11-02 点検）。
動詞が分かれ目の縦の線にかからないよう、曲がる位置 BEND を Notion から離し、右の列を少し右へ寄せた。
分かれた先の線のラベル・動詞・計画画面の絵は、内訳の図（cases/allowance-shopping-plan の score.png・cover.png・mercari.png）と
同じ言葉と形にそろえる（全体像から内訳へつながって読めるように。2026-11-02 点検）。
比べるのは ChatGPT の会話の中なので動詞に書き、Notion への線は渡る物（登録する商品）だけにする
（旧版の「欲しい物と比較」は「欲しい物と、比較」に読めた。2026-11-02 本人）。
メルカリは ChatGPT のプラグインなので fk.plugin で 1 枚の札にする。

細かい入力は内訳の図に任せ、この図には描かない：
- 棚卸しと 5 つの質問の点数（cases/allowance-shopping-plan/score.py → score.png）
- 値段の履歴（Keepa）・セール日程（Amazon）・今あるお小遣い（cases/allowance-shopping-plan/figure.py → cover.png）
- メルカリで比べる中身（cases/allowance-shopping-plan/mercari.py → mercari.png）

描き方の決まりは AGENTS.md「見せ方と図」（矢印＝データが動く向き、1 色、順番が読めることを最優先、
AI の札の下の動詞は fk.verb）。生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
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

LS = 22                       # 線のラベル
PX, GA, HUB, AI = 62, 316, 588, 940   # 列の中心：本人・ChatGPT・Notion・Claude Code
YT, YH, YB = 250, 430, 640    # 行：Claude Code・Notion（と本人・ChatGPT）・メルカリプラグイン
TILE = 104
H = TILE / 2
BEND = HUB + H + 40           # Notion から AI へ曲がる位置（札から横に出て、Notion の下の動詞より右で曲げる）
RIGHT = 1396                  # 出す物の右の辺
PS = .6                       # 本人の大きさ
GAP = 4


def line(x0, x1, y, label):
    """横の線（x0 → x1）のラベルの位置。矢じり（右端の 32px）にかからない範囲で中央に寄せる。"""
    w = fk.width(label, LS)
    x = max(min((x0 + x1) / 2, x1 - 26 - w / 2), x0 + 8 + w / 2)
    return (x, y - LS - 14)


def plan_screen(x1, cy, w=200, h=150):
    """計画画面（右の辺 x1）：買う時期の列（今すぐ・セール・◯月）に商品の四角が並ぶ。
    ai-use-cases の cases/allowance-shopping-plan/cover.png と同じ形を小さくした物。下に名前。左の辺の x を返す。"""
    x, y = x1 - w, cy - h / 2
    fk.rr((x, y, x1, y + h), 'white', fk.TEAL, 3, 12)
    d.rounded_rectangle((x + 2, y + 2, x1 - 2, y + 20), radius=10, fill='#e7eef6')
    cw = (w - 16) / 3
    for k, (name, n) in enumerate(zip(('今すぐ', 'セール', '◯月'), (2, 3, 2))):
        c0 = x + 8 + k * cw
        fk.rr((c0 + 3, y + 28, c0 + cw - 3, y + h - 10), '#f4f7f6', fk.LINE, 2, 8)
        fk.centered(c0 + cw / 2, y + 32, name, 16, fk.TEAL)
        for r in range(n):
            ry = y + 60 + r * 26
            fk.rr((c0 + 12, ry, c0 + cw - 12, ry + 19), fk.NOTE, fk.AMBER, 2, 5)
    fk.centered(x + w / 2, y + h + 12, '計画画面', 25)
    return x


def answer_card(x1, cy, w=124, h=108):
    """チャットの答えの札（右の辺 x1）：吹き出しの中に、候補の印（四角）と文の行。下に名前。左の辺の x を返す。"""
    cx = x1 - w / 2
    x, y = cx - w / 2, cy - h / 2
    tail = [(x + 34, y + h - 2), (x + 34, y + h + 20), (x + 60, y + h - 2)]
    d.polygon(tail, fill='white')
    d.line([tail[0], tail[1], tail[2]], fill=fk.TEAL, width=3, joint='curve')
    fk.rr((x, y, x + w, y + h), 'white', fk.TEAL, 3, 16)
    d.polygon([(x + 36, y + h - 4), (x + 36, y + h + 14), (x + 57, y + h - 4)], fill='white')
    d.line((x + 24, y + 26, x + w - 24, y + 26), fill=fk.LINE, width=6)
    for k in range(2):
        yy = y + 50 + k * 31
        fk.rr((x + 24, yy - 11, x + 46, yy + 11), fk.NOTE, fk.AMBER, 3, 5)
        d.line((x + 56, yy, x + w - 24 - k * 20, yy), fill=fk.LINE, width=6)
    fk.centered(cx, y + h + 26, '提案', 25)
    return x


# ── 左から 1 本の鎖：本人 → ChatGPT（調べて比べる）→ Notion ─────────
fk.person(PX, YH - 20, PS)
fk.centered(PX, YH - 20 + 118 * PS + 10, '本人', 25)
fk.flow([(PX + 68 * PS + 8, YH), (GA - H - GAP, YH)], '用途と条件', at=line(PX + 68 * PS, GA - H, YH, '用途と条件'), size=LS)
fk.service('openai', GA, YH, 'ChatGPT', tile=TILE)
fk.verb(GA, YH + H + 12 + 36, '調べて比べる')
fk.flow([(GA + H + 6, YH), (HUB - H - GAP, YH)], '登録する商品', at=line(GA + H, HUB - H, YH, '登録する商品'), size=LS)
fk.service('notion', HUB, YH, '欲しいもの', tile=TILE)
fk.verb(HUB, YH + H + 12 + 36, '棚卸しして')
fk.verb(HUB, YH + H + 12 + 36 + 32, '点数で並べる')

# ── 上：Notion →（点数順の欲しい物）→ Claude Code（お小遣いで買う月を決める）→ 計画画面 ──
fk.flow([(HUB + H + 6, YH - 22), (BEND, YH - 22), (BEND, YT), (AI - H - GAP, YT)], '点数順の欲しい物',
        at=line(BEND, AI - H, YT, '点数順の欲しい物'), size=LS)
fk.service('claude', AI, YT, 'Claude Code', tile=TILE)
fk.verb(AI, YT + H + 12 + 36, 'お小遣いで買う月を決める')
P_L = plan_screen(RIGHT, YT)
fk.flow([(AI + H + 6, YT), (P_L - GAP, YT)], 'いつ何を買うか', at=line(AI + H, P_L, YT, 'いつ何を買うか'), size=LS)

# ── 下：Notion →（定価つきの欲しい物）→ ChatGPT のメルカリプラグイン（お買い得を探す）→ 提案 ──
GX = AI + 56                  # プラグインの札は横長なので少し右に置き、左の線のラベルの場所を空ける
G_L, G_R = GX - TILE * 1.7 / 2, GX + TILE * 1.7 / 2
fk.flow([(HUB + H + 6, YH + 22), (BEND, YH + 22), (BEND, YB), (G_L - GAP, YB)], '定価つきの欲しい物',
        at=line(BEND, G_L, YB, '定価つきの欲しい物'), size=LS)
fk.plugin('openai', 'mercari', GX, YB, 'メルカリプラグイン', tile=TILE)
fk.verb(GX, YB + H + 12 + 36, 'お買い得を探す')
A_L = answer_card(RIGHT, YB)
fk.flow([(G_R + 6, YB), (A_L - GAP, YB)], 'お買い得の候補', at=line(G_R, A_L, YB, 'お買い得の候補'), size=LS)

fk.save(HERE / 'cover.png')
