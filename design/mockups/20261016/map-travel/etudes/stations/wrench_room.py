#!/usr/bin/env python3
"""ایستگاه E05 «اتاق آچار» (سرزمین شهر، سکوی city).
طرح قطعه‌به‌قطعه (همه در مختصات محلی آچار: مبدأ = مرکز دهانه، محور +x به سمت دسته؛ سپس ۶۶° چرخانده می‌شود):
 ۱ سایهٔ تماس زیر ته دسته (بیضی) + foot_tip
 ۲ بدنهٔ فلزی (سرِ دهانه‌باز + گردن + دسته) یک چندضلعی؛ کرم-نقره‌ای: پایه #efe6d0، روشن #fffaf0، تیره #b9ad90؛ خط OUT
   سر: نیم‌ارتفاع ۲۵، دو شاخهٔ دهانه هر کدام ۱۷ پهن؛ دهانهٔ شش‌ضلعی ۱۶ پهن (نیم‌ارتفاع ۸)؛ دسته ۱۷ پهن، طول کل ۱۱۲ (≈ ۲٫۵ برابر پهنای سر)
   نور: یک نوار ۳٫۵ در شاخهٔ سمت روشن؛ سایه: نوار تیز سمت راست، سپس خط دور دوباره
 ۳ غلاف دسته (بنفش، رنگ‌مایه ≥ ۳۵° از سکو): پایه #9a63e0، روشن #c4a0f5، تیره #6a3cb5؛ خط PART؛ ۱۶ تا ۹۰ در امتداد دسته، ۱۷ پهن
 ۴ سه شیار عرضی تخت تیره + یک نوار زرد تخت کوچک (تأکید) روی غلاف؛ فاصله ≥ ۷٫۵
 بدون پیچ و مهره. لایهٔ متحرک: node_wrench_room_wrench (کل آچار حول مرکز دهانه، ±۲۰° و بازگشت؛ حالت ایستا = ۰°).
 تماس: ته دستهٔ گرد روی سکو (سایه + foot_tip)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
import station_kit as K_
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/wrench_room'

M_B, M_L, M_D = '#efe6d0', '#fffaf0', '#b9ad90'
G_B, G_L, G_D = '#9a63e0', '#c4a0f5', '#6a3cb5'
YEL = '#ffd84d'
ANG = 114
LEN = 112
E = (-26, -4)                       # مرکز ته دسته (جهان)
H = (E[0] - LEN * math.cos(math.radians(ANG)), E[1] - LEN * math.sin(math.radians(ANG)))   # مرکز دهانه
HW = 9.5                          # نیم‌پهنای دسته
SL0, SL1 = 40, 112                 # غلاف از تا


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build():
    p = Pen('wrench_room', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((-62, -10), (-54, 14)), dot=(-70, -24)); p.xf = (1.0, 0, 0)
    f = rot(H[0], H[1], ANG)
    L = lambda pts: TP(f, pts)
    p.tipshadow(E[0] + 2, E[1] + 7, 13); p.foot_tip(E[0], E[1] + 5, 10)
    HH = 27
    nk = SL0 + 6
    body_l = [(-26, -HH), (6, -HH), (22, -13), (34, -HW), (nk, -HW), (nk, HW), (34, HW), (22, 13), (6, HH), (-26, HH),
              (-26, 9.5), (-12, 9.5), (-3, 0), (-12, -9.5), (-26, -9.5)]
    sl_l = [(SL0, -HW), (LEN - HW, -HW)] + ell(LEN - HW, 0, HW, HW, -90, 90, 8)[1:-1] + [(LEN - HW, HW), (SL0, HW)]
    with layer(p, 'wrench'):
        body = L(body_l)
        p.shape(body, M_B, OUT, j=.1, step=6)
        poly(p, L([(-20, 17), (2, 17), (2, 20.5), (-20, 20.5)]), M_L)                                    # نور
        poly(p, L([(-26, -HH), (6, -HH), (22, -13), (34, -HW), (nk, -HW), (nk, -3), (18, -6), (2, -19), (-26, -19)]), M_D)   # سایهٔ تیز
        p.stroke(body, OUT, j=.1, step=6)
        sl = L(sl_l)
        p.shape(sl, G_B, OUT, j=.08, step=6)
        poly(p, L([(SL0 + 8, 2.5), (LEN - 14, 2.5), (LEN - 14, 5.5), (SL0 + 8, 5.5)]), G_L)                # نور غلاف
        poly(p, L([(SL0, -HW), (LEN - HW, -HW), (LEN - HW, -3), (SL0, -3)]), G_D)                          # سایهٔ تیز غلاف
        for x in (SL0 + 22, SL0 + 33, SL0 + 44):
            poly(p, L([(x, -5), (x + 3.5, -5), (x + 3.5, 5), (x, 5)]), G_D)                                 # شیار
        poly(p, L([(SL0 + 4, -5), (SL0 + 9, -5), (SL0 + 9, 5), (SL0 + 4, 5)]), YEL)                        # نوار زرد
        p.stroke(sl, OUT, j=.08, step=6)
    return p


def swing_check(p, stand, angs=(-20, -10, 0, 10, 20), dsf=4):
    import numpy as np
    from scipy.ndimage import distance_transform_edt as edt
    A = lambda im: im[..., 3] > 128
    i, j = p.layers['wrench']; body = ''.join(p.o[i:j])
    top = A(K_._shot(K_._poly(p.padtop), dsf)); sil = top | A(K_._shot(K_._poly(K_._wall_pts(p)), dsf))
    cols = sil.any(0); low = np.where(cols, sil.shape[0] - 1 - np.argmax(sil[::-1], 0), -1)
    allowed = cols[None, :] & (np.arange(sil.shape[0])[:, None] <= low[None, :])
    hm = p.X(H); U = np.zeros_like(sil); res = {}
    for a in angs:
        im = A(K_._shot('<g transform="rotate(%s %s %s)">%s</g>' % (a, hm[0], hm[1], body), dsf)); U |= im
        # ته دسته پایین‌ترین نقطه؛ ارتفاع آن از سطح
    outside = U & ~allowed
    xs = np.where(U.any(0))[0]; px = np.where(top.any(0))[0]
    sx, sy = (100 * K_.K + stand[0]) * dsf, (150 * K_.K + stand[1]) * dsf
    fig = K_._place_fig(U.shape, sx, sy, dsf)
    d = edt(~fig)[U].min() / dsf
    # بالازدگی از لبهٔ رویه (پایین/چپ/راست)
    reg = allowed; dd = edt(reg) / dsf
    return dict(out_px=round(float(outside.sum()) / dsf ** 2, 1), x_margin=round(float(min(xs.min() - px.min(), px.max() - xs.max())) / dsf, 1),
                min_inside=round(float(dd[U].min()), 1), stand_to_swing=round(float(d), 1))


if __name__ == '__main__':
    p = build(); hm = p.X(H)
    import numpy as np
    stand = tuple(float(v) for v in (sys.argv[1:3] or (38, 22)))
    r = finish(p, 'wrench_room', stand, motion={'wrench': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sc = swing_check(p, stand)
    sp = r['spec']
    sp['motion_spec'] = {'node_wrench_room_wrench': dict(center=[round(v, 1) for v in hm], pivot='مرکز دهانهٔ آچار', rotate_deg='0 → -20 → +20 → 0 (حالت ایستا 0)', dur_s=1.6, once=True,
                                                         note='کل آچار حول مرکز دهانه می‌چرخد و برمی‌گردد؛ فقط هنگام رسیدن؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'ایستا'}
    sp['swing_check'] = sc
    (OUTD / 'wrench_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
    print('SWING', sc, 'H', hm)
