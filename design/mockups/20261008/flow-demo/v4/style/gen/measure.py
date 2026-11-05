import os, sys
from PIL import Image
import numpy as np
STY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def lin(c): c=c/255; return c/12.92 if c<=.03928 else ((c+.055)/1.055)**2.4
def L(rgb): r,g,b=rgb[:3]; return .2126*lin(r)+.7152*lin(g)+.0722*lin(b)
def cr(a,b):
    la,lb=L(a),L(b); hi,lo=max(la,lb),min(la,lb); return (hi+.05)/(lo+.05)
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
print('--- ثابت‌های رنگ (WCAG) ---')
OUT=hx('#241a5e'); CREAM=hx('#fff3c4')
Z=dict(sea='#0e8f9f',grass='#4a9a2c',ice='#6f80ee',space='#d0573a')
for k,v in Z.items():
    print('%-6s زمین %s | مسیر-طی‌شده(کرم) %.2f | خط‌دور مسیر %.2f | کرم-روی-خط‌دور %.2f'%(k,v,cr(CREAM,hx(v)),cr(OUT,hx(v)),cr(CREAM,OUT)))
# گره‌ها: روی نمونه‌برداری از عکس
im=Image.open(STY+'/shots/r4_map_y1000.png').convert('RGB'); a=np.array(im)
def px(x,y): return tuple(int(v) for v in a[y,x])
print('--- نمونهٔ پیکسلی نقشه (عکس r4) ---')
print('زمین چمن', px(60,420),'مسیر طی‌شده',px(60,455) ,'ورزشگاه سقف',px(110,300))
# میانگین نسبت: لبهٔ نقشه (مسیر خطدار) نسبت به دور
# آزمون خاکستری: ذخیره و سنجش
for n in ['y1000','y1700','y0','y500']:
    g=Image.open(STY+'/shots/r4_map_%s.png'%n).convert('L'); g.save(STY+'/shots/r4_gray_%s.png'%n)
# آزمون گره-روی-زمین: برای هر عکس سه ناحیه ی مشخص نیست؛ ازبیرون نمونه می‌گیریم
import re
def band_contrast(img,box_node,box_ground):
    n=np.array(img.crop(box_node)).reshape(-1,3).mean(0); g=np.array(img.crop(box_ground)).reshape(-1,3).mean(0); return cr(n,g)
im=Image.open(STY+'/shots/r4_map_y1700.png').convert('RGB')
print('اسکلهٔ چوبی (میانگین) به دریا: %.2f'%band_contrast(im,(200,230,320,265),(330,380,380,420)))
im=Image.open(STY+'/shots/r4_map_y0.png').convert('RGB')
print('اسلب فضا/پایگاه (میانگین) به زمین مریخ: %.2f'%band_contrast(im,(180,385,330,410),(20,420,90,470)))
print('موشک بدنه به زمین: %.2f'%band_contrast(im,(112,140,150,190),(230,60,330,120)))
im=Image.open(STY+'/shots/r4_map_y500.png').convert('RGB')
print('مسیر باقی‌مانده (دور) به زمین یخ: %.2f'%cr(OUT,hx(Z['ice'])))
# شب: متن
print('--- شب ---')
im=Image.open(STY+'/shots/r4_card-night_vfront.png').convert('RGB'); a=np.array(im)
reg=a[430:520,40:350].reshape(-1,3)
bg=np.median(reg,axis=0); lum=[L(p) for p in reg[::3]]; fg=reg[::3][int(np.argmax(lum))]
print('متن توضیحی جلوی کارت: متن',tuple(fg),'زمینه',tuple(int(v) for v in bg),'نسبت %.1f'%cr(fg,bg))
im=Image.open(STY+'/shots/r4_card-night_vshelf.png').convert('RGB'); a=np.array(im)
reg=a[270:305,60:150].reshape(-1,3); bg=np.median(reg,axis=0); fg=reg[int(np.argmax([L(p) for p in reg]))]
print('زیرنویس قفسه (دیده): نسبت %.1f'%cr(fg,bg))
reg=a[560:595,60:150].reshape(-1,3); bg=np.median(reg,axis=0); fg=reg[int(np.argmax([L(p) for p in reg]))]
print('زیرنویس قفسه (خالی): نسبت %.1f'%cr(fg,bg))
print('عنوان لاله‌زار سفید به زمینهٔ بنفش #190539: %.1f'%cr((255,255,255),hx('#190539')))
print('دکمه‌ها: تیره روی طلایی/فیروزه/صورتی: %.1f %.1f %.1f'%(cr(hx('#190539'),hx('#ffd23f')),cr(hx('#190539'),hx('#46f0d8')),cr(hx('#190539'),hx('#ff7be5'))))
