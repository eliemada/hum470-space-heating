// =============================================================================
// EPFL HUM-470 Report Template — Modern 2026
// Economic Growth and Sustainability II
// Prof. Philippe Thalmann, EPFL ENAC LEUrE
// =============================================================================
// Citation: ISO-690 author-date (Author, year, p. X)
// =============================================================================

#let epfl-red = rgb("#FF0000")
#let epfl-dark = rgb("#1A1A1A")
#let accent-gray = rgb("#4A4A4A")
#let light-gray = rgb("#F5F5F5")
#let medium-gray = rgb("#E0E0E0")

#let report(
  title: "",
  subtitle: "",
  group-number: "XX",
  impact: "XX",
  authors: (),
  date: datetime.today().display("[day] [month repr:long] [year]"),
  course: "SHS HUM-470 — Economic Growth and Sustainability II",
  professor: "Prof. Philippe Thalmann",
  institution: "EPFL ENAC LEUrE",
  semester: "Spring 2026",
  abstract: none,
  keywords: (),
  body,
) = {
  // --- Document metadata ---
  set document(
    title: title,
    author: authors.map(a => a.name),
    date: datetime.today(),
  )

  // --- Page setup ---
  set page(
    paper: "a4",
    margin: (top: 3cm, bottom: 2.5cm, left: 2.5cm, right: 2.5cm),
    header: context {
      if counter(page).get().first() > 1 {
        set text(size: 8.5pt, fill: accent-gray)
        grid(
          columns: (1fr, 1fr),
          align: (left, right),
          [#course],
          [Group #group-number],
        )
        v(-2pt)
        line(length: 100%, stroke: 0.4pt + medium-gray)
      }
    },
    footer: context {
      set text(size: 8.5pt, fill: accent-gray)
      line(length: 100%, stroke: 0.4pt + medium-gray)
      v(2pt)
      grid(
        columns: (1fr, 1fr),
        align: (left, right),
        [#semester],
        [#counter(page).display("1 / 1", both: true)],
      )
    },
  )

  // --- Typography ---
  set text(
    font: ("New Computer Modern", "Libertinus Serif", "Palatino"),
    size: 11pt,
    lang: "en",
    region: "gb",
    fill: epfl-dark,
  )

  set par(
    justify: true,
    leading: 0.65em,
    first-line-indent: 0em,
  )
  set par(spacing: 0.8em)

  // --- Headings ---
  set heading(numbering: "1.1")

  show heading.where(level: 1): it => {
    v(1.2em)
    block(width: 100%)[
      #set text(size: 16pt, weight: "bold", fill: epfl-dark)
      #if it.numbering != none {
        text(fill: epfl-red)[#counter(heading).display() #h(6pt)]
      }
      #it.body
      #v(2pt)
      #line(length: 100%, stroke: 1.5pt + epfl-red)
    ]
    v(0.6em)
  }

  show heading.where(level: 2): it => {
    v(0.8em)
    block[
      #set text(size: 13pt, weight: "bold", fill: epfl-dark)
      #if it.numbering != none {
        text(fill: accent-gray)[#counter(heading).display() #h(4pt)]
      }
      #it.body
    ]
    v(0.4em)
  }

  show heading.where(level: 3): it => {
    v(0.5em)
    block[
      #set text(size: 11.5pt, weight: "bold", fill: accent-gray)
      #if it.numbering != none {
        text(fill: accent-gray)[#counter(heading).display() #h(4pt)]
      }
      #it.body
    ]
    v(0.3em)
  }

  // --- Figures and tables ---
  show figure: it => {
    set align(center)
    v(0.5em)
    block(width: 100%, inset: (x: 0pt, y: 8pt))[
      #it.body
      #v(6pt)
      #set text(size: 9.5pt)
      #if it.caption != none {
        it.caption
      }
    ]
    v(0.5em)
  }

  show figure.where(kind: table): set figure.caption(position: top)
  set table(
    stroke: none,
    inset: 6pt,
    fill: (_, y) => if y == 0 { light-gray } else { none },
  )
  show table: set text(size: 10pt)

  // --- Equations ---
  set math.equation(numbering: "(1)")
  show math.equation.where(block: true): it => {
    v(0.3em)
    it
    v(0.3em)
  }

  // --- Lists ---
  set enum(indent: 1em, body-indent: 0.5em)
  set list(indent: 1em, body-indent: 0.5em, marker: text(fill: epfl-red)[--])

  // --- Links ---
  show link: it => {
    set text(fill: rgb("#0066CC"))
    underline(it)
  }

  // --- Footnotes ---
  set footnote.entry(
    separator: line(length: 30%, stroke: 0.4pt + accent-gray),
  )

  // === TITLE PAGE ===
  {
    set page(header: none, footer: none)

    v(1fr)

    // EPFL red accent bar
    place(
      left + top,
      dx: -2.5cm,
      dy: -3cm,
      rect(width: 6pt, height: 100% + 5.5cm, fill: epfl-red),
    )

    // EPFL wordmark
    align(left)[
      #text(size: 28pt, weight: "bold", fill: epfl-red, tracking: 2pt)[EPFL]
      #v(-6pt)
      #text(size: 9pt, fill: accent-gray)[#institution]
    ]

    v(2cm)

    // Course info
    block(width: 100%)[
      #set text(size: 10pt, fill: accent-gray)
      #text(tracking: 1.5pt)[#upper[#course]]
      #v(-2pt)
      #text(size: 9.5pt)[#professor #h(4pt) | #h(4pt) #semester]
    ]

    v(0.8cm)

    // Title
    block(width: 100%)[
      #line(length: 60pt, stroke: 2.5pt + epfl-red)
      #v(8pt)
      #text(size: 26pt, weight: "bold", fill: epfl-dark)[#title]
      #if subtitle != "" {
        v(4pt)
        text(size: 14pt, fill: accent-gray)[#subtitle]
      }
    ]

    v(0.6cm)

    // Group and impact
    block(
      width: 100%,
      inset: (left: 12pt),
      stroke: (left: 2pt + epfl-red),
    )[
      #set text(size: 11pt)
      #text(weight: "bold")[Group #group-number] \
      #text(fill: accent-gray)[Impact analysed: #emph[#impact]]
    ]

    v(1.5cm)

    // Authors grid
    {
      let author-cells = authors.map(a => {
        block(inset: (y: 4pt))[
          #text(size: 11pt, weight: "semibold")[#a.name] \
          #text(size: 9pt, fill: accent-gray)[#a.at("sciper", default: "")]
        ]
      })

      let cols = calc.min(authors.len(), 2)
      grid(
        columns: (1fr,) * cols,
        column-gutter: 1.5em,
        row-gutter: 0.8em,
        ..author-cells,
      )
    }

    v(2fr)

    // Date
    align(center)[
      #text(size: 10pt, fill: accent-gray)[#date]
    ]

    pagebreak()
  }

  // === ABSTRACT (optional) ===
  if abstract != none {
    v(1em)
    block(
      width: 100%,
      inset: (x: 2em, y: 1em),
      stroke: (left: 2pt + epfl-red),
      fill: light-gray,
    )[
      #text(size: 11pt, weight: "bold")[Abstract]
      #v(4pt)
      #set text(size: 10pt)
      #abstract
    ]

    if keywords.len() > 0 {
      v(6pt)
      set text(size: 9.5pt)
      text(weight: "bold")[Keywords: ]
      keywords.join(", ")
    }

    pagebreak()
  }

  // === TABLE OF CONTENTS ===
  {
    show outline.entry.where(level: 1): it => {
      v(4pt)
      strong(it)
    }
    outline(
      title: [Table of Contents],
      indent: 1.5em,
      depth: 3,
    )
    pagebreak()
  }

  // === BODY ===
  body
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

// Highlighted definition box
#let definition(term, body) = {
  block(
    width: 100%,
    inset: (x: 12pt, y: 10pt),
    stroke: (left: 2.5pt + epfl-red),
    fill: light-gray,
    radius: (right: 3pt),
  )[
    #text(weight: "bold", size: 10.5pt)[#term] \
    #v(2pt)
    #set text(size: 10pt)
    #body
  ]
}

// Key insight / finding callout
#let insight(body) = {
  block(
    width: 100%,
    inset: 12pt,
    stroke: 0.5pt + medium-gray,
    fill: rgb("#FFF8F0"),
    radius: 3pt,
  )[
    #set text(size: 10pt)
    #text(weight: "bold", fill: epfl-red)[Key finding: ]
    #body
  ]
}

// Decomposition equation display (centered, prominent)
#let decomposition(body) = {
  block(
    width: 100%,
    inset: (x: 1em, y: 1em),
    stroke: 0.5pt + medium-gray,
    fill: light-gray,
    radius: 3pt,
  )[
    #set align(center)
    #set text(size: 12pt)
    #body
  ]
}

// Data source card
#let datasource(name, url: none, description) = {
  block(
    width: 100%,
    inset: (x: 10pt, y: 8pt),
    stroke: (left: 2pt + accent-gray),
  )[
    #text(weight: "bold", size: 10pt)[#name]
    #if url != none {
      [ — #text(size: 9pt)[#link(url)]]
    }
    \
    #set text(size: 9.5pt, fill: accent-gray)
    #description
  ]
}
