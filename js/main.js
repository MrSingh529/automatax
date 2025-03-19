// Select the glass navigation container and its effect elements
const nav = document.querySelector("nav.glass-nav");
const effectEl = document.querySelector(".effect.filter");
const textEl = document.querySelector(".effect.text");

let animationTime = 600;
let pCount = 15;
const timeVariance = 300;

function noise(n = 1) {
  return n / 2 - Math.random() * n;
}

function getXY(distance, pointIndex, totalPoints) {
  const angle = ((360 + noise(8)) / totalPoints) * pointIndex;
  const rad = angle * Math.PI / 180;
  const x = distance * Math.cos(rad);
  const y = distance * Math.sin(rad);
  return [x, y];
}

function makeParticles($el) {
  const d = [90, 10];
  const r = 100;
  const bubbleTime = animationTime * 2 + timeVariance;
  $el.style.setProperty('--time', bubbleTime + 'ms');

  for (let i = 0; i < pCount; i++) {
    const t = animationTime * 2 + noise(timeVariance * 2);
    const p = createParticle(i, t, d, r);
    setTimeout(() => {
      const particle = document.createElement('span');
      const point = document.createElement('span');
      particle.classList.add('particle');
      particle.style.cssText = `
        --start-x: ${getXY(d[1], pCount - i, pCount)[0]}px;
        --start-y: ${getXY(d[1], pCount - i, pCount)[1]}px;
        --end-x: ${getXY(d[0], pCount - i, pCount)[0]}px;
        --end-y: ${getXY(d[0], pCount - i, pCount)[1]}px;
        --time: ${t}ms;
        --scale: ${1 + noise(0.2)};
        --rotate: ${noise(r / 10) * 10}deg;
      `;
      point.classList.add('point');
      particle.appendChild(point);
      $el.appendChild(particle);
      requestAnimationFrame(() => {
        $el.classList.add('active');
      });
      setTimeout(() => {
        $el.removeChild(particle);
      }, t);
    }, 30);
  }
}

function updateEffectPosition(element) {
  const pos = element.getBoundingClientRect();
  const styles = {
    left: `${pos.x}px`,
    top: `${pos.y}px`,
    width: `${pos.width}px`,
    height: `${pos.height}px`
  };
  Object.assign(effectEl.style, styles);
  Object.assign(textEl.style, styles);
  textEl.innerText = element.innerText;
}

// Set up click and keyboard events on nav items
nav.querySelectorAll('ul li').forEach($el => {
  const link = $el.querySelector('a');

  const handleClick = (e) => {
    updateEffectPosition($el);
    if (!$el.classList.contains('active')) {
      nav.querySelectorAll('ul li').forEach(item => item.classList.remove('active'));
      effectEl.querySelectorAll('.particle').forEach(particle => effectEl.removeChild(particle));
      $el.classList.add('active');
      textEl.classList.remove('active');
      setTimeout(() => {
        textEl.classList.add('active');
      }, 100);
      makeParticles(effectEl);
    }
  };

  $el.addEventListener('click', handleClick);
  link.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick(e);
    }
  });
});

// Reposition effect element on window resize
const resizeObserver = new ResizeObserver(() => {
  const activeEl = nav.querySelector('ul li.active');
  if (activeEl) {
    updateEffectPosition(activeEl);
  }
});
resizeObserver.observe(document.body);

// Optional: Trigger initial active state on first nav item after a brief delay
setTimeout(() => {
  nav.querySelector('ul li').click();
}, 200);
