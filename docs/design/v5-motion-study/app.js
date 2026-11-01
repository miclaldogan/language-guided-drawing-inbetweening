(() => {
  const screens = ['welcome', 'library', 'keyframes', 'motion', 'status', 'result'];
  const titleFor = { welcome: 'WELCOME', library: 'LIBRARY', keyframes: 'NEW STUDY', motion: 'MOTION PLAN', status: 'GENERATION', result: 'RESULT' };
  const state = { frame: 8, playing: false, loop: true, cancelled: false, jobStatus: 'running', files: { start: 'sample', end: 'sample' } };
  let toastTimer;

  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  function toast(message) {
    const node = $('#toast');
    node.textContent = message;
    node.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => node.classList.remove('show'), 2600);
  }
  function showScreen(name) {
    if (!screens.includes(name)) return;
    $$('.screen').forEach(node => node.classList.toggle('active', node.id === `screen-${name}`));
    $$('.rail-item').forEach(node => node.classList.toggle('active', node.dataset.screen === name || (name === 'motion' && node.dataset.screen === 'keyframes')));
    $('#crumb-current').textContent = titleFor[name];
    history.replaceState(null, '', `#${name}`);
    window.scrollTo({ top: 0, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  }
  $$('[data-screen]').forEach(button => button.addEventListener('click', () => showScreen(button.dataset.screen)));
  $('#continue-motion').addEventListener('click', () => {
    if (!state.files.start || !state.files.end) { toast('Add both drawings before continuing.'); return; }
    showScreen('motion');
  });
  if (screens.includes(location.hash.slice(1))) showScreen(location.hash.slice(1));
  $$('[data-auth-mode]').forEach(button => button.addEventListener('click', () => {
    const create = button.dataset.authMode === 'create';
    $$('[data-auth-mode]').forEach(tab => {
      const selected = tab === button;
      tab.classList.toggle('active', selected);
      tab.setAttribute('aria-selected', String(selected));
    });
    $('#password').autocomplete = create ? 'new-password' : 'current-password';
    $('.sign-in-button').innerHTML = `${create ? 'Create account' : 'Sign in'} <span>↗</span>`;
  }));

  // Field study panel
  const overlay = $('#field-overlay');
  const openField = () => {
    overlay.classList.add('open');
    overlay.setAttribute('aria-hidden', 'false');
    $('#field-x').focus();
  };
  const closeField = () => {
    overlay.classList.remove('open');
    overlay.setAttribute('aria-hidden', 'true');
    $('#field-open').focus();
  };
  $('#field-open').addEventListener('click', openField);
  $('#field-close').addEventListener('click', closeField);
  $('#field-x').addEventListener('click', closeField);
  $('#field-done').addEventListener('click', closeField);
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && overlay.classList.contains('open')) closeField();
  });

  // A small, dependency-free WebGL study: an SDF form is raymarched and shaded as an engraved relief.
  const canvas = $('#etch-canvas');
  const hero = $('#hero-art');
  const gl = canvas.getContext('webgl', { alpha: true, antialias: false, powerPreference: 'low-power' });
  let shaderProgram;
  let pointer = [0, 0];
  const uniforms = {};
  const colors = {
    mint: { ink: [0.11, 0.17, 0.18], light: [0.82, 0.94, 0.87], accent: [1.0, 0.42, 0.28] },
    coral: { ink: [0.22, 0.14, 0.12], light: [0.97, 0.87, 0.75], accent: [1.0, 0.40, 0.24] },
    blue: { ink: [0.10, 0.14, 0.24], light: [0.78, 0.85, 0.99], accent: [0.33, 0.52, 1.0] },
  };
  let activePalette = 'mint';
  const vertexSource = `
    attribute vec2 a_position;
    varying vec2 v_uv;
    void main(){ v_uv = a_position * 0.5 + 0.5; gl_Position = vec4(a_position, 0.0, 1.0); }
  `;
  const fragmentSource = `
    precision highp float;
    varying vec2 v_uv;
    uniform vec2 u_resolution;
    uniform vec2 u_mouse;
    uniform float u_time;
    uniform float u_pitch;
    uniform float u_relief;
    uniform float u_speed;
    uniform float u_pointer;
    uniform vec3 u_ink;
    uniform vec3 u_light;
    uniform vec3 u_accent;
    float scene(vec3 p){
      vec3 q = p;
      float t = u_time * u_speed;
      q.x += 0.10 * sin(p.y * 2.6 + t) + u_mouse.x * u_pointer * 0.10 * exp(-p.y*p.y*0.8);
      q.z += 0.08 * sin(p.x * 2.8 - t * 0.72) + u_mouse.y * u_pointer * 0.09;
      q.y += 0.045 * sin(p.x * 4.2 + p.z * 2.0 + t * 0.7);
      float d = length(q * vec3(0.91, 1.0, 0.84)) - 0.76;
      d += 0.025 * sin(q.x * 8.0 + q.y * 3.0) * sin(q.z * 7.0 - q.y * 2.0);
      return d;
    }
    vec3 normalAt(vec3 p){
      vec2 e = vec2(0.0015, 0.0);
      return normalize(vec3(scene(p + e.xyy) - scene(p - e.xyy), scene(p + e.yxy) - scene(p - e.yxy), scene(p + e.yyx) - scene(p - e.yyx)));
    }
    void main(){
      vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution.xy) / min(u_resolution.x, u_resolution.y);
      vec3 ro = vec3(0.0, 0.0, 2.65);
      vec3 rd = normalize(vec3(uv * 1.05, -1.5));
      float travel = 0.0;
      float distanceToForm = 0.0;
      bool hit = false;
      for(int i = 0; i < 76; i++){
        vec3 pos = ro + rd * travel;
        distanceToForm = scene(pos);
        if(distanceToForm < 0.0018){ hit = true; break; }
        travel += distanceToForm * 0.76;
        if(travel > 5.0) break;
      }
      vec3 color = u_ink;
      float vignette = 1.0 - smoothstep(0.1, 1.45, length(uv));
      float field = 0.5 + 0.5 * sin((uv.y * 4.0 + sin(uv.x * 2.0 + u_time * 0.12) * 0.35) * 3.14159);
      color = mix(color, color * 1.18, field * 0.055 * vignette);
      if(hit){
        vec3 p = ro + rd * travel;
        vec3 n = normalAt(p);
        vec3 lightDirection = normalize(vec3(-0.42, 0.72, 0.58));
        float diffuse = clamp(dot(n, lightDirection) * 0.55 + 0.48, 0.0, 1.0);
        float relief = mix(0.34, 1.0, u_relief);
        float tone = clamp(diffuse * relief + 0.08, 0.0, 1.0);
        float bend = sin(p.y * 2.5 + p.z * 2.0 + u_time * u_speed) * 0.19 + u_mouse.x * u_pointer * 0.19 * exp(-p.y*p.y);
        float density = mix(24.0, 76.0, u_pitch);
        float lineA = abs(sin((p.x + p.z * 0.18 + bend) * density));
        float lineB = abs(sin((p.y * 0.96 - p.x * 0.22 - bend * 0.55) * density * 0.92));
        float width = 0.12 + (1.0 - tone) * 0.20;
        float hatchA = 1.0 - smoothstep(width, width + 0.07, lineA);
        float hatchB = 1.0 - smoothstep(width + 0.02, width + 0.12, lineB);
        float shadow = 1.0 - tone;
        float cross = smoothstep(0.40, 0.95, shadow) * hatchB;
        float ink = clamp(hatchA * 0.72 + cross * 0.54, 0.0, 1.0);
        float rim = pow(1.0 - max(dot(n, vec3(0.0,0.0,1.0)), 0.0), 3.0);
        vec3 paper = mix(u_light, u_accent, smoothstep(0.78, 1.0, rim) * 0.34);
        color = mix(paper, u_ink * 0.78, ink);
        color += u_accent * rim * 0.16;
      }
      float grain = fract(sin(dot(gl_FragCoord.xy + u_time * 4.0, vec2(12.9898,78.233))) * 43758.5453) - 0.5;
      color += grain * 0.018;
      gl_FragColor = vec4(color * vignette, 1.0);
    }
  `;
  function compile(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.warn('Engraving shader compile failed:', gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }
  function setPalette(name) {
    activePalette = name;
    const palette = colors[name];
    if (gl && shaderProgram) {
      gl.useProgram(shaderProgram);
      gl.uniform3fv(uniforms.u_ink, palette.ink);
      gl.uniform3fv(uniforms.u_light, palette.light);
      gl.uniform3fv(uniforms.u_accent, palette.accent);
    }
    $$('.swatch').forEach(button => button.classList.toggle('active', button.dataset.palette === name));
  }
  function resizeCanvas() {
    if (!gl) return;
    const rect = hero.getBoundingClientRect();
    const cap = innerWidth < 700 ? 1.15 : 1.45;
    const ratio = Math.min(devicePixelRatio || 1, cap);
    const width = Math.max(1, Math.floor(rect.width * ratio));
    const height = Math.max(1, Math.floor(rect.height * ratio));
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
      gl.viewport(0, 0, width, height);
      gl.useProgram(shaderProgram);
      gl.uniform2f(uniforms.u_resolution, width, height);
    }
  }
  if (gl) {
    const vs = compile(gl.VERTEX_SHADER, vertexSource);
    const fs = compile(gl.FRAGMENT_SHADER, fragmentSource);
    if (vs && fs) {
      shaderProgram = gl.createProgram();
      gl.attachShader(shaderProgram, vs);
      gl.attachShader(shaderProgram, fs);
      gl.linkProgram(shaderProgram);
      if (gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
        gl.useProgram(shaderProgram);
        const buffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
        const position = gl.getAttribLocation(shaderProgram, 'a_position');
        gl.enableVertexAttribArray(position);
        gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);
        ['u_resolution', 'u_mouse', 'u_time', 'u_pitch', 'u_relief', 'u_speed', 'u_pointer', 'u_ink', 'u_light', 'u_accent'].forEach(key => uniforms[key] = gl.getUniformLocation(shaderProgram, key));
        gl.uniform2f(uniforms.u_mouse, 0, 0);
        gl.uniform1f(uniforms.u_pitch, 0.48);
        gl.uniform1f(uniforms.u_relief, 0.62);
        gl.uniform1f(uniforms.u_speed, 0.24);
        gl.uniform1f(uniforms.u_pointer, 0.55);
        setPalette(activePalette);
        resizeCanvas();
      } else {
        console.warn('Engraving shader link failed:', gl.getProgramInfoLog(shaderProgram));
        canvas.hidden = true;
      }
    } else canvas.hidden = true;
  } else {
    canvas.hidden = true;
    console.info('WebGL unavailable; showing the static engraved form fallback.');
  }
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let animationFrame = 0;
  let startAt = performance.now();
  function render(now) {
    if (!gl || !shaderProgram || document.hidden || !hero.getClientRects().length) {
      animationFrame = 0;
      return;
    }
    if (!reduceMotion.matches) {
      gl.useProgram(shaderProgram);
      gl.uniform1f(uniforms.u_time, (now - startAt) / 1000);
      gl.uniform2f(uniforms.u_mouse, pointer[0], pointer[1]);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      animationFrame = requestAnimationFrame(render);
    } else {
      gl.useProgram(shaderProgram);
      gl.uniform1f(uniforms.u_time, 0);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      animationFrame = 0;
      return;
    }
  }
  if (gl && shaderProgram) {
    const heroObserver = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting && !document.hidden && !reduceMotion.matches && !animationFrame) {
        animationFrame = requestAnimationFrame(render);
      } else if ((!entry.isIntersecting || document.hidden || reduceMotion.matches) && animationFrame) {
        cancelAnimationFrame(animationFrame);
        animationFrame = 0;
        if (reduceMotion.matches && entry.isIntersecting) render(performance.now());
      }
    });
    heroObserver.observe(hero);
    if (hero.getBoundingClientRect().height > 0 && !reduceMotion.matches) animationFrame = requestAnimationFrame(render);
    new ResizeObserver(() => resizeCanvas()).observe(hero);
    hero.addEventListener('pointermove', event => {
      const rect = hero.getBoundingClientRect();
      pointer = [(event.clientX - rect.left) / rect.width * 2 - 1, -((event.clientY - rect.top) / rect.height * 2 - 1)];
    });
    hero.addEventListener('pointerleave', () => { pointer = [0, 0]; });
    document.addEventListener('visibilitychange', () => {
      if (!document.hidden && hero.getBoundingClientRect().height > 0 && !reduceMotion.matches && !animationFrame) animationFrame = requestAnimationFrame(render);
      if (document.hidden && animationFrame) { cancelAnimationFrame(animationFrame); animationFrame = 0; }
      if (!document.hidden && reduceMotion.matches && hero.getBoundingClientRect().height > 0) render(performance.now());
    });
    reduceMotion.addEventListener?.('change', () => { startAt = performance.now(); });
  }

  function updateUniform(rangeId, outputId, uniform, scale, digits) {
    const slider = $(`#${rangeId}`);
    const output = $(`#${outputId}`);
    const set = () => {
      const value = Number(slider.value) / scale;
      output.textContent = value.toFixed(digits);
      if (gl && shaderProgram) {
        gl.useProgram(shaderProgram);
        gl.uniform1f(uniforms[uniform], value);
      }
    };
    slider.addEventListener('input', set);
    set();
  }
  if (gl && shaderProgram) {
    updateUniform('pitch-range', 'pitch-value', 'u_pitch', 100, 2);
    updateUniform('relief-range', 'relief-value', 'u_relief', 100, 2);
    updateUniform('speed-range', 'speed-value', 'u_speed', 100, 2);
    updateUniform('pointer-range', 'pointer-value', 'u_pointer', 100, 2);
    $$('.swatch').forEach(button => button.addEventListener('click', () => setPalette(button.dataset.palette)));
  }

  // Upload affordance: local preview only, no bytes leave the browser.
  function chooseFile(kind) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = 'image/png,image/jpeg';
    input.setAttribute('aria-label', `Choose ${kind} drawing`);
    input.addEventListener('change', () => {
      const file = input.files && input.files[0];
      if (!file) return;
      const url = URL.createObjectURL(file);
      if (state.files[kind] && state.files[kind] !== 'sample') URL.revokeObjectURL(state.files[kind]);
      state.files[kind] = url;
      const stage = $(`.drawing-${kind}`);
      const art = $('.portrait', stage);
      art.style.opacity = '0';
      let image = $('.uploaded-preview', stage);
      if (!image) {
        image = document.createElement('img');
        image.className = 'uploaded-preview';
        image.alt = `${kind} drawing preview`;
        stage.append(image);
      }
      image.src = url;
      const column = stage.closest('.keyframe-column');
      $('.file-meta strong', column).textContent = file.name;
      $('.file-meta small', column).textContent = `${(file.size / 1024).toFixed(0)} KB · local preview only`;
      updateContinue();
      $('.stage-corner', stage).textContent = kind === 'start' ? '01 / ORIGIN' : '02 / ARRIVAL';
    });
    input.click();
  }
  $$('[data-upload]').forEach(button => button.addEventListener('click', () => chooseFile(button.dataset.upload)));
  $$('.drawing-stage').forEach(stage => {
    stage.addEventListener('dragover', event => { event.preventDefault(); stage.classList.add('dragging'); });
    stage.addEventListener('dragleave', () => stage.classList.remove('dragging'));
    stage.addEventListener('drop', event => {
      event.preventDefault(); stage.classList.remove('dragging');
      const kind = stage.classList.contains('drawing-start') ? 'start' : 'end';
      const file = event.dataTransfer.files[0];
      if (file && ['image/png', 'image/jpeg'].includes(file.type)) {
        const url = URL.createObjectURL(file); state.files[kind] = url;
        $('.portrait', stage).style.opacity = '0';
        let image = $('.uploaded-preview', stage);
        if (!image) { image = document.createElement('img'); image.className = 'uploaded-preview'; image.alt = `${kind} drawing preview`; stage.append(image); }
        image.src = url;
        const column = stage.closest('.keyframe-column');
        $('.file-meta strong', column).textContent = file.name;
        $('.file-meta small', column).textContent = `${(file.size / 1024).toFixed(0)} KB · local preview only`;
        updateContinue();
      } else if (file) toast('Choose a PNG or JPEG drawing.');
    });
  });
  $$('.remove-button').forEach(button => button.addEventListener('click', () => {
    const kind = button.dataset.remove;
    const stage = $(`.drawing-${kind}`);
    $('.uploaded-preview', stage)?.remove();
    $('.portrait', stage).style.opacity = '';
    if (state.files[kind] && state.files[kind] !== 'sample') URL.revokeObjectURL(state.files[kind]);
    state.files[kind] = null;
    updateContinue();
    toast(`${kind === 'start' ? 'Start' : 'End'} drawing cleared in this preview.`);
  }));
  function updateContinue() {
    const valid = Boolean(state.files.start && state.files.end);
    $('#continue-motion').disabled = !valid;
    $('#continue-motion').setAttribute('aria-disabled', String(!valid));
  }
  updateContinue();

  // Motion plan mock: editing invalidates approval; preview refreshes the plan.
  const prompt = $('#motion-prompt');
  const approval = $('#approve-plan');
  const warning = $('#plan-warning');
  const count = $('#char-count');
  const approvalRow = $('.approval-row');
  const previewButton = $('#preview-plan');
  let planFresh = true;
  prompt.value = 'First move the eyes to the left, then slowly turn the head.';
  count.textContent = prompt.value.length;
  prompt.addEventListener('input', () => {
    count.textContent = prompt.value.length;
    approval.checked = false;
    if (!prompt.value.trim()) {
      planFresh = true;
      warning.classList.add('hidden');
      approvalRow.classList.add('hidden');
      $('#plan-timeline').classList.add('hidden');
      $('#plan-state').innerHTML = '<i></i> DRAWINGS ONLY';
      $('#plan-state').style.color = '#687a70';
      previewButton.disabled = true;
      $('#generate-button').disabled = false;
    } else {
      planFresh = false;
      warning.textContent = 'Edit the instruction, then read the motion again to refresh this plan.';
      warning.classList.remove('hidden');
      approvalRow.classList.remove('hidden');
      $('#plan-timeline').classList.remove('hidden');
      $('#plan-state').innerHTML = '<i></i> OUT OF DATE';
      $('#plan-state').style.color = '#8a713b';
      $('#plan-timeline').style.opacity = '.48';
      previewButton.disabled = false;
      $('#generate-button').disabled = true;
    }
  });
  $$('[data-prompt]').forEach(button => button.addEventListener('click', () => {
    prompt.value = button.dataset.prompt;
    prompt.dispatchEvent(new Event('input', { bubbles: true }));
  }));
  $('#preview-plan').addEventListener('click', () => {
    const value = prompt.value.trim();
    if (!value) return;
    $('#plan-state').innerHTML = '<i></i> READING MOTION';
    $('#plan-state').style.color = '#527bff';
    $('#preview-plan').disabled = true;
    setTimeout(() => {
      if (/\b(don't|do not|never|disappear|reverse time|teleport)\b/i.test(value)) {
        planFresh = false;
        approval.checked = false;
        approvalRow.classList.add('hidden');
        $('#plan-timeline').classList.add('hidden');
        $('#plan-state').innerHTML = '<i></i> NEEDS REVISION';
        $('#plan-state').style.color = '#a66d2b';
        warning.textContent = 'This sample validator cannot map “disappear / reverse time” to a supported motion cue. Edit the sentence or clear it to generate from drawings alone.';
        warning.classList.remove('hidden');
        $('#generate-button').disabled = true;
        $('#preview-plan').disabled = false;
        return;
      }
      const saysSmile = /smil|expression/i.test(value);
      const saysHand = /hand|arm|raise/i.test(value);
      const first = saysHand ? 'Raise the hand' : saysSmile ? 'Begin to smile' : 'Shift the gaze';
      const second = /then|before|first/i.test(value) ? (saysHand ? 'Turn the head' : 'Turn the head') : (saysSmile ? 'Turn the head' : 'Follow the direction');
      $$('#cue-list .cue-description strong').forEach((node, index) => { node.textContent = index === 0 ? first : second; });
      $('#summary-text').textContent = `${first}; then ${second.toLowerCase()}. Review the order before generating.`;
      $('#plan-state').innerHTML = '<i></i> PLAN READY';
      $('#plan-state').style.color = '#337a6b';
      $('#plan-timeline').style.opacity = '1';
      $('#plan-timeline').classList.remove('hidden');
      approvalRow.classList.remove('hidden');
      warning.classList.add('hidden');
      planFresh = true;
      approval.checked = false;
      $('#preview-plan').disabled = false;
      toast('Illustrative plan refreshed. Check the sequence before approving.');
    }, 480);
  });
  approval.addEventListener('change', () => {
    $('#generate-button').disabled = !approval.checked || !planFresh;
    if (approval.checked) warning.classList.add('hidden');
  });
  $('#generate-button').addEventListener('click', event => {
    if (prompt.value.trim() && (!approval.checked || !planFresh)) {
      event.preventDefault();
      toast('Refresh and approve the motion plan before continuing.');
      return;
    }
    setJobStatus('running');
    showScreen('status');
  });

  // Asynchronous job/status representation. It reports elapsed time and states, never fake progress.
  let elapsed = 42;
  function setJobStatus(status) {
    state.jobStatus = status;
    state.cancelled = status !== 'running';
    const pill = $('.status-pill');
    const strip = $('.generation-strip');
    const failed = status === 'failed';
    const cancelled = status === 'cancelled';
    pill.className = `status-pill ${status === 'running' ? 'status-running' : ''} ${failed ? 'status-failed' : ''} ${cancelled ? 'status-cancelled' : ''}`;
    pill.innerHTML = `<i></i> ${status.toUpperCase()}`;
    $('#status-title').innerHTML = status === 'running' ? 'The sequence is <em>forming.</em>' : failed ? 'The sequence <em>stopped.</em>' : 'Generation <em>cancelled.</em>';
    $('#worker-label').textContent = status === 'running' ? 'WORKER 01 · ACTIVE' : failed ? 'WORKER 01 · STOPPED' : 'JOB · CANCELLED';
    $('.status-sentence b').textContent = status === 'running' ? 'Generating your sequence' : failed ? 'This generation could not finish' : 'This generation was cancelled';
    $('.status-sentence small').textContent = status === 'running' ? 'Intermediate frames are being calculated.' : failed ? 'The worker stopped before it could save an output.' : 'No video or frame archive was produced.';
    $('.status-pulse').style.background = status === 'running' ? '#527bff' : failed ? '#c45b4b' : '#8a938d';
    $('.status-pulse').style.boxShadow = status === 'running' ? '0 0 0 5px #527bff20' : 'none';
    strip.style.opacity = status === 'running' ? '1' : '.35';
    $('#status-error').classList.toggle('hidden', !failed);
    $('#status-error').textContent = failed ? 'The worker ended before an output was available. Your drawings are still in the library. You can start a new study.' : '';
    $('#cancel-job').classList.toggle('hidden', status !== 'running');
    $('#status-return').classList.toggle('hidden', status === 'running');
    if (status === 'running') elapsed = 42;
  }
  $$('[data-job-state]').forEach(card => card.addEventListener('click', () => setJobStatus(card.dataset.jobState)));
  setInterval(() => {
    if ($('#screen-status').classList.contains('active') && state.jobStatus === 'running') {
      elapsed += 1;
      $('#elapsed-time').innerHTML = `${String(Math.floor(elapsed / 60)).padStart(2, '0')}<span>:</span>${String(elapsed % 60).padStart(2, '0')}`;
    }
  }, 1000);
  $('#cancel-job').addEventListener('click', () => {
    if (!confirm('Cancel this illustrative generation?')) return;
    setJobStatus('cancelled');
    toast('Generation cancelled in the prototype.');
  });

  // 16-frame result controls and keyboard-operable scrubber.
  function updateFrame(frame) {
    state.frame = Math.max(1, Math.min(16, frame));
    const fraction = (state.frame - 1) / 15 * 100;
    $('#frame-number').textContent = String(state.frame).padStart(2, '0');
    $('.scrub-fill').style.width = `${fraction}%`;
    $('.scrub-thumb').style.left = `${fraction}%`;
    $('#scrubber').setAttribute('aria-valuenow', state.frame);
  }
  $('#previous-frame').addEventListener('click', () => updateFrame(state.frame - 1));
  $('#next-frame').addEventListener('click', () => updateFrame(state.frame + 1));
  $('#loop-button').addEventListener('click', () => {
    state.loop = !state.loop;
    $('#loop-button').style.color = state.loop ? '#337a6b' : '#87918b';
    toast(state.loop ? 'Loop playback enabled.' : 'Loop playback paused.');
  });
  $('#scrubber').addEventListener('pointerdown', event => {
    const scrubber = $('#scrubber');
    const move = e => {
      const rect = scrubber.getBoundingClientRect();
      updateFrame(Math.round(1 + Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width)) * 15));
    };
    move(event);
    const end = () => { window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', end); };
    window.addEventListener('pointermove', move);
    window.addEventListener('pointerup', end);
  });
  $('#scrubber').addEventListener('keydown', event => {
    if (event.key === 'ArrowRight') { event.preventDefault(); updateFrame(state.frame + 1); }
    if (event.key === 'ArrowLeft') { event.preventDefault(); updateFrame(state.frame - 1); }
    if (event.key === 'Home') { event.preventDefault(); updateFrame(1); }
    if (event.key === 'End') { event.preventDefault(); updateFrame(16); }
  });
  $('#play-button').addEventListener('click', () => {
    state.playing = !state.playing;
    $('#play-button').textContent = state.playing ? 'Ⅱ' : '▶';
    $('#play-button').setAttribute('aria-label', state.playing ? 'Pause sequence' : 'Play sequence');
    $('#playback-state').textContent = state.playing ? 'PLAYING' : 'PAUSED';
  });
  setInterval(() => {
    if (!state.playing) return;
    if (state.frame >= 16 && !state.loop) { state.playing = false; $('#play-button').textContent = '▶'; $('#playback-state').textContent = 'PAUSED'; return; }
    updateFrame(state.frame >= 16 ? 1 : state.frame + 1);
  }, 220);
  $('#download-button').addEventListener('click', () => toast('Download is a visual affordance in this mockup; no MP4 is connected.'));
})();
