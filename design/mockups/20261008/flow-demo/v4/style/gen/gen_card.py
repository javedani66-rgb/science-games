import random, math
from common import *
random.seed(3)
BG = '#190539'
dock = img_uri('dock.jpg', 'image/jpeg'); hero = img_uri('b1.png', 'image/png')

def night_bg(h=800):
    s = ['<svg class="bg" width="390" height="%d" viewBox="0 0 390 %d"><defs>' % (h, h)]
    s.append('<radialGradient id="n1" cx=".2" cy=".15" r=".7"><stop offset="0" stop-color="#5a14a8" stop-opacity=".55"/><stop offset="1" stop-color="#5a14a8" stop-opacity="0"/></radialGradient>'
             '<radialGradient id="n2" cx=".85" cy=".85" r=".7"><stop offset="0" stop-color="#a0197a" stop-opacity=".4"/><stop offset="1" stop-color="#a0197a" stop-opacity="0"/></radialGradient>'
             '<pattern id="dots" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="#8a4fe0" opacity=".28"/></pattern>'
             '<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#fff"/></linearGradient>'
             '<mask id="mfade"><rect width="390" height="%d" fill="url(#fade)"/></mask></defs>' % h)
    s.append('<rect width="390" height="%d" fill="%s"/><rect width="390" height="%d" fill="url(#n1)"/><rect width="390" height="%d" fill="url(#n2)"/>' % (h, BG, h, h))
    s.append('<rect width="390" height="%d" fill="url(#dots)" mask="url(#mfade)"/>' % h)
    for _ in range(70):
        x, y = random.uniform(4, 386), random.uniform(4, h - 4); r = random.choice([.8, 1, 1.2, 1.6])
        s.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="#e9dcff" opacity="%.2f"/>' % (x, y, r, random.uniform(.35, .9)))
    for _ in range(7):
        x, y = random.uniform(15, 375), random.uniform(15, h - 15); r = random.uniform(5, 9)
        s.append('<path d="M%.1f,%.1f l%.1f,%.1f l%.1f,-%.1f l-%.1f,%.1f l-%.1f,%.1f l-%.1f,-%.1f z" fill="#ffd9ff" opacity=".75"/>' % (x, y - r, r*.18, r*.82, r*.82, r*.18, r*.82, r*.18, r*.18, r*.82, r*.18, r*.82))
    # گیربکس محو پس‌زمینه (هویت «ماشین»)
    s.append('<g opacity=".08" transform="translate(300,%d)">%s</g>' % (h - 90, cogpath(70)))
    s.append('<g opacity=".06" transform="translate(40,120)">%s</g>' % cogpath(46))
    s.append('</svg>')
    return ''.join(s)

def cogpath(r):
    n = 10; pp = []
    for i in range(n * 2):
        a = math.pi * i / n; rr = r if i % 2 == 0 else r * .78
        for da in (-.1, .1): pp.append('%.1f,%.1f' % (rr * math.cos(a + da), rr * math.sin(a + da)))
    return '<polygon points="%s" fill="#c9a6ff"/><circle r="%.1f" fill="%s"/>' % (' '.join(pp), r * .35, BG)

DEFS = '''<svg width="0" height="0" style="position:absolute"><defs>
<filter id="torn" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".07 .05" numOctaves="3" seed="8" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="9"/></filter>
<filter id="torn2" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".09" numOctaves="2" seed="21" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="6"/></filter>
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="glow2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
</defs></svg>'''

def card_svg(w, h, c1, c2, glowc, plate_y, art=True, uid='a', big=True):
    """کارت تخت با لبهٔ قلم‌مویی، درخشش نئونی فقط دور قاب، صفحهٔ تیره برای متن"""
    r = 26 if big else 16
    s = '<svg width="%d" height="%d" viewBox="-20 -20 %d %d" style="overflow:visible">' % (w, h, w + 40, h + 40)
    s += '<defs><linearGradient id="cg%s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>' % (uid, c1, c2)
    s += '<clipPath id="cp%s"><rect x="0" y="0" width="%d" height="%d" rx="%d"/></clipPath></defs>' % (uid, w, h, r)
    s += '<rect x="0" y="0" width="%d" height="%d" rx="%d" fill="none" stroke="%s" stroke-width="16" filter="url(#glow)" opacity=".95"/>' % (w, h, r, glowc)
    s += '<g filter="url(#torn)"><rect x="0" y="0" width="%d" height="%d" rx="%d" fill="url(#cg%s)" stroke="%s" stroke-width="5"/>' % (w, h, r, uid, BG)
    s += '<g clip-path="url(#cp%s)"><rect x="0" y="%d" width="%d" height="%d" fill="#07203a"/>' % (uid, plate_y, w, h - plate_y)
    s += '<path d="M0,%d q%d,-14 %d,0 t%d,0 t%d,0 t%d,0 V%d H0Z" fill="#07203a"/>' % (plate_y, w/8, w/4, w/4, w/4, w/4, plate_y + 20)
    s += '</g>'
    s += '<rect x="9" y="9" width="%d" height="%d" rx="%d" fill="none" stroke="#ffd23f" stroke-width="3.6"/>' % (w - 18, h - 18, r - 6)
    s += '<rect x="9" y="9" width="%d" height="%d" rx="%d" fill="none" stroke="#fff3c4" stroke-width="1.6" stroke-dasharray="9 5" opacity=".8"/>' % (w - 18, h - 18, r - 6)
    s += '</g></svg>'
    return s

# --- پیکرها (آیکون‌های درونی) ---
def ico_play(c='#190539'): return '<svg width=30 height=30 viewBox="0 0 30 30"><polygon points="7,4 26,15 7,26" fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/></svg>' % (c, c)
def ico_gear(c='#190539'):
    n = 8; pp = []
    for i in range(n * 2):
        a = math.pi * i / n; rr = 13 if i % 2 == 0 else 9.5
        for da in (-.13, .13): pp.append('%.1f,%.1f' % (15 + rr * math.cos(a + da), 15 + rr * math.sin(a + da)))
    return '<svg width=30 height=30 viewBox="0 0 30 30"><polygon points="%s" fill="%s"/><circle cx=15 cy=15 r=4.5 fill="#ffd23f"/></svg>' % (' '.join(pp), c)
def ico_box(c='#190539'): return '<svg width=34 height=30 viewBox="0 0 34 30"><path d="M3,10 L17,3 L31,10 V25 L17,29 L3,25Z" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/><path d="M3,10 L17,17 L31,10 M17,17 V29" fill="none" stroke="%s" stroke-width="3" stroke-linejoin="round"/></svg>' % (c, c)
def ico_lock(c='#cdb8ff'): return '<svg width=34 height=36 viewBox="0 0 34 36"><path d="M9,16 V11 a8,8 0 0 1 16,0 V16" fill="none" stroke="%s" stroke-width="3.6"/><rect x="5" y="16" width="24" height="17" rx="4" fill="%s"/><circle cx=17 cy=24 r=3 fill="#190539"/></svg>' % (c, c)
def ico_eye(c='#fff'): return '<svg width=34 height=24 viewBox="0 0 34 24"><path d="M2,12 Q17,-2 32,12 Q17,26 2,12Z" fill="none" stroke="%s" stroke-width="3"/><circle cx=17 cy=12 r=5 fill="%s"/></svg>' % (c, c)
def ico_plus(c='#9a78e0'): return '<svg width=28 height=28 viewBox="0 0 28 28"><path d="M14,4 V24 M4,14 H24" stroke="%s" stroke-width="5" stroke-linecap="round"/></svg>' % c

CSS = '''
*{box-sizing:border-box;margin:0}
html,body{width:390px;height:800px;overflow:hidden;background:#190539;font-family:Vazirmatn,sans-serif;color:#fff}
.screen{position:absolute;inset:0;width:390px;height:800px;overflow:hidden;display:none}
.screen.on{display:block}
.bg{position:absolute;inset:0}
.abs{position:absolute}
.cardwrap{position:absolute;left:22px;top:26px;width:346px;height:640px}
.cardwrap svg.card{position:absolute;left:-20px;top:-20px}
.title{position:absolute;right:0;left:0;top:54px;text-align:center;font:56px/1.05 Lalezar;color:#fff;-webkit-text-stroke:9px #190539;paint-order:stroke fill;text-shadow:0 0 18px #ff5ad6,0 0 34px #ff5ad6}
.title.sm{font-size:40px;-webkit-text-stroke:7px #190539;top:50px}
.art{position:absolute;left:24px;right:24px;top:140px;height:226px;border:6px solid #190539;border-radius:14px;overflow:hidden;box-shadow:0 0 0 3px #fff3c4,0 0 0 6px #190539}
.art img{width:100%;height:100%;object-fit:cover;display:block}
.body{position:absolute;left:30px;right:30px;top:418px;font:700 23px/1.75 Vazirmatn;color:#fff;text-align:center}
.hero{position:absolute;right:-26px;top:290px;width:118px;height:118px;filter:drop-shadow(0 0 10px #190539) drop-shadow(0 3px 0 #190539)}
.pill{position:absolute;display:flex;align-items:center;justify-content:center;gap:10px;height:64px;border-radius:20px;border:4px solid #190539;font:30px/1 Lalezar;color:#190539}
.pill.gold{background:#ffd23f;box-shadow:0 0 0 3px #ffd23f66,0 0 22px #ffd23f99}
.pill.cyan{background:#46f0d8;box-shadow:0 0 22px #46f0d899}
.pill.pink{background:#ff7be5;box-shadow:0 0 22px #ff7be599}
.flipbtn{position:absolute;left:50%;bottom:20px;transform:translateX(-50%);min-width:170px;height:56px;border-radius:18px;background:#46f0d8;border:4px solid #190539;font:26px Lalezar;color:#190539;display:flex;align-items:center;justify-content:center;box-shadow:0 0 22px #46f0d899}
.cap{font:700 17px/1.2 Vazirmatn;color:#fff;text-align:center}
.shelfhead{position:absolute;top:34px;left:0;right:0;text-align:center;font:50px/1 Lalezar;color:#fff;-webkit-text-stroke:8px #190539;paint-order:stroke fill;text-shadow:0 0 18px #ffd23f,0 0 32px #ffd23f}
.slot{position:absolute;width:158px;height:228px}
.slot svg.card{position:absolute;left:-20px;top:-20px}
.slot .ic{position:absolute;left:0;right:0;top:78px;display:flex;justify-content:center}
.slot .cap{position:absolute;left:0;right:0;top:148px}
.ledge{position:absolute;left:14px;right:14px;height:16px;border-radius:8px;background:#2a0b60;border:3px solid #190539;box-shadow:0 0 14px #8a4fe0aa,inset 0 3px 0 #7b3fd0}
.badgeshape{position:absolute;top:10px;right:10px}
'''

def front():
    s = '<div class="screen" data-v="front">' + night_bg()
    s += '<div class="cardwrap">' + card_svg(346, 600, '#25cdc0', '#0a86a4', '#46f0d8', 392, uid='f')
    s += '<div class="title"><span class="ph" data-ph="title"></span></div>'
    # تصویر با لبهٔ قلم‌مویی
    s += '<div class="art"><img src="%s"></div>' % dock
    s += '<img class="hero" src="%s">' % hero
    s += '<div class="body"><span class="ph" data-ph="body"></span></div>'
    s += '<div class="flipbtn"><span class="ph" data-ph="back"></span></div>'
    s += '</div></div>'
    return s

def schematic():
    # نقشهٔ ساده چرخ‌قرقره (شمای وضعیت بازی) با خط روشن
    return ('<svg width="290" height="150" viewBox="0 0 290 150" fill="none" stroke="#fff3c4" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
            '<path d="M30,140 H260" stroke="#46f0d8"/><path d="M60,140 V20 H190"/><circle cx="190" cy="34" r="16"/><circle cx="190" cy="34" r="3" fill="#fff3c4"/>'
            '<path d="M174,34 V92"/><rect x="156" y="92" width="36" height="32" fill="#c98a45" stroke="#190539" stroke-width="4"/>'
            '<path d="M206,34 L238,110" stroke-dasharray="3 10"/><path d="M238,92 V122 M226,108 L238,124 L250,108" stroke="#ffd23f"/></svg>')

def back():
    s = '<div class="screen" data-v="back">' + night_bg()
    s += '<div class="cardwrap">' + card_svg(346, 640, '#25cdc0', '#0a86a4', '#46f0d8', 116, uid='b')
    s += '<div class="title sm"><span class="ph" data-ph="title"></span></div>'
    s += '<div class="abs" style="left:28px;top:150px">%s</div>' % schematic()
    s += '<div class="pill cyan" style="left:26px;right:26px;top:332px">%s<span class="ph" data-ph="practice"></span></div>' % ico_gear()
    s += '<div class="pill pink" style="left:26px;right:26px;top:418px">%s<span class="ph" data-ph="video"></span></div>' % ico_play()
    s += '<div class="pill gold" style="left:26px;right:26px;top:520px;height:72px;font-size:34px">%s<span class="ph" data-ph="box"></span></div>' % ico_box()
    s += '</div></div>'
    return s

def slot(x, y, kind, uid):
    pal = dict(seen=('#25cdc0', '#0a86a4', '#46f0d8'), kept=('#7a6af5', '#4a2fb8', '#a99dff'),
               empty=('#2a0b60', '#2a0b60', '#6b3fc0'), locked=('#34145f', '#220a45', '#3a1a70'))[kind]
    ic = dict(seen=ico_eye('#fff'), kept=ico_box('#fff'), empty=ico_plus(), locked=ico_lock())[kind]
    s = '<div class="slot" style="left:%dpx;top:%dpx">' % (x, y)
    s += card_svg(158, 228, pal[0], pal[1], pal[2], 130, uid=uid, big=False)
    if kind == 'empty':
        s += '<svg style="position:absolute;left:0;top:0" width=158 height=228><rect x=10 y=10 width=138 height=208 rx=14 fill="#190539" stroke="#9a78e0" stroke-width="4" stroke-dasharray="12 9"/></svg>'
    if kind == 'locked':
        s += '<svg style="position:absolute;left:0;top:0" width=158 height=228><defs><clipPath id="lk"><rect x=14 y=14 width=130 height=200 rx=10 /></clipPath></defs><g clip-path="url(#lk)"><rect x=14 y=14 width=130 height=200 fill="#190539" opacity=".55"/><path d="M-10,60 L170,20 M-10,110 L170,70 M-10,160 L170,120 M-10,210 L170,170" stroke="#5a2fa0" stroke-width="3" opacity=".6"/></g></svg>'
    s += '<div class="ic" style="top:%dpx">%s</div>' % ((46 if kind in ('seen', 'kept') else 70), ic)
    s += '<div class="cap" style="top:150px"><span class="ph" data-ph="%s"></span></div>' % {'seen': 'seen', 'kept': 'kept', 'empty': 'empty', 'locked': 'locked'}[kind]
    if kind in ('seen', 'kept'):
        s += '<div class="abs" style="left:0;right:0;top:92px;display:flex;justify-content:center">%s</div>' % ('<div style="width:96px;height:44px;border-radius:10px;overflow:hidden;border:3px solid #190539"><img src="%s" style="width:100%%;height:100%%;object-fit:cover"></div>' % dock)
    s += '</div>'
    return s

def plank(y):
    return ('<svg class="abs" style="left:14px;top:%dpx" width="362" height="64" viewBox="0 0 362 64" fill="none" stroke="%s" stroke-width="3.4" stroke-linejoin="round">'
      '<path d="M12,8 H350 L362,22 H0 Z" fill="#d9a05a"/><rect x="0" y="22" width="362" height="20" rx="3" fill="#8a5a2e"/>'
      '<path d="M18,32 H90 M120,30 H210 M236,33 H330 M60,15 H150 M200,14 H300" stroke="#5e3a1a" stroke-width="2" stroke-linecap="round"/>'
      '<path d="M40,42 V60 L70,42 Z M292,42 V60 L322,42 Z" fill="#8a5a2e"/></svg>') % (y, '#190539')

def shelf():
    s = '<div class="screen" data-v="shelf">' + night_bg()
    s += '<div class="shelfhead"><span class="ph" data-ph="shelf"></span></div>'
    s += slot(26, 130, 'seen', 's1') + slot(206, 130, 'kept', 's2')
    s += plank(346)
    s += slot(26, 420, 'empty', 's3') + slot(206, 420, 'locked', 's4')
    s += plank(638)
    s += '<img src="%s" style="position:absolute;left:150px;top:690px;width:110px;height:110px;filter:drop-shadow(0 0 8px #190539)">' % hero
    s += '</div>'
    return s

js = "const v=new URLSearchParams(location.search).get('v')||'front';document.querySelector('[data-v='+v+']').classList.add('on');"
body = DEFS + front() + back() + shelf()
open(os.path.join(STYLE, 'card-night.html'), 'w').write(page('card-night', CSS, body, js))
