/* mappath.js: هندسهٔ مسیر نقشه (همان tools/mappath.py؛ برای ادغام در قالب v3).
   مختصات «داخلی» = داخل قاب زمین (پهنا ۳۴۶). ستون‌های ثابت: راست 248، چپ 98؛ شعاع گره 48.
   فقط قوس‌های ملایم: از مرکز گرهٔ بالا با مماس افقی بیرون می‌آید و از بالا (مماس عمودی) به گرهٔ بعدی می‌رسد.
   استفاده:  const p = MapPath.plan({nodes:[{x,y,st}], H:640, first:false, last:false});
     p.inland = [{d, done}]  → مسیرهای داخل قاب (به <svg class="land__path"> بده؛ done→ path-done + path-done--top، وگرنه path-todo--shade + path-todo)
     p.foot   = [{x,y,deg}]  → ردپاها روی بخش‌های طی‌شده (<i class="foot">)
     p.trailTop / p.trailBottom → true اگر روی لبهٔ قاب باید رشتهٔ بیرونی (svg.trail) بیاید؛ done را از p.entryDone / p.exitDone بخوان. */
(function(g){
  const COL_R=248, COL_L=98, NODE_R=48, K=.62, EXIT=30;
  const reached=s=>s==='done'||s==='open';
  function seg(a,b){
    if(Math.abs(a.x-b.x)<1) return `M${a.x} ${a.y}L${b.x} ${b.y}`;
    const f=v=>(Math.round(v*10)/10);
    return `M${a.x} ${a.y}C${f(a.x+K*(b.x-a.x))} ${a.y} ${b.x} ${f(b.y-K*(b.y-a.y))} ${b.x} ${b.y}`;
  }
  function bezPts(a,b,n=200){
    if(Math.abs(a.x-b.x)<1) return Array.from({length:n+1},(_,t)=>({x:a.x,y:a.y+(b.y-a.y)*t/n}));
    const p=[a,{x:a.x+K*(b.x-a.x),y:a.y},{x:b.x,y:b.y-K*(b.y-a.y)},b];const out=[];
    for(let i=0;i<=n;i++){const t=i/n,u=1-t;out.push({x:u*u*u*p[0].x+3*u*u*t*p[1].x+3*u*t*t*p[2].x+t*t*t*p[3].x,y:u*u*u*p[0].y+3*u*u*t*p[1].y+3*u*t*t*p[2].y+t*t*t*p[3].y})}
    return out;
  }
  function footprints(a,b,step=30,margin=34){
    const pts=bezPts(a,b),L=[0];for(let i=1;i<pts.length;i++)L.push(L[i-1]+Math.hypot(pts[i].x-pts[i-1].x,pts[i].y-pts[i-1].y));
    const res=[];let side=1,s=margin;
    while(s<L[L.length-1]-margin){
      let j=L.findIndex(v=>v>=s);const p=pts[j],q=pts[Math.min(j+1,pts.length-1)],an=Math.atan2(q.y-p.y,q.x-p.x);
      res.push({x:p.x+Math.cos(an+Math.PI/2)*3.4*side,y:p.y+Math.sin(an+Math.PI/2)*3.4*side,deg:an*180/Math.PI+90});
      s+=step;side=-side;
    }
    return res;
  }
  function plan(o){
    const N=o.nodes,H=o.H,inland=[],foot=[];
    const startY=o.first?112:EXIT;                      // پرچم شروع (داخل قاب) یا ۳۰px زیر دروازه
    inland.push({d:seg({x:COL_R,y:startY},N[0]),done:reached(N[0].st)&&(o.first||o.entryDone!==false)});
    for(let i=0;i<N.length-1;i++){
      const done=reached(N[i].st)&&reached(N[i+1].st);inland.push({d:seg(N[i],N[i+1]),done});
      if(done)footprints(N[i],N[i+1]).forEach(f=>foot.push(f));
    }
    const last=N[N.length-1];
    const end=o.last?{x:COL_R,y:596}:{x:COL_R,y:H-EXIT};   // پرچم پایان یا ۳۰px بالای دروازهٔ پایین
    inland.push({d:seg(last,end),done:reached(last.st)});
    return {inland,foot,trailTop:!o.first,trailBottom:!o.last,entryDone:o.entryDone,exitDone:reached(last.st)};
  }
  g.MapPath={COL_R,COL_L,NODE_R,K,seg,footprints,plan};
})(typeof window!=='undefined'?window:globalThis);
