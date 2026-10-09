#!/usr/bin/env python3
"""card_sheet.html + عکس‌ها + سنجش سطح گرم. اجرا پس از gen_card.py:  python3 gen_sheet.py [--shots]"""
import json, pathlib, re, sys
HERE = pathlib.Path(__file__).resolve().parent
A = HERE.parent / 'assets'; OUT = A / 'card'
FLOW = HERE.parents[2]
ST = json.load(open(FLOW / 'strings.fa.json', encoding='utf-8'))
ST.update(json.load(open(FLOW / 'v5/strings.fa.json', encoding='utf-8')))
def T(k): return ST[k]['text']
ui_sprite = (A / 'ui/sprite_ui.svg').read_text(encoding='utf-8')
ch_sprite = (A / 'character/sprite_char.svg').read_text(encoding='utf-8')
cd_sprite = (OUT / 'sprite_card.svg').read_text(encoding='utf-8') + (OUT / 'scene/sprite_scene.svg').read_text(encoding='utf-8')
tokens = (A / 'light/tokens.css').read_text(encoding='utf-8')
def inner(s): return re.sub(r'<svg[^>]*>|</svg>', '', s.strip())
sprites = f'<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute" aria-hidden="true">{inner(ui_sprite)}{inner(ch_sprite)}{inner(cd_sprite).replace('</svg><svg xmlns="http://www.w3.org/2000/svg">','')}</svg>'
FONTS = '''@font-face{font-family:Lalezar;src:url(../../../../../../../../assets/fonts/Lalezar-Regular.woff2) format("woff2")}
@font-face{font-family:Vazirmatn;font-weight:400;src:url(../../../../../../../../assets/fonts/Vazirmatn-Regular.woff2) format("woff2")}
@font-face{font-family:Vazirmatn;font-weight:700;src:url(../../../../../../../../assets/fonts/Vazirmatn-Bold.woff2) format("woff2")}'''
def badge(k): return f'<svg class="ui-badge" aria-hidden="true"><use href="#ui-badge-{k}"/></svg>'
def diff(k, cls='cd-diff'): return f'<span class="{cls}">{badge(k)}<span>{T("difficulty." + k)}</span></span>'
def art_inline(k): return f'<svg viewBox="0 0 360 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><use href="#cd-art-harbor-{k}"/></svg>'
def tbar(): return '<svg class="cd-tbar" viewBox="0 0 360 60" preserveAspectRatio="none" aria-hidden="true"><use href="#cd-title-bar"/></svg>'
def frame(): return '<svg class="cd-frame" viewBox="0 0 390 392" preserveAspectRatio="none" aria-hidden="true"><use href="#cd-frame-night"/></svg>'
guide = '''<svg class="cd-guide" viewBox="0 0 100 92" aria-hidden="true"><g class="cs-bust-64 ch-pose-point"><use class="ch-happy" href="#ch-b1"/></g></svg>'''
def front(k, d, title, sent, with_guide=False):
    return (f'<section class="cd-front" aria-label="{title}">{frame()}{tbar()}{diff(d)}<div class="cd-title">{title}</div>'
            f'<div class="cd-art">{art_inline(k)}</div><svg class="cd-ib" viewBox="0 0 334 150" preserveAspectRatio="none" aria-hidden="true"><use href="#cd-image-border"/></svg>'
            f'<div class="cd-sentence">{sent}</div><div class="cd-go"><button class="ui-btn cd-btn-practice">{T("flow.env.start")}</button></div>{guide if with_guide else ""}</section>')
def strip(d, title):
    return (f'<div class="cd-strip" role="button" tabindex="0" data-world="night"><svg class="cd-bg" viewBox="0 0 360 56" preserveAspectRatio="none" aria-hidden="true"><use href="#cd-stack-strip"/></svg>'
            f'{diff(d)}<span class="cd-t">{title}</span></div>')
G, O, R = 'flow.harbor.green', 'flow.harbor.orange', 'flow.harbor.red'
topbar = f'<div class="cd-top" style="block-size:64px;display:flex;align-items:center;justify-content:space-between;padding:0 16px"><button class="ui-btn ui-btn--s ui-btn--sec">{T("flow.menu.open")}</button></div>'
bottom = f'<div class="cd-bot" style="block-size:56px;display:flex;align-items:center;padding:0 16px"><button class="ui-btn ui-btn--sec" style="inline-size:100%">{T("flow.menu.back")}</button></div>'
v_stack = f'''<div class="cd-view" id="v-stack" data-world="night">{topbar}<div class="cd-stack">{strip("hard", T(R + ".title"))}{strip("mid", T(O + ".title"))}{front("day", "easy", T(G + ".title"), T(G + ".ready"), True)}</div>{bottom}</div>'''
v_stack2 = f'''<div class="cd-view" id="v-stack2" data-world="night">{topbar}<div class="cd-stack">{strip("hard", T(R + ".title"))}{front("dusk", "mid", T(O + ".title"), T(O + ".ready"), True)}{strip("easy", T(G + ".title"))}</div>{bottom}</div>'''
v_stack3 = f'''<div class="cd-view" id="v-stack3" data-world="night">{topbar}<div class="cd-stack">{front("night", "hard", T(R + ".title"), T(R + ".ready"), True)}{strip("mid", T(O + ".title"))}{strip("easy", T(G + ".title"))}</div>{bottom}</div>'''
v_back = f'''<div class="cd-view" id="v-back" data-world="night">{topbar}<div class="cd-stack"><section class="cd-back">{frame()}<div class="cd-title">{T("flow.card.back.title")}</div>
<div class="cd-diagram"><svg viewBox="0 0 360 200" aria-hidden="true"><use href="#cd-back-pulley-diagram"/></svg></div>
<button class="ui-btn cd-btn-practice">{T("flow.menu.practice")}</button><button class="ui-btn cd-btn-film">{T("flow.card.video.h")}</button><button class="ui-btn cd-btn-box">{T("flow.box.put")}</button></section></div>{bottom}</div>'''
def mini(k, lbl, thumb=True):
    th = f'<div class="cd-th"><svg viewBox="0 0 360 240" preserveAspectRatio="xMidYMid slice" aria-hidden="true" style="inline-size:100%;block-size:100%"><use href="#cd-art-harbor-day"/></svg></div>' if thumb else ''
    return f'<div class="cd-mini"><svg viewBox="0 0 80 120" aria-hidden="true"><use href="#cd-mini-{k}"/></svg>{th}<span class="cd-lbl">{lbl}</span></div>'
v_shelf = f'''<div class="cd-view" id="v-shelf" data-world="night">{topbar}<h1 style="font:400 28px/1.2 Lalezar,Vazirmatn;text-align:center;margin:8px 0 12px;color:#fff4d2;text-shadow:0 0 12px #5fa8d6">{T("flow.box.title")}</h1>
<div class="cd-shelfrow">{mini("seen", T("flow.box.seen"))}{mini("packed", T("flow.box.collected"))}{mini("empty", "", False)}{mini("locked", "", False)}</div>
<svg class="cd-shelf-svg" viewBox="0 0 360 40" aria-hidden="true"><use href="#cd-shelf"/></svg></div>'''
def scn(name, extra=''):
    return f'''<div class="cd-view cd-scene" id="v-{name}"><div class="cd-sbar"><button class="ui-btn ui-btn--s ui-btn--sec">{T("flow.menu.open")}</button><b>{T("flow.scene.mission")}</b></div>
<svg viewBox="0 0 390 500" class="cd-sc" aria-hidden="true"><use href="#cd-{name}"/></svg>
<div class="ui-sheet cd-sheet"><div class="cd-row"><button class="ui-btn ui-btn--sec">{T("flow.scene.arr.fixed")}</button><button class="ui-btn ui-btn--sec">{T("flow.scene.arr.moving")}</button></div><button class="ui-btn" style="inline-size:100%;margin-block-start:8px">{T("flow.scene.pull")}</button></div></div>'''
scenes = ''.join(scn(k) for k in ('harbor-scene-green', 'harbor-scene-orange', 'harbor-scene-orange-dusk', 'harbor-scene-red', 'harbor-scene-red-night'))
css_scene = '''.cd-scene{background:#fff4d2;color:#241a5e;min-block-size:100%}.cd-sbar{display:flex;align-items:center;gap:10px;padding:8px 16px;min-block-size:56px;box-sizing:border-box;font:700 16px/1.4 Vazirmatn}
.cd-sc{display:block;inline-size:100%;block-size:auto;max-block-size:58vh;margin:0 auto}.cd-row{display:flex;gap:8px}.cd-row .ui-btn{flex:1}.cd-sheet{border-radius:0}
.cd-view{display:none}body[data-v="all"] .cd-view{display:block;margin-block-end:30px;border-bottom:2px dashed #5fa8d6}'''
nightbg = 'body{margin:0;background:#190539;color:#fff4d2;font-family:Vazirmatn,sans-serif}body.day{background:#fff4d2;color:#241a5e}'
html = f'''<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>برگهٔ کارت و صحنهٔ اسکله</title>
<style>{FONTS}
{tokens}
</style><link rel="stylesheet" href="../ui/ui_tokens.css"><link rel="stylesheet" href="card.css">
<style>{nightbg}{css_scene}</style></head><body data-v="stack">{sprites}
{v_stack}{v_stack2}{v_stack3}{v_back}{v_shelf}{scenes}
<script>
function show(){{var h=(location.hash||'#stack').slice(1);document.body.dataset.v=h;document.body.classList.toggle('day',h.indexOf('harbor')===0);
 document.querySelectorAll('.cd-view').forEach(function(v){{v.style.display=(h==='all'||v.id==='v-'+h)?'block':'none'}});}}
addEventListener('hashchange',show);show();
</script></body></html>'''
(OUT / 'card_sheet.html').write_text(html, encoding='utf-8')
print('sheet KB', round(len(html.encode()) / 1024, 1))
if '--shots' in sys.argv:
    from playwright.sync_api import sync_playwright
    SH = OUT / 'shots'; SH.mkdir(exist_ok=True)
    views = ['stack', 'stack2', 'stack3', 'back', 'shelf', 'harbor-scene-green', 'harbor-scene-orange', 'harbor-scene-orange-dusk', 'harbor-scene-red', 'harbor-scene-red-night']
    with sync_playwright() as p:
        b = p.chromium.launch()
        for rm in (False, True):
            for w, h in ((390, 800), (360, 640)):
                pg = b.new_page(viewport={'width': w, 'height': h}, reduced_motion='reduce' if rm else 'no-preference'); errs = []
                pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
                for v in views:
                    if rm and v not in ('stack', 'back'): continue
                    pg.goto((OUT / 'card_sheet.html').as_uri() + '#' + v); pg.wait_for_timeout(350)
                    ov = pg.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
                    full = v.startswith('harbor')
                    pg.screenshot(path=str(SH / f'card_{v}_{w}x{h}{"_rm" if rm else ""}.png'), full_page=full)
                    print(w, h, v, 'rm' if rm else '', 'hscroll', ov, 'errs', errs[:2])
                pg.close()
        b.close()
    from PIL import Image
    for f in list(SH.glob('card_*_390x800.png')) + list(SH.glob('card_*_360x640.png')):
        Image.open(f).convert('L').save(SH / (f.stem + '_gray.png'))
