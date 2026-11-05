# ابزار مشترک تولید صفحه‌های آزمون سبک (نوشتهٔ فقط در همین پوشه)
import base64, os
HERE = os.path.dirname(os.path.abspath(__file__))
STYLE = os.path.dirname(HERE)
FONTS = os.path.abspath(os.path.join(STYLE, '../../../../../../assets/fonts'))

def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()

def font_css():
    f = lambda n: b64(os.path.join(FONTS, n))
    return (
      "@font-face{font-family:Lalezar;src:url(data:font/woff2;base64,%s) format('woff2')}"
      "@font-face{font-family:Vazirmatn;font-weight:400;src:url(data:font/woff2;base64,%s) format('woff2')}"
      "@font-face{font-family:Vazirmatn;font-weight:700;src:url(data:font/woff2;base64,%s) format('woff2')}"
    ) % (f('Lalezar-Regular.woff2'), f('Vazirmatn-Regular.woff2'), f('Vazirmatn-Bold.woff2'))

def img_uri(name, mime):
    return 'data:%s;base64,%s' % (mime, b64(os.path.join(STYLE, name)))

# جاگذارها: همهٔ متن‌های فارسی اینجا فقط «جاگذار» اند (class ph)، نه متن نهایی
PH_JS = """
const PH={start:'شروع',here:'اینجایی',menu:'منو',grade:'پایه',d1:'۱',d2:'۲',d3:'۳',d4:'۴',d5:'۵',d6:'۶',lbl:'نام مرحله',z1:'ورزشگاه',z2:'پایگاه فضایی',z3:'مزرعه و آسیاب',z4:'شهر صنعتی',
 title:'عنوان درس',body:'متن کوتاه توضیح درس این‌جا می‌آید',practice:'تمرین',video:'فیلم',box:'بذارش توی جعبه',
 front:'روی کارت',back:'پشت کارت',seen:'دیده',kept:'جمع‌شده',empty:'خالی',locked:'قفل',
 f1:'غروب',f2:'شب',shelf:'جعبهٔ کارت',day:'روز'};
document.querySelectorAll('.ph').forEach(e=>{const k=e.getAttribute('data-ph');if(PH[k])e.textContent=PH[k]});
"""

def page(title, css, body, js='', w=390, h=800):
    return ("<!doctype html><html lang=fa dir=rtl><head><meta charset=utf-8>"
      "<meta name=viewport content='width=%d'><title>%s</title><style>%s%s</style></head><body>%s<script>%s%s</script></body></html>"
      % (w, title, font_css(), css, body, PH_JS, js))

# رنگ‌های «یک دست»
OUT = '#241a5e'   # خط دور آبی-بنفش تیره
