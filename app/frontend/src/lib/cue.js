/*
 * Cue v11 — shared drawing + planning engine for the mockup.
 *
 * 1. drawFigure(p)        : an ink line drawing of one character, from four motion parameters.
 * 2. parseInstruction(s)  : a small client-side stand-in for Cue's plan parser. It turns an English
 *                           sentence into ordered steps of region events, or a reasoned rejection.
 * 3. framesFromPlan(plan) : the 16 parameter sets (frame 1 = start drawing, frame 16 = end drawing).
 *
 * This is illustration for the mockup. The real system generates frames with a learned model;
 * nothing here is model output.
 */
"use strict";

  var FRAME_COUNT = 16;

  // The sample keyframe pair: start looks forward, neutral; end is turned left and smiling.
  var START = { gaze: 0, head: 0, smile: 0, hand: 0 };
  var END = { gaze: -1, head: -0.85, smile: 1, hand: 0 };

  var REGIONS = [
    { id: "gaze", label: "Gaze" },
    { id: "head", label: "Head" },
    { id: "smile", label: "Expression" },
    { id: "hand", label: "Hand" },
  ];

  /* ---------- 1. Drawing ---------- */

  function r(n) { return Math.round(n * 10) / 10; }

  function eyePath(x, y, w, open) {
    var h = 4.6 * open;
    return "M" + r(x - w) + " " + y +
      " Q" + r(x) + " " + r(y - h * 1.5) + " " + r(x + w) + " " + y +
      " Q" + r(x) + " " + r(y + h) + " " + r(x - w) + " " + y + "Z";
  }

  /**
   * p: { gaze -1..1, head -1..1 (negative = facing screen-left), smile 0..1, hand 0..1 }
   * opts: { stroke, paper, width, onion: p (previous frame, drawn first in the accent) }
   */
  function drawFigure(p, opts) {
    opts = opts || {};
    var ink = opts.stroke || "#1d1219";
    var paper = opts.paper || "#ffffff";
    var sw = opts.width || 2.4;
    var body = figureMarkup(p, ink, paper, sw, false);
    var onion = opts.onion ? figureMarkup(opts.onion, opts.onionColor || "#d8296c", "none", sw, true) : "";
    return '<svg viewBox="0 0 320 200" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="' +
      (opts.label || "Drawing") + '"><rect width="320" height="200" fill="' + paper + '"/>' +
      (onion ? '<g opacity="0.42">' + onion + "</g>" : "") + body + "</svg>";
  }

  function figureMarkup(p, ink, paper, sw, ghost) {
    var d = p.head, ad = Math.abs(d);
    var cx = 160 + d * 5, cy = 92;
    var rx = 45 - ad * 4, ry = 53;
    var fx = d * 21; // features slide toward the facing side
    var s = p.smile, g = p.gaze, h = p.hand;
    var fill = ghost ? "none" : paper;
    var o = [];
    var stroke = 'stroke="' + ink + '" stroke-width="' + sw + '" stroke-linecap="round" stroke-linejoin="round"';
    var line = 'fill="none" ' + stroke;
    var filled = 'fill="' + fill + '" ' + stroke;

    // shoulders and neck (the body barely turns)
    var nx = cx + d * 2;
    o.push('<path ' + line + ' d="M58 200 C70 176 104 168 ' + r(nx - 17) + ' 165 L' + r(nx - 15) + ' 140"/>');
    o.push('<path ' + line + ' d="M262 200 C250 176 216 168 ' + r(nx + 17) + ' 165 L' + r(nx + 15) + ' 140"/>');
    o.push('<path ' + line + ' d="M' + r(nx - 30) + ' 172 Q' + r(nx) + ' ' + r(182 + d * 2) + ' ' + r(nx + 30) + ' 172"/>');

    // ears: the near-side ear hides as the head turns toward it; the far ear stays on the outline
    [-1, 1].forEach(function (side) {
      var toward = Math.max(0, side * d);
      if (toward > 0.45) return;
      var ex = cx + side * (rx - 2.5);
      var w = 7 * (1 - toward * 1.6) + Math.max(0, -side * d) * 2;
      o.push('<path ' + filled + ' d="M' + r(ex) + ' 82 q' + r(side * w) + ' -3 ' + r(side * w) + ' 11 q0 11 ' + r(-side * w * 0.9) + ' 14"/>');
    });

    // head
    o.push('<ellipse cx="' + r(cx) + '" cy="' + cy + '" rx="' + r(rx) + '" ry="' + ry + '" fill="' + fill + '" stroke="' + ink + '" stroke-width="' + sw + '"/>');

    // hair: a cap line and a parting that travels with the turn
    var hp = cx + fx * 0.9;
    o.push('<path ' + line + ' d="M' + r(cx - rx + 3) + ' 78 C' + r(cx - rx + 8) + ' 46 ' + r(hp - 8) + ' 38 ' + r(hp) + ' 40 C' + r(hp + 14) + ' 41 ' + r(cx + rx - 4) + ' 52 ' + r(cx + rx - 2) + ' 76"/>');
    o.push('<path ' + line + ' d="M' + r(hp) + ' 40 Q' + r(hp - 12 - d * 6) + ' 54 ' + r(cx - rx + 10) + ' 66"/>');

    // brows lift a little as the smile arrives
    var browY = 75 - s * 2.5;
    [-1, 1].forEach(function (side) {
      var far = Math.max(0, side * d);
      var ex = cx + fx + side * 17 * (1 - far * 0.45);
      var w = 9 * (1 - far * 0.5);
      o.push('<path ' + line + ' d="M' + r(ex - w) + ' ' + r(browY + 1.5) + ' Q' + r(ex) + ' ' + r(browY - 2.5) + ' ' + r(ex + w) + ' ' + r(browY + 0.5) + '"/>');
    });

    // eyes and pupils
    var open = 1 - s * 0.28;
    [-1, 1].forEach(function (side) {
      var far = Math.max(0, side * d);
      var ex = cx + fx + side * 17 * (1 - far * 0.45);
      var w = 8.5 * (1 - far * 0.5);
      o.push('<path ' + filled + ' d="' + eyePath(ex, 88, w, open) + '"/>');
      var px = ex + g * w * 0.72 + d * 1.5;
      o.push('<circle cx="' + r(px) + '" cy="' + r(88 - 0.6) + '" r="' + r(2.9 * (1 - far * 0.2)) + '" fill="' + ink + '"/>');
    });

    // nose points the way the head faces
    var nnx = cx + fx * 1.18;
    o.push('<path ' + line + ' d="M' + r(nnx) + ' 93 L' + r(nnx + d * 8 - 1.5) + ' 109 Q' + r(nnx + d * 4) + ' 112 ' + r(nnx + 3 + d * 2) + ' 111"/>');

    // mouth: the control point drops as the smile grows
    var mx = cx + fx * 1.05, mw = 15 * (1 - ad * 0.3);
    var my = 126, curve = 1.5 + s * 9;
    o.push('<path ' + line + ' d="M' + r(mx - mw) + ' ' + r(my - s * 2) + ' Q' + r(mx) + ' ' + r(my + curve) + ' ' + r(mx + mw) + ' ' + r(my - s * 2.4) + '"/>');
    if (s > 0.45) {
      var k = (s - 0.45) / 0.55;
      o.push('<path ' + line + ' opacity="' + r(k) + '" d="M' + r(mx + mw + 3) + ' ' + r(my - 6) + ' q3 3 1 7"/>');
      o.push('<path ' + line + ' opacity="' + r(k) + '" d="M' + r(mx - mw - 3) + ' ' + r(my - 6) + ' q-3 3 -1 7"/>');
    }

    // hand rises from below the frame, beside the face: an open palm, four fingers and a thumb
    if (h > 0.02) {
      var hy = 214 - h * 92, hx = 240;
      var tilt = (1 - h) * 16;
      var fl = [12, 16, 15, 11];
      var dpath = "M" + (hx - 1) + " 216 L" + hx + " " + r(hy + 20) +
        " Q" + (hx - 9) + " " + r(hy + 12) + " " + (hx - 12) + " " + r(hy + 2) +
        " Q" + (hx - 11) + " " + r(hy - 3) + " " + (hx - 5) + " " + r(hy + 1) +
        " L" + hx + " " + r(hy + 8) + " L" + hx + " " + r(hy);
      for (var i = 0; i < 4; i++) {
        var x0 = hx + i * 7.4, top = hy - fl[i];
        dpath += " L" + r(x0) + " " + r(top + 3.7) + " Q" + r(x0 + 3.7) + " " + r(top - 3) + " " + r(x0 + 7.4) + " " + r(top + 3.7) +
          (i < 3 ? " L" + r(x0 + 7.4) + " " + r(hy + 1) : "");
      }
      dpath += " L" + r(hx + 30.6) + " 216";
      o.push('<g transform="rotate(' + r(tilt) + ' ' + (hx + 14) + ' 210)"><path ' + filled + ' d="' + dpath + '"/></g>');
    }
    return o.join("");
  }

  /* ---------- 2. Parsing ---------- */

  var RX = {
    gaze: /\b(eyes?|gaze|glances?|glancing|looks?|looking)\b/,
    head: /\b(head|turns?|turning|rotates?)\b/,
    smile: /\b(smil\w*|grin\w*|expression|happy|frown\w*)\b/,
    hand: /\b(hands?|wave[sd]?|waving|raises?|raising|lifts?|lifting|lowers?|lowering)\b/,
  };
  var SLOW = /\b(slow(ly)?|gentl[ey]|gradual(ly)?|softly)\b/;
  var FAST = /\b(quick(ly)?|fast|sudden(ly)?|snaps?|briskly)\b/;
  var NEGATION = /\b(don'?t|do not|never|without|no longer|stop)\b/;

  var EXAMPLES = [
    "First move the eyes to the left, then slowly turn the head, and begin smiling near the end.",
    "Turn the head and smile at the same time.",
    "Glance left quickly, then raise a hand while turning, then lower it and smile.",
  ];

  function actionFor(region, clause) {
    if (region === "gaze") return "Eyes left";
    if (region === "head") return "Head turns left";
    if (region === "smile") return /frown/.test(clause) ? "Frown" : "Smile";
    if (region === "hand") return /\blower/.test(clause) ? "Hand down" : "Hand up";
    return region;
  }

  /**
   * Returns { ok:true, steps:[{ events:[{region, action, speed}] }], added:[...] }
   *      or { ok:false, reason, suggestion }
   *      or { ok:true, empty:true } for an empty instruction (drawings-only run).
   */
  function parseInstruction(text) {
    var raw = (text || "").trim();
    if (!raw) return { ok: true, empty: true, steps: [], added: [] };
    var s = raw.toLowerCase();
    var suggestion = "First move the eyes to the left, then turn the head.";

    if (NEGATION.test(s)) {
      return { ok: false, reason: "Cue plans what moves, not what stays still. Leave a region out of the sentence instead of saying it doesn't move.", suggestion: suggestion };
    }
    if (/\bright\b/.test(s) && (RX.head.test(s) || RX.gaze.test(s))) {
      return { ok: false, reason: "The end drawing faces left, so a turn to the right can't reach it.", suggestion: suggestion };
    }
    if (/\bfrown/.test(s)) {
      return { ok: false, reason: "The end drawing is smiling, so a frown can't be the last expression.", suggestion: "Turn the head, then smile." };
    }

    // split into ordered clauses; "while / as / at the same time / together" keep events in one step
    var clauses = s.split(/\s*(?:,|;|\.|\bthen\b|\bafter that\b|\bfinally\b|\bafterwards\b|\band begin\b|\band start\b)\s*/).filter(Boolean);
    var steps = [];
    clauses.forEach(function (c) {
      var found = [];
      ["gaze", "hand", "head", "smile"].forEach(function (reg) {
        if (!RX[reg].test(c)) return;
        // "eyes turn" is a gaze move, not a head turn
        if (reg === "head" && !/\bhead\b/.test(c) && RX.gaze.test(c)) return;
        found.push(reg);
      });
      if (!found.length) return;
      var speed = SLOW.test(c) ? "slow" : FAST.test(c) ? "fast" : "normal";
      var events = found.map(function (reg) { return { region: reg, action: actionFor(reg, c), speed: speed }; });
      // events named in one clause already share a step; a clause that *opens* with
      // "while / as / meanwhile" joins the step before it ("turn the head, while smiling")
      var prev = steps[steps.length - 1];
      var together = /^(while|as|meanwhile|at the same time)\b/.test(c);
      if (prev && together) prev.events = prev.events.concat(events);
      else steps.push({ events: events });
    });

    if (!steps.length) {
      return { ok: false, reason: "Cue couldn't find a movement of the eyes, head, expression or hand in this sentence.", suggestion: suggestion };
    }
    if (steps.length > 4) {
      return { ok: false, reason: "This prototype plans up to four steps between two drawings; the sentence has " + steps.length + ".", suggestion: suggestion };
    }

    // the end drawing has the hand down: a raised hand must come back down
    var added = [];
    var handUp = -1, handDown = -1;
    steps.forEach(function (st, i) {
      st.events.forEach(function (e) {
        if (e.region === "hand" && e.action === "Hand up") handUp = i;
        if (e.region === "hand" && e.action === "Hand down") handDown = i;
      });
    });
    if (handDown >= 0 && handUp < 0) {
      return { ok: false, reason: "The start drawing already has the hand down, so there is nothing to lower.", suggestion: "Raise a hand while turning, then lower it." };
    }
    if (handUp >= 0 && handDown < handUp) {
      var target = steps[handUp + 1] || (steps.push({ events: [] }), steps[steps.length - 1]);
      target.events.push({ region: "hand", action: "Hand down", speed: "normal", added: true });
      added.push("Hand down — the end drawing has the hand down.");
    }

    // regions that differ between the drawings but were not mentioned still have to arrive
    ["gaze", "head", "smile"].forEach(function (reg) {
      var mentioned = steps.some(function (st) { return st.events.some(function (e) { return e.region === reg; }); });
      if (!mentioned) added.push(REGIONS.filter(function (x) { return x.id === reg; })[0].label + " follows the drawings across the whole clip.");
    });
    return { ok: true, steps: steps, added: added };
  }

  /* ---------- 3. Frames ---------- */

  var WEIGHT = { slow: 1.6, normal: 1, fast: 0.6 };
  function easeInOut(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function clamp01(t) { return Math.max(0, Math.min(1, t)); }

  function windows(plan) {
    var ws = plan.steps.map(function (st) {
      var w = 0.6;
      st.events.forEach(function (e) { w = Math.max(w, WEIGHT[e.speed] || 1); });
      return w;
    });
    var total = ws.reduce(function (a, b) { return a + b; }, 0);
    var at = 0, overlap = plan.steps.length > 1 ? 0.06 : 0;
    return ws.map(function (w) {
      var a = at, b = at + w / total;
      at = b;
      return [Math.max(0, a - overlap), Math.min(1, b + overlap)];
    });
  }

  function framesFromPlan(plan) {
    var frames = [];
    var win = plan && plan.ok && !plan.empty ? windows(plan) : [];
    for (var i = 0; i < FRAME_COUNT; i++) {
      var t = i / (FRAME_COUNT - 1);
      var p = { gaze: 0, head: 0, smile: 0, hand: 0 };
      ["gaze", "head", "smile"].forEach(function (reg) {
        var span = null;
        if (win.length) plan.steps.forEach(function (st, k) {
          st.events.forEach(function (e) { if (e.region === reg && !span) span = win[k]; });
        });
        var u = span ? clamp01((t - span[0]) / (span[1] - span[0])) : t;
        p[reg] = START[reg] + (END[reg] - START[reg]) * easeInOut(u);
      });
      if (win.length) {
        var up = null, down = null;
        plan.steps.forEach(function (st, k) {
          st.events.forEach(function (e) {
            if (e.region === "hand" && e.action === "Hand up" && !up) up = win[k];
            if (e.region === "hand" && e.action === "Hand down" && !down) down = win[k];
          });
        });
        if (up) {
          var a = easeInOut(clamp01((t - up[0]) / (up[1] - up[0])));
          var b = down ? easeInOut(clamp01((t - down[0]) / (down[1] - down[0]))) : 0;
          p.hand = a * (1 - b);
        }
      }
      if (i === 0) p = Object.assign({}, START);
      if (i === FRAME_COUNT - 1) p = Object.assign({}, END);
      frames.push(p);
    }
    return frames;
  }

export const Cue = {
  FRAME_COUNT: FRAME_COUNT,
  START: START,
  END: END,
  REGIONS: REGIONS,
  EXAMPLES: EXAMPLES,
  drawFigure: drawFigure,
  parseInstruction: parseInstruction,
  framesFromPlan: framesFromPlan,
};
export default Cue;
