#!/usr/bin/env python3
"""الگوی خط D198/D199 روی نمادهای ایستگاه (درخواست مالک ۵ نوامبر: «الگوی خط رو هم در کار اصلاح کن»).
قاعده: فقط لبهٔ نماد با زمینه خط دور ضخیم دارد؛ هر خط دیگر (مرز دو جزء، درز داخل سازه) نازک است؛ جزء کوچک، خط کوچک.
روش (لایهٔ پشتی / «برچسب»):
  - برای هر جزء پُر (کلاس eo یا خط سرمه‌ای) یک کپی سرمه‌ای با خط ضخیم در «پشت همه» (اول گروه) گذاشته می‌شود؛ این کپی‌ها
    فقط بیرون از شکل دیده می‌شوند = خط دور بیرونی. خط خود جزء نازک می‌شود (۲٫۶ واحد، در جزء کوچک کمتر).
  - چندضلعی‌های سرمه‌ایِ پشتیِ قدیمی (سبک r6) هم یک کپی در پشت همه می‌گیرند و خودشان نازک می‌شوند تا مرز جزء جلویی نازک بماند.
  - لایه‌های متحرک (گروه‌های شناسه‌دار داخل hero) لایهٔ پشتی خودشان را دارند (با PART) تا با حرکت جدا نشوند.
  - خط سرمه‌ایِ تنها (بدون رنگ، مثل دورگیری دوباره) پهن‌تر از ۲٫۶ نازک می‌شود، مگر طناب دولایه (خط روشن روی خط سرمه‌ای) باشد.
  - چیزهای نیمه‌شفاف، سایه‌ها، سکو (_base) و گروه‌های بریده (clip/mask) دست نمی‌خورند.
فقط روی out/node_<sym>.svg کار می‌کند و علامت data-linepass می‌گذارد (دوباره اجرا نمی‌شود). W01 (space_loading) دستی است و رد می‌شود.
اجرا: python3 line_pass.py [sym ...]   (بدون آرگومان: همه به‌جز space_loading)"""
import sys, pathlib, json

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / 'out'
SKIP = {'space_loading', 'loading_ramp_a', 'loading_ramp_b'}

JS = r"""
(cfg)=>{
const NAVY=['#241a5e','#10083a'],NS='http://www.w3.org/2000/svg';
const sym=document.querySelector('symbol');
if(sym.getAttribute('data-linepass'))return 'skip';
const hero=sym.querySelector('[id$="_hero"]');if(!hero)return 'nohero';
const SH=['path','polygon','polyline','rect','circle','ellipse','line'];
const num=v=>v==null?null:parseFloat(v);
const fillOf=e=>(e.getAttribute('fill')||'').toLowerCase();
const strokeOf=e=>(e.getAttribute('stroke')||(e.classList.contains('eo')?'#241a5e':'')).toLowerCase();
const op=e=>{let o=1;for(let n=e;n&&n!==hero;n=n.parentNode){if(n.getAttribute){const a=n.getAttribute('opacity'),f=n.getAttribute('fill-opacity');if(a!=null)o*=+a;if(f!=null)o*=+f}}return o};
const isNavy=c=>NAVY.includes(c);
/* نزدیک‌ترین «ظرف»: hero یا لایهٔ متحرک شناسه‌دار؛ تبدیل‌های میانی جمع می‌شوند؛ اگر میانه clip/mask داشت: null */
function host(e){let tr=[],n=e.parentNode;while(n&&n!==hero&&!(n.id&&n.tagName==='g')){if(n.getAttribute('clip-path')||n.getAttribute('mask')||n.classList.contains('under'))return null;const t=n.getAttribute('transform');if(t)tr.unshift(t);n=n.parentNode}
 if(!n)return null;return {c:n,tr:tr.join(' ')}}
const bks=new Map();let nB=0,nT=0,nL=0;
function bk(h){if(!bks.has(h.c)){const g=document.createElementNS(NS,'g');g.setAttribute('class','bk');bks.set(h.c,g)}return bks.get(h.c)}
function backCopy(e,h,w){const c=e.cloneNode(false);for(const a of [...c.attributes])if(a.name==='id'||a.name.startsWith('data-')||a.name==='class'||a.name==='opacity'||a.name==='style')c.removeAttribute(a.name);
 c.setAttribute('fill','#241a5e');c.setAttribute('stroke','#241a5e');c.setAttribute('stroke-width',w.toFixed(2));c.setAttribute('stroke-linejoin','round');c.setAttribute('stroke-linecap','round');
 const own=e.getAttribute('transform');const t=[h.tr,own].filter(Boolean).join(' ');if(t)c.setAttribute('transform',t);else c.removeAttribute('transform');bk(h).appendChild(c);nB++}
const els=[...hero.querySelectorAll(SH.join(','))];
const dims=new Map();for(const e of els){let b;try{b=e.getBBox()}catch(_){b={width:0,height:0}}dims.set(e,Math.min(b.width,b.height)||Math.max(b.width,b.height))}
for(const e of els){
 if(e.closest('.bk'))continue;
 const f=fillOf(e),s=strokeOf(e),sw=num(e.getAttribute('stroke-width'));if(sw==null||!s||!isNavy(s))continue;
 const h=host(e),md=dims.get(e)||0,o=op(e);
 const top=h&&h.c===hero,BMAX=top?cfg.OUT:cfg.NEST;
 const thin=Math.max(cfg.TMIN,Math.min(cfg.T,.14*md));
 if(f==='none'||f===''){ /* خط تنها */
   if(e.tagName==='polyline'||e.tagName==='line'||e.tagName==='path'){const geo=x=>x.getAttribute('d')||x.getAttribute('points');let mate=null;
    for(let n=e.nextElementSibling;n;n=n.nextElementSibling)if(geo(n)===geo(e)&&fillOf(n)!==''&&(fillOf(n)==='none')&&!isNavy(strokeOf(n))){mate=n;break}
    if(mate){const lw=num(mate.getAttribute('stroke-width'))||0,want=lw+2*cfg.ROPE;if(sw>want+.05){e.setAttribute('stroke-width',want.toFixed(2));nL++}continue}  /* طناب/میلهٔ دولایه: لبهٔ سرمه‌ای هر طرف ۱٫۸ */
    if(sw>cfg.LINE+.05){e.setAttribute('stroke-width',Math.min(sw,Math.max(thin,cfg.LINE)).toFixed(2));nL++}}
   continue}
 if(o<.95){if(sw>thin){e.setAttribute('stroke-width',thin.toFixed(2));nT++}continue}
 if(isNavy(f)){ /* چندضلعی پشتیِ قدیمی */
   if(sw>=cfg.PART-.1&&h){backCopy(e,h,Math.min(sw,BMAX,Math.max(3,.6*md+sw)));e.setAttribute('stroke-width',(2*thin).toFixed(2));nT++}
   continue}
 if(sw<2.4)continue;
 if(h)backCopy(e,h,Math.min(BMAX,Math.max(3,.8*md)));
 if(sw>thin){e.setAttribute('stroke-width',thin.toFixed(2));nT++}
}
for(const [c,g] of bks){ /* لایهٔ پشتی پیش از اولین جزء پُر؛ سایه‌های نیمه‌شفاف اول گروه زیرش می‌مانند */
 let ref=c.firstElementChild;while(ref&&(ref.getAttribute('opacity')!=null&&ref.tagName==='ellipse'))ref=ref.nextElementSibling;c.insertBefore(g,ref)}
sym.setAttribute('data-linepass','1');
return {svg:new XMLSerializer().serializeToString(sym),nB,nT,nL}}
"""

CFG = dict(OUT=7.6, PART=5.8, NEST=4.6, ROPE=1.8, INNER=3.9, T=2.6, TMIN=1.4, LINE=2.6)


def main():
    from playwright.sync_api import sync_playwright
    syms = sys.argv[1:] or sorted(p.stem[5:] for p in OUT.glob('node_*.svg') if p.stem[5:] not in SKIP)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        for s in syms:
            f = OUT / ('node_%s.svg' % s); src = f.read_text(encoding='utf-8')
            a = src.index('<symbol'); z = src.rindex('</symbol>') + len('</symbol>')
            pg.set_content('<svg xmlns="http://www.w3.org/2000/svg" width="200" height="190">' + src[a:z] + '<use href="#node_%s"/></svg>' % s)
            r = pg.evaluate(JS, CFG)
            if not isinstance(r, dict):
                print(s, r); continue
            svg = r['svg'].replace(' xmlns="http://www.w3.org/2000/svg"', '', 1)
            f.write_text(src[:a] + svg + src[z:], encoding='utf-8')
            print(s, 'backing', r['nB'], 'thinned', r['nT'], 'lines', r['nL'])
        b.close()


if __name__ == '__main__':
    main()
