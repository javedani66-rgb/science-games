#!/usr/bin/env python3
"""ایستگاه «اسکله» (M07؛ ۱۹ اکتبر: عرشهٔ دراز + شمع + بولارد + فانوس، بدون قاب L/قرقره؛ لایهٔ متحرک node_pier_lantern). قدیمی: بازطراحی ۱۸ اکتبر شب، D123): اسکلهٔ چوبی درشت روی سکوی دریایی: عرشهٔ تخته‌ای با لبهٔ روشن و درزها روی چهار پایهٔ چوبی
با کلاهک، بولارد با طناب حلقه، دکل L‌شکل با تکیه‌گاه مورب، قرقرهٔ بزرگ زیر سر بازو (از بالای فیگور رد می‌شود؛ آزاد از بالا) و جعبهٔ آویزان.
پایه‌های عرشه سمت چپ می‌مانند. لایه‌های متحرک: node_pier_load = طناب + جعبه (بالا/پایین ۰ تا ۶-)، node_pier_pulley = قرقره (می‌چرخد). بقیه ثابت."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import station_kit
from station_kit import *
from functools import partial
station_kit.margin_check = partial(station_kit.margin_check, min_margin=4)   # D123: حاشیهٔ چپ/راست ≥۴px
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/v2/pier'
XF = (1.0, 0.0, 0.0)
DECK = '#e9a65b'; DECK_L = '#f6c98a'; DECK_D = '#b8682a'; PILE = '#c9772a'; PILE_L = '#e29a52'; WOOD_D = '#8a4a1c'
ROPE = '#f3dca0'; ROPE_D = '#b8892a'; CREAM = '#fff3c4'; FLAME = '#ffd84d'; LAMP = '#8c9ac8'
UP = 3
DT, DB, DL, DR = -26, -6, -72, 22               # عرشهٔ دراز (۷۲ واحد)
PB = 12                                        # کف پایه‌ها
UNDER = (-38, -12)                              # پایه‌های زیر عرشه
TALL = (-64, 14)                                # دو شمع بلندتر از عرشه
BOLL = (-44, -18)                               # بولاردها
LX, LY = -64, -54                               # فانوس روی شمع چپ


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def pile(p, x, top, w=8):
    p.shape([(x - w, top), (x + w, top), (x + w, PB), (x - w, PB)], PILE, PART, j=.2, step=6)
    rect(p, x - w + 3, top + 4, x - w + 6, PB - 4, PILE_L)


def build():
    p = Pen('pier', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    for x in UNDER + TALL: p.tipshadow(x, PB + 1, 11)
    p.foot_tip(TALL[0], PB, 7); p.foot_tip(TALL[1], PB, 7)
    for x in UNDER: pile(p, x, DB - 2, 7)                                               # پایهٔ میانی زیر عرشه
    for x in TALL: pile(p, x, DT - 18, 7)                                               # شمع‌های بلند پشت عرشه
    # عرشه: روی تخته‌های عرضی روشن + تیر زیرین با ردیف میخ
    p.shape([(DL, DT), (DR, DT), (DR, DB), (DL, DB)], DECK, OUT, j=.25, step=8)
    rect(p, DL + 6, DT + 5, DR - 6, DT + 11, DECK_L)
    for x in range(DL + 15, DR - 6, 14): p.ln((x, DT + 5), (x, DT + 11), INNER, DECK_D, j=0)     # درز تخته‌های عرضی
    for x in range(DL + 15, DR - 6, 14): disc(p, x, DB - 6, 2.4, CREAM)                          # ردیف میخ
    # بولاردها با طناب پیچیده
    p.ln((BOLL[0] + 6, DT - 5), (BOLL[1] - 6, DT - 5), INNER, ROPE, j=0)
    for x in BOLL:
        p.shape([(x - 7, DT - 16), (x + 7, DT - 16), (x + 7, DT + 2), (x - 7, DT + 2)], WOOD_D, PART, j=.1, step=6, clip=False)
        rect(p, x - 6, DT - 12, x + 6, DT - 9, ROPE); rect(p, x - 6, DT - 6, x + 6, DT - 3, ROPE)
    with layer(p, 'lantern'):                                                             # فانوس روی شمع چپ
        p.shape([(LX - 7, LY), (LX + 7, LY), (LX + 7, LY + 16), (LX - 7, LY + 16)], LAMP, PART, j=.1, step=99, clip=False)
        rect(p, LX - 3, LY + 4, LX + 3, LY + 12, FLAME)
        p.shape([(LX - 9, LY), (LX, LY - 9), (LX + 9, LY)], WOOD_D, INNER, j=0, step=99, clip=False)
    return p


def run():
    p = build()
    motion = {'lantern': dict(offsets=[p.V((0, -UP * k / 3)) for k in range(4)])}
    r = finish(p, 'pier', None, motion=motion, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_pier_lantern': dict(translate_y=[0, -UP], unit='symbol', note='فانوس کمی بالا/پایین (تکان نرم)'),
                         'fixed': 'عرشه، پایه‌ها، شمع‌ها، بولاردها و طناب'}
    (OUTD / 'pier.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    return r


if __name__ == '__main__':
    r = run()
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
