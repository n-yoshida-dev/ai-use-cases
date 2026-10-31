"""概念図 cover.png の編集元。このケースの図だけを再生成する。

    cd <ai-use-cases のルート> && python3 cases/bookmark-to-action/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

X の一時保存 → ChatGPT（本人が依頼し、迷うものは本人が判断）→ Raindrop・Notion・Todoist・Google マップへ振り分け。
"""
import argparse, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
import figkit as f

p = argparse.ArgumentParser(); p.add_argument('--font', required=True)
f.init(p.parse_args().font)
f.begin()

# 入口：X の一時保存
f.service('x', 250, 450, 'X')
f.arrow([(322, 450), (552, 450)])
f.centered(437, 402, '一時保存', 26, f.GRAY)

# 振り分け役：ChatGPT。上に本人（依頼する・迷うものを判断する）
f.service('openai', 630, 450, 'ChatGPT')
f.person(630, 150, .45)
f.arrow([(605, 222), (605, 372)], f.TEAL)
f.text(515, 282, '依頼', 26, f.TEAL)
f.arrow([(655, 372), (655, 222)], f.AMBER)
f.text(680, 282, '判断', 26, f.AMBER)

# 振り分け先：4 つのサービス。用途のラベルは 4 つとも同じ色（INK）にして、色に意味を持たせない
# （TEAL は依頼・振り分けの流れ、AMBER は本人の判断にだけ使う）
rows = [
    (160, 'raindrop', 'Raindrop', '記事・資料'),
    (350, 'notion', 'Notion', '購入検討'),
    (540, 'todoist', 'Todoist', '近々の買い物'),
    (730, 'googlemaps', 'Google マップ', '行きたい場所'),
]
f.d.line([(702, 450), (820, 450)], fill=f.TEAL, width=6)
f.d.line([(820, rows[0][0]), (820, rows[-1][0])], fill=f.TEAL, width=6)
for y, name, label, what in rows:
    f.arrow([(820, y), (912, y)], f.TEAL, 5)
    f.service(name, 990, y, label)
    f.text(1090, y - 20, what, 32, f.INK)

f.save(HERE / 'cover.png')
