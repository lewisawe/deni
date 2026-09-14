// Deni UI: before-flow (pick or paste), multilingual explain, during-flow recourse.
const $ = (id) => document.getElementById(id);
const fmt = (n) => Number(n).toLocaleString("en-KE", { maximumFractionDigits: 0 });
let LANG = "en";

/* ---------- language toggle ---------- */
document.querySelectorAll(".lang-btn").forEach((b) => {
  b.addEventListener("click", () => {
    LANG = b.dataset.lang;
    document.querySelectorAll(".lang-btn").forEach((x) =>
      x.setAttribute("aria-pressed", String(x === b)));
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

async function explainInto(el, cost) {
  try {
    const e = await (await fetch("/api/explain", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cost, lang: LANG }),
    })).json();
    if (e.available && e.text) {
      el.innerHTML = `<p style="margin:var(--spacing-8) 0 0;font-style:italic;">${e.text}</p>`;
    }
  } catch (_) { /* AI optional — silent */ }
}

function renderResult(r) {
  const c = r.cost, alt = r.alternative;
  $("result").innerHTML = `
    <div class="card-hard">
      <p style="margin:0 0 var(--spacing-8);font-family:var(--font-geist-mono);text-transform:uppercase;font-size:var(--text-caption);">True cost</p>
      <p class="stat-number" style="font-size:50px;margin:0;line-height:1;">${c.apr_pct}% <span style="font-size:24px;">APR</span></p>
      <p style="margin:var(--spacing-16) 0 0;font-size:var(--text-subheading);">
        You pay <strong>KES ${fmt(c.total_paid)}</strong> for <strong>KES ${fmt(c.principal)}</strong> of value —
        <span class="stat-number" style="font-size:var(--text-subheading);">${c.markup_pct}%</span> more.
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
      <p style="margin:0;">${alt.label} — <span class="stat-number" style="color:var(--color-carbon-black);">${alt.cost.apr_pct}% APR</span> instead of ${c.apr_pct}%.</p></div>` : ""}
    <p style="margin-top:var(--spacing-16);font-size:var(--text-caption);color:var(--color-graphite);">${r.disclaimer}</p>`;
  explainInto($("explain"), c);
}

/* ---------- before: pick a product ---------- */
async function loadProducts() {
  const sel = $("product");
  try {
    const { products } = await (await fetch("/api/products")).json();
    sel.innerHTML = '<option value="">Choose a loan…</option>' +
      products.map((p) => `<option value="${p.id}">${p.label}</option>`).join("");
  } catch (_) { sel.innerHTML = '<option value="">Could not load</option>'; }
}
$("product").addEventListener("change", async (e) => {
  const id = e.target.value;
  $("confirm").innerHTML = "";
  if (!id) { $("result").innerHTML = ""; return; }
  $("result").innerHTML = '<p style="font-family:var(--font-geist-mono);">Computing…</p>';
  renderResult(await (await fetch(`/api/evaluate/${id}`)).json());
});

/* ---------- before: paste an SMS -> parse -> confirm -> compute ---------- */
$("parse-btn").addEventListener("click", async () => {
  const text = $("sms").value.trim();
  if (!text) return;
  $("confirm").innerHTML = '<p style="font-family:var(--font-geist-mono);">Reading…</p>';
  const p = await (await fetch("/api/parse", {
    method: "POST", body: new URLSearchParams({ text }),
  })).json();
  if (!p.available) { $("confirm").innerHTML = `<p>${p.reason}</p>`; return; }
  const f = p.fields;
  $("confirm").innerHTML = `
    <div class="card-hard">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">Is this right? Confirm before we compute.</p>
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
    $("result").innerHTML = '<p style="font-family:var(--font-geist-mono);">Computing…</p>';
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
  $("recourse").innerHTML = '<p style="font-family:var(--font-geist-mono);">Finding your rights…</p>';
  try {
    const r = await (await fetch("/api/recourse", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, lang: LANG }),
    })).json();
    renderRecourse(r);
  } catch (_) { $("recourse").innerHTML = "<p>Could not process that. Try rephrasing.</p>"; }
});

function renderRecourse(r) {
  if (!r || !r.matched) {
    $("recourse").innerHTML = `<div class="card-hard"><p style="margin:0;">${(r && r.message) || "Couldn't match that to a known situation. Try describing what the lender is doing."}</p></div>`;
    return;
  }
  $("recourse").innerHTML = `
    <div class="card-hard">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">${r.title}</p>
      <p style="margin:0 0 var(--spacing-8);">${r.law_statement}</p>
      <p style="margin:0 0 var(--spacing-8);font-size:var(--text-caption);color:var(--color-graphite);"><em>${r.condition}</em></p>
      <span style="display:inline-block;padding:4px 10px;border:1px solid var(--color-carbon-black);border-radius:var(--radius-tags);background:var(--color-chartreuse-highlight);font-family:var(--font-geist-mono);font-size:var(--text-caption);text-transform:uppercase;">Go to: ${r.forum.name}</span>
    </div>
    ${r.complaint ? `<div class="card-hard" style="margin-top:var(--spacing-16);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">Your prepared complaint</p>
      <p style="font-family:var(--font-geist-mono);font-size:var(--text-caption);margin:0 0 var(--spacing-8);">Case ref: <span class="stat-number" style="color:var(--color-carbon-black);">${r.case_ref}</span></p>
      <pre style="white-space:pre-wrap;font-family:var(--font-geist);font-size:var(--text-caption);background:var(--color-paper-white);border:1px solid var(--color-ash);border-radius:var(--radius-smallbuttons);padding:12px;">${r.complaint}</pre>
    </div>` : ""}
    <p style="margin-top:var(--spacing-16);font-size:var(--text-caption);color:var(--color-graphite);">${r.disclaimer}</p>`;
}

loadProducts();
fetch("/api/ai-status").then((r) => r.json()).then((s) => {
  if (!s.available) $("parse-btn").insertAdjacentHTML("afterend",
    '<p style="font-size:var(--text-caption);color:var(--color-graphite);">AI reading is offline — use the picker or enter numbers.</p>');
});
