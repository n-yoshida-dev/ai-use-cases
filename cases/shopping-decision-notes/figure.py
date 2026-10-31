"""このケースの概念図だけを生成する。Python 3 / Pillow / 日本語フォント。
python cases/shopping-decision-notes/figure.py --font /path/to/JapaneseFont.ttf
共通部品は scripts/figkit.py。生成後に日本語・切れ・重なりを目視確認する。
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
f.begin('商品比較の判断を、次の相談へ残す', '会話から仕様・判断の経緯を整理し、Notionに残す')

# 左：本人の困りごと・用途・評価を会話で伝える。
f.person(185, 420, .78)
f.rr((264, 270, 464, 396), 'white', f.AMBER, 3, 18)
f.d.polygon([(264, 366), (240, 392), (282, 390)], fill='white')
f.text(290, 288, '用途・好み', 25, f.AMBER)
for y, end in [(340, 432), (365, 407)]:
    f.d.line((292, y, end, y), fill=f.LINE, width=6)
f.centered(205, 550, '本人の声', 29)
f.centered(205, 592, '判断・訂正', 24, f.GRAY)
f.arrow([(354, 452), (535, 452)], f.AMBER)

# 中：ChatGPTが事実と解釈を分けて整理する。
f.laptop(575, 330, 240, 168)
f.centered(695, 550, 'ChatGPT', 30, f.TEAL)
f.centered(695, 592, '事実と解釈を分ける', 23, f.GRAY)
f.arrow([(855, 420), (915, 420)])

# 右：Notionの中で、商品の資料と比較の判断を分ける。
f.rr((935, 234, 1370, 638), 'white', f.BLUE, 3, 18)
f.text(962, 251, 'Notion', 28, f.BLUE)
f.rr((960, 320, 1110, 482), 'white', f.BLUE, 3, 9)
f.rr((982, 340, 1088, 398), '#e7eef6', f.BLUE, 2, 7)
f.d.ellipse((997, 350, 1015, 368), fill=f.BLUE)
f.d.polygon([(988, 389), (1027, 358), (1078, 389)], fill=f.TEAL)
for y, end in [(424, 1084), (449, 1057)]:
    f.d.line((983, y, end, y), fill=f.LINE, width=6)
f.centered(1035, 504, '商品メモ', 26, f.BLUE)
f.centered(1035, 543, '仕様・出典', 21, f.GRAY)

f.rr((1170, 320, 1336, 482), 'white', f.TEAL, 3, 9)
f.d.line((1192, 348, 1192, 452), fill=f.TEAL, width=3)
for i, y in enumerate([350, 396, 442]):
    f.d.ellipse((1184, y - 8, 1200, y + 8), fill=f.TEAL)
    f.d.line((1214, y, 1312 - i * 8, y), fill=f.LINE, width=6)
f.centered(1253, 504, '購入判断ノート', 23, f.TEAL)
f.centered(1253, 543, '理由・変化', 21, f.GRAY)
f.centered(1152, 593, '比較ページから開く', 23, f.BLUE)

# 保存した記録を次の相談で再利用する。自動起動の矢印ではない。
f.dashed_arrow([(1150, 652), (1150, 710), (205, 710), (205, 634)], f.BLUE, 4)
f.centered(670, 731, '次の相談で読み返す', 24, f.BLUE)
f.footer('判断ノートの保存内容を確認／記事への引き継ぎと継続効果は未検証')
f.save(HERE / 'cover.png')
