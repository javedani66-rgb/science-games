#!/usr/bin/env python3
"""ایستگاه B02 «انبار مصالح» (سرزمین شهر، سکو آبی‌خاکستری ۲۱۳°) — دور ۵ (دستور مدیر هنری: دو پشتهٔ برابر گونی روی پالت، ۶۰٪ وسط).
طرح قطعه‌به‌قطعه (واحد symbol، xf=1، مرکز سکو ≈ (0,0)، کف پالت y=15):
 ۱ دو پالت چوبی (مرکز ±19): عرشه ۳۶×۷ (y 4..11) + سه پایهٔ ۸×۴ (y 11..15) با شکاف تیره؛ چوب #b77a3a.
 ۲ گونی پایین: خوابیده، بدنهٔ بالشی ۲۶×۲۰ (کرم #f3e1b0)، دهانهٔ بسته‌شده به‌صورت دُم کوتاه سمت چپ با نوار قرمز.
 ۳ گونی بالا (لایهٔ bags): ایستاده و کمی افتاده، بدنه ۲۴×۱۸، گردن ۱۰ با نوار قرمز و چین‌دار بالا (ذوزنقهٔ باز).
 ۴ هر گونی یک سایهٔ تیز راست داخل بدنه؛ بدون برچسب و ریزه. سایهٔ تماس زیر هر پالت.
 رنگ: کرم ≈۴۲°، قرمز، چوب ≈۳۰°؛ سکو ۲۱۳°. دو پشته دقیقاً یکسان.
لایهٔ متحرک node_materials_store_bags = گونی بالاییِ هر دو پشته؛ حالت ایستا = روی پشته."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/materials_store'

S_B, S_L, S_D = '#f6e6b8', '#fffaea', '#d9b979'
W_B, W_L, W_D = '#b77a3a', '#d9a463', '#6e421a'
RED, RED_D = '#e0402e', '#a82a1c'
XF = (1.2, 0, -2)
PX = (-24, 24)
GROUND, DECK0, DECK1 = 15, 3, 11
DROP = 16


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def rrect(x0, y0, x1, y1, r, n=5):
    pts = []
    for (ox, oy, a0) in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((ox + r * math.cos(a), oy + r * math.sin(a)))
    return pts


def pallet(p, c):
    pts = [(c - 24, DECK0), (c + 24, DECK0), (c + 24, GROUND), (c - 24, GROUND)]
    p.shape(pts, W_B, PART, j=.05, step=99)
    poly(p, [(c - 19, DECK0 + 2.5), (c + 19, DECK0 + 2.5), (c + 19, DECK0 + 4.3), (c - 19, DECK0 + 4.3)], W_L)
    for dx in (-13, 13): poly(p, [(c + dx - 7, GROUND - 5.5), (c + dx + 7, GROUND - 5.5), (c + dx + 7, GROUND - 2), (c + dx - 7, GROUND - 2)], W_D)
    p.stroke(pts, PART, j=.05, step=99)


def sack(p, bx, by):
    """گونی بالشی خوابیده: بدنه ۳۰×۲۲ از x=bx، کف y=by. دم چین‌دارِ بسته‌شده سمت چپ؛ طناب قرمز پهن."""
    yc = by - 11
    fr = [(bx + 3, yc - 8), (bx - 14, yc - 13), (bx - 14, yc + 13), (bx + 3, yc + 8)]
    p.shape(fr, S_B, PART, j=.05, step=99)
    poly(p, [(bx - 7, yc - 11), (bx - 1, yc - 9.2), (bx - 1, yc + 9.2), (bx - 7, yc + 11)], RED)
    p.stroke(fr, PART, j=.05, step=99)
    body = rrect(bx, by - 22, bx + 30, by, 10)
    p.shape(body, S_B, PART, j=.05, step=99)
    poly(p, [(bx + 23, yc - 5), (bx + 26.5, yc - 5), (bx + 26.5, yc + 7), (bx + 23, yc + 7)], S_D)
    poly(p, [(bx + 8, by - 17), (bx + 19, by - 17), (bx + 19, by - 14.5), (bx + 8, by - 14.5)], S_L)
    p.stroke(body, PART, j=.05, step=99)


def build(out=OUTD):
    p = Pen('materials_store', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((72, -22), (80, 8)), dot=(-74, -14)); p.xf = XF
    for cx in PX:
        p.tipshadow(cx, GROUND + 1.5, 28); p.foot_tip(cx, GROUND, 18)
    for cx in PX: pallet(p, cx)
    for cx in PX: sack(p, cx - 12, DECK0)
    with layer(p, 'bags'):
        for cx in PX: sack(p, cx - 10, DECK0 - 22)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    offs = [p.V((0, -DROP)), p.V((0, -DROP / 2)), (0, 0)]
    r = finish(p, 'materials_store', STAND, motion={'bags': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_materials_store_bags': dict(
        layer='گونی بالاییِ هر دو پشته (هم‌حرکت)', dx=0, dy_from=-DROP, dy_to=0, dur_s=1.4,
        note='هنگام رسیدن: هر دو گونی از ۱۵ واحد بالاتر پایین می‌افتند و روی پشته می‌نشینند (جهش خیلی کوچک)؛ حالت ایستا = روی پشته؛ بدون حلقهٔ بیکار؛ بدون عدد/عقربه.'),
        'reduced_motion': 'گونی‌ها روی پشته (ایستا)'}
    (OUTD / 'materials_store.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
