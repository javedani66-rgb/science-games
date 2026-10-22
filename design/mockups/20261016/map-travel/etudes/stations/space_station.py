#!/usr/bin/env python3
"""ایستگاه W04 «ایستگاه فضایی» (سرزمین فضا، سکوی 'space' رنگ‌مایه ۲۵۶°).
طرح قطعه‌به‌قطعه (واحد symbol، قبل از XF، مرکز ماژول (0,-52)):
 ۱) پایهٔ طلایی (بلوک ذوزنقه‌ای، نیم‌پهنا ۲۰ پایین / ۱۴ بالا، از y=7 تا y=-38) روی سکو؛ ماژول روی آن می‌نشیند.
 ۲) گنبد دریچهٔ بالای ماژول (طلایی، نیم‌دایره ۱۶ پهن) پشت ماژول.
 ۳) ماژول استوانه‌ای افقی سفید-نقره‌ای: x از -24 تا 24، y از -70 تا -34 (۳۶ بلند)، سه پله: #eceff4 / #ffffff / #b4bccd؛ دو نوار طلایی تخت، یک دریچهٔ گردِ شیشه‌ای وسط.
 ۴) دو بند طلایی (۱۴ بلند، هم‌پوشانی ۴ با ماژول و ۴ با بال) روی محور افقی ماژول y=-52.
 ۵) دو بال خورشیدی مستطیلی فیروزه‌ای تیره: x ±30..±58، y -76..-28 (۲۸×۴۸) روی همان محور؛ شبکهٔ چهارخانه (۱ خط عمودی، ۲ افقی)؛ رنگ‌مایه ≈۱۸۵° (دست‌کم ۷۰° از سکو).
لایهٔ متحرک node_space_station_panels = هر دو بال + بند، حول مرکز ماژول؛ ماژول و پایه ثابت‌اند.
حرکت: ±۶° هنگام رسیدن/بیداری، سه تکرار، بدون حلقهٔ بیکار؛ حالت ایستا = افقی."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/space_station'

M_B, M_L, M_D = '#eceff4', '#ffffff', '#b4bccd'
G_B, G_L, G_D = '#f0b03c', '#ffd98a', '#b9741c'
P_B, P_L, P_D = '#1f8a98', '#58c8d0', '#126370'
GLASS = '#cfeaff'

XF = (1.02, -24, 0)
CY = -52
MX, MT, MB = 20, -70, -34


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build(out=OUTD):
    p = Pen('space_station', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.tipshadow(2, 8, 28); p.foot_tip(0, 7, 20)
    # ۱) پایه
    base = [(-20, 7), (20, 7), (14, -38), (-14, -38)]
    p.shape(base, G_B, PART, j=.15, step=8)
    poly(p, [(-16, 2), (-12.5, 2), (-10.5, -34), (-13, -34)], G_L)
    poly(p, [(4, -34), (14, -34), (19, 6), (8, 6)], G_D)
    p.stroke(base, PART, j=.15, step=8)
    # ۲) گنبد
    dome = [(-8, MT + 4)] + ell(0, MT + 4, 8, 11, 180, 360, 10) + [(8, MT + 4)]
    p.shape(dome, G_B, PART, j=.1, step=99, clip=False)
    # ۳) بال‌ها (لایهٔ متحرک): اول بندها، بعد بال‌ها
    with layer(p, 'panels'):
        for s in (-1, 1):
            poly(p, [(s * 14, CY - 7), (s * 28, CY - 7), (s * 28, CY + 7), (s * 14, CY + 7)], G_B)
            p.shape([(s * 16, CY - 7), (s * 28, CY - 7), (s * 28, CY + 7), (s * 16, CY + 7)], G_B, PART, j=.1, step=99, clip=False)
            x0, x1 = (24, 50) if s > 0 else (-50, -24)
            pan = [(x0, -76), (x1, -76), (x1, -28), (x0, -28)]
            p.shape(pan, P_B, PART, j=.1, step=99, clip=False)
            inner, outer = (x0, x1) if s > 0 else (x1, x0)
            poly(p, [(x0 + 4, -72), (x0 + 7.5, -72), (x0 + 7.5, -32), (x0 + 4, -32)], P_L)
            poly(p, [(x1 - 9, -72), (x1 - 3, -72), (x1 - 3, -32), (x1 - 9, -32)], P_D)
            xm = (x0 + x1) / 2 + 1
            p.ln((xm, -73), (xm, -31), INNER, P_D, j=0)
            for yy in (-60, -44):
                p.ln((x0 + 3, yy), (x1 - 3, yy), INNER, P_D, j=0)
    # ۴) ماژول
    body = [(-MX + 8, MT)] + [(MX - 8, MT)] + ell(MX - 8, CY, 8, 18, -90, 90, 10) + [(MX - 8, MB), (-MX + 8, MB)] + ell(-MX + 8, CY, 8, 18, 90, 270, 10)
    p.shape(body, M_B, OUT, j=.15, step=8)
    poly(p, [(-MX + 12, MT + 4), (MX - 12, MT + 4), (MX - 12, MT + 7.5), (-MX + 12, MT + 7.5)], M_L)
    poly(p, [(-MX + 12, MB - 9), (MX - 6, MB - 9), (MX - 8, MB - 3), (-MX + 12, MB - 3)], M_D)
    p.stroke(body, OUT, j=.15, step=8)
    for xx in (-12, 12):
        poly(p, [(xx - 2.5, MT + 2), (xx + 2.5, MT + 2), (xx + 2.5, MB - 2), (xx - 2.5, MB - 2)], G_B)
    p.shape(ell(0, CY, 8, 8, 0, 360, 16), GLASS, INNER, j=.05, step=99, clip=False)
    poly(p, [(-4, CY - 4), (-1.5, CY - 4), (-1.5, CY - 1.5), (-4, CY - 1.5)], '#ffffff')
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    hm = p.X((0, CY))
    r = finish(p, 'space_station', STAND, motion={'panels': dict(rotate=hm)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_space_station_panels': dict(center=[round(v, 1) for v in hm], max_angle_deg=6, pattern='0 -> +6 -> -6 -> 0', repeats=3, duration_s=6,
                                                          note='هر دو بال خورشیدی و بندها با هم حول مرکز ماژول ±۶° مایل می‌شوند؛ فقط هنگام رسیدن/بیداری؛ بدون حلقهٔ بیکار؛ ماژول و پایه ثابت و کامل؛ تزئینی، بدون سبک‌شدن/شناوری.'),
                         'reduced_motion': 'بال‌ها افقی و ثابت'}
    (OUTD / 'space_station.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
