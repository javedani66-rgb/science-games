#!/usr/bin/env python3
"""ایستگاه M04 «گودبرداری» (سرزمین شهر، سکوی آبی-فولادی ۲۱۳°). تصمیم مالک: میلهٔ فلزی روی سنگ تکیه‌گاه که سنگی را از گودال بالا می‌آورد.
نمای جانبی؛ حالت ایستا = پایان حرکت (سر بلند میله پایین آمده و سنگ بالا رفته و در بالاست).

طرح قطعه‌به‌قطعه (واحد symbol، مرکز سکو (0,0)، y منفی = بالا؛ زمین y=8):
 ۱ سایهٔ تماس: بیضی زیر سنگ تکیه‌گاه و زیر گودال (tipshadow)
 ۲ تل خاک: ذوزنقهٔ گرد پشت گودال، خاکی ۳ پله (#9a6636 / #c08850 / #5a3a22)، دور PART
 ۳ گودال: لبهٔ خاکی (بیضی ۲۴×۹) + سوراخ تیره (بیضی تخت ۱۸×۶ بی‌خط)
 ۴ سنگ تکیه‌گاه: چندضلعی ۲۶ پهن × ۲۲ بلند، پایه روی زمین؛ ماده «سنگ» ۳ پله (#d8c3a0 / #f2e6cc / #ad9570)؛ نور چپ، سایهٔ تیز راست داخل جزء، دور دوباره
 ۵ لایهٔ متحرک node_excavation_bar (حول لولا = بالای سنگ تکیه‌گاه):
    ۵a میلهٔ فلزی رنگی: مستطیل ۱۵ پهن، سر چپ (کوتاه) زیر سنگ، سر راست (بلند) روی زمین؛ ۳ پله (#e0553a / #ff9a6c / #9c2f1c)؛ نوار زرد دستگیره (تخت)
    ۵b سنگ بار: چندضلعی ۹ ضلعی ≈ ۳۴ پهن روی سر کوتاه میله؛ ماده سنگ (همان ۳ پله)؛ دو ترک تخت
    ۵c پین زرد روی لولا (r ۲٫۶) تخت
 حرکت: لایه حول لولا از ۸- درجه (سر بلند بالا، سنگ پایین‌تر) تا ۰ (ایستا) می‌چرخد؛ ۱٫۸ ثانیه، ۳ تکرار؛ بدون حلقهٔ بیکار.
"""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/excavation'

# سنگ
S_B, S_L, S_D = '#d8c3a0', '#f2e6cc', '#ad9570'
# میلهٔ رنگ‌شدهٔ فلزی
B_B, B_L, B_D = '#e0553a', '#ff9a6c', '#9c2f1c'
# خاک
E_B, E_L, E_D = '#9a6636', '#c08850', '#5a3a22'
YEL = '#ffd84d'

GY = 8                       # زمین
ANG = 20                     # زاویهٔ ایستای میله (درجه، ساعتگرد در svg = سر راست پایین)
PIV = (-12.0, -14.0)         # لولا
BW = 8.0                     # نیم‌پهنای میله
L0, L1 = -44, 31             # سر کوتاه (چپ) و سر بلند (راست)
BC = (-28.0, -41.0)          # مرکز سنگ بار
BRX, BRY = 19, 17
REST = -8                    # شروع حرکت


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


def build():
    p = Pen('excavation', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.1, 2, 4)
    f = rot(PIV[0], PIV[1], ANG)
    p.tipshadow(-12, GY + 1, 20); p.tipshadow(-42, GY + 4, 20); p.tipshadow(17, GY + 1, 7)
    p.foot_tip(-12, GY, 14); p.foot_tip(-42, GY + 4, 18); p.foot_tip(17, GY, 6)
    # ۲) تل خاک (پشت گودال)
    mound = [(-66, 3), (-62, -8), (-52, -19), (-40, -19), (-30, -8), (-26, 3)]
    p.shape(mound, E_B, PART, j=.3, step=7)
    flat(p, [(-60, -3), (-57, -10), (-51, -15), (-48, -12), (-54, -4)], E_L)
    flat(p, clip_x(mound, -41), E_D, .55); p.stroke(mound, PART, j=.3, step=7)
    # ۳) گودال: لبهٔ خاکی + سوراخ
    rim = ell(-42, 9, 19, 7.5, 0, 360, 24)
    p.shape(rim, E_L, PART, j=.25, step=7)
    flat(p, ell(-42, 10, 12.5, 4, 0, 360, 24), E_D)
    # ۴) سنگ تکیه‌گاه
    ful = [(-30, GY), (-32, -4), (-27, -14), (-14, -18), (-1, -14), (4, -4), (2, GY)]
    p.shape(ful, S_B, OUT, j=.3, step=7)
    flat(p, [(-28, 4), (-28, -5), (-25, -11), (-21, -11), (-24, -5), (-24, 4)], S_L)
    flat(p, clip_x(ful, -4), S_D, .9); p.stroke(ful, OUT, j=.3, step=7)
    # ۵) لایهٔ متحرک: میله + سنگ بار (روی میله) + پین
    with layer(p, 'bar'):
        bar = TP(f, [(L0, -BW), (L1, -BW), (L1, BW), (L0, BW)])
        p.shape(bar, B_B, PART, j=.15, step=6, clip=False)
        flat(p, TP(f, [(L0 + 6, -BW + 3.6), (L1 - 14, -BW + 3.6), (L1 - 14, -BW + 7.1), (L0 + 6, -BW + 7.1)]), B_L)       # نور
        flat(p, TP(f, [(L0 + 6, BW - 5.6), (L1 - 4, BW - 5.6), (L1 - 4, BW - 3.2), (L0 + 6, BW - 3.2)]), B_D)             # سایهٔ تیز زیر
        flat(p, TP(f, [(22, -4.2), (26.5, -4.2), (26.5, 4.2), (22, 4.2)]), YEL)                                            # دستگیرهٔ زرد
        rock = [(BC[0] + BRX * math.cos(math.radians(a)) * k, BC[1] + BRY * math.sin(math.radians(a)) * k)
                for a, k in ((0, 1), (40, .96), (80, 1.02), (125, .95), (165, 1.0), (200, .98), (245, 1.03), (290, 1.0), (330, .95))]
        p.shape(rock, S_B, OUT, j=.4, step=7, clip=False)
        flat(p, [(BC[0] - 14, BC[1] + 3), (BC[0] - 14, BC[1] - 6), (BC[0] - 10, BC[1] - 12), (BC[0] - 10, BC[1] - 5), (BC[0] - 11, BC[1] + 5)], S_L)
        flat(p, clip_x(rock, BC[0] + 7), S_D, .9); p.stroke(rock, OUT, j=.4, step=7)
        p.ln((BC[0] + 3, BC[1] - 12), (BC[0] + 1, BC[1] - 1), INNER, S_D, j=0)
        p.ln((BC[0] + 1, BC[1] - 1), (BC[0] - 6, BC[1] + 5), INNER, S_D, j=0)
        disc(p, PIV[0], PIV[1], 3.2, YEL)
    return p


def rot_states(p, steps=(REST, REST / 2, 0)):
    return steps


if __name__ == '__main__':
    p = build()
    hm = p.X(PIV)
    lift = abs(math.sin(math.radians(ANG)) - math.sin(math.radians(ANG + REST))) * 26
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
        duration_s=1.8, repeat=3, easing='ease-out',
        note='میله و سنگ بار هم‌حرکت‌اند و حول لولا (پین زرد روی سنگ تکیه‌گاه) می‌چرخند؛ سنگ ≈ %.1f واحد بالا می‌آید؛ حالت ایستا = پایان؛ فقط هنگام رسیدن؛ بدون حلقهٔ بیکار.' % lift),
        'reduced_motion': 'ایستا در وضع پایان (زاویه ۰)', 'rotation_check': rot_chk}
    (OUTD / 'excavation.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ROT', json.dumps(rot_chk))
