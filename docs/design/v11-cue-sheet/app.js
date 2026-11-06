/* Cue v11 — studio screens S1–S6, rendered from one sample dataset.
 * Routes: #s1 … #s6, with a state after a slash (#s5/failed). The bar at the bottom switches them.
 * Sample data only: no account, upload, model call, job or download is real. */
(function () {
  "use strict";
  var C = window.Cue;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var app = document.getElementById("app");
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  /* ================= sample data ================= */
  // "Now" in the mockup. Jobs are newest first; durations in seconds.
  var NOW = new Date("2026-11-06T14:04:10+03:00");
  var JOBS = [
    { id: "7f3a21c4", cmd: "First move the eyes to the left, then slowly turn the head, and begin smiling near the end.", status: "running", created: "2026-11-06T14:02:00+03:00", seed: 48213, model: "cue-ib 0.1-dev" },
    { id: "7f2e0b19", cmd: "Eyes left, then a slow head turn.", status: "queued", created: "2026-11-06T14:03:41+03:00", seed: null, model: "cue-ib 0.1-dev" },
    { id: "7f2c90aa", cmd: "Glance left quickly, then raise a hand while turning, then lower it and smile.", status: "done", created: "2026-11-06T11:47:00+03:00", seed: 30551, model: "cue-ib 0.1-dev", took: 222, kb: 184 },
    { id: "7e91d402", cmd: "Turn the head and smile at the same time.", status: "done", created: "2026-11-05T18:20:00+03:00", seed: 9174, model: "cue-ib 0.1-dev", took: 178, kb: 171 },
    { id: "7e5b0277", cmd: "", status: "done", created: "2026-11-03T16:12:00+03:00", seed: 61208, model: "cue-ib 0.1-dev", took: 171, kb: 162 },
    { id: "7c88a1e0", cmd: "First the eyes, then the head.", status: "failed", created: "2026-11-03T10:05:00+03:00", seed: 27719, model: "cue-ib 0.1-dev", reason: "The GPU worker stopped at frame 11: it ran out of memory." },
    { id: "7b4410d3", cmd: "Smile, then turn the head.", status: "cancelled", created: "2026-11-02T21:40:00+03:00", seed: null, model: "cue-ib 0.1-dev" },
    { id: "7a2f37b8", cmd: "Turn the head slowly, then smile.", status: "done", created: "2026-11-01T09:15:00+03:00", seed: 4402, model: "cue-ib 0.1-dev", took: 205, kb: 176 },
  ];
  JOBS.forEach(function (j) {
    j.title = j.cmd ? (j.cmd.length > 40 ? j.cmd.slice(0, 40).replace(/[\s,]+\S*$/, "") + "…" : j.cmd.replace(/\.$/, "")) : "Untitled animation";
    j.plan = C.parseInstruction(j.cmd);
    j.frames = C.framesFromPlan(j.plan);
  });
  var counts = JOBS.reduce(function (a, j) { a[j.status] = (a[j.status] || 0) + 1; return a; }, {});
  console.assert(JOBS.length === Object.keys(counts).reduce(function (a, k) { return a + counts[k]; }, 0), "status counts add up to the job count");
  var RUNNING = JOBS[0], QUEUED = JOBS[1], DONE = JOBS[2], FAILED = JOBS[5], CANCELLED = JOBS[6];
  var ELAPSED0 = Math.round((NOW - new Date(RUNNING.created)) / 1000); // 130 s

  var STATUS = {
    queued: { label: "Queued", icon: '<svg viewBox="0 0 12 12"><circle cx="6" cy="6" r="4.2" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2 2"/></svg>' },
    running: { label: "Running", icon: '<svg viewBox="0 0 12 12"><circle cx="6" cy="6" r="4.2" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M6 1.8a4.2 4.2 0 0 1 4.2 4.2" fill="none" stroke="currentColor" stroke-width="1.6"/><circle cx="6" cy="6" r="1.6" fill="currentColor"/></svg>' },
    done: { label: "Done", icon: '<svg viewBox="0 0 12 12"><path d="m2.6 6.2 2.3 2.3 4.6-5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>' },
    failed: { label: "Failed", icon: '<svg viewBox="0 0 12 12"><path d="M6 3v3.4M6 8.6v.1" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="6" cy="6" r="4.6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>' },
    cancelled: { label: "Cancelled", icon: '<svg viewBox="0 0 12 12"><path d="M3.5 3.5l5 5M8.5 3.5l-5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>' },
  };
  function pill(st) { return '<span class="pill pill--' + st + '">' + STATUS[st].icon + STATUS[st].label + "</span>"; }

  var I = {
    lib: '<svg viewBox="0 0 16 16"><rect x="2" y="3" width="5" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="9" y="3" width="5" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="2" y="9" width="5" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/><rect x="9" y="9" width="5" height="4" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    plus: '<svg viewBox="0 0 16 16"><path d="M8 3v10M3 8h10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    back: '<svg viewBox="0 0 16 16"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    next: '<svg viewBox="0 0 16 16"><path d="m6 3 5 5-5 5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    play: '<svg viewBox="0 0 16 16"><path d="M5 3.2v9.6L12.6 8z" fill="currentColor"/></svg>',
    pause: '<svg viewBox="0 0 16 16"><path d="M4.5 3h2.6v10H4.5zM8.9 3h2.6v10H8.9z" fill="currentColor"/></svg>',
    more: '<svg viewBox="0 0 16 16"><circle cx="3.5" cy="8" r="1.3" fill="currentColor"/><circle cx="8" cy="8" r="1.3" fill="currentColor"/><circle cx="12.5" cy="8" r="1.3" fill="currentColor"/></svg>',
    help: '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M6.3 6.3a1.8 1.8 0 1 1 2.4 1.7c-.5.2-.7.6-.7 1v.4M8 11.4v.1" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
    menu: '<svg viewBox="0 0 16 16"><path d="M2.5 4.5h11M2.5 8h11M2.5 11.5h11" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    swap: '<svg viewBox="0 0 16 16"><path d="M3 5h9l-2.5-2.5M13 11H4l2.5 2.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    up: '<svg viewBox="0 0 24 24"><path d="M12 16V5m0 0-4 4m4-4 4 4M5 19h14" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    warn: '<svg viewBox="0 0 24 24"><path d="M12 8v5m0 3.2v.3M10.3 3.9 2.6 17.3A2 2 0 0 0 4.3 20.3h15.4a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>',
    info: '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 7.2V11M8 5v.1" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
    eye: '<svg viewBox="0 0 20 20"><path d="M2 10s3-5.5 8-5.5S18 10 18 10s-3 5.5-8 5.5S2 10 2 10Z" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="10" cy="10" r="2.5" fill="none" stroke="currentColor" stroke-width="1.5"/></svg>',
    arrow: '<svg viewBox="0 0 20 20"><path d="M3 10h13m0 0-4-4m4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    dl: '<svg viewBox="0 0 16 16"><path d="M8 2.5v8m0 0-3-3m3 3 3-3M3 13.5h10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    mark: '<svg viewBox="0 0 40 28" aria-hidden="true"><rect x="1" y="4" width="14" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="25" y="4" width="14" height="20" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="20" cy="14" r="3" fill="#ff488b"/></svg>',
  };

  function fmtDate(iso) {
    var d = new Date(iso), days = Math.floor((new Date(NOW.toDateString()) - new Date(d.toDateString())) / 864e5);
    var t = new Intl.DateTimeFormat("en-GB", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Istanbul" }).format(d);
    if (days === 0) return "Today, " + t;
    if (days === 1) return "Yesterday, " + t;
    return new Intl.DateTimeFormat("en-GB", { day: "numeric", month: "short", timeZone: "Europe/Istanbul" }).format(d) + ", " + t;
  }
  function dur(s) { var m = Math.floor(s / 60), r = s % 60; return (m ? m + " min " : "") + r + " s"; }
  function draw(p, o) { return C.drawFigure(p, o); }

  /* ================= screens and states ================= */
  var SCREENS = [
    { id: "s1", name: "S1 · Log in", states: ["log in", "create account", "wrong password", "logging in"] },
    { id: "s2", name: "S2 · Library", states: ["animations", "empty", "loading", "fetch error"] },
    { id: "s3", name: "S3 · Drawings", states: ["both ready", "empty", "uploading", "wrong file"] },
    { id: "s4", name: "S4 · Motion plan", states: ["approved", "not approved", "reading", "out of date", "refused", "no instruction"] },
    { id: "s5", name: "S5 · Generation", states: ["running", "queued", "done", "failed", "cancelled"] },
    { id: "s6", name: "S6 · Result", states: ["ready", "video failed"] },
  ];
  var timers = [];
  function later(fn, ms) { timers.push(setTimeout(fn, ms)); }
  function every(fn, ms) { timers.push(setInterval(fn, ms)); }
  function clearTimers() { timers.forEach(function (t) { clearTimeout(t); clearInterval(t); }); timers = []; }

  function route() {
    var h = (location.hash || "#s2").slice(1).split("/");
    var sc = SCREENS.filter(function (s) { return s.id === h[0]; })[0] || SCREENS[1];
    var st = decodeURIComponent(h[1] || sc.states[0]);
    if (sc.states.indexOf(st) < 0) st = sc.states[0];
    return { sc: sc, st: st };
  }
  function go(id, state) { location.hash = "#" + id + (state ? "/" + encodeURIComponent(state) : ""); }

  /* ================= shells ================= */
  function shell(active, crumbs, body) {
    return '<div class="shell" data-shell>' +
      '<aside class="side" aria-label="Studio">' +
        '<a class="brand" href="index.html">' + I.mark + "Cue</a>" +
        '<div class="scope">Studio <b>İclal’s drawings</b></div>' +
        '<nav class="nav" aria-label="Main">' +
          '<a href="#s2"' + (active === "lib" ? ' aria-current="page"' : "") + ">" + I.lib + "Library</a>" +
          '<a href="#s3/empty"' + (active === "new" ? ' aria-current="page"' : "") + ">" + I.plus + "New animation</a>" +
        "</nav>" +
        '<div class="side__foot">' +
          '<nav class="nav" aria-label="Help"><a href="#" data-help>' + I.help + 'Help</a></nav>' +
          '<button class="who" type="button" data-logout title="Log out"><span class="avatar" aria-hidden="true">İ</span><span><span class="who__name">İclal Doğan</span><span class="who__mail" style="display:block">Log out</span></span></button>' +
        "</div>" +
      "</aside>" +
      '<header class="topbar"><button class="btn btn--ghost btn--icon menu-btn" type="button" data-menu aria-label="Open menu">' + I.menu + '</button><nav class="crumbs" aria-label="Breadcrumb">' + crumbs + "</nav></header>" +
      '<main class="sheet" id="main"><div class="sheet__in">' + body + "</div></main>" +
    "</div>";
  }
  function builder(name, step, endHtml, panel, canvas) {
    var stepNames = ["Drawings", "Motion", "Generate"];
    return '<div class="builder">' +
      '<header class="btop">' +
        '<a class="btn btn--ghost btn--icon" href="#s2" aria-label="Back to Library">' + I.back + "</a>" +
        '<span class="btop__name">' + esc(name) + "</span>" + '<span class="pill pill--draft">Draft</span>' +
        '<ol class="stepper" aria-label="Steps">' + stepNames.map(function (n, i) { return "<li" + (i === step ? ' aria-current="step"' : i < step ? ' class="is-done"' : "") + ">" + n + "</li>"; }).join("") + "</ol>" +
        '<div class="btop__end">' + endHtml + "</div>" +
      "</header>" +
      '<div class="bpanels"><aside class="panel">' + panel + '</aside><main class="canvas" id="main">' + canvas + "</main></div>" +
    "</div>";
  }

  /* ================= S1 auth ================= */
  function s1(st) {
    var create = st === "create account";
    var err = st === "wrong password", loading = st === "logging in";
    var strip = C.framesFromPlan(C.parseInstruction(C.EXAMPLES[0]));
    var html = '<div class="auth">' +
      '<section class="auth__brand"><a class="brand" href="index.html">' + I.mark + "Cue</a>" +
        '<div><p class="auth__line">Two drawings in, one clip out.</p></div>' +
        '<div><div class="auth__strip' + (reduce ? "" : " is-settling") + '" data-strip>' + strip.map(function (p, i) { return '<div style="--i:' + i + '">' + draw(p, { width: 4, label: "Frame" }) + "</div>"; }).join("") + '</div><p class="auth__cap" style="margin-top:10px">Sixteen frames: the first and the last are the drawings you bring.</p></div>' +
      "</section>" +
      '<main class="auth__form" id="main"><form class="auth__box" novalidate data-auth>' +
        "<h1>" + (create ? "Create your account" : "Log in to Cue") + "</h1>" +
        '<div class="seg" role="tablist" data-tab="' + (create ? "create" : "login") + '"><span class="seg__thumb" aria-hidden="true"></span>' +
          '<button type="button" role="tab" aria-selected="' + !create + '" data-go="log in">Log in</button>' +
          '<button type="button" role="tab" aria-selected="' + create + '" data-go="create account">Create account</button></div>' +
        (err ? '<div class="alert alert--neg" role="alert"><strong>Email or password is incorrect.</strong></div>' : "") +
        '<div class="field"><label for="em">Email</label><input class="input" id="em" type="email" autocomplete="email" value="iclal@example.edu"' + (loading ? " disabled" : "") + "></div>" +
        '<div class="field"><label for="pw">Password</label><div class="pw"><input class="input" id="pw" type="password" autocomplete="' + (create ? "new-password" : "current-password") + '" value="' + (create ? "" : "inbetween16") + '"' + (loading ? " disabled" : "") + '><button type="button" data-pw aria-label="Show password" aria-pressed="false">' + I.eye + "</button></div>" +
        (create ? '<ul class="rules" aria-label="Password rules"><li>At least 10 characters</li><li>Not the same as your email</li><li class="muted">Exact rules to be confirmed with the backend</li></ul>' : "") + "</div>" +
        '<button class="btn btn--primary btn--lg' + (loading ? " is-loading" : "") + '" type="submit"' + (loading ? ' aria-busy="true"' : "") + ">" + (loading ? '<span class="spinner" aria-hidden="true"></span>Logging in…' : create ? "Create account" : "Log in") + "</button>" +
        '<p class="auth__note">No password reset or social login in this version.</p>' +
      "</form></main></div>";
    return { html: html, after: function () {
      var s = $("[data-strip]");
      if (s) requestAnimationFrame(function () { requestAnimationFrame(function () { s.classList.remove("is-settling"); }); });
      $$("[data-go]").forEach(function (b) { b.addEventListener("click", function () { go("s1", b.getAttribute("data-go")); }); });
      var pwb = $("[data-pw]");
      pwb.addEventListener("click", function () { var i = $("#pw"), on = i.type === "password"; i.type = on ? "text" : "password"; pwb.setAttribute("aria-pressed", String(on)); pwb.setAttribute("aria-label", on ? "Hide password" : "Show password"); });
      $("[data-auth]").addEventListener("submit", function (e) { e.preventDefault(); if (st === "logging in") return; go("s1", "logging in"); later(function () { go("s2"); }, 1100); });
    } };
  }

  /* ================= S2 library ================= */
  function jobCard(j) {
    var thumb;
    if (j.status === "done") thumb = '<div class="job__thumb">' + draw(j.frames[8], { width: 3, label: "Frame 9 of " + j.title }) + '<span class="job__play" aria-hidden="true">' + I.play + "</span></div>";
    else if (j.status === "failed") thumb = '<div class="job__thumb">' + draw(C.START, { width: 3, label: "" }) + '<div class="job__fail">' + I.warn + "</div></div>";
    else {
      var t = ""; for (var i = 0; i < 16; i++) t += '<span class="' + (i === 0 || i === 15 ? "k" : "") + '" style="--i:' + i + '"></span>';
      thumb = '<div class="job__thumb job__thumb--dim">' + draw(C.START, { width: 3, label: "Start drawing of " + j.title }) + '<div class="job__ticks">' + t + "</div></div>";
    }
    var href = j.status === "done" ? "#s6" : "#s5/" + j.status;
    return '<article class="job job--' + j.status + '" data-id="' + j.id + '">' +
      '<a class="job__link" href="' + href + '">' + thumb + '<div class="job__meta"><span class="job__title">' + esc(j.title) + '</span><span class="job__status">' + pill(j.status) + '</span><span class="job__date">' + fmtDate(j.created) + "</span>" +
      (j.status === "failed" ? '<span class="job__reason">' + esc(j.reason) + "</span>" : "") + "</div></a>" +
      '<button class="job__more" type="button" aria-label="More for ' + esc(j.title) + '" aria-haspopup="menu" aria-expanded="false" data-more>' + I.more + "</button></article>";
  }
  function s2(st) {
    var body;
    var title = '<div class="titlerow"><div><h1>Your animations</h1>';
    if (st === "animations") {
      title += '<p class="titlerow__sub">' + JOBS.length + " animations · " + counts.running + " running, " + counts.queued + " queued. “" + esc(RUNNING.title) + "” has been running for " + '<span data-elapsed>' + dur(ELAPSED0) + '</span>. <a href="#s5/running">View status</a></p>';
      body = '<div class="lib" data-lib>' + JOBS.map(jobCard).join("") + "</div>";
    } else if (st === "empty") {
      title += '<p class="titlerow__sub">Nothing here yet.</p>';
      body = '<div class="empty"><div class="empty__pair"><div class="drawing">' + draw(C.START, { width: 3, label: "Start drawing" }) + '</div><span></span><div class="drawing">' + draw(C.END, { width: 3, label: "End drawing" }) + "</div></div><p>No animations yet. Upload two drawings to make your first one.</p>" +
        '<a class="btn" href="#s3/empty">' + I.plus + "New animation</a></div>";
    } else if (st === "loading") {
      title += '<p class="titlerow__sub">Loading your animations…</p>';
      body = '<div class="lib" aria-busy="true">' + [0, 1, 2, 3, 4, 5].map(function () { return '<div><div class="skel" style="aspect-ratio:8/5"></div><div class="skel" style="height:14px;width:70%;margin-top:12px"></div><div class="skel" style="height:12px;width:40%;margin-top:8px"></div></div>'; }).join("") + "</div>";
    } else {
      title += '<p class="titlerow__sub">Couldn’t load the list.</p>';
      body = '<div class="alert alert--neg" role="alert"><strong>Your animations couldn’t be loaded.</strong>The server didn’t answer. Your animations are safe; this is only the list.<div class="alert__actions"><button class="btn" type="button" data-retry>Try again</button></div></div>';
    }
    title += "</div>" + (st === "empty" ? "" : '<div class="titlerow__acts"><a class="btn btn--primary" href="#s3/empty">' + I.plus + "New animation</a></div>") + "</div>";
    return { html: shell("lib", "<b>Library</b>", title + body), after: function () {
      bindShell();
      var r = $("[data-retry]"); if (r) r.addEventListener("click", function () { go("s2", "loading"); later(function () { go("s2"); }, 900); });
      var el = $("[data-elapsed]"); var e = ELAPSED0;
      if (el) every(function () { e++; el.textContent = dur(e); }, 1000);
      bindMenus();
    } };
  }
  function bindMenus() {
    var open = null;
    function close() { if (open) { open.btn.setAttribute("aria-expanded", "false"); open.menu.remove(); open = null; } }
    $$("[data-more]").forEach(function (b) {
      b.addEventListener("click", function (e) {
        e.stopPropagation();
        var was = open && open.btn === b; close(); if (was) return;
        var m = document.createElement("div"); m.className = "menu"; m.setAttribute("role", "menu");
        m.innerHTML = '<button role="menuitem" type="button">Delete animation</button>';
        b.parentNode.appendChild(m); b.setAttribute("aria-expanded", "true"); open = { btn: b, menu: m };
        var card = b.closest(".job");
        m.firstChild.addEventListener("click", function () { close(); confirmDelete(card); });
        m.firstChild.focus();
      });
    });
    document.addEventListener("click", close);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  }
  function confirmDelete(card) {
    var title = $(".job__title", card).textContent;
    var s = document.createElement("div"); s.className = "scrim";
    s.innerHTML = '<div class="dialog" role="alertdialog" aria-modal="true" aria-labelledby="dlg-t" aria-describedby="dlg-d"><h2 id="dlg-t">Delete this animation?</h2><p id="dlg-d">“' + esc(title) + '”, its video and its drawings are removed. This can’t be undone.</p><div class="dialog__acts"><button class="btn" type="button" data-no>Cancel</button><button class="btn btn--destructive" type="button" data-yes>Delete</button></div></div>';
    document.body.appendChild(s);
    var back = document.activeElement;
    $("[data-no]", s).focus();
    function done() { s.remove(); if (back) back.focus(); }
    $("[data-no]", s).addEventListener("click", done);
    s.addEventListener("click", function (e) { if (e.target === s) done(); });
    s.addEventListener("keydown", function (e) { if (e.key === "Escape") done(); });
    $("[data-yes]", s).addEventListener("click", function () {
      s.remove();
      card.style.transition = reduce ? "none" : "opacity 180ms ease, transform 180ms var(--ease-out)";
      card.style.opacity = "0"; card.style.transform = "scale(0.97)";
      later(function () { card.remove(); }, reduce ? 0 : 180);
      toast("Animation deleted");
    });
  }
  function toast(text) {
    var old = $(".toast"); if (old) old.remove();
    var t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); t.setAttribute("data-enter", "");
    t.textContent = text; document.body.appendChild(t);
    requestAnimationFrame(function () { requestAnimationFrame(function () { t.removeAttribute("data-enter"); }); });
    setTimeout(function () { t.setAttribute("data-exit", ""); setTimeout(function () { t.remove(); }, 140); }, 3200);
  }
  function bindShell() {
    var sh = $("[data-shell]"), m = $("[data-menu]");
    if (m) m.addEventListener("click", function (e) { e.stopPropagation(); sh.classList.toggle("is-menu"); });
    var hb = $("[data-help]"); if (hb) hb.addEventListener("click", function (e) { e.preventDefault(); toast("Help isn’t part of this mockup"); });
    if (sh) sh.addEventListener("click", function (e) { if (sh.classList.contains("is-menu") && !e.target.closest(".side")) sh.classList.remove("is-menu"); });
    var lo = $("[data-logout]"); if (lo) lo.addEventListener("click", function () { go("s1"); });
  }

  /* ================= S3 drawings ================= */
  function slot(which, state) {
    var label = which === "start" ? "Start drawing" : "End drawing";
    var p = which === "start" ? C.START : C.END;
    var file = which === "start" ? ["start_front.png", "1280 × 800", "212 KB"] : ["end_left_smile.png", "1280 × 800", "198 KB"];
    var inner;
    if (state === "filled") inner = '<div class="drawing">' + draw(p, { label: label }) + '</div><div class="slot__file"><span>' + file.join(" · ") + '</span><span class="slot__btns"><button class="btn btn--ghost" type="button">Replace</button><button class="btn btn--ghost" type="button" data-remove="' + which + '">Remove</button></span></div>';
    else if (state === "uploading") inner = '<div class="slot__prog"><div style="display:flex;justify-content:space-between"><b style="font-weight:500">' + file[0] + '</b><span class="muted" data-pct>64%</span></div><div class="bar" role="progressbar" aria-label="Uploading ' + file[0] + '" aria-valuenow="64" aria-valuemin="0" aria-valuemax="100"><span style="--p:64%" data-bar></span></div><button class="btn btn--ghost" type="button" style="justify-self:start;margin-left:-12px">Cancel upload</button></div>';
    else if (state === "error") inner = '<div class="slot__drop is-err" role="alert">' + I.warn + '<b style="color:inherit">sketch.heic isn’t a PNG or JPEG.</b><span>Export it as PNG and drop it here again.</span><span><u>Choose another file</u></span></div>';
    else inner = '<div class="slot__drop" data-drop tabindex="0" role="button" aria-label="' + label + ': drop an image or browse">' + I.up + '<b>Drop an image or <u>browse</u></b><span>PNG or JPEG · shown at 8:5 (output 512 × 320)</span></div>';
    return '<section class="slot" aria-label="' + label + '"><div class="slot__head"><h2>' + label + "</h2>" + (state === "filled" ? '<span class="pill pill--done">' + STATUS.done.icon + "Ready</span>" : "") + "</div>" + inner + "</section>";
  }
  function s3(st) {
    var a = { "both ready": ["filled", "filled"], empty: ["empty", "empty"], uploading: ["filled", "uploading"], "wrong file": ["filled", "error"] }[st];
    var ok = a[0] === "filled" && a[1] === "filled";
    var why = ok ? "" : a[1] === "uploading" ? "Waiting for the end drawing to finish uploading." : a[1] === "error" ? "The end drawing needs a PNG or JPEG." : "Add both drawings to continue.";
    var end = '<span class="btop__why">' + why + '</span><button class="btn" type="button" data-continue' + (ok ? "" : " disabled") + ">Continue to motion " + I.next + "</button>";
    var panel = '<div class="panel__group"><h2>Two drawings</h2><p class="help" style="color:var(--muted)">The first and the last frame of your clip. Cue draws the fourteen in between.</p></div>' +
      '<div class="panel__group"><h2>What works</h2><ul class="req"><li><span>Format</span><span>PNG, JPEG</span></li><li><span>Shown at</span><span>8:5</span></li><li><span>Output</span><span>512 × 320</span></li><li><span>Size limit</span><span class="dash">to be set</span></li></ul></div>' +
      '<div class="panel__group"><h2>Same character</h2><p class="help">Both drawings should show the same character, at the same scale, on a plain background.</p></div>';
    var canvas = '<div class="slots">' + slot("start", a[0]) + '<div class="link"><span></span><button class="btn" type="button" aria-label="Swap start and end"' + (ok ? "" : " disabled") + ' data-swap>' + I.swap + "</button><span></span></div>" + slot("end", a[1]) + "</div>" +
      '<div class="canvas__foot"><a class="btn btn--ghost" href="#s2">' + I.back + " Back to Library</a><span>" + (ok ? "Both drawings ready" : "") + "</span></div>";
    return { html: builder("New animation", 0, end, panel, canvas), after: function () {
      var c = $("[data-continue]"); if (c) c.addEventListener("click", function () { go("s4", "not approved"); });
      $$("[data-remove]").forEach(function (b) { b.addEventListener("click", function () { go("s3", "empty"); }); });
      var sw = $("[data-swap]"); if (sw) sw.addEventListener("click", function () { toast("Drawings swapped"); });
      $$("[data-drop]").forEach(function (d) {
        ["dragenter", "dragover"].forEach(function (ev) { d.addEventListener(ev, function (e) { e.preventDefault(); d.classList.add("is-over"); }); });
        ["dragleave", "drop"].forEach(function (ev) { d.addEventListener(ev, function (e) { e.preventDefault(); d.classList.remove("is-over"); if (ev === "drop") go("s3", "uploading"); }); });
        d.addEventListener("click", function () { go("s3", "uploading"); });
        d.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go("s3", "uploading"); } });
      });
      var bar = $("[data-bar]"), pct = $("[data-pct]");
      if (bar) { var p = 64; every(function () { p = Math.min(100, p + 9); bar.style.setProperty("--p", p + "%"); pct.textContent = p + "%"; if (p === 100) later(function () { go("s3", "both ready"); }, 300); }, 320); }
    } };
  }

  /* ================= S4 motion plan ================= */
  var REG = { gaze: "Gaze", head: "Head", smile: "Expression", hand: "Hand" };
  var SPEED = { slow: "slowly", normal: "normal speed", fast: "quickly" };
  function colWord(i, n) { return n === 1 ? "Together" : i === 0 ? "First" : i === n - 1 ? "Last" : "Then"; }
  function lanesHtml(plan) {
    var n = plan.steps.length, order = [], laneOrder = ["gaze", "head", "smile", "hand"];
    plan.steps.forEach(function (st, si) { st.events.forEach(function (e) { order.push({ si: si, e: e }); }); });
    order.sort(function (a, b) { return a.si - b.si || laneOrder.indexOf(a.e.region) - laneOrder.indexOf(b.e.region); });
    order.forEach(function (o, i) { o.n = i + 1; });
    var h = '<div class="lane lane--head" style="--cols:' + n + '"><div></div>';
    for (var i = 0; i < n; i++) {
      var together = plan.steps[i].events.length > 1;
      h += "<div>" + colWord(i, n) + (together ? ' <span class="together">· together</span>' : "") + "</div>";
    }
    h += "</div>";
    laneOrder.forEach(function (reg) {
      var mine = order.filter(function (o) { return o.e.region === reg; });
      h += '<div class="lane" style="--cols:' + n + '"><div class="lane__name">' + REG[reg] + "</div>";
      if (!mine.length) h += reg === "hand" ? '<div class="lane__cell lane__cell--none" style="grid-column:2/-1">No change</div>' : '<div class="lane__cell lane__cell--follow" style="grid-column:2/-1"><span>Follows the drawings across the clip</span></div>';
      else for (var c = 0; c < n; c++) {
        h += '<div class="lane__cell">';
        mine.filter(function (o) { return o.si === c; }).forEach(function (o) {
          h += '<div class="cue' + (o.e.added ? " cue--added" : "") + '" data-n="' + o.n + '"><span class="cue__n">' + o.n + '</span><span><span class="cue__a">' + esc(o.e.action) + '</span><span class="cue__s">' + (o.e.added ? "added by Cue" : SPEED[o.e.speed]) + "</span></span></div>";
        });
        h += "</div>";
      }
      h += "</div>";
    });
    var list = order.map(function (o) { return "<li>" + colWord(o.si, n) + ": " + esc(o.e.action.toLowerCase()) + ", " + (o.e.added ? "added by Cue" : SPEED[o.e.speed]) + "</li>"; }).join("");
    var cueList = order.map(function (o) { return '<li class="cue' + (o.e.added ? " cue--added" : "") + '"><span class="cue__n">' + o.n + '</span><span><span class="cue__a">' + colWord(o.si, n) + ": " + esc(o.e.action) + '</span><span class="cue__s">' + REG[o.e.region] + " · " + (o.e.added ? "added by Cue" : SPEED[o.e.speed]) + "</span></span></li>"; }).join("");
    return { lanes: h, list: list, cueList: cueList, count: order.length };
  }
  function s4(st) {
    var text = st === "refused" ? "Turn the head to the right and smile." : st === "no instruction" ? "" : st === "out of date" ? (customText || C.EXAMPLES[0]) + " Wave too." : (customText || C.EXAMPLES[0]);
    var plan = C.parseInstruction(st === "out of date" ? (customText || C.EXAMPLES[0]) : text);
    var approved = st === "approved";
    var canGo = approved || st === "no instruction";
    var why = canGo ? (st === "no instruction" ? "Drawings-only run" : "Plan approved") : st === "refused" ? "Change the instruction to get a plan." : st === "reading" ? "Reading your instruction…" : st === "out of date" ? "The plan is out of date. Preview it again." : "Approve the plan to generate.";
    var end = '<span class="btop__why">' + why + '</span><a class="btn btn--ghost" href="#s3/both ready">Change drawings</a><span class="btop__sep" aria-hidden="true"></span><button class="btn btn--primary" type="button" data-generate' + (canGo ? "" : " disabled") + ">Generate animation</button>";
    var panel = '<div class="panel__group"><div class="field"><label for="instr">Describe the motion <span class="muted" style="font-weight:400">(optional)</span></label>' +
      '<textarea class="textarea" id="instr" maxlength="280" aria-describedby="instr-h" placeholder="First move the eyes to the left, then turn the head slowly.">' + esc(text) + "</textarea>" +
      '<p class="help" id="instr-h">Describe the order of movements in English. Leave it empty to generate from the drawings only.</p><p class="count"><span data-count>' + text.length + "</span> / 280</p></div></div>" +
      '<div class="panel__group"><h2>Examples</h2><div class="chips">' + C.EXAMPLES.map(function (e, i) { return '<button type="button" class="chip" data-ex="' + i + '">' + esc(e) + "</button>"; }).join("") + "</div></div>" +
      '<div class="panel__group"><button class="btn" type="button" data-preview style="width:100%"' + (st === "reading" ? " disabled" : "") + ">" + (st === "reading" ? '<span class="spinner" aria-hidden="true"></span>Reading…' : "Preview plan") + "</button></div>" +
      (plan.ok && !plan.empty && st !== "reading" ? '<div class="panel__group"><label class="approve"><input type="checkbox" data-approve' + (approved ? " checked" : "") + (st === "out of date" ? " disabled" : "") + "><span><b>This plan is correct</b><span class=\"muted\">" + (st === "out of date" ? "Approval was cleared when the text changed." : "Required before generating.") + "</span></span></label></div>" : "");

    var card;
    if (st === "reading") card = '<div class="lanes" aria-busy="true">' + [0, 1, 2, 3].map(function () { return '<div class="skel skel-lane"></div>'; }).join("") + '</div><p class="help" style="margin-top:12px">Reading your instruction…</p>';
    else if (!plan.ok) card = '<div class="alert alert--warn" role="alert"><strong>Cue couldn’t turn this into a plan.</strong>' + esc(plan.reason) + '<div class="alert__actions"><button class="btn" type="button" data-try>Try: “' + esc(plan.suggestion) + "”</button></div></div>";
    else if (plan.empty) card = '<div class="alert alert--neu"><strong>No instruction, no plan.</strong>Cue will move the eyes, the head and the expression together from the first drawing to the last. That’s a drawings-only run.</div>';
    else {
      var L = lanesHtml(plan);
      card = '<div class="lanes' + (st === "out of date" ? " is-stale" : "") + '" data-lanes>' + L.lanes + "</div>" +
        '<ol class="plan__order plan__order--cues" style="gap:6px" aria-hidden="true">' + L.cueList + "</ol>" +
        '<details style="margin-top:14px"><summary class="muted" style="cursor:pointer">Read the plan as a list</summary><ol class="plan__order">' + L.list + "</ol></details>" +
        (plan.added.length ? '<p class="help" style="margin-top:10px">' + plan.added.map(esc).join(" ") + "</p>" : "");
    }
    var head = '<div class="plancard__head"><h2>Plan</h2><span class="muted">' + (st === "out of date" ? '<span class="pill pill--draft">Out of date</span>' : plan.ok && !plan.empty && st !== "reading" ? "Order shown, not exact timing" : "") + "</span></div>";
    var canvas = '<div class="pair"><div class="drawing">' + draw(C.START, { width: 3.2, label: "Start drawing" }) + '</div><span class="pair__arrow">' + I.arrow + '</span><div class="drawing">' + draw(C.END, { width: 3.2, label: "End drawing" }) + '</div><span class="pair__text">start_front.png → end_left_smile.png</span></div>' +
      '<section class="plancard" aria-label="Plan">' + head + card + "</section>";
    return { html: builder("New animation", 1, end, panel, canvas), after: function () {
      var ta = $("#instr"), cnt = $("[data-count]");
      ta.addEventListener("input", function () {
        cnt.textContent = ta.value.length;
        var l = $("[data-lanes]"); if (l) l.classList.add("is-stale");
        var ap = $("[data-approve]"); if (ap) { ap.checked = false; ap.disabled = true; }
        var g = $("[data-generate]"); if (g && ta.value.trim()) g.disabled = true;
      });
      $$("[data-ex]").forEach(function (b) { b.addEventListener("click", function () { ta.value = C.EXAMPLES[+b.getAttribute("data-ex")]; ta.dispatchEvent(new Event("input")); }); });
      var pv = $("[data-preview]");
      if (pv) pv.addEventListener("click", function () {
        var v = ta.value.trim();
        go("s4", "reading");
        later(function () {
          var p = C.parseInstruction(v);
          var next = !v ? "no instruction" : !p.ok ? "refused" : "not approved";
          if (v && p.ok) customText = v;
          go("s4", next);
        }, 700);
      });
      var ap = $("[data-approve]"); if (ap) ap.addEventListener("change", function () { go("s4", ap.checked ? "approved" : "not approved"); });
      var tr = $("[data-try]"); if (tr) tr.addEventListener("click", function () { go("s4", "not approved"); });
      var g = $("[data-generate]"); if (g) g.addEventListener("click", function () { go("s5", "queued"); later(function () { if (route().sc.id === "s5") go("s5", "running"); }, 1600); });
      // cues arrive in reading order, once per new plan
      if (!reduce && (st === "not approved") ) {
        var cues = $$(".lanes .cue").sort(function (a, b) { return a.getAttribute("data-n") - b.getAttribute("data-n"); });
        cues.forEach(function (c) { c.classList.add("is-entering"); });
        if (cues.length) cues[0].offsetWidth;
        cues.forEach(function (c, i) { c.style.transitionDelay = Math.min(i * 60, 360) + "ms"; c.classList.remove("is-entering"); });
      }
    } };
  }
  var customText = null;

  /* ================= S5 generation ================= */
  function planSummary(j) {
    if (!j.plan.ok || j.plan.empty) return '<p class="muted">No instruction: a drawings-only run.</p>';
    var L = [], n = 0;
    j.plan.steps.forEach(function (st, si) { st.events.forEach(function (e) { L.push('<li><span class="cue__n">' + ++n + "</span><span>" + colWord(si, j.plan.steps.length) + ": " + esc(e.action.toLowerCase()) + ' <span class="muted">· ' + (e.added ? "added by Cue" : SPEED[e.speed]) + "</span></span></li>"); }); });
    return '<ol class="plist">' + L.join("") + "</ol>";
  }
  function s5(st) {
    var j = st === "failed" ? FAILED : st === "cancelled" ? CANCELLED : st === "queued" ? QUEUED : st === "done" ? DONE : RUNNING;
    var ticks = ""; for (var i = 0; i < 16; i++) ticks += '<span class="' + (i === 0 || i === 15 ? "k" : st === "done" ? "f" : "") + '" style="--i:' + i + '"></span>';
    var big = { running: "Generating 16 frames.", queued: "Waiting for the GPU worker.", done: "All 16 frames are ready.", failed: "This animation failed.", cancelled: "You cancelled this animation." }[st];
    var timeHtml = st === "running" ? '<span>Elapsed<b data-elapsed>' + dur(ELAPSED0) + "</b></span>" : st === "queued" ? "<span>Waiting<b data-elapsed>29 s</b></span>" : st === "done" ? "<span>Took<b>" + dur(DONE.took) + "</b></span>" : "";
    var main = '<section class="card ' + (st === "running" ? "is-running" : "") + '" aria-label="Status">' +
      '<div class="statusline"><p class="statusline__big" role="status">' + big + '</p><p class="statusline__time">' + timeHtml + "</p></div>" +
      (st === "failed" ? '<div class="alert alert--neg" role="alert" style="margin-bottom:18px"><strong>' + esc(j.reason) + "</strong>Your drawings and instruction are kept. Start a new animation with them, or try again later." + '<div class="alert__actions"><a class="btn" href="#s2">Back to Library</a><a class="btn" href="#s3/both ready">Start a new animation</a></div></div>' : "") +
      (st === "cancelled" ? '<div class="alert alert--neu" style="margin-bottom:18px"><strong>Nothing more will be generated.</strong>The drawings stay in your library with this entry.<div class="alert__actions"><a class="btn" href="#s2">Back to Library</a><a class="btn" href="#s3/both ready">Start a new animation</a></div></div>' : "") +
      '<div class="genstage"><figure><figcaption>Start drawing · frame 1</figcaption><div class="drawing">' + draw(C.START, { width: 3, label: "Start drawing" }) + '</div></figure>' +
      '<div class="ticks-wrap"><div class="ticks" aria-hidden="true">' + ticks + '</div><div class="ticks__labels"><span>1</span><span>' + (st === "running" ? "frames 2–15 in progress" : st === "done" ? "16 frames" : st === "queued" ? "not started" : "stopped") + "</span><span>16</span></div></div>" +
      '<figure><figcaption>End drawing · frame 16</figcaption><div class="drawing">' + draw(C.END, { width: 3, label: "End drawing" }) + "</div></figure></div>" +
      (st === "running" || st === "queued" ? '<p class="note">' + I.info + "Leaving this page doesn’t stop the job. The Library card keeps updating.</p>" : "") +
      (st === "done" ? '<div style="margin-top:18px;display:flex;justify-content:flex-end"><a class="btn btn--primary btn--lg" href="#s6">View result</a></div>' : "") +
      "</section>";
    var side = '<section class="card"><h2>Plan used</h2>' + planSummary(j) + "</section>" +
      '<section class="card"><h2>Run details</h2><dl class="kv">' +
        "<div><dt>Job</dt><dd class=\"mono\">" + j.id + "</dd></div>" +
        "<div><dt>Submitted</dt><dd>" + fmtDate(j.created) + "</dd></div>" +
        "<div><dt>Model</dt><dd>" + esc(j.model) + "</dd></div>" +
        "<div><dt>Seed</dt><dd>" + (st === "queued" || st === "cancelled" ? '<span class="dash" title="Known once the worker starts">—</span>' : j.seed) + "</dd></div>" +
        "<div><dt>Queue position</dt><dd><span class=\"dash\" title=\"Not reported by the API\">—</span></dd></div>" +
      "</dl></section>";
    var acts = st === "running" || st === "queued" ? '<button class="btn btn--danger" type="button" data-cancel>Cancel generation</button>' : "";
    var head = '<div class="dhead"><div class="dhead__l"><a class="dhead__parent" href="#s2">Library</a><span class="slash">/</span><h1>' + esc(j.title) + "</h1>" + pill(st) + '</div><div class="titlerow__acts">' + acts + "</div></div>" +
      '<div class="tabs" role="tablist"><button role="tab" aria-selected="true" type="button">Status</button><button role="tab" aria-selected="false" type="button" disabled>Result</button></div>';
    var body = head + '<div class="dgrid"><div class="dmain">' + main + '</div><aside class="dside">' + side + "</aside></div>";
    return { html: shell("lib", '<a href="#s2">Library</a><span>/</span><b>' + esc(j.title) + "</b>", body), after: function () {
      bindShell();
      var el = $("[data-elapsed]"), e = st === "queued" ? 29 : ELAPSED0;
      if (el && (st === "running" || st === "queued")) every(function () { e++; el.textContent = dur(e); }, 1000);
      var c = $("[data-cancel]");
      if (c) c.addEventListener("click", function () {
        var s = document.createElement("div"); s.className = "scrim";
        s.innerHTML = '<div class="dialog" role="alertdialog" aria-modal="true" aria-labelledby="dc-t"><h2 id="dc-t">Cancel this generation?</h2><p>Frames made so far are discarded. Your drawings and instruction are kept.</p><div class="dialog__acts"><button class="btn" type="button" data-no>Keep generating</button><button class="btn btn--destructive" type="button" data-yes>Cancel generation</button></div></div>';
        document.body.appendChild(s); $("[data-no]", s).focus();
        $("[data-no]", s).addEventListener("click", function () { s.remove(); c.focus(); });
        s.addEventListener("keydown", function (ev) { if (ev.key === "Escape") { s.remove(); c.focus(); } });
        $("[data-yes]", s).addEventListener("click", function () { s.remove(); go("s5", "cancelled"); });
      });
    } };
  }

  /* ================= S6 result ================= */
  function s6(st) {
    var j = DONE;
    var scrub = ""; for (var i = 0; i < 16; i++) scrub += '<button type="button" class="' + (i === 0 || i === 15 ? "k" : "") + '" data-f="' + i + '" aria-label="Frame ' + (i + 1) + (i === 0 || i === 15 ? ", your drawing" : "") + '"></button>';
    var player = st === "video failed"
      ? '<div class="screen" style="display:grid;place-items:center;background:var(--raised)"><div class="alert alert--neg" role="alert" style="max-width:420px"><strong>The video couldn’t be loaded.</strong>The file is still on the server. Reload the player, or download it directly.<div class="alert__actions"><button class="btn" type="button" data-reload>Reload</button><button class="btn" type="button" data-dl2>Download MP4</button></div></div></div>'
      : '<div class="screen" data-screen tabindex="0" aria-label="Result player. Space plays, arrow keys step a frame.">' + draw(j.frames[0], { label: "Frame 1" }) + '<span class="screen__tag" data-tag>Frame 1 · your drawing</span></div>' +
        '<div class="controls"><button class="btn btn--icon playbtn" type="button" data-play aria-label="Play"><span class="i-play">' + I.play + '</span><span class="i-pause">' + I.pause + "</span></button>" +
        '<button class="btn btn--icon" type="button" data-step="-1" aria-label="Previous frame">' + I.back + '</button><button class="btn btn--icon" type="button" data-step="1" aria-label="Next frame">' + I.next + "</button>" +
        '<span class="controls__count" data-count>Frame 1 of 16</span><span class="controls__end"><label class="toggle"><input type="checkbox" data-loop checked> Loop</label></span></div>' +
        '<div class="scrubber" data-scrub role="group" aria-label="Frames">' + scrub + '</div><div class="scrub__labels"><span>Your drawing</span><span>Your drawing</span></div>';
    var main = '<section class="player">' + player + "</section>";
    var side = '<section class="card"><h2>What was used</h2><dl class="kv">' +
        '<div><dt>Instruction</dt><dd class="l">' + esc(j.cmd) + "</dd></div>" +
        "<div><dt>Model</dt><dd>" + esc(j.model) + "</dd></div>" +
        "<div><dt>Seed</dt><dd>" + j.seed + "</dd></div>" +
        "<div><dt>Generation</dt><dd>" + dur(j.took) + "</dd></div>" +
        "<div><dt>Created</dt><dd>" + fmtDate(j.created) + "</dd></div>" +
        "<div><dt>File</dt><dd>MP4 · 512 × 320 · " + j.kb + " KB</dd></div>" +
        '<div><dt>Job</dt><dd class="mono">' + j.id + "</dd></div>" +
      "</dl></section>" +
      '<section class="card"><h2>Plan</h2>' + planSummary(j) + "</section>";
    var acts = '<a class="btn" href="#s3/empty">' + I.plus + 'New animation</a><button class="btn btn--primary" type="button" data-dl>' + I.dl + "Download MP4</button>";
    var head = '<div class="dhead"><div class="dhead__l"><a class="dhead__parent" href="#s2">Library</a><span class="slash">/</span><h1>' + esc(j.title) + "</h1>" + pill("done") + '</div><div class="titlerow__acts">' + acts + "</div></div>" +
      '<div class="tabs" role="tablist"><button role="tab" aria-selected="false" type="button" data-tab-status>Status</button><button role="tab" aria-selected="true" type="button">Result</button></div>';
    var body = head + '<div class="dgrid"><div class="dmain">' + main + '</div><aside class="dside">' + side + "</aside></div>";
    return { html: shell("lib", '<a href="#s2">Library</a><span>/</span><b>' + esc(j.title) + "</b>", body), after: function () {
      bindShell();
      var ts = $("[data-tab-status]"); if (ts) ts.addEventListener("click", function () { go("s5", "done"); });
      $$("[data-dl], [data-dl2]").forEach(function (b) { b.addEventListener("click", function () { toast("Mockup: no file is downloaded"); }); });
      var rl = $("[data-reload]"); if (rl) rl.addEventListener("click", function () { go("s6", "ready"); });
      var scr = $("[data-screen]"); if (!scr) return;
      var cur = 0, tm = null, hold = 0;
      var playB = $("[data-play]"), loop = $("[data-loop]"), cnt = $("[data-count]"), tag = $("[data-tag]");
      function show(i) {
        cur = (i + 16) % 16;
        scr.firstElementChild.outerHTML = draw(j.frames[cur], { label: "Frame " + (cur + 1) });
        cnt.textContent = "Frame " + (cur + 1) + " of 16";
        tag.textContent = "Frame " + (cur + 1) + (cur === 0 || cur === 15 ? " · your drawing" : "");
        $$("[data-f]").forEach(function (b, k) { b.setAttribute("aria-current", String(k === cur)); b.classList.toggle("past", k < cur && k !== 0); });
      }
      function pause() { clearInterval(tm); tm = null; playB.classList.remove("is-playing"); playB.setAttribute("aria-label", "Play"); }
      function play() {
        if (cur === 15) show(0);
        playB.classList.add("is-playing"); playB.setAttribute("aria-label", "Pause");
        tm = setInterval(function () {
          if (cur === 15) { if (!loop.checked) { pause(); return; } if (hold++ < 3) return; hold = 0; }
          show(cur + 1);
        }, 167);
        timers.push(tm);
      }
      playB.addEventListener("click", function () { tm ? pause() : play(); });
      $$("[data-step]").forEach(function (b) { b.addEventListener("click", function () { pause(); show(cur + +b.getAttribute("data-step")); }); });
      $$("[data-f]").forEach(function (b) { b.addEventListener("click", function () { pause(); show(+b.getAttribute("data-f")); }); });
      // keyboard: Space plays, arrows step. Frame steps are instant (no animation on a keyboard action).
      scr.closest(".player").addEventListener("keydown", function (e) {
        if (e.target.matches("input")) return;
        if (e.key === " ") { e.preventDefault(); tm ? pause() : play(); }
        if (e.key === "ArrowLeft" || e.key === "ArrowRight") { e.preventDefault(); pause(); show(cur + (e.key === "ArrowLeft" ? -1 : 1)); }
      });
      show(0);
    } };
  }

  /* ================= render ================= */
  var R = { s1: s1, s2: s2, s3: s3, s4: s4, s5: s5, s6: s6 };
  var scSel = document.getElementById("mock-screen"), stSel = document.getElementById("mock-state");
  scSel.innerHTML = SCREENS.map(function (s) { return '<option value="' + s.id + '">' + s.name + "</option>"; }).join("");
  scSel.addEventListener("change", function () { go(scSel.value); });
  stSel.addEventListener("change", function () { go(scSel.value, stSel.value); });

  function render() {
    clearTimers();
    $$(".scrim, .toast").forEach(function (n) { n.remove(); });
    var r = route();
    scSel.value = r.sc.id;
    stSel.innerHTML = r.sc.states.map(function (s) { return "<option" + (s === r.st ? " selected" : "") + ">" + s + "</option>"; }).join("");
    var out = R[r.sc.id](r.st);
    app.innerHTML = out.html;
    document.title = "Cue — " + r.sc.name.split(" · ")[1] + " (mockup)";
    if (out.after) out.after();
  }
  window.addEventListener("hashchange", render);
  render();
})();
