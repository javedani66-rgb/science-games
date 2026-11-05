#!/usr/bin/env python3
"""مولد شخصیت‌ها (v5/team/assets/character). اجرا: python3 gen_char.py
خروجی: char_b1..b8.svg، sprite_char.svg، char.css (کلاس‌های حالت/ژست/اندازه)، char_palette.json، assets.json.
حالت و ژست با CSS variable (از مرز <use> رد می‌شود): --s-happy|thinking|surprised|oops|calm، --p-stand|walk1|walk2|jump|point|sit،
اندازه: --ow (خط بیرونی)، --iw (خط داخلی)، --det (none = فرم ساده بدون گوش/گونه/خط داخلی)."""
import json, pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'character'
LINE = '#241a5e'; EYE = '#3a2016'; MOUTH = '#7a1f3a'; TONGUE = '#ef7f8e'; TEETH = '#fff6e8'; CHEEK = '#f08a7a'
CREAM = '#fff4d2'; DARK = '#0d0426'
STATES = ['happy', 'thinking', 'surprised', 'oops']

def n(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def disp(kind, name, default):  # نمایش با CSS var
    return f'style="display:var(--{kind}-{name},{default})"'

CH = {
 'b1': dict(full=True, body='full', hr=(30,28), skin='#c98a5e', top='#2fb8a8', trim=CREAM, hair='#5a2e1a', brow='#5a2e1a', eyes='open', hat='hard', pant='#3a4a7a', back='ponytail', front='bangs', prop='pencil'),
 'b2': dict(skin='#7a4c34', top='#9153da', trim=CREAM, hair='#1b1220', brow='#1b1220', eyes='arc', back=None, front='curls', hat=None, body='hoodie', hr=(31,27), feat=DARK),
 'b3': dict(skin='#e8b48a', top='#b946a6', trim=CREAM, hair='#e0782a', brow='#b85a14', eyes='arc', back='buns', front='fringe', hat='glasses', body='pinafore', hr=(29,29)),
 'b4': dict(skin='#8d5a3c', top='#2f7bd6', trim=CREAM, hair='#6a4128', brow='#4a2c18', eyes='arc', back=None, front='spikes', hat='goggles', body='vest', hr=(30,26), feat=DARK),
 'b5': dict(skin='#c98a5e', top='#d070c0', trim=CREAM, hair='#b9783a', brow='#8a5424', eyes='arc', back='pigtails', front='fringe', hat=None, body='scarf', hr=(28,29)),
 'b6': dict(skin='#e8b48a', top='#fff4d2', trim='#1f6f78', hair='#e0782a', brow='#b85a14', eyes='open', back=None, front='tuft', hat='cap', freckles=True, body='jacket', hr=(31,28)),
 'b7': dict(skin='#8d5a3c', top='#24808a', trim=CREAM, hair='#1b1220', brow='#1b1220', eyes='open', back='braid', front='fringe', hat='bandana', body='work', hr=(29,27), feat=DARK),
 'b8': dict(skin='#7a4c34', top='#fff4d2', trim='#2f7bd6', hair='#1b1220', brow='#1b1220', eyes='arc', back=None, front='bun', hat='goggles2', calm=True, body='lab', hr=(28,28), feat=DARK),
}
def shade(hexc, f=0.82):
    h = hexc.lstrip('#'); r, g, b = [int(h[i:i+2], 16) for i in (0, 2, 4)]
    return '#%02x%02x%02x' % (int(r*f), int(g*f*0.98), int(b*f*1.04 if f < 1 else b))

class Ctx:
    def __init__(s, cid, c, cy, H, ow, iw):
        s.id, s.c, s.cy, s.H, s.ow, s.iw = cid, c, cy, H, ow, iw; s.hr = c.get('hr', (30, 28))
    def L(s, name): return f'{s.id}-{name}'
OW = 'stroke-width:var(--ow,%s)'; IW = 'stroke-width:var(--iw,%s)'

def g(ctx, name, body, extra='', st=''):
    return f'<g id="{ctx.L(name)}" {extra} {st}>{body}</g>'

def ow(ctx): return f'style="stroke:{LINE};stroke-width:var(--ow,{n(ctx.ow)})"'
def iw(ctx): return f'stroke="{ctx.c.get("feat", LINE)}" style="stroke-width:var(--iw,{n(ctx.iw)})"'

def face_layers(x, cx=50):
    """x: Ctx. برمی‌گرداند dict از لایه‌ها."""
    c, cy = x.c, x.cy
    HR = x.hr
    ey, my = cy + 2, cy + 17
    L = {}
    # eyes
    def sclera(px, py, rx, ry, pdx, pdy, pr):
        return (f'<ellipse cx="{n(px)}" cy="{n(py)}" rx="{rx}" ry="{ry}" fill="#fff" {iw(x)}/>'
                f'<circle cx="{n(px+pdx)}" cy="{n(py+pdy)}" r="{pr}" fill="{EYE}"/>'
                f'<circle cx="{n(px+pdx-1)}" cy="{n(py+pdy-1.2)}" r="1.1" fill="#fff"/>')
    def arc(px, py): return f'<path d="M{n(px-6)} {n(py+2)}Q{n(px)} {n(py-6)} {n(px+6)} {n(py+2)}" fill="none" stroke="{x.c.get('feat', LINE)}" style="stroke-width:var(--ow2,3.4)"/>'
    xs = (38.5, 61.5)
    ev = {}
    for st in STATES + ['calm']:
        if st == 'happy' and c['eyes'] == 'arc': ev[st] = ''.join(arc(px, ey) for px in xs)
        elif st == 'calm': ev[st] = ''.join(f'<path d="M{n(px-5.5)} {n(ey+1)}Q{n(px)} {n(ey-4)} {n(px+5.5)} {n(ey+1)}" fill="none" stroke="{x.c.get('feat', LINE)}" style="stroke-width:var(--ow2,3.4)"/>' for px in xs)
        else:
            rx, ry, pdx, pdy, pr = {'happy': (6.2, 6.6, 0, .6, 3.5), 'thinking': (6.2, 6.6, 2.6, -2.8, 3.5),
                                    'surprised': (7.4, 8.2, 0, 0, 2.3), 'oops': (6.2, 6.6, -3, 1.4, 3.5)}[st]
            ev[st] = ''.join(sclera(px, ey, rx, ry, pdx, pdy, pr) for px in xs)
    # brows (قوسِ ضخیم‌تر؛ در فرم ساده هم می‌مانند چون حالت را می‌رسانند)
    by = cy - 9
    bv = {'happy': (f'M31 {n(by)}Q38 {n(by-5)} 46 {n(by)}', f'M54 {n(by)}Q62 {n(by-5)} 69 {n(by)}'),
          'thinking': (f'M31 {n(by-3)}Q38 {n(by-8)} 46 {n(by-3)}', f'M54 {n(by+1)}L69 {n(by-1)}'),
          'surprised': (f'M31 {n(by-6)}Q38 {n(by-11)} 46 {n(by-6)}', f'M54 {n(by-6)}Q62 {n(by-11)} 69 {n(by-6)}'),
          'oops': (f'M31 {n(by+1)}L46 {n(by-4)}', f'M54 {n(by-4)}L69 {n(by+1)}'),
          'calm': (f'M32 {n(by)}L45 {n(by)}', f'M55 {n(by)}L68 {n(by)}')}
    bc = c['brow']
    # mouth
    mv = {
     'happy': (f'<path d="M37 {n(my)}Q50 {n(my+3)} 63 {n(my)}Q59 {n(my+16)} 50 {n(my+16)}Q41 {n(my+16)} 37 {n(my)}Z" fill="{MOUTH}" {iw(x)}/>'
               f'<path d="M40 {n(my+.6)}Q50 {n(my+3.4)} 60 {n(my+.6)}L59 {n(my+4.6)}Q50 {n(my+6.6)} 41 {n(my+4.6)}Z" fill="{TEETH}"/>'
               f'<ellipse cx="50" cy="{n(my+12)}" rx="5" ry="2.6" fill="{TONGUE}"/>'),
     'thinking': f'<path d="M41 {n(my+4)}Q49 {n(my+7)} 54 {n(my+4.5)}Q58 {n(my+2.5)} 61 {n(my-.5)}" fill="none" stroke="{x.c.get('feat', LINE)}" style="stroke-width:var(--ow2,3.4)"/>',
     'surprised': f'<ellipse cx="50" cy="{n(my+5)}" rx="4.4" ry="5.6" fill="{MOUTH}" {iw(x)}/>',
     'oops': f'<path d="M40 {n(my+7)}Q44 {n(my+3)} 48 {n(my+7)}T56 {n(my+7)}T60 {n(my+6)}" fill="none" stroke="{x.c.get('feat', LINE)}" style="stroke-width:var(--ow2,3.4)"/>',
     'calm': f'<path d="M42 {n(my+3)}Q50 {n(my+8)} 58 {n(my+3)}" fill="none" stroke="{x.c.get('feat', LINE)}" style="stroke-width:var(--ow2,3.4)"/>'}
    sts = STATES + (['calm'] if c.get('calm') else [])
    for st in sts:
        dflt = 'inline' if st == 'happy' else 'none'
        L[f'eyes-{st}'] = g(x, f'eyes-{st}', ev[st], st=disp('s', st, dflt))
        L[f'brows-{st}'] = g(x, f'brows-{st}', f'<path d="{bv[st][0]}M{bv[st][1][1:]}" fill="none" stroke="{bc}" style="stroke-width:var(--bw,3.6)"/>', st=disp('s', st, dflt))
        L[f'mouth-{st}'] = g(x, f'mouth-{st}', mv[st], st=disp('s', st, dflt))
    L['sweat'] = g(x, 'sweat', f'<path d="M74 {n(cy-12)}Q70 {n(cy-5)} 74 {n(cy-2)}Q78 {n(cy-5)} 74 {n(cy-12)}Z" fill="#6ab7d8" {iw(x)}/>', st=disp('s', 'oops', 'none'))
    return L

def hair_front(x):
    c, cy = x.c, x.cy; hc = c['hair']; k = c['front']; i = f'{x.id}-hf'
    # اشکال سیلوئت به‌صورت defs و <use> دو‌گذره (خط دورِ یکپارچه با ادغام شکل‌ها)
    if k == 'bangs': d = f'M21 {n(cy-6)}Q38 {n(cy-20)} 50 {n(cy-8)}Q62 {n(cy-20)} 79 {n(cy-6)}L79 {n(cy-16)}L21 {n(cy-16)}Z'
    elif k == 'fringe': d = f'M20 {n(cy-4)}Q22 {n(cy-30)} 50 {n(cy-31)}Q78 {n(cy-30)} 80 {n(cy-4)}Q70 {n(cy-18)} 56 {n(cy-12)}Q44 {n(cy-20)} 30 {n(cy-12)}Q24 {n(cy-10)} 20 {n(cy-4)}Z'
    elif k == 'curls':
        cs = [(22, cy-10, 9), (30, cy-22, 10), (42, cy-28, 10.5), (55, cy-29, 10.5), (67, cy-24, 10), (77, cy-14, 9), (24, cy+2, 6), (76, cy+2, 6)]
        d = ''.join(f'M{n(a-r)} {n(b)}a{r} {r} 0 1 0 {n(2*r)} 0a{r} {r} 0 1 0 {n(-2*r)} 0Z' for a, b, r in cs)
    elif k == 'spikes': d = f'M20 {n(cy-4)}L19 {n(cy-22)}L30 {n(cy-18)}L31 {n(cy-36)}L42 {n(cy-26)}L52 {n(cy-40)}L60 {n(cy-27)}L72 {n(cy-35)}L72 {n(cy-18)}L82 {n(cy-22)}L80 {n(cy-4)}Q70 {n(cy-17)} 50 {n(cy-16)}Q30 {n(cy-17)} 20 {n(cy-4)}Z'
    elif k == 'tuft': d = f'M24 {n(cy-6)}Q26 {n(cy-22)} 42 {n(cy-18)}Q36 {n(cy-10)} 24 {n(cy-6)}ZM76 {n(cy-6)}Q74 {n(cy-22)} 58 {n(cy-18)}Q64 {n(cy-10)} 76 {n(cy-6)}Z'
    elif k == 'bun': d = (f'M20 {n(cy-4)}Q20 {n(cy-32)} 50 {n(cy-32)}Q80 {n(cy-32)} 80 {n(cy-4)}Q70 {n(cy-20)} 50 {n(cy-18)}Q30 {n(cy-20)} 20 {n(cy-4)}Z'
                          f'M41 {n(cy-33)}a9 9 0 1 1 18 0a9 9 0 1 1 -18 0Z')
    else: d = ''
    return d

def hair_back(x):
    c, cy = x.c, x.cy; k = c['back']
    if k == 'ponytail': return f'M28 {n(cy-12)}C6 {n(cy-22)} -2 {n(cy+12)} 10 {n(cy+40)}C16 {n(cy+48)} 26 {n(cy+38)} 20 {n(cy+22)}Q26 {n(cy+4)} 28 {n(cy-12)}Z'
    if k == 'buns': return ''.join(f'M{n(a-10)} {n(cy-28)}a10 10 0 1 0 20 0a10 10 0 1 0 -20 0Z' for a in (22, 78))
    if k == 'pigtails': return ''.join(f'M{n(a-6)} {n(cy+4)}Q{n(a-12*s)} {n(cy+30)} {n(a-8*s)} {n(cy+42)}Q{n(a)} {n(cy+48)} {n(a+8*s)} {n(cy+38)}Q{n(a+10*s)} {n(cy+22)} {n(a+6)} {n(cy+4)}Z' for a, s in ((17, 1), (83, -1)))
    if k == 'braid': return f'M70 {n(cy+10)}Q92 {n(cy+20)} 86 {n(cy+44)}Q82 {n(cy+52)} 76 {n(cy+46)}Q82 {n(cy+30)} 66 {n(cy+22)}Z'
    return ''

def headgear(x):
    c, cy = x.c, x.cy; k = c.get('hat'); i = x.id
    ol = ow(x); il = iw(x)
    if k == 'hard':
        return (f'<path d="M17 {n(cy-6)}Q15 {n(cy-40)} 50 {n(cy-41)}Q85 {n(cy-40)} 83 {n(cy-6)}Z" fill="#f5c518" {ol}/>'
                f'<path d="M44 {n(cy-40.5)}H56V{n(cy-7)}H44Z" fill="#ffe680" {il}/>'
                f'<path d="M12 {n(cy-6)}Q50 {n(cy-13)} 88 {n(cy-6)}L88 {n(cy-1)}Q50 {n(cy-8)} 12 {n(cy-1)}Z" fill="#d49a0a" {ol}/>'
                f'<path d="M24 {n(cy-24)}Q27 {n(cy-33)} 36 {n(cy-35)}" fill="none" stroke="#ffe680" style="stroke-width:3.2;stroke-linecap:round;display:var(--det,inline)"/>')
    if k == 'glasses':
        return (f'<circle cx="38.5" cy="{n(cy+2)}" r="10.5" fill="#d6f1f2" fill-opacity=".35" {ol}/><circle cx="61.5" cy="{n(cy+2)}" r="10.5" fill="#d6f1f2" fill-opacity=".35" {ol}/>'
                f'<path d="M49 {n(cy+1)}Q50 {n(cy-1)} 51 {n(cy+1)}" fill="none" {il}/>')
    if k == 'goggles':   # b4: عینک ایمنی بالای پیشانی
        return (f'<path d="M19 {n(cy-12)}H81" stroke="#4a5a7a" style="stroke-width:7;stroke-linecap:round"/>'
                f'<rect x="26" y="{n(cy-26)}" width="21" height="14" rx="6" fill="#bfe6f5" {ol}/><rect x="53" y="{n(cy-26)}" width="21" height="14" rx="6" fill="#bfe6f5" {ol}/>')
    if k == 'goggles2':  # b8
        return (f'<path d="M17 {n(cy-13)}H83" stroke="#8a93a8" style="stroke-width:8;stroke-linecap:round"/>'
                f'<rect x="24" y="{n(cy-26)}" width="23" height="15" rx="6" fill="#d6f1f2" {ol}/><rect x="53" y="{n(cy-26)}" width="23" height="15" rx="6" fill="#d6f1f2" {ol}/>')
    if k == 'cap':
        return (f'<path d="M17 {n(cy-6)}Q16 {n(cy-38)} 50 {n(cy-38)}Q84 {n(cy-38)} 83 {n(cy-6)}Q50 {n(cy-14)} 17 {n(cy-6)}Z" fill="#1f6f78" {ol}/>'
                f'<path d="M18 {n(cy-7)}Q50 {n(cy-16)} 82 {n(cy-7)}Q92 {n(cy-6)} 90 {n(cy-1)}Q50 {n(cy-10)} 12 {n(cy-1)}Q10 {n(cy-6)} 18 {n(cy-7)}Z" fill="#175862" {ol}/>'
                f'<circle cx="50" cy="{n(cy-38)}" r="3.2" fill="#175862" {il}/>')
    if k == 'bandana':
        return (f'<path d="M18 {n(cy-6)}Q20 {n(cy-34)} 50 {n(cy-35)}Q80 {n(cy-34)} 82 {n(cy-6)}Q50 {n(cy-18)} 18 {n(cy-6)}Z" fill="#d070c0" {ol}/>'
                f'<path d="M80 {n(cy-18)}L94 {n(cy-30)}L96 {n(cy-12)}Z" fill="#d070c0" {ol}/>'
                f'<g fill="{CREAM}" style="display:var(--det,inline)"><circle cx="34" cy="{n(cy-18)}" r="2.4"/><circle cx="50" cy="{n(cy-24)}" r="2.4"/><circle cx="66" cy="{n(cy-18)}" r="2.4"/></g>')
    return ''

BASE_SH = 'M6 100Q8 76 30 72L70 72Q92 76 94 100Z'
def torso_bust(x):
    """برمی‌گرداند (svg، مسیر سیلوئت). هر شخصیت بدن/یقهٔ متمایز دارد."""
    c = x.c; k = c.get('body'); T, R = c['top'], c['trim']; O, I = ow(x), iw(x)
    L = f'stroke="{LINE}" style="stroke-width:var(--iw,{n(x.iw)})"'
    if k == 'hoodie':
        sh = 'M3 100Q3 74 28 70L72 70Q97 74 97 100Z'
        hood = f'<path d="M26 76Q26 54 50 54Q74 54 74 76Z" fill="{shade(T, .8)}" {O}/>'
        return (hood + f'<path d="{sh}" fill="{T}" {O}/><path d="M33 71Q50 92 67 71" fill="{shade(T,.8)}" {L}/>'
                f'<path d="M44 82V96M56 82V96" stroke="{R}" style="stroke-width:3.2;stroke-linecap:round;display:var(--det,inline)"/>'), sh + 'M26 76Q26 54 50 54Q74 54 74 76Z'
    if k == 'pinafore':
        return (f'<path d="{BASE_SH}" fill="{R}" {O}/><path d="M30 100L34 84H66L70 100Z" fill="{T}" {O}/>'
                f'<path d="M34 84L38 72M66 84L62 72" stroke="{T}" style="stroke-width:6;stroke-linecap:round"/>'
                f'<path d="M34 72Q50 90 66 72" fill="{R}" {L}/>'), BASE_SH
    if k == 'vest':
        return (f'<path d="{BASE_SH}" fill="{R}" {O}/><path d="M8 100Q9 78 30 72L40 72L45 100Z" fill="{T}" {O}/><path d="M92 100Q91 78 70 72L60 72L55 100Z" fill="{T}" {O}/>'
                f'<path d="M38 72L50 86L62 72" fill="{R}" {L}/>'), BASE_SH
    if k == 'scarf':
        return (f'<path d="{BASE_SH}" fill="{T}" {O}/><path d="M60 88L70 100H56L53 90Z" fill="#2f7bd6" {I.replace("stroke=", "stroke=")}/>'
                f'<path d="M27 74Q50 92 73 74L75 86Q50 102 25 86Z" fill="#2f7bd6" {O}/>'
                f'<path d="M36 82L33 92M50 87V98M64 82L67 92" stroke="{CREAM}" style="stroke-width:3;stroke-linecap:round;display:var(--det,inline)"/>'), BASE_SH
    if k == 'jacket':
        return (f'<path d="{BASE_SH}" fill="{T}" {O}/><path d="M32 72L46 94L52 72Z" fill="{R}" {L}/><path d="M68 72L54 94L48 72Z" fill="{R}" {L}/>'
                f'<path d="M50 94V100" stroke="{R}" style="stroke-width:3;display:var(--det,inline)"/>'), BASE_SH
    if k == 'work':
        return (f'<path d="{BASE_SH}" fill="{T}" {O}/><path d="M36 72L47 85L33 83Z" fill="{R}" {L}/><path d="M64 72L53 85L67 83Z" fill="{R}" {L}/>'
                f'<g style="display:var(--det,inline)"><rect x="60" y="88" width="14" height="11" rx="2" fill="{shade(T,.85)}" {L}/><path d="M66 84V91" stroke="{R}" style="stroke-width:2.6;stroke-linecap:round"/></g>'), BASE_SH
    if k == 'lab':
        return (f'<path d="{BASE_SH}" fill="{R}" {O}/><path d="M6 100Q8 76 30 72L43 72L49 100Z" fill="{T}" {O}/><path d="M94 100Q92 76 70 72L57 72L51 100Z" fill="{T}" {O}/>'
                f'<path d="M30 92V99" stroke="#2f7bd6" style="stroke-width:3;stroke-linecap:round;display:var(--det,inline)"/>'), BASE_SH
    return (f'<path d="{BASE_SH}" fill="{T}" {O}/><path d="M34 72L50 90L66 72" fill="{R}" {L}/>'), BASE_SH

def head_shapes(x):
    cy = x.cy; HR = x.hr
    return (f'<ellipse cx="50" cy="{n(cy)}" rx="{HR[0]}" ry="{HR[1]}"/>')

def build(cid_name, c):
    full = c.get('full', False)
    H = 150 if full else 100
    cy = 40 if full else 44
    ow_def = 6.2 if full else 5.5     # خط بیرونی بر حسب واحد viewBox برای اندازهٔ پایهٔ نمایش (b1 ≈110px، سرشانه ≈82px)
    iw_def = 3.6 if full else 3.2
    x = Ctx('ch-' + cid_name, c, cy, H, ow_def, iw_def); HR = x.hr
    skin, sk2 = c['skin'], shade(c['skin'])
    parts = []
    defs = []
    # سیلوئت برای rim/shade (یک شکل = سر + تن + کلاه/مو)
    # --- لایه‌ها به ترتیب نقاشی
    if full:
        parts.append(g(x, 'shadow', f'<ellipse cx="50" cy="146" rx="26" ry="4.2" fill="#10083a" fill-opacity=".28" style="display:var(--p-jump,none)"/>'
                       f'<ellipse cx="50" cy="146" rx="32" ry="5" fill="#10083a" fill-opacity=".28" style="display:var(--p-nojump,inline)"/>'))
    halo = f'<g fill="{CREAM}" stroke="{CREAM}" style="stroke-width:calc(var(--ow,{n(ow_def)}) + 4);stroke-linejoin:round"><use href="#{x.L("sil")}"/></g>'
    if full: halo += poses_halo(x)
    parts.append(g(x, 'halo', halo, st='style="display:var(--halo,none)"'))
    hb = hair_back(x)
    if hb:
        parts.append(g(x, 'body-back', f'<path d="{hb}" fill="{c["hair"]}" {ow(x)}/>'))
    if full:
        parts += poses(x)
        parts.append(g(x, 'torso', torso_full(x)))
    else:
        tb, tsil = torso_bust(x); parts.append(g(x, 'torso', tb))
    parts.append(g(x, 'neck', f'<path d="M41 {n(cy+22)}H59V{n(cy+36 if full else 80)}H41Z" fill="{sk2}" {ow(x)}/>'))
    parts.append(g(x, 'ear', f'<circle cx="{n(50-HR[0]+.5)}" cy="{n(cy+3)}" r="6" fill="{skin}" {ow(x)}/><circle cx="{n(50+HR[0]-.5)}" cy="{n(cy+3)}" r="6" fill="{skin}" {ow(x)}/>'
                   f'<path d="M19 {n(cy+1)}Q21 {n(cy+3)} 19 {n(cy+6)}M81 {n(cy+1)}Q79 {n(cy+3)} 81 {n(cy+6)}" fill="none" {iw(x)}/>', st='style="display:var(--det,inline)"'))
    parts.append(g(x, 'head', f'<ellipse cx="50" cy="{n(cy)}" rx="{HR[0]}" ry="{HR[1]}" fill="{skin}" {ow(x)}/>'))
    parts.append(g(x, 'face-shade', f'<path d="M24 {n(cy+14)}Q50 {n(cy+40)} 76 {n(cy+14)}Q72 {n(cy+28)} 50 {n(cy+28)}Q30 {n(cy+28)} 24 {n(cy+14)}Z" fill="{sk2}" fill-opacity=".55" clip-path="url(#{x.L("hclip")})"/>'))
    defs.append(f'<clipPath id="{x.L("hclip")}"><ellipse cx="50" cy="{n(cy)}" rx="{HR[0]}" ry="{HR[1]}"/></clipPath>')
    F = face_layers(x)
    for k in F: parts.append(F[k])
    parts.append(g(x, 'cheeks', f'<circle cx="31" cy="{n(cy+14)}" r="4.6" fill="{CHEEK}" fill-opacity=".5"/><circle cx="69" cy="{n(cy+14)}" r="4.6" fill="{CHEEK}" fill-opacity=".5"/>'
                   + (''.join(f'<circle cx="{a}" cy="{n(cy+b)}" r="1.1" fill="#b85a14"/>' for a, b in ((35, 11), (39, 13), (61, 13), (65, 11))) if c.get('freckles') else ''),
                   st='style="display:var(--det,inline)"'))
    parts.append(g(x, 'nose', f'<path d="M48.5 {n(cy+8)}Q51 {n(cy+11)} 53.5 {n(cy+9)}" fill="none" {iw(x)}/>', st='style="display:var(--det,inline)"'))
    hf = hair_front(x)
    if hf:
        parts.append(g(x, 'hair-front', f'<path d="{hf}" fill="{c["hair"]}" {ow(x)}/>'))
    hg = headgear(x)
    if hg: parts.append(g(x, 'hat', hg))
    if c.get('prop') == 'pencil':
        parts.append(g(x, 'prop', f'<path d="M23 {n(cy-1)}L15 {n(cy+17)}" stroke="{LINE}" style="stroke-width:7.5;stroke-linecap:round"/><path d="M23 {n(cy-1)}L15 {n(cy+17)}" stroke="#ffe680" style="stroke-width:4;stroke-linecap:round"/><circle cx="23.6" cy="{n(cy-2.4)}" r="2.6" fill="#d070c0"/>', st='style="display:var(--det,inline)"'))
    # سایهٔ جهت‌دار و rim (متغیر light؛ نور بالا-چپ): هلالِ ماسک‌شده روی سیلوئت
    sil = []
    sil.append(sil_shapes(x, tsil if not full else None))
    sid = x.L('sil')
    defs.append(f'<g id="{sid}">{"".join(sil)}</g>')
    defs.append(f'<mask id="{x.L("mshade")}"><use href="#{sid}" fill="#fff"/><use href="#{sid}" fill="#000" transform="translate(-5 -5)"/></mask>'
                f'<mask id="{x.L("mrim")}"><use href="#{sid}" fill="#fff"/><use href="#{sid}" fill="#000" transform="translate(3.6 3.6)"/></mask>')
    parts.append(g(x, 'shade', f'<rect width="100" height="{H}" fill="var(--l-shade,#4a3a8c)" fill-opacity="var(--l-shade-a,.22)" mask="url(#{x.L("mshade")})"/>'))
    parts.append(g(x, 'lit', f'<rect width="100" height="{H}" fill="var(--l-lit,#fff4cf)" fill-opacity="var(--l-lit-a,.4)" mask="url(#{x.L("mrim")})"/>'))
    body = f'<defs>{"".join(defs)}</defs>' + '\n'.join(parts)
    return x, H, body

def sil_shapes(x, tsil=None):
    """سیلوئت واقعی (سر، گوش، موی پشت/جلو، کلاه، تن؛ b1 با پاها در halo ژست‌ها)."""
    c, cy = x.c, x.cy; HR = x.hr; s = f'<ellipse cx="50" cy="{n(cy)}" rx="{HR[0]}" ry="{HR[1]}"/>'
    s += f'<circle cx="{n(50-HR[0]+.5)}" cy="{n(cy+3)}" r="6"/><circle cx="{n(50+HR[0]-.5)}" cy="{n(cy+3)}" r="6"/>'
    if c.get('full'): s += f'<path d="M26 {n(cy+34)}Q27 {n(cy+29)} 40 {n(cy+29)}L60 {n(cy+29)}Q73 {n(cy+29)} 74 {n(cy+34)}L76 {n(cy+82)}H24Z"/>'
    else: s += f'<path d="{tsil or BASE_SH}"/>'
    for d in (hair_back(x), hair_front(x)):
        if d: s += f'<path d="{d}"/>'
    if c.get('hat') in ('hard', 'cap', 'bandana'):
        s += f'<path d="M17 {n(cy-6)}Q15 {n(cy-41)} 50 {n(cy-41)}Q85 {n(cy-41)} 83 {n(cy-6)}Z"/>'
    if c.get('hat') == 'bandana': s += f'<path d="M80 {n(cy-18)}L94 {n(cy-30)}L96 {n(cy-12)}Z"/>'
    if c.get('hat') in ('goggles', 'goggles2'): s += f'<rect x="24" y="{n(cy-27)}" width="52" height="16" rx="7"/>'
    return s

def torso_full(x):
    c = x.c; cy = x.cy; t = cy + 30  # y بالای شانه ≈ 70
    return (f'<path d="M26 {n(t+4)}Q27 {n(t-1)} 40 {n(t-1)}L60 {n(t-1)}Q73 {n(t-1)} 74 {n(t+4)}L76 {n(t+44)}Q50 {n(t+50)} 24 {n(t+44)}Z" fill="{c["top"]}" {ow(x)}/>'
            f'<path d="M37 {n(t-1)}L50 {n(t+14)}L63 {n(t-1)}" fill="{c["trim"]}" {iw(x)}/>'
            f'<path d="M36 {n(t+20)}V{n(t+47)}M64 {n(t+20)}V{n(t+47)}" stroke="{c["trim"]}" style="stroke-width:5;stroke-linecap:round;display:var(--det,inline)"/>'
            f'<path d="M22 {n(t+44)}H78V{n(t+52)}H22Z" fill="#3a4a7a" {ow(x)}/>')

def limb(x, pts, w, col, cap_col=None):
    d = 'M' + 'L'.join(f'{n(a)} {n(b)}' for a, b in pts)
    return (f'<path d="{d}" fill="none" stroke="{LINE}" style="stroke-width:calc({w} + var(--ow,{n(x.ow)}));stroke-linecap:round;stroke-linejoin:round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

def arm(x, sh, el, hd, side):
    c = x.c
    return (limb(x, [sh, el], 11, c['top']) + limb(x, [el, hd], 9.5, c['skin']) +
            f'<circle cx="{n(hd[0])}" cy="{n(hd[1])}" r="6" fill="{c["skin"]}" stroke="{LINE}" style="stroke-width:var(--iw,{n(x.iw)})"/>')

def leg(x, hip, kn, ft, side):
    c = x.c
    return (limb(x, [hip, kn], 12, c['pant']) + limb(x, [kn, ft], 11, c['pant']) +
            f'<path d="M{n(ft[0]-7)} {n(ft[1])}Q{n(ft[0]-8)} {n(ft[1]-5)} {n(ft[0])} {n(ft[1]-5)}Q{n(ft[0]+9)} {n(ft[1]-5)} {n(ft[0]+8)} {n(ft[1]+1)}Z" fill="#5a2e1a" stroke="{LINE}" style="stroke-width:var(--iw,{n(x.iw)})"/>')

POSE_P = {
 'stand': dict(
    al=[(30, 76), (21, 94), (22, 110)], ar=[(70, 76), (79, 94), (78, 110)],
    ll=[(40, 118), (39, 132), (38, 142)], lr=[(60, 118), (61, 132), (62, 142)]),
 'walk1': dict(
    al=[(30, 76), (26, 94), (36, 108)], ar=[(70, 76), (74, 94), (66, 82 + 12)],
    ll=[(40, 118), (34, 132), (24, 141)], lr=[(60, 118), (64, 130), (70, 142)]),
 'walk2': dict(
    al=[(30, 76), (26, 94), (34, 84 + 12)], ar=[(70, 76), (76, 94), (68, 108)],
    ll=[(40, 118), (36, 130), (30, 142)], lr=[(60, 118), (66, 132), (76, 141)]),
 'jump': dict(
    al=[(30, 76), (16, 66), (10, 48)], ar=[(70, 76), (84, 66), (90, 48)],
    ll=[(40, 118), (30, 126), (36, 134)], lr=[(60, 118), (70, 126), (64, 134)]),
 'point': dict(
    al=[(30, 76), (14, 78), (-2, 76)], ar=[(70, 76), (79, 94), (78, 110)],
    ll=[(40, 118), (39, 132), (38, 142)], lr=[(60, 118), (61, 132), (62, 142)]),
 'sit': dict(
    al=[(30, 76), (24, 94), (36, 110)], ar=[(70, 76), (76, 94), (64, 110)],
    ll=[(40, 118), (26, 126), (22, 138)], lr=[(60, 118), (74, 126), (78, 138)]),
}

def _pl(pts): return 'M' + 'L'.join(f'{n(a)} {n(b)}' for a, b in pts)
def poses_halo(x):
    out = []
    for name, p in POSE_P.items():
        d = ''.join(f'<path d="{_pl(p[k])}"/>' for k in ('al', 'ar', 'll', 'lr')) + ''.join(f'<circle cx="{n(p[k][-1][0])}" cy="{n(p[k][-1][1])}" r="6" fill="{CREAM}"/>' for k in ('al', 'ar'))
        out.append(f'<g fill="none" stroke="{CREAM}" style="stroke-width:calc(11 + var(--ow,{n(x.ow)}) + 4);display:var(--p-{name},{"inline" if name == "stand" else "none"})">{d}</g>')
    return ''.join(out)

def poses(x):
    c = x.c; out = []; ft = '#5a2e1a'; IWs = f'stroke="{LINE}" style="stroke-width:var(--iw,{n(x.iw)})"'
    for name, p in POSE_P.items():
        dflt = 'inline' if name == 'stand' else 'none'
        o = ''.join(f'<path d="{_pl(p[k])}"/>' for k in ('al', 'ar', 'll', 'lr'))
        f = (f'<g stroke="{c["pant"]}">' + ''.join(f'<path d="{_pl(p[k])}"/>' for k in ('ll', 'lr')) + '</g>'
             f'<g stroke="{c["top"]}">' + ''.join(f'<path d="{_pl(p[k][:2])}"/>' for k in ('al', 'ar')) + '</g>'
             f'<g stroke="{c["skin"]}">' + ''.join(f'<path d="{_pl(p[k][1:])}"/>' for k in ('al', 'ar')) + '</g>')
        hands = ''.join(f'<circle cx="{n(p[k][-1][0])}" cy="{n(p[k][-1][1])}" r="6"/>' for k in ('al', 'ar'))
        shoes = ''.join(f'<path d="M{n(p[k][-1][0]-7)} {n(p[k][-1][1])}Q{n(p[k][-1][0]-8)} {n(p[k][-1][1]-5)} {n(p[k][-1][0])} {n(p[k][-1][1]-5)}Q{n(p[k][-1][0]+9)} {n(p[k][-1][1]-5)} {n(p[k][-1][0]+8)} {n(p[k][-1][1]+1)}Z"/>' for k in ('ll', 'lr'))
        body = (f'<g fill="none" stroke="{LINE}" style="stroke-width:calc(11 + var(--ow,{n(x.ow)}))">{o}</g>'
                f'<g fill="none" stroke-width="11">{f}</g>'
                f'<g fill="{c["skin"]}" {IWs}>{hands}</g><g fill="{ft}" {IWs}>{shoes}</g>')
        out.append(g(x, f'pose-{name}', body, st=disp('p', name, dflt)))
    return out

CSS = """/* حالت: <use class="ch-happy"> ؛ ژست (فقط b1): ch-pose-walk1 …؛ اندازه: cs-bust-82 …. متغیرها از مرز <use> رد می‌شوند. */
.ch-happy{--s-happy:inline;--s-thinking:none;--s-surprised:none;--s-oops:none;--s-calm:none}
.ch-thinking{--s-happy:none;--s-thinking:inline;--s-surprised:none;--s-oops:none;--s-calm:none}
.ch-surprised{--s-happy:none;--s-thinking:none;--s-surprised:inline;--s-oops:none;--s-calm:none}
.ch-oops{--s-happy:none;--s-thinking:none;--s-surprised:none;--s-oops:inline;--s-calm:none}
.ch-calm{--s-happy:none;--s-thinking:none;--s-surprised:none;--s-oops:none;--s-calm:inline}
.ch-pose-stand{--p-stand:inline;--p-walk1:none;--p-walk2:none;--p-jump:none;--p-point:none;--p-sit:none;--p-nojump:inline}
.ch-pose-walk1{--p-stand:none;--p-walk1:inline;--p-walk2:none;--p-jump:none;--p-point:none;--p-sit:none;--p-nojump:inline}
.ch-pose-walk2{--p-stand:none;--p-walk1:none;--p-walk2:inline;--p-jump:none;--p-point:none;--p-sit:none;--p-nojump:inline}
.ch-pose-jump{--p-stand:none;--p-walk1:none;--p-walk2:none;--p-jump:inline;--p-point:none;--p-sit:none;--p-nojump:none}
.ch-pose-point{--p-stand:none;--p-walk1:none;--p-walk2:none;--p-jump:none;--p-point:inline;--p-sit:none;--p-nojump:inline}
.ch-pose-sit{--p-stand:none;--p-walk1:none;--p-walk2:none;--p-jump:none;--p-point:none;--p-sit:inline;--p-nojump:inline}
/* اندازه: خط بیرونی/داخلی بر حسب واحد viewBox = px×H/اندازهٔ نمایش (جدول ۲-ج). سرشانه H=100، b1 تمام‌قد H=150 */
.cs-bust-140{--ow:3.2;--iw:1.9;--ow2:2.6;--bw:2.4}
.cs-bust-82{--ow:5.5;--iw:3.2;--ow2:3.4;--bw:3.6}
.cs-bust-64{--ow:5.5;--iw:3.1;--ow2:3.4;--bw:3.6}
.cs-bust-56{--ow:5.4;--iw:0;--ow2:5.4;--bw:5.4;--det:none}
.cs-full-140{--ow:4.8;--iw:2.8;--ow2:3.0;--bw:3.0}
.cs-full-110{--ow:6.1;--iw:3.5;--ow2:3.4;--bw:3.6}
.cs-full-82{--ow:8.2;--iw:4.7;--ow2:4.4;--bw:4.4}
"""

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    symbols = []; meta = {}; pal = {}
    for name, c in CH.items():
        x, H, body = build(name, c)
        full = c.get('full', False)
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 {H}" style="stroke-linejoin:round;stroke-linecap:round">{body}</svg>'
        # در فایل مستقل پیش‌فرض‌ها (var fallback) کافی است
        (OUT / f'char_{name}.svg').write_text(svg, encoding='utf-8')
        symbols.append(f'<symbol id="ch-{name}" viewBox="0 0 100 {H}" style="stroke-linejoin:round;stroke-linecap:round">{body}</symbol>')
        layers = __import__('re').findall(r'<g id="([^"]+)"', body)
        meta[f'ch-{name}'] = dict(file=f'char_{name}.svg', viewBox=f'0 0 100 {H}', anchor='bottom-center' if full else 'bust-bottom-center',
                                   bytes=len(svg.encode()), states=STATES + (['calm'] if c.get('calm') else []), poses=['stand', 'walk1', 'walk2', 'jump', 'point', 'sit'] if full else [], layers=layers)
        pal[name] = {k: v for k, v in c.items() if isinstance(v, str) and v.startswith('#')}
        pal[name]['top_hue_ok'] = True
    (OUT / 'sprite_char.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">' + ''.join(symbols) + '</svg>', encoding='utf-8')
    (OUT / 'char.css').write_text(CSS, encoding='utf-8')
    (OUT / 'char_palette.json').write_text(json.dumps(pal, ensure_ascii=False, indent=1), encoding='utf-8')
    (OUT / 'assets.json').write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding='utf-8')
    for k, v in meta.items(): print(k, v['bytes'])

if __name__ == '__main__': main()
