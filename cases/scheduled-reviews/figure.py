"""このケースの cover.png / flow.png を生成する。他ケースの画像には触れない。

    python cases/scheduled-reviews/figure.py --font /absolute/path/日本語フォント
    例：python3 cases/scheduled-reviews/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

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


def bubble(x, y, w, h, label, c=fk.TEAL):
    """吹き出し（会話）。右下に小さな尾を出す。"""
    fk.rr((x, y, x + w, y + h), 'white', c, 3, 18)
    fk.d.polygon([(x + w - 44, y + h - 3), (x + w - 14, y + h - 3), (x + w - 6, y + h + 22)], fill='white')
    fk.d.line((x + w - 42, y + h - 1, x + w - 16, y + h - 1), fill='white', width=5)
    fk.d.line([(x + w - 44, y + h - 1), (x + w - 6, y + h + 22), (x + w - 14, y + h - 1)], fill=c, width=3, joint='curve')
    fk.centered(x + w / 2, y + h / 2 - 15, label, 24, c)


# ---- cover.png：一目で分かる入口 ----
fk.begin()

# 上：決めた周期で動く（時計と 2 つの時刻）
fk.clock(680, 112, 36)
fk.text(730, 88, '毎週日曜', 30, fk.BLUE)
fk.text(732, 130, '20:30・22:00', 22, fk.BLUE)

# 中央：ChatGPT のスケジュールが記録と会話を確認・分析する
fk.service('openai', 680, 300, 'ChatGPT')

# 左：記録（GitHub のリポジトリ）。ChatGPT が取りに行って読み（pull）、結果を保存する（arrow）
fk.service('github', 210, 300, 'GitHub')
fk.pull([(614, 268), (276, 268)])
fk.centered(445, 222, '読む', 24, fk.TEAL)
fk.arrow([(614, 330), (276, 330)])
fk.centered(445, 340, '保存', 24, fk.TEAL)

# 左上：もう 1 つの入力。会話（コンテキスト更新）は別の定期処理なので、記録の矢印とはつながない
bubble(400, 92, 140, 80, '会話')
fk.arrow([(548, 196), (606, 232)])

# 右：レビュー結果を本人へ報告し、本人が判断する
fk.doc(960, 221, 140, 158, fk.TEAL)
fk.centered(1030, 410, 'レビュー結果', 26)
fk.arrow([(750, 300), (950, 300)])
fk.centered(850, 258, '報告', 24, fk.TEAL)
fk.person(1250, 290, .72)
fk.centered(1250, 390, '本人', 26)
fk.arrow([(1110, 300), (1175, 300)], fk.BLUE, 5)

# 下：本人が目的・周期・判断基準を決める（arrow）。ChatGPT はそれを取りに行って読む（pull）
fk.rr((460, 585, 900, 655), fk.NOTE, '#e7ca7c', 2, 12)
fk.centered(680, 600, '目的・周期・判断基準', 24)
fk.arrow([(1250, 446), (1250, 620), (910, 620)], fk.AMBER, 5)
fk.pull([(680, 424), (680, 580)], fk.AMBER, 5)
fk.text(706, 486, '設定', 24, fk.AMBER)

fk.save(HERE / 'cover.png')

# ---- flow.png：必要な説明を補う図 ----
fk.cards('定期レビュー：作業と判断の分担', [
    ('課題', ['定期確認や情報収集のたびに', '人間が依頼・確認を繰り返す']),
    ('AIの作業', ['最新の記録・情報を確認し分析する', '許可した範囲へ保存・更新・報告']),
    ('人間の判断', ['目的・周期・判断基準を設定する', '提案の採否と次の行動を決める']),
    ('周期', ['読書レビュー：毎週日曜 20:30', 'コンテキスト更新：毎週日曜 22:00', '取得・保存の失敗は明示する']),
])
fk.save(HERE / 'flow.png')
