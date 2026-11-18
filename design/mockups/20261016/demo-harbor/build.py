#!/usr/bin/env python3
"""یک فایل خودبسندهٔ demo_harbor.html می‌سازد: ماکت کامل جریان (ورود ← نام ← کاراکتر ← نمای کلی ← نقشه ← صفحهٔ محیط) + بازی واقعی اسکله.
روی صفحهٔ اسکله لمس هر سه کارت (سبز/نارنجی/قرمز) بازی واقعی (src/simple-machines/page.html) را برای پایهٔ انتخابی باز می‌کند.
پیش‌نیاز: python3 ../build_all.py  و  python3 ../../../src/simple-machines/build.py   (صفحه‌ها و بازی ساخته باشند)
خروجی: ../entry-page/demo_harbor.html (گیت‌نشده نیست؛ مثل بقیهٔ صفحه‌های ساخته‌شده). ذخیرهٔ بازی زیر پیشوند smdemo: است."""
import json, base64, pathlib, re
H = pathlib.Path(__file__).resolve().parent
ROOT = H.parents[3]
E = H.parent / 'entry-page'
HOOK_OLD = "function envScene(ti){const c=envCards(envNode)[ti];"
HOOK_NEW = "function envScene(ti){if(envNode==='M07'&&window.__DEMOHARBOR){window.__DEMOHARBOR(ti);envRender();return}const c=envCards(envNode)[ti];"

def esc_js(s):   # رشتهٔ JSON امن برای داخل <script>
    return json.dumps(s, ensure_ascii=False).replace('</', '<\\/').replace('<!--', '<\\u0021--')

def page(n):
    t = (E / (n + '.html')).read_text(encoding='utf-8')
    t = re.sub(r'<link rel="prefetch"[^>]*>', '', t)
    t = re.sub(r'(?<![\w.$])(?:window\.)?location\.(href|hash|pathname)\b', r'__L.\1', t)
    if n == 'map':
        assert HOOK_OLD in t, 'envScene hook point moved'
        t = t.replace(HOOK_OLD, HOOK_NEW, 1)
    assert '<head>' in t, n
    return t

def main():
    strings = json.load(open(H / 'strings.fa.json', encoding='utf-8'))
    f = lambda p: base64.b64encode(open(ROOT / 'assets/fonts' / p, 'rb').read()).decode()
    game = (ROOT / 'src/simple-machines/page.html').read_text(encoding='utf-8')
    pages = {n: page(n) for n in ('index', 'name', 'character', 'overview', 'map', 'cardbox')}
    t = (H / 'shell.template.html').read_text(encoding='utf-8')
    rep = dict(FONT_VR=f('Vazirmatn-Regular.woff2'), FONT_VB=f('Vazirmatn-Bold.woff2'),
               STRINGS=esc_js(strings), PAGES='{' + ','.join('%s:%s' % (json.dumps(k), esc_js(v)) for k, v in pages.items()) + '}', GAME=esc_js(game))
    for k, v in rep.items():
        t = t.replace('{{%s}}' % k, v)
    out = E / 'demo_harbor.html'
    out.write_text(t, encoding='utf-8')
    print('demo_harbor.html', len(t) // 1024, 'KB')

if __name__ == '__main__':
    main()
