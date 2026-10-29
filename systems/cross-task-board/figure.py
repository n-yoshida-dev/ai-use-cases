"""全体概念図。python figure.py /path/to/NotoSansJP.ttf"""
import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import figkit as f

f.init(sys.argv[1])


def calendar(x, y, w=74, h=66):
    f.rr((x, y, x + w, y + h), 'white', f.BLUE, 3, 8)
    f.d.rectangle((x + 2, y + 10, x + w - 2, y + 24), fill=f.BLUE)
    for k in range(2):
        f.d.line((x + 20 + k * 34, y - 8, x + 20 + k * 34, y + 12), fill=f.INK, width=4)
    for k in range(3):
        f.d.ellipse((x + 14 + k * 20, y + 38, x + 22 + k * 20, y + 46), fill=f.BLUE)


def folder(x, y, w=78, h=62, c=f.TEAL):
    f.rr((x, y, x + w * .5, y + 18), c, c, 1, 5)
    f.rr((x, y + 10, x + w, y + h), 'white', c, 3, 7)
    f.d.line((x + 14, y + 32, x + w - 14, y + 32), fill=f.LINE, width=5)
    f.d.line((x + 14, y + 46, x + w - 28, y + 46), fill=f.LINE, width=5)


def sticky(x, y, s=68):
    f.d.polygon([(x, y), (x + s, y), (x + s, y + s - 18), (x + s - 18, y + s), (x, y + s)],
                fill=f.NOTE, outline=f.AMBER)
    f.d.line([(x, y), (x + s, y), (x + s, y + s - 18), (x + s - 18, y + s), (x, y + s), (x, y)],
             fill=f.AMBER, width=3, joint='curve')
    f.d.line((x + 12, y + 22, x + s - 14, y + 22), fill=f.AMBER, width=5)
    f.d.line((x + 12, y + 38, x + s - 26, y + 38), fill=f.AMBER, width=5)


def bars(x, y, w=78, h=64):
    f.rr((x, y, x + w, y + h), 'white', f.BLUE, 3, 8)
    for k, bh in enumerate([22, 38, 30]):
        f.d.rectangle((x + 14 + k * 20, y + h - 10 - bh, x + 26 + k * 20, y + h - 10),
                      fill=[f.TEAL, f.BLUE, f.AMBER][k])


f.begin('今日やることを、1枚のボードに', 'タスク・予定・リポジトリの作業を集め、時刻つきの計画にする')

# 左：入力（読むだけ）
rows = [(272, 'Todoist'), (382, 'カレンダー'), (492, '各リポジトリ'), (602, '人間待ちの付箋'), (712, 'アプリの開発状況')]
f.checklist(84, 218, 90, 108)
calendar(86, 350)
folder(86, 460)
sticky(91, 568)
bars(86, 680)
for cy, label in rows:
    f.text(186, cy - 18, label, 25)
    f.d.line((410, cy, 440, cy), fill=f.TEAL, width=5)
f.d.line((440, rows[0][0], 440, rows[-1][0]), fill=f.TEAL, width=5)
f.arrow([(440, 455), (520, 455)])
f.centered(480, 410, '読む', 22, f.TEAL)

# 中央：PCのClaude Code
f.laptop(555, 380, 200, 140)
f.centered(655, 570, 'Claude Code', 29, f.TEAL)
f.centered(655, 608, 'PCで集めて組む', 23, f.GRAY)

# 右：横断タスクボード（アーティファクト＋データベース）
f.centered(1135, 202, '横断タスクボード', 27, f.BLUE)
f.rr((900, 246, 1370, 560), 'white', f.BLUE, 3, 14)
for k, name in enumerate(['予定', '分野別', '開発状況']):
    fill = '#e7eef6' if k else f.BLUE
    f.rr((920 + k * 130, 262, 1036 + k * 130, 298), fill, f.BLUE, 2, 9)
    f.centered(978 + k * 130, 264, name, 20, 'white' if k == 0 else f.BLUE)
for k, (t, c) in enumerate([('朝', f.TEAL), ('朝', f.TEAL), ('夜', f.BLUE), ('夜', f.BLUE)]):
    ry = 326 + k * 54
    f.rr((920, ry, 1006, ry + 36), '#eef3f3', c, 2, 8)
    f.centered(963, ry + 3, t, 20, c)
    f.d.line((1024, ry + 18, 1290 - (k % 2) * 60, ry + 18), fill=f.LINE, width=6)
    f.d.rectangle((1318, ry + 6, 1342, ry + 30), outline=f.TEAL, width=3)
    if k < 2:
        f.d.line([(1322, ry + 18), (1329, ry + 25), (1340, ry + 9)], fill=f.AMBER, width=4, joint='curve')
f.d.line((920, 540, 1350, 540), fill=f.LINE, width=2)
f.arrow([(795, 440), (885, 440)])
f.centered(840, 396, '書き込む', 22, f.TEAL)

# 下：本人が見て実行し、声で指示する
f.arrow([(1135, 566), (1135, 628)], f.BLUE, 5)
f.person(1135, 700, .55)
f.text(1205, 680, '見て・チェック', 23)
f.text(1205, 714, '実行する', 23)
f.arrow([(1068, 712), (700, 712), (700, 646)], f.AMBER, 5)
f.centered(884, 722, '声で指示', 22, f.AMBER)

# Todoistへの書き戻しは、本人が指示したときだけ（点線）
f.dashed_arrow([(620, 372), (620, 198), (129, 198), (129, 214)], f.FAINT, 4)
f.centered(400, 208, '指示した分だけ反映', 21, f.GRAY)

f.footer('2026-10-21から試用（記録は8日分）／ 自動実行はしない ／ 効果は未測定')
f.im.quantize(colors=96).save(Path(__file__).with_name('cover.png'), optimize=True)
