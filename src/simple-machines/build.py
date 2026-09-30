import base64, pathlib, sys
D = pathlib.Path(__file__).parent
FONTS = D.parent.parent/'assets'/'fonts'
css = (D/'style.css').read_text(encoding='utf-8')
for k, f in [('__VAZ_R__','Vazirmatn-Regular.woff2'),('__VAZ_B__','Vazirmatn-Bold.woff2'),('__LALE__','Lalezar-Regular.woff2')]:
    css = css.replace(k, base64.b64encode((FONTS/f).read_bytes()).decode())
js = "\n".join((D/n).read_text(encoding='utf-8') for n in ['core.js','voice.js','st_force.js','st_scale.js','st_lever.js','st_ramp.js','st_pulley.js','st_wheel.js','st_wedge.js','st_sort.js','content.js','quiz.js','assets.js','app.js','journey.js'])
page = f'<title>کارگاه ماشین‌های ساده</title>\n<style>\n{css}\n</style>\n<div class="wrap" id="app"></div>\n<script>\n(function(){{\n{js}\n}})();\n</script>\n'
(D/'page.html').write_text(page, encoding='utf-8')
(D/'preview.html').write_text('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'+page+'</body></html>', encoding='utf-8')
(D/'test.html').write_text('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><script>window.__TEST=1</script>'+page+'</body></html>', encoding='utf-8')
(D/'jtest.html').write_text('<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body><script>window.__JT=1</script>'+page+'</body></html>', encoding='utf-8')
(D/'all.js').write_text(js, encoding='utf-8')
print(len(page))
