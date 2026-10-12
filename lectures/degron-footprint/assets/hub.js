/* Hub đặc hiệu E3–degron — hành vi dùng chung cho mọi trang.
   Script cổ điển (không phải module) để chạy được qua file://.
   Mọi thứ đều là tăng cường: trang vẫn đọc được đầy đủ khi tắt JavaScript. */
(function () {
  "use strict";

  var root = document.documentElement;
  var KEY_THEME = "degron-hub-theme";
  var KEY_MOTION = "degron-hub-motion";
  var KEY_DONE = "degron-hub-done";

  function read(key, fallback) {
    try { var v = localStorage.getItem(key); return v === null ? fallback : v; }
    catch (e) { return fallback; }
  }
  function write(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* chế độ riêng tư: bỏ qua */ }
  }

  /* ---------------------------------------------------------- giao diện */
  var theme = read(KEY_THEME, "auto");
  if (theme === "light" || theme === "dark") root.dataset.theme = theme;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  var motion = read(KEY_MOTION, reduced.matches ? "off" : "on");
  if (reduced.matches) motion = "off";
  root.dataset.motion = motion;

  function buildBar() {
    var bar = document.querySelector(".topbar");
    if (!bar) return;
    var spacer = bar.querySelector(".spacer");
    if (!spacer) { spacer = document.createElement("span"); spacer.className = "spacer"; bar.appendChild(spacer); }

    var tBtn = document.createElement("button");
    tBtn.type = "button";
    tBtn.className = "ctrl";
    var label = { auto: "Giao diện: theo hệ thống", light: "Giao diện: sáng", dark: "Giao diện: tối" };
    tBtn.textContent = label[theme] || label.auto;
    tBtn.addEventListener("click", function () {
      theme = theme === "auto" ? "light" : theme === "light" ? "dark" : "auto";
      if (theme === "auto") delete root.dataset.theme; else root.dataset.theme = theme;
      tBtn.textContent = label[theme];
      write(KEY_THEME, theme);
    });
    bar.appendChild(tBtn);

    var mBtn = document.createElement("button");
    mBtn.type = "button";
    mBtn.className = "ctrl";
    function paint() {
      if (reduced.matches) {
        mBtn.textContent = "Đã giảm chuyển động theo hệ thống";
        mBtn.disabled = true;
      } else {
        mBtn.textContent = motion === "on" ? "Tạm dừng hoạt ảnh" : "Bật hoạt ảnh";
        mBtn.setAttribute("aria-pressed", String(motion === "off"));
      }
    }
    paint();
    mBtn.addEventListener("click", function () {
      motion = motion === "on" ? "off" : "on";
      root.dataset.motion = motion;
      write(KEY_MOTION, motion);
      paint();
    });
    bar.appendChild(mBtn);

    reduced.addEventListener("change", function () {
      if (reduced.matches) { motion = "off"; root.dataset.motion = "off"; }
      paint();
    });
  }

  /* ------------------------------------------- đánh dấu trang đã đọc xong */
  function doneSet() {
    try { return JSON.parse(read(KEY_DONE, "{}")) || {}; } catch (e) { return {}; }
  }
  function pageId() {
    var m = document.querySelector('meta[name="hub-page"]');
    return m ? m.getAttribute("content") : null;
  }

  function buildDoneToggle() {
    var id = pageId();
    if (!id) return;
    var host = document.querySelector("[data-done-slot]");
    if (!host) return;
    var set = doneSet();
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "ctrl";
    function paint() {
      btn.textContent = set[id] ? "✓ Đã học xong bài này" : "Đánh dấu đã học xong";
      btn.setAttribute("aria-pressed", String(!!set[id]));
    }
    paint();
    btn.addEventListener("click", function () {
      if (set[id]) delete set[id]; else set[id] = 1;
      write(KEY_DONE, JSON.stringify(set));
      paint();
    });
    host.appendChild(btn);
  }

  /* đánh dấu các liên kết đã học trên trang hub */
  function markDoneLinks() {
    var set = doneSet();
    var ids = Object.keys(set);
    if (!ids.length) return;
    document.querySelectorAll("[data-page-id]").forEach(function (el) {
      if (set[el.getAttribute("data-page-id")]) el.classList.add("done");
    });
    var out = document.getElementById("progress");
    if (out) {
      out.textContent = "Bạn đã đánh dấu học xong " + ids.length + " trang. " +
        "Dấu ✓ hiện bên cạnh các trang đã học. Trạng thái này chỉ lưu trong trình duyệt bạn đang dùng.";
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }

  function init() {
    buildBar();
    buildDoneToggle();
    markDoneLinks();
  }
})();
