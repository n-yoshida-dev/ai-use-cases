"""このケースの概念図だけを再生成。Python 3 / Pillow / 日本語フォント。
python cases/daily-todoist-triage/figure.py --font /path/to/JapaneseFont.ttf
例：python3 cases/daily-todoist-triage/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
部品は scripts/figkit.py。他ケースの画像には触れない。

構図（矢印 1 本＝データが動く向き。左＝読まれる側、中央＝AI、右＝書かれる側）：
左上が Todoist の Inbox（たまった札）、左下が本人と、本人が決めた基準（優先度・例外・期限）。
中央が毎朝 6 時に動く ChatGPT。右が整理されたあとの Todoist（親子・所要時間・優先度）。
流れ：Inbox → ChatGPT（タスク）、本人 → 基準（判定基準）、基準 → ChatGPT（指示）、ChatGPT → Todoist（整理済みタスク）。
"""
import argparse, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import figkit as fk

parser = argparse.ArgumentParser()
parser.add_argument("--font", required=True)
fk.init(parser.parse_args().font)
fk.begin()
d = fk.d

CY = 300            # 横の流れの中心の高さ
AX = 720            # ChatGPT の札の中心
HALF = 66           # 札の半分（fk.service の既定 132px）


def task_card(x, y, c):
    """ばらばらに書かれたタスクの札（160×112）。"""
    fk.rr((x, y, x + 160, y + 112), 'white', c, 3, 12)
    for k, w in enumerate((96, 78, 90)):
        d.line((x + 30, y + 30 + k * 27, x + 30 + w, y + 30 + k * 27), fill=fk.LINE, width=6)


# 左上：Todoist の中の Inbox。小さな Todoist のロゴと「Inbox」を頭に付けた枠の中に札を重ねる
fk.rr((60, 150, 350, 420), '#f1f3f1', fk.LINE, 3, 20)
fk.logo('todoist', 100, 184, 36)
fk.text(126, 166, 'Inbox', 26, fk.INK)
task_card(96, 214, fk.BLUE)
task_card(160, 274, fk.AMBER)

# 左下：本人 → 基準のメモ（優先度・例外・期限）
NY = 600            # 下の段の中心の高さ
fk.person(110, NY - 10, 0.48)
fk.centered(110, NY + 62, '本人', 24)
fk.rr((270, NY - 35, 510, NY + 35), fk.NOTE, '#e7ca7c', 2, 12)
fk.centered(390, NY - 17, '優先度・例外・期限', 24)
fk.flow([(158, NY), (256, NY)], '判定基準', color=fk.AMBER)

# 中央：ChatGPT（毎朝 6 時に動く）
fk.trigger(AX, CY - HALF, '毎朝6時')
fk.service('openai', AX, CY, 'ChatGPT')
fk.centered(AX, CY + HALF + 50, '読んで整理', 24, fk.GRAY)

# 左 → 中央：Inbox のタスク（左の辺の上寄り）と、基準の指示（左の辺の下寄り）
fk.flow([(362, CY - 28), (AX - HALF - 6, CY - 28)], 'タスク')
fk.flow([(524, NY), (600, NY), (600, CY + 28), (AX - HALF - 6, CY + 28)], '指示',
        at=(562, NY - 37), color=fk.AMBER)

# 中央 → 右：整理済みのタスクを Todoist へ
fk.service('todoist', 1190, CY, 'Todoist')
fk.flow([(AX + HALF + 14, CY), (1190 - HALF - 8, CY)], '整理済みタスク')

# 右下：整理されたあとの姿（親子・所要時間・優先度）
px, py = 1010, 440
fk.rr((px, py, px + 360, py + 190), 'white', fk.TEAL, 3, 16)
fk.rr((px + 24, py + 30, px + 50, py + 56), 'white', fk.TEAL, 3, 4)
d.line((px + 68, py + 43, px + 283, py + 43), fill=fk.LINE, width=6)
fk.rr((px + 50, py + 78, px + 76, py + 104), 'white', fk.BLUE, 3, 4)
d.line((px + 94, py + 91, px + 294, py + 91), fill=fk.LINE, width=6)
d.line([(px + 37, py + 56), (px + 37, py + 91), (px + 48, py + 91)], fill=fk.BLUE, width=3)
fk.rr((px + 24, py + 126, px + 104, py + 165), fk.NOTE, fk.AMBER, 2, 8)
fk.text(px + 32, py + 133, '2分', 24, fk.AMBER)
fk.rr((px + 120, py + 126, px + 224, py + 165), '#eaf3f1', fk.TEAL, 2, 8)
fk.text(px + 128, py + 133, '10分', 24, fk.TEAL)
d.polygon([(px + 260, py + 126), (px + 260, py + 170), (px + 265, py + 152), (px + 302, py + 152), (px + 302, py + 126)],
          fill=fk.AMBER)

fk.save(HERE / "cover.png")
