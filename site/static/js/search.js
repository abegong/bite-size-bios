const searchRoot = document.querySelector("[data-site-search]");

if (searchRoot) {
  const form = searchRoot.querySelector("[data-site-search-form]");
  const input = searchRoot.querySelector("[data-site-search-input]");
  const results = searchRoot.querySelector("[data-site-search-results]");
  const pagefindUrl = searchRoot.dataset.pagefindUrl;
  let pagefindPromise;
  let activeQuery = "";
  let debounceTimer;

  const loadPagefind = () => {
    pagefindPromise ||= import(pagefindUrl).catch(() => null);
    return pagefindPromise;
  };

  const clearResults = () => {
    results.replaceChildren();
    results.classList.add("hidden");
  };

  const showStatus = (message) => {
    results.replaceChildren();
    const item = document.createElement("div");
    item.className = "px-4 py-3 text-sm text-gray-500 dark:text-gray-400";
    item.textContent = message;
    results.append(item);
    results.classList.remove("hidden");
  };

  const renderResults = async (query, matches) => {
    if (query !== activeQuery) return;

    results.replaceChildren();

    if (!matches.length) {
      showStatus("No results");
      return;
    }

    const list = document.createElement("div");
    list.className = "divide-y divide-gray-100 dark:divide-warmgray-700";

    const resultData = await Promise.all(matches.slice(0, 6).map((match) => match.data()));
    if (query !== activeQuery) return;

    resultData.forEach((result) => {
      const link = document.createElement("a");
      link.href = result.url;
      link.className = "block px-4 py-3 transition-colors duration-150 hover:bg-gray-50 dark:hover:bg-warmgray-800";

      const header = document.createElement("div");
      header.className = "flex items-center justify-between gap-2";

      const title = document.createElement("div");
      title.className = "text-sm font-semibold text-gray-900 dark:text-white";
      title.textContent = result.meta?.title || result.url;
      header.append(title);

      if (result.meta?.length) {
        const badge = document.createElement("span");
        badge.className = "bio-chip rounded-full px-3 py-0.5 text-xs font-medium";
        badge.textContent = result.meta.length;
        header.append(badge);
      }

      const excerpt = document.createElement("div");
      excerpt.className = "mt-1 line-clamp-2 text-xs leading-relaxed text-gray-600 dark:text-gray-300";
      excerpt.innerHTML = result.excerpt || "";

      link.append(header, excerpt);
      list.append(link);
    });

    results.append(list);
    results.classList.remove("hidden");
  };

  const search = async () => {
    const query = input.value.trim();
    activeQuery = query;

    if (query.length < 2) {
      clearResults();
      return;
    }

    showStatus("Searching...");
    const pagefind = await loadPagefind();

    if (!pagefind || query !== activeQuery) {
      showStatus("Search is unavailable");
      return;
    }

    try {
      const response = await pagefind.search(query);
      await renderResults(query, response?.results || []);
    } catch {
      if (query === activeQuery) {
        showStatus("Search is unavailable");
      }
    }
  };

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    search();
  });

  input.addEventListener("input", () => {
    window.clearTimeout(debounceTimer);
    debounceTimer = window.setTimeout(search, 150);
  });

  input.addEventListener("focus", () => {
    if (input.value.trim().length >= 2 && results.children.length) {
      results.classList.remove("hidden");
    }
  });

  document.addEventListener("click", (event) => {
    if (!searchRoot.contains(event.target)) {
      results.classList.add("hidden");
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      results.classList.add("hidden");
      input.blur();
    }
  });
}
