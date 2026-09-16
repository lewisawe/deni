# Deni — Suggestions & Roadmap

Ideas surfaced during the build, kept here so they don't get lost. Grouped by the
brief's own criteria. Not all are for the sprint; the sprint-critical ones are marked.

## In progress

- **Real UI translation (en/sw/sheng).** [SPRINT] The language toggle currently only
  translates the AI explanation text; every button, label, and heading is hardcoded
  English, and it does nothing when AI is offline. Externalize all UI strings into a
  per-language dictionary, render the interface from it, re-render on toggle, and set
  `document.documentElement.lang`. This makes the multilingual claim (constraint 5) and
  the inclusion claim (constraint 3) actually true.

## Inclusion (constraint 3: literacy, digital confidence, device access)

- **Number-first visual comparison.** [nice-to-have] Add a simple bar showing
  "you pay" vs "value received" so the cost ratio is graspable without reading prose —
  serves low-literacy users. The big APR number already leads; this reinforces it.
- **Plainer language pass.** Keep sentences short and jargon-light across all three
  languages for low digital confidence.
- **Feature-phone reach is an inclusion feature, not just low-bandwidth.** The USSD
  path reaches people without smartphones — frame it that way in the pitch.

## Accessibility (constraint 3: disability / assistive tech)

- **`prefers-reduced-motion` guard.** [quick] Disable the landing's transitions/sticky
  animation for users who need reduced motion.
- **Skip-to-content link + heading order.** [quick] Add a skip link; confirm one `h1`
  then `h2`s per page for screen-reader navigation.
- **Set `document.documentElement.lang` on language switch.** [quick] So screen readers
  pronounce Kiswahili/Sheng correctly (folds into the UI-translation work).

## Low bandwidth (constraint 2)

- **Font fallback / drop the web font.** [SPRINT-ish] The app loads Google Fonts over
  the network, a render-blocking third-party request on a bad connection. Make the app
  render instantly in the system font stack and treat the web font as pure enhancement
  (or self-host / drop it entirely for zero third-party requests). Total app payload is
  already tiny (~40 KB, no images), so the font fetch is the only real leak.
- **State the offline-core explicitly in the demo.** The cost engine, licence check,
  rights library, and USSD all run with no external calls; AI degrades gracefully. Show
  this ("if Bedrock is unreachable, the core still works").

## Scalability (judging axis)

- **DONE (2026-09-16): South Africa is now a live second country pack.** `data/za/`
  covers lenders, products, rights, forums, and templates built on real SA bodies
  (National Credit Regulator + National Credit Act, POPIA + Information Regulator,
  credit-bureau disputes, Small Claims Court). The licence check was refactored so each
  pack declares its own licensing authority — adding a country is now genuinely a data
  swap, and the app has a country selector to demo it. Scalability is demonstrated, not
  just claimed.
- Further countries (Ghana, etc.) would follow the same pattern: a new `data/<cc>/`
  folder with the five files and a `licence_authority` block.

## Multilingual (constraint 5)

- **Add one of the brief's named languages (Arabic / French / Portuguese).** The brief
  names these specifically. Deni ships EN/SW/Sheng and shows the mechanism, but shipping
  one of AR/FR/PT as a strings file would literally satisfy the constraint's examples.

## Stability & Social Cohesion (track)

- This track is currently argued (blacklisting → household distress → exclusion) rather
  than built as a distinct feature. If time allows, a feature that visibly reduces
  household-level friction would move it from claim to demonstration.

## Channels / integrations (post-sprint)

- **Outbound SMS receipt via a gateway.** Text the true cost + case reference to the
  user's phone. A real "works on any phone" moment. Needs a gateway account + sender
  setup; out of scope for the sprint. (No Africa's Talking key is bundled — USSD is
  inbound and needs none.)
- **Live regulator / CRB API integration.** Currently the app prepares paperwork and
  routes; it does not file. Real filing is post-sprint.
- **Production USSD shortcode.** USSD logic is real and works via a gateway's sandbox
  simulator; a paid production shortcode is post-sprint.

## Notes on honesty (keep these true in demo + docs)

- Deni does not lend, block, freeze, or erase anything, and cannot remove a CRB listing.
- Not legal or financial advice; recourse stated conditionally, never a promised outcome.
- Named lenders: verifiable facts only ("not on CBK's licensed list as of <date>"),
  never "scam."
- Product figures are representative and dated; the engine computes from shown inputs.
