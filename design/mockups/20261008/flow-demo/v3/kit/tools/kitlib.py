# kitlib: small helpers to write the kit SVGs (no text inside any graphic).
import random, math, os
OUT = os.path.join(os.path.dirname(__file__), '..', 'svg')
os.makedirs(OUT, exist_ok=True)

INK='#184441'; INK2='#0f2e2c'; CREAM='#fff0c9'; PAPER='#f6e2b0'
GOLD='#dbac54'; GOLD_L='#f6dc92'; GOLD_D='#a97b2c'; GOLD_DD='#5b3d12'
LINE='#3a2610'

GOLD_GRAD = f'''<linearGradient id="gold" x1="0" y1="0" x2="0.6" y2="1">
<stop offset="0" stop-color="{GOLD_L}"/><stop offset=".45" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_D}"/></linearGradient>'''
WOBBLE = '''<filter id="wob" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="3.2"/></filter>'''
SHADOW = '''<filter id="sh" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur stdDeviation="2.4"/></filter>'''

def svg(name, w, h, body, defs='', extra=''):
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" {extra}>'
         f'<defs>{defs}</defs>{body}</svg>')
    open(os.path.join(OUT, name), 'w').write(s)
    return s

def gear(cx, cy, r, teeth, fill, ln=None, hole=0.35, lw=1.5):
    pts = []
    n = teeth * 4
    for i in range(n):
        a = 2*math.pi*i/n
        rr = r if (i % 4) in (0, 1) else r*0.8
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + 'Z'
    s = f'<path d="{d}" fill="{fill}"' + (f' stroke="{ln}" stroke-width="{lw}" stroke-linejoin="round"' if ln else '') + '/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r*hole:.1f}" fill="rgba(0,0,0,.28)"/>'
    return s

def hills(w, y, amp, seed, fill, ln=None, bottom=None, n=7, ex=''):
    rnd = random.Random(seed)
    bottom = bottom if bottom is not None else y + 2000
    xs = [i*w/(n-1) for i in range(n)]
    ys = [y + rnd.uniform(-amp, amp) for _ in xs]
    d = f'M-10,{bottom} L-10,{ys[0]:.1f}'
    for i in range(n-1):
        x0, y0, x1, y1 = xs[i], ys[i], xs[i+1], ys[i+1]
        mx = (x0+x1)/2
        d += f' C{mx:.1f},{y0:.1f} {mx:.1f},{y1:.1f} {x1:.1f},{y1:.1f}'
    d += f' L{w+10},{bottom} Z'
    st = f' stroke="{ln}" stroke-width="2" stroke-linejoin="round"' if ln else ''
    return f'<path d="{d}" fill="{fill}"{st} {ex}/>'

def star4(cx, cy, r, fill):
    k = r*0.28
    return f'<path d="M{cx},{cy-r} L{cx+k},{cy-k} L{cx+r},{cy} L{cx+k},{cy+k} L{cx},{cy+r} L{cx-k},{cy+k} L{cx-r},{cy} L{cx-k},{cy-k}Z" fill="{fill}"/>'
