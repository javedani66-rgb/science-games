#!/usr/bin/env python3
"""بانک متن‌های فارسی: همهٔ متن‌های قابل‌ویرایش پروژه با شناسهٔ ثابت و جای دقیق در منبع.

دستورها:
  collect                 متن‌های منبع‌ها را وارد بانک می‌کند (متن بازبینی‌شده را بازنویسی نمی‌کند)
  export [--status draft] یک فایل JSON یکپارچه برای دادن به GPT/Gemini می‌سازد
  import فایل             فایل برگشتی را بررسی می‌کند و گزارش می‌دهد؛ با --apply در بانک و منبع‌ها می‌نویسد
  apply                   متن بانک را در منبع‌ها می‌نویسد
  check                   بررسی سلامت بانک (شناسه‌ها، منبع‌ها، واژه‌های ممنوع)
"""
import json, re, sys, argparse, pathlib, datetime, hashlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TXT = ROOT / 'docs/texts'
BANK = TXT / 'TEXT_BANK_FA.json'
NODES = ROOT / 'docs/research/world/nodes_v2_draft.json'
TITLES = ROOT / 'docs/research/world/titles_fa.json'
CARD = ROOT / 'design/mockups/20261007/lesson-card-options/card.html'

# واژه‌های ممنوع/هشدار (قاعدهٔ مالک): اصطلاح علمی نیرو، مسافت نه راه، بدون «باهوشی»
BAD = {'زور': 'به‌جای «نیرو»', 'باهوشی': 'ستایش فرایند، نه هوش (voice.md)', 'راه بیشتر': 'به‌جای «مسافت بیشتر» (B45)', 'هل می‌خوری': 'فارسی نیست'}
GLOSSARY = {
 'نیرو': 'نه «زور»', 'جرم': 'مقدار ماده؛ ترازو، گرم و کیلوگرم', 'وزن': 'نیروی گرانش؛ نیروسنج، نیوتون',
 'مسافت': 'نه «راه» برای فاصلهٔ پیموده‌شده (B45)', 'نیوتون': 'یکای نیرو؛ نه «نیوتن»', 'اهرم': '', 'تکیه‌گاه': '', 'قرقره': '',
 'سطح شیب‌دار': '', 'گوه': '', 'پیچ': '', 'چرخ‌دنده': '', 'کار': 'در علوم: نیرو × جابه‌جایی؛ به‌معنای روزمره نیست'}

def load(p): return json.load(open(p, encoding='utf-8'))
def save(p, d): open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=1) + '\n')

def get_ptr(d, ptr):
    for k in ptr:
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d
def set_ptr(d, ptr, v):
    for k in ptr[:-1]: d = d[int(k)] if isinstance(d, list) else d[k]
    k = ptr[-1]
    if isinstance(d, list): d[int(k)] = v
    else: d[k] = v

def sources():
    """فهرست همهٔ متن‌ها: (id, kind, where_fa, context_fa, band, file, kind_of_target, locator, current)"""
    out = []
    T, N = load(TITLES), load(NODES)
    names = {n['id']: n for n in N['nodes']}
    for nid, v in T['nodes'].items():
        n = names.get(nid, {})
        out.append((f'title.node.{nid}', 'title', f'نام محیط (یک جا) برای گرهٔ {nid} روی نقشه', f'مفهوم: {v.get("subtitle","")}. {n.get("plain_fa","")}', 'همه',
                    TITLES, 'json', ['nodes', nid, 'title'], v['title']))
        if v.get('subtitle'):
            out.append((f'subtitle.node.{nid}', 'title', f'نام مفهوم (سوتیتر محیط {nid}؛ با رفتن اشاره‌گر یا انگشت دیده می‌شود)', f'محیط: {v["title"]}. {n.get("plain_fa","")}', 'همه',
                        TITLES, 'json', ['nodes', nid, 'subtitle'], v['subtitle']))
    for lid, v in T['lands'].items():
        out.append((f'title.land.{lid}', 'title', f'نام سرزمین {lid}', '', 'همه', TITLES, 'json', ['lands', lid, 'title'], v['title']))
    for zid, v in T['zones'].items():
        out.append((f'title.zone.{zid}', 'title', f'نام منطقهٔ {zid} در سرزمین ماشین‌های ساده', '', 'همه', TITLES, 'json', ['zones', zid, 'title'], v['title']))
    for i, v in enumerate(T['path_stages']):
        out.append((f'title.stage.{i+1}', 'title', f'نام مرحلهٔ {i+1} از مسیر هشت‌مرحله‌ای', 'مسیر پیشنهادی از نیرو تا ماشین‌های ساده', 'همه',
                    TITLES, 'json', ['path_stages', str(i), 'title'], v['title']))
    for k, v in T['path_names'].items():
        out.append((f'title.path.{k}', 'title', f'نام مسیر «{k}»', '', 'همه', TITLES, 'json', ['path_names', k, 'title'], v['title']))
    for i, n in enumerate(N['nodes']):
        lab = T['nodes'].get(n['id'], {}).get('subtitle', n['label_fa'])
        if n.get('plain_fa'):
            out.append((f'concept.{n["id"]}.plain', 'explainer', f'توضیح ساده برای معلم و بزرگ‌تر، گرهٔ «{lab}»',
                        'یک یا دو جمله؛ علمی و درست؛ برای بچه‌ها نوشتهٔ ساده‌تر در کارت می‌آید', 'همه', NODES, 'json', ['nodes', str(i), 'plain_fa'], n['plain_fa']))
        for dk in ('D2', 'D3', 'D4'):
            v = (n.get('depths') or {}).get(dk)
            if v:
                out.append((f'concept.{n["id"]}.{dk}', 'explainer', f'متن سطح {dk} گرهٔ «{lab}»', 'D2 کیفی، D3 عددی، D4 فرمول', 'همه', NODES, 'json', ['nodes', str(i), 'depths', dk], v))
    # ماکت کارت آموزشی قرقره
    html = CARD.read_text(encoding='utf-8')
    for b, band in ((1, '۱ و ۲'), (2, '۳ و ۴'), (3, '۵ و ۶')):
        m = re.search(r"\n%d:\{band:'([^']*)',say:'([^']*)',sub:'([^']*)',eq:'([^']*)'" % b, html)
        if not m: continue
        for idx, key, kind, what in ((1, 'band', 'label', 'برچسب سطح بالای کارت'), (2, 'say', 'card', 'جملهٔ اصلی زیر تصویر'), (3, 'sub', 'card', 'توضیح تکمیلی کوچک‌تر')):
            if m.group(idx):
                out.append((f'card.pulley.b{b}.{key}', kind, f'کارت آموزشی قرقره، پایهٔ {band}: {what}', 'کارت درس با تصویر طناب و قرقره (ثابت و متحرک)', f'پایهٔ {band}',
                            CARD, 'card', [str(b), key], m.group(idx)))
    # مؤلفه‌های تازه: هر فایل strings.fa.json (فرمت: {"id": {"text":..., "kind":..., "where_fa":..., "context_fa":..., "band":...}})
    # به‌طور خودکار جمع می‌شود؛ مؤلفه فقط با شناسه به متن مراجعه می‌کند (B50).
    for sf in sorted(list((ROOT / 'design').rglob('strings.fa.json')) + list((ROOT / 'src').rglob('strings.fa.json')) + list((ROOT / 'pilot').rglob('strings.fa.json'))):
        for sid, v in load(sf).items():
            if sid.startswith('_'): continue
            out.append((sid, v.get('kind', 'card'), v.get('where_fa', sid), v.get('context_fa', ''), v.get('band', 'همه'), sf, 'json', [sid, 'text'], v['text']))
    return out

def regroup(src):
    return {s[0]: dict(id=s[0], kind=s[1], where_fa=s[2], context_fa=s[3], band=s[4], file=str(s[5].relative_to(ROOT)), target=s[6], locator=s[7], text=s[8]) for s in src}

def read_bank():
    return load(BANK) if BANK.exists() else {'entries': {}}

def cmd_collect(a):
    bank = read_bank(); cur = regroup(sources()); new = chg = 0
    for k, e in cur.items():
        old = bank['entries'].get(k)
        if not old:
            e['status'] = 'draft'; bank['entries'][k] = e; new += 1
        else:
            old.update({kk: e[kk] for kk in ('kind', 'where_fa', 'context_fa', 'band', 'file', 'target', 'locator')})
            if old['text'] != e['text']:
                if old['status'] in ('reviewed', 'approved') and old.get('applied') is True:
                    pass  # بانک پیش است؛ با apply به منبع می‌رود
                else:
                    old['text'] = e['text']; old['status'] = 'draft'; chg += 1
    gone = [k for k in bank['entries'] if k not in cur]
    bank['meta'] = {'updated': datetime.date.today().isoformat(), 'glossary': GLOSSARY, 'banned': BAD}
    save(BANK, bank); print(f'collect: {new} جدید، {chg} تغییرکرده، {len(gone)} حذف‌شده از منبع', gone or '')

def cmd_export(a):
    bank = read_bank(); items = []
    for k, e in bank['entries'].items():
        if a.status and e['status'] != a.status: continue
        items.append({'id': k, 'kind': e['kind'], 'where': e['where_fa'], 'context': e['context_fa'], 'band': e['band'], 'text': e['text'], 'new_text': ''})
    out = {'_instructions_fa': (TXT / 'PROMPT_FOR_REVIEWER_FA.md').read_text(encoding='utf-8'), 'glossary': GLOSSARY, 'banned': BAD, 'items': items}
    p = TXT / 'export' / f'texts_for_review_{datetime.date.today().isoformat()}.json'
    p.parent.mkdir(exist_ok=True); save(p, out); print('export:', p.relative_to(ROOT), len(items), 'متن')

FRAG = re.compile(r'(<[^>]+>|&nbsp;|[A-Za-z]+\s*=\s*[^،.]*|[۰-۹0-9]+)')
def protected(t): return sorted(set(re.findall(r'<[^>]+>|&nbsp;|[A-Za-z]+(?:\s*[=/×]\s*[A-Za-z0-9]+)+|[0-9۰-۹]+', t)))

def cmd_import(a):
    bank = read_bank(); data = load(a.file); items = data['items'] if isinstance(data, dict) else data
    ids = {i['id'] for i in items}; problems = []; rows = []
    for k in bank['entries']:
        if k not in ids and ('only' not in a or True): pass
    for it in items:
        k = it['id']; e = bank['entries'].get(k)
        if not e: problems.append(f'شناسهٔ ناشناخته: {k}'); continue
        nt = (it.get('new_text') or '').strip()
        if not nt or nt == e['text']: continue
        if protected(e['text']) != protected(nt): problems.append(f'{k}: نشانه‌های محافظت‌شده (عدد/فرمول/برچسب) تغییر کرد: {protected(e["text"])} ← {protected(nt)}')
        for w, why in BAD.items():
            if w in nt: problems.append(f'{k}: واژهٔ ممنوع «{w}» ({why})')
        if e['kind'] == 'title' and len(nt) > 2.2 * max(len(e['text']), 20): problems.append(f'{k}: عنوان خیلی بلند شد')
        rows.append((k, e['text'], nt))
    rep = ['# گزارش وارد کردن متن‌ها', f'تاریخ: {datetime.date.today().isoformat()}', f'فایل: {a.file}', f'تغییرها: {len(rows)}', '']
    rep += ['## مشکل‌ها', *(f'- {p}' for p in problems), ''] if problems else ['## مشکل‌ها', 'ندارد', '']
    rep += ['## تغییرها', '| شناسه | پیش | پس |', '|---|---|---|', *(f'| `{k}` | {o} | {n} |' for k, o, n in rows)]
    (TXT / 'IMPORT_REPORT.md').write_text('\n'.join(rep) + '\n', encoding='utf-8'); print('\n'.join(rep[:4]), f'\nمشکل‌ها: {len(problems)} (گزارش: docs/texts/IMPORT_REPORT.md)')
    if a.apply:
        if problems and not a.force: sys.exit('مشکل دارد؛ با --force دوباره، یا پیش از آن فایل را اصلاح کن.')
        hist = TXT / 'history'; hist.mkdir(exist_ok=True)
        (hist / f'bank_before_{datetime.datetime.now():%Y%m%d_%H%M%S}.json').write_text(BANK.read_text(encoding='utf-8'), encoding='utf-8')
        for k, o, n in rows:
            bank['entries'][k]['text'] = n; bank['entries'][k]['status'] = 'reviewed'; bank['entries'][k]['applied'] = False
        save(BANK, bank); cmd_apply(a)

def cmd_apply(a):
    bank = read_bank(); files = {}
    for k, e in bank['entries'].items():
        if e.get('applied') is True: continue
        p = ROOT / e['file']
        if e['target'] == 'json':
            d = files.setdefault(p, load(p)); set_ptr(d, e['locator'], e['text'])
            if e['file'].endswith('titles_fa.json'): get_ptr(d, e['locator'][:-1])['status'] = e['status'] if e['status'] != 'reviewed' else 'draft'
        else:  # card: مجموعهٔ N در card.html؛ فقط همان کلید همان مجموعه جایگزین می‌شود
            t = files.setdefault(p, p.read_text(encoding='utf-8')); b, key = e['locator']
            pat = re.compile(r"(\n%s:\{band:')([^']*)(',say:')([^']*)(',sub:')([^']*)(',eq:')([^']*)(')" % b)
            m = pat.search(t)
            if not m: print('هشدار: مجموعهٔ', b, 'در', e['file'], 'پیدا نشد'); continue
            g = list(m.groups()); g[{'band': 1, 'say': 3, 'sub': 5}[key]] = e['text'].replace("'", "\\'")
            files[p] = t[:m.start()] + ''.join(g) + t[m.end():]
        e['applied'] = True
    for p, d in files.items():
        if isinstance(d, str): p.write_text(d, encoding='utf-8')
        else: save(p, d)
    save(BANK, bank); print('apply:', len(files), 'فایل منبع به‌روز شد')

def cmd_check(a):
    bank = read_bank(); cur = regroup(sources()); bad = pend = 0
    for k, e in bank['entries'].items():
        if k not in cur: print('منبع پیدا نشد:', k); bad += 1; continue
        for w in BAD:
            if w in e['text']: print(f'واژهٔ ممنوع «{w}» در {k}'); bad += 1
        if cur[k]['text'] != e['text']:
            if e.get('applied') is False: pend += 1
            else: print('بانک و منبع هم‌خوان نیستند (collect یا apply):', k); bad += 1
    print('check:', len(bank['entries']), 'متن؛', bad, 'مشکل؛', pend, 'در انتظار apply'); sys.exit(1 if bad else 0)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='c', required=True)
    sp.add_parser('collect'); e = sp.add_parser('export'); e.add_argument('--status')
    i = sp.add_parser('import'); i.add_argument('file'); i.add_argument('--apply', action='store_true'); i.add_argument('--force', action='store_true')
    sp.add_parser('apply'); sp.add_parser('check')
    a = ap.parse_args(); {'collect': cmd_collect, 'export': cmd_export, 'import': cmd_import, 'apply': cmd_apply, 'check': cmd_check}[a.c](a)
