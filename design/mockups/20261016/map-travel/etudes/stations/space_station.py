#!/usr/bin/env python3
"""ایستگاه W04 «ایستگاه فضایی» (سرزمین فضا، سکوی 'space' رنگ‌مایه ۲۵۶°) — نسخهٔ ۲.
طرح (واحد symbol، قبل از XF؛ محور افقی ماژول y=-29):
 ۱) دو نگهدارندهٔ ساده (بلوک ذوزنقه‌ای طلایی، پهنای ۱۸، در x=±26) از سکو (y=7) تا زیر ماژول، هم‌پوشانی ۴ با ماژول.
 ۲) ماژول افقی بلند: x ±46، y از -44 تا -14 (۹۲×۳۰)، سر گرد؛ سه پله: #eceff4 / روشن #ffffff / تیره #b4bccd / ته #8f98b0؛ دو نوار طلایی در x=±38؛ دریچهٔ گرد کوچک (r=5) وسط.
 ۳) دو بند طلایی (۱۰ پهن) در x=±26 که ۴ داخل ماژول و ۴ داخل بال می‌روند.
 ۴) دو بال خورشیدی مستطیلی فیروزه‌ای تیره (۲۴×۴۴) بالای ماژول، مرکز x=±26، y از -100 تا -56، با شبکهٔ دو خط افقی.
لایهٔ متحرک node_space_station_panels = هر دو بال و بند، حول مرکز ماژول (0,-29)، ±۶°؛ ماژول و نگهدارنده ثابت.
بدون حلقهٔ بیکار؛ حالت ایستا = بال‌ها راست."""
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

XF = (0.96, -25, 0)
CY = -29
MX, MT, MB = 50, -44, -14


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sharp(p, pts, col, sw):
    p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, sw))


def build(out=OUTD, ang=0):
    p = Pen('space_station', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.tipshadow(0, 8, 44); p.foot_tip(0, 7, 38)
    # ۱) نگهدارنده‌ها
    for sx in (-30, 30):
        cr = [(sx - 11, 7), (sx + 11, 7), (sx + 8, MB - 4), (sx - 8, MB - 4)]
        sharp(p, cr, G_B, PART)
        poly(p, [(sx - 7, 3), (sx - 4, 3), (sx - 3.5, MB - 1), (sx - 5.5, MB - 1)], G_L)
        poly(p, [(sx + 2, MB - 1), (sx + 5.5, MB - 1), (sx + 8, 3), (sx + 5, 3)], G_D)
    # ۲) بال‌ها و بندها (لایهٔ متحرک)
    with layer(p, 'panels'):
        cx_, cy_ = p.X((0, CY))
        p.raw('<g transform="rotate(%s %.1f %.1f)">' % (ang, cx_, cy_))
        for sx in (-30, 30):
            sharp(p, [(sx - 5, CY - 11), (sx + 5, CY - 11), (sx + 5, -57), (sx - 5, -57)], G_B, PART)
            x0, x1 = sx - 14, sx + 14
            sharp(p, [(x0, -96), (x1, -96), (x1, -60), (x0, -60)], P_B, PART)
            poly(p, [(x0 + 4, -91), (x0 + 7.5, -91), (x0 + 7.5, -65), (x0 + 4, -65)], P_L)
            for yy in (-83, -73):
                p.ln((x0 + 4, yy), (x1 - 4, yy), INNER, P_D, j=0)
        p.raw('</g>')
    # ۳) ماژول
    body = [(-MX + 8, MT), (MX - 8, MT)] + ell(MX - 8, CY, 8, 15, -90, 90, 10) + [(MX - 8, MB), (-MX + 8, MB)] + ell(-MX + 8, CY, 8, 15, 90, 270, 10)
    sharp(p, body, M_B, OUT)
    poly(p, [(-MX + 9, MT + 4), (MX - 9, MT + 4), (MX - 9, MT + 7.5), (-MX + 9, MT + 7.5)], M_L)
    poly(p, [(-MX + 9, MB - 9), (MX - 9, MB - 9), (MX - 9, MB - 4), (-MX + 9, MB - 4)], M_D)
    poly(p, [(-MX + 9, MB - 4), (MX - 9, MB - 4), (MX - 9, MB - 1.5), (-MX + 9, MB - 1.5)], M_DD)
    for xx in (-42, 42):
        poly(p, [(xx - 2, MT + 2), (xx + 2, MT + 2), (xx + 2, MB - 2), (xx - 2, MB - 2)], G_B)
    p.shape(ell(0, CY, 5, 5, 0, 360, 16), GLASS, INNER, j=.05, step=99, clip=False)
    poly(p, [(-3, CY - 3), (-1, CY - 3), (-1, CY - 1), (-3, CY - 1)], '#ffffff')
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
