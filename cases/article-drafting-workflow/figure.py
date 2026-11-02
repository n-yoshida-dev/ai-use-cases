"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/article-drafting-workflow/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/article-drafting-workflow/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスのロゴは scripts/logos/）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。読まれる側を左、Claude Code を中央、書かれる側を右に置く。
本人は左に 1 回だけ置き、Claude Code へは声の回答と直しだけを送る。Claude Code の質問と下書きは本人との往復になるので線にせず、
札の下の動詞（聞いて書く）に入れる（2026-11-02）。本人が Qiita で画像を貼って公開する流れは、Claude Code の札の上を通して右の Qiita へ入れる。
文章の原則とNG辞書は読み書き両方の相手なので、左（読まれる側）と右（書かれる側）に 2 回置く。
note は Claude Code が note 版の下書きのファイルを書くところまで。note への投稿は本人の手作業で自動にしていないので、note へは線を引かず書類の絵で示す。
今動いている流れだけを描く。まだ動かしていない流れ（Notion の購入判断ノートを材料にする構想、note への下書き保存）は README に書き、図には描かない（2026-11-02）。
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

# 中央：Claude Code（左の辺に入る線 4 本、右の辺から出る線 3 本）
CX, CY, T = 720, 470, 260
L, R, TOP = CX - T // 2, CX + T // 2, CY - T // 2
fk.service('claude', CX, CY, 'Claude Code', tile=T)
fk.verb(CX, CY + T // 2 + 12 + 36, '聞いて書く')

# 左上：本人（s=1.2 の外形は x±82、y-101〜y+142）
PX, PY, PS = 170, 200, 1.2
fk.person(PX, PY, PS)
PR = PX + 82 + 8
fk.centered(PX, PY + 142 + 12, '本人', 25)

# 本人 → Qiita（Claude Code の札の上を通る）：画像と公開設定
QX, QY = 1270, 250
fk.service('qiita', QX, QY, 'Qiita')
fk.flow([(PR, 205), (QX - 66 - 8, 205)], '画像と公開設定', at=(CX, 205 - 37))

# 本人 → Claude Code：声の回答・直し（入れ子の L 字で交差させない）
# 線の間を 65px あけ、ラベルはどれも自分の線の上に置く
fk.flow([(PR, 270), (520, 270), (520, CY - 90), (L - 8, CY - 90)], '声の回答', at=((PR + 520) / 2, 270 - 37))
fk.flow([(PR, 335), (470, 335), (470, CY - 40), (L - 8, CY - 40)], '直し', at=((PR + 470) / 2, 335 - 37))

# 左：ネタ帳 → 題材
fk.folder(117, CY - 20)
fk.centered(170, CY + 80, 'ネタ帳', 24)
fk.flow([(236, CY + 25), (L - 8, CY + 25)], '題材', at=(380, CY + 25 - 37))

# 左下：文章の原則とNG辞書（最初に決めて毎回読む置き場。本人からの線は引かない）
fk.checklist(118, CY + 130)
fk.centered(170, CY + 258, '原則とNG辞書', 24)
fk.flow([(236, CY + 188), (330, CY + 188), (330, CY + 90), (L - 8, CY + 90)], '原則と辞書',
        at=(450, CY + 90 - 37))

# 右上：Qiita へ限定共有の記事
fk.flow([(R + 8, CY - 90), (1080, CY - 90), (1080, QY + 30), (QX - 66 - 8, QY + 30)], '限定共有の記事',
        at=((R + 1080) / 2, CY - 90 - 37))

# 右：note 版の下書き（書類）
NX = 1200
fk.flow([(R + 8, CY + 10), (NX - 8, CY + 10)], '下書き', at=((R + NX) / 2, CY + 10 - 37))
fk.doc(NX, CY + 10 - 79)
fk.centered(NX + 70, CY + 10 + 79 + 12, 'note版の下書き', 24)

# 右下：Claude Code → 文章の原則とNG辞書（書かれる側）：直しの差分
fk.flow([(R + 8, CY + 90), (1080, CY + 90), (1080, CY + 230), (1210, CY + 230)], '直しの差分',
        at=((R + 1080) / 2, CY + 90 - 37))
fk.checklist(1218, CY + 172)
fk.centered(1270, CY + 300, '原則とNG辞書', 24)

fk.save(HERE / 'cover.png')
