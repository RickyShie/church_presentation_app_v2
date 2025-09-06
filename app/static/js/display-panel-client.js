function showLayout(id) {
        if (!id || !layouts.includes(id)) return;
        document.querySelectorAll(".layout").forEach(sec => sec.classList.remove("active"));
        document.getElementById(id)?.classList.add("active");
        if (pill) pill.textContent = "Current: " + id;
        // update URL hash without reloading
        if (history.pushState) history.replaceState(null, "", location.pathname + "?id=" + encodeURIComponent(id));
}
const layouts = ["bible-search", "hymn-search", "display-announcement"];
const pill = document.getElementById("current-pill");
const socket = io();
socket.on("layout_changed", (data) => {
    showLayout(data.layout);
});

function getEmbeddableSlidesUrl(input) {
  try {
    const u = new URL(input);

    const isGoogle = u.hostname.endsWith('google.com');
    const isSlides = u.pathname.includes('/presentation/');
    const isEmbed = u.pathname.includes('/embed') || u.pathname.includes('/pub');

    if (isGoogle && isSlides && isEmbed) return u.href;
    return null;
  } catch {
    // maybe the user pasted a full <iframe>; try to extract src=""
    const m = input.match(/src\s*=\s*"([^"]+)"/i);
    if (!m) return null;
    return getEmbeddableSlidesUrl(m[1]); // recurse check
  }
}

socket.on("bible_search_results", (data) => {
  const results = data.bible_search_results || [];

  // Which div gets which translation
  const containers = {
    KOUGO: "kougo-search-results",
    CUNP:  "cunp-search-results",
    NIV:   "niv-search-results",
  };

  // (optional) simple HTML escape
  const esc = (s) => String(s)
    .replace(/&/g,"&amp;").replace(/</g,"&lt;")
    .replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");

  // make one verse HTML block
  const verseHTML = (v) =>
    `<div class="verse"><sup class="verse-number">${v.verse}</sup>${esc(v.text)}</div>`;

  // group results by translation
  const byTrans = results.reduce((acc, r) => {
    (acc[r.translation] ||= []).push(r);
    return acc;
  }, {});

  // render into each container
  for (const [t, elId] of Object.entries(containers)) {
    const el = document.getElementById(elId);
    const items = byTrans[t] || [];
    el.innerHTML = items.length ? items.map(verseHTML).join("") : `<div class="muted">No results</div>`;
  }
});

socket.on("sermon_metadata", (data) => {
    const sermon_metadata = data.sermon_metadata || {};
    service_type = document.getElementById("service-type");
    service_type.textContent = sermon_metadata.service_type;
    jp_sermon_topic = document.getElementById("jp-sermon-topic");
    jp_sermon_topic.textContent = sermon_metadata.jp_sermon_topic;
    cn_sermon_topic = document.getElementById("cn-sermon-topic");
    cn_sermon_topic.textContent = sermon_metadata.cn_sermon_topic;
    speaker_name = document.getElementById("speaker-name");
    speaker_name.textContent = `説教者：${sermon_metadata.speaker_name}`;
    interpreter_name = document.getElementById("interpreter-name");
    interpreter_name.textContent = `通訳者：${sermon_metadata.interpreter_name}`;
    hymns = document.getElementById("hymns");
    opening_hymn = sermon_metadata.opening_hymn;
    closing_hymn = sermon_metadata.closing_hymn;
    hymns.innerHTML = `讚美詩${opening_hymn}<br/>讚美詩${closing_hymn}`;
    pianist_name = document.getElementById("pianist-name");
    pianist_name.textContent = `ピアノ：${sermon_metadata.pianist_name}`;
});

socket.on("google_slides_url_result", (data) => {
  const container = document.getElementById("google-slides");
  const raw = (data?.google_slides_url_result || "").trim();

  const url = getEmbeddableSlidesUrl(raw);
  if (!url) {
    console.warn("Not an embeddable Slides URL. Use Publish → Embed.");
    return;
  }

  const iframe = document.createElement("iframe");
  iframe.id = "google-slides";
  iframe.src = url;
  iframe.width = "100%";
  iframe.height = "600";
  iframe.setAttribute("frameborder", "0");
  iframe.setAttribute("allowfullscreen", "true");
  iframe.setAttribute("loading", "lazy");
  // Needed for Google to run its player:
  iframe.setAttribute("sandbox", "allow-scripts allow-same-origin allow-presentation");

  container.parentNode.replaceChild(iframe, container);
});