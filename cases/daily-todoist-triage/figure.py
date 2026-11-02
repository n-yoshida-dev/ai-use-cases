"""このケースの概念図だけを再生成。Python 3 / Pillow / 日本語フォント。
python cases/daily-todoist-triage/figure.py --font /path/to/JapaneseFont.ttf
例：python3 cases/daily-todoist-triage/figure.py --font /usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc
部品は scripts/figkit.py。他ケースの画像には触れない。

構図（矢印 1 本＝データが動く向き。左＝読まれる側、中央＝AI、右＝書かれる側）：
左右どちらも「Todoist の Inbox」の枠（同じ形・同じ見出し）。ChatGPT が書き込むのは Inbox だけなので、
右は別の置き場ではなく、同じ Inbox の整理後の姿として描く（2026-11-02 の点検で、左の Inbox と右の Todoist が
別の置き場に見えると指摘があった）。左の枠にはばらばらの札、右の枠には整理後の中身の例
（タスク 2 行・時間タグ（2分以内）・担当タグ（本人対応）・優先度の旗）。親子（サブタスク）の整理は、確かめた記録が無い（meta の confirmed は親子関係の保持だけ）ので描かない。
左下が整理の基準を書いた手順書（GitHub）。6 時の指示文はこの節を読むだけ。メールの図（daily-email-triage）と同じく
GitHub の札に「手順書」と書く。手順書は ChatGPT が毎朝読む置き場なので、本人からの矢印は描かない
（毎回本人が渡しているように見えるため。2026-11-02 本人）。この図では本人が毎回渡すもの・受け取るものが無いので、本人は描かない。
中央が毎朝 6 時に動く ChatGPT。
流れ：Inbox（整理前）→ ChatGPT（未整理タスク）、手順書 → ChatGPT（整理の基準）、ChatGPT → Inbox（整理済みタスク）。
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


FW, FH = 380, 260   # Inbox の枠（左右で同じ大きさ）
FY = CY - FH / 2    # 枠の上端


def inbox(x0):
    """Todoist の Inbox の枠：小さな Todoist のロゴと「Todoist の Inbox」を頭に付ける。左右で同じ形にし、同じ置き場と読ませる。"""
    fk.rr((x0, FY, x0 + FW, FY + FH), '#f1f3f1', fk.LINE, 3, 20)
    fk.logo('todoist', x0 + 40, FY + 34, 36)
    fk.text(x0 + 66, FY + 16, 'Todoist の Inbox', 26, fk.INK)
    return x0 + FW


# 左：整理前の Inbox。ばらばらの札を重ねる
LX = 50
lr = inbox(LX)
task_card(LX + 78, FY + 66, fk.BLUE)
task_card(LX + 142, FY + 126, fk.AMBER)

# 左下：整理の基準を書いた手順書（GitHub）。最初に決めて置いておき、ChatGPT が毎朝読む
NY = 560            # 下の段の中心の高さ
GX = LX + FW / 2
fk.service('github', GX, NY, '手順書')

# 中央：ChatGPT（毎朝 6 時に動く）
fk.trigger(AX, CY - HALF, '毎朝6時')
fk.service('openai', AX, CY, 'ChatGPT')
fk.verb(AX, CY + HALF + 12 + 36, '読んで整理')

# 左 → 中央：Inbox の未整理タスク（左の辺の上寄り）と、手順書の整理の基準（左の辺の下寄り）
fk.flow([(lr + 12, CY - 28), (AX - HALF - 6, CY - 28)], '未整理タスク')
fk.flow([(GX + HALF + 6, NY), (580, NY), (580, CY + 28), (AX - HALF - 6, CY + 28)], '整理の基準')

# 中央 → 右：整理済みのタスクを同じ Inbox へ戻す
RX = 1440 - LX - FW
inbox(RX)
fk.flow([(AX + HALF + 14, CY), (RX - 12, CY)], '整理済みタスク')


def tag(x, y, s, c, fill, h=40, size=22):
    """文字を上下の真ん中に置いたタグ。右端の x を返す。"""
    f = fk.jpfont(size)
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0] + 24
    fk.rr((x, y, x + w, y + h), fill, c, 2, 8)
    d.text((x + 12 - bb[0], y + h / 2 - (bb[1] + bb[3]) / 2), s, font=f, fill=c)
    return x + w


# 右の枠の中：整理されたあとの中身（タスク 2 行・時間タグ・担当タグ・優先度の旗）
cw = 340
px, py = RX + (FW - cw) / 2, FY + 66
fk.rr((px, py, px + cw, py + 176), 'white', fk.TEAL, 3, 16)
for k, w in enumerate((210, 176)):
    y = py + 28 + k * 44
    fk.rr((px + 26, y, px + 52, y + 26), 'white', fk.TEAL, 3, 6)
    d.line((px + 70, y + 13, px + 70 + w, y + 13), fill=fk.LINE, width=6)
ty = py + 116
x = tag(px + 26, ty, '2分以内', fk.AMBER, fk.NOTE)
x = tag(x + 12, ty, '本人対応', fk.TEAL, '#eaf3f1')
# 優先度の旗：竿と布
fx = x + 26
d.line((fx, ty - 2, fx, ty + 42), fill=fk.INK, width=4)
d.polygon([(fx + 2, ty), (fx + 34, ty), (fx + 26, ty + 11), (fx + 34, ty + 22), (fx + 2, ty + 22)], fill=fk.AMBER)

fk.save(HERE / "cover.png")
