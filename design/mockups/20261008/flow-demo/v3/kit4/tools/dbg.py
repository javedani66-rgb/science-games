import sys; sys.path.insert(0,'.')
from mz import *
from PIL import Image
exec(open('measure_new.py').read().split("P=Page")[0].split("TAG=")[0]) if False else None
V3K='file:///home/claude/science-games/design/mockups/20261008/flow-demo/v3/kit4/proof.html?v=stadium'
HIDE=".land__path,.node,.sign,.guide,.portal,.land__head,#gap4,.node__ring{visibility:hidden!important} #phone{height:1060px!important} .topbar{visibility:hidden}"
SH=".land__path .pt-done .pt{visibility:visible!important} .land__path .pt-done .pt-sh,.land__path .pt-done .pt-shine,.land__path .pt-done .pt-dots{visibility:hidden!important}"
P=Page(V3K,None,390,1060); P.css(HIDE+SH); img=P.shot(); Image.fromarray(img.astype('uint8')).crop((0,80,390,400)).resize((780,640)).save('/tmp/claude-0/-home-claude-science-games/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/dbg.png'); P.close()
