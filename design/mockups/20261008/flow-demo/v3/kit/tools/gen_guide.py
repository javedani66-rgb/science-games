from kitlib import *
import base64, shutil, os
SRC='/home/claude/science-games/src/simple-machines/img/'
IMG=os.path.join(os.path.dirname(__file__),'..','img'); os.makedirs(IMG,exist_ok=True)
for st in ('thinking','happy','surprised','oops'):
    shutil.copy(SRC+f'b1_{st}.webp',IMG)
    b64=base64.b64encode(open(SRC+f'b1_{st}.webp','rb').read()).decode()
    d=f'''{GOLD_GRAD}{SHADOW}<radialGradient id="bk" cx=".4" cy=".3" r=".9"><stop offset="0" stop-color="#fffaf0"/><stop offset="1" stop-color="#f1d99c"/></radialGradient>
<clipPath id="cl"><path d="M10,0 H86 V62 H82 A34,34 0 0 1 14,62 H10Z"/></clipPath>'''
    b=(f'<ellipse cx="48" cy="103" rx="22" ry="5.5" fill="#2a1a08" opacity=".42" filter="url(#sh)"/>'
       f'<path d="M36,92 L48,106 L60,92Z" fill="url(#gold)" stroke="{LINE}" stroke-width="2.6" stroke-linejoin="round"/>'
       f'<circle cx="48" cy="62" r="37" fill="url(#gold)" stroke="{LINE}" stroke-width="3"/><circle cx="48" cy="62" r="31" fill="url(#bk)" stroke="{LINE}" stroke-opacity=".55" stroke-width="2"/>'
       f'<g clip-path="url(#cl)"><image href="data:image/webp;base64,{b64}" x="6" y="12" width="84" height="84"/></g>'
       f'<path d="M20,46 A31,31 0 0 1 36,34" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="3" stroke-linecap="round"/>')
    svg(f'guide-{st}.svg',96,112,b,d)
print('guide ok')
