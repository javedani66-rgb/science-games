import re
from common import *
m = open(os.path.join(STYLE, 'map.html')).read()
svg = re.search(r'<svg id="map".*?</svg>', m, re.S).group(0)
# فقط یک نسخهٔ نقشه را اینجا نگه می‌داریم و سه بار با use نشان می‌دهیم تا حجم کم شود
inner = svg
hero = img_uri('b1.png', 'image/png')
Y0 = 40
frame_tpl = '''<div class="fr {cls}"><div class="mapbox">{svg}</div>{over}<span class="tag"><span class="ph" data-ph="{ph}"></span></span></div>'''
stars = ''.join('<i style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;opacity:%.2f"></i>' % (a, b, r, r, o) for a, b, r, o in
                [(20,14,3,.9),(70,40,2,.7),(120,16,2,.8),(165,52,3,.9),(215,12,2,.7),(262,36,3,.9),(310,18,2,.8),(354,50,2,.7),(40,80,2,.6),(340,92,3,.8),(98,70,2,.6),(240,70,2,.6)])
lights = ''.join('<b style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></b>' % (x - r, y - r, 2 * r, 2 * r) for x, y, r in [(53, 116, 9), (67, 116, 9)])
frames = [
 frame_tpl.format(cls='f0', svg=inner, over='', ph='day'),
 frame_tpl.format(cls='f1', svg=inner, over='<div class="dusk"></div><div class="sun"></div>', ph='f1'),
 frame_tpl.format(cls='f2', svg=inner, over='<div class="night"></div><div class="stars">%s</div><div class="moon"></div><div class="lights">%s</div><div class="minicard"></div>' % (stars, lights), ph='f2'),
]
css = '''
*{box-sizing:border-box;margin:0}
html,body{width:390px;height:800px;overflow:hidden;background:#190539;font-family:Vazirmatn}
.sheet{display:flex;flex-direction:column;gap:12px;padding:12px 0}
.fr{position:relative;width:390px;height:250px;overflow:hidden;border-block:4px solid #241a5e}
.mapbox{position:absolute;left:0;top:-%dpx;width:390px;height:2400px}
.mapbox svg{display:block}
.fr>div{position:absolute;inset:0}
.fr>.mapbox{inset:auto;left:0;top:-%dpx;width:390px;height:2400px}
.tag{position:absolute;left:10px;top:10px;z-index:9;background:#241a5e;color:#fff3c4;font:22px/1 Lalezar;padding:6px 14px;border-radius:12px;border:3px solid #fff3c4}
.dusk{background:linear-gradient(#ff7a3d,#c2379a 70%%,#5a2a9a);mix-blend-mode:multiply;opacity:.72}
.sun{background:radial-gradient(circle at 18%% 8%%,#ffd16a 0,#ff9a4a 14%%,transparent 40%%);mix-blend-mode:screen;opacity:.85}
.night{background:linear-gradient(#6a55d8,#3a1c90);mix-blend-mode:multiply;opacity:.8}
.stars i{position:absolute;border-radius:50%%;background:#fff}
.moon{background:radial-gradient(circle at 90%% 14%%,#fff6c8 0 3.4%%,transparent 4%%);}
.lights b{position:absolute;border-radius:50%%;background:radial-gradient(#fff3a8,#ffd23faa 50%%,transparent 72%%);mix-blend-mode:screen}
.lights{mix-blend-mode:normal}
.minicard{inset:auto 14px -34px auto!important;width:116px;height:150px;border-radius:14px;border:4px solid #190539;background:linear-gradient(#25cdc0,#0a86a4);box-shadow:0 0 22px #46f0d8,inset 0 0 0 4px #ffd23f;transform:rotate(-7deg)}
''' % (Y0, Y0)
css = css.replace('.mapbox{position:absolute;left:0;top:-%dpx', '.mapbox{position:absolute;left:0;top:-%dpx')
body = '<div class="sheet">%s</div>' % ''.join(frames)
open(os.path.join(STYLE, 'transition.html'), 'w').write(page('transition', css, body, ''))
