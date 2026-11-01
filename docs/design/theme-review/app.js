const choices = [...document.querySelectorAll('[data-theme-choice]')];
const themeFields = {
  aubergine: '#392942',
  nightprint: '#24395F',
  petrol: '#19494B',
  herbarium: '#4B2834',
  frequency: '#B34730'
};

choices.forEach((choice, index) => {
  choice.addEventListener('click', () => {
    const theme = choice.dataset.themeChoice;
    document.documentElement.dataset.theme = theme;
    document.querySelector('meta[name="theme-color"]').content = themeFields[theme];
    choices.forEach((item) => {
      const selected = item === choice;
      item.classList.toggle('is-active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    document.querySelector('.review-label b').textContent = `${String(index + 1).padStart(2, '0')} — 05`;
  });
});
