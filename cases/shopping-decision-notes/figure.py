"""このケースの概念図だけを生成する。Python 3 / Pillow / 日本語フォント。
python cases/shopping-decision-notes/figure.py --font /path/to/JapaneseFont.ttf
例：python cases/shopping-decision-notes/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
共通部品は scripts/figkit.py（サービスのロゴは scripts/logos/）。生成後に日本語・切れ・重なりを目視確認する。
"""
import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
import figkit as f

parser = argparse.ArgumentParser()
parser.add_argument('--font', required=True)
f.init(parser.parse_args().font)
f.begin()

# 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。左＝読まれる側、中央＝AI、右＝書かれる側。
# Notion は読まれる側（既存の記録）と書かれる側（商品メモ・購入判断ノート）の両方なので、左右に 2 回置く。
# 左に Notion があることで「保存した記録を次の相談で読み返す」も表す。

# 左：本人（用途・好みを話す）と、既存の Notion の記録。
f.person(190, 300, .8)
f.centered(190, 404, '本人', 29)
f.flow([(262, 330), (500, 330), (500, 470), (574, 470)], '用途・好み', color=f.AMBER)

f.service('notion', 190, 630, 'Notion', tile=110)
f.flow([(262, 630), (500, 630), (500, 520), (574, 520)], '既存の記録', color=f.BLUE)

# 中央：ChatGPT が会話と既存の記録を照合し、2 種類のノートへ書き分ける。
f.service('openai', 640, 495, 'ChatGPT')
f.centered(640, 612, '照合して書き分け', 24, f.GRAY)


# 右：Notion の中で、商品メモと購入判断ノートを分ける。
f.rr((1040, 170, 1380, 712), 'white', f.BLUE, 3, 18)
f.service('notion', 1210, 240, 'Notion', tile=96)

f.rr((1140, 350, 1280, 460), 'white', f.BLUE, 3, 9)
f.rr((1158, 364, 1262, 410), '#e7eef6', f.BLUE, 2, 7)
f.d.ellipse((1170, 371, 1186, 387), fill=f.BLUE)
f.d.polygon([(1163, 404), (1198, 378), (1256, 404)], fill=f.TEAL)
for y, end in [(426, 1262), (446, 1234)]:
    f.d.line((1158, y, end, y), fill=f.LINE, width=6)
f.centered(1210, 470, '商品メモ', 26, f.BLUE)

f.rr((1140, 530, 1280, 640), 'white', f.TEAL, 3, 9)
f.d.line((1162, 552, 1162, 618), fill=f.TEAL, width=3)
for i, y in enumerate([552, 585, 618]):
    f.d.ellipse((1155, y - 7, 1169, y + 7), fill=f.TEAL)
    f.d.line((1182, y, 1260 - i * 8, y), fill=f.LINE, width=6)
f.centered(1210, 650, '購入判断ノート', 23, f.TEAL)

# 書く流れは Notion の枠の上に重ねて描く（枠の白で線が隠れないように）。
f.flow([(706, 470), (780, 470), (780, 405), (1140, 405)], '仕様・出典・注意点', at=(900, 368))
f.flow([(706, 520), (780, 520), (780, 585), (1140, 585)], '判断の経緯', at=(900, 548))

f.save(HERE / 'cover.png')
