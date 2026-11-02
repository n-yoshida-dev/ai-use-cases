"""このケースの note.png（note 版に書き直す）を生成する。他の画像には触れない。

再生成：リポジトリの root で
    python3 cases/article-drafting-workflow/note.py --font /absolute/path/日本語フォント
（Python 3 / Pillow。部品は scripts/figkit.py、ロゴは scripts/logos/）

AI の活用の記事だけの流れ。左から右への 1 本の鎖：
Qiita →［記事の本文］→ Claude Code（体験談中心に直す）→［note 版の下書き］→ 本人（読んで直す）→［直した note 版］→ note。
渡る物は線のラベルに書き、置き場の絵を挟まない（cover.png の「下書き」と同じ型）。動詞・ラベルは
systems/article-writing/cover.png とそろえる。
本人の言葉（2026-11-02）：「キータに書いた後、ノート版に文章を直して、まあ、また加筆修正してノートに展開するよね」。
note 版を体験談中心にし、作り方は Qiita の記事へのリンクにするのは本人の決定（2026-10-27）。
cover.png と同じ並べ方（名前の高さをそろえ、作業を灰色で下に書く）。

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

CY = 300            # 鎖の高さ（矢印はすべてこの線の上）
GAP = 10
PS = .8             # 人の大きさ（外形は x±68s、y-84s〜y+118s）
NAME = CY + 92      # どの札も名前をこの高さにそろえ、その下に作業（灰色）を書く


def named(cx, name, act=None):
    fk.centered(cx, NAME, name, 25)
    if act:
        fk.verb(cx, NAME + 36, act)


# Qiita（公開した記事）
QX, QT = 140, 110
fk.service('qiita', QX, CY, tile=QT)
named(QX, 'Qiita')

# Claude Code（体験談中心に直す）
CX, T = 560, 130
fk.service('claude', CX, CY, tile=T)
named(CX, 'Claude Code', '体験談中心に直す')
fk.flow([(QX + QT / 2 + GAP, CY), (CX - T / 2 - GAP, CY)], '記事の本文')

# 本人（読んで直す）
PX = 960
fk.person(PX, CY - 17 * PS, PS)
named(PX, '本人', '読んで直す')
fk.flow([(CX + T / 2 + GAP, CY), (PX - 68 * PS - GAP, CY)], 'note 版の下書き')

# note
NX, NT = 1300, 110
fk.service('note', NX, CY, tile=NT)
named(NX, 'note')
fk.flow([(PX + 68 * PS + GAP, CY), (NX - NT / 2 - GAP, CY)], '直した note 版')

fk.save(HERE / 'note.png')
