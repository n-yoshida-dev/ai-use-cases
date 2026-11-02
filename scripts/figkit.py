"""ケース単位で図を描くための共通部品。Python 3 / Pillow / 日本語フォント。

使い方（各ケースの cases/<id>/figure.py・systems/<id>/figure.py から）:
    import figkit as fk
    fk.init(font_path)
    fk.begin(); ...; fk.save(path)

決まり（AGENTS.md「見せ方と図」）:
- 図の中に題名・副題・説明の帯・注記を入れない。絵・矢印・短いラベル（原則 12 字以内）だけで伝える
- サービスは service()（ロゴ＋名前）で示す。ロゴは scripts/logos/（Simple Icons、CC0）。無いサービスは名前の文字だけ
- 横幅は 1440px。縦は save() が中身に合わせて切り詰める（最大 900px）
- 矢印 1 本＝データが動く向き（根元が出どころ、先端が行き先。2026-11-01 本人が選んだ流儀。DFD）。線は flow() の 1 種類
  - 読まれる側（入力）を左、AI を中央、書かれる側（出力）を右に置き、矢印は原則右向きにそろえる
  - ラベルは動くデータの名詞（新着メール・タスク・朝の報告）。動詞は AI の札の下に書く（「読んで仕分け」）
  - 往復・両端の矢印は描かない。読み書き両方の相手は、同じロゴを左右に 2 回置く（印は付けない）
  - 定期実行のきっかけは trigger() で AI の札の真上に置く。線の上に置かない
  - 矢印は 1 色（TEAL）。色で意味を分けない（2026-11-02 本人）
  - 今動いている流れだけを描く。予定の流れは描かず本文に書く（点線は使わない。2026-11-02）
  - 最初に 1 回決めた手順書・基準は、AI が毎回読む置き場として AI の左に置く。本人からの矢印は描かない
    （毎回本人が渡しているように見えるため。本人から引くのは毎回渡す頼みごと・進捗・答えだけ。2026-11-02）
  - 番号の丸・＊などの記号は使わない
- 人は person()（顔を描かない 1 色の人型。2026-11-01 本人が選んだ形）
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


def _head(points, color, width):
    """開いた V 字の矢じり。"""
    x, y = points[-1]; x0, y0 = points[-2]
    a = math.atan2(y - y0, x - x0)
    for k in (-.5, .5):
        d.line((x, y, x - 20 * math.cos(a + k), y - 20 * math.sin(a + k)), fill=color, width=width)


def arrow(points, width=4):
    """データが動く向きの矢印（ラベルなし）。ふつうは flow() を使う。色は TEAL の 1 色だけ。"""
    d.line(points, fill=TEAL, width=width, joint='curve')
    _head(points, TEAL, width)


def flow(points, label=None, at=None, size=23, width=4):
    """データの流れ：points は出どころ → 行き先の順。label は動くデータの名詞（12 字以内）。

    ラベルは既定で一番長い横の区間の中央の上に置く（横の区間が無ければ一番長い縦の区間の右）。
    at=(x, y) を渡すと、その点を中央・上端にして置く。
    """
    arrow(points, width)
    color = TEAL
    if not label:
        return
    if at:
        centered(at[0], at[1], label, size, color)
        return
    segs = list(zip(points, points[1:]))
    hor = [s for s in segs if abs(s[0][1] - s[1][1]) < 1]
    if hor:
        (x0, y0), (x1, _) = max(hor, key=lambda s: abs(s[1][0] - s[0][0]))
        centered((x0 + x1) / 2, y0 - size - 14, label, size, color)
    else:
        (x0, y0), (_, y1) = max(segs, key=lambda s: abs(s[1][1] - s[0][1]))
        text(x0 + 14, (y0 + y1) / 2 - size / 2 - 4, label, size, color)


def verb(cx, top, s):
    """AI の札の下に書く動詞（「読んで仕分け」）。どの図でも灰色・24px にそろえる（2026-11-02）。
    top は service() が名前を書いた行の下（名前つきの札なら cy + tile/2 + 12 + 36）。"""
    centered(cx, top, s, 24, GRAY)


def trigger(cx, top, label='毎朝6時', c=BLUE):
    """定期実行のきっかけ。時計と文字を 1 行にして、AI の札（上端 top・中心 cx）の真上に置く。"""
    r = 26
    w = 2 * r + 12 + width(label, 24)
    x0 = cx - w / 2
    cy = top - r - 16
    clock(x0 + r, cy, r, c)
    text(x0 + 2 * r + 12, cy - 17, label, 24, c)


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

    name は scripts/logos のファイル名（openai・claude・gmail・todoist・notion・googlecalendar・googlemaps・youtube・x・github・qiita・note・
    amazon・keepa・mercari・raindrop。一覧と出どころは scripts/logos/README.md）。
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


def plugin(host, guest, cx, cy, label=None, tile=132, c=LINE):
    """プラグイン・コネクタで別のサービスを使う AI の札：1 枚の板に AI のロゴ × サービスのロゴを並べる
    （例：ChatGPT のメルカリプラグイン＝plugin('openai', 'mercari', ...)。2026-11-02 本人「チャット GPT とメルカリのロゴが
    掛け合わさってるみたいな見せ方」）。板は横長（幅 tile×1.7）。下に名前。板の左右の辺の x を返す。"""
    w, half = tile * 1.7, tile / 2
    rr((cx - w / 2, cy - half, cx + w / 2, cy + half), 'white', c, 3, 22)
    size = int(tile * .5)
    logo(host, cx - w * .24, cy, size)
    centered(cx, cy - 22, '×', 30, GRAY)
    logo(guest, cx + w * .24, cy, size)
    if label:
        centered(cx, cy + half + 12, label, 25)
    return cx - w / 2, cx + w / 2


def person(x, y, s=1, c=INK):
    """人：顔を描かない 1 色の人型（丸い頭となだらかな肩）。外形は x±68s、y-84s〜y+118s。"""
    d.ellipse((x - 34 * s, y - 84 * s, x + 34 * s, y - 16 * s), fill=c)
    d.rounded_rectangle((x - 68 * s, y - 4 * s, x + 68 * s, y + 118 * s), radius=int(62 * s), fill=c)
    d.rectangle((x - 68 * s, y + 60 * s, x + 68 * s, y + 118 * s), fill=c)


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
