// =============================================================================
// HUM-470 — Final Report
// Economic Growth and Sustainability II
// =============================================================================
// Compile:  typst compile report.typ
// Watch:    typst watch report.typ
// =============================================================================

#import "template.typ": *
#import "figures/fig_methodology_flowchart.typ": methodology-flowchart

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
    This report presents a four-factor LMDI-I decomposition of final energy
    demand for space heating in Swiss residential buildings over 2000--2024.
    We decompose total heating energy into population, floor area per capita,
    climate (heating degree days), and energy intensity. Despite population
    growth (+25%) and expanding per-capita floor area (+38%), space-heating
    energy declined by 17% --- confirming absolute decoupling from GDP (+51%).
    The intensity factor ($-67 "," 366$ TJ) dominates, driven by
    fuel switching from oil to heat pumps (~51% of the intensity effect),
    building envelope improvements (~33%), and behavioural changes (~16%). However, improvement is decelerating: the
    annual intensity gain has moderated from $-3 "," 200$ TJ/yr in the 2000s
    to $-2 "," 500$ TJ/yr in the 2010s. Analysis of GWR building-register
    data shows a four-speed heat-pump transition across building types (EFH:
    28% of buildings with HP as primary heating, MFH: 20%) and a 34-percentage-point spread across cantons. We identify
    the absence of policy targeting per-capita floor area as a structural blind
    spot and recommend doubling the renovation rate from 1.1% to 2%/yr,
    unlocking MFH heat-pump adoption, and introducing cantonal convergence
    incentives.
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

== Global Context: Buildings and Climate Change

Buildings consume 30% of global final energy and produce 27% of
energy-related CO#sub[2] emissions @lucon2014. In cold and temperate
climates, space heating alone accounts for over half of building energy
demand @iea2024buildings. National net-zero pledges, the Paris
Agreement's 1.5°C pathway, and the EU's Fit-for-55 package all
require steep reductions in heating energy.

Buildings also turn over far more slowly than other capital stock.
Vehicles last 12--15 years; industrial equipment, 15--20. Residential
buildings persist for 50--100+ years @meadows2004. A building
constructed today will still stand in 2080; one built in 1970 will
likely survive to 2050. Investment decisions made decades ago continue
to shape today's energy consumption, and today's decisions will lock
in demand well beyond 2050 @lucon2014 @ipcc2023. The window for
transforming the stock is narrowing.

== The Swiss Case: Scale and Significance

Space heating is the single largest end use of energy in Swiss
households, accounting for 65% of total residential energy consumption
in 2024 @prognos2024. In absolute terms, the Swiss residential
building stock consumed approximately 137,000 TJ for space heating in
2024 --- equivalent to 38 TWh of final energy, or roughly 20% of
Switzerland's total final energy demand @bfe2024. Despite decades of
efficiency improvements in building envelopes and heating systems, the
residential sector remains a major contributor to Switzerland's final
energy demand and associated CO#sub[2] emissions @ipcc2023.

Switzerland's building stock comprises approximately 1.8 million
residential buildings, of which 57% are single-family homes (EFH) and
37% multi-family buildings (MFH) @bfs2024. The stock is aging: over
60% of residential buildings were constructed before 1980, when modern
insulation standards did not yet apply. These pre-1980 buildings
account for a disproportionate share of heating energy demand due to
their poor thermal envelopes (typical U-values of 0.8--1.0
W/(m#super[2]K) versus 0.15--0.25 W/(m#super[2]K) for post-2000
construction) @kaempf2018.

Understanding how heating energy demand has evolved, and which factors
have driven that evolution, is essential for designing policies that
reconcile continued economic development with Switzerland's 2050
net-zero commitments @jackson2017.

== Why Switzerland? A Natural Experiment

Switzerland's population grew by 25% since 2000, driven by EU/EFTA
free-movement immigration. Germany grew 3% over the same period;
Italy shrank. This immigration-driven expansion generates sustained
pressure on housing demand that most European countries do not face,
requiring new construction while increasing occupancy in the existing
stock.

The federal structure delegates building regulation to 26 cantons,
each setting its own codes, subsidy levels, and enforcement practices.
Heat-pump adoption rates range from 7% to 42% across cantons. This
variation enables quasi-experimental assessment of policy instruments
that a unitary state could not offer.

Switzerland's GDP per capita exceeds CHF 80,000 in constant terms.
Does affluence enable or hinder the energy transition? The
Environmental Kuznets Curve hypothesis @grossman1995 predicts an
inverted-U relationship. If absolute decoupling is achievable anywhere,
the conditions are met here: wealth, institutional capacity, and
ambitious targets all present. If Switzerland still falls short, the
barriers are structural and relevant to other affluent nations.

== Research Gap and Contribution

Despite extensive monitoring by BFE @bfe2024 and Prognos @prognos2024,
no published study applies a formal LMDI decomposition to Swiss
residential space-heating energy demand. Existing studies either
monitor aggregate trends without formal decomposition, or apply
decomposition methods to the entire Swiss economy without isolating the
residential heating sub-sector. This report fills that gap by
decomposing 2000--2024 demand into four factors (population, floor
area per capita, climate, and energy intensity), quantifying their
relative contributions, and identifying the policy levers most likely
to sustain the observed decoupling trajectory.

Our central research question is: *Has the improvement in energy
intensity been sufficient to achieve absolute decoupling of residential
heating energy from economic growth, and can this trajectory be
sustained under projected demographic and climate trends?*

== Report Structure

This report proceeds as follows. @background reviews the theoretical
background and existing studies. @framework introduces the key concepts
and our decomposition framework. @drivers identifies the possible main
drivers. @data describes data sources and methodology. @results
presents the quantitative decomposition results. @regulation discusses
the regulatory framework. @scenarios explores future scenarios and
policy recommendations. @conclusion concludes.


// =============================================================================
// 2. BACKGROUND AND EXISTING STUDIES
// =============================================================================

= Background and Existing Studies <background>

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
in $P$ and $A$, i.e., whether _decoupling_ has occurred.

#definition[Decoupling][
  A divergence between the growth rates of an environmental pressure (e.g.,
  energy demand) and an economic driver (e.g., GDP). _Relative decoupling_
  occurs when the pressure grows more slowly than GDP. _Absolute decoupling_
  occurs when the pressure decreases while GDP grows.
]

The Kaya identity @kaya1990 decomposes emissions into population, GDP per
capita, energy intensity, and carbon intensity. Its multiplicative logic
extends to sector-specific analyses: in the building sector, the drivers
shift to population, dwelling characteristics, climate exposure, and
heating-system performance @lucon2014. This adaptation is fruitful because
buildings have long asset lifetimes (median >40 years in Switzerland
@bfs2024), creating path dependencies where efficiency improvements in new
and renovated buildings take decades to permeate the stock @meadows2004.

== The Environmental Kuznets Curve Hypothesis

The Environmental Kuznets Curve (EKC) posits that environmental degradation
first rises and then falls as per-capita income increases, forming an
inverted-U shape. @grossman1995 first documented this relationship for
local pollutants, finding turning points at relatively modest income levels.
However, subsequent reviews show that the evidence is considerably weaker for
energy consumption and CO#sub[2] emissions, which are more tightly coupled to
economic activity than local pollutants @stern2004. For residential heating
specifically, two competing channels operate: rising affluence drives
expansion of per-capita living space, while higher incomes also enable
investment in superior insulation and high-efficiency heating systems.

Switzerland, with a GDP per capita exceeding CHF 80,000 (constant terms),
appears to be past the turning point for heating energy: since 2000, total
residential space-heating energy has declined by 17% despite a 51% increase
in real GDP. This observation is consistent with the EKC hypothesis, though
it is more precisely described as absolute decoupling driven by targeted
policy interventions (building codes, CO#sub[2] levies, subsidies for
retrofits) rather than by income growth alone @jackson2017. Where EKC-like
patterns are observed for energy, they typically reflect deliberate policy
choices rather than an automatic consequence of development @stern2004.

== Existing Studies on Building Energy

=== Global assessments

The IPCC AR5 Chapter 9 concludes that buildings account for
one-third of global final energy and that long asset lifetimes create
lock-in effects requiring near-term action @lucon2014. @urgevorsatz2015
find that space heating remains the dominant end use in cold climates
but is declining where active building-efficiency policies exist ---
through tighter codes, retrofit programmes, and the transition to heat
pumps. The IEA @iea2024buildings reports global building energy intensity
improving at ~1.5%/yr in energy intensity per unit of floor area, largely offset by floor-area growth.

=== Decomposition methodology

Among IDA methods, the Logarithmic Mean Divisia Index (LMDI-I) has
emerged as the preferred approach. @ang2004 demonstrates that LMDI
satisfies perfect decomposition (zero residual), time-reversal and
factor-reversal symmetry, and robustness to zero values. @xu2014 survey
over 80 IDA studies, noting that the building sector remains
under-represented. At the European level, @odyssee2023 and @reuter2020
find that intensity improvements are the dominant driver of residential
energy savings, consistent with the Swiss pattern. We adopt LMDI-I in
additive form for this study.

=== Swiss-specific studies

BFE/Prognos @prognos2024 provide the most detailed breakdown of Swiss
residential heating energy by carrier, building type, and heating system.
@kaempf2018 document the generational divide in U-values: pre-1970
buildings at 0.8--1.0 W/(m#super[2]K) vs.\ post-2000 at
0.15--0.25 W/(m#super[2]K). TEP Energy @tep2023 estimates the annual
renovation rate at 1.1%, well below the 2%/yr target for the 2050
net-zero pathway. The _Energieperspektiven 2050+_ @ep2050plus scenarios
provide the benchmark against which our forward-looking analysis in
@scenarios is calibrated. To our knowledge, no published study applies the LMDI-I method specifically to Swiss residential space-heating energy. Our work fills this gap.


// =============================================================================
// 3. KEY CONCEPTS AND DECOMPOSITION FRAMEWORK
// =============================================================================

= Key Concepts and Decomposition Framework <framework>

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
demand $E$ into four multiplicative factors:

#decomposition[
  $ E = underbrace(P, "Population") times underbrace(A / P, "Floor area\nper capita") times underbrace(H, "HDD") times underbrace(I, "Intensity") $
]

where $P$ is the resident population, $A slash P$ is heated floor area per
capita, $H$ denotes heating degree days, and $I = E slash (A times H)$ is
energy intensity per m#super[2] per HDD. This formulation uses only data
reliably available at annual frequency. The intensity factor $I$ captures
_all_ efficiency-related mechanisms --- building-envelope quality,
heating-system performance (including fuel switching), and behavioural
patterns --- in a single term. While this aggregation sacrifices the
ability to separate envelope from fuel-switching effects, it avoids
introducing poorly measured variables. The indicative sub-decomposition
in @sec:intensity provides the complementary disaggregation using
engineering estimates.

== Mapping to the IPAT Framework

#figure(
  table(
    columns: (auto, auto, 1fr),
    align: (center, center, left),
    table.header(
      [*Factor*], [*IPAT category*], [*Interpretation*],
    ),
    table.hline(stroke: 0.8pt),
    [$P$], [Population], [Demographic scale --- immigration-driven growth],
    [$A slash P$], [Affluence], [Per-capita floor area --- living-space standards],
    [$H$], [--- (Climate)], [Heating degree days --- exogenous weather exposure],
    [$I = E slash (A times H)$], [Technology], [Energy intensity --- envelope quality, system efficiency, behaviour],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Mapping of decomposition factors to the IPAT framework.],
) <tab:ipat-mapping>

Note that the theoretical 6-factor decomposition (population $times$ dwellings/capita $times$ area/dwelling $times$ system shares $times$ system efficiencies) is collapsed into four observable factors to match available annual data. The intensity factor $I$ implicitly captures both heating-system mix and building-envelope quality.


// =============================================================================
// 4. POSSIBLE MAIN DRIVERS
// =============================================================================

= Possible Main Drivers <drivers>

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

In our four-factor LMDI, dwelling density ($D slash P$) and floor area per dwelling ($A slash D$) are merged into floor area per capita ($A slash P = D slash P times A slash D$), while heating-system mix ($S_s$), building-envelope quality, and occupant behaviour are absorbed into the intensity factor ($I$). This aggregation sacrifices granularity for data reliability: $A slash P$ and $I$ can be computed from consistent annual time series, whereas the sub-components would require building-stock model estimates.

The contest between scale effects (population, floor area) and efficiency
effects (envelope quality, fuel switching) determines the trajectory of
aggregate heating demand @iea2024buildings @reuter2020. Switzerland has two
distinctive features. First, unusually rapid population growth (+23% since
2002) driven by EU/EFTA free movement creates persistent upward pressure
largely absent in demographically stable countries @bfs2024pop. Second, the
direct rebound effect (10--30% of engineering-predicted savings "taken back"
as higher comfort) @sorrell2009 means that our intensity factor $I$ captures
the _net_ effect of efficiency improvements after behavioural rebound.

The relative importance of each driver is quantified in @results. The
forward-looking analysis in @scenarios explores how different assumptions
alter the balance between upward and downward pressures through 2050.


// =============================================================================
// 5. DATA SOURCES AND METHODOLOGY
// =============================================================================

= Data Sources and Methodology <data>

== Data Sources

Our analysis draws on the following primary data sources. All datasets were
downloaded programmatically, cached locally, and processed using Python
(Polars for tabular data, Plotly for visualisation).

#datasource("BFE — Overall Energy Statistics")[
  _Schweizerische Gesamtenergiestatistik_: final energy consumption by
  sector and carrier, 1980--2024. We filter for _Endverbrauch -- Haushalte_
  to obtain residential heating energy @bfe2024.
]

#datasource("BFE/Prognos — Energy Consumption by End Use")[
  _Analyse des schweizerischen Energieverbrauchs 2000--2023 nach
  Verwendungszwecken_ @prognos2024. Tabelle 1: space-heating share of
  household energy. Tabelle 11: heating energy by carrier (PJ).
  Tabelle 13: floor-area shares by heating system.
]

#datasource("BFE — Heating Degree Days")[
  Population-weighted national HDD (base 20/12 °C), monthly from 1994.
  Pre-1994 supplemented by Zurich-Fluntern station data from Stadt Zürich
  Open Data @meteoswiss2024.
]

#datasource("BFS — Population (STATPOP)")[
  Permanent resident population 2010--2024 via PX-Web API @bfs2024.
  Extended to 1960 using World Bank WDI @worldbank2024. BFS scenarios
  (reference/high/low) for 2025--2075 projections @bfs2024pop.
]

#datasource("BFS — Building and Dwelling Register (GWR)")[
  _Gebäude- und Wohnungsstatistik_ via SDMX REST API @sdmx2024:
  buildings by heating system, building category (EFH/MFH/mixed/partial),
  construction period, and canton. Annual data 2021--2024 @bfs2024.
  Floor area per person by building type and construction period.
]

#datasource("World Bank — World Development Indicators")[
  GDP in constant LCU (indicator NY.GDP.MKTP.KN) for Switzerland,
  2000--2024. Population (SP.POP.TOTL) 1960--2024 @worldbank2024.
]

#datasource("Geospatial — Swiss canton boundaries")[
  TopoJSON canton boundaries from _swiss-maps_ @swissmaps2021, based on
  BFS/GEOSTAT. 26 cantons with BFS canton IDs (1--26), converted to
  GeoJSON for Plotly choropleth rendering.
]

== Methodology

We apply LMDI-I in additive form @ang2004 @ang2015 to decompose
$E = P times (A slash P) times H times I$, where $I = E slash (A times H)$
captures building envelope quality, heating-system efficiency, and
behavioural patterns (see @sec:lmdi). For forward-looking analysis, we use
Monte Carlo simulation (1,000 iterations) complemented by three deterministic
scenarios (BAU 1%/yr, Accelerated 2%/yr, Ambitious 3%/yr renovation rate);
distributional assumptions are justified in @monte-carlo. Heating-system
economics are evaluated as annualised TOTEX for a reference 150 m#super[2]
unrenovated house under three CO#sub[2] levy scenarios (CHF 120/200/300
per tonne) @gebprog2024. @fig:methodology provides an overview of this
analytical pipeline, from data sources through decomposition to outputs.

#figure(
  methodology-flowchart(),
  caption: [Methodology overview: data sources, decomposition framework, and sub-analyses. Author's contribution.],
) <fig:methodology>

== Data Quality and Limitations

- *Floor area time series*: BFS floor-area-per-person data is only
  available from 2012. For the 2000--2011 period, we use linear
  back-extrapolation anchored to known stock estimates.

- *HDD composite series*: The national series (BFE, 1994+) and the
  Zurich-Fluntern series (pre-1994) use different measurement
  methodologies. We validate the overlap period and find close agreement
  (within 3%).

- *GWR coverage*: The SDMX API provides building-level data only from
  2021. For earlier years, we rely on BFS census snapshots (2000, 2021).

- *EBF definition break*: The _Energiebezugsfläche_ definition changed
  with SIA 380/1 revision in 2007. This precludes using per-m#super[2]
  metrics as a formal LMDI factor (see @sec:intensity for discussion).

- *Intensity attribution*: The sub-decomposition of the intensity effect
  into envelope, fuel-switching, and behavioural components is an
  engineering-based attribution distinct from the LMDI framework, relying
  on stock-turnover estimates from @prognos2024, @tep2023, and @kaempf2018
  rather than a formal statistical decomposition. The resulting shares
  carry uncertainty of $plus.minus 10$ percentage points
  because the three mechanisms interact (see @sec:intensity).


// =============================================================================
// 6. DECOMPOSITION RESULTS
// =============================================================================

= Decomposition Results <results>

This section presents the core findings: individual indicator trends
(@sec:indicators), LMDI-I results (@sec:lmdi), intensity attribution
(@sec:intensity), decoupling assessment (@sec:decoupling), building-type
and cantonal heterogeneity (@sec:heterogeneity), and discussion
(@sec:discussion).

// ---------------------------------------------------------------------------
== Evolution of Key Indicators <sec:indicators>
// ---------------------------------------------------------------------------

=== Final energy by carrier

@fig:energy-carrier shows total household final energy consumption by
carrier from 1980 to 2024. Petroleum products --- once accounting for
over half of residential energy --- have halved in absolute
terms, while electricity (including heat pumps) and ambient heat have
risen steadily. Natural gas peaked around 2005 and has since plateaued.
District heating and biomass (wood, pellets) have grown modestly.

#figure(
  image("figures/fig1_energy_by_carrier.svg", width: 100%),
  caption: [Swiss household final energy consumption by energy carrier,
  1980--2024. Petroleum products have halved; electricity and heat-pump
  ambient energy are the main growth carriers. Author's elaboration
  based on BFE @bfe2024.],
) <fig:energy-carrier>

The carrier mix has shifted from a fossil-dominated system (>70% of residential final energy from oil and
gas in 2000) to one where heat pumps and electricity account for the largest
combined share by 2024. This fuel switching is a key driver of the intensity
decline discussed in @sec:intensity.

=== Climate: heating degree days

Heating degree days (HDD) have declined at $-156$ HDD per
decade since the 1980s. The Alps have warmed by +2°C since
pre-industrial levels, roughly twice the global average, and the trend
is expected to continue at a similar pace under moderate climate
scenarios. Year-to-year fluctuations remain large (individual winters
can differ by more than 500 HDD from the trend line), but the secular
direction is unambiguous. In the LMDI decomposition, declining HDD
reduces heating demand by approximately $-450$ TJ/yr, independent of
any policy intervention.

=== Population dynamics

@fig:population shows that the Swiss resident population grew by 25%
between 2000 and 2024 (from 7.2 to 9.0 million), driven primarily by
EU/EFTA free-movement immigration after 2002. BFS reference projections
indicate growth to 10.4 million by 2050. This
demographic expansion is the single strongest upward pressure on aggregate
heating demand.

#figure(
  image("figures/fig3_population.svg", width: 100%),
  caption: [Swiss permanent resident population 1960--2024 (historical)
  and BFS reference-scenario projections to 2050. Key demographic
  waves are annotated: guest-worker era, oil-crisis stagnation,
  EU free-movement acceleration. Author's elaboration based on
  BFS @bfs2024 and World Bank @worldbank2024.],
) <fig:population>

=== Heating-system mix by floor area

@fig:heating-mix shows the shift in heated floor area by system type:
oil has declined from 59.9% to 23.9% of total heated floor area between 2000 and 2024, while heat pumps
have risen from near zero to 28.9% of heated floor area. Gas has remained stable at around
19--21% of floor area; wood and district heating together account for ~12% of floor area.

#figure(
  image("figures/fig4_heating_mix.svg", width: 100%),
  caption: [Floor-area share by primary heating system, 2000--2024.
  Oil heating has more than halved; heat pumps now lead by floor area
  served. Note: shares are weighted by heated floor area
  (Energiebezugsfläche), not building count. Author's elaboration
  based on BFE/Prognos @prognos2024.],
) <fig:heating-mix>

=== Floor area per capita

Single-family homes (EFH) provide 55 m#super[2]/person,
while multi-family buildings (MFH) provide 43 m#super[2]/person
--- a persistent 28% gap (@fig:floor-period). The population-weighted
average of 46.6 m#super[2]/person has remained remarkably
stable, as the shift towards MFH living has offset rising per-unit floor
area in new construction.

// ---------------------------------------------------------------------------
== Quantitative Decomposition <sec:lmdi>
// ---------------------------------------------------------------------------

=== The LMDI-I additive method

As described in @framework, we decompose $E = P times (A slash P) times H
times I$ using the LMDI-I additive method @ang2004 @ang2015. The total
change $Delta E = E^T - E^0$ is split into four exact components:

$ Delta E = Delta E_"pop" + Delta E_"floor" + Delta E_"weather"
  + Delta E_"intensity" $

The LMDI method guarantees zero residual, eliminating the interaction terms
that plague Laspeyres or Paasche decompositions.

=== Cumulative results (2000--2024)

@fig:waterfall presents the cumulative LMDI-I decomposition over the
full 2000--2024 period.

#figure(
  image("figures/fig8_lmdi_waterfall.svg", width: 100%),
  caption: [LMDI-I four-factor decomposition of Swiss residential
  space-heating energy demand --- cumulative change 2000--2024 (TJ).
  Bars show the contribution of each factor; the diamond marks the net
  change. The decomposition is exact (zero residual). Author's
  contribution.],
) <fig:waterfall>

#figure(
  table(
    columns: (auto, auto, auto, auto),
    align: (left, right, center, right),
    table.header(
      [*Factor*], [*$Delta E$ (TJ)*], [*Direction*], [*Share of |total|*],
    ),
    table.hline(stroke: 0.8pt),
    [Population ($P$)], [+37,559], [$+$], [29.3%],
    [Floor area/cap ($A slash P$)], [+12,897], [$+$], [10.1%],
    [Weather ($H$)], [-11,160], [$-$], [8.7%],
    [Intensity ($I$)], [-67,366], [$-$], [52.6%],
    table.hline(stroke: 0.8pt),
    [*Net change*], [*-28,070*], [$-$], [--],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Summary of LMDI-I cumulative factor contributions,
  2000--2024. Shares are computed as a fraction of the sum of
  absolute values ($sum |Delta E_i| = 128 "," 982$ TJ).],
) <tab:lmdi-summary>

Population growth (+37,559 TJ) and rising floor area per capita (+12,897 TJ)
together added +50,456 TJ. On the efficiency side, the intensity factor
--- capturing envelope improvements, fuel switching, and behavioural changes
--- delivered $-67,366$ TJ, offsetting _both_ scale effects. Climate warming
contributed an additional $-11,160$ TJ.

#insight[
  The intensity effect ($-67 "," 366$ TJ) alone exceeds the combined
  upward pressure from population growth ($+37 "," 559$ TJ) and
  expanding floor area ($+12 "," 897$ TJ), yielding a net decline
  of $-28 "," 070$ TJ ($-17%$) over the period. Technology and
  efficiency improvements have been the decisive factor in bending the
  heating-energy curve downward despite sustained demographic and
  affluence growth.
]

*Counterfactual interpretation.*
The intensity effect can be given a concrete counterfactual reading:
_what would Swiss space-heating demand have been in 2024 if energy
intensity had remained at its 2000 level?_ Formally,

$ E_"cf" = P_(2024) times (A slash P)_(2024) times H_(2024) times I_(2000) $

where $P$, $A slash P$, $H$, and $I$ denote population, floor area per
capita, heating degree-days, and energy intensity respectively. This
counterfactual holds every factor at its observed 2024 value except
intensity, which is frozen at the 2000 baseline. The difference
$E_"cf" - E_(2024)$ equals the cumulative intensity contribution from
the LMDI-I additive decomposition ($-67 "," 366$ TJ), confirming
internal consistency: in the additive LMDI framework the factor
effects sum exactly to the observed change with zero residual. In
practical terms, without any efficiency improvement Switzerland would
be consuming $E_(2024) + 67 "," 366$ TJ for space heating in
2024, ~50% more than the actual level --- and the gap
represents the cumulative benefit of tighter building standards,
heat-pump diffusion, and behavioural changes accumulated over the
period.

=== Annual decomposition dynamics

The year-by-year decomposition reveals that structural factors (population,
floor area, intensity) evolve smoothly, while weather introduces large
inter-annual volatility. The population effect has been remarkably
consistent at +1,300 to +1,800 TJ/yr throughout the period, but the
intensity effect has moderated from $-3 "," 200$ TJ/yr in the
2000s to $-2 "," 500$ TJ/yr in the 2010s, a deceleration discussed
further in @sec:discussion.

The 2020--2021 period is anomalous: COVID-19 lockdowns increased residential occupancy and heating demand, while milder winters partially offset this effect. We retain these years in the decomposition as they represent genuine energy consumption, but caution against over-interpreting the year-to-year pattern during this period.

// ---------------------------------------------------------------------------
== Intensity Effect Attribution <sec:intensity>
// ---------------------------------------------------------------------------

The intensity factor ($-67 "," 366$ TJ) is by far the largest single
contributor to the observed decline. Because it captures everything
that reduces energy per unit of heated floor area per HDD, it
aggregates several distinct mechanisms. The LMDI decomposition
quantifies _how much_ of the total energy change is attributable to
intensity improvements, but it does not reveal _why_ intensity
improved. To disaggregate the intensity effect into its component
mechanisms, we perform a separate engineering-based attribution
analysis, distinct from the formal LMDI framework. Rather than a
mathematical decomposition identity, this attribution combines
bottom-up stock-turnover modelling with published engineering
parameters to estimate the relative contribution of each mechanism.
@tab:intensity-attr presents the resulting indicative shares.

#figure(
  table(
    columns: (auto, auto, auto, 1fr),
    align: (left, right, right, left),
    table.header(
      [*Sub-component*], [*Share*], [*$approx Delta E$ (TJ)*],
      [*Mechanism*],
    ),
    table.hline(stroke: 0.8pt),
    [Fuel switching], [~51%], [-34,700],
    [Oil/gas $arrow.r$ heat pumps (COP 3--4) means 60--75% less
    final energy per unit of heat delivered],
    [Building envelope], [~33%], [-22,700],
    [Better insulation (walls, windows, roofs) in new and retrofitted
    buildings],
    [Other], [~16%], [-11,200],
    [Behavioural changes (lower thermostat settings), improved
    controls (thermostatic valves, smart systems), hydraulic
    balancing],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Indicative breakdown of the intensity effect into
  sub-components.],
) <tab:intensity-attr>

The three shares are derived as follows. The *fuel-switching share (~51%)* is calculated from the shift in
heating-system market shares: oil heating declined from
60% to 24% of heated floor area, while heat pumps grew from near
zero to 29% @bfs2024. Each square metre switched from an oil boiler
(seasonal efficiency 0.85--0.95) to a heat pump (seasonal COP 3--4)
reduces final energy consumption by 60--75% for the same useful heat
output. We compute the aggregate fuel-switching contribution by
multiplying the switched floor area by this per-unit saving, drawing
on GWR building-register data @bfs2024 and FWS heat-pump statistics
@fws2024.

The *envelope share (~33%)*
is estimated from the evolution of average U-values in the Swiss
building stock --- from 0.8--1.0 W/(m#super[2]K) in
pre-1975 buildings to 0.15--0.25 W/(m#super[2]K) for post-2000
construction @kaempf2018 --- combined with the observed renovation
rate (1.1%/yr) and the new-construction rate. Using
BFE/Prognos data on building-stock vintage composition @prognos2024
and TEP Energy renovation statistics @tep2023, we estimate the
cumulative share of the stock that has been brought to post-2000
envelope standards (either through new construction or deep retrofit)
and infer how much of the aggregate intensity decline is attributable
to improved insulation.

The *behavioural and controls share (~16%)* is treated as the residual
after accounting for envelope and fuel-switching effects. It
encompasses lower thermostat settings (average room temperatures
declined from 21°C to 20°C over the period), the
diffusion of smart thermostats and building-automation systems, and
reduced ventilation losses. This residual interpretation is partly
supported by Prognos household survey data on heating behaviour
@prognos2024.

The fuel-switching contribution is computed by tracking the year-to-year change in the fleet's effective energy multiplier $Sigma(s_i slash eta_i)$, where $s_i$ is the floor-area share and $eta_i$ the system efficiency (COP for heat pumps, combustion efficiency for boilers). This multiplier declined by ~20% between 2000 and 2024 as oil ($eta = 0.90$, contributing $1 slash 0.90 = 1.11$ units of final energy per unit of useful heat) was progressively replaced by heat pumps ($"COP" approx 3.5$, contributing $1 slash 3.5 = 0.29$). The contribution is weighted using LMDI log-mean weights to maintain consistency with the main decomposition. The envelope and behavioural shares are derived from the residual, split in a 2:1 ratio based on stock-turnover estimates.

These shares carry significant uncertainty --- on the order of
$plus.minus 10$ percentage points each --- because the three
mechanisms interact. Deep renovations, for instance, frequently
combine envelope upgrades with heating-system replacement, making
clean attribution to a single mechanism difficult. The figures in
@tab:intensity-attr should therefore be read as order-of-magnitude
estimates rather than precise decomposition results.

This computed split is independently corroborated by the _Gebäudeprogramm_ Jahresbericht 2024 @gebprog2024jb, which reports the energy savings of all subsidised building measures since 2010 by category: _Haustechnik_ (heating-system replacement) accounts for 62% of lifetime energy savings, _Wärmedämmung_ (envelope insulation) for 19%, _Systemsanierung_ (whole-building renovation) for 8%, _zentrale Wärmeversorgung_ (district heating connections) for 10%, and _Neubau_ for 3%. Combining system-related measures (Haustechnik + district heating = 72%) and envelope-related measures (Wärmedämmung + Neubau = 22%) yields a ratio broadly consistent with our data-driven decomposition, noting that the programme data captures only subsidised measures whereas our LMDI-based attribution covers all intensity improvements including unsubsidised new construction and building-code compliance.

=== Building envelope improvements

Typical wall U-values have improved from 0.8--1.0 W/(m#super[2]K)
(pre-1970) to 0.15--0.25 W/(m#super[2]K) (post-2000) @kaempf2018. However,
the renovation rate remains the binding constraint: at 1.1%/yr, the stock
requires ~90 years for full renewal, far below the 2%/yr target @tep2023
@gebprog2024.

=== Fuel switching

Heat pumps (COP ~3.5) consume ~70% less final energy than oil
boilers for the same useful heat. As @fig:heating-mix shows, heat-pump
floor-area share has risen from near zero to 28.9% of total heated floor area, driving a substantial
portion of the intensity decline.

=== Why insulation is not a separate LMDI factor

Building insulation is not included as a fifth factor because (i) no
annual stock-level U-value time series exists for Switzerland, (ii) the
Energiebezugsfläche definition changed in 2007 @muken2014, introducing a
methodological break, (iii) insulation and heating-system type are
correlated (deep renovations often include system replacement), creating
multicollinearity, and (iv) the intensity factor already implicitly
captures envelope improvements. The attribution in @tab:intensity-attr
provides the complementary disaggregation.

#insight[
  Building envelope improvements account for ~45% of
  the intensity decline ($approx -30 "," 300$ TJ), but the current
  renovation rate of 1.1%/year is half the 2%/year needed
  to meet Switzerland's 2050 targets @tep2023. Accelerating deep
  retrofits is the most impactful lever for further progress.
]

// ---------------------------------------------------------------------------
== Decoupling Assessment <sec:decoupling>
// ---------------------------------------------------------------------------

@fig:decoupling presents five indexed series (2000 = 100) that allow a
direct visual comparison of economic growth, demographic expansion,
building-stock growth, and energy trajectories.

#figure(
  image("figures/fig5_decoupling.svg", width: 100%),
  caption: [Decoupling assessment: five indexed series (2000 = 100).
  GDP grew by 51%, population by 25%, heated floor area by 38%, while
  space-heating energy declined by 17% and energy intensity per
  m#super[2] fell by 40%. Policy milestones annotated: SIA 380/1
  revision (2007), CO#sub[2] levy (2008), Buildings Programme (2010),
  MuKEn 2014 (2015), CHF 120/t CO#sub[2] (2022). Author's
  contribution based on @bfe2024, @bfs2024, @worldbank2024.],
) <fig:decoupling>

The year-to-year fluctuations visible in @fig:decoupling --- particularly the uptick around 2010 and the dip in 2014 --- are predominantly weather-driven. @fig:energy-hdd-norm removes the dominant source of volatility (weather) by normalising heating energy to a reference climate (HDD = 3,159, the 2000--2024 average). Although the normalised series is substantially smoother, some year-to-year variation remains: this residual reflects non-weather factors such as population changes, energy price shocks, economic cycles, and --- notably in 2020 --- increased home occupancy during COVID-19 lockdowns.#footnote[The 2020 uptick in actual heating energy may also partly reflect increased home occupancy during COVID-19 lockdowns, which raised residential heating demand independently of weather.] A linear trend fitted to the HDD-normalised series (dashed line in @fig:energy-hdd-norm) confirms a monotonic structural decline of 19%, strengthening the decoupling finding: the downward trajectory is not an artefact of mild recent winters but reflects genuine, sustained efficiency gains in the building stock. The gap between the actual and normalised series also illustrates the magnitude of weather-induced noise: in cold years (e.g., 2010), actual demand exceeds the structural trend by up to 8%, while mild winters (e.g., 2014, 2020) produce apparent savings that are partly illusory.

#figure(
  image("figures/fig10_energy_hdd_normalized.svg", width: 100%),
  caption: [Space-heating energy: actual vs.\ HDD-normalised (reference HDD = 3,159), with a linear structural trend (dashed). Normalising for weather removes the dominant source of year-to-year volatility; the fitted trend line confirms a steady structural decline in heating demand. Author's contribution based on BFE energy balance @bfe2024 and HDD data @meteoswiss2024.],
) <fig:energy-hdd-norm>

HDD normalisation removes the dominant source of volatility --- weather --- but residual year-to-year variation ($plus.minus 5 "," 000$ TJ around the trend line) remains because several other drivers are not held constant. First, immigration to Switzerland arrives in waves, particularly following the phased activation of EU/EFTA bilateral free-movement agreements, causing discrete jumps in the number of heated dwellings that shift the normalised series upward in specific years. Second, energy price effects produce temporary dips and recoveries: when oil and gas prices spike (notably in 2008 and during 2011--2014), households respond by reducing thermostat settings or heating fewer rooms, depressing demand below the structural trend; conversely, the 2015--2016 oil price collapse enabled more liberal heating behaviour, producing a visible uptick. Third, COVID-19 lockdowns in 2020 increased daytime residential occupancy through widespread work-from-home arrangements, raising heating demand independently of weather. Fourth, construction cycles introduce lumpiness: new building completions arrive in bursts due to planning and permitting lags, adding heated floor area in discrete steps rather than smoothly. Despite these residual bumps, the structural downward trend remains clear and consistent across the full 2000--2024 period, confirming that the observed decoupling is not an artefact of recent mild winters but reflects genuine, sustained improvements in the building stock.

Between 2000 and 2024:
- *GDP* (constant 2017 PPP) rose by *+51%*
- *Population* grew by *+25%*
- *Heated floor area* expanded by *+38%*
- *Space-heating energy* declined by *-17%*
- *Energy intensity per m#super[2]* fell by *-40%*

This constitutes unambiguous *absolute decoupling*: heating energy has
declined in absolute terms while both GDP and population have grown
substantially. The steepest intensity declines coincide with major
regulatory milestones: SIA 380/1 revision (2007), CO#sub[2] levy
introduction (2008), the Buildings Programme (2010), MuKEn 2014 adoption,
and the levy increase to CHF 120/t (2022) @bafu2024 @gebprog2024.

// ---------------------------------------------------------------------------
== Building Type Heterogeneity <sec:heterogeneity>
// ---------------------------------------------------------------------------

The aggregate decomposition masks important differences across building
types and regions. This section examines two dimensions of
heterogeneity: building category and cantonal geography.

=== Heat-pump adoption by building type

@fig:heating-type shows heating source distribution across four
building categories (EFH, MFH, mixed-use, and partial residential),
together with the heat-pump adoption trend from 2021 to 2024.

#figure(
  image("figures/fig15_heating_by_type.svg", width: 100%),
  caption: [Heating source distribution by building category and
  heat-pump adoption trend, 2021--2024. Single-family homes (EFH) lead
  with 28% of buildings using HP as primary heating; mixed-use and
  partial-residential buildings lag. Author's elaboration based on
  BFS GWR @bfs2024.],
) <fig:heating-type>

The transition is proceeding at distinctly different speeds:

#figure(
  table(
    columns: (auto, auto, auto, auto),
    align: (left, right, right, right),
    table.header(
      [*Building type*], [*HP share 2021*], [*HP share 2024*],
      [*Change*],
    ),
    table.hline(stroke: 0.8pt),
    [EFH (single-family)], [21%], [28%], [+7 pp],
    [MFH (multi-family)], [15%], [20%], [+5 pp],
    [Mixed-use], [7%], [11%], [+4 pp],
    [Partial residential], [6%], [9%], [+3 pp],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Heat-pump adoption rates (share of buildings with HP as primary
  heating system) by building type, 2021--2024.
  The "four-speed" transition shows EFH leading and non-residential
  mixed buildings lagging. Source: BFS GWR @bfs2024.],
) <tab:hp-adoption>

EFH buildings benefit from simpler installation logistics, owner-occupancy
that aligns investment incentives, and smaller system sizes. MFH buildings
face structural barriers: split incentives (landlords pay, tenants benefit),
space constraints for outdoor units, cantonal noise regulations, and
permitting complexity for ground-source drilling or system replacement.

=== Floor area by building period

@fig:floor-period shows that EFH provide 55
m#super[2]/person compared to 43 m#super[2]/person in MFH --- a
persistent 28% gap. This matters because a person living in an EFH
requires heating for 12 m#super[2] more floor area than their
MFH counterpart, directly scaling energy demand.

#figure(
  image("figures/fig16_floor_area_by_period.svg", width: 100%),
  caption: [Floor area per person by building type. The 28% gap between
  EFH (55 m#super[2]) and MFH (43 m#super[2]) means the per-capita
  floor-area factor in the LMDI is not uniform across the stock.
  Author's elaboration based on BFS @bfs2024.],
) <fig:floor-period>

Critically, non-EFH buildings (MFH, mixed-use, partial) house
73% of the Swiss population but account for only 20--30% of all heat-pump
installations (by building count). Unlocking this segment is essential for maintaining the pace
of intensity decline.

=== Cantonal variation

@fig:canton-map displays the cantonal heat-pump adoption rate as a
choropleth map, revealing a striking geographic divide.

#figure(
  image("figures/fig17_canton_hp_map.svg", width: 95%),
  caption: [Cantonal heat-pump adoption rates (share of buildings with
  HP as primary heating system), 2024. Fribourg leads at 41.8% of
  buildings, followed by Luzern (33.2%) and Aargau (28.9%).
  Basel-Stadt (7.4% of buildings) and Neuchâtel (12.0% of buildings)
  lag. Author's elaboration based on BFS GWR @bfs2024 @sdmx2024.],
) <fig:canton-map>

Fribourg leads at 41.8% of buildings, while Basel-Stadt (7.4% of buildings) and Neuchâtel (12.0% of buildings)
lag by a wide margin --- a five-fold spread reflecting differences in building
stock composition, MuKEn adoption timing, and cantonal subsidy generosity.
However, much of this spread is explained by building stock composition rather than policy alone. Basel-Stadt is essentially a city-canton --- densely built, with predominantly multi-family housing --- where heat pumps face genuine structural constraints: limited outdoor space for air-source units, noise restrictions in close-quarter settings, and difficult permitting for ground-source drilling in built-up areas. Fribourg, by contrast, has a substantially higher share of single-family homes, where heat-pump installation is mechanically simpler and faces fewer regulatory obstacles. The five-fold spread therefore overstates the pure policy gap; a significant portion reflects the urban--rural gradient in building typology. This does not invalidate the finding --- cantonal policy differences remain real and consequential --- but it means that convergence strategies must address building-type constraints (notably through district heating in dense cantons), not only subsidy levels and MuKEn adoption timing.

This heterogeneity implies that the national-average intensity effect is
disproportionately driven by early-adopter cantons with high EFH shares,
while lagging urban cantons represent untapped potential.

// ---------------------------------------------------------------------------
== Discussion <sec:discussion>
// ---------------------------------------------------------------------------

=== Why intensity dominates

Three reinforcing mechanisms drive the intensity factor's dominance over the 2000--2024 period.

Building standards tightened progressively, lowering new-build heating demand from ~100 kWh/m#super[2]/yr (pre-2000) to less than 40 kWh/m#super[2]/yr under MuKEn 2014 @muken2014. Each new building added to the stock dilutes aggregate intensity downward.

Heat-pump diffusion (seasonal COP 3--4) cut final energy by 60--75% for each unit of floor area switched from fossil boilers @fws2024. The cumulative floor area switched from oil to heat pumps now exceeds 100 million m#super[2].

Behavioural shifts towards lower indoor temperatures, together with improved heating controls (thermostatic radiator valves, building automation), contributed an estimated 10--15% of the total intensity reduction.

These mechanisms are partially correlated: deep renovations typically combine envelope upgrades, system replacement, and improved controls in a single intervention. The aggregate intensity factor captures their joint effect, which is why it dominates the decomposition.

=== Signs of deceleration

Despite the impressive cumulative gains, there are signs that the
rate of intensity improvement is slowing. The annual intensity
contribution averaged $-3 "," 200$ TJ/year during the 2000s
but has moderated to $-2 "," 500$ TJ/year in the 2010s. Early 2020s data suggests further slowing beyond this level, though the short time window and the confounding effect of COVID-19 on residential occupancy patterns make this preliminary. Several factors explain the broader deceleration:

- *Diminishing marginal returns on new construction*: As the share of
  new buildings in the total stock grows, each additional
  high-performance building displaces less energy because it replaces
  an already-reasonable standard, not a pre-1970 building.

- *Slow retrofit rate*: At 1.1%/year, the existing stock turns over
  far too slowly @tep2023. The "easy wins" --- replacing the oldest
  oil boilers in EFH with heat pumps --- are exhausted,
  leaving the harder-to-reach MFH stock.

- *Floor-area rebound*: Some of the efficiency gains have been offset
  by rising comfort expectations and larger per-capita floor area,
  above all in the EFH segment.

=== Absolute decoupling: confirmed but fragile

Switzerland has achieved absolute decoupling between residential
heating energy and GDP --- robust to weather correction and consistent
across sub-periods --- but the decoupling is _fragile_: it depends on
continued intensity improvements that are decelerating (see above).
We present the full quantitative summary in @conclusion.

#insight[
  Switzerland has achieved absolute decoupling: heating energy has
  fallen by 17% while GDP grew by 51% since 2000. However, the
  rate of improvement is decelerating. Sustaining this trajectory
  requires doubling the renovation rate (from 1.1% to 2%/year) and
  unlocking heat-pump adoption in multi-family buildings, which house
  73% of the population but account for a minority of installations.
]

=== Implications for policy

The policy implications of these findings are developed in @scenarios.


// =============================================================================
// 7. REGULATORY FRAMEWORK
// =============================================================================

= Regulatory Framework <regulation>

Swiss building energy policy operates through a multi-level governance
structure in which the Confederation sets framework legislation and economic
instruments, while cantons retain primary authority over building standards
and enforcement. This layered architecture has produced strong results on the
technology side --- intensity and fuel switching --- but leaves important
demand-side drivers unaddressed.

== Swiss Building Energy Policy Landscape <policy-landscape>

=== Federal Level

*CO#sub[2] Act (SR 641.71).* The CO#sub[2] levy on fossil heating fuels was
introduced at CHF 12/t in 2008 and has escalated to CHF 120/t since 2022
@bfe2024b. Two-thirds of revenue is redistributed per capita; the remaining
third finances the Buildings Programme (_Gebäudeprogramm_), which co-finances
envelope retrofits and heating-system replacements with typical subsidies of
CHF 5,000--15,000 @gebprog2024.

*Energy Strategy 2050.* The federal Energy Act (EnG, SR 730.0) targets
$-43%$ final energy consumption by 2035 relative to 2000. The EP2050+
scenarios @ep2050plus require building-sector renovation rates of
2--2.5%/yr, double the current pace @tep2023.

=== Cantonal Level

*MuKEn 2014* has been adopted by 22 of 26 cantons. Key provisions include a
maximum heating demand of 16 kWh/m#super[2]/yr for new buildings and a 10%
renewable share of heating energy when replacing heating systems. The partial adoption creates
cantonal heterogeneity in heat-pump penetration. *SIA 380/1* defines
U-value requirements and the _Energiebezugsfläche_ concept (revised in 2007,
introducing a methodological break). *GEAK* energy certificates (A--G scale)
serve as both an information instrument and a trigger for renovation subsidies.


== CO#sub[2] Levy: Mechanism and Scenario Justification <co2-levy>

To assess how the evolving carbon-pricing landscape affects the economics of
heating-system choice, we evaluate annual total cost of ownership (TOTEX)
under three CO#sub[2] levy scenarios. These span the range from current
policy reality to the theoretical optimum that would fully internalise the
climate externality.

#figure(
  table(
    columns: (auto, auto, 1fr),
    align: (left, center, left),
    table.header(
      [*Scenario*], [*Rate (CHF/t)*], [*Justification*],
    ),
    table.hline(stroke: 0.8pt),
    [Status quo],
    [120],
    [Current rate since 1 Jan 2022. Set by CO#sub[2] Act (SR 641.71) and Ordinance (SR 641.711, Art. 94a). The levy has escalated stepwise from CHF 12/t in 2008.],

    [Policy trajectory],
    [200],
    [Revised CO#sub[2] Act 2025--2030 ceiling of CHF 210/t @co2act. Consistent with the EU ETS trajectory under Fit-for-55 and BFE _EP2050+_ @ep2050plus.],

    [Full externality],
    [300],
    [Aligns with IPCC AR6 WGIII 1.5°C-pathway median social cost of carbon @ipcc2023. Supported by @rennert2022 and @epa2023 SCC estimates (USD 185--220/t CO#sub[2]).],
    table.hline(stroke: 0.8pt),
  ),
  caption: [CO#sub[2] levy scenarios used in the TOTEX comparison. The 120/200/300 CHF/t progression spans from current law through the most likely near-term policy path to the theoretically optimal tax internalising the full climate-damage externality.],
) <tab:co2-scenarios>

@fig:cost-comparison presents the annual TOTEX for a reference 150 m#super[2]
unrenovated house (120 kWh/m#super[2]/yr) across four heating systems and
three levy scenarios.

#figure(
  image("figures/fig14_cost_comparison.svg", width: 100%),
  caption: [Annual TOTEX comparison for four heating systems under three
  CO#sub[2] levy scenarios. CAPEX annualised over 20 years at 3%, net of
  _Gebäudeprogramm_ subsidies. Reference: 150 m#super[2] unrenovated house,
  120 kWh/m#super[2]/yr. Author's contribution.],
) <fig:cost-comparison>

#insight[
  Even at the current CHF 120/t levy, air-source heat pumps (CHF 4,006/yr)
  are already cheaper than oil boilers (CHF 4,246/yr) on a total-cost-of-ownership
  basis. At CHF 300/t, the oil boiler TOTEX (CHF 5,200/yr) exceeds
  ground-source heat pump costs (CHF 4,576/yr) by 14% --- making the economic
  case for fossil heating untenable even for the highest-CAPEX renewable option.
]

The asymmetry is structural: heat pumps consume levy-exempt electricity,
while fossil boilers bear the full charge, creating an increasingly powerful
price signal for fuel switching.


== Scenario Methodology and Sensitivity Analysis <monte-carlo>

=== Why Monte Carlo simulation?

Future renovation rates depend on political will and funding. Population trajectories hinge on immigration agreements. Climate warming follows non-linear dynamics. Three deterministic scenarios (BAU, Accelerated, Ambitious) can only show three discrete outcomes. If a decision-maker looks at BAU vs.\ Ambitious and picks the middle path, they have learned little about which lever matters most or how wide the uncertainty band actually is.

Monte Carlo simulation samples 1,000 parameter combinations from plausible ranges, producing a distribution of outcomes that deterministic scenarios cannot capture. It serves three purposes in this study:

+ *Sensitivity ranking.* Varying parameters independently reveals which levers dominate outcome uncertainty. The renovation rate explains 3--6$times$ more variance in 2050 demand than population or climate parameters (@fig:tornado), directing policy attention to the highest-leverage intervention.

+ *Uncertainty envelopes.* The fan chart (@fig:scenario-fan) shows the 10th--90th percentile range of plausible futures. Under nearly all parameter combinations, achieving the EP2050+ corridor requires action on multiple fronts. The width of the bands quantifies this claim.

+ *Robustness testing.* When the BAU trajectory falls near the 90th percentile (worst outcomes), current policy is inadequate across the full parameter space, not just under pessimistic assumptions.

Our Monte Carlo exercise produces a _sensitivity envelope_, not a probability forecast. The input distributions (uniform for renovation rate and population, normal for HDD decline) bound the range of _plausible_ values, not calibrated probability densities. Future renovation rates are policy choices, not random variables with a known distribution. The exercise ranks sensitivities and communicates uncertainty; it does not predict specific probabilities.

=== Projection model

Future space-heating energy demand is projected using the same multiplicative identity as the LMDI decomposition:

$ E_t = P_t times "HDD"_t times I_t $

where each factor evolves from its observed 2024 base value. Population $P_t$ follows BFS official projections (reference, high, and low scenarios). Heating degree days $"HDD"_t$ decline at 2.5%/decade, consistent with observed Swiss climate trends. Energy intensity $I_t$ declines at a rate linked to the renovation rate:

$ dot(I) = 0.010 + 0.5 times r $

where $r$ is the annual renovation rate (fraction of building stock renovated per year). The two terms capture distinct mechanisms: the base rate (1%/yr) represents _autonomous_ intensity improvements that occur without envelope renovation --- primarily fuel switching at natural system end-of-life (oil boiler replaced by heat pump) and incremental behavioural/controls gains. The renovation-linked term reflects the stock-level energy saving from deep envelope retrofits: a typical Swiss renovation reduces building-level heating demand by ~50% (from $tilde 150$ to $tilde 75$ kWh/m#super[2]/yr), so renovating $r$ percent of the stock yields an additional $0.5 r$ percent intensity decline at the aggregate level.

This functional form is an engineering approximation, not an empirically calibrated relationship. It assumes uniform renovation depth across the stock and does not capture diminishing returns as the most inefficient buildings are renovated first. These simplifications are acceptable for a scenario-comparison exercise but mean the absolute 2050 values should be interpreted as indicative, not predictive.

=== Three named scenarios

#figure(
  table(
    columns: (auto, auto, auto, auto, auto),
    align: (left, center, center, center, left),
    table.header(
      [*Parameter*], [*BAU*], [*Accelerated*], [*Ambitious*], [*Sensitivity range*],
    ),
    table.hline(stroke: 0.8pt),
    [Renovation rate (%/yr)], [1.0], [2.0], [3.0], [0.8--3.2],
    [Population growth], [BFS ref.], [BFS ref.], [BFS ref.], [BFS low--high],
    [HDD decline (%/decade)], [2.5], [2.5], [2.5], [$mu = 2.5$, $sigma = 1.0$],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Scenario parameters and sensitivity ranges. The three named
  scenarios vary only the renovation rate; the sensitivity envelope
  explores the full parameter space.],
) <tab:mc-params>

The three scenarios are deterministic: BAU (1%/yr renovation rate, current pace), Accelerated (2%/yr, EP2050+ target), and Ambitious (3%/yr, upper bound of feasibility). All three use BFS reference population and the central HDD trend.

=== Sensitivity envelope

To explore parameter uncertainty beyond the three named scenarios, we sample 1,000 parameter combinations: renovation rate uniformly in 0.8--3.2%/yr, population uniformly between BFS low and high projections, and HDD decline normally distributed around 2.5%/decade ($sigma = 1.0$). The resulting trajectories produce a sensitivity envelope (@fig:scenario-fan), _not_ a probability distribution --- the shaded bands represent the range of plausible outcomes given the parameter bounds, without implying that any particular outcome is more likely than another. Future renovation rates and population trajectories are outcomes of policy choices and political decisions, not random variables with a known probability distribution.

#figure(
  image("figures/fig12_scenario_fan.svg", width: 100%),
  caption: [Scenario fan chart of projected space-heating energy demand,
  2024--2050. Shaded bands show the 10th--90th and 25th--75th percentile
  sensitivity envelopes from 1,000 parameter combinations. Coloured lines
  show the three named scenarios. Author's contribution.],
) <fig:scenario-fan>

@fig:scenario-fan shows the fan chart with the three named scenarios overlaid on the sensitivity envelope. The BAU scenario (1% renovation rate) remains near the upper bound, while the Ambitious scenario (3%) tracks the lower bound. The median trajectory projects ~30% reduction by 2050 relative to the 2024 baseline.

#figure(
  image("figures/fig13_scenario_tornado.svg", width: 100%),
  caption: [Tornado sensitivity chart showing the impact of one-at-a-time
  parameter perturbation on 2050 energy demand relative to the median
  projection. Author's contribution.],
) <fig:tornado>

The tornado chart (@fig:tornado) confirms that the renovation rate is the dominant lever: varying it from 1% to 3%/yr swings 2050 energy demand by $plus.minus$ 12,600 TJ, while population uncertainty contributes $plus.minus$ 4,500 TJ and HDD decline $plus.minus$ 2,000 TJ. The policy-controllable parameter matters 3--6$times$ more than the exogenous drivers --- the key insight for policy design.


== Policy Impact on Decomposition Factors <policy-decomposition>

The preceding analysis allows us to construct a synthesis linking each
major policy instrument to the LMDI decomposition factors identified in
@results.

#figure(
  table(
    columns: (2.8cm, 2.2cm, 1fr, 3.5cm),
    align: (left, left, left, left),
    table.header(
      [*Policy*], [*Factor*], [*Mechanism*], [*Impact*],
    ),
    table.hline(stroke: 0.8pt),
    [MuKEn 2014],
    [Intensity],
    [Max 16 kWh/m#super[2]/yr for new buildings],
    [New stock at 5$times$ better than pre-1970],

    [Buildings Programme],
    [Intensity],
    [Subsidies for envelope retrofit and HP installation],
    [$tilde$ 1.1%/yr renovation rate],

    [CO#sub[2] levy],
    [Intensity (fuel switching)],
    [Price signal shifts oil $arrow.r$ heat pump],
    [Oil share halved 2000--2024],

    [SIA 380/1 (2007)],
    [Intensity],
    [Updated U-value calculation; EBF harmonisation],
    [Definition break post-2007],

    [Energy Strategy 2050],
    [Intensity, Mix],
    [Framework targets and nuclear phase-out],
    [$-43%$ final energy by 2035],

    [_None_],
    [Floor area/capita],
    [No policy targets per-capita floor area],
    [$+38%$ since 2000, unchecked],

    [_None_ (immigration)],
    [Population],
    [Free movement, economic growth],
    [$+25%$ since 2000],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Mapping of Swiss policy instruments to LMDI decomposition factors.
  Technology-side policies (MuKEn, CO#sub[2] levy, subsidies) target the
  intensity and mix factors, while the two largest upward drivers ---
  population and floor area per capita --- remain largely unaddressed by
  policy.],
) <tab:policy-factors>

@tab:policy-factors reveals a striking asymmetry: Switzerland has deployed
a comprehensive toolkit targeting the _intensity_ factor, but the two
largest upward drivers --- population growth ($+25%$) and floor area per
capita ($+38%$) --- operate outside the regulatory perimeter.

#insight[
  The fundamental policy blind spot in Swiss building energy strategy is the
  absence of instruments targeting per-capita floor area --- the second-largest
  upward driver of heating energy demand ($+12,897$ TJ cumulative). While
  intensity improvements have more than compensated, continued floor-area
  growth at historical rates will erode efficiency gains,
  as the "easy wins" in envelope renovation are exhausted and
  marginal improvement costs rise.
]

Achieving the 2050 net-zero target requires not only accelerating renovation
rates but also considering instruments that address the consumption-side
dynamics of per-capita space demand.


// =============================================================================
// 8. SCENARIOS AND RECOMMENDATIONS
// =============================================================================

= Scenarios and Recommendations <scenarios>

== Future Scenarios <sec:future-scenarios>

=== Three scenarios for 2050

The three named scenarios (methodology in @monte-carlo) yield the following
2050 projections:

#figure(
  table(
    columns: (auto, auto, auto, auto, 1fr),
    align: (left, center, right, right, left),
    table.header(
      [*Scenario*], [*Reno.\ rate*], [*2050 demand (TJ)*],
      [*$Delta$ vs.\ 2024*], [*Key assumptions*],
    ),
    table.hline(stroke: 0.8pt),
    [BAU],
    [1%/yr],
    [$approx$ 100,000],
    [$-27%$],
    [Current policy settings maintained; HP adoption follows historical EFH-led trend],

    [Accelerated],
    [2%/yr],
    [$approx$ 88,000],
    [$-36%$],
    [Renovation rate doubles to EP2050+ target; MFH HP barriers partially removed; MuKEn 2025 fossil heating ban; cantonal renovation mandates emerging (GE, VD)],

    [Ambitious],
    [3%/yr],
    [$approx$ 78,000],
    [$-43%$],
    [Deep-retrofit mandates; full MFH market unlock; progressive floor-area policy],
    table.hline(stroke: 0.8pt),
  ),
  caption: [Summary of three named scenario outcomes for 2050. All scenarios
  assume BFS reference population projection and a $-2.5%$/decade HDD trend.],
) <tab:scenarios>

These trajectories are visualised in @fig:scenario-fan, with the Monte Carlo uncertainty envelope, and @fig:tornado quantifying the sensitivity of the 2050 outcome to individual parameter perturbations.

The plausibility of the Accelerated scenario is supported by tightening regulatory requirements. MuKEn 2025, adopted in August 2025, effectively bans fossil heating-system replacements by requiring 100% renewable energy for all new installations, accelerating the oil-to-heat-pump transition at natural system end-of-life (typically 15--20 years). Beyond this event-triggered mechanism, two cantons have introduced performance-based renovation obligations: Geneva requires buildings exceeding 800 MJ/m#super[2]/yr to renovate within three years (in force since June 2024) @ge2024energy, and the Canton of Vaud has adopted a law requiring GEAK F/G buildings above 750 m#super[2] to be renovated by 2042, with entry into force expected in January 2027 @vd2026energy. If other cantons follow this trajectory, renovation rates could rise above the current 1.1%/yr baseline toward the 2%/yr target.

=== Gap to net-zero

EP2050+ @ep2050plus requires a 60--70% reduction in heating energy relative
to 2000 (target: 50,000--65,000 TJ). None of the three scenarios reaches
this corridor: BAU overshoots by ~1.6--2$times$, Accelerated overshoots the EP2050+ target corridor by 35--75% of the corridor width,
and even Ambitious falls short by 20--55% of the corridor width. Even at 3%/yr renovation rate,
the combined inertia of population growth, floor-area expansion, and slow
MFH turnover prevents convergence.

=== Closing the gap: a multi-lever strategy

Reaching the net-zero corridor requires simultaneous action on multiple
decomposition factors: renovation rates at or above 2.5%/yr @ep2050plus
(bridging half the gap), accelerated MFH heat-pump deployment
(closing the 8-pp EFH--MFH gap), floor-area stabilisation (saving an
estimated 4,000--6,000 TJ by 2050), and complementary pathways for the
hardest-to-electrify segment (biofuels, district heating, behavioural
interventions) contributing the final 5,000--10,000 TJ @iea2024. No
single lever is sufficient.


== Policy Recommendations <sec:policy-recs>

The decomposition results and scenario analysis point to five concrete
policy recommendations, each targeting a specific factor in the LMDI
identity. We develop them in decreasing order of estimated quantitative
impact.

=== Recommendation 1: Double the renovation rate to 2%/yr

*Target factor:* Intensity ($I$) \
*Estimated additional impact:* $approx -10,600$ TJ by 2050 vs.\ BAU

At 1.1%/yr, the stock requires ~90 years for full renewal @tep2023. Two
instruments could accelerate this: (i) mandatory renovation upon change
of ownership, analogous to France's DPE regime; and (ii) doubled
_Gebäudeprogramm_ subsidy ceilings for comprehensive retrofits (walls,
roof, windows, and heating system in a single intervention) @gebprog2024.

=== Recommendation 2: Unlock MFH heat-pump adoption

*Target factor:* Intensity ($I$), specifically fuel switching \
*Scope:* MFH segment houses $approx 73%$ of the population

Four interventions could narrow the EFH--MFH gap (@tab:hp-adoption):
(i) simplified pass-through mechanisms for low-carbon heating costs under
Swiss tenancy law (OR Art.\ 269a); (ii) higher _Gebäudeprogramm_ subsidy
rates for MFH systems (e.g., 50% top-up on the base subsidy for buildings with >4 dwelling units); (iii)
noise-regulation exemptions for certified low-noise models (\<50 dB(A))
@fws2024; and (iv) streamlined collective drilling permits for shared
ground-source systems in dense urban plots.

=== Recommendation 3: Cantonal convergence programme

*Target factor:* Intensity ($I$), geographic equity \
*Reference:* cantonal spread from 7.4% of buildings (Basel-Stadt) to 41.8% (Fribourg)

Two instruments could address the five-fold variation: (i)
performance-linked federal transfers, allocating supplementary
_Gebäudeprogramm_ funding to cantons below the national median, conditional
on MuKEn 2014 adoption; and (ii) targeted district-heating expansion in
dense urban cantons where individual heat pumps face genuine physical
constraints.

District heating deserves particular emphasis as the primary decarbonisation pathway for dense urban cantons like Basel-Stadt and Geneva, where individual heat-pump installations face space, noise, and drilling constraints that are structural rather than regulatory. District heating networks can draw on a diverse mix of heat sources --- waste incineration plants (already a major source in Swiss cities), large-scale centralised heat pumps (river- or lake-water sourced), deep geothermal, and wood-chip boilers --- achieving decarbonisation at the neighbourhood scale without requiring individual building interventions. Several Swiss cities are already operating or expanding district heating networks: Geneva's GeniLac project uses Lake Geneva water, Zurich is extending its _Fernwärme_ network, and Basel has pioneered deep geothermal. District heating is complementary to, not competing with, heat-pump expansion: it serves precisely the dense urban segments where individual heat pumps are least feasible, while heat pumps remain the optimal solution for suburban and rural EFH stock.

=== Recommendation 4: Floor-area efficiency signal

*Target factor:* Affluence ($A slash P$) \
*Quantitative justification:* $+12,897$ TJ cumulative --- the policy blind
spot identified in @tab:policy-factors

Three options: (i) a progressive property tax surcharge above a per-person
threshold (e.g., 50 m#super[2]), earmarked for the _Gebäudeprogramm_; (ii)
density bonuses in cantonal zoning for developments achieving below-average
per-capita floor area; and (iii) reduced property transfer taxes for
downsizing moves, freeing under-occupied EFH stock. These instruments are
politically sensitive, but without addressing the affluence factor, intensity
improvements must work harder each year to maintain decoupling.

=== Recommendation 5: Biofuels as MFH transition fuel

*Target factor:* Intensity ($I$), alternative to electrification \
*Scope:* limited to the 5--10% of the building stock that cannot be electrified by 2050

For MFH buildings where heat pumps are genuinely impractical, bio-heating-oil
(HVO) or renewable gas offer drop-in decarbonisation without replacing
distribution infrastructure. This is a bridge technology, not a long-term
solution, constrained by feedstock availability @iea2024. An explicit
CO#sub[2] levy exemption for certified biofuels would create the necessary
price incentive.

These five recommendations form a coherent package acting on all four LMDI
factors: (1) and (2) target intensity through renovation and fuel switching,
(3) addresses geographic inequity, (4) fills the policy blind spot on
per-capita floor area, and (5) provides a pragmatic bridge for the
hardest-to-electrify buildings.


// =============================================================================
// 9. CONCLUSION
// =============================================================================

= Conclusion <conclusion>

== Main Findings

This report presented a four-factor LMDI decomposition of final energy demand
for space heating in Swiss residential buildings over the period 2000--2024.
The principal findings are as follows.

*A net decline driven by technology.* Total space-heating energy demand fell
by 28,070 TJ ($-17%$) between 2000 and 2024, despite population growth of
25% and GDP growth of 51%. The intensity factor --- capturing building-envelope
improvements, the shift from fossil fuels to heat pumps, and behavioural
adjustments --- contributed $-67,366$ TJ, single-handedly offsetting all
upward pressures from population ($+37,559$ TJ) and floor area per capita
($+12,897$ TJ). Weather (declining HDD) added a further $-11,160$ TJ.

*Absolute decoupling confirmed, but fragile.* Switzerland has achieved
absolute decoupling between residential heating energy and economic output.
However, the annual intensity improvement has decelerated from $-3,200$
TJ/yr in the 2000s to $-2,500$ TJ/yr in the 2010s, and the renovation
rate (1.1%/yr) remains half the 2%/yr target set by EP2050+
@ep2050plus. Without policy escalation, the decoupling trajectory could
flatten or reverse within one to two decades.

*A four-speed transition.* Heat-pump adoption (share of buildings with HP as primary heating) varies sharply across building
types: EFH lead at 28%, followed by MFH at 20%, mixed-use at 11%, and
partial residential at 9%. The MFH segment, which houses 73%
of the population, faces structural barriers (split incentives, noise
regulations, space constraints) that slow the transition.

*Cantonal heterogeneity.* Heat-pump adoption rates (share of buildings) range from 41.8% in
Fribourg to 7.4% in Basel-Stadt --- a five-fold spread that reflects
differences in building stock composition (particularly the urban--rural
gradient in EFH vs.\ MFH shares), MuKEn adoption timing, and
cantonal subsidy generosity.

*Scenarios fall short of net-zero.* Even the Ambitious scenario (3%/yr
renovation rate, $-43%$ by 2050) does not reach the EP2050+ net-zero
corridor ($-60$ to $-70%$). Closing this gap requires simultaneous action
on renovation rates, MFH electrification, floor-area restraint, and
complementary decarbonisation pathways.


== General Lessons <sec:general-lessons>

The Swiss case offers three lessons. First, *technology can outpace
affluence and population --- but only with sustained policy*: the
$-67,366$ TJ intensity reduction exceeded the $+50,456$ TJ combined
upward pressure, but this required a sustained policy ratchet (MuKEn 2014,
six CO#sub[2] levy escalations, _Gebäudeprogramm_ subsidies) @co2act
@gebprog2024. Second, *the affluence blind spot is a structural risk*:
no instrument addresses per-capita floor area ($+12,897$ TJ), an asymmetry
common across OECD energy policies @jackson2017. Third, *the Kaya structure
reveals where policy should go next*: any country with immigration-driven
growth and an aging building stock faces a similar decomposition, and
achieving net-zero requires extending the policy perimeter to
affluence-driven demand factors.


== Limitations and Extensions <sec:limitations>

*Data gaps.* Floor-area data is available only from 2012 (back-extrapolated
to 2000); GWR provides canton-level data only from 2021; the EBF definition
changed in 2007, precluding per-m#super[2] metrics as a formal LMDI factor.

*Scope.* This analysis covers space heating only; hot water (~15% of residential energy), cooling,
and cooking are excluded.

*LMDI limitations.* The decomposition captures _what_ changed, not _why_.
Establishing the causal effect of individual policies would require
econometric methods exploiting cantonal policy variation.

*Possible extensions.* Cantonal-level LMDI decomposition using GWR data,
embodied-energy analysis extending the system boundary to life-cycle energy,
Alpine cross-country comparison (Austria, South Tyrol), and dynamic
building-stock modelling would all strengthen the analysis.


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
