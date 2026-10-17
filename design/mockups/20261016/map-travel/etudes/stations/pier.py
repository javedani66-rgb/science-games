#!/usr/bin/env python3
"""ایستگاه «اسکله» (M07، D118): اسکلهٔ واقعی با قرقره روی سکوی دریایی.
اتود الف (انتخاب‌شده) = عرشهٔ چوبی (۳ تخته + ۲ شمع) + دکل و بازوی چوبی + قرقره + طناب + جعبه.
  لایه‌های متحرک: node_pier_load (جعبه+طناب، بالا/پایین ۰ تا ۸- در مختصات symbol) و node_pier_wheel (چرخش قرقره).
  بدنهٔ ثابت: شمع‌ها، عرشه، دکل، بازو، پایه‌ی قرقره. طناب پشت قرقره می‌رود (قرقره جلوی طناب).
اتود ب (VARIANT='b') = بولارد + طناب روی عرشه؛ سر طناب آویزان (لایهٔ node_pier_b_rope). فقط برای مقایسه."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/batch2/pier'

WOOD = '#ffd84d'; WOOD_D = '#d9961c'; PILE = '#e8892b'; WHEEL = '#ef6a4a'; BOX = '#a4e07a'; BOX_D = '#5fae44'

# ---- هندسهٔ مشترک عرشه ----
DX = 56                            # نیم‌پهنای عرشه
DBK, DT, DB = -26, -8, 2           # پشت رویه، لبهٔ جلوی رویه (= بالای وجه جلو)، کف
FL = -12                           # خط ایستادن اجسام روی رویهٔ عرشه
WOOD_F = '#f0b43a'                 # وجه جلوی عرشه
# ---- قرقره ----
CX, CY, R = -26, -70, 18
RO = 12                            # فاصلهٔ طناب از محور (درون دیسک؛ بالای طناب پشت قرقره پنهان می‌ماند)
BX = CX - RO                       # محور افقی طناب و جعبه
BW, BH = 20, 18                    # جعبه
UP = 8                             # بازهٔ حرکت جعبه (بالا)


def deck(p):
    for x in (-41, 41):            # شمع‌ها: زیر عرشه
        p.shape([(x - 5, DB - 1), (x + 5, DB - 1), (x + 5, DB + 7), (x - 5, DB + 7)], PILE, PART, j=.2, step=5)
    p.shape([(-DX, DBK), (DX, DBK), (DX, DB), (-DX, DB)], WOOD, OUT, j=.25, step=6)         # رویه: ۳ تخته
    h = (DT - DBK) / 3
    p.ln((-DX + 6, DBK + h), (DX - 6, DBK + h), INNER, WOOD_D, j=.1, probe='درز تخته (داخلی)')
    p.ln((-DX + 6, DBK + 2 * h), (DX - 6, DBK + 2 * h), INNER, WOOD_D, j=.1)
    p.fill([(-DX + 3, DT + 1), (DX - 3, DT + 1), (DX - 3, DB - 2), (-DX + 3, DB - 2)], WOOD_F)  # وجه جلو (کمی تیره‌تر)


def frame(p):
    """دکل راست + بازوی افقی + مهار مورب؛ قرقره مستقیم زیر بازو آویزان است."""
    p.ln((26, -56), (12, -87), PART, NAVY, j=.1, probe='مهار (جزء)')
    p.shape([(26, FL), (38, FL), (38, -100), (26, -100)], WOOD, OUT, j=.2, step=6)
    p.shape([(-40, -100), (40, -100), (40, -88), (-40, -88)], WOOD, OUT, j=.2, step=6)


def load(p):
    """جعبه + طناب. طناب از مرکز قرقره تا جعبه؛ بالای آن پشت دیسک قرقره پنهان است (در بازهٔ حرکت)."""
    top = FL - BH                  # جعبه روی عرشه (وضعیت پایین)
    p.ln((BX, CY), (BX, top), PART, NAVY, j=.1)
    p.shape([(BX - BW / 2, top), (BX + BW / 2, top), (BX + BW / 2, FL), (BX - BW / 2, FL)], BOX, PART, j=.2, step=5)
    p.ln((BX - BW / 2 + 4, top + BH / 2), (BX + BW / 2 - 4, top + BH / 2), INNER, BOX_D, j=.1, probe='نوار جعبه (داخلی)')


def wheel(p):
    p.shape(ell(CX, CY, R, R, 0, 360, 36), WHEEL, OUT, j=.3, step=99, clip=False)
    for k in range(3):
        t = math.radians(-90 + 120 * k)
        p.ln((CX + 4 * math.cos(t), CY + 4 * math.sin(t)), (CX + (R - 5) * math.cos(t), CY + (R - 5) * math.sin(t)), INNER, CREAM, j=.05,
             probe='پرهٔ قرقره (داخلی)' if k == 0 else None)
    p.shape(ell(CX, CY, 3.5, 3.5, 0, 360, 14), NAVY, INNER, j=0, step=99, clip=False)


def build_a(out=OUTD):
    p = Pen('pier', 'sea'); pad(p, line=((-62, 14), (-44, 19)), tri=((-60, -8), (62, 12)), dot=(58, -15))
    p.tipshadow(0, DB + 6, 46); p.foot_tip(-41, DB + 7, 8); p.foot_tip(41, DB + 7, 8)
    deck(p); frame(p)
    with layer(p, 'load'): load(p)
    with layer(p, 'wheel'): wheel(p)
    return p


# ---------------- اتود ب: بولارد + طناب ----------------


def build_b(out=None):
    p = Pen('pier_b', 'sea'); pad(p, line=((-62, 14), (-44, 19)), tri=((-60, -8), (62, 12)), dot=(58, -15))
    p.tipshadow(0, DB + 6, 46); p.foot_tip(-41, DB + 7, 8); p.foot_tip(41, DB + 7, 8)
    deck(p)
    # بولارد: تنه + سر پهن
    p.shape([(-9, FL), (9, FL), (7, -50), (-7, -50)], '#6f7fd6', OUT, j=.2, step=6)
    p.shape([(-17, -50), (17, -50), (17, -62), (-17, -62)], '#6f7fd6', OUT, j=.2, step=6)
    p.ln((-5, -26), (-4, -42), INNER, CREAM, j=.05, probe='خط داخلی (درخشش)')
    with layer(p, 'rope'):
        p.ln((-12, -56), (12, -56), PART, WOOD_D, j=.05)
        p.ln((30, FL - 2), (30, -36), PART, NAVY, j=.1, probe='طناب (جزء)')
        p.shape([(24, -36), (36, -36), (36, -24), (24, -24)], BOX, PART, j=.2, step=5)
    return p


def run(variant):
    if variant == 'a':
        p = build_a(); STAND = (0, 17)
        motion = {'load': dict(offsets=[(0, -UP * k / 4) for k in range(5)]), 'wheel': dict(rotate=(CX, CY))}
        out, shots, name = OUTD, SHOTS, 'pier'
    else:
        p = build_b(); STAND = (0, 17)
        motion = {'rope': dict(offsets=[(0, -UP * k / 4) for k in range(5)])}
        out, shots, name = pathlib.Path(SHOTS) / 'etude_b', SHOTS, 'pier_b'
    r = finish(p, name, STAND, motion=motion, out=out, shots=shots)
    sp = r['spec']
    if variant == 'a':
        sp['motion_spec'] = {
            'node_pier_load': dict(translate_y=[-UP, 0], unit='symbol', note='جعبه+طناب بالا/پایین؛ پایین = جعبه روی عرشه'),
            'node_pier_wheel': dict(rotate=[CX, CY], note='قرقره حول محور؛ جهت با حرکت جعبه هماهنگ: جعبه بالا = پادساعتگرد (طناب سمت چپ بالا می‌رود)'),
            'fixed': 'شمع‌ها، عرشه، دکل، بازو، پایهٔ قرقره'}
        (OUTD / 'pier.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    return r


if __name__ == '__main__':
    for v in (sys.argv[1:] or ['a', 'b']):
        r = run(v)
        print(v, json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'],
                             'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
