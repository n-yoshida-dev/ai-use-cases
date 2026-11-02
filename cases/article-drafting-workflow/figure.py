"""このケースの cover.png（下書きから投稿まで）を生成する。他ケースの画像には触れない。

    python cases/article-drafting-workflow/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/article-drafting-workflow/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスのロゴは scripts/logos/）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。

作業の順番を見せる図。左から右への 1 本の鎖だけで描き、並んで走る矢印を置かない（2026-11-02 本人「平行してる矢印が多すぎると、
なんか順番がわかんなくなる」）：ネタ → 本人（声で肉付け）→ Claude Code（下書きを書く）→ 本人（読んで直す）→ Qiita・note。
本人は途中で 2 回関わるので、関わる段ごとに置く（AGENTS.md の例外）。矢印 1 本＝データが動く向き、ラベルは渡る物の名詞、動詞は札の下。
本人の直しを文章の原則と NG 辞書に積み上げる流れ、Qiita の記事を note 版に直す流れは、別の仕組みなのでこの図に混ぜない
（2026-11-02 本人「役割がちょっとごちゃつきすぎててよくわかんない」「分けてもいいんじゃないか」）。README の本文に書く。
左端は記事の種類を問わない「ネタ」（フォルダの絵）。ネタの出どころ（ネタ帳・ai-use-cases・Notion の購入判断ノート）は記事の種類で変わるので、
この図では種類で分けず 1 枚にまとめる（全部の記事がネタ帳から来るように見せないため）。
出す先は記事の種類で変わる（2026-11-02 本人：商品紹介は note だけ、技術記事は Qiita だけ、AI の活用は Qiita のあと note 版にも）ので、
最後だけ「直した記事」を Qiita と note の 2 つ（上下）に分ける。並ぶ出力 2 本は AGENTS.md の範囲内。種類ごとの出し分けは README に書く。
Qiita への限定共有の投稿は Claude Code が API で行い、本人が画像を貼って公開する。図では本人の直しのあと出す先に届く線にまとめ、細部は README に書く。
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

fk.begin()

CY = 300            # 鎖の高さ（矢印はすべてこの線の上）
GAP = 10
PS = .8             # 人の大きさ（外形は x±68s、y-84s〜y+118s）
PW = 68 * PS
NAME = CY + 92      # どの札も名前をこの高さにそろえ、その下に作業（灰色）を書く


def person(cx, act):
    """本人：胴の中ほどが鎖の高さに来るように置き、下に名前と、その段でする作業（灰色）を書く。"""
    py = CY - (118 - 84) * PS / 2          # 外形の上下の中心を CY に合わせる
    fk.person(cx, py, PS)
    fk.centered(cx, NAME, '本人', 25)
    fk.verb(cx, NAME + 36, act)
    return cx - PW, cx + PW


# ネタ（記事の種類を問わない）
NX = 110
fk.folder(NX - 53, CY - 45)
fk.centered(NX, NAME, 'ネタ', 25)

# 本人（声で肉付け）
P1 = 370
p1l, p1r = person(P1, '声で肉付け')
fk.flow([(NX + 53 + GAP, CY), (p1l - GAP, CY)], '題材')

# Claude Code（下書きを書く）
CX, T = 660, 130
fk.service('claude', CX, CY, tile=T)
fk.centered(CX, NAME, 'Claude Code', 25)
fk.verb(CX, NAME + 36, '下書きを書く')
fk.flow([(p1r + GAP, CY), (CX - T / 2 - GAP, CY)], '話した中身')

# 本人（読んで直す）
P2 = 950
p2l, p2r = person(P2, '読んで直す')
fk.flow([(CX + T / 2 + GAP, CY), (p2l - GAP, CY)], '下書き')

# 出す先：Qiita（上）と note（下）。「直した記事」は分かれる前の幹に 1 回だけ書く
QX, QT = 1330, 110
QY, NY = CY - 120, CY + 120
VX = 1170                      # 分かれる位置
SX = p2r + GAP
fk.centered((SX + VX) / 2 - 6, CY - 37, '直した記事', 23, fk.TEAL)
for name, label, y in (('qiita', 'Qiita', QY), ('note', 'note', NY)):
    fk.service(name, QX, y, label, tile=QT)
    fk.flow([(SX, CY), (VX, CY), (VX, y), (QX - QT / 2 - GAP, y)])

fk.save(HERE / 'cover.png')
