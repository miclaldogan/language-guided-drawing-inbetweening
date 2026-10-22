"""Mock keyframe artwork for previews only (ink line studies + one flat pigment shape, slightly misregistered)."""
import re
INK = '#241629'

def _g(s, x, y, w, h, flip, rot, body, size=100):
    body = re.sub(r'stroke-width="1\.5"( stroke-linecap="round" stroke-linejoin="round") stroke-width="([\d.]+)"', r'\1 stroke-width="\2"', body)
    body = re.sub(r'fill="([^"]+)" fill="none"', r'fill="\1"', body)
    k = min(w, h) / size * 0.92
    cx, cy = x + w / 2, y + h / 2
    fx = -1 if flip else 1
    s.a(f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot}) scale({k*fx:.3f},{k:.3f}) translate(-50,-50)">{body}</g>')

def study(s, kind, x, y, w, h, bg, pig, flip=False, rot=0, hair=0, op=1.0, clip=True, ink=INK, gaze=0):
    """kind: front | threeq | profile | shoulder"""
    c = f'a{abs(hash((kind, x, y, w, h, flip, rot, hair))) % 10**8}'
    s.a(f'<clipPath id="{c}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
    s.a(f'<g clip-path="url(#{c})" opacity="{op}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{bg}"/>')
    st = f'fill="none" stroke="{ink}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"'
    fi = f'fill="{ink}"'
    b = ''
    if kind == 'profile':
        b += f'<circle cx="43" cy="42" r="31" fill="{pig}"/>'
        b += f'<path d="M12 104 C16 88 30 82 46 82 C62 82 76 88 80 104 Z" fill="{pig}" opacity=".0"/>'
        if hair == 0:
            b += f'<path d="M53 13 C38 7 21 17 22 37 C23 49 28 55 25 68 C34 66 39 58 40 49 C41 41 46 36 51 31 C56 27 57 20 53 13 Z" {fi}/>'
        else:
            b += f'<path d="M54 14 C42 6 22 12 20 34 C19 46 24 56 30 60 C33 52 36 46 41 41 C47 35 54 31 56 24 Z" {fi}/><path d="M26 58 C22 66 24 74 30 78" {st} stroke-width="2.4"/>'
        b += f'<path d="M54 14 C57 22 58 27 57 31 C59 35 61 39 63 44 C63.5 46.5 62 47.5 60 47.5 L58 48 C59 50 59.5 51 59 52.5 C60 53 60 54 59 55 C60 56 59.5 57.5 58 58.5 C57.5 62.5 54.5 66 49 67 C46 67.5 43.5 66.5 41 65 C37 62 35.5 58 36 52" {st}/>'
        b += f'<path d="M49.5 37 Q52 35 55 36.5 M52 36.5 L54.5 38.8" {st} stroke-width="1.2"/>'
        b += f'<path d="M44 66 C45 73 46 80 46 92 M31 62 C31 72 30 82 29 94" {st}/>'
        b += f'<path d="M10 104 C14 90 28 84 46 84 C64 84 78 90 82 104" {st}/>'
    elif kind == 'front':
        b += f'<rect x="22" y="18" width="62" height="62" rx="2" fill="{pig}" transform="rotate(-4 50 50)"/>'
        b += f'<path d="M50 20 C36 20 31 33 32 47 C33 61 41 71 50 71 C59 71 67 61 68 47 C69 33 64 20 50 20 Z" fill="{bg}" {st}/>'
        if hair == 0:
            b += f'<path d="M30 52 C23 26 38 8 55 10 C72 12 78 30 70 54 C69 41 62 29 50 27 C42 30 36 38 34 56 C32 58 30.5 55 30 52 Z" {fi}/>'
        else:
            b += f'<path d="M31 56 C24 28 36 9 52 9 C70 9 78 28 69 56 C66 44 62 36 54 31 C46 28 38 34 34 46 Z" {fi}/><path d="M69 54 C73 64 72 74 66 82" {st} stroke-width="2.4"/>'
        b += f'<path d="M39 45 Q43.5 41.5 48.5 45 M52.5 45 Q57.5 41.5 62 45" {st}/>'
        b += f'<circle cx="{44+gaze}" cy="46.4" r="1.7" {fi}/><circle cx="{57.5+gaze}" cy="46.4" r="1.7" {fi}/>'
        b += f'<path d="M38.5 39.5 Q43.5 37 48.5 39 M52.5 39 Q57.5 37 62.5 39.5" {st} stroke-width="1.1"/>'
        b += f'<path d="M50.5 47 C50 53 49 56 47.5 58 C49 59.2 52 59.2 53.5 58" {st} stroke-width="1.2"/>'
        b += f'<path d="M44 64 Q50 61.5 56 64 Q50 67.5 44 64 Z" fill="{ink}" opacity=".85"/>'
        b += f'<path d="M43 70 L42 84 M57 70 L58 84" {st}/>'
        b += f'<path d="M8 104 C14 90 28 83 42 83 L58 83 C72 83 86 90 92 104" {st}/>'
    elif kind == 'threeq':
        b += f'<circle cx="52" cy="48" r="33" fill="{pig}"/>'
        b += f'<path d="M44 20 C32 22 29 35 31 48 C33 61 42 71 52 71 C61 71 68 62 70 50 C71 40 69 28 62 22" fill="{bg}" {st}/>'
        b += f'<path d="M29 54 C21 28 34 8 54 9 C73 10 79 30 70 56 C68 42 62 31 52 28 C44 30 38 38 36 52 Z" {fi}/>'
        b += f'<path d="M44 47 Q48.5 44 53 47 M60 46 Q64 43.5 68 46" {st}/>'
        b += f'<circle cx="{48.5+gaze}" cy="47.4" r="1.7" {fi}/><circle cx="{64+gaze}" cy="46.6" r="1.7" {fi}/>'
        b += f'<path d="M43 41 Q48 38.5 53 40.5 M60 40 Q64.5 38.5 69 41" {st} stroke-width="1.1"/>'
        b += f'<path d="M58.5 48 C60.5 53 62 56 63.5 58 C62 59.5 58.5 60 57 58.5" {st} stroke-width="1.2"/>'
        b += f'<path d="M50 65 Q57 62.5 63 64.5 Q57 68 50 65 Z" fill="{ink}" opacity=".85"/>'
        b += f'<path d="M45 70 L44 84 M62 69 C63 74 64 79 64 84" {st}/>'
        b += f'<path d="M8 104 C14 90 28 83 44 83 L64 83 C76 83 88 90 94 104" {st}/>'
    elif kind == 'shoulder':
        b += f'<path d="M6 104 C10 82 28 74 50 74 C72 74 90 82 94 104 Z" fill="{pig}"/>'
        b += f'<path d="M30 40 C28 18 46 8 60 14 C74 20 74 38 66 48 C62 54 58 56 58 62 L56 76 L40 76 C42 66 38 62 34 54 C32 50 31 46 30 40 Z" fill="{bg}" {st}/>'
        b += f'<path d="M26 44 C20 20 40 4 60 9 C78 14 80 36 70 46 C66 32 60 26 50 26 C40 28 34 38 36 56 C32 56 28 52 26 44 Z" {fi}/>'
        b += f'<circle cx="56" cy="9" r="8" {fi}/>'
        b += f'<path d="M30 46 C31 52 33 56 36 58 M33 48 C32 50 33 52 34 52" {st} stroke-width="1.2"/>'
        b += f'<path d="M6 104 C10 82 28 74 50 74 C72 74 90 82 94 104" {st}/>'
    _g(s, x, y, w, h, flip, rot, b)
    s.a('</g>')
