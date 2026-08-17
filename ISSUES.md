# Backlog

42 issues in dependency order. Issues 1–26 are the MVP; everything after is
expansion. `scripts/create_issues.py` parses this file and creates them all in
GitHub, so keep the heading format intact if you edit it.

**How to use this.** Work top to bottom. Don't start an issue whose
dependencies are open. When an issue makes you ask a question the issue
doesn't answer, that's deliberate — the questions under *Sit with these* are
the actual curriculum.

**Milestones**

| | | |
|---|---|---|
| M0 | Foundation | 1–4 |
| M1 | Impervious area core | 5–8 |
| M2 | ESU fee calculation | 9–12 |
| M3 | Pervious pavement comparison | 13–16 |
| M4 | JSON API | 17–20 |
| M5 | React + MUI frontend — **MVP ships here** | 21–26 |
| M6 | On-site mitigation costs | 27–29 |
| M7 | Developer / permitting path | 30–32 |
| M8 | AI recommendation layer | 33–36 |
| M9 | Map-based area capture | 37–38 |
| M10 | Future rainfall & benefits | 39–40 |
| M11 | Multi-municipality scale-out | 41–42 |

**A note on the order.** Milestones 1–4 are pure Python and end with a working
JSON API you can exercise from `/docs`. Not a line of React until M5. That's
deliberate: you're learning a new domain *and* a new frontend framework, and
doing them one at a time means that when something breaks you know which half
of your knowledge is at fault.

---

## M0 — Foundation

### 1. Get the repo, virtualenv, and a green test run
`labels: setup` `milestone: M0 — Foundation` `depends: none`

**Why.** Every hour spent on a broken toolchain later is an hour you thought
you were spending on stormwater. Get boring things boring on day one.

**Done when.**
- [ ] `pip install -e ".[dev]"` succeeds in a clean venv
- [ ] `pytest` runs and reports skipped tests rather than import errors
- [ ] `uvicorn stormwater.api:app --reload` serves `/healthz`
- [ ] `cd frontend && npm install && npm run dev` starts Vite without error
- [ ] First commit pushed

**You'll learn.** Editable installs, why `src/` layout exists, and that you now
have two package managers and two dev servers to keep straight.

**Sit with these.**
- Why does `pyproject.toml` say `pythonpath = ["src"]`? What breaks without it?
- What's the difference between `pip install .` and `pip install -e .`, and
  why does the second one matter while you're building?
- You'll be running `uvicorn` on :8000 and `vite` on :5173 simultaneously,
  forever. Is that two terminals, a process manager, or something else? Decide
  now — you'll do it several hundred times.

---

### 2. Add CI that runs tests and the linter on every push
`labels: setup, infra` `milestone: M0 — Foundation` `depends: 1`

**Why.** You are one person and you will forget things. CI is the teammate who
doesn't.

**Done when.**
- [ ] The backend job runs `pytest` and `ruff check`
- [ ] The frontend job runs `npm run build`
- [ ] The badge is green on `main`
- [ ] A deliberately broken commit turns it red (try it, then revert)

**Sit with these.**
- Why is `npm run build` a useful CI check even before you have tests? What
  class of error does it catch that a linter won't?
- The two jobs run in parallel and neither knows about the other. What kind of
  breakage can that arrangement never catch?

---

### 3. Fill in the domain glossary from primary sources
`labels: research, docs` `milestone: M0 — Foundation` `depends: none`

**Why.** You are building a billing estimator for a domain you don't yet know.
Every `[research]` tag in `docs/domain-glossary.md` is a place where guessing
produces a confidently wrong number.

**Done when.**
- [ ] Every `[research]` marker in the glossary is resolved or converted to a
      dated open question
- [ ] Each definition cites where it came from
- [ ] You can explain ESU vs. ERU vs. stormwater credit out loud, unprompted

**Sit with these.**
- Which of these terms, if you got it wrong, would produce an error nobody
  would notice for months? Start there.

---

### 4. Start an architecture decision log
`labels: docs` `milestone: M0 — Foundation` `depends: none`

**Why.** In four months you will look at a strange choice and not remember
whether it was reasoned or accidental. An ADR is three paragraphs that answer
that.

**Done when.**
- [ ] `docs/decisions/0003-*.md` exists recording your first real decision
- [ ] It states the context, the decision, and what you gave up

**Sit with these.**
- ADR 0002 records why you picked React and MUI. Read it. Do you still agree
  with the reasoning, or did you want it because it looks good? Both are
  allowed — but only one of them is written down.

---

## M1 — Impervious area core

### 5. Define the domain model
`labels: core` `milestone: M1 — Impervious area core` `depends: 1`

**Why.** `models.py` is the vocabulary every other module speaks. Getting it
roughly right now costs an afternoon; getting it wrong costs a rewrite of
everything downstream.

**Done when.**
- [ ] `Surface`, `Property`, `FeeResult`, `PerviousOption`, `Comparison`
      are defined with real types
- [ ] `Surface.__post_init__` rejects negative and absurd areas
- [ ] `python -c "import stormwater.models"` succeeds
- [ ] No calculation, I/O, or framework import appears in the file

**You'll learn.** Dataclasses, frozen vs. mutable, and why a shared vocabulary
is an architectural decision rather than boilerplate.

**Sit with these.**
- Should `Surface` be frozen? What does immutability buy you when
  `pervious.py` needs to produce a modified copy of a property?
- Where should the "can this become pervious pavement?" fact live — on
  `SurfaceKind`, on `SurfaceMaterial`, or in a lookup table in `pervious.py`?
  Argue all three before choosing.

---

### 6. Write failing tests for impervious area
`labels: core, tests` `milestone: M1 — Impervious area core` `depends: 5`

**Why.** Writing these before the implementation forces you to decide what
"impervious area" *means* before you decide how to compute it. That ordering
is the whole point.

**Done when.**
- [ ] `tests/test_surfaces.py` has real assertions with hand-computed expected
      values
- [ ] The skip marker is removed
- [ ] Every test fails for the right reason (`NotImplementedError`)

**Sit with these.**
- Write the expected number in each assertion *before* writing the function.
  If you can't, you don't yet know what the function should do — what's the
  missing information?
- What should a gravel driveway count as? Where did your answer come from?

---

### 7. Source runoff coefficients from a citable reference
`labels: research` `milestone: M1 — Impervious area core` `depends: none`

**Why.** `RUNOFF_COEFFICIENTS` is an empty dict on purpose. Numbers from memory
are how a hobby project becomes a liability.

**Done when.**
- [ ] Coefficients populated from a named engineering manual
- [ ] The source and table number recorded in `docs/data-sources.md`
- [ ] You can explain what `C` means in `Q = C·i·A`

**Sit with these.**
- Your MVP fee calculation doesn't use these at all. Why source them now
  rather than at Milestone 6, when mitigation sizing needs them?
- Coefficients vary by soil group and slope. Does your data structure have
  room for that, or have you flattened away something you'll need?

---

### 8. Implement `surfaces.py`
`labels: core` `milestone: M1 — Impervious area core` `depends: 6, 7`

**Why.** The root of the dependency tree. Everything downstream is a function
of this number.

**Done when.**
- [ ] `is_impervious`, `impervious_area`, `effective_runoff_area` implemented
- [ ] All tests from #6 pass
- [ ] The module imports nothing from `esu`, `pervious`, `rates`, or `fastapi`

**Sit with these.**
- Check that last box carefully. If you needed an import from `rates.py` to
  make this work, something belongs in a different module — what?

---

## M2 — ESU fee calculation

### 9. Design the rate data schema
`labels: core, research` `milestone: M2 — ESU fee calculation` `depends: 5`

**Why.** Rates are data, not code. This issue decides how expressive that data
gets to be — and therefore how many municipalities you can support without
touching Python.

**Done when.**
- [ ] `EsuRate` fields finalized, including provenance and verification date
- [ ] `data/esu_rates.example.json` reflects the final schema
- [ ] The schema can express at minimum: flat fee, ERU multiples, a minimum
      charge, and a cap

**Sit with these.**
- Tiered billing ("0–2,000 sqft = $8, 2,001–5,000 = $16") doesn't fit an
  ERU-multiple model. Do you extend the schema now, or accept that adding
  tiered municipalities later means a migration? What's the cost of each?
- Rates have effective dates. Does the MVP need date-aware lookup?

---

### 10. Research and record one municipality's real rate
`labels: research` `milestone: M2 — ESU fee calculation` `depends: 9`

**Why.** One real, verified municipality beats ten plausible ones. This is
also where you discover which questions the published materials don't answer.

**Done when.**
- [ ] `data/esu_rates.json` has one fully verified entry
- [ ] `rounding_rule` is a real answer, not a TODO — from the ordinance or a
      phone call
- [ ] `verified_on` is today's date and `source_url` points at what you read
- [ ] `docs/data-sources.md` updated

**You'll learn.** That the hardest part of civic software is usually finding
out what the rule actually is.

**Sit with these.**
- The published FAQ probably doesn't state the rounding rule. Who does know,
  and what's the fastest path to them?
- If the ordinance and the FAQ disagree, which do you encode, and what do you
  show the user?

---

### 11. Implement `esu.py`
`labels: core` `milestone: M2 — ESU fee calculation` `depends: 8, 10`

**Why.** Impervious area to dollars. The arithmetic is trivial; the policy
(rounding, floors, caps, billing period) is where every bug will live.

**Done when.**
- [ ] `esu_count`, `billable_esu`, `annual_fee` implemented
- [ ] `tests/test_esu.py` unskipped and passing, including golden numbers
      from the real municipality in #10
- [ ] Money is `Decimal` throughout — no `float` touches a dollar figure
- [ ] `FeeResult` carries enough to explain the number to a skeptical user

**Sit with these.**
- You can build and fully test this module before `rates.py` can load a single
  file, by constructing `EsuRate` objects directly in tests. Why is that
  possible, and what does it tell you about where to draw boundaries?
- Compute the annual fee for 3,000 sq ft under each plausible rounding rule.
  How far apart are they? Is that gap acceptable to ship with a caveat?

---

### 12. Implement `rates.py` loading and validation
`labels: core` `milestone: M2 — ESU fee calculation` `depends: 9`

**Why.** The single door between disk and logic. Everything it lets through
badly formed becomes a mystery bug three modules away.

**Done when.**
- [ ] `load_esu_rates`, `get_rate`, `annualize` implemented
- [ ] A malformed or incomplete rate file fails loudly at load, not at request
- [ ] `get_rate` on an unknown municipality raises `RateNotFoundError`
- [ ] A test asserts the annual/monthly conversion in both directions

**Sit with these.**
- `annualize` is two lines and will silently produce a 12× error if reversed.
  What test catches that, and would you have written it unprompted?
- Should rates load once at startup or on every request? What do you gain and
  lose from each?

---

## M3 — Pervious pavement comparison

### 13. Model material costs
`labels: core` `milestone: M3 — Pervious comparison` `depends: 5`

**Why.** The savings side of your value proposition needs a cost side.

**Done when.**
- [ ] A cost lookup exists keyed by `SurfaceMaterial`
- [ ] The model represents a *range*, not a false-precision point estimate
- [ ] `load_material_costs` implemented and validated

**Sit with these.**
- A range is honest and hard to act on; a midpoint is actionable and slightly
  false. Which do you compute with internally, and which do you display?
  They don't have to be the same choice.

---

### 14. Research pavement costs and record provenance
`labels: research` `milestone: M3 — Pervious comparison` `depends: 13`

**Why.** These numbers drive a five-figure homeowner decision.

**Done when.**
- [ ] `data/material_costs.json` populated from at least two independent
      sources
- [ ] At least one local West Virginia data point (a contractor quote,
      an extension publication, a public bid tabulation)
- [ ] `docs/data-sources.md` updated with sources and date

**Sit with these.**
- Do your pervious figures include the deeper stone sub-base and excavation
  that permeable systems require? If not, your savings estimate is biased in
  the direction most likely to embarrass you.
- National averages vs. Eastern Panhandle reality — how big is the gap, and
  how would you even find out?

---

### 15. Implement swap eligibility and cost delta
`labels: core` `milestone: M3 — Pervious comparison` `depends: 11, 14`

**Why.** Deciding *what can be swapped* and *what the swap costs extra* — the
two inputs to every recommendation this app makes.

**Done when.**
- [ ] `PERVIOUS_SUBSTITUTES` populated as data, not `if`/`else` chains
- [ ] `eligible_surfaces` excludes roofs and anything else non-convertible
- [ ] `upfront_cost_delta` implemented, with the "already repaving?" case
      handled explicitly one way or the other

**Sit with these.**
- A homeowner replacing a failing driveway anyway faces only the *premium*. A
  homeowner with a fine driveway faces the *full* cost. Same app, two
  completely different payback numbers. How does your API know which it is —
  and if it doesn't ask, which assumption did you silently make?

---

### 16. Implement `compare()` and payback
`labels: core` `milestone: M3 — Pervious comparison` `depends: 15`

**Why.** This produces the headline number. It's the reason the project exists.

**Done when.**
- [ ] `compare` returns a populated `Comparison`
- [ ] `tests/test_pervious.py` unskipped and passing
- [ ] Zero-savings does something defined and sane, not `ZeroDivisionError`
- [ ] `pervious.py` contains no fee arithmetic — it calls `esu.py`

**Sit with these.**
- Check that last box honestly. If you divided by `sqft_per_esu` anywhere in
  this module, you now have two copies of the fee rule. When they drift, which
  one will the user see?
- Should `compare` recommend every eligible swap, or only those with a
  reasonable payback? Is that judgment this module's job, or the AI layer's?
- If a utility grants a *credit* rather than reducing assessed area (see
  glossary), is your savings model even structurally right? Verify before you
  build on it.

---

## M4 — JSON API

### 17. Define the request and response contract
`labels: api` `milestone: M4 — JSON API` `depends: 5`

**Why.** You now have two codebases in two languages. This is the seam, and
seams rot silently.

**Done when.**
- [ ] Pydantic models for the estimate request and response
- [ ] `frontend/src/contracts.md` filled in to match, exactly
- [ ] A documented decision on camelCase vs. snake_case over the wire
- [ ] Money serializes as a string, not a float
- [ ] `/docs` renders sensible schemas

**Sit with these.**
- Your core uses `Decimal` specifically to avoid binary floating-point error.
  JSON has no decimal type. If you let FastAPI serialize it as a number,
  what exactly have you thrown away, and where would it first show up?
- camelCase or snake_case? The only wrong answer is "both sides translate" —
  why is that worse than either consistent choice?

---

### 18. Implement `POST /api/estimate`
`labels: api` `milestone: M4 — JSON API` `depends: 16, 17`

**Why.** The MVP endpoint. One call, one scenario function, one result.

**Done when.**
- [ ] The endpoint returns a full comparison for a valid request
- [ ] `scenarios.homeowner_scenario` implemented and called
- [ ] The handler body is thin — parse, call, serialize
- [ ] You have exercised it by hand from `/docs` and the numbers look right

**Sit with these.**
- Count the lines in your handler. If it's over about fifteen, what leaked in
  from the core?
- Poke it from `/docs` before you write any React. Why does having a
  hand-verified endpoint make the frontend milestone dramatically easier to
  debug?

---

### 19. Error handling and API tests
`labels: api, tests` `milestone: M4 — JSON API` `depends: 18`

**Why.** A 500 tells the user nothing and tells you almost as little.

**Done when.**
- [ ] `RateNotFoundError` surfaces as a 404 or 422 with a useful message
- [ ] Invalid input returns 422, never 500
- [ ] `tests/test_api.py` unskipped and passing
- [ ] `rates.py` still contains no HTTP concepts

**Sit with these.**
- How does a domain exception become a status code without the domain knowing
  what a status code is? FastAPI has a mechanism for exactly this — find it
  rather than raising `HTTPException` from deep in your core.
- FastAPI's 422 body is a nested structure describing every validation
  failure. Is that shape something a React component can render usefully, or
  will you need to reshape it? Decide here, not in JSX.

---

### 20. Municipality endpoint
`labels: api` `milestone: M4 — JSON API` `depends: 12, 18`

**Why.** The frontend has to tell the user where they are, and only from the
list you can actually price.

**Done when.**
- [ ] `GET /api/municipalities` returns ids and display names
- [ ] The list comes from the rate data, never a hardcoded array
- [ ] Selecting a municipality with no rate data is impossible by construction

---

## M5 — React + MUI frontend (MVP ships here)

### 21. Scaffold the React app and talk to the API
`labels: frontend` `milestone: M5 — React + MUI` `depends: 20`

**Why.** Smallest possible first step: prove the two halves can speak before
you build anything worth looking at.

**Done when.**
- [ ] `npm run dev` serves a page that renders
- [ ] `MunicipalityPicker` fetches and displays the real list from the API
- [ ] `api/client.js` is the only file that calls `fetch`
- [ ] `ThemeProvider` and `CssBaseline` wrap the app

**You'll learn.** JSX, `useState`, `useEffect`, and the Vite proxy — enough
React to be dangerous, on a component small enough to debug.

**Sit with these.**
- `fetch()` does not throw on a 404 or a 500. It resolves with `ok: false`.
  What would you have shipped if you hadn't known that?
- Your effect fires twice in development. That's `StrictMode` deliberately
  double-invoking to surface impure logic — not a bug. Knowing that now saves
  you an afternoon later. Why would React's authors *want* that?
- What does the user see while the fetch is in flight? "Nothing" is an answer,
  just not a good one.

---

### 22. Build the surface entry form
`labels: frontend, ux` `milestone: M5 — React + MUI` `depends: 21`

**Why.** This is the component that justifies React. A list the user adds to
and removes from, where the parent must always know the contents.

**Done when.**
- [ ] Rows can be added and removed; App holds the array
- [ ] Every input is controlled, with an `onChange` that lifts state up
- [ ] Each row is keyed by a stable id, never the array index
- [ ] There is real help for "I don't know my roof's square footage"
- [ ] It works on a phone
- [ ] A real person who isn't you completes it unaided

**Sit with these.**
- Key on the array index first. Add three rows, delete the middle one, and
  watch what happens to the input values. Then fix it. That bug teaches
  reconciliation better than any article will.
- A frozen-looking MUI input is almost always a missing `onChange`, not a MUI
  problem. Why does React work that way, and what is a "controlled component"?
- Almost nobody knows their driveway's area. Length × width inputs? Size
  presets? Estimate roof footprint from house square footage? A beautiful form
  people abandon at the measuring step is worth less than an ugly one they
  finish.

---

### 23. Build the results view
`labels: frontend, ux` `milestone: M5 — React + MUI` `depends: 22`

**Why.** One number the user came for, plus enough evidence to trust it.

**Done when.**
- [ ] Annual fee prominent; savings and payback alongside
- [ ] Impervious area, ESU count, and rate source visible without navigating
- [ ] A plain-language statement that this is a planning estimate, not a bill
      and not a permit determination
- [ ] Rate source URL and verification date on screen
- [ ] Currency formatted with `Intl.NumberFormat`, not string concatenation

**Sit with these.**
- MUI will let you build something that *looks* authoritative. This number
  isn't. Does your visual design imply more confidence than you have?
- A 40-year payback is a real possible output. Does the panel present it as
  neutrally as a 6-year payback? Look at your color choices specifically —
  green for "savings" is a claim, not a decoration.

---

### 24. Loading, error, and empty states
`labels: frontend` `milestone: M5 — React + MUI` `depends: 23`

**Why.** The happy path is maybe a third of the work, and the other two-thirds
is what makes it feel finished.

**Done when.**
- [ ] In-flight requests show progress and disable resubmission
- [ ] A backend that's down produces a human message, not a blank screen
- [ ] Validation errors from the API render next to the relevant field
- [ ] First load shows something useful before any input

**Sit with these.**
- You modelled status as one string rather than separate `isLoading` and
  `isError` booleans. Try it with booleans and enumerate the combinations.
  How many are impossible-but-representable, and what does that cost you?
- Should the previous result stay on screen while a new request runs, or
  clear? Consider a user staring at a number that no longer matches the form.

---

### 25. Theme and responsive polish
`labels: frontend, ux` `milestone: M5 — React + MUI` `depends: 24`

**Why.** The reason you picked MUI. Cash it in — in one place.

**Done when.**
- [ ] `theme.js` holds the palette and typography; no hardcoded colors in
      components
- [ ] Contrast ratios checked against WCAG AA
- [ ] Layout works from phone to desktop
- [ ] Production bundle size measured and written down

**Sit with these.**
- Defining a theme object inside a component body creates a new object every
  render and re-renders every consumer. Why? This is the one MUI performance
  footgun you're actually likely to fire.
- What's your bundle size? Is it acceptable for someone on a rural WV mobile
  connection — which is a meaningful share of your users?

---

### 26. MVP acceptance walkthrough
`labels: milestone` `milestone: M5 — React + MUI` `depends: 25`

**Why.** Declare it done deliberately, or you'll drift into Milestone 6 without
ever having shipped anything.

**Done when.**
- [ ] A stranger completes the flow end to end and gets a sensible number
- [ ] You hand-verify one property's fee against the utility's own estimator
      or a real bill, and they agree
- [ ] README updated to describe what exists rather than what's planned
- [ ] Tagged `v0.1.0`

**Sit with these.**
- Where did your number differ from the real bill, and was the cause a bug or
  a policy detail you hadn't modelled? Either way, write it down.

---

## M6 — On-site mitigation costs

### 27. Research BMP unit costs
`labels: research` `milestone: M6 — Mitigation costs` `depends: 26`

**Done when.**
- [ ] `data/mitigation_costs.json` populated for rain barrels, rain gardens,
      dry wells, and detention basins
- [ ] Both capital and annual maintenance cost captured
- [ ] Sources recorded

**Sit with these.**
- If you model capital cost but not maintenance, which options does your app
  systematically over-recommend?

---

### 28. Determine the design storm and capture volume rule
`labels: research` `milestone: M6 — Mitigation costs` `depends: 27`

**Done when.**
- [ ] The governing design storm for your target jurisdiction is documented
- [ ] `required_capture_volume_cf` implemented with unit tests
- [ ] Units verified by hand: sq ft × inches → cubic feet → gallons

**Sit with these.**
- Compute how many 55-gallon rain barrels a 2,000 sq ft roof needs to capture
  one inch of rain. Do it on paper first. What does that number tell you about
  whether rain barrels are a mitigation strategy or a public-education gesture
  — and should your app say so?

---

### 29. Implement BMP sizing and costing
`labels: core` `milestone: M6 — Mitigation costs` `depends: 28`

**Done when.**
- [ ] `size_bmp`, `capital_cost`, `annual_maintenance_cost` implemented
- [ ] Results carry an explicit "planning-level, not an engineered design"
      qualifier all the way to the UI

---

## M7 — Developer / permitting path

### 30. Model development-scale inputs
`labels: core` `milestone: M7 — Developer path` `depends: 29`

**Sit with these.**
- Is a development one `Property` with many surfaces, or many `Property`
  objects? Which makes phased build-out easier to express later?

---

### 31. Implement `developer_scenario`
`labels: core` `milestone: M7 — Developer path` `depends: 30`

**Why.** The developer's real question: is it cheaper to build detention, or
to pave pervious and avoid needing as much?

**Done when.**
- [ ] Detention-based and pervious-based compliance paths priced side by side
- [ ] Ongoing ESU fees included, not just capital cost
- [ ] The persona fork lives in `scenarios.py` and nowhere else

**Sit with these.**
- Grep for `if.*developer` outside `scenarios.py`. Every hit is a place the
  design is leaking. Why does that matter more here than it felt like it did
  at Milestone 1?

---

### 32. Research permit thresholds
`labels: research` `milestone: M7 — Developer path` `depends: 31`

**Done when.**
- [ ] The disturbed-area threshold that triggers stormwater permitting in WV
      is documented with a citation
- [ ] The app tells a developer whether they're likely over it — and says
      plainly that this is not a determination

---

## M8 — AI recommendation layer

### 33. Implement the privacy boundary
`labels: ai` `milestone: M8 — AI layer` `depends: 26`

**Why.** Build the boundary before the thing that needs bounding.

**Done when.**
- [ ] `summarize_for_model` returns only what the model needs
- [ ] Addresses and free-text labels are stripped
- [ ] A test asserts that a `Comparison` containing an address produces a
      payload with no address in it

**Sit with these.**
- What's actually in `Surface.label` after a real user fills in your form?
  Have you looked?

---

### 34. Write the system prompt
`labels: ai` `milestone: M8 — AI layer` `depends: 33`

**Done when.**
- [ ] The prompt forbids arithmetic, invented policy, and invented rebates
- [ ] It requires naming the case where the honest answer is "don't do this"
- [ ] It requires the planning-estimate caveat

**Sit with these.**
- An assistant that only ever encourages the purchase is a sales tool. What
  concrete instruction makes yours capable of saying "40-year payback, not
  worth it"?

---

### 35. Wire up generation
`labels: ai` `milestone: M8 — AI layer` `depends: 34`

**Done when.**
- [ ] `generate_recommendation` calls the model with the summarized payload
- [ ] Behind the `ENABLE_AI_RECOMMENDATIONS` flag
- [ ] API key read server-side from environment, never committed
- [ ] Failure degrades to the deterministic numbers, never a broken page

**Sit with these.**
- The key lives on the FastAPI server, not in the React app. Vite only exposes
  `VITE_`-prefixed variables to the client — and everything it exposes ships to
  the browser. Why is that restriction there, and what would putting the key in
  `frontend/.env` actually do?

---

### 36. Implement the ungrounded-number guard
`labels: ai, tests` `milestone: M8 — AI layer` `depends: 35`

**Why.** The most important function in the AI layer. Without it, "the LLM
never does math" is a hope rather than a property of the system.

**Done when.**
- [ ] `validate_no_new_numbers` extracts numeric claims and checks each
      against the input
- [ ] Tests cover a clean case and a hallucinated-figure case
- [ ] Ungrounded output is blocked or flagged, never shown silently

**Sit with these.**
- "$1,200" and "1200 dollars" and "twelve hundred" are the same claim. How far
  do you chase that before the guard becomes its own project?

---

## M9 — Map-based area capture

### 37. Add map polygon drawing
`labels: frontend, feature` `milestone: M9 — Map capture` `depends: 26`

**Why.** The biggest usability win available, and half the reason you adopted
React in the first place.

**Done when.**
- [ ] A user can trace surfaces on aerial imagery
- [ ] Traced areas populate the same state shape the manual form uses
- [ ] Manual entry still works — the map is an input method, not a replacement

**Sit with these.**
- Aerial imagery lets a user trace their roof. It also invites them to trace
  it badly. What does your UI do about a polygon that's obviously wrong?
- The map library owns a chunk of DOM that React doesn't control. That tension
  has a standard answer in React. Find out what `useRef` is for before you
  start fighting it.

---

### 38. Compute area from geometry correctly
`labels: core, feature` `milestone: M9 — Map capture` `depends: 37`

**Done when.**
- [ ] Areas computed in a projected CRS appropriate to West Virginia, not in
      raw lat/lon degrees
- [ ] A known-size building is measured within a few percent

**Sit with these.**
- Compute the area of a rectangle in EPSG:4326 degrees and in a WV State Plane
  projection. How wrong is the first one, and why is it wrong in a way that
  varies with latitude?
- Should this math run in the browser or on the server? You have a perfectly
  good Python geospatial ecosystem available. What does each choice cost?

---

## M10 — Future rainfall & benefits

### 39. Bring in NOAA precipitation data
`labels: research, feature` `milestone: M10 — Future rainfall` `depends: 29`

**Done when.**
- [ ] Current precipitation-frequency values for the target area retrieved
      from NOAA Atlas 14
- [ ] The status and availability of forward-looking projections (Atlas 15)
      documented

---

### 40. Project future benefits
`labels: feature` `milestone: M10 — Future rainfall` `depends: 39`

**Why.** If storms intensify, mitigation built today is worth more than a
present-day payback calculation suggests.

**Sit with these.**
- This is where a defensible tool most easily becomes an indefensible one.
  What's the least speculative version of this claim you can make and still
  have it be useful?

---

## M11 — Multi-municipality scale-out

### 41. Build the rate research pipeline
`labels: research, infra` `milestone: M11 — Scale-out` `depends: 26`

**Done when.**
- [ ] A documented, repeatable process for adding a municipality
- [ ] A staleness check that flags rates not verified within N months

**Sit with these.**
- You chose to keep AI out of data gathering, which was right. Does that hold
  at fifty municipalities? What would have to be true about verification for
  it to change?

---

### 42. Address to municipality lookup
`labels: feature` `milestone: M11 — Scale-out` `depends: 41`

**Sit with these.**
- Municipal boundaries and mailing addresses disagree constantly — a
  Martinsburg mailing address may sit outside the city limits and owe nothing.
  What does your app do when it isn't sure, and is "ask the user" a cop-out or
  the correct answer?
