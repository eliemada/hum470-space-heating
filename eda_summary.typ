// =============================================================================
// HUM-470 - EDA Progress Summary (Week 1)
// Lightweight findings document for supervisor feedback
// Compile: typst compile eda_summary.typ
// =============================================================================

#import "template.typ": *

#show: report.with(
  title: [Exploratory Data Analysis\ Progress Summary],
  subtitle: [Week 1: Data Pipeline & Key Findings],
  group-number: "12",
  impact: "Final energy demand for space heating in Swiss residential buildings",
  authors: (
    (name: "Marc Bischof", sciper: "SCIPER: 395360"),
    (name: "Elie Bruno", sciper: "SCIPER: 355932"),
    (name: "Xavier Magbi", sciper: "SCIPER: 340062"),
    (name: "Andrea Trugenberger", sciper: "SCIPER: 357615"),
  ),
  date: "16 March 2026",
  abstract: [
    This document summarises one week of exploratory data analysis for our
    IPAT decomposition of Swiss residential space-heating energy. All data
    is sourced from official Swiss statistics (BFE, BFS) and international
    databases (World Bank), with a fully reproducible pipeline. We present
    key findings across the three IPAT factors, a 3-factor LMDI
    decomposition, and preliminary Monte Carlo scenario projections.
  ],
  keywords: (
    "EDA",
    "IPAT",
    "LMDI",
    "space heating",
    "Switzerland",
  ),
)

// =============================================================================
// 1. DATA PIPELINE
// =============================================================================

= Data Sources & Pipeline <data>

All datasets are downloaded and cached automatically via the analysis notebook
(Marimo/Python). The pipeline is fully reproducible: running the notebook
fetches all data from official APIs and produces every figure in this document.

#figure(
  table(
    columns: (auto, 1fr, auto),
    align: (left, left, center),
    table.header([*Dataset*], [*Source*], [*Period*]),
    [Energy balance (TJ)], [BFE Gesamtenergiestatistik, opendata.swiss], [1980--2024],
    [Space-heating share], [BFE/Prognos _Ex-Post-Analyse_, Tabelle 1], [2000--2024],
    [Heating mix (EBF m²)], [BFE/Prognos Tabelle 13], [2000--2024],
    [Heating degree days], [BFE ogd105 (1994+) + Zurich Fluntern (1980--93)], [1980--2025],
    [Population], [BFS STATPOP (2010+) + World Bank (2000--09)], [2000--2024],
    [Floor area / person], [BFS GWS T 09.03.02.04.03], [2012--2024],
    [Buildings by heating], [BFS Census (1990, 2000) + GWR (2021)], [1990--2021],
    [GDP (constant CHF)], [World Bank NY.GDP.MKTP.KN], [2000--2024],
  ),
  caption: [Data sources used in the analysis. All verified and cached locally.],
) <tab:data>

Population data was cross-validated between BFS STATPOP and World Bank
(maximum divergence: 0.82%), confirming the gap-fill for 2000--2009 is reliable.


// =============================================================================
// 2. IPAT FACTORS
// =============================================================================

= IPAT Factor Overview <ipat>

== Impact (I): Household Energy by Carrier

#figure(
  image("figures/fig1_energy_by_carrier.svg", width: 92%),
  caption: [Swiss household final energy consumption by carrier, 1980--2024.
  Petroleum products dominated historically but have been overtaken by
  electricity (partly due to heat pump adoption).],
) <fig:carrier>

Total household energy peaked around 2010 and shows a clear downward trend
since ($approx -10%$ vs 2000). Space heating accounts for 65--71% of
household energy (declining share, from BFE/Prognos correction).


== Population (P): Steady Growth

#figure(
  image("figures/fig3_population.svg", width: 80%),
  caption: [Swiss population, 2000--2024. Growth of +26% driven primarily
  by net immigration.],
) <fig:pop>

Population grew from 7.2M to 9.0M (+26%), exerting continuous
upward pressure on total heating demand.


== Weather: Heating Degree Days

#figure(
  image("figures/fig2_hdd_trend.svg", width: 85%),
  caption: [Heating degree days (base 20/12°C). The declining trend
  ($approx -156$ HDD/decade) reflects Switzerland warming at $approx 2.9$°C
  above pre-industrial, roughly double the global average.],
) <fig:hdd>

Warmer winters provide a "free" reduction in heating demand that is
independent of policy or technology. The LMDI decomposition separates this
weather effect from structural improvements.


== Heating Mix Transition

#figure(
  image("figures/fig4_heating_mix.svg", width: 92%),
  caption: [Floor area share by heating system (BFE/Prognos Tabelle 13).
  Oil halved from 60% to 24%; heat pumps now lead at 29% by floor area.],
) <fig:mix>

#insight[
  Heat pumps lead by floor area (29%) but not by building count ($approx$23%).
  The difference reflects their dominance in new large multi-family
  construction. Oil remains \#1 by building count (35%).
]


// =============================================================================
// 3. DECOUPLING
// =============================================================================

= Decoupling Analysis <decoupling>

#figure(
  image("figures/fig5_decoupling.svg", width: 92%),
  caption: [All series indexed to 2000 = 100. Space-heating energy (blue)
  falls while GDP, population, and floor area rise, confirming absolute decoupling.
  Inflection point around 2005--2008.],
) <fig:decoupling>

#figure(
  table(
    columns: (auto, auto, auto),
    align: (left, center, left),
    table.header([*Indicator*], [*Change*], [*Driver*]),
    [GDP (real)], [+53%], [Services, pharma output],
    [Population], [+26%], [Net immigration],
    [Heated floor area], [+36%], [Affluence, smaller households],
    [Space-heating energy], [*--17%*], [Absolute decoupling],
    [Energy intensity (kWh/m²)], [*--39%*], [Insulation + heat pumps + HDD],
  ),
  caption: [Summary of IPAT factor trends since 2000.],
) <tab:decoupling>

#insight[
  Absolute decoupling confirmed: the Technology factor (T) is declining fast
  enough to more than offset growth in Population (P) and Affluence (A). The
  inflection point around 2005--2008 coincides with the CO#sub[2] levy
  introduction (2008) and the Gebäudeprogramm launch (2010).
]


// =============================================================================
// 4. LMDI DECOMPOSITION
// =============================================================================

= LMDI Decomposition <lmdi>

We decompose space-heating energy into three factors using the additive LMDI-I
method (Ang, 2004):

#decomposition[
  $ E_"total" = P times frac(E, P dot "HDD") times "HDD" $
]

- *Population effect* ($Delta E_"pop"$): more people $arrow$ more heating demand
- *Weather effect* ($Delta E_"weather"$): warmer winters $arrow$ less demand
- *Intensity effect* ($Delta E_"int"$): technology, insulation, behaviour

The decomposition is exact: $Delta E_"pop" + Delta E_"int" + Delta E_"weather" = E^T - E^0$ (no residual).

#figure(
  image("figures/fig8_lmdi_waterfall.svg", width: 85%),
  caption: [LMDI-I waterfall: cumulative contribution of each factor to
  the change in space-heating energy, 2000 to 2024.],
) <fig:waterfall>

#figure(
  table(
    columns: (auto, auto, auto, auto),
    align: (left, right, center, center),
    table.header([*Factor*], [*Cumulative $Delta$E (TJ)*], [*Direction*], [*Share*]),
    [Population], [+37,559], [Up], [36%],
    [Weather (HDD)], [--11,160], [Down], [11%],
    [Intensity (tech.)], [*--54,469*], [*Down*], [*53%*],
    [Net Change], [*--28,070*], [*Down*], [--],
  ),
  caption: [LMDI summary, 2000--2024.],
) <tab:lmdi>

#insight[
  The intensity effect alone ($-54,469$ TJ) is large enough to offset *both*
  population growth ($+37,559$ TJ) *and* would still yield a net decline
  even without the weather bonus ($-11,160$ TJ). Technology and policy,
  not just climate luck, are driving absolute decoupling.
]


// =============================================================================
// 5. SCENARIOS & COST
// =============================================================================

= Preliminary Scenario Analysis <scenarios>

== Monte Carlo Projections (2024--2050)

Three named scenarios (BAU, Accelerated, Ambitious) with 1,000 Monte Carlo
iterations varying population, HDD decline, and renovation rate.

#figure(
  image("figures/fig12_scenario_fan.svg", width: 90%),
  caption: [Projected space-heating energy under three renovation-rate
  scenarios with Monte Carlo uncertainty bands.],
) <fig:scenarios>

#figure(
  image("figures/fig13_scenario_tornado.svg", width: 85%),
  caption: [Sensitivity of 2050 energy demand to parameter changes.
  Renovation rate is the dominant lever ($plus.minus$11,500 TJ).],
) <fig:tornado>


== Heating System Economics

#figure(
  image("figures/fig14_cost_comparison.svg", width: 85%),
  caption: [Annual heating cost (fuel + CO#sub[2] levy) for a 150 m²
  unrenovated house. Heat pumps reach near-parity with fossil systems
  at current levy (CHF 120/t); at higher rates they are clearly cheaper.],
) <fig:cost>


// =============================================================================
// 6. NEXT STEPS
// =============================================================================

= Open Questions & Next Steps <next>

== Questions for Supervisor

+ *Decomposition depth:* Is the 3-factor LMDI (P $times$ HDD $times$ Intensity) sufficient, or should we add a 4th factor (e.g. floor area per capita explicitly)?

+ *Monte Carlo calibration:* Should we calibrate assumptions against the SFOE Energieperspektiven 2050+ scenarios?

+ *Report drafting priority:* Ready to start sections 4 (Data & Trends) and 5 (Policy & Efficiency Drivers). Does the current scope look right?

== Planned Work

- Finalise figures 10--14 (HDD-normalised, intensity attribution, Monte Carlo, cost)
- Draft section 6: Decomposition Results ($approx$6 pages)
- Draft section 7: Regulatory Framework ($approx$3.5 pages)
- Interim presentation preparation
