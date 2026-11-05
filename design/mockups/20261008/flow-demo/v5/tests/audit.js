(()=>{
const out=[];const vis=e=>{const r=e.getBoundingClientRect(),cs=getComputedStyle(e);return r.width>0&&r.height>0&&cs.visibility!=='hidden'&&cs.display!=='none'&&+cs.opacity>0.05};
const VW=innerWidth,VH=innerHeight;
const clip=(e,r)=>{let l=r.left,t=r.top,ri=r.right,b=r.bottom;for(let p=e.parentElement;p&&p!==document.body;p=p.parentElement){const o=getComputedStyle(p);if(o.overflowX!=='visible'||o.overflowY!=='visible'){const q=p.getBoundingClientRect();l=Math.max(l,q.left);t=Math.max(t,q.top);ri=Math.min(ri,q.right);b=Math.min(b,q.bottom)}}return {left:l,top:t,right:ri,bottom:b,width:ri-l,height:b-t}};
const inView=r=>r.bottom>0&&r.top<VH&&r.right>0&&r.left<VW;
// نوشتهٔ کوچک‌تر از ۱۴px
const leaves=[];
document.querySelectorAll('body *').forEach(e=>{
  if(e.closest('svg')||e.closest('#rvbar,.rv,.cflip .cface:not(.bk)[style*="hidden"]'))return;
  if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;
  if(!vis(e))return;const r0=e.getBoundingClientRect(),r=clip(e,r0);if(r.width<=0||r.height<=0||!inView(r))return;
  {const t=document.elementFromPoint(Math.min(VW-1,Math.max(0,r.left+r.width/2)),Math.min(VH-1,Math.max(0,r.top+r.height/2)));if(!t||!(e.contains(t)||t.contains(e)))return;}
  const fs=parseFloat(getComputedStyle(e).fontSize);
  if(fs<14)out.push('متن<14px:'+fs+':'+e.textContent.trim().slice(0,18));
  leaves.push([e,r]);
  if(e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=='visible')out.push('بریدگی:'+e.textContent.trim().slice(0,18));
  if(r0.left<-1||r0.right>VW+1)out.push('بیرون‌زدگی:'+e.textContent.trim().slice(0,18));
});
// هم‌پوشانی متن با متن (بدون رابطهٔ پدر/فرزند)
for(let i=0;i<leaves.length;i++)for(let j=i+1;j<leaves.length;j++){
  const [a,ra]=leaves[i],[b,rb]=leaves[j];if(a.contains(b)||b.contains(a))continue;if(a.closest('.ui-chip')&&a.closest('.ui-chip')===b.closest('.ui-chip'))continue;
  const w=Math.min(ra.right,rb.right)-Math.max(ra.left,rb.left),h=Math.min(ra.bottom,rb.bottom)-Math.max(ra.top,rb.top);
  if(w>4&&h>4)out.push('هم‌پوشانی:'+a.textContent.trim().slice(0,12)+' × '+b.textContent.trim().slice(0,12));
}
// هدف لمسی <48
document.querySelectorAll('button,[data-act]').forEach(e=>{if(!vis(e))return;const r=e.getBoundingClientRect();if(!inView(r))return;
  if(e.classList.contains('mn'))return;
  if(r.width<48||r.height<48)out.push('لمس<48:'+Math.round(r.width)+'x'+Math.round(r.height)+':'+(e.textContent.trim().slice(0,12)||e.dataset.act));});
// برچسب‌های نقشه در برابر مسیر
const m=document.querySelector('#map');
if(m){const ps=[...m.querySelectorAll('#env_path path')].filter(x=>x.getTotalLength);const mr=m.getBoundingClientRect();
 m.querySelectorAll('.ml').forEach(el=>{const r=el.getBoundingClientRect();if(!inView(r))return;let bad=0;
  ps.forEach(p=>{const L=p.getTotalLength(),sp=p.getScreenCTM();for(let l=0;l<=L;l+=8){const q=p.getPointAtLength(l),z=new DOMPoint(q.x,q.y).matrixTransform(sp);
   if(z.x>r.left-8&&z.x<r.right+8&&z.y>r.top-8&&z.y<r.bottom+8)bad++}});
  if(bad)out.push('برچسب روی مسیر:'+el.textContent.trim().slice(0,14));});}
return [...new Set(out)];
})()
