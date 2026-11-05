#!/usr/bin/env python3
"""اتودهای ۳ پیچ‌کاری (D110/D111/D112/D113): سکو هم‌ساختار سکوی چوب‌شکافی (node_09)، بدون خانه.
قاعدهٔ ضخامت: همه‌چیز مستقیم در مختصات symbol (viewBox 200x190) کشیده می‌شود و هیچ scale() روی زیرگروه نیست.
نماد روی نقشه ۱۴۴px پهنا دارد (٠٫٧٢)، پس ٥٫٥ واحد = ٣٫٩٦px.  خروجی: e3_a..e3_d.svg + etudes3.html
"""
import math, pathlib, sys, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from make_etudes import hd, ell, NAVY, HERE

K = .72
OUT, PART, INNER, SEAM = 5.5, 4.5, 3.7, 3.7     # SEAM: جدول ۲٫۸ بود ولی ۲٫۸x۰٫۷۲=۲٫۰px < حداقل ۲٫۵px؛ پس ۳٫۵
BLUE = '#8fb5f2'; PURP = '#8f8bd6'; HEAD_S = '#d6e8ff'; HEAD_T = '#f1f8ff'; THREAD = '#ffe08a'; CREAM = '#fff3c4'
NUT_T = '#ffd84d'; NUT_L = '#f2b92c'; NUT_R = '#d9961c'; NUT_H = '#8a5f0c'
PAD_TOP = '#f4e6a0'; PAD_WALL = '#8a7a2a'; PAD_LINE = '#d4c26a'
WOOD_T = '#e0b070'; WOOD_F = '#c98a45'; WOOD_G = '#a06a30'

RX, RY, WALL = 76, 38, 16
M09 = [(50.9, 0), (49.6, 9.1), (34.2, 16.3), (12.2, 20.2), (-12, 19.9), (-33.9, 16.1), (-44, 8.1), (-52.8, 0),
       (-45.4, -8.3), (-33.3, -15.9), (-11.5, -19.1), (11.7, -19.4), (32.6, -15.5), (47.3, -8.7)]


def pad_top():
    return [(x * (RX / 50.9 if x > 0 else RX / 52.8), y * RY / 19.4) for x, y in M09]


class Pen:
    def __init__(s, uid):
        s.ntop = s.npad = 0; s.uid = uid; s.o = []; s.clip = []; s.k = 0; s.probes = []; s.foot = []; s.padtop = pad_top()

    def _d(s, pts, j, step):
        s.k += 1
        return hd(pts, True, s.k * 7 + 3, j, step)

    def shape(s, pts, fill, sw=OUT, j=.7, step=11, clip=True):
        d = s._d(pts, j, step)
        s.o.append('<path d="%s" fill="%s" class="eo" stroke-width="%s"/>' % (d, fill, sw))
        if clip: s.clip.append(d)
        return d

    def fill(s, pts, fill, op=1):
        s.o.append('<path d="%s" fill="%s"%s/>' % (hd(pts, True, 1, 0, 999), fill, '' if op == 1 else ' opacity="%s"' % op))

    def stroke(s, pts, sw=OUT, j=.7, step=11):
        s.o.append('<path d="%s" fill="none" class="eo" stroke-width="%s"/>' % (s._d(pts, j, step), sw))

    def ln(s, a, b, sw, col, op=1, j=.2, cls='', probe=None):
        s.k += 1
        import random
        r = random.Random(s.k * 13)
        s.o.append('<path d="M%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"%s%s/>' % (
            a[0] + r.uniform(-j, j), a[1] + r.uniform(-j, j), b[0] + r.uniform(-j, j), b[1] + r.uniform(-j, j), col, sw,
            '' if op == 1 else ' opacity="%s"' % op, ' class="eo"' if col == NAVY else ''))
        if probe:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
            s.probes.append((probe, sw, (mx, my), (-(b[1] - a[1]) / L, (b[0] - a[0]) / L), col))

    def raw(s, x): s.o.append(x)

    def svg(s): return ''.join(s.o)


def rot(ox, oy, deg):
    c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    f = lambda p: (ox + p[0] * c - p[1] * sn, oy + p[0] * sn + p[1] * c)
    f.dir = lambda v: (v[0] * c - v[1] * sn, v[0] * sn + v[1] * c)
    return f


def TP(f, pts): return [f(p) for p in pts]


# ---------- سکو (هم‌ساختار node_09) ----------
def pad(pen, line=None, tri=(), dot=None):
    P = pen.padtop
    low = P[:8]
    wall = low + [(x, y + WALL) for x, y in low[::-1]]
    pen.shape(wall, PAD_WALL, OUT); pen.ntop = len(pen.o)
    pen.shape(P, PAD_TOP, OUT)
    pen.probes.append(('خط دور سکو', OUT, (-RX, WALL * .5), (1, 0), NAVY))
    if line: pen.ln(line[0], line[1], INNER, PAD_LINE, j=.15, probe='خط داخلی (خط روشن سکو)')
    for (x, y) in tri:      # دو مثلث ریز لبه (مثل چوب‌شکافی)
        pen.shape([(x - 7, y + 5), (x + 7, y + 5), (x, y - 7)], PURP, INNER, j=.2, step=99, clip=False)
    if dot: pen.raw('<circle cx="%s" cy="%s" r="3.5" fill="%s"/>' % (dot[0], dot[1], PAD_WALL))
    pen.npad = len(pen.o)


# ---------- پیچ ----------
def screw(pen, f, w=15, Lb=100, hw=28, hh=14, P=16, d=4, bottom='tip', y0=0, probe=True, head=True, body=True, shade=True):
    """پیچ در مختصات محلی (نوک در (0,0)، سر بالا). f: تبدیل نقاط. ضخامت‌ها ثابت‌اند."""
    ys = []; y = -Lb + 12
    lim = (-26 if bottom == 'tip' else y0 - 12)
    while y + P / 2 + 3 < lim: ys.append(y); y += P
    L = [(-w, -Lb)]; R = [(w, -Lb)]
    for yk in ys:
        L += [(-w, yk - 3), (-w - d, yk), (-w, yk + 3)]
        yr = yk + P / 2; R += [(w, yr - 3), (w + d, yr), (w, yr + 3)]
    if bottom == 'tip':
        L += [(-w, -16), (0, y0)]; R += [(w, -16)]
        poly = L + R[::-1]
    else:
        ry = .34 * w
        L += [(-w, y0)]; R += [(w, y0)]
        poly = L + ell(0, y0, w, ry, 0, 180, 14)[1:-1][::-1] + R[::-1]
    if body:
        pts = TP(f, poly)
        dd = pen._d(pts, .7, 11); pen.clip.append(dd)
        cid = '%s_c%d' % (pen.uid, pen.k)
        strip = [(w * .3, -Lb - 2), (w + d + 3, -Lb - 2), (w + d + 3, y0 + 4), (w * .3, y0 + 4)]
        pen.raw('<path d="%s" fill="%s"/><clipPath id="%s"><path d="%s"/></clipPath><path d="%s" fill="%s" clip-path="url(#%s)"/>' % (
            dd, BLUE, cid, dd, hd(TP(f, strip), True, 2, 0, 999), PURP, cid))
        for i, yk in enumerate(ys):
            a, b = f((-w + 2, yk)), f((w - 2, yk + P / 2))
            pen.ln(a, b, PART, THREAD, j=.1, probe='رزوه (جزء)' if (probe and i == 1) else None)
        pen.raw('<path d="%s" fill="none" class="eo" stroke-width="%s"/>' % (dd, OUT))
    if head:
        ry = .34 * hw; top = -Lb - hh
        side = ell(0, -Lb, hw, ry, 0, 180, 18) + [(-hw, top), (hw, top)]
        pen.shape(TP(f, side), HEAD_S, OUT)
        pen.shape(TP(f, ell(0, top, hw, ry, 0, 360, 30)), HEAD_T, OUT)
        ph = math.radians(24)
        a = (-.6 * hw * math.cos(ph), -.6 * ry * math.sin(ph) * 1.0 + top); b = (.6 * hw * math.cos(ph), .6 * ry * math.sin(ph) + top)
        pen.ln(f(a), f(b), PART, NAVY, j=.1, probe='شیار سر پیچ (جزء)' if probe else None)
        pen.ln(f((-hw + 8, top + 5)), f((-hw + 8, -Lb - 3)), INNER, CREAM, j=.1, probe='خط داخلی (درخشش)' if probe else None)
        if probe:
            pen.probes.append(('خط دور پیچ (لبهٔ سر)', OUT, f((-hw, top + hh * .5)), f.dir((1, 0)) if hasattr(f, 'dir') else (1, 0), NAVY))
    return poly


# ---------- مهره ----------
def hexv(cx, cy, R, k=.4):
    return [(cx + R, cy), (cx + R / 2, cy + k * R * .866 * 2 / 2 * 1.0), (cx - R / 2, cy + k * R * .866 * 2 / 2), (cx - R, cy),
            (cx - R / 2, cy - k * R * .866 * 2 / 2), (cx + R / 2, cy - k * R * .866 * 2 / 2)]


def nut(pen, cx, cy, R, h, hole=None, ground=True, probe=False):
    """cy = مرکز رویهٔ بالا. اگر ground: مهره روی سکو و پایه‌اش (cy+h) ردپا است."""
    v = hexv(cx, cy, R)
    lo = [(x, y + h) for x, y in v]
    # سه وجه جلویی (پرکردن بدون خط؛ خط دور بعداً)
    pen.fill([v[0], v[1], lo[1], lo[0]], NUT_R); pen.fill([v[1], v[2], lo[2], lo[1]], NUT_L); pen.fill([v[2], v[3], lo[3], lo[2]], '#e8a51f')
    sil = [v[3], v[4], v[5], v[0], lo[0], lo[1], lo[2], lo[3]]
    pen.shape(sil, 'none', OUT, step=5, j=.4)
    pen.clip.append(hd(sil, True, 5, 0, 999))
    for a, b in ((v[1], lo[1]), (v[2], lo[2])): pen.ln(a, b, SEAM, NAVY, j=.1, probe='درز ریز (مهره)' if (probe and a is v[1]) else None)
    pen.shape(v, NUT_T, OUT, step=5, j=.4)
    if hole: pen.shape(ell(cx, cy, hole, hole * .4, 0, 360, 24), NUT_H, SEAM, j=.3, clip=False)
    else: pen.shape(ell(cx, cy, R * .38, R * .15, 0, 360, 22), NUT_H, SEAM, j=.3, clip=False)
    pen.ln((cx - R + 7, cy + .4 * R * .5 + 4), (cx - R + 7, cy + h - 3), INNER, '#fff3c4', j=.1)
    if ground:
        pen.foot.append([(x, y) for x, y in lo])
        pen.raw('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#10083a" opacity=".18"/>' % (cx + 3, cy + h + 2, R * .9, R * .4))


def tipshadow(pen, x, y, r=11):
    pen.raw('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#10083a" opacity=".2"/>' % (x + 2, y + 1, r, r * .34))


def foot_tip(pen, x, y, r=8): pen.foot.append(ell(x, y, r, r * .4, 0, 360, 12))


# ---------- ساخت اتودها ----------
def etude_a():
    p = Pen('e3a'); pad(p, line=((-62, 12), (-44, 17)), tri=((-60, -6), (63, 12)), dot=(24, -24))
    tipshadow(p, -8, 6); foot_tip(p, -8, 6, 10)
    screw(p, rot(-8, 6, 0), w=19, Lb=104, hw=33, hh=17)
    nut(p, 38, -9, 18, 14, ground=True, probe=True)
    return p


def etude_b():
    p = Pen('e3b'); pad(p, line=((-62, 12), (-44, 17)), tri=((-60, -6), (61, 13)), dot=(56, -12))
    tipshadow(p, 0, 8); foot_tip(p, 0, 8, 10)
    w, Lb = 18, 116
    # بخش پایین پیچ (زیر مهره) + مهره + بخش بالای پیچ (سر + بدنه تا سوراخ مهره)
    yn = -60                                         # مرکز رویهٔ مهره
    f = rot(0, 8, 0)
    screw(p, f, w=w, Lb=Lb, hw=33, hh=17, bottom='tip', head=False, probe=False)
    p.raw('<g class="nutlayer" id="NUTLAYER">'); nut(p, 0, 8 + yn, 34, 22, hole=w + 7, ground=False, probe=True); p.raw('</g>')
    screw(p, f, w=w, Lb=Lb, hw=33, hh=17, bottom='arc', y0=yn, head=True, shade=False)
    return p


def etude_c():
    p = Pen('e3c'); pad(p, line=((-66, 8), (-50, 14)), tri=((-64, -12), (62, 10)), dot=(60, -16))
    # تختهٔ چوبی مستطیلی روی سکو: رویه + وجه جلو + وجه راست
    X0, X1, Y0, Y1, T = -27, 24, -18, -6, 11
    pen = p
    top = [(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)]
    front = [(X0, Y1), (X1, Y1), (X1, Y1 + T), (X0, Y1 + T)]
    pen.shape(front, WOOD_F, OUT, j=.5, step=5)
    pen.shape(top, WOOD_T, OUT, j=.5, step=5)
    for (a, b) in (((X0 + 10, Y0 + 5), (X1 - 22, Y0 + 5)), ((X0 + 20, Y1 - 5), (X1 - 10, Y1 - 5))):
        pen.ln(a, b, INNER, WOOD_G, j=.15, probe='خط داخلی (رگهٔ چوب)' if a[0] == X0 + 10 else None)
    pen.ln((X0 + 8, Y1 + T / 2), (X0 + 26, Y1 + T / 2), SEAM, WOOD_G, j=.1)
    pen.foot.append([(X0, Y0), (X1, Y0), (X1, Y1 + T), (X0, Y1 + T)])
    # سوراخ و پیچِ کج‌شده (نیمه‌فروکرده)
    ex, ey = -8, -12
    pen.raw('<ellipse cx="%s" cy="%s" rx="17" ry="6" fill="#6b4524"/>' % (ex, ey))
    f = rot(ex, ey, -32)
    screw(p, f, w=16, Lb=70, hw=30, hh=16, bottom='arc', y0=0)
    # پیچ‌گوشتی: نوک روی تخته سمت راست، تکیه به راست
    g = rot(18, -11, 26)
    sw = 4.5
    shaft = [(-4, -2), (4, -2), (4, -62), (-4, -62)]
    pen.shape(TP(g, shaft), '#c6c1b6', OUT, j=.3, step=30)
    pen.shape(TP(g, [(-4.5, -2), (4.5, -2), (0, 6)]), '#c6c1b6', OUT, j=.2, step=99)
    hnd = [(-11, -62), (11, -62), (13, -92), (9, -118), (-9, -118), (-13, -92)]
    pen.shape(TP(g, hnd), '#c8553d', OUT, j=.5, step=14)
    pen.ln(g((-3, -70)), g((-3, -110)), INNER, CREAM, j=.1)
    pen.ln(g((6, -68)), g((6, -108)), PART, '#8d3b2e', j=.1) if False else None
    pen.ln(g((-12, -78)), g((12, -78)), PART, '#8d3b2e', j=.1, probe='جزء (رینگ دستهٔ پیچ‌گوشتی)')
    pen.foot.append([(15, -14), (21, -14), (21, -9), (15, -9)])
    return p


def etude_d():
    p = Pen('e3d'); pad(p, line=((-66, 12), (-50, 17)), tri=((-66, -8), (64, -8)), dot=(62, 8))
    tipshadow(p, -34, 6); foot_tip(p, -34, 6, 9); tipshadow(p, 12, 10); foot_tip(p, 12, 10, 8)
    screw(p, rot(-34, 6, 0), w=16, Lb=112, hw=29, hh=15)
    screw(p, rot(12, 10, 0), w=14, Lb=56, hw=25, hh=13, probe=False)
    nut(p, 42, -8, 15, 11, ground=True, probe=False)
    return p


ETUDES = {'a': (etude_a, 'پیچ بلند + مهرهٔ شش‌ضلعی روی سکو'), 'b': (etude_b, 'پیچ بلند + مهرهٔ بزرگ روی رزوه'),
          'c': (etude_c, 'پیچ کج در تختهٔ چوبی + پیچ‌گوشتی'), 'd': (etude_d, 'دو پیچ (بلند و کوتاه) + یک مهره')}

STYLE = ('.eo{stroke:#241a5e;stroke-linejoin:round;stroke-linecap:round}.elit{fill:#fff4cf;opacity:.3}'
         '.esh{fill:#4a3a8c;opacity:.22}.esd{fill:#10083a;opacity:.28}')


def symbol(p, sid):
    shadow = '<ellipse cx="2" cy="5" rx="%s" ry="%s" class="esd"/>' % (RX - 1, RY - 3)
    under = '<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="#10083a" opacity=".3"/>' % (RY * 1.05 + 1, RX - 2, RY * 1.0)
    cid = sid + '_clip'
    allpad = ''.join('<path d="%s"/>' % hd(pad_top()[:8] + [(x, y + WALL) for x, y in pad_top()[:8][::-1]], True, 1, 0, 999) for _ in [0])
    allpad += '<path d="%s"/>' % hd(p.padtop, True, 1, 0, 999)
    clip = '<defs><clipPath id="%s">%s%s</clipPath></defs>' % (cid, allpad, ''.join('<path d="%s"/>' % d for d in p.clip))
    lit = '<polygon points="-%s,-165 -%s,-165 -%s,50 -%s,50" class="elit"/>' % (RX, RX * .37, RX * .7, RX)
    shade = '<polygon points="%s,-165 %s,-165 %s,50 0,50" class="esh"/>' % (RX * .33, RX, RX)
    return ('<symbol id="%s" viewBox="0 0 200 190" overflow="visible">%s'
            '<g id="%s_shadow" transform="translate(100 150)">%s</g>'
            '<g id="%s_base" transform="translate(100 150)">%s%s</g>'
            '<g id="%s_lit" transform="translate(100 150)" clip-path="url(#%s)">%s</g>'
            '<g id="%s_shade" transform="translate(100 150)" clip-path="url(#%s)">%s</g></symbol>') % (
        sid, clip, sid, shadow, sid, under, p.svg(), sid, cid, lit, sid, cid, shade)


MAPBG = ('<rect width="330" height="200" fill="#c9a35c"/>'
         '<path d="M-10,175 C60,150 70,95 130,60 S200,10 260,-10" fill="none" stroke="#241a5e" stroke-width="34" stroke-linecap="round"/>'
         '<path d="M-10,175 C60,150 70,95 130,60 S200,10 260,-10" fill="none" stroke="#a79c9b" stroke-width="26" stroke-linecap="round"/>')


def main():
    syms = []; cells = []; meta = {}
    for k, (fn, title) in ETUDES.items():
        p = fn(); sid = 'node_screw_workshop_e3' + k
        sym = symbol(p, sid); syms.append(sym)
        (HERE / ('e3_%s.svg' % k)).write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 190" width="144" height="137"><style>%s</style>%s<use href="#%s"/></svg>' % (STYLE, sym, sid), encoding='utf-8')
        meta[k] = dict(foot=[[list(q) for q in poly] for poly in p.foot], probes=[(a, b, list(c), list(d), e) for a, b, c, d, e in p.probes], padtop=pad_top())
        cells.append('<div class="c"><h3>%s) %s</h3><div class="r"><div class="big" id="big%s"><svg width="432" height="522" viewBox="0 0 200 242"><use href="#%s"/></svg></div>'
                     '<svg class="map" id="map%s" width="330" height="200" viewBox="0 0 330 200">%s<use href="#%s" x="95" y="30" width="144" height="137"/></svg></div></div>' % ('ابجد'[ 'abcd'.index(k)], title, k, sid, k, MAPBG, sid))
    html = ('<!doctype html><meta charset=utf-8><title>اتودهای ۳ پیچ‌کاری</title><style>%s'
            'body{margin:0;background:#e9c57e;font-family:Vazirmatn,system-ui,sans-serif;direction:rtl;color:#241a5e}'
            '.c{padding:10px 14px}.r{display:flex;gap:18px;align-items:flex-end;flex-wrap:wrap}h3{margin:6px 0;font-size:18px}'
            '.big{background:#c9a35c;line-height:0}.big svg{overflow:visible}</style>'
            '<svg width="0" height="0" style="position:absolute"><defs>%s</defs></svg>%s') % (STYLE, ''.join(syms), ''.join(cells))
    (HERE / 'etudes3.html').write_text(html, encoding='utf-8')
    (HERE / 'e3_meta.json').write_text(json.dumps(meta), encoding='utf-8')


if __name__ == '__main__': main()
