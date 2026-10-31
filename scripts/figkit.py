"""ケース単位で図を描くための共通部品。Python 3 / Pillow / 日本語フォント。

使い方（各ケースの cases/<id>/figure.py・systems/<id>/figure.py から）:
    import figkit as fk
    fk.init(font_path)
    fk.begin(); ...; fk.save(path)

決まり（AGENTS.md「見せ方と図」）:
- 図の中に題名・副題・説明の帯・注記を入れない。絵・矢印・短いラベル（原則 12 字以内）だけで伝える
- サービスは service()（ロゴ＋名前）で示す。ロゴは scripts/logos/（Simple Icons、CC0）。無いサービスは名前の文字だけ
- 横幅は 1440px。縦は save() が中身に合わせて切り詰める（最大 900px）
- AI が読みに行く関係は pull()（AI → 取りに行く先の順に点を渡す）。AI が書き込む関係・本人の操作・通知は arrow()
"""
import math
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageFont

INK = '#243342'; TEAL = '#237b72'; BLUE = '#5679a8'; AMBER = '#bb7833'
PAPER = '#faf9f5'; LINE = '#cbd4d8'; GRAY = '#6f7479'; NOTE = '#fff4d2'; FAINT = '#d3b48f'
SIZE = (1440, 900)
MARGIN = 56
LOGOS = Path(__file__).resolve().parent / 'logos'

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


def begin(*_ignored):
    """まっさらな画布。引数（旧：題名・副題）は受け取っても描かない。"""
    global im, d
    im = Image.new('RGB', SIZE, PAPER)
    d = ImageDraw.Draw(im)


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


def _offset(points, o):
    """折れ線を法線方向に o だけずらす（角は miter）。水平・垂直の線分向け。"""
    segs = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        length = math.hypot(x1 - x0, y1 - y0) or 1
        segs.append((-(y1 - y0) / length, (x1 - x0) / length))
    out = []
    for i, (x, y) in enumerate(points):
        n1 = segs[max(i - 1, 0)]; n2 = segs[min(i, len(segs) - 1)]
        dot = n1[0] * n2[0] + n1[1] * n2[1]
        k = o / (1 + dot) if dot > -0.9 else o
        out.append((x + (n1[0] + n2[0]) * k, y + (n1[1] + n2[1]) * k))
    return out


def pull(points, color=TEAL, width=6, gap=9):
    """AI が取りに行って読む関係。points は AI → サービス（取りに行く向き）。

    細い線が AI からサービスへ向かい、太い線（データ）がサービスから AI へ戻る。
    サービスが AI に押し込んでいるように見せないための部品。AI が書き込む関係は arrow() のまま。
    """
    out = _offset(points, -gap)
    back = list(reversed(_offset(points, gap)))
    d.line(out, fill=color, width=max(2, width // 2), joint='curve')
    x, y = out[-1]; x0, y0 = out[-2]
    a = math.atan2(y - y0, x - x0)
    d.polygon([(x, y),
               (x - 13 * math.cos(a - .5), y - 13 * math.sin(a - .5)),
               (x - 13 * math.cos(a + .5), y - 13 * math.sin(a + .5))], fill=color)
    arrow(back, color, width)


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


def logo(name, cx, cy, size=72):
    """scripts/logos/<name>.png を中心 (cx, cy) に size 四方で貼る。無ければ何も描かず False を返す。"""
    path = LOGOS / f'{name}.png'
    if not path.exists():
        return False
    mark = Image.open(path).convert('RGBA').resize((size, size), Image.LANCZOS)
    im.paste(mark, (int(cx - size / 2), int(cy - size / 2)), mark)
    return True


def service(name, cx, cy, label=None, tile=132, c=LINE):
    """サービスの札：白い角丸の板にロゴ、下に名前。ロゴが無いサービスは板の中に名前を書く。

    name は scripts/logos のファイル名（openai・claude・gmail・todoist・notion・googlecalendar・googlemaps・youtube・x・github・qiita・note）。
    label を省くと名前の文字を出さない。板の大きさは tile（既定 132px）。
    """
    half = tile / 2
    rr((cx - half, cy - half, cx + half, cy + half), 'white', c, 3, 22)
    if logo(name, cx, cy, int(tile * .56)):
        if label:
            centered(cx, cy + half + 12, label, 25)
    else:
        centered(cx, cy - 15, label or name, 26)
    return cy + half


def person(x, y, s=1):
    d.ellipse((x - 30 * s, y - 80 * s, x + 30 * s, y - 20 * s), fill='#e9cdb6', outline=INK, width=3)
    d.arc((x - 36 * s, y - 91 * s, x + 36 * s, y - 23 * s), 180, 350, fill=INK, width=9)
    rr((x - 65 * s, y - 7 * s, x + 65 * s, y + 80 * s), '#f1c967', INK, 3, 22)
    d.line((x - 33 * s, y + 78 * s, x - 33 * s, y + 122 * s), fill=INK, width=8)
    d.line((x + 33 * s, y + 78 * s, x + 33 * s, y + 122 * s), fill=INK, width=8)


def laptop(x, y, w=220, h=150):
    """画面の絵（サービスを指さない「画面」そのもの）。ChatGPT・Claude を示すときは service() を使う。"""
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


def video(x, y, w=150, h=88, c=BLUE):
    rr((x, y, x + w, y + h), 'white', c, 3, 9)
    d.polygon([(x + w * .43, y + h * .25), (x + w * .43, y + h * .75), (x + w * .68, y + h * .5)], fill=c)


def folder(x, y, w=106, h=90, c=BLUE):
    d.polygon([(x, y + 14), (x + 38, y + 14), (x + 50, y), (x + w, y), (x + w, y + h), (x, y + h)],
              fill='white', outline=c)
    d.line([(x, y + 14), (x + 38, y + 14), (x + 50, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y + 14)],
           fill=c, width=3, joint='curve')


def calendar(x, y, w=172, h=142, c=BLUE):
    rr((x, y, x + w, y + h), 'white', c, 3, 12)
    d.rectangle((x, y, x + w, y + 34), fill=c)
    for r in range(3):
        for k in range(5):
            d.rectangle((x + 16 + k * 30, y + 50 + r * 28, x + 34 + k * 30, y + 68 + r * 28), outline=LINE, width=2)


def doc(x, y, w=140, h=158, c=BLUE):
    d.polygon([(x, y), (x + w - 34, y), (x + w, y + 34), (x + w, y + h), (x, y + h)], fill='white', outline=c)
    d.line([(x, y), (x + w - 34, y), (x + w, y + 34), (x + w, y + h), (x, y + h), (x, y)], fill=c, width=3, joint='curve')
    for k in range(4):
        d.line((x + 20, y + 50 + k * 26, x + w - 20, y + 50 + k * 26), fill=LINE, width=5)


def cards(title, items):
    """説明図（flow.png）。見出しと、(小見出し, [行, 行]) を 4 つ。文章で補う図なので題名を持つ。"""
    begin()
    text(64, 56, title, 40)
    for i, (label, lines) in enumerate(items):
        x = 64 + (i % 2) * 670; y = 150 + (i // 2) * 290
        rr((x, y, x + 638, y + 258))
        text(x + 28, y + 24, label, 28, TEAL)
        for k, line in enumerate(lines):
            text(x + 28, y + 93 + k * 46, line, 28)


def save(path):
    """中身の上下の余白を MARGIN に切り詰めて保存する（横幅は 1440 のまま）。"""
    bg = Image.new('RGB', im.size, PAPER)
    box = ImageChops.difference(im, bg).getbbox()
    if box:
        top = max(0, box[1] - MARGIN)
        bottom = min(im.size[1], box[3] + MARGIN)
        out = im.crop((0, top, im.size[0], bottom))
    else:
        out = im
    out.quantize(colors=128).save(path, optimize=True)
