# Domain glossary

**Impervious surface** — Any surface that prevents rain from soaking into the
ground: roofs, asphalt, concrete, compacted gravel (usually), pools, patios.
The single input everything in this project depends on.

**Pervious / permeable pavement** — Engineered surfaces that let water pass
through into a stone reservoir and then into the soil: pervious concrete,
porous asphalt, permeable interlocking pavers, plastic or concrete grass
grids. Note that "pervious" and "permeable" are used interchangeably in the
trade but sometimes distinguished in specs.
-- Permeable systems are supported by gaps, joints around solid interlocking blocks.
-- Pervious materal allows water to move directly through its entire porous
surface
-- The difference in pervious and permeable is that pervious surface are 
natural absorbing ground and permeable describes engineered systems
and are subject to credits. (permeable pavement, rain barrels/gardens, etc.) 
-- [Source - Permeable and Pervious Definitions](https://stormwater.wef.org/2013/10/pervious-permeable-porous-pavers-really/)
-- Pervious surfaces are excluded from ERU calculations


**ESU — Equivalent Stormwater Unit** / **ERU — Equivalent Residential Unit** —
The billing unit. The utility measures the impervious area of a typical
single-family home in its service area, calls that 1 unit, and bills every
property in multiples of it. *Worked example:* Martinsburg, WV set 1 ERU =
2,280 sq ft of impervious surface at $12.00/month, with a $6.00/month minimum.

-- ESU and ERU are used almost interchangably, the difference is that ESU 
is used to highlight a property's demand for stormwater utlity services. 
-- Most municipalities seem to use the ERU terminology.
-- Determining the amount of sq/ft in an ERU as based on the statistical median 
[Source](https://www.epa.gov/sites/default/files/2015-10/documents/fundingstormwater.pdf)
-- In Washington D.C., an ERU is defined as an area equivalent to 1,000 square feet. 
Each ERU costs $2.67 per month, and the strucure is as follows:
Square Feet of Impervious Surface | Number of ERU's
100 to 600 | 0.6 
700 to 2,000 | 1.0
2,100 to 3,000 | 2.4
3,100 to 7,000 | 3.8
7,100 to 11,000	| 8.6
11,000 and above | 13.5
[Source](https://doee.dc.gov/service/changes-districts-stormwater-fee)
-- For a property encompassing 26,500 square feet, the rate structure would be calculated
as follows: 26,500 sqft / 1000 = 26.5 ERU's * 2.67 = **70.76 per month**
-- Stormwater fees are subject to change via EPA guidelines (at least in DC, need to look at other municipalities)
[Source](https://doee.dc.gov/service/changes-districts-stormwater-fee)


**Rounding rule** — How partial ESUs are billed. A property with 3,000 sq ft
of impervious area is 1.316 ERUs. Utilities variously bill the exact fraction,
round to nearest, round up, or use half-unit tiers.
-- ESU rounding varies depending on what municipality you are looking at.
-- DC calculates raw ESU's and converts the cost of the stormwater fee from there.
-- DC, however, also includes a CRAIC (Clean Rivers Impervious Area Charge) when
assessing stormwater fees, and adds it in to the normal ERU fee calculation.
This fee is 24.23/ERU/Month [Source](https://doee.dc.gov/calculating-a-riversmart-rewards-discount)
-- For a 2.3 ESU property, the calculation is 2.3 * (2.67 per ERU + 24.23 CRAIC fee/ERU) = **$61.87/month**
-- Additional fees can sometimes appear in conjucntion with normal ERU-based assessment fees,
but varies by municipality.
-- Some municipalities, like DC, keep fractional ERUs in place while, other ones round
up to the nearest whole number.


**Stormwater credit** — A reduction in the fee granted when an owner manages
runoff on site. Critically, this is usually a *discount on the bill*, not a
*reduction in assessed impervious area* — which means modeling pervious
pavement as "less impervious area" may produce the wrong number.

-- Permeable paver swaps are subject to a $15 dollar credit per square foot in DC and
$8 per square foot of impervious surface removed and replaces with vegetaion [Source](https://doee.dc.gov/riversmartrebates)
-- This is part of the larger RiverSmart program that DC has in place. There are two different types of applications required to 
recieve these incentives. A *simple application* for residential properties managing **2000 square feet or less of impervious 
surface**, and *standard application* for commercial properties **2000 sqare feet or more** of impervious surface. Complex engineering
documentation is needed to supplement this type of application. [Source](https://doee.dc.gov/riversmartrewards)
-- Washington D.C also has a SRC (Stormwater Retention Credit) program where 
**one gallon of stormwater retention for a year is equivalent to one credit.** 
[Source](https://www.greenfinanceinstitute.com/hive/revenues-for-nature/case-studies/dc-stormwater-retention-credit-trading-programme/)
-- Real estate developers who are legally mandated to retain stormwater on their construction sites but lack the physical space
 can purchase your credits on an open market to fulfill up to 50% of their regulatory requirements off-site



**Runoff coefficient (C)** — The fraction of rainfall that leaves a surface as
runoff. Roughly 0.95 for asphalt, far lower for turf, and dependent on soil
type and slope. Used in the Rational Method (`Q = C·i·A`).
-- Q = Peak rate of runoff
-- C = Dimensionless runoff coefficient (depends on type of surface), ranges from .05 
to 0.95
-- i = Average rainfall intensity
-- A = Tributary drainage area (acres)

| Description of Area / Character of Surface | Runoff Coefficient |
|---|---:|
| **Business** | |
| ↳ Downtown | 0.70 - 0.95 |
| ↳ Neighborhood | 0.50 - 0.70 |
| **Residential** | |
| ↳ Single-family | 0.30 - 0.50 |
| ↳ Multiunits, detached | 0.40 - 0.60 |
| ↳ Multiunits, attached | 0.60 - 0.75 |
| Residential (suburban) | 0.25 - 0.40 |
| Apartment | 0.50 - 0.70 |
| **Industrial** | |
| ↳ Light | 0.50 - 0.80 |
| ↳ Heavy | 0.60 - 0.90 |
| Parks, Cemeteries | 0.10 - 0.25 |
| Playgrounds | 0.20 - 0.35 |
| Railroad yard | 0.20 - 0.35 |
| Unimproved | 0.10 - 0.30 |
| **Character of Surface** | |
| **Pavement** | |
| ↳ Asphaltic and concrete | 0.70 - 0.95 |
| ↳ Brick | 0.70 - 0.85 |
| Roofs | 0.75 - 0.95 |
| **Lawns, sandy soil** | |
| ↳ Flat, 2% | 0.05 - 0.10 |
| ↳ Average, 2-7% | 0.10 - 0.15 |
| ↳ Steep, 7% | 0.15 - 0.20 |
| **Lawns, heavy soil** | |
| ↳ Flat, 2% | 0.13 - 0.17 |
| ↳ Average, 2-7% | 0.18 - 0.22 |
| ↳ Steep, 7% | 0.25 - 0.35 |

[Source](https://www.txdot.gov/manuals/des/hyd/chapter-4--hydrology/section-12--rational-method/runoff-coefficients.html)


**BMP — Best Management Practice** — Any on-site stormwater control: rain
barrel, rain garden / bioretention cell, dry well, infiltration trench,
detention or retention basin, underground vault.

**Detention vs. retention** — Detention holds water and releases it slowly;
retention holds it and lets it infiltrate or evaporate. Different structures,
different costs, different permit language. Don't use them as synonyms.

**Design storm** — The rainfall event a mitigation system must handle, e.g.
"capture the first 1 inch in 24 hours" or "detain the 10-year, 24-hour event".
Set by the permit. Sizing anything without knowing this is
guessing.

-- A design storm is hypothetical or statistical rainfall event defined defined by its
duration and depth, used by engineers to model runoff

**Water quality volume (WQv)** — The runoff volume a BMP must treat, typically
the first fraction of an inch. Distinct from the peak-flow control volume.

**MS4 — Municipal Separate Storm Sewer System** — The federal Clean Water Act
permitting program that pushes municipalities to fund stormwater programs.
It's the *reason* ESU fees exist, and useful context for why rates rise.

**NOAA Atlas 14 / Atlas 15** — The federal precipitation-frequency atlases
that define what a "10-year storm" actually means in inches for a given
location. Atlas 15 is the effort to incorporate future/nonstationary climate
projections. Relevant to the future-benefits milestone.

Atlas 14 is the current regional-volume standard assuming a stationary climate,
 while Atlas 15 is a unified national update incorporating historical climate trends and future projections
 [Source](https://water.noaa.gov/about/atlas15)

**Simple payback period** — `upfront cost premium ÷ annual savings`. Ignores
discount rates, maintenance, surface lifespan, and future rate increases.
Adequate for an MVP if — and only if — you say so on screen.
