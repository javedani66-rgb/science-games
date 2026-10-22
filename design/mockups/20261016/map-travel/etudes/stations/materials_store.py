#!/usr/bin/env python3
"""ایستگاه B02 «انبار مصالح» (سرزمین شهر، سکو #5b7390 رنگ‌مایهٔ ۲۱۳°). تصمیم مالک: دو پشتهٔ گونیِ برابر روی دو پالت هم‌سطح؛
بدون ترازو، بدون عدد/متن، بدون جرثقیل.

طرح قطعه‌به‌قطعه (واحد محلی؛ XF = مقیاس ۱٫۱۵):
 ۱ سایهٔ تماس: یک بیضی زیر هر پالت (rx ۲۰ = ۰٫۶۲ پهنای پالت ۳۲).
 ۲ پایه‌های پالت: دو بلوک ۹×۱۱ (چوب میانه #a8672f، INNER) در دو سر؛ بینشان ۱۴ فاصله (دیدنی ≈ ۱۰).
 ۳ چهار گونی روی هر پشته (۲۶×۲۲، گوشه‌های بریده ۳، دور PART، رنگ کرم #f3e1b0؛ سه پله: پایه/روشن #fff6dc/تیره #d9b979).
   نوار روشن افقی بالای هر گونی، برچسب مستطیلی قرمز تخت #d9503a (۱۰×۶)، سایهٔ تیز راست داخل گونی؛ دورِ گونی بعد از سایه دوباره کشیده می‌شود.
   جابه‌جایی افقی گونی‌ها در دو پشته دقیقاً یکی است (برابری): (۰، +۱٫۵، −۱٫۵، ۰).
 ۴ عرشهٔ پالت ۳۲×۱۱ (چوب #b77a3a، روشن #d9a463، تیره #7a4a1f، INNER) روی لبهٔ پایین گونی‌ها و جلوی آن‌ها (هم‌پوشانی ۶).
 ۵ لایهٔ متحرک node_materials_store_bags = گونی بالاییِ هر دو پشته؛ حالت ایستا = روی پشته.
 رنگ‌مایه: کرم ≈۴۲°، چوب ≈۳۰°، قرمز ≈۷°؛ سکو ۲۱۳° ⇒ فاصله ≥ ۱۷۰°.
 تفاوت مجاور: گونی کرم (L≈۹۰) / چوب (L≈۵۵)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/materials_store'

S_B, S_L, S_D = '#f3e1b0', '#fff6dc', '#d9b979'
W_B, W_L, W_D = '#b77a3a', '#d9a463', '#7a4a1f'
F_B = '#a8672f'
LAB = '#d9503a'
TIE = '#8a5f0c'

PX = (-23.5, 23.5)             # مرکز دو پشته
SW, SH, STEP = 37, 30, 25  # گونی
NS = 3                     # گونی در هر پشته
Y0 = 6                     # کف گونی اول
OFFS = (0, 3, -2)  # جابه‌جایی افقی؛ در دو پشته دقیقاً یکی است
DECK_W, DECK_Y0, DECK_Y1 = 38, 0, 11
GROUND = 19
DROP = 16


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sack_pts(cx, yb):
    """گونیِ گره‌دار: دو گوشهٔ بالا مثل نوک گره بالا می‌آیند، وسط بالا کمی فرو؛ بدنه پر و دو طرف گرد."""
    t = yb - SH
    rel = [(-15, -1), (-9, 2.5), (9, 2.5), (15, -1), (18, 8), (18.5, 19), (15, 26), (9, SH), (-9, SH), (-15, 26), (-18.5, 19), (-18, 8)]
    return [(cx + x, t + y) for x, y in rel]


def sack(p, cx, yb):
    top = yb - SH
    pts = sack_pts(cx, yb)
    p.shape(pts, S_B, INNER, j=.08, step=6)
    poly(p, [(cx + 10, top + 12), (cx + 15, top + 12), (cx + 15, yb - 5), (cx + 10, yb - 5)], S_D)             # سایهٔ تیز راست
    poly(p, [(cx - 14, top + 13), (cx - 10.5, top + 13), (cx - 10.5, yb - 7), (cx - 14, yb - 7)], S_L)           # نوار روشن
    poly(p, [(cx - 5, top + 15), (cx + 5, top + 15), (cx + 5, top + 21), (cx - 5, top + 21)], LAB)           # برچسب کوچک
    poly(p, [(cx - 8, top + 7), (cx + 8, top + 7), (cx + 8, top + 10), (cx - 8, top + 10)], TIE)                  # گرهٔ بالای گونی
    p.stroke(pts, INNER, j=.08, step=6)


def sack_y(i): return Y0 - STEP * i


def pallet_feet(p, cx):
    for dx in (-19, 10):
        p.shape([(cx + dx, DECK_Y1 - 4), (cx + dx + 9, DECK_Y1 - 4), (cx + dx + 9, GROUND), (cx + dx, GROUND)], F_B, INNER, j=.1, step=6, clip=False)
        poly(p, [(cx + dx + 5.5, DECK_Y1 + 1), (cx + dx + 7, DECK_Y1 + 1), (cx + dx + 7, GROUND - 2), (cx + dx + 5.5, GROUND - 2)], W_D)


def deck(p, cx):
    x0, x1 = cx - DECK_W / 2, cx + DECK_W / 2
    pts = [(x0, DECK_Y0), (x1, DECK_Y0), (x1, DECK_Y1), (x0, DECK_Y1)]
    p.shape(pts, W_B, INNER, j=.1, step=6)
    poly(p, [(x0 + 3, DECK_Y0 + 2.5), (x1 - 3, DECK_Y0 + 2.5), (x1 - 3, DECK_Y0 + 4.5), (x0 + 3, DECK_Y0 + 4.5)], W_L)
    poly(p, [(x0 + 3, DECK_Y1 - 4.5), (x1 - 3, DECK_Y1 - 4.5), (x1 - 3, DECK_Y1 - 2.2), (x0 + 3, DECK_Y1 - 2.2)], W_D)
    p.stroke(pts, INNER, j=.1, step=6)


def build(out=OUTD):
    p = Pen('materials_store', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((44, -30), (62, 6)), dot=(58, -16)); p.xf = (1.12, -19, -8)
    for cx in PX:
        p.tipshadow(cx, GROUND + 1.5, 22); p.foot_tip(cx, GROUND, 14)
    for cx in PX: pallet_feet(p, cx)
    for cx in PX:
        for i in range(NS - 1): sack(p, cx + OFFS[i], sack_y(i))
    with layer(p, 'bags'):
        for cx in PX: sack(p, cx + OFFS[NS - 1], sack_y(NS - 1))
    for cx in PX: deck(p, cx)
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
