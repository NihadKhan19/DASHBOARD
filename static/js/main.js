// Formula-bar typing animation in the hero
(function () {
  const el = document.getElementById("formulaInput");
  if (!el) return;

  const words = window.__profileWords || ["Curiosity", "Rigor", "Clarity", "Impact"];
  const full = "=CONCAT(" + words.join(", ") + ") → Insight";
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (prefersReducedMotion) {
    el.textContent = full;
    return;
  }

  let i = 0;
  function type() {
    el.textContent = full.slice(0, i);
    i++;
    if (i <= full.length) {
      setTimeout(type, 38);
    } else {
      el.style.borderRight = "none";
    }
  }
  type();
})();

// Highlight the active sheet tab based on scroll position
(function () {
  const tabs = Array.from(document.querySelectorAll(".sheet-tab"));
  if (!tabs.length || !document.body.contains(document.getElementById("about"))) return;

  const sections = tabs
    .map((tab) => {
      const hash = tab.getAttribute("href").split("#")[1];
      return hash ? document.getElementById(hash) : null;
    })
    .filter(Boolean);

  if (!sections.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.id;
          tabs.forEach((tab) => {
            tab.style.background = tab.getAttribute("href").includes(id) ? "var(--paper-raised)" : "";
            tab.style.color = tab.getAttribute("href").includes(id) ? "var(--ink)" : "";
          });
        }
      });
    },
    { rootMargin: "-40% 0px -50% 0px" }
  );

  sections.forEach((s) => observer.observe(s));
})();
