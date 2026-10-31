"""全体概念図（daily-task-hub）。入力（Gmail・ブックマーク・iPhone の音声・手入力）を
ChatGPT と Todoist に集め、本人が確認して動くまでの流れ。
Gmail・ブックマーク・iPhone の音声は ChatGPT を通って Todoist へ、手入力だけ直接 Todoist へ入る。

再生成:
    cd <ai-use-cases のルート>
    python3 systems/daily-task-hub/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
（フォントは位置引数でも渡せる: python3 systems/daily-task-hub/figure.py /path/to/font.ttf）
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import figkit as fk

ap = argparse.ArgumentParser()
ap.add_argument('font_pos', nargs='?')
ap.add_argument('--font')
a = ap.parse_args()
fk.init(a.font or a.font_pos)
fk.begin()

# 左右の余白はどちらも約 76px（左端はブックマークの文字、右端は本人の体）

# ── 入力（左の列） ─────────────────────────────────────────
GM = (154, 160)       # Gmail
BM = (154, 322)       # ブックマーク（頼んだ時だけ）
VO = (154, 490)       # iPhone の音声（ChatGPT の音声モード経由）
MA = (154, 677)       # 手入力（直接 Todoist）

fk.service('gmail', *GM, 'Gmail')

bx, by = BM
fk.d.polygon([(bx - 22, by - 34), (bx + 22, by - 34), (bx + 22, by + 30), (bx, by + 16), (bx - 22, by + 30)], fill=fk.TEAL)
fk.centered(bx, by + 48, 'ブックマーク', 25)

vx, vy = VO
fk.phone(vx - 42, vy - 72)
fk.centered(vx, vy + 86, 'iPhone 音声', 25)

mx, my = MA
fk.rr((mx - 78, my - 52, mx + 78, my + 52), 'white', fk.BLUE, 3)
fk.d.line((mx - 60, my - 26, mx + 60, my - 26), fill=fk.LINE, width=5)
fk.d.line((mx - 60, my - 3, mx + 38, my - 3), fill=fk.LINE, width=5)
fk.d.polygon([(mx + 54, my + 20), (mx + 64, my + 30), (mx + 32, my + 55), (mx + 20, my + 58), (mx + 24, my + 46)], fill=fk.AMBER)
fk.centered(mx, my + 66, '手入力', 25)

# ── ChatGPT（毎朝の処理と、頼んだ時・音声の窓口。同じ ChatGPT なので 1 つ） ──
CG = (544, 260)
cgx, cgy = CG
CGT = 170
cgl, cgr, cgt, cgb = cgx - CGT / 2, cgx + CGT / 2, cgy - CGT / 2, cgy + CGT / 2
fk.service('openai', cgx, cgy, 'ChatGPT', tile=CGT)
fk.clock(cgr, cgt, 30)
fk.text(cgr + 40, cgt - 16, '毎朝6:00', 26, fk.BLUE)

# Gmail → ChatGPT（読む）：左の上段に入る
fk.arrow([(GM[0] + 66, GM[1]), (404, GM[1]), (404, cgy - 50), (cgl - 6, cgy - 50)])
fk.centered(334, GM[1] - 42, '読む', 23, fk.TEAL)
# ブックマーク ⇢ ChatGPT（頼んだ時だけ）：左の中段に入る
fk.dashed_arrow([(bx + 30, by), (344, by), (344, cgy), (cgl - 6, cgy)])
fk.centered(284, by - 40, '頼んだ時', 23, fk.AMBER)
# iPhone 音声 → ChatGPT（音声モードで頼む）：左の下段に入り、ChatGPT → Todoist に合流する
fk.arrow([(vx + 48, vy), (384, vy), (384, cgy + 50), (cgl - 6, cgy + 50)], fk.BLUE)
fk.centered(293, vy - 40, 'その場で', 23, fk.BLUE)

# ── Todoist（タスクの集まる場所） ──────────────────────────
TD = (954, 540)
tdx, tdy = TD
TDT = 170
tdl, tdr, tdt, tdb = tdx - TDT / 2, tdx + TDT / 2, tdy - TDT / 2, tdy + TDT / 2
fk.service('todoist', tdx, tdy, 'Todoist', tile=TDT)

# ChatGPT → Todoist（登録・整理）
fk.arrow([(cgr + 6, cgy - 25), (tdx - 40, cgy - 25), (tdx - 40, tdt - 6)])
fk.text(tdx - 28, 330, '登録・整理', 23, fk.TEAL)
# Todoist → ChatGPT（読む）
fk.arrow([(tdl - 6, tdy - 30), (774, tdy - 30), (774, cgy + 35), (cgr + 6, cgy + 35)])
fk.text(786, 392, '読む', 23, fk.TEAL)

# 手入力 → Todoist（直接入る）。音声の横線（y=490）より 100px 下を通し、別の線と分かるようにする。
# 曲がる位置は図の下中央が空かないよう右寄り（x=700）。「読む」の縦線（x=774）とは交わらない
JX = 700
fk.arrow([(mx + 84, my), (JX, my), (JX, tdy + 50), (tdl - 6, tdy + 50)], fk.BLUE)

# ── 本人 ────────────────────────────────────────────────
# 本人は図の縦の中央に置き、Todoist から 1 回曲がりの矢印で右上に届ける（右上の角が空かないように）
PX = 1314
PY = 390
KX = 1180
fk.arrow([(tdr + 6, tdy), (KX, tdy), (KX, PY), (PX - 80, PY)])
fk.centered((tdr + KX) / 2, tdy - 42, '確認・実行', 23, fk.TEAL)
fk.person(PX, PY, .75)
fk.centered(PX, PY + 102, '本人', 25)

fk.save(Path(__file__).with_name('cover.png'))
