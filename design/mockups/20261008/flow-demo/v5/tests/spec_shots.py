"""عکس از spec_sample.html در ۳۹۰ و ۳۶۰: برش‌های پیوسته در shots/spec_{w}_{n}.png؛ بدون اسکرول افقی و بدون خطای کنسول.
اجرا: python3 tests/spec_shots.py"""
import pathlib, sys
from playwright.sync_api import sync_playwright
V5 = pathlib.Path(__file__).resolve().parents[1]; OUT = V5 / 'shots'; OUT.mkdir(exist_ok=True)
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
CH = 1500; errs = []
for old in OUT.glob('spec_*.png'): old.unlink()
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
    for w in (390, 360):
        pg = b.new_page(viewport={'width': w, 'height': 800}, device_scale_factor=1)
        pg.on('console', lambda m: errs.append((w, m.text)) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append((w, str(e))))
        pg.goto('file://' + str(V5 / 'spec_sample.html')); pg.wait_for_timeout(500)
        if pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth"): errs.append((w, 'hscroll'))
        H = pg.evaluate("document.documentElement.scrollHeight")
        # عناصر تعاملی کوچک‌تر از ۴۸
        small = pg.evaluate("""[...document.querySelectorAll('.k:not(.is-disabled)')].filter(e=>{const r=e.getBoundingClientRect();return r.height<47.5||r.width<47.5}).map(e=>e.className+' '+Math.round(e.getBoundingClientRect().width)+'x'+Math.round(e.getBoundingClientRect().height))""")
        if small: errs.append((w, 'small targets', small))
        bad = pg.evaluate('''() => {
          const out = [], fam = e => getComputedStyle(e).fontFamily;
          document.querySelectorAll('.k:not(.r-btn_icon):not(.r-tile_card), h1, h2, h3, .badge, .pl, .ml, .np, .zt, .num').forEach(e => { if (!/^"?Lalezar/.test(fam(e))) out.push('not Lalezar: ' + e.className + ' ' + fam(e)); });
          document.querySelectorAll('.desc, .cap, .sheet p, .rt small, .sp, figcaption').forEach(e => { if (!/^"?Vazirmatn/.test(fam(e))) out.push('not Vazirmatn: ' + e.className + ' ' + fam(e)); });
          document.querySelectorAll('*').forEach(e => { const c = getComputedStyle(e); if (c.clipPath !== 'none') out.push('clip-path on ' + e.className);
            if (e.matches('.k, .pane, .sheet, .band, .pl, .ml, .badge, .sc, .np, .tg, .lbp, .zn, .lkb, .chk')) { const r = [c.borderTopLeftRadius, c.borderTopRightRadius, c.borderBottomLeftRadius, c.borderBottomRightRadius]; if (r.some(x => parseFloat(x) === 0) || new Set(r).size > 1) out.push('corner radii ' + r.join('/') + ' on ' + e.className); } });
          return [...new Set(out)];
        }''')
        if bad: errs.append((w, 'font/shape', bad))
        n = 0
        for y in range(0, H, CH):
            n += 1; pg.screenshot(path=str(OUT / f'spec_{w}_{n:02d}.png'), full_page=True, clip={'x': 0, 'y': y, 'width': w, 'height': min(CH, H - y)})
        print(w, 'height', H, 'slices', n)
    b.close()
print('errors:', errs or 'none')
