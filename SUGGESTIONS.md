# Deni Suggestions and Roadmap

Ideas surfaced during the build, kept here so they don't get lost. Grouped by the
brief's own criteria. Not all are for the sprint; the sprint-critical ones are marked.

## Done this session (2026-09-17)

- **Real UI translation (en/sw/sheng).** DONE. All UI strings live in a per-language
  dictionary (`I18N` in `app.js`), the interface re-renders on toggle, and
  `document.documentElement.lang` is set. Works fully offline.
- **Number-first visual comparison.** DONE. A "value received vs you pay" bar now sits
  under the APR in every cost result (and in the landing hero + three-channel preview),
  so the cost ratio is graspable without reading prose.
- **On-device redaction + "not stored" notice.** DONE. The problem text is redacted in
  the browser (phone, ID, email, name) and again server-side, so WhatsApp/USSD are
  covered too; a privacy banner states nothing is stored and lists what was stripped.
- **Stop-contact / cease-and-desist letter.** DONE. A direct-to-lender protective letter
  (Data Protection Act / POPIA) alongside the slow regulator complaint.
- **Helper / multi-case workspace.** DONE, and it is the Stability & Social Cohesion
  feature (see that section below): a paralegal/chief/CSO keeps several borrowers' cases
  on-device.
- **Trust hardening.** DONE. Findings split into official (regulator/court) vs reported
  (press); licence results show the register's as-of date and a verify-live deep link;
  a no-match problem returns a general-body safety net; a source-integrity link checker
  (`backend/check_sources.py`) guards citations.

## In progress

## Inclusion (constraint 3: literacy, digital confidence, device access)

- **Number-first visual comparison.** DONE (see "Done this session"). The value-vs-pay
  bar now reinforces the APR across the result, hero, and channel previews.
- **Plainer language pass.** Keep sentences short and jargon-light across all three
  languages for low digital confidence.
- **Feature-phone reach is an inclusion feature, not just low-bandwidth.** The USSD
  path reaches people without smartphones. Frame it that way in the pitch.

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
  pack declares its own licensing authority. Adding a country is now genuinely a data
  swap, and the app has a country selector to demo it. Scalability is demonstrated, not
  just claimed.
- Further countries (Ghana, etc.) would follow the same pattern: a new `data/<cc>/`
  folder with the five files and a `licence_authority` block.

## Multilingual (constraint 5)

- **Add one of the brief's named languages (Arabic / French / Portuguese).** The brief
  names these specifically. Deni ships EN/SW/Sheng and shows the mechanism, but shipping
  one of AR/FR/PT as a strings file would literally satisfy the constraint's examples.

## Stability & Social Cohesion (track)

- **DONE (2026-09-17): the helper / multi-case workspace is this track's built feature.**
  A chief, paralegal, or CSO worker can hold several borrowers' cases in one place, on
  their device only (localStorage, never a server), and run the same civic engine per
  person. This is community-level coordination, moving the track from an argued claim
  (blacklisting → household distress → exclusion) to a demonstrated feature.

## Channels / integrations (post-sprint)

- **Outbound SMS receipt via a gateway.** Text the true cost + case reference to the
  user's phone. A real "works on any phone" moment. Needs a gateway account + sender
  setup; out of scope for the sprint. (No Africa's Talking key is bundled: USSD is
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
