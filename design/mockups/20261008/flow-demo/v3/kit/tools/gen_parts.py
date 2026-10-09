from kitlib import *

# ============ NODES (96x96) ============
def node_base(ring_a, ring_b, face_a, face_b, extra_def=''):
    d=f'''<linearGradient id="rg" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="{ring_a}"/><stop offset="1" stop-color="{ring_b}"/></linearGradient>
<radialGradient id="fc" cx=".4" cy=".3" r=".85"><stop offset="0" stop-color="{face_a}"/><stop offset="1" stop-color="{face_b}"/></radialGradient>{SHADOW}{extra_def}'''
    b=f'<ellipse cx="48" cy="82" rx="34" ry="8" fill="#2a1a08" opacity=".38" filter="url(#sh)"/>'
    b+=f'<circle cx="48" cy="46" r="40" fill="url(#rg)" stroke="{LINE}" stroke-width="3"/>'
    b+=f'<circle cx="48" cy="46" r="33" fill="none" stroke="{LINE}" stroke-opacity=".35" stroke-width="2"/>'
    b+=f'<circle cx="48" cy="46" r="31" fill="url(#fc)" stroke="{LINE}" stroke-opacity=".5" stroke-width="2"/>'
    b+=f'<path d="M20,34 A31,31 0 0 1 58,17" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="3" stroke-linecap="round"/>'
    for a in (45,135,225,315):  # rivets
        import math
        x=48+36.5*math.cos(math.radians(a)); y=46+36.5*math.sin(math.radians(a))
        b+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.3" fill="{GOLD_L}" stroke="{LINE}" stroke-opacity=".6" stroke-width="1"/>'
    b+='<g id="slot"></g>'
    return d,b
def padlock(cx,cy,s,body,sh,ln=LINE):
    return (f'<g transform="translate({cx},{cy}) scale({s})"><path d="M-9,-4 V-12 a9,9 0 0 1 18,0 V-4" fill="none" stroke="{sh}" stroke-width="5" stroke-linecap="round"/>'
            f'<path d="M-9,-4 V-12 a9,9 0 0 1 18,0 V-4" fill="none" stroke="{ln}" stroke-width="1.4" opacity=".6"/>'
            f'<rect x="-14" y="-5" width="28" height="22" rx="5" fill="{body}" stroke="{ln}" stroke-width="2.4"/>'
            f'<circle cx="0" cy="5" r="3.2" fill="{ln}"/><rect x="-1.4" y="5" width="2.8" height="7" rx="1" fill="{ln}"/></g>')
# locked
d,b=node_base('#a79c8a','#6e6455','#d4ccbd','#a79c8a')
b+=padlock(48,46,1.15,'#8d826f','#5e5547')
b+='<circle cx="48" cy="46" r="31" fill="#4d4436" opacity=".12"/>'
svg('node-locked.svg',96,96,b,d)
# open / fresh
d,b=node_base(GOLD_L,GOLD_D,'#fffaf0','#f6e2b0',f'<radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset=".6" stop-color="#ffe796" stop-opacity=".9"/><stop offset="1" stop-color="#ffe796" stop-opacity="0"/></radialGradient>')
b='<circle cx="48" cy="46" r="47" fill="url(#gl)"/>'+b
b+=f'<g transform="translate(78,16)"><circle r="11" fill="{INK}" stroke="{LINE}" stroke-width="2.4"/><circle r="8" fill="none" stroke="{GOLD_L}" stroke-width="1.6"/>{star4(0,0,6,CREAM)}</g>'
svg('node-open.svg',96,96,b,d)
# done ("after": lit, pennant planted)
d,b=node_base('#3d8f86',INK,'#fffbe0','#ffd87a',f'<radialGradient id="gl" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="#ffd87a" stop-opacity=".75"/><stop offset="1" stop-color="#ffd87a" stop-opacity="0"/></radialGradient>')
b='<circle cx="48" cy="46" r="47" fill="url(#gl)"/>'+b
b+=f'<circle cx="48" cy="46" r="37.5" fill="none" stroke="{GOLD}" stroke-width="2.2" stroke-dasharray="1 5.5" stroke-linecap="round"/>'
b+=f'<g transform="translate(76,12)"><path d="M0,26 V-6" stroke="{LINE}" stroke-width="3.4" stroke-linecap="round"/><path d="M1.5,-6 L17,0 L1.5,6Z" fill="{GOLD}" stroke="{LINE}" stroke-width="2" stroke-linejoin="round"/><circle cx="0" cy="-7" r="2.4" fill="{GOLD_L}" stroke="{LINE}" stroke-width="1.2"/></g>'
svg('node-done.svg',96,96,b,d)
# experimental
d,b=node_base(GOLD_L,GOLD_D,'#fffaf0','#efe3c6',f'<pattern id="hat" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="none"/><rect width="3" height="8" fill="{GOLD}" opacity=".35"/></pattern>')
b=b.replace('<g id="slot"></g>',f'<circle cx="48" cy="46" r="31" fill="url(#hat)"/><g id="slot"></g>')
b+=f'<circle cx="48" cy="46" r="43.5" fill="none" stroke="{INK}" stroke-width="3" stroke-dasharray="7 6" stroke-linecap="round"/>'
fl=f'<g transform="translate(17,70)"><circle r="12" fill="{INK}" stroke="{LINE}" stroke-width="2.4"/><path d="M-3.4,-7 h6.8 M-2.4,-7 v5.5 l-5,8.5 a1.8,1.8 0 0 0 1.6,2.7 h11.6 a1.8,1.8 0 0 0 1.6,-2.7 l-5,-8.5 v-5.5" fill="#bfeee9" stroke="{CREAM}" stroke-width="1.7" stroke-linejoin="round"/><path d="M-5,3 h10" stroke="{CREAM}" stroke-width="1.4"/></g>'
b+=fl
svg('node-trial.svg',96,96,b,d)

# here ring + pin
d=f'{GOLD_GRAD}{SHADOW}'
svg('ring-here.svg',112,112,f'<circle cx="56" cy="56" r="50" fill="none" stroke="{LINE}" stroke-width="9" opacity=".55"/><circle cx="56" cy="56" r="50" fill="none" stroke="url(#gold)" stroke-width="6"/><circle cx="56" cy="56" r="50" fill="none" stroke="{CREAM}" stroke-width="1.5" stroke-dasharray="2 9" stroke-linecap="round"/>',d)
svg('badge-here.svg',40,52,f'<ellipse cx="20" cy="47" rx="9" ry="3.5" fill="#2a1a08" opacity=".35" filter="url(#sh)"/><path d="M20,48 C6,32 4,26 4,19 a16,16 0 0 1 32,0 c0,7 -2,13 -16,29Z" fill="url(#gold)" stroke="{LINE}" stroke-width="2.6" stroke-linejoin="round"/><circle cx="20" cy="19" r="8.5" fill="{CREAM}" stroke="{LINE}" stroke-width="2"/><circle cx="20" cy="19" r="3.6" fill="{INK}"/>',d)

# ============ FOG ============
d='<filter id="bl" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter><filter id="bl2" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>'
b=''
import random
R=random.Random(5)
for i in range(18):
    x=R.uniform(10,350);y=R.uniform(55,145);rx=R.uniform(45,80)
    b+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{rx*.42:.0f}" fill="#b9b2c4" opacity=".55" filter="url(#bl)"/>'
for i in range(7):
    x=R.uniform(30,330);y=R.uniform(70,130);rx=R.uniform(28,50)
    b+=f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rx:.0f}" ry="{rx*.3:.0f}" fill="#f6f1ee" opacity=".92" filter="url(#bl2)"/>'
svg('fog.svg',360,200,b,d)
svg('fog-band.svg',390,120,b.replace('cy="','cy="').replace('viewBox',''),d)  # same puffs, wide band
svg('fog-sign.svg',64,84,f'''<ellipse cx="32" cy="78" rx="18" ry="4.5" fill="#2a1a08" opacity=".35"/><rect x="28" y="24" width="8" height="54" rx="2" fill="#8a5b30" stroke="{LINE}" stroke-width="2.4"/>
<path d="M6,10 H46 L58,24 L46,38 H6Z" fill="#c98c52" stroke="{LINE}" stroke-width="2.6" stroke-linejoin="round"/><path d="M10,14 H44" stroke="#e8b878" stroke-width="2"/>
<path d="M14,30 q8,-14 16,-6 t14,-4" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-dasharray="1 6"/><path d="M40,16 l6,4 -6,4" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>''')

# ============ PATH pieces ============
svg('footprint.svg',24,28,f'<g fill="{CREAM}" stroke="{LINE}" stroke-width="1.4" stroke-opacity=".75"><ellipse cx="7" cy="18" rx="4.2" ry="6.2" transform="rotate(-8 7 18)"/><circle cx="4.6" cy="9.5" r="1.7"/><circle cx="8" cy="8.2" r="1.7"/><circle cx="11.2" cy="9.2" r="1.7"/><ellipse cx="17" cy="11" rx="4" ry="5.8" transform="rotate(8 17 11)"/><circle cx="14.6" cy="3.4" r="1.6"/><circle cx="18" cy="2.6" r="1.6"/><circle cx="21" cy="4" r="1.6"/></g>')
svg('path-done-tile.svg',20,48,f'<rect x="5" y="0" width="10" height="48" fill="{LINE}" opacity=".55"/><rect x="6" y="0" width="8" height="48" fill="{INK}"/><rect x="8" y="0" width="2" height="48" fill="#4aa59b" opacity=".75"/>')
svg('path-todo-tile.svg',20,24,f'<rect x="8.5" y="3" width="3.6" height="12" rx="1.8" fill="#8a6a34" opacity=".75"/>')

# ============ ORNAMENTS ============
svg('rivet.svg',16,16,f'<circle cx="8" cy="8" r="6.5" fill="url(#gold)" stroke="{LINE}" stroke-width="1.6"/><circle cx="6.2" cy="6" r="1.8" fill="#fff" opacity=".7"/>',GOLD_GRAD)
# rope (seamless: period 12, width 48)
r=''
for i in range(-1,6):
    x=i*12
    r+=f'<path d="M{x},16 L{x+7},0 L{x+13},0 L{x+6},16Z" fill="#f0dcab" stroke="{LINE}" stroke-width="1.2" stroke-opacity=".7"/><path d="M{x+3},16 L{x+9},4" stroke="#b78a42" stroke-width="2.2" opacity=".55"/>'
svg('rope-h.svg',48,16,f'<rect width="48" height="16" fill="#d4b06a"/>{r}<rect width="48" height="1.6" fill="{LINE}" opacity=".5"/><rect y="14.4" width="48" height="1.6" fill="{LINE}" opacity=".5"/>')
svg('corner-curl.svg',40,40,f'<path d="M3,37 V16 a13,13 0 0 1 13,-13 H37" fill="none" stroke="{LINE}" stroke-width="7" stroke-linecap="round"/><path d="M3,37 V16 a13,13 0 0 1 13,-13 H37" fill="none" stroke="url(#gold)" stroke-width="4.6" stroke-linecap="round"/><circle cx="12" cy="12" r="4.6" fill="url(#gold)" stroke="{LINE}" stroke-width="1.6"/>',GOLD_GRAD)
def plate(name,fill_a,fill_b,inner_line):
    svg(name,96,48,f'<rect x="2" y="2" width="92" height="44" rx="14" fill="{LINE}"/><rect x="3" y="3" width="90" height="42" rx="13" fill="url(#gold)"/><rect x="8" y="8" width="80" height="32" rx="9" fill="{LINE}" opacity=".5"/><rect x="9" y="9" width="78" height="30" rx="8" fill="url(#f)"/><rect x="9" y="9" width="78" height="30" rx="8" fill="none" stroke="{inner_line}" stroke-width="1.4" opacity=".55"/><circle cx="12" cy="12" r="2.2" fill="{GOLD_L}" stroke="{LINE}" stroke-width=".8"/><circle cx="84" cy="12" r="2.2" fill="{GOLD_L}" stroke="{LINE}" stroke-width=".8"/><circle cx="12" cy="36" r="2.2" fill="{GOLD_L}" stroke="{LINE}" stroke-width=".8"/><circle cx="84" cy="36" r="2.2" fill="{GOLD_L}" stroke="{LINE}" stroke-width=".8"/>',
        GOLD_GRAD+f'<linearGradient id="f" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{fill_a}"/><stop offset="1" stop-color="{fill_b}"/></linearGradient>')
plate('plate-cream.svg','#fffaf0','#f6e2b0','#a97b2c')
plate('plate-teal.svg','#2b6f69','#184441','#f6dc92')

# textures
svg('tile-paper.svg',160,160,f'<filter id="n" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="3" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .45  0 0 0 0 .3  0 0 0 0 .1  0 0 0 .34 0"/></filter><filter id="m" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".012" numOctaves="3" seed="9" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .6  0 0 0 0 .4  0 0 0 0 .1  0 0 0 .3 0"/></filter><rect width="160" height="160" fill="{CREAM}"/><rect width="160" height="160" filter="url(#m)"/><rect width="160" height="160" filter="url(#n)"/>')
svg('tile-teal.svg',120,120,f'<filter id="n" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".7" numOctaves="2" seed="5" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 .9  0 0 0 0 .6  0 0 0 .1 0"/></filter><rect width="120" height="120" fill="#1f5a56"/><rect width="120" height="120" filter="url(#n)"/><path d="M0,60 L30,30 L60,60 L90,30 L120,60 L90,90 L60,60 L30,90Z" fill="none" stroke="#2f7a73" stroke-width="2" opacity=".55"/>')

# ============ MAP BG (vertical tile 390x800) ============
d='''<filter id="paper" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .4  0 0 0 0 .26  0 0 0 0 .08  0 0 0 .25 0"/></filter>
<filter id="blot" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".006 .004" numOctaves="4" seed="12" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .62  0 0 0 0 .4  0 0 0 0 .12  0 0 0 .55 -.12"/></filter>
<filter id="burn" x="-20%" y="0" width="140%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".02 .06" numOctaves="3" seed="8" stitchTiles="stitch" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="26"/><feGaussianBlur stdDeviation="3"/></filter>
<linearGradient id="vigL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#4a2a0c" stop-opacity=".85"/><stop offset=".5" stop-color="#7a4a1a" stop-opacity=".35"/><stop offset="1" stop-color="#9a6a2a" stop-opacity="0"/></linearGradient>
<linearGradient id="vigR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#4a2a0c" stop-opacity=".85"/><stop offset=".5" stop-color="#7a4a1a" stop-opacity=".35"/><stop offset="1" stop-color="#9a6a2a" stop-opacity="0"/></linearGradient>'''
b='<rect width="390" height="800" fill="#f2dca4"/><rect width="390" height="800" filter="url(#blot)"/><rect width="390" height="800" filter="url(#paper)"/>'
# faint folds (continue across tile: at y=0/800 edge)
b+='<g stroke="#b88a46" stroke-opacity=".22" stroke-width="2.2"><path d="M0,0 H390"/><path d="M130,0 V800" stroke-opacity=".12"/><path d="M262,0 V800" stroke-opacity=".12"/></g><g stroke="#fff" stroke-opacity=".35" stroke-width="1.4"><path d="M0,2 H390"/></g>'
b+='<g filter="url(#burn)"><rect x="-30" y="0" width="52" height="800" fill="url(#vigL)"/><rect x="368" y="0" width="52" height="800" fill="url(#vigR)"/></g>'
b+='<g fill="none" stroke="#a87a3c" stroke-opacity=".28" stroke-width="2"><path d="M40,120 q30,-20 60,0 t60,0" stroke-dasharray="2 7" stroke-linecap="round"/><path d="M230,500 q30,-20 60,0 t60,0" stroke-dasharray="2 7" stroke-linecap="round"/><path d="M60,660 q30,-20 60,0" stroke-dasharray="2 7" stroke-linecap="round"/></g>'
svg('map-bg.svg',390,800,b,d)
print('parts ok')
