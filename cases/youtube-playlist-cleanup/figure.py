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


def playlist_folder(x, y, c):
    """中に動画の印が入ったフォルダ（整理後のマイリスト）。"""
    fk.folder(x, y, 105, 88, c)
    fk.video(x + 20, y + 32, 65, 40, c)


# ---- cover.png：一目で分かる入口 ----
fk.begin()

# 左：YouTube に増えたマイリスト（散らばった動画）
fk.service('youtube', 250, 165, 'YouTube', tile=110)
for x, y, c in [(97, 320, fk.BLUE), (254, 282, fk.AMBER), (157, 425, fk.TEAL), (310, 386, fk.BLUE)]:
    fk.video(x, y, 140, 86, c)
fk.centered(250, 540, '増えたマイリスト', 30)

# 中央：ChatGPT（Computer Use）が棚卸しして整理する
fk.centered(720, 262, '棚卸し・整理', 28, fk.TEAL)
fk.service('openai', 720, 400, 'ChatGPT', tile=150)
fk.pull([(645, 400), (460, 400)])      # 画面のマイリストを読みに行く（Computer Use）
fk.arrow([(808, 400), (1035, 400)])    # 名前変更・統合・削除の操作（書き込み）

# 右：整理後のマイリスト（左のまとまりと余白を揃えるため、中心を 1185 に置く）
fk.service('youtube', 1185, 165, 'YouTube', tile=110)
for x, y, c in [(1065, 300, fk.BLUE), (1197, 300, fk.TEAL), (1131, 434, fk.AMBER)]:
    playlist_folder(x, y, c)
fk.centered(1185, 540, '整理後', 30)

# 下：本人が残す基準を決めて渡す
fk.person(490, 672, .65)
fk.centered(490, 756, '本人', 26)
fk.arrow([(534, 688), (572, 688)], fk.AMBER, 5)
fk.rr((584, 652, 856, 724), fk.NOTE, '#e7ca7c', 2, 12)
fk.centered(720, 669, '残す・まとめる基準', 26)
fk.pull([(720, 536), (720, 646)], fk.AMBER, 5)   # 基準は ChatGPT が読みに行く

fk.save(HERE / 'cover.png')

# ---- flow.png：必要な説明を補う図 ----
fk.cards('YouTube整理：作業と判断の分担', [
    ('課題', ['増えたマイリストの確認と整理を', '人間が一つずつ行う負担がある']),
    ('AIの作業', ['棚卸し・分類・統合候補の抽出', '許可された範囲で画面を操作する']),
    ('人間の判断', ['残す基準、統合・削除の方針', '必要な例外を判断する']),
    ('確認状況', ['本人申告で整理完了', '件数・変更前後・効果は未確認']),
])
fk.save(HERE / 'flow.png')
