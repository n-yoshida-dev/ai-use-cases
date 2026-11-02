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
# Notion は読まれる側（登録済みの商品と購入判断ノート）と書かれる側（欲しいもの・購入判断ノート）の両方なので、左右に 2 回置く。
# 左に Notion があることで「保存した記録を次の相談で読み返す」も表す。左の札は欲しいものと購入判断ノートの両方を指すので名前は「Notion」のまま。
# 欲しいものへ渡る物は、欲しいもの DB の書き方「商品の仕様・価格・出典は DB の各商品が正本」に合わせる（2026-11-02 点検）。

# 左：本人（用途と条件を話す）、Web（メーカーの情報・価格・評判を調べる）、Notion の登録済みの商品と購入判断ノート（重ねず、古い記録で上書きしないため）。
f.person(190, 250, .8)
f.centered(190, 354, '本人', 29)
f.flow([(262, 280), (520, 280), (520, 450), (574, 450)], '用途と条件', at=(380, 243))

f.service('web', 190, 495, 'Web', tile=110)
f.flow([(250, 495), (574, 495)], '仕様・価格・評判', at=(400, 458))

f.service('notion', 190, 665, 'Notion', tile=110)
f.flow([(250, 665), (520, 665), (520, 540), (574, 540)], '登録済みの商品・ノート', at=(382, 629), size=22)

# 中央：ChatGPT が会話の中で候補を比べ（登録済みの商品・ノートとも照らし合わせ）、2 種類のノートへ書き分ける。
# 比べる作業は線のラベルに書かず、この動詞に書く（AGENTS.md「見せ方と図」。2026-11-02 本人の指摘）。
f.service('openai', 640, 495, 'ChatGPT')
f.verb(640, 495 + 66 + 12 + 36, '比べて書き分ける')


# 右：Notion の中で、欲しいもの（DB、1 商品 1 行）と購入判断ノートを分ける。
f.rr((1040, 170, 1380, 712), 'white', f.BLUE, 3, 18)
f.service('notion', 1210, 240, 'Notion', tile=96)

f.rr((1140, 350, 1280, 460), 'white', f.BLUE, 3, 9)
f.rr((1158, 364, 1262, 410), '#e7eef6', f.BLUE, 2, 7)
f.d.ellipse((1170, 371, 1186, 387), fill=f.BLUE)
f.d.polygon([(1163, 404), (1198, 378), (1256, 404)], fill=f.TEAL)
for y, end in [(426, 1262), (446, 1234)]:
    f.d.line((1158, y, end, y), fill=f.LINE, width=6)
f.centered(1210, 470, '欲しいもの', 26, f.BLUE)

f.rr((1140, 530, 1280, 640), 'white', f.TEAL, 3, 9)
f.d.line((1162, 552, 1162, 618), fill=f.TEAL, width=3)
for i, y in enumerate([552, 585, 618]):
    f.d.ellipse((1155, y - 7, 1169, y + 7), fill=f.TEAL)
    f.d.line((1182, y, 1260 - i * 8, y), fill=f.LINE, width=6)
f.centered(1210, 650, '購入判断ノート', 23, f.TEAL)

# 書く流れは Notion の枠の上に重ねて描く（枠の白で線が隠れないように）。
f.flow([(706, 470), (780, 470), (780, 405), (1140, 405)], '仕様・価格・出典', at=(900, 368))
f.flow([(706, 520), (780, 520), (780, 585), (1140, 585)], '判断の経緯', at=(900, 548))

f.save(HERE / 'cover.png')
