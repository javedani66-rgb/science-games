# پرامپت‌های لایه‌های صحنهٔ مخفی‌گاه (برای Gemini / نانوبنانا)

**هدف:** تصویر `design/characters/gemini-20261015/monster/hideout-scene-v2.jpg` را برای حرکت لایه‌لایه کنیم، بدون عوض‌شدن سبک (مالک، ۲۱ اکتبر: صحنه همین سبک بماند).
**نکتهٔ فنی:** Gemini شفافیت (آلفا) نمی‌دهد. پس هر لایه روی **زمینهٔ تخت ماژنتا `#FF00FF`** ساخته می‌شود و Claude با حذف رنگ آن را شفاف می‌کند. در هر پرامپت تصویر `hideout-scene-v2.jpg` را پیوست کنید. اگر لایه‌ای چند ثانیه جابه‌جا یا کمی تغییر اندازه آمد، Claude با تطبیق روی صحنهٔ اصلی تنظیم می‌کند؛ مهم این است که اشیا از نظر طرح و رنگ تغییر نکنند.
**ترتیب پیشنهادی:** ۱ (زمینه) ← ۲ (قایق) ← ۳ (چرخ‌دنده‌ها) ← ۴ (چراغ‌ها) ← ۵ (هیولا، فقط اگر لازم شد؛ بریدهٔ آماده `inventor-full.png` هست).

## مشترک (اول هر پرامپت)
```
Use the attached image as the exact reference. Keep the same hand-drawn cartoon style, same thick dark outlines, same colors, same lighting, same camera angle, same image size and aspect ratio (2576x1438). Do not redraw, restyle or move anything that I do not ask to change. No text, no watermark.
```

## ۱) زمینهٔ خالی (بدون قایق و بدون چرخ‌دنده‌های رنگی دستگاه راست)
```
[مشترک]
Task: output the same scene but REMOVE (a) the wooden rowboat with its oar at the bottom-left, and (b) the four colorful gears on the front panel of the big machine on the right. Fill where the boat was with calm water and the rocky shore/dock continuing naturally. Where the four gears were, draw four empty round recessed sockets (darker circles, same size) on the panel. Everything else stays pixel-identical: cave, wooden bridge ceiling, lanterns, bench with machines, shelves, pulley and hook, pipes, gauges, bollard post, floor.
```

## ۲) قایق + طناب (روی زمینهٔ ماژنتا)
```
[مشترک]
Task: output ONLY the wooden rowboat with its oar (and the short rope to the bollard if it is attached) from the bottom-left of the reference, at the SAME position and the SAME size as in the reference, on a perfectly flat solid magenta (#FF00FF) background. No water, no shadow, no ground, no glow, nothing else. Crisp outline edges, no magenta tint on the boat.
```

## ۳) چهار چرخ‌دندهٔ دستگاه (روی ماژنتا)
```
[مشترک]
Task: output ONLY the four colorful gears of the big machine on the right (teal-green, purple, pink-red, lime-green), each at the SAME position and SAME size as in the reference, on a perfectly flat solid magenta (#FF00FF) background. No panel, no pipes, no shadow, nothing else. Gears must not overlap more than they do in the reference. Crisp outlines.
```

## ۴) نور چراغ‌ها (برای سوسو)
```
[مشترک]
Task: output ONLY the three hanging lanterns (with their small chains) at the SAME positions and sizes as in the reference, on a perfectly flat solid magenta (#FF00FF) background, flames lit. No glow halo, no light spill, no shadow. Then, as a second image in the same style, the same three lanterns but with the flames slightly smaller and dimmer (for a flicker animation).
```

## ۵) (اگر لازم شد) میز کار و ماشین‌های ساده
```
[مشترک]
Task: output ONLY the wooden workbench with the machine models on it (lever, screw, wedge, ramp, glowing lamp ball) at the SAME position and SAME size as in the reference, on a perfectly flat solid magenta (#FF00FF) background. No wall, no blueprints, no shadow.
```

## بعد از ساخت
فایل‌ها را در `design/characters/gemini-20261015/monster/layers/` بگذارید (یا به Claude بدهید). Claude: ماژنتا را شفاف می‌کند، اندازه را با صحنه تطبیق می‌دهد، لایه‌ها را به `hideout-scene/index.html` می‌بندد و حرکت (قایق، چرخش چرخ‌دنده‌ها، سوسوی چراغ، موج) را می‌سازد. کیفیت نهایی لبه‌ها را باید مالک ببیند (B9: با کودک آزموده نشده).
