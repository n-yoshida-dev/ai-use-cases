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

CTX, GPT, LOG = 260, 720, 1180   # 左：personal-ai-context、中：ChatGPT、右：reading-log
TY = 250                          # 札の中心 y（札は 184〜316）
HALF = 66


def lock(lx, ly, c=fk.BLUE):
    """非公開の印。札の角に付ける小さな錠。"""
    fk.d.arc((lx - 11, ly - 26, lx + 11, ly - 2), 180, 360, fill=c, width=5)
    fk.rr((lx - 16, ly - 10, lx + 16, ly + 16), 'white', c, 3, 6)
    fk.d.ellipse((lx - 4, ly - 1, lx + 4, ly + 7), fill=c)


# 三つの札。名前は札の上に置く（下から矢印を入れるため）
fk.service('github', CTX, TY)
fk.centered(CTX, TY - HALF - 46, 'personal-ai-context', 25)
lock(CTX - HALF + 2, TY + HALF - 12)   # 左下の角（右下だと矢じりに近い）

fk.service('openai', GPT, TY)
fk.centered(GPT, TY - HALF - 46, 'ChatGPT', 25)
fk.clock(GPT + 120, TY - HALF - 30, 26)
fk.text(GPT + 158, TY - HALF - 47, '毎週', 25, fk.BLUE)

fk.service('github', LOG, TY)
fk.centered(LOG, TY - HALF - 46, 'reading-log', 25)

# personal-ai-context ⇄ ChatGPT：読むのは ChatGPT が取りに行く（pull）、更新は書き込む（arrow）
fk.pull([(GPT - HALF, TY - 16), (CTX + HALF, TY - 16)], fk.BLUE)
fk.centered((CTX + GPT) / 2, TY - 60, '読む', 24, fk.BLUE)
fk.arrow([(GPT - HALF, TY + 26), (CTX + HALF, TY + 26)], fk.TEAL)
fk.centered((CTX + GPT) / 2, TY + 38, '会話の差分を更新', 24, fk.TEAL)   # 元は会話。読書レビューは書き戻さない

# reading-log ⇄ ChatGPT：同じく読むは pull、記録は arrow（gap を負にして細い線を内側に揃える）
fk.pull([(GPT + HALF, TY - 16), (LOG - HALF, TY - 16)], fk.BLUE, gap=-9)
fk.centered((GPT + LOG) / 2, TY - 60, '読む', 24, fk.BLUE)
fk.arrow([(GPT + HALF, TY + 26), (LOG - HALF, TY + 26)], fk.TEAL)
fk.centered((GPT + LOG) / 2, TY + 38, '順位・感想を記録', 24, fk.TEAL)   # 本人の感想も会話経由で reading-log へ

# 本人：reading-log を見て読み、感想を ChatGPT に話す（ChatGPT が reading-log へ記録する往復）
PY = 580
fk.person(GPT, PY, .8)
fk.arrow([(LOG, TY + HALF + 14), (LOG, PY), (GPT + 68, PY)], fk.GRAY)
fk.text(LOG + 22, (TY + HALF + PY) / 2 - 16, '見る', 24, fk.GRAY)
fk.arrow([(GPT, PY - 80), (GPT, TY + HALF + 14)], fk.AMBER)
fk.text(GPT + 22, (TY + HALF + PY - 80) / 2 - 16, '感想を話す', 24, fk.AMBER)

fk.save(Path(__file__).with_name('cover.png'))
