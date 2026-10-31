"""このケースの cover.png を生成する。他ケースの画像には触れない。

    python cases/article-drafting-workflow/figure.py --font /absolute/path/日本語フォント

例（WSL の Noto Sans CJK）:
    python3 cases/article-drafting-workflow/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスのロゴは scripts/logos/）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
点線の矢印は、まだ動かしていない流れ。note への下書き保存は「未検証」、Notion の購入判断ノートを材料にするのは「構想」とラベルで示す。
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

# 中央：Claude Code が聞き取り、書き、投稿する
CX, CY = 760, 330
fk.service('claude', CX, CY, 'Claude Code', tile=160)

# 上：ネタ帳から題材を選ぶ
fk.folder(CX - 53, 65)
fk.centered(CX - 110, 92, 'ネタ帳', 24)
fk.pull([(CX, CY - 90), (CX, 165)])
fk.text(CX + 22, 185, '題材', 22, fk.TEAL)

# 上右：Notion の購入判断ノートを材料にする構想（点線）
fk.service('notion', 1020, 120, '購入判断ノート', tile=120)
fk.dashed_arrow([(960, 150), (CX + 86, CY - 86)])
fk.text(862, 158, '構想', 22, fk.GRAY)

# 左：本人。質問に声で答え、下書きを読んで直す
PX, PY = 170, CY - 30
fk.person(PX, PY)
fk.centered(PX, PY + 132, '本人', 24)
fk.arrow([(CX - 90, CY - 35), (PX + 80, CY - 35)])
fk.centered((CX - 90 + PX + 80) / 2, CY - 70, '質問', 22, fk.TEAL)
fk.arrow([(PX + 75, CY + 35), (CX - 90, CY + 35)], fk.AMBER)
fk.centered((CX - 90 + PX + 75) / 2, CY + 45, '声で答える', 22, fk.AMBER)

# 下：下書きを書き、本人が読んで直し、直しは文章の原則に積み上がる
DX, DY = 560, 490
fk.doc(DX, DY)
fk.centered(DX + 70, DY + 168, '下書き', 24)
fk.arrow([(CX - 82, CY + 70), (DX + 96, DY - 8)])
fk.centered(DX + 60, CY + 108, '書く', 22, fk.TEAL)
fk.arrow([(DX - 10, DY + 80), (PX, DY + 80), (PX, PY + 178)], fk.BLUE, 5)
fk.centered((DX + PX) / 2, DY + 45, '読んで直す', 22, fk.BLUE)

LX, LY = 826, 515
fk.checklist(LX, LY)
fk.centered(LX + 52, LY + 128, '文章の原則', 24, fk.TEAL)
fk.arrow([(DX + 150, DY + 80), (LX - 10, DY + 80)], fk.TEAL, 5)
fk.centered((DX + 150 + LX - 10) / 2, DY + 45, '直しを足す', 20, fk.TEAL)
fk.pull([(LX + 52, CY + 112), (LX + 52, LY - 10)], fk.TEAL, 5)
fk.text(LX + 76, CY + 130, '次に読む', 20, fk.TEAL)

# 右：Qiita へ限定共有で投稿（本人が画像を貼って公開）。note は下書き保存がまだ（点線）
QX, QY = 1270, 200
fk.service('qiita', QX, QY, 'Qiita')
fk.arrow([(CX + 90, CY - 40), (QX - 75, QY + 30)])
fk.centered(1040, 284, '限定共有で投稿', 22, fk.TEAL)
fk.centered(QX, QY + 112, '画像と公開は本人', 22, fk.AMBER)

NX, NY = 1270, 590
fk.service('note', NX, NY, 'note')
fk.dashed_arrow([(CX + 90, CY + 40), (NX - 75, NY - 30)])
fk.centered(1110, 438, '下書き保存は未検証', 22, fk.GRAY)

fk.save(HERE / 'cover.png')
