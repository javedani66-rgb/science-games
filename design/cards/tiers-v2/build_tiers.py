#!/usr/bin/env python3
"""D223: کارت‌های سه‌رنگ چالش از یک قاب (قاب سبز تأییدشدهٔ harbor-v1) + تصویر صحنهٔ هر چالش.
قاب: پس‌زمینهٔ سفید حذف (شفاف با لبهٔ نرم)، فقط سبزِ قاب به نارنجی/قرمز می‌چرخد؛ طلا و طناب و سرمه‌ای دست‌نخورده.
نشان سختی: سبز نهال (اصل)، نارنجی شعله، قرمز آذرخش‌پنجه (اژدر). خروجی: out/card_<tier>.png (۸۵۳×۱۸۴۴، شفاف) + out/<tier>_art.webp.
متن‌ها موقت‌اند (draft) و باید به strings.fa.json بروند."""
import io, json, math, pathlib, sys
from PIL import Image, ImageDraw, ImageFilter
import numpy as np, colorsys
H = pathlib.Path(__file__).resolve().parent
AP = H.parent / 'approved/harbor-v1/assets'
OUT = H / 'out'; OUT.mkdir(exist_ok=True)

def clean_alpha(im):
    im = im.convert('RGBA')
    w, h = im.size
    seeds = [(x, y) for x in range(0, w, 12) for y in (0, h - 1)] + [(x, y) for y in range(0, h, 12) for x in (0, w - 1)]
    for p in seeds:
        px = im.getpixel(p)
        if px[3] and min(px[:3]) > 200: ImageDraw.floodfill(im, p, (255, 255, 255, 0), thresh=150)
    # سوراخ‌های سفید محصور (مثل زیر نشان لنگر، میان طناب‌ها) که از بیرون نمی‌رسند
    arr = np.asarray(im).astype(int); mx = arr[..., :3].max(-1); mn = arr[..., :3].min(-1)
    cand = (mn > 238) & ((mx - mn) < 14) & (arr[..., 3] > 0)
    from scipy import ndimage
    lab, n = ndimage.label(cand); sz = ndimage.sum(cand, lab, range(1, n + 1)); ys = ndimage.center_of_mass(cand, lab, range(1, n + 1))
    A = np.asarray(im.getchannel('A')).copy()
    for i in range(n):
        if 300 < sz[i] < 6000 and ys[i][0] < 300: A[lab == i + 1] = 0
    im.putalpha(Image.fromarray(A.astype(np.uint8)))
    a = im.getchannel('A'); hole = a.point(lambda v: 255 if v == 0 else 0)
    hole = hole.filter(ImageFilter.MaxFilter(5)).filter(ImageFilter.GaussianBlur(1.0))
    im.putalpha(hole.point(lambda v: 255 - v)); return im

def recolor(im, hue_to, vmul=1.0, smul=1.0, lo=60, hi=175):
    a = np.asarray(im.convert('RGBA')).astype(np.float32) / 255
    r, g, b, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    mx, mn = a[..., :3].max(-1), a[..., :3].min(-1); d = mx - mn + 1e-6
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = d / (mx + 1e-6); v = mx
    m = (hue >= lo) & (hue <= hi) & (s > .28)
    nh = np.where(m, hue_to, hue); ns = np.clip(np.where(m, s * smul, s), 0, 1); nv = np.clip(np.where(m, v * vmul, v), 0, 1)
    c = nv * ns; hp = (nh % 360) / 60; x = c * (1 - np.abs(hp % 2 - 1)); m0 = nv - c
    z = np.zeros_like(c)
    sel = [(c, x, z), (x, c, z), (z, c, x), (z, x, c), (x, z, c), (c, z, x)]
    out = np.zeros(a.shape[:2] + (3,), np.float32); hi_ = np.floor(hp).astype(int) % 6
    for k, (R, G, B) in enumerate(sel):
        mk = hi_ == k; out[..., 0][mk] = (R + m0)[mk]; out[..., 1][mk] = (G + m0)[mk]; out[..., 2][mk] = (B + m0)[mk]
    res = np.dstack([out, al]); return Image.fromarray((res * 255).astype(np.uint8), 'RGBA')

TIERS = {
 'green':  dict(hue=None),
 'orange': dict(hue=26, v=1.28, s=1.05, glow=(255, 160, 40)),
 'red':    dict(hue=358, v=1.12, s=1.0, glow=(255, 70, 50)),
}
def chaikin(pts, n=2, closed=True):
    for _ in range(n):
        out = []
        m = len(pts)
        for k in range(m if closed else m - 1):
            p, q = pts[k], pts[(k + 1) % m]
            out += [(.75 * p[0] + .25 * q[0], .75 * p[1] + .25 * q[1]), (.25 * p[0] + .75 * q[0], .25 * p[1] + .75 * q[1])]
        pts = out
    return pts

def emblem(kind, size=360):
    """نماد سختی با همان زبان کارت: شکل نرم، خط دور تیرهٔ ضخیم، یک رنگ روشن و یک سایه."""
    S = 4; im = Image.new('RGBA', (size * S, size * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size * S / 2; k = size / 360 * 1.0
    def P(pts): return [(c + x * k * S, c + y * k * S) for x, y in pts]
    def shape(pts, fill, ol, w=7, sm=2):
        pp = P(chaikin(pts, sm)) if sm else P(pts)
        d.polygon(pp, fill=fill); d.line(pp + [pp[0]], fill=ol, width=int(w * k * S), joint='curve')
    if kind == 'green':
        ol = (14, 56, 26, 255)
        shape([(-14,86),(-16,-4),(14,-4),(16,86)], (110,190,55,255), ol, 6, 0)
        shape([(-10,-2),(-34,22),(-78,18),(-100,-18),(-86,-62),(-44,-52)], (130,214,64,255), ol)
        shape([(12,-14),(40,10),(92,-4),(108,-46),(86,-96),(36,-80)], (168,238,92,255), ol)
        d.line(P([(-20,8),(-72,-14)]), fill=(66,150,40,255), width=int(5 * k * S)); d.line(P([(22,-4),(78,-48)]), fill=(80,170,44,255), width=int(5 * k * S))
        shape([(-64,98),(-30,82),(0,78),(30,82),(64,98),(36,112),(0,116),(-36,112)], (126,76,34,255), (52,28,10,255))
    elif kind == 'orange':
        ol = (84, 30, 6, 255)
        shape([(0,-112),(40,-62),(70,-24),(76,30),(54,82),(0,104),(-54,82),(-76,30),(-64,-14),(-36,-40),(-24,-6),(-6,-52)], (255,150,34,255), ol)
        shape([(4,-40),(30,0),(40,40),(22,76),(0,86),(-22,76),(-34,40),(-18,8),(-8,-18)], (255,208,72,255), ol, 5)
        shape([(0,28),(14,52),(8,72),(0,76),(-8,72),(-14,52)], (255,246,206,255), (255,246,206,255), 1)
    else:
        ol = (80, 8, 10, 255)
        shape([(-84,86),(-98,-44),(-56,-6),(-36,-100),(-10,-24),(0,-116),(10,-24),(36,-100),(56,-6),(98,-44),(84,86),(0,64)], (255,88,70,255), ol, 7, 1)
        shape([(-48,70),(-56,-8),(-30,22),(-16,-50),(0,12),(16,-50),(30,22),(56,-8),(48,70),(0,54)], (255,172,134,255), ol, 5, 1)
    return im.resize((size, size), Image.LANCZOS)

def medallion(tier):
    base = Image.open(AP / 'core-difficulty-medallion.png').convert('RGBA')
    t = TIERS[tier]; m = base.copy() if tier == 'green' else recolor(base, t['hue'], t['v'], t['s'], lo=40, hi=175)
    size = base.width; cx = cy = size / 2
    # دیسک داخلی: بازنقاشی با شیب رنگ سطح تا نهال پنهان شود
    inner = Image.new('RGBA', base.size, (0, 0, 0, 0)); dd = ImageDraw.Draw(inner)
    R = size * .335
    for i in range(24):
        f = i / 23; rr = R * (1 - f * .9)
        lo_, hi_ = {'green': ((8, 52, 30), (20, 110, 50)), 'orange': ((70, 26, 14), (150, 60, 18)), 'red': ((74, 12, 16), (150, 24, 28))}[tier]
        col = tuple(int(a + (b - a) * f) for a, b in zip(lo_, hi_))
        dd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col + (255,))
    m.alpha_composite(inner)
    e = emblem(tier, int(size * .74)); m.alpha_composite(e, (int(cx - e.width / 2), int(cy - e.height / 2 + 2)))
    return m

CARDS = {
 'green':  dict(loc='بندر', title='اسکلهٔ ماهیگیری', mission='تور را با طناب بکش بالا!', art=AP / 'fishing-dock-art.jpg', tcol='#0a3033', mcol='#193b39'),
 'orange': dict(loc='بندر', title='اسکلهٔ دزدان دریایی', mission='بار را بکش بالا!', art=pathlib.Path('/tmp/orange.jpg'), tcol='#3a1a06', mcol='#4a2208'),
 'red':    dict(loc='بندر', title='شکار اژدر!', mission='اژدها را بکش بالا!', art=pathlib.Path('/tmp/red.jpg'), tcol='#3a0a0a', mcol='#4a0f10'),
}
def build_assets():
    frame0 = clean_alpha(Image.open(AP / 'card-frame-base.png'))
    for tier, t in TIERS.items():
        fr = frame0 if t['hue'] is None else recolor(frame0, t['hue'], t['v'], t['s'])
        fr.save(OUT / f'frame_{tier}.png'); medallion(tier).save(OUT / f'medal_{tier}.png')
        src = Image.open(CARDS[tier]['art']).convert('RGB'); w, h = 679, 696
        k = max(w / src.width, h / src.height) * 1.6
        src = src.resize((round(src.width * k), round(src.height * k)), Image.LANCZOS)
        l, tp = (src.width - w * 1.6) // 2, (src.height - h * 1.6) // 2
        src = src.crop((int(l), int(tp), int(l + w * 1.6), int(tp + h * 1.6)))
        src.save(OUT / f'{tier}_art.webp', 'WEBP', quality=88)

def build_cards():
    from playwright.sync_api import sync_playwright
    font = (AP / 'Lalezar.woff2').as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for tier, c in CARDS.items():
            def tx(id_, x, y, size, text, fill, stroke, sw, sh_fill, sh_sw, dx=3, dy=3, sy=0):
                return (f'<text x="{x+dx}" y="{y+dy}" font-family="Lalezar" font-size="{size}" text-anchor="middle" direction="rtl" style="paint-order:stroke fill" fill="{sh_fill}" stroke="{sh_fill}" stroke-width="{sh_sw}">{text}</text>'
                        f'<text x="{x}" y="{y}" font-family="Lalezar" font-size="{size}" text-anchor="middle" direction="rtl" style="paint-order:stroke fill" fill="{fill}" stroke="{stroke}" stroke-width="{sw}">{text}</text>')
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="853" height="1844" viewBox="0 0 853 1844">
<defs><clipPath id="cl"><rect x="86" y="518" width="679" height="696" rx="34"/></clipPath></defs>
<image href="{(OUT / f'frame_{tier}.png').as_uri()}" x="0" y="0" width="853" height="1844"/>
<image href="{(OUT / f'{tier}_art.webp').as_uri()}" x="86" y="518" width="679" height="696" preserveAspectRatio="xMidYMid slice" clip-path="url(#cl)"/>
{tx('l',426,240,47,c['loc'],'#273333','#17292a',1.1,'#265c66',2.1,2,2)}
{tx('t',426.5,436,76,c['title'],'#fff9e9',c['tcol'],1.7,c['tcol'],2.7)}
{tx('m',426,1329,57,c['mission'],c['mcol'],'#f6edda',.6,'#b9a27a',1.6,2,3)}
<image href="{(OUT / f'medal_{tier}.png').as_uri()}" x="337" y="1359" width="180" height="180"/>
{tx('r',426,1637,58,'برگردیم به نقشه','#543016','#f9e9cb',.5,'#9e7042',1.5,2,3)}
</svg>'''
            html = f'<style>@font-face{{font-family:Lalezar;src:url({font})}}html,body{{margin:0;background:transparent}}</style>{svg}'
            (OUT / f'card_{tier}.html').write_text(html, encoding='utf-8')
            pg = b.new_page(viewport={'width': 853, 'height': 1844}); pg.goto((OUT / f'card_{tier}.html').as_uri()); pg.wait_for_timeout(800)
            pg.screenshot(path=str(OUT / f'card_{tier}.png'), omit_background=True); pg.close()
        b.close()
if __name__ == '__main__':
    build_assets(); build_cards(); print('ok')
