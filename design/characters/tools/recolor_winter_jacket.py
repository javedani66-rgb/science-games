"""یکدست‌کردن رنگ کاپشن زمستانی تارا و رویا با بقیه (آبی‌سبز).
اجرا از ریشهٔ پروژه: python3 design/characters/tools/recolor_winter_jacket.py
ورودی: فایل *-gemini-original.jpg کنار هر تصویر؛ خروجی: همان نام بدون پسوند.
روش: ماسک رنگی (آبی مات) + ناحیهٔ بدنه + حذف تکه‌های کوچک (شال)، سپس رنگ و روشنایی به سمت آبی‌سبز.
نیازمند: numpy, pillow, matplotlib, scipy. تأیید مالک: ۱۵ اکتبر ۲۰۲۶ (B64/D73)."""
import numpy as np
from PIL import Image
import matplotlib.colors as mc
from scipy import ndimage as ndi
B = "design/characters/gemini-20261015/outfits/winter/"
CFG = {"tara": (1050, 1570), "roya": (1020, 1605)}  # بازهٔ عمودی بدنهٔ کاپشن (پیکسل)
for n, (y0, y1) in CFG.items():
    f = np.asarray(Image.open(B + n + "-gemini-original.jpg").convert("RGB")) / 255.0
    hsv = mc.rgb_to_hsv(f); H = hsv[..., 0] * 360; S = hsv[..., 1]; V = hsv[..., 2]
    m = (H >= 203) & (H < 228) & (V >= 0.34) & (V < 0.60) & (S > 0.25)
    m[:y0] = False; m[y1:] = False
    lab, k = ndi.label(m)
    area = ndi.sum(m, lab, range(1, k + 1))
    keep = np.isin(lab, [i + 1 for i, a in enumerate(area) if a > 6000])
    keep = ndi.binary_closing(keep, iterations=2)
    keep = ndi.binary_dilation(keep, iterations=2) & (H >= 190) & (H < 240) & (S > 0.2) & (V > 0.18) & (V < 0.75)
    keep[:y0] = False; keep[y1:] = False
    w = ndi.gaussian_filter(keep.astype(float), 1.0)[..., None]
    hh = hsv.copy()
    hh[..., 0] = np.where(keep, 195 / 360, hh[..., 0])
    hh[..., 1] = np.where(keep, np.clip(S * 1.3, 0, 1), S)
    hh[..., 2] = np.where(keep, np.clip(V * 1.32, 0, 1), V)
    out = mc.hsv_to_rgb(hh) * w + f * (1 - w)
    Image.fromarray((out * 255).astype(np.uint8)).save(B + n + ".jpg", quality=95)
    print(n, "ok")
