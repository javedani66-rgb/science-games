import sys; sys.path.insert(0,'.')
import buildings as X, pathlib, re
cells=[]
for n,f in X.LAND.items(): cells.append(f())
pads=[]
from shapes import *
def padsvg(z):
    b=B('pad_'+z); pad(b,z,38); return b.svg((120,100),60,78,38,12,(-38,-14,38,14))
for n,f in X.PROPS.items(): cells.append(X.prop(n,f))
html='<html><body style="margin:0;background:#cfe8c0;display:flex;flex-wrap:wrap;gap:6px">'
for i,c in enumerate(cells):
    z=['sports','space','farm','city'][i%4]
    html+='<div style="width:200px;height:180px;position:relative">'+c.replace('<svg ','<svg width="200" height="180" ')+'</div>'
open('/tmp/claude-0/-home-claude-science-games/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/prev.html','w').write(html)
