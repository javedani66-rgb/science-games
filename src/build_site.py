import pathlib, base64, json, shutil
from PIL import Image, ImageDraw
R=pathlib.Path(__file__).parent; S=R/'site'; V=R/'v3'
if S.exists(): shutil.rmtree(S)
(S/'physics/simple-machines').mkdir(parents=True); (S/'icons').mkdir(); (S/'assets/fonts').mkdir(parents=True)
for f in ['Vazirmatn-Regular.woff2','Vazirmatn-Bold.woff2','Lalezar-Regular.woff2']: shutil.copy(V/f,S/'assets/fonts'/f)
VER='sm-2026-09-29'
# icons: simple lever glyph
for n in (192,512):
    im=Image.new('RGB',(n,n),'#22965A'); d=ImageDraw.Draw(im); k=n/192
    d.polygon([(96*k,110*k),(70*k,150*k),(122*k,150*k)],fill='#FFC43D')
    d.line([(30*k,120*k),(162*k,82*k)],fill='#FFFFFF',width=int(12*k))
    d.rounded_rectangle([(24*k,86*k),(58*k,114*k)],radius=int(5*k),fill='#E8590C')
    im.save(S/f'icons/icon-{n}.png')
man={"name":"بازی‌های علوم","short_name":"علوم","lang":"fa","dir":"rtl","start_url":"./","scope":"./","display":"standalone","background_color":"#EDF4F7","theme_color":"#22965A",
     "icons":[{"src":"icons/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icons/icon-512.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}]}
(S/'manifest.webmanifest').write_text(json.dumps(man,ensure_ascii=False,indent=1),encoding='utf-8')
(S/'sw.js').write_text(f"""// نسخه را با هر انتشار عوض کنید تا فایل‌های تازه گرفته شوند
const V='{VER}';
const FILES=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./assets/fonts/Vazirmatn-Regular.woff2','./assets/fonts/Vazirmatn-Bold.woff2','./assets/fonts/Lalezar-Regular.woff2','./physics/simple-machines/'];
self.addEventListener('install',e=>{{self.skipWaiting();e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)));}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));}});
// اول از شبکه، اگر نبود از حافظه؛ پس بی‌اینترنت هم باز می‌شود
self.addEventListener('fetch',e=>{{if(e.request.method!=='GET')return;e.respondWith(fetch(e.request).then(r=>{{const cp=r.clone();caches.open(V).then(c=>c.put(e.request,cp));return r;}}).catch(()=>caches.match(e.request,{{ignoreSearch:true}})));}});
""",encoding='utf-8')
REG=lambda rel:f'<script>if("serviceWorker"in navigator)addEventListener("load",()=>navigator.serviceWorker.register("{rel}sw.js").catch(()=>{{}}));</script>'
HEAD=lambda title,rel:f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{title}</title><meta name="theme-color" content="#22965A"><link rel="manifest" href="{rel}manifest.webmanifest"><link rel="icon" href="{rel}icons/icon-192.png"><link rel="apple-touch-icon" href="{rel}icons/icon-192.png">'
page=(V/'page.html').read_text(encoding='utf-8').replace('<title>کارگاه ماشین‌های ساده</title>\n','',1)
(S/'physics/simple-machines/index.html').write_text(HEAD('کارگاه ماشین‌های ساده','../../')+REG('../../')+'</head><body>'+page+'</body></html>',encoding='utf-8')
GAMES=[("فیزیک","ماشین‌های ساده","اهرم، سطح شیب‌دار، قرقره، چرخ و محور، گوه و پیچ؛ و نیرو، جرم و وزن. پایهٔ دوم تا ششم.","physics/simple-machines/","#22965A",True),
       ("فیزیک","به‌زودی","بخش‌های دیگر فیزیک","", "#3B6FD4",False),
       ("شیمی","به‌زودی","","", "#E8590C",False),
       ("زیست","به‌زودی","","", "#7A3FC8",False)]
cards="".join(f'''<{"a" if on else "div"} class="card{"" if on else " off"}" {f'href="{href}"' if on else 'aria-disabled="true"'} style="--c:{c}"><span class="sub">{sub}</span><span class="t">{t}</span>{f'<span class="d">{d}</span>' if d else ""}{'<span class="go">بازی کن ←</span>' if on else ""}</{"a" if on else "div"}>''' for sub,t,d,href,c,on in GAMES)
(S/'index.html').write_text(HEAD('بازی‌های علوم','./')+REG('./')+'''<style>
@font-face{font-family:"VazirLocal";src:url(assets/fonts/Vazirmatn-Regular.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"VazirLocal";src:url(assets/fonts/Vazirmatn-Bold.woff2) format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"LalezarLocal";src:url(assets/fonts/Lalezar-Regular.woff2) format("woff2");font-display:swap}
:root{--page:#EDF4F7;--ink:#1B2A41;--muted:#56677F;--line:#D4E1E9}
*{box-sizing:border-box}body{margin:0;background:var(--page);color:var(--ink);font-family:"VazirLocal",Tahoma,sans-serif;line-height:1.8;padding-inline:16px;padding-block:24px 48px}
main{max-width:720px;margin-inline:auto;display:flex;flex-direction:column;gap:20px}
h1{font-family:"LalezarLocal","VazirLocal",Tahoma,sans-serif;font-weight:400;font-size:40px;line-height:1.3;margin:0}
p{margin:0;color:var(--muted);font-size:17px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}
.card{display:flex;flex-direction:column;gap:4px;background:#fff;border-radius:20px;padding:18px;text-decoration:none;color:var(--ink);box-shadow:inset 0 0 0 2px var(--line);border-top:8px solid var(--c)}
a.card:hover,a.card:focus-visible{box-shadow:inset 0 0 0 3px var(--c);outline:none}
.card .sub{font-size:14px;font-weight:700;color:var(--c)}.card .t{font-family:"LalezarLocal","VazirLocal",Tahoma,sans-serif;font-size:28px;line-height:1.3}
.card .d{font-size:15px;color:var(--muted);line-height:1.7}.card .go{margin-top:8px;font-weight:700;color:var(--c)}
.card.off{opacity:.55}
.note{font-size:14px}
</style></head><body><main><h1>بازی‌های علوم</h1><p>بازی‌های کلاس علوم برای دبستان. پیشرفت هر بچه روی همان گوشی یا رایانه ذخیره می‌شود. بعد از یک بار باز کردن، بدون اینترنت هم کار می‌کند.</p>
<div class="grid">'''+cards+'''</div>
<p class="note">روی گوشی: از منوی مرورگر «افزودن به صفحهٔ اصلی» یا «نصب برنامه» را بزنید تا مثل یک برنامه باز شود.</p></main></body></html>''',encoding='utf-8')
(S/'.nojekyll').write_text('')
(S/'README.md').write_text('''# بازی‌های علوم

سایت ایستا برای GitHub Pages.

- `index.html`: صفحهٔ اصلی و فهرست بازی‌ها
- `physics/simple-machines/`: بازی ماشین‌های ساده (یک فایل کامل)
- `chemistry/...`، `biology/...`: بازی‌های بعدی، هر کدام در پوشهٔ خودش
- `sw.js`: برای کار بدون اینترنت؛ با هر انتشار مقدار `V` را عوض کنید و مسیر بازی تازه را به `FILES` اضافه کنید
- `assets/fonts/`: فونت‌های مشترک

همهٔ بازی‌ها روی یک نشانی‌اند، پس بعداً می‌توانند پروفایل مشترک بچه را از localStorage بخوانند. کلید هر بازی جداست (مثلاً `sm-journey-v1`).
''',encoding='utf-8')
print('ok')
