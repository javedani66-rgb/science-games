#!/usr/bin/env python3
"""M03 «رمپ بارگیری» نسخهٔ B (فقط آزمون): عقب کامیون تخت‌دار + تختهٔ شیب‌دار از کف تخت تا زمین + جعبه روی تخته.
لایهٔ متحرک node_loading_ramp_b_crate = فقط جعبه (+ تسمه)، در امتداد شیب بالا می‌رود؛ وضعیت ایستا = پایان."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kitB/loading_ramp_b'
_k.margin_check = functools.partial(_k.margin_check, min_margin=4); _k.motion_check = functools.partial(_k.motion_check, min_margin=4)

CAB = '#ffd84d'; CAB_L = '#fff2a8'; CAB_D = '#d9961c'; GLASS = '#cfeaff'
BED = '#c98a3a'; BED_L = '#e8b25a'; BED_D = '#8a5f0c'
BRD = '#e8b25a'; BRD_L = '#fff0c4'; BRD_D = '#b8742f'
CR = '#f2552e'; CR_L = '#ff9a6c'; CR_D = '#b8381f'; STRAP = '#fff3c4'
WH = '#7b8fe0'; R = 11; WY = 2
GY = WY + R                                   # زمین
BT = -16                                      # سطح کف تخت
P0 = (-14.0, BT); P1 = (30.0, 4.0)           # لبهٔ بالای تخته
TH = 8
ANG = math.atan2(P1[1] - P0[1], P1[0] - P0[0])
U = (math.cos(ANG), math.sin(ANG)); N = (math.sin(ANG), -math.cos(ANG))   # N = عمود رو به بالا
LEN = math.hypot(P1[0] - P0[0], P1[1] - P0[1])
CW, CH = 17, 17
S_END = 9                                     # فاصلهٔ لبهٔ بالایی جعبه از سر بالای تخته در حالت پایان (جعبه کنار کف تخت)
DRISE = 13


def A(p, v, k=1): return (p[0] + v[0] * k, p[1] + v[1] * k)
def on(s): return A(P0, U, s)
def flat(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))
def rect(p, x0, y0, x1, y1, col): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def wheel(p, cx):
    p.shape(ell(cx, WY, R, R, 0, 360, 40), WH, PART, j=.3, step=99, clip=False)
    for a in (0, 60, 120):
        t = math.radians(a + 25)
        p.ln((cx - (R - 4) * math.cos(t), WY - (R - 4) * math.sin(t)), (cx + (R - 4) * math.cos(t), WY + (R - 4) * math.sin(t)), INNER, '#fff3c4', j=0)
    p.raw('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s"/>' % (*p.X((cx, WY)), NAVY))
    p.raw('<circle cx="%.1f" cy="%.1f" r="1.4" fill="%s"/>' % (*p.X((cx, WY)), '#ffd84d'))


def build():
    p = Pen('loading_ramp_b', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    for cx in (-52, -28): p.tipshadow(cx, GY - 1, 13); p.foot_tip(cx, GY - 2, 6)
    p.tipshadow(26, GY, 12); p.foot_tip(28, GY - 1, 6)
    # کابین (پشت)
    cab = [(-64, -2), (-64, -22), (-58, -40), (-42, -40), (-42, -2)]
    p.shape(cab, CAB, PART, j=.2, step=8)
    flat(p, [(-61, -22), (-61, -22), (-56, -37.5), (-52, -37.5), (-52, -22)] , CAB_L) if False else None
    flat(p, [(-58, -24), (-54, -36), (-48, -36), (-48, -24)], GLASS)                       # شیشه
    flat(p, [(-45, -40), (-45, -2), (-42, -2), (-42, -40)], CAB_D)                          # سایهٔ تیز راست
    rect(p, -61, -20, -55, -17, CAB_L)
    p.stroke(cab, PART, j=.2, step=8)
    # کف تخت
    bed = [(-46, BT), (-8, BT), (-8, -3), (-46, -3)]
    p.shape(bed, BED, PART, j=.2, step=8)
    rect(p, -42, BT + 3, -12, BT + 6.5, BED_L)
    rect(p, -12, BT + 3, -9, -6, BED_D)
    p.stroke(bed, PART, j=.2, step=8)
    for cx in (-52, -28): wheel(p, cx)
    # تختهٔ رمپ (روی لبهٔ کف تخت)
    B = [P0, P1, A(P1, (0, 1), TH), A(P0, (0, 1), TH)]
    p.shape(B, BRD, PART, j=.2, step=9)
    flat(p, [A(P0, (0, 1), TH - 3), A(P1, (0, 1), TH - 3), A(P1, (0, 1), TH - .5), A(P0, (0, 1), TH - .5)], BRD_D)   # لبهٔ زیر تیره
    flat(p, [A(A(P0, N, -3.5), U, 4), A(A(P1, N, -3.5), U, -3), A(A(P1, N, -7), U, -3), A(A(P0, N, -7), U, 4)], BRD_L)  # نوار روشن
    p.stroke(B, PART, j=.2, step=9)
    p.raw('<circle cx="%.1f" cy="%.1f" r="2.3" fill="#ffd84d"/>' % p.X(A(P0, (3, 4.5))))                            # لولای زرد
    with layer(p, 'crate'):
        b = A(on(S_END), U, 0)
        b = A(P0, U, S_END)
        c0 = b; c1 = A(b, U, CW); c2 = A(c1, N, CH); c3 = A(c0, N, CH)
        p.shape([c0, c1, c2, c3], CR, PART, j=.15, step=8, clip=False)
        flat(p, [A(c3, U, 3), A(c2, U, -3), A(A(c2, U, -3), N, -3.5), A(A(c3, U, 3), N, -3.5)], CR_L)                   # نور بالا
        flat(p, [A(c1, U, -5), A(c1, U, -2.5), A(c2, U, -2.5), A(c2, U, -5)], CR_D) if False else None
        flat(p, [A(c1, U, -4), c1, c2, A(c2, U, -4)], CR_D, .0) if False else None
        p.stroke([c0, c1, c2, c3], PART, j=.15, step=8)
        m = CW / 2; w = 2
        flat(p, [A(A(c0, U, m - w), N, 3), A(A(c0, U, m + w), N, 3), A(A(c3, U, m + w), N, -3), A(A(c3, U, m - w), N, -3)], STRAP)   # تسمه
    return p


XF = (1.2, -10.0, -2.0)
STAND = None
if __name__ == '__main__':
    if len(sys.argv) > 3: XF = tuple(float(v) for v in sys.argv[1:4])
    p = build()
    offs = [p.V((U[0] * DRISE * f, U[1] * DRISE * f)) for f in (1, .75, .5, .25, 0)]
    r = finish(p, 'loading_ramp_b', STAND, motion={'crate': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    so = [round(v, 1) for v in p.V((U[0] * DRISE, U[1] * DRISE))]
    sp['motion_spec'] = {'node_loading_ramp_b_crate': dict(translate_xy=[so, [0, 0]], unit='واحد symbol', dir_deg=round(math.degrees(ANG), 1),
        start='جعبه پایین‌تر روی تخته', end='حالت ایستا (پایان): جعبه بالاتر نزدیک کف تخت', note='فقط جعبه و تسمه؛ بدون چرخش؛ یک‌بار هنگام رسیدن')}
    (OUTD / 'loading_ramp_b.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
