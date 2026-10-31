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

# 左：本人が用途・好みを話し、判断を訂正する。
f.person(185, 400, .78)
f.rr((264, 250, 464, 376), 'white', f.AMBER, 3, 18)
f.d.polygon([(264, 346), (240, 372), (282, 370)], fill='white')
f.text(290, 268, '用途・好み', 25, f.AMBER)
for y, end in [(320, 432), (345, 407)]:
    f.d.line((292, y, end, y), fill=f.LINE, width=6)
f.centered(205, 515, '本人', 29)
f.arrow([(354, 430), (600, 430)], f.AMBER)
f.centered(477, 388, '相談', 24, f.AMBER)

# 中：ChatGPT が会話と既存の記録を照合して整理する。
f.service('openai', 695, 420, 'ChatGPT')
f.arrow([(780, 392), (915, 392)])
f.centered(848, 350, '書く', 24, f.TEAL)
f.arrow([(915, 452), (780, 452)], f.BLUE)
f.centered(848, 466, '読む', 24, f.BLUE)

# 右：Notion の中で、商品メモと購入判断ノートを分ける。
f.rr((935, 150, 1370, 600), 'white', f.BLUE, 3, 18)
f.service('notion', 1152, 225, 'Notion', tile=110)
f.rr((960, 345, 1110, 507), 'white', f.BLUE, 3, 9)
f.rr((982, 365, 1088, 423), '#e7eef6', f.BLUE, 2, 7)
f.d.ellipse((997, 375, 1015, 393), fill=f.BLUE)
f.d.polygon([(988, 414), (1027, 383), (1078, 414)], fill=f.TEAL)
for y, end in [(449, 1084), (474, 1057)]:
    f.d.line((983, y, end, y), fill=f.LINE, width=6)
f.centered(1035, 528, '商品メモ', 26, f.BLUE)

f.rr((1170, 345, 1336, 507), 'white', f.TEAL, 3, 9)
f.d.line((1192, 373, 1192, 477), fill=f.TEAL, width=3)
for i, y in enumerate([375, 421, 467]):
    f.d.ellipse((1184, y - 8, 1200, y + 8), fill=f.TEAL)
    f.d.line((1214, y, 1312 - i * 8, y), fill=f.LINE, width=6)
f.centered(1253, 528, '購入判断ノート', 23, f.TEAL)

# 保存した記録を次の相談で読み返す。自動起動の矢印ではない。
f.dashed_arrow([(1152, 614), (1152, 690), (205, 690), (205, 560)], f.BLUE, 4)
f.centered(670, 708, '読み返す', 24, f.BLUE)
f.save(HERE / 'cover.png')
