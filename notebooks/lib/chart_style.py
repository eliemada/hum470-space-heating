"""Shared Plotly theme, color palettes, and figure export helper.

All figures in the HUM-470 notebook use these constants for visual consistency.
"""

from pathlib import Path

import plotly.graph_objects as go

# ── Standard dimensions ────────────────────────────────────────────────
FIG_WIDTH = 1400
FIG_HEIGHT = 750

# ── Plotly layout template applied to every figure ─────────────────────
HUM_TEMPLATE = go.layout.Template(
    layout=go.Layout(
        template="plotly_white",
        font=dict(family="Inter, Helvetica, Arial, sans-serif", size=22),
        title=dict(font=dict(size=24)),
        xaxis=dict(title=dict(font=dict(size=20)), tickfont=dict(size=17)),
        yaxis=dict(title=dict(font=dict(size=20)), tickfont=dict(size=17)),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.30,
            xanchor="center",
            x=0.5,
            font=dict(size=16),
        ),
        margin=dict(l=80, r=40, t=90, b=110),
        width=FIG_WIDTH,
        height=FIG_HEIGHT,
    ),
)

# ── Energy carrier color palette (household energy balance) ────────────
CARRIER_COLORS = {
    "Petroleum Products": "#8B4513",
    "Natural Gas": "#FF6B35",
    "Electricity": "#FFC107",
    "Wood / Biomass": "#4CAF50",
    "District Heating": "#9C27B0",
    "Other Renewables": "#00BCD4",
    "Coal": "#607D8B",
    "Waste": "#795548",
}

# German → English carrier name mapping
CARRIER_MAP = {
    "Erdölprodukte": "Petroleum Products",
    "Elektrizität": "Electricity",
    "Gas": "Natural Gas",
    "Holzenergie": "Wood / Biomass",
    "Fernwärme": "District Heating",
    "Kohle": "Coal",
    "Uebrige erneuerbare Energien": "Other Renewables",
    "Müll und Industrieabfälle": "Waste",
}

# ── Heating‐mix color palette (floor‐area shares, Tabelle 13) ─────────
MIX_COLORS = {
    "oil": "#8B4513",
    "gas": "#FF6B35",
    "heat_pump": "#2196F3",
    "wood": "#4CAF50",
    "electric_resistance": "#FFC107",
    "district_heating": "#9C27B0",
    "other_solar": "#00BCD4",
}

MIX_LABELS = {
    "oil": "Heating Oil",
    "gas": "Natural Gas",
    "heat_pump": "Heat Pumps (electric)",
    "wood": "Wood / Biomass",
    "electric_resistance": "Electric Resistance",
    "district_heating": "District Heating",
    "other_solar": "Other (Coal + misc)",
}

MIX_CARRIERS = list(MIX_COLORS.keys())

# ── Building‐heating‐source bar colors ────────────────────────────────
BUILDING_HEAT_COLORS = {
    "Heat Pump": "#2196F3",
    "Gas": "#FF6B35",
    "Heating Oil": "#8B4513",
    "Wood": "#4CAF50",
    "Electricity": "#FFC107",
    "Solar Thermal": "#00BCD4",
    "District Heating": "#9C27B0",
    "Other": "#607D8B",
}

# ── Building type / category colors ───────────────────────────────────
BUILDING_TYPE_COLORS = {
    "EFH": "#FF9800",                   # Orange — matches SFH in fig6
    "MFH": "#2196F3",                   # Blue — matches MFH in fig6
    "Single-Family (EFH)": "#FF9800",
    "Multi-Family (MFH)": "#2196F3",
    "Mixed-Use Residential": "#9C27B0",
    "Partial Residential": "#607D8B",
}

# ── Heating system colors (economics) ─────────────────────────────────
SYSTEM_COLORS = {
    "Oil Boiler": "#8B4513",
    "Gas Condensing": "#FF6B35",
    "Air-Source HP": "#2196F3",
    "Ground-Source HP": "#1565C0",
}

# ── LMDI decomposition colors ────────────────────────────────────────
LMDI_COLORS = {
    "population": "#F44336",
    "floor_area": "#FF9800",
    "weather": "#2196F3",
    "intensity": "#4CAF50",
    "net": "#212121",
}

# ── Decoupling series styles ─────────────────────────────────────────
DECOUPLE_SERIES = [
    ("gdp_idx", "GDP (real)", "#E91E63", "solid", 3),
    ("pop_idx", "Population", "#9C27B0", "dash", 2),
    ("floor_idx", "Heated Floor Area", "#FF9800", "dashdot", 2),
    ("energy_idx", "Space-Heating Energy", "#2196F3", "solid", 3),
    ("intensity_idx", "Energy per m\u00b2 (index)", "#F44336", "dot", 2),
]


def apply_theme(fig: go.Figure) -> go.Figure:
    """Apply the HUM template to a figure and return it (for chaining)."""
    fig.update_layout(template=HUM_TEMPLATE)
    return fig


def export_fig(fig: go.Figure, name: str, figures_dir: Path) -> list[Path]:
    """Export *fig* as SVG + PDF into *figures_dir*.

    Uses the figure's own width/height when explicitly set in the layout,
    falling back to the module-level defaults (FIG_WIDTH, FIG_HEIGHT).
    """
    figures_dir.mkdir(exist_ok=True)
    _w = fig.layout.width if fig.layout.width is not None else FIG_WIDTH
    _h = fig.layout.height if fig.layout.height is not None else FIG_HEIGHT
    paths: list[Path] = []
    for ext in ("svg", "pdf"):
        out = figures_dir / f"{name}.{ext}"
        fig.write_image(str(out), width=_w, height=_h)
        paths.append(out)
    print(f"  Exported {name}.svg + {name}.pdf")
    return paths
