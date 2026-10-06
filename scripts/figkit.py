"""ケース単位で図を描くための共通部品。Python 3 / Pillow / 日本語フォント。

使い方（各ケースの cases/<id>/figure.py から）:
    import figkit as fk
    fk.init(font_path)
    fk.begin('題名', '副題'); ...; fk.footer('確認状況'); fk.save(path)

色・余白・部品の形は scripts/render_covers.py（初期2件の編集元）に合わせている。
"""
import math
from PIL import Image, ImageDraw, ImageFont

INK = '#243342'; TEAL = '#237b72'; BLUE = '#5679a8'; AMBER = '#bb7833'
PAPER = '#faf9f5'; LINE = '#cbd4d8'; GRAY = '#6f7479'; NOTE = '#fff4d2'; FAINT = '#d3b48f'
SIZE = (1440, 900)

_font = None
im = None
d = None


def init(font_path):
    global _font
    _font = font_path


def jpfont(size):
    font = ImageFont.truetype(_font, size)
    try:
        font.set_variation_by_axes([500])
    except (OSError, AttributeError):
        pass
    return font


def begin(title, sub):
    global im, d
    im = Image.new('RGB', SIZE, PAPER)
    d = ImageDraw.Draw(im)
    text(64, 38, 'AI活用の仕組み', 24, TEAL)
    text(64, 83, title, 46)
    text(64, 155, sub, 23, GRAY)


def text(x, y, s, size=28, color=INK):
    d.text((x, y), s, font=jpfont(size), fill=color)


def width(s, size):
    return d.textlength(s, font=jpfont(size))


def centered(x, y, s, size=30, color=INK):
    text(x - width(s, size) / 2, y, s, size, color)


def rr(box, color='white', outline=LINE, width=3, radius=16):
    d.rounded_rectangle(box, radius=radius, fill=color, outline=outline, width=width)


def arrow(points, color=TEAL, width=6):
    d.line(points, fill=color, width=width, joint='curve')
    x, y = points[-1]; x0, y0 = points[-2]
    a = math.atan2(y - y0, x - x0)
    d.polygon([(x, y),
               (x - 19 * math.cos(a - .5), y - 19 * math.sin(a - .5)),
               (x - 19 * math.cos(a + .5), y - 19 * math.sin(a + .5))], fill=color)


def dashed_arrow(points, color=FAINT, width=4, dash=14, gap=10):
    """「必要なときだけ」の関係を示す薄い点線の矢印。水平・垂直の線分向け。"""
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        length = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / length, (y1 - y0) / length
        pos = 0
        while pos < length - 20:
            end = min(pos + dash, length - 20)
            d.line((x0 + ux * pos, y0 + uy * pos, x0 + ux * end, y0 + uy * end), fill=color, width=width)
            pos += dash + gap
    x, y = points[-1]; x0, y0 = points[-2]
    a = math.atan2(y - y0, x - x0)
    d.polygon([(x, y),
               (x - 19 * math.cos(a - .5), y - 19 * math.sin(a - .5)),
               (x - 19 * math.cos(a + .5), y - 19 * math.sin(a + .5))], fill=color)


def person(x, y, s=1):
    d.ellipse((x - 30 * s, y - 80 * s, x + 30 * s, y - 20 * s), fill='#e9cdb6', outline=INK, width=3)
    d.arc((x - 36 * s, y - 91 * s, x + 36 * s, y - 23 * s), 180, 350, fill=INK, width=9)
    rr((x - 65 * s, y - 7 * s, x + 65 * s, y + 80 * s), '#f1c967', INK, 3, 22)
    d.line((x - 33 * s, y + 78 * s, x - 33 * s, y + 122 * s), fill=INK, width=8)
    d.line((x + 33 * s, y + 78 * s, x + 33 * s, y + 122 * s), fill=INK, width=8)


def laptop(x, y, w=220, h=150):
    rr((x, y, x + w, y + h), '#eaf3f1', TEAL, 4)
    d.polygon([(x - 18, y + h + 20), (x + w + 18, y + h + 20), (x + w + 34, y + h + 37), (x - 34, y + h + 37)],
              fill='#d0dcd9', outline=TEAL)
    rr((x + 40, y + 36, x + w - 40, y + h - 35), 'white', TEAL, 3, 14)
    d.polygon([(x + 65, y + h - 35), (x + 65, y + h - 16), (x + 87, y + h - 35)], fill='white')
    for k in range(3):
        d.ellipse((x + 64 + k * 35, y + 65, x + 76 + k * 35, y + 77), fill=TEAL)


def envelope(x, y, w=130, h=86, c=BLUE, tag=None):
    """封筒。tag に色を渡すと右上にラベルの札を付ける。"""
    rr((x, y, x + w, y + h), 'white', c, 3, 9)
    d.line([(x + 5, y + 7), (x + w / 2, y + h * .56), (x + w - 5, y + 7)], fill=c, width=3, joint='curve')
    if tag:
        rr((x + w - 46, y - 16, x + w + 16, y + 14), tag, tag, 1, 8)
        d.ellipse((x + w - 38, y - 6, x + w - 28, y + 4), fill='white')


def funnel(x, y, w=110, h=120, c=BLUE):
    d.polygon([(x, y), (x + w, y), (x + w * .62, y + h * .55), (x + w * .62, y + h),
               (x + w * .38, y + h), (x + w * .38, y + h * .55)], fill='white', outline=c)
    d.line([(x, y), (x + w, y), (x + w * .62, y + h * .55), (x + w * .62, y + h), (x + w * .38, y + h),
            (x + w * .38, y + h * .55), (x, y)], fill=c, width=4, joint='curve')
    for k in range(3):
        d.line((x + 22 + k * 8, y + 16 + k * 14, x + w - 22 - k * 8, y + 16 + k * 14), fill=LINE, width=5)


def clock(cx, cy, r=36, c=BLUE):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill='white', outline=c, width=4)
    d.line((cx, cy, cx, cy - r * .58), fill=INK, width=5)
    d.line((cx, cy, cx + r * .46, cy), fill=INK, width=5)
    d.ellipse((cx - 4, cy - 4, cx + 4, cy + 4), fill=INK)


def checklist(x, y, w=104, h=116, c=TEAL):
    rr((x, y, x + w, y + h), 'white', c, 3, 10)
    for k in range(3):
        by = y + 20 + k * 30
        d.rectangle((x + 16, by, x + 34, by + 18), outline=c, width=3)
        d.line((x + 46, by + 9, x + w - 16, by + 9), fill=LINE, width=6)
    d.line([(x + 19, y + 29), (x + 24, y + 35), (x + 33, y + 21)], fill=AMBER, width=4, joint='curve')


def phone(x, y, w=84, h=144):
    rr((x, y, x + w, y + h), 'white', INK, 4, 16)
    d.line((x + w / 2 - 12, y + h - 12, x + w / 2 + 12, y + h - 12), fill=INK, width=4)
    rr((x + 10, y + 20, x + w - 10, y + 58), NOTE, AMBER, 3, 8)
    d.ellipse((x + 18, y + 33, x + 30, y + 45), fill=AMBER)
    d.line((x + 38, y + 39, x + w - 20, y + 39), fill=AMBER, width=5)


def footer(status):
    rr((64, 808, 1376, 865), '#f1ede5', '#f1ede5', 1, 12)
    text(88, 822, status, 23, '#795527')
    text(64, 876, '実画面ではなく、役割と関係を示す概念図', 16, GRAY)


def cards(title, status, items):
    """説明図（flow.png）。items は (見出し, [行, 行]) を4つ。"""
    begin(title, '作業・判断・検証状況の補足')
    for i, (label, lines) in enumerate(items):
        x = 64 + (i % 2) * 670; y = 226 + (i // 2) * 278
        rr((x, y, x + 638, y + 246))
        text(x + 28, y + 24, label, 28, TEAL)
        for k, line in enumerate(lines):
            text(x + 28, y + 93 + k * 46, line, 28)
    footer(status)


def save(path):
    im.save(path, optimize=True)
