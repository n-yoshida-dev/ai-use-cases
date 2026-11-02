"""このケースの mercari.png（メルカリでお買い得を探す）を生成する。他の画像には触れない。

再生成：リポジトリの root で
    python3 cases/allowance-shopping-plan/mercari.py --font /absolute/path/日本語フォント
（Python 3 / Pillow。部品は scripts/figkit.py、ロゴは scripts/logos/）

ChatGPT のメルカリプラグインが Notion の欲しいもの（定価を含む）を読み、メルカリで探して、
商品の状態と値段を定価と比べ、お買い得の候補を提案する。頼んだときに動く（定期実行ではないので trigger は置かない）。

左から 1 本の鎖：Notion →（定価つきの欲しい物）→ ChatGPT × メルカリ（fk.plugin。1 枚の札）→（お買い得の候補）→ 提案。
メルカリは ChatGPT のプラグインなので、別の「メルカリ」の札は置かない（2026-11-02 本人
「チャット GPT とメルカリのロゴが掛け合わさってるみたいな見せ方が分かりやすい」）。
提案の札は全体像（systems/shopping-plan/figure.py）と同じ絵にそろえる。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
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

SRC, GPT, OUT = 200, 720, 1230   # 左（読まれる側）・中央（AI）・右（出す物）
CY = 300
TILE = 132
H = TILE / 2
LBL = 23
GAP = 4


def answer_card(cx, cy, w=136, h=118):
    """チャットの答えの札：吹き出しの中に、候補の印（四角）と文の行。下に名前。左の辺の x を返す。"""
    x, y = cx - w / 2, cy - h / 2
    tail = [(x + 34, y + h - 2), (x + 34, y + h + 20), (x + 60, y + h - 2)]
    d.polygon(tail, fill='white')
    d.line([tail[0], tail[1], tail[2]], fill=fk.TEAL, width=3, joint='curve')
    fk.rr((x, y, x + w, y + h), 'white', fk.TEAL, 3, 16)
    d.polygon([(x + 36, y + h - 4), (x + 36, y + h + 14), (x + 57, y + h - 4)], fill='white')
    d.line((x + 24, y + 28, x + w - 24, y + 28), fill=fk.LINE, width=6)
    for k in range(2):
        yy = y + 56 + k * 33
        fk.rr((x + 24, yy - 12, x + 48, yy + 12), fk.NOTE, fk.AMBER, 3, 5)
        d.line((x + 60, yy, x + w - 24 - k * 20, yy), fill=fk.LINE, width=6)
    fk.centered(cx, y + h + 28, '提案', 26)
    return x


fk.service('notion', SRC, CY, '欲しいもの', tile=TILE)
G_L, G_R = fk.plugin('openai', 'mercari', GPT, CY, 'メルカリプラグイン', tile=TILE)
fk.verb(GPT, CY + H + 12 + 36, '状態と値段を定価と比べる')
fk.flow([(SRC + H + 6, CY), (G_L - GAP, CY)], '定価つきの欲しい物', size=LBL)
A_L = answer_card(OUT, CY)
fk.flow([(G_R + 6, CY), (A_L - GAP, CY)], 'お買い得の候補', size=LBL)

fk.save(HERE / 'mercari.png')
