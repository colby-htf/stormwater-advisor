# 1. Keep the calculation core pure

Status: accepted (scaffold)

## Context

This app has four plausible front doors — an HTTP API, an HTML form, an LLM
recommendation layer, and eventually a map UI — and one thing of actual value:
a correct chain from measured surfaces to dollars.

The tempting shape is to let FastAPI route handlers read the rate file, do the
ESU arithmetic, and render a template. It is fewer files and it works on day
one. It also means the only way to test whether a fee is right is to boot a web
server, and the only way to change the web layer is to risk the math.

## Decision

`models.py`, `surfaces.py`, `esu.py`, `pervious.py` and `mitigation.py` are
pure: no filesystem, no network, no clock, no framework imports. They receive
already-loaded rate objects as arguments.

`rates.py` is the only module that reads `data/`. `api.py` is the only module
that knows about HTTP. `scenarios.py` composes but does not compute.
Dependencies point downward only.

## Consequences

Good: the economic core is testable in milliseconds with no fixtures. The web
layer can be replaced with a CLI without touching business logic. The LLM layer
is structurally incapable of influencing a number.

Costs: more files than the problem strictly requires at this size, and rate
objects have to be threaded through function signatures rather than looked up
where they're needed. That threading is deliberate — it makes every dependency
visible at the call site.

## The test

Could you delete `api.py`, write a command-line interface instead, and change
nothing else? If not, something has leaked.
