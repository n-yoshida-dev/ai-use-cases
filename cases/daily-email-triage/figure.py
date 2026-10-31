"""このケースの cover.png / flow.png を生成する。他ケースの画像には触れない。

    python cases/daily-email-triage/figure.py --font /absolute/path/日本語フォント
    （例）PYTHONPATH=<Pillow の場所> python3 cases/daily-email-triage/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスはロゴの札 fk.service で示す）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
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

# ---- cover.png：一目で分かる入口（題名・注記は入れない。要素は y=60〜840 に置く） ----
fk.begin()

CY = 470          # 左の列（Gmail → ルールで除外 → ChatGPT）の中心。図全体の上下の中心に合わせる
GPT = 624         # ChatGPT の中心 x
LABEL_Y = CY + 66 + 12   # service() が名前を書く高さ。同じ列の名前はここに揃える

# 左：Gmail の新着 → ルールで先に除外（AIを使わない層）
fk.service('gmail', 172, CY, 'Gmail')
fk.arrow([(254, CY), (314, CY)])
fk.funnel(326, CY - 65, 120, 130)
fk.centered(386, LABEL_Y, 'ルールで除外', 25)
fk.arrow([(458, CY), (524, CY)])

# 中央：毎朝動く ChatGPT（2026-10-28 に Claude Code のルーティンから移した）
fk.clock(GPT - 60, CY - 150)
fk.text(GPT - 16, CY - 166, '毎朝6時', 26, fk.BLUE)
fk.service('openai', GPT, CY, 'ChatGPT')
fk.centered(GPT, LABEL_Y + 36, '読んで仕分け', 25)

# 右：仕分け結果の 3 つ（枠＝この結果をもとに通知する）
ROWS = (140, 300, 460)                 # 封筒の上端。行の中心は +43。名前と次の行の札が重ならない間隔
fk.rr((820, 100, 1340, 610), None, fk.LINE, 2, 18)

fk.envelope(860, ROWS[0], 130, 86, fk.AMBER, tag=fk.AMBER)
fk.centered(925, ROWS[0] + 96, '要対応', 28)
fk.arrow([(1002, ROWS[0] + 43), (1070, ROWS[0] + 43)], fk.AMBER, 5)
fk.service('todoist', 1160, ROWS[0] + 43, 'Todoist')

fk.envelope(860, ROWS[1], 130, 86, fk.BLUE, tag=fk.BLUE)
fk.centered(925, ROWS[1] + 96, '要確認', 28)

fk.envelope(860, ROWS[2], 130, 86, fk.GRAY, tag=fk.GRAY)
fk.centered(925, ROWS[2] + 96, '不要', 28)

# 要確認・不要の 2 行は Gmail のラベルを付けるだけ（括弧で 2 行をまとめ、右に書く）
BR = 1030
fk.d.line([(BR, ROWS[1] + 43), (BR + 22, ROWS[1] + 43), (BR + 22, ROWS[2] + 43), (BR, ROWS[2] + 43)],
          fill=fk.GRAY, width=3, joint='curve')
fk.centered(1140, (ROWS[1] + ROWS[2]) / 2 + 43 - 15, 'ラベルのみ', 26, fk.GRAY)

# ChatGPT から 3 本に分かれる（幹 1 本 → 縦に分岐）
TRUNK = 760
fk.arrow([(GPT + 66, CY), (TRUNK, CY), (TRUNK, ROWS[0] + 43), (848, ROWS[0] + 43)])
fk.arrow([(TRUNK, CY), (TRUNK, ROWS[1] + 43), (848, ROWS[1] + 43)])
fk.arrow([(TRUNK, CY), (TRUNK, ROWS[2] + 43), (848, ROWS[2] + 43)])

# 右下：毎朝通知（0件の日も） → 本人が対応
fk.arrow([(1160, 616), (1160, 648)], fk.TEAL, 5)
fk.phone(1120, 654, 80, 140)
fk.centered(1160, 804, '通知', 26)
fk.person(985, 724, .62)
fk.centered(985, 810, '本人が対応', 26)
fk.arrow([(1112, 724), (1035, 724)], fk.BLUE, 5)

# 下：判定基準は毎朝読まれる入力（実線）。直すのは必要なときだけ（薄い点線）
fk.rr((GPT - 160, 700, GPT + 160, 770), fk.NOTE, '#e7ca7c', 2, 12)
fk.centered(GPT, 717, '判定基準（手順書）', 26)
fk.arrow([(GPT, 694), (GPT, 628)], fk.AMBER, 5)
fk.dashed_arrow([(937, 735), (GPT + 174, 735)], fk.FAINT, 4)
fk.centered(862, 696, '必要なら直す', 22, fk.GRAY)

fk.save(HERE / 'cover.png')


# ---- flow.png：必要な説明を補う図 ----
def cards(title, items):
    """fk.cards と同じ並びで、カードの高さを段ごとの行数（2〜3 行）に合わせて詰めたもの（fk.cards は 258px で下が空く）。"""
    fk.begin()
    fk.text(64, 56, title, 40)
    y = 150
    for row in range(0, len(items), 2):
        pair = items[row:row + 2]
        h = 110 + 46 * max(len(lines) for _, lines in pair)
        for i, (label, lines) in enumerate(pair):
            x = 64 + i * 670
            fk.rr((x, y, x + 638, y + h))
            fk.text(x + 28, y + 22, label, 28, fk.TEAL)
            for k, line in enumerate(lines):
                fk.text(x + 28, y + 90 + k * 46, line, 28)
        y += h + 30


cards('メール仕分け：作業と判断の分担', [
    ('課題', ['通知を切ると大事なメールを見落とす', '全部読むにはノイズが多すぎる']),
    ('AIの作業', ['毎朝、未読を読んで3つに仕分ける', '要対応はTodoistへ登録', '続けてTodoistのInboxを整理']),
    ('人間の判断', ['判定基準を手順書に決めておく', 'メールの削除・返信と実際の対応は本人']),
    ('確認すること', ['ラベル付与は移行の前後とも確認', '判定の正確さと時間削減は未測定']),
])
fk.save(HERE / 'flow.png')
