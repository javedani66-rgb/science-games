"""عکس‌گیری از همهٔ صفحه‌های ماکت v3 در ۳۹۰×۸۰۰ و ۳۲۰×۶۴۰ + خطاهای کنسول + اسکرول افقی.
اجرا: python3 tests/shots.py [tag]  (خروجی در shots/)"""
import sys, pathlib, json
from playwright.sync_api import sync_playwright
V3 = pathlib.Path(__file__).resolve().parents[1]
OUT = V3 / 'shots'; OUT.mkdir(exist_ok=True)
EXE = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
TAG = sys.argv[1] if len(sys.argv) > 1 else 'r1'
errs = []

def run(w, h):
    with sync_playwright() as pw:
        b = pw.chromium.launch(executable_path=EXE, args=['--no-sandbox'])
        pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=1)
        pg.on('console', lambda m: errs.append((w, m.type, m.text)) if m.type in ('error', 'warning') else None)
        pg.on('pageerror', lambda e: errs.append((w, 'pageerror', str(e))))
        pg.goto('file://' + str(V3 / 'index.html')); pg.wait_for_timeout(500)
        pg.evaluate("__st.tutOn=false;__st.tutDone.map=true;__st.tutDone.scene=true;__st.tut=null;renderOv();document.body.classList.add('rm');document.getElementById('rvbar').style.display='none'")
        def shot(name):
            pg.wait_for_timeout(350)
            pg.screenshot(path=str(OUT / f'{TAG}_{w}x{h}_{name}.png'))
            hs = pg.evaluate("document.documentElement.scrollWidth>document.documentElement.clientWidth||[...document.querySelectorAll('.body,.scr,#phone')].some(e=>e.scrollWidth>e.clientWidth+1)")
            if hs: errs.append((w, 'hscroll', name))
        def js(s): return pg.evaluate(s)
        def clk(sel): pg.click(sel); pg.wait_for_timeout(200)
        pg.evaluate("render()"); shot('01_map_here')
        # map scrolled to top / bottom
        js("document.querySelector('#mapbody').scrollTop=0"); shot('02_map_top')
        js("document.querySelector('#mapbody').scrollTop=1500"); shot('03_map_mid')
        js("document.querySelector('#mapbody').scrollTop=99999"); shot('04_map_end')
        js("scrollMapTo('M07',false)"); pg.wait_for_timeout(100)
        clk('.node[data-n=M07]'); shot('05_peek')
        clk('[data-act=closeov]')
        js("scrollMapTo('M08',false)"); pg.wait_for_timeout(100); clk('.node[data-n=M08]'); shot('06_lock')
        clk('[data-act=closeov]')
        js("st.scr='map';render()")
        clk('[data-t=menu]'); shot('07_menu'); clk('.tile--cards'); pg.wait_for_timeout(300); shot('08_box_top')
        for ch in ['C04','C07','C10']:
            clk(f'[data-act=jump][data-ch={ch}]'); pg.wait_for_timeout(300); shot('09_box_'+ch)
        js("document.querySelector('#boxbody').scrollTop=0")
        clk('.pocket[data-id=M07]'); shot('10_card_front'); clk('[data-act=flip]'); pg.wait_for_timeout(600); shot('11_card_back')
        clk('[data-act=put]') if js("!!document.querySelector('[data-act=put]')") else None
        clk('.cbar [data-act=closecard]'); pg.wait_for_timeout(200)
        js("st.search=true;st.q='';render()"); shot('12_box_search')
        js("st.search=false;render()")
        js("go('env',{cur:'M07'},false)"); shot('13_env_harbor'); clk('.hc[data-p="2"]'); shot('14_env_reveal')
        js("go('env',{cur:'M05'},false)"); shot('15_env_generic')
        js("go('scene',{cur:'M07',tier:0},false)"); shot('16_scene'); clk('[data-act=help]'); clk('[data-act=hint]'); shot('17_help'); clk('[data-act=closeov]')
        clk('[data-t=lesson]'); shot('18_scene_card'); clk('.cbar [data-act=closecard]')
        js("go('prac',{prac:1},false)"); shot('19_prac')
        js("go('map',{},false);st.overlay='gate';st.gateOK=false;renderOv()"); shot('20_gate'); js("st.gateOK=true;renderOv()"); shot('21_gate_open')
        js("st.overlay=null;st.tutDone.map=false;st.tut=null;go('map',{},false);startTut('map')"); shot('22_tut_map')
        js("st.tut=null;st.sample='start';loadSample('start');go('map',{},false)"); shot('23_map_start')
        js("document.querySelector('#mapbody').scrollTop=2400"); shot('24_map_start_mid')
        js("loadSample('end');st.teacher=false;go('map',{},false);document.querySelector('#mapbody').scrollTop=99999"); shot('25_map_end_state')
        js("st.teacher=true;st.keepMap=true;render();document.querySelector('#mapbody').scrollTop=99999"); shot('26_map_teacher')
        b.close()
for w, h in ((390, 800), (320, 640)): run(w, h)
print(json.dumps(errs, ensure_ascii=False, indent=1) if errs else 'NO ERRORS')
