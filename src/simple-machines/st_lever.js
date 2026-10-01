/* ================= ایستگاه اهرم (الاکلنگ) ================= */
const LV_MASS={myA:20,myB:15,myC:30};
function brickSvg(x,yb,m,hl){const w=52,h=m/5*13+3;let s=`<rect x="${x-w/2}" y="${yb-h}" width="${w}" height="${h}" rx="3" fill="#C8553D" stroke="${hl?"#1E6FD9":"#8E3322"}" stroke-width="${hl?3.5:1.5}"/>`;
  for(let y=yb-13;y>yb-h+2;y-=13)s+=`<line x1="${x-w/2}" y1="${y}" x2="${x+w/2}" y2="${y}" stroke="#EBA08E" stroke-width="1.5"/>`;
  return `<g>${s}${KID()?"":T(x,yb-h/2+4,`${fa(m)} کیلوگرم`,{size:m===5?9:10,col:"#fff",halo:false})}</g>`;}
const lvItemH=it=>it.k==="b"?it.m/5*13+3:OB[it.id].h*.85;
function lvItemSvg(it,x,yb,hl){if(it.k==="b")return brickSvg(x,yb,it.m,hl);return `<g transform="translate(${x} ${yb}) scale(.85)">${OB[it.id].d}</g>`;}
const lvM=it=>it.k==="b"?it.m:LV_MASS[it.id];

function makeLever(A,cfg){
  const svg=A.svg,P=A.P;A.view(cfg.edit?520:404);svg.setAttribute('role','group');const PX=52,CX=320,CY=290;
  const st={stacks:{},pieces:(cfg.pieces||[]).map((m,i)=>({id:i,it:typeof m==="number"?{k:"b",m}:{k:"o",id:m},used:false})),inf:cfg.inf||null,edit:cfg.edit||"",sup:cfg.sup!==false,a:0,sel:null,hover:null,busy:false,hide:cfg.hide||{}};
  (cfg.items||[]).forEach(([p,it])=>{(st.stacks[p]=st.stacks[p]||[]).push(Object.assign({fixed:1},typeof it==="number"?{k:"b",m:it}:{k:"o",id:it}));});
  const tq=side=>Object.keys(st.stacks).reduce((s,p)=>{p=+p;if((side==="L"&&p<0)||(side==="R"&&p>0))s+=Math.abs(p)*st.stacks[p].reduce((a,it)=>a+lvM(it),0);return s;},0);
  const termStr=side=>Object.keys(st.stacks).map(Number).filter(p=>side==="L"?p<0:p>0).sort((a,b)=>Math.abs(a)-Math.abs(b)).filter(p=>st.stacks[p].length).map(p=>{const hid=st.stacks[p].some(it=>st.hide[it.id]);return hid?`؟ × ${fa(Math.abs(p))}`:`${fa(st.stacks[p].reduce((a,it)=>a+lvM(it),0))} × ${fa(Math.abs(p))}`;}).join(" + ")||"۰";
  const hasHidden=side=>Object.keys(st.stacks).map(Number).some(p=>(side==="L"?p<0:p>0)&&st.stacks[p].some(it=>st.hide[it.id]));
  const canEdit=p=>!A.locked&&(st.sup||cfg.live)&&(st.edit==="both"||(st.edit==="R"&&p>0)||(st.edit==="L"&&p<0));
  function render(){const tL=tq("L"),tR=tq("R"),bal=!st.sup&&tL===tR;
    const focus=svg.contains(document.activeElement)?document.activeElement.dataset.focus:null;
    let s=bgRoom(380);
    s+=`<g transform="translate(20 20)"><rect width="140" height="40" rx="12" fill="#fff" stroke="#C7D3DE" stroke-width="2"/><rect x="14" y="13" width="112" height="14" rx="7" fill="${bal?"#CDEFD9":"#E9EFF3"}" stroke="${bal?GRN:"#B8C6D3"}" stroke-width="2"/><line x1="70" y1="10" x2="70" y2="30" stroke="${bal?GRN:"#9FB0C0"}" stroke-width="2"/><circle cx="${70+clamp(st.a*3.2,-46,46)}" cy="20" r="6" fill="${bal?GRN:"#7D8CA3"}"/></g>`+T(90,78,bal?"تراز است":"تراز",{size:13,col:bal?GRN:MUT,halo:false});
    s+=`<path d="M${CX} ${CY} L${CX-36} 380 H${CX+36}Z" fill="#6B4A2B"/><path d="M${CX} ${CY} L${CX-18} 380 H${CX}Z" fill="#8A6443"/>`;
    if(st.sup)for(const x of[86,554])s+=`<rect x="${x-11}" y="${CY}" width="22" height="${380-CY}" fill="#E8590C"/><path d="M${x-11} ${CY+20} l22 -12 M${x-11} ${CY+44} l22 -12 M${x-11} ${CY+68} l22 -12" stroke="#fff" stroke-width="4" opacity=".6"/>`;
    let forces="";const forceMax=Math.max(1,...Object.values(st.stacks).map(items=>items.reduce((a,it)=>a+lvM(it),0)));
    let g=`<rect x="${CX-282}" y="${CY-12}" width="564" height="12" rx="5" fill="#D08A4B"/><rect x="${CX-282}" y="${CY-12}" width="564" height="4" rx="2" fill="#EAB47C"/>`;
    for(let p=-5;p<=5;p++){if(!p)continue;const x=CX+p*PX;g+=`<line x1="${x}" y1="${CY-12}" x2="${x}" y2="${CY}" stroke="#8A5427" stroke-width="2"/>`+(KID()?`<circle cx="${x}" cy="${CY+20}" r="3" fill="#6B4A2B"/>`:T(x,CY+26,fa(Math.abs(p)),{size:19,col:"#6B4A2B",halo:false}));}
    for(let p=-5;p<=5;p++){if(!p)continue;const x=CX+p*PX,items=st.stacks[p]||[];let yb=CY-12;
      if(canEdit(p)&&(st.sel||st.hover===p)){g+=`<g data-zone="pos" data-p="${p}" style="cursor:pointer"><circle cx="${x}" cy="${CY-24}" r="${st.hover===p?20:15}" fill="${st.hover===p?"#FFF3C4":"#fff"}" stroke="#F0B429" stroke-width="2.5" stroke-dasharray="4 3"/></g>`;}
      else if(canEdit(p))g+=`<g data-zone="pos" data-p="${p}"><rect x="${x-24}" y="${CY-90}" width="48" height="90" fill="#fff" fill-opacity="0"/></g>`;
      if(canEdit(p))g+=`<g data-zone="pos" data-p="${p}" data-focus="pos-${p}" tabindex="0" role="button" aria-label="${p>0?'راست':'چپ'}؛ ${fa(Math.abs(p))} خانه از تکیه‌گاه"><rect x="${x-23}" y="${CY-55}" width="46" height="44" fill="transparent"/></g>`;
      items.forEach((it,i)=>{const drag=canEdit(p)&&!it.fixed;g+=`<g ${drag?`data-drag="stk" data-p="${p}" data-i="${i}" data-focus="stk-${p}-${i}" tabindex="0" role="button" aria-label="برداشتن آجر از تخته" style="cursor:grab"`:""}>${lvItemSvg(it,x,yb)}</g>`;yb-=lvItemH(it)+1;});
      if(S.forces&&items.length&&!hasHidden("L")&&!hasHidden("R")){const m=items.reduce((a,it)=>a+lvM(it),0),hid=items.some(it=>st.hide[it.id]),len=hid?40:Math.min(65,65*m/forceMax),angle=st.a*Math.PI/180,ax=CX+p*PX*Math.cos(angle)-(yb-CY)*Math.sin(angle),endY=Math.max(90,CY+p*PX*Math.sin(angle)+(yb-CY)*Math.cos(angle)-6),ay=endY-len;forces+=arrow(ax,ay,ax,endY,9,p<0?BLUE:RED,.9);}}
    s+=`<g transform="rotate(${st.a} ${CX} ${CY})">${g}</g>`+forces+T(320,397,KID()?"کجیِ تخته فقط جهت چرخش را نشان می‌دهد.":"تخته بی‌وزن است؛ اصطکاک را نادیده می‌گیریم. کجی فقط جهت چرخش را نشان می‌دهد.",{size:13,halo:false,col:MUT});
    if(st.edit){s+=trayPanel("",404);
      const list=st.inf?st.inf.map((m,i)=>({id:"i"+i,it:typeof m==="number"?{k:"b",m}:{k:"o",id:m}})):st.pieces.filter(pc=>!pc.used);const n=list.length;
      list.forEach((pc,j)=>{const x=320+(j-(n-1)/2)*Math.min(96,560/Math.max(n,1)),sel=st.sel&&String(st.sel.pid)===String(pc.id);s+=`<g data-drag="tray" data-pid="${pc.id}" data-focus="tray-${pc.id}" tabindex="${A.locked?-1:0}" role="button" aria-label="${KID()?'انتخاب آجر':`انتخاب ${fa(lvM(pc.it))} کیلوگرم`}" style="cursor:grab"><rect x="${x-44}" y="418" width="88" height="90" rx="12" fill="${sel?"#FFF3C4":"#fff"}" fill-opacity="${sel?1:0}"/><g transform="translate(${x} 500) scale(1.25) translate(${-x} -500)">${lvItemSvg(pc.it,x,500,sel)}</g></g>`;});}
    P.paint(s);
    if(focus)svg.querySelector(`[data-focus="${focus}"]`)?.focus({preventScroll:true});
    if(window.__TEST||window.__JT){window.__T=window.__T||{};window.__T.lever={a:st.a,left:tL,right:tR,stacks:JSON.parse(JSON.stringify(st.stacks)),pieces:st.pieces.map(p=>({id:p.id,used:p.used}))};}
    const hl=hasHidden("L"),hr=hasHidden("R");
    A.counter(`<span class="cc l">چپ (جرم × فاصله): <b class="num">${hl||hr?"؟":fa(tL)}</b></span><span class="cc r">راست (جرم × فاصله): <b class="num">${hl||hr?"؟":fa(tR)}</b></span>`);
    A.formula(FX(`${sy("m","1")} × ${sy("d","1")} = ${sy("m","2")} × ${sy("d","2")}`,`${termStr("L")} ${tL===tR?"=":"≠"} ${termStr("R")}`,[[`${sy("m","1")}، ${sy("m","2")}`,"جرم هر طرف (kg)؛ چون زمین هر کیلوگرم را در دو طرف یکسان می‌کشد، می‌توان به‌جای وزن، جرم را گذاشت"],[`${sy("d","1")}، ${sy("d","2")}`,"فاصله از تکیه‌گاه (تعداد خانه)"]]));}
  function settle(done){const tL=tq("L"),tR=tq("R");const to=st.sup||tL===tR?0:(tR>tL?14:-14);const from=st.a,id=st.tw=(st.tw||0)+1;if(Math.abs(to-from)<.01){render();done&&done();return;}st.busy=true;tween(700,p=>{if(id!==st.tw)return;st.a=from+(to-from)*ease(p);render();},()=>{if(id!==st.tw)return;st.busy=false;render();done&&done();});}
  const posAt=pt=>{const a=st.a*Math.PI/180,dx=pt.x-CX,dy=pt.y-CY;const x=dx*Math.cos(a)+dy*Math.sin(a),y=CY-dx*Math.sin(a)+dy*Math.cos(a);if(y<CY-200||y>CY+40)return null;const p=Math.round(x/PX);if(!p||Math.abs(p)>5)return null;return canEdit(p)?p:null;};
  const findPc=pid=>{if(st.inf){const i=+String(pid).slice(1),m=st.inf[i];return typeof m==="number"?{k:"b",m}:{k:"o",id:m};}const pc=st.pieces.find(q=>String(q.id)===String(pid)&&!q.used);return pc?pc.it:null;};
  const put=(p,g)=>{if(!st.inf&&!findPc(g.pid))return;(st.stacks[p]=st.stacks[p]||[]).push(Object.assign({},g.it,{pid:g.pid}));if(!st.inf){const pc=st.pieces.find(q=>String(q.id)===String(g.pid));if(pc)pc.used=true;}};
  const unput=(p,i)=>{const it=st.stacks[p].splice(i,1)[0];if(!st.inf&&it.pid!=null){const pc=st.pieces.find(q=>String(q.id)===String(it.pid));if(pc)pc.used=false;}return it;};
  const interaction={blocked:()=>A.locked,
    start(d){if(d.drag==="tray"){const it=findPc(d.pid);return it?{from:"tray",pid:d.pid,it}:null;}if(d.drag==="stk"){const p=+d.p;if(!canEdit(p))return null;return{from:"stk",p,i:+d.i,it:st.stacks[p][+d.i]};}return null;},
    begin(g,pt){if(g.from==="stk"){const it=unput(g.p,g.i);g.pid=it.pid;}st.sel=null;P.ghost(lvItemSvg(g.it,0,20,true),pt.x,pt.y);render();},
    move(g,pt){P.move(pt.x,pt.y);const p=posAt(pt);if(p!==st.hover){st.hover=p;render();}},
    end(g,pt){P.clear();st.hover=null;const p=posAt(pt);if(p!=null)put(p,g);settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();},
    tap(g){if(g.from==="tray"){st.sel={pid:g.pid,it:g.it};A.fb("حالا روی جایی از تخته که می‌خواهی بزن.","info");render();}else{unput(g.p,g.i);settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();}},
    zoneTap(z){if(z.zone==="pos"&&st.sel){const p=+z.p;if(!canEdit(p))return;put(p,st.sel);st.sel=null;A.fb("");settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();}}};
  dragKit(svg,interaction);svg.onkeydown=e=>{if(A.locked||!(e.key==='Enter'||e.key===' '))return;const d=e.target.dataset;if(!d.focus)return;e.preventDefault();if(d.zone)interaction.zoneTap(d);else{const g=interaction.start(d);if(g)interaction.tap(g);}};
  settle();
  return{st,render,settle,tq,setSup(v,done){st.sup=v;settle(done);}};
}

/* Geometry follows lever3: the bottom face touches the wedge apex; the stone
   starts on the floor, then follows the short end while staying upright.
   Equal vertical forces share the same scale. Massless rigid beam; no friction. */
function makeLift(A,cfg){const svg=A.svg,P=A.P;A.view(524);svg.setAttribute('role','group');const PX=52,CX=320,FL=480,PY=448,EXT=.08,TH=9;
  const st={f:cfg.f==null?0:cfg.f,a:0,busy:false,W:cfg.W,S:cfg.S};
  const need=()=>st.W*(st.f+5)/(5-st.f);
  const geometry=()=>{const left=(st.f+5)*PX,right=(5-st.f)*PX,fx=CX+st.f*PX;
    const before=-Math.asin((FL-6-PY)/left),after=Math.asin((FL-6-PY)/(right+EXT*PX));
    const angle=before+(after-before)*st.a,co=Math.cos(angle),si=Math.sin(angle);
    const q=p=>({x:fx+(p-st.f)*PX*co,y:PY+(p-st.f)*PX*si});
    const top=p=>{const v=q(p);return{x:v.x+si*TH,y:v.y-co*TH};};
    const rock=top(-5),press=top(5);rock.y+=6+TH*Math.cos(before);
    return{fx,angle,rock,press,q,top,left,right};};
  function render(){const F=need(),ok=canLift(F,st.S),geo=geometry();
    const focused=svg.contains(document.activeElement)?document.activeElement.dataset.focus:null;
    let s=bgOut(FL).replace('height="520"','height="524"'),wedge=LEVER_ART.wedge,wh=(FL-PY)/(1-wedge.apexY),ww=wh*wedge.w/wedge.h;
    s+=`<g data-drag="fulcrum" data-focus="fulcrum" tabindex="${A.locked||cfg.paths?-1:0}" role="${cfg.paths?'img':'slider'}" aria-label="جای تکیه‌گاه؛ با کلیدهای چپ و راست جابه‌جا کن" aria-valuemin="1" aria-valuemax="9" aria-valuenow="${st.f+5}" aria-valuetext="${fa(st.f+5)} خانه تا سنگ" style="cursor:ew-resize"><rect x="${geo.fx-30}" y="${PY-3}" width="60" height="46" rx="8" fill="#fff" fill-opacity="0"/><image href="${wedge.src}" x="${geo.fx-ww*wedge.apexX}" y="${PY-wh*wedge.apexY}" width="${ww}" height="${wh}"/><rect x="${geo.fx-29}" y="${PY-3}" width="58" height="45" rx="8" fill="none" stroke="#D97706" stroke-width="2" stroke-dasharray="4 4"/></g>`;
    s+=`<g pointer-events="none" transform="translate(${geo.fx} ${PY}) rotate(${geo.angle*180/Math.PI})"><image href="${LEVER_ART.plank.src}" x="${-(st.f+5+EXT)*PX}" y="${-TH}" width="${(10+2*EXT)*PX}" height="${TH}" preserveAspectRatio="none"/></g>`;
    const rh=70,rw=rh*LEVER_ART.stone.w/LEVER_ART.stone.h;
    s+=`<image href="${LEVER_ART.stone.src}" x="${geo.rock.x-rw/2}" y="${geo.rock.y-rh}" width="${rw}" height="${rh}"/>`;
    s+=`<circle cx="${geo.fx}" cy="${PY}" r="4" fill="#7A3FC8" pointer-events="none"/>`;
    // Gravity and hand force stay vertical; both arrows use one scale. Leave
    // room above the force row even at the extreme fulcrum positions.
    const forceScale=Math.min(105/Math.max(st.W,st.S,1),Math.max(8,geo.press.y+50)/Math.max(st.W,st.S,1));
    if(S.forces&&!cfg.paths){const wy=Math.max(60,geo.rock.y-rh-120),sy=Math.max(60,geo.press.y-120);
      s+=arrow(geo.rock.x,wy,geo.rock.x,wy+st.W*forceScale,8,RED);
      s+=arrow(geo.press.x,sy,geo.press.x,sy+st.S*forceScale,8,"#D9498B");}
    // Force labels stay on a separate row, away from the arrow geometry.
    s+=T(28,36,KID()?"سنگ":"وزن سنگ: "+fa(st.W)+" نیوتن",{size:20,anchor:"end",halo:false})+
       T(612,36,KID()?"فشار دست":"نیروی دست: "+fa(st.S)+" نیوتن",{size:20,anchor:"start",halo:false});
    s+=`<g data-zone="press" data-focus="press" tabindex="${A.locked?-1:0}" role="button" aria-label="فشار دادن سر راست تخته"><circle cx="${geo.press.x}" cy="${geo.press.y-12}" r="22" fill="#fff" fill-opacity=".03" stroke="#D9498B" stroke-width="2" stroke-dasharray="4 4"/></g>`;
    s+=`<g pointer-events="none">${T(geo.fx,PY+29,"⟷",{size:20,col:"#8A5427",halo:false})}</g>`;
    s+=`<path d="M60 492 H${geo.fx} M${geo.fx} 489 V495 M${geo.fx} 492 H580 M60 489 V495 M580 489 V495" fill="none" stroke="#7D8CA3"/>`;
    s+=T(160,510,KID()?"سمت سنگ":`بازوی مقاوم: ${fa(st.f+5)} خانه`,{size:18,col:INK,halo:false})+
       T(475,510,KID()?"سمت دست":`بازوی محرک: ${fa(5-st.f)} خانه`,{size:18,col:INK,halo:false});
    if(cfg.paths&&st.a>0){const before=-Math.asin((FL-6-PY)/geo.left),paths=[];
      // Trace the same contact points as the animated scene, rather than only
      // their vertical displacement. Both ends move along circular arcs.
      for(const p of [-5,5]){const pts=Array.from({length:25},(_,i)=>{const a=before+(geo.angle-before)*i/24;
        return{x:geo.fx+(p-st.f)*PX*Math.cos(a)+TH*Math.sin(a),
          y:PY+(p-st.f)*PX*Math.sin(a)-TH*Math.cos(a)+(p===-5?6+TH*Math.cos(before):0)};});
        paths.push(pts.map((v,i)=>`${i?'L':'M'}${v.x} ${v.y}`).join(' '));
        for(const v of [pts[0],pts[24]])s+=`<circle cx="${v.x}" cy="${v.y}" r="4" fill="#7A3FC8" pointer-events="none"/>`;}
      s+=`<path d="${paths.join(' ')}" fill="none" stroke="#7A3FC8" stroke-width="4" stroke-dasharray="5 4" pointer-events="none"/>`;}
    P.paint(s);if(focused)svg.querySelector(`[data-focus="${focused}"]`)?.focus({preventScroll:true});
    A.counter(`<span class="cc">${KID()?"":`نیروی تعادل: <b class="num">${fa(Math.round(F*10)/10)} نیوتن</b>`}</span>`);
    A.formula(FX(`${sy("F")} = ${sy("W")} × ${sy("d","بار")} ÷ ${sy("d","دست")}`,`${fa(st.W)} × ${fa(st.f+5)} ÷ ${fa(5-st.f)} = ${fa(Math.round(F*10)/10)} N`,[[sy("F"),"نیروی نگه‌داشتن سنگ؛ برای بلند شدن کمی بیشتر لازم است"],[sy("W"),"وزن سنگ (نیوتن)"],[sy("d","بار"),"بازوی مقاوم"],[sy("d","دست"),"بازوی محرک"]]));
    if(window.__TEST||window.__JT){window.__T=window.__T||{};window.__T.lift={f:st.f,a:st.a,W:st.W,S:st.S,need:F,pivot:{x:geo.fx,y:PY},rock:geo.rock,press:geo.press,angle:geo.angle,busy:st.busy};}
  }
  function moveTo(f){if(A.locked||st.busy||cfg.paths)return;st.f=clamp(f,-4,4);st.a=0;render();if(cfg.onChange)cfg.onChange();}
  dragKit(svg,{blocked:()=>A.locked||st.busy,start(d){return d.drag==="fulcrum"?{}:null;},begin(){},move(g,p){const f=clamp(Math.round((p.x-CX)/PX),-4,4);if(f!==st.f)moveTo(f);},end(){render();},tap(){},zoneTap(z){if(z.zone==="press"&&cfg.onPress)cfg.onPress();}});
  svg.onkeydown=e=>{const id=e.target.dataset.focus;if(id==="fulcrum"&&["ArrowLeft","ArrowRight","Home","End"].includes(e.key)){e.preventDefault();moveTo(e.key==="Home"?-4:e.key==="End"?4:st.f+(e.key==="ArrowLeft"?-1:1));}
    else if(id==="press"&&(e.key==="Enter"||e.key===" ")){e.preventDefault();if(!A.locked&&!st.busy&&cfg.onPress)cfg.onPress();}};
  render();return{st,render,need,moveTo,push(done){if(st.busy||A.locked&&!A.lab)return;const ok=canLift(need(),st.S);st.busy=true;
    tween(ok?1200:700,p=>{st.a=ok?ease(p):0;render();},()=>{st.busy=false;render();done&&done(ok);});}};
}

/* Stable level ids and journey topology are preserved. Every pack starts with
   visible evidence, then manipulation, then use of the same relationship. */
const LEVER_PACKS={
 'lever.a1':[{t:'predict',poe:1,items:[[-2,10],[4,10]]},{t:'balance',items:[[-3,10]],pieces:[10]},{t:'predict',poe:1,items:[[-3,10],[3,10]]}],
 'lever.a2':[{t:'predict',poe:1,items:[[-1,20],[2,10]]},{t:'balance',items:[[-1,20]],pieces:[10]},{t:'balance',items:[[-2,20]],pieces:[10]},
             {t:'predict',poe:1,items:[[-4,5],[1,10]]},{t:'balance',items:[[-2,10]],pieces:[20]},{t:'predict',poe:1,items:[[-2,10],[1,20]]}],
 'lever.a3':[{t:'lift',W:60,S:20},{t:'lift',W:100,S:30},{t:'liftq',W:90,S:30,f:-3}],
 'lever.1':[{t:'predict',poe:1,items:[[-2,10],[4,10]]},{t:'balance',items:[[-3,10]],pieces:[10]},{t:'predict',items:[[-2,20],[4,10]]},
            {t:'predict',poe:1,items:[[-1,20],[2,10]]},{t:'balance',items:[[-2,20]],pieces:[10]},{t:'balance',items:[[-1,10],[-2,5]],pieces:[5]}],
 'lever.2':[{t:'predict',poe:1,items:[[-1,20],[2,10]]},{t:'balance',items:[[-3,20]],pieces:[10,20]},{t:'mystery',items:[[-2,'myA'],[4,10]]},
            {t:'predict',poe:1,items:[[-3,10],[-2,5],[2,20]]},{t:'balance',items:[[-5,5]],pieces:[5,10]},{t:'mystery',items:[[-3,'myB'],[4,10],[1,5]]}],
 'lever.3':[{t:'lift',W:60,S:20},{t:'lift',W:100,S:30},{t:'liftq',W:90,S:30,f:-3},
            {t:'predict',poe:1,items:[[-5,5],[-1,20],[3,10],[1,5]]},{t:'balance',items:[[-4,10],[-1,20]],pieces:[5,10,20]},{t:'mystery',items:[[-1,'myC'],[3,10]]}],
 'lever.4':[{t:'predict',poe:1,items:[[-3,10],[-2,5],[2,20]]},{gen:r=>levGenBalance(r,3)},{gen:r=>levGenMystery(r)},
            {t:'lift',W:120,S:25},{t:'lift',W:80,S:20},{t:'liftq',W:100,S:30,f:-3}]
};
Object.entries(LEVER_PACKS).forEach(([id,pack])=>defCh('lever',pack.map((sp,i)=>({
 id:`${id}.p${i+1}`,d:id==='lever.4'?1:0,phase:['see','try','apply'][i%3],
 terms:sp.t==='lift'||sp.t==='liftq'?['تکیه‌گاه','بازو']:['تکیه‌گاه','جرم'],
 teach:sp.t==='lift'||sp.t==='liftq'?'تکیه‌گاه نزدیک سنگ، نیروی کمتر می‌خواهد؛ سر دورتر تخته مسیر بیشتری می‌رود.':'اثر جرم و فاصله با هم تعیین می‌کند تخته به کدام طرف بچرخد.',
 mk:r=>Object.assign({},sp.gen?sp.gen(r):JSON.parse(JSON.stringify(sp)),{phase:['see','try','apply'][i%3]})
}))));
const leverPack=id=>LEVER_PACKS[id].map((_,i)=>`${id}.p${i+1}`);

const ST_lever={key:"lever",name:"اهرم",c:"#D97706",sub:"الاکلنگ، تکیه‌گاه و قانون اهرم",
 intro:"آجرها را روی تخته بگذار؛ تخته همان لحظه نشان می‌دهد کدام طرف پایین می‌رود. وقتی تخته صاف باشد، نشانگر تراز سبز می‌شود.",
 art(){let h=bgRoom(380).replace(/id="g/g,'id="al').replace(/url\(#g/g,"url(#al");h+=`<path d="M320 290 L284 380 H356Z" fill="#6B4A2B"/><g transform="rotate(-6 320 290)"><rect x="38" y="278" width="564" height="12" rx="5" fill="#D08A4B"/>${brickSvg(164,278,20)}${brickSvg(528,278,10)}${arrow(164,318,164,370,9,BLUE,.9)}${arrow(528,318,528,350,9,RED,.9)}</g>`;return h;},
 lab(A){A.prompt("آزمایشگاه اهرم: آجر یا جعبهٔ مرموز را روی تخته بگذار و ببین تخته چطور می‌چرخد. برای برداشتن، رویش بزن.");
   const lv=makeLever(A,{edit:"both",inf:[5,10,20,"myA","myB"],sup:false,live:true,hide:{}});A.refresh=()=>lv.render();
   const c=A.ctrl("");
   btn(c,"پاک کردن تخته","",()=>{lv.st.stacks={};lv.settle();});
   btn(c,"آزمایش بلند کردن سنگ","pri",()=>{A.prompt("آزمایشگاه: تکیه‌گاه را جابه‌جا کن و ببین نیروی لازم برای بلند کردن سنگ چطور عوض می‌شود.");let go;const lf=makeLift(A,{W:60,S:30,f:0,onPress:()=>go.click()});A.refresh=()=>lf.render();const c2=A.ctrl("");go=btn(c2,"فشار بده!","go",b=>{b.disabled=true;lf.push(ok=>{A.fb(ok?"سنگ بالا رفت!":"نیرویت کافی نبود؛ تکیه‌گاه را به سنگ نزدیک‌تر کن.",ok?"ok":"no");later(900,()=>{lf.st.a=0;lf.render();b.disabled=false;});});});btn(c2,"برگشت به الاکلنگ","pri",()=>ST_lever.lab(A));});},
 kid:[
  {id:"lever.a1",title:"الاکلنگ",desc:"ببین تخته چطور می‌چرخد؛ آجر را جابه‌جا کن تا صاف شود.",ch:leverPack("lever.a1")},
  {id:"lever.a2",title:"جرم و فاصله",desc:"آجر سنگین‌تر را نزدیک‌تر به تکیه‌گاه بگذار و تعادل را پیدا کن.",ch:leverPack("lever.a2")},
  {id:"lever.a3",title:"بلند کردن سنگ",desc:"با جابه‌جایی تکیه‌گاه سنگ را بلند کن و حرکت دو سر تخته را ببین.",ch:leverPack("lever.a3")}],
 levels:[
  {id:"lever.1",title:"الاکلنگ",desc:"چرخش را ببین، تخته را متعادل کن و نتیجه را در چیدمان تازه به کار ببر.",ch:leverPack("lever.1")},
  {id:"lever.2",title:"جرم و فاصله",desc:"تعادل را بساز؛ سپس با جرم و فاصلهٔ آجرها، جرم جعبه را پیدا کن.",ch:leverPack("lever.2")},
  {id:"lever.3",title:"بلند کردن با اهرم",desc:"سنگ را با تغییر تکیه‌گاه بلند کن؛ نیروی لازم و مسیر دو سر تخته را مقایسه کن.",ch:leverPack("lever.3")},
  {id:"lever.4",title:"چیدمان‌های تازه",desc:"تعادل، جرم نامعلوم و بلند کردن سنگ را در چیدمان‌های تازه بررسی کن.",ch:leverPack("lever.4")}],
 endless(r,d){const tp=pick(r,d<2?["predict","balance"]:d<3.5?["predict","balance","mystery","lift"]:["balance","mystery","lift","predict"]);
   if(tp==="predict")return levGenPredict(r,d<2?2:d<3.5?3:4);if(tp==="balance")return levGenBalance(r,d<2?1:d<3.5?2:3);if(tp==="mystery")return levGenMystery(r);
   const W=pick(r,[60,80,100,120]),f=ri(r,-4,-1);return{t:"lift",W,S:Math.floor(W*(f+5)/(5-f)/5)*5+5};},
 mount(sp,A){
  if(sp.t==='lift'||sp.t==='liftq'){
    const observe=sp.t==='liftq';
    A.prompt(observe?'با تکیه‌گاه نزدیک سنگ، تخته را فشار بده. حرکت سنگ و سرِ دست را دنبال کن.':KID()?'تکیه‌گاه نقطه‌ای است که تخته دور آن می‌چرخد. آن را جابه‌جا کن و سر راست تخته را فشار بده تا سنگ بالا برود.':`تکیه‌گاه نقطهٔ چرخش تخته است. سنگ ${fa(sp.W)} نیوتنی را با نیروی دستِ ${fa(sp.S)} نیوتن بلند کن. تکیه‌گاه را جابه‌جا کن و «فشار بده!» را بزن. فاصلهٔ سنگ تا تکیه‌گاه «بازوی مقاوم» و فاصلهٔ دست تا آن «بازوی محرک» است. تخته بی‌وزن است و اصطکاک را نادیده می‌گیریم.`);
    const c=A.ctrl('');let go;
    const press=()=>{if(A.locked||lf.st.busy||go.disabled)return;go.disabled=true;lf.push(ok=>{
      if(observe){go.remove();A.prompt('خط‌های بنفش، مسیر سنگ و سرِ دست را نشان می‌دهند. کدام سر تخته مسیر بیشتری رفت؟');
        const m=mcq(c,['سرِ دست که از تکیه‌گاه دورتر است','سرِ سنگ که به تکیه‌گاه نزدیک‌تر است','هر دو یک مسیر رفتند'],(i,b)=>{if(A.locked)return;
          A.judge(i===0,{ok:'سرِ دست از تکیه‌گاه دورتر بود و مسیر بیشتری رفت. در این چیدمان سنگ با نیروی کمتر بالا می‌رود؛ دست مسیر بیشتری طی می‌کند.',retry:'طول دو خط بنفش را مقایسه کن. سر دورتر از تکیه‌گاه مسیر بیشتری می‌رود.',final:'خط سمت راست بلندتر است؛ سرِ دست مسیر بیشتری رفت.'});if(A.locked){m.disable();m.mark(0,'right');}else{m.mark(i,'wrong');b.disabled=true;}});return;}
      const result=A.trial(ok,{pts:2,ok:KID()?'سنگ بالا رفت. تکیه‌گاه را نزدیک سنگ گذاشتی.':`سنگ بالا رفت. بازوی دست ${fa(5-lf.st.f)} و بازوی سنگ ${fa(lf.st.f+5)} خانه بود؛ نیروی دست از نیروی تعادلِ ${fa(Math.round(lf.need()*10)/10)} نیوتن بیشتر شد.`,
        retry:'سنگ بالا نرفت. تکیه‌گاه را به سنگِ سمت چپ نزدیک‌تر کن و دوباره فشار بده.',more:'فاصلهٔ دست از تکیه‌گاه بیشتر و فاصلهٔ سنگ کمتر می‌شود؛ نیروی لازم کاهش می‌یابد.',
        final:'تکیه‌گاه را نزدیک سنگ می‌گذاریم؛ سنگ با همین نیروی دست بالا می‌رود.',show:()=>{lf.st.f=-4;lf.st.a=1;lf.render();go.disabled=true;}});
      if(!result&&!A.locked){go.disabled=false;lf.st.a=0;lf.render();}
    });};
    const lf=makeLift(A,{W:sp.W,S:sp.S,f:observe?sp.f:2,paths:observe,onPress:press});
    A.refresh=()=>lf.render();go=btn(c,'فشار بده!','go',press);
    return;
  }
  /* پیش‌بینی: در اولین برخورد (سطح ۱ همیشه، و اولین مأموریت سطح‌های بالاتر) فقط حدس است و امتیاز ندارد؛
     بعد تخته رها می‌شود و سؤالِ امتیازدار دربارهٔ چیزی است که دیده. بعد از آن، با قانونِ نوشته‌شده در متن، پیش‌بینی امتیاز دارد. */
  if(sp.t==="predict"){const lv=makeLever(A,{items:sp.items,sup:true});A.refresh=()=>lv.render();const tL=lv.tq("L"),tR=lv.tq("R"),ans=tR>tL?0:tR===tL?1:2;
    const OPTS=["راست پایین می‌رود","صاف می‌ماند","چپ پایین می‌رود"];
    const expl=`چپ: ${fa(tL)} و راست: ${fa(tR)} (جرم × فاصله). ${ans===1?"برابرند؛ تخته صاف می‌ماند.":`طرف ${ans===0?"راست":"چپ"} پایین می‌رود.`}`;
    const kexp=ans===1?"دو طرف با هم برابر بودند؛ تخته صاف ماند.":`طرف ${ans===0?"راست":"چپ"} پایین رفت؛ آجرِ آن طرف سنگین‌تر است یا از وسط دورتر.`;
    if(KID()||sp.poe){poe(A,{prompt:KID()?"تکیه‌گاه جایی است که تخته دور آن می‌چرخد. حدس بزن کدام طرف پایین می‌رود. حدس امتیاز ندارد.":"تکیه‌گاه نقطهٔ چرخش تخته است. حدس بزن پس از رها کردن، تخته چه می‌شود. حدس امتیاز ندارد.",opts:OPTS,right:ans,reveal:(i,next)=>{lv.setSup(false);later(1100,next);}},
      {prompt:KID()?"تخته چه شد؟":"تخته چه شد؟ به کجیِ تخته نگاه کن.",opts:["راست پایین رفت","صاف ماند","چپ پایین رفت"],ans,ok:KID()?kexp:expl,retry:"دوباره به تخته نگاه کن: کدام سر پایین‌تر است؟"});return;}
    A.prompt(`تخته را رها می‌کنیم. تخته چه می‌شود؟ جرم × فاصله تا تکیه‌گاه را در دو طرف مقایسه کن.`);
    const c=A.ctrl("");const m=mcq(c,OPTS,(i,b)=>{if(A.locked)return;if(i===ans){m.disable();m.mark(i,"right");lv.setSup(false);A.judge(true,{ok:expl});}
      else{m.mark(i,"wrong");b.disabled=true;A.judge(false,{retry:"فقط جرم مهم نیست؛ فاصله از تکیه‌گاه هم مهم است. در هر طرف، جرم را در فاصله ضرب کن.",final:expl});if(A.locked){m.disable();m.mark(ans,"right");lv.setSup(false);}}});return;}
  if(sp.t==="balance"){A.prompt(KID()?"آجر را روی الاکلنگ بگذار تا صاف بماند.":`${sp.pieces.length>1?"آجرها را":"آجر را"} روی سمت راست تخته بگذار تا تخته صاف بماند.<small>آجر را از پایین صفحه بردار و روی تخته بگذار؛ تخته همان لحظه می‌چرخد. برای جابه‌جا کردن، آجر را دوباره بردار.</small>`);
    /* الاکلنگ زنده: پایه ندارد؛ وقتی همهٔ آجرها روی تخته‌اند و صاف ماند، چالش تمام است */
    const onSettle=()=>{if(A.locked)return;if(lv.st.pieces.some(p=>!p.used)){A.fb("");return;}const tL=lv.tq("L"),tR=lv.tq("R");
      if(tL===tR){A.judge(true,{pts:2,act:true,ok:KID()?"الاکلنگ صاف ماند!":`جرم × فاصله در هر دو طرف ${fa(tL)} شد. فاصلهٔ آجرها و جرم آن‌ها با هم تعیین‌کننده‌اند.`});return;}
      guide(KID()?(tR>tL?"راست پایین رفت. آجر را به وسط نزدیک‌تر کن.":"چپ پایین رفت. آجر را دورتر بگذار."):`چپ ${fa(tL)} است و راست ${fa(tR)}. ${tR>tL?"راست پایین رفته است؛ آجر را به تکیه‌گاه نزدیک‌تر کن.":"چپ پایین رفته است؛ آجر را دورتر بگذار."}`);};
    const guide=message=>A.trial(false,{retry:message,more:KID()?"آجر را به تکیه‌گاه نزدیک‌تر یا از آن دورتر کن و کجیِ تخته را ببین.":"جرم × فاصله در دو طرف باید برابر شود. جای هر آجر را جداگانه تغییر بده.",final:KID()?"این چیدمان تخته را صاف می‌کند.":levSol(sp),show:()=>{const sol=levPlacement(sp);lv.st.stacks={};sp.items.forEach(([p,it])=>{(lv.st.stacks[p]=lv.st.stacks[p]||[]).push(Object.assign({fixed:1},typeof it==="number"?{k:"b",m:it}:{k:"o",id:it}));});sol.forEach((p,i)=>{(lv.st.stacks[p]=lv.st.stacks[p]||[]).push(Object.assign({},lv.st.pieces[i].it,{pid:lv.st.pieces[i].id}));lv.st.pieces[i].used=true;});lv.st.sel=null;lv.st.tw=(lv.st.tw||0)+1;lv.st.busy=false;lv.st.a=0;lv.render();}});
    const lv=makeLever(A,{items:sp.items,pieces:sp.pieces,edit:"R",sup:false,live:true,onSettle});A.refresh=()=>lv.render();const c=A.ctrl("");btn(c,"راهنمای چیدن","",()=>guide("برای تعادل، جای آجرهای سمت راست را تغییر بده."));
    A.hint(`M${320+(0-(sp.pieces.length-1)/2)*Math.min(96,560/sp.pieces.length)} 478 L${320+3*52} 250`);return;}
  if(sp.t==="mystery"){const my=sp.items.find(x=>typeof x[1]==="string")[1];A.prompt(`تخته صاف است، پس جرم × فاصله در دو طرف برابر است. جرم ${OB[my].n} چند کیلوگرم است؟`);
    const lv=makeLever(A,{items:sp.items,sup:false,hide:{[my]:1}});A.refresh=()=>lv.render();const tR=lv.tq("R"),pos=Math.abs(sp.items.find(x=>x[1]===my)[0]),ans=LV_MASS[my];
    const c=A.ctrl("");const stp=stepper(c,{init:0,max:200,steps:[1,5],unit:"کیلوگرم"});
    const chk=btn(c,"بررسی","go",()=>{const ok=stp.get()===ans;A.judge(ok,{ok:`${fa(ans)} × ${fa(pos)} = ${fa(tR)}، همان مقدار سمت راست.`,retry:`اول جرم × فاصلهٔ سمت راست را حساب کن (${S.nums?fa(tR):"جمع آن"}). بعد آن را بر فاصلهٔ جعبه تقسیم کن.`,final:`جرم × فاصلهٔ سمت راست ${fa(tR)} است؛ ${fa(tR)} ÷ ${fa(pos)} = ${fa(ans)} کیلوگرم.`});if(A.locked){chk.disabled=true;stp.disable();lv.st.hide={};lv.render();}});return;}
 }};
function liftBest(W,Sv){let best=null;for(let f=-4;f<=4;f++)if(canLift(W*(f+5)/(5-f),Sv))best=f;return best==null?1:best+5;}
function levPlacement(sp){const tL=sp.items.filter(x=>x[0]<0).reduce((s,x)=>s+Math.abs(x[0])*(typeof x[1]==="number"?x[1]:LV_MASS[x[1]]),0)-0;const tRfix=sp.items.filter(x=>x[0]>0).reduce((s,x)=>s+x[0]*x[1],0);const need=tL-tRfix;
  const ps=sp.pieces;let out=null;(function f(i,acc,sum){if(out)return;if(i===ps.length){if(sum===need)out=acc.slice();return;}for(let p=1;p<=5;p++){acc.push([ps[i],p]);f(i+1,acc,sum+ps[i]*p);acc.pop();}})(0,[],0);
  return out?out.map(([m,p])=>p):[];}
function levSol(sp){return levPlacement(sp).map((p,i)=>`آجر ${fa(sp.pieces[i])} کیلوگرمی روی خانهٔ ${fa(p)}`).join(" و ");}
function levGenPredict(r,n){for(let k=0;k<200;k++){const items=[];const used=new Set();for(let i=0;i<n;i++){let p;do{p=ri(r,1,5)*(i%2?1:-1);}while(used.has(p));used.add(p);items.push([p,pick(r,[5,10,20])]);}
  const tL=items.filter(x=>x[0]<0).reduce((s,x)=>s-x[0]*x[1],0),tR=items.filter(x=>x[0]>0).reduce((s,x)=>s+x[0]*x[1],0);if(Math.abs(tL-tR)<=15||r()<.3)return{t:"predict",items};}return{t:"predict",items:[[-2,10],[4,5]]};}
function levGenBalance(r,np){for(let k=0;k<400;k++){const pieces=Array.from({length:Math.max(1,np-1)},()=>pick(r,[5,10,20]));const pos=pieces.map(()=>ri(r,1,5));const need=pieces.reduce((s,m,i)=>s+m*pos[i],0);
  const nl=ri(r,1,2),items=[];let rem=need,ok=true;const used=new Set();for(let i=0;i<nl;i++){if(i===nl-1){let f=false;for(const m of shuffle(r,[5,10,20]))for(let p=1;p<=5;p++)if(!f&&!used.has(p)&&m*p===rem){items.push([-p,m]);f=true;}if(!f)ok=false;}else{const m=pick(r,[5,10,20]),p=ri(r,1,5);if(m*p>=rem){ok=false;break;}used.add(p);items.push([-p,m]);rem-=m*p;}}
  if(ok&&items.length)return{t:"balance",items,pieces};}return{t:"balance",items:[[-2,10]],pieces:[5]};}
function levGenMystery(r){for(let k=0;k<300;k++){const my=pick(r,["myA","myB","myC"]),m=LV_MASS[my],p=ri(r,1,5),T=m*p;const items=[[-p,my]];let rem=T;const used=new Set();let ok=true;for(let i=0;i<2&&rem>0;i++){let f=false;for(const w of shuffle(r,[20,10,5]))for(const q of shuffle(r,[1,2,3,4,5]))if(!f&&!used.has(q)&&w*q<=rem&&(i===1?w*q===rem:true)){items.push([q,w]);used.add(q);rem-=w*q;f=true;}if(!f){ok=false;break;}}
  if(ok&&rem===0)return{t:"mystery",items};}return{t:"mystery",items:[[-2,"myA"],[4,10]]};}
