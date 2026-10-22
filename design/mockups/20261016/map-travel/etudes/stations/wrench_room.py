#!/usr/bin/env python3
"""ایستگاه E05 «اتاق آچار» (شهر، پالت city)، دور ۵: یک آچار تخت دوسر بزرگِ خوابیده، افقی-مایل، وسط سکو. بدون پیچ و مهره.
طرح (مختصات محلی: مبدأ = مرکز سر بزرگ، محور +x به سمت سر کوچک؛ سپس ۱۴- درجه چرخانده می‌شود):
 ۱) سایهٔ تماس زیر آچار + ضخامت (نسخهٔ تیره‌تر، ۶ واحد پایین‌تر) تا خوابیده روی سکو دیده شود.
 ۲) بدنهٔ فولادی کرم یک چندضلعی (خط OUT): سر چپ دایره r=24 با دهانهٔ شش‌ضلعی (پهنای ۱۷)، دسته پهنای ۱۶، سر راست r=18 با دهانهٔ ۱۲. فاصلهٔ مرکزها ۷۴.
    پایه #efe6d0، روشن #fffaf0، تیره #b9ad90؛ رنگ‌مایهٔ گرم، دور از سکوی آبی-خاکستری.
 ۳) نوار روشن روی دسته و سر، نوار تیرهٔ تیز زیر دسته، سوراخ آویز بیضی وسط دسته (رنگ رویهٔ سکو).
 عرض ≈۶۴٪ سکو. لایهٔ متحرک node_wrench_room_wrench = کل آچار، چرخش ±۸° حول مرکز آچار؛ حالت ایستا = ۰ (همین شکل)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
import station_kit as K_
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/wrench_room'
M_B, M_L, M_D = '#efe6d0', '#fffaf0', '#b9ad90'
EXT = '#a59878'
PADTOP = '#5b7390'
R1, R2, D, HW = 29, 21, 68, 10           # شعاع‌ها، فاصلهٔ مرکزها، نیم‌پهنای دسته
S1, S2 = 12.5, 9.5                         # نیم‌پهنای دهانه‌ها
ANG = -14
MID = (0, -8)                           # مرکز آچار (جهان)
LO = (D + R2 - R1) / 2                  # مرکز طولی محلی (از مرکز سر بزرگ)
O = (MID[0] - LO * math.cos(math.radians(ANG)), MID[1] - LO * math.sin(math.radians(ANG)))


def arc(cx, cy, r, t0, t1, n=14):
    return [(cx + r * math.cos(math.radians(t0 + (t1 - t0) * i / n)), cy + r * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]


def body_local():
    a1 = math.degrees(math.asin(HW / R1)); b1 = math.degrees(math.asin(S1 / R1))
    a2 = math.degrees(math.asin(HW / R2)); b2 = math.degrees(math.asin(S2 / R2))
    pts = arc(0, 0, R1, -a1, -(180 - b1))                              # سر بزرگ، بالا
    pts += [(-6, -S1), (2, 0), (-6, S1)]                               # دهانهٔ شش‌ضلعی
    pts += arc(0, 0, R1, 180 - b1, a1)                                 # پایین
    pts += arc(D, 0, R2, 180 - a2, b2)                                 # سر کوچک، پایین
    pts += [(D + R2 * math.cos(math.radians(b2)), S2), (D + 8, S2), (D + 2, 0), (D + 8, -S2), (D + R2 * math.cos(math.radians(b2)), -S2)]
    pts += arc(D, 0, R2, -b2, -(180 - a2))                             # بالا
    return pts


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build():
    p = Pen('wrench_room', 'city'); pad(p, line=((60, 14), (76, 10)), tri=((-74, -10), (-66, 12)), dot=(70, -16)); p.xf = (1.0, 0, 0)
    f = rot(O[0], O[1], ANG); L = lambda pts: TP(f, pts)
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="62" ry="12" fill="#10083a" opacity=".22"/>' % p.X((MID[0] + 3, MID[1] + 18)))
    p.foot_tip(MID[0], MID[1] + 14, 34)
    with layer(p, 'wrench'):
        bl = body_local()
        poly(p, [(x + 4, y + 7) for x, y in L(bl)], '#10083a', .3)
        body = L(bl)
        p.shape(body, M_B, PART, j=.1, step=6, clip=False)
        poly(p, L([(34, -HW + 4), (D - 22, -HW + 4), (D - 22, -HW + 7.5), (34, -HW + 7.5)]), M_L)             # نور دسته
        poly(p, L([(34, HW - 8), (D - 22, HW - 8), (D - 22, HW - 4), (34, HW - 4)]), M_D)                     # سایهٔ تیز دسته
        poly(p, L([(-16, -R1 + 8), (0, -R1 + 8), (0, -R1 + 11.5), (-16, -R1 + 11.5)]), M_L)                  # نور سر بزرگ
        poly(p, L([(D - 12, -R2 + 7), (D + 4, -R2 + 7), (D + 4, -R2 + 10.5), (D - 12, -R2 + 10.5)]), M_L)       # نور سر کوچک
        hole = [(x, y) for x, y in arc(D / 2, 0, 1, 0, 360, 16)]
        hole = [(D / 2 + 7 * math.cos(math.radians(t)), 3.2 * math.sin(math.radians(t))) for t in range(0, 360, 24)]
        p.shape(L(hole), PADTOP, INNER, j=.05, step=99, clip=False)
    return p


def swing_check(p, angs=(-8, 0, 8), dsf=4):
    import numpy as np
    from scipy.ndimage import distance_transform_edt as edt
    A = lambda im: im[..., 3] > 128
    i, j = p.layers['wrench']; body = ''.join(p.o[i:j])
    top = A(K_._shot(K_._poly(p.padtop), dsf)); sil = top | A(K_._shot(K_._poly(K_._wall_pts(p)), dsf))
    cols = sil.any(0); low = np.where(cols, sil.shape[0] - 1 - np.argmax(sil[::-1], 0), -1)
    allowed = cols[None, :] & (np.arange(sil.shape[0])[:, None] <= low[None, :])
    hm = p.X(MID); U = np.zeros_like(sil)
    for a in angs: U |= A(K_._shot('<g transform="rotate(%s %s %s)">%s</g>' % (a, hm[0], hm[1], body), dsf))
    xs = np.where(U.any(0))[0]; px = np.where(top.any(0))[0]
    reg = allowed; dd = edt(reg) / dsf
    return dict(out_px=round(float((U & ~allowed).sum()) / dsf ** 2, 1), x_margin=round(float(min(xs.min() - px.min(), px.max() - xs.max())) / dsf, 1),
                min_inside=round(float(dd[U].min()), 1))


if __name__ == '__main__':
    p = build(); hm = p.X(MID)
    r = finish(p, 'wrench_room', None, motion={'wrench': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sc = swing_check(p); sp = r['spec']
    sp['motion_spec'] = {'node_wrench_room_wrench': dict(center=[round(v, 1) for v in hm], pivot='مرکز آچار', rotate_deg='0 → -8 → +8 → 0 (حالت ایستا 0)', dur_s=1.6, once=True,
                                                         note='کل آچار اندکی تاب می‌خورد و برمی‌گردد؛ فقط هنگام رسیدن؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'ایستا'}
    sp['swing_check'] = sc
    (OUTD / 'wrench_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print('SWING', sc, 'MID', hm)
