// =============================================================================
// Methodology Flowchart — HUM-470 Swiss Space Heating Decomposition
// =============================================================================
// Usage: #include "figures/fig_methodology_flowchart.typ"
// Or:   #import "figures/fig_methodology_flowchart.typ": methodology-flowchart
// =============================================================================

#let methodology-flowchart() = {
  // --- Colour palette ---
  let data-fill   = rgb("#E3EFF9")   // light blue — data sources
  let data-stroke = rgb("#4A90C4")   // blue border
  let anal-fill   = rgb("#E6F5E6")   // light green — analysis
  let anal-stroke = rgb("#4A9E4A")   // green border
  let out-fill    = rgb("#FFF0E0")   // light orange — outputs
  let out-stroke  = rgb("#D4873A")   // orange border
  let valid-fill  = rgb("#F5E6F5")   // light purple — validation
  let valid-stroke = rgb("#8A5A8A")  // purple border
  let arrow-col   = rgb("#666666")

  // --- Box helper ---
  let node(content, fill-col, stroke-col, width: 100%) = {
    box(
      width: width,
      inset: (x: 5pt, y: 4pt),
      radius: 3pt,
      fill: fill-col,
      stroke: 0.6pt + stroke-col,
    )[
      #set text(size: 7pt, fill: rgb("#1A1A1A"))
      #set par(justify: false, leading: 0.45em)
      #content
    ]
  }

  // --- Arrow (horizontal, centred in cell) ---
  let harrow() = {
    set align(center + horizon)
    box(inset: (y: 0pt))[
      #polygon(
        fill: arrow-col,
        stroke: none,
        (0pt, 3pt),
        (10pt, 3pt),
        (10pt, 0pt),
        (16pt, 4.5pt),
        (10pt, 9pt),
        (10pt, 6pt),
        (0pt, 6pt),
      )
    ]
  }

  // --- Column headers ---
  let col-header(label, col) = {
    align(center)[
      #box(
        inset: (x: 8pt, y: 3pt),
        radius: 2pt,
        fill: col.lighten(80%),
        stroke: 0.5pt + col,
      )[
        #set text(size: 7.5pt, weight: "bold", fill: col.darken(30%))
        #label
      ]
    ]
  }

  // --- Layout: 3-column grid ---
  // Column widths: data 30%, arrows 6%, analysis 28%, arrows 6%, outputs 30%
  block(width: 100%)[
    // Column headers
    #grid(
      columns: (30%, 6%, 28%, 6%, 30%),
      align: (center, center, center, center, center),
      col-header("Data Sources", data-stroke),
      [],
      col-header("Core Analysis", anal-stroke),
      [],
      col-header("Outputs", out-stroke),
    )

    #v(6pt)

    // --- Row 1: LMDI block ---
    #grid(
      columns: (30%, 6%, 28%, 6%, 30%),
      align: (left + horizon, center + horizon, left + horizon, center + horizon, left + horizon),
      gutter: 3pt,
      // Data sources for LMDI
      stack(
        dir: ttb,
        spacing: 3pt,
        node([*BFE Energy Balance*\ Final energy by carrier, 2000--2024], data-fill, data-stroke),
        node([*BFS Population / World Bank*\ Resident population, 1960--2024], data-fill, data-stroke),
        node([*BFE Heating Degree Days*\ Pop.-weighted national HDD], data-fill, data-stroke),
        node([*BFS Floor Area per Capita*\ Heated area per person, 2012--2024], data-fill, data-stroke),
      ),
      // Arrow
      harrow(),
      // Analysis: LMDI
      node(
        [*4-Factor LMDI-I*\
        $E = P times (A slash P) times H times I$\
        Additive decomposition,\ zero residual @ang2004],
        anal-fill, anal-stroke,
      ),
      // Arrow
      harrow(),
      // Output: LMDI results
      stack(
        dir: ttb,
        spacing: 3pt,
        node(
          [*LMDI Results*\
          Pop. #h(2pt) $+37 569$ TJ\
          Floor #h(1pt) $+12 897$ TJ\
          Weather $-11 160$ TJ\
          Intensity $-67 366$ TJ],
          out-fill, out-stroke,
        ),
        node(
          [*Counterfactual*\
          $E_"cf" = P_2024 dot (A slash P)_2024 dot H_2024 dot I_2000$],
          out-fill, out-stroke,
        ),
      ),
    )

    #v(6pt)

    // --- Row 2: Intensity sub-decomposition ---
    #grid(
      columns: (30%, 6%, 28%, 6%, 30%),
      align: (left + horizon, center + horizon, left + horizon, center + horizon, left + horizon),
      gutter: 3pt,
      // Data sources
      stack(
        dir: ttb,
        spacing: 3pt,
        node([*Prognos Tab. 13*\ Floor area by heating system], data-fill, data-stroke),
        node([*System efficiencies*\ COP (HP), boiler $eta$ by fuel], data-fill, data-stroke),
      ),
      // Arrow
      harrow(),
      // Analysis
      node(
        [*Intensity Sub-Decomposition*\
        Fleet multiplier $sum(s_i slash eta_i)$\
        Fuel switching vs.\ envelope vs.\ behaviour],
        anal-fill, anal-stroke,
      ),
      // Arrow
      harrow(),
      // Output
      node(
        [*Attribution*\
        Fuel switching #h(5pt) ~51%\
        Envelope #h(19pt) ~33%\
        Behavioural #h(12pt) ~16%],
        out-fill, out-stroke,
      ),
    )

    #v(6pt)

    // --- Row 3: Scenarios ---
    #grid(
      columns: (30%, 6%, 28%, 6%, 30%),
      align: (left + horizon, center + horizon, left + horizon, center + horizon, left + horizon),
      gutter: 3pt,
      // Data sources
      stack(
        dir: ttb,
        spacing: 3pt,
        node([*BFS Population Projections*\ Reference / high / low to 2060], data-fill, data-stroke),
        node([*Renovation rate assumptions*\ BAU 1% / Accel. 2% / Amb. 3% yr#super[-1]], data-fill, data-stroke),
      ),
      // Arrow
      harrow(),
      // Analysis
      node(
        [*Monte Carlo Scenarios*\
        1 000 iterations, 3 deterministic\ paths (BAU / Accelerated / Ambitious)],
        anal-fill, anal-stroke,
      ),
      // Arrow
      harrow(),
      // Output
      node(
        [*Scenario Fan Chart*\
        BAU / Accelerated / Ambitious\ energy demand to 2060],
        out-fill, out-stroke,
      ),
    )

    #v(6pt)

    // --- Row 4: TOTEX economics ---
    #grid(
      columns: (30%, 6%, 28%, 6%, 30%),
      align: (left + horizon, center + horizon, left + horizon, center + horizon, left + horizon),
      gutter: 3pt,
      // Data sources
      stack(
        dir: ttb,
        spacing: 3pt,
        node([*CO#sub[2] levy scenarios*\ CHF 120 / 200 / 300 per tonne], data-fill, data-stroke),
        node([*System cost data*\ CAPEX, O&M, fuel prices by system], data-fill, data-stroke),
      ),
      // Arrow
      harrow(),
      // Analysis
      node(
        [*TOTEX Economics*\
        Annualised total cost, 150 m#super[2]\ reference building, 4 systems],
        anal-fill, anal-stroke,
      ),
      // Arrow
      harrow(),
      // Output
      node(
        [*Cost Comparison*\
        4 systems $times$ 3 levy levels\ (oil, gas, HP, pellets)],
        out-fill, out-stroke,
      ),
    )

    #v(8pt)

    // --- Cross-validation box ---
    #align(center)[
      #box(
        width: 80%,
        inset: (x: 10pt, y: 5pt),
        radius: 3pt,
        fill: valid-fill,
        stroke: (
          paint: valid-stroke,
          thickness: 0.6pt,
          dash: "dashed",
        ),
      )[
        #set text(size: 7pt, fill: rgb("#1A1A1A"))
        #set par(justify: false)
        #text(weight: "bold")[Cross-validation:]
        _Gebäudeprogramm_ Jahresbericht 2024 validates the intensity sub-decomposition
        (observed renovation rates and fuel-switching trends consistent with attributed shares).
      ]
    ]

    #v(4pt)

    // --- Legend ---
    #align(center)[
      #set text(size: 6.5pt, fill: rgb("#666666"))
      #box(inset: (x: 4pt, y: 2pt), radius: 2pt, fill: data-fill, stroke: 0.4pt + data-stroke)[Data]
      #h(6pt)
      #box(inset: (x: 4pt, y: 2pt), radius: 2pt, fill: anal-fill, stroke: 0.4pt + anal-stroke)[Analysis]
      #h(6pt)
      #box(inset: (x: 4pt, y: 2pt), radius: 2pt, fill: out-fill, stroke: 0.4pt + out-stroke)[Output]
      #h(6pt)
      #box(inset: (x: 4pt, y: 2pt), radius: 2pt, fill: valid-fill, stroke: (paint: valid-stroke, thickness: 0.4pt, dash: "dashed"))[Validation]
    ]
  ]
}
