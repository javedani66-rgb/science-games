#!/usr/bin/env python3
"""آزمون سقف‌های v5/build.py (گام ۰). اجرا: python3 v5/tests/check_build.py
۱) ساخت با جاگذار می‌گذرد؛ ۲) هر سقف (SVG 40KB، بنا/b1 25KB، پوشه‌ها، صفحه 2.5MB) خطای فارسی می‌دهد؛
۳) پیشوند id و ارجاع‌ها؛ ۴) ظاهر v3 ثابت (نمونه‌برداری پیکسلی)؛ ۵) کنسول بدون خطا و رندر <use> با گرادیان."""
import sys, pathlib, tempfile, shutil, os, random, io
HERE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
import build as B
KB = 1024
fails = []
def check(name, cond, info=''):
    print(('ok   ' if cond else 'FAIL ') + name + (f'  {info}' if info and not cond else ''))
    if not cond: fails.append(name)

def svg(kb, ident='x'):
    head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g id="{ident}"><desc>'
    tail = '</desc></g></svg>'
    return (head + 'x' * (int(kb * KB) - len(head) - len(tail)) + tail).encode()
def tree(files):
    d = pathlib.Path(tempfile.mkdtemp(prefix='v5chk_'))
    for rel, data in files.items():
        p = d / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data if isinstance(data, bytes) else data.encode())
    return d
def errs(files, **kw):
    d = tree(files)
    try: return B.collect_assets(d, **kw)['errors']
    finally: shutil.rmtree(d)
def has(e, word): return any(word in x for x in e)

# ۱) جاگذار
r = B.collect_assets(HERE / 'team/assets')
check('جاگذار بدون خطا', not r['errors'], r['errors'])
check('جاگذار: ۳ نماد', sum(1 for e in r['entries'] if e['type'] == 'symbol') == 3)
# ۲) سقف SVG منفرد
check('SVG 39KB می‌گذرد', not errs({'ui/a.svg': svg(39)}))
check('SVG 41KB خطا', has(errs({'ui/a.svg': svg(41)}), 'سقف 40'))
check('بنا node_01 26KB خطا (سقف 25)', has(errs({'env/node_01.svg': svg(26)}), 'سقف 25'))
check('بنا node_01 24KB می‌گذرد', not errs({'env/node_01.svg': svg(24)}))
check('b1 26KB خطا', has(errs({'character/b1.svg': svg(26)}), 'سقف 25'))
check('نمادِ بنای درون sprite بزرگ‌تر از 25KB خطا', has(errs({'env/sprite_env.svg': '<svg xmlns="http://www.w3.org/2000/svg"><symbol id="node_01" viewBox="0 0 1 1">' + svg(26).decode().split('>', 1)[1].rsplit('</svg>', 1)[0] + '</symbol></svg>'}), 'سقف 25'))
# بودجهٔ پوشه‌ها: n فایل 30KB
for mod, cap, per in (('env', 700, 30), ('character', 300, 30), ('ui', 200, 30), ('card', 500, 30), ('light', 50, 20)):
    n = cap // per
    ok = {f'{mod}/{mod}_f{i}.svg': svg(per, f'i{i}') for i in range(n)}
    check(f'{mod} زیر بودجه {cap}KB می‌گذرد', not has(errs(ok), 'بودجه'), n * per)
    bad = dict(ok); bad[f'{mod}/{mod}_extra.svg'] = svg(per, 'e')
    if (n + 1) * per <= cap: bad[f'{mod}/{mod}_extra2.svg'] = svg(per, 'e2')
    check(f'{mod} بیش از {cap}KB خطای بودجه', has(errs(bad), f'«{mod}»'))
check('پوشهٔ scene به card شمرده می‌شود', has(errs({f'scene/sc_{i}.svg': svg(30, f'i{i}') for i in range(18)}), '«card»'))
# ۳) پیشوند id و ارجاع
d = tree({'ui/a.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 9 9"><defs><clipPath id="c"><rect width="5" height="5"/></clipPath></defs><g id="c2" clip-path="url(#c)"><use href="#c2"/></g></svg>',
          'ui/b.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 9 9"><defs><clipPath id="c"><rect width="5" height="5"/></clipPath></defs><g clip-path="url(#c)"/></svg>'})
r = B.collect_assets(d); shutil.rmtree(d)
ids = [i for e in r['entries'] for i in e['layers']]
check('id یکتا میان دو فایل با id یکسان', not r['errors'] and len(ids) == len(set(ids)) and 'a-c' in r['sprite'] and 'b-c' in r['sprite'], r['errors'])
check('url(#) و href بازنویسی شد', 'url(#a-c)' in r['sprite'] and 'href="#a-c2"' in r['sprite'] and 'url(#b-c)' in r['sprite'])
check('id پیش‌پیشوندی دوباره پیشوند نمی‌گیرد', 'ui-ui-' not in B.collect_assets(tree({'ui/sprite_ui.svg': '<svg xmlns="http://www.w3.org/2000/svg"><symbol id="ui-x" viewBox="0 0 1 1"><g id="ui-x-a"/></symbol></svg>'}))['sprite'])
check('تکرار نام نماد خطا', has(errs({'ui/a.svg': svg(1), 'env/a.svg': svg(1)}), 'تکراری'))
check('script ممنوع', has(errs({'ui/a.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><script>1</script></svg>'}), 'ممنوع'))
check('ارجاع بیرونی ممنوع', has(errs({'ui/a.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><image href="https://x.y/a.png"/></svg>'}), 'ممنوع'))
check('ارجاع بی‌مقصد خطا', has(errs({'ui/a.svg': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"><g fill="url(#nope)"/></svg>'}), 'nope'))
check('بدون viewBox/اندازه خطا', has(errs({'ui/a.svg': '<svg xmlns="http://www.w3.org/2000/svg"><g/></svg>'}), 'viewBox'))
check('اگر sprite هست فایل‌های جدا دوباره نمی‌آیند', len(B.collect_assets(tree({'ui/sprite_ui.svg': '<svg xmlns="http://www.w3.org/2000/svg"><symbol id="ui-x" viewBox="0 0 1 1"/></svg>', 'ui/x.svg': svg(1)}))['entries']) == 1)
check('tokens ادغام می‌شود', 'zone' in B.collect_assets(HERE / 'team/assets')['tokens'] or '--c-cream' in B.collect_assets(HERE / 'team/assets')['tokens'])
check('بدون tokens.css/ui_tokens.css بی‌خطا', B.collect_assets(tree({'ui/a.svg': svg(1)}))['tokens'] == '')
# ۴) سقف صفحه: همهٔ پوشه‌ها نزدیک سقف خودشان (جمع 1750KB + پایهٔ v3) باید از 2.5MB بگذرد
full = {}
for mod, cap in (('env', 700), ('character', 300), ('ui', 200), ('card', 500), ('light', 50)):
    for i in range((cap - 1) // 20): full[f'{mod}/{mod}_f{i}.svg'] = svg(20, f'i{i}')
d = tree(full); out = tempfile.mkdtemp(prefix='v5out_')
import contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf): rc = B.main(['--assets', str(d), '--out-dir', out])
check('صفحهٔ بیش از 2.5MB: build شکست می‌خورد', rc == 1 and 'حجم صفحهٔ نهایی' in buf.getvalue() and not (pathlib.Path(out) / 'index.html').exists(), buf.getvalue()[-300:])
shutil.rmtree(d)
# ۵) ساخت واقعی + مرورگر
out = tempfile.mkdtemp(prefix='v5out_')
with contextlib.redirect_stdout(io.StringIO()): rc = B.main(['--out-dir', out])
page = pathlib.Path(out) / 'index.html'
check('ساخت با جاگذار موفق و خودبسته', rc == 0 and page.exists())
txt = page.read_text(encoding='utf-8')
import re
check('خودبسته: بدون لینک خارجی', not re.search(r'(?:src|href)="https?:', txt) and 'url(svg/' not in txt)
check('assets.json نوشته شد', (pathlib.Path(out) / 'assets.json').exists())
try:
    from playwright.sync_api import sync_playwright
    exe = next(iter(sorted(pathlib.Path('/opt/pw-browsers').glob('chromium-*/chrome-linux*/chrome'))), None)
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path=str(exe) if exe else None)
        def shoot(path, w=390, h=800):
            pg = br.new_page(viewport={'width': w, 'height': h}); logs = []
            pg.on('console', lambda m: logs.append(m.text) if m.type in ('error', 'warning') else None)
            pg.on('pageerror', lambda e: logs.append(str(e)))
            pg.goto('file://' + str(path)); pg.wait_for_timeout(4000)  # بعد از ~1ث نقشه آرام می‌گیرد (اسکرول/انیمیشن)
            return pg, logs
        pg, logs = shoot(page)
        check('کنسول بدون خطا/هشدار', not logs, logs)
        pg.screenshot(path=str(pathlib.Path(out) / 'v5.png'))
        r = pg.evaluate("""()=>{const s=document.querySelector('body>svg');const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
          const d=document.createElementNS('http://www.w3.org/2000/svg','svg');d.setAttribute('width','60');d.setAttribute('height','50');d.style.cssText='position:fixed;left:0;top:0;z-index:99999';
          d.innerHTML='<use href="#ph-box"/>';document.body.appendChild(d);
          return {sym:s?s.querySelectorAll('symbol').length:-1,dups:ids.length-new Set(ids).size,hasRv:!!document.getElementById('rv'),box:d.firstChild.getBBox().width}}""")
        check('sprite در DOM با ۳ نماد', r['sym'] == 3, r); check('بدون id تکراری در DOM', r['dups'] == 0, r); check('پنل #rv هست', r['hasRv'])
        check('<use> نماد را می‌کشد', r['box'] > 50, r)
        pg.wait_for_timeout(200)
        cl = pg.screenshot(clip={'x': 0, 'y': 0, 'width': 60, 'height': 50}); 
        from PIL import Image
        im = Image.open(io.BytesIO(cl)).convert('RGB'); px = im.getpixel((30, 40))
        check('گرادیانِ داخل sprite رندر می‌شود (سبز)', px[1] > px[0] and px[1] > 90, px)
        # ظاهر v3: همان صفحه بدون sprite/tokens با v3 مقایسه می‌شود (اگر v3/index.html هست)
        # ظاهر v3: v3/build.py تازه (بدون دست‌زدن به v3/index.html قدیمی) با خروجی v5 مقایسه می‌شود
        v3dir = HERE.parent / 'v3'
        src = (v3dir / 'build.py').read_text(encoding='utf-8')
        v3out = pathlib.Path(out) / 'v3fresh.html'
        src = src.replace("(HERE / 'index.html').write_text(out, encoding='utf-8')", f"pathlib.Path({str(v3out)!r}).write_text(out, encoding='utf-8')")
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(src, str(v3dir / 'build.py'), 'exec'), {'__file__': str(v3dir / 'build.py'), '__name__': 'v3build'})
        from PIL import Image, ImageChops
        for (w, h) in ((390, 800), (360, 640)):
            ia = Image.open(io.BytesIO(shoot(v3out, w, h)[0].screenshot())).convert('RGB')
            ib = Image.open(io.BytesIO(shoot(page, w, h)[0].screenshot())).convert('RGB')
            diff = ImageChops.difference(ia, ib).getbbox()
            check(f'ظاهر {w}×{h} برابر v3 (ساخت تازه)', diff is None, diff)
        br.close()
except Exception as ex:
    check('Playwright', False, repr(ex))
shutil.rmtree(out, ignore_errors=True)
print('\nنتیجه:', 'همه گذشت' if not fails else f'{len(fails)} شکست: {fails}')
sys.exit(1 if fails else 0)
