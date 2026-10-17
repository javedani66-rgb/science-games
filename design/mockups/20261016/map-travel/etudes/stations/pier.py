#!/usr/bin/env python3
"""ایستگاه «اسکله» (M07، D118): اسکلهٔ واقعی با قرقره روی سکوی دریایی (اتود الف).
طراحی دوباره برای خط ضخیم‌تر (D113، D110): عرشهٔ یک‌تکه + یک درز، یک دکل پهن با بازوی افقی، قرقره، طناب و جعبه؛ بدون مهار مورب.
  لایه‌های متحرک: node_pier_load (جعبه+طناب، بالا/پایین ۰ تا ۸- در مختصات symbol) و node_pier_wheel (چرخش قرقره).
  بدنهٔ ثابت: شمع‌ها، عرشه، دکل، بازو. طناب پشت قرقره می‌رود (قرقره جلوی طناب).
اتود ب (بولارد) این‌جا حذف شد؛ آرگومان 'a' برای سازگاری با خط فرمان قبول می‌شود."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/pier'

XF = (1.0, 0.0, 0.0)             # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
WOOD = '#ffd84d'; WOOD_D = '#d9961c'; PILE = '#e8892b'; WHEEL = '#ef6a4a'; BOX = '#a4e07a'; BOX_D = '#5fae44'
DX0, DX1 = -56, 2                  # عرشه از چپ تا راست
DT, DB = -20, 0                    # بالا و پایین عرشه
CX, CY, R = -40, -70, 16           # قرقره
BX = CX                            # محور طناب و جعبه
BW, BH = 20, 18                    # جعبه
UP = 8                             # بازهٔ حرکت جعبه (بالا)
MX0, MX1 = -18, 2                  # دکل


def deck(p):
    for x in (-44, -12):           # شمع‌ها زیر عرشه
        p.shape([(x - 7, DB - 1), (x + 7, DB - 1), (x + 7, DB + 9), (x - 7, DB + 9)], PILE, PART, j=.2, step=5)
    p.shape([(DX0, DT), (DX1, DT), (DX1, DB), (DX0, DB)], WOOD, OUT, j=.25, step=6)
    p.ln((DX0 + 8, (DT + DB) / 2), (DX1 - 8, (DT + DB) / 2), INNER, WOOD_D, j=.1, probe='درز تخته (داخلی)')


def frame(p):
    """دکل راست + بازوی افقی؛ قرقره مستقیم زیر بازو آویزان است."""
    p.shape([(MX0, DT), (MX1, DT), (MX1, -108), (MX0, -108)], WOOD, OUT, j=.2, step=6)
    p.shape([(DX0, -108), (MX1, -108), (MX1, -88), (DX0, -88)], WOOD, OUT, j=.2, step=6)


def load(p):
    """جعبه + طناب. طناب از مرکز قرقره تا جعبه؛ بالای آن پشت دیسک قرقره پنهان است (در بازهٔ حرکت)."""
    top = DT - BH                  # جعبه روی عرشه (وضعیت پایین)
    p.ln((BX, CY), (BX, top), PART, NAVY, j=.1)
    p.probes.append(('طناب (جزء)', PART, p.X((BX, (CY + R + top) / 2)), (1, 0), NAVY))
    p.shape([(BX - BW / 2, top), (BX + BW / 2, top), (BX + BW / 2, DT), (BX - BW / 2, DT)], BOX, PART, j=.2, step=5)


def wheel(p):
    p.shape(ell(CX, CY, R, R, 0, 360, 30), WHEEL, OUT, j=.3, step=99, clip=False)
    for k in range(3):
        t = math.radians(-90 + 120 * k)
        p.ln((CX + 4 * math.cos(t), CY + 4 * math.sin(t)), (CX + (R - 5) * math.cos(t), CY + (R - 5) * math.sin(t)), INNER, CREAM, j=.05,
             probe='پرهٔ قرقره (داخلی)' if k == 0 else None)
    mx, my = p.X((CX, CY)); p.raw('<circle cx="%s" cy="%s" r="3.2" fill="%s"/>' % (mx, my, NAVY))


def build_a(out=OUTD):
    p = Pen('pier', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.tipshadow((DX0 + DX1) / 2, DB + 8, 36); p.foot_tip(-44, DB + 9, 8); p.foot_tip(-12, DB + 9, 8)
    deck(p); frame(p)
    with layer(p, 'load'): load(p)
    with layer(p, 'wheel'): wheel(p)
    return p


def run(variant='a'):
    p = build_a(); STAND = None
    motion = {'load': dict(offsets=[p.V((0, -UP * k / 4)) for k in range(5)]), 'wheel': dict(rotate=p.X((CX, CY)))}
    r = finish(p, 'pier', STAND, motion=motion, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {
        'node_pier_load': dict(translate_y=[-UP * p.xf[0], 0], unit='symbol', note='جعبه+طناب بالا/پایین؛ پایین = جعبه روی عرشه'),
        'node_pier_wheel': dict(rotate=list(p.X((CX, CY))), note='قرقره حول محور؛ جهت با حرکت جعبه هماهنگ: جعبه بالا = پادساعتگرد (طناب سمت چپ بالا می‌رود)'),
        'fixed': 'شمع‌ها، عرشه، دکل، بازو'}
    (OUTD / 'pier.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    return r


if __name__ == '__main__':
    r = run('a')
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'],
                      'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
