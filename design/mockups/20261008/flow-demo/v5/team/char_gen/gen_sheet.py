#!/usr/bin/env python3
"""char_sheet.html (sprite درون‌خطی) + عکس‌ها با Playwright: 390x800، 360x640، خاکستری، اندازه‌ها. اجرا: python3 gen_sheet.py [--shots]"""
import pathlib, sys, json
A = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'character'
SHOTS = pathlib.Path(__file__).resolve().parent.parent / 'shots_char'
sprite = (A / 'sprite_char.svg').read_text(encoding='utf-8').replace('<svg xmlns="http://www.w3.org/2000/svg">', '<svg xmlns="http://www.w3.org/2000/svg" width="0" height="0" style="position:absolute">')
css = (A / 'char.css').read_text(encoding='utf-8')
IDS = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8']
STATES = ['happy', 'thinking', 'surprised', 'oops']
POSES = ['stand', 'walk1', 'walk2', 'jump', 'point', 'sit']
BG = {'grass': '#7fbf4a', 'space': '#7a5cd0', 'night': '#190539'}

def use(cid, st, size, cls='', pose=None):
    full = cid == 'b1' and pose
    kind = 'full' if full else 'bust'
    H = 150 if full else 100
    w = size * 100 / H if full else size
    csz = f'cs-{kind}-{size}'
    pc = f' ch-pose-{pose}' if pose else ''
    return f'<svg class="{csz}" width="{w:.0f}" height="{size}" viewBox="0 0 100 {H}"><use href="#ch-{cid}" class="ch-{st}{pc}"/></svg>'

def card(inner, lab): return f'<figure><div class="c">{inner}</div><figcaption>{lab}</figcaption></figure>'

body = []
for bg, col in BG.items():
    body.append(f'<h2>{bg}</h2><div class="grid" style="background:{col}">')
    for cid in IDS:
        for st in STATES + (['calm'] if cid == 'b8' else []):
            body.append(card(use(cid, st, 82), f'{cid} {st}'))
    body.append('</div>')
body.append('<h2>b1 poses (110px، حالت happy/thinking)</h2><div class="grid" style="background:#7fbf4a">')
for p in POSES:
    body.append(card(use('b1', 'happy' if p != 'point' else 'thinking', 110, pose=p), p))
body.append('</div><h2>sizes (140 / 82 / 64 / 56) روی چمن و شب</h2>')
for bg in ('grass', 'night'):
    body.append(f'<div class="row" style="background:{BG[bg]}">')
    for cid in IDS:
        for s in (140, 82, 64, 56):
            body.append(use(cid, 'happy', s))
    body.append('</div>')
html = f'''<!doctype html><html lang="fa" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>char_sheet</title>
<style>{css}
body{{margin:0;font:14px Vazirmatn,sans-serif;background:#fff4d2;color:#241a5e;padding:8px}}h2{{margin:14px 6px 4px}}
.grid{{display:flex;flex-wrap:wrap;gap:6px;padding:8px;border-radius:12px}}figure{{margin:0}}.c{{padding:2px}}figcaption{{font-size:12px;color:#fff4d2;text-align:center;direction:ltr}}
.row{{display:flex;flex-wrap:wrap;align-items:flex-end;gap:6px;padding:8px;border-radius:12px}}</style>
<body>{sprite}{"".join(body)}</body></html>'''
(A / 'char_sheet.html').write_text(html, encoding='utf-8')
print('sheet', len(html) // 1024, 'KB')

if '--shots' in sys.argv:
    from playwright.sync_api import sync_playwright
    SHOTS.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for (w, h, nm) in ((390, 800, 'm390x800'), (360, 640, 'm360x640')):
            pg = b.new_page(viewport={'width': w, 'height': h}); msgs = []
            pg.on('console', lambda m: msgs.append(m.text)); pg.on('pageerror', lambda e: msgs.append(str(e)))
            pg.goto((A / 'char_sheet.html').as_uri()); pg.screenshot(path=str(SHOTS / f'sheet_{nm}.png'), full_page=False)
            pg.screenshot(path=str(SHOTS / f'sheet_{nm}_full.png'), full_page=True)
            print(nm, 'console:', msgs)
        pg = b.new_page(viewport={'width': 390, 'height': 800}); pg.goto((A / 'char_sheet.html').as_uri())
        pg.add_style_tag(content='svg{filter:grayscale(1)} body{filter:grayscale(1)}'); pg.screenshot(path=str(SHOTS / 'sheet_gray.png'), full_page=True)
        b.close()
