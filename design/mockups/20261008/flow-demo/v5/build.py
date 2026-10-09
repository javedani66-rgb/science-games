#!/usr/bin/env python3
"""خط تولید v5: index.html خودبسته از template.html + دادهٔ v3 + دارایی هنرمندان (team/assets).
گام ۰ (EXECUTION_ORDER_FA): sprite خام در DOM با پیشوند id یکتا، ادغام tokens.css/ui_tokens.css،
assets.json، و خطای سقف حجم. ظاهر همان v3 است (کیت، داده‌ها، فونت‌ها، پنل #rv).
استفاده:  python3 build.py [--assets DIR] [--out-dir DIR] [--placeholder] [--no-write]
پیام‌های فارسی: v5/strings.fa.json (کلیدهای v5.build.*)."""
import json, base64, pathlib, io, re, sys, argparse

HERE = pathlib.Path(__file__).resolve().parent          # flow-demo/v5
FLOW = HERE.parent                                       # flow-demo
V3 = FLOW / 'v3'
ROOT = HERE.parents[4]
KB = 1024
PAGE_CAP = int(2.5 * 1024 * KB)                          # سقف صفحهٔ نهایی ۲٫۵MB
MODULES = {  # پوشهٔ هنرمند: (بودجهٔ خام بایت، پیشوند شناسهٔ مجاز)
    'env': (700 * KB, ('env', 'n', 'node', 'prop', 'zb')), 'character': (300 * KB, ('ch', 'b')),
    'ui': (200 * KB, ('ui',)), 'card': (500 * KB, ('cd', 'sc')), 'light': (50 * KB, ('lt',))}
MODULE_ALIAS = {'scene': 'card', 'characters': 'character', 'chars': 'character'}
SVG_CAP, BIG_CAP = 40 * KB, 25 * KB                      # هر SVG؛ بنا و b1
BIG_RE = re.compile(r'^(node_?\d|n\d{2}|b1$|b1[-_])')
SYMRE = re.compile(r'<symbol\b([^>]*?)/>|<symbol\b([^>]*)>(.*?)</symbol>', re.S)
SKIP_RE = re.compile(r'(_sheet|^palette_)')
STR = json.load(open(HERE / 'strings.fa.json', encoding='utf-8'))
def msg(key, **kw): return STR[key]['text'].format(**kw)
def slug(s): return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')

def _sub_ids(text, mp):
    """همهٔ ارجاع‌ها به id (id=، url(#)، href=، #id در style) را طبق نگاشت mp عوض می‌کند."""
    text = re.sub(r'(\bid=")([^"]+)(")', lambda m: m.group(1) + mp.get(m.group(2), m.group(2)) + m.group(3), text)
    text = re.sub(r'(url\(\s*[\'"]?#)([^)\'"\s]+)', lambda m: m.group(1) + mp.get(m.group(2), m.group(2)), text)
    text = re.sub(r'((?:xlink:)?href=")#([^"]+)(")', lambda m: m.group(1) + '#' + mp.get(m.group(2), m.group(2)) + m.group(3), text)
    def style(m):
        return m.group(1) + re.sub(r'#([A-Za-z_][\w-]*)', lambda k: '#' + mp.get(k.group(1), k.group(1)), m.group(2)) + m.group(3)
    return re.sub(r'(<style[^>]*>)(.*?)(</style>)', style, text, flags=re.S)

def _clean(t):
    t = re.sub(r'<\?xml.*?\?>|<!DOCTYPE[^>]*>', '', t, flags=re.S)
    return re.sub(r'<!--.*?-->', '', t, flags=re.S).strip()

def module_of(path, base):
    top = path.relative_to(base).parts[0]
    return MODULE_ALIAS.get(top, top)

def collect_assets(assets_dir, placeholder=None):
    """می‌خواند، پیشوند می‌زند، سقف‌ها را می‌سنجد. خروجی: dict(errors, warnings, sprite, entries, tokens, sizes)."""
    base = pathlib.Path(assets_dir)
    errs, warns, entries = [], [], []
    sizes = {m: 0 for m in MODULES}
    defs_parts, symbols, owner = [], [], {}               # owner: id -> فایل (برای یافتن تکرار)
    files = sorted(p for p in base.rglob('*') if p.is_file())
    real_svgs = [p for p in files if p.suffix == '.svg' and not p.relative_to(base).parts[0].startswith('_') and not SKIP_RE.search(p.stem) and 'defs' not in p.stem]
    use_ph = placeholder if placeholder is not None else not real_svgs
    seen_mod = set()
    # بودجهٔ پوشه: svg/json/css به‌جز ورقه‌های بازبینی (palette_* و *_sheet)
    for p in files:
        top = p.relative_to(base).parts[0]
        if top.startswith('_') or p.suffix not in ('.svg', '.json', '.css') or SKIP_RE.search(p.stem): continue
        m = module_of(p, base)
        if m in sizes: sizes[m] += p.stat().st_size
        elif m not in seen_mod: seen_mod.add(m); warns.append(msg('v5.build.unknown_module', mod=m))
    for m, (cap, _) in MODULES.items():
        if sizes[m] > cap: errs.append(msg('v5.build.module_over', mod=m, kb=round(sizes[m] / KB, 1), cap=cap // KB))
    # SVGها
    by_dir = {}
    for p in files:
        if p.suffix != '.svg' or SKIP_RE.search(p.stem): continue
        top = p.relative_to(base).parts[0]
        if top.startswith('_') and not (use_ph and top == '_placeholder'): continue
        by_dir.setdefault(p.parent, []).append(p)
    for d, ps in by_dir.items():     # اگر در یک پوشه sprite_*.svg هست، فایل‌های جدا فقط برای بازبینی‌اند (دوبار نیایند)
        has_sprite = any(p.stem.startswith('sprite_') for p in ps)
        for p in ps:
            if has_sprite and not p.stem.startswith('sprite_') and 'defs' not in p.stem: continue
            _read_svg(p, base, errs, warns, defs_parts, symbols, entries, owner)
    # ارجاع‌های بی‌مقصد (سراسری؛ common_defs می‌تواند مقصد فایل‌های دیگر باشد)
    allids = set(owner)
    blob = ''.join(defs_parts) + ''.join(s[1] for s in symbols)
    for m in re.finditer(r'url\(\s*[\'"]?#([^)\'"\s]+)|href="#([^"]+)"', blob):
        i = m.group(1) or m.group(2)
        if i not in allids: errs.append(msg('v5.build.missing_ref', file='sprite', id=i))
    tokens = ''
    for rel in ('light/tokens.css', 'ui/ui_tokens.css', 'ui/tokens.css'):
        f = base / rel
        if f.exists(): tokens += f'/* {rel} */\n' + f.read_text(encoding='utf-8') + '\n'
    sprite = ''
    if defs_parts or symbols:
        sprite = ('<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false" style="position:absolute;width:0;height:0;overflow:hidden">'
                  + ('<defs>' + ''.join(defs_parts) + '</defs>' if defs_parts else '') + ''.join(s[1] for s in symbols) + '</svg>')
    return dict(errors=errs, warnings=warns, sprite=sprite, entries=entries, tokens=tokens, sizes=sizes, placeholder=bool(use_ph and not real_svgs and entries))

def _read_svg(p, base, errs, warns, defs_parts, symbols, entries, owner):
    rel = str(p.relative_to(base)); mod = module_of(p, base)
    raw = p.read_bytes(); stem = slug(p.stem)
    is_sprite, is_defs = p.stem.startswith('sprite_'), 'defs' in p.stem
    if len(raw) > SVG_CAP and not is_sprite: errs.append(msg('v5.build.svg_over', file=rel, kb=round(len(raw) / KB, 1), cap=SVG_CAP // KB))
    elif BIG_RE.search(p.stem) and len(raw) > BIG_CAP: errs.append(msg('v5.build.svg_over', file=rel, kb=round(len(raw) / KB, 1), cap=BIG_CAP // KB))
    try: text = _clean(raw.decode('utf-8'))
    except UnicodeDecodeError as e: errs.append(msg('v5.build.bad_svg', file=rel, why=str(e))); return
    root = re.match(r'<svg\b([^>]*)>(.*)</svg>\s*$', text, flags=re.S)
    if not root: errs.append(msg('v5.build.bad_svg', file=rel, why='svg')); return
    attrs, inner = root.group(1), root.group(2)
    for pat, what in ((r'<script\b', 'script'), (r'(?:href|src)\s*=\s*"(?:https?:)?//', 'external'), (r'url\(\s*[\'"]?https?:', 'external')):
        if re.search(pat, inner, flags=re.I): errs.append(msg('v5.build.forbidden', file=rel, what=what)); return
    for pat, what in (() if is_defs else ((r'mix-blend-mode', 'mix-blend-mode'), (r'<feTurbulence', 'feTurbulence'))):
        if re.search(pat, inner): warns.append(msg('v5.build.live_effect', file=rel, what=what))
    short = {'character': 'ch', 'card': 'cd', 'light': 'lt'}.get(mod, mod)
    okp = {stem, short} | set(MODULES.get(mod, (0, ()))[1]) | {slug(p.stem.replace('sprite_', ''))}
    def newid(i):
        pre = re.split(r'[-_]', i)[0].lower()
        return i if (pre in okp and re.search(r'[-_]', i)) else f'{stem}-{i}'
    ids = re.findall(r'\bid="([^"]+)"', inner)
    mp = {i: newid(i) for i in ids}
    inner = _sub_ids(inner, mp)
    def reg(i, who):
        if i in owner and owner[i] != who: errs.append(msg('v5.build.dup_id', id=i, a=owner[i], b=who))
        owner[i] = who
    if is_defs:
        for i in mp.values(): reg(i, rel)
        d = re.findall(r'<defs>(.*?)</defs>', inner, flags=re.S)
        defs_parts.append(''.join(d) if d else inner)
        entries.append(dict(name=p.stem, type='defs', file=rel, module=mod, bytes=len(raw), ids=sorted(mp.values()))); return
    if is_sprite:
        outside = re.sub(SYMRE, '', inner)
        d = re.findall(r'<defs>(.*?)</defs>', outside, flags=re.S)
        if d: defs_parts.append(''.join(d))
        for m in re.finditer(SYMRE, inner):
            sa = m.group(1) if m.group(1) is not None else m.group(2)
            sid = re.search(r'\bid="([^"]+)"', sa); vb = re.search(r'viewBox="([^"]+)"', sa)
            full = m.group(0); n = len(full.encode())
            if not sid: continue
            if not vb: errs.append(msg('v5.build.no_viewbox', file=f'{rel}#{sid.group(1)}'))
            lim = BIG_CAP if BIG_RE.search(sid.group(1)) else SVG_CAP
            if n > lim: errs.append(msg('v5.build.svg_over', file=f'{rel}#{sid.group(1)}', kb=round(n / KB, 1), cap=lim // KB))
            symbols.append((sid.group(1), full))
            reg(sid.group(1), rel)
            layers = [i for i in re.findall(r'\bid="([^"]+)"', m.group(3) or '')]
            for i in layers: reg(i, rel)
            entries.append(dict(name=sid.group(1), type='symbol', file=rel, module=mod, bytes=n, viewBox=vb.group(1) if vb else None, layers=layers))
        return
    vb = re.search(r'viewBox="([^"]+)"', attrs)
    if not vb:
        w, h = re.search(r'\bwidth="([\d.]+)', attrs), re.search(r'\bheight="([\d.]+)', attrs)
        if not (w and h): errs.append(msg('v5.build.no_viewbox', file=rel)); return
        vbs = f'0 0 {w.group(1)} {h.group(1)}'
    else: vbs = vb.group(1)
    sid = stem
    sym = f'<symbol id="{sid}" viewBox="{vbs}">{inner}</symbol>'
    reg(sid, rel)
    layers = list(mp.values())
    for i in layers: reg(i, rel)
    symbols.append((sid, sym))
    entries.append(dict(name=sid, type='symbol', file=rel, module=mod, bytes=len(raw), viewBox=vbs, layers=layers))

def b64(b): return base64.b64encode(b).decode()

def build_page(art):
    """صفحهٔ v3 + sprite + tokens (همان منطق v3/build.py؛ کیت و داده از v3)."""
    from PIL import Image, ImageDraw
    J = lambda p: json.load(open(p, encoding='utf-8'))
    TITLES = J(ROOT / 'docs/research/world/titles_fa.json'); NODES = J(ROOT / 'docs/research/world/nodes_v2_draft.json')
    THREAD = J(V3 / 'thread.json'); BANK = J(ROOT / 'docs/texts/TEXT_BANK_FA.json')['entries']
    UI = J(FLOW / 'strings.fa.json'); REV = J(FLOW / 'review.fa.json'); KIT = V3 / 'kit'
    SYM = dict(C01='force', C02='friction', C03='multi', C04='weight', C05='energy', C06='machine', C07='lever', C08='slope', C09='wheel', C10='summary')
    FRAMES = [('stadium', 'L1', ['F01', 'F02', 'F03', 'F04']), ('stadium', 'L1', ['F06', 'F07', 'F08', 'F09']),
              ('space', 'L2', ['W01', 'W02', 'F05', 'W03', 'W04']), ('farm', 'LW', ['E01', 'E02', 'E07']), ('city', 'LM', ['M01', 'B01', 'B02']),
              ('city', 'Z1', ['M04', 'M05', 'M06', 'E05']), ('city', 'Z2', ['M03', 'M09', 'M10', 'E03']), ('city', 'Z3', ['M02', 'M07', 'M08', 'M11']),
              ('city', 'LM', ['E06', 'E04'])]
    ORDER = [n['id'] for c in THREAD['chapters'] for n in c['nodes']]
    assert [i for f in FRAMES for i in f[2]] == [i for i in ORDER if i != 'M12'], 'frames != thread'
    pre = ORDER[:ORDER.index('M07')]
    mid_v = [i for i in pre if i != 'E05']
    mid_c = ['F01', 'F02', 'F03', 'F06', 'F08', 'W01', 'W02', 'F05', 'E01', 'M01', 'B01', 'M04', 'M05']
    mid_s = [i for i in mid_v if i not in mid_c and i not in ('F04', 'E07', 'M02')]
    end_v = [i for i in ORDER if i not in ('E06', 'E04', 'M12')]
    end_c = [i for i in end_v if i not in ('F04', 'F07', 'E07', 'M06', 'M10', 'M11', 'E05')]
    end_s = [i for i in end_v if i not in end_c and i not in ('M11', 'E07')]
    STATES = {'start': dict(visited=[], here='F01', seen=[], coll=[]), 'mid': dict(visited=mid_v, here='M07', seen=mid_s, coll=mid_c),
              'end': dict(visited=end_v, here='E06', seen=end_s, coll=end_c)}
    def split(t):
        i = t.find(':'); return (t[:i].strip(), t[i + 1:].strip()) if i >= 0 else (t, '')
    plates = {k: split(v['title'])[0] for k, v in {**TITLES['lands'], **TITLES['zones']}.items()}
    tn = {n['id']: n for n in NODES['nodes']}
    nodes = []
    for c in THREAD['chapters']:
        for n in c['nodes']:
            i = n['id']; t = TITLES['nodes'][i]
            nodes.append(dict(id=i, env=t['title'], concept=t.get('subtitle', ''), ch=c['id'], pre=n['prereq'], hidden=bool(tn[i].get('hidden_detour')),
                              trial=bool(tn[i].get('experimental')), deferred=bool(tn[i].get('deferred')), fog=(i == 'E04')))
    ENTR = sorted({e['from'] for e in NODES['edges'] if e.get('kind') == 'detour_entrance' and e['to'] == 'E04'})
    chapters = [dict(id=c['id'], sym=SYM[c['id']], ids=[n['id'] for n in c['nodes']]) for c in THREAD['chapters']]
    frames = [dict(skin=s, plate=plates[p], ids=ids) for s, p, ids in FRAMES]
    edges = [e for e in NODES['edges'] if e['from'] in tn and e['to'] in tn and not tn[e['from']].get('deferred') and not tn[e['to']].get('deferred')]
    S = {k: v['text'] for k, v in UI.items()}
    card = {b: {k: BANK[f'card.pulley.b{b}.{k}']['text'] for k in ('band', 'say', 'sub') if f'card.pulley.b{b}.{k}' in BANK} for b in (1, 2, 3)}
    V = [("SciShow Kids: Need a Lift? Try a Pulley!", "یوتیوب · انگلیسی"), ("SciShow Kids: Solving Problems with Simple Machines", "یوتیوب · انگلیسی")]
    def slices(path):
        s = open(path, encoding='utf-8').read()
        return [base64.b64decode(m.group(2)) for m in re.finditer(r'data:(image/[a-z+]+);base64,([A-Za-z0-9+/=]{100,})', s)]
    def webp(raw, w, alpha=False, q=78):
        im = Image.open(io.BytesIO(raw)).convert('RGBA' if alpha else 'RGB')
        if alpha:
            seeds = [(x, y) for x in range(0, im.width, 16) for y in (0, im.height - 1)] + [(x, y) for y in range(0, im.height, 16) for x in (0, im.width - 1)]
            for pt in seeds:
                px = im.getpixel(pt)
                if px[3] and min(px[:3]) > 225: ImageDraw.floodfill(im, pt, (255, 255, 255, 0), thresh=30)
        im = im.resize((w, round(w * im.height / im.width)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, 'WEBP', quality=q); return 'data:image/webp;base64,' + b64(buf.getvalue())
    FL = slices(ROOT / 'design/cards/approved/card-space-full-flow-v1/fragment.html')
    IN = slices(ROOT / 'design/cards/approved/harbor-interaction-v1/fragment.html')
    img = dict(head=webp(FL[0], 420, True), c0=webp(FL[3], 520, True), c1=webp(FL[2], 520, True), c2=webp(FL[1], 520, True),
               a0=webp(IN[0], 395), a1=webp(IN[1], 395), a2=webp(IN[2], 395),
               scene='data:image/webp;base64,' + b64((ROOT / 'design/mockups/20261007/mobile-layout-options/scene-v8-crop.webp').read_bytes()))
    fonts = ''.join(f"@font-face{{font-family:{fam};font-weight:{w};src:url(data:font/woff2;base64,{b64((ROOT / 'assets/fonts' / f).read_bytes())}) format('woff2')}}"
                    for fam, w, f in (('Vazirmatn', 400, 'Vazirmatn-Regular.woff2'), ('Vazirmatn', 700, 'Vazirmatn-Bold.woff2'), ('Lalezar', 400, 'Lalezar-Regular.woff2')))
    tpl = (HERE / 'template.html').read_text(encoding='utf-8')
    for mark in ('/*__FONTS__*/', '/*__TOKENS__*/', '/*__KIT__*/', '/*__DATA__*/null', '<!--__SPRITE__-->'):
        if mark not in tpl: raise SystemExit(msg('v5.build.no_placeholder_tpl', mark=mark))
    css = re.sub(r'@font-face\{[^}]*\}\n?', '', (KIT / 'kit.css').read_text(encoding='utf-8'))
    def inline_all(text):   # SVGهای کیت v3 که در CSS/الگو با url(svg/…) آمده‌اند (مثل v3)
        return re.sub(r'url\((["\']?)svg/([A-Za-z0-9_.-]+\.svg)\1\)', lambda m: 'url("data:image/svg+xml;base64,' + b64((KIT / 'svg' / m.group(2)).read_bytes()) + '")', text)
    css, tpl = inline_all(css), inline_all(tpl)
    data = dict(S=S, R=REV, nodes=nodes, chapters=chapters, frames=frames, edges=edges, entr=ENTR, states=STATES, order=ORDER, card=card, videos=V, img=img)
    # tokens پیش از کیت: اگر نام متغیری با v3 برخورد کند، v3 برنده است (ظاهر ثابت می‌ماند)
    return (tpl.replace('/*__FONTS__*/', fonts).replace('/*__TOKENS__*/', art['tokens']).replace('/*__KIT__*/', css)
               .replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False)).replace('<!--__SPRITE__-->', art['sprite']))

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--assets', default=str(HERE / 'team/assets')); ap.add_argument('--out-dir', default=str(HERE))
    ap.add_argument('--placeholder', action='store_true', help='جاگذار را حتی با هنر واقعی بیاور')
    ap.add_argument('--no-write', action='store_true')
    a = ap.parse_args(argv)
    art = collect_assets(a.assets, True if a.placeholder else None)
    for w in art['warnings']: print(w)
    if art['placeholder']: print(msg('v5.build.placeholder'))
    out = None
    if not art['errors']:
        out = build_page(art)
        n = len(out.encode('utf-8'))
        if n > PAGE_CAP: art['errors'].append(msg('v5.build.page_over', kb=round(n / KB, 1), cap=PAGE_CAP // KB))
    if art['errors']:
        print(msg('v5.build.fail', n=len(art['errors'])))
        for e in art['errors']: print(' -', e)
        return 1
    if not a.no_write:
        od = pathlib.Path(a.out_dir); od.mkdir(parents=True, exist_ok=True)
        (od / 'index.html').write_text(out, encoding='utf-8')
        (od / 'assets.json').write_text(json.dumps(dict(page_bytes=n, page_cap=PAGE_CAP, module_bytes=art['sizes'], module_caps={m: c for m, (c, _) in MODULES.items()},
                                                        assets=art['entries']), ensure_ascii=False, indent=1), encoding='utf-8')
    print(msg('v5.build.ok', kb=round(n / KB), n=sum(1 for e in art['entries'] if e['type'] == 'symbol'),
              mods='، '.join(f'{m} {round(s / KB, 1)}KB' for m, s in art['sizes'].items())))
    return 0

if __name__ == '__main__':
    sys.exit(main())
