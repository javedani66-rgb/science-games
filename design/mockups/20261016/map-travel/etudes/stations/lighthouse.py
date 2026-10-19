#!/usr/bin/env python3
"""ایستگاه «فانوس دریایی» (E04): قهرمان = برج راه‌راه با اتاقک چراغ، سکوی دریایی.
لایه‌های متحرک node_lighthouse_beam_l و node_lighthouse_beam_r = پرتوهای چپ و راست (یکی‌درمیان/جاروب حول اتاقک).
برج و اتاقک چراغ ثابت و کامل زیر پرتو."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/lighthouse'
import functools, station_kit as _k   # D122/D123: حاشیهٔ چپ/راست ≥۴px (بدون دست‌زدن به کیت)
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)
XF = (1.25, -26.7, -6.5)             # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
RED = '#ef6a4a'; RED_D = '#c9452c'; WHITE = '#fffaf0'; WHITE_D = '#e6dcf0'; GLASS = '#ffd84d'; GLASS_D = '#d9961c'; ROOF = '#ef6a4a'
BEAM = '#ffe45c'; ROCK = '#c9c2e6'; ROCK_D = '#8f88c4'; ROCK_L = '#ece8ff'; DOOR = '#7a3a12'; SEA_W = '#d6e8ff'
YB, YT = -8, -50           # پای برج، بالای برج
WB, WT = 33, 21            # نیم‌پهنای پایین/بالا
LY = -70                   # ارتفاع مرکز اتاقک چراغ
BX = 39                    # دورترین نقطهٔ پرتوها از محور


def hw(y): return WB + (WT - WB) * (y - YB) / (YT - YB)


def poly(p, pts, col, op=1):
    """چندضلعی تیز (بدون گردشدن گوشه‌ها) در قاب قهرمان."""
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def build(out=OUTD):
    p = Pen('lighthouse', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(0, 14, 40); p.foot_tip(0, 14, 18)
    # دو پرتو، دو لایهٔ جدا (چپ/راست)، پشت اتاقک چراغ؛ از مرکز اتاقک (0, LY) شروع می‌شوند تا scaleX/opacity حول همان مرکز انجام شود
    for nm, s_ in (('beam_l', -1), ('beam_r', 1)):
        with layer(p, nm):
            poly(p, [(s_ * 4, LY - 6), (s_ * BX, LY - 11), (s_ * BX, LY + 7), (s_ * 4, LY + 6)], BEAM, .95)
            poly(p, [(s_ * 14, LY - 3), (s_ * (BX - 6), LY - 6), (s_ * (BX - 6), LY + 3), (s_ * 14, LY + 3)], '#fffbd0')   # هستهٔ روشن
    # صخرهٔ پایه: سنگ اصلی + دو سنگ کوچک
    p.shape([(-40, 16), (-38, 2), (-26, -8), (26, -8), (38, 2), (40, 16)], ROCK, PART, j=.3, step=99)
    p.ln((-28, 8), (-10, 3), INNER, ROCK_D, j=.1); p.ln((12, 4), (30, 10), INNER, ROCK_D, j=.1); p.ln((-31, -1), (-20, -4), INNER, ROCK_L, j=.1)
    p.shape([(30, 14), (30, 8), (36, 6), (42, 14)], ROCK_L, PART, j=.3, step=99) if False else None
    # برج
    body = [(-WB, YB), (WB, YB), (WT, YT), (-WT, YT)]
    p.shape(body, WHITE, OUT, j=.2, step=5)
    for a_, b_ in ((-16, -27), (-37, -50)):                           # نوارهای قرمز، به‌اندازهٔ دیوارهٔ برج
        poly(p, [(-hw(a_), a_), (hw(a_), a_), (hw(b_), b_), (-hw(b_), b_)], RED)
    poly(p, [(hw(YB) * .35, YB), (hw(YB), YB), (hw(YT), YT), (hw(YT) * .35, YT)], '#241a5e', .13)    # سایهٔ سمت راست
    p.stroke(body, OUT, j=.2, step=5)
    p.shape([(-8, YB), (8, YB), (8, -15), (0, -21), (-8, -15)], DOOR, INNER, j=.1, step=99, clip=False)   # در
    for wy in (-32,):                                                       # پنجرهٔ برج (نوار سفید میانی)
        p.shape([(-4, wy - 4), (4, wy - 4), (4, wy + 4), (-4, wy + 4)], GLASS, INNER, j=.1, step=99, clip=False)
    # اتاقک چراغ + بالکن + سقف
    p.shape([(-14, YT - 7), (14, YT - 7), (14, LY - 12), (-14, LY - 12)], GLASS, PART, j=.2, step=5)
    p.ln((0, YT - 18), (0, LY - 9), INNER, GLASS_D, j=.1, probe='خط داخلی (قاب چراغ)')
    p.shape([(-34, YT), (34, YT), (34, YT - 7), (-34, YT - 7)], GLASS_D, PART, j=.2, step=5)             # کف بالکن
    for x_ in (-30, -15, 15, 30):
        p.ln((x_, YT - 7), (x_, YT - 17), INNER, '#241a5e', j=.05)                                        # تیرک نرده
    p.ln((-32, YT - 17), (32, YT - 17), INNER, '#241a5e', j=.05)                                          # دستهٔ نرده
    p.shape([(-18, LY - 12), (18, LY - 12), (0, LY - 31)], ROOF, PART, j=.2, step=5)
    p.shape(ell(0, LY - 36, 4.5, 4.5, 0, 360, 14), GLASS, INNER, j=.1, step=99, clip=False)               # گوی نوک سقف
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    r = finish(p, 'lighthouse', STAND, motion={'beam_l': dict(offsets=[(0, 0)]), 'beam_r': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    cx, cy = p.X((0, LY)); ax = p.X((0, 0))[0]
    sym_err = round(abs((ax - p.X((-BX, 0))[0]) - (p.X((BX, 0))[0] - ax)), 3); assert sym_err < .01
    sp = r['spec']
    sp['motion_spec'] = {
        'pivot': [round(cx, 1), round(cy, 1)],
        'note': 'برج، بالکن و اتاقک چراغ (شیشه+سقف+گوی) ثابت و کاملند؛ دو پرتو پشت اتاقک‌اند و از مرکز اتاقک شروع می‌شوند. نیم‌سر چرخان وجود ندارد؛ پرتوها جاروب می‌شوند.',
        'node_lighthouse_beam_l': dict(transform_origin=[round(cx, 1), round(cy, 1)], mode_alternate='opacity 1→0.12 و برگشت', mode_sweep='scaleX 1→0.25 (حول مرکز اتاقک) همراه opacity 1→0.3', cycle_s=2.4, phase='شروع در 0'),
        'node_lighthouse_beam_r': dict(transform_origin=[round(cx, 1), round(cy, 1)], mode_alternate='همان، با نیم‌چرخه جابه‌جایی (delay 1.2s) تا یکی‌درمیان روشن شوند', mode_sweep='همان با delay 1.2s', cycle_s=2.4, phase='delay 1.2s'),
        'bounds': 'حالت ایستا بیشینهٔ گسترش است؛ هر حالت دیگر زیرمجموعهٔ آن است پس بیرون‌زدگی ندارد (motion_check با حالت ایستا)',
        'reduced_motion': 'هر دو پرتو ثابت و روشن',
        'beams_symmetry_error': sym_err}
    (OUTD / 'lighthouse.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
