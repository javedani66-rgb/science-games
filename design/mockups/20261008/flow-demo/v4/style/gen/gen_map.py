# نقشهٔ روز v4 (دور ۲): ریسمان درس = ورزشگاه، پایگاه فضایی، مزرعه، شهر صنعتی
from gen_head import *
import gen_head as H
HERE_K = H.HERE_K

defs = '''
<filter id="wob" x="-15%" y="-15%" width="130%" height="130%"><feTurbulence type="fractalNoise" baseFrequency=".045" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.4"/></filter>
<filter id="zone" filterUnits="userSpaceOnUse" x="-200" y="-200" width="790" height="2800"><feTurbulence type="fractalNoise" baseFrequency=".007 .011" numOctaves="2" seed="11" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="60" result="d"/><feGaussianBlur in="d" stdDeviation="30"/></filter>
<filter id="hard" filterUnits="userSpaceOnUse" x="-200" y="-200" width="790" height="2800"><feTurbulence type="fractalNoise" baseFrequency=".012 .02" numOctaves="3" seed="5" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="26" result="d"/><feGaussianBlur in="d" stdDeviation="1.6"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="1" seed="2"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .07 0"/></filter>
<linearGradient id="vig" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#10083a" stop-opacity=".3"/><stop offset=".06" stop-color="#10083a" stop-opacity="0"/><stop offset=".95" stop-color="#10083a" stop-opacity="0"/><stop offset="1" stop-color="#10083a" stop-opacity=".3"/></linearGradient>
'''.replace('\\\\', '')
def wavy_top(y, amp=18, seed=0):
    r = random.Random(seed); d = 'M-200,%d' % (y); x = -200
    while x < 590:
        d += ' L%d,%d' % (x, y + r.uniform(-amp, amp)); x += 40
    return d + ' L590,-300 L-200,-300 Z'

svg = ['<svg id="map" xmlns="http://www.w3.org/2000/svg" width="390" height="2400" viewBox="0 0 390 2400"><defs>%s</defs>' % defs]
# ۱) زمین: چمن پایین؛ مرز زمین‌ها گرادیان نرم؛ آب/خشکی تیز با ساحل شنی
svg.append('<rect width="390" height="2400" fill="%s"/>' % Z['grass'])
svg.append('<g filter="url(#zone)"><path d="%s" fill="%s"/><path d="%s" fill="%s"/></g>' % (wavy_top(1790, 6, 1), Z['space'], wavy_top(1215, 6, 2), Z['farm']))
svg.append('<g filter="url(#hard)"><path d="%s" fill="#f0cf7a"/><path d="%s" fill="%s"/></g>' % (wavy_top(700, 5, 5), wavy_top(668, 5, 3), Z['sea']))
# لکهٔ یخ دور پیست (سفید روشن)
ix, iy = NODE[2]
svg.append('<g filter="url(#hard)"><ellipse cx="%d" cy="%d" rx="128" ry="56" fill="%s"/></g>' % (ix + 8, iy + 4, Z['ice']))
svg.append('<g opacity=".7" stroke="#fff" stroke-width="2" fill="none"><path d="M%d,%d l14,-8 l10,6 M%d,%d l12,8 l16,-4"/></g>' % (ix - 100, iy + 30, ix + 70, iy + 40))
# جزئیات کم‌اهمیت زمین
t = []; g = ''
g += scatter(16, 40, 640, lambda x, y: wave(x - 12, y, 1.1, '#aef0f4', .32), 48, taken=t)
g += scatter(9, 1830, 2390, lambda x, y: tree(x, y, .8 + random.random() * .35), 60, taken=t)
g += ''.join('<rect x="0" y="%d" width="390" height="30" fill="#fff" opacity=".05"/>' % y for y in range(1830, 2390, 62))
g += scatter(9, 1240, 1770, lambda x, y: crater(x, y, 14 + random.random() * 16), 52, taken=t)
g += ''.join('<circle cx="%d" cy="%d" r="%.1f" fill="#fff" opacity=".5"/>' % (random.randint(10, 380), random.randint(1230, 1780), random.random() * 1.5 + .8) for _ in range(14))
# مزرعه: شیار کشت و کاه‌بسته
for yy in range(700, 1215, 26): g += '<path d="M-10,%d Q100,%d 200,%d T400,%d" fill="none" stroke="#fff" stroke-width="5" opacity=".07"/>' % (yy, yy - 8, yy + 4, yy - 3)
g += scatter(5, 720, 1200, lambda x, y: ('<g transform="translate(%.1f,%.1f)"><ellipse rx="12" ry="9" fill="#e9c24a" stroke="%s" stroke-width="1.6"/><path d="M-8,0 h16" stroke="%s" stroke-width="1.2"/></g>' % (x, y, OUT, OUT)), 56, taken=t)
svg.append('<g>%s</g>' % g)
# ۲) رود پیچان در مزرعه (کنار آسیاب) + حوض
rd = 'M420,858 C350,892 318,826 252,840 C196,852 168,896 118,864 C80,840 58,810 40,828 C26,846 40,884 74,884'
svg.append('<g filter="url(#wob)">' + pth(rd, 'none', OUT, 40) + pth(rd, 'none', '#58d8ee', 31) + pth(rd, 'none', '#d4f6ff', 5, 'stroke-dasharray="12 24" transform="translate(0,-4)"') + '</g>')
# ۳) مسیر
svg.append('<g id="path" filter="url(#wob)">')
svg.append(pth(D_ALL, 'none', OUT, 33))
svg.append(pth(D_REST, 'none', CREAM, 22, 'opacity=".34"'))
svg.append(pth(D_REST, 'none', CREAM, 5, 'stroke-dasharray="3 14" opacity=".95"'))
svg.append(pth(D_DONE, 'none', CREAM, 22))
svg.append(pth(D_DONE, 'none', '#f0b429', 3.2, 'stroke-dasharray="10 12"'))
svg.append('</g>')
bx, by = 358, 866
svg.append('<g filter="url(#wob)" transform="translate(%d,%d)">' % (bx, by) + rect(-22, -32, 44, 64, '#c98a45', SW, 4) +
           ''.join(line(-22, y, 22, y, '#8f5a2e', 2) for y in range(-22, 32, 10)) +
           ''.join(rect(sx * 24 - 4, y - 4, 8, 8, '#8f5a2e', 2.8, 2) for sx in (-1, 1) for y in (-30, 0, 30)) + '</g>')
# ۴) بناها + نشان‌ها
for k in range(1, 13):
    fn, rx = BUILD[k]
    x, y = NODE[k]
    inner = fn()
    if k in LOCKED: inner = '<g style="filter:grayscale(.8) brightness(.9)">%s</g>' % inner
    svg.append('<g class="bld b%d" filter="url(#wob)" transform="translate(%.1f,%.1f)">%s</g>' % (k, x, y, inner))
    if k < HERE_K: svg.append('<g transform="translate(%.1f,%.1f)">%s</g>' % (x + rx * .62, y + 22, done_badge(0, 0)))
    if k in LOCKED: svg.append('<g transform="translate(%.1f,%.1f)">%s</g>' % (x + rx * .62, y + 22, lock_badge(0, 0)))
# برچسب کنار گره (جاگذار) زیر پایه، نه روی مسیر
LBL = []
for k in range(1, 13):
    if k == HERE_K: continue
    x, y = NODE[k]; rx = BUILD[k][1]
    ly = y + .36 * rx + 12 + 26
    LBL.append((k, x, ly))
    svg.append('<text class="ph" data-ph="lbl" x="%.1f" y="%.1f" text-anchor="middle" font-family="Lalezar" font-size="20" fill="#fff3c4" stroke="%s" stroke-width="6" paint-order="stroke" stroke-linejoin="round">.</text>' % (x, ly, OUT))
# تابلوی زون روی زمین (بی‌قاب)
ZS = [('z1', 285, 2112), ('z2', 118, 1586), ('z3', 270, 1024), ('z4', 112, 478)]
for key, x, y in ZS:
    svg.append('<text class="ph" data-ph="%s" x="%d" y="%d" text-anchor="middle" font-family="Lalezar" font-size="34" fill="#ffffff" stroke="%s" stroke-width="9" paint-order="stroke" stroke-linejoin="round" transform="rotate(-3 %d %d)">.</text>' % (key, x, y, OUT, x, y))
# شروع
sx, sy = START
chk = ''.join('<rect x="%d" y="%d" width="7" height="7" fill="%s"/>' % (-14 + 7 * i, -14 + 7 * j, OUT if (i + j) % 2 == 0 else '#fff') for i in range(4) for j in range(4))
svg.append('<g filter="url(#wob)" transform="translate(%.1f,%.1f)">%s</g>' % (sx + 38, sy, chk))
svg.append('<g filter="url(#wob)" transform="translate(%.1f,%.1f)">' % (sx - 8, sy - 22) + rect(-6, -56, 9, 56, '#d9a05a', SW) + rect(60, -56, 9, 56, '#d9a05a', SW) + rect(-14, -86, 96, 36, '#ffd23f', SW, 10) + '</g>')
svg.append('<text class="ph" data-ph="start" x="%.1f" y="%.1f" text-anchor="middle" font-family="Lalezar" font-size="24" fill="%s">.</text>' % (sx + 26, sy - 81, OUT))
# شخصیت راهنما روی «اینجایی»
hx_, hy_ = NODE[HERE_K]
svg.append('<g class="hero" transform="translate(%.1f,%.1f)">' % (hx_, hy_) +
           '<ellipse cx="0" cy="10" rx="98" ry="40" fill="none" stroke="%s" stroke-width="10"/><ellipse class="ring" cx="0" cy="10" rx="98" ry="40" fill="none" stroke="#ffd23f" stroke-width="5.5" stroke-dasharray="16 10"/>' % OUT +
           '<ellipse cx="0" cy="40" rx="30" ry="8" fill="#10083a" opacity=".35"/>'
           '<image href="%s" x="-41" y="-44" width="82" height="82"/>' % img_uri('b1.png', 'image/png') +
           '<g class="lbl"><path d="M-40,-150 h80 a12,12 0 0 1 12,12 v26 a12,12 0 0 1 -12,12 h-18 l-22,14 l-22,-14 h-18 a12,12 0 0 1 -12,-12 v-26 a12,12 0 0 1 12,-12z" fill="#ffd23f" stroke="%s" stroke-width="4" stroke-linejoin="round"/>' % OUT +
           '<text class="ph" data-ph="here" x="0" y="-119" text-anchor="middle" font-family="Lalezar" font-size="23" fill="%s">.</text></g></g>' % OUT)
# ابر و پرنده
sky = ''
for (x, y, s) in [(335, 1830, 1.0), (50, 1215, 1.1), (330, 640, 1.0), (60, 60, 1.2), (320, 1560, .8)]:
    if pdist(x, y) > 60: sky += cloud(x, y, s)
for (x, y) in [(300, 120), (70, 330), (330, 300), (60, 560), (320, 2300), (80, 2100)]:
    if pdist(x, y) > 40: sky += bird(x, y, 1.1)
svg.append('<g>%s</g>' % sky)
svg.append('<rect width="390" height="2400" fill="url(#vig)"/><rect width="390" height="2400" filter="url(#grain)"/></svg>')

css = '''
*{box-sizing:border-box;margin:0}
html,body{width:390px;height:800px;overflow:hidden;background:#10083a}
#phone{position:relative;width:390px;height:800px;overflow:hidden}
#scroll{width:390px;height:800px;overflow-y:auto;overflow-x:hidden;scrollbar-width:none}
#scroll::-webkit-scrollbar{display:none}
svg{display:block}
.ring{animation:spin 14s linear infinite}
@keyframes spin{to{stroke-dashoffset:-260}}
#bar{position:absolute;top:0;left:0;right:0;height:86px;z-index:5;pointer-events:none}
#bar svg{position:absolute;inset:0}
#bar .row{position:absolute;top:6px;left:0;right:0;height:62px;display:flex;align-items:center;gap:7px;padding:0 9px;pointer-events:auto}
.chip{flex:1;min-width:60px;height:60px;border-radius:16px;border:3.5px solid #241a5e;background:#4b3b9e;color:#fff3c4;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;box-shadow:0 4px 0 #120c3a}
.chip .w{font:700 15px/1.1 Vazirmatn}
.chip .n{display:flex;direction:ltr;gap:3px;font:25px/1 Lalezar}
.chip.on{background:#ffd23f;color:#241a5e;transform:translateY(2px);box-shadow:0 2px 0 #120c3a,0 0 0 3px #fff3c4}
.menu{width:58px;height:60px;border-radius:16px;border:3.5px solid #241a5e;background:#fff3c4;display:flex;flex-direction:column;gap:6px;align-items:center;justify-content:center;box-shadow:0 4px 0 #120c3a}
.menu i{display:block;width:26px;height:4.5px;border-radius:3px;background:#241a5e}
.menu span{position:absolute;width:1px;height:1px;overflow:hidden}
'''.replace('\\\\', '')
def chip(a, b, on=False):
    return '<div class="chip%s"><span class="w ph" data-ph="grade"></span><span class="n"><bdi class="ph" data-ph="d%d"></bdi><span>–</span><bdi class="ph" data-ph="d%d"></bdi></span></div>' % (' on' if on else '', a, b)
bar = ('<div id="bar"><svg width="390" height="86" viewBox="0 0 390 86"><defs><filter id="bw"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter></defs>'
       '<path filter="url(#bw)" d="M-6,-6 H396 V70 Q370,82 340,72 T280,74 T220,70 T160,76 T100,71 T40,76 T-6,70 Z" fill="#241a5e"/>'
       '<path filter="url(#bw)" d="M-6,70 Q40,82 100,71 T220,70 T340,72 T396,70" fill="none" stroke="#ffd23f" stroke-width="3" opacity=".55"/></svg>'
       '<div class="row"><div class="menu"><i></i><i></i><i></i><span class="ph" data-ph="menu"></span></div>' + chip(1, 2) + chip(3, 4, True) + chip(5, 6) + '</div></div>')
js = "const sc=document.getElementById('scroll');const q=new URLSearchParams(location.search);sc.scrollTop=q.has('y')?+q.get('y'):%d;" % int(NODE[HERE_K][1] - 400)
body = '<div id="phone">%s<div id="scroll">%s</div></div>' % (bar, ''.join(svg))
open(os.path.join(STYLE, 'map.html'), 'w').write(page('map', css, body, js))
print({k: (round(x), round(ly)) for k, x, ly in LBL})
bad = [(k, round(pdist(x, ly - 7))) for k, x, ly in LBL if pdist(x, ly - 7) < 24]
print('labels near path:', bad)
