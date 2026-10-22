import os, sys, random
from lib3 import *
from exp3 import save
import final3 as F3

DEFS4 = DEFS.replace('</defs>', '''<filter id="rough4" x="-5%" y="-10%" width="110%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.016" numOctaves="2" seed="9" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="8" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="scrim"><feGaussianBlur stdDeviation="0"/></filter></defs>''')

ML, CW = 72, 1296

def canvas(s):
    rect(s, 0, 0, 1440, 900, P['paper']); grain(s, 0, 0, 1440, 900, 0, .05, .04)

def mark(s, x, y, r=6, op=.30):
    s.a(f'<g fill="none" stroke="{P["pur"]}" stroke-width="1" opacity="{op}"><circle cx="{x}" cy="{y}" r="{r}"/><path d="M{x} {y-r-6}V{y+r+6}M{x-r-6} {y}H{x+r+6}"/></g>')

def margin_marks(s, gold_tl=False, gold_br=False):
    # sparse marks that live only in the 72 px side margins and the corners
    for y in (116, 470, 836):
        if not (gold_tl and y == 116): mark(s, 30, y)
        if not (gold_br and y == 836): mark(s, 1410, y)
    s.a(f'<line x1="30" y1="128" x2="30" y2="458" stroke="{P["pur"]}" stroke-opacity=".12"/><line x1="30" y1="482" x2="30" y2="824" stroke="{P["pur"]}" stroke-opacity=".12"/>')
    s.a(f'<line x1="1410" y1="128" x2="1410" y2="458" stroke="{P["pur"]}" stroke-opacity=".12"/><line x1="1410" y1="482" x2="1410" y2="824" stroke="{P["pur"]}" stroke-opacity=".12"/>')

def brush(s, which):
    random.seed(5)
    if which == 'tl':
        d = 'M0 64 H300 C250 74 170 80 110 88 C74 93 52 106 46 130 C40 170 24 220 0 276 Z'
    else:
        d = 'M1440 900 V780 C1428 820 1408 846 1384 866 C1330 892 1230 898 1120 900 Z'
    s.a(f'<g filter="url(#rough4)"><path d="{d}" fill="{P["gold"]}"/>')
    cid = uid('bc')
    s.a(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})" opacity=".55">')
    for i in range(14):
        if which == 'tl': y = 66 + random.random() * 110; x0 = random.random() * 120; ln = 60 + random.random() * 200
        else: y = 830 + random.random() * 70; x0 = 1200 + random.random() * 200; ln = 40 + random.random() * 160
        s.a(f'<line x1="{x0:.0f}" y1="{y:.0f}" x2="{x0+ln:.0f}" y2="{y-random.random()*6:.0f}" stroke="{"#FFD25A" if i%2 else "#E69A00"}" stroke-width="{1+random.random()*2:.1f}"/>')
    s.a('</g></g>')
    # paper grain over the paint so it reads as pigment on paper
    s.a(f'<g clip-path="url(#{cid})"><rect x="0" y="0" width="1440" height="900" filter="url(#grain)" opacity=".10"/></g>')

def page(s, frame='paper', title_marks=True):
    canvas(s)
    if title_marks: margin_marks(s, frame == 'gold', frame == 'gold')
    if frame == 'gold': brush(s, 'tl'); brush(s, 'br')
    nav(s, 'purple')
    s.a(f'<g filter="url(#rough4)"><rect x="-10" y="64" width="1460" height="6" fill="{P["gold"]}"/></g>')

def eyebrow(s, text, xend=1368):
    T(s, ML, 114, text, 12.5, 700, UI, P['ink6'], extra='letter-spacing="0.4"')
    hair(s, ML + len(text) * 7.6 + 18, 110, xend, .16)

def head(s, eyebrow_text, title, sub, cur=None, btn=None):
    xend = 1368
    if cur is not None: xend = 1368 - 350
    eyebrow(s, eyebrow_text, xend)
    if cur is not None: F3.stepper(s, 1368, 110, cur)
    T(s, ML, 166, title, 34, 600, FD, P['ink'], extra='letter-spacing="-0.6"')
    T(s, ML, 194, sub, 14.5, 500, UI, P['ink7'])
    if btn: button(s, 1368 - btn[1], 142, btn[1], 46, btn[0], 'primary', 'plus')
    hair(s, ML, 220, 1368, .16)

def kebab(s, x, y):
    for i in range(3): s.a(f'<circle cx="{x}" cy="{y+i*5}" r="1.4" fill="{P["ink6"]}"/>')

def gallery4(s, x, y, w, cols=4, gap=24, row_gap=24, items=ITEMS):
    cw = (w - gap * (cols - 1)) / cols; pad = 8; tw = cw - 2 * pad; th = tw * .625; ch = pad + th + 72
    for i, (title, meta, st) in enumerate(items):
        cx = x + (i % cols) * (cw + gap); cy = y + (i // cols) * (ch + row_gap)
        rect(s, cx, cy + 2, cw, ch, '#241629', 8, op=.10, extra='filter="url(#sh2)"')
        rect(s, cx, cy, cw, ch, P['paper2'], 8, stroke='#241629', sw=1, extra='stroke-opacity=".10"')
        k, hr, fl, bg, pg = STUDIES[i % len(STUDIES)]; tx, ty = cx + pad, cy + pad
        if st == 'done':
            study(s, k, tx, ty, tw, th, bg, pg, bool(fl), 0, hr)
            rect(s, tx + tw - 50, ty + th - 28, 42, 20, P['ink'], 4, op=.86); T(s, tx + tw - 29, ty + th - 14, '3.2 s', 11.5, 700, UI, '#FFFAF0', 'middle')
        elif st in ('running', 'queued'):
            study(s, k, tx, ty, tw, th, bg, pg, bool(fl), 0, hr, op=.45)
            rect(s, tx + 10, ty + th - 34, tw - 20, 22, P['paper2'], 4, op=.92); ticks(s, tx + 20, ty + th - 31, tw - 40, 16)
        else:
            rect(s, tx, ty, tw, th, P['paper3'], 4); rect(s, tx, ty, tw, th, 'url(#hatch)', 4)
            ic(s, 'alert', tx + tw / 2 - 14, ty + th / 2 - 22, P['red'], 28); T(s, tx + tw / 2, ty + th / 2 + 28, 'Generation failed', 13.5, 700, UI, P['red'], 'middle')
        T(s, cx + 12, cy + pad + th + 26, title if len(title) < 34 else title[:33] + '…', 14.5, 700)
        kebab(s, cx + cw - 16, cy + pad + th + 14)
        T(s, cx + 12, cy + pad + th + 50, meta, 12.5, 500, UI, P['ink6'])
        chip(s, cx + cw - 12, cy + pad + th + 38, st, 'end', 24)
    return ch

def dash(frame):
    s = S(); page(s, frame)
    head(s, 'Library', 'Your animations', '8 animations, newest first', None, ('New animation', 192))
    gallery4(s, ML, 244, CW, 4, 24, 24)
    return s

# --- screens (same page template, no enclosing panel) ---
def s3():
    s = S(); page(s, 'gold'); head(s, 'New animation', 'Add your keyframes', 'Cue animates from the start drawing to the end drawing. Use two images of the same size.', 0)
    # continuous worktable: a full-bleed tonal band, not a card
    by, bh = 240, 516
    rect(s, 0, by, 1440, bh, '#F0E4CC'); grain(s, 0, by, 1440, bh, 0, .04, .03)
    hair(s, 0, by, 1440, .12); hair(s, 0, by + bh, 1440, .12)
    sw, sh = 600, 375; sx, ex, sy = ML, 1368 - sw, by + 40
    F3.tag(s, sx, sy - 14, 'start', 'Start drawing'); F3.tag(s, ex, sy - 14, 'end', 'End drawing')
    T(s, sx + sw, sy - 9, 'Where the motion begins', 13, 500, UI, P['ink6'], 'end'); T(s, ex + sw, sy - 9, 'Where it ends', 13, 500, UI, P['ink6'], 'end')
    rect(s, sx, sy + 12, sw, sh, '#241629', 6, op=.14, extra='filter="url(#sh2)"')
    sy += 12 + 0
    study(s, 'front', sx, sy, sw, sh, P['paper2'], P['gold'], False, 0, 1)
    rect(s, sx, sy, sw, sh, 'none', 6, stroke=P['ink'], sw=1, extra='stroke-opacity=".14"')
    T(s, sx, sy + sh + 30, 'start-pose.png', 14, 800); T(s, sx + 108, sy + sh + 30, '1.2 MB · 1024 × 640', 14, 500, UI, P['ink6'])
    button(s, sx + sw - 176, sy + sh + 10, 84, 36, 'Replace', 'secondary'); button(s, sx + sw - 84, sy + sh + 10, 84, 36, 'Remove', 'secondary')
    rect(s, ex, sy, sw, sh, '#FAF3E3', 6, stroke=P['line'], sw=1.5, dash='9 7')
    ic(s, 'img', ex + sw / 2 - 20, sy + 118, P['ink6'], 40)
    T(s, ex + sw / 2, sy + 198, 'Drop the end drawing here', 17, 800, UI, P['ink'], 'middle')
    T(s, ex + sw / 2, sy + 224, 'PNG or JPG, up to 10 MB, same size as the start drawing', 13.5, 500, UI, P['ink7'], 'middle')
    button(s, ex + sw / 2 - 74, sy + 248, 148, 42, 'Browse files', 'secondary')
    rect(s, ex, sy + sh + 10, sw, 48, P['red_t'], 6); rect(s, ex, sy + sh + 10, 4, 48, P['red'], 2)
    ic(s, 'alert', ex + 20, sy + sh + 25, P['red'], 17)
    T(s, ex + 46, sy + sh + 31, 'That file is 14.3 MB. Choose an image under 10 MB.', 14, 800, UI, P['red']); T(s, ex + 46, sy + sh + 49, 'Nothing was uploaded. Your start drawing is kept.', 12.5, 500, UI, P['ink7'])
    s.a(f'<path d="M{sx+sw+12} {sy+sh/2} H{ex-12} M{ex-19} {sy+sh/2-6} L{ex-12} {sy+sh/2} L{ex-19} {sy+sh/2+6}" fill="none" stroke="{P["ink6"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    F3.footer(s, 786, 'Back to Library', 'Continue to motion', 'Add both drawings to continue', 'disabled', 240)
    return s

def s4():
    s = S(); page(s, 'gold'); head(s, 'New animation', 'Describe the motion', 'Cue turns your sentence into an ordered plan. Nothing is generated until you approve it.', 1)
    lx, lw, y0 = ML, 520, 246
    T(s, lx, y0 + 16, 'Instruction', 20, 800, UI, P['ink'], extra='letter-spacing="-0.2"')
    T(s, lx, y0 + 50, 'Describe the motion', 13.5, 800); T(s, lx + 150, y0 + 50, 'Optional, in English', 13, 500, UI, P['ink6'])
    rect(s, lx, y0 + 62, lw, 118, P['paper2'], 8, stroke=P['line'], sw=1)
    T(s, lx + 16, y0 + 94, 'First move the eyes to the left, then', 16, 500); T(s, lx + 16, y0 + 120, 'slowly turn the head.', 16, 500); rect(s, lx + 177, y0 + 106, 2, 20, P['pur'])
    T(s, lx + lw, y0 + 202, '61 / 280', 12.5, 600, UI, P['ink6'], 'end'); T(s, lx, y0 + 202, 'Leave empty to use the drawings alone.', 12.5, 500, UI, P['ink6'])
    T(s, lx, y0 + 240, 'Examples', 13, 800)
    rect(s, lx + 76, y0 + 224, 170, 30, P['paper3'], 15); T(s, lx + 90, y0 + 244, 'Eyes first, then head', 12.5, 700)
    rect(s, lx + 258, y0 + 224, 196, 30, P['paper3'], 15); T(s, lx + 272, y0 + 244, 'Head turns while smiling', 12.5, 700)
    button(s, lx, y0 + 276, 150, 44, 'Preview plan', 'secondary')
    hair(s, lx, y0 + 346, lx + lw, .14)
    T(s, lx, y0 + 376, 'Keyframes', 13.5, 800); T(s, lx + lw, y0 + 376, 'Change drawings', 13.5, 800, UI, P['pur'], 'end', 'text-decoration="underline"')
    for i, (k, f, bg) in enumerate([('front', 0, P['paper2']), ('profile', 0, '#EFE4F3')]):
        x = lx + i * 200; study(s, k, x, y0 + 392, 160, 100, bg, P['gold'], False, 0, 1 if i == 0 else 0)
        rect(s, x, y0 + 392, 160, 100, 'none', 4, stroke=P['ink'], sw=1, extra='stroke-opacity=".16"'); F3.tag(s, x + 8, y0 + 408, 'start' if i == 0 else 'end')
    s.a(f'<path d="M{lx+168} {y0+442} H{lx+192} M{lx+186} {y0+436} L{lx+192} {y0+442} L{lx+186} {y0+448}" fill="none" stroke="{P["ink6"]}" stroke-width="1.5" stroke-linecap="round"/>')
    s.a(f'<line x1="640" y1="{y0}" x2="640" y2="{y0+498}" stroke="{P["ink"]}" stroke-opacity=".12"/>')
    px, pw = 684, 684
    T(s, px, y0 + 16, 'Motion plan', 20, 800, UI, P['ink'], extra='letter-spacing="-0.2"')
    w = 150; rect(s, px + pw - w, y0 - 2, w, 26, P['pur_t'], 13); ic(s, 'check', px + pw - w + 10, y0 + 4, P['pur'], 14); T(s, px + pw - w + 31, y0 + 16.5, 'Ready to approve', 12.5, 700, UI, P['pur'])
    T(s, px, y0 + 44, 'Cue read your sentence as 2 events, in this order.', 14, 500, UI, P['ink7'])
    ry = y0 + 90; cxr = px + 15
    s.a(f'<line x1="{cxr}" y1="{ry+15}" x2="{cxr}" y2="{ry+103}" stroke="{P["pur"]}" stroke-opacity=".38" stroke-width="1.5"/>'); T(s, cxr + 22, ry + 63, 'then', 12.5, 600, UI, P['ink6'])
    for i, (ti, su, sp, wd) in enumerate([('Look left', 'Gaze · eyes', 3, 'Fast'), ('Turn left', 'Head', 1, 'Slow')]):
        yy = ry + i * 88
        s.a(f'<circle cx="{cxr}" cy="{yy+15}" r="15" fill="{P["paper"]}" stroke="{P["pur"]}" stroke-width="1.6"/>'); T(s, cxr, yy + 22, str(i + 1), 18, 600, FD, P['pur'], 'middle')
        T(s, px + 48, yy + 14, ti, 17, 800); T(s, px + 48, yy + 35, su, 13.5, 500, UI, P['ink7'])
        for b in range(3): rect(s, px + pw - 92 + b * 10, yy + 30 - (7 + b * 5), 6, 7 + b * 5, P['org_g'] if b < sp else '#D8CBB4', 1.5)
        T(s, px + pw, yy + 22, wd, 13.5, 700, UI, P['ink'], 'end')
    T(s, px, y0 + 292, 'In plain words: the eyes look left quickly, then the head turns left slowly.', 14.5, 600)
    rect(s, px, y0 + 314, 22, 22, P['pur'], 5); ic(s, 'check', px + 3, y0 + 317, '#FFFAF0', 16)
    T(s, px + 34, y0 + 331, 'This plan matches what I meant', 15, 800); T(s, px + 34, y0 + 352, 'Order and speed only. Exact frame timing is not part of the plan.', 12.5, 500, UI, P['ink6'])
    hair(s, px, y0 + 386, px + pw, .14)
    T(s, px, y0 + 414, 'Output', 13.5, 800); T(s, px + pw, y0 + 414, '16 frames', 13, 600, UI, P['ink6'], 'end')
    ticks(s, px, y0 + 430, pw, 24, 16, P['ink'], .5)
    T(s, px, y0 + 476, 'Your start drawing', 12.5, 700, UI, P['pur']); T(s, px + pw, y0 + 476, 'Your end drawing', 12.5, 700, UI, P['ink'], 'end')
    F3.footer(s, 784, 'Back', 'Generate animation', None, 'primary', 244)
    return s

def s5(state='running'):
    s = S(); page(s, 'gold'); head(s, 'New animation', 'Generating your animation', 'You can leave this page. The job keeps running and stays in your library.', 2)
    ty = 266; cur = 1
    for i, lb in enumerate(['Queued', 'Processing', 'Completed']):
        x = ML + i * 220
        if i < cur: s.a(f'<circle cx="{x+12}" cy="{ty}" r="12" fill="{P["ink"]}"/>'); ic(s, 'check', x + 5, ty - 7, '#FFFAF0', 14)
        elif i == cur and state == 'running': s.a(f'<circle cx="{x+12}" cy="{ty}" r="12" fill="{P["blue_t"]}" stroke="{P["blue"]}" stroke-width="1.6" stroke-dasharray="4 3"/><circle cx="{x+12}" cy="{ty}" r="3.2" fill="{P["blue"]}"/>')
        elif i == cur: s.a(f'<circle cx="{x+12}" cy="{ty}" r="12" fill="{P["red_t"]}" stroke="{P["red"]}" stroke-width="1.6"/>'); ic(s, 'alert', x + 5, ty - 7, P['red'], 14)
        else: s.a(f'<circle cx="{x+12}" cy="{ty}" r="11.5" fill="none" stroke="{P["line"]}" stroke-width="1.3"/>')
        failed = (i == cur and state == 'failed')
        T(s, x + 34, ty + 5.5, 'Failed' if failed else lb, 15, 800 if i == cur else 600, UI, P['red'] if failed else (P['ink'] if i <= cur else P['ink6']))
        if i < 2: s.a(f'<line x1="{x+128}" y1="{ty}" x2="{x+206}" y2="{ty}" stroke="{P["line"]}" stroke-opacity=".7"/>')
    T(s, 1368, ty - 2, 'Elapsed', 13, 500, UI, P['ink6'], 'end'); T(s, 1368, ty + 24, '02:14', 22, 700, UI, P['ink'], 'end', 'style="font-variant-numeric: tabular-nums"')
    T(s, ML, ty + 62, 'Cue is drawing frames 2 to 15. Frames 1 and 16 are your own drawings, kept exactly as uploaded.' if state == 'running' else 'Generation stopped at the GPU worker. Your drawings and plan are saved.', 15.5, 600, UI, P['ink'] if state == 'running' else P['red'])
    T(s, ML, ty + 88, 'No estimate is shown because Cue cannot tell how long this will take.' if state == 'running' else 'Go back to your library to start a new animation.', 13.5, 500, UI, P['ink7'])
    fy, fw = 400, CW; pitch = fw / 16
    rect(s, ML, fy, fw, 108, P['viewer'], 6)
    for i in range(16):
        x = ML + i * pitch
        for sy in (fy + 7, fy + 93): rect(s, x + pitch / 2 - 5, sy, 10, 7, '#3A2C44', 2)
        cx, cw = x + 6, pitch - 12; chh = cw * .625; cy = fy + 21
        if i == 0: study(s, 'front', cx, cy, cw, chh, P['paper2'], P['gold'], False, 0, 1); rect(s, cx - 2, cy - 2, cw + 4, chh + 4, 'none', 2, stroke=P['pur_t'], sw=2)
        elif i == 15: study(s, 'profile', cx, cy, cw, chh, '#EFE4F3', P['gold']); rect(s, cx - 2, cy - 2, cw + 4, chh + 4, 'none', 2, stroke=P['gold'], sw=2)
        else: rect(s, cx, cy, cw, chh, '#2A1E33', 2); rect(s, cx, cy, cw, chh, 'none', 2, stroke='#5E4F68', sw=1, dash='3 3' if state == 'running' else None)
        T(s, x + pitch / 2, fy + 132, str(i + 1), 12, 600, UI, P['ink6'], 'middle', 'style="font-variant-numeric: tabular-nums"')
    T(s, ML, fy + 160, 'Your start drawing', 12.5, 700, UI, P['pur']); T(s, ML + fw, fy + 160, 'Your end drawing', 12.5, 700, UI, P['ink'], 'end')
    dy = 628; hair(s, ML, dy - 30, 1368, .14); s.a(f'<line x1="720" y1="{dy-30}" x2="720" y2="{dy+130}" stroke="{P["ink"]}" stroke-opacity=".12"/>')
    T(s, ML, dy, 'Your plan', 16, 800)
    for i, (t, su) in enumerate([('Look left', 'Gaze · fast'), ('Turn left', 'Head · slow')]):
        s.a(f'<circle cx="{ML+15}" cy="{dy+34+i*34}" r="11" fill="none" stroke="{P["pur"]}" stroke-width="1.4"/>'); T(s, ML + 15, dy + 39 + i * 34, str(i + 1), 13, 600, FD, P['pur'], 'middle')
        T(s, ML + 38, dy + 39 + i * 34, t, 14.5, 700); T(s, ML + 138, dy + 39 + i * 34, su, 13.5, 500, UI, P['ink7'])
    T(s, 756, dy, 'Run details', 16, 800)
    for i, (k, v) in enumerate([('Job', '#A83F'), ('Submitted', 'Oct 22, 13:42'), ('Model version', 'cue-m3 0.3.1'), ('Seed', '41827')]):
        T(s, 756, dy + 30 + i * 26, k, 13.5, 500, UI, P['ink6']); T(s, 1010, dy + 30 + i * 26, v, 13.5, 700)
    button(s, 1210, dy - 14, 158, 42, 'Cancel generation' if state == 'running' else 'New animation', 'danger' if state == 'running' else 'primary')
    button(s, ML, 800, 160, 44, 'Back to Library', 'secondary')
    return s

def s6():
    s = S(); page(s, 'gold'); head(s, 'New animation', 'Your animation is ready', '“First move the eyes to the left, then slowly turn the head.”', 3)
    vx, vy, vw, vh = ML, 240, 864, 540
    rect(s, vx, vy + 4, vw, vh, '#241629', 10, op=.18, extra='filter="url(#sh2)"')
    rect(s, vx, vy, vw, vh, P['viewer'], 10)
    study(s, 'threeq', vx + 16, vy + 12, vw - 32, vh - 24, P['paper2'], P['gold'], False, 0, 0, gaze=-2)
    cy = vy + vh + 22
    s.a(f'<circle cx="{vx+22}" cy="{cy+20}" r="22" fill="{P["pur"]}"/>'); ic(s, 'play', vx + 15, cy + 12, '#FFFAF0', 16)
    for i, k in enumerate(['prev', 'next', 'loop']): ic(s, k, vx + 68 + i * 44, cy + 12, P['ink'], 16)
    ticks(s, vx + 210, cy + 6, 500, 30, 16, P['ink'], .55)
    s.a(f'<rect x="{vx+210+500/16*7.5-6}" y="{cy}" width="12" height="42" rx="3" fill="none" stroke="{P["pur"]}" stroke-width="2.2"/>')
    T(s, vx + vw, cy + 25, 'Frame 8 of 16', 13.5, 700, UI, P['ink'], 'end', 'style="font-variant-numeric: tabular-nums"')
    rx, rw = 984, 384
    s.a(f'<line x1="{rx-24}" y1="240" x2="{rx-24}" y2="{vy+vh+60}" stroke="{P["ink"]}" stroke-opacity=".12"/>')
    button(s, rx, 240, rw, 50, 'Download MP4', 'primary', 'down')
    T(s, rx, 330, 'Details', 16, 800)
    for i, (k, v) in enumerate([('Plan', '1 Look left, 2 Turn left'), ('Format', 'MP4 · 512 × 320'), ('Length', '16 frames · 3.2 s'), ('Created', 'Oct 22, 13:46'), ('Generated in', '3 min 52 s'), ('Model version', 'cue-m3 0.3.1'), ('Seed', '41827')]):
        yy = 362 + i * 38; T(s, rx, yy, k, 13.5, 500, UI, P['ink6']); T(s, rx + rw, yy, v, 13.5, 700, UI, P['ink'], 'end'); hair(s, rx, yy + 14, rx + rw, .10)
    button(s, rx, 656, 180, 44, 'Back to Library', 'secondary'); button(s, rx + 192, 656, 184, 44, 'New animation', 'ghost', 'plus')
    return s

def s1():
    s = S(); canvas(s)
    # painterly gold brand panel: its right edge is brushed, not ruled
    s.a(f'<g filter="url(#rough4)"><rect x="-40" y="-40" width="900" height="980" fill="{P["gold"]}"/></g>')
    s.a(f'<rect x="0" y="0" width="840" height="900" fill="url(#reg)" opacity=".9"/>')
    grain(s, 0, 0, 840, 900, 0, .08, .0)
    rect(s, 36, 170, 660, 250, P['gold']); grain(s, 36, 170, 660, 250, 0, .08, 0)
    F3.wordmark(s, 64, 100, 34, P['ink'], P['pur']) if hasattr(F3, 'wordmark') else wordmark(s, 64, 100, 34, P['ink'], P['pur'])
    T(s, 64, 244, 'Two drawings in.', 54, 600, FD, P['ink'], extra='letter-spacing="-1"'); T(s, 64, 306, 'One animation out.', 54, 600, FD, P['ink'], extra='letter-spacing="-1"')
    T(s, 64, 362, 'Upload a start and an end drawing, describe the motion in English,', 17, 500, UI, P['ink7']); T(s, 64, 388, 'and Cue draws the frames in between.', 17, 500, UI, P['ink7'])
    s.a(f'<g filter="url(#rough4)"><rect x="-30" y="476" width="868" height="470" fill="{P["pur"]}"/></g>'); grain(s, 0, 480, 828, 420, 0, .06, 0)
    for i, (k, hr, f, bg, pg, lab) in enumerate([('front', 0, 0, '#FBE8D2', P['gold'], 'Start drawing'), ('threeq', 0, 0, '#E9EEF7', P['org'], 'Drawn by Cue'), ('profile', 0, 0, '#EFE4F3', P['gold'], 'End drawing')]):
        x = 64 + i * 232; y = 526 + (0 if i != 1 else 24)
        rect(s, x, y + 8, 208, 236, '#000', 4, op=.28, extra='filter="url(#sh2)"'); study(s, k, x, y, 208, 236, bg, pg, False, 0, hr)
        T(s, x, y + 266, lab, 13.5, 700, UI, '#FFFAF0')
    ticks(s, 64, 856, 712, 24, 16, '#FFFAF0', .6)
    rect(s, 840, 0, 600, 900, P['paper']); grain(s, 840, 0, 600, 900, 0, .05, .04)
    s.a(f'<g filter="url(#rough4)"><rect x="826" y="-20" width="26" height="940" fill="{P["gold"]}"/></g>')
    mark(s, 1410, 60); mark(s, 1410, 840)
    fx, fw = 928, 424
    T(s, fx, 214, 'Welcome back', 28, 800, UI, P['ink'], extra='letter-spacing="-0.4"'); T(s, fx, 242, 'Log in to see your animations.', 15, 500, UI, P['ink7'])
    T(s, fx, 304, 'Log in', 15, 800); rect(s, fx, 316, 52, 3, P['pur']); T(s, fx + 100, 304, 'Create account', 15, 600, UI, P['ink6']); hair(s, fx, 318, fx + fw, .2); rect(s, fx, 316, 52, 3, P['pur'])
    T(s, fx, 364, 'Email', 13.5, 800); rect(s, fx, 376, fw, 46, P['paper2'], 8, stroke=P['line'], sw=1); T(s, fx + 14, 405, 'mira@studio.example', 15.5, 500)
    T(s, fx, 452, 'Password', 13.5, 800); rect(s, fx - 3, 461, fw + 6, 52, P['paper'], 10); rect(s, fx - 1.5, 462.5, fw + 3, 49, 'none', 9, stroke=P['pur'], sw=2); rect(s, fx, 464, fw, 46, P['paper2'], 8)
    T(s, fx + 14, 495, '••••••••••', 17, 700); T(s, fx + fw - 14, 493, 'Show', 13.5, 800, UI, P['pur'], 'end'); T(s, fx, 536, 'Use at least 8 characters.', 13, 500, UI, P['ink6'])
    button(s, fx, 572, fw, 50, 'Log in', 'primary'); T(s, fx + fw / 2, 668, 'New to Cue? Create an account', 14.5, 700, UI, P['pur'], 'middle', 'text-decoration="underline"')
    return s

def overlay():
    s = dash('gold')  # Level 3 demo: a temporary dialog over the library
    rect(s, 0, 64, 1440, 836, P['ink'], 0, op=.38)
    rect(s, 480, 330, 480, 230, '#241629', 14, op=.30, extra='filter="url(#sh)"'); rect(s, 480, 320, 480, 230, P['paper2'], 14, stroke=P['ink'], sw=1, extra='stroke-opacity=".12"')
    T(s, 512, 366, 'Delete this animation?', 20, 800); T(s, 512, 394, 'The video, its plan and its drawings are removed.', 14, 500, UI, P['ink7']); T(s, 512, 414, 'This cannot be undone.', 14, 500, UI, P['ink7'])
    T(s, 512, 446, '“Look down, then look up quickly”', 14, 700)
    button(s, 618, 486, 140, 44, 'Cancel', 'secondary'); button(s, 770, 486, 160, 44, 'Delete', 'danger')
    return s

def tile():
    s = S(); canvas(s); margin_marks(s); brush(s, 'tl'); brush(s, 'br'); nav(s, 'purple')
    eyebrow(s, 'Integrated Atelier'); T(s, ML, 166, 'Paper is the canvas', 34, 600, FD, extra='letter-spacing="-0.6"'); T(s, ML, 194, 'No enclosing panel: navigation, page canvas, then components directly on the page.', 14.5, 500, UI, P['ink7']); hair(s, ML, 220, 1368, .16)
    T(s, ML, 262, 'Surface levels', 16, 800)
    lv = [('1  Page canvas', 'Warm paper with grain and fibre. The working surface.', P['paper'], None, 0), ('2  Functional surfaces', 'Cards, inputs, upload zones, viewer. Tone and hairline.', P['paper2'], '#241629', .10), ('3  Overlays', 'Dialogs and menus only. Elevated, with a scrim.', P['paper2'], '#241629', .12)]
    for i, (n, d, c, bc, bo) in enumerate(lv):
        x = ML + i * 336
        if i == 2: rect(s, x, 292 + 10, 308, 104, '#241629', 12, op=.25, extra='filter="url(#sh)"')
        rect(s, x, 292, 308, 104, c, 8 if i < 2 else 12, stroke=bc, sw=1 if bc else 0, extra=f'stroke-opacity="{bo}"')
        if i == 1: rect(s, x, 292 + 2, 308, 104, '#241629', 8, op=.0)
        T(s, x + 16, 326, n, 14.5, 800); T(s, x + 16, 350, d[:46], 12.5, 500, UI, P['ink7']); T(s, x + 16, 368, d[46:], 12.5, 500, UI, P['ink7'])
    T(s, ML, 450, 'Palette', 16, 800)
    for i, (n, c) in enumerate([('Deep purple', P['pur']), ('Golden yellow', P['gold']), ('Warm paper', P['paper']), ('Light paper', P['paper2']), ('Dark ink', P['ink']), ('Painted blue', P['blue']), ('Pigment orange', P['org'])]):
        x = ML + i * 112; rect(s, x, 470, 100, 60, c, 6, stroke='#241629', sw=1, extra='stroke-opacity=".16"'); T(s, x, 550, n, 12, 700); T(s, x, 566, c, 12, 500, UI, P['ink6'])
    T(s, ML, 622, 'Type', 16, 800); T(s, ML, 668, 'Your animations', 34, 600, FD, extra='letter-spacing="-0.6"'); T(s, ML, 694, 'Fraunces for page titles and brand moments · Manrope for everything operational', 13.5, 500, UI, P['ink7'])
    button(s, ML, 730, 190, 46, 'Generate animation', 'primary'); button(s, ML + 204, 730, 110, 46, 'Back', 'secondary'); chip(s, ML + 330, 740, 'running'); chip(s, ML + 460, 740, 'done'); chip(s, ML + 552, 740, 'failed')
    T(s, 760, 262, 'Marks and brush', 16, 800)
    rect(s, 760, 282, 300, 200, P['paper']); mark(s, 800, 322); mark(s, 1020, 322); mark(s, 800, 442); mark(s, 1020, 442); T(s, 910, 388, 'Margins only', 13, 700, UI, P['ink7'], 'middle')
    rect(s, 1084, 282, 284, 200, P['paper']); s.a(f'<g filter="url(#rough4)"><path d="M1084 282 H1250 C1230 306 1200 320 1170 330 C1140 340 1100 350 1084 392 Z" fill="{P["gold"]}"/></g>'); T(s, 1226, 440, 'Corners and brand', 13, 700, UI, P['ink7'], 'middle')
    T(s, 760, 520, 'Brush is used on S1, the page corners, and empty states. Never on cards, buttons, inputs or data.', 13, 500, UI, P['ink7'])
    return s

if __name__ == '__main__':
    out = sys.argv[1]
    import lib3
    def sv(name, scr, sub):
        os.makedirs(f'{out}/{sub}', exist_ok=True)
        open(f'{out}/{sub}/{name}.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="900" viewBox="0 0 1440 900">{DEFS4}\n{scr}\n</svg>')
    sv('dashboard-A-integrated-paper', dash('paper'), 'experiments'); sv('dashboard-B-paper-golden-frame', dash('gold'), 'experiments')
    sv('s1-authentication', s1(), 'previews'); sv('s2-dashboard', dash('gold'), 'previews'); sv('s3-keyframe-upload', s3(), 'previews'); sv('s4-motion-plan', s4(), 'previews')
    sv('s5-generation-status', s5(), 'previews'); sv('s5-generation-status-failed', s5('failed'), 'previews'); sv('s6-result-preview', s6(), 'previews')
    sv('overlay-delete-dialog', overlay(), 'previews'); sv('style-tile', tile(), 'style-tile')
