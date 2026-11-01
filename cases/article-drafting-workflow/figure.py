"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/article-drafting-workflow/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/article-drafting-workflow/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスのロゴは scripts/logos/）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。読まれる側を左、Claude Code を中央、書かれる側を右に置く。
本人は読み書き両方の相手なので上に置く。本人から出る線は札の左の辺へ右向きに入れ、本人へ入る線は札の上の辺から真上に出して本人の下の辺へ入れる（主な流れと直角に逃がす）。
文章の原則とNG辞書は読み書き両方の相手なので、左（読まれる側）と右（書かれる側）に 2 回置く。
点線の矢印は、まだ動かしていない流れ（Notion の購入判断ノートを材料にする構想、note への下書き保存）。
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

fk.begin()


def side_label(x, y, s, right=True, color=fk.TEAL, size=23):
    """縦の線の横に置くラベル。right=False なら線の左に右寄せで置く。"""
    if right:
        fk.text(x + 14, y, s, size, color)
    else:
        fk.text(x - 14 - fk.width(s, size), y, s, size, color)


# 中央：Claude Code（左の辺に入る線、右の辺から出る線）
CX, CY, T = 720, 520, 240
L, R = CX - T // 2, CX + T // 2          # 札の左右の辺
fk.service('claude', CX, CY, 'Claude Code', tile=T)
fk.centered(CX, CY + T // 2 + 50, '聞いて書き、投稿する', 22, fk.GRAY)

# 上：本人（s=1.1 の外形は x±75、y-92〜y+130）
PX, PY, S = 720, 130, 1.1
fk.person(PX, PY, S)
PL, PR, PB = PX - 75, PX + 75, PY + 130
fk.text(PX - 37 - 14 - fk.width('本人', 24), PY - 66, '本人', 24)

# 本人 → Claude Code（左回りで札の左の辺へ）：直し・声の回答
fk.flow([(PL, 205), (480, 205), (480, 475), (L, 475)])
side_label(480, 240, '直し', right=False)
fk.flow([(PL, 245), (530, 245), (530, 430), (L, 430)])
side_label(530, 300, '声の回答')

# Claude Code → 本人（札の上の辺から真上へ）：質問・下書き
fk.flow([(735, CY - T // 2), (735, PB)])
side_label(735, 352, '質問', right=False)
fk.flow([(775, CY - T // 2), (775, PB)])
side_label(775, 352, '下書き')

# 左：読まれる側
# ネタ帳 → 題材
fk.folder(117, 285)
fk.centered(170, 387, 'ネタ帳', 24)
fk.flow([(236, 330), (400, 330), (400, 520), (L, 520)], '題材', at=(318, 293))

# Notion の購入判断ノート → 判断と分析（構想・点線）
fk.service('notion', 180, 565, '購入判断ノート', tile=120)
fk.dashed_arrow([(252, 565), (L, 565)])
fk.centered(340, 528, '判断と分析', 23, fk.GRAY)

# 文章の原則とNG辞書 → 原則と辞書
fk.checklist(118, 692)
fk.centered(170, 820, '原則とNG辞書', 24)
fk.flow([(236, 750), (400, 750), (400, 610), (L, 610)], '原則と辞書', at=(318, 713))

# 右：書かれる側
# Qiita：Claude Code が限定共有の記事を投稿し、本人が画像を貼って公開する
QX, QY = 1270, 210
fk.service('qiita', QX, QY, 'Qiita')
fk.flow([(PR, 215), (QX - 66, 215)], '画像と公開設定', at=(1000, 178))
fk.flow([(R, 520), (1070, 520), (1070, 255), (QX - 66, 255)])
side_label(1070, 400, '限定共有の記事')

# note：下書き保存はまだ動かしていない（点線）
NX, NY = 1270, 565
fk.service('note', NX, NY, 'note')
fk.dashed_arrow([(R, 565), (NX - 66, 565)])
fk.centered(1060, 577, 'note版の下書き', 23, fk.GRAY)

# Claude Code → 文章の原則とNG辞書（書かれる側）：直しの差分
fk.checklist(1218, 692)
fk.centered(1270, 820, '原則とNG辞書', 24)
fk.flow([(R, 610), (900, 610), (900, 750), (1206, 750)], '直しの差分', at=(1053, 713))

fk.save(HERE / 'cover.png')
