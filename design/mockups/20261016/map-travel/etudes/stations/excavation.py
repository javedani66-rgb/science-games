#!/usr/bin/env python3
"""ایستگاه M04 «گودبرداری» (سرزمین شهر، سکوی آبی-فولادی ۲۱۳°). تصمیم مالک: میلهٔ فلزی روی سنگ تکیه‌گاه که سنگی را بالا می‌آورد.
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

S_B, S_L, S_D = '#ecdcb4', '#fbf2da', '#c2ae85'     # تخته‌سنگ بار
F_B, F_L, F_D = '#7f7968', '#a59f8c', '#58533f'     # سنگ تکیه‌گاه
B_B, B_L, B_D = '#e8483c', '#ff8a78', '#a82a24'     # میلهٔ فلزی
YEL = '#ffd84d'
GY = 8
ANG = 12
PIV = (0.0, -23.0)
BW = 6.5
L0, L1 = -34, 32
REST = -8
XF = (1.5, 24, -6)


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


def build():
    p = Pen('excavation', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    f = rot(PIV[0], PIV[1], ANG)
    P = lambda pts: TP(f, [(x, y) for x, y in pts])      # نقطه‌های محلی (نسبت به لولا) -> جهان
    p.tipshadow(0, GY + 1, 19); p.tipshadow(28, GY + 1, 5)
    p.foot_tip(0, GY, 15); p.foot_tip(28, GY, 5)
    ful = [(-17, -22), (17, -22), (17, GY), (-17, GY)]
    p.shape(ful, F_B, OUT, j=0, step=6)
    flat(p, [(-17, -22), (-12, -22), (-12, GY), (-17, GY)], F_L)
    flat(p, [(11, -22), (17, -22), (17, GY), (11, GY)], F_D)
    p.stroke(ful, OUT, j=0, step=6)
    with layer(p, 'bar'):
        rock = [(-32, -1.5), (-33, -10), (-30, -19), (-23, -25), (-14, -27), (-6, -23), (-1, -15), (-1, -1.5)]
        rk = P(rock)
        p.shape(rk, S_B, OUT, j=0, step=6, clip=False)
        flat(p, P(clip_x_l(rock, -26)), S_L)
        flat(p, P(clip_x(rock, -7)), S_D); p.stroke(rk, OUT, j=0, step=6)
        bar = P([(L0, -BW), (L1, -BW), (L1, BW), (L0, BW)])
        p.shape(bar, B_B, PART, j=0, step=6, clip=False)
        flat(p, P([(L0 + 5, -BW + 2.6), (L1 - 10, -BW + 2.6), (L1 - 10, -BW + 5), (L0 + 5, -BW + 5)]), B_L)
        flat(p, P([(L0 + 5, BW - 5), (L1 - 3, BW - 5), (L1 - 3, BW - 2.6), (L0 + 5, BW - 2.6)]), B_D)
        flat(p, P([(25, -3.2), (30, -3.2), (30, 3.2), (25, 3.2)]), YEL)
        disc(p, PIV[0], PIV[1], 3.4, YEL)
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
