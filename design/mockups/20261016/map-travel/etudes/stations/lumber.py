#!/usr/bin/env python3
"""ایستگاه «انبار الوار» (E03): پشتهٔ سه کنده (نمای مقطع). لایهٔ متحرک: نقش مقطع کندهٔ بالا (node_lumber_marks) که می‌چرخد.
طراحی دوباره برای خط ضخیم‌تر (D113): کنده‌ها بزرگ‌تر و ساده‌تر؛ رویهٔ مقطع بدون خط دور، فقط یک حلقه و یک مغز."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent

XF = (1.0, -24.0, 0.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
BARK = '#a8672f'; FACE = '#f2cf8e'; RING = '#c98f4a'; PITH = '#8a4f1f'
CX = 0; R = 17; BY = -4
FACE_R = 10.5


def log(pen, cx, cy, marks=False):
    if not marks:
        pen.shape(ell(cx, cy, R, R, 0, 360, 28), BARK, PART, j=.5)
        pen.fill(ell(cx, cy, FACE_R, FACE_R, 0, 360, 24), FACE)
    else:
        # حلقهٔ سالانه (کمی خارج از مرکز) + مغز
        pts = ell(cx + 2, cy, 5.5, 5.5, 0, 360, 20)
        pen.raw('<path d="M%s Z" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            'L'.join('%.1f,%.1f' % q for q in pen.X(pts)), RING, INNER))
        mx, my = pen.X((cx + 2, cy))
        pen.raw('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (mx, my, 2.4 * pen.xf[0], PITH))


def build(out=HERE / 'out'):
    p = Pen('lumber', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    for dx in (-R, R):
        p.tipshadow(CX + dx, BY + R - 2, 12); p.foot_tip(CX + dx, BY + R - 2, 8)
    ty = BY - math.sqrt((2 * R) ** 2 - R ** 2)
    log(p, CX - R, BY); log(p, CX + R, BY)
    p.probes.append(('خط دور کنده (جزء)', PART, p.X((CX - 2 * R, BY)), (1, 0), NAVY))
    log(p, CX, ty)
    with layer(p, 'marks'): log(p, CX, ty, marks=True)
    for dx in (-R, R): log(p, CX + dx, BY, marks=True)   # نقش ثابت کنده‌های پایین (بیرون از لایهٔ متحرک)
    return p, symbol(p, 'lumber', ['marks'], out=out), ty


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/lumber'

if __name__ == '__main__':
    p, sym, ty = build()
    r = finish(p, 'lumber', STAND, motion={'marks': dict(rotate=p.X((CX, ty)))}, out=HERE / 'out', shots=SHOTS)
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')}, ensure_ascii=False))
