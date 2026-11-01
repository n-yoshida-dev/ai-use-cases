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
fk.begin()

# 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。線は fk.flow() だけ。
# 読まれる側（入力）を左、ChatGPT を中央、書かれる側（出力）を右。読み書き両方の正本は左右に 2 回置く。
# ChatGPT の札は 3 枚：上が毎週の読書レビュー、中が本人の会話での記録（定期実行ではないので時計なし）、
# 下が毎週のコンテキスト更新。読書レビューは personal-ai-context へ書き戻さない（右の personal-ai-context へは下の札からだけ）。
# 本人は下の中央寄り。reading-log から「次に読む本」を受け取り、右の 3 枚へ会話を渡す。
LX, GX, RX = 220, 820, 1260      # 左：読まれる側、中：ChatGPT、右：書かれる正本
AY, BY, UY = 165, 405, 712       # 読書レビュー・会話で記録・コンテキスト更新の段
CY, RY = 130, 345                # 左の personal-ai-context・reading-log
PX, PY = 430, 650                # 本人
HALF = 66
GL, GR = GX - HALF, GX + HALF    # ChatGPT の札の左右の端
PR = PX + 54 + 14                # 本人の右（線の根元）


def lock(lx, ly, c=fk.BLUE):
    """非公開の印。札の角に付ける小さな錠。"""
    fk.d.arc((lx - 11, ly - 26, lx + 11, ly - 2), 180, 360, fill=c, width=5)
    fk.rr((lx - 16, ly - 10, lx + 16, ly + 16), 'white', c, 3, 6)
    fk.d.ellipse((lx - 4, ly - 1, lx + 4, ly + 7), fill=c)


def store(name, x, y, private=False, lock_side=-1):
    """正本の札（GitHub のロゴ）。名前は札の上。錠は lock_side（-1 左下・1 右下）の角。"""
    fk.service('github', x, y)
    fk.centered(x, y - HALF - 46, name, 25)
    if private:
        lock(x + lock_side * (HALF - 2), y + HALF - 12)


def chatgpt(y, verb, when=None):
    """ChatGPT の札。きっかけ（定期実行のときだけ）は真上、名前と動詞は下。"""
    fk.service('openai', GX, y, 'ChatGPT')
    if when:
        fk.trigger(GX, y - HALF, when)
    fk.centered(GX, y + HALF + 52, verb, 24, fk.GRAY)


store('personal-ai-context', LX, CY, True)
store('reading-log', LX, RY)
store('reading-log', RX, AY)
store('personal-ai-context', RX, UY, True, 1)

chatgpt(AY, '読んで順位付け', '毎週')
chatgpt(BY, '会話で記録')
chatgpt(UY, '差分を整理', '毎週')

# 読書レビュー：入力（左・本人 → 上の ChatGPT）
fk.flow([(LX + HALF, AY - 40), (GL, AY - 40)], '長期の文脈', color=fk.BLUE)
fk.flow([(LX + HALF, RY), (470, RY), (470, AY), (GL, AY)], '読書記録', at=(378, RY - 37), color=fk.BLUE)
fk.flow([(PR, 590), (560, 590), (560, AY + 40), (GL, AY + 40)], '今週の会話', at=(632, 300), color=fk.AMBER)

# 読書レビュー：出力（上の ChatGPT → 右の reading-log）。1 本 1 データ
fk.flow([(GR, AY - 30), (RX - HALF, AY - 30)], '読む順位')
fk.flow([(GR, AY + 30), (RX - HALF, AY + 30)], '週次レビュー', at=((GR + RX - HALF) / 2, AY + 42))

# 会話で記録：本人の進捗・感想 → 中の ChatGPT → 右の reading-log（下から入る）
fk.flow([(PR, 632), (660, 632), (660, BY), (GL, BY)], '進捗・感想', at=(579, 644), color=fk.AMBER)
fk.flow([(GR, BY), (RX, BY), (RX, AY + HALF + 14)], '進捗・感想')

# コンテキスト更新：本人の会話 → 下の ChatGPT → 右の personal-ai-context
fk.flow([(PR, UY), (GL, UY)], '会話', at=((PR + GL) / 2, UY + 12), color=fk.AMBER)
fk.flow([(GR, UY), (RX - HALF, UY)], '会話の差分')

# 本人：reading-log の本棚を見て読む
fk.person(PX, PY, .8)
fk.centered(PX, PY + 94 + 10, '本人', 25)
fk.flow([(LX, RY + HALF + 14), (LX, PY), (PX - 54 - 14, PY)], '次に読む本', at=(292, 520), color=fk.GRAY)

fk.save(Path(__file__).with_name('cover.png'))
