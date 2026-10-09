#!/usr/bin/env python3
"""report.py: از before.json و after.json جدول فارسی results_FA.md می‌سازد."""
import json,os,sys
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'..','tools'))
from palettes import ratio,PAL,FIG
H=os.path.dirname(__file__)
B=json.load(open(f'{H}/before.json'));A=json.load(open(f'{H}/after.json'))
names={'stadium':'ورزشگاه','space':'پایگاه فضایی','farm':'مزرعه و آسیاب','city':'شهر ماشین‌ها'}
def row(m):
    return f"{m['min']} | {m['p10']} | {m['med']} | {round(m['ok3']*100)}٪"
out=['# نتایج اندازه‌گیری کنتراست (نسبت روشنایی WCAG، شکل در برابر زمینهٔ واقعی)','',
 'روش: `measure/measure.py` در Chromium از هر صفحه ۴ عکس می‌گیرد (همه‌چیز / فقط زمینه / زمینه+مسیر / زمینه+گره‌ها) و در همان نقطه‌ها روشنایی «شکل» را با زمینهٔ زیرش می‌سنجد؛ نسبت = (روشن‌تر+۰٫۰۵)/(تیره‌تر+۰٫۰۵). حد: ۳:۱ (WCAG 1.4.11 برای اجزای گرافیکی).',
 '«پیش» = کیت کامیت‌شدهٔ قبلی (HEAD) با همان هندسهٔ نقطه‌ها؛ «پس» = این بازنگری. هر دو با همان اسکریپت و همان ۳۹۰×۸۰۰.','',
 'ستون‌ها: کمینه | صدک ۱۰ (۹۰٪ نقطه‌ها بهتر از این) | میانه | سهم نقطه‌های ≥۳:۱.','']
def table(title,key,note=''):
    out.append(f'## {title}'); 
    if note: out.append(note)
    out.extend(['','| زمین | پیش: کمینه | صدک۱۰ | میانه | ≥۳ | پس: کمینه | صدک۱۰ | میانه | ≥۳ |','|---|---|---|---|---|---|---|---|---|'])
    for k,n in names.items():
        b=B['b-'+k][key];a=A['m-'+k][key]
        out.append(f"| {n} | {row(b).replace(' | ',' | ')} | {row(a)} |")
    out.append('')
table('مسیر (بهترین مرز: رنگ روشن یا دورگیر تیره، هر کدام مرز بهتری بدهد)','path_best_vs_bg','نقطه‌های زیر گره‌ها و پرچم‌ها و مانع کنار گذاشته شده؛ فقط «هستهٔ» هر خط‌چین سنجیده شده.')
table('مسیر (فقط رنگ روشن، سخت‌گیرانه‌ترین حالت)','path_lightfill_only_vs_bg')
table('لبهٔ گره (بهترین حلقه: حلقهٔ بیرونی روشن یا نوار تأکید)','node_silhouette_vs_bg','۲۴ نقطه دور هر گره؛ نشان‌های گوشه (پرچمک/ستاره/فلاسک) کنار گذاشته شد.')
out.append('## برچسب‌ها (چسبک‌ها)\n')
out+=['بهترین مرز هر چسبک = بیشینهٔ (پر شدن، لبهٔ طلایی، حلقهٔ کرم دور چسبک تیره). چسبک‌های روشن با پر شدنشان، «تو اینجایی» با حلقهٔ کرم.','','| زمین | پیش: میانه | پس: کمینه | پس: صدک۱۰ | پس: میانه | پس: ≥۳ |','|---|---|---|---|---|---|']
for k,n in names.items():
    bb=B['b-'+k]['chip_fill_vs_bg'];a=A['m-'+k]['chip_best_vs_bg']
    out.append(f"| {n} | {bb['med']} | {a['min']} | {a['p10']} | {a['med']} | {round(a['ok3']*100)}٪ |")
out+=['','نسبت متن به چسبک (از توکن‌ها): جوهر `#184441` روی کرم `#fff0c9` = '+str(round(ratio('#184441','#fff0c9'),1))+':۱؛ کرم روی فیروزه‌ای تیره `#184441` = '+str(round(ratio('#fff0c9','#184441'),1))+':۱.','']
out.append('## روشنایی میانگین زمینهٔ داخل قاب (Y نسبی)\n')
out+=['| زمین | پیش | پس |','|---|---|---|']
for k,n in names.items(): out.append(f"| {n} | {B['b-'+k]['bg_Y_mean_inland']} | {A['m-'+k]['bg_Y_mean_inland']} |")
out+=['','## یادداشت‌های صادقانه','- «پیش» برای مسیر دورگیرِ جداگانه نداشت؛ ستون «فقط دورگیر» در json برای پیش معنی ندارد.','- اعداد از چهار صفحهٔ نمونه‌اند، نه همهٔ ترکیب‌های ممکن (تعداد گره‌ها، حالت‌ها).','- نقطه‌های کم‌کنتراست باقی‌مانده: `_low_ink_points` و `_low_node_points` در `after.json`.','- این اندازه‌گیری روشنایی است؛ ادعای «کودک می‌خواند/دوست دارد» نیست (B9: فقط از مشاهدهٔ واقعی).']
open(f'{H}/results_FA.md','w').write('\n'.join(out)); print('\n'.join(out))

# ورق خاکستری (آزمون خاکستری): ۴ صفحه کنار هم
from PIL import Image
def sheet(tag,ids,outp):
    ims=[Image.open(f'{H}/gray/gray_{tag}_{i}.png') for i in ids]
    S=Image.new('L',(sum(i.width for i in ims)+6*(len(ims)-1),max(i.height for i in ims)),40);x=0
    for im in ims: S.paste(im,(x,0)); x+=im.width+6
    S.save(outp)
sheet('after',['m-stadium','m-space','m-farm','m-city'],f'{H}/gray_after_sheet.png'); sheet('before',['b-stadium','b-space','b-farm','b-city'],f'{H}/gray_before_sheet.png')
