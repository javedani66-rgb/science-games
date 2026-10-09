# gen_phone.py: kit/phone.html؛ ۴ صفحهٔ نقشه ۳۹۰×۸۰۰ (هر زمین یکی) + ۲ صفحهٔ «اتصال» (دروازه–گپ–دروازه).
# متن‌های نمونه فقط برای دیدن کیت‌اند (نه متن نهایی).
import os
from mappath import *
OUT=os.path.join(os.path.dirname(__file__),'..','phone.html')
H=640; YS=[184,292,400,508]; BORDER=6; GAP=64
LAND_HEAD_SYM={'stadium':'force','space':'energy','farm':'wheel','city':'machine'}
PAGES={
 'stadium':dict(plate='ورزشگاه',first=True,last=False,nodes=[('force','done','هل دادن'),('friction','done','لغزیدن'),('multi','open','کشیدن با هم'),('weight','locked','ترازوی بزرگ')],lock='اول: کشیدن با هم'),
 'space':dict(plate='پایگاه فضایی',first=False,last=False,nodes=[('energy','done','پنل خورشیدی'),('machine','open','کارگاه ماشین'),('lever','locked','اهرم فضایی'),('slope','trial','سطح شیب‌دار')],lock='اول: کارگاه ماشین'),
 'farm':dict(plate='مزرعه و آسیاب',first=False,last=False,nodes=[('wheel','done','آسیاب آبی'),('summary','done','جمع‌بندی'),('energy','trial','بادآسیاب'),('lever','locked','الاکلنگ')],lock='اول: بادآسیاب'),
 'city':dict(plate='شهر ماشین‌ها',first=False,last=True,nodes=[('slope','done','رمپ بار'),('wheel','done','چرخ دنده'),('summary','open','جمع‌بندی'),('machine','trial','ماشین بزرگ')],lock=''),
}
def reached(s): return s in ('done','open')
def landbox(k,ext=44,style='',states=None,entry_done=None):
    P=PAGES[k]; nodes=[(a,(states[i] if states else b),c) for i,(a,b,c) in enumerate(PAGES[k]['nodes'])]; pts=[(col_x(i),YS[i]) for i in range(len(nodes))]
    st=[n[1] for n in nodes]
    pd='';pt='';foot='';barrier=''
    def add(d,done):
        nonlocal pd,pt
        if done: pd+=f'<path class="path-done" d="{d}"/><path class="path-done--top" d="{d}"/>'
        else: pt+=f'<path class="path-todo--shade" d="{d}"/><path class="path-todo" d="{d}"/>'
    if P['first']: add(seg((COL_R,112),pts[0]),reached(st[0]))
    else: add(seg((COL_R,30),pts[0]),reached(st[0]) if entry_done is None else entry_done)
    for i in range(len(nodes)-1):
        done=reached(st[i]) and reached(st[i+1]); add(seg(pts[i],pts[i+1]),done)
        if done:
            for x,y,an in footprints(pts[i],pts[i+1]):
                foot+=f'<i class="foot" style="left:{x:.1f}px;top:{y:.1f}px;transform:translate(-50%,-50%) rotate({an:.0f}deg)"></i>'
        if st[i+1]=='locked':
            barrier+=f'<i class="barrier" style="left:{pts[i+1][0]}px;top:{pts[i+1][1]-66}px"></i>'
    marks='';last=pts[-1]
    if P['last']:   # پایان: همان قوس خروجی، ولی به پرچم پایان روی خود مسیر
        fx,fy=COL_R,596
        add(seg(last,(fx,fy)),reached(st[-1]))
        marks+=f'<i class="mark mark--end" style="left:{fx}px;top:{fy}px"></i><span class="chip chip--label mark__chip" style="left:{fx}px;top:{fy+26}px;transform:translate(-50%,-50%)">پایان</span>'
    else:
        add(seg(last,(COL_R,H-30)) if last[0]!=COL_R else f'M{last[0]} {last[1]}L{COL_R} {H-30}',reached(st[-1]))
    if P['first']:
        marks+=f'<i class="mark mark--start" style="left:{COL_R}px;top:112px"></i><span class="chip chip--label mark__chip" style="left:{COL_R-38}px;top:92px">شروع</span>'
    nh=''
    for i,(sym,s,label) in enumerate(nodes):
        x,y=pts[i]; here=(s=='open')
        chips=f'<span class="chip chip--label">{label}</span>'
        if here: chips+='<span class="chip chip--here"><i class="ic"></i>تو اینجایی</span>'
        if s=='locked': chips+=f'<span class="chip chip--lock"><i class="ic"></i>{P["lock"]}</span>'
        if s=='trial': chips+='<span class="chip chip--trial"><i class="ic"></i>آزمایشی</span>'
        nh+=(f'<button class="node" data-state="{s}" style="left:{x}px;top:{y}px" aria-label="{label}">'+('<i class="node__ring"></i>' if here else '')+
             f'<span class="node__disc"><i class="node__glyph" data-sym="{sym}"></i></span><span class="node__labels">{chips}</span></button>')
        if here: nh+=f'<i class="guide" data-state="thinking" style="left:{x}px;top:{y}px;margin-top:-34px"></i>'
    # مسیر روی لبهٔ قاب (روی دروازه): ۳۰px داخل + گپ. مختصات بیرونی (+6)؛ svg با top:-ext
    X=COL_R+BORDER; OUTH=H+2*BORDER
    def tr(d,done): return (f'<path class="path-done" d="{d}"/><path class="path-done--top" d="{d}"/>' if done else f'<path class="path-todo--shade" d="{d}"/><path class="path-todo" d="{d}"/>')
    trail=''
    if not P['first']: trail+=tr(f'M{X} 0L{X} {BORDER+30+ext}',reached(st[0]) if entry_done is None else entry_done)
    if not P['last']:  trail+=tr(f'M{X} {BORDER+H-30+ext}L{X} {OUTH+2*ext}',reached(st[-1]))
    gates=('' if P['first'] else '<i class="gate gate--in"></i>')+('' if P['last'] else '<i class="gate gate--out"></i>')
    svg_in=f'<svg class="land__path" viewBox="0 0 346 {H}" width="346" height="{H}" aria-hidden="true">{pt}{pd}</svg>'
    svg_tr=f'<svg class="trail" style="top:-{ext}px" width="358" height="{OUTH+2*ext}" viewBox="0 0 358 {OUTH+2*ext}" aria-hidden="true">{trail}</svg>'
    head=f'<div class="land__head"><i class="sym land__sym" data-sym="{LAND_HEAD_SYM[k]}"></i><div class="plate">{P["plate"]}</div></div>'
    land=(f'<div class="land" data-land="{k}" style="height:{OUTH}px"><div class="land__layer land__layer--back"></div><div class="land__layer land__layer--mid"></div><div class="land__layer land__layer--front"></div>{head}{svg_in}{foot}{barrier}{marks}{nh}</div>')
    return f'<div class="landbox" data-land="{k}" style="margin-bottom:0;{style}">{land}{gates}{svg_tr}</div>'
TOP='<div class="topbar"><button class="btn btn--icon" aria-label="منو"><i class="ic ic-menu"></i></button><span class="t-title">نقشهٔ علوم</span><span class="spacer"></span></div>'
def screen(id,inner,pad=44): return f'<div class="screen" id="{id}">{TOP}<div class="map" style="height:736px;overflow:hidden;padding-top:{pad}px">{inner}</div></div>'
OUTH=H+12
def join(a,b,id,sa=None,sb=None,done=False):   # پایین a + بالای b با گپ ۶۴؛ مسیر دقیقاً در وسط گپ به هم می‌رسد
    bottom=340
    return screen(id,landbox(a,32,f'position:absolute;left:16px;top:{bottom-OUTH}px',sa)+landbox(b,32,f'position:absolute;left:16px;top:{bottom+GAP}px',sb,entry_done=done),0)
html=('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>نقشه: ۴ زمین ۳۹۰×۸۰۰</title><link rel="stylesheet" href="kit.css">'
 '<style>body.kit{background:#0f2e2c}.row4{display:flex;flex-wrap:wrap;gap:0;justify-content:center}.row4 .screen{flex:none}</style></head><body class="kit"><div class="row4">'
 +''.join(screen('m-'+k,landbox(k)) for k in PAGES)+join('stadium','space','j-stadium-space')+join('farm','city','j-farm-city',['done']*4,['done','done','open','trial'],True)+'</div><script src="kit.js"></script></body></html>')
open(OUT,'w').write(html); print('phone ok',len(html))
