"""Generate the methodology flowchart (fig0) for the HUM-470 report.

Produces fig0_methodology.svg and fig0_methodology.pdf in the figures/ directory.
Run with: uv run python notebooks/gen_methodology_fig.py
"""

import math
from pathlib import Path

import plotly.graph_objects as go

# ── Import project style ─────────────────────────────────────────────
from lib.chart_style import export_fig

# ── Layout constants ─────────────────────────────────────────────────
W, H = 1200, 720
FONT = "Inter, Helvetica, Arial, sans-serif"

# Column x-centres
X_DATA = 0.14          # Data Sources column
X_ANALYSIS = 0.50      # Analysis column
X_OUTPUT = 0.86        # Outputs column

# Box half-widths / half-heights
BW_DATA = 0.115
BW_ANALYSIS = 0.145
BW_OUTPUT = 0.115
BH_DATA = 0.038
BH_ANALYSIS = 0.055
BH_OUTPUT = 0.065

# Colors
COL_BLUE = "#1565C0"
COL_BLUE_FILL = "rgba(21,101,192,0.10)"
COL_GREEN = "#388E3C"
COL_GREEN_FILL = "rgba(56,142,60,0.10)"
COL_ORANGE = "#E65100"
COL_ORANGE_FILL = "rgba(230,81,0,0.10)"
COL_GREY = "#757575"
COL_GREY_FILL = "rgba(158,158,158,0.10)"
COL_ARROW = "#546E7A"

# ── Helper: draw rounded box ─────────────────────────────────────────

def _box(
    fig: go.Figure,
    cx: float,
    cy: float,
    hw: float,
    hh: float,
    line_color: str,
    fill_color: str,
    label: str,
    font_size: int = 11,
    font_color: str = "#212121",
    dash: str = "solid",
) -> None:
    """Add a rounded rectangle with centred text."""
    fig.add_shape(
        type="rect",
        x0=cx - hw, x1=cx + hw,
        y0=cy - hh, y1=cy + hh,
        xref="paper", yref="paper",
        line=dict(color=line_color, width=1.8, dash=dash),
        fillcolor=fill_color,
        layer="below",
    )
    fig.add_annotation(
        x=cx, y=cy,
        xref="paper", yref="paper",
        text=label,
        showarrow=False,
        font=dict(family=FONT, size=font_size, color=font_color),
        align="center",
        xanchor="center",
        yanchor="middle",
    )


# ── Helper: draw arrow ───────────────────────────────────────────────

def _arrow(
    fig: go.Figure,
    x0: float, y0: float,
    x1: float, y1: float,
    color: str = COL_ARROW,
    width: float = 1.4,
    dashed: bool = False,
) -> None:
    """Draw an arrow from (x0,y0) to (x1,y1) in paper coordinates.

    Plotly does not support axref='paper', so we convert the tail
    position to a pixel offset from the head.  The usable plot area
    (inside margins) is W - margin_l - margin_r by H - margin_t - margin_b.

    For dashed arrows we draw a dashed line shape + a small solid
    arrowhead annotation at the tip, because Plotly annotations
    don't support dashed arrow shafts.
    """
    margin_l, margin_r, margin_t, margin_b = 10, 10, 10, 10
    plot_w = W - margin_l - margin_r
    plot_h = H - margin_t - margin_b
    # ax/ay are pixel offsets from the arrowhead (x1,y1)
    ax_px = (x0 - x1) * plot_w
    ay_px = -(y0 - y1) * plot_h  # y is inverted in pixel space

    if dashed:
        # Draw the dashed line as a shape
        fig.add_shape(
            type="line",
            x0=x0, y0=y0, x1=x1, y1=y1,
            xref="paper", yref="paper",
            line=dict(color=color, width=width, dash="dash"),
        )
        # Small arrowhead at the tip (short shaft so it looks like just a head)
        length = math.sqrt(ax_px**2 + ay_px**2)
        # Use a short 12 px shaft for the arrowhead
        shaft = min(12.0, length)
        scale = shaft / length if length > 0 else 0
        fig.add_annotation(
            x=x1, y=y1,
            ax=ax_px * scale, ay=ay_px * scale,
            xref="paper", yref="paper",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.0,
            arrowwidth=width,
            arrowcolor=color,
            text="",
            standoff=2,
        )
    else:
        fig.add_annotation(
            x=x1, y=y1,
            ax=ax_px, ay=ay_px,
            xref="paper", yref="paper",
            showarrow=True,
            arrowhead=3,
            arrowsize=1.0,
            arrowwidth=width,
            arrowcolor=color,
            text="",
            standoff=2,
        )


# ── Build figure ─────────────────────────────────────────────────────

def build_flowchart() -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        width=W,
        height=H,
        template="plotly_white",
        font=dict(family=FONT, size=12),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    # ── Column headers ────────────────────────────────────────────────
    hdr_y = 0.97
    for cx, label in [
        (X_DATA, "<b>Data Sources</b>"),
        (X_ANALYSIS, "<b>Analysis Methods</b>"),
        (X_OUTPUT, "<b>Outputs</b>"),
    ]:
        fig.add_annotation(
            x=cx, y=hdr_y,
            xref="paper", yref="paper",
            text=label,
            showarrow=False,
            font=dict(family=FONT, size=14, color="#37474F"),
            xanchor="center",
        )

    # ── DATA SOURCE boxes (Column 1) ─────────────────────────────────
    data_labels = [
        "BFE Energy Balance",
        "BFS Population",
        "BFE HDD",
        "BFS Floor Area",
        "Prognos Tab.13<br>(heating mix)",
        "System efficiencies",
        "BFS Projections",
        "CO\u2082 levy scenarios",
    ]
    # Evenly space 8 boxes from y=0.88 down to y=0.16
    data_ys = [0.88 - i * 0.103 for i in range(8)]

    for i, (label, cy) in enumerate(zip(data_labels, data_ys)):
        _box(fig, X_DATA, cy, BW_DATA, BH_DATA,
             COL_BLUE, COL_BLUE_FILL, label, font_size=10)

    # ── ANALYSIS boxes (Column 2) ────────────────────────────────────
    # Box A — LMDI  (connected from rows 0-3)
    ya = 0.785
    _box(fig, X_ANALYSIS, ya, BW_ANALYSIS, BH_ANALYSIS,
         COL_GREEN, COL_GREEN_FILL,
         "<b>4-Factor LMDI-I</b><br>E = P \u00d7 (A/P) \u00d7 HDD \u00d7 I",
         font_size=11)

    # Box B — Intensity sub-decomposition (connected from rows 4-5 + A)
    yb = 0.58
    _box(fig, X_ANALYSIS, yb, BW_ANALYSIS, BH_ANALYSIS,
         COL_GREEN, COL_GREEN_FILL,
         "<b>Intensity Sub-Decomp.</b><br>Fleet multiplier \u03a3(s\u1d62/\u03b7\u1d62)",
         font_size=11)

    # Box C — Monte Carlo (connected from rows 1,2,6)
    yc = 0.375
    _box(fig, X_ANALYSIS, yc, BW_ANALYSIS, BH_ANALYSIS,
         COL_GREEN, COL_GREEN_FILL,
         "<b>Monte Carlo Scenarios</b><br>1 000 iterations",
         font_size=11)

    # Box D — TOTEX Economics (connected from row 7)
    yd = 0.19
    _box(fig, X_ANALYSIS, yd, BW_ANALYSIS, BH_ANALYSIS,
         COL_GREEN, COL_GREEN_FILL,
         "<b>TOTEX Economics</b><br>System cost comparison",
         font_size=11)

    # ── OUTPUT boxes (Column 3) ──────────────────────────────────────
    yo1 = 0.785
    _box(fig, X_OUTPUT, yo1, BW_OUTPUT, BH_OUTPUT,
         COL_ORANGE, COL_ORANGE_FILL,
         "<b>Factor effects</b><br>Pop +37 559 TJ<br>Floor +12 897<br>"
         "Weather \u221211 160<br>Intensity \u221267 366",
         font_size=9, font_color="#BF360C")

    yo2 = 0.58
    _box(fig, X_OUTPUT, yo2, BW_OUTPUT, BH_OUTPUT,
         COL_ORANGE, COL_ORANGE_FILL,
         "<b>Attribution</b><br>Fuel switch ~51%<br>"
         "Envelope ~33%<br>Behaviour ~16%",
         font_size=9, font_color="#BF360C")

    yo3 = 0.375
    _box(fig, X_OUTPUT, yo3, BW_OUTPUT, BH_OUTPUT,
         COL_ORANGE, COL_ORANGE_FILL,
         "<b>Scenario fan chart</b><br>BAU / Accelerated<br>/ Ambitious",
         font_size=9, font_color="#BF360C")

    yo4 = 0.19
    _box(fig, X_OUTPUT, yo4, BW_OUTPUT, BH_OUTPUT,
         COL_ORANGE, COL_ORANGE_FILL,
         "<b>Cost comparison</b><br>4 systems \u00d7 3 CO\u2082 levies",
         font_size=9, font_color="#BF360C")

    # ── ARROWS: Data → Analysis ──────────────────────────────────────
    x_src = X_DATA + BW_DATA
    x_dst = X_ANALYSIS - BW_ANALYSIS

    # Rows 0-3 → Box A
    for i in range(4):
        _arrow(fig, x_src, data_ys[i], x_dst, ya)

    # Rows 4-5 → Box B
    for i in [4, 5]:
        _arrow(fig, x_src, data_ys[i], x_dst, yb)

    # Rows 1,2,6 → Box C  (Population, HDD, Projections)
    for i in [1, 2, 6]:
        _arrow(fig, x_src, data_ys[i], x_dst, yc)

    # Row 7 → Box D
    _arrow(fig, x_src, data_ys[7], x_dst, yd)

    # ── ARROWS: A → B (internal) ────────────────────────────────────
    _arrow(fig, X_ANALYSIS, ya - BH_ANALYSIS,
           X_ANALYSIS, yb + BH_ANALYSIS,
           color=COL_GREEN, width=1.6)

    # ── ARROWS: Analysis → Output ────────────────────────────────────
    x_a_out = X_ANALYSIS + BW_ANALYSIS
    x_o_in = X_OUTPUT - BW_OUTPUT

    for y_pair in [(ya, yo1), (yb, yo2), (yc, yo3), (yd, yo4)]:
        _arrow(fig, x_a_out, y_pair[0], x_o_in, y_pair[1])

    # ── VALIDATION box (bottom) ──────────────────────────────────────
    yv = 0.04
    _box(fig, 0.50, yv, 0.22, 0.030,
         COL_GREY, COL_GREY_FILL,
         "<b>Cross-validation:</b> Geb\u00e4udeprogramm JB 2024",
         font_size=10, font_color=COL_GREY, dash="dash")

    # Dashed L-shaped path: validation box → right → up → Attribution (Out 2)
    # Horizontal segment: right edge of validation box → corner point
    corner_x = X_OUTPUT + BW_OUTPUT + 0.025  # just past the right edge of outputs
    fig.add_shape(
        type="line",
        x0=0.50 + 0.22, y0=yv,
        x1=corner_x, y1=yv,
        xref="paper", yref="paper",
        line=dict(color=COL_GREY, width=1.2, dash="dash"),
    )
    # Vertical segment: corner → beside Attribution box, with arrowhead
    _arrow(fig, corner_x, yv,
           X_OUTPUT + BW_OUTPUT, yo2,
           color=COL_GREY, width=1.2, dashed=True)

    return fig


# ── Main ─────────────────────────────────────────────────────────────

def main() -> None:
    fig = build_flowchart()
    figures_dir = Path(__file__).resolve().parent.parent / "figures"
    export_fig(fig, "fig0_methodology", figures_dir)


if __name__ == "__main__":
    import sys
    # Ensure the lib package is importable when run from project root
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
