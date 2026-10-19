#!/usr/bin/env python3
"""ایستگاه M12 «مخفی‌گاه هیولای مخترع»: قهرمان = لانهٔ تپه‌ای پشمالوی بنفش با درِ گردِ چوبی نیمه‌باز و درون گرم،
لامپ بالای در، دودکش با دود، و یک چرخ‌دندهٔ کوچک (۸ دنده، رنگ تخت بدون خط دور) به‌عنوان تابلو. هیولا دیده نمی‌شود.
لایه‌های متحرک: node_final_workshop_gear (چرخش آهسته) و node_final_workshop_smoke_1..3 (سه حباب دود جدا که از دودکش بالا می‌روند و محو می‌شوند). id نود: node_final_workshop (ثابت)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/final_workshop'

FUR = '#a477e8'; FUR_D = '#7c52c9'; FUR_L = '#c9a8f5'
HOLE = '#2b1d5e'; GLOW = '#ffd84d'; WOOD = '#c98f4a'; WOOD_D = '#8a5a26'
BRICK = '#e0674c'; BRICK_D = '#b8432f'; SMOKE = '#f3eefc'; GEAR = '#ffd84d'; GEAR_D = '#e0a020'
import functools, station_kit as _k   # D122/D123: حاشیهٔ چپ/راست ≥۴px (بدون دست‌زدن به کیت)
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)
CX, BASE, HW, HH = -23, 7, 33, 58       # مرکز تپه، خط کف، نیم‌پهنا، ارتفاع
DX, DY, DR = -24, -17, 16                  # مرکز و شعاع در
XF = (1.0, -18, 6)
CHX0, CHX1 = 14, 30
ROOF = '#6a45c4'; ROOF_D = '#4f2f9a'; ROOF_L = '#9a78e6'
SMOKE_B = ((20, -100, 5), (28, -105, 6), (36, -111, 7))
RISE = 8; DELAYS = (0, .7, 1.4); CYCLE = 2.8
GX, GY = 14, -23                         # مرکز چرخ‌دندهٔ تابلو


def hill():
    pts = []
    n = 72
    for i in range(n + 1):                       # گنبد پشمالو: برآمدگی‌های گرد با شکاف تیز (پشم)
        t = math.pi * i / n
        r = 1 + .075 * abs(math.sin(t * 5)) - .04
        c, sn = math.cos(t), math.sin(t); e = .78
        pts.append((CX + HW * math.copysign(abs(c) ** e, c) * r, BASE - HH * abs(sn) ** e * r))
    pts += [(CX + HW * math.cos(math.radians(a)), BASE + 7 * math.sin(math.radians(a))) for a in range(170, 9, -20)]   # کف بیضوی مثل سکو
    return pts[::-1]


def gear_poly(cx, cy, ri, ro, n=8, w=.36):
    pt = 2 * math.pi / n; out = []
    for k in range(n):
        a = k * pt + math.radians(22.5)
        for da, r in ((-.5 * pt, ri), (-w * pt / 2 * 1.0 - .02, ri), (-w * pt / 2 * .8, ro), (w * pt / 2 * .8, ro), (w * pt / 2 + .02, ri)):
            out.append((cx + r * math.cos(a + da), cy + r * math.sin(a + da)))
    return out


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sharp(p, pts, col, sw=OUT, clipit=True):
    """چندضلعی تیز (کنج‌ها نرم نمی‌شوند)؛ مثل sail() در shipyard.py."""
    q = p.X(pts)
    p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % t for t in q), col, sw))
    if clipit: p.clip.append('M' + ' L'.join('%.1f,%.1f' % t for t in q) + ' Z')


def dots(p, pts, r, col):
    for x, y in pts:
        a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def build(out=OUTD):
    p = Pen('final_workshop', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-8, 3, 42)
    # دودکش آجری بلند (پشت سقف) با کلاهک
    sharp(p, [(CHX0, -30), (CHX1, -30), (CHX1, -84), (CHX0, -84)], BRICK, PART)
    for y in (-50, -64, -76): p.ln((CHX0 + 2, y), (CHX1 - 2, y), INNER, BRICK_D, j=.1)
    sharp(p, [(CHX0 - 5, -94), (CHX1 + 5, -94), (CHX1 + 5, -84), (CHX0 - 5, -84)], BRICK_D, PART)
    # سه حباب دود: هرکدام یک لایهٔ جدا؛ حالت ایستا = روی دودکشِ کامل
    for k, (x, y, r) in enumerate(SMOKE_B, 1):
        with layer(p, 'smoke_%d' % k):
            p.shape(ell(x, y, r, r * .85, 0, 360, 16), SMOKE, INNER, j=.1, step=99, clip=False)
    # دیوار تخته‌ای بنفش
    sharp(p, [(-48, 0), (32, 0), (32, -46), (-48, -46)], FUR, PART)
    for x in (-1, 28): p.ln((x, -6), (x, -40), INNER, FUR_D, j=.05)
    for x in (-42, 38 - 4): pass
    p.ln((-44, -40), (-30, -40), INNER, FUR_L, j=.05)
    # در قوسی با هیولای کوچک پشمالو که از تاریکی نگاه می‌کند (چشم‌های درشت، گوش، دو پنجه روی آستانه)
    sharp(p, [(-42, -2), (-6, -2), (-6, -30), (-12, -38), (-36, -38), (-42, -30)], HOLE, PART)
    sharp(p, [(-38, -22), (-35, -31), (-30, -26), (-18, -26), (-13, -31), (-10, -22), (-10, -8), (-38, -8)], FUR_D, INNER, clipit=False)   # سر با دو گوش
    poly(p, [(-36, -20), (-12, -20), (-12, -10), (-36, -10)], FUR_D)
    for ex in (-30, -18):
        p.fill(ell(ex, -20, 5.2, 5.6, 0, 360, 16), '#ffffff'); p.fill(ell(ex + 1, -19, 2.4, 2.8, 0, 360, 12), NAVY)
    p.fill([(-28, -11), (-20, -11), (-20, -9), (-28, -9)], GLOW)                       # دهان کوچک خندان
    for px in (-34, -14):
        p.shape(ell(px, -5, 6, 5, 0, 360, 14), FUR, INNER, j=.1, step=99, clip=False)   # پنجه‌ها روی آستانه
    # سقف دوشیب: شیب چپ بنفش، شیب راست تیره‌تر؛ زِرِه و پیچ
    sharp(p, [(-58, -44), (-12, -90), (-12, -44)], ROOF, PART)
    sharp(p, [(-12, -90), (42, -44), (-12, -44)], ROOF_D, PART)
    for (x0, x1, y) in ((-48, -36, -52), (-30, -18, -52), (-40, -28, -63), (-6, 6, -52), (12, 24, -52), (4, 14, -62)):
        if y > -46: continue
        p.ln((x0, y), (x1, y), INNER, ROOF_L, j=.05)
    dots(p, [(-52, -55), (-30, -52), (28, -53)], 0, CREAM)
    # پنجرهٔ گرد روی سقف
    p.shape(ell(-12, -64, 10, 10, 0, 360, 24), GLOW, PART, j=.15, step=99)
    p.ln((-12, -72), (-12, -56), INNER, WOOD_D, j=.05); p.ln((-20, -64), (-4, -64), INNER, WOOD_D, j=.05)
    # لولهٔ کوچک روی سقف (با کلاهک)
    sharp(p, [(-49, -58), (-41, -58), (-41, -80), (-49, -80)], GEAR_D, INNER)
    sharp(p, [(-52, -80), (-38, -80), (-38, -86), (-52, -86)], GEAR, INNER)
    dots(p, [(-45, -66), (-45, -73)], 1.8, WOOD_D)
    # چراغ روی قلهٔ سقف
    p.ln((-12, -90), (-12, -97), INNER, WOOD_D, j=.05)
    p.shape(ell(-12, -102, 7, 7, 0, 360, 20), GLOW, PART, j=.2, step=99)
    # تابلو = چرخ‌دندهٔ زرد (لایهٔ متحرک) کنار در
    with layer(p, 'gear'):
        p.fill(gear_poly(GX, GY, 8, 12.5), GEAR)
        p.fill(ell(GX, GY, 4, 4, 0, 360, 16), FUR_D)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    gm = p.X((GX, GY))
    mot = {'gear': dict(rotate=gm)}
    for k in (1, 2, 3): mot['smoke_%d' % k] = dict(offsets=[(0, 0), p.V((0, -RISE / 2)), p.V((0, -RISE))])
    r = finish(p, 'final_workshop', STAND, motion=mot, out=OUTD, shots=SHOTS)
    sp = r['spec']
    ms = {'node_final_workshop_gear': dict(center=[round(v, 1) for v in gm], dir='cw', note='چرخ‌دندهٔ تابلو؛ ۸ دنده، چرخش آهسته. لامپ ثابت.')}
    for k in (1, 2, 3):
        ms['node_final_workshop_smoke_%d' % k] = dict(translate_y=[0, -RISE], opacity=[1, 0], delay_s=DELAYS[k - 1], cycle_s=CYCLE, easing='ease-out', loop=True,
                                                     start='همان جای ایستا (دهانهٔ دودکش)', note='بالا می‌رود و محو می‌شود؛ بعد از محوشدن به جای ایستا برمی‌گردد. دودکش آجری کامل و ثابت زیر آن است.')
    ms['reduced_motion'] = 'همهٔ لایه‌ها ثابت؛ حباب‌ها در جای ایستا با opacity کامل'
    sp['motion_spec'] = ms
    (OUTD / 'final_workshop.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
