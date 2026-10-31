"""このケースの概念図だけを再生成。Python 3 / Pillow / 日本語フォント。
python cases/daily-todoist-triage/figure.py --font /path/to/JapaneseFont.ttf
例：python3 cases/daily-todoist-triage/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
部品は scripts/figkit.py。他ケースの画像には触れない。

構図：左が Todoist の Inbox（たまった札）、中央が毎朝 6:00 に動く ChatGPT、右が整理されたあとの Todoist。
下は本人が基準（優先度・例外・期限）を決めて ChatGPT へ渡す流れ。
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

CY = 300  # 横の流れの中心の高さ


def task_card(x, y, c):
    """ばらばらに書かれたタスクの札（160×112）。"""
    fk.rr((x, y, x + 160, y + 112), 'white', c, 3, 12)
    for k, w in enumerate((96, 78, 90)):
        d.line((x + 30, y + 30 + k * 27, x + 30 + w, y + 30 + k * 27), fill=fk.LINE, width=6)


# 左：Todoist の中の Inbox。小さな Todoist のロゴと「Inbox」を頭に付けた枠の中に札を重ねる
fk.rr((60, 150, 350, 420), '#f1f3f1', fk.LINE, 3, 20)
fk.logo('todoist', 100, 184, 36)
fk.text(126, 166, 'Inbox', 26, fk.INK)
task_card(96, 214, fk.BLUE)      # 214–326
task_card(160, 274, fk.AMBER)    # 274–386 → 束の中心は y=300

# 中央：ChatGPT（毎朝 6:00 に動く）
fk.clock(640, 150, 36)
fk.text(690, 130, '毎朝6:00', 30, fk.BLUE)
fk.service('openai', 720, CY, 'ChatGPT')

# Inbox → ChatGPT（読む） → Todoist（更新）
fk.arrow([(362, CY), (640, CY)])
fk.centered(501, CY - 42, '読む', 24, fk.TEAL)
fk.arrow([(800, CY), (1110, CY)])
fk.centered(955, CY - 42, '更新', 24, fk.TEAL)

# 右：Todoist と、整理されたあとの姿（親子・所要時間・優先度）
fk.service('todoist', 1190, CY, 'Todoist')
fk.arrow([(1190, 424), (1190, 462)], fk.TEAL, 5)
px, py = 1010, 470
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

# 下：本人が基準（優先度・例外・期限）を決めて ChatGPT へ指示する
fk.person(218, 620, 0.48)
fk.centered(218, 690, '本人', 24)
fk.rr((372, 585, 814, 655), fk.NOTE, '#e7ca7c', 2, 12)
fk.centered(593, 600, '優先度・例外・期限', 24)
fk.arrow([(281, 620), (354, 620)], fk.AMBER, 5)
fk.arrow([(720, 580), (720, 424)], fk.AMBER, 5)
fk.text(738, 486, '指示', 24, fk.AMBER)

fk.save(HERE / "cover.png")
