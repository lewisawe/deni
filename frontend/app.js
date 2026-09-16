// Deni UI: before-flow (pick or paste), multilingual explain, during-flow recourse.
const $ = (id) => document.getElementById(id);
let CURRENCY = { code: "KES", symbol: "KES", locale: "en-KE" };
const fmt = (n) => Number(n).toLocaleString(CURRENCY.locale || "en-KE", { maximumFractionDigits: 0 });
const money = (n) => `${CURRENCY.symbol} ${fmt(n)}`;
let LANG = "en";
let COUNTRY = "ke";
let META = { authority_short: "CBK", authority_name: "the regulator", examples: "e.g. a lender's name" };

/* ---------- UI string dictionary (real interface translation, en/sw/sheng) ----------
   The whole interface translates on toggle, not just the AI explanation, so a
   Kiswahili- or Sheng-only speaker can navigate. Works fully offline (no AI needed). */
const I18N = {
  en: {
    hero_pre: "Know your ", hero_hl: "rights", hero_post: " as a borrower.",
    hero_lead: "Deni helps you understand what a lender can and can't do, check whether they're licensed, see what a loan really costs, and take action with the right public body, on any phone, in your language. Not legal advice; every fact is sourced.",
    door_rights: "Know your rights", door_lender: "Check a lender", door_cost: "Check a loan's cost",
    rights_intro: "Read what Kenyan law says about how lenders must treat you, before anything goes wrong.",
    loading_rights: "Loading your rights…",
    lender_label: "Is this lender licensed/registered with {authority}?",
    lender_ph: "e.g. Tala, Mogo, QuickCash", lender_btn: "Check the register",
    cost_intro_pre: "See what a loan will ", cost_intro_hl: "really", cost_intro_post: " cost. The true price behind the daily/weekly framing.",
    pick_loan: "Pick a loan", or_paste: "or paste the SMS the lender sent you",
    sms_ph: "e.g. Congrats! You qualify for KES 1,000. Repay KES 1,150 in 30 days.",
    parse_btn: "Read my offer",
    action_title: "Something already went wrong? Take action.",
    action_intro: "Harassment, repossession, a wrongful CRB listing, or money you want back? Describe it. Deni tells you the law, which public body handles it, and drafts your complaint or claim with a case reference.",
    problem_ph: "e.g. They are calling everyone in my phone and threatening to take my boda.",
    recourse_btn: "Show me what to do",
    whatnext_title: "What you can do next", wn_rights: "Know your rights",
    wn_report: "Report this lender to {authority}", wn_action: "Take action on a problem",
    computing: "Computing…", finding: "Finding your rights…", reading: "Reading…",
    source: "Source", go_to: "Go to",
  },
  sw: {
    hero_pre: "Fahamu ", hero_hl: "haki zako", hero_post: " kama mkopaji.",
    hero_lead: "Deni inakusaidia kuelewa mkopeshaji anaweza na hawezi kufanya nini, kuangalia kama ana leseni, kuona gharama halisi ya mkopo, na kuchukua hatua na taasisi ya umma inayohusika, kwenye simu yoyote, kwa lugha yako. Si ushauri wa kisheria; kila ukweli una chanzo.",
    door_rights: "Fahamu haki zako", door_lender: "Angalia mkopeshaji", door_cost: "Angalia gharama ya mkopo",
    rights_intro: "Soma sheria ya Kenya inavyosema kuhusu jinsi wakopeshaji wanavyopaswa kukutendea, kabla mambo hayajaharibika.",
    loading_rights: "Inapakia haki zako…",
    lender_label: "Je, mkopeshaji huyu amesajiliwa na {authority}?",
    lender_ph: "mf. Tala, Mogo, QuickCash", lender_btn: "Angalia rejista",
    cost_intro_pre: "Ona mkopo utakugharimu ", cost_intro_hl: "kiasi gani hasa", cost_intro_post: ". Bei halisi nyuma ya maelezo ya kila siku/wiki.",
    pick_loan: "Chagua mkopo", or_paste: "au bandika SMS uliyotumiwa na mkopeshaji",
    sms_ph: "mf. Hongera! Umestahili KES 1,000. Lipa KES 1,150 katika siku 30.",
    parse_btn: "Soma ofa yangu",
    action_title: "Kuna kilichoharibika tayari? Chukua hatua.",
    action_intro: "Unyanyaswaji, kunyang'anywa mali, kuorodheshwa vibaya CRB, au pesa unazotaka kurudishiwa? Eleza. Deni inakuambia sheria, taasisi ya umma inayohusika, na kuandaa malalamiko au madai yako yenye nambari ya kumbukumbu.",
    problem_ph: "mf. Wanapiga simu kila mtu kwenye simu yangu na kutishia kuchukua boda yangu.",
    recourse_btn: "Nionyeshe la kufanya",
    whatnext_title: "Unachoweza kufanya sasa", wn_rights: "Fahamu haki zako",
    wn_report: "Ripoti mkopeshaji huyu kwa {authority}", wn_action: "Chukua hatua kuhusu tatizo",
    computing: "Inakokotoa…", finding: "Inatafuta haki zako…", reading: "Inasoma…",
    source: "Chanzo", go_to: "Nenda",
  },
  sheng: {
    hero_pre: "Jua ", hero_hl: "haki zako", hero_post: " kama mtu wa mkopo.",
    hero_lead: "Deni inakusaidia kuelewa venye lender anaweza na hawezi kufanya, kucheki kama ako na leseni, kuona mkopo itakugharimu pesa ngapi kwa uhalisia, na kuchukua hatua na ile ofisi ya serikali inafaa, kwa simu yoyote, kwa lugha yako. Si ushauri wa mawakili; kila kitu kina chanzo.",
    door_rights: "Jua haki zako", door_lender: "Cheki lender", door_cost: "Cheki gharama ya mkopo",
    rights_intro: "Soma vile sheria ya Kenya inasema kuhusu venye malenda wanafaa kukutreat, kabla mambo iharibike.",
    loading_rights: "Inaload haki zako…",
    lender_label: "Huyu lender ako na leseni/amesajiliwa na {authority}?",
    lender_ph: "mf. Tala, Mogo, QuickCash", lender_btn: "Cheki rejista",
    cost_intro_pre: "Ona mkopo itakugharimu ", cost_intro_hl: "pesa ngapi kwa ukweli", cost_intro_post: ". Bei halisi nyuma ya story ya kila siku/wiki.",
    pick_loan: "Chagua mkopo", or_paste: "ama paste SMS ile lender alikutumia",
    sms_ph: "mf. Congrats! Umequalify KES 1,000. Lipa KES 1,150 kwa siku 30.",
    parse_btn: "Soma offer yangu",
    action_title: "Kuna kitu tayari imeharibika? Chukua hatua.",
    action_intro: "Wanakusumbua, wamechukua mali yako, umelistiwa vibaya CRB, ama kuna doo unataka urudishiwe? Elezea. Deni inakuambia sheria, ofisi gani ya serikali inashughulikia, na inaandaa complaint ama claim yako na reference number.",
    problem_ph: "mf. Wanapigia kila mtu kwa simu yangu na kutishia kuchukua boda yangu.",
    recourse_btn: "Nionyeshe nifanye aje",
    whatnext_title: "Vitu unaweza fanya sasa", wn_rights: "Jua haki zako",
    wn_report: "Report huyu lender kwa {authority}", wn_action: "Chukua hatua kuhusu shida",
    computing: "Inakalmap…", finding: "Inatafuta haki zako…", reading: "Inasoma…",
    source: "Chanzo", go_to: "Nenda",
  },
};
const BCP = { en: "en", sw: "sw", sheng: "sw" };
function t(key) { return (I18N[LANG] && I18N[LANG][key]) || I18N.en[key] || key; }

/* Apply the current language to every marked element + the document lang attribute. */
function applyLang() {
  document.documentElement.lang = BCP[LANG] || "en";
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const k = el.getAttribute("data-i18n");
    if (I18N[LANG] && I18N[LANG][k] != null) {
      el.textContent = I18N[LANG][k].replace("{authority}", (META && META.authority_name) || "the regulator");
    }
  });
  document.querySelectorAll("[data-i18n-ph]").forEach((el) => {
    const k = el.getAttribute("data-i18n-ph");
    if (I18N[LANG] && I18N[LANG][k] != null) el.setAttribute("placeholder", I18N[LANG][k]);
  });
}

/* ---------- language toggle ---------- */
document.querySelectorAll(".lang-btn").forEach((b) => {
  b.addEventListener("click", () => {
    LANG = b.dataset.lang;
    document.querySelectorAll(".lang-btn").forEach((x) =>
      x.setAttribute("aria-pressed", String(x === b)));
    applyLang();
    // Re-render the rights library in the new language (it's fetched fresh per language).
    RIGHTS_LOADED = false;
    if (document.querySelector('.door-btn[data-panel="rights"]').getAttribute("aria-selected") === "true") {
      loadRights();
    }
  });
});

/* ---------- helpers ---------- */
function licenceBadge(l) {
  const map = {
    licensed: ["Licensed by CBK", "var(--color-chartreuse-highlight)", "var(--color-carbon-black)"],
    unlicensed: ["NOT on CBK licensed list", "var(--color-signal-orange)", "var(--color-paper-white)"],
    "not-applicable": ["Not a CBK digital lender", "var(--color-paper-white)", "var(--color-carbon-black)"],
  };
  const [txt, bg, fg] = map[l.status] || map["not-applicable"];
  return `<span style="display:inline-block;padding:4px 10px;border:1px solid var(--color-carbon-black);
    border-radius:var(--radius-tags);background:${bg};color:${fg};
    font-family:var(--font-geist-mono);font-size:var(--text-caption);text-transform:uppercase;font-weight:500;">${txt}</span>`;
}

/* ---------- shareable Deni report (Copy / WhatsApp / Image / PDF) ---------- */
async function buildReceipt(kind, data) {
  return await (await fetch("/api/receipt", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ kind, data, lang: LANG }),
  })).json();
}

function receiptToImage(text) {
  // Render the receipt text to a PNG on canvas (Timescale: paper-white, mono).
  const lines = text.split("\n");
  const pad = 32, lh = 26, w = 720;
  const cvs = document.createElement("canvas");
  cvs.width = w; cvs.height = pad * 2 + lh * lines.length;
  const ctx = cvs.getContext("2d");
  ctx.fillStyle = "#fafafa"; ctx.fillRect(0, 0, cvs.width, cvs.height);
  ctx.fillStyle = "#000"; ctx.fillRect(0, 0, 6, cvs.height); // orange-ish rail
  ctx.fillStyle = "#ff5b29"; ctx.fillRect(0, 0, 6, cvs.height);
  lines.forEach((ln, i) => {
    const y = pad + lh * (i + 1);
    if (i === 0) { ctx.font = "700 22px 'JetBrains Mono', monospace"; ctx.fillStyle = "#ff5b29"; }
    else { ctx.font = "400 15px 'JetBrains Mono', monospace"; ctx.fillStyle = "#242424"; }
    ctx.fillText(ln, pad, y);
  });
  return cvs.toDataURL("image/png");
}

function shareBar(kind, data) {
  const el = document.createElement("div");
  el.className = "card-hard";
  el.style.marginTop = "var(--spacing-16)";
  el.innerHTML = `<p style="margin:0 0 8px;font-weight:600;">Keep or share this report</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      <button class="btn-primary" data-a="copy" style="padding:6px 16px;">Copy text</button>
      <button class="btn-primary" data-a="wa" style="padding:6px 16px;">WhatsApp</button>
      <button class="btn-primary" data-a="img" style="padding:6px 16px;">Image</button>
      <button class="btn-primary" data-a="pdf" style="padding:6px 16px;">PDF</button>
    </div><div data-note style="font-size:var(--text-caption);color:var(--color-graphite);margin-top:8px;"></div>`;
  const note = el.querySelector("[data-note]");
  el.querySelectorAll("button").forEach((b) => b.addEventListener("click", async () => {
    const r = await buildReceipt(kind, data);
    const text = r.text + (r.sources && r.sources.length ? "\n\nSources:\n" + r.sources.join("\n") : "");
    const act = b.dataset.a;
    if (act === "copy") {
      await navigator.clipboard.writeText(text); note.textContent = "Copied. Ref " + r.ref;
    } else if (act === "wa") {
      window.open("https://wa.me/?text=" + encodeURIComponent(text), "_blank");
    } else if (act === "img") {
      const a = document.createElement("a");
      a.href = receiptToImage(text); a.download = r.ref + ".png"; a.click();
    } else if (act === "pdf") {
      const w = window.open("", "_blank");
      w.document.write(`<pre style="font-family:monospace;white-space:pre-wrap;padding:24px;">${text}</pre>`);
      w.document.title = r.ref; w.document.close(); w.print();
    }
  }));
  return el;
}

async function explainInto(el, cost) {
  try {
    const e = await (await fetch("/api/explain", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cost, lang: LANG }),
    })).json();
    if (e.available && e.text) {
      el.innerHTML = `<p style="margin:var(--spacing-8) 0 0;font-style:italic;">${e.text}</p>`;
    }
  } catch (_) { /* AI optional, silent */ }
}

function renderResult(r) {
  const c = r.cost, alt = r.alternative;
  if (r.currency) CURRENCY = r.currency;
  $("result").innerHTML = `
    <div class="card-hard">
      <p style="margin:0 0 var(--spacing-8);font-family:var(--font-geist-mono);text-transform:uppercase;font-size:var(--text-caption);">True cost</p>
      <p class="stat-number" style="font-size:50px;margin:0;line-height:1;">${c.apr_pct}% <span style="font-size:24px;">APR</span></p>
      <p style="margin:var(--spacing-16) 0 0;font-size:var(--text-subheading);">
        You pay <strong>${money(c.total_paid)}</strong> for <strong>${money(c.principal)}</strong> of value:
        <span class="stat-inline" style="font-size:var(--text-subheading);">${c.markup_pct}%</span> more.
      </p>
      <div id="explain"></div>
      <details style="margin-top:var(--spacing-16);">
        <summary style="cursor:pointer;font-family:var(--font-geist-mono);font-size:var(--text-caption);">Show the math</summary>
        <ol style="font-family:var(--font-geist-mono);font-size:var(--text-caption);color:var(--color-graphite);">
          ${c.steps.map((s) => `<li>${s}</li>`).join("")}
        </ol>
      </details>
    </div>
    ${r.licence ? `<div class="card-hard" style="margin-top:var(--spacing-16);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">Is this lender allowed to lend?</p>
      ${licenceBadge(r.licence)}<p style="margin:var(--spacing-8) 0 0;">${r.licence.note}</p></div>` : ""}
    ${r.at_risk ? `<div class="card-hard" style="margin-top:var(--spacing-16);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">What can they take?</p>
      <p style="margin:0;">${r.at_risk.note}</p></div>` : ""}
    ${alt ? `<div class="card-hard" style="margin-top:var(--spacing-16);background:var(--color-chartreuse-highlight);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">A cheaper licensed option</p>
      <p style="margin:0 0 6px;">${alt.label}: <span class="stat-inline" style="color:var(--color-carbon-black);">${alt.cost.apr_pct}% APR</span> instead of ${c.apr_pct}%.</p>
      ${(Number(alt.cost.principal) === Number(c.principal)) ? `<p style="margin:0;font-size:var(--text-subheading);">You would pay <span class="stat-inline" style="color:var(--color-carbon-black);">${money(Number(c.total_paid) - Number(alt.cost.total_paid))}</span> less.</p>` : ""}</div>` : ""}
    <p style="margin-top:var(--spacing-16);font-size:var(--text-caption);color:var(--color-graphite);">${r.disclaimer}</p>`;
  explainInto($("explain"), c);
  $("result").appendChild(shareBar("cost", r));
  $("result").appendChild(whatNextCivic(r));
}

/* ---------- Enhancement D: always-on civic "what next" ----------
   Every flow ends with a concrete civic action, never just a number. Wires the
   money path back into the rights/accountability spine (brief constraint 7). */
function whatNextCivic(r) {
  const unlicensed = r && r.licence && r.licence.status === "unlicensed";
  const el = document.createElement("div");
  el.className = "card-hard";
  el.style.marginTop = "var(--spacing-16)";
  el.style.background = "var(--color-chartreuse-highlight)";
  el.innerHTML = `<p style="margin:0 0 8px;font-weight:600;">${t("whatnext_title")}</p>
    <div style="display:flex;gap:8px;flex-wrap:wrap;">
      <button class="btn-primary" data-go="rights" style="padding:6px 16px;">${t("wn_rights")}</button>
      ${unlicensed ? `<button class="btn-primary" data-go="report" style="padding:6px 16px;">${t("wn_report").replace("{authority}", META.authority_short)}</button>` : ""}
      <button class="btn-primary" data-go="action" style="padding:6px 16px;">${t("wn_action")}</button>
    </div>`;
  el.querySelector("[data-go='rights']").addEventListener("click", () => selectDoor("rights"));
  const act = el.querySelector("[data-go='action']");
  if (act) act.addEventListener("click", () => {
    document.getElementById("problem").scrollIntoView({ behavior: "smooth", block: "center" });
    document.getElementById("problem").focus();
  });
  const rep = el.querySelector("[data-go='report']");
  if (rep) rep.addEventListener("click", () => {
    const p = document.getElementById("problem");
    p.value = "An unlicensed lender is chasing me for repayment.";
    p.scrollIntoView({ behavior: "smooth", block: "center" });
    document.getElementById("recourse-btn").click();
  });
  return el;
}

/* ---------- before: pick a product ---------- */
async function loadProducts() {
  const sel = $("product");
  try {
    const { products } = await (await fetch("/api/products?country=" + COUNTRY)).json();
    sel.innerHTML = '<option value="">Choose a loan…</option>' +
      products.map((p) => `<option value="${p.id}">${p.label}</option>`).join("");
  } catch (_) { sel.innerHTML = '<option value="">Could not load</option>'; }
}
$("product").addEventListener("change", async (e) => {
  const id = e.target.value;
  $("confirm").innerHTML = "";
  if (!id) { $("result").innerHTML = ""; return; }
  $("result").innerHTML = `<p style="font-family:var(--font-geist-mono);">${t("computing")}</p>`;
  renderResult(await (await fetch(`/api/evaluate/${id}?country=${COUNTRY}`)).json());
});

/* ---------- before: paste an SMS -> parse -> confirm -> compute ---------- */
$("parse-btn").addEventListener("click", async () => {
  const text = $("sms").value.trim();
  if (!text) return;
  $("confirm").innerHTML = `<p style="font-family:var(--font-geist-mono);">${t("reading")}</p>`;
  const p = await (await fetch("/api/parse", {
    method: "POST", body: new URLSearchParams({ text }),
  })).json();
  if (!p.available) { $("confirm").innerHTML = `<p>${p.reason}</p>`; return; }
  const f = p.fields;
  $("confirm").innerHTML = `
    <div class="card-hard">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">Is this right? Confirm before we compute.</p>
      ${p.confidence != null ? `<p style="margin:0 0 var(--spacing-8);font-size:var(--text-caption);color:var(--color-graphite);">I'm about <strong>${Math.round(p.confidence * 100)}%</strong> sure I read this correctly. Please check the fields below.</p>` : ""}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-family:var(--font-geist-mono);font-size:var(--text-caption);">
        <label>Amount received<input id="f-principal" value="${f.principal}" style="width:100%"></label>
        <label>Repay total<input id="f-repay" value="${f.repay_total ?? ""}" style="width:100%"></label>
        <label>Term (days)<input id="f-term" value="${f.term_days}" style="width:100%"></label>
      </div>
      <button id="confirm-btn" class="btn-primary" style="margin-top:var(--spacing-8);">Compute true cost</button>
    </div>`;
  $("confirm-btn").addEventListener("click", async () => {
    const body = {
      principal: Number($("f-principal").value),
      term_days: Number($("f-term").value),
      repay_total: $("f-repay").value ? Number($("f-repay").value) : null,
    };
    $("result").innerHTML = `<p style="font-family:var(--font-geist-mono);">${t("computing")}</p>`;
    renderResult(await (await fetch("/api/cost", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })).json());
  });
});

/* ---------- during: describe a problem -> recourse ---------- */
$("recourse-btn").addEventListener("click", async () => {
  const text = $("problem").value.trim();
  if (!text) return;
  $("recourse").innerHTML = `<p style="font-family:var(--font-geist-mono);">${t("finding")}</p>`;
  try {
    const r = await (await fetch("/api/recourse", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, lang: LANG, country: COUNTRY }),
    })).json();
    renderRecourse(r);
  } catch (_) { $("recourse").innerHTML = "<p>Could not process that. Try rephrasing.</p>"; }
});

function renderRecourse(r) {
  if (!r || !r.matched) {
    $("recourse").innerHTML = `<div class="card-hard"><p style="margin:0;">${(r && r.message) || "Couldn't match that to a known situation. Try describing what the lender is doing."}</p></div>`;
    return;
  }
  const forums = (r.forums && r.forums.length) ? r.forums : (r.forum ? [{ ...r.forum, primary: true }] : []);
  const forumsHtml = forums.map((f) => `
    <div style="border:1px solid var(--color-carbon-black);border-radius:var(--radius-cards);padding:12px;margin-bottom:10px;${f.primary ? "background:var(--color-chartreuse-highlight);" : ""}">
      <p style="margin:0 0 4px;font-weight:600;">${t("go_to")}: ${f.name}${f.primary ? "" : ` <span style="font-weight:400;font-size:var(--text-caption);color:var(--color-graphite);">(also applies)</span>`}</p>
      ${f.handles ? `<p style="margin:0 0 6px;font-size:var(--text-caption);color:var(--color-graphite);">${f.handles}</p>` : ""}
      ${f.channel ? `<p style="margin:0 0 6px;font-size:var(--text-caption);"><strong>How to file:</strong> ${f.channel}</p>` : ""}
      ${(f.what_to_include && f.what_to_include.length) ? `
        <p style="margin:6px 0 4px;font-size:var(--text-caption);font-weight:600;">What to bring (tick what you have):</p>
        <div>${f.what_to_include.map((w, i) => `<label style="display:flex;gap:8px;align-items:flex-start;font-size:var(--text-caption);margin-bottom:3px;"><input type="checkbox"> <span>${w}</span></label>`).join("")}</div>` : ""}
    </div>`).join("");
  $("recourse").innerHTML = `
    <div class="card-hard">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">${r.title}</p>
      <p style="margin:0 0 var(--spacing-8);">${r.law_statement}</p>
      <p style="margin:0 0 var(--spacing-8);font-size:var(--text-caption);color:var(--color-graphite);"><em>${r.condition}</em></p>
      ${r.citation ? `<p style="margin:0;font-size:var(--text-caption);font-family:var(--font-geist-mono);color:var(--color-steel);">${t("source")}: <a href="${r.citation}" target="_blank" rel="noopener">${r.citation}</a>${r.citation_date ? ` · ${r.citation_date}` : ""}</p>` : ""}
    </div>
    <div class="card-hard" style="margin-top:var(--spacing-16);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">Where to take it${forums.length > 1 ? ` (${forums.length} bodies apply)` : ""}</p>
      ${forumsHtml}
    </div>
    ${r.complaint ? `<div class="card-hard" style="margin-top:var(--spacing-16);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">Your prepared document</p>
      <p style="font-family:var(--font-geist-mono);font-size:var(--text-caption);margin:0 0 var(--spacing-8);">Case ref: <span class="stat-inline" style="color:var(--color-carbon-black);">${r.case_ref}</span></p>
      <p style="margin:0 0 6px;font-size:var(--text-caption);color:var(--color-graphite);">Edit the details in [brackets], then share. Your changes are kept on this device only.</p>
      <textarea id="complaint-edit" rows="16" aria-label="Editable complaint document" style="width:100%;white-space:pre-wrap;font-family:var(--font-geist);font-size:var(--text-caption);background:var(--color-paper-white);border:1px solid var(--color-ash);border-radius:var(--radius-smallbuttons);padding:12px;"></textarea>
    </div>` : ""}
    <p style="margin-top:var(--spacing-16);font-size:var(--text-caption);color:var(--color-graphite);">${r.disclaimer}</p>`;
  // Fill the editable document and keep r.complaint in sync so the share bar uses edits.
  const edit = $("complaint-edit");
  if (edit) {
    edit.value = r.complaint;
    edit.addEventListener("input", () => { r.complaint = edit.value; });
  }
  $("recourse").appendChild(shareBar("recourse", r));
}

/* ---------- Enhancement A: civic doors (tab switching) ---------- */
function selectDoor(panel) {
  document.querySelectorAll(".door-btn").forEach((b) =>
    b.setAttribute("aria-selected", String(b.dataset.panel === panel)));
  ["rights", "lender", "cost"].forEach((p) => {
    const sec = document.getElementById("panel-" + p);
    if (sec) sec.hidden = p !== panel;
  });
  if (panel === "rights") loadRights();
}
document.querySelectorAll(".door-btn").forEach((b) =>
  b.addEventListener("click", () => selectDoor(b.dataset.panel)));

/* ---------- Enhancement B: know-your-rights browse (access to information) ---------- */
let RIGHTS_LOADED = false;
async function loadRights() {
  if (RIGHTS_LOADED) return;
  const box = $("rights-list");
  try {
    const data = await (await fetch("/api/rights?country=" + COUNTRY)).json();
    box.innerHTML = data.rights.map((r) => `
      <details class="card-hard" style="margin-bottom:var(--spacing-16);">
        <summary style="cursor:pointer;font-weight:600;">${r.title}</summary>
        <p style="margin:var(--spacing-8) 0 0;">${r.law_statement}</p>
        ${r.condition ? `<p style="margin:var(--spacing-8) 0 0;font-size:var(--text-caption);color:var(--color-graphite);"><em>${r.condition}</em></p>` : ""}
        ${r.forum && r.forum.name ? `<p style="margin:var(--spacing-8) 0 0;"><strong>Where to go:</strong> ${r.forum.name}${r.forum.handles ? `: ${r.forum.handles}` : ""}</p>` : ""}
        <p style="margin:var(--spacing-8) 0 0;font-family:var(--font-geist-mono);font-size:var(--text-caption);color:var(--color-steel);">
          ${t("source")}: <a href="${r.citation}" target="_blank" rel="noopener">${r.citation}</a>${r.citation_date ? ` · ${r.citation_date}` : ""}
        </p>
        <button class="btn-primary" data-act-title="${(r.title || "").replace(/"/g, "&quot;")}" style="margin-top:var(--spacing-16);padding:6px 16px;">${t("wn_action")}</button>
      </details>`).join("") +
      `<p style="font-size:var(--text-caption);color:var(--color-graphite);">${data.disclaimer}${data.last_updated ? ` Last updated: ${data.last_updated}.` : ""}</p>`;
    // Cross-link: reading a right flows straight into acting on it.
    box.querySelectorAll("[data-act-title]").forEach((b) => b.addEventListener("click", () => {
      const p = $("problem");
      p.value = b.getAttribute("data-act-title");
      p.scrollIntoView({ behavior: "smooth", block: "center" });
      $("recourse-btn").click();
    }));
    RIGHTS_LOADED = true;
  } catch (_) {
    box.innerHTML = '<p>Could not load rights. Try refreshing.</p>';
  }
}

/* ---------- Enhancement A: standalone lender check (accountability) ---------- */
$("lender-btn").addEventListener("click", async () => {
  const name = $("lender-name").value.trim();
  if (!name) return;
  const box = $("lender-result");
  box.innerHTML = '<p style="font-family:var(--font-geist-mono);">Checking CBK register…</p>';
  try {
    const r = await (await fetch("/api/check-lender?country=" + COUNTRY + "&name=" + encodeURIComponent(name))).json();
    const map = {
      licensed: ["var(--color-chartreuse-highlight)", "var(--color-carbon-black)"],
      unlicensed: ["var(--color-signal-orange)", "var(--color-paper-white)"],
      "not-applicable": ["var(--color-paper-white)", "var(--color-carbon-black)"],
      unknown: ["var(--color-paper-white)", "var(--color-carbon-black)"],
    };
    const [bg, fg] = map[r.status] || map.unknown;
    const findingsHtml = (r.findings && r.findings.length) ? `
      <div style="margin-top:var(--spacing-16);">
        <p style="margin:0 0 8px;font-weight:600;font-size:var(--text-caption);text-transform:uppercase;font-family:var(--font-geist-mono);">On record against this lender</p>
        ${r.findings.map((f) => `<div style="border-left:3px solid var(--color-signal-orange);padding-left:12px;margin-bottom:10px;">
          <p style="margin:0;font-size:var(--text-caption);"><strong>${f.body || ""}</strong>${f.date ? ` · ${f.date}` : ""}</p>
          <p style="margin:2px 0 0;font-size:var(--text-caption);">${f.summary || ""}</p>
          ${f.citation ? `<a href="${f.citation}" target="_blank" rel="noopener" style="font-size:var(--text-caption);font-family:var(--font-geist-mono);color:var(--color-steel);word-break:break-all;">${f.citation}</a>` : ""}
        </div>`).join("")}
      </div>` : "";
    box.innerHTML = `<div class="card-hard">
      <span style="display:inline-block;padding:4px 10px;border:1px solid var(--color-carbon-black);border-radius:var(--radius-tags);background:${bg};color:${fg};font-family:var(--font-geist-mono);font-size:var(--text-caption);text-transform:uppercase;font-weight:500;">${r.label}</span>
      <p style="margin:var(--spacing-8) 0 0;">${r.note}</p>
      ${findingsHtml}
      ${r.status === "unlicensed" ? `<button class="btn-primary" style="margin-top:var(--spacing-8);padding:6px 16px;" id="lender-report">${t("wn_report").replace("{authority}", META.authority_short)}</button>` : ""}
      <p style="margin:var(--spacing-8) 0 0;font-family:var(--font-geist-mono);font-size:var(--text-caption);color:var(--color-steel);">Facts only, each sourced. Verify current status on the official register.</p>
    </div>`;
    const rep = document.getElementById("lender-report");
    if (rep) rep.addEventListener("click", () => {
      const p = $("problem");
      p.value = "An unlicensed lender (" + name + ") is chasing me for repayment.";
      p.scrollIntoView({ behavior: "smooth", block: "center" });
      $("recourse-btn").click();
    });
  } catch (_) { box.innerHTML = "<p>Could not check that lender. Try again.</p>"; }
});

/* ---------- country meta: adapt regulator names + examples per country ---------- */
async function applyCountryMeta() {
  try {
    META = await (await fetch("/api/meta?country=" + COUNTRY)).json();
  } catch (_) { /* keep defaults */ }
  if (META.currency) CURRENCY = META.currency;
  // Lender panel label + placeholder adapt to the country's regulator.
  const label = document.querySelector('[data-i18n="lender_label"]');
  if (label) label.textContent = t("lender_label").replace("{authority}", META.authority_name);
  const ph = $("lender-name");
  if (ph && META.examples) ph.setAttribute("placeholder", META.examples);
}

/* ---------- country selector (scalability: swap the data pack) ---------- */
$("country").addEventListener("change", (e) => {
  COUNTRY = e.target.value;
  applyCountryMeta().then(applyLang);
  // Reload the data-driven surfaces for the new country.
  loadProducts();
  RIGHTS_LOADED = false;
  if (document.querySelector('.door-btn[data-panel="rights"]').getAttribute("aria-selected") === "true") {
    loadRights();
  }
  // Clear stale results from the previous country.
  $("result").innerHTML = ""; $("confirm").innerHTML = "";
  $("lender-result").innerHTML = ""; $("recourse").innerHTML = "";
});

/* ---------- init ---------- */
applyCountryMeta().then(applyLang);   // fetch regulator names/currency, then render UI
loadProducts();
// Open the door named in the URL hash (from the landing page CTAs), else default to rights.
(function initDoor() {
  const h = (location.hash || "").replace("#", "");
  selectDoor(["rights", "lender", "cost"].includes(h) ? h : "rights");
})();
fetch("/api/ai-status").then((r) => r.json()).then((s) => {
  if (!s.available) $("parse-btn").insertAdjacentHTML("afterend",
    '<p style="font-size:var(--text-caption);color:var(--color-graphite);">AI reading is offline. Use the picker or enter numbers.</p>');
});
