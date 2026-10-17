#!/usr/bin/env python3
"""ایستگاه «کارگاه ماشین مرکب» (M12): قهرمان = دو چرخ‌دندهٔ درگیر (۱۲ و ۸ دندانه) روی دو پایهٔ ثابت.
لایه‌های متحرک: node_final_workshop_gear_big (ساعتگرد) و node_final_workshop_gear_small (پاددوری).
نسبت سرعت: کوچک = -1.5 × بزرگ (۱۲/۸). فاز دندانه‌ها طوری است که دندانه در شکاف می‌نشیند."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent

Y_T = '#ffd84d'; Y_L = '#f2b92c'; Y_H = '#8a5f0c'
G_T = '#7fd36b'; G_L = '#4fae4a'; G_H = '#1f6b2e'      # چرخ‌دندهٔ دوم سبز تا دو ماشین جدا خوانده شوند
POST_L = '#8fb5f2'; POST_R = '#8f8bd6'
B = (-25, -44, 26, 12, 0)       # cx, cy, r گام، تعداد دندانه، فاز
S = (18, -44, 17, 8, 22.5)
FOOT = 26


def post(p, cx, cy):
    w = 9; yb = FOOT - 6
    base = ell(cx, yb, w, 4, 0, 180, 10)
    p.shape([(cx - w, cy)] + base[::-1] + [(cx + w, cy)], POST_L, OUT, j=.3, step=99)
    p.fill([(cx + 1, cy), (cx + w, cy)] + [q for q in base if q[0] >= cx + 1][::-1], POST_R)
    p.shape(ell(cx, yb, w + 11, 5, 0, 360, 24), POST_R, PART, j=.3, clip=False)


def gear_pts(cx, cy, rp, n, ph):
    pt = 360.0 / n; out = []
    for k in range(n):
        a = ph + k * pt
        for da, r in ((-.32, rp - 4), (-.17, rp + 4), (.17, rp + 4), (.32, rp - 4)):
            t = math.radians(a + da * pt); out.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return out


def gear(p, g, top, low, hub, probe=False, peg=False):
    cx, cy, rp, n, ph = g
    p.shape(gear_pts(cx, cy, rp, n, ph), top, OUT, j=.25, step=99)
    p.shape(ell(cx, cy, rp * .62, rp * .62, 0, 360, 32), low, INNER, j=.2, step=99, clip=False)
    for k in range(4):
        t = math.radians(ph + 45 + 90 * k)
        p.ln((cx + 8 * math.cos(t), cy + 8 * math.sin(t)), (cx + rp * .62 * math.cos(t), cy + rp * .62 * math.sin(t)),
             PART, hub, j=.1, probe=('پرهٔ چرخ‌دنده (جزء)' if probe and k == 0 else None))
    p.shape(ell(cx, cy, 8, 8, 0, 360, 20), top, INNER, j=.2, clip=False)


def build(out=HERE, legacy_shadow=False):
    p = Pen('final_workshop', 'land'); pad(p, line=((-62, 12), (-44, 17)), tri=((-60, -6), (61, 13)), dot=(56, -12))
    for g in (B, S):
        p.tipshadow(g[0], FOOT - 6, 18); p.foot_tip(g[0], FOOT - 6, 12)
    post(p, B[0], B[1]); post(p, S[0], S[1])
    with layer(p, 'gear_big'): gear(p, B, Y_T, Y_L, Y_H, probe=True)
    with layer(p, 'gear_small'): gear(p, S, G_T, G_L, G_H)
    for g, c in ((B, Y_H), (S, G_H)):
        p.shape(ell(g[0], g[1], 4, 4, 0, 360, 12), c, INNER, j=.1, clip=False)
    return p, symbol(p, 'final_workshop', ['gear_big', 'gear_small'], out=out, legacy_shadow=legacy_shadow)


STAND = (41, 4)
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/batch2/final_workshop'
OUTD = HERE / 'out'

if __name__ == '__main__':
    p, sym = build(out=OUTD)
    r = finish(p, 'final_workshop', STAND, motion={'gear_big': dict(rotate=(B[0], B[1])), 'gear_small': dict(rotate=(S[0], S[1]))}, out=OUTD, shots=SHOTS)
    sp = json.loads((OUTD / 'final_workshop.json').read_text())
    sp['motion_spec'] = {'node_final_workshop_gear_big': dict(center=[B[0], B[1]], deg_per_turn=360, dir='cw'),
                         'node_final_workshop_gear_small': dict(center=[S[0], S[1]], ratio=-1.5, dir='ccw', note='کوچک=-1.5×بزرگ')}
    (OUTD / 'final_workshop.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False, indent=1))
