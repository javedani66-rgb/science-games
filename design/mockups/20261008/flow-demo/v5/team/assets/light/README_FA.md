# دارایی‌های light (فاز ۰ و ۳؛ پیشنهاد، آزموده‌نشده با کودک)
- `zone_tokens.json` منبع حقیقت hex (با `_corrections`)؛ `build_light.py` ← `tokens.css`، `common_defs.svg`، `palette_*.svg`؛ `build_demos.py` ← `light_layers_demo.html`، `transition_demo.html`.
- tokens.css: `[data-light=day|dusk|night]`، شدت rim/سایه (`--l-lit-a/-shade-a` برای شخصیت، `--l-nlit-a/-nshade-a` برای بنا؛ قاعدهٔ `[data-light] .elit/.esh` شدت بناهای env را به نور وصل می‌کند)، `.lt-layer[data-for]` برای انتقال، reduced-motion بدون انیمیشن. بدون blend و بدون filter زنده.
- `light_layers_demo.html`: ۱۲ بنا + ۴ شخصیت در سه نور، تیک خاموش‌کردن rim/shade/windows. `transition_demo.html`: روز←شب ۱٫۲ث فقط opacity (دو لایه هر دو در DOM، ماه بالا-چپ)، و غروب ثابت (rim گرم + سایهٔ بنفش در سیلوئت + رگهٔ بازتاب، بی‌خورشید-دایره، بی‌multiply).
- عکس‌ها در `shots/` (390×800، 360×640، خاکستری، mid-transition با opacity 0.52/0.48، reduced-motion).
- اندازه‌گیری: `measure/light_contrast.py` (جدول کنتراست/رنگ‌مایه/کوررنگی، ۰ قرمز)، `measure/light_render_check.py` (پیکسلی روی بناهای واقعی)، `measure/ui_char_check.py` (ui و شخصیت). اصلاح‌های پیشنهادی ui/character در `ui_char_corrections.json` (فایل‌های آن‌ها دست نخورده).
- حجم: demo ها به‌خاطر inline شدن SVG بیش از 50KB سقف پوشه‌اند (197KB و 20KB، هر دو ≤400KB صفحه)؛ بقیهٔ فایل‌ها ≈30KB.
