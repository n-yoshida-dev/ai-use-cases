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
    """吹き出し（会話）。尾は上の辺の左から、何も無い左上へ出す（ほかの札を指さない）。"""
    fk.rr((x, y, x + w, y + h), 'white', c, 3, 18)
    tail = [(x + 42, y + 2), (x + 10, y - 16), (x + 18, y + 2)]
    fk.d.polygon(tail, fill='white')
    fk.d.line(tail, fill=c, width=3, joint='curve')
    fk.d.line((x + 21, y + 1, x + 39, y + 1), fill='white', width=4)
    fk.centered(x + w / 2, y + h / 2 - 17, label, 24, c)


# ---- cover.png：一目で分かる入口 ----
# 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。左＝読まれる側、中央＝ChatGPT、右＝書かれる側。
# 本人は読まれる（レビューの指示）と受け取る（レビュー結果）の両方なので札の真下に置き、
# 入る線を札の左の辺、出る線を札の右の辺に付ける。
fk.begin()

AX, AY, T = 720, 380, 200          # ChatGPT の札の中心と大きさ
L, R = AX - T // 2, AX + T // 2    # 札の左右の辺

# 上：きっかけ（毎週日曜の 2 つの定期処理）
fk.trigger(AX, AY - T // 2, '毎週日曜 20:30・22:00')

# 中央：ChatGPT（動詞は札の下に 1 行）
bottom = fk.service('openai', AX, AY, 'ChatGPT', tile=T)
fk.centered(AX, bottom + 52, '確認して分析', 24, fk.GRAY)

# 左：読まれる側。会話（コンテキスト更新）と GitHub の記録は別の定期処理なので、線は別々に引く
bubble(300, 277, 140, 76, '会話')
fk.flow([(440, 315), (L, 315)], '会話の差分')
fk.service('github', 200, 395, 'GitHub')
fk.flow([(266, 395), (L, 395)], '記録', at=(500, 358))

# 右：書かれる側。GitHub に保存する
fk.service('github', 1210, 315, 'GitHub')
fk.flow([(R, 315), (1144, 315)], '更新した記録')

# 下：本人（札の真下）。レビュー結果を受け取り、レビューの指示（目的・周期・判断基準）を決める
PX, PY, PS = 720, 720, .8
fk.person(PX, PY, PS)
fk.centered(PX, PY + 118 * PS + 12, '本人', 26)
fk.flow([(R, 455), (880, 455), (880, 700), (PX + 68 * PS + 10, 700)], 'レビュー結果', at=(966, 566))
fk.flow([(PX - 68 * PS - 10, 750), (560, 750), (560, 455), (L, 455)], 'レビューの指示', at=(462, 590),
        color=fk.AMBER)

fk.save(HERE / 'cover.png')

# ---- flow.png：必要な説明を補う図 ----
fk.cards('定期レビュー：作業と判断の分担', [
    ('課題', ['定期確認や情報収集のたびに', '人間が依頼・確認を繰り返す']),
    ('AIの作業', ['最新の記録・情報を確認し分析する', '許可した範囲へ保存・更新・報告']),
    ('人間の判断', ['目的・周期・判断基準を設定する', '提案の採否と次の行動を決める']),
    ('周期', ['読書レビュー：毎週日曜 20:30', 'コンテキスト更新：毎週日曜 22:00', '取得・保存の失敗は明示する']),
])
fk.save(HERE / 'flow.png')
