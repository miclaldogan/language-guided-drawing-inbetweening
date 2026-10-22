import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen import S, rect, grain, ic, uid
from art3 import study

P = dict(
    gold='#FFB509', gold_t='#FFEFC2', gold_d='#E09A00',
    pur='#431452', pur7='#5A2370', pur9='#2E0C3A', pur_t='#EFE4F3',
    paper='#F5EBD8', paper2='#FFFAF0', paper3='#EBDFC8',
    ink='#241629', ink7='#4D3D55', ink6='#6E5F76', line='#85748A',
    blue='#23437C', blue_t='#E1E9F4', org='#ED782A', org_t='#B4440F', org_g='#C4531A', org_bg='#FBE2CC',
    red='#A1413C', red_t='#F8E0DC', grn='#2F6B3B', grn_t='#DFEBD9', warn='#7A4F00', warn_t='#FFEFC2',
    viewer='#17101C',
)
FD, FB, UI = 'Fraunces Display', 'Fraunces Display Bold', 'Manrope'

DEFS = f'''<defs>
<filter id="grain" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7"/>
<feColorMatrix type="matrix" values="0 0 0 0 0.14  0 0 0 0 0.086  0 0 0 0 0.16  0 0 0 1.3 -0.5"/></filter>
<filter id="fiber" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.30" numOctaves="2" seed="21"/>
<feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.30  0 0 0 0 0.20  0 0 0 1.6 -0.7"/></filter>
<filter id="sh" x="-10%" y="-10%" width="120%" height="130%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="sh2" x="-10%" y="-10%" width="120%" height="140%"><feGaussianBlur stdDeviation="3.5"/></filter>
<pattern id="reg" width="96" height="96" patternUnits="userSpaceOnUse">
<g fill="none" stroke="#241629" stroke-width="1" opacity=".20"><circle cx="48" cy="48" r="5"/><path d="M48 37v22M37 48h22"/></g>
<g fill="#241629" opacity=".18"><circle cx="0" cy="0" r="1.1"/><circle cx="96" cy="0" r="1.1"/><circle cx="0" cy="96" r="1.1"/><circle cx="96" cy="96" r="1.1"/></g></pattern>
<pattern id="regp" width="96" height="96" patternUnits="userSpaceOnUse">
<g fill="none" stroke="#431452" stroke-width="1" opacity=".16"><circle cx="48" cy="48" r="5"/><path d="M48 37v22M37 48h22"/></g>
<g fill="#431452" opacity=".14"><circle cx="0" cy="0" r="1.1"/><circle cx="96" cy="0" r="1.1"/><circle cx="0" cy="96" r="1.1"/><circle cx="96" cy="96" r="1.1"/></g></pattern>
<pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#6E5F76" stroke-width="1" opacity=".28"/></pattern>
</defs>'''

def T(s, x, y, txt, size=14, w=500, fam=UI, fill=None, anchor='start', extra=''):
    fill = fill or P['ink']
    txt = txt.replace('&', '&amp;')
    s.a(f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{txt}</text>')

def sheet(s, x, y, w, h, fill=None, rx=14, shadow=True, border=True, tex=True):
    fill = fill or P['paper2']
    if shadow:
        s.a(f'<rect x="{x+4}" y="{y+14}" width="{w-8}" height="{h-6}" rx="{rx}" fill="#241629" opacity=".20" filter="url(#sh)"/>')
    rect(s, x, y, w, h, fill, rx, stroke='#241629' if border else None, sw=1 if border else 0, extra='stroke-opacity=".10"')
    if tex: grain(s, x, y, w, h, rx, .05, .0)

def hair(s, x1, y, x2, op=.14, col=None):
    s.a(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col or P["ink"]}" stroke-width="1" opacity="{op}"/>')

def wordmark(s, x, y, size=26, col='#FFFAF0', ends=None, ink_end='none'):
    ends = ends or P['gold']
    for i in range(7):
        e = i in (0, 6); h = size * (.74 if e else .5)
        rect(s, x + i * size * .17, y - h, size * .085, h, ends if e else col, size * .02, op=None if e else .85)
    T(s, x + size * 1.34, y, 'Cue', size * 1.12, 800, FB, col)

def nav(s, kind='purple'):
    if kind == 'purple':
        rect(s, 0, 0, 1440, 64, P['pur']); grain(s, 0, 0, 1440, 64, 0, .06, 0)
        wordmark(s, 40, 41, 24, '#FFFAF0', P['gold'])
        s.a(f'<line x1="196" y1="18" x2="196" y2="46" stroke="#FFFAF0" stroke-opacity=".18"/>')
        T(s, 220, 38, 'Library', 15, 700, UI, '#FFFAF0'); rect(s, 220, 58, 52, 3, P['gold'])
        s.a(f'<line x1="1176" y1="18" x2="1176" y2="46" stroke="#FFFAF0" stroke-opacity=".18"/>')
        s.a(f'<circle cx="1210" cy="32" r="15" fill="{P["gold"]}"/>'); T(s, 1210, 38, 'M', 14, 800, UI, P['ink'], 'middle')
        T(s, 1234, 37, 'mira@studio.example', 13.5, 600, UI, '#FFFAF0'); ic(s, 'chev', 1380, 24, '#FFFAF0', 16)
    else:
        rect(s, 0, 0, 1440, 64, P['paper2']); s.a(f'<line x1="0" y1="64" x2="1440" y2="64" stroke="{P["ink"]}" stroke-opacity=".16"/>')
        wordmark(s, 40, 41, 24, P['ink'], P['pur'])
        s.a(f'<line x1="196" y1="18" x2="196" y2="46" stroke="{P["ink"]}" stroke-opacity=".16"/>')
        T(s, 220, 38, 'Library', 15, 700, UI, P['ink']); rect(s, 220, 58, 52, 3, P['pur'])
        s.a(f'<line x1="1176" y1="18" x2="1176" y2="46" stroke="{P["ink"]}" stroke-opacity=".16"/>')
        s.a(f'<circle cx="1210" cy="32" r="15" fill="{P["pur"]}"/>'); T(s, 1210, 38, 'M', 14, 800, UI, '#FFFAF0', 'middle')
        T(s, 1234, 37, 'mira@studio.example', 13.5, 600, UI, P['ink']); ic(s, 'chev', 1380, 24, P['ink'], 16)

CH = dict(done=('Done', 'check', P['grn_t'], P['grn']), running=('Processing', 'run', P['blue_t'], P['blue']),
          queued=('Queued', 'clock', P['paper3'], P['ink7']), failed=('Failed', 'alert', P['red_t'], P['red']),
          cancelled=('Cancelled', 'alert', P['paper3'], P['ink7']))
def chip(s, x, y, kind, anchor='start', h=26):
    lab, icon, bg, fg = CH[kind]; w = 38 + len(lab) * 7.6
    if anchor == 'end': x -= w
    rect(s, x, y, w, h, bg, h / 2)
    ic(s, icon, x + 10, y + (h - 14) / 2, fg, 14)
    T(s, x + 29, y + h / 2 + 4.5, lab, 12.5, 700, UI, fg)
    return w

def button(s, x, y, w, h, label, kind='primary', icon=None):
    if kind == 'primary': rect(s, x, y, w, h, P['pur'], 8); fg = '#FFFAF0'
    elif kind == 'gold': rect(s, x, y, w, h, P['gold'], 8); fg = P['ink']
    elif kind == 'secondary': rect(s, x, y, w, h, P['paper2'], 8, stroke=P['line'], sw=1); fg = P['ink']
    elif kind == 'ghost': fg = P['pur']
    elif kind == 'danger': rect(s, x, y, w, h, P['paper2'], 8, stroke=P['red'], sw=1); fg = P['red']
    elif kind == 'disabled': rect(s, x, y, w, h, P['paper3'], 8); fg = P['ink6']
    tw = len(label) * 8.3 + (22 if icon else 0); sx = x + (w - tw) / 2
    if icon: ic(s, icon, sx, y + h / 2 - 8, fg, 16)
    T(s, sx + (22 if icon else 0), y + h / 2 + 5.2, label, 14.5, 700, UI, fg)

def ticks(s, x, y, w, h=18, n=16, tick=None, op=.55):
    pitch = w / n; tick = tick or P['ink']; tw = max(4, min(6, h / 4))
    for i in range(n):
        e = i in (0, n - 1); th = h if e else h * .62; xx = x + i * pitch + (pitch - tw) / 2
        if i == 0: rect(s, xx, y + h - th, tw, th, P['pur'] if tick == P['ink'] else '#FFFAF0', 1.2)
        elif i == n - 1: rect(s, xx, y + h - th, tw, th, P['gold'], 1.2, stroke=P['ink'] if tick == P['ink'] else None, sw=1)
        else: rect(s, xx, y + h - th, tw, th, tick, 1.2, op=op)

STUDIES = [  # (kind, hair, flip, bg, pigment) for dashboard variety
    ('profile', 0, 0, '#FBE8D2', P['gold']), ('front', 1, 0, '#E9EEF7', P['org']), ('threeq', 0, 0, '#EFE4F3', P['blue']),
    ('profile', 1, 1, '#FFFAF0', P['pur']), ('front', 0, 0, '#FBE8D2', P['blue']), ('threeq', 0, 1, '#E9EEF7', P['gold']),
    ('profile', 0, 1, '#EFE4F3', P['org']), ('front', 1, 1, '#FFFAF0', P['gold'])]
ITEMS = [
    ('Move the eyes left, then turn the head', 'Oct 22, 13:42', 'running'),
    ('Nod slowly, then start smiling', 'Oct 22, 13:20', 'queued'),
    ('Turn the head, then move the eyes', 'Oct 21, 17:08', 'done'),
    ('Raise the hand while turning', 'Oct 21, 16:51', 'done'),
    ('Blink twice, then tilt the head', 'Oct 20, 22:15', 'done'),
    ('Look down, then look up quickly', 'Oct 19, 11:02', 'failed'),
    ('Smile near the end of the turn', 'Oct 19, 09:30', 'done'),
    ('Slow head turn to the left', 'Oct 18, 09:47', 'done'),
]

def gallery(s, x, y, w, cols=4, gap=24, rows_gap=30, items=ITEMS, th_ratio=.625):
    tw = (w - gap * (cols - 1)) / cols; th = tw * th_ratio; ph = th + 66
    for i, (title, meta, st) in enumerate(items):
        cx = x + (i % cols) * (tw + gap); cy = y + (i // cols) * (ph + rows_gap)
        k, hr, fl, bg, pg = STUDIES[i % len(STUDIES)]
        rect(s, cx, cy + 3, tw, th, '#241629', 6, op=.14, extra='filter="url(#sh2)"')
        if st in ('done',):
            study(s, k, cx, cy, tw, th, bg, pg, bool(fl), 0, hr)
            rect(s, cx + tw - 54, cy + th - 30, 44, 20, P['ink'], 4, op=.86); T(s, cx + tw - 32, cy + th - 16, '3.2 s', 11.5, 700, UI, '#FFFAF0', 'middle')
        elif st in ('running', 'queued'):
            study(s, k, cx, cy, tw, th, bg, pg, bool(fl), 0, hr, op=.45)
            rect(s, cx + 12, cy + th - 34, tw - 24, 22, P['paper2'], 4, op=.92); ticks(s, cx + 22, cy + th - 31, tw - 44, 16)
        else:
            rect(s, cx, cy, tw, th, P['paper3'], 6); rect(s, cx, cy, tw, th, 'url(#hatch)', 6)
            ic(s, 'alert', cx + tw / 2 - 14, cy + th / 2 - 22, P['red'], 28)
            T(s, cx + tw / 2, cy + th / 2 + 28, 'Generation failed', 13.5, 700, UI, P['red'], 'middle')
        T(s, cx, cy + th + 24, title if len(title) < 36 else title[:35] + '…', 14.5, 700)
        T(s, cx, cy + th + 45, meta, 12.5, 500, UI, P['ink6'])
        chip(s, cx + tw, cy + th + 32, st, 'end', 24)
    return th

def page_title(s, x, y, title, sub, fill=None, subfill=None):
    T(s, x, y, title, 30, 800, UI, fill or P['ink'], extra='letter-spacing="-0.4"')
    T(s, x, y + 28, sub, 15, 500, UI, subfill or P['ink7'])
