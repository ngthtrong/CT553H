/* ============================================================================
   Engine slide — viết riêng cho deck này, không phụ thuộc thư viện ngoài,
   nên mở được bằng file:// khi không có mạng.

   Phím:
     →  ↓  Space  PageDown   bước tiếp (hiện bước animation kế, hết thì sang slide)
     ←  ↑  Backspace PageUp  lùi
     Ctrl + ← / →              chuyển thẳng slide trước / sau, bỏ qua bước
     Home / End                slide đầu / cuối
     N                         bật/tắt ghi chú người nói
     O  hoặc Esc               bảng tổng quan 34 slide + 7 phụ lục
     F                         toàn màn hình
     P                         chế độ in (mọi bước hiện sẵn) — rồi Ctrl+P để xuất PDF
     số + Enter                nhảy tới slide

   Bước animation: phần tử có [data-step="k"] hiện khi bước hiện tại >= k.
   Phần tử có [data-dim-until="k"] bị làm nhoè tới khi đạt bước k.
   ========================================================================== */

(function () {
  'use strict';

  var stage   = document.getElementById('stage');
  var slides  = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  // phụ lục (A1…A7) nằm sau 34 slide lõi: không tính vào số đếm và vạch tiến độ
  var CORE    = slides.filter(function (s) { return !s.hasAttribute('data-appendix'); }).length;
  var hudPos  = document.getElementById('hud-pos');
  var hudSec  = document.getElementById('hud-sec');
  var hudStep = document.getElementById('hud-step');
  var bar     = document.getElementById('progress');
  var notes   = document.querySelector('#notes .n-body');
  var ovGrid  = document.querySelector('#overview .grid');

  // ?all trong URL: mọi bước hiện sẵn — dùng để soát bố cục và để in
  var SHOW_ALL = location.search.indexOf('all') >= 0;

  var i = 0;        // slide hiện tại
  var step = 0;     // bước animation trong slide
  var typed = '';   // bộ đệm nhảy slide bằng số

  /* ------------------------------------------------------------ co giãn 16:9 */

  function fit() {
    var pad = 30;
    var w = window.innerWidth - pad * 2;
    var h = window.innerHeight - 30 - pad * 2;      // 30px cho HUD
    if (document.body.classList.contains('notes-on')) w -= 380;
    var s = Math.min(w / 1280, h / 720);
    stage.style.transform = 'scale(' + s + ')';
  }

  /* -------------------------------------------------------------- số bước tối đa */

  function maxStep(sl) {
    var m = 0;
    sl.querySelectorAll('[data-step]').forEach(function (el) {
      m = Math.max(m, parseInt(el.getAttribute('data-step'), 10) || 0);
    });
    sl.querySelectorAll('[data-dim-until]').forEach(function (el) {
      m = Math.max(m, parseInt(el.getAttribute('data-dim-until'), 10) || 0);
    });
    return m;
  }

  /* ---------------------------------------------------------------- áp dụng bước */

  function applySteps() {
    var sl = slides[i];
    sl.querySelectorAll('[data-step]').forEach(function (el) {
      var k = parseInt(el.getAttribute('data-step'), 10) || 0;
      el.classList.toggle('on', step >= k);
    });
    sl.querySelectorAll('[data-dim-until]').forEach(function (el) {
      var k = parseInt(el.getAttribute('data-dim-until'), 10) || 0;
      el.classList.toggle('dim', step < k);
    });
    var m = maxStep(sl);
    hudStep.textContent = m ? ('bước ' + step + '/' + m) : '';
  }

  /* ------------------------------------------------------------------ đổi slide */

  function show(n, back) {
    n = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach(function (s) { s.classList.remove('current', 'back'); });
    i = n;
    var sl = slides[i];
    if (back) sl.classList.add('back');
    sl.classList.add('current');

    var ap = sl.getAttribute('data-appendix');
    hudPos.textContent = ap ? ('A' + ap + ' / 7 · phụ lục') : ((i + 1) + ' / ' + CORE);
    hudSec.textContent = sl.getAttribute('data-section') || '';
    bar.style.width = (Math.min(i + 1, CORE) / CORE * 100) + '%';

    var note = sl.querySelector('.speaker-note');
    notes.innerHTML = note ? note.innerHTML
      : '<p style="color:#7E949C">— không có ghi chú —</p>';

    if (SHOW_ALL) step = maxStep(sl);
    applySteps();
    location.hash = 's' + (i + 1);
    document.querySelectorAll('#overview .ov').forEach(function (o, k) {
      o.classList.toggle('here', k === i);
    });
  }

  function next() {
    if (step < maxStep(slides[i])) { step += 1; applySteps(); return; }
    if (i < slides.length - 1) { step = 0; show(i + 1); }
  }

  function prev() {
    if (step > 0) { step -= 1; applySteps(); return; }
    if (i > 0) {
      step = maxStep(slides[i - 1]);      // lùi vào slide trước ở trạng thái đầy đủ
      show(i - 1, true);
    }
  }

  function goto(n) { step = 0; show(n); }

  /* ----------------------------------------------------------------- bảng tổng quan */

  slides.forEach(function (sl, k) {
    var d = document.createElement('div');
    d.className = 'ov';
    var apk = sl.getAttribute('data-appendix');
    d.innerHTML = '<div class="n">' + (apk ? 'A' + apk : (k + 1)) + ' · ' +
      (sl.getAttribute('data-section') || '') + '</div><div class="t">' +
      (sl.getAttribute('data-title') || '') + '</div>';
    d.addEventListener('click', function () {
      document.body.classList.remove('overview-on');
      goto(k);
    });
    ovGrid.appendChild(d);
  });

  /* ------------------------------------------------------------------- bàn phím */

  document.addEventListener('keydown', function (e) {
    var k = e.key;
    if (e.metaKey || e.altKey) return;
    if (e.ctrlKey) {
      if (k === 'ArrowLeft' || k === 'ArrowRight') {
        e.preventDefault();
        typed = '';
        var target = i + (k === 'ArrowRight' ? 1 : -1);
        if (target >= 0 && target < slides.length) {
          step = 0;
          show(target, k === 'ArrowLeft');
        }
      }
      return;
    }

    if (k >= '0' && k <= '9') { typed += k; return; }
    if (k === 'Enter' && typed) { goto(parseInt(typed, 10) - 1); typed = ''; return; }
    typed = '';

    switch (k) {
      case 'ArrowRight': case 'ArrowDown': case ' ': case 'PageDown':
        e.preventDefault(); next(); break;
      case 'ArrowLeft': case 'ArrowUp': case 'Backspace': case 'PageUp':
        e.preventDefault(); prev(); break;
      case 'Home': e.preventDefault(); goto(0); break;
      case 'End':  e.preventDefault(); goto(slides.length - 1); break;
      case 'n': case 'N':
        document.body.classList.toggle('notes-on'); fit(); break;
      case 'o': case 'O':
        document.body.classList.toggle('overview-on'); break;
      case 'Escape':
        document.body.classList.toggle('overview-on'); break;
      case 'f': case 'F':
        if (document.fullscreenElement) document.exitFullscreen();
        else document.documentElement.requestFullscreen();
        break;
      case 'p': case 'P':
        document.body.classList.toggle('print-preview');
        window.print();
        break;
    }
  });

  /* --------------------------------------------------------------------- chạm */

  var tx = null;
  document.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (tx === null) return;
    var dx = e.changedTouches[0].clientX - tx;
    if (Math.abs(dx) > 48) { dx < 0 ? next() : prev(); }
    tx = null;
  }, { passive: true });

  /* ----------------------------------------------------------------------- khởi động */

  window.addEventListener('resize', fit);
  window.addEventListener('beforeprint', function () {
    document.querySelectorAll('[data-step]').forEach(function (el) { el.classList.add('on'); });
    document.querySelectorAll('[data-dim-until]').forEach(function (el) { el.classList.remove('dim'); });
  });
  window.addEventListener('afterprint', applySteps);

  fit();
  var h = (location.hash || '').match(/^#s(\d+)$/);
  show(h ? parseInt(h[1], 10) - 1 : 0);
})();
