# پرامپت نانوبنانا برای قاب کارت هر سرزمین (D235)

تصمیم مالک (۱۴ نوامبر ۲۰۲۶): هر سرزمین قاب کارت مخصوص خودش را دارد. قاب سرزمین دریایی (طناب، لنگر، برنج) ساخته شده؛ این‌جا چهار قاب دیگر.

## هر بار ضمیمه کن
`design/cards/approved/harbor-v1/assets/card-frame-base.png` (قاب سبز دریایی). بنویس: «keep exactly the same layout, proportions and element positions as the reference».

## قواعد ثابت (برای ساخت سه رنگ با کد)
- بدنهٔ اصلی قاب **سبز** بماند (من نارنجی و قرمز را با چرخاندن سبز می‌سازم). هیچ جزء تزئینی دیگری سبز یا فیروزه‌ای نباشد.
- پس‌زمینهٔ بیرون سفید ساده؛ بدون سایهٔ روی زمین؛ بدون متن و حرف.
- پنجرهٔ بزرگ تصویر و جای عنوان بالا: رنگ سبز تیره، صاف و بدون طرح.
- پنل متن پایین و تابلوی نام بالا و تابلوی دکمهٔ پایین: کاغذ کرم خالی.
- مدالیون پایین (نشان سختی): دیسک خالی، من نشان را خودم می‌گذارم.
- مدالیون بالا: نشان همان سرزمین (در هر پرامپت آمده).

## بلوک سبک (اول هر پرامپت)
```
Hand-painted children's game UI card frame, thick dark navy outline, glossy storybook look, rich saturated colors, clean readable shapes, flat empty panels, white background, no text, no letters, no logo, no watermark, no scene inside the window. Keep exactly the same layout, proportions and element positions as the reference image (top badge with side ornaments and empty name plate, main frame with title bar, big picture window, cream text panel, bottom medallion, separate button plate under the card). Frame body stays GREEN; all decorative parts use the materials below and contain no green.
```

## ورزشگاه
```
[style block] Land theme: sports stadium. Replace the ropes and brass with stitched white leather ball panels, athletic tape wraps at the two top corners, chrome rivets, white painted lane-line stripes along the green frame edges, small orange traffic cones as end ornaments on the top badge wings. Top badge emblem on a dark blue disc: a classic football. Bottom medallion disc empty.
```

## پایگاه فضایی
```
[style block] Land theme: space base. Replace the ropes and brass with brushed steel panels, hex bolts, bundles of dark cables with glowing white-blue indicator lights, small satellite-dish and antenna ornaments on the top badge wings, porthole-style round badge. Top badge emblem on a deep blue disc: a small rocket with a star. Bottom medallion disc empty.
```

## مزرعه و آسیاب
```
[style block] Land theme: farm and windmill. Replace the ropes and brass with natural twine and golden wheat sheaves tied at the two top corners, warm wooden plank trim and wooden pegs along the green frame edges, tiny wooden windmill sails as ornaments on the top badge wings. Top badge emblem on a warm brown disc: a windmill. Bottom medallion disc empty.
```

## شهر صنعتی
```
[style block] Land theme: industrial city. Replace the ropes and brass with riveted iron plates, big brass gear halves at the two top corners, small pipe elbows and pressure-gauge ornaments on the top badge wings, yellow-and-black hazard stripe accents on the frame edges. Top badge emblem on a dark steel-blue disc: a gear with a wrench. Bottom medallion disc empty.
```

## بعد از تولید
تصویر هر قاب را بده. پس‌زمینه را شفاف می‌کنم، نارنجی و قرمز را از سبز می‌سازم (مثل قاب دریایی، `design/cards/tiers-v2/build_tiers.py`) و نشان سختی را روی مدالیون پایین می‌گذارم. قاب قرمز و نارنجی باید روشن بماند (D230).
