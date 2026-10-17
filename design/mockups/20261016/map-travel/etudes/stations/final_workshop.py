#!/usr/bin/env python3
"""ایستگاه «کارگاه ماشین مرکب» (M12): قهرمان = دو چرخ‌دندهٔ درگیر (۸ و ۶ دندانه) روی یک صفحهٔ پشتی عمودی (بزرگ پایین، کوچک بالا).
لایه‌های متحرک: node_final_workshop_gear_big (ساعتگرد) و node_final_workshop_gear_small (پاددوری).
نسبت سرعت: کوچک = -(8/6) × بزرگ. فاز دندانه‌ها طوری است که دندانه در شکاف می‌نشیند.
طراحی دوباره برای خط ضخیم‌تر (D113، D110): دندانه‌های درشت‌تر و کم‌تر، دو چرخ روی هم (کم‌عرض)، رنگ تخت بدون خط دور کوچک."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent

XF = (1.0, 0.0, 0.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
Y_T = '#ffd84d'; Y_L = '#f2b92c'; Y_H = '#8a5f0c'
G_T = '#7fd36b'; G_L = '#4fae4a'; G_H = '#1f6b2e'      # چرخ‌دندهٔ دوم سبز تا دو ماشین جدا خوانده شوند
POST_L = '#8fb5f2'; POST_R = '#8f8bd6'
PITCH = 21.0                                            # گام دندانه (طول کمان) برابر در هر دو چرخ ⇒ درگیری درست
CXG = -26
B = (CXG, -32, 8 * PITCH / (2 * math.pi), 8, 0)         # cx, cy, r گام، تعداد دندانه، فاز
S = (CXG, -32 - (8 + 6) * PITCH / (2 * math.pi), 6 * PITCH / (2 * math.pi), 6, 0)
FOOT = 26


def plate(p):
    """صفحهٔ پشتی عمودی از پایه تا محور چرخ کوچک، دو رنگ مثل دیوارهٔ سکو؛ پایهٔ پهن زیر آن."""
    w = 9; yb = FOOT - 6; top = S[1]
    base = ell(CXG, yb, w, 4, 0, 180, 10)
    p.shape([(CXG - w, top)] + base[::-1] + [(CXG + w, top)], POST_L, OUT, j=.3, step=99)
    p.fill([(CXG + 1, top), (CXG + w, top)] + [q for q in base if q[0] >= CXG + 1][::-1], POST_R)
    p.shape(ell(CXG, yb, w + 12, 5, 0, 360, 24), POST_R, PART, j=.3, clip=False)


def gear_pts(cx, cy, rp, n, ph):
    pt = 360.0 / n; out = []
    for k in range(n):
        a = ph + k * pt
        for da, r in ((-.31, rp - 4), (-.2, rp + 4), (.2, rp + 4), (.31, rp - 4)):
            t = math.radians(a + da * pt); out.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return out


def gear(p, g, top, low, hub, probe=False):
    cx, cy, rp, n, ph = g
    p.shape(gear_pts(cx, cy, rp, n, ph), top, PART, j=.25, step=99)
    p.fill(ell(cx, cy, rp * .55, rp * .55, 0, 360, 32), low)
    t = math.radians(ph - 90)
    p.ln((cx, cy), (cx + rp * .55 * math.cos(t), cy + rp * .55 * math.sin(t)), PART, hub, j=.1, probe=('نشانهٔ چرخش (جزء)' if probe else None))
    mx, my = p.X((cx, cy)); p.raw('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (mx, my, 4.2 * p.xf[0], hub))


def build(out=None, legacy_shadow=False):
    p = Pen('final_workshop', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(CXG, FOOT - 6, 22); p.foot_tip(CXG, FOOT - 6, 12)
    plate(p)
    with layer(p, 'gear_big'): gear(p, B, Y_T, Y_L, Y_H, probe=True)
    with layer(p, 'gear_small'): gear(p, S, G_T, G_L, G_H)
    return p, symbol(p, 'final_workshop', ['gear_big', 'gear_small'], out=out, legacy_shadow=legacy_shadow)


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/final_workshop'
OUTD = HERE / 'out'

if __name__ == '__main__':
    p, sym = build(out=OUTD)
    r = finish(p, 'final_workshop', STAND, motion={'gear_big': dict(rotate=p.X((B[0], B[1]))), 'gear_small': dict(rotate=p.X((S[0], S[1])))}, out=OUTD, shots=SHOTS)
    sp = json.loads((OUTD / 'final_workshop.json').read_text())
    sp['motion_spec'] = {'node_final_workshop_gear_big': dict(center=list(p.X((B[0], B[1]))), deg_per_turn=360, dir='cw'),
                         'node_final_workshop_gear_small': dict(center=list(p.X((S[0], S[1]))), ratio=-8 / 6, dir='ccw', note='کوچک=-(8/6)×بزرگ؛ چرخ بالا، چرخ پایین')}
    (OUTD / 'final_workshop.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False, indent=1))
