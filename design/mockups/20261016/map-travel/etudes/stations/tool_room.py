#!/usr/bin/env python3
"""ایستگاه M06 «اتاق ابزار» (سرزمین شهر، پالت city).
طرح قطعه‌به‌قطعه (واحد symbol، قاب قهرمان pen.xf = ۰٫۸):
 ۱) پایهٔ سنگی (بلوک کرم #efe3c4 / روشن #fff7e0 / تیره #cdbb90): x -92..32، y -12..8، زیر تخته.
 ۲) تختهٔ ابزار دیواری (چوب زرد-کهربایی #f3cf7a / #ffe9a8 / #d9a647): x -88..30، y -118..-8؛ نوار ریل بالا قهوه‌ای کم‌رنگ
    و یک ردیف سوراخ تخت در پایین (تختهٔ سوراخ‌دار).
 ۳) قیچی (ستون چپ cx=-67): دو بازوی فولادی #d4dce8 (روشن #f6f9fd، تیره #94a2b8) با پیچ مرکزی و دو حلقهٔ دستهٔ بنفش #8b5fd0
    (روشن #b898ec، تیره #5d3a9e). نیمهٔ راست = لایهٔ متحرک node_tool_room_scissors حول پیچ؛ نیمهٔ چپ ثابت.
 ۴) چکش میخ‌کش (ستون میانی cx=-29): دستهٔ بنفش، سر فولادی با سطح کوبه (راست) و چنگک خمیده (چپ).
 ۵) انبردست (ستون راست cx=9): دو فک ضخیم کند، پیچ، دو دستهٔ بنفش راست. بدون آچار.
 رنگ قهرمان: چوب زرد ≈۴۵°، فولاد خنثی، بنفش ≈۲۶۰°؛ سکوی شهر آبی-خاکستری ≈۲۱۰° (فاصلهٔ ≥۳۵°).
 ماشین‌های ساده را نام نمی‌برد؛ فقط سه ابزار."""
import sys, pathlib, json, math
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from station_kit import *
OUTD = pathlib.Path(__file__).resolve().parent / 'out'
SHOTS = '/tmp/claude-0/-home-claude/b8272ea8-e944-5634-98c3-e9535737ce2f/scratchpad/s24/tool_room'

S_B, S_L, S_D = '#efe3c4', '#fff7e0', '#cdbb90'      # پایهٔ سنگی
W_B, W_L, W_D = '#f3cf7a', '#ffe9a8', '#d9a647'      # تخته
F_B, F_L, F_D = '#d4dce8', '#f6f9fd', '#94a2b8'      # فولاد
H_B, H_L, H_D = '#8b5fd0', '#b898ec', '#5d3a9e'      # دستهٔ بنفش
HOLE = '#a8742a'
BX0, BX1, BY0, BY1 = -88, 30, -118, -8


def poly(p, pts, col):
    p.raw('<polygon points="%s" fill="%s"/>' % (' '.join('%.1f,%.1f' % q for q in p.X(pts)), col))


def rect(p, x0, y0, x1, y1, col): poly(p, [(x0, y0), (x1, y0), (x1, y1), (x0, y1)], col)


def disc(p, x, y, r, col):
    a, b = p.X((x, y)); p.raw('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (a, b, r * p.xf[0], col))


def part(p, pts, col, sw=INNER):
    p.shape(pts, col, sw, j=.12, step=6, clip=False)


def board(p):
    part(p, [(BX0, BY0), (BX1, BY0), (BX1, BY1), (BX0, BY1)], W_B, PART)
    rect(p, BX0 + 4, BY0 + 4, BX1 - 4, BY0 + 8, W_L)                       # نور بالا
    rect(p, BX1 - 9, BY0 + 8, BX1 - 3, BY1 - 3, W_D)                       # سایهٔ تیز راست
    for i in range(7): disc(p, -78 + i * 17, -20, 2.4, HOLE)               # ردیف سوراخ


def plinth(p):
    part(p, [(-92, -13), (32, -13), (32, 7), (-92, 7)], S_B, PART)
    rect(p, -87, -9, 26, -6, S_L)
    rect(p, 20, -6, 28, 3, S_D)
    rect(p, -88, 1, 26, 3.5, S_D)


def arm(p, f, tip_x, tip_y, hx, hy):
    """یک نیمهٔ قیچی در قاب f (مبدأ = پیچ): تیغه از پیچ تا نوک، دستهٔ بنفش با حلقه."""
    pass


def scissors(p, cx, py):
    """دو نیمه. نیمهٔ چپ (ثابت): تیغه تا بالا-چپ، حلقه پایین-راست. نیمهٔ راست (متحرک): آینه."""
    def half(sg, f):
        # محلی: مبدأ = پیچ؛ sg=-1 تیغه به چپ بالا
        blade = [(-sg * 1, -6), (sg * 7, -6), (sg * 11, -42), (sg * 6, -42), (-sg * 2, 4)]
        blade = [(sg * 6.5, 4), (-sg * 5, 4), (sg * 0.5, -44), (sg * 7, -40)]
        return blade
    return None
