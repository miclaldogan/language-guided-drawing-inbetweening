const app = document.querySelector('#app');
const toast = document.querySelector('#toast');
let specimenIndex = 0;

const state = {
  authTab: 'login',
  files: { start: null, end: null },
  prompt: '',
  plan: null,
  approved: false,
  jobStatus: 'queued',
  activeFrame: 1,
  playing: false,
  line: { pitch: 18, warp: 52, speed: 32 },
  pointer: { x: .52, y: .45 }
};

const specimens = {
  sprout: { title: 'A stem turns toward light', motif: 'leaf' },
  profile: { title: 'A face meets the window', motif: 'profile' },
  bloom: { title: 'A seed opens', motif: 'bloom' }
};

function route() {
  const raw = window.location.hash.replace(/^#\/?/, '');
  return raw || 'home';
}

function go(next) {
  if (route() === next) { render(); return; }
  window.location.hash = `/${next}`;
}

function mark() {
  return '<span class="logo-mark" aria-hidden="true"><i></i><i></i><i></i><i></i></span>';
}

function wordmark() {
  return `<a class="wordmark" href="#/home" aria-label="Cue home">${mark()}<span>Cue</span></a>`;
}

function icon(name) {
  const paths = {
    arrow: '<path d="M5 12h14M13 5l7 7-7 7"/>',
    upload: '<path d="M12 16V4m0 0L7 9m5-5 5 5M4 15v4h16v-4"/>',
    leaf: '<path d="M20 4c-8 0-14 3-14 10a6 6 0 0 0 6 6c7 0 8-8 8-16ZM5 20c3-5 6-8 11-11"/>',
    play: '<path d="m8 5 12 7-12 7z"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    swap: '<path d="M7 7h13l-3-3m3 3-3 3M17 17H4l3 3m-3-3 3-3"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
    pause: '<path d="M8 5v14m8-14v14"/>',
    download: '<path d="M12 4v11m0 0 5-5m-5 5-5-5M4 20h16"/>',
    more: '<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>',
    back: '<path d="M19 12H5m7 7-7-7 7-7"/>'
  };
  return `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name] || ''}</svg>`;
}

function botanicalArt({ small = false, alternate = 0 } = {}) {
  const instance = specimenIndex++;
  const cls = small ? 'specimen-svg specimen-svg--small' : 'specimen-svg';
  const shift = alternate % 3;
  const stem = shift === 1 ? 'M244 494c3-105-5-180-54-288' : shift === 2 ? 'M244 494c12-110 31-186 90-290' : 'M244 494c0-117 0-198 0-305';
  const budX = shift === 1 ? 189 : shift === 2 ? 334 : 244;
  return `<svg xmlns="http://www.w3.org/2000/svg" class="${cls}" viewBox="0 0 480 560" role="img" aria-label="Engraved botanical study, frame ${shift + 1}">
    <defs><pattern id="hatch-${instance}" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(18)"><path d="M0 0v6M3 0v6" stroke="#4B2834" stroke-opacity=".26" stroke-width=".7"/></pattern><pattern id="fine-${instance}" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" stroke="#4B2834" stroke-opacity=".08" stroke-width=".6"/></pattern></defs>
    <rect width="480" height="560" fill="#F4EBDD"/><rect width="480" height="560" fill="url(#fine-${instance})"/>
    <path d="M24 24h432v512H24z" fill="none" stroke="#4B2834" stroke-opacity=".3"/><path d="M34 34h412v492H34z" fill="none" stroke="#4B2834" stroke-opacity=".12"/>
    <path d="M64 462c54-7 101-9 153-5 73 5 126 2 200-12" stroke="#4B2834" stroke-opacity=".5" stroke-width="1" fill="none"/>
    <g transform="translate(-14 0) translate(244 494) scale(.8) translate(-244 -494)">
    <path d="${stem}" fill="none" stroke="#4B2834" stroke-width="3" stroke-linecap="round"/>
    <path d="M242 421c-68-33-106-85-128-159M243 369c60-21 109-67 141-135M241 309c-47-28-70-72-81-119M244 272c53-19 86-54 108-98" fill="none" stroke="#4B2834" stroke-width="2" stroke-linecap="round"/>
    <path d="M119 264c-61-11-91-44-97-97 53 4 87 31 97 97Zm-8-22c21-63 61-93 120-90-14 56-52 85-120 90Zm274-8c38-57 81-77 130-64-27 49-68 70-130 64Zm-73-42c3-61 34-99 91-115 7 55-22 94-91 115Zm-125 42c-3-55 23-91 70-109 4 51-18 87-70 109Z" fill="#F4EBDD" stroke="#4B2834" stroke-width="2" stroke-linejoin="round"/>
    <path d="M119 264c-61-11-91-44-97-97 53 4 87 31 97 97Zm-8-22c21-63 61-93 120-90-14 56-52 85-120 90Zm274-8c38-57 81-77 130-64-27 49-68 70-130 64Zm-73-42c3-61 34-99 91-115 7 55-22 94-91 115Z" fill="url(#hatch-${instance})" opacity=".8"/>
    <path d="M${budX} 189c-22-36-16-75 4-103 20 28 26 67 4 103-3 5-5 9-4 14-1-5-3-9-4-14Z" fill="#91AA8A" stroke="#4B2834" stroke-width="2"/>
    <path d="M244 186c-33-12-49-35-48-64 31 6 49 26 48 64Zm2-24c20-31 47-42 73-32-12 29-37 41-73 32Z" fill="#91AA8A" stroke="#4B2834" stroke-width="1.6"/>
    <path d="M89 130c30 25 52 57 62 93M364 117c-21 24-41 54-52 90M170 239c-12 21-27 38-45 51" fill="none" stroke="#4B2834" stroke-opacity=".6" stroke-width="1"/></g>
    <path d="M56 442c80-26 179-31 285-8M63 451c91-25 180-26 288-2M81 430c74-26 159-32 230-22" fill="none" stroke="#4B2834" stroke-opacity=".5" stroke-width="1"/>
    <path d="M49 497h382M49 491v12m38-7v7m38-7v7m38-7v7m38-12v12m38-7v7m38-7v7m38-7v7m38-7v7m38-12v12" stroke="#D39A62" stroke-width="1.5"/>
    <g fill="#4B2834" font-family="monospace" font-size="10" letter-spacing="1"><text x="50" y="57">CUE / SPECIMEN ${String(shift + 1).padStart(2, '0')}</text><text x="430" y="57" text-anchor="end">MOTION PLATE</text><text x="49" y="520">START</text><text x="430" y="520" text-anchor="end">STUDY 0${shift + 1}</text></g>
    <path d="M39 39h22M39 39v22m402-22h-22m22 0v22M39 521h22m-22 0v-22m402 22h-22m22 0v-22" fill="none" stroke="#D39A62" stroke-width="1.4"/>
  </svg>`;
}

function framesStrip({ active = 1, mode = 'static' } = {}) {
  return `<div class="frame-strip frame-strip--${mode}" aria-label="16 frame sequence">${Array.from({ length: 16 }, (_, i) => `<i style="--n:${i}" ${mode === 'scrub' ? `role="button" tabindex="0" data-tick="${i + 1}" aria-label="Frame ${i + 1}"` : ''} class="${i === 0 || i === 15 ? 'endpoint' : ''} ${i + 1 === active ? 'current' : ''}" ${i + 1 === active ? 'aria-current="true"' : ''}></i>`).join('')}</div>`;
}

function header({ active = '', landing = false } = {}) {
  if (landing) return `<header class="public-nav">${wordmark()}<nav><a href="#process">The approach</a><a href="#principles">Principles</a><a href="#/signin">Sign in</a></nav><a class="button button--copper button--small" href="#/library">Enter the studio ${icon('arrow')}</a><button class="mobile-menu" aria-label="Open navigation">${icon('more')}</button></header>`;
  return `<header class="app-nav">${wordmark()}<nav class="app-nav__links" aria-label="Studio"><a href="#/library" class="${active === 'library' ? 'is-active' : ''}">Library</a><a href="#/keyframes" class="${['keyframes','plan','status','result'].includes(active) ? 'is-active' : ''}">New animation</a></nav><div class="app-nav__right"><span class="account-mark">A</span><span class="account-name">A. Morgan</span><button class="account-menu" aria-label="Account menu">${icon('more')}</button></div></header>`;
}

function stepper(active) {
  const steps = [['keyframes','Keyframes'],['plan','Motion plan'],['status','Generate'],['result','Result']];
  const index = steps.findIndex(([key]) => key === active);
  return `<nav class="stepper" aria-label="Animation steps">${steps.map(([key,label], i) => `<a href="#/${key}" class="stepper__step ${i < index ? 'is-done' : ''} ${i === index ? 'is-current' : ''}" ${i === index ? 'aria-current="step"' : ''}><span class="stepper__number">${i < index ? icon('check') : `0${i + 1}`}</span><span>${label}</span></a>`).join('<span class="stepper__rule"></span>')}</nav>`;
}

function appShell(screen, content, { workflow = false } = {}) {
  return `<div class="app-shell">${header({ active: screen })}<main class="app-main">${workflow ? stepper(screen) : ''}${content}</main><footer class="app-footer"><span>Cue</span><a href="#/lab">Line study</a></footer></div>`;
}

function homePage() {
  return `<div class="landing">${header({ landing: true })}
    <main>
      <section class="landing-hero">
        <div class="landing-hero__copy"><p class="eyebrow eyebrow--light"><span class="eyebrow-mark">✳</span> Drawing and motion</p><h1>Draw what<br />happens <em>between.</em></h1><p class="landing-lede">Two drawings hold the beginning and the end. Cue gives shape to everything in between.</p><div class="landing-actions"><a class="button button--copper" href="#/library">Enter the studio ${icon('arrow')}</a><a class="link-light" href="#process">A short introduction <span>↓</span></a></div></div>
        <div class="landing-art"><div class="hero-plate">${botanicalArt()}</div></div>
        
      </section>
      <section class="intro-strip" id="principles"><p class="eyebrow"><span>An open studio for</span></p><p>Slow looking. Precise marks.<br /><em>Unexpected movement.</em></p><span class="intro-note">Start · End · What can happen</span></section>
      <section class="process-section" id="process"><div class="process-heading"><p class="eyebrow"><span>The method</span> · three moments</p><h2>There is a world<br />inside the <em>interval.</em></h2><p>Begin with the drawings. Describe a movement, or leave the interpretation open. Review the plan before a single frame is made.</p><a class="underlined-link" href="#/library">Make your first study ${icon('arrow')}</a></div><div class="process-list"><article><span class="process-number">01</span><div class="process-mini process-mini--pair"><i>${botanicalArt({small:true,alternate:0})}</i><b>→</b><i>${botanicalArt({small:true,alternate:2})}</i></div><h3>Choose two moments</h3><p>Place a start drawing and an end drawing on the worktable.</p></article><article><span class="process-number">02</span><div class="process-mini process-mini--cues"><i></i><i></i><i></i></div><h3>Describe the change</h3><p>Give Cue an optional English instruction. Read and approve its ordered plan.</p></article><article><span class="process-number">03</span><div class="process-mini process-mini--frames">${framesStrip({mode:'static'})}</div><h3>See what unfolds</h3><p>Review the intermediate frames, then play or export your short clip.</p></article></div></section>
      <section class="quote-band"><span></span><p>“A drawing is a record of attention.<br /><em>Movement lets it continue.”</em></p><span></span><svg viewBox="0 0 700 180" aria-hidden="true"><path d="M0 150c80-90 120-90 200 0s120 90 200 0 120-90 200 0 120 90 200 0"/></svg></section>
      <section class="landing-cta"><div><p class="eyebrow eyebrow--light"><span>Your worktable is ready</span></p><h2>Begin with a<br /><em>single line.</em></h2></div><a href="#/library" class="button button--paper">Open the studio ${icon('arrow')}</a></section>
    </main><footer class="public-footer"><span>Cue</span><a href="#/lab">Line study</a></footer></div>`;
}

function signInPage() {
  const create = state.authTab === 'create';
  return `<div class="auth-layout"><aside class="auth-art"><a class="auth-wordmark" href="#/home">${wordmark()}</a><div class="auth-art__quote"><p>Two drawings in.<br /><em>A little more life out.</em></p></div><div class="auth-specimen">${botanicalArt({small:false,alternate:1})}</div><a class="auth-back" href="#/home">← Back to Cue</a></aside><main class="auth-form-wrap"><div class="auth-form"><div class="auth-tabs" role="tablist" aria-label="Account"><button data-auth="login" class="${!create?'is-active':''}" role="tab" aria-selected="${!create}">Log in</button><button data-auth="create" class="${create?'is-active':''}" role="tab" aria-selected="${create}">Create account</button></div><h1>${create?'Make room':'Return to'}<br /><em>your work.</em></h1><p class="auth-intro">${create?'Create an account to keep your studies together.':'Your drawings and motion studies are waiting.'}</p><form id="auth-form"><label for="email">Email address</label><input id="email" type="email" autocomplete="email" placeholder="you@example.com" required /><label for="password">Password <span class="password-hint">${create?'Use at least 8 characters.':''}</span></label><div class="password-input"><input id="password" type="password" autocomplete="${create?'new-password':'current-password'}" placeholder="••••••••••" required minlength="${create?8:1}" /><button type="button" class="password-toggle" aria-label="Show password">Show</button></div><div class="form-alert" hidden role="alert"></div><button class="button button--copper button--wide" type="submit">${create?'Create account':'Log in'} ${icon('arrow')}</button><p class="auth-privacy">Your drawings stay private to your account.</p></form></div></main></div>`;
}

function jobCard(id, title, status, detail, artShift) {
  return `<article class="job-card"><button class="job-card__open" data-open-job="${status === 'done'?'result':'status'}" data-job-status="${status}" aria-label="Open ${title}"><div class="job-poster">${botanicalArt({small:true,alternate:artShift})}${status === 'done'?'<span class="poster-play">'+icon('play')+'</span>':''}</div><div class="job-card__body"><div class="job-card__meta"><span class="status status--${status}"><i></i>${status[0].toUpperCase()+status.slice(1)}</span><time>Oct 2${artShift + 1}, 2026</time></div><h3>${title}</h3><p>${detail}</p><div class="job-card__foot"><span>${id}</span><span class="job-open-arrow">↗</span></div></div></button><button class="job-menu" data-delete="${id}" aria-label="Delete ${title}">${icon('more')}</button></article>`;
}

function libraryPage() {
  return appShell('library', `<section class="page-heading page-heading--library"><div><h1>Your <em>animations.</em></h1><p>Every study, from first sketch to finished movement.</p></div><a class="button button--copper" href="#/keyframes">${icon('plus')} New animation</a></section><section class="library-tools"><span>Recent studies <b>3</b></span><span>Newest first</span></section><section class="job-grid">${jobCard('CU—024','A stem turns toward light','done','16 frames · 3.2 sec',0)}${jobCard('CU—023','A face meets the window','running','Submitted 4 minutes ago',1)}${jobCard('CU—022','A seed opens','failed','The worker stopped unexpectedly.',2)}</section><section class="library-note"><span></span><p>Studies are private to your account. Return to a running animation at any time; the work continues in the studio.</p><a href="#/keyframes">Start a new study ${icon('arrow')}</a></section>`, {});
}

function uploadSlot(which, label) {
  const file = state.files[which];
  return `<section class="upload-slot ${file?'has-file':''}" data-slot="${which}"><div class="upload-slot__head"><b>${label}</b><button class="slot-menu" type="button" aria-label="${file?'Replace':'Upload'} ${label}">${file?icon('more'):icon('plus')}</button></div><label class="upload-canvas" for="${which}-file">${file?`<img src="${file.url}" alt="Preview of ${file.name}" />`:`<div class="upload-placeholder">${botanicalArt({small:true,alternate:which==='start'?0:2})}<span class="upload-prompt"><i>${icon('upload')}</i><b>Drop an image or browse</b><small>Shown at 8:5 · PNG or JPEG</small></span></div>`}</label><input class="file-input" id="${which}-file" data-file-slot="${which}" type="file" accept="image/png,image/jpeg" /><div class="upload-slot__footer"><span>${file?`${file.name} · ${file.dimensions}`:'No drawing yet'}</span>${file?`<button data-remove-file="${which}">Remove</button>`:'<span>PNG or JPEG</span>'}</div></section>`;
}

function keyframesPage() {
  const canContinue = Boolean(state.files.start && state.files.end);
  return appShell('keyframes', `<section class="page-heading"><div><h1>Two moments, <em>one movement.</em></h1><p>Begin and end with the drawings. Cue will find the path between.</p></div></section><section class="upload-intro"><span class="upload-intro__rule"></span><p>Place the first drawing on the left and the final drawing on the right. Both images will be fitted to the same 8:5 frame.</p><button class="sample-pair" data-sample-pair type="button">Load sample drawings</button><button class="swap-button" data-swap type="button" aria-label="Swap start and end drawings">${icon('swap')} Swap order</button></section><div class="upload-pair">${uploadSlot('start','Start drawing')}<div class="pair-connector" aria-hidden="true"><i></i><b>→</b><i></i></div>${uploadSlot('end','End drawing')}</div><div class="form-bottom"><a class="button button--outline" href="#/library">Back to library</a><div class="form-bottom__right"><p class="inline-help">${canContinue?'Both drawings are ready.':'Add a start and end drawing to continue.'}</p><button class="button button--copper" data-route="plan" ${canContinue?'':'disabled'}>Continue to motion ${icon('arrow')}</button></div></div>`, { workflow:true });
}

function cueRow(number, area, action, pace) {
  return `<div class="cue-row"><span class="cue-row__num">${number}</span><span class="cue-row__area">${area}</span><span class="cue-row__action">${action}</span><span class="cue-row__pace">${pace}</span></div>`;
}

function planPage() {
  const hasText = state.prompt.trim().length > 0;
  const unsupported = state.plan?.kind === 'rejected';
  const current = state.plan?.kind === 'ready';
  const allowed = !hasText || (current && state.approved);
  return appShell('plan', `<section class="page-heading page-heading--compact"><div><h1>Describe the <em>change.</em></h1><p>An optional English instruction lets you direct the movement.</p></div><div class="mini-pair"><span>${botanicalArt({small:true,alternate:0})}</span><b>→</b><span>${botanicalArt({small:true,alternate:2})}</span></div></section><div class="plan-layout"><section class="prompt-panel"><label for="motion-prompt" class="field-label">Describe the motion <span>Optional</span></label><textarea id="motion-prompt" maxlength="1000" placeholder="First the petals draw inward, then the stem turns slowly toward the window.">${escapeHtml(state.prompt)}</textarea><div class="prompt-help"><span>Describe the order of movement in English. Leave empty to generate from the drawings alone.</span><span class="char-count">${state.prompt.length} / 1000</span></div><div class="prompt-examples"><span>Try a direction</span><button data-example="First, the petals fold inward. Then the stem turns slowly toward the light.">A gradual turn</button><button data-example="The flower closes slightly, then opens toward the light.">A soft opening</button></div><div class="prompt-actions"><button class="button button--outline" data-preview-plan ${hasText?'':'disabled'}>Preview plan ${icon('arrow')}</button></div></section><section class="cue-panel ${unsupported?'cue-panel--error':''}"><div class="cue-panel__head"><span>Interpretation</span><span class="cue-panel__edition">${current?'Ready':'Waiting'}</span></div>${unsupported?`<div class="plan-rejection" role="alert"><span>${icon('close')}</span><div><b>This instruction needs another pass.</b><p>Try describing a visible movement in order. The text is still editable; no plan has been saved.</p></div></div>`:current?`<p class="cue-caption">Order is shown, not exact timing.</p><div class="cue-lanes"><div class="cue-lane"><span>Cue 1</span><i><b>01&nbsp; · &nbsp;Draw inward</b></i></div><div class="cue-lane"><span>Cue 2</span><i class="cue-lane__after"><b>02&nbsp; · &nbsp;Turn toward light</b></i></div></div><ol class="cue-order"><li><b>01</b> Petals draw inward <span>slow</span></li><li><b>02</b> Stem turns toward light <span>normal</span></li></ol><label class="approve-plan"><input type="checkbox" data-approve ${state.approved?'checked':''} /><span class="fake-check">${icon('check')}</span><span>This plan is correct</span></label><p class="cue-disclaimer">Changing the instruction clears this approval. The plan is a preview until you start the animation.</p>`:`<div class="cue-empty"><span class="cue-empty__symbol">✳</span><b>Your plan will appear here.</b><p>Preview the instruction to review its order before generating.</p><div class="cue-empty__ticks">${Array.from({length:9},(_,i)=>`<i style="height:${9+(i%3)*8}px"></i>`).join('')}</div></div>`}</section></div><div class="form-bottom"><a class="button button--outline" href="#/keyframes">${icon('back')} Back to drawings</a><div class="form-bottom__right"><p class="inline-help">${!hasText?'Drawings-only generation is ready.':unsupported?'Revise the instruction and preview again.':!current?'Preview the plan before continuing.':!state.approved?'Approve the plan to continue.':'The approved plan will be saved with this animation.'}</p><button class="button button--copper" data-generate ${allowed?'':'disabled'}>Generate animation ${icon('arrow')}</button></div></div><p class="prototype-note">Plan preview is illustrative in this mockup. No language model is connected.</p>`, { workflow:true });
}

function statusCopy(status) {
  return {
    queued: ['Queued','Your study is waiting for an available worker.'],
    running: ['Running','The worker is drawing the in-between frames. You can leave this page; the animation will remain in your library.'],
    done: ['Done','Your movement study is ready to view.'],
    failed: ['Failed','The worker stopped before producing a result. Your drawings are still available in this study.'],
    cancelled: ['Cancelled','This animation was cancelled before a result was created.']
  }[status];
}

function statusPage() {
  const [label, message] = statusCopy(state.jobStatus);
  const done = state.jobStatus === 'done';
  const failed = state.jobStatus === 'failed';
  const terminal = done || failed || state.jobStatus === 'cancelled';
  return appShell('status', `<section class="page-heading page-heading--compact"><div><p class="eyebrow"><span>Animation CU—025</span></p><h1>Let the drawing <em>move.</em></h1><p>Submitted from two drawings${state.prompt?' and an approved motion plan':''}.</p></div><span class="status status--${state.jobStatus}"><i></i>${label}</span></section><section class="status-workbench"><div class="status-visual"><div class="status-visual__heads"><span>Start</span><span>16-frame sequence</span><span>End</span></div><div class="status-visual__row"><div class="status-thumb">${botanicalArt({small:true,alternate:0})}</div><div class="status-film">${framesStrip({mode:done?'filled':state.jobStatus==='running'?'running':'static'})}<p>${done?'16 frames · 3.2 sec':state.jobStatus==='queued'?'Waiting for worker':state.jobStatus==='running'?'Generating 16 frames':label}</p></div><div class="status-thumb">${botanicalArt({small:true,alternate:2})}</div></div><div class="status-message"><span class="status-message__glyph">${done?'✓':failed?'!':state.jobStatus==='cancelled'?'–':'✳'}</span><div><b>${label}</b><p>${message}</p></div></div>${done?'<button class="button button--copper" data-route="result">View result '+icon('arrow')+'</button>':failed?'<div class="status-actions"><button class="button button--outline" data-route="library">Back to library</button><button class="button button--copper" data-route="keyframes">Start a new animation '+icon('arrow')+'</button></div>':state.jobStatus==='cancelled'?'<a class="button button--outline" href="#/library">Back to library</a>':'<button class="button button--danger-quiet" data-cancel>Cancel generation</button>'}</div><aside class="job-details"><p class="eyebrow"><span>Submitted study</span></p><h2>A stem turns<br /><em>toward light.</em></h2><dl><div><dt>Status</dt><dd>${label}</dd></div><div><dt>Output</dt><dd>16 frames · 512 × 320</dd></div><div><dt>Request</dt><dd>${state.prompt?'Approved motion plan':'Drawings only'}</dd></div><div><dt>Job ID</dt><dd>CU—025</dd></div></dl><div class="detail-rule"></div><p class="job-details__note">${terminal?'This is a prototype state; no real job was submitted.':'State is shown without a percentage or estimated finish time.'}</p></aside></section><div class="prototype-state"><span>Mock state</span><div class="state-switch">${['queued','running','done','failed','cancelled'].map(k=>`<button type="button" data-status="${k}" class="${state.jobStatus===k?'is-on':''}">${k[0].toUpperCase()+k.slice(1)}</button>`).join('')}</div></div><div class="step-footer"><a href="#/plan">${icon('back')} Back to motion plan</a><span>Leaving this page does not stop the job.</span></div>`, { workflow:true });
}

function resultPage() {
  const frame = state.activeFrame;
  return appShell('result', `<section class="page-heading page-heading--compact"><div><p class="eyebrow"><span>Animation CU—024</span></p><h1>The space <em>between.</em></h1><p>A stem turns toward the light · 16 frames · 3.2 seconds</p></div><span class="status status--done"><i></i>Done</span></section><section class="result-layout"><div class="player-column"><div class="video-stage"><div class="video-art ${state.playing?'is-playing':''}">${botanicalArt({small:false,alternate:frame > 12?2:frame > 7?1:0})}${state.playing?'':`<div class="video-mark">${icon('play')}</div>`}</div><div class="video-stage__bottom"><span>Start 0:00</span><span>Frame ${String(frame).padStart(2,'0')} of 16</span><span>End 0:03</span></div></div><div class="player-controls"><button class="control-play" data-play aria-label="${state.playing?'Pause':'Play'}">${icon(state.playing?'pause':'play')}</button><button class="frame-step" data-frame="-1" aria-label="Previous frame">←</button><button class="frame-step" data-frame="1" aria-label="Next frame">→</button><div class="player-timeline"><div class="player-timeline__labels"><span>Your drawing</span><span>Generated frames</span><span>Your drawing</span></div>${framesStrip({active:frame,mode:'scrub'})}</div></div><div class="result-actions"><a class="button button--outline" href="#/library">Back to library</a><button class="button button--copper" data-download>Download MP4 ${icon('download')}</button><a class="new-study-link" href="#/keyframes">Start a new study ${icon('arrow')}</a></div><p class="prototype-note">Sample result preview. Video export is not connected.</p></div><aside class="result-details"><p class="eyebrow"><span>Study notes</span></p><h2>A stem turns<br />toward light.</h2><div class="result-pair"><span>${botanicalArt({small:true,alternate:0})}<b>Start</b></span><i>→</i><span>${botanicalArt({small:true,alternate:2})}<b>End</b></span></div><dl><div><dt>Instruction</dt><dd>${state.prompt?escapeHtml(state.prompt):'No instruction · drawings only'}</dd></div><div><dt>Frames</dt><dd>16 · first and last are your drawings</dd></div><div><dt>Created</dt><dd>Oct 21, 2026 · 14:32 UTC</dd></div></dl><a class="archive-link" href="#/library">View all studies ${icon('arrow')}</a></aside></section>`, { workflow:true });
}

function labPage() {
  return appShell('lab', `<section class="page-heading"><div><p class="eyebrow"><span>Independent experiment</span></p><h1>Line, light, <em>attention.</em></h1><p>A living engraving study. Move the pointer through the field; tune the line behavior below.</p></div><a class="button button--outline" href="#/home">Return to Cue ${icon('arrow')}</a></section><section class="lab-layout"><div class="lab-stage"><div class="lab-stage__head"><span>PLATE 01 / SPECIMEN</span><span><i></i> WEBGL STUDY</span></div><canvas id="wave-canvas" aria-label="Interactive Wave-Line engraving study"></canvas><div class="lab-stage__foot"><span>POINTER → DISTORTION</span><span>BURGUNDY / PAPER / SAGE</span></div></div><aside class="lab-controls"><p class="eyebrow"><span>STUDY PARAMETERS</span></p><h2>Adjust the<br /><em>engraving.</em></h2>${rangeControl('pitch','Line density',4,40,2,'px')}${rangeControl('warp','Wave depth',0,100,1,'%')}${rangeControl('speed','Motion speed',0,100,1,'%')}<div class="lab-note"><span>${icon('leaf')}</span><p>The line field is a visual experiment. It does not alter uploaded drawings or animation results.</p></div><button class="button button--outline button--wide" data-reset-lab>Reset study</button></aside></section><div class="step-footer"><a href="#/home">${icon('back')} Back to Cue</a><span>REDUCED MOTION IS RESPECTED</span></div>`, {});
}

function rangeControl(key, label, min, max, step, unit) {
  return `<label class="range-control"><span>${label}<output data-output="${key}">${state.line[key]}${unit}</output></span><input type="range" min="${min}" max="${max}" step="${step}" value="${state.line[key]}" data-line="${key}" /><i class="range-track"><b style="--value:${(state.line[key]-min)/(max-min)*100}%"></b></i></label>`;
}

function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
}

function render() {
  const screen = route();
  document.body.dataset.screen = screen;
  if (screen === 'home') app.innerHTML = homePage();
  else if (screen === 'signin') app.innerHTML = signInPage();
  else if (screen === 'library') app.innerHTML = libraryPage();
  else if (screen === 'keyframes') app.innerHTML = keyframesPage();
  else if (screen === 'plan') app.innerHTML = planPage();
  else if (screen === 'status') app.innerHTML = statusPage();
  else if (screen === 'result') app.innerHTML = resultPage();
  else if (screen === 'lab') app.innerHTML = labPage();
  else { window.location.hash = '/home'; return; }
  bindScreen(screen);
}

function announce(message) {
  toast.textContent = message;
  toast.classList.add('is-visible');
  window.clearTimeout(announce.timer);
  announce.timer = window.setTimeout(() => toast.classList.remove('is-visible'), 3200);
}

function bindScreen(screen) {
  document.querySelectorAll('[data-route]').forEach(button => button.addEventListener('click', () => go(button.dataset.route)));
  document.querySelectorAll('[data-auth]').forEach(tab => tab.addEventListener('click', () => { state.authTab = tab.dataset.auth; render(); }));
  const authForm = document.querySelector('#auth-form');
  authForm?.addEventListener('submit', event => { event.preventDefault(); go('library'); });
  document.querySelector('.password-toggle')?.addEventListener('click', event => {
    const input = document.querySelector('#password');
    const show = input.type === 'password'; input.type = show ? 'text' : 'password'; event.currentTarget.textContent = show ? 'Hide' : 'Show'; event.currentTarget.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
  });
  document.querySelector('.account-menu')?.addEventListener('click', () => go('signin'));
  document.querySelector('#motion-prompt')?.addEventListener('input', event => {
    state.prompt = event.target.value; state.approved = false; state.plan = null;
    const count = document.querySelector('.char-count'); if (count) count.textContent = `${state.prompt.length} / 1000`;
    const approval = document.querySelector('.approve-plan input'); if (approval) approval.checked = false;
    const preview = document.querySelector('[data-preview-plan]'); if (preview) preview.disabled = !state.prompt.trim();
    const generate = document.querySelector('[data-generate]'); if (generate) generate.disabled = Boolean(state.prompt.trim());
    const hint = document.querySelector('.inline-help'); if (hint) hint.textContent = state.prompt.trim() ? 'Preview the plan before continuing.' : 'Drawings-only generation is ready.';
    const panel = document.querySelector('.cue-panel');
    if (panel) { panel.classList.remove('cue-panel--error'); panel.innerHTML = `<div class="cue-panel__head"><span>Interpretation</span><span class="cue-panel__edition">Waiting</span></div><div class="cue-empty"><span class="cue-empty__symbol">✳</span><b>Your plan will appear here.</b><p>Preview the instruction to review its order before generating.</p><div class="cue-empty__ticks">${Array.from({length:9},(_,i)=>`<i style="height:${9+(i%3)*8}px"></i>`).join('')}</div></div>`; }
  });
  document.querySelectorAll('[data-example]').forEach(button => button.addEventListener('click', () => { state.prompt = button.dataset.example; state.plan = null; state.approved = false; render(); }));
  document.querySelector('[data-preview-plan]')?.addEventListener('click', () => {
    if (!state.prompt.trim()) return;
    state.plan = /explode|destroy|negative command/i.test(state.prompt) ? {kind:'rejected'} : {kind:'ready'}; state.approved = false; render();
  });
  document.querySelector('[data-approve]')?.addEventListener('change', event => { state.approved = event.target.checked; render(); });
  document.querySelector('[data-generate]')?.addEventListener('click', () => {
    if (state.prompt.trim() && (!state.plan || !state.approved)) return;
    state.jobStatus = 'queued'; go('status');
  });
  document.querySelectorAll('[data-file-slot]').forEach(input => input.addEventListener('change', async () => {
    const file = input.files?.[0]; if (!file) return;
    if (!['image/png','image/jpeg'].includes(file.type)) { announce('Choose a PNG or JPEG image.'); return; }
    const dimensions = await imageDimensions(file);
    state.files[input.dataset.fileSlot] = {name:file.name,url:URL.createObjectURL(file),dimensions:`${dimensions.width} × ${dimensions.height}`};
    render();
  }));
  document.querySelector('[data-sample-pair]')?.addEventListener('click', () => {
    const sample = (alternate, name) => ({name, url:`data:image/svg+xml;charset=utf-8,${encodeURIComponent(botanicalArt({alternate}))}`, dimensions:'512 × 320'});
    state.files.start = sample(0,'Cue specimen · start.svg');
    state.files.end = sample(2,'Cue specimen · end.svg');
    render();
  });
  document.querySelectorAll('[data-remove-file]').forEach(button => button.addEventListener('click', () => { state.files[button.dataset.removeFile] = null; render(); }));
  document.querySelector('[data-swap]')?.addEventListener('click', () => { [state.files.start,state.files.end] = [state.files.end,state.files.start]; render(); });
  document.querySelectorAll('[data-status]').forEach(b => b.addEventListener('click', () => { state.jobStatus = b.dataset.status; render(); }));
  document.querySelector('[data-cancel]')?.addEventListener('click', () => { if (window.confirm('Cancel this animation?')) { state.jobStatus = 'cancelled'; render(); } });
  document.querySelector('[data-play]')?.addEventListener('click', () => { state.playing = !state.playing; render(); });
  document.querySelectorAll('[data-frame]').forEach(button => button.addEventListener('click', () => { state.activeFrame = Math.max(1,Math.min(16,state.activeFrame+Number(button.dataset.frame))); render(); }));
  document.querySelectorAll('[data-tick]').forEach(tick => {
    const pick = () => { state.activeFrame = Number(tick.dataset.tick); render(); };
    tick.addEventListener('click', pick);
    tick.addEventListener('keydown', event => { if (event.key === 'Enter') pick(); });
  });
  document.querySelector('[data-download]')?.addEventListener('click', () => announce('This result is a mockup; MP4 export is not connected.'));
  document.querySelectorAll('[data-delete]').forEach(button => button.addEventListener('click', () => {
    const card = button.closest('.job-card');
    if (window.confirm('Delete this animation? The video and drawings are removed.')) { card.remove(); announce('Animation deleted.'); }
  }));
  document.querySelectorAll('[data-open-job]').forEach(button => button.addEventListener('click', () => { state.jobStatus=button.dataset.jobStatus; go(button.dataset.openJob); }));
  document.querySelectorAll('[data-line]').forEach(input => input.addEventListener('input', () => {
    state.line[input.dataset.line] = Number(input.value);
    const output = document.querySelector(`[data-output="${input.dataset.line}"]`);
    const unit = input.dataset.line === 'pitch' ? 'px' : '%';
    output.textContent = `${input.value}${unit}`;
    input.nextElementSibling.firstElementChild.style.setProperty('--value', `${(input.value-input.min)/(input.max-input.min)*100}%`);
    updateWave();
  }));
  document.querySelector('[data-reset-lab]')?.addEventListener('click', () => { state.line = {pitch:18,warp:52,speed:32}; render(); });
  if (screen === 'lab') initWave();
}

function imageDimensions(file) {
  return new Promise(resolve => { const image = new Image(); image.onload = () => resolve({width:image.naturalWidth,height:image.naturalHeight}); image.onerror = () => resolve({width:0,height:0}); image.src = URL.createObjectURL(file); });
}

let wave = null;
function initWave() {
  const canvas = document.querySelector('#wave-canvas'); if (!canvas) return;
  const gl = canvas.getContext('webgl', {antialias:true, alpha:false, powerPreference:'low-power'});
  if (!gl) { canvas.parentElement.classList.add('lab-stage--fallback'); return; }
  const vertex = `attribute vec2 position; varying vec2 uv; void main(){uv=position*.5+.5;gl_Position=vec4(position,0.,1.);}`;
  const fragment = `precision mediump float; varying vec2 uv; uniform vec2 resolution; uniform float time; uniform vec2 mouse; uniform float pitch; uniform float warp; uniform float speed; void main(){vec2 p=uv; float d=distance((p-mouse)*vec2(resolution.x/resolution.y,1.),vec2(0.)); float influence=exp(-d*5.); float bend=sin(p.x*8.+time*speed)*warp*.018+sin(p.x*2.4-time*speed*.45)*warp*.025; bend+=influence*warp*.055*sin((p.x-mouse.x)*15.); float y=p.y+bend; float lines=mix(55.,150.,1.-pitch); float f=abs(fract(y*lines)-.5); float ink=1.-smoothstep(.08,.2,f); float paper=1.-smoothstep(.44,.5,f); vec3 bg=vec3(.957,.929,.875); vec3 burgundy=vec3(.294,.157,.204); vec3 sage=vec3(.569,.667,.541); vec3 copper=vec3(.827,.604,.384); vec3 col=mix(bg,burgundy,ink*.92); float accent=(1.-smoothstep(0.,.2,abs(uv.x-mouse.x)))*smoothstep(.05,.6,influence); col=mix(col,sage,accent*.34*paper); float wash=sin(uv.x*3.+time*.25)*.5+.5; col=mix(col,copper,step(.985,fract(uv.y*lines+wash*.03))*.55); gl_FragColor=vec4(col,1.);}`;
  function compile(type, source) { const shader=gl.createShader(type); gl.shaderSource(shader,source); gl.compileShader(shader); return shader; }
  const program=gl.createProgram(); gl.attachShader(program,compile(gl.VERTEX_SHADER,vertex)); gl.attachShader(program,compile(gl.FRAGMENT_SHADER,fragment)); gl.linkProgram(program); gl.useProgram(program);
  const buffer=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,buffer); gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);
  const position=gl.getAttribLocation(program,'position'); gl.enableVertexAttribArray(position); gl.vertexAttribPointer(position,2,gl.FLOAT,false,0,0);
  wave={gl,program,canvas,uniforms:{resolution:gl.getUniformLocation(program,'resolution'),time:gl.getUniformLocation(program,'time'),mouse:gl.getUniformLocation(program,'mouse'),pitch:gl.getUniformLocation(program,'pitch'),warp:gl.getUniformLocation(program,'warp'),speed:gl.getUniformLocation(program,'speed')},started:performance.now()};
  canvas.addEventListener('pointermove', event => { const rect=canvas.getBoundingClientRect(); state.pointer={x:(event.clientX-rect.left)/rect.width,y:1-(event.clientY-rect.top)/rect.height}; });
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) { renderWave(performance.now()); return; }
  const draw = now => { if (!wave || !document.body.contains(canvas)) return; renderWave(now); requestAnimationFrame(draw); };
  requestAnimationFrame(draw);
}
function updateWave(){ if(wave) renderWave(performance.now()); }
function renderWave(now){
  if(!wave)return; const {gl,canvas,uniforms}=wave; const ratio=Math.min(devicePixelRatio||1,1.5); const width=Math.floor(canvas.clientWidth*ratio),height=Math.floor(canvas.clientHeight*ratio); if(canvas.width!==width||canvas.height!==height){canvas.width=width;canvas.height=height;} gl.viewport(0,0,width,height); gl.uniform2f(uniforms.resolution,width,height); gl.uniform1f(uniforms.time,(now-wave.started)*.001); gl.uniform2f(uniforms.mouse,state.pointer.x,state.pointer.y); gl.uniform1f(uniforms.pitch,state.line.pitch/40); gl.uniform1f(uniforms.warp,state.line.warp/100); gl.uniform1f(uniforms.speed,state.line.speed/25); gl.drawArrays(gl.TRIANGLES,0,6);
}

window.addEventListener('hashchange', render);
window.addEventListener('keydown', event => {
  if(route()==='result' && !['INPUT','TEXTAREA'].includes(document.activeElement?.tagName)) {
    if(event.code==='Space'){event.preventDefault();state.playing=!state.playing;render();}
    if(event.key==='ArrowRight'){state.activeFrame=Math.min(16,state.activeFrame+1);render();}
    if(event.key==='ArrowLeft'){state.activeFrame=Math.max(1,state.activeFrame-1);render();}
  }
});

render();
