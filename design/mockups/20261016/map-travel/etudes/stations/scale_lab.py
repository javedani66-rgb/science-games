#!/usr/bin/env python3
"""ایستگاه W02 «آزمایشگاه ترازو» (سرزمین فضا، پالت 'space').
طرح قطعه‌به‌قطعه (واحد symbol؛ زمین y=12):
 ۱) پایه: بلوک ذوزنقه‌ای سفید-خاکستری (OUT) y از -6 تا 12، نیم‌پهنا 24 پایین / 19 بالا؛ سه پلهٔ سفید (پایه/روشن/تیره).
 ۲) ستون: میلهٔ سفید پهنای 13 (PART) روی محور x=0 از y=-2 تا -66؛ زیر پایه رفته (پایه روی آن).
 ۳) تیر: میلهٔ فیروزه‌ای افقی، ارتفاع 13 (PART)، نیم‌طول 41، مرکز y=-66 روی محور ستون؛ پایه/روشن/تیره.
 ۴) محور: کلاهک زرد گرد r6.5 (INNER) روی تیر، دقیقاً در (0,-66).
 ۵) دو کفهٔ گرد کم‌عمق سفید-خاکستری (PART)، مرکز x=±26، نیم‌پهنا 12، عمق 11، لبه y=-28؛ هرکدام با دو بند عمودی (INNER)
    در x=cx±12 از زیر تیر تا لبهٔ کفه (بندها از میان چیزی رد نمی‌شوند؛ اجسام میان بندها می‌نشینند).
 ۶) کفهٔ چپ: سه مکعب واحد زرد (هرم: دو + یک، ضلع 8، رنگ تخت)؛ کفهٔ راست: یک گوی مرجانی بزرگ‌تر (r 7.5) با لکهٔ نور.
    رنگ قهرمان‌ها: فیروزه/سفید/زرد/مرجانی؛ پایهٔ سکو بنفش (رنگ‌مایه ≈258°).
لایهٔ متحرک node_scale_lab_beam = بندها + تیر + کلاهک + کفه‌ها با اجسام (تیر ±۵° می‌چرخد؛ کفه‌ها خلاف جهت حول سر تیر).
حالت ایستا = تراز (۰°). بدون حلقهٔ بیکار، بدون متن."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/scale_lab'

W_B, W_L, W_D = '#f1f5fa', '#ffffff', '#b9c5dc'           # سفید-خاکستری
T_B, T_L, T_D = '#22bfb2', '#8ae8dc', '#12857f'           # فیروزه‌ای
Y_B, Y_L, Y_D = '#ffd84d', '#fff0a0', '#d9a01e'           # مکعب زرد
S_B, S_L = '#ff6f61', '#ffc2b8'                           # گوی مرجانی
STR = '#fff3c4'
G = 12
PY = -88                  # محور تیر
HL = 62                   # نیم‌طول تیر
PX, PR, PD, PTOP = 40, 24, 13, -34


def poly(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def box(p, x0, y0, x1, y1, col):
    pts = ' '.join('%.1f,%.1f' % q for q in p.X([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]))
    p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (pts, col, INNER))


def cube(p, cx, yb, c):
    box(p, cx - c / 2, yb - c, cx + c / 2, yb, Y_B)
    poly(p, [(cx - c / 2 + 2.6, yb - c + 2.6), (cx + c / 2 - 2.6, yb - c + 2.6), (cx + c / 2 - 2.6, yb - c + 4.4), (cx - c / 2 + 2.6, yb - c + 4.4)], Y_L)


def stack3(p, cx, yb, c=13):
    """سه مکعب واحد (هرم دو + یک): دو مکعب کنار هم، یکی روی آن‌ها."""
    cube(p, cx - c / 2, yb, c); cube(p, cx + c / 2, yb, c); cube(p, cx, yb - c + 1.5, c)


def hanger(p, cx):
    """بند مثلثی (یک جزء): از سر تیر به دو لبهٔ کفه."""
    a = p.X([(cx, PY), (cx - PR + 2, PTOP + 1), (cx + PR - 2, PTOP + 1)])
    p.raw('<path d="M%.1f,%.1f L%.1f,%.1f M%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="butt"/>' % (
        a[1][0], a[1][1], a[0][0], a[0][1], a[2][0], a[2][1], a[0][0], a[0][1], STR, INNER))


def build(out=OUTD):
    p = Pen('scale_lab', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((40, -6), (62, 8)), dot=(58, -18)); p.xf = (0.88, 0, 8)
    p.tipshadow(2, G + 3, 30); p.foot_tip(0, G + 1, 22)
    p.shape([(-8, PY), (8, PY), (8, 0), (-8, 0)], W_B, PART, j=.1, step=8)
    poly(p, [(-4.6, PY + 8), (-1.6, PY + 8), (-1.6, -6), (-4.6, -6)], W_L)
    poly(p, [(1.8, PY + 8), (4.6, PY + 8), (4.6, -6), (1.8, -6)], W_D)
    body = [(-24, G), (24, G), (19, -6), (-19, -6)]
    p.shape(body, W_B, OUT, j=.1, step=8)
    poly(p, [(-14.5, -1.8), (-11.2, -1.8), (-15.8, G - 4.5), (-18.2, G - 4.5)], W_L)
    poly(p, [(5, -1.8), (15.3, -1.8), (19.5, G - 4), (5, G - 4)], W_D)
    p.stroke(body, OUT, j=.1, step=8)
    with layer(p, 'beam'):
        for s in (-1, 1):
            cx = s * PX
            p.raw('<g class="pan" data-side="%d" data-pivot="%.1f,%.1f">' % (s, *p.X((cx, PY))))
            hanger(p, cx)
            bowl = [(cx + PR, PTOP)] + ell(cx, PTOP, PR, PD, 0, 180, 16)[1:-1] + [(cx - PR, PTOP)]
            p.shape(bowl, W_B, PART, j=.1, step=99, clip=False)
            poly(p, [(cx - 12, PTOP + 3.8), (cx - 4, PTOP + 3.8), (cx - 4, PTOP + 5.8), (cx - 11, PTOP + 5.8)], W_L)
            inn = [q for q in ell(cx, PTOP, PR - 4.5, PD - 4.5, 0, 180, 16) if q[1] > PTOP + (PD - 4.5) * .55]
            poly(p, inn, W_D)
            yb = PTOP + 4                        # بار ۴ واحد داخل کفه
            if s == -1:
                stack3(p, cx, yb)
            else:
                ax, ay = p.X((cx, yb - 10)); p.raw('<circle cx="%.1f" cy="%.1f" r="10" fill="%s" class="eo" stroke-width="%s"/>' % (ax, ay, S_B, INNER))
                poly(p, [(cx - 5.2, yb - 15), (cx - 2.2, yb - 16.4), (cx - 2.2, yb - 13), (cx - 5.2, yb - 11.6)], S_L)
            p.raw('</g>')
        beam = [(-HL, PY - 6.5), (HL, PY - 6.5), (HL, PY + 6.5), (-HL, PY + 6.5)]
        p.shape(beam, T_B, PART, j=.1, step=8, clip=False)
        poly(p, [(-HL + 5, PY - 3.9), (HL - 5, PY - 3.9), (HL - 5, PY - 1.9), (-HL + 5, PY - 1.9)], T_L)
        poly(p, [(-HL + 5, PY + 1.6), (HL - 5, PY + 1.6), (HL - 5, PY + 3.7), (-HL + 5, PY + 3.7)], T_D)
        p.shape(ell(0, PY, 6.5, 6.5, 0, 360, 16), Y_B, INNER, j=.05, step=99, clip=False)
        disc(p, -1.6, PY - 1.8, 1.8, Y_L)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    px, py = p.X((0, PY))
    # حرکت: تیر ±۵° حول محور؛ برای سنجش قاب، جابه‌جایی عمودی سر تیر (±sin5°×۴۱ ≈ ۳٫۶)
    offs = [(0, 0), (0, -3.6), (0, 3.6)]
    r = finish(p, 'scale_lab', STAND, motion={'beam': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_scale_lab_beam': dict(center=[round(px, 1), round(py, 1)], keyframes_deg=[0, 5, -3.5, 2, -1, 0], duration_s=2.2, once=True,
                                                    note='کل لایه حول محور تیر می‌چرخد؛ هر کفه (g.pan، pivot در data-pivot = سر تیر آن سمت) خلاف جهت همان زاویه می‌چرخد تا افقی بماند؛ حالت ایستا = تراز؛ هنگام رسیدن، یک‌بار؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'تراز ثابت'}
    (OUTD / 'scale_lab.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
