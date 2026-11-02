"""このケースの cover.png / flow.png を生成する。他ケースの画像には触れない。

    python cases/youtube-playlist-cleanup/figure.py --font /absolute/path/日本語フォント

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


def playlist_folder(x, y, c, w=105, h=88):
    """中に動画の印が入ったフォルダ（マイリスト 1 つ）。"""
    fk.folder(x, y, w, h, c)
    fk.video(x + w * .19, y + h * .36, w * .62, h * .45, c)


# ---- cover.png：一目で分かる入口 ----
# 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。左＝読まれる側、中央＝AI、右＝書かれる側。
# YouTube は読まれる側（増えたマイリスト）と書かれる側（整理後）の両方なので、左右に 2 回置く。
fk.begin()

# 左上：YouTube に増えたマイリスト（小さなフォルダがたくさん散らばる。右の整理後の 3 つと対比）
fk.service('youtube', 250, 150, 'YouTube', tile=110)
for x, y, c in [
        (74, 276, fk.BLUE), (178, 264, fk.AMBER), (290, 282, fk.TEAL),
        (110, 364, fk.TEAL), (224, 354, fk.BLUE), (338, 370, fk.AMBER),
        (70, 452, fk.AMBER), (178, 442, fk.TEAL), (288, 458, fk.BLUE)]:
    playlist_folder(x, y, c, 76, 64)

# 左下：本人（残す基準を渡すだけなので入力側）
fk.person(230, 640, .65)
fk.centered(230, 726, '本人', 26)

# 中央：ChatGPT
bottom = fk.service('openai', 740, 400, 'ChatGPT', tile=150)
fk.verb(740, bottom + 12 + 36, '棚卸し・作成・統合・削除')   # 動詞は名前の真下（灰色・24px）

# 右：整理後の YouTube のマイリスト
fk.service('youtube', 1185, 150, 'YouTube', tile=110)
for x, y, c in [(1065, 300, fk.BLUE), (1197, 300, fk.TEAL), (1131, 422, fk.AMBER)]:
    playlist_folder(x, y, c)

# 流れ（出どころ → 行き先）
fk.flow([(445, 372), (661, 372)], '増えたマイリスト', at=(543, 326))
fk.flow([(300, 650), (545, 650), (545, 432), (661, 432)], '残す・まとめる基準', at=(422, 604))
fk.flow([(819, 400), (1040, 400)], '整理後のマイリスト', at=(925, 354))

fk.save(HERE / 'cover.png')

# ---- flow.png：必要な説明を補う図 ----
fk.cards('YouTube整理：作業と判断の分担', [
    ('課題', ['増えたマイリストの確認と整理を', '人間が一つずつ行う負担がある']),
    ('AIの作業', ['棚卸し・分類・統合候補の抽出', '許可された範囲で画面を操作する']),
    ('人間の判断', ['残す基準、統合・削除の方針', '必要な例外を判断する']),
    ('確認状況', ['本人申告で整理完了', '件数・変更前後・効果は未確認']),
])
fk.save(HERE / 'flow.png')
