#!/usr/bin/env python3
"""W02 «آزمایشگاه ترازو» (سکوی space، رنگ‌مایهٔ ۲۵۶°) — دور ۶ بازطراحی (هم‌سطح پیچ‌کاری).
قهرمان: ترازوی دوکفه ¾، ≈۷۲٪ عرض سکو. طرح قطعه‌به‌قطعه (واحد symbol، سکو مرکز (0,0)):
 ۱) پایهٔ گرد: استوانهٔ نقره‌ای-سفید (r36،h11) + ۲) ستون استوانه (r10) تا y=-96؛ سه پله (سفید/لاوندر/آبی-خاکستری).
 ۳) تیر فیروزه‌ای ¾ (۱۰۸×۱۴ با رویهٔ روشن و کنارهٔ تیره)، کج ۷° (چپ پایین‌تر) — لایهٔ متحرک node_scale_lab_beam.
 ۴) زنجیرهای مثلثی ریز + دو کفهٔ برنجی (کاسهٔ نیم‌بیضی + لبهٔ روشن + درون تیره)؛ ۵) مکعب زرد روی کفهٔ چپ، گوی قرمز روی کفهٔ راست.
 ۶) مفصل زرین روی تیر (ثابت). بدون متن/عدد/پیکان."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from station_kit import *
from r6_helpers import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/scale_lab'
SIL = ('#e9ecf8', '#ffffff', '#9aa6cc', '#ffffff')          # نقره‌ای-سفید (میانی، روشن، تیره، رویه)
TB = ('#19b5b0', '#86eee2', '#0d7a84')                       # تیر فیروزه‌ای: جلو، رویه، کنار
BR = ('#e8a634', '#ffd77a', '#a8661a')                       # برنج
PY, TH = -100, -7
HALF = 48; CHAIN = 44; PR = 24


def build():
    p = Pen('scale_lab', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.12, 0, 4)
    p.tipshadow(0, 12, 40); p.foot_tip(0, 12, 20)
    cyl(p, 0, 12, 40, 12, SIL)                                                   # پایهٔ گرد
    cyl(p, 0, 3, 11, 98, SIL, top=False)                                          # ستون
    f = rot(0, PY, TH)
    with layer(p, 'beam'):
        for sgn, obj in ((-1, 'cube'), (1, 'ball')):
            E = f((sgn * (HALF - 5), 8)); cx, cy = E[0], E[1] + CHAIN
            for q in (-PR + 5, PR - 5): p.ln(E, (cx + q, cy), INNER, NAVY, j=.05)
            bowl = ell(cx, cy, PR, 17, 0, 180, 18)
            p.shape(bowl, BR[0], PART, j=.1, step=8)
            p.fill([(cx - PR + 4, cy + 2), (cx - 9, cy + 2), (cx - 7, cy + 13), (cx - PR + 9, cy + 9)], BR[1])
            p.fill([(cx + 10, cy + 2), (cx + PR - 3, cy + 2), (cx + PR - 9, cy + 10), (cx + 8, cy + 14)], BR[2], .9)
            p.stroke(bowl, PART, j=.1, step=8)
            p.shape(ell(cx, cy, PR, 8, 0, 360, 24), BR[1], PART, j=.1, step=99, clip=False)
            if obj == 'cube':
                box(p, cx - 12, cy - 19, 22, 22, (9, -6), ('#ffe14d', '#fff6a8', '#d99a14'), sw=PART, seam=INNER)
            else:
                bx, by = cx, cy - 11
                p.shape(ell(bx, by, 13, 13, 0, 360, 28), '#e0443a', PART, j=.1, step=99, clip=False)
                p.fill(ell(bx, by, 10.5, 10.5, 5, 95, 12), '#a82a24', .8)
                p.fill(ell(bx - 4.5, by - 4.5, 3.6, 3, 0, 360, 10), '#ffb1a0')
        box(p, -HALF, -7, 2 * HALF, 14, (9, -6), TB, f=f)                       # تیر
    p.shape(ell(0, PY + 1, 11, 11, 0, 360, 26), '#ffd23f', PART, j=.1, step=99, clip=False)
    p.fill(ell(-2.5, PY - 2, 4, 3.4, 0, 360, 10), '#fff3b0')
    return p


if __name__ == '__main__':
    p = build()
    ang = [-9, 6, -4, 0]
    r = finish(p, 'scale_lab', None, motion={'beam': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_scale_lab_beam': dict(kind='چرخش تیر با دو کفه حول مفصل (x=0,y=%s)' % round(p.X((0, PY))[1], 1),
        center=[round(v, 1) for v in p.X((0, PY))], keyframes_deg=[10, -6, 3, 0], duration_s=2.2, easing='ease-out', loop=False,
        trigger='رسیدن کودک (یک‌بار)', note='لایه سفت می‌چرخد (کفه‌ها همراه تیر)؛ حالت ایستا = پایان = همین کج‌بودن ۷°', reduced_motion='ایستا')}
    (OUTD / 'scale_lab.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
