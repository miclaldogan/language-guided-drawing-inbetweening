import os, sys
from lib3 import *

def save(name, body, outdir, w=1440, h=900):
    os.makedirs(outdir, exist_ok=True)
    open(f'{outdir}/{name}.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}\n{body}\n</svg>')

def exp(n):
    s = S()
    if n == 1:  # purple nav, paper sheet on patterned gold ground
        rect(s, 0, 0, 1440, 900, P['gold']); rect(s, 0, 0, 1440, 900, 'url(#reg)'); grain(s, 0, 0, 1440, 900, 0, .07, 0)
        nav(s, 'purple')
        sheet(s, 40, 92, 1360, 700, P['paper'])
        page_title(s, 72, 148, 'Your animations', '8 animations, newest first')
        button(s, 1176, 124, 192, 44, 'New animation', 'primary', 'plus')
        hair(s, 72, 198, 1368)
        gallery(s, 72, 224, 1296, 4, 24, 28)
    elif n == 2:  # cream nav, paper page, yellow accents
        rect(s, 0, 0, 1440, 900, P['paper']); rect(s, 0, 64, 1440, 836, 'url(#regp)'); grain(s, 0, 0, 1440, 900, 0, .05, 0)
        nav(s, 'cream')
        rect(s, 56, 104, 6, 62, P['gold'])
        page_title(s, 78, 128, 'Your animations', '8 animations, newest first')
        button(s, 1192, 112, 192, 44, 'New animation', 'gold', 'plus')
        hair(s, 56, 188, 1384)
        rect(s, 56, 206, 1328, 650, P['paper'], 0, op=1)  # quiet area under gallery (no pattern)
        gallery(s, 56, 224, 1328, 4, 24, 28)
    else:  # purple nav, paper page, restrained gold band
        rect(s, 0, 0, 1440, 900, P['paper']); rect(s, 0, 64, 1440, 836, 'url(#regp)'); grain(s, 0, 0, 1440, 900, 0, .05, 0)
        nav(s, 'purple')
        rect(s, 0, 64, 1440, 112, P['gold']); rect(s, 0, 64, 1440, 112, 'url(#reg)'); grain(s, 0, 64, 1440, 112, 0, .06, 0)
        page_title(s, 56, 114, 'Your animations', '8 animations, newest first', P['ink'], P['ink7'])
        button(s, 1192, 100, 192, 44, 'New animation', 'primary', 'plus')
        rect(s, 36, 196, 1368, 680, P['paper'], 0)
        gallery(s, 56, 214, 1328, 4, 24, 28)
    return s

if __name__ == '__main__':
    out = sys.argv[1]
    for n in (1, 2, 3): save(f'experiment-{n}', exp(n), out)
