#!/usr/bin/env python3
"""ایستگاه «انبار الوار» (بازطراحی ۱۷ اکتبر): پشتهٔ سه کندهٔ افقی از کنار (دو پایین، یکی بالا) با پوست قهوه‌ای؛
سرِ بریده (حلقهٔ سالیانه) فقط در سمت چپ هر کنده؛ دو طناب دور پشته. سکوی زمینی.
لایهٔ متحرک node_lumber_marks = حلقهٔ سالیانهٔ سرِ کندهٔ بالا (کمان باز که حول مرکز سر می‌چرخد). حلقه‌های کنده‌های پایین ثابت‌اند."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/lumber'
XF = (1.0, 10.0, -4.0)
BARK = '#a8672f'; BARK_D = '#7a4a1f'; FACE = '#f2cf8e'; RING = '#c98f4a'; PITH = '#8a4f1f'; ROPE = '#fff3c4'
R = 12; FX = 9; FY = R - 2.9       # نیم‌پهنای بیضی سر، و نیم‌ارتفاع درونی آن
TOP = (-38, -13, -42)              # (x چپ، x راست، y مرکز) — کندهٔ بالا (D122: پشتهٔ بلندتر، سه ردیف)
LOW = [(-52, -27, 14), (-25, 0, 14), (-52, -27, -14), (-25, 0, -14)]


def body(p, x0, x1, cy):
    pts = ell(x1, cy, 4, R, -90, 90, 10) + ell(x0, cy, FX, R, 90, 270, 14)
    p.shape(pts, BARK, PART, j=.3, step=99)
    p.fill(ell(x0, cy, FX - 2.9, FY, 0, 360, 24), FACE)                  # سرِ بریده (بیضی کامل)
    p.ln((x0 + 12, cy + 6), (x0 + 22, cy + 6), INNER, BARK_D, j=.1)       # خط پوست


def rings(p, x0, cy, arc=False):
    x, y = p.X((x0, cy))
    if not arc:
        p.raw('<circle cx="%.1f" cy="%.1f" r="2.2" fill="%s"/>' % (x, y, PITH)); return
    r = 3.8; a0, a1 = math.radians(40), math.radians(310)
    d = 'M%.1f,%.1f A%s,%s 0 1 1 %.1f,%.1f' % (x + r * math.cos(a0), y + r * math.sin(a0), r, r, x + r * math.cos(a1), y + r * math.sin(a1))
    p.raw('<path d="%s" fill="none" stroke="%s" stroke-width="3.5" stroke-linecap="round"/>' % (d, RING))


def build(out=OUTD):
    p = Pen('lumber', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    for x0, x1, cy in LOW[:2]:
        c = (x0 + x1) / 2; p.tipshadow(c, cy + R - 1, 13); p.foot_tip(c, cy + R - 2, 7)
    for x0, x1, cy in LOW: body(p, x0, x1, cy)
    body(p, *TOP)
    p.probes.append(('خط دور کنده (جزء)', PART, p.X((-40, LOW[0][2] + R)), (0, 1), NAVY))
    for x0, x1, cy in LOW: rings(p, x0, cy)
    rings(p, TOP[0], TOP[2])
    for xr in (-14,):   # طناب دور پشته
        p.ln((xr, -52), (xr, 24), INNER, ROPE, j=.1)
    with layer(p, 'marks'): rings(p, TOP[0], TOP[2], arc=True)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'lumber', STAND, motion={'marks': dict(rotate=p.X((TOP[0], TOP[2])))}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(marks=dict(layer='node_lumber_marks', rotate_about=[round(v, 1) for v in p.X((TOP[0], TOP[2]))],
                                                         note='کمان حلقهٔ سالیانهٔ سرِ کندهٔ بالا (سمت چپ) می‌چرخد؛ id قدیمی حفظ شد، محتوا تغییر کرد'))
    (OUTD / 'lumber.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')}, ensure_ascii=False))
