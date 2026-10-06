"""このケースの概念図だけを再生成する。Python 3 / Pillow / 美咲FONTX2。
部品は scripts/figkit.py。ほかのケースのPNGには触れない。

    python cases/daily-todoist-triage/figure.py --font /absolute/path/MISAKI.FNT

元フォント（リポジトリには同梱しない）:
https://github.com/yuyabu/MisakiFont-sandbox/blob/082d58b660a27d3dbb08883eccfbc6c91450eb6e/MISAKI.FNT
美咲フォント Copyright(C) Num Kadoma。商用・非商用の使用・改変・再配布が許可されている。
ライセンス: https://github.com/up9cloud/font-misaki/blob/master/misaki/misaki.txt
生成後は欠字・切れ・重なりと確認状況の表記を目視確認する。
初版は同じ配置・ビットマップ字形をJavaScriptで描画し、PNGを目視確認した。
"""
import argparse
import json
import struct
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import figkit as fk

parser = argparse.ArgumentParser()
parser.add_argument("--font", required=True, help="美咲8x8 FONTX2のMISAKI.FNT")
data = Path(parser.parse_args().font).read_bytes()
if data[:6] != b"FONTX2" or data[14:17] != bytes([8, 8, 1]):
    raise ValueError("8x8の2バイト文字用FONTX2が必要です")
blocks = []
base = 18 + data[17] * 4
for i in range(data[17]):
    lo, hi = struct.unpack_from("<HH", data, 18 + i * 4)
    blocks.append((lo, hi, base))
    base += (hi - lo + 1) * 8

def glyph(ch):
    if "!" <= ch <= "~":
        ch = chr(ord(ch) + 0xFEE0)
    elif ch == " ":
        ch = "　"
    code = int.from_bytes(ch.encode("cp932"), "big")
    for lo, hi, offset in blocks:
        if lo <= code <= hi:
            at = offset + (code - lo) * 8
            return data[at:at + 8]
    raise ValueError("フォントにない文字: " + ch)

def bitmap_text(x, y, s, size=32, color=fk.INK):
    # 同一の8x8字形を拡大する。本文は絵の外に短いラベルとして置く。
    scale = size / 8
    for ch in s:
        for row, bits in enumerate(glyph(ch)):
            for col in range(8):
                if bits & (128 >> col):
                    fk.d.rectangle((x + col * scale, y + row * scale,
                                    x + (col + 1) * scale - 1,
                                    y + (row + 1) * scale - 1), fill=color)
        x += size

fk.im = Image.new("RGB", fk.SIZE, fk.PAPER)
fk.d = ImageDraw.Draw(fk.im)
fk.text = bitmap_text
fk.centered = lambda x, y, s, size=32, color=fk.INK: bitmap_text(x - len(s) * size / 2, y, s, size, color)
SCENE = json.loads(r'''[["text",64,40,"AI活用の仕組み",24,"#237b72"],["text",64,90,"毎朝のタスク整理をAIへ",48],["text",64,165,"本人が基準を決める",24,"#6f7479"],["rr",[86,280,246,392],"white","#5679a8",3,12],["line",[[116,310],[212,310]],"#cbd4d8",6],["line",[[116,337],[194,337]],"#cbd4d8",6],["line",[[116,364],[206,364]],"#cbd4d8",6],["rr",[214,398,374,510],"white","#bb7833",3,12],["line",[[244,428],[340,428]],"#cbd4d8",6],["line",[[244,455],[322,455]],"#cbd4d8",6],["line",[[244,482],[334,482]],"#cbd4d8",6],["centered",230,545,"Inbox",32,"#5679a8"],["centered",230,590,"音声・外部入力",24],["arrow",[[405,403],[567,403]]],["clock",645,270,42],["text",706,250,"毎朝6時",32,"#5679a8"],["laptop",610,330,220,160],["centered",720,545,"ChatGPT",32,"#237b72"],["centered",720,590,"分類・期限見直し",24],["arrow",[[870,403],[981,403]]],["rr",[1010,252,1370,520],"white","#237b72",3,16],["text",1034,270,"Todoist",24,"#237b72"],["rr",[1034,318,1060,344],"white","#237b72",3,4],["line",[[1078,331],[1293,331]],"#cbd4d8",6],["rr",[1060,366,1086,392],"white","#5679a8",3,4],["line",[[1104,379],[1304,379]],"#cbd4d8",6],["line",[[1047,344],[1047,379],[1058,379]],"#5679a8",3],["rr",[1034,414,1114,453],"#fff4d2","#bb7833",2,8],["text",1042,421,"2分",24,"#bb7833"],["rr",[1130,414,1234,453],"#eaf3f1","#237b72",2,8],["text",1138,421,"10分",24,"#237b72"],["poly",[[1270,414],[1270,458],[1275,440],[1312,440],[1312,414]],"#bb7833"],["centered",1190,545,"整理結果",32],["centered",1190,590,"朝の自動化は未検証",24,"#6f7479"],["person",218,711,0.48],["centered",218,780,"本人の判断",24],["rr",[372,680,814,750],"#fff4d2","#e7ca7c",2,12],["centered",593,695,"優先度・例外・期限",24],["arrow",[[281,720],[354,720]],"#bb7833",5],["arrow",[[720,675],[720,630]],"#bb7833",5],["centered",1095,700,"繰り返しは除外",24,"#6f7479"],["rr",[64,820,1376,865],"#f1ede5","#f1ede5",1,12],["text",88,830,"初回整理・設定を確認／自動実行は未確認",24,"#795527"],["text",64,878,"実画面ではない概念図",16,"#6f7479"]]''')
for op, *args in SCENE:
    if op == "line":
        fk.d.line([tuple(p) for p in args[0]], fill=args[1], width=args[2], joint="curve")
    elif op == "poly":
        fk.d.polygon([tuple(p) for p in args[0]], fill=args[1])
    else:
        getattr(fk, op)(*args)
fk.save(HERE / "cover.png")
