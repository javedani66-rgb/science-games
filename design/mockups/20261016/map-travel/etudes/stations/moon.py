#!/usr/bin/env python3
"""ایستگاه W03 «کرهٔ ماه» (سرزمین فضا، پالت space، سکوی بنفش #7a5cd0، رنگ‌مایه ۲۵۶°). شناسه: moon (node_moon_shade).
طرح قطعه‌به‌قطعه (۷ جزء):
 ۱) پایهٔ سنگی: استوانهٔ کوتاه (rx=28، ارتفاع ≈۹) آبی-خاکستری #b7c4d4 / روشن #dbe4ee / تیره #8e9db6 (رنگ‌مایهٔ ≈۲۱۵°، ۴۱° از سکو)؛ دور OUT. ماه «نیمه‌نشسته» در آن فرو رفته.
 ۲) کره: r=38 مرکز (-12,-26)، کرم #fff4d2 (رنگ‌مایه ≈۴۶°، ۲۱۰° از سکو)؛ دور OUT؛ پایین ۴ واحد درون پایه.
 ۳) سه دهانه (تخت، بدون خط): بیضی‌های #dccb9e با سایهٔ تیز نیم‌هلالی #b8a578 بالا-چپ؛ فاصلهٔ دهانه‌ها ≥۸، همه داخل کره.
 ۴) برق سفید بالا-چپ (ثابت).
 ۵) سایهٔ هلالی لاوندر #d2c4e4 پایین-راست = کره منهای کرهٔ جابه‌جاشده (چندضلعی تیز، داخل کره با ۳ واحد حاشیه).
 ۶) سایهٔ تماس زیر پایه + ردپا برای حاشیهٔ ۸px.
لایهٔ متحرک: node_moon_shade (فقط هلال سایه). از ≈۶px بالا-چپ می‌لغزد و در جای ایستا می‌ایستد؛ ۳ث؛ یک‌بار. بدنهٔ کره زیر آن کامل است."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/moon'

M_B, M_L, M_SH = '#fff4d2', '#ffffff', '#d2c4e4'
CR, CR_D = '#e6d49a', '#a89258'
S_B, S_L, S_D = '#b7c4d4', '#dbe4ee', '#8e9db6'
R = 48
CX, CY = 0, -40
SLIDE = 8.3          # ≈۶px نقشه (واحد)
SH = (-14, -14)


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))   # حاشیهٔ هم‌رنگ: درز مویی بین چندضلعی‌ها نماند


def crescent(p, c, r, s, col):
    d = math.hypot(*s); h = math.sqrt(r * r - d * d / 4)
    mx, my = c[0] + s[0] / 2, c[1] + s[1] / 2; ux, uy = s[0] / d, s[1] / d
    P = [(mx - uy * h, my + ux * h), (mx + uy * h, my - ux * h)]
    c2 = (c[0] + s[0], c[1] + s[1]); t = math.radians(45)
    ang = lambda cc, q: math.atan2(q[1] - cc[1], q[0] - cc[0])

    def sweep(cc, a, b, n=24):
        da = (b - a) % (2 * math.pi)
        if not (0 <= (t - a) % (2 * math.pi) <= da): da -= 2 * math.pi
        return [(cc[0] + r * math.cos(a + da * i / n), cc[1] + r * math.sin(a + da * i / n)) for i in range(n + 1)]
    q1, q2 = P
    poly(p, sweep(c, ang(c, q1), ang(c, q2)) + sweep(c2, ang(c2, q2), ang(c2, q1)), col)


def crater(p, x, y, r):
    a, b = p.X((x, y))
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>' % (a, b, r, r * .8, CR))
    # هلال تیرهٔ بالا-چپ = بیضی تیره منهای بیضی روشنِ جابه‌جا (بدون نوک)؛ بیضی روشن درون تیره می‌ماند
    ex, ey = p.X((x + r * .2, y + r * .16))
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>' % (a, b, r, r * .8, CR_D))
    p.raw('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>' % (ex, ey, r * .78, r * .62, CR))


def build():
    p = Pen('moon', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 0, 0)
    p.tipshadow(CX + 3, 19, 42); p.foot_tip(CX, 18, 38)
    body = ell(CX, 6, 40, 11, 180, 360, 36) + ell(CX, 15, 40, 11, 0, 180, 36)
    p.shape(body, S_B, OUT, j=.0, step=99)
    poly(p, ell(CX, 6, 40, 11, 180, 360, 36) + ell(CX, 6, 40, 11, 360, 180, 36), S_L)                      # رویهٔ روشن (بیضی کامل)
    poly(p, ell(CX, 15, 40, 11, 0, 180, 36) + ell(CX, 6, 40, 11, 180, 0, 36), S_D)                         # نوار تیرهٔ جلو
    p.stroke(body, OUT, j=.0, step=99)
    sph = p.shape(ell(CX, CY, R, R, 0, 352.5, 47), M_B, OUT, j=0, step=99)   # بدون نقطهٔ تکراری Z (زائدهٔ خط دور)
    crater(p, CX - 25, CY - 9, 9.5); crater(p, CX + 16, CY - 26, 9.5); crater(p, CX - 9, CY + 19, 8.5)
    ha = math.radians(-126); tx, ty = -math.sin(ha), math.cos(ha); nx, ny = math.cos(ha), math.sin(ha)
    hx, hy = CX + 36 * nx, CY + 36 * ny
    poly(p, [(hx + tx * 8 + nx * 3, hy + ty * 8 + ny * 3), (hx + tx * 8 - nx * 3, hy + ty * 8 - ny * 3), (hx - tx * 8 - nx * 3, hy - ty * 8 - ny * 3), (hx - tx * 8 + nx * 3, hy - ty * 8 + ny * 3)], M_L)
    p.raw('<defs><clipPath id="moon_sph_clip"><circle cx="%.1f" cy="%.1f" r="%.1f"/></clipPath></defs><g clip-path="url(#moon_sph_clip)">' % (*p.X((CX, CY)), R - 2))
    with layer(p, 'shade'):
        crescent(p, (CX, CY), R - 3, SH, M_SH)
    p.raw('</g>')
    p.raw('<path d="%s" fill="none" class="eo" stroke-width="%s"/>' % (sph, OUT))       # همان دور کره دوباره روی هلال
    return p


if __name__ == '__main__':
    p = build()
    a = SLIDE / math.sqrt(2)
    mo = {'shade': dict(offsets=[(-a, -a), (-a * .75, -a * .75), (-a * .5, -a * .5), (-a * .25, -a * .25), (0, 0)])}
    r = finish(p, 'moon', None, motion=mo, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_moon_shade': dict(type='translate', from_offset_units=[round(-a, 1), round(-a, 1)], from_offset_map_px=round(-SLIDE * K, 1), to=[0, 0],
                                                 duration_s=3, easing='ease-in-out', repeat=1,
                                                 note='فقط هلال سایه روی کره می‌لغزد؛ حالت ایستا = پایان؛ بدنهٔ کره زیر آن کامل؛ بدون حلقهٔ بیکار'),
                         'reduced_motion': 'ایستا'}
    (OUTD / 'moon.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
