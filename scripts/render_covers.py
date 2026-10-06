"""Render editable conceptual diagrams; no screenshots or measured claims."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def render(case, title, badge, items):
    im = Image.new('RGB', (1440, 900), '#f5f6f8')
    d = ImageDraw.Draw(im)
    def txt(x,y,s,size=28,color='#172234',bold=False):
        d.text((x,y),s,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=color)
    txt(64,44,'AI USE CASES / CONCEPT DIAGRAM',20,'#526277',True)
    txt(64,87,title,46,bold=True)
    txt(64,155,badge,23,'#7b5423')
    for i,(label,lines,icon) in enumerate(items):
        x=64+(i%2)*670; y=226+(i//2)*290
        d.rounded_rectangle((x,y,x+638,y+258),radius=18,fill='white',outline='#dce1e7',width=2)
        txt(x+28,y+24,label,23,'#34766d',True)
        for j,line in enumerate(lines): txt(x+28,y+141+j*37,line,27)
        # Compact pictograms convey list, clock, decision, and result.
        ix=x+34; iy=y+76
        if icon=='list':
            for k in range(3):
                d.rectangle((ix,iy+k*16,ix+9,iy+k*16+9),fill='#526277')
                d.line((ix+18,iy+k*16+5,ix+130-k*20,iy+k*16+5),fill='#526277',width=4)
        elif icon=='clock':
            d.ellipse((ix,iy-6,ix+54,iy+48),outline='#526277',width=4)
            d.line((ix+27,iy+3,ix+27,iy+21,ix+41,iy+21),fill='#526277',width=4)
        elif icon=='choice':
            d.polygon([(ix+27,iy-7),(ix+57,iy+21),(ix+27,iy+49),(ix-3,iy+21)],outline='#526277',width=4)
            d.line((ix+60,iy+21,ix+132,iy+21),fill='#526277',width=4)
        else:
            for k in range(3):
                d.rounded_rectangle((ix+k*62,iy,ix+k*62+46,iy+46),radius=5,outline='#526277',width=3)
            txt(ix+17,iy+4,'?',30,'#7b5423',True)
    txt(64,841,'Conceptual workflow. Status is shown above; outcomes require evidence.',20,'#526277')
    im.save(ROOT/'cases'/case/'cover.png',optimize=True)

render('youtube-playlist-cleanup','YouTube playlist cleanup','REQUEST CAPTURED / Completion not verified',[
    ('01 / PROBLEM',['Many playlists to inspect','Manual cleanup takes attention'],'list'),
    ('02 / AI WORK',['Inspect, classify, propose','Operate within agreed scope'],'list'),
    ('03 / HUMAN DECISIONS',['Define keep / merge / delete','Resolve exceptions'],'choice'),
    ('04 / VERIFICATION',['Check actual changes','Measure time before claiming gains'],'result'),
])
render('scheduled-reviews','Scheduled AI reviews','ACTIVE SETUP + RUN RECORDS / Outputs not verified',[
    ('01 / PROBLEM',['Repeated reviews and research','Need a recurring trigger'],'clock'),
    ('02 / AI WORK',['Read current sources, analyze','Save and report where authorized'],'list'),
    ('03 / HUMAN DECISIONS',['Set cadence and evaluation rules','Choose the next action'],'choice'),
    ('04 / VERIFICATION',['Run records confirmed','Check outputs and useful impact'],'result'),
])
