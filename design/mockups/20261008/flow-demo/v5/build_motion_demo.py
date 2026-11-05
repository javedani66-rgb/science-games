"""ساخت v5/motion_demo.html: قالب + فونت‌ها + رنگ‌ها (component_spec.json) + قاب کارت (team/assets_r2/card) + متن‌ها (strings.fa.json).
اجرا: python3 v5/build_motion_demo.py"""
import json, base64, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
A = HERE / 'team/assets_r2'
b64 = lambda b: base64.b64encode(b).decode()
fonts = ''.join(f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64((ROOT / 'assets/fonts' / f).read_bytes())}) format('woff2')}}"
                for fam, w, f in (('Vazirmatn', 400, 'Vazirmatn-Regular.woff2'), ('Vazirmatn', 700, 'Vazirmatn-Bold.woff2'), ('Lalezar', 400, 'Lalezar-Regular.woff2')))
spec = json.load(open(HERE / 'component_spec.json', encoding='utf-8'))
pal = ''.join(f"  --{k}:{v};\n" for k, v in spec['palette'].items())
S = {k: v['text'] for k, v in json.load(open(HERE / 'strings.fa.json', encoding='utf-8')).items()}
S.update({k: v['text'] for k, v in json.load(open(HERE.parent / 'strings.fa.json', encoding='utf-8')).items() if k.startswith(('flow.harbor', 'flow.env.start', 'flow.nav.toMap', 'flow.map.here'))})
need = {k: S[k] for k in S if k.startswith(('motion.demo', 'difficulty.', 'flow.harbor', 'flow.env.start', 'flow.nav.toMap', 'flow.map.here'))}
html = (HERE / 'motion_demo.tpl.html').read_text(encoding='utf-8')
html = (html.replace('/*__FONTS__*/', fonts)
        .replace('/*__TOKENS__*/', (A / 'ui/ui_tokens.css').read_text(encoding='utf-8'))
        .replace('/*__CARDCSS__*/', (A / 'card/card.css').read_text(encoding='utf-8'))
        .replace('/*__PALETTE__*/', pal)
        .replace('<!--__SPRITE_CARD__-->', (A / 'card/sprite_card.svg').read_text(encoding='utf-8'))
        .replace('<!--__SPRITE_UI__-->', (A / 'ui/sprite_ui.svg').read_text(encoding='utf-8'))
        .replace('/*__STRINGS__*/{}', json.dumps(need, ensure_ascii=False)))
(HERE / 'motion_demo.html').write_text(html, encoding='utf-8')
print('motion_demo.html', len(html) // 1024, 'KB; strings', len(need))
