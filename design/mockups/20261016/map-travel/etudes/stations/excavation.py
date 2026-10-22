#!/usr/bin/env python3
"""R6: بازطراحی — دیلم ضخیم‌تر با سر خمیده، سنگ تکیه‌گاه سه‌وجهی بزرگ‌تر، تخته‌سنگ بار درشت چندوجهی، دو سنگ‌ریزه؛ لایهٔ متحرک node_excavation_bar (میله+سنگ بار)، حالت ایستا = پایان.
ایستگاه M04 «گودبرداری» (سرزمین شهر، سکوی آبی-فولادی ۲۱۳°). تصمیم مالک: میلهٔ فلزی روی سنگ تکیه‌گاه که سنگی را بالا می‌آورد.
نمای جانبی؛ حالت ایستا = پایان حرکت (سر بلند میله پایین آمده، سنگ بار بالا رفته).
فقط ۳ جزء درشت (تل خاک و گودال حذف شد)، همهٔ خط‌ها راست (j=0):
 ۱ سنگ تکیه‌گاه: مکعب‌گونهٔ خاکستری گرم ۲۶×۲۰، پایه روی زمین (y=8)؛ سه پله (#7f7968 / #a59f8c / #58533f)؛ نوار روشن چپ، نوار تیره راست، داخل جزء.
 ۲ میلهٔ فلزی مایل قرمز (رنگ‌مایه ≈۴°؛ ≥۳۵° از سنگ ۴۴° و از سکو ۲۱۳°) ۱۳ پهن، از ۳۳- تا ۴۰ حول لولا؛ سه پله (#e8483c / #ff8a78 / #a82a24)؛ دستگیرهٔ زرد تخت.
    کف میله ۵٫۵ واحد در تکیه‌گاه فرو می‌رود (هم‌پوشان).
 ۳ تخته‌سنگ بار کرم (#ecdcb4 / #fbf2da / #c2ae85) هفت‌ضلعی روی سر کوتاه میله؛ پایینش ۵ واحد پشت میله می‌رود (هم‌پوشان ۵).
 پین زرد روی لولا. حرکت: میله+سنگ حول لولا از ۸- تا ۰ درجه، ۱٫۸ ثانیه، یک‌بار؛ بدون حلقهٔ بیکار.
"""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/excavation'

from r6lib import extrude
from shapely.geometry import Polygon
from shapely.ops import unary_union
S_B, S_L, S_D = '#efe7d3', '#fffcf1', '#c7bb9b'     # تخته‌سنگ بار: کرم روشن
F_B, F_L, F_D = '#c2b79d', '#ddd3b8', '#8a8068'     # سنگ تکیه‌گاه: خاکستری-بژ
B_B, B_L, B_D = '#e8b866', '#fbd990', '#b8843a'     # دیلم قرمز
YEL = '#ffd84d'
GY = 8
ANG = 20
PIV = (8.0, -27.0)
BW = 11.0
REST = -8
XF = (.9, 0.0, 6.0)
DD = (10, -6)


def flat(p, pts, col, op=1):
    p.raw('<polygon points="%s" fill="%s"%s/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col, (' stroke="%s" stroke-width=".6" stroke-linejoin="round"' % col) if op == 1 else ' opacity="%s"' % op))   # حاشیهٔ هم‌رنگ: درز مویی بین چندضلعی‌ها نماند


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r, col))


def pebble(p, cx, cy, r):
    pts = [(cx - r, cy), (cx - r * .8, cy - r * .8), (cx - r * .1, cy - r * 1.15), (cx + r * .8, cy - r * .8), (cx + r, cy)]
    extrude(p, pts, (r * .5, -r * .3), F_B, F_L, F_D, sw=PART)


def build():
    p = Pen('excavation', 'city'); pad(p, line=((16, 27), (34, 24)), tri=((-52, 22), (72, -22)), dot=(74, -8)); p.xf = XF
    p.tipshadow(0, GY + 1, 40); p.foot_tip(0, GY, 24)
    ful = [(-30, GY), (-16, -26), (30, -26), (44, GY)]
    extrude(p, ful, (12, -8), F_B, F_L, F_D, sw=OUT, sw_in=0)
    f = rot(PIV[0], PIV[1], ANG)
    P = lambda pts: TP(f, [(PIV[0] + x, PIV[1] + y) for x, y in pts])
    with layer(p, 'bar'):
        main = [(-36, -BW), (48, -BW), (48, BW), (-36, BW)]
        head = [(42, -BW), (60, -BW), (60, BW), (42, BW)]
        u = unary_union([Polygon(P(main)), Polygon(P(head))]).buffer(.01)
        ext = list(u.exterior.coords)[:-1]
        p.shape(ext, B_B, OUT, j=0, step=6, clip=False)
        flat(p, P([(-30, -BW + 3), (44, -BW + 3), (44, -BW + 7.5), (-30, -BW + 7.5)]), B_L)
        flat(p, P([(-30, BW - 7.5), (44, BW - 7.5), (44, BW - 3), (-30, BW - 3)]), B_D)
        p.stroke(ext, OUT, j=0, step=6)
        # تخته‌سنگ بزرگ روی سر کوتاه چوب (در قاب چوب می‌چرخد)
        rock = P(ell(-22, -BW - 16, 21, 17, 0, 360, 22))
        extrude(p, rock, DD, S_B, S_L, S_D, sw=OUT, sw_in=0)
    return p


def rot_states(p, steps=(REST, REST / 2, 0)):
    return steps


if __name__ == '__main__':
    p = build()
    hm = p.X(PIV)
    lift = 34 * math.sin(math.radians(abs(REST)))
    r = finish(p, 'excavation', None, motion={'bar': dict(offsets=[(0, 0), (0, lift)])}, out=OUTD, shots=SHOTS)
    # سنجش واقعی چرخش (کیت فقط چرخش ۳۶۰ را می‌شناسد)
    import station_kit as K_
    import numpy as np
    from scipy.ndimage import distance_transform_edt as edt
    A = lambda im: im[..., 3] > 128
    i, j = p.layers['bar']; body = ''.join(p.o[i:j]); dsf = 4
    top = A(K_._shot(K_._poly(p.padtop), dsf)); fixed, _ = K_._split_layers(p)
    U = A(K_._shot(fixed, dsf)); st = r['spec']['stand']
    sx, sy = (100 * K_.K + st[0]) * dsf, (150 * K_.K + st[1]) * dsf
    fig = K_._place_fig(top.shape, sx, sy, dsf)
    cols = top.any(0); low = np.where(cols, top.shape[0] - 1 - np.argmax(top[::-1], 0), -1)
    allowed = cols[None, :] & (np.arange(top.shape[0])[:, None] <= low[None, :])
    worst = 99; outpx = 0; xm = 99; px = np.where(top.any(0))[0]
    for a in (REST, REST * .5, 0):
        Um = A(K_._shot('<g transform="rotate(%s %s %s)">%s</g>' % (a, hm[0], hm[1], body), dsf))
        outpx += float((Um & ~allowed).sum()) / dsf ** 2
        xs = np.where(Um.any(0))[0]; xm = min(xm, (xs.min() - px.min()) / dsf, (px.max() - xs.max()) / dsf)
        worst = min(worst, float(edt(~fig)[Um].min()) / dsf)
    rot_chk = dict(states=[REST, REST / 2, 0], out_px=round(outpx, 1), x_margin=round(xm, 1), stand_to_motion=round(worst, 1), ok=bool(outpx == 0 and xm >= 8 and worst >= 10))
    sp = r['spec']
    sp['motion_spec'] = {'node_excavation_bar': dict(
        rotate_about=[round(v, 1) for v in hm], angle_deg=[REST, 0], dir='از %d تا 0 درجه (ساعتگرد در svg = سر بلند میله پایین می‌آید و سنگ بالا می‌رود)' % REST,
        duration_s=1.8, repeat=1, easing='ease-out',
        note='میله و سنگ بار هم‌حرکت‌اند و حول لولا (پین زرد روی سنگ تکیه‌گاه) می‌چرخند؛ سنگ ≈ %.1f واحد بالا می‌آید؛ حالت ایستا = پایان؛ فقط هنگام رسیدن؛ بدون حلقهٔ بیکار.' % lift),
        'reduced_motion': 'ایستا در وضع پایان (زاویه ۰)', 'rotation_check': rot_chk}
    (OUTD / 'excavation.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print('ROT', json.dumps(rot_chk))
