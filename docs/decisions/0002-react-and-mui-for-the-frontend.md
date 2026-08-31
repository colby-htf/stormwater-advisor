# 2. React and MUI for the frontend

Status: accepted 2026-08-14

## Context

The original scaffold used server-rendered Jinja templates: no build step, no
npm, one language. That was chosen to minimise what had to be learned at once.

We are changing it. The stated motivation was that MUI looks good, and that
React is fast and resembles HTML. Two of those three are wrong, and the
decision is still right — so it's worth recording why, because the wrong
reasons will otherwise get repeated.

**React is not fast.** A server-rendered page beats a React SPA to first paint
essentially always. React ships a runtime, hydrates, and re-renders; the
virtual DOM is a mitigation for the cost of React's own render model, not a
speedup over plain DOM. React is fast *enough*, which is a different claim.

**JSX resembles HTML but is not HTML.** `className`, camelCase attributes,
expressions in braces, no loops in markup. Closer than the alternatives,
genuinely not the same.

**MUI's performance reputation is real and inapplicable here.** The complaints
trace to Emotion injecting styles at runtime and to bundle size. Those bite on
dense tables and large dashboards. This app renders a form and a result card.

## Decision

React 18 + Vite + MUI v6 as a separate app in `frontend/`, talking to a
JSON-only FastAPI backend. Jinja templates removed.

The reasons that actually justify it:

1. **The surface entry form is a dynamic list.** Users add and remove rows, and
   the parent must know the contents at all times. This is unpleasant in
   server-rendered HTML and pleasant in React. It is the single most-used
   screen in the app.
2. **Milestone 9 requires it.** Drawing polygons on aerial imagery is stateful
   client-side UI that server rendering cannot do. Adopting React later means
   rewriting the frontend later.


MUI specifically, over other component libraries: it's the most documented
React component library, which matters most when you're learning.

## Consequences

Costs, stated plainly:

- Two package managers, two dev servers, two CI jobs.
- A contract between two codebases in two languages
  (`frontend/src/contracts.md`), which will rot unless maintained.
- CORS or a dev proxy, and the confusion that comes with it.
- Slower first paint than the Jinja version would have had.
- The MVP grows from 8 steps to 11 — issues 21–26 replace what was one issue.

Mitigation: milestones 1–4 remain pure Python and end at a working JSON API
exercisable from `/docs`. No React until M5. Learning the domain and learning
the framework stay separated in time, so a broken thing is diagnosable.

## What would reverse this

If the map feature is abandoned and the form stays under about four fixed
fields, the React app is carrying its cost without earning it. ADR 0001's
boundary means reverting to server-rendered HTML would touch `api.py` and
`frontend/` only — which is the point of that boundary.
