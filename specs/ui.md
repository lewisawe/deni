# Deni: UI/UX spec

> Spec addendum. Frozen 14 Sep 2026. Design system: "Timescale" (../../DESIGN.md).
> Decision: SPLIT by surface. Realizes R9 (accessibility) alongside the Timescale look.

## Design system source

Timescale (see repo-root `DESIGN.md`): warm off-white `#fafafa`, Signal Orange
`#ff5b29` (emphasis only), Chartreuse `#f5ff80` (highlight/spotlight only), Carbon
Black structure, hard offset shadow `5px 5px 0px #000`, Geist (voice) + Geist Mono
(numbers/data). Its CSS custom properties + Tailwind `@theme` are drop-in.

## The split (two surfaces, one token set)

### Surface A: Pitch / landing / result cards (JUDGE-FACING) → FULL Timescale
Where judges look. Use the system at full strength:
- Hero + landing: full blueprint aesthetic, grid-pattern background, hard-shadow cards.
- **The cost result card is the money moment:** the true APR / total / markup rendered
  in **Geist Mono, large, Signal Orange**, the "switched on" number against the
  monochrome page. This is the single most important visual in the product; it uses
  the Timescale stat-banner treatment (`5px 5px 0px #000` shadow, mono numerals).
- Licence-status + "not on CBK list" callouts use the Chartreuse spotlight wash.
- Rationale: engineered, number-forward, trust-signalling, perfect for the shock
  figure and the "AI Coding Usage / Presentation" judging.

### Surface B: Borrower chat flow (END-USER-FACING) → Timescale TOKENS, simplified layout
Where a stressed, low-data, varied-literacy borrower actually is. Keep the *language*
(colors, fonts, orange-for-the-number rule) but relax the marketing density:
- WhatsApp-shaped conversational layout, not a landing-page grid.
- Larger tap targets, larger base text, one action per screen.
- Keep the Geist Mono + Signal Orange treatment for the key number (consistency +
  it IS the point), but everything else simple and calm.

### Surface C: USSD → plain text, no styling
Africa's Talking `CON`/`END` text menus. Inherits none of the visual system by
nature. The design system does not apply; the *content hierarchy* (number first,
next step last) still does.

## Accessibility adjustments to the base system (R9): required overrides

Timescale is a light desktop-web marketing aesthetic; these overrides make it serve
low-literacy, feature-phone, stressed users without breaking the look:

1. **Body-text contrast:** use Carbon Black `#000` (or no lighter than `#242424`
   Graphite) for body copy in Surface B, NOT Steel `#6c6c6c`. Steel `#6c6c6c` on
   `#fafafa` is ~4.0:1, below WCAG AA 4.5:1 for body. Reserve Steel for large text /
   captions only. Verify every text/background pair ≥ 4.5:1 (≥ 3:1 for large).
2. **Type scale in Surface B:** minimum 16px body, prefer 18px; do not use the 52/80px
   display or the tightest -0.03em tracking in the app flow (marketing sizes only).
3. **Number-first, icon-first cards (R9):** the shock figure is graspable without
   reading prose; an icon/plain-language one-liner supports it.
4. **Audio:** every explanation has an audio-play control (Nova 2 Sonic or TTS).
5. **Semantics:** proper headings, labelled controls, focus-visible states,
   screen-reader order matches visual order. Timescale's "no focus glow" note is
   overridden, a visible focus indicator is required for a11y.
6. **Language:** EN/SW/Sheng selector prominent; the number treatment is
   language-independent so the figure reads the same in any language.

## Concrete component mapping

| Deni element | Timescale component | Surface |
|---|---|---|
| Landing hero | Hero Section | A |
| **Cost result (APR/markup)** | **Stats Banner** (mono, orange, hard shadow) | A |
| Licence flag / "not on CBK list" | Chartreuse callout / Pill Tag | A + B |
| What's-at-risk | Feature Card (outlined icon) | A |
| Chat bubbles | simplified cards, tokens only | B |
| Offer input / paste / upload | Text Input | A + B |
| Recourse result + forum | Feature Card + Pill Tag | A/B |
| Complaint doc preview | Card, mono for reference/case-id | A/B |
| Language selector | Pill Tag group | A + B |

## Do / Don't (inherited + Deni-specific)

- DO render every key number in Geist Mono Signal Orange, it is the product's voice.
- DO keep the hard offset shadow on judge-facing cards; it is the signature.
- DON'T use Steel `#6c6c6c` for body text in the borrower flow (contrast).
- DON'T bring 80px display type or the densest tracking into the chat flow.
- DON'T add a third chromatic color; orange = number/emphasis, chartreuse = licence
  spotlight, black = structure.
- DON'T style the USSD flow, it's plain text; carry only the content hierarchy.

## Build integration

- T1: drop Timescale CSS custom properties into the frontend base; load Geist +
  Geist Mono (fallbacks Inter / JetBrains Mono per DESIGN.md).
- T4: build the cost result card as the Stats Banner treatment (the money moment).
- T4/T6: build Surface B chat with tokens + the a11y overrides above.
- T10: verify contrast, audio, focus, screen-reader order (the a11y pass).
