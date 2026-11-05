/* map4.js (kit4): هندسهٔ نقشه + مسیر + دروازه. بدون وابستگی. همهٔ متن‌ها از داده می‌آیند.
   Map4.build(root, data) → HTML + کشیدن مسیر. data.frames[i] = {skin, plate, sym, first, last, exitDone, nodes:[{id,env,state,here,sym,tags:[{cls,text,ic}]}]}
   state: done | open | locked | trial. «done» و «here» = رسیده. */
(function(g){
var K={Y0:140,Y0F:170,DY:148,TAIL:130,LANE:.156,XL:.36,XR:.64,BORDER:6,SIGN_Y:44};
function sc(x1,y1,x2,y2){var k=(y2-y1)*.55;return 'C'+x1+' '+(y1+k)+' '+x2+' '+(y2-k)+' '+x2+' '+y2}   // S با مماس عمودی در هر دو سر: بدون زاویه
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;')}
function frameH(f){return (f.first?K.Y0F:K.Y0)+(f.nodes.length-1)*K.DY+K.TAIL}
function layers(d,done){ // یک گروه مسیر (همهٔ قطعه‌های هم‌وضعیت)
  if(!d)return'';
  if(done)return '<g class="pt-done"><path class="pt pt-sh" d="'+d+'"/><path class="pt pt-halo" d="'+d+'"/><path class="pt pt-edge" d="'+d+'"/><path class="pt pt-fill pt-fill--done" d="'+d+'"/><path class="pt pt-shine" d="'+d+'"/><path class="pt pt-dots" d="'+d+'"/></g>';
  return '<g class="pt-todo"><path class="pt pt-sh" d="'+d+'"/><path class="pt pt-halo" d="'+d+'"/><path class="pt pt-edge" d="'+d+'"/><path class="pt pt-fill pt-fill--todo" d="'+d+'"/></g>';
}
function reach(n){return n.state==='done'||n.here}
function nodeHTML(n,side,o){
  var fog=!!n.fog, tags=fog?'':(n.tags||[]).map(function(t){return '<span class="chip chip--'+t.cls+'">'+(t.ic?'<i class="ic"></i>':'')+esc(t.text)+'</span>'}).join('');
  return '<button class="node'+(fog?' fogged':'')+'" data-act="node" data-id="'+n.id+'" data-n="'+n.id+'" data-state="'+(fog?'locked':n.state)+'" data-side="'+side+'"'+(n.here?' data-t="here"':'')+' aria-label="'+esc(fog?(n.fogLabel||n.env):n.env)+'">'
   +(n.here?'<i class="node__ring"></i>':'')+'<span class="node__disc"></span>'+(fog?'':'<i class="node__glyph" data-sym="'+n.sym+'"></i>')
   +(fog?'':'<span class="node__labels"><span class="chip chip--label">'+esc(n.env)+'</span>'+tags+'</span>')
   +(n.here&&o.guideInNode?'<i class="guide" data-state="thinking"></i>':'')+'</button>';
}
function frameHTML(f,i,S,o){
  var H=frameH(f);
  return '<section class="landwrap" data-fi="'+i+'" style="height:'+(H+2*K.BORDER)+'px"><div class="land" data-land="'+f.skin+'">'
   +'<div class="land__layer land__layer--back"></div><div class="land__layer land__layer--mid"></div><div class="land__layer land__layer--front"></div>'
   +'<div class="land__head"><div class="plate"><span>'+esc(f.plate)+'</span></div><i class="sym land__sym" data-sym="'+f.sym+'"></i></div>'
   +'<svg class="land__path" aria-hidden="true"></svg>'
   +(f.first?'<div class="chip chip--label sign sign--start"><i class="ic ic-flag"></i>'+esc(S.start)+'</div>':'')
   +f.nodes.map(function(n,j){return nodeHTML(n,j%2?'R':'L',o)}).join('')
   +(f.last?'<div class="chip chip--label sign sign--end"><i class="ic ic-flag"></i>'+esc(S.end)+'</div>':'')
   +'</div>'+(f.first?'':'<i class="portal portal--top"></i>')+(f.last?'':'<i class="portal portal--bot"></i>')+'</section>';
}
function layout(root,data){
  var map=root, wraps=[].slice.call(map.querySelectorAll('.landwrap')), gap='', gapT='', pos={};
  wraps.forEach(function(w,i){
    var f=data.frames[i], land=w.querySelector('.land'), W=land.clientWidth, H=frameH(f), lane=Math.round(K.LANE*W), xl=Math.round(K.XL*W), xr=Math.round(K.XR*W);
    land.style.setProperty('--fw',W+'px');
    var pts=[], y0=f.first?K.Y0F:K.Y0;
    pts.push({x:lane,y:f.first?K.SIGN_Y:0,r:f.first?reach(f.nodes[0]):reach(f.nodes[0])});
    f.nodes.forEach(function(n,j){var x=j%2?xr:xl,y=y0+j*K.DY;pts.push({x:x,y:y,r:reach(n)});
      var el=land.querySelectorAll('.node')[j];el.style.left=x+'px';el.style.top=y+'px';pos[n.id]={ax:w.offsetLeft+K.BORDER+x,ay:w.offsetTop+K.BORDER+y,side:j%2?'R':'L'};
      [].forEach.call(land.querySelectorAll('[data-fx="'+n.id+'"]'),function(e){e.remove()});
      if(n.fog)land.insertAdjacentHTML('beforeend','<i class="fog-patch" data-fx="'+n.id+'" data-fog style="left:'+(x-100)+'px;top:'+(y-58)+'px;width:200px;height:116px"></i>');
      if(n.fogSign)land.insertAdjacentHTML('beforeend','<i class="fogsign" data-fx="'+n.id+'" style="left:'+(x+(j%2?-88:52))+'px;top:'+(y-96)+'px"></i>')});
    pts.push({x:lane,y:f.last?H-K.SIGN_Y-14:H,r:!!f.exitDone});
    var dd='',dt='';
    for(var k=0;k<pts.length-1;k++){var a=pts[k],b=pts[k+1],d='M'+a.x+' '+a.y+sc(a.x,a.y,b.x,b.y);
      var done=(k===0)?b.r:(k===pts.length-2?b.r:(a.r&&b.r)); if(done)dd+=d;else dt+=d}
    land.querySelector('.land__path').setAttribute('viewBox','0 0 '+W+' '+H);
    land.querySelector('.land__path').innerHTML=layers(dt,false)+layers(dd,true);
    var sg=land.querySelector('.sign--start'),se=land.querySelector('.sign--end');
    [[sg,K.SIGN_Y],[se,H-K.SIGN_Y]].forEach(function(p){var e=p[0];if(!e)return;e.style.top=p[1]+'px';e.style.left=Math.max(lane,Math.ceil(e.offsetWidth/2)+10)+'px'});  // تابلو هرگز از قاب بیرون نمی‌زند؛ مسیر زیر آن می‌ماند
    [].forEach.call(w.querySelectorAll('.portal'),function(p){p.style.left=(K.BORDER+lane)+'px'});
    // جادهٔ کاغذی تا قاب بعدی (خط راست عمودی)
    if(!f.last){var nx=wraps[i+1],x=w.offsetLeft+K.BORDER+lane,y1=w.offsetTop+w.offsetHeight,y2=nx.offsetTop,d='M'+x+' '+y1+'L'+x+' '+y2;if(f.exitDone)gap+=d;else gapT+=d}
  });
  var gs=map.querySelector('#gap4');gs.setAttribute('width',map.scrollWidth);gs.setAttribute('height',map.scrollHeight);gs.setAttribute('viewBox','0 0 '+map.scrollWidth+' '+map.scrollHeight);
  gs.innerHTML=layers(gapT,false)+layers(gap,true);
  return pos;
}
// نقطهٔ پای راهنما وقتی بیرون از گره (در لایهٔ #fx) نشانده می‌شود: کنار قرص، سمتِ بی‌چسبک
function guideAt(p){return{x:p.ax+(p.side==='L'?-69:69),y:p.ay+42}}
g.Map4={K:K,guideAt:guideAt,html:function(data,S,o){return '<svg id="gap4" aria-hidden="true"></svg>'+data.frames.map(function(f,i){return frameHTML(f,i,S,o||{guideInNode:true})}).join('')},
  build:function(root,data,S,o){root.innerHTML=this.html(data,S,o);return layout(root,data)},layout:layout,frameH:frameH};
})(window);
