#!/usr/bin/env python3
"""ساخت spec_sample.html از component_spec.json و spec/strings.fa.json (هیچ رنگ، شعاع یا متنی در این فایل دست‌نویس نیست؛
فقط ساختار صفحه). اجرا:  python3 spec/build_sample.py   ← v5/spec_sample.html"""
import json, base64, pathlib, html, re

V5 = pathlib.Path(__file__).resolve().parents[1]
ROOT = V5.parents[4]
SPEC = json.load(open(V5 / 'component_spec.json', encoding='utf-8'))
STR = json.load(open(V5 / 'spec/strings.fa.json', encoding='utf-8'))
ROWS = {r['id']: r for r in SPEC['rows']}
PAL = SPEC['palette']
ST = SPEC['state_rules']


def S(k, **kw):
    t = html.escape(STR['spec.' + k if not k.startswith('spec.') else k]['text'])
    for a, b in kw.items(): t = t.replace('{' + a + '}', str(b))
    return t

def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)

def cr(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True); return (x + .05) / (y + .05)

def rgba(h, a):
    h = h.lstrip('#'); return 'rgba(%d,%d,%d,%s)' % (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

def fa(n):  # عدد فارسی
    return str(n).translate(str.maketrans('0123456789.', '۰۱۲۳۴۵۶۷۸۹٫'))

# ---------- آیکون‌ها (ساده، گوشه‌گرد، رنگ از currentColor؛ موقت تا آیکون‌های هنرمند)
IC = {
 'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
 'lock': '<rect x="5" y="11" width="14" height="10" rx="3"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
 'check': '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 'back': '<path d="M4 12h15M13 6l6 6-6 6"/>',
 'search': '<circle cx="11" cy="11" r="6"/><path d="M16 16l4.5 4.5"/>',
 'play': '<path d="M8 5l11 7-11 7z" fill="currentColor"/>',
 'box': '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9zM4 7.5l8 4.5 8-4.5M12 12v9"/>',
 'plus': '<path d="M12 5v14M5 12h14"/>',
 'eye': '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
 'flag': '<path d="M6 21V4M6 5h11l-2.5 4 2.5 4H6"/>',
 'cards': '<rect x="7" y="4" width="13" height="16" rx="3"/><path d="M3.5 8v9a3 3 0 0 0 3 3"/>',
 'bulb': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
}

def ic(n, px=24, cls=''):
    return f'<svg class="ic {cls}" viewBox="0 0 24 24" width="{px}" height="{px}" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[n]}</svg>'

def peaks(n):
    p = ''.join(f'<path d="M{1 + i * 13} 17l6-11 6 11z"/>' for i in range(n))
    return f'<svg class="ic peaks" viewBox="0 0 {2 + 13 * n} 20" width="{2 + 13 * n}" height="20" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true">{p}</svg>'

# ---------- CSS تولیدی از JSON
def css():
    o = []
    for r in SPEC['rows']:
        sh, f, sz, b = r['shape'], r['font'], r['size'], r['border']
        v = [f'--rad:{sh.get("radius_px") or 0}px', f'--bw:{b["width_px"]}px', f'--h:{sz.get("min_height_px", 0)}px', f'--minw:{sz.get("min_width_px", 0)}px', f'--pad:{sz.get("padding_inline_px", 12)}px']
        if f.get('family'):
            ff = "'Lalezar','Vazirmatn',sans-serif" if f['family'] == 'Lalezar' else "'Vazirmatn',system-ui,sans-serif"
            v += [f'--ff:{ff}', f'--fw:{f["weight"]}', f'--fs:{f["size_px"]}px', f'--lh:{f.get("line_height", 1.4)}']
        o.append(f'.r-{r["id"]}{{{";".join(v)}}}')
        for var in r['variants']:
            for mode in ('day', 'night'):
                c = var[mode]; d = r['depth'][mode]
                vs = [f'--fill:{c["fill"]}', f'--text:{c["text"]}', f'--rim:{c["rim"]}', f'--icon:{c.get("icon", c["text"])}', f'--pfill:{c.get("pressed_fill", c["fill"])}',
                      f'--bs:{c.get("rim_style", "solid")}']
                if d['type'] == 'lip':
                    vs += [f'--depth:0 {d["px"]}px 0 {d["color"]}', f'--depth-p:0 {max(d["px"] - 2, 0)}px 0 {d["color"]}']
                elif d['type'] == 'glow':
                    g = c.get('glow') or c['rim']
                    vs += [f'--depth:0 0 {d["blur_px"]}px {rgba(g, d["alpha"])}', f'--depth-p:0 0 10px {rgba(g, d["alpha"])}']
                else:
                    vs += ['--depth:none', '--depth-p:none']
                o.append(f'[data-mode={mode}] .r-{r["id"]}.v-{var["id"]}{{{";".join(vs)}}}')
    for mode in ('day', 'night'):
        d = ST['disabled'][mode]
        o.append(f'[data-mode={mode}]{{--dfill:{d["fill"]};--dtext:{d["text"]};--drim:{d["rim"]};--stripe:{rgba(d["text"], .16)};--cap:{"#241a5e" if mode == "day" else "#ffffff"}}}')
    o.append(f'.pane.light{{--ring:{ST["focus"]["on_light_surface"]}}} .pane.dark{{--ring:{ST["focus"]["on_dark_surface"]}}}')
    o.append(f'.pane.dark{{--cap:#fff3c4}}')
    return '\n'.join(o)

def font64(f): return base64.b64encode(open(ROOT / 'assets/fonts' / f, 'rb').read()).decode()

BASE_CSS = '''
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:#efeaf8;color:#241a5e;font:400 16px/1.7 'Vazirmatn',system-ui,sans-serif;direction:rtl}
.wrap{max-width:460px;margin:0 auto;padding:14px 12px 40px}
h1{font:400 34px/1.3 'Lalezar','Vazirmatn',sans-serif;margin:8px 0 0}
.sub{margin:0 0 14px;font-weight:700}
.row{margin:0 0 28px}
.row h2{display:flex;align-items:center;gap:10px;margin:0;font:700 22px/1.4 'Vazirmatn',sans-serif}
.num{display:inline-grid;place-items:center;inline-size:34px;block-size:34px;border-radius:17px;background:#241a5e;color:#fff3c4;font:700 18px/1 'Vazirmatn',sans-serif}
.desc{margin:2px 0 4px}
.cap{margin:0 0 8px;font-weight:700;color:#4b3b9e}
.pane{position:relative;margin:0 0 10px;padding:30px 14px 16px;border-radius:22px;border:2.6px solid #241a5e}
.pane[data-mode=day]{background:var(--surf);color:#241a5e}
.pane[data-mode=night]{background:var(--surf);color:#fff}
.pane .mt{position:absolute;inset-block-start:6px;inset-inline-start:12px;font-weight:700;font-size:16px;line-height:1.3;color:var(--cap)}
.stack{display:flex;flex-direction:column;gap:12px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.flex{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-start}
figure{margin:0;display:flex;flex-direction:column;gap:2px;align-items:stretch;min-width:0}
figcaption{font-size:16px;font-weight:700;line-height:1.4;color:var(--cap)}
.ic{flex:none}
.w{width:100%}
/* ----- کنترل پایه */
.k{position:relative;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:var(--h);min-width:var(--minw);padding:0 var(--pad);margin:0 0 4px;
  font-family:var(--ff);font-weight:var(--fw);font-size:var(--fs);line-height:var(--lh);color:var(--text);background-color:var(--fill);
  border:var(--bw) var(--bs,solid) var(--rim);border-radius:var(--rad);box-shadow:var(--depth);cursor:pointer;text-align:center;-webkit-appearance:none;appearance:none}
.k.is-pressed,.k:active{background-color:var(--pfill);transform:translateY(2px);box-shadow:var(--depth-p)}
.k.is-disabled,.k:disabled{background-color:var(--dfill);background-image:repeating-linear-gradient(135deg,transparent 0 6px,var(--stripe) 6px 8px);color:var(--dtext);border:var(--bw) dashed var(--drim);box-shadow:none;transform:none;cursor:default}
.k.is-focus,.k:focus-visible{outline:4px solid var(--ring);outline-offset:3px}
.k .ic{color:var(--icon)}
.k.is-disabled .ic{color:var(--dtext)}
/* دکمه‌های ردیف */
.r-btn_icon{padding:0;inline-size:56px}
.r-btn_icon .ic{inline-size:32px;block-size:32px}
.r-chip_base{flex-direction:column;gap:0;inline-size:96px;line-height:1.15}
.r-chip_base b{font-size:20px;font-weight:700;line-height:1.15}
.r-chip_base .chk{position:absolute;inset-block-start:-12px;inset-inline-start:-10px;display:grid;place-items:center;inline-size:24px;block-size:24px;border-radius:12px;background:#46f0d8;color:#190539;border:2.6px solid #190539}
.r-chip_base .chk .ic{color:#190539}
.bar{display:flex;align-items:center;gap:8px;padding:8px 10px 10px;border-radius:0 0 22px 22px;margin:-6px -4px 8px}
.bar .r-chip_base{flex:1;inline-size:auto;min-inline-size:76px}
.r-tab{flex:1;padding:0 8px;position:relative}
.r-tab.v-on::after{content:"";position:absolute;inset-inline:16px;inset-block-end:5px;block-size:4px;border-radius:2px;background:var(--icon)}
.r-tab.v-on{padding-block-end:6px}
.tabs{display:flex;gap:8px}
.ch{inline-size:100%;justify-content:flex-start;padding-inline:14px 18px;gap:12px;text-align:start}
.ch .t{flex:1;text-align:start}
.badge{display:inline-flex;align-items:center;gap:6px;block-size:36px;padding:0 10px;border:2.6px solid #241a5e;border-radius:12px;color:#241a5e;font:700 16px/1 'Vazirmatn',sans-serif;flex:none}
.d-easy{background:#2fa44a}.d-mid{background:#ff9d1c}.d-hard{background:#ff4b4b}
.badge .ic{color:#241a5e}
.is-disabled .badge .ic{color:#241a5e}
.is-disabled .lk{color:var(--dtext)}
.r-tile_menu{flex-direction:column;justify-content:flex-end;gap:6px;inline-size:100%;padding:12px 8px 12px}
.r-tile_menu .ic{inline-size:56px;block-size:56px}
.r-tile_card{flex-direction:column;justify-content:space-between;inline-size:100%;padding:10px 8px 8px;gap:6px}
.r-tile_card .ic{inline-size:40px;block-size:40px}
.np{align-self:stretch;padding:2px 8px;border-radius:10px;background:#07203a;color:#fff;font:700 16px/1.5 'Vazirmatn',sans-serif}
.is-disabled .np{opacity:1}
.r-chip_simple{padding:0 18px}
.pl{display:inline-flex;align-items:center;min-height:32px;padding:0 14px;border-radius:10px;border:2.6px solid var(--rim);background:var(--fill);color:var(--text);font:700 16px/1.5 'Vazirmatn',sans-serif}
.ml{display:inline-flex;align-items:center;min-height:32px;padding:0 12px;border-radius:10px;border:2.6px solid var(--rim);background:var(--fill);color:var(--text);font:700 17px/1.4 'Vazirmatn',sans-serif;box-shadow:var(--depth)}
.zt{font:400 34px/1.3 'Lalezar','Vazirmatn',sans-serif;color:var(--text);-webkit-text-stroke:9px var(--fill);paint-order:stroke fill;stroke-linejoin:round;display:inline-block}
.zones{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.zn{display:grid;place-items:center;min-height:84px;border-radius:16px;border:2.6px solid #241a5e;padding:6px}
.zn.wide{grid-column:1/-1}
.lkb{display:inline-grid;place-items:center;inline-size:36px;block-size:36px;border-radius:18px;background:var(--fill);border:2.6px solid var(--rim);color:var(--icon)}
.lkb .ic{inline-size:20px;block-size:20px}
.sheet{margin:0 -4px;padding:10px 16px 16px;border-radius:28px;border:3.5px solid var(--rim);background:var(--fill);color:var(--text);box-shadow:var(--depth);font:400 16px/1.7 'Vazirmatn',sans-serif}
.sheet::before{content:"";display:block;inline-size:44px;block-size:6px;margin:0 auto 8px;border-radius:3px;background:var(--rim);opacity:1}
.sheet h3{margin:0 0 4px;font:400 28px/1.4 'Lalezar','Vazirmatn',sans-serif}
.sheet h3.long{font:700 24px/1.4 'Vazirmatn',sans-serif}
.sheet p{margin:0 0 10px}
.sheet .btns{display:flex;flex-direction:column;gap:10px}
.sheet .btns .k{inline-size:100%}
/* ممنوع */
.fbs{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:10px 14px;border-radius:16px;border:2.6px dashed #241a5e;font:700 20px/1.3 'Vazirmatn',sans-serif}
.fbs b{font:700 16px/1 'Vazirmatn',sans-serif;direction:ltr;background:#fff3c4;color:#241a5e;padding:4px 8px;border-radius:10px}
.fb{display:flex;flex-direction:column;gap:2px;margin-bottom:8px}
.fb .why{font-size:16px;line-height:1.5}
.alw{display:flex;flex-wrap:wrap;gap:6px 14px;font:700 20px/1.5 'Vazirmatn',sans-serif}
.alw small{font:700 16px/1 'Vazirmatn',sans-serif;direction:ltr;opacity:1}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
'''

def modes_for(row):
    return [('day', row['surface']['day']), ('night', row['surface']['night'])]

def pane(row, mode, body, surf=None, extra=''):
    surf = surf or row['surface'][mode]
    cls = 'dark' if lum(surf) <= .3 else 'light'
    return f'<div class="pane {cls} {extra}" data-mode="{mode}" style="--surf:{surf}"><span class="mt">{S("mode." + mode)}</span>{body}</div>'

def cap_for(row):
    f, sh, sz = row['font'], row['shape'], row['size']
    fam = '<bdi dir="ltr">' + (f.get('family') or '') + (f' {f["weight"]}' if f.get('weight') else '') + '</bdi>'
    r = fa(sh['radius_px']) if sh.get('radius_px') else ''
    if row['id'] == 'zone_title':
        return S('cap.fmt.text', font=fam, size=fa(f['size_px']), halo=fa(row['border']['width_px']))
    if row['id'] == 'lock':
        return S('cap.fmt.icon', size=fa(sh['size_px']))
    if row['id'] == 'btn_icon':
        return S('cap.fmt.iconbtn', r=r, icon=fa(sz['icon_px']), touch=fa(sz['touch_px']))
    if row['interactive']:
        return S('cap.fmt', r=r, font=fam, size=fa(f['size_px']), touch=fa(sz['touch_px']))
    return S('cap.fmt.nobtn', r=r, font=fam, size=fa(f['size_px']))

def fig(inner, cap): return f'<figure>{inner}<figcaption>{cap}</figcaption></figure>'

def stfig(btn_fn, states=('pressed', 'disabled', 'focus')):
    return ''.join(fig(btn_fn(st), S('state.' + st)) for st in states)

def sc(st): return {'normal': '', 'pressed': ' is-pressed', 'disabled': ' is-disabled', 'focus': ' is-focus'}[st]

def B(rid, vid, content, st='normal', extra='', tag='button'):
    dis = ' aria-disabled="true"' if st == 'disabled' else ''
    return f'<{tag} class="k r-{rid} v-{vid}{sc(st)} {extra}"{dis} type="button">{content}</{tag}>'

# ---------- ردیف‌ها
def r_btn_primary(mode):
    c = lambda v, t, i='': B('btn_primary', v, f'{i}{t}', extra='w')
    body = '<div class="stack">' + c('cyan', S('s.go')) + c('gold', S('s.box'), ic('box')) + c('pink', S('s.video'), ic('play')) + c('violet', S('s.hold')) + '</div>'
    body += '<div class="grid2" style="margin-top:14px">' + stfig(lambda st: B('btn_primary', 'cyan', S('s.video'), st, 'w'), ('pressed', 'disabled', 'focus')) + '</div>'
    return body

def r_btn_secondary(mode):
    body = '<div class="grid2">' + B('btn_secondary', 'plain', ic('back') + S('s.back'), extra='w') + B('btn_secondary', 'plain', ic('search') + S('s.search'), extra='w') + '</div>'
    body += '<div class="grid2" style="margin-top:14px">' + stfig(lambda st: B('btn_secondary', 'plain', S('s.back'), st, 'w'), ('pressed', 'disabled', 'focus')) + '</div>'
    return body

def r_btn_icon(mode):
    one = lambda st: B('btn_icon', 'plain', ic('menu', 32), st).replace('type="button"', f'type="button" aria-label="{S("s.menu")}"')
    return '<div class="flex">' + fig(one('normal'), S('state.normal')) + stfig(one) + '</div>'

def chip(on, st='normal', num='b12'):
    chk = f'<i class="chk">{ic("check", 16)}</i>' if on else ''
    return B('chip_base', 'on' if on else 'off', f'<span>{S("s.base")}</span><b>{S(f"s.{num}")}</b>{chk}', st)

def r_chip_base(mode):
    bar = f'<div class="bar" style="background:{ROWS["chip_base"]["surface"][mode]}">' + \
          B('btn_icon', 'plain', ic('menu', 32), extra='').replace('type="button"', f'type="button" aria-label="{S("s.menu")}"') + \
          chip(True, num='b12') + chip(False, num='b34') + chip(False, num='b56') + '</div>'
    sts = '<div class="flex" style="margin-top:10px">' + stfig(lambda st: chip(False, st, 'b34'), ('pressed', 'disabled', 'focus')) + '</div>'
    return bar + sts

def r_chip_simple(mode):
    cs = lambda on, t, st='normal': B('chip_simple', 'on' if on else 'off', (ic('check', 20) if on else '') + S(t), st)
    return '<div class="flex">' + cs(True, 's.all') + cs(False, 's.seen') + cs(False, 's.kept') + '</div><div class="flex" style="margin-top:12px">' + \
        stfig(lambda st: cs(False, 's.seen', st)) + '</div>'

def chrow(n, word, st='normal', title='s.ch1', lock=False):
    badge = f'<span class="badge d-{["easy", "mid", "hard"][n - 1]}">{peaks(n)}{S("s." + ["easy", "mid", "hard"][n - 1])}</span>'
    lk = f'<span class="lk">{ic("lock", 28)}</span>' if lock else ''
    return B('challenge_row', 'shell', f'{badge}<span class="t">{S(title)}</span>{lk}', st, 'ch')

def r_challenge_row(mode):
    body = '<div class="stack">' + chrow(1, 0, title='s.ch1') + chrow(2, 0, title='s.ch2') + chrow(3, 0, title='s.ch3') + '</div>'
    body += '<div class="stack" style="margin-top:14px">' + fig(chrow(1, 0, 'pressed', 's.ch1'), S('state.pressed')) + fig(chrow(2, 0, 'disabled', 's.ch2', True), S('state.disabled')) + fig(chrow(3, 0, 'focus', 's.ch3'), S('state.focus')) + '</div>'
    return body

ZN = [('sports', 's.z_sports'), ('space', 's.z_space'), ('farm', 's.z_farm'), ('city', 's.z_city'), ('sand', 's.z_sand'), ('ice', 's.z_ice')]

def zone_grid(row, mode, inner_fn):
    if mode == 'night':
        return f'<div class="zones"><div class="zn wide" style="background:{row["surface"]["night"]}">{inner_fn("s.z_city", mode)}</div></div>'
    return '<div class="zones">' + ''.join(f'<div class="zn" style="background:{row["surfaces_extra"][k]}">{inner_fn(s, mode)}</div>' for k, s in ZN) + '</div>'

def r_map_label(mode):
    row = ROWS['map_label']
    def inner(s, m):
        k = {'s.z_sports': 's.lbl1', 's.z_space': 's.lbl2', 's.z_farm': 's.lbl1', 's.z_city': 's.lbl2', 's.z_sand': 's.lbl1', 's.z_ice': 's.lbl2'}[s]
        return f'<span class="ml r-map_label v-plain">{S(k)}</span>'
    return zone_grid(row, mode, inner)

def r_zone_title(mode):
    row = ROWS['zone_title']
    return zone_grid(row, mode, lambda s, m: f'<span class="zt r-zone_title v-plain">{S(s)}</span>')

def r_plate(mode):
    return '<div class="flex">' + ''.join(f'<span class="pl r-plate v-{v}">{S(s)}</span>' for v, s in (('plain', 's.first'), ('here', 's.here'), ('new', 's.newp'))) + '</div>'

def r_sheet(mode):
    def sheet(title, long=False):
        return (f'<div class="sheet r-sheet v-plain"><h3 class="{"long" if long else ""}">{S(title)}</h3><p>{S("s.sheet_body")}</p><div class="btns">' +
                B('btn_primary', 'cyan', S('s.go')) + B('btn_secondary', 'plain', ic('back') + S('s.back')) + '</div></div>')
    return sheet('s.sheet_title') + '<div style="height:14px"></div>' + sheet('s.sheet_long', True)

def r_tab(mode):
    def tb(on, t, st='normal'): return B('tab', 'on' if on else 'off', S(t), st)
    bar = '<div class="tabs">' + tb(True, 's.tab1') + tb(False, 's.tab2') + tb(False, 's.tab3') + '</div>'
    sts = '<div class="flex" style="margin-top:12px">' + stfig(lambda st: tb(False, 's.tab2', st).replace('r-tab', 'r-tab fx'), ('pressed', 'disabled', 'focus')) + '</div>'
    return bar + sts

def r_tile_menu(mode):
    tl = lambda v, ico, t, st='normal': B('tile_menu', v, ic(ico, 56) + f'<span>{S(t)}</span>', st)
    body = '<div class="grid2">' + tl('cyan', 'flag', 's.t_map') + tl('violet', 'cards', 's.t_cards') + tl('gold', 'box', 's.t_prac') + tl('pink', 'bulb', 's.t_guide') + '</div>'
    body += '<div class="grid2" style="margin-top:14px">' + stfig(lambda st: tl('cyan', 'flag', 's.t_map', st), ('pressed', 'disabled', 'focus')) + '</div>'
    return body

def r_tile_card(mode):
    tl = lambda v, ico, t, st='normal': B('tile_card', v, ic(ico, 40) + f'<span class="np">{S(t)}</span>', st)
    body = '<div class="grid2">' + tl('seen', 'eye', 's.cn1') + tl('kept', 'box', 's.cn2') + tl('new', 'plus', 's.cn3') + tl('locked', 'lock', 's.cn4') + '</div>'
    body += '<div class="grid2" style="margin-top:14px">' + stfig(lambda st: tl('seen', 'eye', 's.cn1', st), ('pressed', 'disabled', 'focus')) + '</div>'
    return body

def r_lock(mode):
    row = ROWS['lock']
    return zone_grid(row, mode, lambda s, m: f'<span class="lkb r-lock v-plain" role="img" aria-label="{S("s.st_locked")}">{ic("lock", 20)}</span>')

FN = {k: globals()['r_' + k] for k in ROWS}

def build():
    fonts = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{font64(f)}) format('woff2')}}" for n, w, f in
                    (('Vazirmatn', 400, 'Vazirmatn-Regular.woff2'), ('Vazirmatn', 700, 'Vazirmatn-Bold.woff2'), ('Lalezar', 400, 'Lalezar-Regular.woff2')))
    parts = [f'<h1>{S("title")}</h1><p class="sub">{S("sub")}</p>']
    for i, row in enumerate(SPEC['rows'], 1):
        rid = row['id']
        panes = ''.join(pane(row, m, FN[rid](m), extra=f'row-{rid}') for m in ('day', 'night'))
        parts.append(f'<section class="row" id="{rid}"><h2><span class="num">{fa(i)}</span>{S("spec.row." + rid)}</h2><p class="desc">{S("spec.desc." + rid)}</p><p class="cap">{cap_for(row)}</p>{panes}</section>')
    # ممنوع
    fb = ''.join(f'<div class="fb"><div class="fbs" style="background:{f["bg"]};color:{f["fg"]}"><span>{S("forbid.sample")}</span><b>{fa(f"{cr(f["fg"], f["bg"]):.2f}")} / {S("forbid.tag")}</b></div><div class="why">{S(f["why_key"])}</div></div>'
                 for f in SPEC['forbidden_pairs'])
    parts.append(f'<section class="row" id="forbidden"><h2>{S("sec.forbid")}</h2><p class="desc">{S("sec.forbid.intro")}</p>{fb}</section>')
    A = SPEC['allowed_text_on_dark']
    al = ''.join(f'<div class="pane dark" data-mode="night" style="--surf:{bg};--cap:#fff3c4"><div class="alw">' + ''.join(f'<span style="color:{fg}">{S("forbid.sample")} <small>{fa(f"{cr(fg, bg):.1f}")}</small></span>' for fg in A['colors']) + '</div></div>' for bg in A['on'])
    parts.append(f'<section class="row" id="allowed"><h2>{S("sec.allowed")}</h2><p class="desc">{S("sec.allowed.intro")}</p>{al}</section>')
    doc = f'<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{S("title")}</title><style>{fonts}{BASE_CSS}\n{css()}</style></head><body><div class="wrap">{"".join(parts)}</div></body></html>'
    (V5 / 'spec_sample.html').write_text(doc, encoding='utf-8')
    print('spec_sample.html', len(doc) // 1024, 'KB')

if __name__ == '__main__':
    build()
