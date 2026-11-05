import sys; sys.path.insert(0,'.')
from lib4 import *; from pal4 import P
import random
def write(key,back,mid,front,defs_b='',defs_m='',defs_f=''):
    svg(f'land4-{key}-back.svg',360,420,back,defs_b); svg(f'land4-{key}-mid.svg',360,520,mid,defs_m); svg(f'land4-{key}-front.svg',360,220,front,defs_f)

# ---------- ورزشگاه ----------
def stadium():
    c=P('stadium'); R=random.Random(11)
    defs=rg('fl',[(0,c['glow'],.95),(.35,c['glow'],.35),(1,c['glow'],0)])+lg('stf',[(0,c['stand_far']),(1,c['stand_near'])])+lg('gr',[(0,c['pitch_a']),(1,c['pitch_b'])])+lg('sh',[(0,'#000',.0),(1,'#000',.38)])
    back=''.join(circ(R.uniform(10,350),R.uniform(8,170),R.choice([.8,1,1.3]),'#ebede9',R.uniform(.35,.8)) for _ in range(22))
    defs_b=rg('hz1',[(0,c['sky3'],.35),(1,c['sky3'],0)])+rg('hz2',[(0,c['sky2'],.4),(1,c['sky2'],0)])
    back+=ell(90,170,190,90,'url(#hz1)')+ell(300,120,170,70,'url(#hz2)')
    for x,y,s in ((60,60,1),(250,36,.8),(320,110,.6)):
        back+=f'<g fill="{c["crowd4"]}" opacity=".16" transform="translate({x},{y}) scale({s})"><ellipse rx="40" ry="10"/><ellipse cx="-14" cy="-8" rx="18" ry="11"/><ellipse cx="12" cy="-10" rx="22" ry="13"/></g>'
    mid=''
    # سکوی دور: نوار منحنی + تماشاگران ریز
    mid+=path('M-10,150 L-10,70 Q180,18 370,70 L370,150Z',f='url(#stf)')
    mid+=path('M-10,150 L-10,108 Q180,60 370,108 L370,150Z',f=c['stand_near'],op=.55)
    cols=[c['crowd1'],c['crowd2'],c['crowd3'],c['crowd4']]
    for row in range(4):
        for k in range(44):
            x=k*8.4+R.uniform(-1,1); y=88+row*13+((x-180)/180)**2*14-30+R.uniform(-1,1)
            mid+=circ(x,y,1.9,R.choice(cols),.62)
    # برج نورافکن
    for x in (46,314):
        mid+=rect(x-2,34,4,112,c['wall'],1)+rect(x-14,22,28,14,c['wall'],3)+circ(x,29,26,'url(#fl)',1)
        for dx in (-9,-3,3,9): mid+=circ(x+dx,29,1.8,c['glow'],.95)
    # زمین
    defs2=lg('gr2',[(0,'#5a98a0'),(.5,c['pitch_a']),(1,'#2f5961')])
    mid+=rect(-10,146,380,400,'url(#gr2)')
    # راه‌راه چمن با پرسپکتیو
    for i in range(-7,8,2): mid+=poly([(180+i*34,146),(180+(i+1)*34,146),(180+(i+1)*128,540),(180+i*128,540)],'#fff',.07)
    # پیست دور (قوس) با خط‌های راه
    mid+=path('M-30,240 Q180,128 390,240 L390,300 Q180,190 -30,300Z',f=c['track'],op=.95)
    for k,o in enumerate((250,264,278)): mid+=path(f'M-30,{o} Q180,{o-112} 390,{o}',st='#ba756a',sw=2,op=.7)
    mid+=path('M-30,300 Q180,190 390,300',st='#e9b5a3',sw=3,op=.35)
    # خط‌کشی زمین
    mid+=path('M-10,350 L370,350',st=c['line'],sw=3,op=.4)
    mid+=ell(180,350,64,20,'none',.45,ex=f'stroke="{c["line"]}" stroke-width="3"')+circ(180,350,3.5,c['line'],.6)
    mid+=path('M70,350 L40,440 L320,440 L290,350',st=c['line'],sw=3,op=.38)+path('M110,440 L96,500 L264,500 L250,440',st=c['line'],sw=3,op=.34)
    mid+=ell(180,146,260,18,c['sky3'],.28)
    mid+=rect(0,400,360,120,'#0e0c1a',op=.16)
    front=rect(0,0,360,220,'none')
    front+=path('M-10,230 L-10,196 Q22,206 40,230Z',f='#0e0c1a',op=.55)+path('M370,230 L370,192 Q338,204 320,230Z',f='#0e0c1a',op=.55)
    for i,(x,y) in enumerate(((20,198),(36,210),(340,192),(322,208))): front+=circ(x,y,2.4,[c['crowd1'],c['crowd2']][i%2],.8)
    write('stadium',back,mid,front,defs_b=defs_b,defs_m=defs+defs2)

# ---------- فضا ----------
def space():
    c=P('space'); R=random.Random(5)
    defs=rg('neb1',[(0,c['nebula'],.45),(1,c['nebula'],0)])+rg('neb2',[(0,c['sky3'],.5),(1,c['sky3'],0)])+lg('pa',[(0,c['planetA']),(1,c['planetA_s'])],0,0,1,1)+lg('pb',[(0,c['planetB']),(1,c['planetB_s'])],0,0,1,1)+lg('gro',[(0,'#394a50'),(1,'#202e37')])+lg('hu',[(0,c['hull']),(1,c['hull_s'])])
    back=ell(80,110,170,90,'url(#neb2)')+ell(280,260,160,100,'url(#neb1)')
    for _ in range(46):
        x,y=R.uniform(6,354),R.uniform(6,400); back+=circ(x,y,R.choice([.7,.9,1.2,1.6]),c['star'] if R.random()<.8 else c['star2'],R.uniform(.35,.9))
    for x,y,r in ((300,70,7),(60,260,6),(190,180,5)): back+=star4(x,y,r,c['star'],.8)
    # سیارهٔ صورتی با حلقه
    back+=f'<g transform="translate(86,110) rotate(-18)"><ellipse rx="86" ry="17" fill="none" stroke="{c["ring"]}" stroke-width="8" opacity=".5"/>{circ(0,0,46,"url(#pa)")}<path d="M-86,0 A86,17 0 0 0 86,0" fill="none" stroke="{c["ring"]}" stroke-width="8" opacity=".6"/></g>'
    back+=circ(310,330,30,'url(#pb)')+path('M290,320 Q300,306 322,310',st='#fff',sw=3,op=.25)
    mid=ell(180,160,230,40,c['sky3'],.35)
    mid+=path('M-10,520 L-10,175 Q80,150 180,160 Q280,150 370,172 L370,520Z',f='url(#gro)')
    for x,y,rx,ry in ((60,230,34,8),(290,260,40,10),(140,330,26,6),(250,420,36,9),(40,440,28,7)):
        mid+=ell(x,y,rx,ry,'#10141f',.45)+ell(x,y-1.5,rx*.9,ry*.7,'#4a5462',.5)
    # ایستگاه (راست بالا)
    mid+=f'<g transform="translate(246,70)">{path("M0,92 Q0,24 60,24 Q120,24 120,92Z",f="url(#hu)")}{rect(-40,86,200,14,c["hull_s"],5)}{rect(56,0,3,26,c["hull"])}{circ(57.5,0,3.5,c["lamp"])}'
    for i in range(5): mid+=rect(16+i*18,52,10,8,'#fee761',2,.9)
    mid+=rect(-70,60,56,26,'#3c5e8b',3,.9)+rect(134,60,56,26,'#3c5e8b',3,.9)+'</g>'
    mid+=rect(0,380,360,140,'#05060c',op=.28)
    front=''
    for x,y,r in ((14,200,22),(344,196,26)): front+=ell(x,y+10,r*1.4,r*.5,'#05060c',.5)+circ(x,y,r,'#2b3340',.95)
    write('space',back,mid,front,defs_m=defs,defs_b=defs)

# ---------- مزرعه ----------
def farm():
    c=P('farm'); R=random.Random(8)
    defs=rg('sunr',[(0,c['sun'],.95),(.4,c['sun'],.3),(1,c['sun'],0)])+lg('fi',[(0,'#b79970'),(1,'#7c6548')])+lg('rv',[(0,'#73b4f0'),(1,c['river'])],0,0,1,0)+lg('hm',[(0,c['hill_mid']),(1,c['hill_near'])])
    back=circ(84,120,120,'url(#sunr)')+circ(84,120,24,c['sun'],.98)
    for x,y,s in ((250,64,1.1),(318,150,.7),(168,214,.9),(36,260,.6)):
        back+=f'<g fill="{c["cloud"]}" opacity=".8" transform="translate({x},{y}) scale({s})"><ellipse rx="40" ry="10"/><ellipse cx="-14" cy="-8" rx="18" ry="11"/><ellipse cx="12" cy="-10" rx="22" ry="13"/></g>'
    for x,y in ((190,96),(206,110),(176,114)): back+=path(f'M{x-6},{y} q6,-6 6,0 q0,-6 6,0',st='#253a5e',sw=1.8,op=.7)
    mid=ell(180,150,260,26,c['sky3'],.5)
    mid+=path(smooth_ridge(360,110,16,2,6,520),f=c['hill_far'])+path(smooth_ridge(360,138,14,4,6,520),f='url(#hm)')
    # آسیاب بادی
    mid+=f'<g transform="translate(262,30)">{path("M-28,126 L-17,40 L17,40 L28,126Z",f=c["wind"])}{path("M-28,126 L-17,40 L-3,40 L-9,126Z",f="#a08662",op=.4)}{path("M-22,44 L0,18 L22,44Z",f=c["roof"])}{rect(-5,92,10,34,"#7a4841",3)}{circ(0,44,5,"#4a3a3a")}'
    for a in (15,105,195,285): mid+=f'<g transform="translate(0,44) rotate({a})">{rect(-2.2,-64,4.4,62,"#7a4841")}{rect(2.4,-62,18,42,c["cloud"],1,.95)}</g>'
    mid+='</g>'
    # انبار
    mid+=f'<g transform="translate(16,80)">{poly([(0,56),(0,24),(28,2),(56,24),(56,56)],c["barn"])}{poly([(-5,26),(28,-3),(61,26),(56,31),(28,6),(0,31)],c["roof"])}{rect(17,32,22,24,"#5b2d17",2)}{path("M17,32 L39,56 M39,32 L17,56",st=c["cloud"],sw=2,op=.9)}</g>'
    mid+=rect(-10,196,380,330,'url(#fi)')
    # شیارهای کشت (پرسپکتیو)
    for i in range(-6,9): mid+=path(f'M{180+i*22},196 L{180+i*92},540',st=c['field_hi'],sw=4,op=.28)
    # رود
    mid+=path('M-10,246 Q90,224 160,278 T380,316 L380,354 Q260,348 170,318 T-10,290Z',f='url(#rv)')
    mid+=path('M10,258 Q100,242 160,288',st='#fff',sw=2.4,op=.45)+path('M200,300 Q290,318 360,312',st='#fff',sw=2.4,op=.4)
    # حصار و بالۀ کاه
    for x in range(8,360,34): mid+=rect(x,388,5,22,'#7a4841')
    mid+=rect(0,394,360,4,'#7a4841')+rect(0,402,360,3,'#7a4841')
    for x,y in ((60,470),(290,440)): mid+=ell(x,y,17,10,c['field_hi'])+ell(x,y-3,12,6,'#f0c98a',.6)
    mid+=rect(0,420,360,100,'#1d2a1d',op=.18)
    front=path('M-10,230 L-10,176 Q8,156 14,196 Q26,162 42,230Z',f=c['hill_near'])+path('M370,230 L370,170 Q352,148 342,190 Q326,158 310,230Z',f=c['hill_near'])
    for x,y in ((330,196),(346,206),(22,200)): front+=circ(x,y,3,c['flower'],.95)+circ(x,y,1.2,c['sun'])
    write('farm',back,mid,front,defs_b=defs,defs_m=defs)

# ---------- شهر ----------
def city():
    c=P('city'); R=random.Random(3)
    defs=lg('bl',[(0,c['bld']),(1,c['bld_n'])])+lg('st',[(0,'#56627a'),(1,'#2f3742')])+rg('lampg',[(0,'#fee761',.9),(.4,'#fee761',.3),(1,'#fee761',0)])
    back=''
    for x,y,s in ((60,90,1.3),(250,50,1),(310,170,.8),(120,240,.9)):
        back+=f'<g fill="{c["smoke"]}" opacity=".22" transform="translate({x},{y}) scale({s})"><ellipse rx="44" ry="12"/><ellipse cx="-16" cy="-9" rx="20" ry="13"/><ellipse cx="14" cy="-12" rx="24" ry="15"/></g>'
    mid=''
    # خط آسمان دور
    x=-10
    while x<370:
        w=R.randint(22,40); h=R.randint(40,90); mid+=rect(x,150-h,w,h+10,c['haze'],0,.7); x+=w+R.randint(0,4)
    # ساختمان‌ها + دودکش
    x=-6
    while x<366:
        w=R.randint(34,58); h=R.randint(70,126); mid+=rect(x,160-h,w,h+10,'url(#bl)')
        for ry in range(int(160-h+10),150,16):
            for rx in range(int(x+6),int(x+w-8),12):
                if R.random()<.35: mid+=rect(rx,ry,5,7,c['window'],1,.85)
        x+=w+R.randint(2,8)
    for cx in (52,296):
        mid+=rect(cx-9,24,18,120,c['brick'])+rect(cx-12,20,24,8,'#6b3e3e')
        for i,(dx,dy,r) in enumerate(((0,-6,10),(8,-22,14),(18,-42,18))): mid+=circ(cx+dx,20+dy,r,c['smoke'],.35-.08*i)
    # ریسمان پرچم بین دودکش‌ها
    mid+=path('M52,34 Q174,96 296,34',st='#1e1d39',sw=1.6,op=.8)
    for i in range(1,12):
        t=i/12; x=52+244*t; y=34+ (1-(2*t-1)**2)*31+2
        mid+=poly([(x-6,y),(x+6,y),(x,y+13)],['#df84a5','#fee761','#73bed3'][i%3],.95)
    mid+=rect(-10,158,380,400,'url(#st)')
    mid+=rect(-10,158,380,3,'#8b93af',op=.4)
    mid+=ell(180,160,250,26,c['sky3'],.35)
    # لوله
    mid+=rect(-10,300,380,16,c['pipe'])+rect(-10,303,380,3,c['pipe_hi'],0,.7)
    for x in (70,210,320): mid+=rect(x-5,296,10,24,c['brass_s'])
    # سنگ‌فرش
    for j in range(7):
        y=340+j*24
        mid+=path(f'M-10,{y} L370,{y}',st=c['street_l'],sw=1.5,op=.28)
        for i in range(10): mid+=path(f'M{(i*44+(j%2)*22):.0f},{y} v24',st=c['street_l'],sw=1.5,op=.2)
    for x in (112,248):
        mid+=rect(x-2,218,4,100,'#202e37')+circ(x,214,30,'url(#lampg)')+circ(x,214,5,c['window'])
    mid+=gear(300,420,46,12,c['brass'],op=.55)+gear(40,470,34,10,c['brass_s'],op=.5)
    mid+=rect(0,380,360,140,'#10141f',op=.22)
    front=gear(12,200,40,10,c['brass'],op=.95)+gear(350,206,34,9,c['brass_s'],op=.95)+rect(250,190,24,24,'#6b4a2a',3,.9)
    write('city',back,mid,front,defs_m=defs)
if __name__=='__main__': stadium();space();farm();city();print('lands ok')
