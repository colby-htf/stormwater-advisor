# Stormwater Advisor

Estimates a property's stormwater utility fee from its impervious area, and
compares that against what pervious pavement alternatives would cost and save.

**Status:** scaffold. Nothing is implemented. Every module is a stub with a
docstring explaining its job and the questions you should answer before
writing it. Work the issues in `ISSUES.md` in order.

---

## The one-paragraph version of what this thing does

Rain that lands on grass soaks in. Rain that lands on your roof, driveway and
patio runs off into a pipe someone has to pay for. Municipalities increasingly
bill for that runoff by measuring your impervious area and dividing it by a
standard unit — one ESU/ERU, roughly one typical house's worth. This app takes
a property's surfaces, computes the fee, and then asks the useful follow-up
question: if you replaced the driveway with permeable pavers, how much less
would you pay, and how long until the extra construction cost pays for itself?

## Architecture

Two applications. A Python backend that serves JSON only, and a React frontend
that renders it. Inside the backend, dependencies point downward — nothing
below ever imports anything above it.

```
   frontend/  React + MUI + Vite   ── HTTP/JSON ──►  api.py
      App.jsx owns all state                            │
      client.js is the only fetch                       │
                                                        ▼
                                                  scenarios.py
                                                 (persona fork)
                                                        │
                             ┌──────────────────────────┼──────────────────────┐
                             ▼                          ▼                      ▼
                          esu.py                  pervious.py           mitigation.py
                        fee policy              swap economics        BMP sizing & cost
                             └──────────────────────────┼──────────────────────┘
                                                        ▼
                                                   surfaces.py
                                           area, perviousness, runoff
                                                        │
                                                        ▼
                                                    models.py
                                                shared vocabulary
                                                        ▲
                                                    rates.py
                                       the ONLY module that reads from data/
```

**Why this shape.** The whole economic core — `models`, `surfaces`, `esu`,
`pervious` — is pure functions over plain data. No network, no filesystem, no
framework. That means you can test the part that matters at full speed, and it
means the React app and the AI layer are both replaceable without touching a
line of business logic.

The test you can apply at any point: *could I delete `api.py` and `frontend/`,
write a CLI instead, and change nothing else?* If yes, the boundary is intact.

`frontend/src/contracts.md` documents the JSON between the two halves. It is
the thing most likely to rot — keep it current.

## Layout

| Path | What lives here |
|---|---|
| `src/stormwater/` | All logic. Pure core at the bottom, adapters at the top. |
| `data/` | ESU rates, material costs. Data, not code — changes without a deploy. |
| `frontend/` | React + MUI app. Vite dev server, proxies `/api` to FastAPI. |
| `tests/` | Mirrors `src/`. Start with `test_surfaces.py`. |
| `docs/` | Glossary, data provenance, and architecture decision records. |
| `ISSUES.md` | Your backlog, in dependency order. |

## Getting started

Two terminals. You'll be doing this a lot — consider how you want to handle it.

```bash
# terminal 1 — backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp data/esu_rates.example.json data/esu_rates.json
cp .env.example .env
pytest                                    # everything skipped; expected
uvicorn stormwater.api:app --reload       # http://localhost:8000/docs
```

```bash
# terminal 2 — frontend
cd frontend
cp .env.example .env
npm install
npm run dev                               # http://localhost:5173
```

Vite proxies `/api` to `:8000`, so the browser sees one origin and CORS never
comes up in development. Know that this is a dev-time convenience, not a
production arrangement.

## The MVP is done when

A person can open the app, enter their surfaces, pick a municipality, and see
their estimated annual stormwater fee alongside what pervious alternatives
would cost, save, and pay back — with the rate source shown on screen.

Everything else — on-site mitigation costs, the developer permitting path, AI
recommendations, map drawing, NOAA rainfall projections — is after that.

## Build order

Milestones 1–4 are **pure Python** and end with a working JSON API you can
exercise by hand from `/docs`. Not a line of React until Milestone 5. That's
deliberate: you're learning a new domain and a new frontend framework at the
same time, and separating them in time means that when something breaks you
know which half of your knowledge is at fault.

## Ground rules worth keeping

1. **Money is `Decimal`, never `float`.** Run `0.1 + 0.2 == 0.3` in a REPL
   once and you'll never forget why. It crosses the wire as a *string*.
2. **One canonical unit internally** (square feet). Convert only at the edges.
3. **Every rate carries its source URL and the date you verified it.** When
   someone disputes a number you need to answer in seconds.
4. **The LLM writes sentences, never numbers.**
5. **Unknown data raises, never returns zero.** A silent `$0.00` is the worst
   possible bug in a billing estimator.
6. **`client.js` is the only file that calls `fetch`.** Same one-door principle
   as `rates.py`, applied on the other side of the wire.
