#!/usr/bin/env python3
"""ایستگاه W01 «ایستگاه بارگیری فضایی» (سرزمین فضا، سکوی 'space' رنگ‌مایه ۲۵۶°).
قهرمان: صندوق بار فضایی نقره‌ای (نمای روبه‌رو)، بدون ترازو؛ دو دستگیرهٔ کناری و چراغ کوچک روی درپوش.
طرح قطعه‌به‌قطعه (واحد symbol، مرکز محور CX، کف BASE):
 ۱ سایهٔ تماس: بیضی r=۳۶ زیر کف.
 ۲ دو دستگیره (پشت بدنه): مستطیل ۱۲ بیرون‌زده × ۲۴ بلند، فولادی خاکستری ۸d9099، شکاف تیره ۴×۱۰ وسط؛ ۴ واحد زیر بدنه می‌رود.
 ۳ بدنه: مستطیل ۶۰×۵۷ (CX±۳۰، y ‑۵۰..۷)، نقره‌ای گرم e6e5e3 / روشن fafaf8 / تیره bcbab6 (سه پله)؛ OUT؛
   نور چپ، سایهٔ تیز راست، ۳ شیار عمودی تخت (فاصلهٔ ۱۵)، کرسی تیره پایین ۶ واحد.
 ۴ درپوش (لبهٔ طلایی): مستطیل ۶۶×۱۶ (CX±۳۳، y ‑۶۴..‑۴۸) ffd84d / روشن fff3c4 / تیره d9961c؛ PART.
 ۵ پایهٔ چراغ: مستطیل ۲۰×۷ فولادی روی درپوش (محور CX). ۶ گنبد چراغ خاموش (ثابت): نیم‌دایره r=۸ قرمز تیره.
 ۷ لایهٔ متحرک node_space_loading_light: گنبد روشن ef6a4a + برق ffb59c، روی گنبد خاموش؛ چشمک = محوشدن لایه (۳ بار)، حالت پایان = روشن.
رنگ‌مایه: بدنه خنثی گرم (≈۴۰°)، طلایی ۴۸°، چراغ ۱۰°؛ همه دور از ۲۵۶° سکو. بدون ترازو/عدد/متن/پیکان."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/space_loading'

S_B, S_L, S_D = '#e6e5e3', '#fafaf8', '#bcbab6'      # نقره‌ای
G_B, G_L, G_D = '#ffd84d', '#fff3c4', '#d9961c'      # طلایی
H_B, H_D = '#a4a8b0', '#3f424c'                      # دستگیره/پایهٔ چراغ (فولاد)
L_B, L_L, L_OFF = '#ef6a4a', '#ffb59c', '#9c2f1c'   # چراغ

CX, BASE = -29, 7
BT, LT, LB = -46, -62, -44        # بالای بدنه، بالای درپوش، کف درپوش
BW, LW = 36, 39


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def dome(r=8):
    return [(CX + r * math.cos(math.radians(a)), -62 - 7 + 0 + r * math.sin(math.radians(a))) for a in range(180, 361, 15)]


def build(out=OUTD):
    p = Pen('space_loading', 'space'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = (1.0, 9, 0)
    p.tipshadow(CX + 2, BASE + 3, 36); p.foot_tip(CX, BASE + 2, 26)
    # ۲) دستگیره‌ها (پشت بدنه)
    for s in (-1, 1):
        x_in, x_out = CX + s * (BW - 4), CX + s * (BW + 14)
        p.shape(rect(min(x_in, x_out), -34, max(x_in, x_out), -4), H_B, PART, j=.12, step=6)
        xs = CX + s * (BW + 6.5)
        poly(p, rect(xs - 2.5, -26, xs + 2.5, -12), H_D)
    # ۳) بدنه
    body = rect(CX - BW, BT, CX + BW, BASE)
    p.shape(body, S_B, OUT, j=.12, step=6)
    poly(p, rect(CX - BW + 5, BT + 8, CX - BW + 8.5, BASE - 12), S_L)                               # نور
    poly(p, rect(CX + BW - 14, BT + 4, CX + BW - 3, BASE - 1), S_D)                                  # سایهٔ تیز راست
    poly(p, rect(CX - BW + 3, BASE - 7, CX + BW - 3, BASE - 1), S_D)                                 # کرسی
    for y in (-14,):
        poly(p, rect(CX - BW + 8, y - 1.95, CX + BW - 8, y + 1.95), S_D)                         # دو نوار افقی
    for sx in (-1, 1):
        x0 = CX + sx * (BW - 13)
        poly(p, rect(min(x0, x0 + sx * 9), BT + 5, max(x0, x0 + sx * 9), BT + 14), G_D if sx > 0 else G_B)   # گوشه‌بند طلایی
    p.stroke(body, OUT, j=.12, step=6)
    # ۴) درپوش طلایی
    lid = rect(CX - LW, LT, CX + LW, LB)
    p.shape(lid, G_B, PART, j=.12, step=6)
    poly(p, rect(CX - LW + 5, LT + 4, CX - LW + 8.5, LB - 4), G_L)
    poly(p, rect(CX + LW - 12, LT + 3, CX + LW - 3, LB - 1), G_D)
    p.stroke(lid, PART, j=.12, step=6)
    # ۵) پایهٔ چراغ و ۶) گنبد خاموش
    p.shape(rect(CX - 11, LT - 6, CX + 11, LT + 3), H_B, INNER, j=.05, step=99, clip=False)
    base_dome = [(CX + 10 * math.cos(math.radians(a)), LT - 6 + 10 * math.sin(math.radians(a))) for a in range(180, 361, 15)]
    p.shape(base_dome, L_OFF, INNER, j=.05, step=99, clip=False)
    # ۷) لایهٔ متحرک: گنبد روشن
    with layer(p, 'light'):
        p.shape(base_dome, L_B, INNER, j=.05, step=99, clip=False)
        poly(p, [(CX - 6, LT - 12), (CX - 2.5, LT - 12), (CX - 2.5, LT - 8.5), (CX - 6, LT - 8.5)], L_L)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'space_loading', STAND, motion={'light': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_space_loading_light': dict(kind='opacity-blink', blinks=3, duration_s=1.8, trigger='هنگام رسیدن', iterations=1,
                                                         note='لایهٔ گنبد روشن ۳ بار محو و دوباره پدیدار می‌شود (زیرش گنبد خاموش ثابت است)؛ حالت ایستا و پایان = روشن؛ تزئینی؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'چراغ روشن ثابت'}
    (OUTD / 'space_loading.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
