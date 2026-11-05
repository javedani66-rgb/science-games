import sys, json
sys.path.insert(0,'.')
from mz import *
V3='file:///home/claude/science-games/design/mockups/20261008/flow-demo/v3/index.html'
SETUP="__st.tutOn=false;__st.tutDone.map=true;__st.tut=null;renderOv();document.body.classList.add('rm');document.getElementById('rvbar').style.display='none';render()"
HIDE=".land__path,.foot,.node,.fogsign,.fog-patch,#gapsvg,#fx,.land__head,.flagc,.me-btn,.fog{visibility:hidden!important}"
SHOW={'done':".land__path .path-done,.land__path .path-done--top,.foot{visibility:visible!important}",
      'todo':".land__path .path-todo,.land__path .path-todo--shade{visibility:visible!important}",
      'nodes':".node__disc{visibility:visible!important}"}
P=Page(V3,SETUP)
res={}
for key in ('stadium','space','farm','city'):
    # scroll land top to y=60
    P.pg.evaluate("""k=>{const l=document.querySelector('.land[data-land='+k+']');const b=document.querySelector('#mapbody');b.style.scrollBehavior='auto';const r=l.getBoundingClientRect(),br=b.getBoundingClientRect();b.scrollTop+=r.top-br.top-8;}""",key)
    P.pg.wait_for_timeout(250)
    info=P.pg.evaluate("""k=>{const l=document.querySelector('.land[data-land='+k+']');const r=l.getBoundingClientRect();
      const nd=[...l.querySelectorAll('.node')].map(n=>{const d=n.querySelector('.node__disc').getBoundingClientRect();return{id:n.dataset.n,st:n.dataset.state,cx:d.left+d.width/2,cy:d.top+d.height/2,w:d.width}});
      return {l:[r.left,r.top,r.right,r.bottom],nodes:nd}}""",key)
    L=info['l'];H=int(1000);Wd=390
    roi=np.zeros((H,Wd),bool); roi[int(max(L[1],0))+6:int(min(L[3],H))-6, int(L[0])+8:int(L[2])-8]=True
    P.css(HIDE); bare=P.shot()
    out={}
    for g in ('done','todo'):
        P.css(HIDE+SHOW[g]); gimg=P.shot()
        mask=(np.abs(gimg-bare).sum(2)>24)&roi
        if mask.sum()<60: continue
        # full render equals group-only for fill/edge colours
        if g=='done': out['path_done']=ring_stats(bare,gimg,mask,roi)
        else:
            d_out=ndi.distance_transform_edt(~mask); ring=(d_out>2)&(d_out<=10)&roi
            Lf=float(np.median(lum(gimg[mask]))); Lbg=lum(bare[ring]); c=cr(Lbg,Lf)
            out['path_todo']=dict(Lfill=round(Lf,3),Lbg_med=round(float(np.median(Lbg)),3),pct_fill3=round(100*float((c>=3).mean()),1),pct_edge3=0,pct_any3=round(100*float((c>=3).mean()),1),best_p10=round(float(np.percentile(c,10)),2),Ledge=0,bg_std=0)
    # nodes: full render
    P.css(""); full=P.shot()
    ns=[]
    for n in info['nodes']:
        if n['cy']<L[1]+20 or n['cy']>min(L[3],H)-60: continue
        s=node_stats(bare,full,n['cx'],n['cy'],n['w']*0.432,roi,edge_w=1.8)
        if s: s['id']=n['id'];s['state']=n['st'];ns.append(s)
    out['nodes']=ns
    res[key]=out
P.close()
json.dump(res,open('old_measure.json','w'),ensure_ascii=False,indent=1)
for k,v in res.items():
    print('==',k)
    for g in ('path_done','path_todo'):
        if g in v and v[g]: print(g,{a:v[g][a] for a in ('Lfill','Ledge','Lbg_med','bg_std','pct_fill3','pct_edge3','pct_any3','best_p10')})
    for n in v['nodes']: print(' node',n['id'],n['state'],{a:n[a] for a in ('Lfill','Ledge','Lbg_med','pct_fill3','pct_edge3','pct_any3','best_p10')})
