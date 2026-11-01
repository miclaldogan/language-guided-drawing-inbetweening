const choices = [...document.querySelectorAll('[data-theme-choice]')];
const themes = {
  herbarium: {
    field: '#4B2834',
    title: 'FORMUN<br>HAFIZASINI<br><em>ÇİZ.</em>',
    kicker: 'BOTANİK HAREKET ETÜDÜ / 01',
    description: 'Bir dalın kıvrımı, bir yüzün dönüşü. İki çizim arasındaki hareketi keşfet; görünmeyen geçişlere biçim ver.',
    artLabel: 'Bordo Herbaryum: botanik gravür çizgileri ve hareket eden bir form',
    caption: 'PLATE 01 — BOTANICAL GESTURE'
  },
  frequency: {
    field: '#B34730',
    title: 'ÇİZGİLER<br>ARASINDA<br><em>FREKANS.</em>',
    kicker: 'RİTİM VE HAREKET / 02',
    description: 'Her çizgi bir titreşim, her kare yeni bir vuruş. Başlangıç ve bitiş arasındaki ritmi tarif et; Cue aradaki kareleri çizsin.',
    artLabel: 'Kiremit Frekans: dalga çizgileri, dairesel ritimler ve hareket eden bir form',
    caption: 'PLATE 02 — WAVE / MOTION STUDY'
  }
};

choices.forEach((choice, index) => {
  choice.addEventListener('click', () => {
    const theme = choice.dataset.themeChoice;
    const content = themes[theme];
    document.documentElement.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]').content = content.field;
    document.querySelector('.hero-title').innerHTML = content.title;
    document.querySelector('.hero-kicker-copy').textContent = content.kicker;
    document.querySelector('.hero-description').textContent = content.description;
    document.querySelector('.plate-art').setAttribute('aria-label', content.artLabel);
    document.querySelector('.plate-caption').textContent = content.caption;
    choices.forEach((item) => {
      const selected = item === choice;
      item.classList.toggle('is-active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    document.querySelector('.review-label b').textContent = `0${index + 1} — 02`;
  });
});

const requestedTheme = new URLSearchParams(window.location.search).get('theme');
if (requestedTheme === 'frequency') {
  document.querySelector('[data-theme-choice="frequency"]').click();
}
