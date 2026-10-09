import os
KIT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
def node(x,y,state,sym,label,reason=None,here=False,guide=None,ring=False):
    xp=x/346*100
    s=f'<button class="node" data-state="{state}" style="left:{xp:.2f}%;top:{y}px" aria-label="{label}">'
    if ring: s+='<i class="node__ring"></i>'
    s+=f'<span class="node__disc"><i class="node__glyph" data-sym="{sym}"></i></span><span class="node__labels"><span class="chip chip--label">{label}</span>'
    if reason: s+=f'<span class="chip chip--lock"><i class="ic"></i>{reason}</span>'
    if here: s+='<span class="chip chip--here"><i class="ic"></i>اینجایی</span>'
    s+='</span></button>'
    if guide: s+=f'<i class="guide" data-state="{guide}" style="left:{xp:.2f}%;top:{y+6}px"></i>'
    return s
def land(key,sym,title,body='',paths=''):
    return (f'<div class="land" data-land="{key}"><div class="land__layer land__layer--back"></div><div class="land__layer land__layer--mid"></div><div class="land__layer land__layer--front"></div>'
            f'<div class="land__head"><div class="plate">{title}</div><i class="sym land__sym" data-sym="{sym}"></i></div>{paths}{body}</div>')
N1=(236,150);N2=(104,274);N3=(236,398);N4=(104,522)
def seg(a,b): return f'M{a[0]},{a[1]} C{a[0]-110 if a[0]>b[0] else a[0]+110},{a[1]+8} {b[0]+110 if a[0]>b[0] else b[0]-110},{b[1]-8} {b[0]},{b[1]}'
paths=(f'<svg class="land__path" viewBox="0 0 346 648" preserveAspectRatio="none" aria-hidden="true">'
  f'<path class="path-done" vector-effect="non-scaling-stroke" d="{seg(N1,N2)}"/><path class="path-done--top" vector-effect="non-scaling-stroke" d="{seg(N1,N2)}"/><path class="path-done--hi" vector-effect="non-scaling-stroke" d="{seg(N1,N2)}" data-footprints/>'
  f'<path class="path-todo--shade" vector-effect="non-scaling-stroke" d="{seg(N2,N3)} {seg(N3,N4)}"/><path class="path-todo" vector-effect="non-scaling-stroke" d="{seg(N2,N3)} {seg(N3,N4)}"/></svg>')
nodes=(node(*N1,'done','force','هل دادن و کشیدن')+node(*N2,'open','force','اثر نیرو',here=True,ring=True)+node(*N3,'locked','force','جهت و اندازهٔ نیرو',reason='اول: اثر نیرو')+node(*N4,'trial','force','هاکی آهنربایی')
       +f'<i class="guide" data-state="thinking" style="left:{N2[0]/346*100:.2f}%;top:{N2[1]}px"></i>')
sample=land('stadium','force','ورزشگاه',nodes,paths)
mini=''.join(f'<div class="mini">{land(k,s,t)}</div>' for k,s,t in (('stadium','force','ورزشگاه'),('space','weight','پایگاه فضایی'),('farm','energy','مزرعه و آسیاب'),('city','lever','شهر ماشین‌ها')))
SYMS=['force','friction','multi','weight','energy','machine','lever','slope','wheel','summary']
SYMN=['نیرو','اصطکاک','چند نیرو','وزن و جرم','کار و انرژی','ماشین و تعادل','اهرم','شیب و گوه','چرخ و قرقره','جمع‌بندی']
syms=''.join(f'<figure><i class="sym" data-sym="{s}" style="width:64px;height:64px"></i><figcaption>{n}</figcaption></figure>' for s,n in zip(SYMS,SYMN))
glyphs=''.join(f'<figure><span class="node__disc" style="display:block;position:relative;width:72px;height:72px;background-image:url(svg/node-open.svg)"><i class="node__glyph" data-sym="{s}"></i></span><figcaption>{n}</figcaption></figure>' for s,n in zip(SYMS,SYMN))
sw=lambda n,c,l='',d='':f'<div class="sw"><i style="background:{c}"></i><b>{n}</b><code>{c}</code></div>'
base=[('طلایی','#dbac54'),('طلایی روشن','#f6dc92'),('طلایی تیره','#a97b2c'),('کرم','#fff0c9'),('کاغذ','#f6e2b0'),('فیروزه‌ای تیره','#184441'),('فیروزه‌ای میانه','#2b6f69'),('قهوه‌ای خط','#3a2610'),('چوب','#a86f35'),('سنگ قفل','#a79c8a')]
ch=[('نیرو','#3f7fd0'),('اصطکاک','#9a6b43'),('چند نیرو','#8a5bc7'),('وزن و جرم','#17a79f'),('کار و انرژی','#efbd1f'),('ماشین و تعادل','#e0699c'),('اهرم','#4a55c4'),('شیب و گوه','#8d3562'),('چرخ و قرقره','#6a8aa5'),('جمع‌بندی','#263e6e')]
swatches=''.join(sw(n,c) for n,c in base); chs=''.join(sw(n,c) for n,c in ch)
icons=''.join(f'<figure><img src="svg/icon-{k}.svg" width="64" height="64" alt=""><figcaption>{n}</figcaption></figure>' for k,n in (('map','نقشه'),('cards','کارت‌دان'),('practice','تمرین'),('guide','راهنما'),('adults','بزرگ‌ترها'),('game','بازی'),('eye','دیده‌ای'),('box','توی جعبه'),('lock','قفل'),('arrow','فلش'),('bolt','جرقه'),('flag','پرچم'),('flask','آزمایشی')))
icons_lg=''.join(f'<figure><img src="svg/icon-{k}-lg.svg" width="120" height="120" alt=""><figcaption>{n}</figcaption></figure>' for k,n in (('map','نقشه'),('cards','کارت‌دان'),('practice','تمرین'),('guide','راهنما'),('adults','بزرگ‌ترها')))
nodes4=''.join(f'<figure><span class="node" style="position:relative;transform:none;left:auto" data-state="{s}"><span class="node__disc"><i class="node__glyph" data-sym="force"></i></span></span><figcaption>{n}</figcaption></figure>' for s,n in (('locked','قفل'),('open','تازه/باز'),('done','رفته («پس»)'),('trial','آزمایشی')))
guides=''.join(f'<figure><i class="guide guide--lg" data-state="{s}"></i><figcaption>{s}</figcaption></figure>' for s in ('thinking','happy','surprised','oops'))
def pocket(state,name,art=None,sym='force',ghost=True,game=True,reason=None):
    a=f'style="background-image:url({art})"' if art else ''
    s=f'<button class="pocket" data-state="{state}" aria-label="{name}">'
    if state in('seen','collected'):
        s+=f'<span class="pocket__art" {a}></span><span class="pocket__frame"></span><span class="pocket__title">{name}</span><i class="pocket__seal sym" data-sym="{sym}" style="width:34px;height:34px"></i>'
        s+=f'<span class="pocket__badge"></span>'
        s+=f'<span class="pocket__cap"><span class="chip chip--{"seen" if state=="seen" else "box"}"><i class="ic"></i>{"دیده‌ای" if state=="seen" else "توی جعبه"}</span></span>'
        if game: s+='<span class="pocket__game"></span>'
    elif state=='empty':
        s+=f'<span class="pocket__ghost sym" data-sym="{sym}"></span><span class="pocket__name"><span class="chip chip--tbd" style="width:100%;justify-content:center">{name}</span></span><span class="pocket__badge" style="background:var(--g-gold)"><i style="position:absolute;inset:3px;background:url(svg/badge-new.svg) center/contain no-repeat"></i></span>'
    else:
        s+=f'<span class="pocket__name"><span class="chip chip--lock" style="width:100%;justify-content:center">{reason}</span></span>'
    return s+'</button>'
HARB='img/sample-harbor.jpg'
shelf=(f'<div class="jump">'+''.join(f'<i class="sym{" is-cur" if i==0 else ""}" data-sym="{s}"></i>' for i,s in enumerate(SYMS))+'</div>'
 f'<div class="shelf"><div class="shelf__head"><i class="sym" data-sym="force"></i><span class="t-h">نیرو</span><span class="shelf__dots" aria-hidden="true"><i class="dot dot--got"></i><i class="dot dot--seen"></i><i class="dot"></i><i class="dot"></i></span></div>'
 f'<div class="shelf__row">{pocket("collected","هل دادن و کشیدن",HARB)}{pocket("seen","اثر نیرو","svg/land-stadium-mid.svg")}{pocket("empty","جهت و اندازهٔ نیرو")}{pocket("locked","نیروی تماسی",reason="اول: جهت و اندازه")}</div>'
 f'<div class="shelf__head" style="margin-top:26px"><i class="sym" data-sym="friction"></i><span class="t-h">اصطکاک</span></div><div class="shelf__row"><div class="card-back" aria-label="پشت کارت"></div>{pocket("collected","اصطکاک","svg/land-farm-mid.svg",sym="friction")}</div></div>')
phone_peek=(f'<div class="phone"><div class="map" style="height:100%;padding:0;overflow:hidden"><div style="transform:translateY(-120px);padding:20px 16px">{sample}</div></div><div class="scrim" style="position:absolute;inset:0"></div>'
 '<div class="sheet anim-sheet" style="position:absolute;inset-inline:0;bottom:0"><h3 class="t-title sheet__title" style="font-size:26px">اثر نیرو</h3><p class="sheet__sub">سالن بسکتبال</p>'
 '<div class="sheet__row"><span class="chip chip--here"><i class="ic"></i>اینجایی</span><span class="chip chip--seen"><i class="ic"></i>دیده‌ای</span></div>'
 '<button class="btn btn--primary btn--wide"><i class="ic ic-go"></i>برو داخل</button></div></div>')
phone_menu=(f'<div class="phone"><div class="map" style="height:100%;padding:0;overflow:hidden"><div style="transform:translateY(-120px);padding:20px 16px">{sample}</div></div><div class="scrim" style="position:absolute;inset:0"></div>'
 '<div class="sheet anim-sheet" style="position:absolute;inset-inline:0;bottom:0"><div class="tiles"><button class="tile tile--map"><i class="tile__ic"></i>نقشه</button><button class="tile tile--cards"><i class="tile__ic"></i>کارت‌دان</button><button class="tile tile--practice"><i class="tile__dot"></i><i class="tile__ic"></i>تمرین</button><button class="tile tile--guide"><i class="tile__ic"></i>راهنما</button></div>'
 '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:18px;gap:10px"><button class="btn btn--secondary btn--sm"><i class="ic ic-back"></i>برگرد</button><span class="adults" style="color:var(--ink);background:rgba(255,255,255,.35);border-color:rgba(58,38,16,.4)"><i class="ic"></i>ویژهٔ بزرگ‌ترها</span></div></div></div>')
fogdemo=('<div class="fogbox"><button class="node" data-state="trial" style="left:50%;top:92px"><span class="node__disc"><i class="node__glyph" data-sym="summary"></i></span></button>'
 '<i class="fog" style="left:-25%;top:30px"></i><i class="fog-sign" style="left:calc(50% + 40px);top:78px"></i>'
 '<span class="chip chip--fog" style="position:absolute;left:50%;top:176px;transform:translateX(-50%);z-index:10"><i class="ic"></i>راهی اینجاست</span></div>')
textures=('<div class="swatchrow"><figure><i style="display:block;width:96px;height:64px;background:url(svg/tile-paper.svg) 0 0/160px;border:3px solid var(--line);border-radius:10px"></i><figcaption>کاغذ</figcaption></figure>'
 '<figure><i style="display:block;width:96px;height:64px;background:url(svg/tile-teal.svg) 0 0/120px;border:3px solid var(--line);border-radius:10px"></i><figcaption>پارچهٔ فیروزه‌ای</figcaption></figure>'
 '<figure><i style="display:block;width:96px;height:64px;background:url(svg/shelf-back.svg) 0 0/240px;border:3px solid var(--line);border-radius:10px"></i><figcaption>پشت قفسه</figcaption></figure>'
 '<figure><i style="display:block;width:96px;height:28px;background:url(svg/rope-h.svg) 0 0/96px 32px"></i><figcaption>طناب</figcaption></figure>'
 '<figure><img src="svg/plate-teal.svg" width="96" alt=""><figcaption>لوحه (۹تکه)</figcaption></figure><figure><img src="svg/plate-cream.svg" width="96" alt=""><figcaption>لوحه کرم</figcaption></figure>'
 '<figure><img src="svg/rivet.svg" width="32" alt=""><figcaption>پرچ</figcaption></figure><figure><img src="svg/corner-curl.svg" width="48" alt=""><figcaption>گوشه</figcaption></figure>'
 '<figure><img src="svg/footprint.svg" width="36" alt="" style="background:#184441;border-radius:6px"><figcaption>ردپا</figcaption></figure><figure><img src="svg/badge-here.svg" width="40" alt=""><figcaption>اینجایی</figcaption></figure><figure><img src="svg/ring-here.svg" width="64" alt=""><figcaption>حلقه</figcaption></figure></div>')
HEAD='''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>برگ کیت تصویری v3</title><link rel="stylesheet" href="kit.css"><style>
body.kit{background:radial-gradient(1200px 600px at 50% -10%,#1f5a56,#0f2e2c 70%) no-repeat,#0f2e2c}
.wrap{max-width:1100px;margin:0 auto;padding:20px var(--gutter) 60px}@media(max-width:430px){.wrap{padding:12px 8px 40px}.sec{padding:10px;border-width:4px}.phone{border-width:4px}}
.hero{display:flex;align-items:center;gap:14px;margin:8px 0 18px}.hero h1{margin:0;color:var(--cream)}
.note{color:#cfe3dc;font-size:14px;margin:0 0 18px}
.sec{background:var(--tex-paper);background-size:160px;border:5px solid transparent;border-radius:var(--r-card);background-clip:padding-box;margin:0 0 22px;padding:16px;box-shadow:0 0 0 2px var(--line),0 8px 0 2px rgba(0,0,0,.35);position:relative}
.sec{background:var(--tex-paper) padding-box,var(--g-gold) border-box;background-size:160px,auto}
.sec>h2{margin:0 0 12px;font-family:var(--f-title);font-weight:400;font-size:24px;color:var(--ink)}
.sec>h2 small{font:700 14px var(--f-body);color:var(--ink-mid);margin-inline-start:8px}
.grid{display:grid;gap:14px}.g2{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}.g3{grid-template-columns:repeat(auto-fill,minmax(110px,1fr))}
figure{margin:0;text-align:center;display:flex;flex-direction:column;align-items:center;gap:4px}figcaption{font-size:14px;font-weight:700;color:var(--ink)}
.sw{display:flex;align-items:center;gap:8px;font-size:14px}.sw i{width:34px;height:34px;border-radius:9px;border:2.5px solid var(--line);box-shadow:0 2px 0 rgba(0,0,0,.3);flex:none}.sw code{direction:ltr;font-size:12px;color:#6b5a3a;margin-inline-start:auto}
.row{display:flex;flex-wrap:wrap;gap:14px;align-items:center}
.swatchrow{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end}
.phones{display:flex;flex-wrap:wrap;gap:22px;justify-content:center}
.phone{position:relative;width:390px;max-width:100%;height:640px;overflow:hidden;border-radius:30px;border:6px solid #2a1a08;box-shadow:0 14px 30px rgba(0,0,0,.45);background:#000}
.minis{display:flex;flex-wrap:wrap;gap:14px;justify-content:center}.mini{--s:.46;width:calc(358px*var(--s));height:calc(660px*var(--s));position:relative;overflow:hidden}.mini .land{position:absolute;left:0;top:0;transform:scale(var(--s));transform-origin:0 0;margin:0;max-width:none;width:358px}
@media(min-width:900px){.mini{--s:.62}}
.fogbox{position:relative;width:100%;max-width:358px;height:230px;margin:0 auto;border-radius:18px;overflow:hidden;background:var(--parchment) url(svg/map-bg.svg) 0 0/100% auto;border:3px solid var(--line)}
.fogbox .node{--node:80px}
.sampleframe{max-width:390px;margin:0 auto}
.dark{background:var(--ink-deep);border-radius:14px;padding:14px}
.dark .t-title,.dark .t-h{color:var(--cream)}
@media(min-width:900px){.cols{display:grid;grid-template-columns:1fr 1fr;gap:22px;align-items:start}}
</style></head><body class="kit"><div class="wrap">'''
def sec(t,sub,body): return f'<section class="sec"><h2>{t}<small>{sub}</small></h2>{body}</section>'
body=HEAD+'<div class="hero"><i class="guide guide--lg" data-state="happy" style="width:70px;height:82px"></i><h1 class="t-title t-title--cream" style="font-size:34px">برگ کیت تصویری v3</h1></div><p class="note">پیشنهاد (نه تصمیم). متن‌های این برگ فقط جاگذارند و در محصول از strings می‌آیند. هنوز با هیچ کودکی آزموده نشده (B9).</p>'
body+=sec('توکن‌های رنگ','پایه و ۱۰ رنگ فصل (بیرون از سبز/نارنجی/قرمز سختی)',f'<div class="cols"><div class="grid" style="grid-template-columns:1fr 1fr">{swatches}</div><div class="grid" style="grid-template-columns:1fr 1fr">{chs}</div></div>')
body+=sec('تایپ','لالهزار برای تیتر، وزیرمتن برای متن','<div class="t-title">تیتر بزرگ: کارگاه ماشین‌های ساده</div><div class="t-h">تیتر قفسه یا بخش</div><div class="t-label">برچسب مهم، ۱۸ بولد</div><div class="t-body">متن توضیح ۱۶ پیکسل با فاصلهٔ خط ۱٫۷ برای خواندن راحت.</div><div class="t-small">کوچک‌ترین متن مجاز: ۱۴ پیکسل</div>')
body+=sec('دکمه‌ها','اصلی / ثانویه / آیکونی / فشرده','<div class="row"><button class="btn btn--primary"><i class="ic ic-go"></i>برو داخل</button><button class="btn btn--primary is-pressed">فشرده</button><button class="btn btn--secondary"><i class="ic ic-back"></i>برگرد</button><button class="btn btn--secondary is-pressed">فشرده</button><button class="btn btn--icon" aria-label="منو"><i class="ic ic-map"></i></button><button class="btn btn--icon is-pressed" aria-label="فشرده"><i class="ic ic-cards"></i></button><button class="btn btn--primary" disabled>غیرفعال</button></div>')
body+=sec('چسبک‌ها','نام گره، اینجایی، قفل با دلیل، تازه، دیده، جعبه، آزمایشی، مه، موقت','<div class="row"><span class="chip chip--label">هل دادن و کشیدن</span><span class="chip chip--here"><i class="ic"></i>اینجایی</span><span class="chip chip--lock"><i class="ic"></i>اول: اثر نیرو</span><span class="chip chip--new"><i class="ic"></i>تازه</span><span class="chip chip--seen"><i class="ic"></i>دیده‌ای</span><span class="chip chip--box"><i class="ic"></i>توی جعبه</span><span class="chip chip--trial"><i class="ic"></i>آزمایشی</span><span class="chip chip--fog"><i class="ic"></i>راهی اینجاست</span><span style="display:inline-block;background:var(--ink-deep);padding:8px 10px;border-radius:12px"><span class="chip chip--tbd">موقت</span></span></div>')
body+=sec('کاشی منو و برگهٔ پایین','peek و منو؛ بزرگ‌ترها جدا از شبکه',f'<div class="phones">{phone_peek}{phone_menu}</div>')
body+=sec('نمونهٔ قاب زمین','ورزشگاه: ۴ گره (طی‌شده، اینجایی با راهنما، قفل با دلیل، آزمایشی) و مسیر',f'<div class="map sampleframe" style="border-radius:20px;padding:20px 16px 8px">{sample}</div>')
body+=sec('۴ زمین','هر کدام ۳ لایهٔ جدا (عقب/میان/جلو)، پوست تنها',f'<div class="minis">{mini}</div>')
body+=sec('قفسهٔ کارت','خالی، دیده، جمع‌شده، قفل؛ نوار پرش فصل؛ پشت کارت',f'<div class="phones"><div class="phone" style="overflow:auto;height:720px;background:#2a1a08">{shelf}</div></div>')
body+=sec('نماد فصل‌ها','۱۰ مدال (روی قفسه/نوار پرش) و ۱۰ نشانهٔ داخل گره',f'<div class="grid g3">{syms}</div><hr style="border:0;border-top:2px dashed rgba(58,38,16,.3);margin:14px 0"><div class="grid g3">{glyphs}</div>')
body+=sec('آیکون‌ها','کوچک ۹۶ و بزرگ ۱۶۰ (با مدال)',f'<div class="grid g3">{icons}</div><hr style="border:0;border-top:2px dashed rgba(58,38,16,.3);margin:14px 0"><div class="grid g3">{icons_lg}</div>')
body+=sec('گره‌ها و راهنما','۴ حالت گره؛ راهنما ۴ حالت',f'<div class="grid g3">{nodes4}</div><hr style="border:0;border-top:2px dashed rgba(58,38,16,.3);margin:14px 0"><div class="row" style="justify-content:space-around">{guides}</div>')
body+=sec('مه و تابلو','فقط برای مسیر پنهانِ کشف‌نشده؛ بدون تابلو هیچ مه‌ای نیست',fogdemo)
body+=sec('تکه‌ها و بافت‌ها','ابزار ساخت',textures)
body+='</div><script src="kit.js"></script></body></html>'
# mini scaling
open(os.path.join(KIT,'index.html'),'w').write(body)
print('index ok',len(body))

# ---------- phone.html : three exact 390x800 screens ----------
def topbar(title,btn='menu'):
    return f'<div class="topbar"><button class="btn btn--icon" aria-label="منو"><i class="ic ic-{btn}"></i></button><span class="t-title">{title}</span><span class="spacer"></span></div>'
mapscreen=(f'<div class="screen" id="s-map">{topbar("نقشهٔ علوم")}<div class="map" style="height:736px;overflow:hidden;padding-top:22px">{sample}</div></div>')
menuscreen=(f'<div class="screen" id="s-menu">{topbar("نقشهٔ علوم")}<div class="map" style="height:736px;overflow:hidden;padding-top:22px">{sample}</div><div class="scrim" style="position:absolute;inset:0;z-index:40"></div>'
 '<div class="sheet anim-sheet" style="position:absolute;z-index:41;inset-inline:0;bottom:0"><div class="tiles"><button class="tile tile--map"><i class="tile__ic"></i>نقشه</button><button class="tile tile--cards"><i class="tile__ic"></i>کارت‌دان</button><button class="tile tile--practice"><i class="tile__dot"></i><i class="tile__ic"></i>تمرین</button><button class="tile tile--guide"><i class="tile__ic"></i>راهنما</button></div>'
 '<div style="display:flex;justify-content:space-between;align-items:center;margin-top:18px;gap:10px"><button class="btn btn--secondary btn--sm"><i class="ic ic-back"></i>برگرد</button><span class="adults" style="color:var(--ink);background:rgba(255,255,255,.35);border-color:rgba(58,38,16,.4)"><i class="ic"></i>ویژهٔ بزرگ‌ترها</span></div></div></div>')
cardscreen=f'<div class="screen" id="s-cards" style="background:#2a1a08">{topbar("کارت‌دان","map")}<div style="height:736px;overflow:auto">{shelf}</div></div>'
PH=HEAD.replace('<title>برگ کیت تصویری v3</title>','<title>صفحه‌های نمونه ۳۹۰×۸۰۰</title>').replace('.wrap{max-width:1100px;','.wrap{max-width:none;padding:0!important;')
open(os.path.join(KIT,'phone.html'),'w').write(PH+'<div style="display:flex;flex-wrap:wrap;gap:0;justify-content:center">'+mapscreen+menuscreen+cardscreen+'</div></div><script src="kit.js"></script></body></html>')
print('phone ok')

# ---------- guide.html ----------
cands=''.join(f'<figure><img src="img/cand/b{i}_happy.webp" width="96" height="96" alt="" style="{"outline:4px solid var(--gold);outline-offset:2px;border-radius:50%;background:var(--paper)" if i==1 else "background:var(--paper);border-radius:50%"}"><figcaption>b{i}{" (انتخاب)" if i==1 else ""}</figcaption></figure>' for i in range(1,9))
G=HEAD.replace('<title>برگ کیت تصویری v3</title>','<title>شخصیت راهنما</title>')
G+='<div class="hero"><i class="guide guide--lg" data-state="happy" style="width:70px;height:82px"></i><h1 class="t-title t-title--cream" style="font-size:32px">شخصیت راهنما: b1</h1></div>'
G+=sec('چهار حالت','نشانگر گرد با دم کوچک؛ سر از لبهٔ گرد بیرون می‌زند. هر فایل مستقل است (عکس داخل SVG گذاشته شده).',f'<div class="row" style="justify-content:space-around">{guides}</div>')
G+=sec('روی گره','اندازهٔ واقعی (۶۲×۷۲) و دو برابر؛ دم نشانگر روی لبهٔ بالای گره می‌نشیند',
 '<div class="row" style="justify-content:space-around;align-items:flex-end">'
 '<div style="position:relative;width:120px;height:150px"><span class="node" data-state="open" style="left:60px;top:90px"><span class="node__disc"><i class="node__glyph" data-sym="force"></i></span></span><i class="guide" data-state="thinking" style="left:60px;top:90px"></i></div>'
 '<div style="position:relative;width:240px;height:300px"><span class="node" data-state="done" style="--node:176px;left:120px;top:180px"><span class="node__disc"><i class="node__glyph" data-sym="force"></i></span></span><i class="guide" data-state="happy" style="left:120px;top:180px;width:124px;height:144px;margin-top:-44px"></i></div></div>')
G+=sec('چرا b1','انتخاب من، نه تصمیم؛ نام و نقش راهنما هنوز باز است (پرسش ۲ مشخصات)',
 f'<div class="row" style="margin-bottom:12px;justify-content:space-around">{cands}</div>'
 '<ul class="t-body" style="margin:0;padding-inline-start:22px"><li>کلاه ایمنی زرد یعنی «کارگاه و ساختن»: با موضوع ماشین‌های ساده می‌خواند و آیکون «راهنما» در منو هم همین کلاه است.</li>'
 '<li>زرد پررنگ‌ترین لکهٔ رنگ بین هشت شخصیت است و روی هر چهار زمینه (کرم، شب، هلویی، آبی‌خاکستری) در دید اول از زمینه جدا می‌ماند. این را با چشم خودم دیده‌ام، نه با آزمون کودک.</li>'
 '<li>چهار ژست لازم را دارد: thinking، happy، surprised، oops. هشت‌تای b* همه‌شان این‌ها را دارند.</li>'
 '<li>از آثار موجود پروژه است؛ شخصیت شناخته‌شده یا لوگوی کسی نیست.</li></ul>'
 '<p class="t-small" style="margin:12px 0 0"><b>محدودیت‌ها (صادقانه):</b> عکس‌ها فقط سر و شانه‌اند، ۱۶۰×۱۶۰ (نه تمام‌قد). ایستادن، راه‌رفتن و چرخیدن واقعی ممکن نیست؛ «راه رفتن روی خط» فقط با جابه‌جایی نشانگر (پرش کوتاه) نشان داده می‌شود. بالاتر از حدود ۱۲۰px نرم می‌شود (در بوم ۲× هم‌اکنون دیده می‌شود). اگر مالک «ژست ایستاده/راه‌رفتن» بخواهد، باید تصویر تازه ساخته شود (خارج از این کیت). دربارهٔ دوست‌داشتنی بودنِ این شخصیت هیچ ادعایی نمی‌شود (B9).</p>')
G+='</div><script src="kit.js"></script></body></html>'
open(os.path.join(KIT,'guide.html'),'w').write(G)
print('guide page ok')
