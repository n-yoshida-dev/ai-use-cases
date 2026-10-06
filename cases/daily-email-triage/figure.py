"""このケースの cover.png / flow.png を生成する。他ケースの画像には触れない。

    python cases/daily-email-triage/figure.py --font /absolute/path/日本語フォント

Python 3 / Pillow。部品は scripts/figkit.py。生成後は欠字・はみ出し・重なりを目視確認する。
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

# ---- cover.png：一目で分かる入口 ----
fk.begin('毎朝のメール仕分けをAIに任せる', '人が基準を決める → AIが読んで仕分け、必要な日だけ知らせる')

# 左：たまっていく新着メール
for x, y, c in [(84, 322, fk.BLUE), (214, 268, fk.AMBER), (128, 424, fk.TEAL), (250, 388, fk.BLUE)]:
    fk.envelope(x, y, 130, 86, c)
fk.centered(232, 545, '毎日の新着メール', 30)

# ルールで先に除外（AIを使わない層）
fk.funnel(462, 348)
fk.centered(517, 490, 'ルールで除外', 26)
fk.arrow([(398, 408), (450, 408)])
fk.arrow([(584, 408), (630, 408)])

# 中央：毎朝動くClaude
fk.clock(700, 262)
fk.text(748, 244, '毎朝7時', 26, fk.BLUE)
fk.laptop(655, 325, 210, 162)
fk.centered(760, 533, 'Claude', 32, fk.TEAL)
fk.centered(760, 578, '読んで仕分け', 29)

# 右：仕分け結果（枠＝この結果をもとに通知する）
fk.rr((966, 228, 1370, 574), None, fk.LINE, 2, 18)
fk.envelope(1010, 270, 130, 86, fk.AMBER, tag=fk.AMBER)
fk.centered(1075, 366, '要対応', 28)
fk.checklist(1218, 252)
fk.centered(1270, 378, 'Todoistに登録', 26)
fk.arrow([(1162, 313), (1206, 313)], fk.AMBER, 5)

fk.envelope(1010, 432, 130, 86, fk.BLUE, tag=fk.BLUE)
fk.centered(1075, 528, '要確認', 28)
fk.centered(1270, 462, 'ラベルのみ', 26, fk.GRAY)

fk.arrow([(894, 380), (930, 380), (930, 313), (998, 313)])
fk.arrow([(894, 440), (930, 440), (930, 475), (998, 475)])

# 右下：必要な日だけ通知 → 本人が対応
fk.phone(1246, 606, 80, 140)
fk.centered(1286, 752, '通知', 26)
fk.arrow([(1286, 576), (1286, 600)], fk.TEAL, 5)
fk.person(1096, 668, .62)
fk.centered(1096, 752, '本人が対応', 26)
fk.arrow([(1234, 676), (1160, 676)], fk.BLUE, 5)

# 下：判定基準は毎朝読まれる入力（実線）。直すのは必要なときだけ（薄い点線）
fk.rr((500, 664, 800, 735), fk.NOTE, '#e7ca7c', 2, 12)
fk.centered(650, 681, '判定基準（手順書）', 26)
fk.arrow([(640, 658), (640, 534)], fk.AMBER, 5)
fk.dashed_arrow([(1032, 700), (814, 700)], fk.FAINT, 4)
fk.centered(923, 656, '必要なときだけ直す', 22, fk.GRAY)

fk.footer('設定・ラベル付与・タスク登録を確認 ／ 判定の正確さ・効果は未測定')
fk.save(HERE / 'cover.png')

# ---- flow.png：必要な説明を補う図 ----
fk.cards('メール仕分け：作業と判断の分担', '設定と出力を確認 ／ 判定の正確さ・効果は未測定', [
    ('課題', ['通知を切ると大事なメールを見落とす', '全部読むにはノイズが多すぎる']),
    ('AIの作業', ['毎朝、未読を読んで3つに仕分ける', '要対応はTodoistへ登録、該当日だけ通知']),
    ('人間の判断', ['判定基準を手順書に決めておく', '削除・整理と実際の対応は本人が行う']),
    ('確認すること', ['ラベル付与とタスク登録は確認済み', '判定の正確さと時間削減は未測定']),
])
fk.save(HERE / 'flow.png')
