# gen_map.py: گره‌ها (۴ حالت × ۴ زمین)، دروازه، پرچم شروع/پایان، مانع طنابی، ردپا.
# گره: حلقهٔ دو‌لایه (دورگیر تیره بیرون، باند تأکید زمین، نوار کرم، رو) تا روی هر زمین جدا بماند.
# رنگ تأکید به نوع مرحله/پیشرفت ربط ندارد؛ فقط پوست زمین است (D11). حالت‌ها با شکل جدا می‌شوند، نه رنگ.
from kitlib import *
from palettes import PAL, FIG
import math
def mix(a,b,t):
    A=[int(a[i:i+2],16) for i in (1,3,5)];B=[int(b[i:i+2],16) for i in (1,3,5)]
    return '#%02x%02x%02x'%tuple(round(A[i]*(1-t)+B[i]*t) for i in range(3))
PALX=dict(PAL); PALX['gen']=dict(accent=GOLD_L,accent_d=GOLD_D,accent_l='#fff0c9')  # نسخهٔ بی‌زمین (طلایی)

def node_svg(state, P):
    A,AD,AL=P['accent'],P['accent_d'],P['accent_l']
    locked=state=='locked'
    if locked: A,AD,AL='#b3a893','#6e6455','#d8cfbd'
    d=(f'<linearGradient id="ac" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="{AL}"/><stop offset=".5" stop-color="{A}"/><stop offset="1" stop-color="{AD}"/></linearGradient>'
       f'<linearGradient id="ol" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffdf4"/><stop offset="1" stop-color="{mix(AL,"#fff1c8",.6)}"/></linearGradient>'
       f'<linearGradient id="cb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset="1" stop-color="#ead2a0"/></linearGradient>'
       f'<radialGradient id="fc" cx=".4" cy=".3" r=".85"><stop offset="0" stop-color="{"#e3dccd" if locked else ("#fffbe0" if state=="done" else "#fffaf0")}"/><stop offset="1" stop-color="{"#a99f8c" if locked else ("#ffd87a" if state=="done" else "#f3dca4")}"/></radialGradient>{SHADOW}')
    b='<ellipse cx="48" cy="90" rx="34" ry="5.5" fill="#1a0e04" opacity=".42" filter="url(#sh)"/>'
    # حلقهٔ بیرونی روشن (کرم-تأکید) تا لبهٔ گره روی هر زمین ≥۳:۱ شود؛ باند تأکید داخل آن؛ دورگیر تیره بیرون و بین لایه‌ها
    b+=f'<circle cx="48" cy="48" r="46" fill="{LINE}"/>'
    b+=f'<circle cx="48" cy="48" r="44.2" fill="url(#ol)"/>'
    b+=f'<circle cx="48" cy="48" r="40.4" fill="{LINE}"/>'
    b+=f'<circle cx="48" cy="48" r="39" fill="url(#ac)"/>'
    for a in (45,135,225,315):
        x=48+37.1*math.cos(math.radians(a));y=48+37.1*math.sin(math.radians(a))
        b+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.9" fill="{FIG["path_light"]}" stroke="{LINE}" stroke-opacity=".7" stroke-width=".9"/>'
    b+=f'<circle cx="48" cy="48" r="35.2" fill="{LINE}"/><circle cx="48" cy="48" r="33.6" fill="url(#cb)"/>'
    b+=f'<circle cx="48" cy="48" r="30" fill="{LINE}" opacity=".55"/><circle cx="48" cy="48" r="29" fill="url(#fc)"/>'
    b+='<path d="M22,36 A29,29 0 0 1 52,20" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="3" stroke-linecap="round"/>'
    if state=='done':
        b+=f'<g transform="translate(76,8)"><path d="M0,26 V-4" stroke="{LINE}" stroke-width="3.6" stroke-linecap="round"/><path d="M1.6,-4 L18,2 L1.6,8Z" fill="{GOLD}" stroke="{LINE}" stroke-width="2.2" stroke-linejoin="round"/><circle cx="0" cy="-5" r="2.6" fill="{GOLD_L}" stroke="{LINE}" stroke-width="1.3"/></g>'
    if state=='open':
        b+=f'<g transform="translate(80,14)"><circle r="12" fill="{LINE}"/><circle r="10" fill="{INK}"/><circle r="8" fill="none" stroke="{GOLD_L}" stroke-width="1.5"/>{star4(0,0,6.4,CREAM)}</g>'
    if state=='trial':
        b+=f'<circle cx="48" cy="48" r="46" fill="none" stroke="{FIG["path_light"]}" stroke-width="2.2" stroke-dasharray="8 6" stroke-linecap="round" opacity=".9"/>'
        b+=f'<g transform="translate(15,76)"><circle r="14" fill="{LINE}"/><circle r="12" fill="{INK}"/><path d="M-3.6,-7.4 h7.2 M-2.6,-7.4 v5.8 l-5.4,9 a1.9,1.9 0 0 0 1.7,2.9 h12.6 a1.9,1.9 0 0 0 1.7,-2.9 l-5.4,-9 v-5.8" fill="#bfeee9" stroke="{CREAM}" stroke-width="1.8" stroke-linejoin="round"/><path d="M-5,4 H5" stroke="#17a79f" stroke-width="3" stroke-linecap="round"/></g>'
    if locked:
        b+='<circle cx="48" cy="48" r="29" fill="#3d362a" opacity=".16"/>'
        b+=(f'<g transform="translate(48,50) scale(1.55)"><path d="M-9,-4 V-12 a9,9 0 0 1 18,0 V-4" fill="none" stroke="{LINE}" stroke-width="6.8" stroke-linecap="round"/><path d="M-9,-4 V-12 a9,9 0 0 1 18,0 V-4" fill="none" stroke="#c7bfae" stroke-width="4.2" stroke-linecap="round"/>'
            f'<rect x="-14" y="-5" width="28" height="22" rx="5" fill="#8d826f" stroke="{LINE}" stroke-width="2.6"/><path d="M-10,-1 H10" stroke="#d6cdbb" stroke-width="2" opacity=".6"/><circle cx="0" cy="5" r="3.2" fill="{LINE}"/><rect x="-1.4" y="5" width="2.8" height="7" rx="1" fill="{LINE}"/></g>')
    return d,b

for st in ('open','done','trial','locked'):
    d,b=node_svg(st,PALX['gen']); svg(f'node-{st}.svg',96,96,b,d)
    for k,P in PAL.items():
        d,b=node_svg(st,P); svg(f'node-{st}-{k}.svg',96,96,b,d)

# ---------- دروازه (دید از بالا): دو ستون + روزنهٔ تیره؛ لبهٔ قاب پشت ستون‌ها ادامه دارد ----------
for k,P in list(PAL.items())+[('gen',PALX['gen'])]:
    A,AD,AL=P['accent'],P['accent_d'],P['accent_l']
    d=GOLD_GRAD+SHADOW+f'<linearGradient id="pas" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0f1a1a"/><stop offset=".5" stop-color="#1d2a29"/><stop offset="1" stop-color="#0f1a1a"/></linearGradient><radialGradient id="cap" cx=".35" cy=".3" r=".9"><stop offset="0" stop-color="{AL}"/><stop offset=".6" stop-color="{A}"/><stop offset="1" stop-color="{AD}"/></radialGradient>'
    b=f'<rect x="32" y="14" width="56" height="44" rx="4" fill="{LINE}"/><rect x="34" y="16" width="52" height="40" rx="3" fill="url(#pas)"/>'
    b+=f'<rect x="34" y="16" width="52" height="5" fill="#000" opacity=".4"/><rect x="34" y="51" width="52" height="5" fill="#000" opacity=".4"/>'
    for cx in (18,102):
        b+=f'<ellipse cx="{cx}" cy="57" rx="18" ry="6" fill="#1a0e04" opacity=".4" filter="url(#sh)"/>'
        b+=f'<rect x="{cx-17}" y="19" width="34" height="34" rx="7" fill="{LINE}"/><rect x="{cx-15}" y="21" width="30" height="30" rx="5.5" fill="url(#gold)"/>'
        b+=(f'<path d="M{cx-12},24 H{cx+12} L{cx},36Z" fill="#fff" opacity=".38"/><path d="M{cx-12},24 L{cx},36 L{cx-12},48Z" fill="#fff" opacity=".1"/>'
            f'<path d="M{cx+12},24 L{cx},36 L{cx+12},48Z" fill="#000" opacity=".16"/><path d="M{cx-12},48 H{cx+12} L{cx},36Z" fill="#000" opacity=".3"/>')
        b+=f'<circle cx="{cx}" cy="36" r="5.2" fill="url(#cap)" stroke="{LINE}" stroke-width="1.8"/><circle cx="{cx-1.4}" cy="34.6" r="1.4" fill="#fff" opacity=".8"/>'
    svg(f'gate-{k}.svg',120,72,b,d)

# ---------- پرچم شروع / پایان (میخ‌شده روی خود مسیر) ----------
def flag(name,kind,P):
    A,AD,AL=P['accent'],P['accent_d'],P['accent_l']
    d=GOLD_GRAD+SHADOW+f'<pattern id="ck" width="12" height="12" patternUnits="userSpaceOnUse"><rect width="12" height="12" fill="#fff6dc"/><rect width="6" height="6" fill="{LINE}"/><rect x="6" y="6" width="6" height="6" fill="{LINE}"/></pattern>'
    b=f'<ellipse cx="32" cy="82" rx="26" ry="7" fill="#1a0e04" opacity=".4" filter="url(#sh)"/>'
    b+=f'<ellipse cx="32" cy="78" rx="22" ry="8" fill="{LINE}"/><ellipse cx="32" cy="76" rx="20" ry="7" fill="{FIG["path_light"]}"/><ellipse cx="32" cy="76" rx="20" ry="7" fill="none" stroke="{LINE}" stroke-opacity=".4" stroke-width="1.4"/>'
    b+=f'<rect x="29" y="12" width="6" height="66" rx="2" fill="{LINE}"/><rect x="30.4" y="12" width="3.2" height="64" fill="#e9c27c"/>'
    fill='url(#ck)' if kind=='end' else A
    b+=f'<path d="M35,10 H62 L55,24 L62,38 H35Z" fill="{LINE}" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/><path d="M35,10 H62 L55,24 L62,38 H35Z" fill="{fill}"/>'
    if kind=='start': b+=f'<path d="M38,13 H56" stroke="#fff" stroke-opacity=".5" stroke-width="2.4" stroke-linecap="round"/><path d="M42,24 l6,-5 v10Z" fill="{FIG["path_light"]}" stroke="{LINE}" stroke-width="1.6" stroke-linejoin="round"/>'
    b+=f'<circle cx="32" cy="10" r="5.6" fill="url(#gold)" stroke="{LINE}" stroke-width="2.2"/>'
    svg(name,64,90,b,d)
flag('flag-start.svg','start',PALX['gen']); flag('flag-end.svg','end',PALX['gen'])
for k,P in PAL.items(): flag(f'flag-start-{k}.svg','start',P); flag(f'flag-end-{k}.svg','end',P)

# ---------- مانع طنابی (قفل = مانع فیزیکی): دو تیرک + طناب کرم خمیده ----------
d=GOLD_GRAD+SHADOW
b=f'<ellipse cx="14" cy="38" rx="11" ry="4" fill="#1a0e04" opacity=".4" filter="url(#sh)"/><ellipse cx="86" cy="38" rx="11" ry="4" fill="#1a0e04" opacity=".4" filter="url(#sh)"/>'
b+=f'<path d="M14,12 Q50,40 86,12" fill="none" stroke="{LINE}" stroke-width="9" stroke-linecap="round"/><path d="M14,12 Q50,40 86,12" fill="none" stroke="#e8cf92" stroke-width="5.4" stroke-linecap="round"/><path d="M14,12 Q50,40 86,12" fill="none" stroke="#a97b2c" stroke-width="5.4" stroke-dasharray="3 6" stroke-linecap="butt" opacity=".7"/>'
for x in (14,86):
    b+=f'<rect x="{x-4.5}" y="8" width="9" height="28" rx="3" fill="{LINE}"/><rect x="{x-3}" y="9" width="6" height="26" rx="2" fill="#b97d3f"/><circle cx="{x}" cy="8" r="6.2" fill="url(#gold)" stroke="{LINE}" stroke-width="2"/>'
svg('barrier-rope.svg',100,46,b,d)

# ---------- ردپا (تیره روی مسیر روشن) ----------
svg('footprint.svg',12,18,f'<g fill="{FIG["foot"]}" opacity=".9"><ellipse cx="6" cy="5" rx="3.4" ry="4.6"/><ellipse cx="6" cy="13.4" rx="2.6" ry="3.4"/></g>')
print('map ok')
