#!/usr/bin/env python3
"""ایستگاه F03 «میدان کمان‌کِشی» (سرزمین ورزشگاه، سکوی سبز) — بازسازی کامل (۲۲ اکتبر).
کمان چوبی باریک و ایستاده (شکم به چپ = سمت هدف)، زه سمت راست، تیر روی دستگیره: نوک فلزی سمت هدف، پر سمت زه،
ته تیر دقیقاً روی رأس V زه. فقط خط‌های ۷٫۶/۵٫۸/۳٫۹؛ چوب = همان سه پلهٔ چوب‌شکافی/تبر؛ فلز = پله‌های تیغهٔ تبر؛
زه = رنگ کابل جرثقیل؛ قرمز = بدنهٔ جرثقیل. لایهٔ متحرک node_archery_range_string = زه + تیر. حالت ایستا = زه کشیده (پایان)."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import functools, station_kit as _k
from station_kit import *
_k.margin_check = functools.partial(_k.margin_check, min_margin=8); _k.motion_check = functools.partial(_k.motion_check, min_margin=8)
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/archery'

WOOD = '#b77a3a'; WOOD_L = '#d9a463'; WOOD_D = '#7a4a1f'
RED = '#e0553a'; RED_L = '#ff9a6c'; RED_D = '#9c2f1c'
STEEL = '#dbe9f8'; STEEL_S = '#a3bbd9'; STEEL_L = '#ffffff'
CORD = '#8a5f0c'; CREAM = '#fff3c4'; YEL = '#ffd84d'; FEA_D = '#c9452c'

XF = (0.9, 2.0, 0.0)
YT, YB = -112, 4
YM = (YT + YB) / 2            # -54
HC = (YB - YT) / 2 - 0        # 58
SAG = 24
R = (HC ** 2 + SAG ** 2) / (2 * SAG)
X0 = math.sqrt(R * R - 0) - SAG   # = R - SAG
AY = YM - 12                   # ارتفاع تیر = رأس V (روی بخش بالایی دستگیره)
NX = 16                       # ته تیر (رأس V) در حالت کشیده
PULL = 6                     # جابه‌جایی تا حالت رها
TIPX = -66


def cx(dy): return -(math.sqrt(R * R - dy * dy) - X0)          # خط مرکز کمان (دایره‌ای)
def half(dy): return 8 - 3 * abs(dy / HC) ** 3                # نیم‌پهنای بدنه: ۷ در میانه، ۴٫۵ در نوک


def frame(dy):
    """نقطهٔ مرکز، نرمال (به سمت +x)."""
    e = .01
    d = (cx(dy + e) - cx(dy - e)) / (2 * e)
    n = math.hypot(d, 1)
    return (cx(dy), YM + dy), (1 / n, -d / n)


def band(d0, d1, f0, f1, n=24, absolute=False):
    """نوار موازی منحنی بین دو سطح dy، از آفست f0 تا f1 (کسری از نیم‌پهنای دیدنی h = نیم‌پهنا − ۲٫۹)."""
    A, B = [], []
    for i in range(n + 1):
        dy = d0 + (d1 - d0) * i / n
        (x, y), (nx, ny) = frame(dy); h = half(dy) - PART / 2
        o0 = f0 if absolute else f0 * h; o1 = f1 if absolute else f1 * h
        A.append((x + nx * o0, y + ny * o0)); B.append((x + nx * o1, y + ny * o1))
    return A + B[::-1]


def outline(n=40):
    """بدنهٔ پیوستهٔ کمان با دو نوک گرد (نیم‌دایره r=۴٫۵)."""
    L, Rr = [], []
    for i in range(n + 1):
        dy = -HC + 2 * HC * i / n
        (x, y), (nx, ny) = frame(dy); w = half(dy)
        L.append((x - nx * w, y - ny * w)); Rr.append((x + nx * w, y + ny * w))
    return L, Rr


def body_pts():
    L, Rr = outline()
    # مسیر: چپ از بالا به پایین، نوک پایین (چپ→راست)، راست از پایین به بالا، نوک بالا (راست→چپ)
    return L + bottom_fix(L, Rr) + Rr[::-1] + top_fix(L, Rr)


def _cap(c, a, b, flip):
    """نیم‌دایره از نقطهٔ a تا b دور مرکز c (همسو با جهت: از a به b از بیرونِ نوک)."""
    r = math.hypot(a[0] - c[0], a[1] - c[1]); a0 = math.atan2(a[1] - c[1], a[0] - c[0])
    out = []
    for k in range(1, 8):
        t = a0 + flip * math.pi * k / 8
        out.append((c[0] + r * math.cos(t), c[1] + r * math.sin(t)))
    return out


def bottom_fix(L, Rr):
    c = ((L[-1][0] + Rr[-1][0]) / 2, (L[-1][1] + Rr[-1][1]) / 2)
    # از چپ-پایین به راست-پایین از زیر (y بزرگ‌تر): در مختصات y-پایین، زاویه از ~۱۸۰° به ~۰° از طریق ۹۰°
    a0 = math.atan2(L[-1][1] - c[1], L[-1][0] - c[0]); r = math.hypot(L[-1][0] - c[0], L[-1][1] - c[1])
    best = None
    for flip in (1, -1):
        mid = (c[0] + r * math.cos(a0 + flip * math.pi / 2), c[1] + r * math.sin(a0 + flip * math.pi / 2))
        if best is None or mid[1] > best[1][1]: best = (flip, mid)
    return _cap(c, L[-1], Rr[-1], best[0])


def top_fix(L, Rr):
    c = ((L[0][0] + Rr[0][0]) / 2, (L[0][1] + Rr[0][1]) / 2)
    a0 = math.atan2(Rr[0][1] - c[1], Rr[0][0] - c[0]); r = math.hypot(Rr[0][0] - c[0], Rr[0][1] - c[1])
    best = None
    for flip in (1, -1):
        mid = (c[0] + r * math.cos(a0 + flip * math.pi / 2), c[1] + r * math.sin(a0 + flip * math.pi / 2))
        if best is None or mid[1] < best[1][1]: best = (flip, mid)
    return _cap(c, Rr[0], L[0], best[0])


def mpoly(p, pts, fill, sw):
    """چندضلعی تیز: دور سرمه‌ای با miter (نوک تیز، نه گرد)."""
    q = p.X(pts)
    d = 'M' + 'L'.join('%.1f,%.1f' % z for z in q) + 'Z'
    p.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s" stroke-linejoin="miter" stroke-miterlimit="6"/>' % (d, fill or 'none', sw))


def build():
    p = Pen('archery_range', 'sports'); pad(p, line=((16, 27), (34, 24)), tri=((18, -22), (62, 6)), dot=(58, -16))
    p.xf = XF
    p.tipshadow(-.5, YB + 4, 14); p.foot_tip(-.5, YB + 6, 9)
    # ۱) بدنهٔ کمان: یک بدنهٔ پیوسته، خط دور PART (هم‌ضخامت بازوی جرثقیل)، نوک گرد
    pts = body_pts()
    p.shape(pts, WOOD, PART, j=.04, step=99, clip=True)
    # ۲) نور چوب: یک نوار تخت در لبهٔ بیرونی (چپ)، هر بازو
    for d0, d1 in ((-46, -8), (8, 46)):
        p.fill(band(d0, d1, -.86, -.2), WOOD_L)
    # ۳) سایهٔ تیز راست هر بازو، سپس دور بدنه دوباره
    for d0, d1 in ((-50, -8), (8, 50)):
        p.fill(band(d0, d1, .3, 1.6), WOOD_D, .55)
    p.stroke(pts, PART, j=.04, step=99)
    # ۴) دستگیره: قرمز تخت روی بدنه، دو نوار تیره، یک نوار روشن
    p.fill(band(-22, 6, -1, 1), RED)
    p.fill(band(-22, 6, -.85, -.2), RED_L)
    p.fill(band(-22, -19, -1, 1), RED_D); p.fill(band(3, 6, -1, 1), RED_D)
    # ۵) نوک‌گیر زرد
    for dy in (-HC + 4, HC - 4):
        (x, y), _ = frame(dy); a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>' % (a, b, YEL))
    # ۶) لایهٔ متحرک: زه + تیر
    (tx, ty), _ = frame(-HC + 4); (bx, by), _ = frame(HC - 4)
    with layer(p, 'string'):
        p.raw('<g id="node_archery_range_string_cord">')
        p.ln((tx, ty), (NX, AY), INNER, CORD, j=.03, probe='زه (بالا)')
        p.ln((NX, AY), (bx, by), INNER, CORD, j=.03)
        p.raw('</g><g id="node_archery_range_string_arrow">')
        # شفت باریک: زیرخط سرمه‌ای PART (۵٫۸) + هستهٔ کرم ۲٫۹
        p.ln((NX - 1, AY), (TIPX + 14, AY), PART, NAVY, j=.02)
        p.ln((NX - 1, AY), (TIPX + 14, AY), 2.9, CREAM, j=.02)
        # پرها: دو ذوزنقهٔ باریک و بلند موازی شفت، ۱۲ واحد آخر تیر (لبهٔ بیرونی کمی به سمت زه)
        for sg, col in ((-1, RED), (1, CREAM)):
            mpoly(p, [(NX - 17, AY + sg * 3.5), (NX - 13, AY + sg * 11), (NX - 1, AY + sg * 11), (NX - 4, AY + sg * 3.5)], col, INNER)
        # نوک فلزی: مثلث کشیدهٔ تیز، دور INNER با miter؛ دو پله + برق
        T0 = TIPX; L = 17; HW = 6
        Hd = [(T0, AY), (T0 + L, AY - HW), (T0 + L, AY + HW)]
        mpoly(p, Hd, STEEL, INNER)
        p.fill([(T0 + 4, AY + .5), (T0 + L - 1, AY + .5), (T0 + L - 1, AY + HW - 2.2), (T0 + 7.2, AY + 2.2)], STEEL_S)
        p.ln((T0 + 8, AY - 1.4), (T0 + 14, AY - 3.2), 2.2 if False else INNER * .6, STEEL_L, j=.02)
        mpoly(p, Hd, None, INNER)
        # کام روی رأس V
        a, b = p.X((NX, AY)); p.raw('<circle cx="%.1f" cy="%.1f" r="2.4" fill="%s"/>' % (a, b, YEL))
        p.raw('</g>')
    return p


if __name__ == '__main__':
    p = build()
    offs = [p.V((-PULL, 0)), (0, 0)]
    r = finish(p, 'archery_range', None, motion={'string': dict(offsets=offs)}, out=OUTD, shots=SHOTS)
    sp = r['spec']
    nk_rest = p.X((NX - PULL, AY)); nk_end = p.X((NX, AY))
    (tx, ty), _ = frame(-HC + 4); (bx, by), _ = frame(HC - 4)
    ms = {'node_archery_range_string': dict(
        kind='زه + تیر؛ حالت ایستا = حالت کشیده (پایان حرکت)',
        children={'node_archery_range_string_arrow': 'تیر + پر + نوک + کام؛ فقط translateX',
                  'node_archery_range_string_cord': 'دو خط زه؛ دو سر بالا و پایین ثابت روی نوک‌گیرها، سر میانی روی ته تیر'},
        translate_x_symbol_units=[-PULL, 0], translate_x_map_px=[round(-PULL * K, 1), 0],
        string_fixed_ends_map_px=[[round(v, 1) for v in p.X((tx, ty))], [round(v, 1) for v in p.X((bx, by))]],
        nock_rest=[round(v, 1) for v in nk_rest], nock_end=[round(v, 1) for v in nk_end],
        duration_s=.7, easing='ease-out', loop=False, trigger='رسیدن کودک (یک‌بار)',
        how='گروه arrow را از translateX(-%d) به 0 ببر. زه: دو خط (یا یک path با سه نقطه) که دو سر ثابت می‌مانند و نقطهٔ میانی (رأس V) با ته تیر از x=%.1f تا x=%.1f می‌رود؛ یعنی در حالت رها زه تقریباً راست است. بدنهٔ کمان ثابت و کامل.' % (PULL, nk_rest[0], nk_end[0]),
        note='بدون حلقهٔ بیکار؛ با reduced-motion ثابت در حالت کشیده.')}
    sp['motion_spec'] = ms
    (OUTD / 'archery_range.json').write_text(json.dumps(sp, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: r[k] for k in ('ok', 'margin', 'inside', 'motion')} | {'widths': [(w['label'], w['measured_px'], w['ok']) for w in r['widths']]}, ensure_ascii=False))
