from kitlib import *
import math
CH=[ # id, name, main, light, dark
('force','#3f7fd0','#8db8ee','#1f4a8c'),
('friction','#9a6b43','#d1a679','#5e3d22'),
('multi','#8a5bc7','#c4a4ee','#50308a'),
('weight','#17a79f','#7fdcd3','#0b6762'),
('energy','#efbd1f','#ffe48a','#a47a07'),
('machine','#e0699c','#f5b0cd','#9c2f62'),
('lever','#4a55c4','#9ca3ee','#272f86'),
('slope','#8d3562','#c47a9f','#54183a'),
('wheel','#6a8aa5','#aec3d4','#3a566e'),
('summary','#263e6e','#6f89c0','#121f40'),
]
def glyph(k, fg, hi, ln, acc):
    """64x64 drawing. fg main fill, hi highlight fill, ln outline, acc accent (gold)."""
    S=f'stroke="{ln}" stroke-width="2.6" stroke-linejoin="round" stroke-linecap="round"'
    if k=='force':
        return (f'<path d="M3,35 H20 V29 L31,40 L20,51 V45 H3Z" fill="{acc}" {S}/>'
                f'<rect x="33" y="24" width="26" height="26" rx="3" fill="{fg}" {S}/><path d="M33,30 H59 M33,44 H59" stroke="{ln}" stroke-width="1.6" opacity=".5"/><path d="M36,27 H56" stroke="{hi}" stroke-width="2" opacity=".8"/>'
                f'<path d="M26,17 l-4,-7 M34,15 v-8 M42,17 l4,-7" stroke="{ln}" stroke-width="2.4" stroke-linecap="round" opacity=".6"/>')
    if k=='friction':
        return (f'<path d="M2,50 l5,5 5,-5 5,5 5,-5 5,5 5,-5 5,5 5,-5 5,5 5,-5 5,5 5,-5 V60 H2Z" fill="{hi}" {S}/>'
                f'<rect x="12" y="24" width="30" height="24" rx="3" fill="{fg}" {S}/><path d="M16,28 H38" stroke="{hi}" stroke-width="2" opacity=".8"/>'
                f'<path d="M46,40 l9,-3 M46,46 l11,0 M48,34 l7,-6" stroke="{acc}" stroke-width="3" stroke-linecap="round"/><path d="M6,20 H26 M6,14 H18" stroke="{ln}" stroke-width="2.4" stroke-linecap="round" opacity=".5"/>')
    if k=='multi':
        return (f'<rect x="22" y="22" width="22" height="26" rx="3" fill="{fg}" {S}/><path d="M25,26 H41" stroke="{hi}" stroke-width="2" opacity=".8"/>'
                f'<path d="M2,35 H14 V29 L21,35 L14,41 V35" fill="{acc}" {S}/>'
                f'<path d="M62,35 H54 V30 L45,35 L54,40 V35" fill="{hi}" {S}/><path d="M6,12 L30,12 M34,12 H58" stroke="{ln}" stroke-width="2" opacity="0"/>')
    if k=='weight':
        return (f'<path d="M12,50 h40 a4,4 0 0 1 4,4 v2 a3,3 0 0 1 -3,3 h-42 a3,3 0 0 1 -3,-3 v-2 a4,4 0 0 1 4,-4Z" fill="{fg}" {S}/>'
                f'<circle cx="32" cy="54" r="3.6" fill="{hi}" stroke="{ln}" stroke-width="1.6"/><path d="M10,44 Q32,38 54,44 V50 H10Z" fill="{hi}" {S}/>'
                f'<path d="M32,16 C22,10 12,18 14,30 c1,8 8,14 18,12 c10,2 17,-4 18,-12 c2,-12 -8,-20 -18,-14Z" fill="{acc}" {S}/><path d="M32,16 q0,-8 6,-11" fill="none" {S}/><path d="M33,9 q8,-5 12,1 q-6,5 -12,-1Z" fill="{hi}" {S}/><path d="M20,24 q2,-5 6,-6" stroke="#fff" stroke-width="2.4" stroke-linecap="round" fill="none" opacity=".7"/>')
    if k=='energy':
        s=f'<path d="M24,58 L28,30 H36 L40,58Z" fill="{hi}" {S}/><path d="M30,30 L32,22 L34,30" fill="{ln}" opacity=".3"/>'
        for a in (20,110,200,290):
            s+=f'<g transform="rotate({a} 32 25)"><path d="M32,25 L30,3 H35 Q42,5 36,14 Z" fill="{fg}" {S}/></g>'
        s+=f'<circle cx="32" cy="25" r="4.4" fill="{acc}" {S}/>'+star4(54,12,7,acc).replace('/>',f' stroke="{ln}" stroke-width="1.6"/>')
        return s
    if k=='machine':
        return (f'<path d="M32,20 V54" {S}/><path d="M18,57 H46 L42,50 H22Z" fill="{fg}" {S}/>'
                f'<path d="M8,20 L56,20" fill="none" stroke="{ln}" stroke-width="3.2" stroke-linecap="round"/><circle cx="32" cy="18" r="4" fill="{acc}" {S}/>'
                f'<path d="M8,20 L2,38 M8,20 L16,38 M56,20 L48,38 M56,20 L62,38" fill="none" stroke="{ln}" stroke-width="1.8"/>'
                f'<path d="M0,38 H18 a9,9 0 0 1 -18,0Z" fill="{hi}" {S}/><path d="M46,38 H64 a9,9 0 0 1 -18,0Z" fill="{hi}" {S}/>'
                f'<circle cx="9" cy="33" r="4.4" fill="{fg}" stroke="{ln}" stroke-width="2"/>')
    if k=='lever':
        return (f'<path d="M32,36 L20,56 H44Z" fill="{hi}" {S}/><g transform="rotate(-14 32 36)"><rect x="3" y="31" width="58" height="8" rx="3" fill="{fg}" {S}/></g>'
                f'<rect x="3" y="14" width="15" height="15" rx="2.5" fill="{acc}" {S} transform="rotate(-14 10 22)"/><circle cx="53" cy="22" r="6" fill="{hi}" {S}/><path d="M53,10 v-6" stroke="{ln}" stroke-width="2.4" stroke-linecap="round" opacity=".6"/>')
    if k=='slope':
        return (f'<path d="M3,56 H61 V16Z" fill="{fg}" {S}/><path d="M3,56 L61,16" stroke="{hi}" stroke-width="2.6" opacity=".7"/>'
                f'<g transform="translate(26 38) rotate(-34)"><rect x="-9" y="-16" width="18" height="16" rx="2.5" fill="{acc}" {S}/></g>'
                f'<path d="M44,56 V44 L61,56Z" fill="{hi}" {S}/>')
    if k=='wheel':
        s=f'<path d="M44,28 V48" stroke="{ln}" stroke-width="2.4"/><rect x="38" y="48" width="12" height="11" rx="2.5" fill="{acc}" {S}/>'
        s+=f'<circle cx="26" cy="26" r="17" fill="{hi}" {S}/><circle cx="26" cy="26" r="11" fill="{fg}" stroke="{ln}" stroke-width="2"/>'
        for a in range(0,360,60): s+=f'<path d="M26,26 L{26+11*math.cos(math.radians(a)):.1f},{26+11*math.sin(math.radians(a)):.1f}" stroke="{ln}" stroke-width="1.8"/>'
        s+=f'<circle cx="26" cy="26" r="3.2" fill="{acc}" stroke="{ln}" stroke-width="1.6"/><path d="M43,26 A17,17 0 0 1 26,43" fill="none" stroke="{ln}" stroke-width="2.4"/>'
        s+=gear(12,52,9,7,acc,ln=ln,lw=1.8)
        return s
    if k=='summary':
        return (f'<path d="M14,58 V30 a18,18 0 0 1 36,0 V58Z" fill="{ln}" {S}/><path d="M18,58 V30 a14,14 0 0 1 28,0 V58Z" fill="{acc}" opacity=".85"/>'
                f'<path d="M18,58 L32,54 V22 L18,28Z" fill="{fg}" {S}/><circle cx="28" cy="40" r="1.8" fill="{ln}"/>'
                +star4(32,6,6,hi).replace('/>',f' stroke="{ln}" stroke-width="1.5"/>')+
                f'<ellipse cx="14" cy="59" rx="12" ry="3.5" fill="{hi}" opacity=".85"/><ellipse cx="48" cy="60" rx="14" ry="3.2" fill="{hi}" opacity=".85"/>')
for k,main,light,dark in CH:
    g=glyph(k,main,light,dark,GOLD_L)
    svg(f'glyph-{k}.svg',64,64,g)   # for the cream face of a node / card
    # medallion (chapter badge)
    d=f'<radialGradient id="m" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="{light}"/><stop offset=".55" stop-color="{main}"/><stop offset="1" stop-color="{dark}"/></radialGradient>{GOLD_GRAD}{SHADOW}'
    g2=glyph(k,CREAM,'#fff',dark,GOLD_L)
    b=(f'<ellipse cx="32" cy="58" rx="22" ry="4" fill="#2a1a08" opacity=".3" filter="url(#sh)"/><circle cx="32" cy="31" r="30" fill="url(#gold)" stroke="{LINE}" stroke-width="2.4"/>'
       f'<circle cx="32" cy="31" r="25" fill="url(#m)" stroke="{LINE}" stroke-width="2"/><g transform="translate(8 7) scale(.75)">{g2}</g>'
       f'<path d="M12,20 A22,22 0 0 1 30,8" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2.4" stroke-linecap="round"/>')
    svg(f'sym-{k}.svg',64,64,b,d)

# ================= ICONS (96) =================
S=f'stroke="{LINE}" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"'
def ico(name,body,defs=''):
    svg(f'icon-{name}.svg',96,96,body,GOLD_GRAD+SHADOW+defs)
WOOD='<linearGradient id="wd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d49a5a"/><stop offset="1" stop-color="#9a5f2c"/></linearGradient>'
ico('map',f'<path d="M8,26 L34,16 L62,28 L88,18 V70 L62,80 L34,68 L8,78Z" fill="#f6e2b0" {S}/><path d="M34,16 V68 M62,28 V80" stroke="{LINE}" stroke-width="2.4" opacity=".55"/><path d="M34,16 L62,28 V80 L34,68Z" fill="#fff3d0" opacity=".6"/>'
    f'<path d="M16,64 q10,-14 22,-4 t20,-12" fill="none" stroke="{INK}" stroke-width="3.4" stroke-dasharray="1 7" stroke-linecap="round"/>'
    f'<g transform="translate(66,12)"><path d="M0,34 C-10,22 -12,18 -12,13 a12,12 0 0 1 24,0 c0,5 -2,9 -12,21Z" fill="url(#gold)" {S}/><circle cx="0" cy="13" r="5" fill="{INK}"/></g>')
ico('cards',''.join(f'<g transform="rotate({a} 48 82)"><rect x="29" y="20" width="38" height="54" rx="6" fill="url(#gold)" {S}/><rect x="34" y="25" width="28" height="44" rx="3.5" fill="{c}" stroke="{LINE}" stroke-width="2"/>{extra}</g>' for a,c,extra in ((-22,'#fff0c9',''),(0,'#fff0c9',''),(22,'#fff0c9','')))
    +f'<g transform="translate(48 46)"><circle r="10" fill="{INK}" stroke="{LINE}" stroke-width="2.4"/>{gear(0,0,7,6,GOLD_L,ln=None,hole=.3)}</g><path d="M38,30 H58" stroke="{GOLD_D}" stroke-width="3" stroke-linecap="round" opacity=".6"/>')
ico('practice',f'<g transform="rotate(-10 40 30)"><rect x="24" y="10" width="26" height="36" rx="4" fill="#fff0c9" {S}/><path d="M30,20 H44 M30,27 H44" stroke="{GOLD_D}" stroke-width="2.6" stroke-linecap="round"/></g>'
    f'<g transform="rotate(8 58 30)"><rect x="44" y="6" width="26" height="38" rx="4" fill="#f6dc92" {S}/><path d="M50,18 H64 M50,25 H64" stroke="{GOLD_D}" stroke-width="2.6" stroke-linecap="round"/></g>'
    f'<path d="M10,48 H86 V82 a4,4 0 0 1 -4,4 H14 a4,4 0 0 1 -4,-4Z" fill="url(#wd)" {S}/><rect x="6" y="42" width="84" height="12" rx="4" fill="#8a5428" {S}/><rect x="38" y="62" width="20" height="9" rx="4.5" fill="{CREAM}" {S}/>'
    f'<g transform="translate(76 20)"><circle r="14" fill="{INK}" {S}/><path d="M-6,3 A7.5,7.5 0 1 1 5,5" fill="none" stroke="{CREAM}" stroke-width="3.2" stroke-linecap="round"/><path d="M5,-1 V6 H-2" fill="none" stroke="{CREAM}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></g>',WOOD)
ico('guide',f'<ellipse cx="48" cy="82" rx="34" ry="6" fill="#2a1a08" opacity=".3" filter="url(#sh)"/><path d="M14,62 a34,34 0 0 1 68,0Z" fill="#f4c430" {S}/><path d="M42,26 h12 v36 h-12Z" fill="#e9a91a" stroke="{LINE}" stroke-linejoin="round" stroke-width="2.6"/><path d="M22,50 a28,28 0 0 1 12,-18" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="4" stroke-linecap="round"/><rect x="6" y="60" width="84" height="12" rx="6" fill="#f4c430" {S}/><path d="M12,66 H84" stroke="#fff" stroke-opacity=".4" stroke-width="2.4" stroke-linecap="round"/><circle cx="48" cy="38" r="5" fill="{CREAM}" stroke="{LINE}" stroke-width="2.2"/>')
ico('menu',''.join(f'<rect x="{x}" y="{y}" width="36" height="36" rx="9" fill="{col}" {S}/><path d="M{x+7},{y+9} h16" stroke="#fff" stroke-opacity=".5" stroke-width="3.2" stroke-linecap="round"/>' for x,y,col in ((8,8,'#17a79f'),(52,8,'#f6dc92'),(8,52,'#8a5bc7'),(52,52,'#3f7fd0'))))
ico('adults',f'<path d="M48,8 L80,20 V46 C80,66 66,80 48,88 C30,80 16,66 16,46 V20Z" fill="url(#gold)" {S}/><path d="M48,16 L72,25 V46 C72,61 62,72 48,79 C34,72 24,61 24,46 V25Z" fill="{INK}" stroke="{LINE}" stroke-width="2.4"/><circle cx="48" cy="40" r="8" fill="none" stroke="{GOLD_L}" stroke-width="4"/><path d="M48,48 V66 M48,56 h7 M48,63 h5" fill="none" stroke="{GOLD_L}" stroke-width="4.4" stroke-linecap="round"/>')
ico('game',f'<ellipse cx="48" cy="80" rx="36" ry="6" fill="#2a1a08" opacity=".3" filter="url(#sh)"/><path d="M26,28 H70 C84,28 92,48 90,66 C88,74 80,76 74,70 L66,60 H30 L22,70 C16,76 8,74 6,66 C4,48 12,28 26,28Z" fill="{INK}" {S}/><path d="M18,34 q8,-4 16,-3" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="3.4" stroke-linecap="round"/><path d="M26,40 V54 M19,47 H33" stroke="{CREAM}" stroke-width="5" stroke-linecap="round"/><circle cx="64" cy="40" r="4.6" fill="{GOLD}" stroke="{LINE}" stroke-width="2"/><circle cx="74" cy="48" r="4.6" fill="{GOLD_L}" stroke="{LINE}" stroke-width="2"/><circle cx="64" cy="54" r="4.6" fill="#8db8ee" stroke="{LINE}" stroke-width="2"/>')
ico('eye',f'<path d="M4,48 C20,22 76,22 92,48 C76,74 20,74 4,48Z" fill="{CREAM}" {S}/><circle cx="48" cy="48" r="17" fill="#2b6f69" {S}/><circle cx="48" cy="48" r="8" fill="{INK2}"/><circle cx="42" cy="42" r="4.4" fill="#fff"/>')
ico('box',f'<ellipse cx="48" cy="84" rx="36" ry="6" fill="#2a1a08" opacity=".3" filter="url(#sh)"/><path d="M10,42 V30 a16,16 0 0 1 16,-16 H70 a16,16 0 0 1 16,16 V42Z" fill="#b97d3f" {S}/><rect x="8" y="40" width="80" height="42" rx="6" fill="url(#wd)" {S}/><path d="M8,52 H88" stroke="{LINE}" stroke-width="2.4" opacity=".5"/><rect x="38" y="36" width="20" height="24" rx="4" fill="url(#gold)" {S}/><circle cx="48" cy="46" r="3.6" fill="{LINE}"/><rect x="46.4" y="46" width="3.2" height="8" fill="{LINE}"/><path d="M16,24 q8,-6 18,-6" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="3.4" stroke-linecap="round"/>',WOOD)
ico('lock',f'<ellipse cx="48" cy="84" rx="26" ry="5" fill="#2a1a08" opacity=".3" filter="url(#sh)"/><path d="M28,44 V32 a20,20 0 0 1 40,0 V44" fill="none" stroke="{LINE}" stroke-width="13" stroke-linecap="round"/><path d="M28,44 V32 a20,20 0 0 1 40,0 V44" fill="none" stroke="#cfc6b6" stroke-width="8" stroke-linecap="round"/><rect x="16" y="42" width="64" height="40" rx="9" fill="#8d826f" {S}/><path d="M22,50 H74" stroke="#fff" stroke-opacity=".3" stroke-width="3.4" stroke-linecap="round"/><circle cx="48" cy="60" r="6" fill="{LINE}"/><rect x="45" y="60" width="6" height="14" rx="2" fill="{LINE}"/>')
ico('arrow',f'<path d="M86,36 H44 V20 L10,48 L44,76 V60 H86Z" fill="url(#gold)" {S}/><path d="M42,26 L20,48" stroke="#fff" stroke-opacity=".5" stroke-width="3.4" stroke-linecap="round"/>')
ico('bolt',f'<path d="M56,6 L20,54 H42 L34,90 L76,36 H52Z" fill="url(#gold)" {S}/>')
ico('flag',f'<path d="M26,90 V8" stroke="{LINE}" stroke-width="7" stroke-linecap="round"/><path d="M26,10 H78 L66,30 L78,50 H26Z" fill="{INK}" {S}/><circle cx="26" cy="8" r="6" fill="url(#gold)" {S}/>')
ico('flask',f'<path d="M36,8 h24 M40,8 v26 L16,72 a8,8 0 0 0 7,12 H73 a8,8 0 0 0 7,-12 L56,34 V8" fill="#bfeee9" {S}/><path d="M24,66 H72 l6,10 a6,6 0 0 1 -5,8 H23 a6,6 0 0 1 -5,-8Z" fill="#17a79f" {S}/><circle cx="40" cy="74" r="3" fill="#fff" opacity=".7"/><circle cx="56" cy="70" r="2.2" fill="#fff" opacity=".7"/>')
# big medallion variants (160)
for n,col in (('map','#17a79f'),('cards','#8a5bc7'),('practice','#e0a21a'),('guide','#3f7fd0'),('adults','#6a8aa5')):
    base=open(os.path.join(OUT,f'icon-{n}.svg')).read()
    inner=base.split('</defs>',1)[1].rsplit('</svg>',1)[0]
    defs_in=base.split('<defs>',1)[1].split('</defs>',1)[0]
    d=defs_in.replace('id="gold"','id="gold"')+f'<radialGradient id="mb" cx=".35" cy=".25" r=".9"><stop offset="0" stop-color="#fff0c9"/><stop offset="1" stop-color="{col}" stop-opacity=".55"/></radialGradient>'
    b=(f'<circle cx="80" cy="80" r="76" fill="url(#gold)" stroke="{LINE}" stroke-width="4"/><circle cx="80" cy="80" r="65" fill="#fff0c9" stroke="{LINE}" stroke-width="3"/><circle cx="80" cy="80" r="65" fill="url(#mb)"/>'
       f'<g transform="translate(35 33) scale(.92)">{inner}</g>')
    svg(f'icon-{n}-lg.svg',160,160,b,d)
print('icons ok')
