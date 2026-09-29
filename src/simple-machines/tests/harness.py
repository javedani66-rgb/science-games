from playwright.sync_api import sync_playwright
import sys, json
import pathlib
D=str(pathlib.Path(__file__).resolve().parent.parent)+'/'
OUT_=str(pathlib.Path(__file__).resolve().parent)+'/shots/'
OUT=OUT_
import os; os.makedirs(OUT,exist_ok=True)
URL='file://'+D+'preview.html'

class G:
    def __init__(s,pg): s.pg=pg
    def pt(s,x,y):
        s.pg.evaluate("()=>{const v=document.querySelector('#sc');const r=v.getBoundingClientRect();if(r.top<0||r.bottom>innerHeight)v.scrollIntoView({block:'center'});}")
        return s.pg.evaluate("([x,y])=>{const v=document.querySelector('#sc');const m=v.getScreenCTM();return {x:m.a*x+m.c*y+m.e,y:m.b*x+m.d*y+m.f};}",[x,y])
    def drag(s,x1,y1,x2,y2,steps=12):
        a=s.pt(x1,y1); b=s.pt(x2,y2)
        s.pg.mouse.move(a['x'],a['y']); s.pg.mouse.down()
        for i in range(1,steps+1):
            s.pg.mouse.move(a['x']+(b['x']-a['x'])*i/steps, a['y']+(b['y']-a['y'])*i/steps)
            s.pg.wait_for_timeout(15)
        s.pg.mouse.up(); s.pg.wait_for_timeout(120)
    def circle(s,cx,cy,r,turns,start=-1.5708,ry=None,steps_per_turn=24):
        import math
        ry=ry or r
        p0=s.pt(cx+r*math.cos(start),cy+ry*math.sin(start))
        s.pg.mouse.move(p0['x'],p0['y']); s.pg.mouse.down()
        n=int(turns*steps_per_turn)
        for i in range(1,n+1):
            a=start+2*math.pi*i/steps_per_turn
            p=s.pt(cx+r*math.cos(a),cy+ry*math.sin(a)); s.pg.mouse.move(p['x'],p['y']); s.pg.wait_for_timeout(8)
        s.pg.mouse.up(); s.pg.wait_for_timeout(100)
    def tap(s,x,y):
        a=s.pt(x,y); s.pg.mouse.click(a['x'],a['y']); s.pg.wait_for_timeout(150)
    def shot(s,name,full=False): s.pg.screenshot(path=OUT+name+'.png',full_page=full)
    def text(s,sel):
        return s.pg.locator(sel).inner_text() if s.pg.locator(sel).count() else ''
    def attr_all(s,sel,attr):
        return s.pg.evaluate("([sel,a])=>[...document.querySelectorAll(sel)].map(e=>e.getAttribute(a))",[sel,attr])

def open_page(pw,w=400,h=900,prog=None):
    b=pw.chromium.launch(); pg=b.new_page(viewport={'width':w,'height':h})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append('console:'+m.text) if m.type=='error' else None)
    pg.goto(URL)
    if prog is not None:
        pg.evaluate("p=>localStorage.setItem('sm-workshop-v3',JSON.stringify(p))",prog); pg.reload()
    pg.wait_for_timeout(300)
    return b,pg,errs
