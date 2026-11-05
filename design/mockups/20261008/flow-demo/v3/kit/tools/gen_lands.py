# gen_lands.py (نسخهٔ ۲): چهار زمین، هر کدام سه لایه (back/mid/front) بر پایهٔ palettes.py
# اصل شکل–زمینه: پس‌زمینه روشنایی میانی و کم‌اشباع؛ جزئیات تزئینی کم‌نور و دور از ستون‌های مسیر
# (ستون راست x≈248 و چپ x≈98 در بوم ۳۶۰). هیچ متنی در گرافیک نیست.
from kitlib import *
from palettes import PAL
W,H=360,720
_id=[0]
def uid(p='g'):
    _id[0]+=1; return f'{p}{_id[0]}'
def lg(stops,x2=0,y2=1):
    i=uid('l')
    return i,f'<linearGradient id="{i}" x1="0" y1="0" x2="{x2}" y2="{y2}">'+''.join(f'<stop offset="{o}" stop-color="{c}"'+(f' stop-opacity="{a}"' if a is not None else '')+'/>' for o,c,*r in stops for a in [r[0] if r else None])+'</linearGradient>'
def rg(col,a=.6):
    i=uid('r'); return i,f'<radialGradient id="{i}"><stop offset="0" stop-color="{col}" stop-opacity="{a}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>'
def glow(defs,cx,cy,r,col,a=.6):
    i,d=rg(col,a); defs.append(d); return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{i})"/>'
def vgrad(defs,stops):
    i,d=lg(stops); defs.append(d); return f'url(#{i})'
BLUR='<filter id="bl6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter><filter id="bl14" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter><filter id="bl3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>'
def ridge(y,amp,seed,fill,n=7,ex=''):
    return hills(W,y,amp,seed,fill,ln=None,bottom=H+20,n=n,ex=ex)
def cloud(cx,cy,s,col,a):
    return f'<g fill="{col}" opacity="{a}" transform="translate({cx},{cy}) scale({s})"><ellipse rx="40" ry="10"/><ellipse cx="-16" cy="-8" rx="18" ry="11"/><ellipse cx="10" cy="-11" rx="22" ry="14"/></g>'
def rim(path_d,col,a=.35,w=2):
    return f'<path d="{path_d}" fill="none" stroke="{col}" stroke-opacity="{a}" stroke-width="{w}"/>'
def write_land(key, defs, back, mid, front):
    dd=''.join(defs) if isinstance(defs,list) else defs
    for part,body in (('back',back),('mid',mid),('front',front)):
        svg(f'land-{key}-{part}.svg',W,H,body,dd+BLUR)
    svg(f'land-{key}.svg',W,H,f'<g id="back">{back}</g><g id="mid">{mid}</g><g id="front">{front}</g>',dd+BLUR)

# ===================== ورزشگاه =====================
def stadium():
    P=PAL['stadium'];R=random.Random(7);D=[]
    sky=vgrad(D,[(0,P['sky0']),(.34,P['sky1']),(.58,P['sky2']),(1,P['sky2'])])
    back=f'<rect width="{W}" height="{H}" fill="{sky}"/>'
    back+=glow(D,330,190,210,P['glow'],.42)+glow(D,330,190,80,P['glow'],.3)
    back+=cloud(70,120,1.3,'#e2909a',.22)+cloud(240,80,1.0,'#e2909a',.18)+cloud(330,170,.8,'#f0a874',.2)
    # تپه‌های دور (مهآلود، کم‌اشباع)
    back+=ridge(262,10,3,P['far'],ex='opacity=".85"')
    # چراغ‌های ورزشگاه (فقط حاشیه)
    for x in (18,342):
        back+=f'<rect x="{x-3}" y="170" width="6" height="110" fill="#4a2a44"/><rect x="{x-17}" y="150" width="34" height="24" rx="4" fill="#5e3a58"/>'
        back+=''.join(f'<circle cx="{x-10+j*10}" cy="{157+i*10}" r="3.2" fill="#ffd9a0" opacity=".9"/>' for i in range(2) for j in range(3))+glow(D,x,162,46,P['glow'],.5)
    # سکوی تماشاگران: دیوار + ردیف تماشاگر کم‌نور
    back+=f'<path d="M0,300 V252 Q180,228 360,252 V300Z" fill="{P["stand"]}"/>'
    back+=f'<path d="M0,252 Q180,228 360,252" fill="none" stroke="#c9849a" stroke-opacity=".35" stroke-width="3"/>'
    cols=['#b5566e','#d79a62','#6a6aa8','#4aa6a0','#c9a24a']
    for row in range(4):
        for k in range(36):
            x=5+k*10+R.uniform(-1.2,1.2); y=262+row*10+ ((x-180)**2)/9000*-1*-1 - 14*(1-((x-180)/180)**2)*0 +R.uniform(-1,1)
            back+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.8" fill="{cols[R.randrange(5)]}" opacity=".5"/>'
    back+=f'<path d="M0,300 H360" stroke="#2a1420" stroke-opacity=".45" stroke-width="3"/>'
    # پرچم‌های ریسه‌ای بالا (کم‌نور)
    back+=f'<path d="M0,232 Q180,196 360,232" fill="none" stroke="#3a1c30" stroke-opacity=".5" stroke-width="1.6"/>'
    for i in range(12):
        t=(i+.5)/12;x=t*360;y=232-(1-(2*t-1)**2)*36
        back+=f'<path d="M{x:.0f},{y:.0f} l8,0 l-4,11Z" fill="{cols[i%5]}" opacity=".55"/>'
    # زمین چمن
    mid=f'<path d="M0,300 H360 V{H} H0Z" fill="{vgrad(D,[(0,P["pitch0"]),(.55,P["pitch1"]),(1,"#35603a")])}"/>'
    mid+='<g opacity=".07">'+''.join(f'<rect x="{i*60}" y="300" width="30" height="{H}" fill="#fff"/>' for i in range(6))+'</g>'
    mid+='<g opacity=".06">'+''.join(f'<rect x="{i*60+30}" y="300" width="30" height="{H}" fill="#000"/>' for i in range(6))+'</g>'
    mid+=glow(D,330,330,170,P['glow'],.12)
    # خطوط زمین بسیار کم‌نور
    mid+=f'<g fill="none" stroke="#e8f2d0" stroke-opacity=".13" stroke-width="3"><ellipse cx="180" cy="470" rx="120" ry="52"/><path d="M-10,470 H370"/><rect x="40" y="320" width="280" height="70" rx="4" transform="skewX(0)"/></g>'
    # دروازهٔ دور: جیب راست (x≈262..340 داخلی) که از مسیر آزاد است
    mid+=f'<g transform="translate(284,326)" fill="none" stroke="#f0d8b8" stroke-opacity=".45" stroke-width="3.5" stroke-linecap="round"><path d="M0,34 V0 H52 V34"/><path d="M8,4 V32 M17,4 V32 M26,4 V32 M35,4 V32 M44,4 V32" stroke-width=".8" opacity=".6"/></g>'
    # مسیر دویدن
    mid+=f'<path d="M-20,650 Q180,600 380,650 V{H} H-20Z" fill="{P["track"]}" opacity=".9"/><path d="M-20,650 Q180,600 380,650" fill="none" stroke="#e8b28a" stroke-opacity=".16" stroke-width="3"/>'
    mid+=f'<path d="M-20,676 Q180,626 380,676" fill="none" stroke="#e8b28a" stroke-opacity=".12" stroke-width="2"/>'
    front=f'<path d="M-4,{H} V610 Q50,598 78,{H}Z" fill="{P["front"]}" opacity=".9"/><path d="M364,{H} V620 Q320,606 294,{H}Z" fill="{P["front"]}" opacity=".9"/>'
    front+=f'<circle cx="30" cy="680" r="12" fill="#d8b896" opacity=".7"/><path d="M30,672 l5,3 -2,6 h-6 l-2,-6Z" fill="#4a2a20" opacity=".6"/>'
    write_land('stadium',D,back,mid,front)

# ===================== پایگاه فضایی =====================
def space():
    P=PAL['space'];R=random.Random(11);D=[]
    sky=vgrad(D,[(0,P['sky0']),(.45,P['sky1']),(.8,P['sky2']),(1,'#5a2f7e')])
    back=f'<rect width="{W}" height="{H}" fill="{sky}"/>'
    # سحابی‌های رنگی نرم
    for cx,cy,rx,ry,c,a in ((70,120,150,90,'#1f8a9a',.28),(300,210,130,100,'#c0448a',.28),(150,330,170,80,'#6a3ab8',.3),(300,420,150,90,'#1f8a9a',.2)):
        back+=f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}" opacity="{a}" filter="url(#bl14)"/>'
    for i in range(90):
        x,y=R.uniform(0,W),R.uniform(0,420);r=R.choice((.7,.9,1.1,1.5))
        back+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff0d0" opacity="{R.uniform(.35,.9):.2f}"/>'
    for i in range(6): back+=star4(R.uniform(20,340),R.uniform(15,300),R.choice((4,5,6)),'#fff0d0').replace('/>',' opacity=".7"/>')
    # سیارهٔ حلقه‌دار، کم‌نور و دور از مسیر (چپ-بالا زیر لوحه)
    back+=f'<g transform="rotate(-18 82 168)" opacity=".92"><ellipse cx="82" cy="168" rx="62" ry="13" fill="none" stroke="#b86a9a" stroke-width="7" opacity=".6"/><circle cx="82" cy="168" r="34" fill="{vgrad(D,[(0,"#a8587e"),(1,"#4a2a62")])}"/><path d="M52,160 q30,-10 60,0" stroke="#6a3a7a" stroke-width="5" fill="none" opacity=".5"/><path d="M20,170 q60,24 124,-4" fill="none" stroke="#b86a9a" stroke-width="7" opacity=".6"/></g>'
    # زمین دور (کم‌اشباع): کرهٔ آبی کوچک راست
    back+=f'<circle cx="318" cy="300" r="20" fill="{vgrad(D,[(0,"#4a86b8"),(1,"#1c3a78")])}" opacity=".85"/>'
    mid=ridge(372,16,11,'#4d3380',n=6)
    mid+=rim('M-10,372 C60,356 120,386 180,370 S300,360 370,372','#b08ae0',.35,2)
    for x,y,rx in ((300,420,30),(60,470,24),(220,500,34),(330,520,18),(140,560,22)):
        mid+=f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*.3:.0f}" fill="#2c1a58" opacity=".6"/><path d="M{x-rx},{y} a{rx},{rx*.3:.0f} 0 0 1 {2*rx},0" fill="none" stroke="#a88ae0" stroke-width="2.2" opacity=".3"/>'
    # گنبد پایگاه (چپ، دور از ستون‌ها)
    mid+=f'<g transform="translate(14,480)"><rect x="0" y="30" width="80" height="22" rx="4" fill="#5e4c92"/><path d="M8,30 a32,32 0 0 1 64,0Z" fill="{vgrad(D,[(0,"#8c7cc4"),(1,"#4e3e86")])}"/>'
    mid+=''.join(f'<rect x="{x}" y="36" width="8" height="8" rx="2" fill="#e8b45e" opacity=".6"/>' for x in (10,28,44,60))
    mid+=f'<path d="M20,18 q6,-12 18,-14" stroke="#e0d0ff" stroke-opacity=".35" stroke-width="3" fill="none"/></g>'
    front=ridge(612,12,5,'#2c1850',n=5)+rim('M-10,612 C80,600 150,626 230,610 S330,604 370,612','#8a6ad0',.3,2)
    front+=f'<g transform="translate(276,636)"><circle cx="20" cy="30" r="12" fill="#2c2a4a"/><circle cx="20" cy="30" r="4" fill="#7a74a8"/><circle cx="60" cy="30" r="12" fill="#2c2a4a"/><circle cx="60" cy="30" r="4" fill="#7a74a8"/><rect x="8" y="10" width="64" height="16" rx="5" fill="#5c5496"/></g>'
    write_land('space',D,back,mid,front)

# ===================== مزرعه و آسیاب =====================
def farm():
    P=PAL['farm'];R=random.Random(21);D=[]
    sky=vgrad(D,[(0,P['sky0']),(.3,P['sky1']),(.55,P['sky2']),(1,P['sky2'])])
    back=f'<rect width="{W}" height="{H}" fill="{sky}"/>'
    back+=glow(D,95,225,230,P['glow'],.5)+glow(D,95,225,80,P['glow'],.35)
    for cx,cy,s,c,a in ((280,70,1.2,'#d98a9a',.25),(120,60,.9,'#d98a9a',.2),(320,190,.8,'#ffc490',.22)): back+=cloud(cx,cy,s,c,a)
    # پرتوهای خورشید کم‌نور
    import math
    back+=''.join(f'<path d="M95,225 L{95+360*math.cos(a):.0f},{225+360*math.sin(a):.0f}" stroke="#ffd09a" stroke-width="10" opacity=".07" stroke-linecap="round"/>' for a in [-math.pi*i/12 for i in range(1,12)])
    back+=ridge(268,14,21,'#7b6585',n=6)+ridge(300,12,22,'#8a6a70',n=6)
    mid=ridge(336,10,23,'#6e7240',n=6)
    mid+=rim('M-10,336 C60,326 120,344 180,334 S300,330 370,338','#d6c27a',.28,2)
    # آسیاب بادی: جیب بالا-چپ (زیر لوحه، دور از مسیر)
    mid+=f'<g transform="translate(95,196)"><path d="M-22,94 L-14,22 L14,22 L22,94Z" fill="#9a6a62"/><path d="M-14,22 L0,6 L14,22Z" fill="#5e2e4a"/><rect x="-4" y="60" width="9" height="34" rx="2" fill="#4a2438"/>'
    for k in range(4):
        a=k*90+16
        mid+=f'<g transform="rotate({a} 0 22)"><rect x="-2.5" y="-46" width="5" height="68" fill="#6a4a3a"/><rect x="2.5" y="-42" width="15" height="30" fill="#c8a48a" opacity=".6"/></g>'
    mid+=f'<circle cx="0" cy="22" r="5" fill="#c8a24a"/></g>'
    # خانهٔ کوچک: جیب راست (بین ردیف‌های گره)
    mid+=f'<g transform="translate(284,360)"><rect x="0" y="20" width="54" height="36" fill="#9a6a62"/><path d="M-6,22 L27,-4 L60,22Z" fill="#5e2e4a"/><rect x="21" y="34" width="13" height="22" fill="#4a2438"/><rect x="40" y="-2" width="7" height="14" fill="#7a4642"/></g>'
    # جویبار فیروزه‌ای
    mid+=f'<path d="M-10,470 Q80,440 150,478 T370,462 V500 Q250,504 150,508 Q70,476 -10,502Z" fill="#2f8088"/><path d="M20,484 q20,-6 40,0 M200,484 q20,-6 40,0" stroke="#b6eaea" stroke-width="2.2" fill="none" opacity=".35" stroke-linecap="round"/>'
    # مزرعه‌های ردیفی کم‌نور پایین
    mid+=f'<path d="M-10,540 Q180,512 370,540 V{H} H-10Z" fill="#66763a"/>'
    for i in range(9): mid+=f'<path d="M-10,{556+i*18} Q180,{528+i*18} 370,{556+i*18}" fill="none" stroke="#4e5e2c" stroke-opacity=".5" stroke-width="5"/>'
    front=f'<path d="M-4,{H} V640 Q60,626 96,{H}Z" fill="#4a5a28"/><path d="M364,{H} V650 Q310,634 280,{H}Z" fill="#4a5a28"/>'
    for i in range(7):
        x=R.uniform(4,70);y=700
        front+=f'<path d="M{x:.0f},{y} q{R.uniform(-3,3):.0f},-14 0,-28" stroke="#c8a850" stroke-width="2" fill="none" opacity=".7"/><ellipse cx="{x:.0f}" cy="{y-30}" rx="2.6" ry="6" fill="#d8b860" opacity=".7"/>'
    write_land('farm',D,back,mid,front)

# ===================== شهر ماشین‌ها =====================
def city():
    P=PAL['city'];R=random.Random(33);D=[]
    sky=vgrad(D,[(0,P['sky0']),(.36,P['sky1']),(.6,P['sky2']),(1,P['sky2'])])
    back=f'<rect width="{W}" height="{H}" fill="{sky}"/>'
    back+=glow(D,200,290,240,P['glow'],.42)+glow(D,200,290,80,P['glow'],.3)
    back+=cloud(80,90,1.2,'#7ab0b8',.22)+cloud(300,60,.9,'#7ab0b8',.2)
    # خط افق دور
    sk=''
    x=0
    while x<W:
        w=R.randrange(24,48);h=R.randrange(50,130)
        sk+=f'<rect x="{x}" y="{300-h}" width="{w}" height="{h+60}" fill="{P["far"]}"/>';x+=w+R.randrange(0,5)
    back+=f'<g opacity=".9">{sk}</g>'
    back+=gear(60,200,36,10,'#4a7a88',hole=.3)+gear(318,236,26,9,'#4a7a88',hole=.3)
    # ساختمان‌های میانی آجری-بنفش
    mid=''
    for x,w,h,c in ((6,52,150,'#6e4250'),(66,40,110,'#5c4458'),(238,44,130,'#6e4250'),(292,60,160,'#5c4458')):
        mid+=f'<rect x="{x}" y="{330-h}" width="{w}" height="{h+30}" fill="{c}"/><rect x="{x}" y="{330-h}" width="{w}" height="4" fill="#a8707a" opacity=".35"/>'
        for yy in range(int(330-h+14),322,22):
            for xx in range(x+8,x+w-10,16):
                if R.random()<.5: mid+=f'<rect x="{xx}" y="{yy}" width="8" height="10" rx="1.5" fill="#e8b45e" opacity=".55"/>'
    # دودکش‌ها + دود نرم
    for x in (128,206):
        mid+=f'<rect x="{x}" y="226" width="20" height="104" fill="#7a4642"/><rect x="{x-3}" y="222" width="26" height="8" fill="#8a524a"/>'
        mid+=f'<g fill="#9ac0c6" opacity=".25" filter="url(#bl6)"><circle cx="{x+12}" cy="204" r="12"/><circle cx="{x+22}" cy="186" r="15"/><circle cx="{x+10}" cy="164" r="18"/></g>'
    mid+=f'<rect x="0" y="330" width="{W}" height="{H}" fill="{vgrad(D,[(0,"#4a5c60"),(.4,"#3c5c66"),(1,"#2a3f58")])}"/>'
    for yy in range(372,700,26):
        for xx in range(-20,380,48): mid+=f'<rect x="{xx+(yy%48)}" y="{yy}" width="44" height="21" rx="6" fill="#4a6c76" opacity=".35"/>'
    mid+=f'<rect x="0" y="342" width="{W}" height="8" fill="#5a4a46"/>'+''.join(f'<rect x="{i*18}" y="350" width="9" height="5" fill="#3a2e2c"/>' for i in range(21))
    mid+=glow(D,200,350,200,P['glow'],.14)
    # فانوس‌های خیابان: لکه‌های نور گرم در حاشیه‌ها (جیب‌های چپ/راست، دور از ستون مسیر)
    for x,y in ((16,420),(340,470),(20,600)):
        mid+=glow(D,x,y,70,P['glow'],.32)+f'<rect x="{x-2}" y="{y-6}" width="4" height="64" fill="#1f343c"/><circle cx="{x}" cy="{y-8}" r="6" fill="#ffd9a0" opacity=".85"/>'
    # لوله‌های بزرگ و بخار در جیب چپ-پایین
    mid+=f'<rect x="0" y="520" width="70" height="14" rx="7" fill="#3a5a64"/><rect x="62" y="514" width="12" height="26" rx="4" fill="#4a6c76"/>'
    front=f'<path d="M-4,{H} V620 Q60,606 96,{H}Z" fill="#243c46"/><path d="M364,{H} V630 Q300,612 270,{H}Z" fill="#243c46"/>'
    front+=gear(34,690,34,10,'#8a6a3a',hole=.3)+gear(92,716,20,9,'#7a5c34',hole=.3)+gear(334,694,30,10,'#8a6a3a',hole=.3)
    write_land('city',D,back,mid,front)

stadium();space();farm();city()
print('lands ok')
