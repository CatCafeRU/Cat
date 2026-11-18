(function () {
  const root = document.getElementById('carousel');
  if (!root) return;

  const slides = root.querySelectorAll('.carousel-slide');
  const dots   = root.querySelectorAll('.carousel-dots .dot');
  if (!slides.length) return;

  let i = 0;
  let timer = null;
  const DELAY = 5000;

  function show(idx) {
    i = (idx + slides.length) % slides.length;
    slides.forEach((s, k) => s.classList.toggle('active', k === i));
    dots.forEach((d, k) => d.classList.toggle('active', k === i));
  }

  function start() {
    stop();
    timer = setInterval(() => show(i + 1), DELAY);
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }

  root.querySelectorAll('.carousel-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      show(i + Number(btn.dataset.dir));
      start();
    });
  });
  dots.forEach(dot => {
    dot.addEventListener('click', () => {
      show(Number(dot.dataset.index));
      start();
    });
  });

  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', start);

  show(0);
  start();
})();