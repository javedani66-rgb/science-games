/* ================= ایستگاه اهرم (الاکلنگ) ================= */
const LV_MASS={myA:20,myB:15,myC:30};
function brickSvg(x,yb,m,hl){const w=52,h=m/5*13+3;let s=`<rect x="${x-w/2}" y="${yb-h}" width="${w}" height="${h}" rx="3" fill="#C8553D" stroke="${hl?"#1E6FD9":"#8E3322"}" stroke-width="${hl?3.5:1.5}"/>`;
  for(let y=yb-13;y>yb-h+2;y-=13)s+=`<line x1="${x-w/2}" y1="${y}" x2="${x+w/2}" y2="${y}" stroke="#EBA08E" stroke-width="1.5"/>`;
  return `<g>${s}${KID()?"":T(x,yb-h/2+4,`${fa(m)} کیلوگرم`,{size:m===5?9:10,col:"#fff",halo:false})}</g>`;}
const lvItemH=it=>it.k==="b"?it.m/5*13+3:OB[it.id].h*.85;
function lvItemSvg(it,x,yb,hl){if(it.k==="b")return brickSvg(x,yb,it.m,hl);return `<g transform="translate(${x} ${yb}) scale(.85)">${OB[it.id].d}</g>`;}
const lvM=it=>it.k==="b"?it.m:LV_MASS[it.id];

function makeLever(A,cfg){
  const svg=A.svg,P=A.P;A.view(cfg.edit?520:404);const PX=52,CX=320,CY=290;
  const st={stacks:{},pieces:(cfg.pieces||[]).map((m,i)=>({id:i,it:typeof m==="number"?{k:"b",m}:{k:"o",id:m},used:false})),inf:cfg.inf||null,edit:cfg.edit||"",sup:cfg.sup!==false,a:0,sel:null,hover:null,busy:false,hide:cfg.hide||{}};
  (cfg.items||[]).forEach(([p,it])=>{(st.stacks[p]=st.stacks[p]||[]).push(Object.assign({fixed:1},typeof it==="number"?{k:"b",m:it}:{k:"o",id:it}));});
  const tq=side=>Object.keys(st.stacks).reduce((s,p)=>{p=+p;if((side==="L"&&p<0)||(side==="R"&&p>0))s+=Math.abs(p)*st.stacks[p].reduce((a,it)=>a+lvM(it),0);return s;},0);
  const termStr=side=>Object.keys(st.stacks).map(Number).filter(p=>side==="L"?p<0:p>0).sort((a,b)=>Math.abs(a)-Math.abs(b)).filter(p=>st.stacks[p].length).map(p=>{const hid=st.stacks[p].some(it=>st.hide[it.id]);return hid?`؟ × ${fa(Math.abs(p))}`:`${fa(st.stacks[p].reduce((a,it)=>a+lvM(it),0))} × ${fa(Math.abs(p))}`;}).join(" + ")||"۰";
  const hasHidden=side=>Object.keys(st.stacks).map(Number).some(p=>(side==="L"?p<0:p>0)&&st.stacks[p].some(it=>st.hide[it.id]));
  const canEdit=p=>!A.locked&&(st.sup||cfg.live)&&(st.edit==="both"||(st.edit==="R"&&p>0)||(st.edit==="L"&&p<0));
  function render(){const tL=tq("L"),tR=tq("R"),bal=!st.sup&&tL===tR;
    let s=bgRoom(380);
    s+=`<g transform="translate(20 20)"><rect width="140" height="40" rx="12" fill="#fff" stroke="#C7D3DE" stroke-width="2"/><rect x="14" y="13" width="112" height="14" rx="7" fill="${bal?"#CDEFD9":"#E9EFF3"}" stroke="${bal?GRN:"#B8C6D3"}" stroke-width="2"/><line x1="70" y1="10" x2="70" y2="30" stroke="${bal?GRN:"#9FB0C0"}" stroke-width="2"/><circle cx="${70+clamp(st.a*3.2,-46,46)}" cy="20" r="6" fill="${bal?GRN:"#7D8CA3"}"/></g>`+T(90,78,bal?"تراز است":"تراز",{size:13,col:bal?GRN:MUT,halo:false});
    s+=`<path d="M${CX} ${CY} L${CX-36} 380 H${CX+36}Z" fill="#6B4A2B"/><path d="M${CX} ${CY} L${CX-18} 380 H${CX}Z" fill="#8A6443"/>`;
    if(st.sup)for(const x of[86,554])s+=`<rect x="${x-11}" y="${CY}" width="22" height="${380-CY}" fill="#E8590C"/><path d="M${x-11} ${CY+20} l22 -12 M${x-11} ${CY+44} l22 -12 M${x-11} ${CY+68} l22 -12" stroke="#fff" stroke-width="4" opacity=".6"/>`;
    let g=`<rect x="${CX-282}" y="${CY-12}" width="564" height="12" rx="5" fill="#D08A4B"/><rect x="${CX-282}" y="${CY-12}" width="564" height="4" rx="2" fill="#EAB47C"/>`;
    for(let p=-5;p<=5;p++){if(!p)continue;const x=CX+p*PX;g+=`<line x1="${x}" y1="${CY-12}" x2="${x}" y2="${CY}" stroke="#8A5427" stroke-width="2"/>`+T(x,CY+26,fa(Math.abs(p)),{size:19,col:"#6B4A2B",halo:false});}
    for(let p=-5;p<=5;p++){if(!p)continue;const x=CX+p*PX,items=st.stacks[p]||[];let yb=CY-12;
      if(canEdit(p)&&(st.sel||st.hover===p)){g+=`<g data-zone="pos" data-p="${p}" style="cursor:pointer"><circle cx="${x}" cy="${CY-24}" r="${st.hover===p?20:15}" fill="${st.hover===p?"#FFF3C4":"#fff"}" stroke="#F0B429" stroke-width="2.5" stroke-dasharray="4 3"/></g>`;}
      else if(canEdit(p))g+=`<g data-zone="pos" data-p="${p}"><rect x="${x-24}" y="${CY-90}" width="48" height="90" fill="#fff" fill-opacity="0"/></g>`;
      items.forEach((it,i)=>{const drag=canEdit(p)&&!it.fixed;g+=`<g ${drag?`data-drag="stk" data-p="${p}" data-i="${i}" style="cursor:grab"`:""}>${lvItemSvg(it,x,yb)}</g>`;yb-=lvItemH(it)+1;});
      if(S.forces&&items.length){const m=items.reduce((a,it)=>a+lvM(it),0),hid=items.some(it=>st.hide[it.id]),len=hid?40:16+m*1.6;g+=arrow(x,CY+40,x,CY+40+len,9,p<0?BLUE:RED,.9);}}
    s+=`<g transform="rotate(${st.a} ${CX} ${CY})">${g}</g>`;
    if(st.edit){s+=trayPanel("",404);
      const list=st.inf?st.inf.map((m,i)=>({id:"i"+i,it:typeof m==="number"?{k:"b",m}:{k:"o",id:m}})):st.pieces.filter(pc=>!pc.used);const n=list.length;
      list.forEach((pc,j)=>{const x=320+(j-(n-1)/2)*Math.min(96,560/Math.max(n,1)),sel=st.sel&&st.sel.pid===pc.id;s+=`<g data-drag="tray" data-pid="${pc.id}" style="cursor:grab"><rect x="${x-44}" y="418" width="88" height="90" rx="12" fill="${sel?"#FFF3C4":"#fff"}" fill-opacity="${sel?1:0}"/><g transform="translate(${x} 500) scale(1.25) translate(${-x} -500)">${lvItemSvg(pc.it,x,500,sel)}</g></g>`;});}
    P.paint(s);
    const hl=hasHidden("L"),hr=hasHidden("R");
    A.counter(`<span class="cc l">چپ (جرم × فاصله): <b class="num">${hl?"؟":fa(tL)}</b></span><span class="cc r">راست (جرم × فاصله): <b class="num">${hr?"؟":fa(tR)}</b></span>`);
    A.formula(FX(`${sy("m","1")} × ${sy("d","1")} = ${sy("m","2")} × ${sy("d","2")}`,`${termStr("L")} ${tL===tR?"=":"≠"} ${termStr("R")}`,[[`${sy("m","1")}، ${sy("m","2")}`,"جرم هر طرف (kg)؛ چون جاذبه دو طرف یکی است، می‌شود به‌جای وزن، جرم گذاشت"],[`${sy("d","1")}، ${sy("d","2")}`,"فاصله از تکیه‌گاه (تعداد خانه)"]]));}
  function settle(done){const tL=tq("L"),tR=tq("R");const to=st.sup||tL===tR?0:(tR>tL?14:-14);const from=st.a,id=st.tw=(st.tw||0)+1;if(Math.abs(to-from)<.01){render();done&&done();return;}st.busy=true;tween(700,p=>{if(id!==st.tw)return;st.a=from+(to-from)*ease(p);render();},()=>{if(id!==st.tw)return;st.busy=false;render();done&&done();});}
  const posAt=pt=>{if(pt.y<CY-200||pt.y>CY+40)return null;const p=Math.round((pt.x-CX)/PX);if(!p||Math.abs(p)>5)return null;return canEdit(p)?p:null;};
  const findPc=pid=>{if(st.inf){const i=+String(pid).slice(1),m=st.inf[i];return typeof m==="number"?{k:"b",m}:{k:"o",id:m};}const pc=st.pieces.find(q=>String(q.id)===String(pid));return pc?pc.it:null;};
  const put=(p,g)=>{(st.stacks[p]=st.stacks[p]||[]).push(Object.assign({},g.it,{pid:g.pid}));if(!st.inf){const pc=st.pieces.find(q=>String(q.id)===String(g.pid));if(pc)pc.used=true;}};
  const unput=(p,i)=>{const it=st.stacks[p].splice(i,1)[0];if(!st.inf&&it.pid!=null){const pc=st.pieces.find(q=>String(q.id)===String(it.pid));if(pc)pc.used=false;}return it;};
  dragKit(svg,{blocked:()=>A.locked,
    start(d){if(d.drag==="tray"){const it=findPc(d.pid);return it?{from:"tray",pid:d.pid,it}:null;}if(d.drag==="stk"){const p=+d.p;if(!canEdit(p))return null;return{from:"stk",p,i:+d.i,it:st.stacks[p][+d.i]};}return null;},
    begin(g,pt){if(g.from==="stk"){const it=unput(g.p,g.i);g.pid=it.pid;}st.sel=null;P.ghost(lvItemSvg(g.it,0,20,true),pt.x,pt.y);render();},
    move(g,pt){P.move(pt.x,pt.y);const p=posAt(pt);if(p!==st.hover){st.hover=p;render();}},
    end(g,pt){P.clear();st.hover=null;const p=posAt(pt);if(p!=null)put(p,g);settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();},
    tap(g){if(g.from==="tray"){st.sel={pid:g.pid,it:g.it};A.fb("حالا روی جای دلخواه روی تخته بزن.","info");render();}else{unput(g.p,g.i);settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();}},
    zoneTap(z){if(z.zone==="pos"&&st.sel){const p=+z.p;if(!canEdit(p))return;put(p,st.sel);st.sel=null;A.fb("");settle(cfg.onSettle);if(cfg.onChange)cfg.onChange();}}});
  settle();
  return{st,render,settle,tq,setSup(v,done){st.sup=v;settle(done);}};
}

function makeLift(A,cfg){const svg=A.svg,P=A.P;A.view(424);const PX=52,CX=320,CY=300;const st={f:cfg.f==null?0:cfg.f,a:0,busy:false,W:cfg.W,S:cfg.S};
  const need=()=>st.W*(st.f+5)/(5-st.f);
  function render(){const F=need(),ok=canLift(F,st.S);let s=bgOut(380);
    const fx=CX+st.f*PX;
    let g=`<rect x="${CX-282}" y="${CY-12}" width="564" height="12" rx="5" fill="#D08A4B"/><rect x="${CX-282}" y="${CY-12}" width="564" height="4" rx="2" fill="#EAB47C"/>`;
    for(let p=-5;p<=5;p++){const x=CX+p*PX;g+=`<line x1="${x}" y1="${CY-12}" x2="${x}" y2="${CY}" stroke="#8A5427" stroke-width="2"/>`;}
    g+=`<g transform="translate(${CX-5*PX} ${CY-12})"><path d="M-40 0 Q-48 -38 -16 -58 Q16 -70 40 -44 Q52 -18 40 0Z" fill="#8D96A3"/><path d="M-40 0 Q-6 -14 40 0Z" fill="#6F7885"/>${T(0,-22,kn(st.W),{size:20,col:"#fff",halo:false})}</g>`;
    const ex=CX+5*PX;if(S.forces)g+=arrow(ex,CY-100,ex,CY-16,Math.max(8,Math.min(20,F/5)),ok?GRN:RED)+T(ex-34,CY-80,`نیروی لازم<tspan class="num">: ${fa(Math.round(F*10)/10)}</tspan>`,{size:14,col:ok?GRN:RED,anchor:"start"});
    s+=`<g transform="rotate(${st.a} ${fx} ${CY})">${g}</g>`;
    s+=`<g data-drag="fulcrum" style="cursor:ew-resize"><path d="M${fx} ${CY} L${fx-34} 380 H${fx+34}Z" fill="#6B4A2B" stroke="#FFC43D" stroke-width="3"/><rect x="${fx-44}" y="${CY}" width="88" height="84" fill="#fff" fill-opacity="0"/>${T(fx,368,"⟷",{size:26,col:"#FFC43D",halo:false})}</g>`;
    s+=T((CX-5*PX+fx)/2,406,`بازوی مقاوم: ${fa(st.f+5)}`,{size:12,col:INK})+T((fx+CX+5*PX)/2,406,`بازوی محرک: ${fa(5-st.f)}`,{size:12,col:INK});
    s+=gBar(F,st.S,150,36,260);
    
    P.paint(s);
    A.counter(`<span class="cc">بار: <b class="num">${fa(st.W)} نیوتن</b></span><span class="cc">بازوی مقاوم: <b>${fa(st.f+5)}</b></span><span class="cc">بازوی محرک: <b>${fa(5-st.f)}</b></span><span class="cc ${ok?"":"r"}">نیروی لازم: <b class="num">${fa(Math.round(F*10)/10)} نیوتن</b></span>`);
    A.formula(FX(`${sy("F","1")} × ${sy("d","1")} = ${sy("F","2")} × ${sy("d","2")}`,`${sy("F","1")} = ${fa(st.W)} × ${fa(st.f+5)} ÷ ${fa(5-st.f)} = ${fa(Math.round(F*10)/10)} N`,[[sy("F","1"),"نیروی محرک (دست تو)"],[sy("d","1"),"بازوی محرک"],[sy("F","2"),"نیروی مقاوم (وزن سنگ)"],[sy("d","2"),"بازوی مقاوم"]])+FX(`${sy("MA")} = ${sy("F","2")} ÷ ${sy("F","1")}`,`${sy("MA")} = ${fa(st.W)} ÷ ${fa(Math.round(F*10)/10)} ${Math.abs(st.W/F-Math.round(st.W/F*10)/10)<1e-9?"=":"≈"} ${fa(Math.round(st.W/F*10)/10)}`,[[sy("MA"),"مزیت مکانیکی"]]));}
  dragKit(svg,{blocked:()=>A.locked||st.busy,start(d){return d.drag==="fulcrum"?{}:null;},begin(){},move(g,p){const f=clamp(Math.round((p.x-CX)/PX),-4,4);if(f!==st.f){st.f=f;render();}},end(){render();},tap(){}});
  render();
  return{st,render,need,push(done){const F=need(),ok=canLift(F,st.S);st.busy=true;const fx=CX+st.f*PX,maxA=Math.asin(Math.min(1,(380-CY)/(5-st.f)/PX))*180/Math.PI;
    if(ok)tween(1200,p=>{st.a=Math.min(maxA,16)*ease(p);render();},()=>{st.busy=false;done&&done(true);});
    else tween(900,p=>{st.a=Math.sin(p*Math.PI*3)*1.5*(1-p);render();},()=>{st.a=0;st.busy=false;render();done&&done(false);});}};
}

const ST_lever={key:"lever",name:"اهرم",c:"#D97706",sub:"الاکلنگ، تکیه‌گاه و قانون اهرم",
 intro:"آجرها را روی تخته بکش؛ تخته همان لحظه نشان می‌دهد کدام طرف سنگین‌تر است. وقتی تخته صاف باشد، نشانگر تراز سبز می‌شود.",
 art(){let h=bgRoom(380).replace(/id="g/g,'id="al').replace(/url\(#g/g,"url(#al");h+=`<path d="M320 290 L284 380 H356Z" fill="#6B4A2B"/><g transform="rotate(-6 320 290)"><rect x="38" y="278" width="564" height="12" rx="5" fill="#D08A4B"/>${brickSvg(164,278,20)}${brickSvg(528,278,10)}${arrow(164,318,164,370,9,BLUE,.9)}${arrow(528,318,528,350,9,RED,.9)}</g>`;return h;},
 lab(A){A.prompt("آزمایشگاه اهرم: آجر یا جعبهٔ مرموز را روی تخته بکش و ببین تخته چطور می‌چرخد. برای برداشتن، بیرونش بکش یا رویش بزن.");
   const lv=makeLever(A,{edit:"both",inf:[5,10,20,"myA","myB"],sup:false,live:true,hide:{}});A.refresh=()=>lv.render();
   const c=A.ctrl("");
   btn(c,"پاک کردن تخته","",()=>{lv.st.stacks={};lv.settle();});
   btn(c,"آزمایش بلند کردن سنگ","pri",()=>{A.prompt("آزمایشگاه: تکیه‌گاه را جابه‌جا کن و ببین نیروی لازم برای بلند کردن سنگ چطور عوض می‌شود.");const lf=makeLift(A,{W:60,S:30,f:0});A.refresh=()=>lf.render();const c2=A.ctrl("");btn(c2,"فشار بده!","go",b=>{b.disabled=true;lf.push(ok=>{A.fb(ok?"سنگ بالا رفت!":"نیرویت کافی نبود؛ تکیه‌گاه را به سنگ نزدیک‌تر کن.",ok?"ok":"no");later(900,()=>{lf.st.a=0;lf.render();b.disabled=false;});});});btn(c2,"برگشت به الاکلنگ","pri",()=>ST_lever.lab(A));});},
 kid:[
  {title:"الاکلنگ",desc:"پیش‌بینی کن کدام طرف پایین می‌رود و آجر را درست بگذار.",gen(r){return[{t:"predict",items:[[-2,10],[4,10]]},{t:"predict",items:[[-2,20],[2,10]]},{t:"balance",items:[[-3,10]],pieces:[10]},{t:"predict",items:[[-3,10],[3,10]]},{t:"balance",items:[[-1,10]],pieces:[10]}];}},
  {title:"سنگین‌تر نزدیک‌تر",desc:"آجر سنگین را نزدیک وسط و آجر سبک را دور بگذار.",gen(r){return[{t:"balance",items:[[-1,20]],pieces:[10]},{t:"predict",items:[[-1,20],[2,10]]},{t:"balance",items:[[-2,20]],pieces:[10]},{t:"predict",items:[[-4,5],[1,10]]},{t:"balance",items:[[-2,10]],pieces:[20]}];}},
  {title:"بلند کردن سنگ",desc:"با جابه‌جا کردن تکیه‌گاه، سنگ سنگین را با نیروی کم بلند کن.",gen(r){return[{t:"lift",W:60,S:20},{t:"balance",items:[[-4,5]],pieces:[20]},{t:"lift",W:100,S:30},{t:"predict",items:[[-1,20],[4,5]]},{t:"lift",W:90,S:15}];}}],
 levels:[
  {title:"الاکلنگ",desc:"پیش‌بینی کن تخته به کدام طرف می‌چرخد و آجر را جایی بگذار که صاف بماند.",gen(r){return[{t:"predict",items:[[-2,10],[4,10]]},{t:"balance",items:[[-3,10]],pieces:[10]},{t:"predict",items:[[-1,20],[2,10]]},{t:"balance",items:[[-2,20]],pieces:[10]},{t:"predict",items:[[-4,5],[1,10]]},{t:"balance",items:[[-1,10],[-2,5]],pieces:[5]}];}},
  {title:"جرم × فاصله",desc:"قانون اهرم: جرم × فاصله تا تکیه‌گاه در دو طرف برابر است. با آن جرم جعبه‌های مرموز را پیدا کن.",gen(r){return[{t:"balance",items:[[-3,20]],pieces:[10,20]},{t:"mystery",items:[[-2,"myA"],[4,10]]},{t:"predict",items:[[-3,10],[-2,5],[2,20]]},{t:"balance",items:[[-5,5]],pieces:[5,10]},{t:"mystery",items:[[-3,"myB"],[4,10],[1,5]]},{t:"predict",items:[[-2,20],[5,5],[1,10]]}];}},
  {title:"بلند کردن با اهرم",desc:"تکیه‌گاه را جابه‌جا کن تا با نیروی کم، سنگ سنگین را بلند کنی.",gen(r){return[{t:"lift",W:60,S:20},{t:"mystery",items:[[-1,"myC"],[3,10]]},{t:"balance",items:[[-4,10],[-1,20]],pieces:[5,10,20]},{t:"lift",W:100,S:30},{t:"predict",items:[[-5,5],[-1,20],[3,10],[1,5]]},{t:"lift",W:90,S:15}];}},
  {title:"قهرمان اهرم",desc:"چند آجر، چند جای مختلف و جعبه‌های مرموز. همه را با قانون اهرم حل کن.",gen(r){return[levGenBalance(r,3),levGenMystery(r),{t:"lift",W:120,S:25},levGenPredict(r,4),levGenBalance(r,3),levGenMystery(r)];}}],
 endless(r,d){const tp=pick(r,d<2?["predict","balance"]:d<3.5?["predict","balance","mystery","lift"]:["balance","mystery","lift","predict"]);
   if(tp==="predict")return levGenPredict(r,d<2?2:d<3.5?3:4);if(tp==="balance")return levGenBalance(r,d<2?1:d<3.5?2:3);if(tp==="mystery")return levGenMystery(r);
   const W=pick(r,[60,80,100,120]),f=ri(r,-4,-1);return{t:"lift",W,S:Math.floor(W*(f+5)/(5-f)/5)*5+5};},
 mount(sp,A){
  if(sp.t==="lift"){A.hint("M424 340 L216 340");A.prompt(KID()?"تکیه‌گاه را جابه‌جا کن تا بتوانی سنگ را بلند کنی. هر چند بار خواستی امتحان کن.":`سنگ ${fa(sp.W)} نیوتنی را بلند کن. نیروی تو فقط <b>${fa(sp.S)} نیوتن</b> است. هر چند بار خواستی امتحان کن.<small>تکیه‌گاه را بکش و جابه‌جا کن، بعد «فشار بده!» را بزن.</small>`);
    const lf=makeLift(A,{W:sp.W,S:sp.S,f:2});A.refresh=()=>lf.render();const c=A.ctrl("");
    const go=btn(c,"فشار بده!","go",()=>{go.disabled=true;lf.push(ok=>{const res=A.trial(ok,{k:{ok:"سنگ بالا رفت! تکیه‌گاه نزدیک سنگ بود.",retry:"تکیه‌گاه را به سنگ نزدیک‌تر کن.",final:"تکیه‌گاه باید خیلی نزدیک سنگ باشد."},ok:`بازوی محرک ${fa(5-lf.st.f)} و بازوی مقاوم ${fa(lf.st.f+5)} خانه است؛ نیروی لازم ${fa(Math.round(lf.need()*10)/10)} نیوتن شد.`,retry:"تکیه‌گاه را به سنگ نزدیک‌تر کن تا بازوی محرک بلندتر شود.",final:`تکیه‌گاه باید نزدیک سنگ باشد؛ آن را جایی بگذار که بازوی مقاوم ${fa(liftBest(sp.W,sp.S))} خانه شود.`});if(!res&&!A.locked)go.disabled=false;});});
    return;}
  if(sp.t==="predict"){A.prompt(KID()?"پایه‌ها را برمی‌داریم. کدام طرف پایین می‌رود؟":`وقتی پایه‌ها را برداریم، تخته چه می‌شود؟<small>جرم آجرها و فاصله‌شان تا تکیه‌گاه را نگاه کن و پیش‌بینی کن.</small>`);
    const lv=makeLever(A,{items:sp.items,sup:true});A.refresh=()=>lv.render();const tL=lv.tq("L"),tR=lv.tq("R"),ans=tR>tL?0:tR===tL?1:2;
    const expl=`چپ: ${fa(tL)} و راست: ${fa(tR)} (جرم × فاصله). ${ans===1?"برابرند؛ تخته صاف می‌ماند.":`طرف ${ans===0?"راست":"چپ"} پایین می‌رود.`}`;
    const KL={ok:ans===1?"دو طرف مثل هم است؛ صاف ماند.":`طرف ${ans===0?"راست":"چپ"} پایین رفت.`,retry:"به سنگینی آجرها و دوری‌شان از وسط نگاه کن.",final:ans===1?"دو طرف مثل هم بود؛ صاف ماند.":`طرف ${ans===0?"راست":"چپ"} پایین رفت، چون ${"آجرش سنگین‌تر یا دورتر از وسط است"}.`};
    const c=A.ctrl("");const m=mcq(c,["راست پایین می‌رود","صاف می‌ماند","چپ پایین می‌رود"],(i,b)=>{if(A.locked)return;if(i===ans){m.disable();m.mark(i,"right");lv.setSup(false);A.judge(true,{ok:expl,k:KL});}
      else{m.mark(i,"wrong");b.disabled=true;A.judge(false,{retry:"فقط جرم مهم نیست؛ فاصله از تکیه‌گاه هم مهم است. جرم را در فاصله ضرب کن.",final:expl,k:KL});if(A.locked){m.disable();m.mark(ans,"right");lv.setSup(false);}}});return;}
  if(sp.t==="balance"){A.prompt(KID()?"آجر را روی الاکلنگ بگذار تا صاف بماند.":`${sp.pieces.length>1?"آجرها را":"آجر را"} روی سمت راست تخته بگذار تا تخته صاف بماند.<small>بکش و روی تخته رها کن؛ تخته همان لحظه می‌چرخد. برای جابه‌جا کردن، آجر را دوباره بکش.</small>`);
    /* الاکلنگ زنده: پایه ندارد؛ وقتی همهٔ آجرها روی تخته‌اند و صاف ماند، چالش تمام است */
    const onSettle=()=>{if(A.locked)return;if(lv.st.pieces.some(p=>!p.used)){A.fb("");return;}const tL=lv.tq("L"),tR=lv.tq("R");
      if(tL===tR){A.trial(true,{ok:`هر دو طرف ${fa(tL)} شد.`,k:{ok:"الاکلنگ صاف ماند!"}});return;}
      A.fb(KID()?(tR>tL?"راست پایین رفت. آجر را به وسط نزدیک‌تر کن.":"چپ پایین رفت. آجر را دورتر بگذار."):`چپ ${fa(tL)} است و راست ${fa(tR)}. ${tR>tL?"راست سنگین‌تر است؛ آجر را به تکیه‌گاه نزدیک‌تر کن.":"چپ سنگین‌تر است؛ آجر را دورتر بگذار."}`,"info");};
    const lv=makeLever(A,{items:sp.items,pieces:sp.pieces,edit:"R",sup:false,live:true,onSettle});A.refresh=()=>lv.render();A.ctrl("");
    A.hint(`M${320+(0-(sp.pieces.length-1)/2)*Math.min(96,560/sp.pieces.length)} 478 L${320+3*52} 250`);return;}
  if(sp.t==="mystery"){const my=sp.items.find(x=>typeof x[1]==="string")[1];A.prompt(`تخته صاف است. جرم ${OB[my].n} چند کیلوگرم است؟<small>از قانون اهرم استفاده کن: جرم × فاصله در دو طرف برابر است.</small>`);
    const lv=makeLever(A,{items:sp.items,sup:false,hide:{[my]:1}});A.refresh=()=>lv.render();const tR=lv.tq("R"),pos=Math.abs(sp.items.find(x=>x[1]===my)[0]),ans=LV_MASS[my];
    const c=A.ctrl("");const stp=stepper(c,{init:0,max:200,steps:[1,5],unit:"کیلوگرم"});
    const chk=btn(c,"بررسی","go",()=>{const ok=stp.get()===ans;A.judge(ok,{ok:`${fa(ans)} × ${fa(pos)} = ${fa(tR)}، همان مقدار سمت راست.`,retry:`اول جرم × فاصلهٔ سمت راست را حساب کن (${S.nums?fa(tR):"جمع آن"}). بعد آن را بر فاصلهٔ جعبه تقسیم کن.`,final:`سمت راست ${fa(tR)} است؛ ${fa(tR)} ÷ ${fa(pos)} = ${fa(ans)} کیلوگرم.`});if(A.locked){chk.disabled=true;stp.disable();lv.st.hide={};lv.render();}});return;}
 }};
function liftBest(W,Sv){let best=null;for(let f=-4;f<=4;f++)if(canLift(W*(f+5)/(5-f),Sv))best=f;return best==null?1:best+5;}
function levSol(sp){const tL=sp.items.filter(x=>x[0]<0).reduce((s,x)=>s+Math.abs(x[0])*(typeof x[1]==="number"?x[1]:LV_MASS[x[1]]),0)-0;const tRfix=sp.items.filter(x=>x[0]>0).reduce((s,x)=>s+x[0]*x[1],0);const need=tL-tRfix;
  const ps=sp.pieces;let out=null;(function f(i,acc,sum){if(out)return;if(i===ps.length){if(sum===need)out=acc.slice();return;}for(let p=1;p<=5;p++){acc.push([ps[i],p]);f(i+1,acc,sum+ps[i]*p);acc.pop();}})(0,[],0);
  return out?out.map(([m,p])=>`آجر ${fa(m)} کیلوگرمی روی خانهٔ ${fa(p)}`).join(" و "):"—";}
function levGenPredict(r,n){for(let k=0;k<200;k++){const items=[];const used=new Set();for(let i=0;i<n;i++){let p;do{p=ri(r,1,5)*(i%2?1:-1);}while(used.has(p));used.add(p);items.push([p,pick(r,[5,10,20])]);}
  const tL=items.filter(x=>x[0]<0).reduce((s,x)=>s-x[0]*x[1],0),tR=items.filter(x=>x[0]>0).reduce((s,x)=>s+x[0]*x[1],0);if(Math.abs(tL-tR)<=15||r()<.3)return{t:"predict",items};}return{t:"predict",items:[[-2,10],[4,5]]};}
function levGenBalance(r,np){for(let k=0;k<400;k++){const pieces=Array.from({length:Math.max(1,np-1)},()=>pick(r,[5,10,20]));const pos=pieces.map(()=>ri(r,1,5));const need=pieces.reduce((s,m,i)=>s+m*pos[i],0);
  const nl=ri(r,1,2),items=[];let rem=need,ok=true;const used=new Set();for(let i=0;i<nl;i++){if(i===nl-1){let f=false;for(const m of shuffle(r,[5,10,20]))for(let p=1;p<=5;p++)if(!f&&!used.has(p)&&m*p===rem){items.push([-p,m]);f=true;}if(!f)ok=false;}else{const m=pick(r,[5,10,20]),p=ri(r,1,5);if(m*p>=rem){ok=false;break;}used.add(p);items.push([-p,m]);rem-=m*p;}}
  if(ok&&items.length)return{t:"balance",items,pieces};}return{t:"balance",items:[[-2,10]],pieces:[5]};}
function levGenMystery(r){for(let k=0;k<300;k++){const my=pick(r,["myA","myB","myC"]),m=LV_MASS[my],p=ri(r,1,5),T=m*p;const items=[[-p,my]];let rem=T;const used=new Set();let ok=true;for(let i=0;i<2&&rem>0;i++){let f=false;for(const w of shuffle(r,[20,10,5]))for(const q of shuffle(r,[1,2,3,4,5]))if(!f&&!used.has(q)&&w*q<=rem&&(i===1?w*q===rem:true)){items.push([q,w]);used.add(q);rem-=w*q;f=true;}if(!f){ok=false;break;}}
  if(ok&&rem===0)return{t:"mystery",items};}return{t:"mystery",items:[[-2,"myA"],[4,10]]};}
