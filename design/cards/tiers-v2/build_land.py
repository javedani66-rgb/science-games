#!/usr/bin/env python3
"""D235: کارت‌های سه‌رنگ برای یک سرزمین از قاب سبزِ همان سرزمین (ساخته با نانوبنانا).
استفاده: python3 build_land.py sports   → out/<land>/card_<tier>.png و frame_/medal_/art
قاب باید همان چیدمان قاب دریایی را داشته باشد (۸۵۳×۱۸۴۴ پس از کوچک‌کردن). صحنه از ../lands/<land>/art_<tier>.(jpg|png|webp)؛ اگر نبود جای‌نگهدار."""
import sys, pathlib, io
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build_tiers as B
H = B.H; LAND = sys.argv[1] if len(sys.argv) > 1 else 'sports'
SRC = H.parent / 'lands' / LAND
OUT = B.OUT / LAND; OUT.mkdir(parents=True, exist_ok=True)
CARDS = {
 'sports': {
  'green':  dict(loc='ورزشگاه', title='زمین صبحگاهی', mission='توپ را به هدف بزن!', tcol='#0a3033', mcol='#193b39'),
  'orange': dict(loc='ورزشگاه', title='شب مسابقه', mission='توپ را سریع‌تر بزن!', tcol='#3a1a06', mcol='#4a2208'),
  'red':    dict(loc='ورزشگاه', title='فینال بزرگ!', mission='توپ را محکم بزن!', tcol='#3a0a0a', mcol='#4a0f10')},
}[LAND]
CX, CY, DISC = 426, 1452, 60   # مرکز مدالیون داخل قاب و شعاع دیسک رنگی

def load_frame():
    im = Image.open(SRC / 'frame-source.jpg').convert('RGBA')
    im = im.resize((853, round(im.height * 853 / im.width)), Image.LANCZOS)
    im = im.crop((0, 0, 853, 1844)); return B.clean_alpha(im)

def art_for(tier):
    for ext in ('webp', 'png', 'jpg'):
        f = SRC / f'art_{tier}.{ext}'
        if f.exists(): return Image.open(f).convert('RGB')
    col = {'green': (70, 160, 80), 'orange': (230, 140, 50), 'red': (190, 50, 50)}[tier]
    im = Image.new('RGB', (679, 696), col); d = ImageDraw.Draw(im)
    for y in range(696): d.line([(0, y), (679, y)], fill=tuple(int(c * (1 - .35 * y / 696)) for c in col))
    return im

def build():
    f0 = load_frame()
    for tier, t in B.TIERS.items():
        fr = f0 if t['hue'] is None else B.recolor(f0, t['hue'], t['v'], t['s'])
        # دیسک مدالیون: شیب رنگ سطح + نشان
        d = ImageDraw.Draw(fr); lo_, hi_ = {'green': ((8, 52, 30), (20, 110, 50)), 'orange': ((70, 26, 14), (150, 60, 18)), 'red': ((74, 12, 16), (150, 24, 28))}[tier]
        for i in range(24):
            f = i / 23; rr = DISC * (1 - f * .9); col = tuple(int(a + (b - a) * f) for a, b in zip(lo_, hi_))
            d.ellipse([CX - rr, CY - rr, CX + rr, CY + rr], fill=col + (255,))
        e = B.emblem(tier, 112); fr.alpha_composite(e, (CX - 56, CY - 56 + 2))
        fr.save(OUT / f'frame_{tier}.png')
        src = art_for(tier); w, h = 679, 696
        k = max(w / src.width, h / src.height) * 1.6
        src = src.resize((round(src.width * k), round(src.height * k)), Image.LANCZOS)
        l, tp = (src.width - w * 1.6) // 2, (src.height - h * 1.6) // 2
        src.crop((int(l), int(tp), int(l + w * 1.6), int(tp + h * 1.6))).save(OUT / f'{tier}_art.webp', 'WEBP', quality=88)

def cards():
    from playwright.sync_api import sync_playwright
    font = (B.AP / 'Lalezar.woff2').as_uri()
    with sync_playwright() as p:
        b = p.chromium.launch()
        for tier, c in CARDS.items():
            def tx(x, y, size, text, fill, stroke, sw, sh_fill, sh_sw, dx=3, dy=3):
                a = f'font-family="Lalezar" font-size="{size}" text-anchor="middle" direction="rtl" style="paint-order:stroke fill"'
                return (f'<text x="{x+dx}" y="{y+dy}" {a} fill="{sh_fill}" stroke="{sh_fill}" stroke-width="{sh_sw}">{text}</text>'
                        f'<text x="{x}" y="{y}" {a} fill="{fill}" stroke="{stroke}" stroke-width="{sw}">{text}</text>')
            svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="853" height="1844" viewBox="0 0 853 1844">
<defs><clipPath id="cl"><rect x="88" y="520" width="676" height="692" rx="30"/></clipPath></defs>
<image href="{(OUT / f'frame_{tier}.png').as_uri()}" width="853" height="1844"/>
<image href="{(OUT / f'{tier}_art.webp').as_uri()}" x="88" y="520" width="676" height="692" preserveAspectRatio="xMidYMid slice" clip-path="url(#cl)"/>
{tx(426,246,47,c['loc'],'#273333','#17292a',1.1,'#8aa0a8',2.1,2,2)}
{tx(426.5,436,76,c['title'],'#fff9e9',c['tcol'],1.7,c['tcol'],2.7)}
{tx(426,1345,57,c['mission'],c['mcol'],'#f6edda',.6,'#b9a27a',1.6,2,3)}
{tx(426,1637,58,'برگردیم به نقشه','#543016','#f9e9cb',.5,'#9e7042',1.5,2,3)}
</svg>'''
            (OUT / f'card_{tier}.html').write_text(f'<style>@font-face{{font-family:Lalezar;src:url({font})}}html,body{{margin:0;background:transparent}}</style>{svg}', encoding='utf-8')
            pg = b.new_page(viewport={'width': 853, 'height': 1844}); pg.goto((OUT / f'card_{tier}.html').as_uri()); pg.wait_for_timeout(800)
            pg.screenshot(path=str(OUT / f'card_{tier}.png'), omit_background=True); pg.close()
        b.close()
if __name__ == '__main__':
    build(); cards()
    ims = [Image.open(OUT / f'card_{t}.png').convert('RGBA') for t in ('green', 'orange', 'red')]
    sh = Image.new('RGB', (853 * 3 // 2, 922), (246, 240, 221))
    for i, im in enumerate(ims): im = im.resize((426, 922)); sh.paste(im, (i * 426, 0), im)
    sh.save(OUT / 'sheet.png'); print('ok')
