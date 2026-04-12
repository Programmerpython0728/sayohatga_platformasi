function initGalleries() {
  document.querySelectorAll("[data-gallery]").forEach((gallery) => {
    const main = gallery.querySelector("[data-gallery-main]");
    if (!main) return;
    gallery.querySelectorAll("[data-gallery-thumb]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const src = btn.getAttribute("data-src");
        if (!src) return;
        main.style.backgroundImage = `url('${src}')`;
      });
    });
  });
}

function initRegionCityFilter() {
  const regionSelect = document.querySelector("[data-filter-region]");
  const citySelect = document.querySelector("[data-filter-city]");
  if (!regionSelect || !citySelect) return;

  const update = () => {
    const regionId = regionSelect.value;
    const selectedCity = citySelect.value;
    let selectedCityVisible = false;

    Array.from(citySelect.options).forEach((opt) => {
      const optRegion = opt.getAttribute("data-region") || "";
      if (!opt.value) {
        opt.hidden = false;
        return;
      }
      if (!regionId) {
        opt.hidden = false;
        if (opt.value === selectedCity) selectedCityVisible = true;
        return;
      }
      const visible = optRegion === regionId;
      opt.hidden = !visible;
      if (visible && opt.value === selectedCity) selectedCityVisible = true;
    });

    if (selectedCity && !selectedCityVisible) {
      citySelect.value = "";
    }
  };

  regionSelect.addEventListener("change", update);
  update();
}

function initReveal() {
  const items = Array.from(document.querySelectorAll(".reveal"));
  if (!items.length) return;

  if (!("IntersectionObserver" in window)) {
    items.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "80px 0px", threshold: 0.08 },
  );

  items.forEach((el, idx) => {
    el.style.transitionDelay = `${Math.min(idx * 35, 240)}ms`;
    io.observe(el);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initGalleries();
  initRegionCityFilter();
  initReveal();
  initLikes();
  initBasket();
  initCarousel();
  initMobileMenu();
});

function initMobileMenu() {
  const btn = document.querySelector("[data-menu-toggle]");
  const nav = document.querySelector("[data-mobile-nav]");
  if (!btn || !nav) return;

  const close = () => document.body.classList.remove("menu-open");
  const toggle = () => document.body.classList.toggle("menu-open");

  btn.addEventListener("click", toggle);
  nav.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (a) close();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return "";
}

function initLikes() {
  const buttons = Array.from(document.querySelectorAll("[data-like]"));
  if (!buttons.length) return;

  const csrf = getCookie("csrftoken");
  const likeUrl = (window.SAYOHATGA && window.SAYOHATGA.likeToggleUrl) || "/catalog/like/toggle/";
  const loginUrl = (window.SAYOHATGA && window.SAYOHATGA.loginUrl) || "/accounts/login/";
  buttons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!csrf) {
        // Likely logged out. Let the server handle, but provide a hint.
        window.location.href = loginUrl;
        return;
      }
      const kind = btn.getAttribute("data-kind");
      const id = btn.getAttribute("data-id");
      try {
        const form = new FormData();
        form.append("kind", kind || "");
        form.append("id", id || "");
        const res = await fetch(likeUrl, {
          method: "POST",
          headers: { "X-CSRFToken": csrf },
          body: form,
        });
        const data = await res.json();
        if (!data.ok) return;
        btn.classList.toggle("is-liked", !!data.liked);
        const countEl = btn.querySelector(".like-count");
        if (countEl) countEl.textContent = String(data.count ?? 0);
      } catch (e) {
        // ignore
      }
    });
  });
}

function initBasket() {
  const buttons = Array.from(document.querySelectorAll("[data-basket]"));
  if (!buttons.length) return;
  const csrf = getCookie("csrftoken");
  const basketUrl = (window.SAYOHATGA && window.SAYOHATGA.basketToggleUrl) || "/catalog/basket/toggle/";

  buttons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        const form = new FormData();
        form.append("kind", btn.getAttribute("data-kind") || "");
        form.append("id", btn.getAttribute("data-id") || "");
        const res = await fetch(basketUrl, {
          method: "POST",
          headers: { "X-CSRFToken": csrf },
          body: form,
        });
        const data = await res.json();
        if (!data.ok) return;
        btn.classList.toggle("is-selected", !!data.in_basket);
        const basketCount = document.querySelector(".basket-count");
        if (basketCount) {
          basketCount.textContent = String(data.count ?? 0);
        } else if (data.count) {
          const navBasket = document.querySelector(".nav-link--basket");
          if (navBasket) {
            const span = document.createElement("span");
            span.className = "basket-count";
            span.textContent = String(data.count);
            navBasket.append(" ", span);
          }
        }
      } catch (e) {
        // ignore
      }
    });
  });
}

function initCarousel() {
  const root = document.querySelector("[data-carousel]");
  if (!root) return;

  const slides = Array.from(root.querySelectorAll("[data-slide]"));
  const dots = Array.from(root.querySelectorAll("[data-dot]"));
  const prev = root.querySelector("[data-prev]");
  const next = root.querySelector("[data-next]");
  if (!slides.length) return;

  let idx = 0;
  let timer = null;

  const set = (i) => {
    idx = (i + slides.length) % slides.length;
    slides.forEach((s, n) => s.classList.toggle("is-active", n === idx));
    dots.forEach((d, n) => d.classList.toggle("is-active", n === idx));
  };

  const start = () => {
    stop();
    timer = window.setInterval(() => set(idx + 1), 5200);
  };
  const stop = () => {
    if (timer) window.clearInterval(timer);
    timer = null;
  };

  prev?.addEventListener("click", () => {
    set(idx - 1);
    start();
  });
  next?.addEventListener("click", () => {
    set(idx + 1);
    start();
  });
  dots.forEach((d, n) =>
    d.addEventListener("click", () => {
      set(n);
      start();
    }),
  );

  root.addEventListener("mouseenter", stop);
  root.addEventListener("mouseleave", start);
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stop();
    else start();
  });

  set(0);
  start();
}
