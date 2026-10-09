import sys; sys.path.insert(0,'.')
from pal4 import PAL
head='''/* ==========================================================================
   tokens.css (kit4) — متغیرهای نهایی نقشه: جداسازی لایه‌ای + پالت زمین‌ها.
   از kit/kit.css بالاتر بارگذاری شود (آن‌ها را نگه می‌دارد و فقط اضافه/بازنویسی می‌کند).
   پالت زمین‌ها از tools/pal4.py ساخته شده است (tools/gen_tokens.py)؛ دستی ویرایش نکن.
   ========================================================================== */
:root{
  /* --- مسیر: روبان با ۵ لایه (سایه، هالهٔ روشن، لبهٔ تیره، پر، برق) --- */
  --pt-shadow:rgba(18,10,4,.34);
  --pt-halo:#fff7e0;            /* حلقهٔ روشن بیرونی: روی زمین تیره دیده می‌شود */
  --pt-edge:#2b190a;            /* لبهٔ تیره: روی زمین روشن دیده می‌شود */
  --pt-done:#f5c04a;            /* طی‌شده: طلایی پر */
  --pt-done-hi:#fff3c4;
  --pt-todo:#fff3d6;            /* مانده: سنگ‌های کرم (شکل متفاوت، نه فقط رنگ) */
  --pt-dot:#fffaf0;
  --pt-w-halo:26px; --pt-w-edge:20px; --pt-w-fill:13.5px; --pt-w-shadow:22px;
  --pt-t-halo:24px; --pt-t-edge:18.5px; --pt-t-fill:12px;   /* مانده: باریک‌تر، سنگ‌ریزه‌های کپسولی */
  --pt-stones:8 24;           /* dasharray کپسول‌ها (طول ۸ + کپ گرد)، دورهٔ ۳۲ */
  /* --- گره --- */
  --node:100px;                 /* جعبهٔ SVG ؛ قطر قرص زیرین ≈ ۹۶px؛ هدف لمس بسیار بزرگ‌تر از ۴۸ */
  --node-glyph:36%;
  /* --- دروازه و تابلوی شروع/پایان --- */
  --portal:56px;
  --land-gap:84px;              /* فاصلهٔ بین قاب‌ها = جادهٔ کاغذی + دو دروازه */
  --lane:.156;                  /* خط مسیر در لبه‌ها: ۱۵٫۶٪ عرض قاب (از چپ) */
  --xl:.36; --xr:.64;           /* ستون گره‌ها */
  /* --- کاغذ نقشه (بیرون قاب‌ها) --- */
  --paper-hi:#f9ebc3; --paper-lo:#e8c982;
  /* --- منوی پایه --- */
  --grade-w:108px; --grade-h:88px;
  /* --- رنگ سختی: فقط برای نشان سختی (تکرار kit؛ در نقشه/زمین استفاده نشود) --- */
  --diff-easy:#2e9a52; --diff-mid:#e98a1f; --diff-hard:#c8352f;
}
'''
out=head
for k,v in PAL.items():
    out+=f'\n/* {v["title"]} */\n[data-land="{k}"]{{\n'
    for r,h,src,desc in v['roles']: out+=f'  --{r.replace("_","-")}:{h}; /* {desc} ({src}) */\n'
    out+='}\n'
open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','tokens.css'),'w',encoding='utf-8').write(out); print('tokens ok')
