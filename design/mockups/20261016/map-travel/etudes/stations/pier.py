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
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/pier'
XF = (1.12, 0.0, 2.0)
DECK = '#e9a65b'; DECK_L = '#f6c98a'; DECK_D = '#b8682a'; PILE = '#c9772a'; PILE_L = '#e29a52'; WOOD_D = '#8a4a1c'
ROPE = '#f3dca0'; ROPE_D = '#b8892a'; CREAM = '#fff3c4'; FLAME = '#ffd84d'; LAMP = '#8c9ac8'
UP = 3
DT, DB, DL, DR = -26, -6, -72, 22               # عرشهٔ دراز (۷۲ واحد)
PB = 12                                        # کف پایه‌ها
UNDER = (-38, -12)                              # پایه‌های زیر عرشه
TALL = (-64, 14)                                # دو شمع بلندتر از عرشه
BOLL = (-44, -18)                               # بولاردها
LX, LY = -64, -54                               # فانوس روی شمع چپ


from r6lib import extrude, poly, rect, circ, box3        # حجم ¾ با سه پلهٔ رنگ؛ بین وجه‌ها خط نیست (قاعده ۱۴)
from g4_helpers import vcyl, arcline
D_DECK = (26, -15)                                   # عمق عرشه (پشت-راست)
DK_F, DK_T, DK_S = '#e9a65b', '#fbd9a0', '#b8682a'   # عرشه: جلو / رو / پهلو
PL_F, PL_T, PL_S = '#c9772a', '#e8a860', '#8a4a1c'   # شمع‌ها
HERO_W, HERO_T = 3.6, 2.8                            # خط دور قهرمان / قطعهٔ فرعی (قاعده ۲۴)
DECK_X0, DECK_X1, DECK_Y0, DECK_Y1 = -64, 44, -32, -8
POLE_X = -48


def piles(p):
    """سه شمع زیر عرشه، هم‌ضخامت (قاعده ۲۰)؛ اول کشیده می‌شوند تا عرشه روی آن‌ها بیاید."""
    for x in (-52, -20, 12, 40):
        p.tipshadow(x + 6, PB + 1, 14)
        extrude(p, [(x - 8, DECK_Y1 - 2), (x + 8, DECK_Y1 - 2), (x + 8, PB), (x - 8, PB)], (9, -6), PL_F, PL_T, PL_S, sw=HERO_T, sw_in=0)
        rect(p, x - 4, DECK_Y1 + 4, x - 1.8, PB - 4, '#f0b774', .9)          # نوار برق باریک


def deck(p):
    extrude(p, [(DECK_X0, DECK_Y0), (DECK_X1, DECK_Y0), (DECK_X1, DECK_Y1), (DECK_X0, DECK_Y1)], D_DECK, DK_F, DK_T, DK_S, mid=DK_F, sw=HERO_W, sw_in=0)
    rect(p, DECK_X0 + 3, DECK_Y0 + 3, DECK_X1 - 3, DECK_Y0 + 7.5, '#f6c98a')       # لبهٔ روشن جلو (پلهٔ رنگ)
    for x in range(DECK_X0 + 14, DECK_X1 - 4, 14):                                     # درز تخته‌های رو: خط ریز هم‌رنگ
        p.ln((x, DECK_Y0 - .5), (x + D_DECK[0] - 2, DECK_Y0 + D_DECK[1] + 1.5), 2.6, '#c98a45', j=0)


def bollard(p):
    bx, by = 34, DECK_Y0 - 5
    p.tipshadow(bx + 3, by + 3, 9)
    vcyl(p, bx, by - 22, by, 10, 4.2, '#8a4a1c', '#b8682a', '#5c2f10', '#c9772a', sw=HERO_T)
    arcline(p, ell(bx, by - 14, 10.4, 4.4, 8, 172, 12), '#f3dca0', 3.2)                # طناب دور بولارد
    arcline(p, ell(bx, by - 8, 10.4, 4.4, 8, 172, 12), '#f3dca0', 3.2)


def ring(p):
    cx, cy = -26, DECK_Y0 + 12
    p.shape(ell(cx, cy, 9.5, 9.5, 0, 360, 22), '#e2483a', HERO_T, j=0, step=99, clip=False)
    for dx, dy, w, h in ((6.6, 0, 3.2, 5), (-6.6, 0, 3.2, 5), (0, 6.6, 5, 3.2), (0, -6.6, 5, 3.2)):
        rect(p, cx + dx - w / 2, cy + dy - h / 2, cx + dx + w / 2, cy + dy + h / 2, '#ffffff')
    p.shape(ell(cx, cy, 4.2, 4.2, 0, 360, 16), DK_F, 2.6, j=0, step=99, clip=False)


def crate(p):
    box3(p, -6, -52, 12, -34, (8, -5), '#ffd84d', '#fff0a0', '#c9961a', sw=HERO_T, sw_in=0)
    rect(p, -6, -45, 12, -41, '#e8b52a')


def pole(p):
    x, base = POLE_X, DECK_Y0 - 3
    extrude(p, [(x + 7, -78), (x + 7, -97), (x + 21, -97)], (6, -4), PL_F, PL_T, PL_S, sw=HERO_T, sw_in=0)     # تکیه‌گاه مورب زیر بازو
    extrude(p, [(x - 7, -104), (x + 7, -104), (x + 6, base), (x - 6, base)], (6, -4), PL_F, PL_T, PL_S, sw=HERO_T, sw_in=0)
    extrude(p, [(x + 7, -104), (x + 40, -104), (x + 40, -97), (x + 7, -97)], (6, -4), PL_F, PL_T, PL_S, sw=HERO_T, sw_in=0)   # بازوی فانوس (یک شکل با ستون)


def lantern(p):
    cx, top = POLE_X + 33, -98
    gx, gy = p.X((cx, top + 22)); p.raw('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#ffe27a" opacity=".32"/>' % (gx, gy, 19 * p.xf[0], 19 * p.xf[0]))
    p.ln((cx, top + 1), (cx, top + 8), 2.2, NAVY, j=0)                                   # زنجیر
    p.shape([(cx - 11, top + 8), (cx + 11, top + 8), (cx + 11, top + 34), (cx - 11, top + 34)], LAMP, HERO_T, j=.05, step=99, clip=False)
    rect(p, cx - 7, top + 13, cx + 7, top + 29, FLAME)                                    # شعله
    rect(p, cx - 7, top + 13, cx - 3.5, top + 29, '#fff3c4')
    p.shape([(cx - 14, top + 8), (cx, top - 5), (cx + 14, top + 8)], WOOD_D, HERO_T, j=.05, step=99, clip=False)   # سقف


def build():
    p = Pen('pier', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.foot_tip(-20, PB, 40)
    piles(p); deck(p); ring(p); crate(p); bollard(p); pole(p)
    with layer(p, 'lantern'): lantern(p)
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
