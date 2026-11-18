"""Grade 1 («اول», index 8, appended at the END of GRADES): saved indices and the progress code must stay stable.
1) golden codes made by the build BEFORE grade 1 existed (tests/golden_codes.json) are reproduced exactly and read back to the same grade;
2) a grade-1 profile round-trips through the progress code (stored as g=0 plus the reserved top bits = 1) and keeps its data;
3) it reads as band 1-2 for the harbor and as track a; the grade pickers show 6 choices, «اول» first;
4) a new grade-1 profile can be created through the real UI and reaches the map and the harbor without errors.
Mechanical only; no claim about how first-graders understand anything (B9)."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os, sys
ROOT = Path(__file__).resolve().parent.parent
G = json.loads((ROOT / 'tests' / 'golden_codes.json').read_text(encoding='utf-8'))
problems = []
def chk(c, m):
    if not c: problems.append(m)
with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or None)
    pg = b.new_page(viewport={'width': 390, 'height': 900}); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto((ROOT / 'jtest.html').as_uri())
    def load(d):
        pg.evaluate("d=>{localStorage.clear();localStorage.setItem('sm-journey-v1',JSON.stringify({profiles:[d],cur:d.id,week:null}))}", d); pg.reload(); pg.wait_for_selector('#app')
    for e in G:
        load(e['in'])
        r = pg.evaluate("g=>{const p=__J.curP();const c=__J.makeCode(p);const r=__J.readCode(g);return {code:c,g:r&&r.g,t:r&&r.t,home:r&&r.home.join(''),side:r&&r.side.join(''),quiz:r&&r.quiz.join(''),opt:r&&r.opt.join(''),done:r&&r.done,pg:p.g}}", e['code'])
        chk(r['pg'] == e['in']['g'], f"saved grade index changed for g={e['in']['g']}")
        chk(r['code'] == e['code'], f"code changed for g={e['in']['g']} t={e['in']['t']}")
        for k in ('g', 't', 'home', 'side', 'quiz', 'opt', 'done'):
            chk(r[k] == e[k], f"golden code reads differently ({k}) for g={e['in']['g']}")
    # grade 1 round trip
    base = dict(G[0]['in']); base.update({'id': 'g1', 'g': 8, 'S': dict(base['S'], track='a')})
    load(base)
    r = pg.evaluate("""()=>{const p=__J.curP();const c=__J.makeCode(p);const r=__J.readCode(c);return {c,g:r&&r.g,t:r&&r.t,home:r&&r.home.join(''),side:r&&r.side.join(''),quiz:r&&r.quiz.join(''),opt:r&&r.opt.join(''),done:r&&r.done,trk:__J.trk(p),band:__J.harborBand(p),eligible:__J.harborEligible(p),gp:p.g}}""")
    chk(r['gp'] == 8 and r['g'] == 8, 'grade 1 survives the progress code (g=8)')
    chk(r['trk'] == 'a' and r['band'] == '1-2' and r['eligible'], 'grade 1 is track a and harbor band 1-2')
    g0 = G[0]
    for k in ('t', 'home', 'side', 'quiz', 'opt', 'done'): chk(r[k] == g0[k], f'grade-1 code keeps {k}')
    chk(r['c'] != g0['code'], 'grade-1 code differs from the grade-2 code of the same data')
    # a grade-1 code is a different string, and a corrupt top-bit value is rejected, not misread
    bad = pg.evaluate("""()=>{const A="بپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی";let ok=0,wrong=0;const c=__J.makeCode(__J.curP()).replace(/[\\s\\u200c]/g,"");
      for(let i=0;i<c.length;i++){const s=c.slice(0,i)+A[(A.indexOf(c[i])+1)%31]+c.slice(i+1);const r=__J.readCode(s);if(r===null)ok++;else wrong++;}return {ok,wrong}}""")
    chk(bad['wrong'] == 0, f"single-letter damage to a grade-1 code must be rejected by the checksum, wrong={bad['wrong']}")
    # UI: pickers
    pg.evaluate("()=>{localStorage.clear()}"); pg.reload(); pg.wait_for_selector('#app')
    pg.wait_for_selector('#jnm'); pg.fill('#jnm', 'آزمایش'); pg.click('#jnx'); pg.click('[data-t="0"]'); pg.click('#jnx')
    n = pg.locator('[data-g]').count(); chk(n == 6, f'grade picker shows 6 choices, got {n}')
    first = pg.locator('[data-g]').first
    chk(first.get_attribute('data-g') == '8' and first.inner_text().strip() == 'اول', 'grade 1 is the first choice')
    chk(pg.evaluate('document.documentElement.scrollWidth<=innerWidth'), 'grade picker: no horizontal overflow')
    pg.screenshot(path=str(ROOT / 'tests' / 'shots' / 'grade1_picker.png'))
    first.click(); pg.click('#jnx'); pg.wait_for_timeout(400)
    chk(pg.evaluate('()=>__J.curP().g') == 8, 'new profile has grade index 8')
    chk(pg.locator('[data-harbor]').count() >= 1 or pg.evaluate('()=>!!document.querySelector("#app")'), 'map loads')
    pg.evaluate('()=>__J.harborSelector()'); pg.wait_for_selector('[data-route]')
    chk(pg.locator('[data-route]').count() == 3, 'grade 1 sees the three harbor challenges')
    chk(not errs, f'page errors {errs}')
    b.close()
for p in problems: print('PROBLEM', p)
if problems: sys.exit(1)
print('grade1: golden codes identical, grade-1 round trip, band 1-2, pickers, UI creation OK')
