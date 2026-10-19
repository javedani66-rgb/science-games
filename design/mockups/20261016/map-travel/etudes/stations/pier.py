#!/usr/bin/env python3
"""ایستگاه «اسکله» (M07؛ بازطراحی ۱۸ اکتبر شب، D123): اسکلهٔ چوبی درشت روی سکوی دریایی: عرشهٔ تخته‌ای با لبهٔ روشن و درزها روی چهار پایهٔ چوبی
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
XF = (1.13, -2.6, -1.8)
DECK = '#e9a65b'; DECK_L = '#f6c98a'; DECK_D = '#b8682a'; PILE = '#c9772a'; PILE_L = '#e29a52'; WOOD_D = '#8a4a1c'; MAST = '#d98f45'; MAST_L = '#f0b878'
BOX = '#ffd84d'; BOX_D = '#c9892a'; ROPE = '#7a4a1c'; IRON = '#c9d3ea'; IRON_D = '#8c9ac8'; CREAM = '#fff3c4'
UP = 6
DT, DB, DL, DR = -34, -14, -62, 6              # عرشه
PB = 10                                       # کف پایه‌ها
PILES = (-50, -26, 0)
MXL, MXR, JT, JB, JR = -58, -46, -120, -108, 20    # دکل و بازو
PX, PY, PR = 4, -96, 11                      # قرقره
RX = PX - PR + 1                              # محور طناب (لبهٔ چپ قرقره)


def flat(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): flat(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def build():
    p = Pen('pier', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    for x in PILES: p.tipshadow(x, PB + 1, 11)
    p.foot_tip(-50, PB, 7); p.foot_tip(0, PB, 7)
    for x in PILES:                                                                       # چهار پایه با کلاهک
        p.shape([(x - 5, DB - 2), (x + 5, DB - 2), (x + 5, PB), (x - 5, PB)], PILE, PART, j=.2, step=6)
        rect(p, x - 2.5, DB + 4, x - .5, PB - 3, PILE_L)
        rect(p, x - 9, PB - 2, x + 9, PB + 3, WOOD_D)
    # دکل L‌شکل (بازو بالای فیگور)
    p.shape([(MXL, DT), (MXL, JT), (JR, JT), (JR, JB), (MXR, JB), (MXR, DT)], MAST, PART, j=.2, step=6)
    rect(p, MXL + 3, JT + 3, JR - 3, JT + 5.5, MAST_L); rect(p, MXL + 3, JT + 3, MXL + 5.5, DT - 4, MAST_L)
    p.ln((-46, -70), (-20, -106), PART + 2 * INNER, NAVY, j=.05); p.ln((-46, -70), (-20, -106), PART, MAST, j=.05)          # تکیه‌گاه مورب
    # عرشه
    p.shape([(DL, DT), (DR, DT), (DR, DB), (DL, DB)], DECK, OUT, j=.25, step=8)
    rect(p, DL + 5, DT + 4, DR - 5, DT + 7, DECK_L)                                       # نور لبهٔ عرشه
    for x in (-42, -22, -2): p.ln((x, DT + 10), (x, DB - 4), INNER, DECK_D, j=0)             # درز تخته‌ها (عمودی)
    p.ln((DL + 6, DT + 13), (DR - 8, DT + 13), INNER, DECK_D, j=0, probe='درز تخته (داخلی)')
    # بولارد با طناب حلقه
    p.shape([(-34, DT - 12), (-22, DT - 12), (-22, DT + 2), (-34, DT + 2)], WOOD_D, PART, j=.1, step=6, clip=False)
    rect(p, -31, DT - 9, -25, DT - 6, CREAM); rect(p, -31, DT - 3, -25, DT, CREAM)
    with layer(p, 'load'):                                                                # طناب + جعبه
        p.ln((RX, PY), (RX, -60), PART, ROPE, j=0); p.probes.append(('طناب (جزء)', PART, p.X((RX, -75)), (1, 0), ROPE))
        p.shape([(PX - 17, -60), (PX + 5, -60), (PX + 5, -42), (PX - 17, -42)], BOX, PART, j=.2, step=6, clip=False)
        rect(p, PX - 14, -57, PX + 2, -55, '#fff3b0')
        p.ln((PX - 12, -49), (PX, -49), INNER, BOX_D, j=0, probe='تختهٔ جعبه (داخلی)')
    with layer(p, 'pulley'):                                                              # قرقرهٔ درشت
        p.shape(ell(PX, PY, PR, PR, 0, 360, 28), IRON, PART, j=.1, step=99, clip=False)
        for a in range(3):
            c, sn = math.cos(math.radians(a * 120 + 30)), math.sin(math.radians(a * 120 + 30))
            p.ln((PX, PY), (PX + (PR - 4) * c, PY + (PR - 4) * sn), INNER, WOOD_D, j=0)
        p.raw('<circle cx="%s" cy="%s" r="3.6" fill="%s" class="eo" stroke-width="3"/>' % (*p.X((PX, PY)), WOOD_D))
    return p


def run():
    p = build()
    motion = {'load': dict(offsets=[p.V((0, -UP * k / 3)) for k in range(4)]), 'pulley': dict(rotate=p.X((PX, PY)))}
    r = finish(p, 'pier', None, motion=motion, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_pier_pulley': dict(rotate_deg=[0, 360], center=[round(v, 1) for v in p.X((PX, PY))], unit='symbol', note='قرقره می‌چرخد'),
                         'node_pier_load': dict(translate_y=[0, -UP], unit='symbol', note='جعبه با طناب بالا/پایین'),
                         'fixed': 'پایه‌ها، عرشه، بولارد، دکل، بازو و تکیه‌گاه'}
    (OUTD / 'pier.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    return r


if __name__ == '__main__':
    r = run()
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'inside': r['inside'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
