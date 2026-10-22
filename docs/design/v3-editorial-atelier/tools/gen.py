import math, random, sys, os

# ---------- tokens (V2 candidates, see tokens.json) ----------
K = dict(
    gold='#F8AA09', gold3='#FBC750', gold6='#E68F1F',
    cream1='#FBF3E4', cream2='#F6E8D1', cream3='#EDE0CA',
    ink='#241629', ink7='#4B3B52', ink6='#6B5A72', hair='#CDB99A',
    pur='#4F0964', pur7='#65198A', pur9='#3B0650', pur1='#E8D7F0',
    blue='#23437C', blue8='#1F3664', blue1='#DCE5F3',
    org='#F88526', org6='#D2620F', org7='#B03E06', org1='#FCE0C4',
    red='#A1413C', red1='#F6D9D4', grn='#2F6B3B', grn1='#D9EAD3',
    warn='#8A5A00', warn1='#FBE6A6', viewer='#1B1220', paper='#FFFDF7',
)
FD, FB, UI = 'Fraunces Display', 'Fraunces Display Bold', 'Manrope'
_id = [0]
def uid(p='i'):
    _id[0] += 1
    return f'{p}{_id[0]}'

DEFS = f'''<defs>
<filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/>
<feColorMatrix type="matrix" values="0 0 0 0 0.14  0 0 0 0 0.086  0 0 0 0 0.16  0 0 0 1.3 -0.5"/></filter>
<filter id="fiber" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.012 0.30" numOctaves="2" seed="21"/>
<feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.30  0 0 0 0 0.20  0 0 0 1.6 -0.7"/></filter>
<filter id="rough" x="-5%" y="-10%" width="110%" height="120%">
<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="16" xChannelSelector="R" yChannelSelector="G"/></filter>
<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<line x1="0" y1="0" x2="0" y2="8" stroke="#6B5A72" stroke-width="1" opacity=".35"/></pattern>
</defs>'''

class S:
    def __init__(self): self.p = []
    def a(self, s): self.p.append(s)
    def __str__(self): return '\n'.join(self.p)

def T(s, x, y, txt, size=14, w=500, fam=UI, fill=K['ink'], anchor='start', extra=''):
    txt = txt.replace('&', '&amp;')
    s.a(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{txt}</text>')

def rect(s, x, y, w, h, fill, rx=0, stroke=None, sw=1, op=None, dash=None, extra=''):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ''
    o = f' opacity="{op}"' if op is not None else ''
    d = f' stroke-dasharray="{dash}"' if dash else ''
    s.a(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}{o}{d} {extra}/>')

def grain(s, x, y, w, h, rx=0, op=.10, fib=.07):
    c = uid('c')
    s.a(f'<clipPath id="{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>')
    s.a(f'<g clip-path="url(#{c})"><rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#grain)" opacity="{op}"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#fiber)" opacity="{fib}"/></g>')

def panel(s, x, y, w, h, fill=None, rx=12, tex=True):
    fill = fill or K['cream2']
    rect(s, x, y + 3, w, h, K['ink'], rx, op=.16)          # hard print shadow
    rect(s, x, y, w, h, fill, rx, stroke=K['ink'], sw=1.5)
    if tex: grain(s, x, y, w, h, rx, .09, .05)

# ---------- icons (20px box at x,y) ----------
def ic(s, kind, x, y, col, sz=16):
    k = sz / 16
    g = f'<g transform="translate({x},{y}) scale({k})" fill="none" stroke="{col}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
    if kind == 'check': g += '<path d="M2.5 8.5 6.5 12.5 13.5 4"/>'
    elif kind == 'clock': g += '<circle cx="8" cy="8" r="6"/><path d="M8 4.5V8l2.5 1.5"/>'
    elif kind == 'alert': g += '<path d="M8 2 14.5 13.5H1.5Z"/><path d="M8 6.5v3.2M8 11.8v.1"/>'
    elif kind == 'run': g += '<circle cx="8" cy="8" r="6" stroke-dasharray="4 3"/><circle cx="8" cy="8" r="1.8" fill="%s" stroke="none"/>' % col
    elif kind == 'play': g += '<path d="M4.5 2.8 13 8l-8.5 5.2Z" fill="%s"/>' % col
    elif kind == 'pause': g += '<path d="M5 3v10M11 3v10" stroke-width="2.6"/>'
    elif kind == 'down': g += '<path d="M8 2v8.5M4.5 7.5 8 11l3.5-3.5M2.5 14h11"/>'
    elif kind == 'plus': g += '<path d="M8 2.5v11M2.5 8h11"/>'
    elif kind == 'prev': g += '<path d="M11 3 5 8l6 5M3.5 3v10"/>'
    elif kind == 'next': g += '<path d="M5 3l6 5-6 5M12.5 3v10"/>'
    elif kind == 'loop': g += '<path d="M3 7V6a2 2 0 0 1 2-2h7l-2-2M13 9v1a2 2 0 0 1-2 2H4l2 2"/>'
    elif kind == 'img': g += '<rect x="2" y="3" width="12" height="10" rx="1.5"/><circle cx="6" cy="7" r="1.2"/><path d="m3 12 3.5-3 3 2.5 2-1.5 2 2"/>'
    elif kind == 'swap': g += '<path d="M2.5 5.5h10l-2.5-2.5M13.5 10.5h-10l2.5 2.5"/>'
    elif kind == 'chev': g += '<path d="M3 6l5 5 5-5"/>'
    elif kind == 'user': g += '<circle cx="8" cy="5.5" r="2.8"/><path d="M2.5 14c.6-3 2.8-4.4 5.5-4.4s4.9 1.4 5.5 4.4"/>'
    g += '</g>'
    s.a(g)

# ---------- line-art faces (stand-in for user drawings) ----------
def face(s, cx, cy, sz, turn=0, gaze=0, smile=.3, col=None, hair=False):
    col = col or K['ink']; sw = max(1.6, sz * .022)
    rx = .36 * sz * (1 - .16 * abs(turn)); ry = .44 * sz; hx = cx + turn * .24 * sz
    a = lambda t: s.a(t)
    st = f'fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    a(f'<path d="M{hx-.13*sz:.1f} {cy+ry*.95:.1f} L{hx-.12*sz:.1f} {cy+ry+.20*sz:.1f} M{hx+.13*sz:.1f} {cy+ry*.95:.1f} L{hx+.12*sz:.1f} {cy+ry+.20*sz:.1f}" {st}/>')
    a(f'<path d="M{cx-.62*sz:.1f} {cy+ry+.62*sz:.1f} Q{cx-.55*sz:.1f} {cy+ry+.26*sz:.1f} {hx:.1f} {cy+ry+.24*sz:.1f} Q{cx+.55*sz:.1f} {cy+ry+.26*sz:.1f} {cx+.62*sz:.1f} {cy+ry+.62*sz:.1f}" {st}/>')
    a(f'<ellipse cx="{hx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" {st}/>')
    a(f'<path d="M{hx-rx:.1f} {cy-.08*sz:.1f} Q{hx-rx*.9:.1f} {cy-ry*1.18:.1f} {hx+rx*.2:.1f} {cy-ry*1.08:.1f} Q{hx+rx*.9:.1f} {cy-ry*.95:.1f} {hx+rx:.1f} {cy-.1*sz:.1f} Q{hx+rx*.3:.1f} {cy-ry*.62:.1f} {hx-rx*.55:.1f} {cy-ry*.5:.1f}Z" {st.replace('fill="none"', 'fill="%s"' % (col if hair else 'none'))}/>')
    ex = .14 * sz * (1 - .25 * abs(turn)); mid = hx + turn * .13 * sz; ey = cy - .02 * sz
    for sgn in (-1, 1):
        x0 = mid + sgn * ex
        a(f'<ellipse cx="{x0:.1f}" cy="{ey:.1f}" rx="{.05*sz:.1f}" ry="{.032*sz:.1f}" {st}/>')
        a(f'<circle cx="{x0+gaze*.026*sz:.1f}" cy="{ey:.1f}" r="{.02*sz:.1f}" fill="{col}"/>')
        a(f'<path d="M{x0-.05*sz:.1f} {ey-.08*sz:.1f} Q{x0:.1f} {ey-.105*sz:.1f} {x0+.05*sz:.1f} {ey-.08*sz:.1f}" {st}/>')
    nx = hx + turn * .20 * sz
    a(f'<path d="M{nx:.1f} {ey+.03*sz:.1f} L{nx-.02*sz:.1f} {ey+.13*sz:.1f} L{nx+.03*sz:.1f} {ey+.13*sz:.1f}" {st}/>')
    mx = hx + turn * .16 * sz; my = cy + .22 * sz
    a(f'<path d="M{mx-.09*sz:.1f} {my:.1f} Q{mx:.1f} {my+smile*.22*sz:.1f} {mx+.09*sz:.1f} {my:.1f}" {st}/>')

def drawing(s, x, y, w, h, bg=None, rx=6, turn=0, gaze=0, smile=.3, stroke=None, scale=.62, hair=False):
    bg = bg or K['paper']
    rect(s, x, y, w, h, bg, rx)
    c = uid('d')
    s.a(f'<clipPath id="{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath><g clip-path="url(#{c})">')
    face(s, x + w / 2, y + h * .43, min(w, h * 1.25) * scale, turn, gaze, smile, hair=hair)
    s.a('</g>')

# ---------- shared components ----------
def wordmark(s, x, y, size=34, col=None, ends=None):
    col = col or K['ink']; ends = ends or K['pur']
    for i in range(7):
        e = i in (0, 6); h = size * (.62 if e else .42)
        rect(s, x + i * size * .17, y - h + (0 if e else -size * .04), size * .09, h, ends if e else col, size * .02)
    T(s, x + size * 1.32, y, 'Cue', size * 1.18, 800, FB, col)

CH = dict(done=('Done', 'check', K['grn1'], K['grn']), running=('Running', 'run', K['blue1'], K['blue']),
          queued=('Queued', 'clock', K['cream3'], K['ink7']), failed=('Failed', 'alert', K['red1'], K['red']),
          cancelled=('Cancelled', 'alert', K['cream3'], K['ink7']))
def chip(s, x, y, kind, anchor='start'):
    lab, icon, bg, fg = CH[kind]; w = 42 + len(lab) * 8.4
    if anchor == 'end': x = x - w
    rect(s, x, y, w, 28, bg, 14, stroke=fg, sw=1.2)
    ic(s, icon, x + 10, y + 6, fg, 16)
    T(s, x + 32, y + 19, lab, 13, 700, UI, fg)
    return w

def button(s, x, y, w, h, label, kind='primary', icon=None):
    if kind == 'primary':
        rect(s, x, y + 3, w, h, K['ink'], 9, op=.9); rect(s, x, y, w, h, K['pur'], 9, stroke=K['ink'], sw=1.5); fg = K['cream1']
    elif kind == 'secondary':
        rect(s, x, y, w, h, K['cream1'], 9, stroke=K['ink'], sw=1.5); fg = K['ink']
    elif kind == 'disabled':
        rect(s, x, y, w, h, K['cream3'], 9, stroke=K['hair'], sw=1.5); fg = K['ink6']
    elif kind == 'danger':
        rect(s, x, y, w, h, K['cream1'], 9, stroke=K['red'], sw=1.5); fg = K['red']
    tw = len(label) * 8.4; ix = 0
    if icon: ix = 24
    sx = x + (w - tw - ix) / 2
    if icon: ic(s, icon, sx, y + h / 2 - 8, fg, 16)
    T(s, sx + ix + (0 if icon else 0), y + h / 2 + 5.5, label, 15, 700, UI, fg)

def stepbar(s, x, y, cur, shell_text=K['ink']):
    names = ['Keyframes', 'Motion', 'Generate', 'Result']; px = x
    for i, n in enumerate(names):
        st = 'done' if i < cur else 'cur' if i == cur else 'todo'
        if st == 'done': s.a(f'<circle cx="{px+14}" cy="{y}" r="13" fill="{K["ink"]}"/>'); ic(s, 'check', px + 6, y - 8, K['cream1'], 16)
        elif st == 'cur': s.a(f'<circle cx="{px+14}" cy="{y}" r="13" fill="{K["pur"]}" stroke="{K["ink"]}" stroke-width="1.5"/>'); T(s, px + 14, y + 6, str(i + 1), 15, 800, FB, K['cream1'], 'middle')
        else: s.a(f'<circle cx="{px+14}" cy="{y}" r="12.5" fill="none" stroke="{K["ink7"]}" stroke-width="1.5"/>'); T(s, px + 14, y + 6, str(i + 1), 14, 700, UI, K['ink7'], 'middle')
        T(s, px + 36, y + 5, n, 15, 800 if st == 'cur' else 600, UI, shell_text if st != 'todo' else K['ink7'])
        px += 36 + len(n) * 8.6 + 22
        if i < 3: s.a(f'<line x1="{px-14}" y1="{y}" x2="{px+6}" y2="{y}" stroke="{K["ink7"]}" stroke-width="1.5"/>'); px += 14

def page(s, theme, band=240):
    if theme == 'A':
        rect(s, 0, 0, 1440, 900, K['gold'])
        grain(s, 0, 0, 1440, 900, 0, .12, .05)
    else:
        rect(s, 0, 0, 1440, 900, K['cream2'])
        grain(s, 0, 0, 1440, 900, 0, .08, .06)
        rect(s, 0, 0, 1440, band, K['gold'])
        grain(s, 0, 0, 1440, band, 0, .12, .07)
        s.a(f'<line x1="0" y1="{band}" x2="1440" y2="{band}" stroke="{K["ink"]}" stroke-width="1.5"/>')

def topbar(s, active='Library', theme='A'):
    wordmark(s, 40, 50, 30)
    T(s, 190, 48, 'Library', 16, 800 if active == 'Library' else 600)
    if active == 'Library': rect(s, 190, 56, 56, 3, K['pur'], 1.5)
    s.a(f'<line x1="40" y1="76" x2="1400" y2="76" stroke="{K["ink"]}" stroke-width="1.2" opacity=".55"/>')
    s.a(f'<circle cx="1190" cy="40" r="15" fill="{K["cream1"]}" stroke="{K["ink"]}" stroke-width="1.5"/>')
    T(s, 1190, 46, 'M', 15, 800, FB, K['ink'], 'middle')
    T(s, 1214, 45, 'mira@studio.example', 14, 600, UI, K['ink'])
    ic(s, 'chev', 1376, 32, K['ink'], 16)

def stripe(s, x, y, w, h=22, ends=(K['org6'], K['org6']), tick=K['ink'], op=1, n=16):
    pitch = w / n
    for i in range(n):
        e = i in (0, n - 1)
        th = h if e else h * .66
        rect(s, x + i * pitch + pitch * .2, y + (h - th), pitch * .46, th, ends[0] if e else tick, 1.5, op=None if e else .85 * op)

# ---------- cue sheet ----------
def cuesheet(s, x, y, w, events, label_w=92):
    tx = x + label_w; tw = w - label_w
    T(s, tx, y - 6, 'Start drawing', 12, 800, UI, K['org7'])
    T(s, tx + tw, y - 6, 'End drawing', 12, 800, UI, K['org7'], 'end')
    stripe(s, tx, y + 4, tw, 22, (K['org6'], K['org6']), K['ink'])
    lanes = {}
    for i, e in enumerate(events):
        ly = y + 50 + i * 76; lanes[i] = ly
        T(s, x, ly + 38, e['region'], 14, 800, UI, K['ink'])
        rect(s, tx, ly, tw, 60, K['cream3'], 6)
        for j in range(17):  # ruled sheet lines
            s.a(f'<line x1="{tx + j*tw/16:.1f}" y1="{ly}" x2="{tx + j*tw/16:.1f}" y2="{ly+60}" stroke="{K["hair"]}" stroke-width=".8"/>')
        bx = tx + e['x']; bw = e['w']
        rect(s, bx + 2, ly + 5, bw, 50, K['ink'], 7, op=.18)
        rect(s, bx, ly + 3, bw, 50, K['pur1'], 7, stroke=K['ink'], sw=1.5)
        s.a(f'<circle cx="{bx+27}" cy="{ly+28}" r="16" fill="{K["pur"]}"/>')
        T(s, bx + 27, ly + 35, str(i + 1), 20, 800, FB, K['cream1'], 'middle')
        T(s, bx + 52, ly + 25, e['title'], 15, 800, UI, K['ink'])
        T(s, bx + 52, ly + 44, e['sub'], 13, 600, UI, K['ink7'])
        for c in range(3):  # speed chevrons: filled count = speed
            on = c < e['speed']
            s.a(f'<path d="M{bx+bw-58+c*13} {ly+18} l8 10 -8 10" fill="none" stroke="{K["org7"] if on else K["hair"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    for i in range(len(events) - 1):
        a = events[i]; b = events[i + 1]
        x1 = tx + a['x'] + a['w']; y1 = lanes[i] + 28; x2 = tx + b['x']; y2 = lanes[i + 1] + 28; mx = (x1 + x2) / 2
        s.a(f'<path d="M{x1} {y1} H{mx} V{y2} H{x2-4}" fill="none" stroke="{K["ink"]}" stroke-width="1.8"/>'
            f'<path d="M{x2-9} {y2-5} L{x2-1} {y2} L{x2-9} {y2+5}" fill="none" stroke="{K["ink"]}" stroke-width="1.8" stroke-linejoin="round"/>')
    return y + 50 + len(events) * 76

# ---------- screens ----------
CARDS = [
    ('Move the eyes left, then turn the head', 'Oct 22 · 13:42', 'running', 0, .1),
    ('Nod slowly, then start smiling', 'Oct 22 · 13:20', 'queued', .2, .4),
    ('Raise the hand while turning', 'Oct 21 · 17:08', 'done', -.8, .1),
    ('Turn the head, then move the eyes', 'Oct 21 · 16:51', 'done', -.9, -.8),
    ('Blink twice, then tilt the head', 'Oct 20 · 22:15', 'done', .2, .6),
    ('Smile near the end of the turn', 'Oct 20 · 19:34', 'done', .9, .9),
    ('Look down, then look up quickly', 'Oct 19 · 11:02', 'failed', 0, 0),
    ('Slow head turn to the left', 'Oct 18 · 09:47', 'done', -.8, -.3),
]
BGS = [K['paper'], '#EAF0FA', '#FDEBD3', '#F1E6F6', K['paper'], '#EAF0FA', K['paper'], '#FDEBD3']

def screen_s2(theme):
    s = S(); page(s, theme, 232); topbar(s, 'Library', theme)
    T(s, 40, 150, 'Your animations', 52, 600, FD, K['ink'])
    T(s, 40, 186, '8 animations, newest first.', 16, 500, UI, K['ink7'])
    button(s, 1196, 128, 204, 50, 'New animation', 'primary', 'plus')
    px, py, pw, ph = 40, 232 if theme == 'A' else 262, 1360, 610
    if theme == 'B': panel(s, px, py, pw, ph)
    cw, ch = (313, 282) if theme == 'B' else (322, 290)
    for i, (title, meta, st, turn, gz) in enumerate(CARDS):
        if theme == 'B': cx = px + 24 + (i % 4) * (cw + 20); cy = py + 24 + (i // 4) * (ch + 14)
        else: cx = px + (i % 4) * (cw + 24); cy = py + (i // 4) * (ch + 24)
        if theme == 'A': rect(s, cx, cy + 3, cw, ch, K['ink'], 10, op=.16)
        rect(s, cx, cy, cw, ch, K['cream1'], 10, stroke=K['ink'], sw=1.5 if theme == 'A' else 1.2)
        if theme == 'A': grain(s, cx, cy, cw, ch, 10, .08, .04)
        tx, ty, tw, th = cx + 8, cy + 8, cw - 16, 186 if theme == 'B' else 190
        if st in ('done',):
            drawing(s, tx, ty, tw, th, BGS[i], 6, turn, gz, .4, hair=(i % 3 == 0))
            s.a(f'<circle cx="{tx+24}" cy="{ty+th-24}" r="15" fill="{K["cream1"]}" stroke="{K["ink"]}" stroke-width="1.5"/>'); ic(s, 'play', tx + 17, ty + th - 31, K['ink'], 14)
        elif st in ('running', 'queued'):
            drawing(s, tx, ty, tw, th, BGS[i], 6, turn, gz, .4, hair=(i % 3 == 0))
            rect(s, tx, ty, tw, th, K['cream1'], 6, op=.62)
            rect(s, tx + 10, ty + th - 40, tw - 20, 30, K['cream1'], 6, stroke=K['ink'], sw=1.2)
            stripe(s, tx + 22, ty + th - 35, tw - 44, 20, (K['org6'], K['org6']))
        else:
            rect(s, tx, ty, tw, th, K['red1'], 6)
            ic(s, 'alert', tx + tw / 2 - 18, ty + 62, K['red'], 36)
            T(s, tx + tw / 2, ty + 128, 'Generation failed', 15, 800, UI, K['red'], 'middle')
            T(s, tx + tw / 2, ty + 148, 'The GPU worker stopped.', 13, 500, UI, K['ink7'], 'middle')
        T(s, cx + 12, cy + (222 if theme == 'B' else 228), title if len(title) < 34 else title[:33] + '…', 15, 800)
        T(s, cx + 12, cy + (244 if theme == 'B' else 250), meta, 13, 500, UI, K['ink6'])
        chip(s, cx + cw - 12, cy + (244 if theme == 'B' else 252), st, 'end')
    return s

def screen_s4(theme):
    s = S(); page(s, theme, 232); topbar(s, 'New', theme)
    stepbar(s, 40, 118, 1)
    T(s, 40, 190, 'Describe the motion', 46, 600, FD)
    T(s, 40, 220, 'Cue turns your sentence into an ordered plan. Nothing is generated until you approve it.', 16, 500, UI, K['ink7'])
    top = 252 if theme == 'A' else 262
    # left: instruction
    panel(s, 40, top, 560, 536)
    T(s, 68, top + 50, 'Your instruction', 26, 600, FD)
    T(s, 68, top + 84, 'Describe the motion (optional)', 14, 800)
    rect(s, 68, top + 96, 504, 118, K['cream1'], 8, stroke=K['ink6'], sw=1.5)
    T(s, 84, top + 126, 'First move the eyes to the left, then', 16, 500, UI, K['ink'])
    T(s, 84, top + 152, 'slowly turn the head.', 16, 500, UI, K['ink'])
    s.a(f'<line x1="{84+172}" y1="{top+139}" x2="{84+172}" y2="{top+161}" stroke="{K["pur"]}" stroke-width="2"/>')
    T(s, 572, top + 232, '61 / 280', 13, 600, UI, K['ink6'], 'end')
    T(s, 68, top + 232, 'English only. Leave it empty to use the drawings alone.', 13, 500, UI, K['ink6'])
    T(s, 68, top + 268, 'Try an example', 13, 800)
    for i, ex in enumerate(['Eyes first, then head', 'Head turns while smiling']):
        xx = 68 + i * 196; rect(s, xx, top + 278, 184 if i == 0 else 200, 32, K['cream1'], 16, stroke=K['ink6'], sw=1.2)
        T(s, xx + 14, top + 299, ex, 13, 700, UI, K['ink'])
    button(s, 68, top + 330, 160, 44, 'Preview plan', 'secondary')
    s.a(f'<line x1="68" y1="{top+398}" x2="572" y2="{top+398}" stroke="{K["hair"]}" stroke-width="1.2"/>')
    T(s, 68, top + 430, 'Keyframes', 14, 800)
    drawing(s, 68, top + 442, 128, 80, K['paper'], 5, 0, 0, .3, scale=.62); rect(s, 68, top + 442, 128, 80, 'none', 5, stroke=K['ink'], sw=1.2)
    drawing(s, 262, top + 442, 128, 80, K['paper'], 5, -.9, -.9, .8, scale=.62); rect(s, 262, top + 442, 128, 80, 'none', 5, stroke=K['ink'], sw=1.2)
    s.a(f'<path d="M204 {top+482} H254 M248 {top+476} L254 {top+482} L248 {top+488}" fill="none" stroke="{K["ink"]}" stroke-width="1.8" stroke-linecap="round"/>')
    T(s, 68, top + 520 - 2, '', 1)
    T(s, 572, top + 488, 'Change drawings', 14, 800, UI, K['pur'], 'end', 'text-decoration="underline"')
    # right: cuesheet
    panel(s, 624, top, 776, 536)
    T(s, 652, top + 50, 'Motion plan', 26, 600, FD)
    chip_x = 1372
    rect(s, chip_x - 152, top + 28, 152, 28, K['pur1'], 14, stroke=K['pur'], sw=1.2)
    ic(s, 'check', chip_x - 142, top + 34, K['pur'], 16); T(s, chip_x - 120, top + 47, 'Plan is ready', 13, 700, UI, K['pur'])
    T(s, 652, top + 80, 'Order is shown, not exact timing. Chevrons show speed.', 14, 500, UI, K['ink7'])
    ev = [dict(region='Gaze', title='Look left', sub='Eyes · fast', speed=3, x=0, w=262),
          dict(region='Head', title='Turn left', sub='Head · slow', speed=1, x=306, w=262)]
    end = cuesheet(s, 652, top + 140, 720, ev)
    # approval
    T(s, 652, end + 10, 'In plain words: the eyes look left quickly, then the head turns left slowly.', 15, 600, UI, K['ink'])
    ay = end + 36
    rect(s, 652, ay, 720, 64, K['cream1'], 8, stroke=K['pur'], sw=2)
    rect(s, 672, ay + 20, 24, 24, K['pur'], 5); ic(s, 'check', 676, ay + 24, K['cream1'], 16)
    T(s, 710, ay + 31, 'This plan matches what I meant', 16, 800)
    T(s, 710, ay + 50, 'Change the sentence and preview again if it does not.', 13, 500, UI, K['ink6'])
    # actions
    button(s, 40, 812, 140, 48, 'Back', 'secondary')
    button(s, 1136, 812, 264, 50, 'Generate animation', 'primary')
    return s

def screen_s1(theme='A'):
    s = S(); rect(s, 0, 0, 1440, 900, K['gold']); grain(s, 0, 0, 1440, 900, 0, .12, .07)
    wordmark(s, 56, 84, 40)
    T(s, 56, 260, 'Two drawings in.', 74, 600, FD)
    T(s, 56, 340, 'One animation out.', 74, 600, FD)
    T(s, 56, 394, 'Upload a start and an end drawing, describe the motion in English,', 19, 500, UI, K['ink7'])
    T(s, 56, 422, 'and Cue draws the frames in between.', 19, 500, UI, K['ink7'])
    # painted swash
    sw = S()
    s.a(f'<g filter="url(#rough)"><rect x="56" y="520" width="768" height="300" rx="14" fill="{K["pur"]}"/></g>')
    random.seed(3)
    for i in range(46):
        yy = 540 + random.random() * 260; x0 = 80 + random.random() * 150; ln = 200 + random.random() * 400
        s.a(f'<line x1="{x0:.0f}" y1="{yy:.0f}" x2="{x0+ln:.0f}" y2="{yy:.0f}" stroke="{K["pur9"] if i%2 else K["pur7"]}" stroke-width="{1+random.random()*2:.1f}" opacity=".35"/>')
    turns = [(0, 0, .3), (-.2, -.4, .35), (-.45, -.7, .45), (-.7, -.9, .6), (-.9, -1, .8)]
    for i, (tn, gz, sm) in enumerate(turns):
        x0 = 88 + i * 144; end = i in (0, 4)
        drawing(s, x0, 566, 126, 174, K['paper'], 6, tn, gz, sm, scale=.74)
        rect(s, x0, 566, 126, 174, 'none', 6, stroke=K['org'] if end else K['cream2'], sw=4 if end else 1.5, op=None if end else .5)
        T(s, x0 + 63, 770, 'Your start' if i == 0 else 'Your end' if i == 4 else '', 14, 800, UI, K['cream1'], 'middle')
        if 0 < i < 4: T(s, x0 + 63, 770, f'Frame {i*3+1}' if False else 'Cue draws', 13, 600, UI, K['cream2'], 'middle', 'opacity=".75"')
    # form
    rect(s, 880, 0, 560, 900, K['cream2']); grain(s, 880, 0, 560, 900, 0, .09, .05)
    s.a(f'<line x1="880" y1="0" x2="880" y2="900" stroke="{K["ink"]}" stroke-width="1.5"/>')
    fx = 960; fw = 400
    T(s, fx, 214, 'Welcome back', 38, 600, FD)
    T(s, fx, 246, 'Log in to see your animations.', 16, 500, UI, K['ink7'])
    T(s, fx, 312, 'Log in', 16, 800); rect(s, fx, 322, 56, 3, K['pur'], 1.5)
    T(s, fx + 112, 312, 'Create account', 16, 600, UI, K['ink7'])
    s.a(f'<line x1="{fx}" y1="325" x2="{fx+fw}" y2="325" stroke="{K["hair"]}" stroke-width="1.2"/>'); rect(s, fx, 323, 56, 3, K['pur'], 1.5)
    T(s, fx, 372, 'Email', 14, 800); rect(s, fx, 384, fw, 46, K['cream1'], 8, stroke=K['ink6'], sw=1.5)
    T(s, fx + 14, 413, 'mira@studio.example', 16, 500)
    T(s, fx, 462, 'Password', 14, 800); rect(s, fx, 474, fw, 46, K['cream1'], 8, stroke=K['ink'], sw=2.5)
    s.a(f'<rect x="{fx-3}" y="471" width="{fw+6}" height="52" rx="10" fill="none" stroke="{K["cream1"]}" stroke-width="0"/>')
    T(s, fx + 14, 504, '••••••••••', 18, 700)
    T(s, fx + fw - 14, 503, 'Show', 14, 800, UI, K['pur'], 'end')
    T(s, fx, 546, 'Use at least 8 characters.', 13, 500, UI, K['ink6'])
    button(s, fx, 582, fw, 52, 'Log in', 'primary')
    T(s, fx + fw / 2, 676, 'New to Cue? Create an account', 15, 700, UI, K['pur'], 'middle', 'text-decoration="underline"')
    return s

def screen_s3(theme='A'):
    s = S(); page(s, theme, 232); topbar(s, 'New', theme); stepbar(s, 40, 118, 0)
    T(s, 40, 190, 'Add your two keyframes', 46, 600, FD)
    T(s, 40, 220, 'Cue animates from the start drawing to the end drawing. Keep both the same size.', 16, 500, UI, K['ink7'])
    panel(s, 40, 258, 1360, 520)
    for i in range(2):
        x = 72 + i * 668; w = 620
        if i == 0:
            rect(s, x, 286, 28, 28, K['pur'], 14); T(s, x + 14, 307, '1', 16, 800, FB, K['cream1'], 'middle')
            T(s, x + 40, 307, 'Start drawing', 20, 600, FD)
        else:
            rect(s, x, 286, 28, 28, K['org'], 3, stroke=K['ink'], sw=1.5); T(s, x + 14, 307, '2', 16, 800, FB, K['ink'], 'middle')
            T(s, x + 40, 307, 'End drawing', 20, 600, FD)
    # slot 1 filled
    drawing(s, 72, 326, 620, 340, K['paper'], 8, 0, 0, .3, scale=.58); rect(s, 72, 326, 620, 340, 'none', 8, stroke=K['ink'], sw=2)
    T(s, 72, 696, 'start-pose.png', 14, 800); T(s, 186, 696, '1.2 MB · 1024 × 640', 14, 500, UI, K['ink6'])
    button(s, 520, 678, 80, 36, 'Replace', 'secondary'); button(s, 608, 678, 84, 36, 'Remove', 'secondary')
    # slot 2 empty + error
    rect(s, 740, 326, 620, 340, K['cream1'], 8, stroke=K['ink6'], sw=2, dash='10 8')
    ic(s, 'img', 1030, 440, K['ink6'], 40)
    T(s, 1050, 520, 'Drop the end drawing here', 18, 800, UI, K['ink'], 'middle')
    T(s, 1050, 546, 'PNG or JPG, up to 10 MB, same size as the start drawing', 14, 500, UI, K['ink7'], 'middle')
    button(s, 974, 574, 152, 42, 'Browse files', 'secondary')
    rect(s, 740, 684, 620, 52, K['red1'], 8, stroke=K['red'], sw=1.5); rect(s, 740, 684, 6, 52, K['red'], 3)
    ic(s, 'alert', 762, 701, K['red'], 18)
    T(s, 792, 706, 'That file is 14.3 MB. Choose an image under 10 MB.', 15, 800, UI, K['red'])
    T(s, 792, 726, 'Nothing was uploaded. Your start drawing is kept.', 13, 500, UI, K['ink7'])
    # connector
    s.a(f'<path d="M700 496 H732 M726 490 L732 496 L726 502" fill="none" stroke="{K["ink"]}" stroke-width="1.8" stroke-linecap="round"/>')
    button(s, 40, 806, 170, 48, 'Back to Library', 'secondary')
    T(s, 1136 - 12, 826, 'Add both drawings to continue', 13, 600, UI, K['ink'], 'end')
    button(s, 1136, 806, 264, 50, 'Continue to motion', 'disabled')
    return s

def filmstrip(s, x, y, rows=2):
    cw, chh, pitch = 96, 62, 104
    for r in range(rows):
        yy = y + r * 140
        rect(s, x, yy, 8 * pitch + 8, 128, K['viewer'], 4)
        for c in range(8):
            cx0 = x + 8 + c * pitch
            for hx_ in (cx0 + 14, cx0 + cw - 24):
                for sy in (yy + 6, yy + 114):
                    rect(s, hx_, sy, 10, 8, K['gold3'], 2, op=.9)
        for c in range(8):
            n = r * 8 + c + 1; cx = x + 8 + c * pitch; cy = yy + 22
            if n in (1, 16):
                drawing(s, cx, cy, cw, chh, K['paper'], 2, 0 if n == 1 else -1.0, 0 if n == 1 else -1, .3 if n == 1 else .8, scale=.55)
                rect(s, cx, cy, cw, chh, 'none', 2, stroke=K['org'], sw=3)
            else:
                rect(s, cx, cy, cw, chh, K['cream2'], 2); rect(s, cx, cy, cw, chh, 'url(#hatch)', 2)
            T(s, cx + 2, cy + chh + 16, str(n), 11, 700, UI, K['cream2'])
            if n in (1, 16): T(s, cx + cw - 2, cy + chh + 16, 'Start' if n == 1 else 'End', 11, 800, UI, K['org'], 'end')

def screen_s5(theme='A'):
    s = S(); page(s, theme, 232); topbar(s, 'New', theme); stepbar(s, 40, 118, 2)
    T(s, 40, 190, 'Generating your animation', 46, 600, FD)
    T(s, 40, 220, 'You can leave this page. The job keeps running and stays in your library.', 16, 500, UI, K['ink7'])
    panel(s, 40, 258, 880, 520)
    chip(s, 68, 282, 'running')
    T(s, 190, 303, 'Elapsed', 14, 600, UI, K['ink6']); T(s, 256, 305, '02:14', 22, 600, FD)
    T(s, 68, 356, 'Drawing frames 2 to 15', 24, 600, FD)
    T(s, 68, 380, 'Frames 1 and 16 are your own drawings and are kept exactly as uploaded.', 14, 500, UI, K['ink7'])
    filmstrip(s, 68, 402)
    T(s, 68, 722, 'Cue does not know how long this will take, so no estimate is shown.', 14, 600, UI, K['ink'])
    T(s, 68, 746, 'Generation waits for a free GPU worker and then runs.', 14, 500, UI, K['ink7'])
    # side
    panel(s, 944, 258, 456, 520)
    T(s, 972, 308, 'Your plan', 24, 600, FD)
    for i, (t, sub) in enumerate([('Look left', 'Gaze · fast'), ('Turn left', 'Head · slow')]):
        yy = 332 + i * 56
        s.a(f'<circle cx="{988}" cy="{yy+22}" r="14" fill="{K["pur"]}"/>'); T(s, 988, yy + 28, str(i + 1), 17, 800, FB, K['cream1'], 'middle')
        T(s, 1014, yy + 20, t, 15, 800); T(s, 1014, yy + 40, sub, 13, 500, UI, K['ink7'])
    s.a(f'<line x1="972" y1="456" x2="1372" y2="456" stroke="{K["hair"]}" stroke-width="1.2"/>')
    T(s, 972, 488, 'Run details', 24, 600, FD)
    for i, (k, v) in enumerate([('Job', '#A83F'), ('Submitted', 'Oct 22, 13:42'), ('Model version', 'cue-m3 0.3.1'), ('Seed', '41827')]):
        T(s, 972, 520 + i * 28, k, 14, 500, UI, K['ink6']); T(s, 1372, 520 + i * 28, v, 14, 700, UI, K['ink'], 'end')
    button(s, 972, 668, 400, 46, 'Cancel generation', 'danger')
    button(s, 40, 806, 170, 48, 'Back to Library', 'secondary')
    return s

def screen_s6(theme='A'):
    s = S(); page(s, theme, 232); topbar(s, 'New', theme); stepbar(s, 40, 118, 3)
    T(s, 40, 190, 'Your animation is ready', 46, 600, FD)
    T(s, 40, 220, '“First move the eyes to the left, then slowly turn the head.”', 16, 500, UI, K['ink7'])
    panel(s, 40, 258, 908, 596)
    rect(s, 64, 282, 860, 480, K['viewer'], 8)
    drawing(s, 64 + 40, 282 + 0, 780, 480, K['paper'], 0, -.55, -.6, .55, scale=.52)
    s.a(f'<clipPath id="vc"><rect x="104" y="282" width="780" height="480"/></clipPath>')
    rect(s, 64, 282, 860, 480, 'none', 8, stroke=K['ink'], sw=1.5)
    # controls
    cy = 786
    s.a(f'<circle cx="92" cy="{cy+16}" r="22" fill="{K["pur"]}" stroke="{K["ink"]}" stroke-width="1.5"/>'); ic(s, 'play', 85, cy + 8, K['cream1'], 16)
    for i, k in enumerate(['prev', 'next', 'loop']):
        rect(s, 128 + i * 46, cy - 4, 40, 40, K['cream1'], 8, stroke=K['ink'], sw=1.2); ic(s, k, 140 + i * 46, cy + 8, K['ink'], 16)
    stripe(s, 290, cy - 4, 520, 36, (K['org6'], K['org6']))
    px = 290 + 520 / 16 * 8
    s.a(f'<rect x="{px+520/16*.2-2:.1f}" y="{cy-10}" width="{520/16*.46+4:.1f}" height="48" rx="3" fill="none" stroke="{K["pur"]}" stroke-width="3"/>')
    T(s, 830, cy + 22, 'Frame 9 of 16', 14, 700, UI, K['ink'])
    T(s, 290, cy + 52 - 6, 'Your start', 11, 800, UI, K['org7']); T(s, 810, cy + 46, 'Your end', 11, 800, UI, K['org7'], 'end')
    # side
    panel(s, 972, 258, 428, 596)
    button(s, 1000, 286, 372, 54, 'Download MP4', 'primary', 'down')
    T(s, 1000, 392, 'Details', 24, 600, FD)
    rows = [('Plan', '1 Look left, 2 Turn left'), ('Format', 'MP4 · 512 × 320'), ('Length', '16 frames, 3.2 s'), ('Created', 'Oct 22, 13:46'),
            ('Generated in', '3 min 52 s'), ('Model version', 'cue-m3 0.3.1'), ('Seed', '41827')]
    for i, (k, v) in enumerate(rows):
        T(s, 1000, 430 + i * 34, k, 14, 500, UI, K['ink6']); T(s, 1372, 430 + i * 34, v, 14, 700, UI, K['ink'], 'end')
    s.a(f'<line x1="1000" y1="690" x2="1372" y2="690" stroke="{K["hair"]}" stroke-width="1.2"/>')
    button(s, 1000, 714, 372, 46, 'Back to Library', 'secondary')
    button(s, 1000, 772, 372, 46, 'New animation', 'secondary', 'plus')
    return s

# ---------- tiles ----------
def tile(theme):
    s = S(); page(s, theme, 170)
    A = theme == 'A'
    wordmark(s, 56, 84, 40)
    T(s, 56, 126, 'Prismatic Paper' if A else 'Atelier Paper', 22, 800, FD)
    T(s, 56, 152, 'Gold-dominant shell, cream work surfaces, ink and pigment accents.' if A else 'Same colour family, more cream, gold used for the frame and header.', 14, 500, UI, K['ink7'])
    # palette
    sw = [('gold', K['gold'], 'Golden yellow'), ('cream', K['cream2'], 'Paper cream'), ('ink', K['ink'], 'Dark ink'), ('purple', K['pur'], 'Ink purple'), ('blue', K['blue'], 'Painted blue'), ('orange', K['org'], 'Pigment orange')]
    for i, (n, c, lab) in enumerate(sw):
        x = 56 + i * 104
        rect(s, x, 190, 94, 74, c, 8, stroke=K['ink'], sw=1.5)
        T(s, x, 286, lab, 12, 800, UI, K['ink']); T(s, x, 302, c, 12, 500, UI, K['ink7'])
    # ratio bar
    T(s, 56, 336, 'Surface balance in the app' , 13, 800)
    gw, cw = (0.60, 0.30) if A else (0.30, 0.60)
    x = 56
    for c, share, lab in [(K['gold'], gw, 'gold'), (K['cream2'], cw, 'cream'), (K['pur'], .05, ''), (K['blue'], .02, ''), (K['org'], .03, '')]:
        rect(s, x, 346, 600 * share, 26, c, 0, stroke=K['ink'], sw=1); x += 600 * share
    # surfaces
    T(s, 56, 410, 'Three surfaces', 13, 800)
    for i, (c, lab) in enumerate([(K['gold'], 'Golden paper (shell)'), (K['cream2'], 'Warm cream (panels)'), (K['paper'], 'Neutral canvas (artwork)')]):
        x = 56 + i * 208; rect(s, x, 422, 196, 110, c, 8, stroke=K['ink'], sw=1.5)
        if i < 2: grain(s, x, 422, 196, 110, 8, .12 if i == 0 else .09, .07)
        T(s, x, 554, lab, 12, 700, UI, K['ink'])
    drawing(s, 56 + 2 * 208 + 28, 432, 140, 90, K['paper'], 4, -.3, -.4, .5, scale=.5)
    # type
    T(s, 56, 606, 'Fraunces', 13, 800, UI, K['ink7'])
    T(s, 56, 652, 'Describe the motion', 38, 600, FD)
    T(s, 56, 682, 'Manrope for every control, label and metadata. Ğ ş ı İ ç ö ü', 15, 500)
    # components
    button(s, 56, 716, 190, 48, 'Generate animation', 'primary'); button(s, 262, 716, 110, 48, 'Back', 'secondary')
    chip(s, 388, 726, 'running'); chip(s, 506, 726, 'done'); chip(s, 612, 726, 'failed')
    stripe(s, 56, 796, 320, 24)
    T(s, 392, 814, 'Sixteen frames. First and last are yours.', 13, 600, UI, K['ink'])
    # mini preview of the S2 shell at right
    sc = .385; mx, my = 744, 64
    s.a(f'<g transform="translate({mx},{my}) scale({sc})">')
    s.a(f'<clipPath id="mini{theme}"><rect width="1440" height="900" rx="10"/></clipPath><g clip-path="url(#mini{theme})">')
    s.a(str(screen_s2(theme)))
    s.a('</g></g>')
    s.a(f'<rect x="{mx}" y="{my}" width="{1440*sc:.0f}" height="{900*sc:.0f}" rx="4" fill="none" stroke="{K["ink"]}" stroke-width="1.5"/>')
    sc2 = .385; my2 = my + 900 * sc + 24
    s.a(f'<g transform="translate({mx},{my2})  scale({sc2})"><clipPath id="mini4{theme}"><rect width="1440" height="900"/></clipPath><g clip-path="url(#mini4{theme})">')
    s.a(str(screen_s4(theme))); s.a('</g></g>')
    s.a(f'<rect x="{mx}" y="{my2}" width="{1440*sc2:.0f}" height="{900*sc2:.0f}" rx="4" fill="none" stroke="{K["ink"]}" stroke-width="1.5"/>')
    return s

def save(name, scr, outdir, w=1440, h=900):
    body = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}\n{scr}\n</svg>'
    open(f'{outdir}/{name}.svg', 'w').write(body)

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out + '/style-tiles', exist_ok=True); os.makedirs(out + '/previews', exist_ok=True)
    for th in 'AB':
        save(f'style-tile_{th}_' + ('prismatic-paper' if th == 'A' else 'atelier-paper'), tile(th), out + '/style-tiles', 1440, 900)
        save(f's2-dashboard_{th}', screen_s2(th), out + '/previews'); save(f's4-motion-plan_{th}', screen_s4(th), out + '/previews')
    save('s1-authentication_A', screen_s1(), out + '/previews'); save('s3-keyframes_A', screen_s3(), out + '/previews')
    save('s5-status_A', screen_s5(), out + '/previews'); save('s6-result_A', screen_s6(), out + '/previews')
