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
DX, DY, DR = -35, -4, 16                  # مرکز و شعاع در
XF = (1.05, -14.1, -0.7)
SMOKE_B = ((2, -87, 7), (12, -95, 8), (25, -101, 9))
RISE = 25; DELAYS = (0, .7, 1.4); CYCLE = 2.8
GX, GY = -3, -24                         # مرکز چرخ‌دندهٔ تابلو


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
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))   # حاشیهٔ هم‌رنگ: درز مویی بین چندضلعی‌ها نماند


def build(out=OUTD):
    p = Pen('final_workshop', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(CX + 2, BASE + 8, 40)
    # دودکش آجری (پشت تپه) با کلاهک و دودِ رو به راست-بالا (بالاتر از سر فیگور)
    p.shape([(-8, -20), (8, -20), (8, -68), (-8, -68)], BRICK, PART, j=.3, step=6)
    p.ln((-8, -34), (8, -34), INNER, BRICK_D, j=.1); p.ln((-8, -48), (8, -48), INNER, BRICK_D, j=.1)
    p.shape([(-12, -78), (12, -78), (12, -68), (-12, -68)], BRICK_D, PART, j=.3, step=6)
    # سه حباب دود: هرکدام یک لایهٔ جدا؛ حالت ایستا = همان چینش قبلی (روی دودکشِ کامل)
    for k, (x, y, r) in enumerate(SMOKE_B, 1):
        with layer(p, 'smoke_%d' % k):
            p.shape(ell(x, y, r, r * .85, 0, 360, 16), SMOKE, INNER, j=.1, step=99, clip=False)
    # تپه
    p.shape(hill(), FUR, OUT, j=.4, step=99)
    p.fill(ell(CX - 16, BASE - HH * .66, 13, 5.5, 0, 360, 20), FUR_L)                                                     # نور روی پشم
    for (x, y) in ((-48, -24), (-33, -38), (-18, -36), (6, -10)):      # نشانهٔ پشم: v کوچک تخت
        p.ln((x - 4, y - 4), (x, y), INNER, FUR_D, j=.05); p.ln((x, y), (x + 4, y - 4), INNER, FUR_D, j=.05)
    # در گرد بزرگ: دهانهٔ تیره + درون گرم + لنگهٔ چوبی نیمه‌باز
    p.shape(ell(DX, DY, DR, DR, 0, 360, 28), HOLE, PART, j=.2, step=99)
    p.fill(ell(DX - 5, DY + 2, 9, 10, 0, 360, 20), GLOW)
    p.shape(ell(DX + 10, DY, 8, DR - 1, 0, 360, 20), WOOD, PART, j=.2, step=99)
    p.ln((DX + 10, DY - 5), (DX + 10, DY + 5), INNER, WOOD_D, j=.05)
    # لامپ: روی قله با پایهٔ کوچک
    p.ln((CX, BASE - HH + 1), (CX, BASE - HH - 5), INNER, WOOD_D, j=.05)
    p.shape(ell(CX, BASE - HH - 9, 8, 8, 0, 360, 20), GLOW, PART, j=.2, step=99)
    # تابلو: چرخ‌دندهٔ کوچک (لایهٔ متحرک)
    with layer(p, 'gear'):
        p.fill(gear_poly(GX, GY, 7.5, 11.5), GEAR)
        p.fill(ell(GX, GY, 3.8, 3.8, 0, 360, 16), FUR_D)
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
