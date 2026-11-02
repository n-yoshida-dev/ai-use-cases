"""この全体構成の cover.png（記事の種類でネタの出どころと出す先が変わる）を生成する。他の画像には触れない。

再生成：リポジトリの root で
    python3 systems/article-writing/figure.py --font /absolute/path/日本語フォント
（Python 3 / Pillow。部品は scripts/figkit.py、ロゴは scripts/logos/）

記事の種類ごとに 1 行。行どうしは交わらず、各行は左から右への 1 本の鎖（ネタの出どころ → Claude Code → 出す先）。
- 商品紹介：Notion の購入判断ノート → Claude Code（書く）→ note
- AI の活用：GitHub のネタ帳と ai-use-cases → Claude Code（書く）→ Qiita → Claude Code（体験談中心に直す）→ note
- 技術記事：GitHub のネタ帳 → Claude Code（書く）→ Qiita
本人の言葉（2026-11-02）：「商品紹介ってノートにしか公開しませんよ。つまり、キータは関係ないです。（略）キータに書いた後、
ノート版に文章を直して、まあ、また加筆修正してノートに展開するよね。（略）キータにしか書けない本当の技術記事みたいなのがあるけど、
まあ、それは、まあ、ノートは関係なかったりする」。購入判断ノート・ai-use-cases もネタになることは同日の本人の指摘。
本人の声・本人の直しは全部の行に共通なので、この図には描かない（下書きから投稿までは cases/article-drafting-workflow/cover.png、
note 版は同じフォルダの note.png に任せる）。
AI の活用の入力 2 つは同じ Claude Code に同時に入るので上下に並べる（AGENTS.md：同時に入る入力は 3 本まで）。
列をそろえる：Claude Code（書く）は全行で同じ列、Qiita は AI の活用と技術記事で同じ列、note は右端の列。商品紹介の線は空いた列を素通りして note へ届く。

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

SRC, CC, QI, CC2, NO = 270, 540, 790, 1070, 1340   # 列の中心：出どころ・Claude Code・Qiita・Claude Code・note
LANES = (120, 400, 690)                           # 行：商品紹介・AI の活用・技術記事（AI の活用は入力 2 つ分の高さ）
SPLIT = 72                                        # AI の活用の入力 2 つの、行の高さからの上下のずれ
T = 96                                            # サービスの札
LBL = 22
GAP = 6


def tile(name, cx, cy, label):
    fk.service(name, cx, cy, label, tile=T)


def link(x0, x1, y, label=None):
    fk.flow([(x0 + T / 2 + GAP, y), (x1 - T / 2 - GAP, y)], label, size=LBL)


def verb(cx, cy, s):
    fk.verb(cx, cy + T / 2 + 12 + 36, s)


# 行：(種類, 出どころの並び, [(線のラベル, 札, 列, 札の名前, 動詞), ...])
# 出どころの並びは (札, 名前, 線のラベル)。空なら描かない。
ROWS = (
    ('商品紹介', [('notion', '購入判断ノート', '判断の記録')],
     [('claude', CC, 'Claude Code', '書く'), ('記事', 'note', NO, 'note', None)]),
    ('AI の活用', [('github', 'ネタ帳', '題材'), ('github', 'ai-use-cases', '活用事例')],
     [('claude', CC, 'Claude Code', '書く'), ('記事', 'qiita', QI, 'Qiita', None),
      ('記事の本文', 'claude', CC2, 'Claude Code', '体験談中心に直す'), ('note 版', 'note', NO, 'note', None)]),
    ('技術記事', [('github', 'ネタ帳', '題材')],
     [('claude', CC, 'Claude Code', '書く'), ('記事', 'qiita', QI, 'Qiita', None)]),
)

for k, (y, (kind, sources, stops)) in enumerate(zip(LANES, ROWS)):
    if k:   # 行の境目に細い罫線
        mid = (LANES[k - 1] + y) / 2 + (10 if k == 1 else 34)
        d.line((56, mid, 1440 - 56, mid), fill=fk.LINE, width=2)
    fk.text(56, y - 20, kind, 28)
    (name, cx, name_label, act), rest = stops[0], stops[1:]
    tile(name, cx, y, name_label)
    verb(cx, y, act)
    if len(sources) == 1:
        src, src_label, label = sources[0]
        tile(src, SRC, y, src_label)
        link(SRC, cx, y, label)
    elif sources:   # 同じ Claude Code に同時に入る入力 2 つ：上下に置き、横に出てから斜めに Claude Code の左辺へ
        bend = (SRC + cx) / 2 + 20
        for (src, src_label, label), dy in zip(sources, (-SPLIT, SPLIT)):
            sy = y + dy
            tile(src, SRC, sy, src_label)
            x0 = SRC + T / 2 + GAP
            fk.flow([(x0, sy), (bend, sy), (cx - T / 2 - GAP, y + dy / 3)], label, size=LBL,
                    at=((x0 + bend) / 2, sy - LBL - 14))
    x = cx
    for label, name, cx, name_label, act in rest:
        link(x, cx, y, label)
        tile(name, cx, y, name_label)
        if act:
            verb(cx, y, act)
        x = cx

fk.save(HERE / 'cover.png')
