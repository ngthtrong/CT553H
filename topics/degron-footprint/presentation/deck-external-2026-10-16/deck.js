/* Local-only presentation controls. No network request is required. */
(() => {
  const params = new URLSearchParams(location.search);
  const printing = params.has('print-pdf');
  const reader = !printing && (params.has('reader') || innerWidth < 760);
  const sections = [...document.querySelectorAll('.slides > section')];
  const notesDialog = document.getElementById('notes-dialog');
  const tocDialog = document.getElementById('toc-dialog');
  const motionButton = document.getElementById('motion-button');
  let motion = !matchMedia('(prefers-reduced-motion: reduce)').matches && !printing;
  let activeIndex = 0;
  const currentIndex = () => reader ? activeIndex : Reveal.getIndices().h;
  function applyMotion() {
    document.body.classList.toggle('motion-off', !motion);
    motionButton.textContent = motion ? 'Motion: on' : 'Motion: off';
    motionButton.setAttribute('aria-pressed', String(motion));
    document.querySelectorAll('img[data-gif]').forEach(img => {
      const play = motion && (reader || img.closest('section').classList.contains('present'));
      const next = play ? img.dataset.gif : img.dataset.poster;
      if (img.getAttribute('src') !== next) img.setAttribute('src', next);
    });
  }
  function jump(i) {
    i = Math.min(Math.max(i, 0), sections.length - 1);
    activeIndex = i;
    if (reader) sections[i].scrollIntoView({behavior: motion ? 'smooth' : 'instant'});
    else Reveal.slide(i);
  }
  function showNotes() {
    const section = sections[currentIndex()];
    document.getElementById('notes-heading').textContent = `${section.dataset.number} · Speaker notes / Ghi chú`;
    document.getElementById('notes-content').textContent = window.SPEAKER_NOTES?.[section.id] || section.querySelector('.notes')?.textContent.trim() || '';
    notesDialog.showModal();
  }
  document.getElementById('toc-button').onclick = () => tocDialog.showModal();
  document.getElementById('notes-button').onclick = showNotes;
  motionButton.onclick = () => {motion = !motion; applyMotion();};
  document.getElementById('fullscreen-button').onclick = () => {
    if (document.fullscreenElement) document.exitFullscreen();
    else document.documentElement.requestFullscreen?.().catch(() => {});
  };
  document.querySelectorAll('[data-close]').forEach(b => b.onclick = () => b.closest('dialog').close());
  document.querySelectorAll('[data-jump]').forEach(b => b.onclick = () => {jump(Number(b.dataset.jump)); tocDialog.close();});
  document.querySelectorAll('dialog').forEach(d => d.addEventListener('click', e => {if (e.target === d) d.close();}));
  document.addEventListener('keydown', e => {
    if (e.ctrlKey || e.altKey || e.metaKey || /INPUT|TEXTAREA/.test(e.target.tagName)) return;
    if (notesDialog.open || tocDialog.open) return;
    if (e.key.toLowerCase() === 'n') {e.preventDefault();showNotes();}
    if (e.key.toLowerCase() === 'm') {motion = !motion; applyMotion();}
    if (e.key.toLowerCase() === 't') tocDialog.showModal();
    if (reader && ['ArrowRight','ArrowLeft'].includes(e.key)) {e.preventDefault();jump(currentIndex() + (e.key === 'ArrowRight' ? 1 : -1));}
  });
  if (reader) {
    document.body.classList.add('reader');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => {if (e.isIntersecting) activeIndex = sections.indexOf(e.target);});
    }, {rootMargin:'-10% 0px -70% 0px'});
    sections.forEach(s => observer.observe(s));
    applyMotion();
    window.deckReady = true;
  } else {
    Reveal.initialize({width:1600,height:900,margin:.02,center:false,hash:true,controls:true,progress:true,
      transition:motion ? 'fade' : 'none',transitionSpeed:'fast',backgroundTransition:'none',
      slideNumber:false,pdfSeparateFragments:false,pdfMaxPagesPerSlide:1,showNotes:false,
      autoAnimate:false,scrollActivationWidth:null,keyboardCondition:() => !notesDialog.open && !tocDialog.open})
      .then(() => {applyMotion();window.deckReady = true;});
    Reveal.on('slidechanged', () => applyMotion());
  }
})();
