import base64,io,pathlib,math
from PIL import Image
D='/tmp/claude-0/-home-claude-science-games/3daf9092-144f-588c-9647-272dca618339/scratchpad/gem/'
F=pathlib.Path('/home/claude/science-games/assets/fonts');fb=lambda n: base64.b64encode((F/n).read_bytes()).decode()
FONTS=f'@font-face{{font-family:V;src:url(data:font/woff2;base64,{fb("Vazirmatn-Regular.woff2")});font-weight:400}}@font-face{{font-family:V;src:url(data:font/woff2;base64,{fb("Vazirmatn-Bold.woff2")});font-weight:700}}'
def b64(p,maxw=None):
    im=Image.open(p)
    if maxw: im.thumbnail((maxw,maxw*3),Image.LANCZOS)
    bio=io.BytesIO();im.save(bio,'PNG');return 'data:image/png;base64,'+base64.b64encode(bio.getvalue()).decode()
def bust(k,mood,size,ring,bg='#FFF6E6'):
    src=b64(D+f'faces/out/c{k}_{mood}.png',300)
    return f'<div class="bust" style="width:{size}px;height:{size}px;border-color:{ring};background:{bg}"><img src="{src}"></div>'
fa=lambda n:str(n).translate(str.maketrans('0123456789','۰۱۲۳۴۵۶۷۸۹'))
star=lambda on,c:f'<svg width="20" height="20" viewBox="0 0 24 24"><path d="M12 2l3 7 7 .6-5.3 4.7 1.6 7.2L12 17.8 5.7 21.5l1.6-7.2L2 9.6 9 9z" fill="{c if on else "none"}" stroke="{c if on else "currentColor"}" stroke-width="2"/></svg>'
CSS=f'''{FONTS}*{{box-sizing:border-box}}body{{margin:0;font-family:V,sans-serif;direction:rtl}}
.ph{{width:390px;background:var(--paper);color:var(--ink);overflow:hidden}}
header{{display:flex;align-items:center;gap:10px;padding:12px 16px;background:var(--hdr);color:var(--hink)}}
.ib{{width:44px;height:44px;border-radius:50%;background:transparent;color:inherit;border:2.5px solid currentColor;font:700 26px/1 V;display:grid;place-items:center;padding-bottom:4px;flex:none}}
  .hb{{width:48px;height:48px;border-radius:50%;background:var(--hbg);color:var(--hfg);border:3px solid var(--hed);box-shadow:0 3px 0 var(--hed);font:700 24px/1 V;flex:none}}
.tt{{flex:1;min-width:0;display:flex;flex-direction:column}}.tt small{{font-size:13px;opacity:.92;white-space:nowrap}}.tt b{{font-size:22px;line-height:1.3}}
.stars{{display:flex;gap:2px}}
.scene img{{display:block;width:100%}}
.panel{{padding:24px 20px 28px;display:flex;flex-direction:column;gap:24px}}
.who{{display:flex;flex-direction:column;gap:10px}}.who .nm{{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;color:var(--muted)}}.who p{{margin:0;font-size:20px;line-height:1.9;text-align:justify;text-align-last:right}}
.bust{{flex:none;border-radius:50%;border:3.5px solid;overflow:hidden;position:relative}}.bust img{{position:absolute;left:6%;top:6%;width:88%}}
.btn{{min-height:58px;border-radius:18px;font:700 21px V;padding:0 20px;flex:1}}
.btn.pri{{background:var(--btn);color:var(--bink);border:3px solid var(--edge);box-shadow:0 5px 0 var(--edge)}}
.btn.sec{{background:#fff;color:var(--ink);border:3px solid var(--sec);box-shadow:0 5px 0 var(--sec)}}
.row{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.legend{{display:flex;gap:18px;font-size:16px;color:var(--muted)}}.sw{{display:flex;align-items:center;gap:6px}}.sw i{{width:22px;height:8px;border-radius:4px;display:inline-block}}
.term{{text-decoration:underline;text-decoration-thickness:3px;text-underline-offset:7px;text-decoration-color:var(--sec);font-weight:700}}
.slider{{display:flex;align-items:center;gap:10px;font-size:16px;color:var(--muted)}}.track{{flex:1;height:12px;border-radius:6px;background:var(--trk);position:relative}}.track i{{position:absolute;top:-12px;right:44%;width:36px;height:36px;border-radius:50%;background:var(--btn);box-shadow:0 0 0 3px var(--edge) inset,0 3px 0 var(--edge)}}
.fb{{margin:0;font-size:20px;font-weight:700;color:var(--ok)}}
.tray{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.wt{{height:92px;border-radius:16px;background:#fff;border:3px solid var(--sec);box-shadow:0 4px 0 var(--sec);display:flex;flex-direction:column;align-items:center;justify-content:flex-end;padding-bottom:6px;gap:4px;font:700 15px V}}
.wt img{{max-height:52px}}.wt.used{{opacity:.45;box-shadow:none;border-style:dashed}}
'''
L1=dict(paper='#FFF6E6',ink='#2A1A14',muted='#5C4630',hdr='#E3AE52',hink='#2A1A14',btn='#1F6F6B',edge='#134A47',bink='#FFFFFF',sec='#1F6F6B',trk='#D8EDEA',ok='#146B38',starc='#5B3A29',hbg='#1F6F6B',hfg='#FFFFFF',hed='#134A47')
L2=dict(paper='#F2F6F4',ink='#1E2A2E',muted='#4A5A5E',hdr='#174656',hink='#F2F6F4',btn='#F2785C',edge='#B84A33',bink='#2A1A14',sec='#B84A33',trk='#F7DCD4',ok='#146B38',starc='#F2C14E',hbg='#F2C14E',hfg='#2A1A14',hed='#B8861E')
var=lambda L:';'.join(f'--{k}:{v}' for k,v in L.items())
def hdr(L,land,stop,name,n):
    return f'<header><button class="ib">›</button><div class="tt"><small>{land} · منزل {fa(stop)}</small><b>{name}</b></div><div class="stars">{"".join(star(i<n,L["starc"]) for i in range(3))}</div><button class="hb" aria-label="راهنما">؟</button></header>'
lever=f'''<style>{CSS}</style><section class="ph" style="{var(L2)}">{hdr(L2,"کارگاه ساختمانی و بندر",5,"اهرم",1)}
<div class="scene"><img src="{b64(D+'props/m6/lever.png')}"></div><div class="panel">
<div class="who"><div class="nm">{bust(1,"thinking",52,"#B84A33","#FFFFFF")}اوستا هستی</div><p>این سنگ باید داخلِ فرغون بیفتد. جای <span class="term">تکیه‌گاه</span> را انتخاب کن و سرِ تخته را فشار بده.</p></div>
<div class="slider"><span>نزدیک به سنگ</span><div class="track"><i></i></div><span>دور از سنگ</span></div>
<div class="row"><button class="btn pri">امتحان کن</button><button class="btn sec">از نو</button></div></div></section>'''
tray=''.join(f'<div class="wt{" used" if u else ""}"><img style="max-height:{hh}px" src="{b64(D+f"props/m6/w{i}.png")}">{t}</div>' for i,t,u,hh in [(0,'۱ کیلوگرم',False,34),(1,'۱ کیلوگرم',True,38),(3,'۲ کیلوگرم',True,48),(2,'۳ کیلوگرم',False,56)])
bal=f'''<style>{CSS}</style><section class="ph" style="{var(L1)}">{hdr(L1,"کارگاه نجاری",2,"جرم و وزن",2)}
<div class="scene"><img src="{b64(D+'props/m6/balance.png')}"></div><div class="panel">
<div class="who"><div class="nm">{bust(1,"thinking",52,"#1F6F6B")}اوستا هستی</div><p>جرمِ این جعبه ۳ کیلوگرم است. وزنه‌ها را روی کفهٔ دیگر بگذار تا ترازو صاف شود.</p></div>
<div class="tray">{tray}</div>
<div class="row"><button class="btn pri">بررسی کن</button><button class="btn sec">از نو</button></div></div></section>'''
NAMES=["نیرو","جرم و وزن","نیروسنج","اصطکاک","اهرم ۱","اهرم ۲","سطح شیب‌دار","گوه و پیچ","چرخ و محور","قرقره","چالش مهندسی","نمایشگاه"]
LANDS=[("کارگاه نجاری","#F2C66D","#E8B75B",(0,4),"#5B3A29","#2A1A14"),("کارگاه ساختمانی و بندر","#1E576A","#24637A",(4,10),"#F3E9E6","#F2F6F4"),("کارخانهٔ اختراع","#2D1F39","#3A2A4A",(10,12),"#EDD9C9","#F7F1F4")]
CUR=5;STARS=[3,2,3,2,1]
Wm=390;SP=150;TOP=110;y=0;svg=[];pos=[];bands=[]
for i,(n,bgc,envc,(a,b),path,ink) in enumerate(LANDS):
    h=TOP+(b-a)*SP+10;bands.append((y,h))
    for k,s in enumerate(range(a,b)): pos.append((Wm/2+(-82 if s%2==0 else 82),y+TOP+50+k*SP))
    y+=h
Hm=y
TT=[]
for i,(n,bgc,envc,(a,b),path,ink) in enumerate(LANDS):
    y0,h=bands[i];svg.append(f'<rect x="0" y="{y0}" width="{Wm}" height="{h}" fill="{bgc}"/>')
    if i==1: svg+= [f'<path d="M{x} {y0}V{y0+h}" stroke="{envc}" stroke-width="1.5"/>' for x in range(0,Wm,30)]+[f'<path d="M0 {yy}H{Wm}" stroke="{envc}" stroke-width="1.5"/>' for yy in range(int(y0),int(y0+h),30)]
    elif i==0: svg+= [f'<rect x="{x}" y="{y0}" width="4" height="{h}" fill="{envc}"/>' for x in range(20,Wm,70)]
    else: svg+= [f'<circle cx="{x}" cy="{yy}" r="3" fill="{envc}"/>' for x in range(20,Wm,44) for yy in range(int(y0)+20,int(y0+h),44)]
    TT.append(f'<rect x="12" y="{y0+18}" width="{Wm-24}" height="58" rx="16" fill="{["#FFF6E6","#2B6A80","#3F2E50"][i]}" stroke="{["#E3AE52","#3E8196","#56436A"][i]}" stroke-width="2"/>')
    TT.append(f'<text x="{Wm-28}" y="{y0+56}" font-family="V" font-weight="700" font-size="23" fill="{ink}">{n}</text>')
for i in range(1,12):
    (x1,y1),(x2,y2)=pos[i-1],pos[i];L=LANDS[0 if i<4 else 1 if i<10 else 2]
    svg.append(f'<path d="M{x1} {y1} C{x1} {y1+SP*.6} {x2} {y2-SP*.6} {x2} {y2}" stroke="{L[4]}" stroke-width="7" stroke-dasharray="{"3 13" if i>CUR else "16 11"}" stroke-linecap="round" fill="none" opacity="{.7 if i>CUR else 1}"/>')
svg+=TT
BR=46
for i,(x,yy) in enumerate(pos):
    L=LANDS[0 if i<4 else 1 if i<10 else 2];done=i<CUR;now=i==CUR;lock=i>CUR
    img=b64(D+f'props/m6/{"bl" if lock else "b"}{i+1}.png',140)
    if now: svg.append(f'<circle cx="{x}" cy="{yy}" r="{BR+12}" fill="none" stroke="#FF94C2" stroke-width="6"/>')
    svg.append(f'<circle cx="{x}" cy="{yy+4}" r="{BR}" fill="#000" opacity=".25"/><image href="{img}" x="{x-BR}" y="{yy-BR}" width="{2*BR}" height="{2*BR}"/>')
    if lock: svg.append(f'<g transform="translate({x+BR-10} {yy+BR-14})"><circle r="15" fill="#3B2417"/><rect x="-7" y="-2" width="14" height="10" rx="2" fill="#FFF6E6"/><path d="M-4 -2V-5a4 4 0 0 1 8 0V-2" stroke="#FFF6E6" stroke-width="2.6" fill="none"/></g>')
    lw=len(NAMES[i])*9.5+30;ly=yy+BR+26
    svg.append(f'<rect x="{x-lw/2}" y="{ly-19}" width="{lw}" height="34" rx="17" fill="#FFFDF8" stroke="#3B2417" stroke-width="2"/><text x="{x}" y="{ly+5}" text-anchor="middle" font-family="V" font-weight="700" font-size="16" fill="#2A1A14">{NAMES[i]}</text>')
    if done:
        for k in range(3):
            c='#F2C14E' if k<STARS[i] else '#FFFDF8';svg.append(f'<path transform="translate({x-24+k*24} {ly+32}) scale(.75)" d="M0 -14 L4 -4 L14 -3 L6 4 L9 14 L0 8 L-9 14 L-6 4 L-14 -3 L-4 -4 Z" fill="{c}" stroke="#3B2417" stroke-width="2.5"/>')
    if now:
        bx=x-110 if x>Wm/2 else x+110
        svg.append(f'<foreignObject x="{bx-38}" y="{yy-24}" width="76" height="76"><div xmlns="http://www.w3.org/1999/xhtml">{bust(1,"happy",72,"#FF94C2")}</div></foreignObject>')
        svg.append(f'<rect x="{bx-44}" y="{yy+54}" width="88" height="30" rx="15" fill="#FF94C2"/><text x="{bx}" y="{yy+75}" text-anchor="middle" font-family="V" font-weight="700" font-size="15" fill="#2A1A14">تو اینجایی</text>')
mp=f'''<style>{CSS}.top{{display:flex;align-items:center;gap:10px;padding:10px 14px;background:#FFF6E6;color:#2A1A14}}.top b{{font-size:20px;flex:1}}.top span{{font-weight:700;font-size:16px}}.top .wb{{height:44px;border-radius:14px;border:2.5px solid #1F6F6B;padding:0 12px;display:grid;place-items:center;font-weight:700;color:#134A47;background:#fff}}</style>
<section class="ph" style="--paper:#FFF6E6"><div class="top">{bust(1,"happy",50,"#1F6F6B")}<b>اوستا هستی</b><span>★ ۱۱</span><div class="wb">واژه‌ها</div></div>
<svg viewBox="0 0 {Wm} {Hm}" width="{Wm}" xmlns="http://www.w3.org/2000/svg" direction="rtl">{"".join(svg)}</svg></section>'''
for k,v in {'lever':lever,'balance':bal,'map':mp}.items(): pathlib.Path(D+f'props/m6/{k}.html').write_text('<meta charset=utf8>'+v,encoding='utf-8')
