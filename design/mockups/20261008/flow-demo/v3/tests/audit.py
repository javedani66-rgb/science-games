"""بازرسی خودکار: همپوشانی متن/گره/دکمه روی نقشه و قفسه، متن < ۱۴px، هدف لمس < ۴۸px، اسکرول افقی، خطای کنسول.
اجرا: python3 tests/audit.py   (خروجی خالی = مشکلی پیدا نشد)"""
import pathlib, json
from playwright.sync_api import sync_playwright
V3 = pathlib.Path(__file__).resolve().parents[1]
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
JS_MAP = r"""
() => {
  const out = [];
  const els = [...document.querySelectorAll('#map .node__labels .chip, #map .node__disc, #map .guide, #map .fogsign, #map .plate, #map .land__sym, #map .flagc')];
  const R = e => e.getBoundingClientRect();
  const name = e => (e.closest('.node') ? 'node:' + e.closest('.node').dataset.n + ':' : '') + (e.className.baseVal || e.className).split(' ').slice(0, 2).join('.') + (e.textContent ? '[' + e.textContent.trim().slice(0, 14) + ']' : '');
  for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
    const a = els[i], b = els[j]; if (a.contains(b) || b.contains(a)) continue;
    const ni = a.closest('.node'), nj = b.closest('.node');
    const ra = R(a), rb = R(b);
    const w = Math.min(ra.right, rb.right) - Math.max(ra.left, rb.left), h = Math.min(ra.bottom, rb.bottom) - Math.max(ra.top, rb.top);
    if (w > 2 && h > 2) {
      if (ni && ni === nj && h <= 10) continue; // برچسب زیر قرص همان گره (طرح کیت)
      const cls = [a.className, b.className].join(' ');
      if (cls.includes('guide') && ((ni && ni.dataset.t === 'here') || (nj && nj.dataset.t === 'here'))) continue; // راهنما روی گرهٔ خودش
      if (cls.includes('fogsign') && (ni || nj)) { const n = ni || nj; if (n.dataset.n && (a.className.includes('fogsign') ? true : true)) {
          // تابلو باید فقط با قرص گرهٔ خودش کمی هم‌پوشانی داشته باشد
          const sg = a.className.includes('fogsign') ? a : b, other = sg === a ? b : a;
          if (other.className.includes('node__disc')) continue; } }
      out.push(['overlap', name(a), name(b), Math.round(w) + 'x' + Math.round(h)]);
    }
  }
  // بیرون از قاب زمین
  document.querySelectorAll('#map .land').forEach(l => { const lr = R(l);
    l.querySelectorAll('.node__labels .chip,.node__disc').forEach(e => { const r = R(e);
      if (r.left < lr.left + 4 || r.right > lr.right - 4 || r.bottom > lr.bottom - 4) out.push(['clip', name(e)]); }); });
  return out;
}
"""
JS_GEN = r"""
() => {
  const out = [];
  const vis = e => { const r = e.getBoundingClientRect(); const s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  // متن کوچک
  const w = document.createTreeWalker(document.querySelector('#phone'), NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (w.nextNode()) { const n = w.currentNode; if (!n.textContent.trim()) continue; const p = n.parentElement; if (!p || seen.has(p)) continue; seen.add(p);
    if (p.closest('svg')) continue; if (!vis(p)) continue; const fs = parseFloat(getComputedStyle(p).fontSize);
    if (fs < 13.9) out.push(['small-text', fs, n.textContent.trim().slice(0, 20)]); }
  // هدف لمس
  document.querySelectorAll('#phone button, #phone [data-act]:not(.scrim):not(.cscrim):not(.tmask):not(.hc):not(.gc)').forEach(e => { if (!vis(e)) return; const r = e.getBoundingClientRect();
    if (e.closest('#rv')) return; if (e.className.includes && e.className.includes('node')) return;
    if (Math.min(r.width, r.height) < 47.5) out.push(['small-target', Math.round(r.width) + 'x' + Math.round(r.height), (e.getAttribute('aria-label') || e.textContent || '').trim().slice(0, 20)]); });
  // اسکرول افقی
  document.querySelectorAll('#phone .body, #phone .scr, #phone').forEach(e => { if (e.scrollWidth > e.clientWidth + 1) out.push(['hscroll', e.className]); });
  return out;
}
"""
JS_BOX = r"""
() => {
  const out = [];
  const pk = [...document.querySelectorAll('#boxbody .pk')];
  const R = e => e.getBoundingClientRect();
  for (let i = 0; i < pk.length; i++) for (let j = i + 1; j < pk.length; j++) { const a = R(pk[i]), b = R(pk[j]);
    const w = Math.min(a.right, b.right) - Math.max(a.left, b.left), h = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    if (w > 2 && h > 2) out.push(['pk-overlap', pk[i].dataset.pk, pk[j].dataset.pk]); }
  // متن عنوان/چسبک داخل جیب سرریز نکند
  document.querySelectorAll('#boxbody .pocket__title,#boxbody .pocket__name,#boxbody .pocket__ln,#boxbody .pocket__cap').forEach(e => {
    if (e.scrollHeight > e.clientHeight + 4 || e.scrollWidth > e.clientWidth + 2) out.push(['pocket-text-overflow', e.className, e.textContent.trim().slice(0, 24), e.scrollHeight + '>' + e.clientHeight]);
    const p = e.closest('.pocket').getBoundingClientRect(), r = e.getBoundingClientRect();
    if (r.left < p.left - 1 || r.right > p.right + 1 || r.top < p.top - 1 || r.bottom > p.bottom + 1) out.push(['pocket-text-outside', e.textContent.trim().slice(0, 24)]); });
  document.querySelectorAll('#boxbody .shelf__head').forEach(h => { if (h.scrollWidth > h.clientWidth + 1) out.push(['shelf-head-overflow', h.textContent.trim().slice(0, 20)]); });
  return out;
}
"""
res = {}
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
    for w, h in ((390, 800), (320, 640), (360, 740)):
        pg = b.new_page(viewport={'width': w, 'height': h})
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('file://' + str(V3 / 'index.html')); pg.wait_for_timeout(400)
        pg.evaluate("__st.tutOn=false;__st.tutDone.map=true;__st.tutDone.scene=true;__st.tut=null;document.body.classList.add('rm');renderOv()")
        for sample in ('start', 'mid', 'end'):
            for teacher in (False, True):
                pg.evaluate(f"loadSample('{sample}');st.teacher={'true' if teacher else 'false'};go('map',{{}},false)"); pg.wait_for_timeout(250)
                for r in pg.evaluate(JS_MAP): res.setdefault(f'{w} map {sample} t={teacher}', []).append(r)
                for r in pg.evaluate(JS_GEN): res.setdefault(f'{w} map-gen {sample} t={teacher}', []).append(r)
            pg.evaluate("st.fogClear=true;go('map',{},false)"); pg.wait_for_timeout(200)
            for r in pg.evaluate(JS_MAP): res.setdefault(f'{w} map {sample} fogClear', []).append(r)
        for sample in ('start', 'mid', 'end'):
            for teacher in (False, True):
                pg.evaluate(f"loadSample('{sample}');st.teacher={'true' if teacher else 'false'};go('box',{{}},false)"); pg.wait_for_timeout(250)
                for r in pg.evaluate(JS_BOX): res.setdefault(f'{w} box {sample} t={teacher}', []).append(r)
                for r in pg.evaluate(JS_GEN): res.setdefault(f'{w} box-gen {sample} t={teacher}', []).append(r)
        for scr, extra in (('env', "cur:'M07'"), ('env', "cur:'M05'"), ('scene', "cur:'M07',tier:0"), ('scene', "cur:'M05',tier:1"), ('prac', 'prac:0')):
            pg.evaluate(f"loadSample('mid');go('{scr}',{{{extra}}},false)"); pg.wait_for_timeout(200)
            for r in pg.evaluate(JS_GEN): res.setdefault(f'{w} {scr} {extra}', []).append(r)
        for ov in ("st.overlay='menu'", "st.peek='M07'", "st.lock='M08'", "st.overlay='gate'", "st.overlay='gate';st.gateOK=true", "st.overlay='help';st.hint=3"):
            pg.evaluate(f"loadSample('mid');go('map',{{}},false);{ov};renderOv()"); pg.wait_for_timeout(200)
            for r in pg.evaluate(JS_GEN): res.setdefault(f'{w} overlay {ov}', []).append(r)
        for face in ('front', 'back'):
            pg.evaluate(f"loadSample('mid');go('box',{{}},false);openCard('M07','box',null);st.card.face='{face}';renderCard(false)"); pg.wait_for_timeout(200)
            for r in pg.evaluate(JS_GEN): res.setdefault(f'{w} card {face}', []).append(r)
            pg.evaluate("st.card=null;renderCard(false)")
        if errs: res[f'{w} console'] = errs
        pg.close()
    b.close()
# گزارش: یکتاسازی
bad = 0
for k, v in res.items():
    u = []
    for x in v:
        if x not in u: u.append(x)
    if u: bad += 1; print(k, len(u), json.dumps(u[:4], ensure_ascii=False)[:420])
print('DONE', 'issues in', bad, 'groups' if bad else '— no issues')
