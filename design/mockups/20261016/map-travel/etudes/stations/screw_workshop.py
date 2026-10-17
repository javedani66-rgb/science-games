#!/usr/bin/env python3
"""ایستگاه «پیچ‌کاری» (اتود ب) با station_kit: پیچ بلند + مهرهٔ بزرگ روی رزوه. مهره = لایهٔ متحرک node_screw_workshop_nut."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent     # station_kit.HERE (etudes/) را نپوشاند

XF = (1.0, 0.0, 0.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
BLUE = '#8fb5f2'; PURP = '#8f8bd6'; HEAD_S = '#d6e8ff'; HEAD_T = '#f1f8ff'; THREAD = '#ffe08a'
NUT_T = '#ffd84d'; NUT_L = '#f2b92c'; NUT_R = '#d9961c'; NUT_H = '#8a5f0c'


def screw(pen, f, w=15, Lb=100, hw=28, hh=14, P=16, d=4, bottom='tip', y0=0, probe=True, head=True, body=True, lim=None):
    """پیچ در مختصات محلی (نوک در (0,0)، سر بالا). f: تبدیل نقاط."""
    ys = []; y = -Lb + 12
    lim = lim if lim is not None else (-26 if bottom == 'tip' else y0 - 12)
    while y + P / 2 + 3 < lim: ys.append(y); y += P
    L = [(-w, -Lb)]; R = [(w, -Lb)]
    for yk in ys:
        L += [(-w, yk - 3), (-w - d, yk), (-w, yk + 3)]
        yr = yk + P / 2; R += [(w, yr - 3), (w + d, yr), (w, yr + 3)]
    if bottom == 'tip':
        L += [(-w, -16), (0, y0)]; R += [(w, -16)]
        poly = L + R[::-1]
    else:
        ry = .34 * w
        L += [(-w, y0)]; R += [(w, y0)]
        poly = L + ell(0, y0, w, ry, 0, 180, 14)[1:-1][::-1] + R[::-1]
    if body:
        dd = pen._d(TP(f, poly), .7, 11); pen.clip.append(dd)
        cid = '%s_c%d' % (pen.uid, pen.k)
        strip = [(w * .3, -Lb - 2), (w + d + 3, -Lb - 2), (w + d + 3, y0 + 4), (w * .3, y0 + 4)]
        pen.raw('<path d="%s" fill="%s"/><clipPath id="%s"><path d="%s"/></clipPath><path d="%s" fill="%s" clip-path="url(#%s)"/>' % (
            dd, BLUE, cid, dd, hd(pen.X(TP(f, strip)), True, 2, 0, 999), PURP, cid))
        for i, yk in enumerate(ys):
            pen.ln(f((-w + 2, yk)), f((w - 2, yk + P / 2)), PART, THREAD, j=.1, probe='رزوه (جزء)' if (probe and i == 1) else None)
        pen.raw('<path d="%s" fill="none" class="eo" stroke-width="%s"/>' % (dd, OUT))
    if head:
        ry = .34 * hw; top = -Lb - hh
        pen.shape(TP(f, ell(0, -Lb, hw, ry, 0, 180, 18) + [(-hw, top), (hw, top)]), HEAD_S, OUT)
        pen.shape(TP(f, ell(0, top, hw, ry, 0, 360, 30)), HEAD_T, OUT)
        ph = math.radians(24)
        a = (-.6 * hw * math.cos(ph), -.6 * ry * math.sin(ph) + top); b = (.6 * hw * math.cos(ph), .6 * ry * math.sin(ph) + top)
        pen.ln(f(a), f(b), PART, NAVY, j=.1, probe='شیار سر پیچ (جزء)' if probe else None)
        pen.ln(f((-hw + 8, top + 5)), f((-hw + 8, -Lb - 3)), INNER, CREAM, j=.1, probe='خط داخلی (درخشش)' if probe else None)
        if probe: pen.probes.append(('خط دور پیچ (لبهٔ سر)', OUT, pen.X(f((-hw, top + hh * .7))), (1, 0), NAVY))
    return poly


def hexv(cx, cy, R, k=.4):
    h = k * R * .866
    return [(cx + R, cy), (cx + R / 2, cy + h), (cx - R / 2, cy + h), (cx - R, cy), (cx - R / 2, cy - h), (cx + R / 2, cy - h)]


def nut_back(pen, cx, cy, R, h, hole):
    """لایهٔ پشت مهره: کل پیکره (وجه‌ها، رویه، سوراخ تیره)؛ بدنهٔ پیچ روی آن می‌آید."""
    v = hexv(cx, cy, R); lo = [(x, y + h) for x, y in v]
    pen.fill([v[0], v[1], lo[1], lo[0]], NUT_R); pen.fill([v[1], v[2], lo[2], lo[1]], NUT_L); pen.fill([v[2], v[3], lo[3], lo[2]], '#e8a51f')
    sil = [v[3], v[4], v[5], v[0], lo[0], lo[1], lo[2], lo[3]]
    pen.shape(sil, 'none', OUT, step=5, j=.4, clip=False)
    pen.shape(v, NUT_T, OUT, step=5, j=.4, clip=False)
    pen.shape(ell(cx, cy, hole, hole * .4, 0, 360, 24), NUT_H, SEAM, j=.3, clip=False)


def nut_front(pen, cx, cy, R, h, hole, probe=False):
    """لایهٔ جلوی مهره: وجه‌های جلو + هلال جلوی رویه (زیر سوراخ)؛ پیچ از سوراخ رد می‌شود و پشت این لایه می‌رود."""
    v = hexv(cx, cy, R); lo = [(x, y + h) for x, y in v]
    pen.fill([v[0], v[1], lo[1], lo[0]], NUT_R); pen.fill([v[1], v[2], lo[2], lo[1]], NUT_L); pen.fill([v[2], v[3], lo[3], lo[2]], '#e8a51f')
    arc = ell(cx, cy, hole, hole * .4, 180, 0, 24)
    cres = [v[0], v[1], v[2], v[3]] + arc
    pen.fill(cres, NUT_T)
    front = [v[3], v[2], v[1], v[0], lo[0], lo[1], lo[2], lo[3]]
    pen.stroke(front, OUT, j=.4, step=5)
    for a, b in ((v[1], lo[1]), (v[2], lo[2])): pen.ln(a, b, SEAM, NAVY, j=.1, probe='درز ریز (مهره)' if (probe and a is v[1]) else None)
    pen.raw('<path d="%s" fill="none" class="eo" stroke-width="%s"/>' % (hd(pen.X(arc), False, 6, .3, 5), SEAM))
    pen.ln((cx - R + 7, cy + .4 * R * .5 + 4), (cx - R + 7, cy + h - 3), INNER, '#fff3c4', j=.1)


NUT_C = -64; RANGE = 22     # مرکز مهره (مختصات symbol) و بازهٔ حرکت ±۲۲


def build(out=HERE, legacy_shadow=False):
    p = Pen('screw_workshop', 'land'); pad(p, line=((-62, 12), (-44, 17)), tri=((-60, -6), (61, 13)), dot=(56, -12))
    p.xf = XF
    p.tipshadow(0, 8); p.foot_tip(0, 8, 10)
    w, Lb, R, h, hole = 13, 132, 40, 20, 28
    f = rot(0, 8, 0)
    with layer(p, 'nut_back'): nut_back(p, 0, NUT_C, R, h, hole)
    screw(p, f, w=w, Lb=Lb, hw=28, hh=16, bottom='tip', head=True, lim=-20)       # بدنهٔ پیوسته + سر
    with layer(p, 'nut_front'): nut_front(p, 0, NUT_C, R, h, hole, probe=True)
    return p, symbol(p, 'screw_workshop', ['nut_back', 'nut_front'], out=out, legacy_shadow=legacy_shadow)


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/screw_workshop'
OUTD = HERE / 'out'


if __name__ == '__main__':
    p, sym = build(out=OUTD)
    offs = [p.V(o) for o in [(0, -RANGE), (0, -RANGE / 2), (0, 0), (0, RANGE / 2), (0, RANGE)]]
    r = finish(p, 'screw_workshop', STAND, motion={'nut_back': dict(offsets=offs), 'nut_front': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    print(json.dumps(r, ensure_ascii=False, indent=1))
