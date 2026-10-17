#!/usr/bin/env python3
"""ایستگاه «اسکله» (M07): اسکلهٔ واقعی روی سکوی دریایی = عرشهٔ تخته‌ای کوتاه (نمای سه‌چهارم) روی سه پایهٔ چوبی،
یک بولارد (دکل بستن) با طناب حلقه‌شده، و یک جعبهٔ کوچک کنار آن. اولویت خوانایی اسکله است؛ قرقره (مفهوم علمی ایستگاه) در اتود بعدی.
  لایهٔ متحرک: node_pier_load = جعبه (بالا/پایین ۰ تا ۶- در مختصات symbol، مثل موج). بقیه ثابت."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit3/pier'
XF = (1.0, 0.0, 0.0)
PL = '#ffd84d'; PL_D = '#e0a22a'; PILE = '#c9772a'; BOX = '#a4e07a'; BOX_D = '#5fae44'; ROPE = '#f2e2b0'; BOL = '#ef6a4a'
UP = 6
DT, DB, DL, DR = -26, -6, -56, 8          # عرشه (نمای کنار): بالا، پایین، چپ، راست


def build():
    p = Pen('pier', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    p.tipshadow(-24, 12, 34); p.foot_tip(-44, 9, 8); p.foot_tip(-4, 9, 8)
    for x in (-44, -24, -4):                       # سه پایهٔ چوبی
        p.shape([(x - 6, DB - 2), (x + 6, DB - 2), (x + 6, 10), (x - 6, 10)], PILE, PART, j=.2, step=6)
    p.shape([(DL, DT), (DR, DT), (DR, DB), (DL, DB)], PL, OUT, j=.25, step=8)                          # عرشه
    p.ln((DL + 8, (DT + DB) / 2), (DR - 8, (DT + DB) / 2), INNER, PL_D, j=.05, probe='درز تخته (داخلی)')
    # بولارد: تنهٔ باریک‌شونده + کلاهک + طناب حلقه‌شده
    bx = -42
    p.shape([(bx - 9, DT), (bx + 9, DT), (bx + 6, DT - 24), (bx - 6, DT - 24)], BOL, PART, j=.2, step=6)
    p.shape([(bx - 12, DT - 24), (bx + 12, DT - 24), (bx + 12, DT - 33), (bx - 12, DT - 33)], BOL, PART, j=.2, step=6)
    p.ln((bx - 8, DT - 8), (bx + 8, DT - 8), PART, ROPE, j=.05)
    p.ln((bx - 7, DT - 17), (bx + 7, DT - 17), PART, ROPE, j=.05)
    with layer(p, 'load'):                         # جعبه
        cx = -10
        p.shape([(cx - 12, DT - 22), (cx + 12, DT - 22), (cx + 12, DT), (cx - 12, DT)], BOX, PART, j=.2, step=6)
        p.ln((cx - 12, DT - 11), (cx + 12, DT - 11), INNER, BOX_D, j=.05, probe='تختهٔ جعبه (داخلی)')
    return p


def run():
    p = build()
    motion = {'load': dict(offsets=[p.V((0, -UP * k / 3)) for k in range(4)])}
    r = finish(p, 'pier', None, motion=motion, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_pier_load': dict(translate_y=[-UP, 0], unit='symbol', note='جعبه آرام بالا/پایین (موج)'),
                         'fixed': 'پایه‌ها، عرشه، بولارد و طناب', 'note': 'قرقره در این نسخه نیست؛ بعدا روی بولارد'}
    (OUTD / 'pier.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    return r


if __name__ == '__main__':
    r = run()
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
