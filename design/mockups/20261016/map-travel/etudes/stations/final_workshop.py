#!/usr/bin/env python3
"""ایستگاه «کارگاه ماشین مرکب» (M12): قهرمان = دو چرخ‌دندهٔ درگیر (۸ و ۶ دندانه)، بزرگ پایین-چپ و کوچک بالا-راست، همه روی سکو.
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
PITCH = 16.5                                            # گام دندانه (طول کمان) برابر در هر دو چرخ ⇒ درگیری درست
TH = math.radians(-42)                                  # جهت از چرخ بزرگ به کوچک (بالا-راست)
RB, RS = 8 * PITCH / (2 * math.pi), 6 * PITCH / (2 * math.pi)
CB = (-32, 1)
CS = (CB[0] + (RB + RS) * math.cos(TH), CB[1] + (RB + RS) * math.sin(TH))
B = (CB[0], CB[1], RB, 8, math.degrees(TH))              # cx, cy, r گام، تعداد دندانه، فاز (دندانه روی خط تماس)
S = (CS[0], CS[1], RS, 6, math.degrees(TH) + 210)        # فاز کوچک: شکاف روی خط تماس
FOOT = 22


def gear_pts(cx, cy, rp, n, ph):
    pt = 360.0 / n; out = []
    for k in range(n):
        a = ph + k * pt
        for da, r in ((-.34, rp - 3), (-.15, rp + 4.5), (.15, rp + 4.5), (.34, rp - 3)):
            t = math.radians(a + da * pt); out.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return out


def gear(p, g, top, low, hub, probe=False):
    cx, cy, rp, n, ph = g
    p.shape(gear_pts(cx, cy, rp, n, ph), top, PART, j=.2, step=99)
    p.fill(ell(cx, cy, rp * .5, rp * .5, 0, 360, 32), low)
    mx, my = p.X((cx, cy)); p.raw('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (mx, my, 3.6 * p.xf[0], hub))
    t = math.radians(ph + 45 if n == 8 else ph + 30)
    p.ln((cx, cy), (cx + rp * .5 * math.cos(t), cy + rp * .5 * math.sin(t)), PART, hub, j=.1, probe=('نشانهٔ چرخش (جزء)' if probe else None))


def build(out=None, legacy_shadow=False):
    p = Pen('final_workshop', 'land'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(CB[0] + 4, CB[1] + RB + 3, 30)
    with layer(p, 'gear_big'): gear(p, B, Y_T, Y_L, Y_H, probe=True)
    with layer(p, 'gear_small'): gear(p, S, G_T, G_L, G_H)
    return p, symbol(p, 'final_workshop', ['gear_big', 'gear_small'], out=out, legacy_shadow=legacy_shadow)


STAND = None     # خودکار: find_stand
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/final_workshop'
OUTD = HERE / 'out'

if __name__ == '__main__':
    p, sym = build(out=OUTD)
    r = finish(p, 'final_workshop', STAND, motion={'gear_big': dict(rotate=p.X((B[0], B[1]))), 'gear_small': dict(rotate=p.X((S[0], S[1])))}, out=OUTD, shots=SHOTS)
    sp = json.loads((OUTD / 'final_workshop.json').read_text())
    sp['motion_spec'] = {'node_final_workshop_gear_big': dict(center=list(p.X((B[0], B[1]))), deg_per_turn=360, dir='cw'),
                         'node_final_workshop_gear_small': dict(center=list(p.X((S[0], S[1]))), ratio=-8 / 6, dir='ccw', note='کوچک=-(8/6)×بزرگ؛ چرخ بالا، چرخ پایین')}
    (OUTD / 'final_workshop.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False, indent=1))
