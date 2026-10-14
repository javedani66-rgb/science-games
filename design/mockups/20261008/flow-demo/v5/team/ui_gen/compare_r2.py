import pathlib, json, io
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
HERE = pathlib.Path(__file__).resolve().parent
UI = HERE.parent / 'assets_r2/ui'; SH = UI / 'shots'
V4 = HERE.parents[2] / 'v4/style'
S = {}
for f in (HERE.parents[2] / 'strings.fa.json', HERE.parents[1] / 'strings.fa.json'):
    S.update(json.load(open(f, encoding='utf-8')))
t = lambda k: S[k]['text']
css = (UI / 'ui_tokens.css').read_text(encoding='utf-8')
sprite = (UI / 'sprite_ui.svg').read_text(encoding='utf-8')
def use(i, c): return f'<svg class="{c}" aria-hidden="true"><use href="#{i}"/></svg>'
def chip(k, on): return (f'<button class="ui-chip" aria-pressed="{str(on).lower()}"><svg class="ui-tick" aria-hidden="true"><use href="#ui-check"/></svg><small>{t("v5.ui.base.label")}</small><b><bdi dir="rtl">{t("v5.ui.base."+k)}</bdi></b></button>')
def hard(k): return f'<span class="ui-hard">{use("ui-badge-"+k,"ui-badge")}<span>{t("difficulty."+k)}</span></span>'
menu = f'<button class="ui-btn ui-btn--icon" aria-label="{t("flow.menu.open")}"><svg class="ui-gear"><use href="#ui-gearbtn"/></svg><svg class="ui-ic"><use href="#ui-ic-menu"/></svg></button>'
topbar = f'<div class="ui-topbar" style="position:absolute;top:0;left:0;right:0;z-index:20">{menu}<div class="ui-chips">{chip("b12",False)}{chip("b34",True)}{chip("b56",False)}</div></div>'
panel = (f'<div class="ui-sheet" style="position:absolute;left:0;right:0;bottom:0;z-index:20"><div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">{hard("easy")}{hard("mid")}{hard("hard")}</div>'
         f'<div style="display:flex;gap:10px;align-items:center;margin-bottom:10px">{use("ui-lock","ui-lockbadge")}<span class="ui-plate ui-cut ui-plate--16">{t("flow.lock.reason").format(name=t("flow.menu.map"))}</span></div>'
         f'<div style="display:flex;gap:12px;flex-wrap:wrap"><button class="ui-btn">{t("flow.lock.go")}</button><button class="ui-btn ui-btn--sec ui-cut">{t("flow.menu.back")}</button><button class="ui-btn ui-btn--video">{t("v5.ui.state.video")}</button></div></div>')
INJ_MAP = """([css,sprite,topbar,panel])=>{const s=document.createElement('style');s.textContent=css+'.ui-topbar{padding-top:8px}';document.head.appendChild(s);
 const d=document.createElement('div');d.style.cssText='position:absolute;width:0;height:0;overflow:hidden';d.innerHTML=sprite;document.body.appendChild(d);
 document.getElementById('bar').style.display='none';const w=document.createElement('div');w.dir='rtl';w.innerHTML=topbar+panel;w.style.cssText='position:absolute;inset:0;pointer-events:none;z-index:30';w.querySelectorAll('*').forEach(e=>e.style.pointerEvents='auto');document.getElementById('phone').appendChild(w)}"""
night_btns = {'cyan': t('flow.menu.practice'), 'pink': t('v5.ui.state.video'), 'gold': t('flow.box.put')}
INJ_NIGHT = """([css,sprite,labels])=>{const s=document.createElement('style');s.textContent=css+'.ui-btn{position:absolute;left:26px;right:26px;font-size:30px;min-block-size:64px;border-radius:20px;margin:0}';document.head.appendChild(s);
 const d=document.createElement('div');d.style.cssText='position:absolute;width:0;height:0;overflow:hidden';d.innerHTML=sprite;document.body.appendChild(d);
 const ps=[...document.querySelectorAll('[data-v=back] .pill')];const cls=['','ui-btn--video','ui-btn--gold'];const tops=['332px','418px','520px'];
 ps.forEach((p,i)=>{const b=document.createElement('button');b.className='ui-btn '+cls[i];b.innerHTML='<svg class="ui-svg ui-svg--32" style="flex:none"><use href="#ui-ic-'+['game','play','box'][i]+'"/></svg>'+labels[i];b.style.top=tops[i];if(i==2)b.style.minBlockSize='72px';b.setAttribute('data-world','night');p.replaceWith(b)})}"""
def shot(b, w, h, page, q, inj, args):
    pg = b.new_page(viewport={'width': 390, 'height': 800})
    pg.goto((V4 / page).as_uri() + q); pg.wait_for_timeout(500)
    old = pg.screenshot()
    if inj:
        pg.evaluate(inj, args); pg.wait_for_timeout(500)
    new = pg.screenshot()
    pg.close()
    return Image.open(io.BytesIO(old)), Image.open(io.BytesIO(new))
def fit(im, w, h):
    if (w, h) == (390, 800): return im
    s = w / 390
    return im.resize((w, round(800 * s))).crop((0, 0, w, h))
def pair(a, b, w, h, path):
    a, b = fit(a, w, h), fit(b, w, h)
    can = Image.new('RGB', (w * 2 + 20, h + 30), '#ffffff')
    can.paste(a, (0, 30)); can.paste(b, (w + 20, 30))
    dr = ImageDraw.Draw(can); dr.text((6, 8), 'v4', fill='black'); dr.text((w + 26, 8), 'new r2', fill='black')
    can.save(path); can.convert('L').save(str(path).replace('.png', '_gray.png'))
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--no-sandbox'])
    mo, mn = shot(b, 390, 800, 'map.html', '?y=0', INJ_MAP, [css, sprite, topbar, panel])
    no, nn = shot(b, 390, 800, 'card-night.html', '?v=back', INJ_NIGHT, [css, sprite, [night_btns['cyan'], night_btns['pink'], night_btns['gold']]])
    b.close()
for (w, h) in ((390, 800), (360, 640)):
    pair(mo, mn, w, h, SH / f'compare_map_{w}.png')
    pair(no, nn, w, h, SH / f'compare_night_{w}.png')
print('done')
