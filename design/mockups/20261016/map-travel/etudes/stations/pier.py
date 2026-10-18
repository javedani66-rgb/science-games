#!/usr/bin/env python3
"""ایستگاه «اسکله» (M07، بازطراحی با قرقره): اسکلهٔ واقعی روی سکوی دریایی = عرشهٔ تخته‌ای کوتاه (نمای سه‌چهارم) روی سه پایهٔ چوبی،
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
DECK='#e9a65b'; DECK_D='#b8682a'; PILE='#c9772a'; WOOD_D='#8a4a1c'; MAST='#d98f45'; WATER='#6fc3f0'; WATER_L='#d6f0ff'
BOX='#ffd84d'; BOX_D='#c9892a'; ROPE='#7a4a1c'; IRON='#c9d3ea'
UP = 6
DT, DB, DL, DR = -32, -10, -58, 10          # عرشه: بالا، پایین، چپ، راست
MX, MW = 4, 6                              # دکل: محور، نیم‌پهنا
JT, JB, JL = -104, -93, -46                 # تیر افقی: بالا، پایین، چپ
PX, PY, PR = -35, -84, 12                  # قرقره
PB = 10                                    # کف پایه‌ها روی سکو


def build():
    p = Pen('pier', 'sea'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16)); p.xf = XF
    for x in (-51, -24, 3):                        # سه پایه روی رویهٔ سکو، با کف کوچک و سایهٔ تماس
        p.tipshadow(x, PB + 1, 11)
    p.foot_tip(-44, PB, 8); p.foot_tip(-6, PB, 8)
    for x in (-51, -24, 3):
        p.shape([(x - 7, DB - 2), (x + 7, DB - 2), (x + 7, PB), (x - 7, PB)], PILE, PART, j=.2, step=6)
        p.ln((x, DB + 3), (x, PB - 4), INNER, WOOD_D, j=.05)                    # رگهٔ چوب
        p.shape([(x - 8, PB - 3), (x + 8, PB - 3), (x + 8, PB + 2), (x - 8, PB + 2)], WOOD_D, PART, j=.1, step=99, clip=False)   # کف کوچک
    p.shape([(DL, DT), (DR, DT), (DR, DB), (DL, DB)], DECK, OUT, j=.25, step=8)             # عرشه
    p.ln((DL + 8, (DT + DB) / 2), (DR - 14, (DT + DB) / 2), INNER, DECK_D, j=.05, probe='درز تخته (داخلی)')
    # دکل + تیر افقی (یک تکهٔ L)
    p.shape([(MX - MW, DT), (MX - MW, JB), (JL, JB), (JL, JT), (MX + MW, JT), (MX + MW, DT)], MAST, PART, j=.2, step=6)
    p.ln((MX, DT - 4), (MX, JB + 8), INNER, WOOD_D, j=.05)
    with layer(p, 'load'):                         # طناب + جعبه
        p.ln((PX, PY), (PX, -54), PART, ROPE, j=0); p.probes.append(('طناب (جزء)', PART, (PX, -64), (1, 0), ROPE))
        p.shape([(PX - 12, -56), (PX + 12, -56), (PX + 12, -40), (PX - 12, -40)], BOX, PART, j=.2, step=6, clip=False)
        p.ln((PX - 8, -48), (PX + 8, -48), INNER, BOX_D, j=.05, probe='تختهٔ جعبه (داخلی)')
    with layer(p, 'pulley'):                       # قرقرهٔ درشت
        p.shape(ell(PX, PY, PR, PR, 0, 360, 24), IRON, PART, j=.1, step=99, clip=False)
        for a in range(3):
            c, sn = math.cos(math.radians(a * 120 + 30)), math.sin(math.radians(a * 120 + 30))
            p.ln((PX, PY), (PX + (PR - 3) * c, PY + (PR - 3) * sn), INNER, WOOD_D, j=0)
        p.raw('<circle cx="%s" cy="%s" r="3.6" fill="%s" class="eo" stroke-width="3"/>' % (PX, PY, WOOD_D))
    return p


def run():
    p = build()
    motion = {'load': dict(offsets=[p.V((0, -UP * k / 3)) for k in range(4)]), 'pulley': dict(rotate=(PX, PY))}
    r = finish(p, 'pier', None, motion=motion, out=OUTD, shots=SHOTS)
    sp = r['spec']
    sp['motion_spec'] = {'node_pier_pulley': dict(rotate_deg=[0, 360], center=[PX, PY], unit='symbol', note='قرقره می‌چرخد'),
                         'node_pier_load': dict(translate_y=[0, -UP], unit='symbol', note='جعبه با طناب بالا/پایین؛ سر طناب پشت قرقره است'),
                         'fixed': 'پایه‌ها، عرشه، دکل، تیر و آویز'}
    (OUTD / 'pier.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    return r


if __name__ == '__main__':
    r = run()
    print(json.dumps({'ok': r['ok'], 'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
