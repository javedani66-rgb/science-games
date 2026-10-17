#!/usr/bin/env python3
"""ایستگاه «بارانداز» (M02): قهرمان = چرخ و محور (چرخ پره‌دار روی پایهٔ ثابت)، سکوی دریایی.
لایهٔ متحرک node_wheel_dock_wheel = چرخ (چرخش حول محور). پایه (پشت) و سرِ محور (جلو) ثابت‌اند.
VARIANT='gear' اتود الف (چرخ‌دندهٔ تنها، طرح قبلی)؛ 'wheel' اتود ب (انتخاب‌شده)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent

XF = (1.0, 0.0, 0.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
Y_T = '#ffd84d'; Y_L = '#f2b92c'; Y_H = '#8a5f0c'
POST_L = '#8fb5f2'; POST_R = '#8f8bd6'
CX, CY, R = -8, -48, 42
FOOT = 26                          # y تماس پایه با سکو


def post(p):
    """پایهٔ ثابت: ستون راست و پیوسته از سکو تا محور (پشت چرخ)، دو رنگ مثل دیوارهٔ سکو."""
    w = 12
    L = [(CX - w, CY), (CX - w, FOOT - 6)]; Rr = [(CX + w, FOOT - 6), (CX + w, CY)]
    base = ell(CX, FOOT - 6, w, 4, 0, 180, 10)
    p.shape([(CX - w, CY)] + [(x, y) for x, y in base[::-1]] + [(CX + w, CY)], POST_L, OUT, j=.3, step=99)
    p.fill([(CX + 1, CY), (CX + w, CY)] + [(x, y) for x, y in base if x >= CX + 1][::-1], POST_R)
    # پایهٔ پهن زیر ستون
    p.shape(ell(CX, FOOT - 6, w + 14, 6, 0, 360, 24), POST_R, PART, j=.3, clip=False)


def wheel(p):
    """چرخ: رینگ، دیسک، شش پره (خط راست)، توپی. هر زاویهٔ چرخش ایمن است (دایره)."""
    p.shape(ell(CX, CY, R, R, 0, 360, 48), Y_T, OUT, j=.4, step=99)
    p.shape(ell(CX, CY, R * .70, R * .70, 0, 360, 36), Y_L, INNER, j=.3, step=99, clip=False)
    for k in range(6):
        t = math.radians(30 + 60 * k)
        p.ln((CX + 12 * math.cos(t), CY + 12 * math.sin(t)), (CX + R * .70 * math.cos(t), CY + R * .70 * math.sin(t)),
             PART, Y_H, j=.1, probe='پرهٔ چرخ (جزء)' if k == 0 else None)
    p.shape(ell(CX, CY, 13, 13, 0, 360, 24), Y_T, INNER, j=.3, clip=False)


def cap(p):
    """سرِ محور: ثابت، جلوی چرخ."""
    p.shape(ell(CX, CY, 7, 7, 0, 360, 16), Y_H, INNER, j=.2, clip=False)
    p.ln((CX - 22, CY - 24), (CX - 30, CY - 12), INNER, CREAM, j=.1, probe='خط داخلی (درخشش)') if False else None


def build(out=None, legacy_shadow=False):
    p = Pen('wheel_dock', 'sea'); pad(p, line=((-60, 13), (-42, 18)), tri=((-58, -8), (61, 12)), dot=(56, -14))
    p.xf = XF
    p.tipshadow(CX, FOOT - 6, 24); p.foot_tip(CX, FOOT - 6, 14)
    post(p)
    with layer(p, 'wheel'): wheel(p)
    cap(p)
    p.ln((CX - 24, CY - 22), (CX - 14, CY - 32), INNER, CREAM, j=.1, probe='خط داخلی (درخشش)') if False else None
    return p, symbol(p, 'wheel_dock', ['wheel'], out=out, legacy_shadow=legacy_shadow), p.X((CX, CY))


STAND = None     # خودکار: find_stand
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/wheel_dock'

if __name__ == '__main__':
    p, sym, c = build()
    r = finish(p, 'wheel_dock', STAND, motion={'wheel': dict(rotate=c)}, out=OUTD, shots=SHOTS)
    print(json.dumps({k: r[k] for k in ('ok',)} | {'margin': r['margin'], 'motion': r['motion'], 'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
