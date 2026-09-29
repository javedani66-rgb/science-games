"""بازی را از src می‌سازد، در پوشهٔ سایت می‌گذارد و نسخهٔ sw.js را عوض می‌کند.
استفاده:  python3 tools/publish_game.py simple-machines physics/simple-machines "کارگاه ماشین‌های ساده"
"""
import sys, subprocess, pathlib, re, datetime
R=pathlib.Path(__file__).resolve().parent.parent
name,dest,title=sys.argv[1],sys.argv[2],sys.argv[3]
src=R/'src'/name
subprocess.run([sys.executable,str(src/'build.py')],check=True)
page=(src/'page.html').read_text(encoding='utf-8')
page=re.sub(r'^<title>.*?</title>\n','',page,count=1)
depth='../'*len(pathlib.PurePosixPath(dest).parts)
head=(f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
      f'<title>{title}</title><meta name="theme-color" content="#22965A"><link rel="manifest" href="{depth}manifest.webmanifest">'
      f'<link rel="icon" href="{depth}icons/icon-192.png"><link rel="apple-touch-icon" href="{depth}icons/icon-192.png">'
      f'<script>if("serviceWorker"in navigator)addEventListener("load",()=>navigator.serviceWorker.register("{depth}sw.js").catch(()=>{{}}));</script>')
out=R/dest/'index.html'; out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(head+'</head><body>'+page+'</body></html>',encoding='utf-8')
sw=R/'sw.js'; s=sw.read_text(encoding='utf-8')
s=re.sub(r"const V='[^']*';",f"const V='v-{datetime.datetime.utcnow():%Y%m%d%H%M%S}';",s)
if f"'./{dest}/'" not in s: s=s.replace("];",f",'./{dest}/'];",1)
sw.write_text(s,encoding='utf-8')
print('published',out,len(page))
