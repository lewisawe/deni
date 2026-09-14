// Deni before-flow UI. Renders the money moment (Timescale stat treatment) + licence + risk + alternative.
const $ = (id) => document.getElementById(id);
const fmt = (n) => Number(n).toLocaleString("en-KE", { maximumFractionDigits: 0 });

async function loadProducts() {
  const sel = $("product");
  try {
    const { products } = await (await fetch("/api/products")).json();
    sel.innerHTML = '<option value="">Choose a loan…</option>' +
      products.map((p) => `<option value="${p.id}">${p.label}</option>`).join("");
  } catch (e) {
    sel.innerHTML = '<option value="">Could not load</option>';
  }
}

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

function render(r) {
  const c = r.cost;
  const alt = r.alternative;
  $("result").innerHTML = `
    <div class="card-hard">
      <p style="margin:0 0 var(--spacing-8);font-family:var(--font-geist-mono);text-transform:uppercase;font-size:var(--text-caption);">True cost</p>
      <p class="stat-number" style="font-size:50px;margin:0;line-height:1;">${c.apr_pct}% <span style="font-size:24px;">APR</span></p>
      <p style="margin:var(--spacing-16) 0 0;font-size:var(--text-subheading);">
        You pay <strong>KES ${fmt(c.total_paid)}</strong> for <strong>KES ${fmt(c.principal)}</strong> of value —
        that's <span class="stat-number" style="font-size:var(--text-subheading);">${c.markup_pct}%</span> more.
      </p>
      <details style="margin-top:var(--spacing-16);">
        <summary style="cursor:pointer;font-family:var(--font-geist-mono);font-size:var(--text-caption);">Show the math</summary>
        <ol style="font-family:var(--font-geist-mono);font-size:var(--text-caption);color:var(--color-graphite);">
          ${c.steps.map((s) => `<li>${s}</li>`).join("")}
        </ol>
      </details>
    </div>

    <div class="card-hard" style="margin-top:var(--spacing-16);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">Is this lender allowed to lend?</p>
      ${licenceBadge(r.licence)}
      <p style="margin:var(--spacing-8) 0 0;">${r.licence.note}</p>
    </div>

    <div class="card-hard" style="margin-top:var(--spacing-16);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">What can they take?</p>
      <p style="margin:0;">${r.at_risk.note}</p>
    </div>

    ${alt ? `
    <div class="card-hard" style="margin-top:var(--spacing-16);background:var(--color-chartreuse-highlight);">
      <p style="margin:0 0 var(--spacing-8);font-weight:600;">A cheaper licensed option</p>
      <p style="margin:0;">${alt.label} — <span class="stat-number" style="color:var(--color-carbon-black);">${alt.cost.apr_pct}% APR</span>
      instead of ${c.apr_pct}%.</p>
    </div>` : ""}

    <p style="margin-top:var(--spacing-16);font-size:var(--text-caption);color:var(--color-graphite);">
      ${r.disclaimer} ${r.sources && r.sources.length ? `Sources on file. Data: ${r.data_date}.` : ""}
    </p>
  `;
}

$("product").addEventListener("change", async (e) => {
  const id = e.target.value;
  if (!id) { $("result").innerHTML = ""; return; }
  $("result").innerHTML = '<p style="font-family:var(--font-geist-mono);">Computing…</p>';
  try {
    render(await (await fetch(`/api/evaluate/${id}`)).json());
  } catch (err) {
    $("result").innerHTML = '<p>Could not evaluate that loan.</p>';
  }
});

loadProducts();
