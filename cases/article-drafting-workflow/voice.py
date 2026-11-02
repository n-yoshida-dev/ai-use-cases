"""このケースの voice.png（直すほど自分の文体になる）を生成する。他の画像には触れない。

再生成：リポジトリの root で
    python3 cases/article-drafting-workflow/voice.py --font /absolute/path/日本語フォント
（Python 3 / Pillow。部品は scripts/figkit.py、ロゴは scripts/logos/）

左から右への 1 本の鎖：本人（読んで直す）→ Claude Code（原則と辞書に足す）→ GitHub（文章の原則・NG 辞書）→ Claude Code（次の下書きを書く）。
直す前の状態を残し、直した後との差分と会話の指示を、本人の文章の原則と NG 辞書（textlint）に足す（このケースの README）。
同じ Claude Code に戻る往復は描かず、右端に次の下書きを書く Claude Code をもう一度置く（AGENTS.md「往復・両端の矢印は描かない」）。
下書きの流れとは別の仕組みなので、別の図にした（2026-11-02 本人「役割がちょっとごちゃつきすぎててよくわかんない」「分けてもいいんじゃないか」）。
「直しの差分」は本人が意味を読み取れなかった言葉なので（同日「直しの差分っていうのもなんか別途あるけど」）、線のラベルは「直したところ」にした。

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
T = 130


def named(cx, name, act=None):
    fk.centered(cx, NAME, name, 25)
    if act:
        fk.verb(cx, NAME + 36, act)


# 本人（読んで直す。下書きから投稿までの図と同じ動詞）
PX = 150
fk.person(PX, CY - 17 * PS, PS)
named(PX, '本人', '読んで直す')

# Claude Code（原則と辞書に足す）
C1 = 530
fk.service('claude', C1, CY, tile=T)
named(C1, 'Claude Code', '原則と辞書に足す')
fk.flow([(PX + 68 * PS + GAP, CY), (C1 - T / 2 - GAP, CY)], '直したところ')

# GitHub（文章の原則・NG 辞書）
GX = 910
fk.service('github', GX, CY, tile=T)
named(GX, '原則・NG 辞書')
fk.flow([(C1 + T / 2 + GAP, CY), (GX - T / 2 - GAP, CY)], '新しい決まり')

# 次の下書きを書く Claude Code
C2 = 1290
fk.service('claude', C2, CY, tile=T)
named(C2, 'Claude Code', '次の下書きを書く')
fk.flow([(GX + T / 2 + GAP, CY), (C2 - T / 2 - GAP, CY)], '文章の決まり')

fk.save(HERE / 'voice.png')
