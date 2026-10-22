#!/usr/bin/env python3
"""R6: بازطراحی — دیلم ضخیم‌تر با سر خمیده، سنگ تکیه‌گاه سه‌وجهی بزرگ‌تر، تخته‌سنگ بار درشت چندوجهی، دو سنگ‌ریزه؛ لایهٔ متحرک node_excavation_bar (میله+سنگ بار)، حالت ایستا = پایان.
ایستگاه M04 «گودبرداری» (سرزمین شهر، سکوی آبی-فولادی ۲۱۳°). تصمیم مالک: میلهٔ فلزی روی سنگ تکیه‌گاه که سنگی را بالا می‌آورد.
نمای جانبی؛ حالت ایستا = پایان حرکت (سر بلند میله پایین آمده، سنگ بار بالا رفته).
فقط ۳ جزء درشت (تل خاک و گودال حذف شد)، همهٔ خط‌ها راست (j=0):
 ۱ سنگ تکیه‌گاه: مکعب‌گونهٔ خاکستری گرم ۲۶×۲۰، پایه روی زمین (y=8)؛ سه پله (#7f7968 / #a59f8c / #58533f)؛ نوار روشن چپ، نوار تیره راست، داخل جزء.
 ۲ میلهٔ فلزی مایل قرمز (رنگ‌مایه ≈۴°؛ ≥۳۵° از سنگ ۴۴° و از سکو ۲۱۳°) ۱۳ پهن، از ۳۳- تا ۴۰ حول لولا؛ سه پله (#e8483c / #ff8a78 / #a82a24)؛ دستگیرهٔ زرد تخت.
    کف میله ۵٫۵ واحد در تکیه‌گاه فرو می‌رود (هم‌پوشان).
 ۳ تخته‌سنگ بار کرم (#ecdcb4 / #fbf2da / #c2ae85) هفت‌ضلعی روی سر کوتاه میله؛ پایینش ۵ واحد پشت میله می‌رود (هم‌پوشان ۵).
 پین زرد روی لولا. حرکت: میله+سنگ حول لولا از ۸- تا ۰ درجه، ۱٫۸ ثانیه، یک‌بار؛ بدون حلقهٔ بیکار.
"""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/excavation'

S_B, S_L, S_D = '#efe7d3', '#fffcf1', '#c7bb9b'     # بار: تخته‌سنگ کرم روشن
F_B, F_L, F_D = '#c9b68a', '#e6d8ae', '#8f7d52'     # سنگ تکیه‌گاه: ماسه‌سنگ
B_B, B_L, B_D = '#e8483c', '#ff8a78', '#a82a24'     # دیلم قرمز
YEL = '#ffd84d'
GY = 8
ANG = 26
PX = -7.5
PIV = (PX, -37.0)
BW = 10.0
L0, L1 = -48, 62
REST = -8
XF = (1.0, 0.0, 4.0)


def flat(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def clip_x(pts, x0):
    """بخشی از چندضلعی محدب که x ≥ x0 است (سایهٔ تیز داخل جزء)."""
    out = []; n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]; ia, ib = a[0] >= x0, b[0] >= x0
        if ia: out.append(a)
        if ia != ib:
            t = (x0 - a[0]) / (b[0] - a[0]); out.append((x0, a[1] + t * (b[1] - a[1])))
    return out


def clip_x_l(pts, x1):
    """بخشی که x ≤ x1 است."""
    return clip_x([(-x, y) for x, y in pts][::-1], -x1) and [(-x, y) for x, y in clip_x([(-x, y) for x, y in pts][::-1], -x1)]


def pebble(p, cx, cy, r, col=(F_B, F_L, F_D)):
    pts = [(cx - r, cy), (cx - r * .85, cy - r * .8), (cx - r * .2, cy - r * 1.2), (cx + r * .7, cy - r * 1.0), (cx + r * 1.1, cy - r * .3), (cx + r * 1.0, cy)]
    p.shape(pts, col[0], PART, j=0, step=99)
    flat(p, [(cx - r * .5, cy - r * .6), (cx - r * .2, cy - r * .95), (cx + r * .1, cy - r * .85), (cx - r * .1, cy - r * .45)], col[1])


def build():
    p = Pen('excavation', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((-52, 22), (72, -22)), dot=(74, -8)); p.xf = XF
    f = rot(PIV[0], PIV[1], ANG)
    P = lambda pts: TP(f, [(x, y) for x, y in pts])
    p.tipshadow(PX, GY + 1, 30); p.foot_tip(PX, GY, 24)
    pebble(p, -62, GY, 11); pebble(p, -42, GY + 3, 8)
    ful = [(PX - 32, GY), (PX - 31, -6), (PX - 23, -17), (PX - 10, -26), (PX + 10, -26), (PX + 23, -17), (PX + 31, -6), (PX + 32, GY)]
    p.shape(ful, F_B, OUT, j=0, step=6)
    flat(p, [(PX - 32, GY), (PX - 31, -6), (PX - 23, -17), (PX - 10, -26), (PX - 4, -26), (PX - 17, -10), (PX - 21, GY)], F_L)
    flat(p, [(PX + 16, -22), (PX + 23, -17), (PX + 31, -6), (PX + 32, GY), (PX + 17, GY)], F_D)
    p.stroke(ful, OUT, j=0, step=6)
    py = 0; QX = 0
    with layer(p, 'bar'):
        bar = P([(QX - 50, py - BW), (QX + 58, py - BW), (QX + 58, py + BW), (QX - 50, py + BW)])
        p.shape(bar, B_B, PART, j=0, step=6, clip=False)
        flat(p, P([(QX - 44, py - BW + 3), (QX + 44, py - BW + 3), (QX + 44, py - BW + 7.5), (QX - 44, py - BW + 7.5)]), B_L)
        flat(p, P([(QX - 44, py + BW - 7.5), (QX + 55, py + BW - 7.5), (QX + 55, py + BW - 3), (QX - 44, py + BW - 3)]), B_D)
        flat(p, P([(QX + 40, py - 4.5), (QX + 49, py - 4.5), (QX + 49, py + 4.5), (QX + 40, py + 4.5)]), YEL)
        hook = P([(QX + 52, py - BW), (QX + 62, py - BW + 2), (QX + 70, py + BW + 6), (QX + 64, py + BW + 14), (QX + 57, py + BW + 6), (QX + 52, py + BW)])
        p.shape(hook, B_B, PART, j=0, step=6, clip=False)
        rock = [(QX - 58, py + 2), (QX - 66, py - 14), (QX - 60, py - 34), (QX - 46, py - 48), (QX - 28, py - 50), (QX - 14, py - 38), (QX - 8, py - 20), (QX - 8, py + 2)]
        rk = P(rock)
        p.shape(rk, S_B, OUT, j=0, step=6, clip=False)
        flat(p, P(clip_x_l(rock, QX - 48)), S_L)
        flat(p, P(clip_x(rock, QX - 20)), S_D)
        p.ln(f((QX - 46, py - 48)), f((QX - 38, py - 26)), INNER, NAVY, j=0); p.ln(f((QX - 38, py - 26)), f((QX - 58, py + 2)), INNER, NAVY, j=0)
        p.stroke(rk, OUT, j=0, step=6)
        disc(p, PIV[0], PIV[1], 3.6, YEL)
    return p


def rot_states(p, steps=(REST, REST / 2, 0)):
    return steps


if __name__ == '__main__':
    p = build()
    hm = p.X(PIV)
    lift = abs(math.sin(math.radians(ANG)) - math.sin(math.radians(ANG + REST))) * 30
    r = finish(p, 'excavation', None, motion={'bar': dict(offsets=[(0, 0), (0, lift)])}, out=OUTD, shots=SHOTS)
    # سنجش واقعی چرخش (کیت فقط چرخش ۳۶۰ را می‌شناسد)
    import station_kit as K_
    import numpy as np
    from scipy.ndimage import distance_transform_edt as edt
    A = lambda im: im[..., 3] > 128
    i, j = p.layers['bar']; body = ''.join(p.o[i:j]); dsf = 4
    top = A(K_._shot(K_._poly(p.padtop), dsf)); fixed, _ = K_._split_layers(p)
    U = A(K_._shot(fixed, dsf)); st = r['spec']['stand']
    sx, sy = (100 * K_.K + st[0]) * dsf, (150 * K_.K + st[1]) * dsf
    fig = K_._place_fig(top.shape, sx, sy, dsf)
    cols = top.any(0); low = np.where(cols, top.shape[0] - 1 - np.argmax(top[::-1], 0), -1)
    allowed = cols[None, :] & (np.arange(top.shape[0])[:, None] <= low[None, :])
    worst = 99; outpx = 0; xm = 99; px = np.where(top.any(0))[0]
    for a in (REST, REST * .5, 0):
        Um = A(K_._shot('<g transform="rotate(%s %s %s)">%s</g>' % (a, hm[0], hm[1], body), dsf))
        outpx += float((Um & ~allowed).sum()) / dsf ** 2
        xs = np.where(Um.any(0))[0]; xm = min(xm, (xs.min() - px.min()) / dsf, (px.max() - xs.max()) / dsf)
        worst = min(worst, float(edt(~fig)[Um].min()) / dsf)
    rot_chk = dict(states=[REST, REST / 2, 0], out_px=round(outpx, 1), x_margin=round(xm, 1), stand_to_motion=round(worst, 1), ok=bool(outpx == 0 and xm >= 8 and worst >= 10))
    sp = r['spec']
    sp['motion_spec'] = {'node_excavation_bar': dict(
        rotate_about=[round(v, 1) for v in hm], angle_deg=[REST, 0], dir='از %d تا 0 درجه (ساعتگرد در svg = سر بلند میله پایین می‌آید و سنگ بالا می‌رود)' % REST,
        duration_s=1.8, repeat=1, easing='ease-out',
        note='میله و سنگ بار هم‌حرکت‌اند و حول لولا (پین زرد روی سنگ تکیه‌گاه) می‌چرخند؛ سنگ ≈ %.1f واحد بالا می‌آید؛ حالت ایستا = پایان؛ فقط هنگام رسیدن؛ بدون حلقهٔ بیکار.' % lift),
        'reduced_motion': 'ایستا در وضع پایان (زاویه ۰)', 'rotation_check': rot_chk}
    (OUTD / 'excavation.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ROT', json.dumps(rot_chk))
