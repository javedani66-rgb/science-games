#!/usr/bin/env python3
"""ایستگاه «فانوس دریایی» (E04): قهرمان = برج راه‌راه با اتاقک چراغ، سکوی دریایی.
لایهٔ متحرک node_lighthouse_light = دو پرتو چپ و راست (چشمک: روشن/خاموش، بدون خروج از سکو).
برج و اتاقک چراغ ثابت و کامل زیر پرتو."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
HERE = pathlib.Path(__file__).resolve().parent
OUTD = HERE / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/kit2/after/lighthouse'
XF = (1.0, 0.0, 0.0)            # قاب قهرمان: (مقیاس هندسه، dx، dy) در واحد symbol؛ ضخامت خط ثابت می‌ماند
RED = '#ef6a4a'; WHITE = '#fffaf0'; GLASS = '#ffd84d'; GLASS_D = '#d9961c'; ROOF = '#ef6a4a'; BEAM = '#fff1a0'
YB, YT = 10, -56           # پای برج، بالای برج
WB, WT = 19, 12           # نیم‌پهنای پایین/بالا
LY = -77                  # ارتفاع مرکز چراغ


def hw(y): return WB + (WT - WB) * (y - YB) / (YT - YB)


def build(out=OUTD):
    p = Pen('lighthouse', 'sea'); pad(p, line=((-62, 14), (-44, 19)), tri=((-60, -8), (62, 12)), dot=(58, -15))
    p.xf = XF
    p.tipshadow(0, YB - 2, 26); p.foot_tip(0, YB - 2, 14)
    # پرتوها (لایهٔ متحرک): دو گوهٔ ساده پشت اتاقک؛ بیرون از سکو نمی‌زنند
    with layer(p, 'light'):
        for s in (-1, 1):
            p.raw('<polygon points="%s" fill="%s" opacity=".92"/>' % (' '.join('%.1f,%.1f' % q for q in p.X([(s * 9, LY - 2), (s * 54, LY - 12), (s * 54, LY + 12), (s * 9, LY + 2)])), BEAM))
    # برج
    body = [(-WB, YB), (WB, YB), (WT, YT), (-WT, YT)]
    p.shape(body, WHITE, OUT, j=.2, step=5)
    for y0, y1 in ((YB - 38, YB - 20), (YB - 74, YB - 56)):      # دو نوار قرمز (برش‌های ذوزنقه‌ای)
        pass
    for y0, y1 in ((-8, -26), (-30, -48)):
        pass
    for a, b in ((0, -16), (-24, -40)):                           # نوارهای قرمز، به‌اندازهٔ دیوارهٔ برج
        p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X([(-hw(a), a), (hw(a), a), (hw(b), b), (-hw(b), b)])), RED))
    p.stroke(body, OUT, j=.2, step=5)
        # بالکن
    p.shape([(-18, YT), (18, YT), (18, YT - 7), (-18, YT - 7)], GLASS_D, PART, j=.2, step=5)
    # اتاقک چراغ
    p.shape([(-9, YT - 7), (9, YT - 7), (9, LY - 9), (-9, LY - 9)], GLASS, PART, j=.2, step=5)
    p.ln((0, YT - 11), (0, LY - 6), INNER, GLASS_D, j=.1, probe='خط داخلی (قاب چراغ)')
    # سقف
    p.shape([(-13, LY - 9), (13, LY - 9), (0, LY - 26)], ROOF, PART, j=.2, step=5)
    return p


STAND = None     # خودکار: find_stand

if __name__ == '__main__':
    p = build()
    r = finish(p, 'lighthouse', STAND, motion={'light': dict(offsets=[(0, 0)])}, out=OUTD, shots=SHOTS)
    sp = r['spec']; sp['motion_spec'] = dict(kind='blink', note='پرتوها با opacity روشن/خاموش؛ بدنه و اتاقک ثابت')
    (OUTD / 'lighthouse.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps(r, ensure_ascii=False, indent=1))
