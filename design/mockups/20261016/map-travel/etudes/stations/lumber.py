#!/usr/bin/env python3
"""ایستگاه «انبار الوار» (E03): پشتهٔ سه کنده (نمای مقطع). لایهٔ متحرک: نقش مقطع کندهٔ بالا (node_lumber_marks) که می‌چرخد."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent

BARK = '#a8672f'; FACE = '#f2cf8e'; RING = '#c98f4a'; PITH = '#8a4f1f'
CX = 12; R = 24; BY = -13
FACE_R = R - 10


def log(pen, cx, cy, marks=False):
    if not marks:
        pen.shape(ell(cx, cy, R, R, 0, 360, 28), BARK, OUT, j=.5)
        pen.shape(ell(cx, cy, FACE_R, FACE_R, 0, 360, 24), FACE, PART, j=.3, clip=False)
    else:
        # حلقهٔ سالانه (کمی خارج از مرکز) + ترک راست + مغز
        ox = 4
        pts = ell(cx + 2, cy, 7, 7, 0, 360, 20)
        pen.raw('<path d="M%s Z" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"/>' % (
            'L'.join('%.1f,%.1f' % p for p in pts), RING, INNER))
        pen.raw('<circle cx="%s" cy="%s" r="2.6" fill="%s"/>' % (cx + ox * .5, cy, PITH))


def build(out=HERE / 'out'):
    p = Pen('lumber', 'land'); pad(p, line=((-62, 12), (-44, 17)), tri=((-60, -6), (61, 13)), dot=(56, -12))
    for dx in (-R, R):
        p.tipshadow(CX + dx, 8, 12); p.foot_tip(CX + dx, 8, 12)
    ty = BY - math.sqrt((2 * R) ** 2 - R ** 2)
    log(p, CX - R, BY); log(p, CX + R, BY)
    log(p, CX, ty)
    with layer(p, 'marks'): log(p, CX, ty, marks=True)
    for dx in (-R, R): log(p, CX + dx, BY, marks=True)   # نقش ثابت کنده‌های پایین (بیرون از لایهٔ متحرک)
    return p, symbol(p, 'lumber', ['marks'], out=out), ty


STAND = (-38, 4)
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/batch1/lumber'

if __name__ == '__main__':
    p, sym, ty = build()
    r = finish(p, 'lumber', STAND, motion={'marks': dict(rotate=(CX, ty))}, out=HERE / 'out', shots=SHOTS)
    print(json.dumps(r, ensure_ascii=False, indent=1))
