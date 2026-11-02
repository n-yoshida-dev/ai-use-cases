"""このケースの cover.png / flow.png を生成する。他ケースの画像には触れない。

    python cases/daily-email-triage/figure.py --font /absolute/path/日本語フォント
    （例）PYTHONPATH=<Pillow の場所> python3 cases/daily-email-triage/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc

Python 3 / Pillow。部品は scripts/figkit.py（サービスはロゴの札 fk.service で示す）。
生成後は欠字・はみ出し・重なり・ロゴの欠けを目視確認する。
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

# ---- cover.png：一目で分かる入口（題名・注記は入れない） ----
# 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先）。左＝読まれる側、中央＝AI、右＝書かれる側。
# Gmail は読む相手（左）とラベルを付ける相手（右）の 2 回置く。本人は朝の報告を受け取るだけなので下に 1 回置く。
fk.begin()

CY = 300                 # 主な流れ（Gmail → フィルタ → ChatGPT）の高さ
GPT = 760                # ChatGPT の中心 x
HALF = 66                # service() の札の半分
LABEL_Y = CY + HALF + 12  # service() が名前を書く高さ。同じ列の名前はここに揃える

# 左：Gmail の新着 → Gmail のフィルタ（AI を使わない層）→ 残りを ChatGPT が読む
# フィルタはノイズを既読にして受信トレイから外す（アーカイブ）だけで、削除はしない。
# 「除外」は削除にも読めたので、名前「フィルタ」の下に何をするかを書く（2026-11-02）
fk.service('gmail', 130, CY, 'Gmail')
FX, FW, FH = 340, 120, 130
fk.funnel(FX, CY - FH / 2, FW, FH)
fk.centered(FX + FW / 2, LABEL_Y, 'フィルタ', 25)
fk.verb(FX + FW / 2, LABEL_Y + 36, 'ノイズは既読で保管')
SLOPE = FW * .38 * (FH / 2) / (FH * .55)   # 中心の高さでの、漏斗の縁の内側への入り込み
fk.flow([(130 + HALF, CY), (FX + SLOPE - 4, CY)], '新着メール')
fk.flow([(FX + FW - SLOPE + 4, CY), (GPT - HALF, CY)], '残ったメール')

# 中央：毎朝 6 時に動く ChatGPT（2026-10-28 に Claude Code のルーティンから移した）
fk.trigger(GPT, CY - HALF, '毎朝6時')
fk.service('openai', GPT, CY, 'ChatGPT')
fk.verb(GPT, LABEL_Y + 36, '読んで仕分け')

# 右：要対応は Todoist のタスクに、仕分けのラベルは Gmail に書く
TX, TY = 1290, 140       # Todoist
GX, GY = 1290, 440       # Gmail（書かれる側）
fk.service('todoist', TX, TY, 'Todoist')
fk.service('gmail', GX, GY, 'Gmail')
fk.flow([(GPT + HALF, CY - 44), (980, CY - 44), (980, TY), (TX - HALF, TY)], 'タスク')
fk.flow([(GPT + HALF, CY), (1040, CY), (1040, GY), (GX - HALF, GY)], '仕分けラベル',
        at=((1040 + GX - HALF) / 2, GY - 37))

# 左下：判定基準を書いた手順書（GitHub の README）。最初に 1 回決めて置いておき、ChatGPT が毎朝読む。
# 本人が毎回渡すものではないので、本人からの矢印は引かない（2026-11-02 本人）
DX, DY = 400, 540                        # 手順書（GitHub）の札の中心
fk.service('github', DX, DY, '手順書')
fk.flow([(DX + HALF, DY), (620, DY), (620, CY + 44), (GPT - HALF, CY + 44)], '判定基準')

# 下：本人。朝の報告を本人のスマホで受け取る（0 件の日も）
PX, PY, PS = 740, 724, .8                # 人の中心。外形は x±68s、y-84s〜y+118s
fk.person(PX, PY, PS)
fk.centered(PX, PY + 118 * PS + 12, '本人', 25)

PHX, PHY = 840, 640                      # スマホ（本人の手元）
fk.phone(PHX, PHY, 84, 144)
fk.flow([(GPT + HALF, CY + 44), (PHX + 42, CY + 44), (PHX + 42, PHY - 6)], '朝の報告',
        at=(PHX + 42 + 64, (CY + 44 + PHY) / 2 - 10))

fk.save(HERE / 'cover.png')


# ---- flow.png：必要な説明を補う図 ----
def cards(title, items):
    """fk.cards と同じ並びで、カードの高さを段ごとの行数（2〜3 行）に合わせて詰めたもの（fk.cards は 258px で下が空く）。"""
    fk.begin()
    fk.text(64, 56, title, 40)
    y = 150
    for row in range(0, len(items), 2):
        pair = items[row:row + 2]
        h = 110 + 46 * max(len(lines) for _, lines in pair)
        for i, (label, lines) in enumerate(pair):
            x = 64 + i * 670
            fk.rr((x, y, x + 638, y + h))
            fk.text(x + 28, y + 22, label, 28, fk.TEAL)
            for k, line in enumerate(lines):
                fk.text(x + 28, y + 90 + k * 46, line, 28)
        y += h + 30


cards('メール仕分け：作業と判断の分担', [
    ('課題', ['通知を切ると大事なメールを見落とす', '全部読むにはノイズが多すぎる']),
    ('AIの作業', ['毎朝、未読を読んで3つに仕分ける', '要対応はTodoistへ登録', '続けてTodoistのInboxを整理']),
    ('人間の判断', ['判定基準を手順書に決めておく', 'メールの削除・返信と実際の対応は本人']),
    ('確認すること', ['ラベル付与は移行の前後とも確認', '判定の正確さと時間削減は未測定']),
])
fk.save(HERE / 'flow.png')
