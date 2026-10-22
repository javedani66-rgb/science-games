#!/usr/bin/env python3
"""ایستگاه E02 «ایستگاه گاری‌ها» (سرزمین مزرعه، پالت farm). نمای کنار، بدون حیوان.
طرح قطعه‌به‌قطعه (واحد symbol، y منفی = بالا، زمین y=8):
 ۱ سایهٔ تماس چرخ و سر دسته (بیرون از لایهٔ متحرک، ایستا)
 لایهٔ متحرک node_cart_station_roll (کل گاری؛ پایان = جای ایستا):
 ۲ دستهٔ بلند (شافت): متوازی‌الاضلاع ۱۳ پهن، از زیر تختهٔ بار (x=-26) رو به راست-پایین تا زمین (x=24)؛ چوب روشن #d9784a
 ۳ تختهٔ بار: x -80..-14، y -31..-19، چوب سرخ #b8572f، روشن #d9784a، تیره #7f3a1f
 ۴ دیوارهٔ عقب: x -80..-70، y -48..-19 (هم‌پوشان با تخته)
 ۵ گونی سفید-آبی #f4f7ff با بند #6f8fe8
 ۶ چرخ بلند: مرکز (-44,-16) شعاع ۲۴؛ لبه #6e2f1b، داخل کرم #fbeee0، ۸ پره، توپی زرد، میخ زرد روی لبه (تا چرخش دیده شود)
 چرخ داخل گروه تو‌در‌توی node_cart_station_roll_wheel است.
رنگ قهرمان رنگ‌مایهٔ ≈۱۵° در برابر سکوی مزرعه ۵۰°."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/cart_station'

W_B, W_L, W_D = '#b8572f', '#d9784a', '#7f3a1f'
RIM = '#6e2f1b'; HUBC = '#fbeee0'; YEL = '#ffd84d'
SK, SK_D, BLUE = '#f4f7ff', '#cfd8ee', '#6f8fe8'
G = 8
WC = (-44, -16); WR = 24
SH0, SH1 = (-26, -25), (24, 3)
SLIDE = -14


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def build(out=OUTD):
    p = Pen('cart_station', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 8, 0)
    p.tipshadow(WC[0] + 4, G - 1, 20); p.foot_tip(WC[0] + 2, G - 1, 14)
    p.tipshadow(SH1[0] + 3, G - 3, 8); p.foot_tip(SH1[0] + 1, G - 3, 6)
    with layer(p, 'roll'):
        dx, dy = SH1[0] - SH0[0], SH1[1] - SH0[1]; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L; nx, ny = -uy * 6.5, ux * 6.5
        sh = [(SH0[0] + nx, SH0[1] + ny), (SH1[0] + nx, SH1[1] + ny), (SH1[0] - nx, SH1[1] - ny), (SH0[0] - nx, SH0[1] - ny)]
        p.shape(sh, W_L, PART, j=.1, step=99, clip=False)
        poly(p, [(SH0[0] + 12 * ux - nx * .15, SH0[1] + 12 * uy - ny * .15), (SH1[0] - 4 * ux - nx * .15, SH1[1] - 4 * uy - ny * .15),
                 (SH1[0] - 4 * ux + nx * .15, SH1[1] - 4 * uy + ny * .15), (SH0[0] + 12 * ux + nx * .15, SH0[1] + 12 * uy + ny * .15)], '#f2a47a')
        p.shape([(-80, -48), (-70, -48), (-70, -19), (-80, -19)], W_B, PART, j=.1, step=99, clip=False)
        poly(p, [(-77, -45), (-74.5, -45), (-74.5, -22), (-77, -22)], W_L)
        bed = [(-80, -31), (-14, -31), (-14, -19), (-80, -19)]
        p.shape(bed, W_B, PART, j=.1, step=99, clip=False)
        poly(p, [(-69, -28.3), (-17, -28.3), (-17, -25.5), (-69, -25.5)], W_L)
        poly(p, [(-69, -22), (-17, -22), (-17, -19.6), (-69, -19.6)], W_D)
        p.stroke(bed, PART, j=.1, step=99)
        sack = [(-65, -31), (-65, -40)] + ell(-49, -40, 16, 12, 180, 360, 12) + [(-33, -31)]
        p.shape(sack, SK, PART, j=.1, step=99, clip=False)
        poly(p, [(-42, -48), (-34, -43), (-34, -33), (-42, -33)], SK_D)
        poly(p, [(-60, -45), (-57, -47), (-57, -36), (-60, -36)], '#ffffff')
        p.ln((-60, -46.5), (-39, -46.5), INNER, BLUE, j=0)
        p.raw('<g id="node_cart_station_roll_wheel">')
        p.shape(ell(WC[0], WC[1], WR, WR, 0, 360, 48), RIM, PART, j=.05, step=99, clip=False)
        a, b = p.X(WC)
        p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, 14.5, HUBC))
        for k in range(8):
            t = math.radians(k * 45 + 10)
            p.ln((WC[0], WC[1]), (WC[0] + 17 * math.cos(t), WC[1] + 17 * math.sin(t)), INNER, RIM, j=0)
        disc(p, WC[0], WC[1], 6.5, RIM); disc(p, WC[0], WC[1], 3, YEL)
        t = math.radians(32.5)
        disc(p, WC[0] + 19.5 * math.cos(t), WC[1] + 19.5 * math.sin(t), 2.6, YEL)
        p.raw('</g>')
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    mo = {'roll': dict(offsets=[(SLIDE * i / 6, 0) for i in range(7)])}
    r = finish(p, 'cart_station', STAND, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']; hub = [round(v, 1) for v in p.X(WC)]
    sp['motion_spec'] = {'node_cart_station_roll': dict(kind='translate', dx_from=SLIDE, dx_to=0, dur_s=1.8, count=1, ease='ease-out',
                         note='کل گاری از ۱۴ واحد (≈۱۰px) چپ می‌غلتد و در جای ایستا می‌ایستد؛ حالت ایستا = پایان؛ بدون حلقهٔ بیکار.'),
                         'node_cart_station_roll_wheel': dict(kind='rotate', about=hub, deg_from=-33, deg_to=0,
                         note='گروه تو‌در‌توی چرخ؛ ۱۴ واحد روی شعاع ۲۴ ≈ ۳۳°؛ ساعت‌گرد؛ هم‌زمان با غلتیدن'),
                         'reduced_motion': 'ایستا'}
    (OUTD / 'cart_station.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
