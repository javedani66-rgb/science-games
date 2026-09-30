import json,math,base64
exec(open('page.py').read().split("lever=f'''")[0])
M=json.load(open('lever2_meta.json'))
PANEL=400
CSS2=CSS+f'''.ph{{height:844px;display:flex;flex-direction:column}}header{{position:relative;z-index:5}}
.scene{{flex:1;min-height:0;position:relative;overflow:hidden}}.scene svg{{position:absolute;inset:0;width:100%;height:100%}}
.panel{{flex:none;height:{PANEL}px;padding:20px 20px 24px;gap:16px}}.bar{{margin-top:auto}}
.tt .st{{display:flex;gap:2px;margin-top:2px}}.tt .st svg{{width:16px;height:16px}}
.hb{{position:relative;background:#FFFDF8!important;color:#1E2A2E!important;border:2.5px solid var(--hbd,#FFFDF8)!important;box-shadow:0 3px 0 rgba(0,0,0,.28)!important;font-size:24px}}.btn.full{{width:100%}}.hb{{display:grid;place-items:center;padding:0}}.tt{{min-width:0}}.tt small{{font-size:13px;white-space:nowrap}}.nb{{flex:none;height:48px;padding:0 14px 0 16px;border-radius:24px;display:flex;align-items:center;gap:6px;background:#FFFDF8;color:#1E2A2E;border:2.5px solid var(--hbd,#FFFDF8);box-shadow:0 3px 0 rgba(0,0,0,.28);font:700 17px V}}.panel{{position:relative}}.track i{{right:calc(40% - 18px)!important}}.bar{{position:absolute;left:20px;right:20px;bottom:24px;margin:0!important}}
.fx{{direction:ltr;text-align:center;background:#fff;border:2.5px solid var(--sec);border-radius:16px;padding:10px 12px;font:700 22px V;color:var(--ink);letter-spacing:.5px}}
.fx small{{display:block;direction:rtl;font:400 16px V;color:var(--muted);letter-spacing:0;margin-top:2px}}
.fx .p{{color:#7A3FC8}}.fx .f{{color:#C2407E}}.fx .b{{color:#2E5AA8}}.fx sub{{font-size:.6em}}
'''
def hdr2(L,land,stop,name,n):
    st="".join(star(i<n,L["starc"]) for i in range(3))
    return f'<header><button class="nb" aria-label="بازگشت به نقشه"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"><path d="M3 6.5l6-2.5 6 2.5 6-2.5v13.5l-6 2.5-6-2.5-6 2.5z"/><path d="M9 4v13.5M15 6.5V20"/></svg><span>نقشه</span></button><div class="tt"><small>{land}</small><b>{name}</b><div class="st">{st}</div></div><button class="hb" aria-label="از نو"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"><path d="M19.5 12a7.5 7.5 0 1 1-2.2-5.3"/><path d="M18.6 3.2v4.4h-4.4"/></svg></button><button class="hb" aria-label="راهنما"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round"><g transform="translate(24 0) scale(-1 1)"><path d="M8.6 8.4a3.5 3.5 0 1 1 5 3.2c-1 .5-1.6 1.2-1.6 2.3v.9"/><circle cx="12" cy="19.2" r=".6" fill="currentColor"/></g></svg></button></header>'
def scene(png,extra='',vb="0 0 800 820"):
    src='data:image/png;base64,'+base64.b64encode(open(png,'rb').read()).decode()
    return f'<div class="scene"><svg viewBox="{vb}" preserveAspectRatio="xMidYMax slice"><image href="{src}" width="800" height="820"/>{extra}</svg></div>'
def bracket(x1,y1,x2,y2,off,col,label,up=True):
    a=math.atan2(y2-y1,x2-x1);nx,ny=math.sin(a),-math.cos(a)
    if not up: nx,ny=-nx,-ny
    p1=(x1+nx*off,y1+ny*off);p2=(x2+nx*off,y2+ny*off)
    t=10
    s=f'<path d="M{p1[0]-nx*t:.1f} {p1[1]-ny*t:.1f} L{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f} L{p2[0]-nx*t:.1f} {p2[1]-ny*t:.1f}" stroke="{col}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    mx,my=(p1[0]+p2[0])/2+nx*36,(p1[1]+p2[1])/2+ny*36
    w=len(label)*17+36
    s+=f'<rect x="{mx-w/2:.1f}" y="{my-22:.1f}" width="{w}" height="44" rx="22" fill="{col}"/><text x="{mx:.1f}" y="{my+10:.1f}" text-anchor="middle" font-family="V" font-weight="700" font-size="26" fill="#fff" direction="rtl">{label}</text>'
    return s
M=json.load(open('lever3_meta.json'))
def hdim(x1,x2,y,col,label):
    t=12;o=f'<path d="M{x1:.1f} {y-t} V{y} H{x2:.1f} V{y-t}" stroke="{col}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    w=len(label)*16+34;mx=(x1+x2)/2
    return o+f'<rect x="{mx-w/2:.1f}" y="{y+8}" width="{w}" height="40" rx="20" fill="{col}"/><text x="{mx:.1f}" y="{y+37}" text-anchor="middle" font-family="V" font-weight="700" font-size="24" fill="#fff" direction="rtl">{label}</text>'
def drop(x,y0,y1): return f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1}" stroke="#CFE3E8" stroke-width="3" stroke-dasharray="7 7"/>'
def dims(m):
    Y=752;(px,py),(sx,sy),(fx_,fy)=m['pivot'],m['stone'],m['force'];f=m['f']
    o=drop(sx,sy+8,Y)+drop(px,py+50,Y)+drop(fx_,fy+8,Y)
    o+=hdim(sx,px,Y,'#2E5AA8',fa(f)+' متر')+hdim(px,fx_,Y,'#7A3FC8',fa(5-f)+' متر')
    o+=f'<circle cx="{px}" cy="{py}" r="8" fill="#F2C14E" stroke="#2A1A14" stroke-width="3"/>'
    return o
VB='10 230 620 590'
L=dict(L2)
before=f'''<style>{CSS2}</style><section class="ph" style="{var(L)}">{hdr2(L,"کارگاه ساختمانی و بندر",5,"اهرم",1)}
{scene('lever3_before.png',dims(M['before']),vb=VB)}<div class="panel">
<div class="who"><div class="nm">{bust(1,"thinking",52,"#B84A33","#FFFFFF")}اوستا هستی</div><p>این سنگ سنگین است. با اهرم آن را از زمین بلند کن. <span class="term">تکیه‌گاه</span> را جابه‌جا کن و سرِ تخته را فشار&nbsp;بده.</p></div>
<div class="slider"><span>به طرفِ سنگ</span><div class="track"><i></i></div><span>به طرفِ دست</span></div>
<div class="bar"><button class="btn pri full">امتحان کن</button></div></div></section>'''
after=f'''<style>{CSS2}</style><section class="ph" style="{var(L)}">{hdr2(L,"کارگاه ساختمانی و بندر",5,"اهرم",2)}
{scene('lever3_after.png',dims(M['after']),vb=VB)}<div class="panel">
<div class="who"><div class="nm">{bust(1,"happy",52,"#B84A33","#FFFFFF")}اوستا هستی</div><p style="font-weight:700;color:#0F4F2A">آفرین! <span style="color:#7A3FC8">بازوی محرک</span> ۴ متر است و <span style="color:#2E5AA8">بازوی مقاوم</span> ۱ متر. چون تکیه‌گاه نزدیکِ سنگ است، سنگ با نیروی کمتری بلند&nbsp;شد.</p></div>
<div class="fx"><span class="f">F<sub>1</sub></span> × <span class="p">۴</span> = ۲۴۰ × <span class="b">۱</span> &nbsp;⟹&nbsp; <span class="f">F<sub>1</sub></span> = ۶۰ N<small>با ۶۰ نیوتن، اهرم در تعادل&nbsp;است.</small></div>
<div class="bar"><button class="btn pri full">مأموریتِ بعد</button></div></div></section>'''
open('s_before.html','w').write('<meta charset=utf8>'+before);open('s_after.html','w').write('<meta charset=utf8>'+after)
