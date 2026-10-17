#!/usr/bin/env python3
"""کیت مشترک نماد ایستگاه نقشه (قواعد D107-D115، docs/STATION_SYMBOL_RULES_FA.md).
ماژول مستقل: فقط numpy / scipy / playwright لازم است (برای سنجش‌ها)، به هیچ اتودی وابسته نیست.

گردش کار یک ایستگاه:
    pen = Pen('my_station', kind='land'|'sea')      # kind پالت را تعیین می‌کند
    pad(pen, line=..., tri=..., dot=...)             # سکو (اول از همه)
    with layer(pen, 'gear'): ...                      # بخش متحرک = id پایدار node_<id>_<part>
    ... شیء قهرمان را با pen.shape / pen.ln / pen.fill بکش ...
    sym = symbol(pen, 'my_station', motion_layers=['gear'], out=پوشه)   # node_my_station.svg
    margin_check(pen, stand=(dx, dy)); width_check(pen)
    spec('my_station', pad_px(pen, bh), stand, ['node_my_station_gear'], kind=pen.kind, out=پوشه)
قاعده: همه‌چیز مستقیم در مختصات symbol (0 0 200 190، مرکز translate(100 150)) کشیده شود؛ هیچ scale() روی زیرگروه.
"""
import math, random, json, pathlib
from contextlib import contextmanager

HERE = pathlib.Path(__file__).resolve().parent
K = .72                                   # مقیاس نماد روی نقشه (144px از 200)
OUT, PART, INNER = 5.5, 4.5, 3.7         # ضخامت اسمی: دور سکو/بنا، جزء، داخلی (≈4 / 3.2 / 2.7px نقشه)
SEAM = INNER                              # درز ریز هم‌اندازهٔ داخلی (حداقل 2.5px نقشه)
MIN_PX = 2.5                              # کمینهٔ قطر خط روی نقشه
NAVY = '#241a5e'
CREAM = '#fff3c4'

# پالت سکو. «زمینی» = کرم/زیتونی (سکوی چوب‌شکافی)؛ «دریایی» = آبی روشن/آبی تیره (رنگ‌های node_wheel_dock).
PALETTES = {
    'land': dict(top='#f4e6a0', wall='#8a7a2a', line='#d4c26a', tri='#8f8bd6', dot='#8a7a2a'),
    'sea': dict(top='#a6bde8', wall='#4d6fb0', line='#d6e8ff', tri='#7b8fe0', dot='#4d6fb0'),
}
STYLE = ('.eo{stroke:#241a5e;stroke-linejoin:round;stroke-linecap:round}.elit{fill:#fff4cf;opacity:.3}'
         '.esh{fill:#4a3a8c;opacity:.22}.esd{fill:#10083a;opacity:.28}')

# شکل ارگانیک لبهٔ سکو (از node_09)، در مختصات «نیم‌پهنا≈۵۱، نیم‌ارتفاع≈۱۹٫۴»
_M09 = [(50.9, 0), (49.6, 9.1), (34.2, 16.3), (12.2, 20.2), (-12, 19.9), (-33.9, 16.1), (-44, 8.1), (-52.8, 0),
        (-45.4, -8.3), (-33.3, -15.9), (-11.5, -19.1), (11.7, -19.4), (32.6, -15.5), (47.3, -8.7)]


# ---------------- هندسه و خط دستی ----------------
def sub(pts, closed, step):
    out = []; n = len(pts)
    for i in range(n if closed else n - 1):
        a, b = pts[i], pts[(i + 1) % n]
        L = math.hypot(b[0] - a[0], b[1] - a[1]); k = max(1, int(L / step))
        for t in range(k): out.append((a[0] + (b[0] - a[0]) * t / k, a[1] + (b[1] - a[1]) * t / k))
    if not closed: out.append(pts[-1])
    return out


def hd(pts, closed=True, seed=1, j=1.1, step=11):
    """مسیر «خط دست» برداری: لرزش در خود مسیر پخته می‌شود (بدون فیلتر رستری)."""
    r = random.Random(seed); p = [(x + r.uniform(-j, j), y + r.uniform(-j, j)) for x, y in sub(pts, closed, step)]
    f = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    n = len(p)
    if closed:
        s = f(p[-1], p[0]); d = 'M%.1f,%.1f' % s
        for i in range(n): m = f(p[i], p[(i + 1) % n]); d += 'Q%.1f,%.1f %.1f,%.1f' % (p[i][0], p[i][1], m[0], m[1])
        return d + 'Z'
    d = 'M%.1f,%.1f' % p[0]
    for i in range(1, n - 1): m = f(p[i], p[i + 1]); d += 'Q%.1f,%.1f %.1f,%.1f' % (p[i][0], p[i][1], m[0], m[1])
    return d + 'L%.1f,%.1f' % p[-1]


def ell(cx, cy, rx, ry, a0=0, a1=360, n=40):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * i / n)))
            for i in range(n + (0 if a1 - a0 >= 360 else 1))]


def rot(ox, oy, deg):
    """تبدیل نقطه‌ها (چرخش حول (ox,oy)) — به‌جای transform روی زیرگروه، تا ضخامت خط تغییر نکند."""
    c, sn = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    f = lambda p: (ox + p[0] * c - p[1] * sn, oy + p[0] * sn + p[1] * c)
    f.dir = lambda v: (v[0] * c - v[1] * sn, v[0] * sn + v[1] * c)
    return f


def TP(f, pts): return [f(p) for p in pts]


# ---------------- قلم ----------------
class Pen:
    def __init__(s, station_id, kind='land', rx=76, ry=38, wall=16):
        assert kind in PALETTES, 'kind باید land یا sea باشد'
        s.id = s.uid = station_id; s.kind = kind; s.rx, s.ry, s.wall = rx, ry, wall
        s.ntop = s.npad = 0; s.o = []; s.clip = []; s.k = 0; s.probes = []; s.foot = []; s.layers = {}
        s.padtop = _padtop(rx, ry)

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

    def ln(s, a, b, sw, col, op=1, j=.2, probe=None):
        """خط راست. probe='برچسب' آن را برای width_check ثبت می‌کند."""
        s.k += 1
        r = random.Random(s.k * 13)
        s.o.append('<path d="M%.1f,%.1f L%.1f,%.1f" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round"%s%s/>' % (
            a[0] + r.uniform(-j, j), a[1] + r.uniform(-j, j), b[0] + r.uniform(-j, j), b[1] + r.uniform(-j, j), col, sw,
            '' if op == 1 else ' opacity="%s"' % op, ' class="eo"' if col == NAVY else ''))
        if probe:
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1
            s.probes.append((probe, sw, (mx, my), (-(b[1] - a[1]) / L, (b[0] - a[0]) / L), col))

    def raw(s, x): s.o.append(x)

    def svg(s): return ''.join(s.o)

    def tipshadow(s, x, y, r=11):
        """سایهٔ کوچک زیر نقطهٔ تماس (روی سکو)."""
        s.raw('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="#10083a" opacity=".2"/>' % (x + 2, y + 1, r, r * .34))

    def foot_tip(s, x, y, r=8):
        """ردپای تماس با سکو؛ margin_check فاصلهٔ آن تا لبهٔ سکو را می‌سنجد."""
        s.foot.append(ell(x, y, r, r * .4, 0, 360, 12))


@contextmanager
def layer(pen, name):
    """بخش متحرک: همهٔ ترسیم‌های داخل with در <g id="node_<id>_<name>"> می‌روند (قاعدهٔ ۱۱)."""
    pen.o.append('<g id="node_%s_%s">' % (pen.id, name)); i = len(pen.o)
    yield
    pen.layers[name] = (i, len(pen.o)); pen.o.append('</g>')


def _padtop(rx, ry):
    return [(x * (rx / 50.9 if x > 0 else rx / 52.8), y * ry / 19.4) for x, y in _M09]


def _wall_pts(pen):
    low = pen.padtop[:8]
    return low + [(x, y + pen.wall) for x, y in low[::-1]]


# ---------------- سکو ----------------
def pad(pen, kind=None, rx=None, ry=None, wall=None, line=None, tri=(), dot=None):
    """سکوی هم‌ساختار چوب‌شکافی: دیوارهٔ دو‌رنگ + رویه + یک خط روشن + مثلث‌های ریز لبه + یک نقطهٔ تیره.
    kind و اندازه‌ها (در مختصات symbol) در صورت پرشدن Pen را به‌روز می‌کنند. باید اولین فراخوانی ترسیم باشد."""
    assert not pen.o, 'pad باید قبل از هر ترسیم دیگر صدا زده شود'
    if kind: assert kind in PALETTES; pen.kind = kind
    if rx or ry or wall:
        pen.rx, pen.ry, pen.wall = rx or pen.rx, ry or pen.ry, wall or pen.wall; pen.padtop = _padtop(pen.rx, pen.ry)
    pal = PALETTES[pen.kind]
    pen.shape(_wall_pts(pen), pal['wall'], OUT); pen.ntop = len(pen.o)
    pen.shape(pen.padtop, pal['top'], OUT)
    pen.probes.append(('خط دور سکو', OUT, (-pen.rx, pen.wall * .5), (1, 0), NAVY))
    if line: pen.ln(line[0], line[1], INNER, pal['line'], j=.15, probe='خط داخلی (خط روشن سکو)')
    for (x, y) in tri:
        pen.shape([(x - 7, y + 5), (x + 7, y + 5), (x, y - 7)], pal['tri'], INNER, j=.2, step=99, clip=False)
    if dot: pen.raw('<circle cx="%s" cy="%s" r="3.5" fill="%s"/>' % (dot[0], dot[1], pal['dot']))
    pen.npad = len(pen.o)


# ---------------- symbol ----------------
def symbol(pen, name, motion_layers=(), out=None, legacy_shadow=False):
    """symbol با viewBox 0 0 200 190، مرکز translate(100 150)، گروه‌های _shadow/_base/_lit/_shade و clipPath.
    name = شناسهٔ ایستگاه؛ id نماد node_<name>. اگر out (پوشه) داده شود، فایل node_<name>.svg نوشته می‌شود.
    legacy_shadow=True سایهٔ زیرین قدیمی اتود ب را می‌سازد (فقط برای مقایسه؛ روی راه می‌افتد)."""
    for m in motion_layers:
        assert m in pen.layers, 'لایهٔ متحرک %r در Pen ساخته نشده' % m
    sid = 'node_' + name; RX, RY, W = pen.rx, pen.ry, pen.wall
    shadow = '<ellipse cx="2" cy="5" rx="%s" ry="%s" class="esd"/>' % (RX - 7 if not legacy_shadow else RX - 1, RY - 3)
    if legacy_shadow:
        under = '<ellipse cx="0" cy="%s" rx="%s" ry="%s" fill="#10083a" opacity=".3"/>' % (RY * 1.05 + 1, RX - 2, RY * 1.0)
    else:   # D112: سایه کاملاً درون سیلوئت سکو (رویه+دیواره) می‌ماند و روی راه نمی‌افتد
        under = '<ellipse cx="2" cy="%s" rx="%s" ry="%s" fill="#10083a" opacity=".3"/>' % (W * .6, RX - 4, RY * .9 + W * .4 - 1)
    under = '<g class="under">%s</g>' % under
    cid = sid + '_clip'
    allpad = '<path d="%s"/><path d="%s"/>' % (hd(_wall_pts(pen), True, 1, 0, 999), hd(pen.padtop, True, 1, 0, 999))
    clip = '<defs><clipPath id="%s">%s%s</clipPath></defs>' % (cid, allpad, ''.join('<path d="%s"/>' % d for d in pen.clip))
    lit = '<polygon points="-%s,-165 -%s,-165 -%s,50 -%s,50" class="elit"/>' % (RX, RX * .37, RX * .7, RX)
    shade = '<polygon points="%s,-165 %s,-165 %s,50 0,50" class="esh"/>' % (RX * .33, RX, RX)
    sym = ('<symbol id="%s" viewBox="0 0 200 190" overflow="visible">%s'
           '<g id="%s_shadow" transform="translate(100 150)">%s</g>'
           '<g id="%s_base" transform="translate(100 150)">%s%s</g>'
           '<g id="%s_lit" transform="translate(100 150)" clip-path="url(#%s)">%s</g>'
           '<g id="%s_shade" transform="translate(100 150)" clip-path="url(#%s)">%s</g></symbol>') % (
        sid, clip, sid, shadow, sid, under, pen.svg(), sid, cid, lit, sid, cid, shade)
    if out:
        out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
        (out / ('node_%s.svg' % name)).write_text(sym, encoding='utf-8')
    return sym


def preview(sym, name, w=144, tall=False):
    """صفحهٔ svg مستقل برای دیدن نماد (با STYLE). w = پهنای نمایش؛ ۱۴۴ = اندازهٔ نقشه."""
    vh = 222.2 if tall else 190     # tall: دیوارهٔ سکو زیر خط ۱۹۰ بریده نشود (فقط برای شات)
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 %s" width="%s" height="%s"><style>%s</style>%s'
            '<use href="#node_%s"/></svg>') % (vh, w, round(w * vh / 200), STYLE, sym, name)


def pad_px(pen, bh):
    """اندازهٔ سکو به px نقشه (مقیاس ۰٫۷۲): [rx, ry, wall, bh]. bh = ارتفاع بنا/قهرمان روی سکو (از margin_check)."""
    return [round(pen.rx * K, 1), round(pen.ry * K, 1), round(pen.wall * K, 1), round(bh)]


def spec(id, pad_px, stand, motion, kind='land', ring=(0, 0, 0), out=None):
    """فایل مشخصات ایستگاه: stations/<id>.json.
    pad=[rx,ry,wall,bh] px نقشه؛ stand=[dx,dy] جای فیگور از مرکز سکو؛ ring=[drx,dry,dx]؛ motion=[ids لایه‌ها]."""
    d = dict(id=id, kind=kind, pad=list(pad_px), stand=list(stand), ring=list(ring), motion=list(motion))
    p = pathlib.Path(out) if out else HERE / 'stations'; p.mkdir(parents=True, exist_ok=True)
    (p / ('%s.json' % id)).write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding='utf-8')
    return d


# ---------------- رندر و سنجش ----------------
def _shot(body, dsf=4, bg=None, w=144, h=160):
    """body: محتوای svg (سطر بالا مثل symbol؛ پایین بلندتر تا دیوارهٔ سکو بریده نشود) → آرایهٔ RGBA. هر px نقشه = dsf پیکسل."""
    import numpy as np, io
    from PIL import Image
    from playwright.sync_api import sync_playwright
    html = ('<body style="margin:0;background:%s"><svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" viewBox="0 0 200 %.1f">'
            '<style>%s</style><g transform="translate(100 150)">%s</g></svg>') % (bg or 'transparent', w, h, h / K, STYLE, body)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(device_scale_factor=dsf, viewport={'width': w, 'height': h})
        pg.set_content(html); png = pg.screenshot(omit_background=bg is None); b.close()
    return np.array(Image.open(io.BytesIO(png)).convert('RGBA'))


def _poly(pts): return '<path d="%s" fill="#000"/>' % hd(pts, True, 1, 0, 999)


def margin_check(pen, stand=None, dsf=4, min_margin=8, min_stand=10, save=None, legacy_shadow=False):
    """سنجش از رندر: (۱) پیکسل‌های قهرمان بیرون از سیلوئت سکو، (۲) حاشیهٔ افقی قهرمان تا لبهٔ سکو،
    (۳) حاشیهٔ ردپا (foot) تا لبهٔ رویه، (۴) سایه روی راه، (۵) فاصلهٔ جای فیگور (stand) از قهرمان و از لبهٔ رویه.
    همه به px نقشه. stand=(dx,dy) px نقشه از مرکز سکو. برمی‌گرداند dict با کلید ok."""
    import numpy as np
    from scipy.ndimage import distance_transform_edt as edt
    A = lambda im: im[..., 3] > 128
    top = A(_shot(_poly(pen.padtop), dsf)); wall = A(_shot(_poly(_wall_pts(pen)), dsf)); sil = top | wall
    hero_svg = ''.join(pen.o[pen.npad:])
    hero = A(_shot(hero_svg, dsf))
    # ناحیهٔ مجاز: هر ستونِ سکو، از بالا تا پایین‌ترین نقطهٔ سیلوئت (قهرمان بلند می‌تواند بالای سکو بیاید)
    cols = sil.any(0); low = np.where(cols, sil.shape[0] - 1 - np.argmax(sil[::-1], 0), -1)
    rows = np.arange(sil.shape[0])[:, None]
    allowed = cols[None, :] & (rows <= low[None, :])
    outside = hero & ~allowed
    res = dict(out_px=round(float(outside.sum()) / dsf ** 2, 1))
    xs = np.where(hero.any(0))[0]; px = np.where(top.any(0))[0]
    res['x_margin'] = round(float(min(xs.min() - px.min(), px.max() - xs.max())) / dsf, 1) if len(xs) else None
    ys = np.where(hero.any(1))[0]
    cy = 150 * K * dsf                                   # ردیف مرکز سکو
    res['bh'] = round((cy - ys.min()) / dsf, 1) if len(ys) else 0
    if pen.foot:
        foot = A(_shot(''.join(_poly(f) for f in pen.foot), dsf)); d = edt(top)
        res['foot_margin'] = round(float(d[foot].min()) / dsf, 1) if foot.any() else None
    # سایه روی راه: سایه‌های _shadow و under را جدا رندر کن
    res['shadow_on_road_px'] = _shadow_leak(pen, sil, dsf, legacy_shadow)
    if stand:
        sx, sy = (100 * K + stand[0]) * dsf, (150 * K + stand[1]) * dsf
        yy, xx = np.mgrid[0:top.shape[0], 0:top.shape[1]]
        near = np.hypot(xx - sx, yy - sy)
        res['stand_to_hero'] = round(float(near[hero].min()) / dsf, 1)
        res['stand_to_pad_edge'] = round(float(edt(top)[int(sy), int(sx)]) / dsf, 1)
        res['stand_on_pad'] = bool(top[int(sy), int(sx)])
    ok = res['out_px'] == 0 and (res['x_margin'] or 0) >= min_margin and res['shadow_on_road_px'] == 0
    if 'foot_margin' in res: ok = ok and (res['foot_margin'] or 0) >= min_margin
    if stand: ok = ok and res['stand_on_pad'] and res['stand_to_hero'] >= min_stand and res['stand_to_pad_edge'] >= min_stand
    res['ok'] = bool(ok)
    if save:
        from PIL import Image
        Image.fromarray((np.dstack([hero * 255, top * 255, outside * 255]).astype('uint8'))).save(save)
    return res


def _shadow_leak(pen, sil, dsf, legacy=False):
    """پیکسل‌های سایه (_shadow و under) که بیرون از سیلوئت سکو افتاده‌اند (px نقشه²). سایه‌ها را از symbol می‌خوانیم."""
    import re
    s = symbol(pen, 'x_probe', legacy_shadow=legacy)
    parts = re.findall(r'<g id="node_x_probe_shadow"[^>]*>(.*?)</g>', s) + re.findall(r'<g class="under">(.*?)</g>', s)
    im = _shot(''.join(parts), dsf)
    from scipy.ndimage import binary_dilation
    return round(float(((im[..., 3] > 10) & ~binary_dilation(sil, iterations=2)).sum()) / dsf ** 2, 1)   # 2 پیکسل رندر = تحمل لبهٔ نرم


def motion_check(pen, part, rotate=None, offsets=(), steps=12, stand=None, dsf=4, min_margin=8, min_stand=10):
    """قاب حرکت (قاعدهٔ ۱۲): لایهٔ متحرک را در همهٔ وضعیت‌ها (چرخش حول rotate=(x,y) یا جابه‌جایی‌های offsets=[(dx,dy)] در
    مختصات symbol) می‌کشد و اجتماع را می‌سنجد: پیکسل بیرون از سکو، حاشیهٔ افقی، فاصله از جای فیگور."""
    import numpy as np
    A = lambda im: im[..., 3] > 128
    i, j = pen.layers[part]; body = ''.join(pen.o[i:j])
    ts = ['rotate(%s %s %s)' % (a * 360 / steps, rotate[0], rotate[1]) for a in range(steps)] if rotate else []
    ts += ['translate(%s %s)' % tuple(o) for o in offsets] or ([] if ts else ['translate(0 0)'])
    top = A(_shot(_poly(pen.padtop), dsf)); sil = top | A(_shot(_poly(_wall_pts(pen)), dsf))
    cols = sil.any(0); low = np.where(cols, sil.shape[0] - 1 - np.argmax(sil[::-1], 0), -1)
    allowed = cols[None, :] & (np.arange(sil.shape[0])[:, None] <= low[None, :])
    U = np.zeros_like(sil)
    for t in ts: U |= A(_shot('<g transform="%s">%s</g>' % (t, body), dsf))
    outside = U & ~allowed
    xs = np.where(U.any(0))[0]; px = np.where(top.any(0))[0]
    r = dict(part=part, states=len(ts), out_px=round(float(outside.sum()) / dsf ** 2, 1),
             x_margin=round(float(min(xs.min() - px.min(), px.max() - xs.max())) / dsf, 1))
    ok = r['out_px'] == 0 and r['x_margin'] >= min_margin
    if stand:
        sx, sy = (100 * K + stand[0]) * dsf, (150 * K + stand[1]) * dsf
        yy, xx = np.mgrid[0:U.shape[0], 0:U.shape[1]]
        r['stand_to_motion'] = round(float(np.hypot(xx - sx, yy - sy)[U].min()) / dsf, 1); ok = ok and r['stand_to_motion'] >= min_stand
    r['ok'] = bool(ok); return r


def width_check(pen, dsf=8, tol=.6):
    """قطر رندرشدهٔ خط‌های ثبت‌شده (probe) را روی نقشه (۰٫۷۲) می‌سنجد: از وسط خط، عمود بر آن، طول ران همرنگ.
    ok اگر |اندازه‌گیری-اسمی×۰٫۷۲| ≤ tol و ≥ ۲٫۵px. خروجی: فهرست dict."""
    import numpy as np
    # فقط _base، بدون روکش‌های lit/shade که رنگ را تغییر می‌دهند، روی زمینهٔ سفید
    im = _shot(pen.svg(), dsf, bg='#ffffff')[..., :3].astype(int)
    out = []
    for label, sw, (mx, my), (nx, ny), col in pen.probes:
        L = math.hypot(nx, ny) or 1; nx, ny = nx / L, ny / L
        tgt = np.array([int(col[i:i + 2], 16) for i in (1, 3, 5)])
        R = int(sw * 2.5 * K * dsf); run = []
        for t in range(-R, R + 1):
            x = (100 + mx) * K * dsf + nx * t; y = (150 + my) * K * dsf + ny * t
            xi, yi = int(round(x)), int(round(y))
            ok = 0 <= yi < im.shape[0] and 0 <= xi < im.shape[1] and np.abs(im[yi, xi] - tgt).max() < 28
            run.append(ok)
        c = R; best = None                       # ران شامل مرکز، یا نزدیک‌ترین ران
        runs = []; i = 0
        while i < len(run):
            if run[i]:
                j = i
                while j < len(run) and run[j]: j += 1
                runs.append((i, j)); i = j
            else: i += 1
        if runs: best = min(runs, key=lambda r: 0 if r[0] <= c < r[1] else min(abs(r[0] - c), abs(r[1] - c)))
        meas = round((best[1] - best[0]) / dsf, 2) if best else None
        exp = round(sw * K, 2)
        out.append(dict(label=label, nominal=sw, expected_px=exp, measured_px=meas,
                        ok=bool(meas is not None and abs(meas - exp) <= tol and meas >= MIN_PX)))
    return out


def finish(pen, name, stand, motion=None, out=None, shots=None, ring=(0, 0, 0), legacy_shadow=False):
    """همهٔ مراحل پایانی یک ایستگاه: symbol → سنجش حاشیه → سنجش قاب حرکت → سنجش قطر خط → spec json → شات.
    motion = {'gear': dict(rotate=(x, y))} یا {'door': dict(offsets=[(0,0),(0,-10)])}. برمی‌گرداند dict همهٔ اعداد."""
    motion = motion or {}
    sym = symbol(pen, name, list(motion), out=out, legacy_shadow=legacy_shadow)
    m = margin_check(pen, stand=stand)
    mo = [motion_check(pen, part, stand=stand, **kw) for part, kw in motion.items()]
    w = width_check(pen)
    sp = spec(name, pad_px(pen, m['bh']), stand, ['node_%s_%s' % (name, x) for x in motion], kind=pen.kind, ring=ring, out=out)
    if shots:
        from playwright.sync_api import sync_playwright
        shots = pathlib.Path(shots); shots.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as p:
            b = p.chromium.launch()
            for tag, scale in (('map', 1), ('big', 4)):
                pg = b.new_page(device_scale_factor=4 if tag == 'big' else 2, viewport={'width': 144 * (3 if tag == 'big' else 1), 'height': 160 * (3 if tag == 'big' else 1)})
                pg.set_content(('<body style="margin:0;background:#c9a35c">' + preview(sym, name, 144 * (3 if tag == 'big' else 1), tall=True)))
                pg.screenshot(path=str(shots / ('%s_%s.png' % (name, tag)))); pg.close()
            b.close()
    return dict(name=name, kind=pen.kind, margin=m, motion=mo, widths=w, spec=sp, ok=bool(m['ok'] and all(x['ok'] for x in mo) and all(x['ok'] for x in w)))
