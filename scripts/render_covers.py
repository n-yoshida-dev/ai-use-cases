"""日本語の概念図と説明図を再生成。Python 3 / Pillow / 日本語フォント。"""
from pathlib import Path
import argparse, math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--font', required=True, help='Noto Sans JP等の日本語フォント')
FONT = parser.parse_args().font
INK='#243342'; TEAL='#237b72'; BLUE='#5679a8'; AMBER='#bb7833'
PAPER='#faf9f5'; LINE='#cbd4d8'
im=None; d=None

def begin(title,sub):
    global im,d
    im=Image.new('RGB',(1440,900),PAPER); d=ImageDraw.Draw(im)
    text(64,38,'AI活用の仕組み',24,TEAL)
    text(64,83,title,46)
    text(64,155,sub,23,'#6f7479')

def jpfont(size):
    font=ImageFont.truetype(FONT,size)
    try:
        font.set_variation_by_axes([500])
    except (OSError, AttributeError):
        pass
    return font

def text(x,y,s,size=28,color=INK):
    font=jpfont(size)
    d.text((x,y),s,font=font,fill=color)

def centered(x,y,s,size=30,color=INK):
    font=jpfont(size)
    w=d.textlength(s,font=font); text(x-w/2,y,s,size,color)

def rr(box,color='white',outline=LINE,width=3,radius=16):
    d.rounded_rectangle(box,radius=radius,fill=color,outline=outline,width=width)

def arrow(points,color=TEAL,width=6):
    d.line(points,fill=color,width=width,joint='curve')
    x,y=points[-1]; x0,y0=points[-2]; a=math.atan2(y-y0,x-x0)
    pts=[(x,y),(x-19*math.cos(a-.5),y-19*math.sin(a-.5)),(x-19*math.cos(a+.5),y-19*math.sin(a+.5))]
    d.polygon(pts,fill=color)

def video(x,y,w=150,h=88,c=BLUE):
    rr((x,y,x+w,y+h),'white',c,3,9)
    d.polygon([(x+w*.43,y+h*.25),(x+w*.43,y+h*.75),(x+w*.68,y+h*.5)],fill=c)

def person(x,y,s=1):
    d.ellipse((x-30*s,y-80*s,x+30*s,y-20*s),fill='#e9cdb6',outline=INK,width=3)
    d.arc((x-36*s,y-91*s,x+36*s,y-23*s),180,350,fill=INK,width=9)
    rr((x-65*s,y-7*s,x+65*s,y+80*s),'#f1c967',INK,3,22)
    d.line((x-33*s,y+78*s,x-33*s,y+122*s),fill=INK,width=8)
    d.line((x+33*s,y+78*s,x+33*s,y+122*s),fill=INK,width=8)

def laptop(x,y,w=220,h=150):
    rr((x,y,x+w,y+h),'#eaf3f1',TEAL,4)
    d.polygon([(x-18,y+h+20),(x+w+18,y+h+20),(x+w+34,y+h+37),(x-34,y+h+37)],fill='#d0dcd9',outline=TEAL)
    # Chat bubble with three large dots.
    rr((x+40,y+36,x+w-40,y+h-35),'white',TEAL,3,14)
    d.polygon([(x+65,y+h-35),(x+65,y+h-16),(x+87,y+h-35)],fill='white')
    for k in range(3): d.ellipse((x+64+k*35,y+65,x+76+k*35,y+77),fill=TEAL)

def folder(x,y,w=106,h=90,c=BLUE):
    rr((x,y,x+w*.55,y+30),c,c,2,5)
    rr((x,y+20,x+w,y+h),'white',c,3,8)
    video(x+17,y+36,w-34,38,c)

def calendar(x,y,w=172,h=142):
    rr((x,y,x+w,y+h),'white',BLUE,3)
    d.rectangle((x+2,y+18,x+w-2,y+48),fill=BLUE)
    for k in range(2): d.line((x+38+k*90,y-12,x+38+k*90,y+22),fill=INK,width=6)
    for j in range(2):
        for k in range(3):
            d.ellipse((x+27+k*47,y+64+j*35,x+40+k*47,y+77+j*35),fill=BLUE)

def doc(x,y,w=140,h=158,c=BLUE):
    rr((x,y,x+w,y+h),'white',c,3,10)
    for k,l in enumerate([.7,.5,.66]):
        d.line((x+24,y+35+k*23,x+w*l,y+35+k*23),fill=LINE,width=6)
    d.rectangle((x+24,y+h-49,x+42,y+h-20),fill=c)
    d.rectangle((x+53,y+h-65,x+71,y+h-20),fill=TEAL)
    d.rectangle((x+82,y+h-83,x+100,y+h-20),fill=AMBER)

def footer(status):
    rr((64,808,1376,865),'#f1ede5','#f1ede5',1,12)
    text(88,822,status,23,'#795527')
    text(64,876,'実画面ではなく、役割と関係を示す概念図',16,'#6f7479')

def save(case,name):
    im.save(ROOT/'cases'/case/name,optimize=True)

begin('YouTubeの整理をAIへ任せる','人が基準を決める → AIが確認・整理する')
# disorder is visible without reading paragraphs
for x,y,c in [(97,330,BLUE),(254,267,AMBER),(157,435,TEAL),(310,396,BLUE)]:
    video(x,y,140,86,c)
centered(250,555,'増えたマイリスト',32)
laptop(615,325,210,162)
centered(720,523,'ChatGPT Work',32,TEAL)
centered(720,568,'棚卸し・操作',29)
for x,y,c in [(1010,324,BLUE),(1142,324,TEAL),(1076,458,AMBER)]:
    folder(x,y,105,88,c)
centered(1130,574,'整理後の姿（想定）',31)
arrow([(455,408),(590,408)])
arrow([(854,408),(983,408)])
person(405,660,.65)
centered(406,745,'本人',26)
rr((510,658,762,729),'#fff4d2','#e7ca7c',2,12)
centered(636,674,'残す・まとめる基準',26)
arrow([(768,690),(916,690),(916,555),(850,555)],AMBER,5)
arrow([(446,677),(493,677)],AMBER,5)
footer('依頼・方針を記録済み ／ 整理の完了結果は未確認')
save('youtube-playlist-cleanup','cover.png')

begin('定期レビューをAIに任せる','毎回の依頼を、周期と判断基準の設定へ')
calendar(103,282)
centered(190,460,'実行の周期',30)
doc(99,552,145,150)
centered(180,718,'最新の記録',30)
laptop(615,388,210,162)
centered(720,582,'ChatGPT',32,TEAL)
centered(720,628,'確認・分析',30)
doc(1065,286,145,154,TEAL)
centered(1140,459,'レビュー結果',30)
person(1135,648,.72)
centered(1135,750,'本人が判断',30)
arrow([(299,364),(435,364),(435,445),(590,445)])
arrow([(275,626),(440,626),(440,500),(590,500)])
arrow([(855,461),(958,461),(958,365),(1036,365)])
arrow([(1140,499),(1140,548)],BLUE,5)
# feedback from human to cadence, rather than a linear fan-out
arrow([(1050,683),(914,683),(914,239),(190,239),(190,267)],AMBER,5)
centered(630,194,'方針・周期を見直す',26,AMBER)
footer('有効設定・実行日時を確認 ／ 成果物の内容・効果は未検証')
save('scheduled-reviews','cover.png')

def details(case,title,status,items):
    begin(title,'作業・判断・検証状況の補足')
    for i,(label,lines) in enumerate(items):
        x=64+(i%2)*670; y=226+(i//2)*278
        rr((x,y,x+638,y+246))
        text(x+28,y+24,label,28,TEAL)
        for k,line in enumerate(lines): text(x+28,y+93+k*46,line,28)
    footer(status)
    save(case,'flow.png')

details('youtube-playlist-cleanup','YouTube整理：作業と判断の分担','依頼を記録済み ／ 実際の変更・完了結果は未確認',[
    ('課題',['増えたマイリストの確認と整理を','人間が一つずつ行う負担がある']),
    ('AIの作業',['棚卸し・分類・統合候補の抽出','許可された範囲で画面を操作する']),
    ('人間の判断',['残す基準、統合・削除の方針','必要な例外を判断する']),
    ('確認すること',['実際の変更件数と整理結果','時間削減は測定後に記録する']),
])
details('scheduled-reviews','定期レビュー：作業と判断の分担','設定・実行日時を確認 ／ 各成果物の成功を示すものではない',[
    ('課題',['定期確認や情報収集のたびに','人間が依頼・確認を繰り返す']),
    ('AIの作業',['最新の記録・情報を確認し分析する','許可した範囲へ保存・更新・報告']),
    ('人間の判断',['目的・周期・判断基準を設定する','提案の採否と次の行動を決める']),
    ('確認すること',['設定と実行日時は確認済み','成果物の正確性と効果は未検証']),
])
