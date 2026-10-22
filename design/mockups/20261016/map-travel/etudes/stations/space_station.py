#!/usr/bin/env python3
"""ایستگاه W04 «ایستگاه فضایی» (سرزمین فضا، سکوی 'space' رنگ‌مایه ۲۵۶°) — نسخهٔ ۳.
طرح (واحد symbol، قبل از XF؛ محور افقی y=-52):
 ۱) یک پایهٔ کوتاه طلایی زیر بدنه (ذوزنقه، پهنای ۲۸ پایین/۲۰ بالا) از y=7 تا زیر بدنه، هم‌پوشانی ۴.
 ۲) گنبد طلایی اتصال روی بدنه.
 ۳) بدنهٔ افقی سفید-نقره‌ای x ±21، y از -70 تا -34، سر گرد؛ سه پله روشن/پایه/تیره/تیره‌تر؛ یک دریچهٔ گرد r=6 وسط.
 ۴) دو بال افقی هم‌محور با بدنه: ساقهٔ طلایی (x 17 تا 31، ۱۴ بلند، ۴ داخل بدنه و ۴ داخل پنل) و بعد پنل فیروزه‌ای ۱۸×۲۸ (x 27 تا 45)، یک خط شبکه.
لایهٔ متحرک node_space_station_panels = ساقه‌ها و پنل‌ها حول مرکز بدنه (0,-52)، ±۶°؛ بدنه، دریچه و پایه ثابت.
بدون حلقهٔ بیکار؛ حالت ایستا = بال‌ها افقی."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/space_station'

M_B, M_L, M_D = '#eceff4', '#ffffff', '#b4bccd'
G_B, G_L, G_D = '#f0b03c', '#ffd98a', '#b9741c'
P_B, P_L, P_D = '#1f8a98', '#58c8d0', '#126370'
GLASS = '#cfeaff'; M_DD = '#8f98b0'

XF = (0.94, -23, 0)
CY = -44
MX, MT, MB = 21, -62, -26


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sharp(p, pts, col, sw):
    p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, sw))


def build(out=OUTD, ang=0):
    p = Pen('space_station', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.tipshadow(0, 8, 30); p.foot_tip(0, 7, 26)
    # ۱) پایه
    sharp(p, [(-14, 7), (14, 7), (10, MB - 4), (-10, MB - 4)], G_B, PART)
    poly(p, [(-9.5, 3), (-6, 3), (-5, MB - 1), (-7, MB - 1)], G_L)
    poly(p, [(3, MB - 1), (6, MB - 1), (9, 3), (5, 3)], G_D)
    # ۲) گنبد
    sharp(p, [(-9, MT + 4)] + ell(0, MT + 4, 9, 14, 180, 360, 10) + [(9, MT + 4)], G_B, PART)
    # ۳) ساقه‌ها و پنل‌ها (لایهٔ متحرک)؛ پنل بعد از ساقه
    with layer(p, 'panels'):
        cx_, cy_ = p.X((0, CY))
        p.raw('<g transform="rotate(%s %.1f %.1f)">' % (ang, cx_, cy_))
        for sg in (-1, 1):
            sharp(p, [(sg * 17, CY - 7), (sg * 37, CY - 7), (sg * 37, CY + 7), (sg * 17, CY + 7)], G_B, PART)
            xa, xb = sorted((sg * 33, sg * 51))
            sharp(p, [(xa, CY - 14), (xb, CY - 14), (xb, CY + 14), (xa, CY + 14)], P_B, PART)
            poly(p, [(xa + 4, CY - 10), (xa + 7.5, CY - 10), (xa + 7.5, CY + 10), (xa + 4, CY + 10)], P_L)
            p.ln((xa + 4, CY), (xb - 4, CY), INNER, P_D, j=0)
        p.raw('</g>')
    # ۴) بدنه
    body = [(-MX + 8, MT), (MX - 8, MT)] + ell(MX - 8, CY, 8, 18, -90, 90, 10) + [(MX - 8, MB), (-MX + 8, MB)] + ell(-MX + 8, CY, 8, 18, 90, 270, 10)
    sharp(p, body, M_B, OUT)
    poly(p, [(-MX + 9, MT + 4), (MX - 9, MT + 4), (MX - 9, MT + 7.5), (-MX + 9, MT + 7.5)], M_L)
    poly(p, [(-MX + 9, MB - 11), (MX - 9, MB - 11), (MX - 9, MB - 5), (-MX + 9, MB - 5)], M_D)
    poly(p, [(-MX + 9, MB - 5), (MX - 9, MB - 5), (MX - 9, MB - 2), (-MX + 9, MB - 2)], M_DD)
    p.shape(ell(0, CY, 6, 6, 0, 360, 16), GLASS, INNER, j=.05, step=99, clip=False)
    poly(p, [(-3.5, CY - 3.5), (-1, CY - 3.5), (-1, CY - 1), (-3.5, CY - 1)], '#ffffff')
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    hm = p.X((0, CY))
    r = finish(p, 'space_station', STAND, motion={'panels': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    st = r['spec']['stand']; ext = []
    for a_ in (-6, 6):    # قاب حرکت واقعی ±۶° (کیت فقط چرخش ۳۶۰° یا جابه‌جایی می‌شناسد)
        q = build(ang=a_)
        ext.append((a_, motion_check(q, 'panels', offsets=[(0, 0)], stand=st), inside_check(q, {'panels': dict(offsets=[(0, 0)])})))
    print('EXT', json.dumps([(a, m, i) for a, m, i in ext], ensure_ascii=False))
    sp = r['spec']
    sp['motion_spec'] = {'node_space_station_panels': dict(center=[round(v, 1) for v in hm], max_angle_deg=6, pattern='0 -> +6 -> -6 -> 0', repeats=3, duration_s=6,
                                                          note='هر دو بال خورشیدی و بندها با هم حول مرکز ماژول ±۶° مایل می‌شوند؛ فقط هنگام رسیدن/بیداری؛ بدون حلقهٔ بیکار؛ ماژول و نگهدارنده‌ها ثابت و کامل؛ تزئینی، بدون سبک‌شدن/شناوری.'),
                         'reduced_motion': 'بال‌ها ایستا و راست'}
    (OUTD / 'space_station.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
