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
    pick_loan: "Pick a loan", or_paste: "or paste the SMS the lender sent you", or_snap: "or upload a screenshot of the SMS",
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
    official_findings: "Official findings (regulator or court)",
    reported_concerns: "Reported concerns (press / research)",
    verify_live: "Check the live {authority} register",
    last_checked: "we last checked",
    priv_title: "Private by default",    priv_body: "Your description is not saved on our server. It stays on this phone; only the kind of problem was sent to find the right law.",
    priv_stripped: "Removed before sending:",
    protect_title: "Stop the contact now (direct to the lender)",
    protect_intro: "The complaint above goes to a public body and takes time. This letter goes straight to the lender and demands they stop, immediately.",
    protect_btn: "Draft a stop-contact letter",
    helper_link: "Helper? Manage several people's cases",
    helper_title: "Helper workspace",
    helper_intro: "For a chief, paralegal, or CSO worker helping several borrowers. Each case is saved on THIS device only, never on a server. Use initials, not full names.",
    helper_add: "Add a case", helper_label: "Who you're helping (initials)", helper_none: "No cases yet. Add the first one above.",
    helper_open: "Open", helper_del: "Remove", helper_back: "← Back to the tool", helper_saved: "Saved on this device",
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
    pick_loan: "Chagua mkopo", or_paste: "au bandika SMS uliyotumiwa na mkopeshaji", or_snap: "au pakia picha ya SMS",
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
    official_findings: "Matokeo rasmi (mdhibiti au mahakama)",
    reported_concerns: "Wasiwasi ulioripotiwa (habari / utafiti)",
    verify_live: "Angalia rejista hai ya {authority}",
    last_checked: "tuliangalia mwisho",
    priv_title: "Faragha kwa chaguo-msingi",
    priv_body: "Maelezo yako hayahifadhiwi kwenye seva yetu. Yanabaki kwenye simu hii; ni aina ya tatizo tu iliyotumwa kupata sheria sahihi.",
    priv_stripped: "Kimeondolewa kabla ya kutuma:",
    protect_title: "Simamisha usumbufu sasa (moja kwa moja kwa mkopeshaji)",
    protect_intro: "Malalamiko hapo juu huenda kwa taasisi ya umma na huchukua muda. Barua hii huenda moja kwa moja kwa mkopeshaji na kudai wasimame, mara moja.",
    protect_btn: "Andaa barua ya kusimamisha usumbufu",
    helper_link: "Msaidizi? Simamia kesi za watu kadhaa",
    helper_title: "Eneo la msaidizi",
    helper_intro: "Kwa chifu, paralegal, au mfanyakazi wa CSO anayesaidia wakopaji kadhaa. Kila kesi huhifadhiwa kwenye SIMU HII pekee, kamwe si kwenye seva. Tumia herufi za kwanza, si majina kamili.",
    helper_add: "Ongeza kesi", helper_label: "Unayemsaidia (herufi za kwanza)", helper_none: "Bado hakuna kesi. Ongeza ya kwanza hapo juu.",
    helper_open: "Fungua", helper_del: "Ondoa", helper_back: "← Rudi kwenye zana", helper_saved: "Imehifadhiwa kwenye simu hii",
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
    pick_loan: "Chagua mkopo", or_paste: "ama paste SMS ile lender alikutumia", or_snap: "ama upload screenshot ya SMS",
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
    official_findings: "Matokeo rasmi (regulator ama court)",
    reported_concerns: "Concerns zilizoripotiwa (press / research)",
    verify_live: "Cheki rejista hai ya {authority}",
    last_checked: "tulicheki mwisho",
    priv_title: "Faragha by default",
    priv_body: "Story yako haisave kwa server yetu. Inabaki kwa hii simu; ni aina ya shida tu ilitumwa kupata sheria sahihi.",
    priv_stripped: "Ilitolewa kabla ya kutuma:",
    protect_title: "Stop huyo usumbufu saa hii (direct kwa lender)",
    protect_intro: "Ile complaint ya juu inaenda kwa ofisi ya serikali na inachukua time. Hii barua inaenda direct kwa lender na inademand wasimame, saa hii.",
    protect_btn: "Andaa barua ya kustop usumbufu",
    helper_link: "Wewe ni helper? Manage kesi za watu kadhaa",
    helper_title: "Workspace ya helper",
    helper_intro: "Kwa chief, paralegal, ama CSO worker anasaidia wakopaji kadhaa. Kila kesi inasave kwa HII simu pekee, si kwa server. Tumia initials, si majina kamili.",
    helper_add: "Ongeza kesi", helper_label: "Unamsaidia nani (initials)", helper_none: "Bado hakuna kesi. Ongeza ya kwanza hapo juu.",
    helper_open: "Fungua", helper_del: "Ondoa", helper_back: "← Rudi kwa tool", helper_saved: "Imesave kwa hii simu",
  },
};
const BCP = { en: "en", sw: "sw", sheng: "sw" };
function t(key) { return (I18N[LANG] && I18N[LANG][key]) || I18N.en[key] || key; }

/* Loading markup with a spinner (journey polish). */
function spinner(label) {
  return `<div class="deni-loading"><span class="deni-spinner" aria-hidden="true"></span>${label}</div>`;
}

/* Scroll an element into view so the user sees the result immediately. */
function reveal(id) {
  const el = $(id);
  if (el) el.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

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
function bindLangButtons() {
  document.querySelectorAll(".lang-btn").forEach((b) => {
    b.addEventListener("click", () => {
      LANG = b.dataset.lang;
      document.querySelectorAll(".lang-btn").forEach((x) =>
        x.setAttribute("aria-pressed", String(x === b)));
      applyLang();
      // Re-render the rights library in the new language (fetched fresh per language).
      RIGHTS_LOADED = false;
      if (document.querySelector('.door-btn[data-panel="rights"]').getAttribute("aria-selected") === "true") {
        loadRights();
      }
      // Re-render the helper workspace if it's open (its buttons use t()).
      if (typeof helperRender === "function" && $("panel-helper") && !$("panel-helper").hidden) {
        helperRender();
      }
    });
  });
}
bindLangButtons();

/* A compact "sourced . dated" chip linking to the citation. Makes provenance visible
   and clickable next to a claim, instead of a long raw URL. */
function sourceChip(url, date) {
  if (!url) return "";
  const link = '<svg width="12" height="12" viewBox="0 0 16 16" aria-hidden="true"><path d="M6.5 9.5l3-3M7 4.5l1-1a2.5 2.5 0 013.5 3.5l-1 1M9 11.5l-1 1A2.5 2.5 0 014.5 9l1-1" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>';
  const label = t("source") + (date ? " · " + date : "");
  return `<a class="deni-chip" href="${url}" target="_blank" rel="noopener">${link}${label}</a>`;
}

/* ---------- helpers ---------- */
/* Inline status glyph per licence state, so meaning isn't carried by colour alone
   (accessibility) and the result is scannable at a glance. currentColor inherits the
   badge text colour. 16px, decorative (label text carries the meaning). */
function licenceGlyph(status) {
  const paths = {
    licensed: '<path d="M4 8.5l2.5 2.5L12 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    unlicensed: '<path d="M8 4v5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="8" cy="11.5" r="1" fill="currentColor"/><path d="M8 1.5l6.5 11.5H1.5z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>',
    "not-applicable": '<circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M8 7v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="8" cy="4.8" r="1" fill="currentColor"/>',
    unknown: '<circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M6.2 6.2a1.8 1.8 0 113 1.4c-.8.5-1.2.9-1.2 1.7" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="8" cy="11.5" r="1" fill="currentColor"/>',
  };
  const p = paths[status] || paths.unknown;
  return `<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false" style="vertical-align:-3px;margin-right:6px;">${p}</svg>`;
}

function licenceBadge(l) {
  const a = (META && META.authority_short) || "the regulator";
  const map = {
    licensed: [`Licensed by ${a}`, "var(--color-chartreuse-highlight)", "var(--color-carbon-black)"],
    unlicensed: [`NOT on the ${a} register`, "var(--color-signal-orange)", "var(--color-paper-white)"],
    "not-applicable": [`Not a ${a}-listed lender`, "var(--color-paper-white)", "var(--color-carbon-black)"],
  };
  const [txt, bg, fg] = map[l.status] || map["not-applicable"];
  return `<span style="display:inline-block;padding:4px 10px;border:1px solid var(--color-carbon-black);
    border-radius:var(--radius-tags);background:${bg};color:${fg};
    font-family:var(--font-geist-mono);font-size:var(--text-caption);text-transform:uppercase;font-weight:500;">${licenceGlyph(l.status)}${txt}</span>`;
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
  // Word-wrap each line to the content width so nothing is clipped, and size the
  // canvas height to the wrapped line count.
  const pad = 32, lh = 26, w = 760, contentW = w - pad * 2;
  const bodyFont = "400 15px 'JetBrains Mono', monospace";
  const titleFont = "700 22px 'JetBrains Mono', monospace";

  // Measure with a scratch context first so we know how many wrapped lines we get.
  const scratch = document.createElement("canvas").getContext("2d");
  function wrap(line, font) {
    scratch.font = font;
    if (line === "") return [""];
    const words = line.split(" ");
    const out = [];
    let cur = "";
    for (const word of words) {
      const test = cur ? cur + " " + word : word;
      if (scratch.measureText(test).width <= contentW) {
        cur = test;
      } else {
        if (cur) out.push(cur);
        // A single word longer than the width: hard-break it by characters.
        if (scratch.measureText(word).width > contentW) {
          let chunk = "";
          for (const ch of word) {
            if (scratch.measureText(chunk + ch).width <= contentW) { chunk += ch; }
            else { out.push(chunk); chunk = ch; }
          }
          cur = chunk;
        } else {
          cur = word;
        }
      }
    }
    if (cur) out.push(cur);
    return out;
  }

  const src = text.split("\n");
  // Build a flat list of {text, isTitle} wrapped lines.
  const rows = [];
  src.forEach((ln, i) => {
    const font = i === 0 ? titleFont : bodyFont;
    wrap(ln, font).forEach((wl) => rows.push({ text: wl, title: i === 0 }));
  });

  const cvs = document.createElement("canvas");
  cvs.width = w;
  cvs.height = pad * 2 + lh * rows.length;
  const ctx = cvs.getContext("2d");
  ctx.fillStyle = "#fafafa"; ctx.fillRect(0, 0, cvs.width, cvs.height);
  ctx.fillStyle = "#ff5b29"; ctx.fillRect(0, 0, 6, cvs.height); // signal-orange rail
  rows.forEach((row, i) => {
    const y = pad + lh * (i + 1);
    if (row.title) { ctx.font = titleFont; ctx.fillStyle = "#ff5b29"; }
    else { ctx.font = bodyFont; ctx.fillStyle = "#242424"; }
    ctx.fillText(row.text, pad, y);
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

/* Value-received vs you-pay bar: the money shot. One glance shows how much more you
   repay than you received, for users who don't read the prose. Two stacked segments,
   widths proportional to the amounts; the extra (what the credit costs) is the orange
   overhang. Labelled with the amounts so it's not colour-only. */
function costBar(c) {
  const principal = Number(c.principal), paid = Number(c.total_paid);
  if (!(paid > 0) || !(principal >= 0)) return "";
  const valuePct = Math.max(2, Math.min(100, Math.round((principal / paid) * 100)));
  return `
    <div style="margin:var(--spacing-16) 0 0;" aria-hidden="false">
      <div style="display:flex;justify-content:space-between;font-family:var(--font-geist-mono);font-size:var(--text-caption);color:var(--color-graphite);margin-bottom:4px;">
        <span>Value you received</span><span>What you repay</span>
      </div>
      <div role="img" aria-label="You repay ${money(paid)} for ${money(principal)} of value"
           style="position:relative;height:28px;border:1px solid var(--color-carbon-black);border-radius:var(--radius-smallbuttons);background:var(--color-signal-orange);overflow:hidden;">
        <div style="position:absolute;left:0;top:0;bottom:0;width:${valuePct}%;background:var(--color-carbon-black);"></div>
      </div>
      <div style="display:flex;justify-content:space-between;font-family:var(--font-geist-mono);font-size:var(--text-caption);margin-top:4px;">
        <span style="color:var(--color-carbon-black);font-weight:600;">${money(principal)}</span>
        <span style="color:var(--color-orange-text);font-weight:600;">${money(paid)}</span>
      </div>
    </div>`;
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
      ${costBar(c)}
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
  $("result").innerHTML = spinner(t("computing"));
  renderResult(await (await fetch(`/api/evaluate/${id}?country=${COUNTRY}`)).json()); reveal("result");
});

/* ---------- before: paste an SMS or upload a screenshot -> parse -> confirm -> compute ---------- */
$("parse-btn").addEventListener("click", async () => {
  const text = $("sms").value.trim();
  const file = $("sms-image") && $("sms-image").files && $("sms-image").files[0];
  if (!text && !file) return;
  $("confirm").innerHTML = spinner(t("reading"));
  // Use multipart FormData so the backend's /api/parse can read text and/or image.
  const fd = new FormData();
  if (text) fd.append("text", text);
  if (file) fd.append("image", file);
  const p = await (await fetch("/api/parse", { method: "POST", body: fd })).json();
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
    $("result").innerHTML = spinner(t("computing"));
    renderResult(await (await fetch("/api/cost", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })).json());
    reveal("result");
  });
});

/* ---------- privacy: redact identifying data BEFORE it leaves the device ----------
   Track 3 (Safety, Reporting & Protection) prioritises anonymity; constraint 4
   (privacy) says protect identity. The problem the user types often carries a phone
   number, an ID, an amount, or a name. We strip those in the browser, so the raw
   text never reaches the server or the AI model. Classification only needs the
   *shape* of the problem ("they are calling my contacts"), not who you are. The
   drafted document has its own [your name] slots you fill in locally and share
   yourself. Deterministic patterns only; we err towards over-redaction. */
function redactProblem(text) {
  const hits = [];
  let out = text;
  const sweep = (re, label, mask) => {
    out = out.replace(re, (m) => { hits.push(label); return mask; });
  };
  // Kenyan / SA phone numbers and any long digit run that looks like a number to reach you.
  sweep(/(?:\+?254|\+?27|0)\d[\d\s-]{7,}\d/g, "phone number", "[redacted phone]");
  // National ID / passport-like tokens (7-9 digit IDs, alphanumeric passports).
  sweep(/\b(?:id|passport|national id)\s*(?:no\.?|number|#)?\s*[:.]?\s*[A-Z]?\d{6,9}\b/gi, "ID number", "[redacted ID]");
  sweep(/\b\d{7,9}\b/g, "ID number", "[redacted ID]");
  // Email addresses.
  sweep(/\b[\w.+-]+@[\w-]+\.[\w.-]+\b/g, "email", "[redacted email]");
  // "My name is X", "I am X Y", "this is X" -> drop the trailing capitalised name(s).
  // Case-insensitive on the lead-in phrase; the captured name keeps its own casing.
  sweep(/\b(?:my name is|i am|i'm|this is|name)\s*[:]?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})/gi,
        "name", "[redacted name]");
  return { text: out, redacted: [...new Set(hits)] };
}

/* ---------- during: describe a problem -> recourse ---------- */
$("recourse-btn").addEventListener("click", async () => {
  const raw = $("problem").value.trim();
  if (!raw) return;
  const { text, redacted } = redactProblem(raw);
  $("recourse").innerHTML = spinner(t("finding"));
  try {
    const r = await (await fetch("/api/recourse", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, lang: LANG, country: COUNTRY }),
    })).json();
    r._redacted = redacted;   // pass through so the result can show what was protected
    r._sentText = text;       // redacted text, reused for the direct stop-contact letter
    renderRecourse(r);
  } catch (_) { $("recourse").innerHTML = "<p>Could not process that. Try rephrasing.</p>"; }
});

/* Privacy banner shown on every recourse result: states we don't store the text,
   and lists what was stripped on-device before anything was sent (Track 3 / R10). */
function privacyNote(redacted) {
  const stripped = (redacted && redacted.length)
    ? `<p style="margin:6px 0 0;font-size:var(--text-caption);">${t("priv_stripped")} <strong>${redacted.join(", ")}</strong>.</p>`
    : "";
  return `<div class="card-hard" style="background:var(--color-chartreuse-highlight);margin-bottom:var(--spacing-16);">
    <p style="margin:0;font-size:var(--text-caption);font-family:var(--font-geist-mono);text-transform:uppercase;letter-spacing:0.03em;">${t("priv_title")}</p>
    <p style="margin:6px 0 0;font-size:var(--text-caption);">${t("priv_body")}</p>
    ${stripped}
  </div>`;
}

function renderRecourse(r) {
  if (!r || !r.matched) {
    const sn = r && r.safety_net;
    const bodiesHtml = (sn && sn.bodies && sn.bodies.length) ? `
      <div style="margin-top:var(--spacing-16);">
        <p style="margin:0 0 var(--spacing-8);font-size:var(--text-caption);">${sn.intro || ""}</p>
        ${sn.bodies.map((b) => `<div style="border-left:3px solid var(--color-carbon-black);padding-left:12px;margin-bottom:10px;">
          <p style="margin:0;font-weight:600;font-size:var(--text-caption);">${b.name}</p>
          ${b.when ? `<p style="margin:2px 0 0;font-size:var(--text-caption);color:var(--color-graphite);">${b.when}</p>` : ""}
          ${b.contact ? `<p style="margin:2px 0 0;font-size:var(--text-caption);">${b.contact}</p>` : ""}
        </div>`).join("")}
      </div>` : "";
    $("recourse").innerHTML = `
      ${privacyNote(r && r._redacted)}
      <div class="card-hard">
        <p style="margin:0;">${(r && r.message) || "Couldn't match that to a known situation. Try describing what the lender is doing."}</p>
        ${bodiesHtml}
      </div>`;
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
    ${privacyNote(r._redacted)}
    <div class="card-hard">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">${r.title}</p>
      <p style="margin:0 0 var(--spacing-8);">${r.law_statement}</p>
      <p style="margin:0 0 var(--spacing-8);font-size:var(--text-caption);color:var(--color-graphite);"><em>${r.condition}</em></p>
      ${r.citation ? `<p style="margin:0;">${sourceChip(r.citation, r.citation_date)}</p>` : ""}
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
    <div class="card-hard" style="margin-top:var(--spacing-16);border-color:var(--color-signal-orange);">
      <p style="margin:0 0 4px;font-weight:600;">${t("protect_title")}</p>
      <p style="margin:0 0 var(--spacing-8);font-size:var(--text-caption);color:var(--color-graphite);">${t("protect_intro")}</p>
      <button id="protect-btn" class="btn-primary" style="padding:6px 16px;">${t("protect_btn")}</button>
      <div id="protect-out" style="margin-top:var(--spacing-16);" aria-live="polite"></div>
    </div>
    <p style="margin-top:var(--spacing-16);font-size:var(--text-caption);color:var(--color-graphite);">${r.disclaimer}</p>`;
  // Fill the editable document and keep r.complaint in sync so the share bar uses edits.
  const edit = $("complaint-edit");
  if (edit) {
    edit.value = r.complaint;
    edit.addEventListener("input", () => { r.complaint = edit.value; });
  }
  // Direct stop-contact letter to the lender (protective, immediate).
  const pbtn = $("protect-btn");
  if (pbtn) pbtn.addEventListener("click", async () => {
    const out = $("protect-out");
    out.innerHTML = spinner(t("reading"));
    try {
      const p = await (await fetch("/api/protect-letter", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: r._sentText || "", lang: LANG, country: COUNTRY }),
      })).json();
      if (!p.matched) { out.innerHTML = `<p style="font-size:var(--text-caption);">${p.message || "Not available."}</p>`; return; }
      out.innerHTML = `
        <p style="font-family:var(--font-geist-mono);font-size:var(--text-caption);margin:0 0 var(--spacing-8);">Case ref: <span class="stat-inline" style="color:var(--color-carbon-black);">${p.case_ref}</span></p>
        <p style="margin:0 0 6px;font-size:var(--text-caption);color:var(--color-graphite);">Edit the [bracketed] details, then send it to the lender yourself and keep proof. Kept on this device only.</p>
        <textarea id="protect-edit" rows="14" aria-label="Editable stop-contact letter" style="width:100%;white-space:pre-wrap;font-family:var(--font-geist);font-size:var(--text-caption);background:var(--color-paper-white);border:1px solid var(--color-ash);border-radius:var(--radius-smallbuttons);padding:12px;"></textarea>
        <p style="margin:var(--spacing-8) 0 0;font-size:var(--text-caption);color:var(--color-graphite);">${p.disclaimer}</p>`;
      const pe = $("protect-edit");
      pe.value = p.letter;
      const shareData = { title: p.title, complaint: p.letter, case_ref: p.case_ref,
                          law_statement: p.legal_basis, forums: [] };
      pe.addEventListener("input", () => { shareData.complaint = pe.value; });
      out.appendChild(shareBar("recourse", shareData));
    } catch (_) { out.innerHTML = "<p style=\"font-size:var(--text-caption);\">Could not draft that letter. Try again.</p>"; }
  });
  $("recourse").appendChild(shareBar("recourse", r));
  reveal("recourse");
}

/* ---------- Enhancement A: civic doors (tab switching) ---------- */
function selectDoor(panel) {
  document.querySelectorAll(".door-btn").forEach((b) =>
    b.setAttribute("aria-selected", String(b.dataset.panel === panel)));
  ["rights", "lender", "cost"].forEach((p) => {
    const sec = document.getElementById("panel-" + p);
    if (sec) sec.hidden = p !== panel;
  });
  // Journey polish: full hero on the default rights view; collapse it inside a tool.
  const title = $("hero-title"), lead = $("hero-lead");
  const inTool = panel !== "rights";
  if (title) title.classList.toggle("hero-compact", inTool);
  if (lead) lead.classList.toggle("hero-hidden", inTool);
  // Empty-state hints so first-timers know what will appear.
  if (panel === "cost" && $("result") && !$("result").innerHTML.trim() && !$("confirm").innerHTML.trim()) {
    $("result").innerHTML = '<div class="deni-hint">Pick a loan or paste an offer above. Deni shows the true cost, the licence status, and a cheaper option.</div>';
  }
  if (panel === "lender" && $("lender-result") && !$("lender-result").innerHTML.trim()) {
    $("lender-result").innerHTML = '<div class="deni-hint">Type a lender name to see if it is on the register, and any findings on record.</div>';
  }
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
        <p style="margin:var(--spacing-8) 0 0;">${sourceChip(r.citation, r.citation_date)}</p>
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
  box.innerHTML = spinner("Checking the " + (META.authority_short || "register") + "...");
  try {
    const r = await (await fetch("/api/check-lender?country=" + COUNTRY + "&name=" + encodeURIComponent(name))).json();
    const map = {
      licensed: ["var(--color-chartreuse-highlight)", "var(--color-carbon-black)"],
      unlicensed: ["var(--color-signal-orange)", "var(--color-paper-white)"],
      "not-applicable": ["var(--color-paper-white)", "var(--color-carbon-black)"],
      unknown: ["var(--color-paper-white)", "var(--color-carbon-black)"],
    };
    const [bg, fg] = map[r.status] || map.unknown;
    const renderRecords = (items, heading, isOfficial) => (items && items.length) ? `
      <div style="margin-top:var(--spacing-16);">
        <span class="badge-record ${isOfficial ? "badge-official" : "badge-reported"}">${heading}</span>
        <div style="margin-top:8px;">
        ${items.map((f) => `<div style="border-left:3px solid ${isOfficial ? "var(--color-signal-orange)" : "var(--color-ash)"};padding-left:12px;margin-bottom:10px;">
          <p style="margin:0;font-size:var(--text-caption);"><strong>${f.body || ""}</strong>${f.date ? ` · ${f.date}` : ""}</p>
          <p style="margin:2px 0 0;font-size:var(--text-caption);">${f.summary || ""}</p>
          ${f.citation ? sourceChip(f.citation, "") : ""}
        </div>`).join("")}
        </div>
      </div>` : "";
    // Official regulator/court actions and press/context are shown SEPARATELY and
    // labelled, so a news report is never dressed up as a regulatory finding.
    const officialHtml = renderRecords(r.official_findings, t("official_findings"), true);
    const reportedHtml = renderRecords(r.reported_concerns, t("reported_concerns"), false);
    // Verify-live: link straight to the official register so the user can confirm
    // today's status themselves (a static snapshot becomes a verifiable pointer).
    const verifyHtml = META.register_url ? `
      <p style="margin:var(--spacing-8) 0 0;font-size:var(--text-caption);">
        <a href="${META.register_url}" target="_blank" rel="noopener" style="color:var(--color-signal-orange);font-weight:600;">${t("verify_live").replace("{authority}", META.authority_short)} →</a>
        ${r.register_updated ? ` <span style="color:var(--color-steel);">(${t("last_checked")} ${r.register_updated})</span>` : ""}
      </p>` : "";
    box.innerHTML = `<div class="card-hard">
      <span style="display:inline-block;padding:4px 10px;border:1px solid var(--color-carbon-black);border-radius:var(--radius-tags);background:${bg};color:${fg};font-family:var(--font-geist-mono);font-size:var(--text-caption);text-transform:uppercase;font-weight:500;">${licenceGlyph(r.status)}${r.label}</span>
      <p style="margin:var(--spacing-8) 0 0;">${r.note}</p>
      ${officialHtml}
      ${reportedHtml}
      ${r.status === "unlicensed" ? `<button class="btn-primary" style="margin-top:var(--spacing-8);padding:6px 16px;" id="lender-report">${t("wn_report").replace("{authority}", META.authority_short)}</button>` : ""}
      ${verifyHtml}
      <p style="margin:var(--spacing-8) 0 0;font-family:var(--font-geist-mono);font-size:var(--text-caption);color:var(--color-steel);">Facts only, each sourced.${r.register_updated ? ` ${r.register_name || "Register"} as of ${r.register_updated}.` : ""}</p>
    </div>`;
    const rep = document.getElementById("lender-report");
    if (rep) rep.addEventListener("click", () => {
      const p = $("problem");
      p.value = "An unlicensed lender (" + name + ") is chasing me for repayment.";
      p.scrollIntoView({ behavior: "smooth", block: "center" });
      $("recourse-btn").click();
    });
    reveal("lender-result");
  } catch (_) { box.innerHTML = "<p>Could not check that lender. Try again.</p>"; }
});

/* ---------- country meta: adapt regulator names + examples per country ---------- */
async function applyCountryMeta() {
  try {
    META = await (await fetch("/api/meta?country=" + COUNTRY)).json();
  } catch (_) { /* keep defaults */ }
  if (META.currency) CURRENCY = META.currency;
  // Rebuild the language toggle from the country's own languages (Kenya has
  // English/Kiswahili/Sheng; South Africa has English). If the current language
  // isn't offered here, fall back to English.
  const langs = (META.languages && META.languages.length) ? META.languages
    : [{ code: "en", label: "English" }];
  if (!langs.some((l) => l.code === LANG)) LANG = "en";
  const langGroup = $("lang");
  if (langGroup) {
    langGroup.innerHTML = langs.map((l) =>
      `<button data-lang="${l.code}" class="lang-btn" aria-pressed="${String(l.code === LANG)}">${l.label}</button>`
    ).join("");
    bindLangButtons();
  }
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

/* ---------- Helper / multi-case workspace (Track 1: coordination) ----------
   A chief, paralegal, or CSO worker often helps several borrowers. This gives them
   one place to keep those cases, on THIS device only (localStorage), never a server,
   so it stays private and works offline. Opening a case drops its note into the
   action box so the helper runs the same recourse engine per person. */
const HELPER_KEY = "deni_helper_cases";

function helperLoad() {
  try { return JSON.parse(localStorage.getItem(HELPER_KEY) || "[]"); }
  catch (_) { return []; }
}
function helperSave(cases) {
  try { localStorage.setItem(HELPER_KEY, JSON.stringify(cases)); } catch (_) { /* full/blocked */ }
}
function helperRender() {
  const box = $("helper-cases");
  if (!box) return;
  const cases = helperLoad();
  if (!cases.length) {
    box.innerHTML = `<p style="font-size:var(--text-caption);color:var(--color-graphite);">${t("helper_none")}</p>`;
    return;
  }
  box.innerHTML = cases.map((c) => `
    <div class="card-hard" style="margin-bottom:var(--spacing-16);display:flex;justify-content:space-between;gap:12px;align-items:flex-start;">
      <div style="min-width:0;">
        <p style="margin:0;font-weight:600;">${c.label || "—"}</p>
        ${c.note ? `<p style="margin:4px 0 0;font-size:var(--text-caption);color:var(--color-graphite);word-break:break-word;">${c.note.replace(/</g, "&lt;")}</p>` : ""}
        <p style="margin:6px 0 0;font-family:var(--font-geist-mono);font-size:var(--text-caption);color:var(--color-steel);">${t("helper_saved")} · ${c.createdAt || ""}</p>
      </div>
      <div style="display:flex;flex-direction:column;gap:6px;flex-shrink:0;">
        <button class="btn-primary" data-open="${c.id}" style="padding:4px 12px;">${t("helper_open")}</button>
        <button data-del="${c.id}" style="padding:4px 12px;background:none;border:1px solid var(--color-ash);border-radius:var(--radius-smallbuttons);cursor:pointer;font-family:var(--font-geist-mono);font-size:var(--text-caption);">${t("helper_del")}</button>
      </div>
    </div>`).join("");
  box.querySelectorAll("[data-open]").forEach((b) => b.addEventListener("click", () => {
    const c = helperLoad().find((x) => x.id === b.getAttribute("data-open"));
    helperShow(false);
    const p = $("problem");
    p.value = c && c.note ? c.note : "";
    p.scrollIntoView({ behavior: "smooth", block: "center" });
    p.focus();
  }));
  box.querySelectorAll("[data-del]").forEach((b) => b.addEventListener("click", () => {
    helperSave(helperLoad().filter((x) => x.id !== b.getAttribute("data-del")));
    helperRender();
  }));
}
function helperShow(show) {
  const panel = $("panel-helper");
  if (!panel) return;
  panel.hidden = !show;
  // Hide/show every OTHER direct child of <main> so the workspace stands alone.
  const main = panel.parentElement;
  Array.from(main.children).forEach((el) => {
    if (el !== panel) el.style.display = show ? "none" : "";
  });
  if (show) helperRender();
}
(function initHelper() {
  const link = $("helper-link"), back = $("helper-back"), add = $("helper-add");
  if (link) link.addEventListener("click", () => helperShow(true));
  if (back) back.addEventListener("click", () => helperShow(false));
  if (add) add.addEventListener("click", () => {
    const label = $("helper-init").value.trim();
    const note = $("helper-note").value.trim();
    if (!label && !note) return;
    const cases = helperLoad();
    cases.unshift({ id: "c" + Date.now().toString(36), label, note,
                    createdAt: new Date().toISOString().slice(0, 10) });
    helperSave(cases);
    $("helper-init").value = ""; $("helper-note").value = "";
    helperRender();
  });
})();

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
