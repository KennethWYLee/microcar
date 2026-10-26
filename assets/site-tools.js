const siteRoot = new URL("../", import.meta.url);
const iconSprite = new URL("./vendor/lucide/icons.svg", import.meta.url);

const makeIcon = name => {
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  const use = document.createElementNS("http://www.w3.org/2000/svg", "use");
  svg.classList.add("site-icon");
  svg.setAttribute("viewBox", "0 0 24 24");
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("focusable", "false");
  use.setAttribute("href", `${iconSprite.href}#${name}`);
  svg.append(use);
  return svg;
};

const makeElement = (tag, className, text) => {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text) element.textContent = text;
  return element;
};

const editableTarget = target => target instanceof Element && (
  target.closest("input, textarea, select") || target.closest('[contenteditable]:not([contenteditable="false"])')
);

const initSearch = () => {
  const toolbar = document.querySelector(".site-header .header-actions, .site-header .nav-controls");
  if (!toolbar || document.getElementById("site-search")) return;

  const trigger = makeElement("button", "search-trigger");
  trigger.type = "button";
  trigger.setAttribute("aria-label", "搜尋教材");
  trigger.setAttribute("aria-haspopup", "dialog");
  trigger.setAttribute("aria-controls", "site-search");
  trigger.setAttribute("aria-keyshortcuts", "Control+K Meta+K");
  trigger.append(makeIcon("search"), makeElement("span", "search-trigger-label", "搜尋教材"));
  const shortcut = makeElement("kbd", "search-shortcut", "Ctrl K");
  shortcut.setAttribute("aria-hidden", "true");
  trigger.append(shortcut);
  toolbar.prepend(trigger);

  const dialog = makeElement("dialog", "search-dialog");
  dialog.id = "site-search";
  dialog.setAttribute("aria-labelledby", "site-search-title");
  const heading = makeElement("div", "search-heading");
  heading.append(makeElement("h2", "search-title", "搜尋教材"));
  heading.firstElementChild.id = "site-search-title";
  const close = makeElement("button", "search-close");
  close.type = "button";
  close.setAttribute("aria-label", "關閉搜尋");
  close.append(makeIcon("x"));
  heading.append(close);

  const form = makeElement("form", "search-form");
  form.setAttribute("role", "search");
  const label = makeElement("label", "search-label", "輸入教材關鍵字");
  label.htmlFor = "site-search-input";
  const field = makeElement("div", "search-field");
  const input = makeElement("input", "search-input");
  input.id = "site-search-input";
  input.type = "search";
  input.placeholder = "搜尋 LED、循跡、UDP…";
  input.autocomplete = "off";
  input.spellcheck = false;
  input.setAttribute("autocapitalize", "off");
  input.setAttribute("enterkeyhint", "search");
  input.setAttribute("aria-describedby", "site-search-status");
  field.append(makeIcon("search"), input);
  form.append(label, field);

  const status = makeElement("p", "search-status", "正在準備搜尋…");
  status.id = "site-search-status";
  status.setAttribute("role", "status");
  status.setAttribute("aria-live", "polite");
  const results = makeElement("div", "search-results");
  results.id = "site-search-results";
  input.setAttribute("aria-controls", results.id);
  const hint = makeElement("p", "search-hint", "Enter 開啟第一項結果 · Esc 關閉");
  dialog.append(heading, form, status, results, hint);
  document.body.append(dialog);

  let records = [];
  let fuse = null;
  let loadPromise = null;
  let request = 0;
  let composing = false;
  let returnFocus = trigger;

  const safeURL = value => {
    const url = new URL(value, siteRoot);
    if (url.origin !== siteRoot.origin || !url.pathname.startsWith(siteRoot.pathname)) {
      throw new Error("Search result must stay inside the website.");
    }
    return url.href;
  };

  const loadSearch = () => {
    if (fuse) return Promise.resolve();
    if (loadPromise) return loadPromise;
    loadPromise = Promise.all([
      import("./vendor/fuse/fuse.min.mjs"),
      fetch(new URL("./search-index.json", import.meta.url)).then(response => {
        if (!response.ok) throw new Error(`Search index: ${response.status}`);
        return response.json();
      })
    ]).then(([library, index]) => {
      if (!Array.isArray(index)) throw new Error("Invalid search index.");
      records = index.map(item => {
        if (!item || typeof item.title !== "string" || typeof item.url !== "string") {
          throw new Error("Invalid search entry.");
        }
        return {
          title: item.title,
          category: String(item.category || "教材"),
          summary: String(item.summary || ""),
          keywords: Array.isArray(item.keywords) ? item.keywords.join(" ") : String(item.keywords || ""),
          url: safeURL(item.url)
        };
      });
      fuse = new library.default(records, {
        keys: [
          { name: "title", weight: 0.6 },
          { name: "keywords", weight: 0.25 },
          { name: "category", weight: 0.1 },
          { name: "summary", weight: 0.05 }
        ],
        threshold: 0.32,
        ignoreLocation: true,
        minMatchCharLength: 1
      });
    }).catch(error => {
      loadPromise = null;
      throw error;
    });
    return loadPromise;
  };

  const showError = () => {
    status.textContent = "搜尋暫時無法載入。";
    results.replaceChildren();
    const empty = makeElement("div", "search-empty");
    empty.append(makeElement("p", "", "請重試，或從課程總覽與下載區查找教材。"));
    const retry = makeElement("button", "button ghost search-retry", "重新載入搜尋");
    retry.type = "button";
    retry.addEventListener("click", () => {
      input.focus();
      runSearch();
    });
    const topics = makeElement("a", "search-fallback-link", "查看課程總覽");
    topics.href = new URL("index.html#topic-roadmap", siteRoot).href;
    const downloads = makeElement("a", "search-fallback-link", "前往下載區");
    downloads.href = new URL("downloads.html", siteRoot).href;
    empty.append(retry, topics, downloads);
    results.append(empty);
  };

  const renderResults = (items, query) => {
    results.replaceChildren();
    status.textContent = query ? `顯示 ${items.length} 項符合的教材` : "常用入口";
    if (!items.length) {
      results.append(makeElement("p", "search-empty", "找不到符合的教材，請換個關鍵字，例如 LED、馬達或循跡。"));
      return;
    }
    for (const item of items) {
      const link = makeElement("a", "search-result");
      link.href = item.url;
      const copy = makeElement("div", "search-result-copy");
      copy.append(makeElement("small", "search-result-category", item.category));
      copy.append(makeElement("strong", "search-result-title", item.title));
      if (item.summary) copy.append(makeElement("p", "search-result-summary", item.summary));
      link.append(copy, makeIcon("arrow-up-right"));
      results.append(link);
    }
  };

  const findResults = query => {
    if (!query) return records.slice(0, 5);
    const normalized = query.toLocaleLowerCase();
    const direct = records.filter(item => item.title.toLocaleLowerCase().includes(normalized));
    const fuzzy = fuse.search(query, { limit: 40 }).map(result => result.item);
    const unique = new Map([...direct, ...fuzzy].map(item => [item.url, item]));
    const rank = item => {
      const title = item.title.toLocaleLowerCase();
      return title === normalized ? 0 : title.includes(normalized) ? 1 : 2;
    };
    return [...unique.values()].sort((a, b) => rank(a) - rank(b)).slice(0, 10);
  };

  const runSearch = async () => {
    const revision = ++request;
    const query = input.value.trim();
    if (!fuse) {
      status.textContent = "正在載入教材索引…";
      results.replaceChildren();
      results.setAttribute("aria-busy", "true");
    }
    try {
      await loadSearch();
      if (revision !== request || !dialog.open) return;
      renderResults(findResults(query), query);
    } catch {
      if (revision === request && dialog.open) showError();
    } finally {
      if (revision === request) results.removeAttribute("aria-busy");
    }
  };

  const openSearch = () => {
    if (dialog.open) return;
    returnFocus = document.activeElement instanceof HTMLElement && document.activeElement !== document.body
      ? document.activeElement : trigger;
    dialog.showModal();
    document.body.classList.add("search-open");
    input.focus({ preventScroll: true });
    input.select();
    runSearch();
  };

  trigger.addEventListener("click", openSearch);
  close.addEventListener("click", () => dialog.close());
  dialog.addEventListener("close", () => {
    request += 1;
    results.removeAttribute("aria-busy");
    document.body.classList.remove("search-open");
    (returnFocus.isConnected ? returnFocus : trigger).focus({ preventScroll: true });
  });
  dialog.addEventListener("keydown", event => {
    if (event.key !== "Tab") return;
    const focusable = [...dialog.querySelectorAll('button:not([disabled]), input:not([disabled]), a[href]')]
      .filter(element => element.getClientRects().length);
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last?.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first?.focus();
    }
  });
  dialog.addEventListener("click", event => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) {
      dialog.close();
    }
  });
  document.addEventListener("keydown", event => {
    if ((event.ctrlKey || event.metaKey) && !event.altKey && event.key.toLowerCase() === "k" && !editableTarget(event.target)) {
      event.preventDefault();
      openSearch();
    }
  });
  input.addEventListener("compositionstart", () => { composing = true; });
  input.addEventListener("compositionend", () => { composing = false; runSearch(); });
  input.addEventListener("input", () => { if (!composing) runSearch(); });
  input.addEventListener("keydown", event => {
    if (!composing && event.key === "ArrowDown") {
      const first = results.querySelector("a.search-result");
      if (first) {
        event.preventDefault();
        first.focus();
      }
    }
  });
  form.addEventListener("submit", event => {
    event.preventDefault();
    if (composing) return;
    const first = results.querySelector("a.search-result");
    if (first) {
      dialog.close();
      window.location.assign(first.href);
    }
  });
  results.addEventListener("click", event => {
    if (event.defaultPrevented || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    if (event.target instanceof Element && event.target.closest("a.search-result")) dialog.close();
  });
  results.addEventListener("keydown", event => {
    if (event.key !== "ArrowDown" && event.key !== "ArrowUp") return;
    const links = [...results.querySelectorAll("a.search-result")];
    const position = links.indexOf(document.activeElement);
    if (position < 0) return;
    event.preventDefault();
    if (event.key === "ArrowUp" && position === 0) input.focus();
    else links[(position + (event.key === "ArrowDown" ? 1 : -1) + links.length) % links.length].focus();
  });
};

if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initSearch, { once: true });
else initSearch();
