const app = document.querySelector('#app');
let waveRaf = 0;
let waveObserver = null;
let waveVisibilityHandler = null;

function stopWaveLine() {
  cancelAnimationFrame(waveRaf);
  waveObserver?.disconnect();
  if (waveVisibilityHandler) document.removeEventListener('visibilitychange', waveVisibilityHandler);
  waveObserver = null;
  waveVisibilityHandler = null;
}

const screens = [
  ['login', '00', 'Oturum'],
  ['library', '01', 'Kütüphane'],
  ['keyframes', '02', 'Çizimler'],
  ['plan', '03', 'Hareket planı'],
  ['status', '04', 'Üretim'],
  ['result', '05', 'Sonuç'],
  ['lab', '✳', 'Wave-Line lab'],
];

function drawing(variant = 0, extraClass = '') {
  const turn = variant ? 'translate(30 0) scale(.93 1)' : '';
  return `<svg class="figure ${extraClass}" viewBox="0 0 640 400" role="img" aria-label="Örnek çizim karesi">
    <defs>
      <linearGradient id="shade-${variant}" x1="0" y1="0" x2="1" y2=".85"><stop stop-color="#171a18"/><stop offset=".48" stop-color="#65645c"/><stop offset="1" stop-color="#e7e3d8"/></linearGradient>
      <pattern id="grain-${variant}" width="9" height="9" patternUnits="userSpaceOnUse"><path d="M1 0v9 M5 0v9" stroke="#272925" stroke-opacity=".12" stroke-width=".7"/></pattern>
    </defs>
    <rect width="640" height="400" fill="#e5e2d9"/>
    <path d="M73 350h500M104 324h432M117 72v260M521 72v260" fill="none" stroke="#9f9b91" stroke-width="1"/>
    <g transform="${turn}">
      <path d="M216 350c21-51 48-63 72-76 17-9 23-22 19-42-28-14-44-46-42-88 2-49 33-91 84-93 53-2 84 34 88 85 2 31-7 50-18 67-9 14-7 33 12 45 29 19 53 45 67 102Z" fill="url(#shade-${variant})"/>
      <path d="M282 171c10-61 47-94 91-92 43 2 69 34 71 72 1 13-4 21-12 27l-13 10 12 14-13 10 3 16-20 7c-7 19-23 31-48 30-29-1-52-19-65-44" fill="none" stroke="#252824" stroke-width="2.2"/>
      <path d="M431 181c-13 0-24 4-35 11m36 6-29 7m9 17-20 2m-9 20c-10 8-22 8-34 2m70 57c-29-17-56-24-88-22m-53 56c45-14 110-15 186 4" fill="none" stroke="#ede9df" stroke-opacity=".8" stroke-width="1.5"/>
      <path d="M302 145c12-35 41-57 71-59m-73 79c7-33 33-55 62-60m-48 88c8-19 23-32 44-38m-46 57c12-14 27-22 44-24m12 60c18 3 35-3 46-18m-86 44c40-11 83-5 117 15m-159 38c76-19 145-9 210 9m-219-30c58-16 131-14 189 3" fill="none" stroke="#f0ede4" stroke-opacity=".4" stroke-width="1"/>
      <path d="M247 350c16-33 31-49 57-65m172 65c-11-28-29-47-56-62" fill="none" stroke="#191c19" stroke-width="1.5"/>
    </g>
    <rect width="640" height="400" fill="url(#grain-${variant})" opacity=".22"/>
    <path d="M31 32h18M31 32v18M609 32h-18M609 32v18M31 368h18M31 368v-18M609 368h-18M609 368v-18" stroke="#77766e" stroke-width="1"/>
  </svg>`;
}

const appIcon = `<span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span>`;

function nav() {
  return `<aside class="rail">
    <a class="brand" href="#" data-go="welcome">${appIcon}<span>CUE<span class="brand-sub">MOTION STUDIO</span></span></a>
    <div class="rail-rule"></div>
    <p class="rail-label">ÇALIŞMA ALANI</p>
    <nav class="side-nav" aria-label="Ana gezinme">
      ${screens.slice(1, 6).map(([id, n, label]) => `<button class="nav-item ${id === 'library' ? 'current' : ''}" data-go="${id}"><span class="nav-num">${n}</span><span>${label}</span>${id === 'library' ? '<span class="nav-dot"></span>' : ''}</button>`).join('')}
    </nav>
    <div class="rail-bottom">
      <button class="lab-link" data-go="lab"><span class="lab-star">∿</span><span>Wave-Line<small>GÖRSEL LABORATUVARI</small></span><span class="external">↗</span></button>
      <div class="rail-rule"></div>
      <div class="user"><span class="user-avatar">AD</span><span>Ayşe Demir<small>KİŞİSEL ALAN</small></span><button class="more" aria-label="Hesap seçenekleri">···</button></div>
    </div>
  </aside>`;
}

function shell(content, eyebrow, title, screen) {
  return `<div class="workspace">${nav()}<main class="main">
    <header class="topbar"><div class="crumb"><span>STÜDYO</span><b>/</b><span>${eyebrow}</span></div><div class="top-actions"><span class="save-state"><i></i> Değişiklik yok</span><span class="top-divider"></span><button class="quiet-button" data-go="library">Çalışmalarım</button><span class="avatar-mini">AD</span></div></header>
    <div class="page" data-screen="${screen}">${title ? `<div class="page-head"><div>${title}</div></div>` : ''}${content}</div>
    <footer class="footer"><span>CUE STUDIO <b>·</b> HAREKETİ ÇİZ</span><span>ÖNİZLEME / 2026</span></footer>
  </main></div>`;
}

function keyframePair(compact = false) {
  return `<div class="pair ${compact ? 'pair-compact' : ''}">
    <article class="frame-card"><div class="frame-meta"><span><b>A</b> BAŞLANGIÇ</span><span>00:00</span></div><div class="frame-art">${drawing(0)}</div><div class="frame-foot"><span>yüz_on_01.png</span><span>1280 × 800</span></div></article>
    <div class="pair-axis"><span class="axis-line"></span><span class="axis-arrow">→</span><span class="axis-line"></span>${compact ? '' : '<button class="swap-button" title="Sıralamayı değiştir" aria-label="Sıralamayı değiştir">↔</button>'}</div>
    <article class="frame-card"><div class="frame-meta"><span><b>B</b> BİTİŞ</span><span>00:16</span></div><div class="frame-art">${drawing(1)}</div><div class="frame-foot"><span>yüz_on_02.png</span><span>1280 × 800</span></div></article>
  </div>`;
}

function stepper(current) {
  const items = [['keyframes','01','Çizimler'],['plan','02','Plan'],['status','03','Üretim'],['result','04','Sonuç']];
  return `<div class="stepper">${items.map(([id,n,label],i)=>`<button class="step ${id===current?'active':''} ${items.findIndex(x=>x[0]===current)>i?'complete':''}" data-go="${id}"><span>${items.findIndex(x=>x[0]===current)>i?'✓':n}</span>${label}</button>${i<3?'<i class="step-rule"></i>':''}`).join('')}</div>`;
}

const login = `<section class="login-screen">
  <div class="login-art"><div class="cover-head"><span>CUE / MOTION STUDIO</span><span>STÜDYO NOTU&nbsp;&nbsp; 001</span></div><div class="cover-title"><p>İki çizim.<br/><em>Aradaki hareket.</em></p><span class="cover-index">A—B<br/>16 KAREYE KADAR</span></div><div class="cover-figure"><img class="cover-art-image" src="hero-art.svg" alt=""/></div><div class="cover-bottom"><span>ÇİZİMDEN HAREKETE</span><span>01 — 06</span></div></div>
  <div class="login-form-wrap"><div class="login-top"><a class="brand dark-brand" data-go="library">${appIcon}<span>CUE<span class="brand-sub">MOTION STUDIO</span></span></a><span class="locale">TR <b>⌄</b></span></div><div class="login-form"><p class="eyebrow">KİŞİSEL ÇALIŞMA ALANIN</p><h1>Tekrar<br/><em>hoş geldin.</em></h1><p class="login-intro">Çizimlerini hareketlendirmeye kaldığın yerden devam et.</p><div class="auth-tabs"><button class="selected">Giriş yap</button><button>Kayıt ol</button></div><label class="field-label" for="email">E-posta adresi</label><input class="text-input" id="email" type="email" value="ayse@ornek.com"/><label class="field-label" for="password">Şifre</label><div class="password-wrap"><input class="text-input" id="password" type="password" value="motionstudy"/><button class="show-password" type="button">Göster</button></div><div class="form-row"><label class="check-label"><input type="checkbox" checked/> Oturumu açık tut</label><a href="#">Şifremi unuttum</a></div><button class="button-primary wide" data-go="library">Stüdyoya gir <span>↗</span></button><p class="privacy-note"><span class="lock-icon">◈</span> Çalışmaların yalnızca senin hesabında saklanır.</p></div><div class="login-foot"><span>© CUE STUDIO 2026</span><a data-go="lab">WAVE-LINE LAB ↗</a></div></div>
</section>`;

const welcome = `<div class="open-studio-home">
  <header class="home-nav"><a class="home-brand" href="#top" data-go="welcome"><span class="home-mark"><i></i><i></i><i></i></span><span>CUE<small>DRAWING / MOTION STUDIO</small></span></a><nav aria-label="Sayfa bağlantıları"><a href="#method">Yöntem</a><a href="#work">Görsel dil</a><button class="home-login" data-go="login">Giriş yap</button></nav><button class="button-primary home-enter" data-go="login">Stüdyoya gir <span>↗</span></button></header>
  <main id="top">
   <section class="home-hero"><div class="hero-copy"><p class="hero-kicker"><span></span>HAREKET / ÇİZİM LABORATUVARI&nbsp; — &nbsp;2026</p><h1>Çizginin<br/><em>arasındaki</em><br/><span>hareket.</span></h1><p class="hero-description">İki çizim arasındaki sessizliği, hareketle doldur. Cue; başlangıç ve bitiş çizimlerinden, adım adım bir animasyon üretir.</p><div class="hero-actions"><button class="button-primary hero-cta" data-go="login">Stüdyoyu keşfet <span>↗</span></button><a class="hero-secondary" href="#method"><span class="down-mark">↓</span> Nasıl çalışır?</a></div><div class="hero-proof"><span>01—16</span><i></i><span>KARELER ARASI BİR ÇALIŞMA</span></div></div><div class="hero-art-wrap"><span class="art-orbit orbit-a"></span><span class="art-orbit orbit-b"></span><img class="hero-art" src="hero-art.svg" alt="Gravür portre, turuncu daire, mavi renk plakası ve dalgalı kontur çizgilerinden oluşan hareket etüdü"/><canvas class="hero-wave" id="hero-wave-canvas" aria-hidden="true"></canvas><span class="art-side-note">KARE ETÜDÜ&nbsp; / &nbsp;NO. 01</span></div><div class="home-index"><span>01</span><span>HERO STUDY</span><i></i><span>SCROLL TO EXPLORE</span></div></section>
   <section class="method-section" id="method"><div class="method-heading"><p class="hero-kicker dark-kicker"><span></span>ÜRETİMİN YAPISI</p><h2>Bir hareket.<br/><em>Üç kısa adım.</em></h2><p>Kontroller sade; çizimlerin, sıralaman ve çıkan kareler sahnenin merkezinde.</p></div><div class="method-steps"><article><span class="method-number">01 / GİRİŞ</span><div class="method-glyph glyph-start"><i></i><i></i></div><h3>İki kare seç.</h3><p>Başlangıç ve bitiş çizimini yükle; hareketin sınırlarını belirle.</p></article><article><span class="method-number">02 / YÖNERGE</span><div class="method-glyph glyph-middle"><i></i><i></i><i></i></div><h3>Hareketi tarif et.</h3><p>İngilizce kısa bir yönerge yaz; Cue sırasını önizleyip onaylamanı sağlar.</p></article><article><span class="method-number">03 / SONUÇ</span><div class="method-glyph glyph-end"><i></i><i></i><i></i><i></i></div><h3>Kareleri incele.</h3><p>Oluşan animasyonda kare kare ilerle; MP4 ve kare arşivini al.</p></article></div></section>
   <section class="art-statement" id="work"><div class="statement-mark">C / 01</div><p>Çizgi bir yüzey değil.<br/><em>Zamanın izi.</em></p><div class="statement-right"><span>WAVE-LINE / LIVE STUDY</span><button class="button-light" data-go="lab">Görsel laboratuvarı <span>↗</span></button></div><svg class="statement-lines" viewBox="0 0 900 220" aria-hidden="true"><path d="M0 178C140 26 235 23 378 128s207 105 328-6S855 24 900 38M0 194C140 42 235 39 378 144s207 105 328-6S855 40 900 54M0 210C140 58 235 55 378 160s207 105 328-6S855 56 900 70"/></svg></section>
   <section class="home-end"><div><p class="hero-kicker"><span></span>HAZIRSAN BAŞLAYALIM</p><h2>İki çizim.<br/><em>Yeni bir hareket.</em></h2></div><button class="button-primary hero-cta" data-go="login">Cue stüdyosuna gir <span>↗</span></button><span class="end-serial">CUE — OPEN STUDIO<br/>DRAWING INBETWEENING</span></section>
  </main><footer class="home-footer"><span>CUE / MOTION STUDIO</span><span>İKİ KARE ARASINDAKİ ALAN</span><span>TR · 2026</span></footer>
 </div>`;

const library = shell(`<section class="library-intro"><div><p class="eyebrow">ÇALIŞMA ARŞİVİ <span class="eyebrow-line"></span> 04 ÖĞE</p><h1>Hareket<br/><em>çalışmaları.</em></h1><p class="lede">İki çizimden doğan sekansların, tek bir yerde.</p></div><button class="button-primary" data-go="keyframes">Yeni çalışma <span>＋</span></button></section>
  <div class="filterline"><span>SON ÇALIŞMALAR</span><span>EN YENİDEN ESKİYE&nbsp;&nbsp; ↕</span></div>
  <section class="work-grid">
   <button class="work-card" data-go="result"><div class="work-art">${drawing(0)}<span class="play-overlay">▶</span><span class="work-count">16 KARE</span></div><div class="work-info"><div><span class="work-title">Baş sola döner, gözler takip eder</span><span class="work-date">BUGÜN · 14:32</span></div><span class="status-done"><i></i>Tamamlandı</span></div></button>
   <button class="work-card" data-go="status"><div class="work-art pending-art">${drawing(1)}<span class="work-count">GPU İŞLİYOR</span><div class="scanline"></div></div><div class="work-info"><div><span class="work-title">Yukarı bakıştan hafif gülümsemeye</span><span class="work-date">BUGÜN · 14:19</span></div><span class="status-running"><i></i>Üretiliyor</span></div></button>
   <button class="work-card" data-go="result"><div class="work-art">${drawing(1)}<span class="play-overlay">▶</span><span class="work-count">12 KARE</span></div><div class="work-info"><div><span class="work-title">Profil çizimi / deneme 03</span><span class="work-date">DÜN · 17:06</span></div><span class="status-done"><i></i>Tamamlandı</span></div></button>
   <button class="work-card" data-go="status"><div class="work-art failed-art">${drawing(0)}<span class="work-count">İŞ #CU-2048</span></div><div class="work-info"><div><span class="work-title">Kaş hareketi — alternatif</span><span class="work-date">18 MAY · 11:40</span></div><span class="status-failed"><i></i>Başarısız</span></div></button>
  </section>`, 'KÜTÜPHANE', '', 'library');

const keyframes = shell(`${stepper('keyframes')}<section class="flow-intro"><div><p class="eyebrow">YENİ ÇALIŞMA <span class="eyebrow-line"></span> 01 / 04</p><h1>Hareketin iki<br/><em>ucunu seç.</em></h1><p class="lede">Başlangıç ve bitiş çizimini ekle. Aradaki kareleri Cue oluşturacak.</p></div><span class="field-note">DESTEKLENEN GÖRSEL<br/>PNG · JPG · WEBP</span></section>
  ${keyframePair()}
  <div class="upload-bottom"><p><span class="info-mark">i</span> Çizimler 8:5 alana sığdırılarak gösterilir; özgün dosyan korunur.</p><div><button class="button-text" data-go="library">← Kütüphaneye dön</button><button class="button-outline" data-go="plan">Hareketi tarif et <span>→</span></button></div></div>`, 'YENİ ÇALIŞMA', '', 'keyframes');

const plan = shell(`${stepper('plan')}<section class="flow-intro compact-intro"><div><p class="eyebrow">HAREKETİ TANIMLA <span class="eyebrow-line"></span> 02 / 04</p><h1>Hareketi<br/><em>tarif et.</em></h1></div><div class="pair-mini">${keyframePair(true)}</div></section>
  <div class="plan-layout"><section class="prompt-column"><label class="field-label" for="motion-prompt">Hareket yönergesi <span>İSTEĞE BAĞLI</span></label><textarea id="motion-prompt" class="prompt-area">First move the eyes to the left, then turn the head slowly.</textarea><p class="field-hint">Yönergeyi İngilizce yaz. Çizimlerden üretmek için boş bırakabilirsin.</p><div class="sample-prompts"><span>ÖRNEKLER</span><button data-prompt="First move the eyes to the left, then turn the head slowly.">Bakış ve baş</button><button data-prompt="Raise the eyebrows, then open the mouth slightly.">Mimik</button></div><button class="button-outline plan-button" data-plan-preview>Planı önizle <span>↗</span></button></section>
  <section class="plan-column"><div class="section-cap"><span>01 / ANLAŞILAN SIRA</span><span class="plan-status"><i></i>ÖNİZLEME</span></div><p class="plan-caption">Sıra gösterilir; kesin zamanlama belirtilmez.</p><ol class="cue-list"><li><span class="cue-no">01</span><span class="cue-region">BAKIŞ</span><span class="cue-desc">Sola yönelir</span><span class="cue-speed">YAVAŞ</span></li><li><span class="cue-no">02</span><span class="cue-region">BAŞ</span><span class="cue-desc">Sola döner</span><span class="cue-speed">YAVAŞ</span></li></ol><div class="plan-approval"><label class="check-label"><input type="checkbox" checked/> Bu hareket planı doğru.</label><span>Yönerge değişirse tekrar önizle.</span></div></section></div>
  <div class="flow-actions"><button class="button-text" data-go="keyframes">← Çizimlere dön</button><div><span class="action-helper">Planı onayladıktan sonra üretimi başlat.</span><button class="button-primary" data-go="status">Animasyonu üret <span>→</span></button></div></div>`, 'HAREKET PLANI', '', 'plan');

const status = shell(`${stepper('status')}<section class="flow-intro compact-intro status-head"><div><p class="eyebrow">ÇALIŞMA CU-2048 <span class="eyebrow-line"></span> 03 / 04</p><h1>Hareket<br/><em>işleniyor.</em></h1><p class="lede">GPU işçisi çizimler arasındaki kareleri oluşturuyor.</p></div><span class="status-running large-status"><i></i>ÜRETİLİYOR</span></section>
  ${keyframePair(true)}
  <section class="generation-stage"><div class="stage-label"><span>KARE DİZİSİ</span><span>BAŞLANGIÇ <i></i> BİTİŞ</span></div><div class="frame-track">${Array.from({length:16},(_,i)=>`<span class="track-cell ${i===0?'edge-cell':''} ${i===15?'edge-cell':''} ${i===7?'active-cell':''}">${i===0?'A':i===15?'B':''}</span>`).join('')}</div><div class="stage-bottom"><span>İşlem sürüyor · ilerleme yüzdesi mevcut değil</span><span>GEÇEN SÜRE&nbsp;&nbsp; 00:38</span></div></section>
  <div class="status-lower"><div><span class="section-cap">HAREKET PLANI</span><p>01 Bakış sola · 02 Baş sola döner</p></div><div><span class="section-cap">İŞLEM KİMLİĞİ</span><p>CU-2048 <span class="muted-sep">·</span> 16 kare <span class="muted-sep">·</span> İstek alındı 14:19</p></div><button class="button-text danger-text">Üretimi iptal et</button></div>`, 'ÜRETİM DURUMU', '', 'status');

const result = shell(`${stepper('result')}<section class="result-heading"><div><p class="eyebrow">ÇALIŞMA CU-2048 <span class="eyebrow-line"></span> 04 / 04</p><h1>Hareketin<br/><em>tamamlandı.</em></h1><p class="lede">16 kare · MP4 video ve kare arşivi hazır.</p></div><button class="button-primary" data-download>MP4 indir <span>↓</span></button></section>
  <section class="result-layout"><div class="player-column"><div class="video-stage"><div class="video-art">${drawing(1)}</div><span class="video-corner">00:04 / 00:04</span><button class="play-main" aria-label="Oynat">▶</button><span class="video-label">KARE 08 / 16</span></div><div class="player-controls"><button aria-label="Önceki kare">←</button><button class="control-play">▶</button><button aria-label="Sonraki kare">→</button><div class="scrub-track"><span class="scrub-fill"></span><i></i><b></b></div><span class="frame-counter">08 <i>/</i> 16</span><button class="loop-control">↻</button></div><div class="filmstrip">${Array.from({length:8},(_,i)=>`<button class="thumb-frame ${i===4?'chosen':''}" data-frame="${i+1}">${drawing(i%2)}<span>${String(i+1).padStart(2,'0')}</span></button>`).join('')}</div></div>
  <aside class="result-meta"><div class="meta-top"><span class="section-cap">ÇALIŞMA BİLGİSİ</span><button class="more">···</button></div><div class="meta-command"><span>YÖNERGE</span><p>First move the eyes to the left, then turn the head slowly.</p></div><div class="meta-group"><span>HAREKET PLANI</span><p>01&nbsp;&nbsp; Bakış sola<br/>02&nbsp;&nbsp; Baş yavaşça sola döner</p></div><div class="meta-group"><span>MODEL SÜRÜMÜ</span><p>Gösterilmiyor</p></div><div class="meta-group"><span>ÜRETİM SÜRESİ</span><p>00:38</p></div><div class="meta-group"><span>OLUŞTURULMA</span><p>Bugün, 14:19</p></div><button class="button-outline archive-button" data-download>Kare arşivini indir <span>↓</span></button></aside></section>
  <div class="result-footer"><button class="button-text" data-go="library">← Kütüphaneye dön</button><button class="button-text" data-go="keyframes">Yeni çalışma <span>＋</span></button></div>`, 'SONUÇ ÖNİZLEMESİ', '', 'result');

const lab = shell(`<section class="lab-intro"><div><p class="eyebrow">GÖRSEL LABORATUVARI <span class="eyebrow-line"></span> STUDY 01</p><h1>Ton, çizgiye<br/><em>dönüşür.</em></h1><p class="lede">Wave-Line, görüntünün gölgesini çizgi yoğunluğuna çevirir. Ayarları değiştir; örnek çizim etkisini canlı izle.</p></div><a class="back-link" data-go="library">STÜDYODAN ÇIK&nbsp; ↗</a></section>
  <section class="lab-layout"><div class="shader-panel"><div class="shader-toolbar"><span><i class="live-dot"></i>WEBGL / CANLI ÖNİZLEME</span><button data-reset>AYARLARI SIFIRLA&nbsp; ↺</button></div><div class="shader-frame"><canvas id="wave-canvas" aria-label="Dalgalı gravür çizgileriyle işlenmiş örnek çizim"></canvas><div class="shader-stamp"><span>CUE / ETÜT 001</span><span>TON → ÇİZGİ</span></div></div><div class="shader-caption"><span>ÖRNEK PORTRE / GRİ TON EŞLEMESİ</span><span>İŞARETÇİYLE ETKİLEŞ</span></div></div>
  <aside class="lab-controls"><div class="control-head"><span class="section-cap">PARAMETRELER</span><span>01 — 04</span></div>
    <label class="range-control"><span><b>Çizgi aralığı</b><output id="pitch-value">8.0 px</output></span><input type="range" min="4" max="18" step=".5" value="8" data-uniform="pitch"/><small>SIK <i></i> SEYREK</small></label>
    <label class="range-control"><span><b>Ton derinliği</b><output id="relief-value">1.2</output></span><input type="range" min=".2" max="2" step=".1" value="1.2" data-uniform="relief"/><small>DÜZ <i></i> BELİRGİN</small></label>
    <label class="range-control"><span><b>Dalga genliği</b><output id="warp-value">0.65</output></span><input type="range" min="0" max="1.5" step=".05" value=".65" data-uniform="warp"/><small>SAKİN <i></i> AKIŞKAN</small></label>
    <label class="range-control"><span><b>Hareket hızı</b><output id="speed-value">0.25×</output></span><input type="range" min="0" max="1" step=".05" value=".25" data-uniform="speed"/><small>SABİT <i></i> CANLI</small></label>
    <div class="control-note"><span>i</span><p>Görüntü tarayıcıda işlenir. Yüklenen veya üretilen gerçek kareler bu deneye dahil değildir.</p></div>
    <button class="button-outline copy-shader" data-copy>GLSL KAYNAĞINI KOPYALA&nbsp; ↗</button>
  </aside></section>
  <section class="lab-principle"><span>01 / YÖNTEM</span><p>Her çizginin kalınlığı alttaki tonla belirlenir. Koyu bölgeler mürekkep taşır; ışıkta çizgi incelip kâğıda çekilir.</p><span>WEBGL FRAGMENT SHADER</span></section>`, 'WAVE-LINE LAB', '', 'lab');

function render(id = 'login') {
  stopWaveLine();
  if (id === 'welcome') app.innerHTML = welcome;
  else if (id === 'login') app.innerHTML = login;
  else app.innerHTML = ({library,keyframes,plan,status,result,lab})[id] || library;
  document.querySelectorAll('.nav-item').forEach(b => b.classList.toggle('current', b.dataset.go === id));
  if (id === 'lab') initWaveLine('wave-canvas','sample');
  if (id === 'welcome') initWaveLine('hero-wave-canvas','hero');
  window.scrollTo(0,0);
}

app.addEventListener('click', e => {
  const target = e.target.closest('[data-go]');
  if (target) { e.preventDefault(); render(target.dataset.go); return; }
  if (e.target.closest('[data-plan-preview]')) document.querySelector('.plan-status').innerHTML = '<i></i>ÖNİZLEME GÜNCEL';
  if (e.target.closest('[data-download]')) e.preventDefault();
  const prompt = e.target.closest('[data-prompt]');
  if (prompt) document.querySelector('#motion-prompt').value = prompt.dataset.prompt;
  const frame = e.target.closest('[data-frame]');
  if (frame) { document.querySelectorAll('.thumb-frame').forEach(t => t.classList.remove('chosen')); frame.classList.add('chosen'); document.querySelector('.frame-counter').innerHTML = `${String(frame.dataset.frame).padStart(2,'0')} <i>/</i> 16`; }
  if (e.target.closest('[data-reset]')) { render('lab'); }
  if (e.target.closest('[data-copy]')) { const button=e.target.closest('[data-copy]');navigator.clipboard?.writeText(window.waveLineSource||'').then(()=>button.textContent='GLSL KAYNAĞI KOPYALANDI ✓').catch(()=>button.textContent='KOPYALAMA İZNİ GEREKİYOR'); }
});

function initWaveLine(canvasId='wave-canvas', sourceKind='sample') {
  const canvas = document.querySelector(`#${canvasId}`);
  if (!canvas) return;
  const gl = canvas.getContext('webgl', {alpha:false, antialias:true, powerPreference:'low-power'});
  if (!gl) { if(sourceKind==='hero'){canvas.hidden=true;return;}const fallback=new Image();fallback.className='wave-fallback';fallback.alt='Wave-Line örnek çizim';fallback.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(drawing(0));canvas.replaceWith(fallback);return; }
  const vertex = `attribute vec2 p; varying vec2 uv; void main(){uv=p*.5+.5;gl_Position=vec4(p,0.,1.);}`;
  const fragment = `precision highp float; varying vec2 uv; uniform vec2 res; uniform float time; uniform vec2 mouse; uniform float pitch; uniform float relief; uniform float warp; uniform float speed; uniform sampler2D sourceTex;
  void main(){vec2 px=uv*res;float dist=length((uv-mouse)*vec2(res.x/res.y,1.));float pull=exp(-dist*8.)*.035;vec2 sampleUV=uv+vec2(pull*(uv.x-mouse.x),pull*(uv.y-mouse.y));vec3 source=texture2D(sourceTex,sampleUV).rgb;float tone=clamp(1.-dot(source,vec3(.299,.587,.114)),0.,1.);tone=smoothstep(.035,.72,tone)*relief;float t=time*speed;float pitchPx=max(3.,pitch);float phase=(px.y + sin(px.x*.018+t)*warp*12. + sin(px.x*.006-t*.55)*warp*6. + tone*warp*18.)/pitchPx;float lineDist=abs(fract(phase)-.5);float thickness=mix(.045,.44,tone);float line=1.-smoothstep(thickness,thickness+.09,lineDist);vec3 paper=vec3(.94,.94,.89);vec3 graphite=vec3(.15,.27,.23);vec3 col=mix(paper,graphite,line);float blueInk=smoothstep(.06,.30,source.b-max(source.r,source.g));float warmInk=smoothstep(.08,.36,source.r-source.b);col=mix(col,vec3(.46,.65,.82),blueInk*line);col=mix(col,vec3(.88,.31,.19),warmInk*line);gl_FragColor=vec4(col,1.);}`;
  window.waveLineSource=fragment;
  function shader(type, source){const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);return s;}
  const program=gl.createProgram(); gl.attachShader(program,shader(gl.VERTEX_SHADER,vertex));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,fragment));gl.linkProgram(program);gl.useProgram(program);
  const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]),gl.STATIC_DRAW);const loc=gl.getAttribLocation(program,'p');gl.enableVertexAttribArray(loc);gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
  const uniforms={res:gl.getUniformLocation(program,'res'),time:gl.getUniformLocation(program,'time'),mouse:gl.getUniformLocation(program,'mouse'),pitch:gl.getUniformLocation(program,'pitch'),relief:gl.getUniformLocation(program,'relief'),warp:gl.getUniformLocation(program,'warp'),speed:gl.getUniformLocation(program,'speed'),sourceTex:gl.getUniformLocation(program,'sourceTex')};
  const texture=gl.createTexture();gl.activeTexture(gl.TEXTURE0);gl.bindTexture(gl.TEXTURE_2D,texture);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR);gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);gl.uniform1i(uniforms.sourceTex,0);
  const image=new Image();image.onload=()=>{try{gl.bindTexture(gl.TEXTURE_2D,texture);gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,true);gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,image);if(sourceKind==='hero')canvas.parentElement.classList.add('shader-ready');}catch{canvas.hidden=true;}};image.onerror=()=>{canvas.hidden=true;};image.src=sourceKind==='hero'?'hero-art.svg':'data:image/svg+xml;charset=utf-8,'+encodeURIComponent(drawing(0));
  const params={pitch:8,relief:1.2,warp:.65,speed:.25}, pointer={x:.5,y:.5};
  const values={pitch:'pitch-value',relief:'relief-value',warp:'warp-value',speed:'speed-value'};
  document.querySelectorAll('[data-uniform]').forEach(input=>{input.addEventListener('input',()=>{params[input.dataset.uniform]=Number(input.value);const out=document.getElementById(values[input.dataset.uniform]);out.textContent=input.dataset.uniform==='pitch'?`${Number(input.value).toFixed(1)} px`:input.dataset.uniform==='speed'?`${Number(input.value).toFixed(2)}×`:Number(input.value).toFixed(2);});});
  canvas.addEventListener('pointermove',e=>{const r=canvas.getBoundingClientRect();pointer.x=(e.clientX-r.left)/r.width;pointer.y=1-(e.clientY-r.top)/r.height;});canvas.addEventListener('pointerleave',()=>{pointer.x=.5;pointer.y=.5;});
  let start=performance.now(),lastFrame=0;function resize(){const r=canvas.getBoundingClientRect(),d=Math.min(devicePixelRatio||1,1.5);canvas.width=Math.max(1,Math.floor(r.width*d));canvas.height=Math.max(1,Math.floor(r.height*d));gl.viewport(0,0,canvas.width,canvas.height);}waveObserver=new ResizeObserver(resize);waveObserver.observe(canvas);resize();
  function draw(now){if(now-lastFrame<1000/30){waveRaf=requestAnimationFrame(draw);return;}lastFrame=now;gl.uniform2f(uniforms.res,canvas.width,canvas.height);gl.uniform1f(uniforms.time,(now-start)/1000);gl.uniform2f(uniforms.mouse,pointer.x,pointer.y);for(const k of Object.keys(params))gl.uniform1f(uniforms[k],params[k]);gl.drawArrays(gl.TRIANGLES,0,6);if(!matchMedia('(prefers-reduced-motion: reduce)').matches)waveRaf=requestAnimationFrame(draw);}
  draw(performance.now());waveVisibilityHandler=()=>{if(document.hidden)cancelAnimationFrame(waveRaf);else if(!matchMedia('(prefers-reduced-motion: reduce)').matches){start=performance.now();draw(start);}};document.addEventListener('visibilitychange',waveVisibilityHandler);
}

render('welcome');
