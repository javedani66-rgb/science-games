# صحنهٔ بازی اسکله 390×500: دکل با دو قرقره، طناب، تور، دست، سکوی اسکله، دریا. قطعات متحرک گروه جدا با data-origin
from lib import *
from art import band
PAL = {
 'day':  dict(sky='#9fdcf2', sky2='#d6f1ee', sea='#2fa3c4', sea2='#1f87b8', conc='#c6c1b6', top='#fff4d2', steel='#2fb8a8', steel2='#1f8a7d', wheel='#3a2a7a', rope='#c98a45', cream='#fff4d2', skin='#c98a5e', sleeve='#2fb8a8', rim=None, shade=None, white='#ffffff', gold='#ffe9a8'),
 'dusk': dict(sky='#6a3fa0', sky2='#e0728a', sea='#3277a5', sea2='#2a5f8a', conc='#5b3490', top='#8a6fb0', steel='#3a2a7a', steel2='#2a1f5c', wheel='#8a4fd0', rope='#c98a45', cream='#fff4d2', skin='#c98a5e', sleeve='#2f7bd6', rim='#f2a65a', shade='#5b3490', white='#ffffff', gold='#ffe9a8'),
 'night':dict(sky='#1c1460', sky2='#2a1f7a', sea='#245090', sea2='#1a3a70', conc='#3a2a7a', top='#6f78c8', steel='#6f78c8', steel2='#3a2a7a', wheel='#8a4fd0', rope='#c98a45', cream='#d8e6ff', skin='#c98a5e', sleeve='#2fb8a8', rim='#d8e6ff', shade='#190539', white='#ffffff', gold='#ffd86b'),
}
def wheel(p, cx, cy, c, seed):
    s = S(el(cx, cy, 26, 26, 20), c['wheel'], 4.5, seed)
    s += S(el(cx, cy, 15, 15, 14), c['cream'], 2.6)
    for a in range(0, 360, 60):
        s += L([(cx, cy), (cx + 15 * math.cos(math.radians(a)), cy + 15 * math.sin(math.radians(a)))], LINE, 2.6)
    s += S(el(cx, cy, 5, 5, 8), c['steel'], 2.6)
    return s
def net_content(kind, c):
    s = ''
    if kind == 'chest':
        s += S(rr(92, 352, 34, 22, 3), '#c98a45', 2.6) + S([(92, 352), (96, 344), (122, 344), (126, 352)], '#8a5a2a', 2.6) + S(rr(104, 358, 10, 8, 2), c['gold'], 2.6)
        s += S(el(86, 372, 6, 5, 8), c['gold'], 2.6) + S(el(130, 372, 6, 5, 8), c['gold'], 2.6)
    else:
        for (x, y, r) in ((92, 360, 1), (112, 352, -1), (108, 372, 1)):
            s += S(el(x, y, 11, 6, 10), '#d6f1ee', 2.6) + S([(x - 11 * r, y), (x - 19 * r, y - 6), (x - 19 * r, y + 6)], '#d6f1ee', 2.6)
            s += f'<circle cx="{x + 5 * r}" cy="{y - 1}" r="1.5" fill="{LINE}"/>'
    return s
def net(p, c, kind):
    mesh = ''
    for x in range(76, 140, 9): mesh += L([(x, 340), (x - 4 + (x - 104) * .3, 394)], LINE, 1.2, .55)
    for y in range(348, 392, 9): mesh += L([(72, y), (136, y)], LINE, 1.2, .55)
    bag = [(78, 340), (130, 340), (136, 366), (106, 394), (72, 366)]
    s = f'<clipPath id="{p}-netclip"><path d="{pd(bag)}"/></clipPath>'
    s += S(bag, '#e9d9b0', 4.5, 61)
    s += f'<g clip-path="url(#{p}-netclip)">{net_content(kind, c)}{mesh}</g>'
    s += S(bag, 'none', 4.5, 61)
    s += L([(104, 324), (78, 340)], c['rope'], 2.6) + L([(104, 324), (130, 340)], c['rope'], 2.6) + L([(104, 324), (104, 340)], c['rope'], 2.6)
    s += S(el(104, 320, 6, 6, 10), c['steel'], 2.6)
    return s
def bgfar(p, c, bg):
    s = ''
    if bg == 'lighthouse':
        s += S([(10, 312), (30, 288), (64, 284), (92, 306), (96, 312)], c['conc'], 2.6)
        s += S([(40, 288), (46, 236), (60, 236), (66, 288)], c['cream'], 2.6) + S([(40, 244), (66, 244), (64, 254), (42, 254)], '#1f6f78', 2.6)
        s += S([(42, 238), (53, 224), (64, 238)], '#1f6f78', 2.6) + S(rr(46, 224, 14, 12, 2), c['gold'], 2.6)
    if bg == 'pirate':
        s += S([(130, 300), (270, 300), (254, 328), (146, 328)], '#1c1460', 4.5, 71)
        s += S([(176, 214), (182, 214), (182, 300), (176, 300)], '#3a2a7a', 2.6) + S([(222, 232), (228, 232), (228, 300), (222, 300)], '#3a2a7a', 2.6)
        s += S([(146, 222), (174, 216), (172, 292), (146, 298), (140, 258)], '#1c1460', 4.5, 72)
        s += S([(186, 232), (220, 228), (220, 292), (186, 296), (182, 262)], '#1c1460', 4.5, 73)
        s += S(el(203, 258, 9, 8, 12), '#fff', 2.6) + f'<circle cx="199" cy="257" r="2.4" fill="#1c1460"/><circle cx="207" cy="257" r="2.4" fill="#1c1460"/>'
        s += L([(190, 276), (216, 286)], '#fff', 2.6) + L([(216, 276), (190, 286)], '#fff', 2.6)
    return s
def bgdrag(p, c, bg):
    s = ''
    if bg == 'dragon':
        neck = bez((250, 470), (300, 400), (210, 360), (190, 330), 14)
        s += tube(neck, 34, '#8a4fd0', 4.5, 81)
        s += S([(204, 350), (170, 346), (130, 342), (140, 378), (176, 380), (206, 368)], '#c4262e', 2.6)
        s += S([(204, 314), (168, 322), (128, 326), (122, 338), (168, 344), (206, 346)], '#8a4fd0', 4.5, 82)
        s += S([(206, 354), (170, 362), (144, 376), (150, 388), (186, 382), (210, 370)], '#8a4fd0', 4.5, 83)
        for x in (136, 150, 164, 178):
            s += S([(x, 342), (x + 6, 342), (x + 3, 352)], '#fff', 1.2, stroke=LINE) if False else f'<path d="M{x} 343L{x + 6} 343L{x + 3} 352Z" fill="#fff" stroke="{LINE}" stroke-width="1.2" stroke-linejoin="round"/>'
        for x in (158, 172):
            s += f'<path d="M{x} 366L{x + 6} 366L{x + 3} 358Z" fill="#fff" stroke="{LINE}" stroke-width="1.2" stroke-linejoin="round"/>'
        s += S([(196, 314), (206, 288), (218, 318)], '#3a2a7a', 2.6) + S([(210, 322), (230, 300), (232, 330)], '#3a2a7a', 2.6)
        s += S(el(184, 326, 6, 5, 10), '#ffd86b', 2.6) + f'<circle cx="182" cy="326" r="2.2" fill="{LINE}"/>'
        s += S([(210, 430), (240, 416), (276, 420), (296, 440), (300, 470), (230, 470)], '#c4262e', 4.5, 84)
        s += S(el(238, 414, 10, 7, 8), '#fff', 2.6)
    return s
def build(p, tone, bg, load, story_rim=False):
    c = PAL[tone]; seed0 = 100
    sky = f'<rect width="390" height="316" fill="{c["sky"]}"/>'
    if tone == 'day':
        sky += f'<rect y="260" width="390" height="56" fill="{c["sky2"]}"/>'
        for x, y, rx, ry in ((60, 120, 36, 10), (88, 112, 22, 12), (330, 220, 38, 9), (180, 190, 26, 8)):
            sky += f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{c["white"]}"/>'
    elif tone == 'dusk':
        sky += band(262, 316, c['sky2'], 61, 390) + band(290, 316, '#f2a65a', 62, 390, 2) + f'<circle cx="340" cy="40" r="16" fill="#ffe9a8"/><circle cx="347" cy="35" r="13" fill="{c["sky"]}"/>'
        for x, y in ((30, 40), (120, 20), (200, 60), (300, 100), (60, 150)): sky += f'<circle cx="{x}" cy="{y}" r="1.7" fill="#fff"/>'
    else:
        sky += band(200, 316, c['sky2'], 63, 390, 3, 24) + f'<circle cx="60" cy="50" r="22" fill="#d8e6ff"/><circle cx="68" cy="44" r="19" fill="{c["sky"]}"/>'
        for x, y in ((30, 100), (120, 30), (200, 70), (310, 44), (350, 120), (250, 140)): sky += f'<circle cx="{x}" cy="{y}" r="1.7" fill="#fff"/>'
    far = bgfar(p, c, bg)
    sea = f'<rect y="310" width="390" height="190" fill="{c["sea"]}"/>'
    for x, y, w in ((10, 330, 60), (170, 344, 80), (20, 420, 70), (150, 450, 90), (300, 340, 60)):
        sea += L([(x, y), (x + w * .3, y - 2), (x + w * .6, y + 1), (x + w, y - 1)], c['sea2'], 1.2)
    if tone != 'day':
        for y, w in ((322, 24), (336, 36), (354, 22)):
            sea += f'<rect x="{60 - w // 2 if tone == "night" else 340 - w // 2}" y="{y}" width="{w}" height="3" rx="1.5" fill="{c["gold"]}"/>'
    # سکو
    plat = ''
    for x in (262, 358):
        plat += S(rr(x - 7, 162, 14, 250, 3), c['steel'], 4.5, seed0 + x)
    plat += L([(268, 176), (352, 256)], LINE, 2.6) + L([(352, 176), (268, 256)], LINE, 2.6) + L([(268, 256), (352, 256)], LINE, 2.6) + L([(268, 340), (352, 340)], LINE, 2.6)
    plat += S(rr(226, 404, 164, 100), c['conc'], 4.5, 111) + S(rr(226, 404, 164, 18), c['top'], 2.6)
    for x in range(240, 390, 36): plat += L([(x, 424), (x - 4, 498)], LINE, 1.2, .35)
    plat += S(rr(232, 144, 158, 20), c['steel'], 4.5, 112) + S(rr(232, 144, 158, 8), c['steel2'], 2.6)
    plat += L([(238, 160), (390, 160)], LINE, 1.2, .4)
    for x in (330, 360, 388):
        plat += L([(x, 144), (x, 108)], LINE, 2.6)
    plat += S([(330, 108), (390, 108), (390, 114), (330, 114)], c['steel2'], 2.6)
    # دست
    hand = S(rr(252, 116, 50, 26, 6), c['sleeve'], 4.5, 121) + S(el(248, 130, 14, 13, 12), c['skin'], 4.5, 122) + L([(236, 125), (250, 125)], LINE, 2.6) + L([(236, 132), (250, 132)], LINE, 2.6) + S(rr(292, 114, 10, 30, 3), c['cream'], 2.6)
    # دکل
    gantry = ''
    gantry += S(rr(296, 34, 16, 112, 3), c['steel'], 4.5, 131)
    gantry += S([(296, 100), (296, 70), (262, 48), (262, 56)], c['steel'], 2.6)
    gantry += S(rr(96, 32, 216, 16, 3), c['steel'], 4.5, 132)
    gantry += L([(130, 48), (130, 76)], LINE, 2.6) + L([(222, 48), (222, 76)], LINE, 2.6)
    w1 = wheel(p, 130, 76, c, 133); w2 = wheel(p, 222, 76, c, 134)
    rope = tube([(104, 324), (104, 80)], 5, c['rope'], 2.6, 0, jit=False)
    rope += tube(bez((104, 80), (104, 40), (130, 44), (130, 48), 6) + [(222, 48)] + bez((222, 48), (246, 48), (248, 66), (248, 84), 6) + [(248, 134)], 5, c['rope'], 2.6, 0, jit=False)
    # فلش‌ها (class farr؛ بدون متن)
    arr = ''
    arr += S([(226, 108), (232, 108), (232, 124), (238, 124), (229, 140), (220, 124), (226, 124)], '#2fb8a8', 2.6, extra='class="farr"')
    arr += S([(42, 340), (50, 340), (50, 366), (58, 366), (46, 390), (34, 366), (42, 366)], '#d070c0', 2.6, extra='class="farr"')
    # نور غروب: فقط گرمای لبه + سایهٔ بنفش (بدون multiply)
    lights = ''
    if c['rim']:
        rm = c['rim']
        lights += L([(298, 36), (298, 144)], rm, 2.6) + L([(98, 34), (310, 34)], rm, 2.6) + L([(234, 146), (390, 146)], rm, 2.6) + L([(258, 164), (258, 410)], rm, 2.6) + L([(354, 164), (354, 410)], rm, 2.6)
        lights += L([(105, 60), (110, 52)], rm, 2.6) if False else ''
        lights += f'<path d="M{104} 76 a26 26 0 0 1 22 -24" fill="none" stroke="{rm}" stroke-width="2.6" stroke-linecap="round"/>' + f'<path d="M{196} 76 a26 26 0 0 1 22 -24" fill="none" stroke="{rm}" stroke-width="2.6" stroke-linecap="round"/>'
        lights += L([(228, 405), (390, 405)], rm, 2.6) + L([(76, 342), (104, 330)], rm, 2.6)
        sh = c['shade']
        # سایهٔ بنفش: باند افقیِ پایین هر بنا، با clip به همان سیلوئت (بنا، نه روی هوا)؛ بدون چندضلعی مورب
        sil = (f'<clipPath id="{p}-shclip"><rect x="226" y="404" width="164" height="100"/><rect x="255" y="162" width="14" height="250"/><rect x="351" y="162" width="14" height="250"/>'
               f'<rect x="232" y="144" width="158" height="20"/><rect x="296" y="34" width="16" height="112"/><rect x="96" y="32" width="216" height="16"/></clipPath>')
        bands = (f'<rect x="226" y="470" width="164" height="34" fill="{sh}" opacity=".4"/><rect x="226" y="404" width="164" height="6" fill="{sh}" opacity=".3"/>'
                 f'<rect x="250" y="360" width="120" height="52" fill="{sh}" opacity=".35"/><rect x="232" y="156" width="158" height="8" fill="{sh}" opacity=".4"/>'
                 f'<rect x="296" y="124" width="16" height="22" fill="{sh}" opacity=".4"/><rect x="96" y="42" width="216" height="6" fill="{sh}" opacity=".4"/>')
        lights += sil + f'<g clip-path="url(#{p}-shclip)">{bands}</g>'
    global LAST
    LAST = dict(gantry=gantry, w1=w1, w2=w2, net=net(p, c, load), rope=rope, hand=hand)
    body = (g(f'{p}-sky', sky) + g(f'{p}-far', far) + g(f'{p}-sea', sea) + g(f'{p}-mid', bgdrag(p, c, bg)) + g(f'{p}-pier', plat) + g(f'{p}-hand', hand)
            + g(f'{p}-gantry', gantry) + g(f'{p}-wheel1', w1, 'data-origin="130 76"') + g(f'{p}-wheel2', w2, 'data-origin="222 76"')
            + g(f'{p}-rope', rope, 'data-origin="104 80"') + g(f'{p}-net', net(p, c, load), 'data-origin="104 320"') + g(f'{p}-arrows', arr)
            + (g(f'{p}-rim', lights) if lights else ''))
    return body
SCENES = {  # نام: (tone, bg, load)
 'harbor_scene_green': ('day', 'lighthouse', 'fish'),
 'harbor_scene_orange': ('day', 'pirate', 'chest'),
 'harbor_scene_orange_dusk': ('dusk', 'pirate', 'chest'),
 'harbor_scene_red': ('day', 'dragon', 'fish'),
 'harbor_scene_red_night': ('night', 'dragon', 'fish'),
}

LAST = {}
