"""python figure.py --font /path/to/JapaneseFont.ttf。概念図のみを再生成。"""
import argparse, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'scripts'))
import figkit as f
p=argparse.ArgumentParser();p.add_argument('--font',required=True)
f.init(p.parse_args().font)
f.begin('保存した情報を、使える形へ','分類・移行はAIへ委譲／迷うものは本人が判断')
f.phone(100,330,110,190)
f.d.polygon([(130,410),(181,410),(181,476),(156,460),(130,476)],fill=f.BLUE)
f.centered(155,568,'X：一時保存',27)
f.arrow([(240,423),(460,423)])
f.laptop(480,350,225,160)
f.centered(593,570,'AIが振り分け',28,f.TEAL)
f.person(565,270,.35);f.text(605,235,'気づいた時',25,f.BLUE)
f.person(590,701,.42);f.centered(590,776,'本人の判断',22)
f.arrow([(590,663),(590,616)],f.AMBER)
for y in [250,395,540,685]:
    f.arrow([(752,425),(825,425),(825,y+40),(907,y+40)],f.TEAL,5)
f.rr((930,223,1060,330),'#eaf3f1',f.TEAL)
for x in [947,982,1017]:
    f.rr((x,245,x+24,306),'white',f.TEAL,2,4)
f.text(1090,230,'Raindrop',30,f.TEAL);f.text(1090,279,'読む・資料',24)
f.checklist(943,366,105,112,f.BLUE)
f.text(1090,373,'Notion',30,f.BLUE);f.text(1090,422,'購入検討',24)
f.checklist(943,513,105,112,f.AMBER)
f.text(1090,520,'Todoist',30,f.AMBER);f.text(1090,570,'近々の買い物',24)
f.rr((930,659,1060,767),'white',f.BLUE)
f.d.line([(950,678),(1039,749)],fill=f.LINE,width=12)
f.d.line([(947,747),(1038,680)],fill=f.LINE,width=12)
f.d.ellipse((980,680,1013,713),fill=f.TEAL)
f.d.polygon([(982,703),(1011,703),(996,733)],fill=f.TEAL)
f.text(1090,671,'Google Maps',28,f.BLUE);f.text(1090,722,'行きたい場所',24)
f.footer('初回整理を確認／定期は停止中・本人が気づいたときに依頼')
f.save(HERE/'cover.png')
