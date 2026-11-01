"""概念図 cover.png の編集元。このケースの図だけを再生成する。

    cd <ai-use-cases のルート> && python3 cases/bookmark-to-action/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

X の一時保存 → ChatGPT（本人が依頼し、迷うものは本人が判断）→ Raindrop・Notion・Todoist・Google マップへ振り分け。

矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。左＝読まれる側（X・本人）、中央＝ChatGPT、右＝書かれる側。
定期運用は停止中（本人が気づいたときに頼む）なので、きっかけの時計は置かない。
"""
import argparse, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'scripts'))
import figkit as f

p = argparse.ArgumentParser(); p.add_argument('--font', required=True)
f.init(p.parse_args().font)
f.begin()

# 中央：振り分け役の ChatGPT。動詞は札の下に 1 行
AX, AY, AT = 640, 420, 170
L, R, T, B = AX - AT / 2, AX + AT / 2, AY - AT / 2, AY + AT / 2
bottom = f.service('openai', AX, AY, 'ChatGPT', tile=AT)
f.centered(AX, bottom + 52, '読んで振り分け', 26, f.GRAY)

# 左上：X の一時保存 → ChatGPT（ChatGPT が読みに行く）
XY = AY - 60
f.service('x', 240, XY, 'X')
f.flow([(306, XY), (L, XY)], '一時保存')

# 左下：本人 → ChatGPT（依頼と、迷うものの判断）
PX, PY = 240, 640
f.person(PX, PY, .8)
f.centered(PX, PY + 118 * .8 + 14, '本人', 25)
f.flow([(PX + 66, PY - 20), (470, PY - 20), (470, AY + 10), (L, AY + 10)], '依頼',
       at=((PX + 66 + 470) / 2, PY - 20 - 37))
f.flow([(PX + 66, PY + 50), (510, PY + 50), (510, AY + 60), (L, AY + 60)], '判断',
       at=((PX + 66 + 510) / 2, PY + 50 - 37))

# 右：振り分け先の 4 つ。ChatGPT の右の辺から 40px おきに出て、外側の行ほど手前で曲がる
SX = 1180
rows = [
    # (行の y, 出る y, 曲がる x, ロゴ, 名前, 動くデータ)
    (135, AY - 60, 780, 'raindrop', 'Raindrop', '記事・資料'),
    (325, AY - 20, 830, 'notion', 'Notion', '購入検討'),
    (515, AY + 20, 870, 'todoist', 'Todoist', '近々の買い物'),
    (705, AY + 60, 790, 'googlemaps', 'Google マップ', '行きたい場所'),
]
for y, ey, ex, name, label, what in rows:
    f.flow([(R, ey), (ex, ey), (ex, y), (SX - 66, y)], what, at=((ex + SX - 66) / 2, y - 37))
    f.service(name, SX, y, label)

f.save(HERE / 'cover.png')
