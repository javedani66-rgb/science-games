#!/usr/bin/env python3
"""ایستگاه B02 «انبار مصالح» (سرزمین شهر، سکو #5b7390 رنگ‌مایهٔ ۲۱۳°). تصمیم مالک: دو پشتهٔ گونیِ برابر روی دو پالت هم‌سطح؛
بدون ترازو، بدون عدد/متن، بدون جرثقیل.

طرح قطعه‌به‌قطعه (واحد محلی؛ XF = مقیاس ۱٫۱۲) — دور دوم (پس از ردّ ناظر):
 ۱ سایهٔ تماس: یک بیضی زیر هر پالت.
 ۲ پایه‌های پالت: دو بلوک ۹×۸ (چوب میانه #a8672f) در دو سر، بینشان ۱۶ فاصله؛ خط دور PART ۵٫۸.
 ۳ دو گونی درشت در هر پشته (جمعاً ۴): بالشیِ مستطیلی ۳۲×۲۴ با گوشهٔ گرد (شعاع ۸)، بدون گوش نوک‌دار؛
   رنگ کرم #f3e1b0، تنها یک نوار دوخت تخت (#d9b979) و یک سایهٔ تیز راست داخل گونی؛ بدون برچسب و ریزه. خط دور PART ۵٫۸.
   جابه‌جایی افقی در دو پشته یکی است (۰، +۲) ⇒ دو پشتهٔ برابر و قرینهٔ خوانا.
 ۴ عرشهٔ پالت ۳۴×۱۰ (چوب #b77a3a، روشن #d9a463، تیره #7a4a1f)، خط دور PART ۵٫۸، روی لبهٔ پایین گونی‌ها.
 ۵ لایهٔ متحرک node_materials_store_bags = گونی بالاییِ هر دو پشته؛ حالت ایستا = روی پشته.
 رنگ‌مایه: کرم ≈۴۲°، چوب ≈۳۰°؛ سکو ۲۱۳°. تفاوت مجاور: گونی کرم (L≈۹۰) / چوب (L≈۵۵).
 موتیف جدا از M05 (تیرآهن): گونی گرد کرم، نه تیر فلزی."""
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

PX = (-25, 25)             # مرکز دو پشته
SW, SH, STEP, R = 40, 26, 24, 9   # گونی
NS = 2                     # گونی در هر پشته
Y0 = 8                     # کف گونی اول
OFFS = (0, 3)              # جابه‌جایی افقی؛ در دو پشته دقیقاً یکی است
DECK_W, DECK_Y0, DECK_Y1 = 42, 0, 16
GROUND = 16
DROP = 16
LW = PART                  # دور گونی و پالت ۵٫۸


def poly(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, '' if op == 1 else ' opacity="%s"' % op))


def sack_pts(cx, yb):
    """گونیِ بالشی: مستطیل با گوشهٔ گرد؛ بالا و پایین کمی برآمده."""
    t = yb - SH; w = SW / 2
    pts = []
    for (ox, oy, a0) in ((w - R, t + R, -90), (w - R, yb - R, 0), (-w + R, yb - R, 90), (-w + R, t + R, 180)):
        for k in range(6):
            a = math.radians(a0 + 15 * k)
            pts.append((cx + ox + R * math.cos(a), oy + R * math.sin(a)))
    return pts


def sack(p, cx, yb):
    top = yb - SH
    pts = sack_pts(cx, yb)
    p.shape(pts, S_B, LW, j=.05, step=6)
    poly(p, [(cx + 11, top + 12), (cx + 15, top + 12), (cx + 15, yb - 9), (cx + 11, yb - 9)], S_D)                  # سایهٔ تیز راست
    poly(p, [(cx - 15, top + 9), (cx + 4, top + 9), (cx + 4, top + 13), (cx - 15, top + 13)], S_D)                # نوار دوخت
    p.stroke(pts, LW, j=.05, step=6)


def sack_y(i): return Y0 - STEP * i


def pallet_feet(p, cx):
    for dx in (-18, 9):
        p.shape([(cx + dx, DECK_Y1 - 3.5), (cx + dx + 9, DECK_Y1 - 3.5), (cx + dx + 9, GROUND), (cx + dx, GROUND)], F_B, LW, j=.08, step=6, clip=False)


def deck(p, cx):
    x0, x1 = cx - DECK_W / 2, cx + DECK_W / 2
    pts = [(x0, DECK_Y0), (x1, DECK_Y0), (x1, DECK_Y1), (x0, DECK_Y1)]
    p.shape(pts, W_B, LW, j=.08, step=6)
    poly(p, [(x0 + 5, DECK_Y0 + 3), (x1 - 5, DECK_Y0 + 3), (x1 - 5, DECK_Y0 + 5), (x0 + 5, DECK_Y0 + 5)], W_L)
    for dx in (-12, 12): poly(p, [(cx + dx - 4, DECK_Y1 - 8), (cx + dx + 4, DECK_Y1 - 8), (cx + dx + 4, DECK_Y1 - 3.5), (cx + dx - 4, DECK_Y1 - 3.5)], W_D)   # دو جیب چنگک
    p.stroke(pts, LW, j=.08, step=6)


def build(out=OUTD):
    p = Pen('materials_store', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((44, -30), (62, 6)), dot=(58, -16)); p.xf = (0.93, -19, -4)
    for cx in PX:
        p.tipshadow(cx, GROUND + 1.5, 22); p.foot_tip(cx, GROUND, 12)
    for cx in PX:
        sack(p, cx + OFFS[0], sack_y(0))
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
