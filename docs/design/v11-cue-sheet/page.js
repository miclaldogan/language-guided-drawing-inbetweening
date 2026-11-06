/* Cue v11 — page behaviour. Everything renders without this file except the live parts. */
(function () {
  "use strict";
  var C = window.Cue;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var REGION_LABEL = { gaze: "Gaze", head: "Head", smile: "Expression", hand: "Hand" };
  var SPEED_LABEL = { slow: "slowly", normal: "normal speed", fast: "quickly" };

  function colWord(i, n) {
    if (n === 1) return "Together";
    if (i === 0) return "First";
    if (i === n - 1) return "Last";
    return "Then";
  }

  /* ================= the live cue sheet ================= */
  function Playground(root) {
    this.root = root;
    this.text = $("#cs-text", root);
    this.grid = $("[data-plan]", root);
    this.list = $("[data-plan-list]", root);
    this.added = $("[data-plan-added]", root);
    this.note = $("[data-plan-note]", root);
    this.stripEl = $("[data-strip]", root);
    this.stage = $("[data-stage]", root);
    this.layerA = $('[data-layer="a"]', root);
    this.layerB = $('[data-layer="b"]', root);
    this.tag = $("[data-stage-tag]", root);
    this.count = $("[data-count]", root);
    this.playBtn = $('[data-act="play"]', root);
    this.onion = $("[data-onion]", root);
    this.cur = 0;
    this.frames = [];
    this.lastKey = "";
    this.timer = null;
    this.idle = null;
    this.bind();
    this.update(true);
    this.startIdle();
  }

  Playground.prototype.bind = function () {
    var self = this, t = null;
    this.text.addEventListener("input", function () {
      self.grid.classList.add("is-stale");
      self.note.textContent = "Reading your instruction…";
      $$(".chip", self.root).forEach(function (c) { c.setAttribute("aria-pressed", "false"); });
      clearTimeout(t);
      t = setTimeout(function () { self.update(); }, 380);
    });
    $$(".chip", this.root).forEach(function (chip) {
      chip.setAttribute("aria-pressed", "false");
      chip.addEventListener("click", function () {
        var k = chip.getAttribute("data-example");
        self.text.value = k === "reject" ? "Turn the head to the right and smile." : C.EXAMPLES[+k];
        $$(".chip", self.root).forEach(function (c) { c.setAttribute("aria-pressed", String(c === chip)); });
        self.update();
      });
    });
    this.root.addEventListener("click", function (e) {
      var b = e.target.closest("[data-act]");
      if (!b) return;
      var a = b.getAttribute("data-act");
      if (a === "play") self.togglePlay();
      if (a === "prev") { self.pause(); self.show(self.cur - 1); }
      if (a === "next") { self.pause(); self.show(self.cur + 1); }
    });
    this.onion.addEventListener("change", function () { self.show(self.cur, true); });
    this.stripEl.addEventListener("click", function (e) {
      var f = e.target.closest(".fr");
      if (!f) return;
      self.pause();
      self.show(+f.getAttribute("data-i"));
    });
    // arrow keys step frames when focus is on the strip or the transport (never while typing)
    this.root.addEventListener("keydown", function (e) {
      if (e.target === self.text) return;
      if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
        if (!e.target.closest(".strip, .transport")) return;
        e.preventDefault();
        self.pause();
        self.show(self.cur + (e.key === "ArrowLeft" ? -1 : 1));
        var btn = self.stripEl.children[self.cur];
        if (btn && e.target.closest(".strip")) btn.focus();
      }
    });
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) { self.pause(); self.stopIdle(); }
    });
  };

  Playground.prototype.update = function (first) {
    var plan = C.parseInstruction(this.text.value);
    var key = JSON.stringify(plan);
    this.grid.classList.remove("is-stale");
    this.note.textContent = plan.ok ? (plan.empty ? "No instruction: a drawings-only run" : "Order shown, not exact timing") : "Not a plan yet";
    if (key === this.lastKey) return;
    this.lastKey = key;
    this.plan = plan;
    this.renderPlan(plan, !first);
    if (plan.ok) {
      this.frames = C.framesFromPlan(plan);
      this.renderStrip(!first);
      if (!first) { this.stopIdle(); this.show(Math.min(this.cur, 15), true); }
    }
  };

  Playground.prototype.renderPlan = function (plan, animate) {
    var g = this.grid;
    this.list.innerHTML = "";
    this.added.textContent = "";
    if (!plan.ok) {
      g.removeAttribute("style");
      g.innerHTML = '<div class="plan__alert" role="alert"><strong>Cue couldn’t turn this into a plan.</strong>' +
        esc(plan.reason) + '<br><button type="button" data-try>Try: “' + esc(plan.suggestion) + '”</button></div>';
      g.style.border = "0";
      var self = this;
      $("[data-try]", g).addEventListener("click", function () { self.text.value = plan.suggestion; self.update(); self.text.focus(); });
      return;
    }
    g.style.border = "";
    if (plan.empty) {
      g.innerHTML = '<div class="plan__empty">Nothing to plan. Cue will move the eyes, the head and the expression together, from the first drawing to the last.</div>';
      g.style.border = "0";
      return;
    }
    var n = plan.steps.length;
    g.style.setProperty("--cols", n);
    var html = '<div class="pg__row pg__row--head"><div class="pg__lane"></div>';
    for (var i = 0; i < n; i++) html += '<div class="pg__cell">' + colWord(i, n) + "</div>";
    html += "</div>";
    var num = 0, order = [];
    plan.steps.forEach(function (st, si) { st.events.forEach(function (e) { order.push({ si: si, e: e }); }); });
    // number in reading order: by step, then lane order
    var laneOrder = ["gaze", "head", "smile", "hand"];
    order.sort(function (a, b) { return a.si - b.si || laneOrder.indexOf(a.e.region) - laneOrder.indexOf(b.e.region); });
    order.forEach(function (o) { o.n = ++num; });
    var self = this;
    laneOrder.forEach(function (reg) {
      var mine = order.filter(function (o) { return o.e.region === reg; });
      html += '<div class="pg__row"><div class="pg__lane">' + REGION_LABEL[reg] + "</div>";
      if (!mine.length) {
        if (reg === "hand") html += '<div class="pg__cell" style="grid-column: 2 / -1; color: var(--ui-muted); font-size: 12px; align-items: center; padding-left: 10px;">No change</div>';
        else html += '<div class="pg__cell pg__cell--follow is-first" style="grid-column: 2 / -1"></div>';
      } else {
        for (var i = 0; i < n; i++) {
          var here = mine.filter(function (o) { return o.si === i; });
          html += '<div class="pg__cell">';
          here.forEach(function (o) {
            html += '<div class="cue' + (o.e.added ? " cue--added" : "") + '" data-n="' + o.n + '"><span class="cue__n">' + o.n + '</span><span class="cue__t"><span class="cue__a">' + esc(o.e.action) + '</span><span class="cue__s">' + (o.e.added ? "added" : SPEED_LABEL[o.e.speed]) + "</span></span></div>";
          });
          html += "</div>";
        }
      }
      html += "</div>";
    });
    g.innerHTML = html;
    order.forEach(function (o) {
      var li = document.createElement("li");
      li.className = "cue" + (o.e.added ? " cue--added" : "");
      li.innerHTML = '<span class="cue__n" aria-hidden="true">' + o.n + '</span><span class="cue__t"><span class="cue__a">' + colWord(o.si, n) + ": " + esc(o.e.action) + '</span><span class="cue__s">' + REGION_LABEL[o.e.region] + " · " + (o.e.added ? "added by Cue" : SPEED_LABEL[o.e.speed]) + "</span></span>";
      self.list.appendChild(li);
    });
    this.added.textContent = plan.added.join(" ");

    // cue blocks arrive left to right, in reading order: teaches the order, plays once per new plan
    if (animate && !reduce) {
      var cues = $$(".cue", g).sort(function (a, b) { return a.getAttribute("data-n") - b.getAttribute("data-n"); });
      cues.forEach(function (c) { c.classList.add("is-entering"); });
      g.offsetWidth; // commit the start state
      cues.forEach(function (c, i) {
        c.style.transitionDelay = Math.min(i * 60, 360) + "ms";
        c.classList.remove("is-entering");
      });
    }
  };

  Playground.prototype.renderStrip = function (animate) {
    var self = this;
    var build = function () {
      var html = "";
      self.frames.forEach(function (p, i) {
        var key = i === 0 || i === 15;
        html += '<button type="button" class="fr' + (key ? " fr--key" : "") + '" role="option" data-i="' + i + '" aria-selected="' + (i === self.cur) + '" aria-label="Frame ' + (i + 1) + (key ? ", your drawing" : "") + '">' + C.drawFigure(p, { width: 3.4, label: "Frame " + (i + 1) }) + "</button>";
      });
      self.stripEl.innerHTML = html;
      if (!self.stripEl.nextElementSibling) {
        self.stripEl.insertAdjacentHTML("afterend", '<div class="strip__labels"><span>Frame 1 · your start drawing</span><span>Frame 16 · your end drawing</span></div>');
      }
    };
    if (!animate || reduce) { build(); return; }
    // mask the swap: a short blur bridges the old strip and the new one
    this.stripEl.classList.add("is-updating");
    setTimeout(function () { build(); requestAnimationFrame(function () { self.stripEl.classList.remove("is-updating"); }); }, 120);
  };

  Playground.prototype.show = function (i, force) {
    if (!this.frames.length) return;
    i = (i + 16) % 16;
    if (i === this.cur && !force && this.stage.classList.contains("is-manual")) return;
    this.cur = i;
    this.stage.classList.add("is-manual");
    var onion = this.onion.checked && i > 0 ? this.frames[i - 1] : null;
    this.layerA.innerHTML = C.drawFigure(this.frames[i], { onion: onion, label: "Frame " + (i + 1) });
    this.layerA.classList.add("is-shown");
    this.layerB.classList.remove("is-shown");
    this.count.textContent = "Frame " + (i + 1) + " of 16";
    this.tag.textContent = i === 0 ? "Your start drawing" : i === 15 ? "Your end drawing" : onion ? "Onion skin: frame " + i + " in pink" : "Frame " + (i + 1);
    $$(".fr", this.stripEl).forEach(function (f, k) { f.setAttribute("aria-selected", String(k === i)); });
  };

  Playground.prototype.togglePlay = function () { this.timer ? this.pause() : this.play(); };
  Playground.prototype.play = function () {
    var self = this;
    this.stopIdle();
    if (this.cur === 15) this.show(0, true);
    this.playBtn.classList.add("is-playing");
    this.playBtn.setAttribute("aria-label", "Pause");
    var hold = 0;
    // 12 fps on twos: each drawing holds for two film frames
    this.timer = setInterval(function () {
      if (self.cur === 15 && hold < 3) { hold++; return; }
      hold = 0;
      self.show(self.cur + 1, true);
    }, 167);
  };
  Playground.prototype.pause = function () {
    clearInterval(this.timer);
    this.timer = null;
    this.playBtn.classList.remove("is-playing");
    this.playBtn.setAttribute("aria-label", "Play");
  };

  // The signature move: while nobody is touching it, the stage crossfades slowly between
  // the two drawings, like flipping a sheet on a light table.
  Playground.prototype.startIdle = function () {
    var self = this;
    this.layerA.innerHTML = C.drawFigure(C.START, { label: "Start drawing" });
    this.layerB.innerHTML = C.drawFigure(C.END, { label: "End drawing" });
    if (reduce) return;
    var showingEnd = false;
    this.idle = setInterval(function () {
      if (document.hidden) return;
      showingEnd = !showingEnd;
      self.layerA.classList.toggle("is-shown", !showingEnd);
      self.layerB.classList.toggle("is-shown", showingEnd);
      self.tag.textContent = showingEnd ? "Your end drawing" : "Your start drawing";
    }, 6600);
  };
  Playground.prototype.stopIdle = function () {
    if (this.idle) { clearInterval(this.idle); this.idle = null; }
  };

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  var pgRoot = $("[data-playground]");
  var pg = pgRoot ? new Playground(pgRoot) : null;

  /* ================= CTA feeds the cue sheet ================= */
  var form = $("[data-ctaform]");
  if (form && pg) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = $("#cta-input").value.trim() || $("#cta-input").placeholder;
      var sentence = v.charAt(0).toUpperCase() + v.slice(1);
      pg.text.value = sentence.replace(/[.\s]*$/, ".");
      pg.update();
      $("#playground").scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
      setTimeout(function () { pg.text.focus({ preventScroll: true }); }, reduce ? 0 : 600);
    });
  }

  /* ================= drawings placed in static fragments ================= */
  var demoPlan = C.parseInstruction(C.EXAMPLES[0]);
  var demoFrames = C.framesFromPlan(demoPlan);
  var wavePlan = C.parseInstruction(C.EXAMPLES[2]);
  var waveFrames = C.framesFromPlan(wavePlan);
  $$("[data-draw]").forEach(function (el) {
    var k = el.getAttribute("data-draw");
    var p = k === "start" ? C.START : k === "end" ? C.END : demoFrames[8];
    el.innerHTML = C.drawFigure(p, { width: k === "mid" ? 2.4 : 3, label: k === "start" ? "Start drawing" : k === "end" ? "End drawing" : "Frame 9" });
  });

  var mini = $("[data-miniplan]");
  if (mini) {
    var rows = [["Gaze", 0, "Eyes left", "normal speed"], ["Head", 1, "Head turns left", "slowly"], ["Expression", 2, "Smile", "normal speed"]];
    mini.innerHTML = rows.map(function (r, i) {
      var cells = "";
      for (var c = 0; c < 3; c++) cells += '<div class="mp__slot">' + (c === r[1] ? '<div class="cue"><span class="cue__n">' + (i + 1) + '</span><span class="cue__t"><span class="cue__a">' + r[2] + '</span><span class="cue__s">' + r[3] + "</span></span></div>" : "") + "</div>";
      return '<div class="mp__row"><span class="mp__lane">' + r[0] + "</span>" + cells + "</div>";
    }).join("");
  }
  var ms = $("[data-ministrip]");
  if (ms) { var s = ""; for (var i = 0; i < 16; i++) s += '<span class="' + (i === 0 || i === 15 ? "k" : "") + '"></span>'; ms.innerHTML = s; }
  var ticks = $("[data-ticks]");
  if (ticks) { var t = ""; for (var j = 0; j < 14; j++) t += '<span style="--i:' + j + '"></span>'; ticks.innerHTML = t; }
  var scrub = $("[data-scrub]");
  if (scrub) { var sc = ""; for (var k = 0; k < 16; k++) sc += '<span class="' + (k === 0 || k === 15 ? "k" : k === 8 ? "cur" : k < 8 ? "done" : "") + '"></span>'; scrub.innerHTML = sc; }
  var m16 = $("[data-mini16]");
  if (m16) m16.innerHTML = waveFrames.map(function (p, i) { return "<div>" + C.drawFigure(p, { width: 4, label: "Frame " + (i + 1) }) + "</div>"; }).join("");

  var lib = $("[data-lib]");
  if (lib) {
    var jobs = [
      { name: "Eyes, then head, then smile", date: "Today, 14:02", state: "run", label: "Running", p: C.START, dim: true },
      { name: "Glance left, wave, smile", date: "Today, 11:47", state: "pos", label: "Done", p: waveFrames[9] },
      { name: "Turn and smile together", date: "Yesterday", state: "pos", label: "Done", p: C.END },
      { name: "Untitled animation", date: "3 Nov", state: "fail", label: "Failed", p: C.START },
    ];
    lib.innerHTML = jobs.map(function (j) {
      return '<div class="lib__row"><div class="lib__thumb"' + (j.dim ? ' style="opacity:.55"' : "") + ">" + C.drawFigure(j.p, { width: 4.2, label: j.name }) + '</div><div><div class="lib__name">' + j.name + '</div><div class="lib__date">' + j.date + '</div></div><span class="pill pill--' + j.state + '">' + j.label + "</span></div>";
    }).join("");
  }

  /* ================= how it works: the pinned fragment follows the statements ================= */
  var howui = $("[data-howui]");
  var steps = $$(".how__step");
  var result = $("[data-result]");
  var resultTimer = null, rf = 0;
  function setHow(i) {
    steps.forEach(function (s, k) { s.classList.toggle("is-active", k === i); });
    if (!howui || howui.getAttribute("data-state") === String(i)) return;
    howui.setAttribute("data-state", String(i));
    clearInterval(resultTimer);
    if (i === 2 && result) {
      rf = 0;
      result.innerHTML = C.drawFigure(demoFrames[0], { label: "Result" });
      if (!reduce) resultTimer = setInterval(function () {
        rf = (rf + 1) % 20;
        result.innerHTML = C.drawFigure(demoFrames[Math.min(rf, 15)], { label: "Result, frame " + (Math.min(rf, 15) + 1) });
      }, 167);
    }
  }
  if (steps.length && "IntersectionObserver" in window) {
    var hio = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) setHow(steps.indexOf(en.target)); });
    }, { rootMargin: "-45% 0px -45% 0px" });
    steps.forEach(function (s) { hio.observe(s); });
    setHow(0);
  }

  /* ================= showcase: the centred panel is lit ================= */
  var row = $("[data-showrow]");
  if (row) {
    var panels = $$(".show__panel", row);
    var cap = $(".show__caption");
    var nameEl = $("[data-showname]"), descEl = $("[data-showdesc]");
    var lit = -1, swapT = null;
    var light = function () {
      var mid = row.getBoundingClientRect().left + row.clientWidth / 2, best = 0, bd = Infinity;
      panels.forEach(function (p, i) {
        var r = p.getBoundingClientRect(), d = Math.abs(r.left + r.width / 2 - mid);
        if (d < bd) { bd = d; best = i; }
      });
      if (best === lit) return;
      lit = best;
      panels.forEach(function (p, i) { p.classList.toggle("is-lit", i === best); p.setAttribute("aria-hidden", String(i !== best)); });
      var p = panels[best];
      if (reduce) { nameEl.textContent = p.dataset.name; descEl.textContent = p.dataset.desc; return; }
      cap.classList.add("is-swapping");
      clearTimeout(swapT);
      swapT = setTimeout(function () { nameEl.textContent = p.dataset.name; descEl.textContent = p.dataset.desc; cap.classList.remove("is-swapping"); }, 180);
    };
    var raf = 0;
    row.addEventListener("scroll", function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(light); }, { passive: true });
    window.addEventListener("resize", light);
    light();
    // drag with a mouse; touch scrolls natively
    var down = false, sx = 0, sl = 0;
    row.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") return; down = true; sx = e.clientX; sl = row.scrollLeft; row.setPointerCapture(e.pointerId); row.classList.add("is-dragging"); });
    row.addEventListener("pointermove", function (e) { if (down) row.scrollLeft = sl - (e.clientX - sx); });
    var up = function () { if (!down) return; down = false; row.classList.remove("is-dragging"); var p = panels[lit]; if (p) p.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest", inline: "center" }); };
    row.addEventListener("pointerup", up);
    row.addEventListener("pointercancel", up);
    row.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
      e.preventDefault();
      var n = Math.max(0, Math.min(panels.length - 1, lit + (e.key === "ArrowLeft" ? -1 : 1)));
      panels[n].scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest", inline: "center" });
    });
  }

  /* ================= entrances: heading, then text, then picture, once ================= */
  var rev = $$("[data-reveal]");
  var groups = new Map();
  rev.forEach(function (el) {
    var sec = el.closest("section, header, footer") || document.body;
    var list = groups.get(sec) || [];
    el.style.setProperty("--d", list.length % 6);
    list.push(el);
    groups.set(sec, list);
  });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    rev.forEach(function (el) { io.observe(el); });
  } else {
    rev.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ================= the one film: plays only while on screen, never under reduced motion ================= */
  $$("video[data-loop]").forEach(function (v) {
    if (reduce || !("IntersectionObserver" in window)) return;
    new IntersectionObserver(function (ents) {
      ents.forEach(function (en) {
        if (en.isIntersecting) { v.preload = "auto"; var pr = v.play(); if (pr && pr.catch) pr.catch(function () {}); }
        else v.pause();
      });
    }, { threshold: 0.25 }).observe(v);
  });

  /* ================= the zoetrope strip moves with the reader's scroll, not on its own ================= */
  var band = $(".hist__band"), drift = $(".hist__drift");
  if (band && drift && !reduce) {
    var pending = false;
    var place = function () {
      pending = false;
      var r = band.getBoundingClientRect(), vh = window.innerHeight;
      if (r.bottom < 0 || r.top > vh) return;
      var t = Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
      var travel = Math.max(0, drift.scrollWidth - band.clientWidth);
      drift.style.transform = "translate3d(" + (-t * travel).toFixed(1) + "px,0,0)";
    };
    window.addEventListener("scroll", function () { if (!pending) { pending = true; requestAnimationFrame(place); } }, { passive: true });
    window.addEventListener("resize", place);
    place();
  }

  /* ================= local time in the footer ================= */
  var clock = $("[data-clock]");
  if (clock) {
    var fmt = new Intl.DateTimeFormat("en-GB", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Istanbul" });
    var tick = function () { clock.textContent = fmt.format(new Date()); };
    tick();
    setInterval(tick, 30000);
  }
})();
