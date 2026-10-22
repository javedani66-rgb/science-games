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

XF = (0.84, -21.5, 0)
CY = -52
MX, MT, MB = 22, -66, -38


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sharp(p, pts, col, sw):
    p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, sw))


def build(out=OUTD):
    p = Pen('space_station', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((62, 6),), dot=(58, -16)); p.xf = XF
    p.tipshadow(2, 8, 28); p.foot_tip(0, 7, 20)
    # ۱) پایه
    base = [(-20, 7), (20, 7), (14, -42), (-14, -42)]
    p.shape(base, G_B, PART, j=.15, step=8)
    poly(p, [(-16, 2), (-12.5, 2), (-10.5, -34), (-13, -34)], G_L)
    poly(p, [(4, -34), (14, -34), (19, 6), (8, 6)], G_D)
    p.stroke(base, PART, j=.15, step=8)
    # ۲) گنبد
    dome = [(-11, MT + 4)] + ell(0, MT + 4, 11, 19, 180, 360, 10) + [(11, MT + 4)]
    sharp(p, dome, G_B, PART)
    # ۳) بال‌ها (لایهٔ متحرک): بندها و بال‌ها
    with layer(p, 'panels'):
        for s in (-1, 1):
            sharp(p, [(s * 18, CY - 8), (s * 40, CY - 8), (s * 40, CY + 8), (s * 18, CY + 8)], G_B, PART)
            x0, x1 = (38, 56) if s > 0 else (-56, -38)
            sharp(p, [(x0, -78), (x1, -78), (x1, -26), (x0, -26)], P_B, PART)
            poly(p, [(x0 + 4, -73), (x0 + 7.5, -73), (x0 + 7.5, -31), (x0 + 4, -31)], P_L)
            for yy in (-62, -42):
                p.ln((x0 + 4, yy), (x1 - 4, yy), INNER, P_D, j=0)
    # ۴) ماژول
    body = [(-MX + 8, MT), (MX - 8, MT)] + ell(MX - 8, CY, 8, 14, -90, 90, 10) + [(MX - 8, MB), (-MX + 8, MB)] + ell(-MX + 8, CY, 8, 14, 90, 270, 10)
    sharp(p, body, M_B, OUT)
    poly(p, [(-MX + 9, MT + 4), (MX - 9, MT + 4), (MX - 9, MT + 7.5), (-MX + 9, MT + 7.5)], M_L)
    poly(p, [(-MX + 9, MB - 8), (MX - 9, MB - 8), (MX - 9, MB - 3), (-MX + 9, MB - 3)], M_D)
    for xx in (-13, 13):
        poly(p, [(xx - 2, MT + 2), (xx + 2, MT + 2), (xx + 2, MB - 2), (xx - 2, MB - 2)], G_B)
    p.shape(ell(0, CY, 6, 6, 0, 360, 16), GLASS, INNER, j=.05, step=99, clip=False)
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
