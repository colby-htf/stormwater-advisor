# Data sources & provenance

Every number this app shows a user must be traceable to a source and a date.
This file is that ledger. 

## Why this file matters more than it looks

Your app tells someone their driveway will save them $186/year. They will
either act on that or dispute it. Either way, "where did that come from?" must
be answerable in under a minute, by you, in six months, without re-deriving
anything.

## ESU / stormwater utility rates

| Municipality | 1 ESU (sq ft) | Rate | Period | Source | Verified |
|---|---|---|---|---|---|
| Martinsburg, WV | 2,280 | $12.00 | monthly | [City announcement](https://www.cityofmartinsburg.org/Home/Components/News/News/73/) | **TODO** |
| Morgantown, WV | ? | ? | ? | [MUB Stormwater](ht

tps://mub.org/stormwater) — figures not on the landing page; MUB directs enquiries to (304) 292-8443 / stormwater@mub.org, and Article 929 of the city code | **TODO** |
| Beckley, WV | ? | ? | ? | [Beckley Sanitary Board stormwater FAQ](https://beckleysanitaryboard.org/stormwater-faq/) | **TODO** |

Notes:

- The Martinsburg figures come from the utility's launch announcement covering
  the fee's 2022 start, including a phase-in that capped billed ERUs (1 in
  2022, 2 in 2023, 4 in 2024, uncapped after). **Rates are revised over time —
  confirm the current schedule before shipping.** Issue #10.
- The minimum charge there was $6.00/month, described as a half-ERU floor.
- The rounding rule is not stated in the announcement. Find it in the
  ordinance or by calling. It changes every bill you compute.

### Where to look for a municipality's rate

1. The municipal code (Municode / American Legal Publishing) — search
   "stormwater utility" and look for the fee article.
2. The utility board's tariff or rate sheet.
3. The public-service commission filing, if the utility is regulated.
4. Call. Utility billing offices answer this question routinely.

Prefer the ordinance over a news article or FAQ page. Record the URL you
actually read, not a search result.

## Fee methodology background

Stormwater utilities generally use one of four approaches — flat fee, ERU/ESU
multiples, tiered bands, or residential equivalency factors that fold in slope
and soil. ERU-based billing is the most common. Useful overview:
[Types of stormwater utility fees](https://www.ecopiatech.com/resources/blog/types-of-stormwater-utility-fees-how-to-calculate).

Your data model should be able to express at least flat, ERU, and tiered.
Whether the MVP *implements* all three is a separate question — see Issue #9.

## Pavement material costs

Installed cost per square foot, US national ranges. Regional variance is large
and these move with materials pricing, so re-check before shipping.

| Material | Low | High | Pervious |
|---|---|---|---|
| Concrete driveway | $4 | $8 | no |
| Asphalt driveway | $5 | $12 | no |
| Porous asphalt | $7 | $13 | yes |
| Pervious concrete | $8 | $16 | yes |
| Permeable pavers | $10 | $30 | yes |
| Grass grid (concrete or plastic) | $4 | $12 | yes |

Source: [HomeGuide permeable pavers cost guide](https://homeguide.com/costs/permeable-pavers-cost)
(2026 figures). Cross-check against at least one contractor-facing source and
one local WV quote before these numbers drive a recommendation. Issue #14.

**A trap worth naming:** permeable systems usually need a deeper stone
sub-base than conventional paving, and the sub-base is a real share of the
cost. If your "low" figures quietly exclude excavation, your savings estimate
is optimistic in exactly the direction that gets people annoyed with you.

## Mitigation / BMP costs

Not yet researched. Issue #27. Candidate sources: EPA stormwater BMP cost
literature, state DEP stormwater manuals, university extension publications,
and the WV DEP stormwater program.

## Runoff coefficients

[Source](https://www.txdot.gov/manuals/des/hyd/chapter-4--hydrology/section-12--rational-method/runoff-coefficients.html)

## Future rainfall projections

Not yet researched. Issue #39. Start with NOAA Atlas 14 for current
precipitation frequency, and check the status of Atlas 15 for projections that
account for a changing climate.
