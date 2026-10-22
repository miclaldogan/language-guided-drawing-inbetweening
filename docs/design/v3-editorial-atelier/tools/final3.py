import os, sys
from lib3 import *
from exp3 import save, exp

def ground(s, kind):
    if kind == 'gold':
        rect(s, 0, 0, 1440, 900, P['gold']); rect(s, 0, 0, 1440, 900, 'url(#reg)'); grain(s, 0, 0, 1440, 900, 0, .07, 0)
    else:
        rect(s, 0, 0, 1440, 900, P['paper']); rect(s, 0, 0, 1440, 900, 'url(#regp)'); grain(s, 0, 0, 1440, 900, 0, .05, 0)

def frame(s, ground_kind='gold', nav_kind='purple', sheet_h=732, sheet_fill=None):
    ground(s, ground_kind); nav(s, nav_kind)
    if ground_kind == 'paper': rect(s, 0, 64, 1440, 4, P['gold'])
    sheet(s, 40, 92, 1360, sheet_h, sheet_fill or (P['paper'] if ground_kind == 'gold' else P['paper2']))

def stepper(s, xr, y, cur):
    names = ['Keyframes', 'Motion', 'Generate', 'Result']
    widths = [22 + 8 + len(n) * 7.9 + 28 for n in names]; x = xr - sum(widths) + 28
    for i, n in enumerate(names):
        st = 'done' if i < cur else 'cur' if i == cur else 'todo'
        cx = x + 11
        if st == 'done': s.a(f'<circle cx="{cx}" cy="{y}" r="11" fill="{P["ink"]}"/>'); ic(s, 'check', cx - 6, y - 6, '#FFFAF0', 12)
        elif st == 'cur': s.a(f'<circle cx="{cx}" cy="{y}" r="11" fill="{P["pur"]}"/>'); T(s, cx, y + 4.5, str(i + 1), 12.5, 800, UI, '#FFFAF0', 'middle')
        else: s.a(f'<circle cx="{cx}" cy="{y}" r="10.5" fill="none" stroke="{P["line"]}" stroke-width="1.2"/>'); T(s, cx, y + 4.5, str(i + 1), 12.5, 700, UI, P['ink6'], 'middle')
        T(s, x + 30, y + 5, n, 13.5, 800 if st == 'cur' else 600, UI, P['ink'] if st != 'todo' else P['ink6'])
        x += widths[i]
        if i < 3: s.a(f'<line x1="{x-24}" y1="{y}" x2="{x-6}" y2="{y}" stroke="{P["line"]}" stroke-opacity=".6"/>')

def header(s, title, sub, cur=None, y0=92):
    T(s, 72, y0 + 56, title, 28, 800, UI, P['ink'], extra='letter-spacing="-0.4"')
    T(s, 72, y0 + 84, sub, 14.5, 500, UI, P['ink7'])
    if cur is not None: stepper(s, 1368, y0 + 50, cur)
    hair(s, 72, y0 + 112, 1368)

def tag(s, x, y, kind, label=None):
    if kind == 'start':
        s.a(f'<circle cx="{x+11}" cy="{y}" r="11" fill="{P["pur"]}"/>'); T(s, x + 11, y + 4.5, '1', 12.5, 800, UI, '#FFFAF0', 'middle')
    else:
        s.a(f'<circle cx="{x+11}" cy="{y}" r="10.5" fill="{P["gold"]}" stroke="{P["ink"]}" stroke-width="1.3"/>'); T(s, x + 11, y + 4.5, '2', 12.5, 800, UI, P['ink'], 'middle')
    if label: T(s, x + 30, y + 5.5, label, 16, 800)

def footer(s, y, back='Back', right=None, hint=None, rk='primary', rw=240):
    hair(s, 72, y, 1368)
    button(s, 72, y + 22, 118 if len(back) < 8 else 160, 46, back, 'secondary')
    if right:
        if hint: T(s, 1368 - rw - 20, y + 51, hint, 13, 600, UI, P['ink7'], 'end')
        button(s, 1368 - rw, y + 20, rw, 50, right, rk)

# ---------------- S1 ----------------
def s1():
    s = S(); ground(s, 'gold'); rect(s, 840, 0, 600, 900, P['paper']); grain(s, 840, 0, 600, 900, 0, .05, 0)
    s.a(f'<line x1="840" y1="0" x2="840" y2="900" stroke="{P["ink"]}" stroke-opacity=".18"/>')
    rect(s, 36, 170, 660, 250, P['gold']); grain(s, 36, 170, 660, 250, 0, .07, 0)  # keep the pattern out from under the hero text
    wordmark(s, 64, 100, 34, P['ink'], P['pur'])
    T(s, 64, 244, 'Two drawings in.', 54, 600, FD, P['ink'], extra='letter-spacing="-1"')
    T(s, 64, 306, 'One animation out.', 54, 600, FD, P['ink'], extra='letter-spacing="-1"')
    T(s, 64, 362, 'Upload a start and an end drawing, describe the motion in English,', 17, 500, UI, P['ink7'])
    T(s, 64, 388, 'and Cue draws the frames in between.', 17, 500, UI, P['ink7'])
    # purple study block, bleeds off the left and bottom edges
    rect(s, 0, 470, 840, 430, P['pur']); grain(s, 0, 470, 840, 430, 0, .06, 0)
    fr = [('front', 0, 0, '#FBE8D2', P['gold'], 'Start drawing'), ('threeq', 0, 0, '#E9EEF7', P['org'], 'Drawn by Cue'), ('profile', 0, 0, '#EFE4F3', P['gold'], 'End drawing')]
    for i, (k, h, f, bg, pg, lab) in enumerate(fr):
        x = 64 + i * 232; y = 520 + (0 if i != 1 else 24)
        rect(s, x, y + 8, 208, 236, '#000', 4, op=.28, extra='filter="url(#sh2)"')
        study(s, k, x, y, 208, 236, bg, pg, bool(f), 0, h)
        T(s, x, y + 266, lab, 13.5, 700, UI, '#FFFAF0')
    ticks(s, 64, 850, 712, 24, 16, '#FFFAF0', .6)
    # form
    fx = 928; fw = 424
    T(s, fx, 214, 'Welcome back', 28, 800, UI, P['ink'], extra='letter-spacing="-0.4"')
    T(s, fx, 242, 'Log in to see your animations.', 15, 500, UI, P['ink7'])
    T(s, fx, 304, 'Log in', 15, 800, UI, P['ink']); rect(s, fx, 316, 52, 3, P['pur'])
    T(s, fx + 100, 304, 'Create account', 15, 600, UI, P['ink6'])
    hair(s, fx, 318, fx + fw, .2)
    T(s, fx, 364, 'Email', 13.5, 800); rect(s, fx, 376, fw, 46, P['paper2'], 8, stroke=P['line'], sw=1)
    T(s, fx + 14, 405, 'mira@studio.example', 15.5, 500)
    T(s, fx, 452, 'Password', 13.5, 800)
    rect(s, fx - 3, 461, fw + 6, 52, P['paper'], 10); rect(s, fx - 1.5, 462.5, fw + 3, 49, 'none', 9, stroke=P['pur'], sw=2)
    rect(s, fx, 464, fw, 46, P['paper2'], 8)
    T(s, fx + 14, 495, '••••••••••', 17, 700); T(s, fx + fw - 14, 493, 'Show', 13.5, 800, UI, P['pur'], 'end')
    T(s, fx, 536, 'Use at least 8 characters.', 13, 500, UI, P['ink6'])
    button(s, fx, 572, fw, 50, 'Log in', 'primary')
    T(s, fx + fw / 2, 668, 'New to Cue? Create an account', 14.5, 700, UI, P['pur'], 'middle', 'text-decoration="underline"')
    return s

# ---------------- S2 ----------------
def s2(nav_kind='purple'):
    s = S(); frame(s, 'gold', nav_kind, 690)
    T(s, 72, 148, 'Your animations', 28, 800, UI, P['ink'], extra='letter-spacing="-0.4"')
    T(s, 72, 176, '8 animations, newest first', 14.5, 500, UI, P['ink7'])
    button(s, 1176, 128, 192, 46, 'New animation', 'primary', 'plus')
    hair(s, 72, 204, 1368)
    gallery(s, 72, 230, 1296, 4, 24, 28)
    return s

# ---------------- S3 ----------------
def s3():
    s = S(); frame(s, 'gold', 'purple', 730)
    header(s, 'Add your keyframes', 'Cue animates from the start drawing to the end drawing. Use two images of the same size.', 0)
    sx, ex, sw, sh = 72, 748, 620, 387; sy = 262
    tag(s, sx, sy - 22, 'start', 'Start drawing'); tag(s, ex, sy - 22, 'end', 'End drawing')
    T(s, sx + sw, sy - 16, 'Where the motion begins', 13, 500, UI, P['ink6'], 'end'); T(s, ex + sw, sy - 16, 'Where it ends', 13, 500, UI, P['ink6'], 'end')
    rect(s, sx, sy + 3, sw, sh, '#241629', 8, op=.10, extra='filter="url(#sh2)"')
    study(s, 'front', sx, sy, sw, sh, P['paper2'], P['gold'], False, 0, 1)
    rect(s, sx, sy, sw, sh, 'none', 8, stroke=P['ink'], sw=1, extra='stroke-opacity=".14"')
    T(s, sx, sy + sh + 32, 'start-pose.png', 14, 800); T(s, sx + 108, sy + sh + 32, '1.2 MB · 1024 × 640', 14, 500, UI, P['ink6'])
    button(s, sx + sw - 180, sy + sh + 12, 84, 36, 'Replace', 'secondary'); button(s, sx + sw - 88, sy + sh + 12, 88, 36, 'Remove', 'secondary')
    rect(s, ex, sy, sw, sh, '#F9F1E0', 8, stroke=P['line'], sw=1.5, dash='9 7')
    ic(s, 'img', ex + sw / 2 - 20, sy + 120, P['ink6'], 40)
    T(s, ex + sw / 2, sy + 202, 'Drop the end drawing here', 17, 800, UI, P['ink'], 'middle')
    T(s, ex + sw / 2, sy + 228, 'PNG or JPG, up to 10 MB, same size as the start drawing', 13.5, 500, UI, P['ink7'], 'middle')
    button(s, ex + sw / 2 - 74, sy + 252, 148, 42, 'Browse files', 'secondary')
    rect(s, ex, sy + sh + 14, sw, 52, P['red_t'], 8); rect(s, ex, sy + sh + 14, 4, 52, P['red'], 2)
    ic(s, 'alert', ex + 20, sy + sh + 32, P['red'], 17)
    T(s, ex + 46, sy + sh + 36, 'That file is 14.3 MB. Choose an image under 10 MB.', 14, 800, UI, P['red'])
    T(s, ex + 46, sy + sh + 55, 'Nothing was uploaded. Your start drawing is kept.', 12.5, 500, UI, P['ink7'])
    s.a(f'<path d="M700 {sy+sh/2} H740 M733 {sy+sh/2-6} L740 {sy+sh/2} L733 {sy+sh/2+6}" fill="none" stroke="{P["ink6"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    footer(s, 744 - 12, 'Back to Library', 'Continue to motion', 'Add both drawings to continue', 'disabled', 240)
    return s

# ---------------- S4 ----------------
def s4(nav_kind='purple', ground_kind='gold'):
    s = S(); frame(s, ground_kind, nav_kind, 784)
    header(s, 'Describe the motion', 'Cue turns your sentence into an ordered plan. Nothing is generated until you approve it.', 1)
    lx, lw = 72, 520; y0 = 228
    T(s, lx, y0 + 16, 'Instruction', 20, 800, UI, P['ink'], extra='letter-spacing="-0.2"')
    T(s, lx, y0 + 50, 'Describe the motion', 13.5, 800); T(s, lx + 150, y0 + 50, 'Optional, in English', 13, 500, UI, P['ink6'])
    rect(s, lx, y0 + 62, lw, 124, P['paper2'], 8, stroke=P['line'], sw=1)
    T(s, lx + 16, y0 + 94, 'First move the eyes to the left, then', 16, 500); T(s, lx + 16, y0 + 120, 'slowly turn the head.', 16, 500)
    rect(s, lx + 177, y0 + 106, 2, 20, P['pur'])
    T(s, lx + lw, y0 + 208, '61 / 280', 12.5, 600, UI, P['ink6'], 'end'); T(s, lx, y0 + 208, 'Leave empty to use the drawings alone.', 12.5, 500, UI, P['ink6'])
    T(s, lx, y0 + 248, 'Examples', 13, 800)
    for i, ex in enumerate(['Eyes first, then head', 'Head turns while smiling']):
        xx = lx + 76 + i * 182; w = 170 if i == 0 else 196
        if i == 1: xx = lx + 76 + 182
        rect(s, xx, y0 + 232, w, 30, P['paper3'], 15); T(s, xx + 14, y0 + 252, ex, 12.5, 700, UI, P['ink'])
    button(s, lx, y0 + 284, 150, 44, 'Preview plan', 'secondary')
    hair(s, lx, y0 + 356, lx + lw)
    T(s, lx, y0 + 388, 'Keyframes', 13.5, 800); T(s, lx + lw, y0 + 388, 'Change drawings', 13.5, 800, UI, P['pur'], 'end', 'text-decoration="underline"')
    for i, (k, f, bg, pg) in enumerate([('front', 0, P['paper2'], P['gold']), ('profile', 0, '#EFE4F3', P['gold'])]):
        x = lx + i * 200
        study(s, k, x, y0 + 404, 160, 100, bg, pg, bool(f), 0, 1 if i == 0 else 0)
        rect(s, x, y0 + 404, 160, 100, 'none', 4, stroke=P['ink'], sw=1, extra='stroke-opacity=".16"')
        tag(s, x + 8, y0 + 420, 'start' if i == 0 else 'end')
    s.a(f'<path d="M{lx+168} {y0+454} H{lx+192} M{lx+186} {y0+448} L{lx+192} {y0+454} L{lx+186} {y0+460}" fill="none" stroke="{P["ink6"]}" stroke-width="1.5" stroke-linecap="round"/>')
    # divider + plan
    s.a(f'<line x1="640" y1="{y0}" x2="640" y2="{y0+500}" stroke="{P["ink"]}" stroke-opacity=".12"/>')
    px = 684; pw = 684
    T(s, px, y0 + 16, 'Motion plan', 20, 800, UI, P['ink'], extra='letter-spacing="-0.2"')
    w = 150; rect(s, px + pw - w, y0 - 2, w, 26, P['pur_t'], 13); ic(s, 'check', px + pw - w + 10, y0 + 4, P['pur'], 14); T(s, px + pw - w + 31, y0 + 16.5, 'Ready to approve', 12.5, 700, UI, P['pur'])
    T(s, px, y0 + 44, 'Cue read your sentence as 2 events, in this order.', 14, 500, UI, P['ink7'])
    ev = [('Look left', 'Gaze · eyes', 3, 'Fast'), ('Turn left', 'Head', 1, 'Slow')]
    ry = y0 + 92
    cxr = px + 15
    s.a(f'<line x1="{cxr}" y1="{ry+15}" x2="{cxr}" y2="{ry+15+88}" stroke="{P["pur"]}" stroke-opacity=".38" stroke-width="1.5"/>')
    T(s, cxr + 22, ry + 63, 'then', 12.5, 600, UI, P['ink6'])
    for i, (ti, su, sp, wd) in enumerate(ev):
        yy = ry + i * 88
        s.a(f'<circle cx="{cxr}" cy="{yy+15}" r="15" fill="{P["paper"] if ground_kind=="gold" else P["paper2"]}" stroke="{P["pur"]}" stroke-width="1.6"/>')
        T(s, cxr, yy + 22, str(i + 1), 18, 600, FD, P['pur'], 'middle')
        T(s, px + 48, yy + 14, ti, 17, 800, UI, P['ink']); T(s, px + 48, yy + 35, su, 13.5, 500, UI, P['ink7'])
        for b in range(3):
            on = b < sp; hh = 7 + b * 5
            rect(s, px + pw - 92 + b * 10, yy + 26 - hh + 4, 6, hh, P['org_g'] if on else '#D8CBB4', 1.5)
        T(s, px + pw, yy + 22, wd, 13.5, 700, UI, P['ink'], 'end')
    T(s, px, y0 + 296, 'In plain words: the eyes look left quickly, then the head turns left slowly.', 14.5, 600, UI, P['ink'])
    rect(s, px, y0 + 318, 22, 22, P['pur'], 5); ic(s, 'check', px + 3, y0 + 321, '#FFFAF0', 16)
    T(s, px + 34, y0 + 335, 'This plan matches what I meant', 15, 800)
    T(s, px + 34, y0 + 356, 'Order and speed only. Exact frame timing is not part of the plan.', 12.5, 500, UI, P['ink6'])
    hair(s, px, y0 + 394, px + pw, .12)
    T(s, px, y0 + 424, 'Output', 13.5, 800); T(s, px + pw, y0 + 424, '16 frames', 13, 600, UI, P['ink6'], 'end')
    ticks(s, px, y0 + 444, pw, 24, 16, P['ink'], .5)
    T(s, px, y0 + 490, 'Your start drawing', 12.5, 700, UI, P['pur']); T(s, px + pw, y0 + 490, 'Your end drawing', 12.5, 700, UI, P['ink'], 'end')
    footer(s, 770, 'Back', 'Generate animation', None, 'primary', 244)
    return s

# ---------------- S5 ----------------
def s5(state='running'):
    s = S(); frame(s, 'paper', 'purple', 730)
    header(s, 'Generating your animation', 'You can leave this page. The job keeps running and stays in your library.', 2)
    # status track
    tx = 72; ty = 252
    labels = ['Queued', 'Processing', 'Completed']
    cur = {'running': 1, 'failed': 1}[state]
    for i, lb in enumerate(labels):
        x = tx + i * 220
        if i < cur: s.a(f'<circle cx="{x+12}" cy="{ty}" r="12" fill="{P["ink"]}"/>'); ic(s, 'check', x + 5, ty - 7, '#FFFAF0', 14)
        elif i == cur and state == 'running': s.a(f'<circle cx="{x+12}" cy="{ty}" r="12" fill="{P["blue_t"]}" stroke="{P["blue"]}" stroke-width="1.6" stroke-dasharray="4 3"/><circle cx="{x+12}" cy="{ty}" r="3.2" fill="{P["blue"]}"/>')
        elif i == cur and state == 'failed': s.a(f'<circle cx="{x+12}" cy="{ty}" r="12" fill="{P["red_t"]}" stroke="{P["red"]}" stroke-width="1.6"/>'); ic(s, 'alert', x + 5, ty - 7, P['red'], 14)
        else: s.a(f'<circle cx="{x+12}" cy="{ty}" r="11.5" fill="none" stroke="{P["line"]}" stroke-width="1.3"/>')
        fg = P['ink'] if i <= cur else P['ink6']
        T(s, x + 34, ty + 5.5, lb if not (i == cur and state == 'failed') else 'Failed', 15, 800 if i == cur else 600, UI, fg if not (i == cur and state == 'failed') else P['red'])
        if i < 2: s.a(f'<line x1="{x+128}" y1="{ty}" x2="{x+206}" y2="{ty}" stroke="{P["line"]}" stroke-opacity=".7" stroke-width="1.2"/>')
    T(s, 1368, ty - 2, 'Elapsed', 13, 500, UI, P['ink6'], 'end'); T(s, 1368, ty + 24, '02:14', 22, 700, UI, P['ink'], 'end', 'style="font-variant-numeric: tabular-nums"')
    msg = 'Cue is drawing frames 2 to 15. Frames 1 and 16 are your own drawings, kept exactly as uploaded.' if state == 'running' else 'Generation stopped at the GPU worker. Your drawings and plan are saved.'
    T(s, 72, ty + 62, msg, 15.5, 600, UI, P['ink'] if state == 'running' else P['red'])
    T(s, 72, ty + 88, 'No estimate is shown because Cue cannot tell how long this will take.' if state == 'running' else 'Go back to your library to start a new animation.', 13.5, 500, UI, P['ink7'])
    # film strip
    fy = 386; fw = 1296; pitch = fw / 16
    rect(s, 72, fy, fw, 108, P['viewer'], 6)
    for i in range(16):
        x = 72 + i * pitch
        for sy in (fy + 7, fy + 93): rect(s, x + pitch / 2 - 5, sy, 10, 7, '#3A2C44', 2)
        cx = x + 6; cw = pitch - 12; chh = cw * .625; cy = fy + 21
        if i == 0: study(s, 'front', cx, cy, cw, chh, P['paper2'], P['gold'], False, 0, 1); rect(s, cx - 2, cy - 2, cw + 4, chh + 4, 'none', 2, stroke=P['pur_t'], sw=2)
        elif i == 15: study(s, 'profile', cx, cy, cw, chh, '#EFE4F3', P['gold']); rect(s, cx - 2, cy - 2, cw + 4, chh + 4, 'none', 2, stroke=P['gold'], sw=2)
        else:
            rect(s, cx, cy, cw, chh, '#2A1E33', 2)
            if state == 'running': rect(s, cx, cy, cw, chh, 'none', 2, stroke='#5E4F68', sw=1, dash='3 3')
            else: rect(s, cx, cy, cw, chh, 'none', 2, stroke='#5E4F68', sw=1)
    for i in range(16):
        x = 72 + i * pitch
        T(s, x + pitch / 2, fy + 132, str(i + 1), 12, 600, UI, P['ink6'], 'middle', 'style="font-variant-numeric: tabular-nums"')
    T(s, 72, fy + 160, 'Your start drawing', 12.5, 700, UI, P['pur']); T(s, 72 + fw, fy + 160, 'Your end drawing', 12.5, 700, UI, P['ink'], 'end')
    # details
    dy = 590
    hair(s, 72, dy - 30, 1368, .12)
    T(s, 72, dy, 'Your plan', 16, 800)
    for i, (t, su) in enumerate([('Look left', 'Gaze · fast'), ('Turn left', 'Head · slow')]):
        s.a(f'<circle cx="87" cy="{dy+34+i*34}" r="11" fill="none" stroke="{P["pur"]}" stroke-width="1.4"/>'); T(s, 87, dy + 39 + i * 34, str(i + 1), 13, 600, FD, P['pur'], 'middle')
        T(s, 110, dy + 39 + i * 34, t, 14.5, 700); T(s, 210, dy + 39 + i * 34, su, 13.5, 500, UI, P['ink7'])
    T(s, 760, dy, 'Run details', 16, 800)
    for i, (k, v) in enumerate([('Job', '#A83F'), ('Submitted', 'Oct 22, 13:42'), ('Model version', 'cue-m3 0.3.1'), ('Seed', '41827')]):
        T(s, 760, dy + 30 + i * 26, k, 13.5, 500, UI, P['ink6']); T(s, 1060, dy + 30 + i * 26, v, 13.5, 700, UI, P['ink'])
    if state == 'running': button(s, 1210, 584, 158, 42, 'Cancel generation', 'danger')
    else: button(s, 1210, 584, 158, 42, 'New animation', 'primary')
    button(s, 72, 758, 160, 44, 'Back to Library', 'secondary')
    return s

# ---------------- S6 ----------------
def s6():
    s = S(); frame(s, 'paper', 'purple', 760)
    T(s, 72, 148, 'Your animation is ready', 28, 800, UI, P['ink'], extra='letter-spacing="-0.4"')
    T(s, 72, 174, '“First move the eyes to the left, then slowly turn the head.”', 14.5, 500, UI, P['ink7'])
    stepper(s, 1368, 142, 3)
    vx, vy, vw, vh = 72, 200, 880, 556
    rect(s, vx, vy, vw, vh, P['viewer'], 10)
    gx, gy, gw, gh = vx + 20, vy + 15, 840, 525
    study(s, 'threeq', gx, gy, gw, gh, P['paper2'], P['gold'], False, 0, 0, gaze=-2)
    s.a(f'<circle cx="{vx+vw/2}" cy="{vy+vh/2}" r="0" fill="none"/>')
    cy = vy + vh + 22
    s.a(f'<circle cx="{vx+22}" cy="{cy+20}" r="22" fill="{P["pur"]}"/>'); ic(s, 'play', vx + 15, cy + 12, '#FFFAF0', 16)
    for i, k in enumerate(['prev', 'next', 'loop']):
        rect(s, vx + 56 + i * 44, cy, 40, 40, 'none', 8); ic(s, k, vx + 68 + i * 44, cy + 12, P['ink'], 16)
    ticks(s, vx + 210, cy + 6, 520, 30, 16, P['ink'], .55)
    s.a(f'<rect x="{vx+210+520/16*7.5-6}" y="{cy}" width="12" height="42" rx="3" fill="none" stroke="{P["pur"]}" stroke-width="2.2"/>')
    T(s, vx + vw, cy + 25, 'Frame 8 of 16', 13.5, 700, UI, P['ink'], 'end', 'style="font-variant-numeric: tabular-nums"')
    rx = 992; rw = 376
    button(s, rx, 200, rw, 50, 'Download MP4', 'primary', 'down')
    T(s, rx, 292, 'Details', 16, 800)
    rows = [('Plan', '1 Look left, 2 Turn left'), ('Format', 'MP4 · 512 × 320'), ('Length', '16 frames · 3.2 s'), ('Created', 'Oct 22, 13:46'), ('Generated in', '3 min 52 s'), ('Model version', 'cue-m3 0.3.1'), ('Seed', '41827')]
    for i, (k, v) in enumerate(rows):
        yy = 324 + i * 38
        T(s, rx, yy, k, 13.5, 500, UI, P['ink6']); T(s, rx + rw, yy, v, 13.5, 700, UI, P['ink'], 'end')
        hair(s, rx, yy + 14, rx + rw, .10)
    button(s, rx, 612, 180, 44, 'Back to Library', 'secondary'); button(s, rx + 192, 612, 184, 44, 'New animation', 'ghost', 'plus')
    return s

# ---------------- style tile ----------------
def tile():
    s = S(); rect(s, 0, 0, 1440, 900, P['paper']); rect(s, 0, 0, 1440, 900, 'url(#regp)'); grain(s, 0, 0, 1440, 900, 0, .05, 0)
    nav(s, 'purple'); rect(s, 0, 64, 1440, 4, P['gold'])
    sheet(s, 40, 92, 1360, 780, P['paper2'], 14)
    T(s, 72, 140, 'Editorial Atelier', 28, 800, UI, extra='letter-spacing="-0.4"'); T(s, 72, 166, 'Warm paper for work, deep purple for structure, golden yellow for the brand ground.', 14.5, 500, UI, P['ink7'])
    # palette
    sw = [('Golden yellow', P['gold']), ('Deep purple', P['pur']), ('Warm paper', P['paper']), ('Elevated paper', P['paper2']), ('Dark ink', P['ink']), ('Painted blue', P['blue']), ('Pigment orange', P['org'])]
    for i, (n, c) in enumerate(sw):
        x = 72 + i * 110
        rect(s, x, 196, 100, 76, c, 8, stroke=P['ink'], sw=1, extra='stroke-opacity=".18"'); T(s, x, 292, n, 12, 700); T(s, x, 308, c, 12, 500, UI, P['ink6'])
    # distribution
    T(s, 72, 348, 'Distribution (visual guide)', 13, 800)
    x = 72; W = 760
    for c, sh, lab in [(P['paper'], .56, 'Paper 56%'), (P['gold'], .28, 'Gold 28%'), (P['pur'], .10, ''), (P['blue'], .03, ''), (P['org'], .03, '')]:
        rect(s, x, 360, W * sh, 24, c, 0, stroke=P['ink'], sw=1, extra='stroke-opacity=".18"'); x += W * sh
    T(s, 72, 404, 'Paper and work surfaces 56%  ·  Gold brand ground 28%  ·  Purple and pigment accents 16%', 12.5, 500, UI, P['ink6'])
    # type
    T(s, 72, 462, 'Typography', 13, 800)
    T(s, 72, 506, 'Two drawings in.', 40, 600, FD, extra='letter-spacing="-0.8"'); T(s, 72, 530, 'Fraunces for the login hero, wordmark and printed numerals', 13, 500, UI, P['ink6'])
    T(s, 72, 574, 'Your animations', 28, 800, UI, extra='letter-spacing="-0.4"'); T(s, 72, 598, 'Manrope for navigation, titles, forms, buttons and metadata', 13, 500, UI, P['ink6'])
    # components
    T(s, 72, 650, 'Components', 13, 800)
    button(s, 72, 668, 190, 46, 'Generate animation', 'primary'); button(s, 276, 668, 120, 46, 'Back', 'secondary'); button(s, 410, 668, 160, 46, 'Cancel', 'danger')
    chip(s, 72, 734, 'running'); chip(s, 200, 734, 'done'); chip(s, 290, 734, 'queued'); chip(s, 394, 734, 'failed')
    rect(s, 72, 782, 330, 44, P['paper2'], 8, stroke=P['line'], sw=1); T(s, 86, 810, 'Describe the motion', 14.5, 500, P['ink6'])
    ticks(s, 430, 790, 190, 26, 16)
    # border hierarchy + patterns right column
    T(s, 700, 462, 'Border hierarchy', 13, 800)
    rect(s, 700, 480, 190, 66, P['paper'], 8); T(s, 714, 508, 'No border', 13.5, 700); T(s, 714, 528, 'spacing and tone group it', 12, 500, UI, P['ink6'])
    rect(s, 910, 480, 190, 66, P['paper2'], 8, stroke=P['ink'], sw=1, extra='stroke-opacity=".14"'); T(s, 924, 508, 'Hairline', 13.5, 700); T(s, 924, 528, 'secondary surfaces', 12, 500, UI, P['ink6'])
    rect(s, 1120, 480, 192, 66, P['paper2'], 8, stroke=P['pur'], sw=2); T(s, 1134, 508, 'Strong outline', 13.5, 700); T(s, 1134, 528, 'selected, focus, input', 12, 500, UI, P['ink6'])
    T(s, 700, 600, 'Background pattern: registration marks', 13, 800)
    rect(s, 700, 618, 300, 130, P['gold']); rect(s, 700, 618, 300, 130, 'url(#reg)'); grain(s, 700, 618, 300, 130, 0, .07, 0)
    rect(s, 1012, 618, 300, 130, P['paper']); rect(s, 1012, 618, 300, 130, 'url(#regp)')
    T(s, 700, 770, 'On the gold ground, 20% ink', 12, 500, UI, P['ink6']); T(s, 1012, 770, 'On paper margins, 16% purple', 12, 500, UI, P['ink6'])
    T(s, 700, 806, 'Texture (paper grain) and pattern are separate layers. Neither is used under text, inputs or artwork.', 12.5, 500, UI, P['ink7'])
    return s

# ---------------- pattern samples ----------------
def patterns():
    s = S(); rect(s, 0, 0, 1440, 640, P['paper'])
    T(s, 48, 56, 'Background pattern candidates', 24, 800, UI); T(s, 48, 84, 'One primary language is selected: registration marks. The others are shown for comparison only.', 14, 500, UI, P['ink7'])
    defs = '''<defs>
<pattern id="pa" width="96" height="96" patternUnits="userSpaceOnUse"><g fill="none" stroke="#241629" stroke-width="1" opacity=".2"><circle cx="48" cy="48" r="5"/><path d="M48 37v22M37 48h22"/></g><g fill="#241629" opacity=".18"><circle cx="0" cy="0" r="1.1"/><circle cx="96" cy="0" r="1.1"/><circle cx="0" cy="96" r="1.1"/><circle cx="96" cy="96" r="1.1"/></g></pattern>
<pattern id="pb" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#241629" stroke-width=".6" opacity=".14"/></pattern>
<pattern id="pc" width="8" height="8" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#241629" opacity=".16"/></pattern>
<pattern id="pd" width="64" height="48" patternUnits="userSpaceOnUse"><g fill="#241629" opacity=".16"><rect x="4" y="22" width="2" height="20"/><rect x="10" y="26" width="2" height="16"/><rect x="16" y="26" width="2" height="16"/><rect x="22" y="26" width="2" height="16"/><rect x="28" y="26" width="2" height="16"/><rect x="34" y="26" width="2" height="16"/><rect x="40" y="26" width="2" height="16"/><rect x="46" y="22" width="2" height="20"/></g></pattern></defs>'''
    s.a(defs)
    for i, (pid, name, verdict) in enumerate([('pa', 'A  Registration marks', 'Selected. Sparse, precise, from animation paper. Reads as print, not decoration.'), ('pb', 'B  Drafting grid', 'Rejected as primary: competes with ruled lanes and thumbnails.'), ('pc', 'C  Halftone dots', 'Rejected: busy at 200% zoom and looks like a generic texture.'), ('pd', 'D  Frame-sequence rhythm', 'Rejected: repeats the sixteen-frame strip, which is a component, not a backdrop.')]):
        x = 48 + i * 346
        rect(s, x, 118, 322, 300, P['gold']); rect(s, x, 118, 322, 300, f'url(#{pid})'); rect(s, x, 118, 322, 300, 'none', 0, stroke=P['ink'], sw=1, extra='stroke-opacity=".2"')
        T(s, x, 448, name, 15, 800);
        words = verdict.split(' '); line = ''; yy = 472
        for w in words:
            if len(line + w) > 40: T(s, x, yy, line, 13, 500, UI, P['ink7']); line = w + ' '; yy += 18
            else: line += w + ' '
        T(s, x, yy, line, 13, 500, UI, P['ink7'])
    return s

if __name__ == '__main__':
    out = sys.argv[1]
    save('s1-authentication', s1(), out + '/previews'); save('s2-dashboard', s2(), out + '/previews')
    save('s3-keyframe-upload', s3(), out + '/previews'); save('s4-motion-plan', s4(), out + '/previews')
    save('s5-generation-status', s5('running'), out + '/previews'); save('s5-generation-status-failed', s5('failed'), out + '/previews')
    save('s6-result-preview', s6(), out + '/previews')
    save('style-tile', tile(), out + '/style-tile'); save('pattern-samples', patterns(), out + '/patterns', 1440, 640)
    save('navbar-B-cream_s4', s4('cream'), out + '/navbar-comparison'); save('navbar-A-purple_s4', s4('purple'), out + '/navbar-comparison')
    for n in (1, 2, 3): save(f'experiment-{n}', exp(n), out + '/experiments')
