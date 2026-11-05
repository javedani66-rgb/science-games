# lib4: کمک‌های ساخت SVG برای kit4 (هیچ متنی داخل گرافیک نیست). خروجی در ../svg
import os, math, random
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','svg'); os.makedirs(OUT,exist_ok=True)
def svg(name,w,h,body,defs=''):
    s=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{defs}</defs>{body}</svg>'
    open(os.path.join(OUT,name),'w',encoding='utf-8').write(s); return s
def _stops(stops):
    o=''
    for t in stops:
        off,c=t[0],t[1]; a=t[2] if len(t)>2 else None
        o+=f'<stop offset="{off}" stop-color="{c}"'+(f' stop-opacity="{a}"' if a is not None else '')+'/>'
    return o
def lg(i,stops,x1=0,y1=0,x2=0,y2=1): return f'<linearGradient id="{i}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{_stops(stops)}</linearGradient>'
def rg(i,stops,cx=.5,cy=.5,r=.5): return f'<radialGradient id="{i}" cx="{cx}" cy="{cy}" r="{r}">{_stops(stops)}</radialGradient>'
def rect(x,y,w,h,f,rx=0,op=1,ex=''): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{f}" opacity="{op}" {ex}/>'
def circ(x,y,r,f,op=1,ex=''): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{f}" opacity="{op}" {ex}/>'
def ell(x,y,rx,ry,f,op=1,ex=''): return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{f}" opacity="{op}" {ex}/>'
def poly(pts,f,op=1,ex=''): return '<path d="M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+f'Z" fill="{f}" opacity="{op}" {ex}/>'
def path(d,f='none',st=None,sw=1,op=1,ex=''): return f'<path d="{d}" fill="{f}"'+(f' stroke="{st}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if st else '')+f' opacity="{op}" {ex}/>'
def blur(i,sd): return f'<filter id="{i}" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="{sd}"/></filter>'
def smooth_ridge(w,y,amp,seed,n=7,bottom=2000,step=None):
    r=random.Random(seed); xs=[i*w/(n-1) for i in range(n)]; ys=[y+r.uniform(-amp,amp) for _ in xs]
    d=f'M-10,{bottom} L-10,{ys[0]:.1f}'
    for i in range(n-1):
        mx=(xs[i]+xs[i+1])/2; d+=f' C{mx:.1f},{ys[i]:.1f} {mx:.1f},{ys[i+1]:.1f} {xs[i+1]:.1f},{ys[i+1]:.1f}'
    return d+f' L{w+10},{bottom} Z'
def gear(cx,cy,r,teeth,fill,hole=.32,op=1):
    pts=[];n=teeth*4
    for i in range(n):
        a=2*math.pi*i/n; rr=r if (i%4) in (0,1) else r*.8; pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    d='M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z'
    return f'<g opacity="{op}"><path d="{d}" fill="{fill}"/><circle cx="{cx}" cy="{cy}" r="{r*hole:.1f}" fill="#000" opacity=".28"/></g>'
def star4(cx,cy,r,f,op=1):
    k=r*.28; return f'<path d="M{cx},{cy-r} L{cx+k},{cy-k} L{cx+r},{cy} L{cx+k},{cy+k} L{cx},{cy+r} L{cx-k},{cy+k} L{cx-r},{cy} L{cx-k},{cy-k}Z" fill="{f}" opacity="{op}"/>'
