#!/usr/bin/env python3
"""ایستگاه «اسکله» (M07): الاکلنگ/اهرم روی سکوی دریایی. تکیه‌گاه ثابت؛ تخته+صندوق = لایهٔ متحرک node_pier_lever (چرخش ±۱۲° حول تکیه‌گاه)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import station_kit as K_
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/batch1/pier'
WOOD = '#ffd84d'; WOOD_D = '#d9961c'; RED = '#ef6a4a'; BOX = '#a4e07a'
PX, PY = 0, -52          # تکیه‌گاه
HALF = 52                # نیم‌طول تخته
ANG = 12


def build(out=OUTD):
    p = Pen('pier', 'sea'); pad(p, line=((-62, 14), (-44, 19)), tri=((-60, -8), (62, 12)), dot=(58, -15))
    # تکیه‌گاه ثابت (زیر تخته، کامل و پیوسته)
    p.tipshadow(0, 5, 24); p.foot_tip(0, 5, 12)
    p.shape([(-22, 6), (22, 6), (7, PY), (-7, PY)], RED, OUT, j=.2, step=5)
    p.ln((-9, -2), (-4, -26), INNER, CREAM, j=.1, probe='خط داخلی (درخشش تکیه‌گاه)')
    with layer(p, 'lever'):
        p.shape([(-HALF, PY - 7), (HALF, PY - 7), (HALF, PY + 7), (-HALF, PY + 7)], WOOD, OUT, j=.2, step=5)
        p.ln((14, PY), (HALF - 8, PY), INNER, WOOD_D, j=.1, probe='خط داخلی (تختهٔ اهرم)')
        p.shape([(-HALF + 6, PY - 7 - 20), (-HALF + 26, PY - 7 - 20), (-HALF + 26, PY - 7), (-HALF + 6, PY - 7)], BOX, PART, j=.2, step=5)
        p.shape(ell(PX, PY, 5, 5, 0, 360, 20), NAVY, INNER, j=0, clip=False)
    return p


def lever_motion(p, stand, dsf=4):
    import numpy as np
    A = lambda im: im[..., 3] > 128
    i, j = p.layers['lever']; body = ''.join(p.o[i:j])
    top = A(K_._shot(K_._poly(p.padtop), dsf)); sil = top | A(K_._shot(K_._poly(K_._wall_pts(p)), dsf))
    cols = sil.any(0); low = np.where(cols, sil.shape[0] - 1 - np.argmax(sil[::-1], 0), -1)
    allowed = cols[None, :] & (np.arange(sil.shape[0])[:, None] <= low[None, :])
    U = np.zeros_like(sil); angs = [-ANG, -ANG / 2, 0, ANG / 2, ANG]
    for a in angs: U |= A(K_._shot('<g transform="rotate(%s %s %s)">%s</g>' % (a, PX, PY, body), dsf))
    xs = np.where(U.any(0))[0]; px = np.where(top.any(0))[0]
    sx, sy = (100 * K + stand[0]) * dsf, (150 * K + stand[1]) * dsf
    yy, xx = np.mgrid[0:U.shape[0], 0:U.shape[1]]
    r = dict(part='lever', angles=angs, out_px=round(float((U & ~allowed).sum()) / dsf ** 2, 1),
             x_margin=round(float(min(xs.min() - px.min(), px.max() - xs.max())) / dsf, 1),
             stand_to_motion=round(float(np.hypot(xx - sx, yy - sy)[U].min()) / dsf, 1))
    r['ok'] = r['out_px'] == 0 and r['x_margin'] >= 8 and r['stand_to_motion'] >= 10
    return r


STAND = (0, 17)

if __name__ == '__main__':
    p = build()
    r = finish(p, 'pier', STAND, motion={}, out=OUTD, shots=SHOTS)
    m = lever_motion(p, STAND); r['motion'] = [m]; r['ok'] = bool(r['ok'] and m['ok'])
    sp = r['spec']; sp['motion'] = ['node_pier_lever']; sp['motion_spec'] = dict(rotate=[PX, PY], range_deg=[-ANG, ANG], note='تخته+صندوق حول تکیه‌گاه؛ تکیه‌گاه ثابت')
    (OUTD / 'pier.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(r, ensure_ascii=False, indent=1))
