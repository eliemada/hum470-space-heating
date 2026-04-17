# Supervisor Meeting Notes — Week of March 31

## EUBUCCO Dataset — Disappointing for Switzerland

Last week you suggested looking into the satellite-based building database from the
German team. We investigated two datasets:

1. **EUBUCCO** (TU Berlin, Milojevic-Dupont et al., *Scientific Data* 2023)
   - 2.6 million Swiss building footprints
   - **Problem: 0% building type coverage for Switzerland.** The Swiss source data
     (swisstopo swissTLM3D) only contributed geometry and height — no classification
     (residential/non-residential), no construction year. Switzerland is one of the
     worst-covered countries in the dataset for non-geometric attributes.
   - We cannot distinguish EFH from MFH with EUBUCCO alone.

2. **GlobalBuildingAtlas** (TU Munich, Zhu et al., *ESSD* 2025)
   - 2.75 billion buildings worldwide, 3m resolution from PlanetScope satellite
   - Same issue: footprints + heights only, no building type classification.

**What we used instead:** The official Swiss GWR (Gebäude- und Wohnungsregister),
accessed via the stats.swiss SDMX API. This gives us:
- All 1.8M residential buildings classified by category (EFH, MFH, mixed-use, partial)
- Heating energy source per building (oil, gas, heat pump, wood, etc.)
- Annual data 2021–2024
- Cross-tabulated: building type × heating source × construction period × canton

This is strictly better than EUBUCCO for our analysis because we need heating system
data, not satellite geometry.

---

## What We Did This Week (Progress Update)

### Phase 7: EFH vs MFH Building Type Analysis (NEW)
- Downloaded GWR data via stats.swiss API — all 4 residential building categories
- Created **fig15**: Two-panel chart showing:
  - Left: heating source composition across all 4 building categories (2024)
  - Right: heat pump adoption trend 2021→2024 (slope chart by category)
- Created **fig16**: Floor area per person by construction period — EFH vs MFH
- Key finding: **"Four-speed transition"** — HP adoption rates:
  - EFH: 21% → 28% (fastest)
  - MFH: 15% → 20%
  - Mixed-use: 7% → 11%
  - Partial residential: 6% → 9% (slowest)
- Added narrative on split incentive, MFH barriers, biofuels as transitional option

### Other Improvements (from last week)
- 4-factor LMDI decomposition (added floor area/capita as a factor, with toggle)
- Replaced waterfall charts with IPCC-style diverging bars (fig8, fig9)
- Full TOTEX analysis across 3 CO₂ levy scenarios with justification (fig14)
- Monte Carlo fan chart now shows full historical data 2000–2024
- CO₂ levy justification: CHF 120/t (current law), 200/t (revised CO₂ Act), 300/t (IPCC SCC)

### Total: 16 figures now (fig1–fig16)

---

## Questions for Supervisor

1. For the EFH vs MFH analysis, should we go deeper into cantonal differences
   (the API supports canton-level data), or is the national-level split sufficient?

2. The EUBUCCO/satellite data could still be useful for *spatial* analysis
   (e.g., mapping HP adoption by neighborhood density). Is that worth pursuing,
   or should we stay focused on the aggregate decomposition?

3. For Monte Carlo distributions: we currently use uniform for renovation rate
   and normal for HDD decline. Should we justify these more formally (e.g.,
   triangular based on expert elicitation), or is the current approach acceptable?

4. Timeline: interim presentation is April 22. Do you have a preferred slide format?

---

## Insulation / Retrofit Investigation

### What we investigated
You suggested looking at insulation rates as a potential 5th LMDI factor to
separate envelope improvements from the catch-all intensity term. We spent time
exploring whether this could work as a formal decomposition factor.

### Data sources we checked
- **GEAK/CECB database**: Has building-level energy ratings, but only as
  cross-sectional snapshots (when a building gets certified). No consistent
  annual time series of stock-level U-values.
- **TEP Energy renovation rate estimates**: National average ~1.1%/yr
  (2016–2020 period). This is a useful headline number but not a yearly series
  we can feed into LMDI.
- **SIA 380/1 (2007 revision)**: Standardized the thermal energy calculation
  method and introduced the Energiebezugsfläche (EBF) definition. Important
  milestone, but the definition change creates a data discontinuity.
- **MuKEn 2014 / MuKEn 2025**: Cantonal energy codes — useful for the policy
  narrative but don't provide annual stock-level insulation data.

### Why we chose NOT to add it as a formal LMDI factor
1. **No annual time series.** The GEAK database gives snapshots, not a
   continuous yearly variable. You can't do LMDI without a consistent annual
   series for each factor.
2. **EBF definition trap.** You warned us about this — the Energiebezugsfläche
   definition changed with SIA 380/1 (2007). Pre-2007 and post-2007 floor area
   numbers aren't directly comparable. If we tried to construct a U-value index
   using EBF-normalized data, we'd have a structural break in the middle of the
   time series.
3. **Already captured implicitly.** The intensity factor (E / floor area) in our
   4-factor LMDI already absorbs envelope improvements alongside system
   efficiency and behavioral changes. Adding a separate insulation factor would
   create multicollinearity — we'd be double-counting.

### What we DID instead
Rather than forcing a methodologically shaky 5th factor, we added a qualitative
narrative section after fig11 (intensity attribution) that includes:
- Literature-backed U-value table by construction vintage (pre-1970 through
  Minergie-P), sourced from GEAK/CECB data
- Renovation rate context: 1.1%/yr actual vs 2.0–2.5%/yr needed for 2050
  net-zero (BFE Energieperspektiven 2050+)
- Regulatory timeline: SIA 380/1 (2007) → MuKEn 2014 → MuKEn 2025
- Explicit justification for why insulation isn't a separate LMDI factor

We also added SIA 380/1 (2007) as a policy annotation on the decoupling chart
(fig5), alongside the existing CO₂ levy / Gebäudeprogramm / MuKEn markers.

### Assumptions we're making (for discussion)
- The ~45%/35%/20% split of the intensity effect (envelope / fuel switching /
  other) is based on literature estimates (Kämpf et al. 2018, TEP Energy
  synthesis), not directly measured. We present it as "indicative" in the chart.
- The 1.1%/yr renovation rate is the TEP Energy national estimate (2016–2020
  average). Actual rates vary significantly by canton (Zurich and Basel-Stadt
  are higher) and building type (EFH vs MFH).
- We assume the intensity factor in our LMDI fully absorbs envelope
  improvements. This is standard practice in energy decomposition literature
  (Ang 2015, Xu & Ang 2013) but means envelope and system efficiency gains
  are conflated in a single term.

---

## Visual Polish (this week)

A few presentation improvements that aren't big enough for their own section:
- **fig5 (decoupling)**: Decluttered — rotated policy labels to -35° and moved
  them to paper coordinates so they don't overlap data lines. Added SIA 380/1
  (2007) annotation.
- **fig13/fig14 (tornado + cost)**: Fixed y-axis clipping where long labels were
  getting cut off. Added margin padding.
- **fig7 (buildings by heating source)**: Improved color scheme — 2000 bars now
  use a muted opacity (0.5) of the same hues as 2024 bars, so the before/after
  comparison is visually cleaner.
- All figures now export at consistent 1200×700px with matching font sizes.
