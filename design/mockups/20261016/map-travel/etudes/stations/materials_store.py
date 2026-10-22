#!/usr/bin/env python3
"""B02 «انبار مصالح» (سکوی city) — دور ۷، تصمیم تازهٔ مالک: آجر انبارشده + میلگرد (نه آجر).
طرح (واحد symbol، xf=1.3، کف y=15): سه جزء درشت، همه ¾ با سه پله (جلو/رویه/پهلو) و خط دور یکدست.
 ۱ پشتهٔ آجر قرمز-نارنجی (۴۶ پهن، ۴ ردیف×۱۱، عمق (14,-10))؛ ملات روشن چینش کله‌راهه (درزهای عمودی یک‌درمیان)؛ x -52..-6.
 ۲ دستهٔ میلگرد زرد-طلایی خوابیده (۴۴×۱۶) با سه میلهٔ روشن، کنار پشته؛ x 0..44. (تیر I نیست؛ آجر غالب است.)
 ۳ یک آجر شل روی پشته (لایهٔ متحرک node_materials_store_brick)؛ هنگام رسیدن از ۱۱ واحد بالاتر می‌نشیند؛ ایستا = روی پشته؛ بدون بیکار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent)); sys.path.insert(0, str(HERE))
from r6lib import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/materials_store'
BR_F, BR_T, BR_S = '#ef7a45', '#ffb98a', '#b4482a'
MORT = '#ffe3cc'
GO_F, GO_T, GO_S = '#ffe04a', '#fffbd0', '#e0a81c'
XF = (1.2, -3, -1)
G, DROP = 15, 11
D = (14, -10)


def brick_wall(p, x0, x1, rows, rh):
    top = G - rows * rh
    box3(p, x0, top, x1, G, D, BR_F, BR_T, BR_S, sw=PART, sw_in=0)
    for r in range(1, rows):
        y = top + r * rh; rect(p, x0 + 1.5, y - 1, x1 - 1.5, y + 1, MORT, .9)
    for r in range(rows):
        y = top + r * rh; off = 0 if r % 2 == 0 else (x1 - x0) / 4
        for xv in ((x0 + (x1 - x0) / 2 + off - (x1 - x0) / 4 * (1 if off else 0)),):
            pass
        xs = [x0 + (x1 - x0) * .5] if r % 2 == 0 else [x0 + (x1 - x0) * .25, x0 + (x1 - x0) * .75]
        for xv in xs: rect(p, xv - 1, y + 1, xv + 1, y + rh - 2.6, MORT, .9)
    return top


def rebar(p, x0, x1, h):
    y0 = G - h
    box3(p, x0, y0, x1, G, (12, -8), GO_F, GO_T, GO_S, sw=PART, sw_in=0)
    for k in range(3):
        y = y0 + 3.5 + k * 5.6; rect(p, x0 + 3, y, x1 - 3, y + 2.4, '#8aa0c8', .95)


def build():
    p = Pen('materials_store', 'city'); pad(p, line=((-80, 12), (-66, 20)), tri=((72, -22), (80, 8)), dot=(-74, -14)); p.xf = XF
    p.tipshadow(4, G + 1.5, 52); p.foot_tip(4, G, 40)
    top = brick_wall(p, -46, 0, 5, 11)
    rebar(p, 7, 47, 20)
    with layer(p, 'brick'):
        y0 = top - 11
        box3(p, -36, y0, -12, top, D, BR_F, BR_T, BR_S, sw=PART, sw_in=0)
    return p


STAND = None
if __name__ == '__main__':
    p = build()
    offs = [p.V((0, -DROP)), p.V((0, -DROP / 2)), (0, 0)]
    r = finish(p, 'materials_store', STAND, motion={'brick': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_materials_store_brick': dict(
        layer='آجر بالای پشته', dx=0, dy_from=-DROP, dy_to=0, dur_s=1.2,
        note='هنگام رسیدن: آجر از ۱۱ واحد بالاتر پایین می‌افتد و روی پشته می‌نشیند؛ حالت ایستا = روی پشته؛ بدون حلقهٔ بیکار.'),
        'reduced_motion': 'آجر روی پشته (ایستا)'}
    (OUTD / 'materials_store.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
