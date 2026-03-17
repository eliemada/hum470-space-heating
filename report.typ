// =============================================================================
// HUM-470 — Final Report
// Economic Growth and Sustainability II
// =============================================================================
// Compile:  typst compile report.typ
// Watch:    typst watch report.typ
// =============================================================================

#import "template.typ": *

#show: report.with(
  title: [Energy Demand for Space Heating\ in Swiss Residential Buildings],
  subtitle: [A Decomposition Analysis],
  group-number: "12",
  impact: "Final energy demand for space heating in Swiss residential buildings",
  authors: (
    (name: "Marc Bischof", sciper: "SCIPER: 395360"),
    (name: "Elie Bruno", sciper: "SCIPER: 355932"),
    (name: "Xavier Magbi", sciper: "SCIPER: 340062"),
    (name: "Andrea Trugenberger", sciper: "SCIPER: 357615"),
  ),
  date: "14 May 2026",
  abstract: [
    // TODO: Write final abstract once analysis is complete.
    // Guidelines: ~150 words summarising context, method, key results, and
    // policy implications.
    This report presents a decomposition analysis of the final energy demand
    for space heating in Swiss residential buildings over the period 2000--2023.
    Using a Kaya-type identity adapted to the building sector, we decompose
    total heating energy into population, dwelling density, floor area,
    heating-system mix, and energy-intensity factors.
    // TODO: Add key results summary here.
  ],
  keywords: (
    "decomposition analysis",
    "space heating",
    "residential buildings",
    "Switzerland",
    "Kaya identity",
    "decoupling",
    "energy efficiency",
  ),
)

// =============================================================================
// 1. INTRODUCTION
// =============================================================================

= Introduction <intro>

// Context: why space heating energy matters for growth & sustainability
// Time-series of this impact compared to total energy or GDP

Space heating is the single largest end use of energy in Swiss households,
accounting for approximately XX% of total residential energy consumption in
2023 @bfe2024. Despite decades of efficiency improvements in building
envelopes and heating systems, the residential sector remains a major
contributor to Switzerland's final energy demand and associated CO#sub[2]
emissions @ipcc2023.

Understanding how heating energy demand has evolved --- and which factors have
driven that evolution --- is essential for designing policies that reconcile
continued economic development with Switzerland's 2050 net-zero commitments
@jackson2017.

// TODO: Add time-series figure
// #figure(
//   image("figures/heating-timeseries.svg", width: 85%),
//   caption: [Final energy demand for space heating in Swiss residential
//   buildings vs.\ total final energy consumption, 2000--2023.],
// ) <fig:timeseries>

This report proceeds as follows. @background reviews the theoretical
background and existing studies. @framework introduces the key concepts and
our decomposition framework. @drivers identifies the possible main drivers.
@data describes data sources and methodology. @results presents the
quantitative decomposition results. @regulation discusses the regulatory
framework. @scenarios explores future scenarios and policy recommendations.
@conclusion concludes.


// =============================================================================
// 2. BACKGROUND AND EXISTING STUDIES
// =============================================================================

= Background and Existing Studies <background>

// Theoretical foundations and what other studies have found
// What could lead to diverging evolutions of heating energy vs. GDP

== Theoretical Framework

The relationship between economic growth and environmental pressure has been
studied through three complementary lenses: the IPAT identity @ehrlich1971,
the Kaya identity @kaya1990, and index decomposition analysis (IDA)
@ang2004.

The IPAT framework expresses environmental impact $I$ as:

$ I = P times A times T $

where $P$ is population, $A$ is affluence (GDP per capita), and $T$ is
technology (impact per unit of GDP). This multiplicative structure allows one
to assess whether improvements in $T$ have been sufficient to offset growth
in $P$ and $A$ --- i.e., whether _decoupling_ has occurred.

#definition[Decoupling][
  A divergence between the growth rates of an environmental pressure (e.g.,
  energy demand) and an economic driver (e.g., GDP). _Relative decoupling_
  occurs when the pressure grows more slowly than GDP. _Absolute decoupling_
  occurs when the pressure decreases while GDP grows.
]

== The Environmental Kuznets Curve Hypothesis

The Environmental Kuznets Curve (EKC) posits that environmental degradation
first rises and then falls as per-capita income increases, forming an
inverted-U shape. While evidence for the EKC is mixed across pollutants
and countries, the Swiss residential heating sector offers a potential case
study: rising affluence may drive larger dwellings and higher comfort
expectations, yet also enables investment in insulation and modern heating
technologies.

// TODO: Discuss EKC evidence specific to heating/buildings

== Existing Studies on Building Energy

// TODO: Review studies on decomposition of residential heating energy
// Key references to look for:
// - IEA studies on building energy efficiency
// - Swiss-specific studies (Prognos, SFOE analyses)
// - European building energy decomposition studies

@xu2014 provide a comprehensive review of index decomposition analysis applied
to CO#sub[2] emission studies, including applications to the building sector.
@ang2015 recommend the Logarithmic Mean Divisia Index (LMDI) approach for
its theoretical consistency and perfect decomposition properties.

// TODO: Add more topic-specific literature


// =============================================================================
// 3. KEY CONCEPTS AND DECOMPOSITION FRAMEWORK
// =============================================================================

= Key Concepts and Decomposition Framework <framework>

// Define key concepts, present adapted Kaya identity

== Key Definitions

#definition[Final energy demand for space heating][
  The total energy consumed by residential buildings for the purpose of space
  heating, measured at the point of final use. This includes fossil fuels
  (heating oil, natural gas), electricity (heat pumps, direct electric
  heating), biomass (wood, pellets), and district heating, but excludes
  transformation and distribution losses upstream.
]

#definition[Heating degree days (HDD)][
  A weather-based index measuring the cumulative difference between a base
  temperature (typically 20 °C in Switzerland) and the daily mean outdoor
  temperature over the heating season. Higher HDD values indicate colder
  winters and greater heating demand.
]

== Adapted Kaya Identity

We adapt the Kaya identity to decompose total residential heating energy
demand $E_"heat"$ as follows:

#decomposition[
  $ E_"heat" = underbrace(P, "Population") times underbrace(D / P, "Dwelling\ndensity") times underbrace(A / D, "Floor area\nper dwelling") times underbrace(sum_s (S_s times e_s), "Heating system\nmix × intensity") $
]

where:
- $P$ = total resident population
- $D slash P$ = number of dwellings per capita (dwelling density)
- $A slash D$ = average heated floor area per dwelling (m#super[2])
- $S_s$ = share of heating energy source $s$ (oil, gas, heat pump, wood,
  district heating, electric)
- $e_s$ = specific energy consumption per m#super[2] of heated floor area
  for source $s$ (MJ/m#super[2])

// NOTE: You may also wish to include a climate-correction factor (HDD)
// as an additional multiplicative term:
// E_heat = P × (D/P) × (A/D) × (HDD/HDD_ref) × Σ(S_s × e_s)

== Mapping to the IPAT Framework

#figure(
  table(
    columns: (auto, auto, 1fr),
    align: (center, center, left),
    table.header(
      [*Factor*], [*IPAT category*], [*Interpretation*],
    ),
    table.hline(stroke: 0.8pt),
    [$P$], [Population], [Demographic scale],
    [$D slash P$], [Affluence / Structure], [Household formation, urbanisation],
    [$A slash D$], [Affluence], [Living-space standards, comfort expectations],
    [$S_s$], [Technology / Structure], [Heating-system mix (fuel switching)],
    [$e_s$], [Technology], [Building-envelope quality, system efficiency],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Mapping of decomposition factors to the IPAT framework.],
) <tab:ipat-mapping>


// =============================================================================
// 4. POSSIBLE MAIN DRIVERS
// =============================================================================

= Possible Main Drivers <drivers>

// Identify and discuss factors that could drive heating energy demand

Based on the decomposition framework and literature, we identify the following
potential drivers of residential heating energy demand in Switzerland:

#figure(
  table(
    columns: (auto, 1fr, auto),
    align: (left, left, center),
    table.header(
      [*Driver*], [*Mechanism*], [*Expected effect*],
    ),
    table.hline(stroke: 0.8pt),
    [Population growth ($P$)],
    [More residents require more heated dwellings],
    [$+$],

    [Dwelling density ($D slash P$)],
    [Trend towards smaller households increases dwellings per capita],
    [$+$],

    [Floor area per dwelling ($A slash D$)],
    [Rising affluence drives demand for larger living spaces],
    [$+$],

    [Heating-system mix ($S_s$)],
    [Shift from oil/gas to heat pumps reduces final energy per m#super[2]],
    [$-$],

    [Building-envelope quality],
    [Insulation retrofits and new building standards (MuKEn) reduce heat losses],
    [$-$],

    [Climate (HDD)],
    [Warmer winters reduce heating demand; cold spells increase it],
    [$+/-$],

    [Occupant behaviour],
    [Thermostat settings, ventilation habits, rebound effects],
    [$+/-$],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Summary of potential drivers and their expected directional effect
  on residential heating energy demand.],
) <tab:drivers>


// =============================================================================
// 5. DATA SOURCES AND METHODOLOGY
// =============================================================================

= Data Sources and Methodology <data>

== Data Sources

#datasource("Swiss Federal Office of Energy (SFOE / BFE)")[
  Overall energy statistics (_Schweizerische Gesamtenergiestatistik_):
  final energy consumption by sector and energy carrier, including
  residential heating. Annual reports 2000--2023 @bfe2024.
]

#datasource("Swiss Federal Statistical Office (FSO / BFS)")[
  Population, number of dwellings, average dwelling size (m#super[2]),
  building and dwelling register (GWR). @bfs2024.
]

#datasource(
  "MeteoSwiss",
  url: "https://www.meteoswiss.admin.ch",
)[
  Heating degree days (HDD) for Swiss reference stations. Used for
  climate correction of energy demand.
]

#datasource(
  "International Energy Agency (IEA)",
  url: "https://www.iea.org/data-and-statistics",
)[
  Cross-country energy balances and building-sector efficiency indicators
  for international benchmarking @iea2024.
]

#datasource(
  "World Bank — World Development Indicators",
  url: "https://databank.worldbank.org",
)[
  GDP (constant 2017 PPP USD), population for macroeconomic context
  @worldbank2024.
]

== Methodology

// TODO: Describe the decomposition method used (e.g., LMDI-I additive
// or multiplicative), time period, data processing steps.

== Data Quality and Limitations

// TODO: Discuss gaps, proxy variables, breaks in time series,
// definitional changes in the GWR, HDD measurement consistency, etc.


// =============================================================================
// 6. DECOMPOSITION RESULTS
// =============================================================================

= Decomposition Results <results>

// Quantitative contribution of each driver
// Graphic representations (waterfall, stacked bar, time series)

== Evolution of Key Indicators

// TODO: Present time-series plots of:
// - Total heating energy demand
// - Population, dwelling count, average floor area
// - Heating-system shares (oil, gas, heat pump, wood, district heating)
// - Specific energy consumption per m²
// - Heating degree days

== Quantitative Decomposition

// TODO: Insert decomposition results table and waterfall chart
// #figure(
//   image("figures/waterfall.svg", width: 90%),
//   caption: [Contribution of each factor to the change in residential
//   heating energy demand, Switzerland 2000--2023.],
// ) <fig:waterfall>

== Decoupling Assessment

// TODO: Assess whether absolute or relative decoupling has occurred
// between heating energy demand and GDP (or population).
// Compare with total energy and other sectors.

== Discussion

// TODO: Interpret results in light of the theoretical framework.
// Which factors dominated? Were there structural breaks?
// How does Switzerland compare internationally?


// =============================================================================
// 7. REGULATORY FRAMEWORK
// =============================================================================

= Regulatory Framework <regulation>

// Policies that regulate the activity
// How they explain the decomposition results
// Government goals and instruments

== Swiss Building Energy Policies

// TODO: Discuss relevant policies, including:
// - MuKEn (Mustervorschriften der Kantone im Energiebereich) — cantonal
//   model energy regulations for buildings
// - Swiss CO2 Act (CO2-Gesetz) — carbon tax on heating fuels
// - The Building Programme (Gebäudeprogramm) — federal-cantonal subsidy
//   programme for energy-efficient retrofits
// - Energy Strategy 2050 — long-term targets
// - Cantonal building standards and enforcement
// - SIA norms (e.g., SIA 380/1 for heating energy demand)

== Policy Impact on Decomposition Factors

// TODO: Link specific policies to factors in the decomposition.
// e.g.:
// - MuKEn → reduces e_s for new buildings
// - Building Programme → accelerates retrofit rate, reduces e_s
// - CO2 tax → incentivises fuel switching (S_s shift from oil to HP)
// - No direct policy on A/D (floor area per dwelling keeps growing)


// =============================================================================
// 8. SCENARIOS AND RECOMMENDATIONS
// =============================================================================

= Scenarios and Recommendations <scenarios>

== Future Scenarios

// TODO: Project future heating energy demand under different assumptions
// about population growth, renovation rates, heat pump adoption,
// climate warming (lower HDD), and floor-area trends.

== Policy Recommendations

Based on our decomposition analysis and review of the regulatory framework, we
propose the following recommendations:

// TODO: Develop each recommendation with evidence from the analysis.
// Suggested structure for each:
// 1. What the recommendation is
// 2. Which decomposition factor it targets
// 3. Expected quantitative impact
// 4. Implementation considerations

+ *Accelerate building-envelope retrofits.* ...
+ *Promote heat-pump adoption through targeted subsidies.* ...
+ *Introduce floor-area efficiency incentives.* ...
+ *Strengthen cantonal enforcement of MuKEn.* ...
+ *Set binding sectoral energy-reduction targets.* ...


// =============================================================================
// 9. CONCLUSION
// =============================================================================

= Conclusion <conclusion>

// Summary, general lessons, limitations

This report presented a decomposition analysis of final energy demand for
space heating in Swiss residential buildings over the period 2000--2023.

== Main Findings

// TODO: Summarise key quantitative results. Example structure:
// - Overall change in heating energy demand
// - Dominant upward drivers (population, floor area)
// - Dominant downward drivers (efficiency, fuel switching)
// - Net effect and decoupling assessment

== General Lessons

// TODO: What can be learned that is of general interest beyond
// the Swiss case? Connections to broader growth-vs-sustainability debate.

== Limitations and Extensions

// TODO: Discuss limitations of:
// - Data availability and quality
// - Decomposition methodology (residuals, aggregation level)
// - Scope (only space heating, not hot water or cooling)
// Possible extensions:
// - Cantonal-level decomposition
// - Inclusion of embodied energy in building materials
// - Comparison with other Alpine countries


// =============================================================================
// BIBLIOGRAPHY — ISO-690 Author-Date
// =============================================================================

#pagebreak()

#bibliography(
  "references.bib",
  title: [References],
  style: "iso-690-author-date",
)


// =============================================================================
// APPENDIX (optional)
// =============================================================================

// #pagebreak()
// #heading(numbering: none)[Appendix]
//
// == A.1 Detailed Data Tables
// == A.2 Decomposition Calculations
// == A.3 Sensitivity Analysis
