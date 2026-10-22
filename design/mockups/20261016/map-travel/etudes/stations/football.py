#!/usr/bin/env python3
"""ایستگاه F01 «زمین فوتبال» (سرزمین ورزشگاه، پالت sports، سکوی سبز با رنگ‌مایهٔ ۹۳°).
طرح قطعه‌به‌قطعه:
 ۱) توپ: یک کرهٔ درشت r=38 (قطر ≈۵۵px نقشه)، رنگ سفید-کرم سه‌پله‌ای: پایه #f3ead6، سایهٔ تیز هلالی لاوندر پایین-راست، برق سفید بالا-چپ. دور OUT.
 ۲) لکه‌ها: یک پنج‌ضلعی مرکزی (r=11) + پنج پنج‌ضلعی لبه (r=7، فاصله ۲۱ از مرکز، رأس به سمت بیرون) به رنگ آبی‌بنفش تیره #3a3a86 (رنگ‌مایهٔ ≈۲۴۰°، ۱۴۷° از سکو)؛ بین مرکز و هر لکهٔ لبه یک درز تخت INNER=3.9 پهنا.
    همه تخت و بی‌خط؛ فاصلهٔ لکه‌ها ≥۸؛ لکه‌ها داخل کره‌اند (۳ واحد تا لبه) و با چرخش بیرون نمی‌زنند.
 ۲b) نشان گچی زیر توپ: بیضی تخت سفید-سبز روشن (نقطهٔ پنالتی) بدون خط؛ توپ را به سکو می‌چسباند.
 ۳) سایهٔ تماس زیر توپ (داخل لایهٔ متحرک تا توپ شناور نماند).
لایهٔ متحرک: node_football_ball (انتقال از ≈۱۲px چپ) و داخلش node_football_ball_spin (لکه‌ها و درزها، چرخش حول مرکز توپ).
سایه و برق ثابت بر توپ‌اند (نور از بالا-چپ ثابت می‌ماند). بدون عامل نیرو، بدون پیکان، بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/football'

B_, B_L, B_D = '#f3ead6', '#ffffff', '#cfc7e6'
PATCH = '#3a3a86'
CHALK = '#d9f0b4'
R = 38
CX, CY = -12, -24          # مرکز توپ (کفش y=14 روی سکو)
RC, RE, DE = 11, 11, 35     # پنج‌ضلعی مرکزی، لبه‌ای، فاصلهٔ مرکز لبه‌ای‌ها (فاصلهٔ لکه‌ها 13)
ROLL = 9                  # ≈۶px نقشه؛ شروع ≥۸px از لبهٔ سکو


def penta(cx, cy, r, a):
    return [(cx + r * math.cos(math.radians(a + 72 * i)), cy + r * math.sin(math.radians(a + 72 * i))) for i in range(5)]


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def crescent(p, c, r, s, col, op):
    """هلال = کره منهای کرهٔ جابه‌جاشده به s؛ هر دو قوس از سمت پایین-راست (زاویه ۴۵°)؛ چندضلعی تیز."""
    d = math.hypot(*s); h = math.sqrt(r * r - d * d / 4); ux, uy = s[0] / d, s[1] / d
    mx, my = c[0] + s[0] / 2, c[1] + s[1] / 2
    P = [(mx - uy * h, my + ux * h), (mx + uy * h, my - ux * h)]
    def sweep(cc, a, b, n=20):
        t = math.radians(45)
        da = (b - a) % (2 * math.pi)
        if not (0 <= (t - a) % (2 * math.pi) <= da): da -= 2 * math.pi
        return [(cc[0] + r * math.cos(a + da * i / n), cc[1] + r * math.sin(a + da * i / n)) for i in range(n + 1)]
    ang = lambda cc, q: math.atan2(q[1] - cc[1], q[0] - cc[0])
    c2 = (c[0] + s[0], c[1] + s[1])
    # ترتیب نقطه‌ها را طوری بگیر که هر قوس از 45° بگذرد
    best = None
    for q1, q2 in (P, P[::-1]):
        big = sweep(c, ang(c, q1), ang(c, q2)); sm = sweep(c2, ang(c2, q2), ang(c2, q1))
        best = (big, sm); break
    poly(p, best[0] + best[1], col, op)


def build():
    p = Pen('football', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 0, 0)
    # نشان گچی (ثابت): بیضی تخت زیر جای ایستادن توپ
    p.raw('<ellipse cx="%s" cy="%s" rx="24" ry="9.5" fill="%s" opacity=".85"/>' % (CX, CY + R + 1, CHALK))
    p.foot_tip(CX, CY + R + 1, 20)
    with layer(p, 'ball'):
        p.tipshadow(CX, CY + R + 1, 24)
        disc = ell(CX, CY, R, R, 0, 360, 48)
        p.shape(disc, B_, PART, j=0, step=99)
        # جزئیات داخل توپ با clip به دایره (لکه‌های لبه نیمه‌بریده)؛ clip ثابت، چرخش داخلش
        p.raw('<clipPath id="fbclip"><circle cx="%s" cy="%s" r="%s"/></clipPath><g clip-path="url(#fbclip)">' % (CX, CY, R - 1))
        p.raw('<g id="node_football_ball_spin">')
        c = (CX, CY)
        for i in range(5):
            ang = -90 + 72 * i; ax = math.radians(ang)
            q = (CX + DE * math.cos(ax), CY + DE * math.sin(ax))   # مرکز لکهٔ لبه روی همان شعاع رأس
            p.raw('<path d="M%.1f,%.1f L%.1f,%.1f" stroke="%s" stroke-width="%s" fill="none"/>' % (CX + (RC - 3) * math.cos(ax), CY + (RC - 3) * math.sin(ax), q[0], q[1], PATCH, INNER))
            poly(p, penta(q[0], q[1], RE, ang + 180), PATCH)   # رأس رو به مرکز
        poly(p, penta(CX, CY, RC, -90), PATCH)
        p.raw('</g>')
        # ثابت‌ها (در همان clip): سایهٔ تیز هلالی و برق
        crescent(p, c, R, (-9, -9), '#4a3a8c', .2)
        ha = math.radians(-126); tx, ty = -math.sin(ha), math.cos(ha); nx, ny = math.cos(ha), math.sin(ha)
        hx, hy = CX + 26 * nx, CY + 26 * ny
        poly(p, [(hx + tx * 7 + nx * 2.2, hy + ty * 7 + ny * 2.2), (hx + tx * 7 - nx * 2.2, hy + ty * 7 - ny * 2.2), (hx - tx * 7 - nx * 2.2, hy - ty * 7 - ny * 2.2), (hx - tx * 7 + nx * 2.2, hy - ty * 7 + ny * 2.2)], B_L)
        p.raw('</g>')
        p.stroke(disc, PART, j=0, step=99)                # خط دور ۵٫۸ روی همه
    return p


if __name__ == '__main__':
    p = build()
    mo = {'ball': dict(offsets=[(-ROLL, 0), (-ROLL * .75, 0), (-ROLL * .5, 0), (-ROLL * .25, 0), (0, 0)])}
    r = finish(p, 'football', None, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_football_ball': dict(type='translate+rotate', from_offset_units=[-ROLL, 0], from_offset_map_px=round(-ROLL * K, 1), to=[0, 0],
                                                    duration_s=1.6, easing='ease-out (آرام کندتر می‌شود)', repeat=1,
                                                    spin=dict(layer='node_football_ball_spin', center=[CX + 100, CY + 150], deg_cw=round(math.degrees(ROLL / R), 1), note='چرخش ساعت‌گرد (غلتیدن به راست) هم‌زمان با انتقال و با همان easing؛ در پایان زاویه ۰ (ایستا)'),
                                                    note='حالت ایستا = توپ روی نشان گچی؛ بدون حلقهٔ بیکار؛ سایه و برق ثابت‌اند'),
                         'reduced_motion': 'ایستا'}
    (OUTD / 'football.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
