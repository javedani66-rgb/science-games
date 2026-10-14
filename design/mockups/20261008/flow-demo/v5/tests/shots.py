"""عکس‌گیری از همهٔ صفحه‌های ماکت v5 در ۳۹۰×۸۰۰ و ۳۶۰×۶۴۰ + نسخهٔ خاکستری + خطاهای کنسول + اسکرول افقی.
اجرا: python3 tests/shots.py [tag] [--gray] [--only=عدد،...]   (خروجی در shots/)"""
import sys, pathlib, json
from playwright.sync_api import sync_playwright
V5 = pathlib.Path(__file__).resolve().parents[1]
OUT = V5 / 'shots'; OUT.mkdir(exist_ok=True)
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
args = [a for a in sys.argv[1:] if not a.startswith('--')]
TAG = args[0] if args else 'g1'
GRAY = '--gray' in sys.argv
AUDIT = '--audit' in sys.argv
AJS = open(pathlib.Path(__file__).with_name('audit.js')).read()
errs = []

def run(w, h):
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.on('console', lambda m: errs.append((w, m.type, m.text)) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append((w, 'pageerror', str(e))))
        pg.goto('file://' + str(V5 / 'index.html')); pg.wait_for_timeout(600)
        pg.evaluate("__st.tutOn=false;__st.tutDone.map=true;__st.tutDone.scene=true;__st.tut=null;renderOv();document.body.classList.add('rm');document.getElementById('rvbar').style.display='none'")
        if GRAY: pg.add_style_tag(content='html{filter:grayscale(1)}')
        sfx = '_gray' if GRAY else ''
        def shot(name):
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(OUT / f'{TAG}_{w}x{h}_{name}{sfx}.png'))
            hs = pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth||[...document.querySelectorAll('.body,.scr,#phone,.mapbody,.envbody')].some(e=>e.scrollWidth>e.clientWidth+1)")
            if hs: errs.append((w, 'hscroll', name))
            if AUDIT:
                for r in pg.evaluate(AJS): errs.append((w, name, r))
        def js(s): return pg.evaluate(s)
        def clk(sel): pg.click(sel); pg.wait_for_timeout(200)
        def mapat(y): js(f"document.querySelector('#mapbody').scrollTop={y}*document.querySelector('#map').clientWidth/390")
        js("render()")
        shot('01_map_here')
        mapat(0); shot('02_map_top_fog')
        mapat(1500); shot('03_map_city')
        mapat(3000); shot('04_map_farm')
        mapat(3700); shot('05_map_space')
        mapat(4700); shot('06_map_sports')
        mapat(99999); shot('07_map_start')
        js("scrollMapTo('M07',false)"); pg.wait_for_timeout(100)
        clk('.mn[data-n=M07]'); shot('08_peek')
        clk('.sheet button[data-act=closeov]')
        js("scrollMapTo('M08',false)"); pg.wait_for_timeout(100); clk('.mn[data-n=M08]'); shot('09_lock')
        clk('.sheet button[data-act=closeov]')
        js("scrollMapTo('M07',false)")
        clk('[data-t=menu]'); shot('10_menu')
        clk('[data-act=srch]'); pg.fill('#mq', 'اسکله'); pg.wait_for_timeout(200); shot('11_search')
        clk('.sheet button[data-act=closeov]')
        clk('[data-t=menu]'); clk('.ui-tile[data-act=box]'); pg.wait_for_timeout(300); shot('12_box_top')
        for ch in ['C04', 'C07', 'C10']:
            clk(f'[data-act=jump][data-ch={ch}]'); pg.wait_for_timeout(300); shot('13_box_' + ch)
        js("document.querySelector('#boxbody').scrollTop=0")
        clk('.mc[data-id=M07]'); shot('14_card_front'); clk('[data-act=flip]'); pg.wait_for_timeout(600); shot('15_card_back')
        js("document.querySelector('#cbk .cbd').scrollTop=9999"); shot('15b_card_back_end')
        clk('[data-act=put]') if js("!!document.querySelector('[data-act=put]')") else None
        clk('.cbar [data-act=closecard]'); pg.wait_for_timeout(200)
        js("st.search=true;st.q='';render()"); shot('16_box_search')
        js("st.search=false;render()")
        js("go('env',{cur:'M07'},false,false)"); shot('17_env_harbor'); clk('.cd-strip[data-i="1"]'); shot('18_env_orange'); clk('.cd-strip[data-i="2"]'); shot('18b_env_red')
        js("go('env',{cur:'M05'},false,false)"); shot('19_env_generic')
        js("go('scene',{cur:'M07',tier:0},false,false)"); shot('20_scene'); clk('[data-act=help]'); clk('[data-act=hint]'); shot('21_help'); clk('.sheet button[data-act=closeov]')
        clk('[data-t=lesson]'); shot('22_scene_card'); clk('.cbar [data-act=closecard]')
        js("st.storyLight=true;go('scene',{cur:'M07',tier:1},false,false)"); shot('23_scene_dusk')
        js("go('scene',{cur:'M07',tier:2},false,false)"); shot('23b_scene_night'); js("st.storyLight=false")
        js("go('scene',{cur:'M05',tier:0},false,false)"); shot('24_scene_generic')
        js("go('prac',{prac:1},false,false)"); shot('25_prac')
        js("go('map',{},false,false);st.overlay='gate';st.gateOK=false;renderOv()"); shot('26_gate'); js("st.gateOK=true;renderOv()"); shot('27_gate_open')
        js("st.overlay=null;st.tutDone.map=false;st.tut=null;go('map',{},false,false);startTut('map')"); shot('28_tut_map')
        js("st.tut=null;loadSample('start');go('map',{},false,false)"); shot('29_map_start_state')
        js("loadSample('end');st.teacher=false;go('map',{},false,false);document.querySelector('#mapbody').scrollTop=0"); shot('30_map_end_state')
        js("st.teacher=true;st.keepMap=true;render();document.querySelector('#mapbody').scrollTop=0"); shot('31_map_teacher')
        b.close()
for w, h in ((390, 800), (360, 640)): run(w, h)
print(json.dumps(errs, ensure_ascii=False, indent=1) if errs else 'NO ERRORS')
