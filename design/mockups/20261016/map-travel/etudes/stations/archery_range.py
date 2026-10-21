#!/usr/bin/env python3
"""ایستگاه F03 «میدان کمان‌کِشی» (سرزمین ورزشگاه، سکوی سبز): کمان چوبی نارنجی-قهوه‌ای ایستاده، دو سر نوک‌تیز، زه سمت راست،
یک تیر با پر دم روی زه. لایهٔ متحرک node_archery_range_string = زه + تیر (با هم). حالت ایستا = زه کشیده‌شده (پایان حرکت)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/archery'

import functools, station_kit as _k
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)

WOOD = '#e0702a'; WOOD_D = '#a8480f'; WOOD_L = '#f59a55'; GRIP = '#c8321f'
STRING = '#fff3c4'; SHAFT = '#f6dfa4'; HEAD = '#dfe6f2'; FEA = '#ffffff'; FEA2 = '#ff5a48'
XF = (1.0, -11.0, -4.0)
YT, YB = -128, -4              # نوک بالا و پایین کمان
YM = (YT + YB) / 2             # مرکز (جای تیر)
HALF = (YB - YT) / 2
BELLY = 36                     # عمق خمیدگی کمان به چپ
NOCK = 12                      # جای ته تیر روی زه در حالت کشیده (ایستا)
PULL = 11                      # جابه‌جایی زه/تیر از حالت رها تا کشیده (واحد symbol ≈ ۸px نقشه)
AY = YM - 16                  # ارتفاع تیر (کمی بالاتر از دستگیره)
TIP = -50                      # نوک تیر (حالت کشیده)


def bow_center(t):
    return (-BELLY * (1 - t * t) ** 1.15, YM + HALF * t)


def limb(a, b, n=40):
    """چندضلعی چوب کمان بین پارامتر a..b؛ ضخامت از میانه (۱۲) به نوک (۰) باریک می‌شود."""
    L, R = [], []
    for i in range(n + 1):
        t = a + (b - a) * i / n; x, y = bow_center(t)
        e = 1e-3; x2, y2 = bow_center(min(1, t + e)); x1, y1 = bow_center(max(-1, t - e))
        dx, dy = x2 - x1, y2 - y1; m = math.hypot(dx, dy); nx, ny = -dy / m, dx / m     # نرمال (به سمت راست/زه = +x)
        w = 1.5 + 10.5 * (1 - abs(t) ** 2.0)
        L.append((x - nx * w * .85, y - ny * w * .85)); R.append((x + nx * w * .85, y + ny * w * .85))
    return L, R


def rawpoly(p, pts, fill, sw, miter=True):
    q = p.X(pts)
    d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="%s" stroke-miterlimit="8"/>' % (d, fill, sw, 'miter' if miter else 'round'))
    p.clip.append(d)


def build():
    p = Pen('archery_range', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-2, 7, 11); p.foot_tip(-2, 7, 8)
    # بدنهٔ کمان: یک تکهٔ پیوسته (نوک‌تیز)، بدون زه
    L, R = limb(-1, 1, 60)
    rawpoly(p, L + R[::-1], WOOD, OUT)
    # خط روشن چوب روی بازوها (داخل بدنه)
    for a, b in ((-.88, -.22), (.22, .88)):
        pts = [((lambda c: (c[0] - 4.5, c[1]))(bow_center(a + (b - a) * i / 10))) for i in range(11)]
        for u, v in zip(pts, pts[1:]): p.ln(u, v, INNER, WOOD_L, j=.05)
    # دستگیره (قرمز، رنگ تخت)
    gl, gr = limb(-.13, .13, 6)
    p.fill(gl + gr[::-1], GRIP)
    for s in (-.06, .06):
        c = bow_center(s); p.ln((c[0] - 8, c[1]), (c[0] + 8, c[1]), INNER, WOOD_D, j=.05)
    # لایهٔ متحرک: زه + تیر
    with layer(p, 'string'):
        tt = (0, YT + 1); tb = (0, YB - 1); nk = (NOCK, AY)
        p.ln(tt, nk, INNER + 2.4, NAVY, j=.05); p.ln(nk, tb, INNER + 2.4, NAVY, j=.05)       # زیرخط تیره تا زه روی سبز گم نشود
        p.ln(tt, nk, INNER, STRING, j=.05, probe='زه (بالا)'); p.ln(nk, tb, INNER, STRING, j=.05)
        # تیر: چوب + نوک فلزی + پر دم؛ روی زه، بالای دستگیره
        p.ln((NOCK - 28, AY), (TIP + 22, AY), PART + 3, NAVY, j=.0)
        p.ln((NOCK + 1, AY), (TIP + 22, AY), PART, SHAFT, j=.0, probe='تیر (چوب)')
        rawpoly(p, [(TIP, AY), (TIP + 26, AY - 11), (TIP + 20, AY), (TIP + 26, AY + 11)], HEAD, INNER + 1)
        for sgn in (-1, 1):
            rawpoly(p, [(NOCK - 1, AY + sgn * 2), (NOCK - 12, AY + sgn * 14), (NOCK - 30, AY + sgn * 14), (NOCK - 22, AY + sgn * 2)], FEA2 if sgn < 0 else FEA, INNER + 1, miter=False)
        p.ln((NOCK - 22, AY), (NOCK + 1, AY), PART, SHAFT, j=.0)
    return p


if __name__ == '__main__':
    p = build()
    offs = [p.V((-PULL, 0)), (0, 0)]
    r = finish(p, 'archery_range', None, motion={'string': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    nk_rest = p.X((NOCK - PULL, AY)); nk_end = p.X((NOCK, AY))
    ms = {'node_archery_range_string': dict(
        kind='زه + تیر با هم؛ حالت ایستا = حالت کشیده (پایان حرکت)',
        translate_x_symbol_units=[-PULL * XF[0], 0], translate_x_map_px=[round(-PULL * XF[0] * K, 1), 0],
        nock_rest=[round(v, 1) for v in nk_rest], nock_end=[round(v, 1) for v in nk_end],
        duration_s=.7, easing='ease-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        string_ends='دو سر زه روی نوک کمان می‌ماند: زه را به‌صورت path-morph (یا دو خط با انتهای ثابت) اجرا کن؛ نوک تیر و پر دم با ته تیر (translateX) می‌روند. حالت رها: ته تیر در x=%.1f' % nk_rest[0],
        note='بدنهٔ کمان ثابت و کامل؛ بدون حلقهٔ بیکار.')}
    ms['reduced_motion'] = 'ثابت در حالت کشیده'
    sp['motion_spec'] = ms
    (OUTD / 'archery_range.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
