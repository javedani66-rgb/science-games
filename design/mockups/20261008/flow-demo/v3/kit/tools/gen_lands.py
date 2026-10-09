from kitlib import *
W,H=360,600
R=random.Random(7)

def write_land(key, defs, back, mid, front):
    for part,body in (('back',back),('mid',mid),('front',front)):
        svg(f'land-{key}-{part}.svg',W,H,body,defs)
    svg(f'land-{key}.svg',W,H,f'<g id="back">{back}</g><g id="mid">{mid}</g><g id="front">{front}</g>',defs)

# ---------- 1. stadium ----------
defs=f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4c978"/><stop offset=".55" stop-color="#fbe6b4"/><stop offset="1" stop-color="#fff3d6"/></linearGradient>
<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff6cf"/><stop offset=".5" stop-color="#ffe08a" stop-opacity=".8"/><stop offset="1" stop-color="#ffe08a" stop-opacity="0"/></radialGradient>
<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b7cf8e"/><stop offset="1" stop-color="#8fb27a"/></linearGradient>
<linearGradient id="trk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d08a5a"/><stop offset="1" stop-color="#b3683f"/></linearGradient>{WOBBLE}'''
back=f'<rect width="{W}" height="{H}" fill="url(#sky)"/><circle cx="270" cy="70" r="90" fill="url(#sun)"/>'
# clouds
for cx,cy,s in ((60,60,1),(200,110,.8),(310,40,.6)):
    back+=f'<g fill="#fffaf0" opacity=".85" transform="translate({cx},{cy}) scale({s})"><ellipse cx="0" cy="0" rx="34" ry="11"/><ellipse cx="-14" cy="-8" rx="16" ry="12"/><ellipse cx="10" cy="-11" rx="20" ry="14"/></g>'
# far grandstand with crowd dots
stand='<g filter="url(#wob)">'
stand+=f'<path d="M0,215 L0,150 Q180,110 360,150 L360,215Z" fill="#c9733e" stroke="{LINE}" stroke-width="2.5" stroke-opacity=".6"/>'
for i,c in enumerate(('#e8a85a','#d9944c','#c9733e')):
    stand+=f'<path d="M0,{175+i*14} Q180,{138+i*14} 360,{175+i*14} L360,{190+i*14} Q180,{153+i*14} 0,{190+i*14}Z" fill="{c}" opacity=".9"/>'
cols=['#184441','#fff0c9','#8a5bc7','#3f7fd0','#efbd1f','#e0699c']
for row in range(3):
    for k in range(34):
        x=8+k*10.3+R.uniform(-1,1); yb=170+row*14-(abs(x-180)**2)/1500*-1
        y=148+row*14+ (x-180)**2/ (1500) *0.9+R.uniform(-1,1)
        stand+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="{cols[R.randrange(6)]}"/>'
stand+='</g>'
back+=stand
# flag string
back+=f'<path d="M0,140 Q180,95 360,140" fill="none" stroke="{LINE}" stroke-opacity=".5" stroke-width="1.5"/>'
for i in range(14):
    t=(i+.5)/14; x=t*360; y=140-4*0 -( (0.5-abs(t-.5))*2 )*45*0.9*1 + 0
    y=140-(1-(2*t-1)**2)*45*.98*0.5*2*0.5+0
    back+=f'<path d="M{x:.1f},{y:.1f} l7,0 l-3.5,10Z" fill="{cols[i%6]}"/>'
mid=hills(W,235,10,3,'url(#grass)',ln=None,n=5)
# mown stripes
mid+='<g opacity=".18">'+''.join(f'<rect x="{i*60}" y="225" width="30" height="400" fill="#fff"/>' for i in range(6))+'</g>'
# running track curve and field lines
mid+=f'<path d="M-20,330 Q180,262 380,330 L380,372 Q180,300 -20,372Z" fill="url(#trk)" stroke="{LINE}" stroke-opacity=".35" stroke-width="2"/>'
for k in (0,1):
    mid+=f'<path d="M-20,{342+k*10} Q180,{274+k*10} 380,{342+k*10}" fill="none" stroke="#fff0c9" stroke-width="1.6" opacity=".7" stroke-dasharray="1 0"/>'
# goal posts (far)
mid+=f'<g transform="translate(62,238)" fill="none" stroke="#fff8e8" stroke-width="4" stroke-linecap="round"><path d="M0,40 V0 H44 V40"/><path d="M6,4 L6,38 M14,4 V38 M22,4 V38 M30,4 V38 M38,4 V38" stroke-width=".8" opacity=".6"/></g>'
mid+=f'<circle cx="296" cy="262" r="2" fill="none"/>'
# center circle
mid+=f'<ellipse cx="260" cy="470" rx="70" ry="22" fill="none" stroke="#fff0c9" stroke-width="3" opacity=".65"/><path d="M-20,540 Q180,500 380,540" fill="none" stroke="#fff0c9" stroke-width="3" opacity=".55"/>'
front=''
# bottom bleachers wood steps left/right + cones + ball + rope
front+=f'<path d="M0,520 L0,600 L60,600 L40,540 Z" fill="#a8672f" stroke="{LINE}" stroke-width="2.5" stroke-opacity=".7"/><path d="M360,505 L360,600 L292,600 L318,530Z" fill="#a8672f" stroke="{LINE}" stroke-width="2.5" stroke-opacity=".7"/>'
for yy in (545,568,590): front+=f'<path d="M0,{yy} L{40-(yy-540)*0.0+10},{yy}" stroke="#e8b878" stroke-width="3"/>'
for x,y in ((88,560),(262,580)):
    front+=f'<path d="M{x-11},{y+12} L{x-6},{y-14} L{x+6},{y-14} L{x+11},{y+12}Z" fill="#fb9b3a" stroke="{LINE}" stroke-width="2"/><rect x="{x-5.5}" y="{y-6}" width="11" height="4" fill="#fff0c9"/><ellipse cx="{x}" cy="{y+13}" rx="14" ry="3.5" fill="{LINE}" opacity=".35"/>'
front+=f'<circle cx="150" cy="578" r="13" fill="#fff8e8" stroke="{LINE}" stroke-width="2.2"/><path d="M150,570 l6,4 -2,7 h-8 l-2,-7Z" fill="{LINE}"/><ellipse cx="150" cy="592" rx="14" ry="3" fill="{LINE}" opacity=".3"/>'
front+=f'<rect x="0" y="0" width="{W}" height="{H}" fill="none"/>'
write_land('stadium',defs,back,mid,front)

# ---------- 2. space base ----------
defs=f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b1442"/><stop offset=".6" stop-color="#34307a"/><stop offset="1" stop-color="#5b4a96"/></linearGradient>
<radialGradient id="pl" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffd7a8"/><stop offset="1" stop-color="#c96a8e"/></radialGradient>
<radialGradient id="ea" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#9ee0ff"/><stop offset="1" stop-color="#2a6fb5"/></radialGradient>
<linearGradient id="moon" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a08ccf"/><stop offset=".45" stop-color="#7a66ab"/><stop offset="1" stop-color="#43347a"/></linearGradient>
<linearGradient id="dome" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f1ecfa"/><stop offset="1" stop-color="#9d92c4"/></linearGradient>{WOBBLE}'''
back=f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
for i in range(70):
    x,y=R.uniform(0,W),R.uniform(0,300); r=R.choice((.8,1,1.3,1.8))
    back+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff6d8" opacity="{R.uniform(.5,1):.2f}"/>'
for i in range(5): back+=star4(R.uniform(20,340),R.uniform(15,260),R.choice((5,7,9)),'#fff6d8')
back+=f'<g transform="rotate(-18 90 90)"><ellipse cx="90" cy="90" rx="62" ry="13" fill="none" stroke="#f0b9d0" stroke-width="7" opacity=".7"/><circle cx="90" cy="90" r="34" fill="url(#pl)" stroke="{LINE}" stroke-opacity=".5" stroke-width="2.5"/><path d="M56,90 a62,13 0 0 0 68,12" fill="none" stroke="#f0b9d0" stroke-width="7" opacity=".9"/></g>'
back+=f'<circle cx="290" cy="150" r="22" fill="url(#ea)" stroke="{LINE}" stroke-opacity=".5" stroke-width="2"/><path d="M276,146 q8,-8 14,0 q4,6 -4,10 q-8,0 -10,-10Z" fill="#7fc67a" opacity=".85"/><path d="M296,160 q6,-3 12,-8" stroke="#fff" opacity=".6" stroke-width="3" fill="none"/>'
mid=hills(W,330,16,11,'url(#moon)',ln=LINE,n=6,ex='stroke-opacity=".5"')
for x,y,rx in ((60,380,28),(230,430,38),(320,372,20),(130,480,26),(300,500,24),(40,470,16)):
    mid+=f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx*.3:.0f}" fill="#4d3c80" opacity=".55"/><path d="M{x-rx},{y} a{rx},{rx*.3:.0f} 0 0 1 {2*rx},0" fill="none" stroke="#d6c9f0" stroke-width="2.5" opacity=".6"/>'
# dome base
mid+=f'<g filter="url(#wob)"><rect x="205" y="318" width="110" height="26" rx="5" fill="#8a7cb8" stroke="{LINE}" stroke-width="2.5" stroke-opacity=".7"/><path d="M215,318 a45,45 0 0 1 90,0Z" fill="url(#dome)" stroke="{LINE}" stroke-width="2.5" stroke-opacity=".7"/>'
for x in (228,250,272,292): mid+=f'<rect x="{x}" y="326" width="9" height="9" rx="2" fill="#ffe08a"/>'
mid+=f'<path d="M232,309 q6,-18 28,-20" fill="none" stroke="#fff" opacity=".6" stroke-width="3"/><path d="M290,274 V300" stroke="{LINE}" stroke-width="3"/><circle cx="290" cy="272" r="4" fill="#ff7c9a"/><path d="M273,284 q17,-18 34,0" fill="none" stroke="#e8e0f6" stroke-width="3.5"/></g>'
front=hills(W,545,12,5,'#7a6aa6',ln=LINE,n=5,ex='stroke-opacity=".6"')
for x,y,r in ((40,575,16),(300,580,22),(180,590,12)):
    front+=f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*.32:.1f}" fill="#4a3c78" opacity=".7"/>'
front+=f'<g transform="translate(14,520)"><circle cx="20" cy="38" r="13" fill="#3b3a4f" stroke="{LINE}" stroke-width="2"/><circle cx="20" cy="38" r="5" fill="#9a93b8"/><circle cx="60" cy="38" r="13" fill="#3b3a4f" stroke="{LINE}" stroke-width="2"/><circle cx="60" cy="38" r="5" fill="#9a93b8"/><rect x="8" y="16" width="64" height="20" rx="7" fill="#efe9fa" stroke="{LINE}" stroke-width="2"/><rect x="44" y="20" width="20" height="9" rx="3" fill="#6bd2c6"/></g>'
front+=f'<path d="M318,538 l10,-24 l9,24Z" fill="#8f82bd" stroke="{LINE}" stroke-width="2"/>'
write_land('space',defs,back,mid,front)

# ---------- 3. farm & mill ----------
defs=f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f6b58a"/><stop offset=".5" stop-color="#ffd9b0"/><stop offset="1" stop-color="#ffeed6"/></linearGradient>
<radialGradient id="sun" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fffbe0"/><stop offset=".4" stop-color="#ffd35c" stop-opacity=".9"/><stop offset="1" stop-color="#ffd35c" stop-opacity="0"/></radialGradient>{WOBBLE}'''
back=f'<rect width="{W}" height="{H}" fill="url(#sky)"/><circle cx="90" cy="120" r="130" fill="url(#sun)"/><circle cx="90" cy="120" r="30" fill="#fff1b5" stroke="#f1b43c" stroke-width="3"/>'
back+=''.join(f'<path d="M90,120 L{90+150*math.cos(a):.0f},{120+150*math.sin(a):.0f}" stroke="#ffe08a" stroke-width="6" opacity=".25" stroke-linecap="round"/>' for a in [i*math.pi/6 for i in range(12)])
for cx,cy,s in ((250,70,1.1),(320,140,.7)): back+=f'<g fill="#fffaf0" opacity=".9" transform="translate({cx},{cy}) scale({s})"><ellipse rx="34" ry="10"/><ellipse cx="-12" cy="-7" rx="15" ry="11"/><ellipse cx="10" cy="-9" rx="18" ry="13"/></g>'
back+=hills(W,250,14,21,'#e9a67e',n=6)+hills(W,285,12,22,'#d98a6c',n=6)
mid=hills(W,320,10,23,'#c9726a',ln=None,n=6)
# windmill
mid+=f'<g filter="url(#wob)" transform="translate(262,210)"><path d="M-26,118 L-16,26 L16,26 L26,118Z" fill="#f4e0b8" stroke="{LINE}" stroke-width="2.6" stroke-opacity=".75"/><path d="M-16,26 L0,6 L16,26Z" fill="#7a2e4f" stroke="{LINE}" stroke-width="2.6" stroke-opacity=".75"/><rect x="-7" y="92" width="14" height="26" rx="7" fill="#7a2e4f"/><circle cx="0" cy="52" r="7" fill="#7a2e4f"/>'
for k in range(4):
    a=k*90+14
    mid+=f'<g transform="rotate({a} 0 26)"><rect x="-3" y="-60" width="6" height="86" fill="#8a5b30" stroke="{LINE}" stroke-width="1.5"/><rect x="3" y="-56" width="20" height="40" fill="#fff0c9" stroke="{LINE}" stroke-width="2" stroke-opacity=".7"/><path d="M5,-44 H21 M5,-32 H21 M5,-20 H21" stroke="{LINE}" stroke-width="1" opacity=".5"/></g>'
mid+=f'<circle cx="0" cy="26" r="6" fill="#dbac54" stroke="{LINE}" stroke-width="2"/></g>'
# water wheel house + stream
mid+=f'<g transform="translate(40,300)"><rect x="0" y="20" width="58" height="42" fill="#f4e0b8" stroke="{LINE}" stroke-width="2.4" stroke-opacity=".7"/><path d="M-6,22 L29,-6 L64,22Z" fill="#a5473c" stroke="{LINE}" stroke-width="2.4" stroke-opacity=".7"/><rect x="22" y="38" width="14" height="24" fill="#7a2e4f"/><g transform="translate(70,44)"><circle r="22" fill="none" stroke="#8a5b30" stroke-width="4"/><circle r="4" fill="#8a5b30"/>'
for k in range(8):
    a=k*45
    mid+=f'<g transform="rotate({a})"><path d="M0,0 V-22" stroke="#8a5b30" stroke-width="3"/><rect x="-5" y="-27" width="10" height="7" fill="#c9884d" stroke="{LINE}" stroke-width="1.2"/></g>'
mid+='</g></g>'
mid+=f'<path d="M-10,420 Q80,380 150,430 T360,420 L360,450 Q250,455 150,462 Q70,420 -10,455Z" fill="#8fd3de" stroke="{LINE}" stroke-opacity=".35" stroke-width="2"/><path d="M20,432 q20,-6 40,0 M180,438 q20,-6 40,0" stroke="#fff" stroke-width="2.5" fill="none" opacity=".7" stroke-linecap="round"/>'
front=hills(W,520,10,24,'#b9583f',n=5)
# fence
for i in range(9):
    x=10+i*42
    front+=f'<rect x="{x}" y="{540}" width="9" height="46" rx="2" fill="#c98c52" stroke="{LINE}" stroke-width="2" stroke-opacity=".7"/>'
front+=f'<rect x="0" y="552" width="{W}" height="6" fill="#d9a064" stroke="{LINE}" stroke-width="1.6" stroke-opacity=".6"/><rect x="0" y="570" width="{W}" height="6" fill="#d9a064" stroke="{LINE}" stroke-width="1.6" stroke-opacity=".6"/>'
# haystack and wheat
front+=f'<g transform="translate(300,560)"><path d="M-30,32 Q-30,-14 0,-18 Q30,-14 30,32Z" fill="#f0c15a" stroke="{LINE}" stroke-width="2.4" stroke-opacity=".7"/><path d="M-18,10 q18,-8 36,0 M-22,22 q22,-8 44,0" stroke="#c78d2a" stroke-width="2" fill="none"/></g>'
for i in range(14):
    x=R.uniform(6,350);y=592
    front+=f'<path d="M{x:.0f},{y} q{R.uniform(-4,4):.0f},-18 0,-36" stroke="#e9b63e" stroke-width="2" fill="none"/><ellipse cx="{x:.0f}" cy="{y-38}" rx="3" ry="7" fill="#f4cb5c"/>'
write_land('farm',defs,back,mid,front)

# ---------- 4. machine city ----------
defs=f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a9d2dc"/><stop offset="1" stop-color="#eaf5ee"/></linearGradient>
<linearGradient id="bld" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6f8f96"/><stop offset="1" stop-color="#5b7b86"/></linearGradient>
<linearGradient id="brk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c0805c"/><stop offset="1" stop-color="#a5694b"/></linearGradient>{WOBBLE}'''
back=f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
for cx,cy,s in ((70,70,1),(250,100,.8),(330,50,.6)): back+=f'<g fill="#fff" opacity=".8" transform="translate({cx},{cy}) scale({s})"><ellipse rx="34" ry="10"/><ellipse cx="-12" cy="-7" rx="15" ry="11"/><ellipse cx="10" cy="-9" rx="18" ry="13"/></g>'
# far skyline silhouette
sk='<g fill="#9fbfc4" stroke="#7fa0a8" stroke-width="2">'
x=0
while x<W:
    w=R.randrange(26,50);h=R.randrange(60,150);sk+=f'<rect x="{x}" y="{330-h}" width="{w}" height="{h+60}"/>';x+=w+R.randrange(0,6)
sk+='</g>'
back+=sk
back+=gear(60,200,38,10,'#8fb0b6',ln='#7fa0a8',lw=2)+gear(300,250,28,9,'#8fb0b6',ln='#7fa0a8',lw=2)+gear(100,255,18,8,'#a3c2c6',ln='#7fa0a8',lw=2)
mid=''
# chimneys with smoke
for x in (40,150,312):
    mid+=f'<g filter="url(#wob)"><rect x="{x}" y="230" width="22" height="110" fill="url(#brk)" stroke="{LINE}" stroke-width="2.4" stroke-opacity=".7"/><rect x="{x-3}" y="226" width="28" height="9" fill="#8a5538" stroke="{LINE}" stroke-width="2" stroke-opacity=".7"/></g>'
    mid+=f'<g fill="#fff" opacity=".8"><circle cx="{x+14}" cy="206" r="11"/><circle cx="{x+26}" cy="190" r="14"/><circle cx="{x+14}" cy="168" r="16"/></g>'
# factory body
mid+=f'<g filter="url(#wob)"><path d="M0,350 V300 H70 V270 L110 296 V270 L150 296 V270 L190 296 V340 H360 V350Z" fill="url(#bld)" stroke="{LINE}" stroke-width="2.6" stroke-opacity=".7"/>'
for xx in range(14,340,34):
    if xx<190 or xx>200: mid+=f'<rect x="{xx}" y="{314 if xx>70 else 316}" width="18" height="14" rx="3" fill="#fbe08a" stroke="{LINE}" stroke-width="1.5" stroke-opacity=".6"/>'
mid+='</g>'
mid+='<rect x="0" y="350" width="360" height="260" fill="#c9d6c6"/>'
for yy in range(392,520,22):
    for xx in range(-20,380,44): mid+=f'<rect x="{xx+(yy%44)}" y="{yy}" width="40" height="18" rx="5" fill="#b6c6b4" opacity=".7"/>'
# rail
mid+=f'<rect x="0" y="364" width="{W}" height="9" fill="#7c6b5e"/>'+''.join(f'<rect x="{i*18}" y="372" width="9" height="6" fill="#5b4a3e"/>' for i in range(21))
front=f'<rect x="0" y="520" width="{W}" height="80" fill="#8e9a9a"/><path d="M0,520 H360" stroke="{LINE}" stroke-width="3" stroke-opacity=".6"/>'
for i in range(0,360,40): front+=f'<path d="M{i},520 v80" stroke="#7a8686" stroke-width="2"/>'
front+=gear(40,560,38,10,'#d0a24a',ln=LINE,lw=2.4)+gear(100,590,24,9,'#bd8a3a',ln=LINE,lw=2.2)+gear(330,566,34,10,'#d0a24a',ln=LINE,lw=2.4)
front+=f'<rect x="150" y="540" width="120" height="14" rx="7" fill="#6f8f96" stroke="{LINE}" stroke-width="2.2"/><rect x="146" y="536" width="12" height="22" rx="4" fill="#5b7b86" stroke="{LINE}" stroke-width="2"/><rect x="262" y="536" width="12" height="22" rx="4" fill="#5b7b86" stroke="{LINE}" stroke-width="2"/>'
front+=f'<g transform="translate(184,572) rotate(-12)"><rect x="-4" y="-2" width="62" height="7" rx="3" fill="#8a5b30" stroke="{LINE}" stroke-width="1.8"/><rect x="-14" y="-12" width="22" height="16" rx="3" fill="#6f7d84" stroke="{LINE}" stroke-width="1.8"/></g>'
write_land('city',defs,back,mid,front)
print('lands ok')
