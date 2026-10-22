#!/usr/bin/env python3
"""ایستگاه M06 «اتاق ابزار» (شهر، پالت city)، دور ۵: میز کار پهن و کوتاه با دو ابزار درشت. مرکز سکو x=0، کف y=8، عرض کل ≈۶۵٪.
 ۱) میز کار چوب کرم-کهربایی (#e8b866/#fbd990/#b8843a): رویهٔ ضخیم x=±60، دو پایه (±49)، پیشانی (کشو) تیره‌تر با دستگیرهٔ زرد.
 ۲) چکش (چپ، روی میز): دستهٔ فیروزه‌ای #2fb5a8 قائم، سر فولادی (#d4dce8/#f6f9fd/#94a2b8) با چنگک به چپ.
 ۳) قیچی (راست، لایهٔ node_tool_room_scissors): دو تیغهٔ فولادی بازشده V و دو دستهٔ حلقه‌ای قرمز #e2553d؛ پیچ مرکزی. هر نیمه زیرگروه
    node_tool_room_scissors_a / _b (چرخش حول پیچ). ایستادن روی دو حلقه.
 فاصلهٔ ابزارها ≥ ۱۲ واحد؛ بدون انبر و آچار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tool_room'

B_B, B_L, B_D = '#e8b866', '#fbd990', '#b8843a'      # میز
A_B, A_L, A_D = '#cf9a4a', '#cf9a4a', '#9a6a26'      # پیشانی
F_B, F_L, F_D = '#d4dce8', '#f6f9fd', '#94a2b8'      # فولاد
T_B, T_L, T_D = '#2fb5a8', '#7fe0d4', '#1f7f77'      # دستهٔ چکش
H_B = '#e2553d'; H_L = '#ff9b84'
YEL = '#ffd84d'
TOPY0, TOPY1 = -34, -20
HX = -34                       # محور چکش
PIV = (34, -80)                # پیچ قیچی


def poly(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): poly(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r * p.xf[0], col))


def part(p, pts, col, sw=PART, step=6):
    p.shape(pts, col, sw, j=.12, step=step, clip=False)


def bar(a, b, w0, w1):
    dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
    return [(a[0] + nx * w0 / 2, a[1] + ny * w0 / 2), (b[0] + nx * w1 / 2, b[1] + ny * w1 / 2),
            (b[0] - nx * w1 / 2, b[1] - ny * w1 / 2), (a[0] - nx * w0 / 2, a[1] - ny * w0 / 2)]


def build():
    p = Pen('tool_room', 'city'); pad(p, line=((60, 14), (76, 10)), tri=((-74, -10), (-66, 12)), dot=(70, -16)); p.xf = (1.0, 0, 8)
    p.tipshadow(0, 10, 60); p.foot_tip(0, 9, 34)
    # ۱) میز کار
    for x in (-49, 49):
        part(p, [(x - 7, -24), (x + 7, -24), (x + 7, 8), (x - 7, 8)], B_B)
        rect(p, x - 3.5, -18, x - 0.5, 3, B_L); rect(p, x + 2, -18, x + 4.5, 3, B_D)
    part(p, [(-43, -22), (43, -22), (43, -8), (-43, -8)], A_B)
    rect(p, -36, -14.5, 36, -11.5, A_D)
    disc(p, 0, -15, 3.2, YEL)
    part(p, [(-62, TOPY0), (62, TOPY0), (62, TOPY1), (-62, TOPY1)], B_B)
    rect(p, -54, TOPY0 + 3.5, 54, TOPY0 + 7, B_L); rect(p, -54, TOPY1 - 6, 54, TOPY1 - 3, B_D)
    # ۲) چکش
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="12" ry="3" fill="#10083a" opacity=".22"/>' % p.X((HX, TOPY0 + 1)))
    part(p, [(HX - 6.5, -92), (HX + 6.5, -92), (HX + 6.5, TOPY0 + 2), (HX - 6.5, TOPY0 + 2)], T_B)
    rect(p, HX - 3, -88, HX - 0.5, TOPY0 - 4, T_L); rect(p, HX + 2, -88, HX + 4, TOPY0 - 4, T_D)
    head = [(HX + 22, -116), (HX + 22, -96), (HX - 2, -96), (HX - 26, -86), (HX - 12, -102), (HX - 12, -116)]
    part(p, head, F_B)
    rect(p, HX - 6, -112, HX + 17, -108, F_L); rect(p, HX + 14, -110, HX + 19, -99, F_D)
    # ۳) قیچی
    ra, rb = (PIV[0] + 14, -51), (PIV[0] - 14, -51)
    ta = (PIV[0] - 1.5 * 14, PIV[1] - 1.5 * 29 + 0); tb = (PIV[0] + 1.5 * 14, PIV[1] - 1.5 * 29 + 0)
    with layer(p, 'scissors'):
        for nm, tip, ring, hx in (('a', ta, ra, 1), ('b', tb, rb, -1)):
            p.raw('<g id="node_tool_room_scissors_%s">' % nm)
            part(p, bar(PIV, ring, 11, 11), H_B)
            part(p, ell(ring[0], ring[1], 11, 11, 0, 360, 20), H_B, PART, 99)
            p.fill(ell(ring[0], ring[1], 4.5, 4.5, 0, 360, 14), '#c9a35c')
            part(p, bar(PIV, tip, 15, 5), F_B)
            p.raw('</g>')
        disc(p, PIV[0], PIV[1], 5, YEL)
    return p


def swing_ok(p, ang=12, dsf=4):
    """بازشدن بیشتر قیچی (هر نیمه ±ang درجه حول پیچ) از سکو بیرون نزند و از چکش دور بماند."""
    import numpy as np, station_kit as K_
    A = lambda im: im[..., 3] > 128
    i, j = p.layers['scissors']; body = ''.join(p.o[i:j])
    top = A(K_._shot(K_._poly(p.padtop), dsf)); hm = p.X(PIV); U = np.zeros_like(top)
    for a in (-ang, 0, ang): U |= A(K_._shot('<g transform="rotate(%s %s %s)">%s</g>' % (a, hm[0], hm[1], body), dsf))
    xs = np.where(U.any(0))[0]
    return dict(x_right_to_pad_px=round(float(np.where(top.any(0))[0].max() - xs.max()) / dsf, 1))


if __name__ == '__main__':
    p = build(); hm = p.X(PIV)
    r = finish(p, 'tool_room', None, motion={'scissors': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['swing_check'] = swing_ok(p)
    sp['motion_spec'] = {'node_tool_room_scissors': dict(center=[round(v, 1) for v in hm], parts=['node_tool_room_scissors_a', 'node_tool_room_scissors_b'],
        angle_deg='هر نیمه ±۱۲ حول پیچ: بسته‌تر → بازتر → حالت ایستا', dur_s=1.2, once=True,
        note='فقط قیچی؛ میز و چکش ثابت؛ حالت ایستا = بازِ V؛ هنگام رسیدن؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'قیچی ایستا'}
    (OUTD / 'tool_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
