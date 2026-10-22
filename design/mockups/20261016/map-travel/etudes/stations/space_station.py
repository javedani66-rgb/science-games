#!/usr/bin/env python3
"""ایستگاه W04 «ایستگاه فضایی» (سرزمین فضا، سکوی بنفش ۲۵۶°) — دور ۵ (دستور مدیر هنری: ماژول استوانه‌ای، دو بال خورشیدی بزرگ، دریچهٔ گرد، ۶۵٪ وسط، ماهواره نشود).
طرح قطعه‌به‌قطعه (واحد symbol، xf=1٫5، مرکز سکو (0,0)، محور بال‌ها y=-16):
 ۱) پایهٔ طلایی: ذوزنقهٔ کوتاه زیر بدنه x ±13 (پایین y 12)، سه پله.
 ۲) ماژول اصلی: کپسول افقی x ±17، y -28..-4 (سفید-نقره‌ای #eceff4 / روشن / تیره)، دو شیار قائم، دریچهٔ گرد r=6٫5 وسط (حلقهٔ NAVY + شیشهٔ آبی).
 ۳) ماژول بالایی (گره اتصال): کپسول کوچک x ±6، y -37..-27 با کلاهک طلایی؛ نشان می‌دهد چند ماژول است.
 ۴) دو بال خورشیدی بزرگ (لایهٔ panels): بازوی طلایی x 15..24 (۶ بلند) و پنل فیروزه‌ای x 21..37، y -36..4 (۱۶×۴۰) با شبکهٔ سه‌ردیفه و نوار نور؛ حول (0,-16) ±۶°؛ حالت ایستا = افقی.
لایهٔ متحرک node_space_station_panels؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/space_station'

M_B, M_L, M_D = '#eceff4', '#ffffff', '#b4bccd'
G_B, G_L, G_D = '#f0b03c', '#ffd98a', '#b9741c'
P_B, P_L, P_D = '#1f8a98', '#58c8d0', '#0f5560'
GLASS = '#cfeaff'; M_DD = '#8f98b0'
XF = (1.25, 0, 12)
CY = -16


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sharp(p, pts, col, sw):
    p.raw('<polygon points="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, sw))


def capsule(x0, y0, x1, y1, r):
    cy = (y0 + y1) / 2
    return [(x0 + r, y0), (x1 - r, y0)] + ell(x1 - r, cy, r, (y1 - y0) / 2, -90, 90, 10) + [(x1 - r, y1), (x0 + r, y1)] + ell(x0 + r, cy, r, (y1 - y0) / 2, 90, 270, 10)


def build(out=OUTD, ang=0):
    p = Pen('space_station', 'space'); pad(p, line=((-80, 12), (-66, 20)), tri=((74, -20), (80, 6)), dot=(-76, -14)); p.xf = XF
    p.tipshadow(0, 13, 30); p.foot_tip(0, 12, 16)
    # ۱) پایه
    sharp(p, [(-13, 12), (13, 12), (9, -6), (-9, -6)], G_B, PART)
    poly(p, [(-8.5, 9), (-5, 9), (-4, -3), (-6, -3)], G_L)
    poly(p, [(3, -3), (5.5, -3), (8, 9), (4.5, 9)], G_D)
    # ۴) بال‌ها (لایهٔ متحرک)
    with layer(p, 'panels'):
        cx_, cy_ = p.X((0, CY))
        p.raw('<g transform="rotate(%s %.1f %.1f)">' % (ang, cx_, cy_))
        for sg in (-1, 1):
            sharp(p, [(sg * 17, CY - 5), (sg * 31, CY - 5), (sg * 31, CY + 5), (sg * 17, CY + 5)], G_B, PART)
            xa, xb = sorted((sg * 29, sg * 44))
            sharp(p, [(xa, -42), (xb, -42), (xb, 6), (xa, 6)], P_B, PART)
            poly(p, [(xa + 3, -38), (xa + 6.5, -38), (xa + 6.5, 2), (xa + 3, 2)], P_L)
            for y in (-29, -17, -5): p.ln((xa + 3, y), (xb - 3, y), INNER, P_D, j=0)
        p.raw('</g>')
    # ۲) ماژول اصلی
    body = capsule(-21, -28, 21, -4, 10)
    sharp(p, body, M_B, OUT)
    poly(p, [(-14, -25), (14, -25), (14, -22), (-14, -22)], M_L)
    poly(p, [(-14, -9), (14, -9), (14, -6.5), (-14, -6.5)], M_D)
    for x in (-12.5, 12.5): poly(p, [(x - 1.2, -23), (x + 1.2, -23), (x + 1.2, -9), (x - 1.2, -9)], M_DD)
    p.shape(ell(0, CY, 7, 7, 0, 360, 16), GLASS, PART, j=.05, step=99, clip=False)
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
