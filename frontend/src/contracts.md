# Frontend/backend contract

Keep this file in sync with `src/stormwater/api.py`. It exists because the two
sides of the wire are now separate codebases in separate languages, and the
first thing that rots in that arrangement is the shared understanding of what
the JSON looks like.

## `GET /api/municipalities`

```json
[{ "id": "wv-martinsburg", "displayName": "City of Martinsburg, WV" }]
```

## `POST /api/estimate`

Request:

```json
{
  "municipalityId": "wv-martinsburg",
  "surfaces": [
    { "kind": "roof", "material": "shingle", "areaSqft": 1800 },
    { "kind": "driveway", "material": "asphalt", "areaSqft": 600 }
  ]
}
```

Response: a serialized `Comparison`. Fill this in once Issue #17 settles the
schema — and note that money fields are **strings**, not numbers, because the
backend uses `Decimal`. Do not `parseFloat` them for display.

## Open question for Issue #17

Does the API speak camelCase (shown above) or snake_case (Python-native)?
Pick one and write it down here. The only wrong answer is "both sides
translate", because then neither side is authoritative and the bug appears
exactly once, in the field.
