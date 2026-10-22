#!/usr/bin/env python3
"""ایستگاه M05 «انبار تیرآهن» (سکوی شهر، city). id=beam_store؛ لایهٔ متحرک node_beam_store_prop.
طرح قطعه‌به‌قطعه (واحد symbol؛ y منفی = بالا؛ زمین G=10):
 تیرآهن (فلز کرمی-خاکستری سه پله #e6dfca / #fffaf0 / #b3aa92): مستطیل بلند ۹۴×۱۶ (PART) با نوار روشن بالا (بالهٔ بالایی)، نوار تیرهٔ پایین
   (بالهٔ پایینی) و سه پرچ زرد؛ حول نقطهٔ تکیه‌گاه P=(-24,-14) با ۲۵° خوابیده (سر راست پایین و روی زمین، سر چپ بالا).
 تکیه‌گاه (آجری-نارنجی #e0702a / #ffa561 / #a64a16): بلوک ۲۴ پهن از زمین تا زیر تیر؛ لبهٔ بالایی موازی تیر و ۶ واحد داخل تیر (پشتِ تیر)؛
   لایهٔ node_beam_store_prop: از ۱۱ واحد راست‌تر تا جای نهایی (چپ، نزدیک جعبه)؛ حالت ایستا = پایان.
 جعبه (بنفش #8a5ad0 / #b992f0 / #5b3a9c): مربع ۲۸×۲۶ روی سر بالای تیر، هم‌شیب تیر، نوار نور بالا، دو آج، تسمهٔ زرد.
 سایهٔ تماس زیر تکیه‌گاه و سر پایین تیر."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/beam_store'

S_B, S_L, S_D = '#e6dfca', '#fffaf0', '#b3aa92'          # تیرآهن
F_B, F_L, F_D = '#e0702a', '#ffa561', '#a64a16'          # تکیه‌گاه
B_B, B_L, B_D = '#8a5ad0', '#b992f0', '#5b3a9c'          # جعبه
YEL = '#ffd84d'
G = 10
ANG = 25
P = (-24, -14)
U0, U1, TH = -42, 52, 16
SLIDE = 11
FW = 24
XF = (1.0, 8, 0)
f = rot(P[0], P[1], ANG)
M = math.tan(math.radians(ANG))


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def yu(x): return P[1] + M * (x - P[0])      # خط زیر تیر


def L(u0, u1, v0, v1): return TP(f, [(u0, v0), (u1, v0), (u1, v1), (u0, v1)])


def prop(p):
    xc = P[0]
    top = lambda x: yu(x) - 6
    pts = [(xc - FW / 2, G), (xc + FW / 2, G), (xc + FW / 2, top(xc + FW / 2)), (xc - FW / 2, top(xc - FW / 2))]
    p.shape(pts, F_B, PART, j=.1, step=6, clip=False)
    poly(p, [(xc - FW / 2 + 3.5, G - 3), (xc - FW / 2 + 7, G - 3), (xc - FW / 2 + 7, top(xc - FW / 2 + 5) + 12), (xc - FW / 2 + 3.5, top(xc - FW / 2 + 5) + 12)], F_L)       # نور
    poly(p, [(xc + 3, G - 3), (xc + FW / 2 - 3, G - 3), (xc + FW / 2 - 3, top(xc + FW / 2) + 12), (xc + 3, top(xc + 3) + 12)], F_D)                                          # سایهٔ تیز راست
    p.stroke(pts, PART, j=.1, step=6)


def beam(p):
    body = L(U0, U1, -TH, 0)
    p.shape(body, S_B, PART, j=.1, step=6, clip=False)
    poly(p, L(U0 + 4, U1 - 4, -TH + 3.5, -TH + 6.8), S_L)           # بالهٔ بالایی (روشن)
    poly(p, L(U0 + 4, U1 - 4, -6.8, -3.5), S_D)                      # بالهٔ پایینی (تیره)
    for u in (-6, 18, 42):
        a = f((u, -TH / 2)); disc(p, a[0], a[1], 2.2, YEL)            # پرچ
    p.stroke(body, PART, j=.1, step=6)


def box(p):
    u0, u1 = -38, -10; h = 26
    pts = L(u0, u1, -TH - h, -TH + 2)
    p.shape(pts, B_B, PART, j=.1, step=6, clip=False)
    poly(p, L(u0 + 4, u1 - 4, -TH - h + 4, -TH - h + 7.5), B_L)
    poly(p, L(u1 - 9, u1 - 4, -TH - h + 10, -TH - 3), B_D)           # سایهٔ تیز راست
    poly(p, L(u0 + 3, u1 - 3, -TH - 15, -TH - 11), YEL)              # تسمهٔ زرد
    p.stroke(pts, PART, j=.1, step=6)


def build(out=OUTD):
    p = Pen('beam_store', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(P[0] + 2, G + 2, 18); p.foot_tip(P[0], G, 12)
    rx = f((U1, 0))[0]
    p.tipshadow(rx - 2, G + 1, 9); p.foot_tip(rx - 4, G, 6)
    with layer(p, 'prop'): prop(p)
    beam(p)
    box(p)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    offs = [p.V(o) for o in [(SLIDE, 0), (SLIDE * .75, 0), (SLIDE * .5, 0), (SLIDE * .25, 0), (0, 0)]]
    r = finish(p, 'beam_store', STAND, motion={'prop': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_beam_store_prop': dict(translate_from=[SLIDE, 0], translate_to=[0, 0], dur_s=1.6, repeat=1,
                         note='تکیه‌گاه ≈۸px (۱۱ واحد) از راست به سوی جعبه می‌لغزد و می‌ماند؛ تیر و جعبه ثابت‌اند و لبهٔ تکیه‌گاه پشت تیر است؛ حالت ایستا = پایان؛ بدون حلقهٔ بیکار.'),
                         'reduced_motion': 'تکیه‌گاه در جای نهایی'}
    (OUTD / 'beam_store.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
