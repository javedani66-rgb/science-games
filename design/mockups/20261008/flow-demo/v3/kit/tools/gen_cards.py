from kitlib import *
W,H=168,224
def rivets(pts,r=3):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#gold)" stroke="{LINE}" stroke-width="1.2"/><circle cx="{x-.8}" cy="{y-.8}" r="{r*.35:.1f}" fill="#fff" opacity=".7"/>' for x,y in pts)
RV=[(10,10),(158,10),(10,214),(158,214)]
# card frame: opening for art is cut (evenodd) so art sits behind
art=(16,54,136,108)   # x,y,w,h
d=GOLD_GRAD+SHADOW+f'<linearGradient id="tp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f7a73"/><stop offset="1" stop-color="{INK}"/></linearGradient><linearGradient id="cp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fffaf0"/><stop offset="1" stop-color="#f1d99c"/></linearGradient>'
ax,ay,aw,ah=art
b=(f'<path fill-rule="evenodd" d="M16,2 H152 a14,14 0 0 1 14,14 V208 a14,14 0 0 1 -14,14 H16 a14,14 0 0 1 -14,-14 V16 a14,14 0 0 1 14,-14Z M{ax+10},{ay} H{ax+aw-10} a10,10 0 0 1 10,10 V{ay+ah-10} a10,10 0 0 1 -10,10 H{ax+10} a10,10 0 0 1 -10,-10 V{ay+10} a10,10 0 0 1 10,-10Z" fill="url(#gold)" stroke="{LINE}" stroke-width="3"/>'
   f'<path fill-rule="evenodd" d="M16,8 H152 a8,8 0 0 1 8,8 V208 a8,8 0 0 1 -8,8 H16 a8,8 0 0 1 -8,-8 V16 a8,8 0 0 1 8,-8Z M{ax+10},{ay} H{ax+aw-10} a10,10 0 0 1 10,10 V{ay+ah-10} a10,10 0 0 1 -10,10 H{ax+10} a10,10 0 0 1 -10,-10 V{ay+10} a10,10 0 0 1 10,-10Z" fill="none" stroke="{LINE}" stroke-opacity=".35" stroke-width="1.5"/>'
   f'<rect x="{ax-1}" y="{ay-1}" width="{aw+2}" height="{ah+2}" rx="11" fill="none" stroke="{LINE}" stroke-width="2.4" opacity=".75"/>'
   f'<rect x="22" y="14" width="124" height="36" rx="10" fill="{LINE}" opacity=".5"/><rect x="22" y="12.5" width="124" height="36" rx="10" fill="url(#tp)" stroke="{GOLD_L}" stroke-width="1.6"/>'
   f'<rect x="22" y="170" width="124" height="44" rx="10" fill="{LINE}" opacity=".45"/><rect x="22" y="168.5" width="124" height="44" rx="10" fill="url(#cp)" stroke="{GOLD_D}" stroke-width="1.8"/>'
   f'<circle cx="84" cy="168" r="11" fill="url(#gold)" stroke="{LINE}" stroke-width="2"/><circle cx="84" cy="168" r="6.5" fill="{INK}" stroke="{LINE}" stroke-width="1.4" id="seal"/>'
   +rivets(RV)+rivets([(28,19),(140,19),(28,206),(140,206)],2.2))
svg('card-frame.svg',W,H,b,d)
# card back
d=GOLD_GRAD+f'<pattern id="lat" width="24" height="24" patternUnits="userSpaceOnUse"><rect width="24" height="24" fill="#1f5a56"/><path d="M12,0 L24,12 L12,24 L0,12Z" fill="none" stroke="#3b8d84" stroke-width="1.6" opacity=".7"/><circle cx="12" cy="12" r="2" fill="{GOLD}" opacity=".6"/></pattern><radialGradient id="mc" cx=".4" cy=".3" r=".9"><stop offset="0" stop-color="#2f7a73"/><stop offset="1" stop-color="{INK2}"/></radialGradient>'
b=(f'<rect x="2" y="2" width="164" height="220" rx="14" fill="url(#gold)" stroke="{LINE}" stroke-width="3"/><rect x="9" y="9" width="150" height="206" rx="9" fill="url(#lat)" stroke="{LINE}" stroke-width="2.4"/>'
   f'<rect x="15" y="15" width="138" height="194" rx="6" fill="none" stroke="{GOLD_L}" stroke-width="1.6" opacity=".8"/>'
   f'<circle cx="84" cy="112" r="40" fill="url(#gold)" stroke="{LINE}" stroke-width="2.6"/><circle cx="84" cy="112" r="33" fill="url(#mc)" stroke="{LINE}" stroke-width="2"/>'
   +gear(84,112,24,10,GOLD,ln=LINE,lw=2,hole=.3)+star4(84,112,15,CREAM).replace('/>',f' stroke="{LINE}" stroke-width="1.6"/>')+f'<circle cx="84" cy="112" r="3.4" fill="{INK}"/>'
   +rivets(RV))
svg('card-back.svg',W,H,b,d)
# empty slot (not yet found): dashed outline on recess
d=f'<linearGradient id="rc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2e1c0b"/><stop offset="1" stop-color="#4a2f14"/></linearGradient>{GOLD_GRAD}'
sil=f'<rect x="22" y="14" width="124" height="36" rx="9" fill="#fff" opacity=".07"/><rect x="16" y="54" width="136" height="108" rx="11" fill="#fff" opacity=".06"/><rect x="22" y="170" width="124" height="44" rx="10" fill="#fff" opacity=".07"/>'
b=(f'<rect x="2" y="2" width="164" height="220" rx="14" fill="url(#rc)" stroke="{LINE}" stroke-width="3"/><rect x="2" y="2" width="164" height="30" rx="14" fill="#000" opacity=".28"/>{sil}'
   f'<rect x="8" y="8" width="152" height="208" rx="10" fill="none" stroke="{GOLD}" stroke-width="2.4" stroke-dasharray="9 7" stroke-linecap="round" opacity=".75"/>')
svg('card-slot-empty.svg',W,H,b,d)
# recess (plain) for any card
b=(f'<rect x="2" y="2" width="164" height="220" rx="14" fill="url(#rc)" stroke="{LINE}" stroke-width="3"/><rect x="2" y="2" width="164" height="26" rx="14" fill="#000" opacity=".3"/><rect x="2" y="196" width="164" height="26" rx="14" fill="#fff" opacity=".05"/>')
svg('pocket.svg',W,H,b,d)
# shelf board (wood plank, tile horizontally)
d='<filter id="g" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".008 .5" numOctaves="3" seed="6" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .25  0 0 0 0 .13  0 0 0 0 .03  0 0 0 .6 -.1"/></filter><linearGradient id="wb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c58a4c"/><stop offset=".5" stop-color="#a86f35"/><stop offset="1" stop-color="#7d4d22"/></linearGradient>'
b=(f'<rect width="240" height="36" fill="url(#wb)"/><rect width="240" height="36" filter="url(#g)"/><rect width="240" height="4" fill="#f1c88a" opacity=".75"/><rect y="4" width="240" height="2" fill="#6d4a18" opacity=".35"/><rect y="32" width="240" height="4" fill="#2a1a08" opacity=".45"/><rect y="0" width="240" height="1.5" fill="{LINE}"/>')
svg('shelf-board.svg',240,36,b,d)
svg('shelf-back.svg',240,240,f'<filter id="g" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".5 .01" numOctaves="3" seed="2" stitchTiles="stitch"/><feColorMatrix values="0 0 0 0 .1  0 0 0 0 .05  0 0 0 0 0  0 0 0 .45 -.05"/></filter><rect width="240" height="240" fill="#4b2f15"/><rect width="240" height="240" filter="url(#g)"/><path d="M0,0 V240 M80,0 V240 M160,0 V240" stroke="#1d1005" stroke-width="2" opacity=".55"/>')
print('cards ok')
