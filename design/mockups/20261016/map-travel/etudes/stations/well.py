#!/usr/bin/env python3
"""ایستگاه E07 «چاه آب» (سرزمین مزرعه، سکوی farm #d6c98a، رنگ‌مایهٔ ۵۰°).
طرح قطعه‌به‌قطعه (واحد symbol؛ CX=-34 مرکز چاه؛ پایهٔ تماس y=+7):
 ۱) بدنهٔ چاه: استوانهٔ سنگی نیم‌پهنا ۳۶، از y=-36 تا کف خمیده (+7)؛ سنگ آبی-خاکستری ۲۱۳° (سه پله: پایه/روشن/تیره)؛ سه ردیف درز آجری تخت.
 ۲) لبهٔ دهانه (بیضی ۳۶×۱۰ روشن) و دهانهٔ تیرهٔ آب (۲۲×۷).
 ۳) دو ستون چوبی (۱۳ پهنا، مرکز CX±۲۶، y -98..-33) با خط PART، روی لبه می‌نشینند.
 ۴) قرقره: استوانهٔ افقی کرم (پهنا ۵۲، ارتفاع ۱۶، y=-66) بین ستون‌ها؛ دو سرش پشت ستون‌ها می‌رود.
 ۵) سقف دوشیبهٔ کوچک: مثلث ۹۶×۲۶ قرمز-قهوه‌ای (رنگ‌مایهٔ ≈۵°، دور از ۵۰°)؛ لبهٔ تیره، نور چپ، سایهٔ تیز راست.
 ۶) چرخ‌چاه: دیسک r=12 در (CX+40,-66) با دو پره و کلاهک (روی محور افقی قرقره y=-66).
 ۷) دلو (لایهٔ متحرک): دلوِ نارنجی با طناب از قرقره، روی محور CX؛ حالت ایستا = پایین.
حرکت: node_well_bucket ۸ واحد بالا و آهسته برمی‌گردد؛ یک‌بار؛ بدون حلقهٔ بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/well'

S_B, S_L, S_D = '#b4c3d6', '#d6e1ee', '#8798b3'          # سنگ
R_B, R_L, R_D = '#b3362b', '#dc5a4a', '#7a1f19'          # سقف
W_B, W_L, W_D = '#c28a4a', '#e2ae6c', '#966126'          # چوب ستون
C_B, C_L, C_D = '#f3e2b5', '#fff6d8', '#c99a58'          # قرقره/چرخ
B_B, B_L, B_D = '#f0913a', '#ffc07a', '#a8531a'          # دلو
ROPE = '#6b4a2a'; HOLE = '#1f3560'; WATER = '#4f86c6'; YEL = '#ffd84d'

CX = -34
HW = 36
RIM_Y = -36
BASE = 7
SPOOL_Y = -66
PX = 26
PW = 13
POST_T, POST_B = -98, -33
ROOF_B, ROOF_T = -92, -118
BUCKET_DY = -8


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def rect(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def build(out=OUTD):
    p = Pen('well', 'farm'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.tipshadow(CX + 4, BASE + 3, 34); p.foot_tip(CX + 2, BASE + 2, 26)
    # ۱) بدنهٔ سنگی
    body = [(CX - HW, RIM_Y), (CX + HW, RIM_Y)] + ell(CX, BASE - 8, HW, 8, 0, 180, 16)
    p.shape(body, S_B, OUT, j=.15, step=8)
    poly(p, rect(CX - HW + 4.5, -30, CX - HW + 8.5, -1), S_L)
    k = math.acos(14 / HW)
    arc = [(CX + HW * math.cos(a * k / 10), BASE - 8 + 8 * math.sin(a * k / 10)) for a in range(11)]
    poly(p, [(CX + 14, RIM_Y + 2), (CX + HW, RIM_Y + 2)] + arc, S_D)
    for y in (-22, -8):
        poly(p, rect(CX - HW + 5, y - 1.6, CX + HW - 5, y + 1.6), S_D)
    for y0, y1, xs in ((-22, -8, (-12, 12)), (-8, 3, (-24, 0, 24))):
        for x in xs:
            poly(p, rect(CX + x - 1.6, y0 + 1.6, CX + x + 1.6, y1 - 1.6), S_D)
    p.stroke(body, OUT, j=.15, step=8)
    # ۲) لبه و دهانه
    p.shape(ell(CX, RIM_Y, HW, 10, 0, 360, 40), S_L, PART, j=.1, step=8)
    p.shape(ell(CX, RIM_Y + 1, 22, 7, 0, 360, 32), HOLE, INNER, j=.05, step=99, clip=False)
    poly(p, [(CX - 9, RIM_Y + 3.5), (CX + 9, RIM_Y + 3.5), (CX + 7, RIM_Y + 5.5), (CX - 7, RIM_Y + 5.5)], WATER)
    # ۳) دلو و طناب (لایهٔ متحرک)
    with layer(p, 'bucket'):
        p.ln((CX, SPOOL_Y + 4), (CX, -46), INNER, ROPE, j=0)
        bk = [(CX - 12, -46), (CX + 12, -46), (CX + 9.5, -31), (CX - 9.5, -31)]
        p.shape(bk, B_B, PART, j=.1, step=8)
        poly(p, rect(CX - 8, -44, CX - 5, -33.5), B_L)
        poly(p, [(CX + 3, -44), (CX + 8, -44), (CX + 7, -33.5), (CX + 3, -33.5)], B_D)
        poly(p, rect(CX - 8.5, -40.5, CX + 8.5, -37), '#7a3a1a')
    # ۴) قرقره
    sp = rect(CX - PX, SPOOL_Y - 8, CX + PX, SPOOL_Y + 8)
    p.shape(sp, C_B, PART, j=.1, step=8)
    poly(p, rect(CX - PX + 5, SPOOL_Y - 5, CX + PX - 5, SPOOL_Y - 2.5), C_L)
    for x in (-12, 0, 12): poly(p, rect(CX + x - 1.8, SPOOL_Y - 1, CX + x + 1.8, SPOOL_Y + 5), C_D)
    p.stroke(sp, PART, j=.1, step=8)
    # ۵) ستون‌ها
    for s in (-1, 1):
        c = CX + s * PX
        pts = rect(c - PW / 2, POST_T, c + PW / 2, POST_B)
        p.shape(pts, W_B, PART, j=.1, step=8)
        poly(p, rect(c - 3.4, POST_T + 8, c - 1.4, POST_B - 4), W_L)
        poly(p, rect(c + 0.8, POST_T + 8, c + 3.4, POST_B - 4), W_D)
        p.stroke(pts, PART, j=.1, step=8)
    # ۶) سقف
    roof = [(CX - 48, ROOF_B), (CX + 48, ROOF_B), (CX, ROOF_T)]
    p.shape(roof, R_B, PART, j=.1, step=8)
    poly(p, [(CX - 9, -111), (CX - 5.5, -111), (CX - 24.5, -100), (CX - 28, -100)], R_L)
    poly(p, [(CX + 8, -110), (CX + 42, -94.5), (CX + 42, ROOF_B), (CX + 8, ROOF_B)], R_D)
    poly(p, [(CX - 40.5, -96), (CX + 40.5, -96), (CX + 48, ROOF_B), (CX - 48, ROOF_B)], R_D)
    p.stroke(roof, PART, j=.1, step=8)
    # ۷) چرخ‌چاه
    WX = CX + 40
    p.shape(ell(WX, SPOOL_Y, 12, 12, 0, 360, 24), C_B, PART, j=.05, step=99, clip=False)
    poly(p, rect(WX - 9, SPOOL_Y - 1.75, WX + 9, SPOOL_Y + 1.75), C_D)
    poly(p, rect(WX - 1.75, SPOOL_Y - 9, WX + 1.75, SPOOL_Y + 9), C_D)
    p.shape(ell(WX, SPOOL_Y, 4.5, 4.5, 0, 360, 12), '#7a4a1f', INNER, j=0, step=99, clip=False)
    disc(p, WX, SPOOL_Y, 1.6, YEL)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    r = finish(p, 'well', STAND, motion={'bucket': dict(offsets=[(0, 0), (0, BUCKET_DY)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_well_bucket': dict(offsets=[[0, 0], [0, BUCKET_DY]], dy_px=round(BUCKET_DY * K, 1), duration_s=2, repeat=1,
                                                  note='دلو با طناب ۸ واحد (≈۵٫۸px نقشه) بالا می‌رود و آهسته به حالت ایستا برمی‌گردد؛ سر طناب پشت قرقره می‌ماند؛ بدون حلقهٔ بیکار؛ تزئینی.'),
                         'reduced_motion': 'دلو ثابت در حالت پایین'}
    (OUTD / 'well.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
