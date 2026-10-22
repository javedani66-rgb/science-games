#!/usr/bin/env python3
"""ایستگاه E05 «اتاق آچار» (شهر، پالت city)، دور ۶: آچار تخت ایستادهٔ سه‌بعدی (¾، ضخامت واقعی) + مهرهٔ شش‌ضلعی زرد درشت در دهانه + جعبهٔ ابزار قرمز.
اجزای درشت (۳): ۱) آچار: نیم‌رخ بیرون‌کشیده با عمق (12,-8)؛ رخ جلو #cfdcf4، رویه #f6f9ff، پهلوی راست #7f86c8؛ سر دایره r=34، دهانهٔ باز رو به بالا
 (پهنا ۳۴)، دستهٔ پهنای ۳۰؛ نوار برق و نوار سایهٔ دسته؛ سوراخ آویز. ۲) مهره (لایهٔ node_wrench_room_nut): شش‌ضلعی زرد (#ffd84d / رویه #ffe98f / پهلو #c9891a) با سوراخ،
 در دهانه؛ حرکت: از ۱۶ واحد بالاتر به دهانه می‌نشیند. ۳) جعبهٔ ابزار قرمز (#e2553d/#ff9b84/#9c2a1a) با دستهٔ زرد و قفل زرد. سایهٔ تماس زیر هر دو."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from r6lib import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/wrench_room'
F_, T_, S_, M_ = '#cfdcf4', '#f6f9ff', '#7f86c8', '#a9b4e6'
Y_F, Y_T, Y_S = '#ffd84d', '#ffe98f', '#c9891a'
R_F, R_T, R_S = '#e2553d', '#ff9b84', '#9c2a1a'
D = (12, -8)
CX = -26; CY = -94; RH = 36; HW = 15; SL = 18.5; BASE = 8


def arc(cx, cy, r, t0, t1, n=16):
    return [(cx + r * math.cos(math.radians(t0 + (t1 - t0) * i / n)), cy + r * math.sin(math.radians(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]


def profile():
    ty = math.degrees(math.asin(SL / RH)); hy = math.degrees(math.asin(HW / RH))
    # از لبهٔ راست دهانه، ساعت‌گرد (در SVG زاویهٔ مثبت = پایین): راست بالا → راست پایین
    jd = math.degrees(math.acos(HW / RH))
    right = arc(CX, CY, RH, -(90 - ty), jd, 22)
    left = arc(CX, CY, RH, 180 - jd, 270 - ty, 22)
    pts = right + [(CX + HW, BASE - 6), (CX + HW - 5, BASE), (CX - HW + 5, BASE), (CX - HW, BASE - 6)] + left
    pts += [(CX - SL, CY + 8), (CX + SL, CY + 8)]          # ته دهانه
    return pts


def hexf(cx, cy, w=14, h=16.2):
    return [(cx, cy - h), (cx + w, cy - h / 2), (cx + w, cy + h / 2), (cx, cy + h), (cx - w, cy + h / 2), (cx - w, cy - h / 2)]


NY = CY - 10          # مرکز مهره
def build():
    p = Pen('wrench_room', 'city'); pad(p, line=((60, 24), (76, 20)), tri=((-74, 4), (-66, 20)), dot=(72, -10)); p.xf = (1.0, 0, 0)
    p.tipshadow(CX + 6, BASE + 2, 44); p.foot_tip(CX, BASE, 26)
    p.tipshadow(38, 10, 40); p.foot_tip(38, 10, 26)
    # دهانهٔ تیره پشت مهره (لایهٔ ثابت زیر آچار)
    extrude(p, profile(), D, F_, T_, S_, mid=M_, sw=OUT, sw_in=PART)
    # نوارها روی دسته و سر
    rect(p, CX + 5, -60, CX + HW - 2, BASE - 8, M_)
    rect(p, CX - HW + 5, -62, CX - HW + 8.5, BASE - 10, '#ffffff', .9)
    rect(p, CX - RH + 8, CY - 8, CX - RH + 11.5, CY + 14, '#ffffff', .9)
    p.shape([(CX + x, BASE - 28 + y) for x, y in ell(0, 0, 5, 9, 0, 360, 16)], '#3a4c68', INNER, j=.05, step=99, clip=False)
    top_y = CY - math.sqrt(RH ** 2 - SL ** 2)
    poly(p, [(CX - SL, top_y + 3), (CX + SL, top_y + 3), (CX + SL, CY + 8), (CX - SL, CY + 8)], '#5d64a8')
    p.stroke([(CX - SL, top_y - 1), (CX - SL, CY + 8), (CX + SL, CY + 8), (CX + SL, top_y - 1)][:0] or [(CX-SL,CY+8),(CX+SL,CY+8),(CX+SL,CY+8.1)], PART)
    with layer(p, 'nut'):
        hx = hexf(CX, NY)
        extrude(p, hx, (7, -5), Y_F, Y_T, Y_S, sw=PART, sw_in=INNER)
        p.shape([(CX + x, NY + y) for x, y in ell(0, 0, 6.5, 6.5, 0, 360, 14)], '#3a2a6a', INNER, j=.05, step=99, clip=False)
    # جعبهٔ ابزار
    bx0, bx1, by0, by1 = 22, 64, -28, 10
    box3(p, bx0, by0, bx1, by1, (12, -9), R_F, R_T, R_S, sw=OUT)
    p.shape([(bx0 + 7, by0 - 5), (bx0 + 7, by0 - 28), (bx1 + 2, by0 - 28), (bx1 + 2, by0 - 5), (bx1 - 9, by0 - 5), (bx1 - 9, by0 - 17), (bx0 + 18, by0 - 17), (bx0 + 18, by0 - 5)], Y_F, PART, j=.05, step=6, clip=False)
    rect(p, bx0 + 4, by0 + 3, bx0 + 8, by1 - 4, R_T, .5)
    p.shape([(bx0 + 13, by0 + 6), (bx1 - 13, by0 + 6), (bx1 - 13, by0 + 15), (bx0 + 13, by0 + 15)], Y_F, INNER, j=.05, step=99, clip=False)
    return p


if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(0, -16), (0, -10), (0, -4), (0, 0)]]
    r = finish(p, 'wrench_room', None, motion={'nut': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_wrench_room_nut': dict(translate_from=[0, -16], translate_to=[0, 0], dur_s=1.2, easing='ease-in', repeat=1,
        note='مهره از بالای دهانه آرام در دهانهٔ آچار می‌نشیند؛ آچار و جعبه ثابت؛ حالت ایستا = نشسته؛ بدون حلقهٔ بیکار.'), 'reduced_motion': 'مهره در دهانه'}
    (OUTD / 'wrench_room.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
