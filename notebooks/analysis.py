# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "polars",
#     "plotly",
#     "kaleido",
#     "httpx",
#     "openpyxl",
#     "pyarrow",
#     "numpy",
#     "pandas",
# ]
# ///

import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.md(
        """
        # HUM-470 — Swiss Residential Space Heating Analysis
        ## IPAT Decomposition: Energy Demand for Space Heating

        **Group 12** | Elie's Sections: Data & Trends, Policy & Efficiency Drivers, Conclusion

        This notebook downloads, caches, and visualizes key datasets for the IPAT decomposition
        of energy demand for space heating in
        Swiss residential buildings.
        """
    )
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    ## 0. Setup & Data Download
    """)
    return


@app.cell
def _():
    import polars as pl
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    from pathlib import Path
    import json

    # Resolve project root
    _app_path = Path(__file__).resolve()
    _PROJECT_DIR = _app_path.parent.parent if _app_path.parent.name == "notebooks" else _app_path.parent
    DATA_DIR = _PROJECT_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)
    RAW_DIR = DATA_DIR / "raw"
    RAW_DIR.mkdir(exist_ok=True)
    FIGURES_DIR = _PROJECT_DIR / "figures"
    FIGURES_DIR.mkdir(exist_ok=True)

    # Import lib modules
    from lib.data_sources import (
        download_file,
        download_json,
        download_sdmx_csv,
        load_household_energy,
        load_sh_share,
        get_sh_share_fn,
        load_heating_mix,
        load_heating_energy,
        load_hdd,
        load_population,
        load_gdp,
        load_floor_area,
        load_floor_area_by_period,
        load_buildings_heating,
        load_gwr_heating_by_type,
        topojson_to_geojson_cantons,
        load_gwr_canton_hp_share,
    )
    import plotly.express as px
    from lib.chart_style import (
        apply_theme,
        export_fig,
        CARRIER_MAP,
        CARRIER_COLORS,
        MIX_COLORS,
        MIX_LABELS,
        MIX_CARRIERS,
        BUILDING_HEAT_COLORS,
        BUILDING_TYPE_COLORS,
        SYSTEM_COLORS,
        LMDI_COLORS,
        DECOUPLE_SERIES,
    )
    from lib.lmdi import compute_lmdi_3factor, compute_lmdi_4factor, verify_decomposition
    from lib.monte_carlo import (
        run_monte_carlo,
        compute_named_trajectories,
        compute_tornado_sensitivity,
        extract_base_values,
        DEFAULT_SCENARIOS,
    )
    from lib.economics import (
        compute_opex,
        compute_totex,
        DEFAULT_SYSTEMS,
        CO2_LEVY_SCENARIOS,
        annuity_factor,
    )

    print("Setup complete — lib modules loaded.")
    return (
        BUILDING_HEAT_COLORS,
        BUILDING_TYPE_COLORS,
        CARRIER_COLORS,
        CARRIER_MAP,
        CO2_LEVY_SCENARIOS,
        DATA_DIR,
        DECOUPLE_SERIES,
        DEFAULT_SCENARIOS,
        DEFAULT_SYSTEMS,
        FIGURES_DIR,
        LMDI_COLORS,
        MIX_CARRIERS,
        MIX_COLORS,
        MIX_LABELS,
        RAW_DIR,
        SYSTEM_COLORS,
        annuity_factor,
        apply_theme,
        compute_lmdi_3factor,
        compute_lmdi_4factor,
        compute_named_trajectories,
        compute_opex,
        compute_tornado_sensitivity,
        compute_totex,
        download_file,
        download_json,
        download_sdmx_csv,
        export_fig,
        extract_base_values,
        get_sh_share_fn,
        go,
        json,
        load_buildings_heating,
        load_floor_area,
        load_floor_area_by_period,
        load_gdp,
        load_gwr_heating_by_type,
        load_hdd,
        load_heating_energy,
        load_heating_mix,
        load_household_energy,
        load_population,
        load_sh_share,
        make_subplots,
        pl,
        run_monte_carlo,
        verify_decomposition,
    )


# ═══════════════════════════════════════════════════════════════════════
# DATA DOWNLOAD
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(DATA_DIR, RAW_DIR, download_file, download_json, download_sdmx_csv, mo):
    mo.md("### Downloading datasets...")

    # 1. BFE Energy Balance
    energy_balance_path = download_file(
        DATA_DIR,
        "https://www.uvek-gis.admin.ch/BFE/ogd/115/ogd115_gest_bilanz.csv",
        "bfe_energy_balance.csv",
    )

    # 2. BFE official HDD (monthly, 1994+)
    hdd_path = download_file(
        DATA_DIR,
        "https://www.uvek-gis.admin.ch/BFE/ogd/105/ogd105_heizgradtage.csv",
        "bfe_hdd_monthly.csv",
    )

    # 2b. Zurich Fluntern HDD (1864+)
    hdd_zurich_path = download_file(
        DATA_DIR,
        "https://data.stadt-zuerich.ch/dataset/umw_heizgradtage_standort_jahr_monat_od1031/download/UMW103OD1031.csv",
        "zurich_hdd_annual.csv",
    )

    # 3. BFS Population (PX-Web, 2010-2024)
    pop_path = download_json(
        DATA_DIR,
        "https://www.pxweb.bfs.admin.ch/api/v1/en/px-x-0102010000_101/px-x-0102010000_101.px",
        "bfs_population.json",
        payload={
            "query": [
                {"code": "Kanton (-) / Bezirk (>>) / Gemeinde (......)", "selection": {"filter": "item", "values": ["8100"]}},
                {"code": "Bevölkerungstyp", "selection": {"filter": "item", "values": ["1"]}},
                {"code": "Staatsangehörigkeit (Kategorie)", "selection": {"filter": "item", "values": ["-99999"]}},
                {"code": "Geschlecht", "selection": {"filter": "item", "values": ["-99999"]}},
                {"code": "Alter", "selection": {"filter": "item", "values": ["-99999"]}},
            ],
            "response": {"format": "json"},
        },
    )

    # 4. BFE/Prognos household energy by end use
    download_file(RAW_DIR, "https://pubdb.bfe.admin.ch/de/publication/download/12388", "bfe_hh_energy_by_use_2024.xlsx")

    # 5. BFS floor area per person
    download_file(RAW_DIR, "https://dam-api.bfs.admin.ch/hub/api/dam/assets/36158296/master", "floor_area_by_building_category.xlsx")

    # 6. BFS floor area by rooms and canton
    download_file(RAW_DIR, "https://dam-api.bfs.admin.ch/hub/api/dam/assets/36158430/master", "floor_area_by_rooms_canton.csv")

    # 7. BFS buildings by heating system (2000 vs 2021)
    download_file(RAW_DIR, "https://dam-api.bfs.admin.ch/hub/api/dam/assets/23524602/master", "buildings_heating_source_2000_2021.xlsx")

    # 8. BFS construction & housing summary
    download_file(RAW_DIR, "https://dam-api.bfs.admin.ch/hub/api/dam/assets/24885538/master", "bau_wohnungswesen.csv")

    # 9. World Bank GDP (constant LCU, 2000-2024)
    download_json(RAW_DIR, "https://api.worldbank.org/v2/country/CHE/indicator/NY.GDP.MKTP.KN?format=json&per_page=50&date=2000:2024", "worldbank_gdp_ch.json")

    # 10. World Bank population (1960-2024, extended for historical context)
    download_json(RAW_DIR, "https://api.worldbank.org/v2/country/CHE/indicator/SP.POP.TOTL?format=json&per_page=100&date=1960:2024", "worldbank_pop_ch.json")

    # 11. GWR Buildings by type × heating source (SDMX, 2021-2024)
    gwr_heating_path = download_sdmx_csv(
        DATA_DIR,
        "https://disseminate.stats.swiss/rest/data/CH1.GWS,DF_GWS_REG4,1.0.0/A._T..._T.8100?dimensionAtObservation=AllDimensions",
        "gwr_heating_by_type.csv",
    )

    # 12. Swiss cantons TopoJSON (interactivethings/swiss-maps v4)
    canton_topo_path = download_file(
        RAW_DIR,
        "https://unpkg.com/swiss-maps@4/2021/ch-combined.json",
        "ch_combined_topo.json",
    )

    # 13. GWR heating by canton (all cantons, all building types, heating source)
    gwr_canton_path = download_sdmx_csv(
        DATA_DIR,
        "https://disseminate.stats.swiss/rest/data/CH1.GWS,DF_GWS_REG4,1.0.0/A._T._T.._T.?dimensionAtObservation=AllDimensions",
        "gwr_heating_by_canton.csv",
    )

    mo.md("**All datasets downloaded / cached.**")
    return canton_topo_path, energy_balance_path, gwr_canton_path, gwr_heating_path, hdd_path, hdd_zurich_path, pop_path


# ═══════════════════════════════════════════════════════════════════════
# 1. HOUSEHOLD ENERGY BALANCE
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 1. Swiss Energy Balance — Household Final Energy Consumption

    Source: BFE/SFOE Gesamtenergiestatistik (opendata.swiss)

    The BFE energy balance gives us total final energy consumption by sector and by energy
    carrier from 1980 to 2024. We filter for **"Endverbrauch - Haushalte"** (household final
    consumption) which is dominated by space heating.
    """)
    return


@app.cell
def _(energy_balance_path, load_household_energy):
    df_hh = load_household_energy(energy_balance_path)
    print(f"Household energy data: {df_hh.shape[0]} rows, years {df_hh['Jahr'].min()}-{df_hh['Jahr'].max()}")
    print(f"Energy carriers: {df_hh['Energietraeger'].unique().sort().to_list()}")
    df_hh.head(15)
    return (df_hh,)


@app.cell
def _(CARRIER_COLORS, CARRIER_MAP, apply_theme, df_hh, go, pl):
    # Stacked area — household energy by carrier
    df_hh_plot = df_hh.with_columns(
        pl.col("Energietraeger").replace(CARRIER_MAP).alias("carrier_en")
    )
    df_pivot = (
        df_hh_plot
        .group_by(["Jahr", "carrier_en"])
        .agg(pl.col("TJ").sum())
        .sort("Jahr")
    )
    carrier_totals = (
        df_pivot.group_by("carrier_en")
        .agg(pl.col("TJ").sum().alias("total"))
        .sort("total", descending=True)
    )

    fig_hh_energy = go.Figure()
    for _carrier in carrier_totals["carrier_en"].to_list():
        _sub = df_pivot.filter(pl.col("carrier_en") == _carrier).sort("Jahr")
        fig_hh_energy.add_trace(go.Scatter(
            x=_sub["Jahr"].to_list(),
            y=_sub["TJ"].to_list(),
            name=_carrier,
            mode="lines",
            stackgroup="one",
            line=dict(width=0.5, color=CARRIER_COLORS.get(_carrier, "#999")),
        ))

    apply_theme(fig_hh_energy).update_layout(
        title="Swiss Household Final Energy Consumption by Carrier (TJ)",
        xaxis_title="Year",
        yaxis_title="Final Energy (TJ)",
    )
    fig_hh_energy
    return


@app.cell
def _(mo):
    mo.md("""
    ### Observations

    - Household energy was historically **dominated by petroleum products** (heating oil),
      but oil's share fell from ~57% (1990) to ~23% (2024). **Electricity surpassed oil** by 2024 (34% vs 23%).
    - **Electricity** has been rising steadily (partly from heat pump adoption — HPs use electricity).
    - **Other renewables** (includes heat pump ambient heat contribution) growing rapidly (~10% by 2024).
    - Total household energy peaked around **2010** and shows a clear **downward trend** since (~-10% vs 2000).
    """)
    return


# ═══════════════════════════════════════════════════════════════════════
# SPACE-HEATING SHARE
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ### Space-Heating Adjustment

    The BFE energy balance reports **total household energy** (space heating + hot water +
    cooking + appliances + lighting). For our decomposition of **space-heating demand**, we
    apply a correction factor from the BFE/Prognos *Ex-Post-Analyse des schweizerischen
    Energieverbrauchs nach Bestimmungsfaktoren* (annual reports, 2000–2024).

    Space heating's share of household energy varies year-to-year with weather (cold winters
    raise the share) but the trend is downward: from ~71 % (2000) to ~65 % (2024), as heating
    efficiency improved faster than growth in other end uses (appliances, hot water).

    Data downloaded directly from **pubdb.bfe.admin.ch** (publication 12388, Nov 2025).
    """)
    return


@app.cell
def _(RAW_DIR, get_sh_share_fn, load_sh_share):
    df_sh_share = load_sh_share(RAW_DIR / "bfe_hh_energy_by_use_2024.xlsx")
    get_sh_share = get_sh_share_fn(df_sh_share)

    print("Space-heating share loaded from BFE/Prognos Tabelle 1.")
    print(f"  SH share 2000: {get_sh_share(2000):.1%}")
    print(f"  SH share 2012: {get_sh_share(2012):.1%}")
    print(f"  SH share 2024: {get_sh_share(2024):.1%}")
    df_sh_share
    return (get_sh_share,)


# ═══════════════════════════════════════════════════════════════════════
# 2. HEATING DEGREE DAYS
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 2. Heating Degree Days (HDD)

    Source: BFE official population-weighted HDD (1994+) + Zurich Fluntern (pre-1994)

    - **1980-1993**: Zurich Fluntern station (Stadt Zurich open data)
    - **1994-2025**: BFE national population-weighted (opendata.swiss, ogd105)
    - Base: 20/12°C (Swiss standard)
    """)
    return


@app.cell
def _(hdd_path, hdd_zurich_path, load_hdd):
    df_hdd = load_hdd(hdd_path, hdd_zurich_path)
    print(f"HDD data: {df_hdd.shape[0]} years from {df_hdd['year'].min()} to {df_hdd['year'].max()}")
    df_hdd.tail(10)
    return (df_hdd,)


@app.cell
def _(apply_theme, df_hdd, go):
    # HDD trend with OLS trendline
    years = df_hdd["year"].to_list()
    hdds = df_hdd["hdd"].to_list()

    n = len(years)
    sum_x = sum(years)
    sum_y = sum(hdds)
    sum_xy = sum(x * y for x, y in zip(years, hdds))
    sum_x2 = sum(x * x for x in years)
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
    intercept = (sum_y - slope * sum_x) / n
    trend_y = [slope * yr + intercept for yr in years]
    decline_per_decade = slope * 10

    fig_hdd = go.Figure()
    fig_hdd.add_trace(go.Scatter(
        x=years, y=hdds,
        name="HDD (actual)", mode="markers",
        marker=dict(size=8, color="#FF9800"),
    ))
    fig_hdd.add_trace(go.Scatter(
        x=years, y=trend_y,
        name=f"Trend ({decline_per_decade:.0f} HDD/decade)",
        mode="lines",
        line=dict(color="#F44336", width=2, dash="dash"),
    ))

    apply_theme(fig_hdd).update_layout(
        title="Heating Degree Days — Switzerland (base 20/12°C, Zurich Plateau)",
        xaxis_title="Year",
        yaxis_title="HDD",
    )
    fig_hdd
    return


@app.cell
def _(mo):
    mo.md("""
    ### Weather is Getting Warmer

    HDD show a clear declining trend — Switzerland is warming faster than the global average
    (~2.9C above pre-industrial vs ~1.5C globally). This provides a "free" reduction in
    heating demand that is **independent of policy or technology**.

    When analyzing energy trends, we must separate this weather effect from structural
    improvements (insulation, heat pumps). That's why the LMDI decomposition should
    show both raw and HDD-normalized results.
    """)
    return


# ═══════════════════════════════════════════════════════════════════════
# 3. POPULATION
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 3. Population — The P Factor

    Sources:
    - **1960–2009**: World Bank (SP.POP.TOTL) — annual mid-year estimates
    - **2010–2024**: BFS STATPOP (permanent resident population, end-of-year)
    - **2025–2060**: BFS Population Projections (reference, high, low scenarios)

    The extended historical view reveals Switzerland's immigration-driven
    population waves: rapid growth in the 1960s (Italian/Spanish guest workers),
    stagnation in the 1970s (oil crisis + Schwarzenbach initiative), and
    re-acceleration from the 1990s (Yugoslav immigration, EU free movement from 2002).
    """)
    return


@app.cell
def _(RAW_DIR, load_population, pl, pop_path):
    df_pop_full = load_population(pop_path, RAW_DIR / "worldbank_pop_ch.json")
    print(f"Full population series: {df_pop_full.shape[0]} years ({df_pop_full['year'].min()}-{df_pop_full['year'].max()})")

    # Load BFS projections (reference, high, low)
    _proj_path = RAW_DIR / "bfs_pop_projections.csv"
    df_pop_proj = pl.read_csv(_proj_path) if _proj_path.exists() else None
    if df_pop_proj is not None:
        print(f"BFS projections: {df_pop_proj.shape[0]} years ({df_pop_proj['year'].min()}-{df_pop_proj['year'].max()})")

    df_pop_full
    return df_pop_full, df_pop_proj


@app.cell
def _(apply_theme, df_pop_full, df_pop_proj, go):
    fig_pop = go.Figure()

    # Historical data (solid line)
    fig_pop.add_trace(go.Scatter(
        x=df_pop_full["year"].to_list(),
        y=[p / 1_000_000 for p in df_pop_full["population"].to_list()],
        name="Historical",
        mode="lines+markers",
        line=dict(color="#9C27B0", width=3),
        marker=dict(size=4),
    ))

    # BFS projections (if available)
    if df_pop_proj is not None:
        _proj_years = df_pop_proj["year"].to_list()
        # Connect projection to last historical point
        _last_hist_year = df_pop_full["year"].max()
        _last_hist_pop = df_pop_full.filter(df_pop_full["year"] == _last_hist_year)["population"][0] / 1e6

        # High/Low envelope
        _hi = [p / 1e6 for p in df_pop_proj["pop_high"].to_list()]
        _lo = [p / 1e6 for p in df_pop_proj["pop_low"].to_list()]
        fig_pop.add_trace(go.Scatter(
            x=[_last_hist_year] + _proj_years + _proj_years[::-1] + [_last_hist_year],
            y=[_last_hist_pop] + _hi + _lo[::-1] + [_last_hist_pop],
            fill="toself",
            fillcolor="rgba(156, 39, 176, 0.12)",
            line=dict(width=0),
            name="BFS high/low range",
            showlegend=True,
        ))

        # Reference scenario (dashed)
        _ref = [p / 1e6 for p in df_pop_proj["pop_reference"].to_list()]
        fig_pop.add_trace(go.Scatter(
            x=[_last_hist_year] + _proj_years,
            y=[_last_hist_pop] + _ref,
            name="BFS Reference",
            mode="lines",
            line=dict(color="#9C27B0", width=2.5, dash="dash"),
        ))

    # Annotations for key inflection points
    _annotations = [
        (1964, 5.6, "Guest worker wave<br>(IT, ES, PT)", "right"),
        (1974, 6.3, "Oil crisis +<br>Schwarzenbach", "left"),
        (2002, 7.3, "EU free<br>movement", "right"),
    ]
    for _yr, _y, _text, _anchor in _annotations:
        fig_pop.add_annotation(
            x=_yr, y=_y, text=_text,
            showarrow=True, arrowhead=2, arrowsize=0.8,
            ax=40 if _anchor == "right" else -40, ay=-30,
            font=dict(size=10, color="#666"),
        )

    apply_theme(fig_pop).update_layout(
        title="Swiss Population — History (1960–2024) & BFS Projections (2025–2060)",
        xaxis_title="Year",
        yaxis_title="Population (millions)",
    )
    fig_pop
    return


# ═══════════════════════════════════════════════════════════════════════
# 4. HEATING MIX (Floor Area Shares)
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 4. Heating Mix — Floor Area Share by Heating System

    **Sources (automated pipeline):**
    1. **BFE/Prognos Tabelle 13** (2000–2024): Energiebezugsfläche (EBF) by heating system — annual, Mio m²
    2. **BFE/Prognos Tabelle 11** (2000–2024): Space heating energy (PJ) by carrier — for cross-check
    3. **BFS Census via PxWeb** (1990, 2000): Building counts by heating energy source — for pre-2000 context
    4. **BFS GWS Excel** (2000, 2021): Building counts by heating system & energy source — for census cross-check

    The primary metric is **floor area share (%)** from Tabelle 13, which is more meaningful for
    IPAT analysis than raw building counts (a large MFH matters more than a small EFH).

    > **Caveat:** Floor area shares differ from building count shares (BFS GWR).
    > Heat pumps dominate new large MFH construction, so their floor area share (~29% in 2024)
    > exceeds their building count share (~23%). Oil remains #1 by building count (35%).
    """)
    return


@app.cell
def _(RAW_DIR, load_heating_mix):
    df_mix = load_heating_mix(RAW_DIR / "bfe_hh_energy_by_use_2024.xlsx")
    df_mix
    return (df_mix,)


@app.cell
def _(RAW_DIR, load_heating_energy):
    df_heating_energy_pct = load_heating_energy(RAW_DIR / "bfe_hh_energy_by_use_2024.xlsx")
    df_heating_energy_pct
    return


@app.cell
def _(DATA_DIR, download_json, json, mo, pl):
    # BFS Census — Building counts by heating energy source, 1990 & 2000
    census_path = download_json(
        DATA_DIR,
        "https://www.pxweb.bfs.admin.ch/api/v1/de/px-x-0902020100_122/px-x-0902020100_122.px",
        "bfs_census_buildings_heating.json",
        payload={
            "query": [
                {"code": "Kanton", "selection": {"filter": "item", "values": ["00"]}},
                {"code": "Energieträger der Heizung", "selection": {
                    "filter": "item", "values": ["1", "2", "3", "4", "5", "9"]
                }},
                {"code": "Jahr", "selection": {"filter": "item", "values": ["1990", "2000"]}},
            ],
            "response": {"format": "json"},
        },
    )

    raw_census = json.loads(census_path.read_text())
    code_to_carrier = {
        "1": "oil", "2": "gas", "3": "electric",
        "4": "wood_coal", "5": "other", "9": "none",
    }

    _census_records = []
    for _entry in raw_census["data"]:
        _carrier_code = _entry["key"][1]
        _year = int(_entry["key"][2])
        _count = int(_entry["values"][0]) if _entry["values"][0] != "..." else 0
        _census_records.append({"year": _year, "carrier": code_to_carrier.get(_carrier_code, _carrier_code), "buildings": _count})

    df_census = (
        pl.DataFrame(_census_records)
        .pivot(on="carrier", index="year", values="buildings")
        .sort("year")
    )

    mo.md(f"""
    ### BFS Census — Buildings by Heating Energy Source (1990 & 2000)

    Note: Census categories are coarser — "Elektrizität" includes both heat pumps and resistance
    heating, "Holz, Kohle" is combined. These serve as a historical anchor, not the primary metric.

    {mo.as_html(df_census)}
    """)
    return


@app.cell
def _(MIX_CARRIERS, MIX_COLORS, MIX_LABELS, apply_theme, df_mix, go):
    fig_mix = go.Figure()
    for _carrier in MIX_CARRIERS:
        fig_mix.add_trace(go.Scatter(
            x=df_mix["year"].to_list(),
            y=df_mix[_carrier].to_list(),
            name=MIX_LABELS[_carrier],
            mode="lines",
            stackgroup="one",
            line=dict(width=0.5, color=MIX_COLORS[_carrier]),
            fillcolor=MIX_COLORS[_carrier],
        ))

    apply_theme(fig_mix).update_layout(
        title="Swiss Residential Heating — Floor Area Share by System (%, BFE/Prognos 2025)",
        xaxis_title="Year",
        yaxis_title="Share of Floor Area (%)",
        yaxis=dict(range=[0, 100]),
    )
    fig_mix
    return


@app.cell
def _(mo):
    mo.md("""
    ### Key Observations — Heating Mix

    **Important: this chart shows floor area shares (BFE/Prognos Tabelle 13), not building counts.**

    - **Oil floor area halved**: 59.9% (2000) → 23.9% (2024) — still #1 by building count (35%)
    - **Heat pumps lead by floor area** (28.9%) but not by building count (~23%)
    - **Gas peaked ~2022** at ~27% and is declining (energy crisis + cantonal fossil bans)
    - **Wood + district heating growing steadily**: combined ~12% → ~16%
    - **Electric resistance flat** at ~5–7% — legacy stock, no new installs
    """)
    return


# ═══════════════════════════════════════════════════════════════════════
# 5. DECOUPLING ANALYSIS
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 5. Decoupling Analysis — Energy Demand vs GDP

    The core IPAT question: is residential heating energy (I) decoupling from
    economic growth (P x A)?

    All series indexed to base year 2000 = 100.
    """)
    return


@app.cell
def _(RAW_DIR, load_floor_area, load_gdp):
    df_floor_area = load_floor_area(RAW_DIR / "floor_area_by_building_category.xlsx")
    df_wb_gdp = load_gdp(RAW_DIR / "worldbank_gdp_ch.json")
    print(f"Floor area data: {df_floor_area.shape[0]} years ({df_floor_area['year'].min()}-{df_floor_area['year'].max()})")
    print(f"World Bank GDP: {df_wb_gdp.shape[0]} years ({df_wb_gdp['year'].min()}-{df_wb_gdp['year'].max()})")
    return df_floor_area, df_wb_gdp


@app.cell
def _(DECOUPLE_SERIES, apply_theme, df_floor_area, df_hh, df_pop_full, df_wb_gdp, get_sh_share, go, pl):
    # Build the decoupling chart from REAL data
    _df_hh_yearly = (
        df_hh
        .group_by("Jahr")
        .agg(pl.col("TJ").sum().alias("hh_TJ"))
        .sort("Jahr")
        .filter(pl.col("Jahr") >= 2000)
        .rename({"Jahr": "year"})
    )
    _sh_shares = [get_sh_share(y) for y in _df_hh_yearly["year"].to_list()]
    _df_hh_yearly = _df_hh_yearly.with_columns(
        (pl.col("hh_TJ") * pl.Series("_sh", _sh_shares)).alias("total_TJ"),
    )

    _df_gdp = df_wb_gdp.select(pl.col("year"), pl.col("gdp_bn_chf").alias("gdp_bn"))
    _df_pop = df_pop_full.filter(pl.col("year") >= 2000)

    # Back-extrapolate floor area for 2000–2011
    _m2pp_2012 = df_floor_area.filter(pl.col("year") == 2012)["m2_per_person_avg"][0]
    _floor_pre_records = []
    for _row in _df_pop.filter(pl.col("year") < 2012).iter_rows(named=True):
        _yr, _pop = _row["year"], _row["population"]
        _m2pp = _m2pp_2012 * (1 - 0.003) ** (2012 - _yr)
        _floor_pre_records.append({"year": _yr, "floor_area_mio_m2": round(_m2pp * _pop / 1e6, 1)})
    _floor_hardcoded = pl.DataFrame(_floor_pre_records)

    _df_floor_real = (
        df_floor_area
        .select("year", "m2_per_person_avg")
        .join(_df_pop.select("year", "population"), on="year", how="left")
        .with_columns(
            (pl.col("m2_per_person_avg") * pl.col("population") / 1e6).round(1).alias("floor_area_mio_m2"),
        )
        .select("year", "floor_area_mio_m2")
    )
    _df_floor = pl.concat([_floor_hardcoded, _df_floor_real]).sort("year")

    _df_decoupling = (
        _df_hh_yearly
        .join(_df_gdp, on="year", how="left")
        .join(_df_pop, on="year", how="left")
        .join(_df_floor, on="year", how="left")
    )

    _base = _df_decoupling.filter(pl.col("year") == 2000)
    df_indexed = _df_decoupling.with_columns(
        (pl.col("total_TJ") / _base["total_TJ"][0] * 100).alias("energy_idx"),
        (pl.col("gdp_bn") / _base["gdp_bn"][0] * 100).alias("gdp_idx"),
        (pl.col("population") / _base["population"][0] * 100).alias("pop_idx"),
        (pl.col("floor_area_mio_m2") / _base["floor_area_mio_m2"][0] * 100).alias("floor_idx"),
    ).with_columns(
        (pl.col("energy_idx") / pl.col("floor_idx") * 100).alias("intensity_idx"),
    )

    _fig_decouple = go.Figure()
    for _col, _name, _color, _dash, _width in DECOUPLE_SERIES:
        _fig_decouple.add_trace(go.Scatter(
            x=df_indexed["year"].to_list(),
            y=df_indexed[_col].to_list(),
            name=_name,
            mode="lines+markers",
            line=dict(color=_color, width=_width, dash=_dash),
            marker=dict(size=4),
        ))
    _fig_decouple.add_hline(y=100, line_dash="dot", line_color="gray", opacity=0.5)

    # Policy milestones — stagger y to avoid overlap when years are close
    _policy_milestones = [
        (2007, "SIA 380/1",       1.02),
        (2008, "CO\u2082 levy",   1.10),  # stagger up — only 1 yr from SIA
        (2010, "Buildings Prog.", 1.02),
        (2015, "MuKEn 2014",      1.02),
        (2022, "CHF 120/t CO\u2082", 1.02),
    ]
    for _yr, _text, _ypos in _policy_milestones:
        _fig_decouple.add_vline(x=_yr, line_dash="dot", line_color="rgba(0,0,0,0.12)")
        _fig_decouple.add_annotation(
            x=_yr, y=_ypos, yref="paper", text=_text,
            showarrow=False, font=dict(size=8, color="#555"),
            textangle=-35, xanchor="left", yanchor="bottom",
        )

    apply_theme(_fig_decouple).update_layout(
        title="Decoupling: Space-Heating Energy vs Economic Growth (2000 = 100)",
        xaxis_title="Year",
        yaxis_title="Index (2000 = 100)",
        margin=dict(t=110),
    )
    _fig_decouple
    return (df_indexed,)


@app.cell
def _(df_indexed, mo):
    last = df_indexed.filter(df_indexed["year"] == df_indexed["year"].max())
    energy_change = last["energy_idx"][0] - 100
    gdp_change = last["gdp_idx"][0] - 100
    pop_change = last["pop_idx"][0] - 100
    floor_change = last["floor_idx"][0] - 100
    intensity_change = last["intensity_idx"][0] - 100

    mo.md(
        f"""
        ### Key Finding — Absolute Decoupling

        Since 2000 (all series indexed to 2000 = 100):

        | Indicator | Change | Why this value |
        |-----------|-------:|----------------|
        | **GDP (real)** | +{gdp_change:.0f}% | Steady Swiss economic growth; services and pharma drove output despite a strong franc |
        | **Population** | +{pop_change:.0f}% | Driven primarily by net immigration; Switzerland grew from 7.2 M to ~9.0 M |
        | **Heated floor area** | +{floor_change:.0f}% | Rising affluence → larger dwellings + more single-person households → more m² per capita |
        | **Space-heating energy** | {energy_change:+.0f}% | Despite upward pressure from P and A, heating energy **fell** — absolute decoupling |
        | **Energy intensity** | {intensity_change:+.0f}% | Energy per m² declined thanks to insulation retrofits, heat-pump adoption, and warmer winters |

        **Absolute decoupling confirmed**: the Technology factor (T) is declining fast enough
        to more than offset growth in Population (P) and Affluence (A).
        """
    )
    return


# ═══════════════════════════════════════════════════════════════════════
# 6–8. FLOOR AREA, BUILDINGS, BUILDING STANDARDS
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 6. BFS Floor Area per Person (2012-2024)

    Source: BFS GWS — T 09.03.02.04.03
    """)
    return


@app.cell
def _(apply_theme, df_floor_area, go):
    fig_floor = go.Figure()
    fig_floor.add_trace(go.Scatter(
        x=df_floor_area["year"].to_list(),
        y=df_floor_area["m2_per_person_sfh"].to_list(),
        name="Single-Family Houses",
        mode="lines+markers", line=dict(color="#FF9800", width=2.5), marker=dict(size=6),
    ))
    fig_floor.add_trace(go.Scatter(
        x=df_floor_area["year"].to_list(),
        y=df_floor_area["m2_per_person_mfh"].to_list(),
        name="Multi-Family Buildings",
        mode="lines+markers", line=dict(color="#2196F3", width=2.5), marker=dict(size=6),
    ))
    fig_floor.add_trace(go.Scatter(
        x=df_floor_area["year"].to_list(),
        y=df_floor_area["m2_per_person_avg"].to_list(),
        name="Weighted Average (~30/70)",
        mode="lines+markers", line=dict(color="#4CAF50", width=3, dash="dash"), marker=dict(size=5),
    ))
    apply_theme(fig_floor).update_layout(
        title="Average Floor Area per Person — Swiss Residential Buildings (BFS GWS)",
        xaxis_title="Year", yaxis_title="m² per person",
    )
    fig_floor
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 7. BFS Buildings by Heating Source — 2000 vs 2021
    """)
    return


@app.cell
def _(BUILDING_HEAT_COLORS, RAW_DIR, apply_theme, go, load_buildings_heating):
    df_heating_compare = load_buildings_heating(RAW_DIR / "buildings_heating_source_2000_2021.xlsx")

    _sources = df_heating_compare["source"].to_list()
    _v2000 = df_heating_compare["buildings_2000"].to_list()
    _v2021 = df_heating_compare["buildings_2021"].to_list()

    fig_heating_cmp = go.Figure()
    fig_heating_cmp.add_trace(go.Bar(
        x=_sources, y=[v / 1000 for v in _v2000], name="2000",
        marker_color="#BDBDBD",
        marker_line=dict(color="#757575", width=1.5),
    ))
    fig_heating_cmp.add_trace(go.Bar(
        x=_sources, y=[v / 1000 for v in _v2021], name="2021",
        marker_color=[BUILDING_HEAT_COLORS.get(s, "#999") for s in _sources],
    ))
    apply_theme(fig_heating_cmp).update_layout(
        title="Residential Buildings by Heating Energy Source \u2014 2000 vs 2021 (BFS GWS)",
        xaxis_title="Energy Source", yaxis_title="Number of Buildings (thousands)",
        barmode="group",
    )
    fig_heating_cmp
    return (df_heating_compare,)


@app.cell
def _(mo):
    mo.md("""
    ### Key Changes 2000 to 2021

    - **Heat pumps**: 60k to 302k buildings (+403%) — the dominant growth story
    - **Heating oil**: 815k to 723k (-11%) — still the largest single source but declining
    - **Gas**: 200k to 312k (+56%) — grew but now peaked (post-2018 decline)
    - **District heating**: 21k to 64k (+210%) — tripled but still small in absolute terms
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 8. Building Standards Evolution — kWh/m2 Limits
    """)
    return


@app.cell
def _(apply_theme, go):
    standards = {
        "year": [1970, 1975, 2000, 2008, 2014],
        "limit_kwh_m2": [250, 180, 90, 60, 16],
        "label": ["No regulation<br>(~250)", "First SIA norm<br>(~180)",
                  "MuKEn 2000<br>(~90)", "MuKEn 2008<br>(~60)", "MuKEn 2014<br>(16)"],
    }
    fig_standards = go.Figure()
    fig_standards.add_trace(go.Bar(
        x=standards["year"], y=standards["limit_kwh_m2"],
        text=standards["label"], textposition="outside",
        marker_color=["#F44336", "#FF9800", "#FFC107", "#4CAF50", "#2196F3"],
        width=4,
    ))
    apply_theme(fig_standards).update_layout(
        title="New Building Heating Energy Limit (kWh/m2/yr) — Swiss Standards",
        xaxis_title="Year", yaxis_title="Max Heating Energy (kWh/m2/yr)",
        yaxis=dict(range=[0, 310]),
    )
    fig_standards
    return


@app.cell
def _(apply_theme, go, make_subplots):
    age_data = {
        "period": ["Pre-1919", "1919-1945", "1946-1960", "1961-1970", "1971-1980",
                    "1981-1990", "1991-2000", "2001-2010", "2011-2020", "2021+"],
        "share": [12, 8, 10, 14, 16, 11, 9, 8, 9, 3],
        "typical_kwh_m2": [220, 200, 180, 160, 140, 100, 80, 45, 25, 16],
    }
    eff_colors = ["#F44336" if k > 150 else "#FF9800" if k > 80 else "#4CAF50"
                  for k in age_data["typical_kwh_m2"]]

    fig_stock = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Building Stock by Construction Period (%)", "Typical Energy Demand (kWh/m2/yr)"),
        horizontal_spacing=0.12,
    )
    fig_stock.add_trace(go.Bar(x=age_data["period"], y=age_data["share"], marker_color=eff_colors, showlegend=False), row=1, col=1)
    fig_stock.add_trace(go.Bar(x=age_data["period"], y=age_data["typical_kwh_m2"], marker_color=eff_colors, showlegend=False), row=1, col=2)
    apply_theme(fig_stock).update_layout(title="Swiss Building Stock: Age Distribution & Energy Performance")
    fig_stock.update_yaxes(title_text="Share (%)", row=1, col=1)
    fig_stock.update_yaxes(title_text="kWh/m2/yr", row=1, col=2)
    fig_stock.update_xaxes(tickangle=45)
    fig_stock
    return


@app.cell
def _(mo):
    mo.md("""
    ### The Inertia Problem

    - **60% of buildings built before 1980** — most with poor insulation (140-220 kWh/m2)
    - Current renovation rate: **0.9-1.4%/year** — would take **~100 years** to renovate all
    - Net-zero by 2050 requires **~3%/year** — more than double current rate
    """)
    return


# ═══════════════════════════════════════════════════════════════════════
# 8b. EFH vs MFH — BUILDING TYPE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 8b. EFH vs MFH — Building Type Analysis

    The aggregate heating statistics mask a critical structural divide: single-family
    houses (EFH) and multi-family buildings (MFH) differ profoundly in their
    decarbonisation trajectories.

    **Key asymmetry (GWR 2024, 1.8 M residential buildings):**

    | Category | Code | Buildings | Population share |
    |----------|------|-----------|-----------------|
    | Single-Family (*Einfamilienhaus*, EFH) | 1021 | 1,019k (57%) | ~27% |
    | Multi-Family (*Mehrfamilienhaus*, MFH) | 1025 | 501k (28%) | ~53% |
    | Mixed-Use Residential (shop on ground floor) | 1030 | 200k (11%) | ~12% |
    | Partial Residential (offices with some flats) | 1040 | 80k (4%) | ~8% |

    MFH and mixed-use buildings house the majority of the population but face distinct
    barriers to heat pump adoption that do not apply to single-family houses.

    **Data source:** Swiss Federal Register of Buildings and Dwellings (GWR), accessed
    via the stats.swiss SDMX API (dataflow `DF_GWS_REG4`, 2021–2024).
    """)
    return


@app.cell
def _(gwr_heating_path, load_gwr_heating_by_type):
    df_gwr_by_type = load_gwr_heating_by_type(gwr_heating_path)
    print(f"GWR data: {df_gwr_by_type.shape[0]} rows, "
          f"years {df_gwr_by_type['year'].unique().sort().to_list()}")
    df_gwr_by_type.head(20)
    return (df_gwr_by_type,)


@app.cell
def _(BUILDING_HEAT_COLORS, apply_theme, df_gwr_by_type, go, make_subplots, pl):
    # fig15: Two-panel chart
    #   Left: 100% stacked bars — heating source by building category (2024)
    #   Right: HP adoption trend 2021→2024 by category (slope chart)

    _latest = df_gwr_by_type.filter(pl.col("year") == df_gwr_by_type["year"].max())
    _yr = int(_latest["year"].max())
    _source_order = ["Heating Oil", "Gas", "Heat Pump", "Wood", "Electricity",
                     "District Heating", "Solar Thermal", "Other"]
    _cat_order = ["Single-Family (EFH)", "Multi-Family (MFH)",
                  "Mixed-Use Residential", "Partial Residential"]
    _cat_short = {"Single-Family (EFH)": "Single-Family\n(EFH)",
                  "Multi-Family (MFH)": "Multi-Family\n(MFH)",
                  "Mixed-Use Residential": "Mixed-Use\nResidential",
                  "Partial Residential": "Partial\nResidential"}

    fig_heating_by_type = make_subplots(
        rows=1, cols=2, column_widths=[0.55, 0.45],
        subplot_titles=(
            f"Heating Source by Building Category ({_yr})",
            "Heat Pump Adoption Trend (2021–2024)",
        ),
        horizontal_spacing=0.12,
    )

    # ── Left panel: 100% stacked horizontal bars ──
    for _src in _source_order:
        _pcts = []
        for _cat in _cat_order:
            _sub = _latest.filter(
                (pl.col("building_type") == _cat) & (pl.col("heating_source") == _src)
            )
            _count = _sub["building_count"].sum() if len(_sub) > 0 else 0
            _total = _latest.filter(pl.col("building_type") == _cat)["building_count"].sum()
            _pcts.append(round(_count / _total * 100, 1) if _total > 0 else 0)

        _color = BUILDING_HEAT_COLORS.get(_src, "#999")
        fig_heating_by_type.add_trace(go.Bar(
            y=[_cat_short[c] for c in _cat_order], x=_pcts, orientation="h",
            name=_src, marker_color=_color, legendgroup=_src,
            text=[f"{p:.0f}%" if p >= 4 else "" for p in _pcts],
            textposition="inside", textfont=dict(color="white", size=11),
            showlegend=True,
        ), row=1, col=1)

    # Total building count annotations on left panel
    for _i, _cat in enumerate(_cat_order):
        _total = _latest.filter(pl.col("building_type") == _cat)["building_count"].sum()
        fig_heating_by_type.add_annotation(
            x=102, y=_cat_short[_cat], text=f"<b>n={_total/1000:.0f}k</b>",
            showarrow=False, font=dict(size=10, color="#444"),
            xref="x", yref="y",
        )

    # ── Right panel: HP adoption slope chart ──
    _hp_colors = {
        "Single-Family (EFH)": "#FF9800",
        "Multi-Family (MFH)": "#2196F3",
        "Mixed-Use Residential": "#9C27B0",
        "Partial Residential": "#607D8B",
    }
    _years = sorted(df_gwr_by_type["year"].unique().to_list())

    for _cat in _cat_order:
        _hp_pcts = []
        for _y in _years:
            _ysub = df_gwr_by_type.filter(
                (pl.col("year") == _y) & (pl.col("building_type") == _cat)
            )
            _hp = _ysub.filter(pl.col("heating_source") == "Heat Pump")["building_count"].sum()
            _tot = _ysub["building_count"].sum()
            _hp_pcts.append(round(_hp / _tot * 100, 1) if _tot > 0 else 0)

        fig_heating_by_type.add_trace(go.Scatter(
            x=_years, y=_hp_pcts, name=_cat, mode="lines+markers+text",
            line=dict(color=_hp_colors[_cat], width=2.5),
            marker=dict(size=8, color=_hp_colors[_cat]),
            text=[f"{p:.0f}%" if i in (0, len(_years)-1) else "" for i, p in enumerate(_hp_pcts)],
            textposition="top center", textfont=dict(size=10, color=_hp_colors[_cat]),
            showlegend=False,
        ), row=1, col=2)

    apply_theme(fig_heating_by_type).update_layout(
        barmode="stack", height=500, width=1300,
        margin=dict(l=170, t=85),
        legend=dict(orientation="h", y=-0.10, x=0.28, xanchor="center", font=dict(size=11)),
    )
    fig_heating_by_type.update_xaxes(title_text="Share (%)", range=[0, 108], row=1, col=1)
    fig_heating_by_type.update_xaxes(title_text="Year", dtick=1, row=1, col=2)
    fig_heating_by_type.update_yaxes(title_text="Heat Pump Share (%)", row=1, col=2)
    fig_heating_by_type
    return (fig_heating_by_type,)


@app.cell
def _(mo):
    mo.md("""
    ### Heat Pump Adoption: A Four-Speed Transition

    The GWR data (2021–2024) reveals a clear hierarchy in heat pump adoption speed:

    | Building Category | HP Share 2021 | HP Share 2024 | Δ (3 yr) |
    |-------------------|--------------|--------------|----------|
    | Single-Family (EFH) | 20.9% | 27.8% | **+6.9 pp** |
    | Multi-Family (MFH) | 14.8% | 20.5% | **+5.7 pp** |
    | Mixed-Use Residential | 7.2% | 10.9% | +3.7 pp |
    | Partial Residential | 6.2% | 9.0% | +2.8 pp |

    EFH are leading the transition — but **all categories are accelerating**.
    The gap between EFH and mixed-use/partial buildings (18 pp) reflects
    compounding structural barriers:

    **Barriers beyond EFH:**
    1. **Split incentive** (principal–agent problem): The landlord pays the CAPEX for a
       heating system replacement, but the tenant benefits from lower *Nebenkosten*
       (heating costs). This decouples the investment decision from the energy savings.
    2. **Technical constraints**: Large MFH require higher heating capacity; air-source
       HPs face noise constraints in dense urban settings; ground-source HPs need
       drilling permits and outdoor space.
    3. **Coordination costs**: *Stockwerkeigentum* (condominium) buildings require
       supermajority owner agreement for major investments — a collective action problem.
    4. **Temperature requirements**: Older MFH often have radiator-based distribution
       designed for 55–70 °C flow temperatures, which reduces HP efficiency (COP drops
       from ~3.5 to ~2.5). Retrofit to underfloor heating is expensive and disruptive.
    5. **Mixed-use complexity**: Buildings with commercial ground floors (cat. 1030)
       have different heating profiles per storey and may require separate systems.

    **Policy implication:** Non-EFH buildings house ~73% of the population but
    adopt heat pumps at half the rate. Targeted instruments are needed: biofuels
    as a transitional fuel where HP don't fit, mandatory replacement-at-end-of-life
    rules (as in several cantons), or subsidies that address the split incentive
    (e.g., allowing landlords to pass through green CAPEX via *Mietzinserhöhung*).
    """)
    return


@app.cell
def _(BUILDING_TYPE_COLORS, RAW_DIR, apply_theme, go, load_floor_area_by_period):
    # fig16: Floor area per person by construction period — EFH vs MFH
    df_fa_period = load_floor_area_by_period(RAW_DIR / "floor_area_by_building_category.xlsx")

    _periods = df_fa_period["period"].to_list()
    _efh = df_fa_period["m2_efh"].to_list()
    _mfh = df_fa_period["m2_mfh"].to_list()

    fig_floor_period = go.Figure()
    fig_floor_period.add_trace(go.Bar(
        x=_periods, y=_efh, name="EFH (Single-Family)",
        marker_color=BUILDING_TYPE_COLORS["EFH"],
        text=[f"{v:.0f}" for v in _efh], textposition="outside",
        textfont=dict(size=10),
    ))
    fig_floor_period.add_trace(go.Bar(
        x=_periods, y=_mfh, name="MFH (Multi-Family)",
        marker_color=BUILDING_TYPE_COLORS["MFH"],
        text=[f"{v:.0f}" for v in _mfh], textposition="outside",
        textfont=dict(size=10),
    ))

    # National average line
    fig_floor_period.add_hline(
        y=46.6, line_dash="dash", line_color="#4CAF50", opacity=0.7,
        annotation_text="National avg: 46.6 m²", annotation_position="top left",
        annotation_font=dict(size=10, color="#4CAF50"),
    )

    apply_theme(fig_floor_period).update_layout(
        title="Floor Area per Person by Construction Period — EFH vs MFH (BFS GWS 2024)",
        xaxis_title="Construction Period", yaxis_title="m² per person",
        barmode="group", yaxis=dict(range=[0, 72]),
    )
    fig_floor_period.update_xaxes(tickangle=35)
    fig_floor_period
    return (fig_floor_period,)


@app.cell
def _(mo):
    mo.md("""
    ### The Affluence Gap

    Floor area per person is systematically higher in EFH than MFH across all
    construction periods. As of 2024, EFH residents occupy **55.4 m²/person** vs
    **43.4 m²/person** in MFH — a **28% premium**.

    This gap reflects both self-selection (wealthier households choose EFH) and
    structural differences (EFH are designed for single families with more rooms
    per person). From an IPAT perspective, this means the **A (Affluence)** factor
    has a spatial dimension: the building type you live in determines your per-capita
    floor area, which directly scales heating demand.

    **For the LMDI decomposition**, this implies that the "floor area per capita"
    factor is not uniform across the building stock. A shift toward denser MFH
    living (driven by urbanisation and immigration) would structurally reduce
    per-capita floor area and hence energy demand — even without any efficiency
    improvement.
    """)
    return


# ═══════════════════════════════════════════════════════════════════════
# 8c. CANTONAL HEAT PUMP MAP
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ### 8c. Cantonal Heat Pump Adoption Map

    The GWR SDMX API provides canton-level building data, enabling a spatial
    view of the energy transition. We map **heat pump share (% of buildings)**
    for each of the 26 cantons, revealing the geographic heterogeneity behind
    the national averages shown above.

    This connects to MuKEn adoption timing: cantons that implemented MuKEn 2014
    earlier tend to show higher HP penetration.
    """)
    return


@app.cell
def _(canton_topo_path, gwr_canton_path, load_gwr_canton_hp_share, topojson_to_geojson_cantons):
    # Convert TopoJSON → GeoJSON with canton properties
    ch_geojson = topojson_to_geojson_cantons(canton_topo_path)

    # Compute HP share by canton for latest year
    df_canton_hp = load_gwr_canton_hp_share(gwr_canton_path, year=2024)
    print(f"Canton HP data: {df_canton_hp.shape[0]} cantons")
    print(df_canton_hp.select("canton_abbr", "canton_name", "hp_share", "total_buildings").head(5))
    return ch_geojson, df_canton_hp


@app.cell
def _(apply_theme, ch_geojson, df_canton_hp, go, px):
    # Choropleth map — HP adoption by canton
    fig_canton_map = px.choropleth(
        df_canton_hp.to_pandas(),
        geojson=ch_geojson,
        locations="canton_id",
        featureidkey="properties.canton_id",
        color="hp_share",
        hover_name="canton_name",
        hover_data={"hp_share": ":.1f", "total_buildings": ":,", "canton_id": False},
        color_continuous_scale=[
            [0.0, "#F44336"],    # red — low HP
            [0.35, "#FF9800"],   # orange
            [0.55, "#FFC107"],   # yellow
            [0.75, "#8BC34A"],   # light green
            [1.0, "#2E7D32"],    # dark green — high HP
        ],
        labels={"hp_share": "HP Share (%)"},
    )

    fig_canton_map.update_geos(
        fitbounds="locations",
        visible=False,
        bgcolor="rgba(0,0,0,0)",
    )

    # Add canton abbreviation labels at centroids
    _centroids: dict[str, tuple[float, float]] = {
        "ZH":(8.55,47.37),"BE":(7.45,46.95),"LU":(8.30,47.05),"UR":(8.64,46.77),
        "SZ":(8.65,47.02),"OW":(8.25,46.88),"NW":(8.38,46.93),"GL":(9.07,46.98),
        "ZG":(8.52,47.17),"FR":(7.11,46.80),"SO":(7.54,47.33),"BS":(7.59,47.56),
        "BL":(7.67,47.45),"SH":(8.64,47.70),"AR":(9.38,47.38),"AI":(9.41,47.32),
        "SG":(9.38,47.25),"GR":(9.53,46.66),"AG":(8.07,47.39),"TG":(9.10,47.58),
        "TI":(8.95,46.30),"VD":(6.63,46.62),"VS":(7.60,46.23),"NE":(6.86,46.99),
        "GE":(6.15,46.20),"JU":(7.16,47.35),
    }
    for _, row in df_canton_hp.to_pandas().iterrows():
        _abbr = row["canton_abbr"]
        if _abbr in _centroids:
            _lon, _lat = _centroids[_abbr]
            fig_canton_map.add_trace(go.Scattergeo(
                lon=[_lon], lat=[_lat],
                text=[_abbr],
                mode="text",
                textfont=dict(size=8, color="#333", family="Inter, Helvetica, sans-serif"),
                showlegend=False,
                hoverinfo="skip",
            ))

    apply_theme(fig_canton_map).update_layout(
        title="Heat Pump Adoption by Canton (% of buildings, 2024)",
        height=600, width=800,
        margin=dict(l=10, r=10, t=80, b=10),
        coloraxis_colorbar=dict(
            title="HP Share (%)",
            thickness=15,
            len=0.6,
            y=0.5,
        ),
        geo=dict(
            projection_type="mercator",
            lonaxis_range=[5.8, 10.6],
            lataxis_range=[45.8, 47.9],
        ),
    )
    fig_canton_map
    return (fig_canton_map,)


@app.cell
def _(df_canton_hp, mo):
    _top = df_canton_hp.sort("hp_share", descending=True).head(5)
    _bot = df_canton_hp.sort("hp_share").head(5)

    _top_rows = "\n".join(
        f"        | {r['canton_name']} ({r['canton_abbr']}) | {r['hp_share']:.1f}% | {r['total_buildings']:,} |"
        for r in _top.to_dicts()
    )
    _bot_rows = "\n".join(
        f"        | {r['canton_name']} ({r['canton_abbr']}) | {r['hp_share']:.1f}% | {r['total_buildings']:,} |"
        for r in _bot.to_dicts()
    )

    _spread = _top["hp_share"][0] - _bot["hp_share"][0]
    _nat_avg = (df_canton_hp["hp_buildings"].sum() / df_canton_hp["total_buildings"].sum() * 100)

    mo.md(
        f"""
        ### Cantonal Disparities in Heat Pump Adoption

        National average: **{_nat_avg:.1f}%** of buildings heated by HP (2024).
        The spread between the leading and lagging canton is **{_spread:.0f} pp**.

        **Top 5 cantons** (highest HP share):

        | Canton | HP Share | Buildings |
        |--------|--------:|----------:|
{_top_rows}

        **Bottom 5 cantons** (lowest HP share):

        | Canton | HP Share | Buildings |
        |--------|--------:|----------:|
{_bot_rows}

        Urban cantons with dense MFH stock (Basel-Stadt, Genève) tend to lag due to
        space constraints and the split-incentive problem. Rural cantons with
        predominantly EFH stock show higher adoption — consistent with the
        "four-speed transition" pattern from fig15.
        """
    )
    return


# ═══════════════════════════════════════════════════════════════════════
# 9. GDP + CROSS-VALIDATION
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(apply_theme, df_wb_gdp, go):
    fig_wb_gdp = go.Figure()
    fig_wb_gdp.add_trace(go.Scatter(
        x=df_wb_gdp["year"].to_list(),
        y=df_wb_gdp["gdp_bn_chf"].to_list(),
        name="GDP (constant CHF)",
        mode="lines+markers", line=dict(color="#E91E63", width=3), marker=dict(size=5),
    ))
    apply_theme(fig_wb_gdp).update_layout(
        title="Swiss GDP — World Bank (constant LCU, billion CHF)",
        xaxis_title="Year", yaxis_title="GDP (billion CHF, constant prices)",
    )
    fig_wb_gdp
    return


@app.cell
def _(RAW_DIR, json, mo, pl, pop_path):
    # Population cross-validation — BFS vs World Bank
    _bfs_data = json.loads(pop_path.read_text())
    _bfs_records = [
        {"year": int(e["key"][0]), "bfs_population": int(e["values"][0])}
        for e in _bfs_data.get("data", [])
        if e["values"][0] and e["values"][0] != "..."
    ]
    _df_bfs = pl.DataFrame(_bfs_records).sort("year")

    _wb_raw = json.loads((RAW_DIR / "worldbank_pop_ch.json").read_text())
    _wb_records = [
        {"year": int(e["date"]), "wb_population": int(e["value"])}
        for e in _wb_raw[1] if e["value"] is not None
    ]
    _df_wb = pl.DataFrame(_wb_records).sort("year")

    df_pop_validation = _df_bfs.join(_df_wb, on="year", how="inner").with_columns(
        ((pl.col("wb_population") - pl.col("bfs_population")) / pl.col("bfs_population") * 100).round(2).alias("diff_pct"),
    )
    _max_diff = df_pop_validation["diff_pct"].abs().max()
    mo.md(f"""
    ### Population Cross-Validation

    Maximum BFS vs World Bank difference: **{_max_diff:.2f}%** — both sources consistent.
    """)
    return


# ═══════════════════════════════════════════════════════════════════════
# 14. LMDI DECOMPOSITION
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(USE_LMDI_4FACTOR, mo):
    _n = "4" if USE_LMDI_4FACTOR else "3"
    if USE_LMDI_4FACTOR:
        _formula = r"$$E = P \times \frac{A}{P} \times HDD \times \frac{E}{A \cdot HDD}$$"
        _factors = (
            r"- **Population effect** ($\Delta E_{\text{pop}}$): more people → more demand" "\n"
            r"    - **Floor-area effect** ($\Delta E_{\text{floor}}$): rising m² per capita → more space to heat" "\n"
            r"    - **Weather effect** ($\Delta E_{\text{weather}}$): warmer winters → less demand" "\n"
            r"    - **Intensity effect** ($\Delta E_{\text{int}}$): technology & behaviour (insulation, heat pumps, efficiency per m²·HDD)"
        )
    else:
        _formula = r"$$E = P \times \frac{E}{P \cdot HDD} \times HDD$$"
        _factors = (
            r"- **Population effect** ($\Delta E_{\text{pop}}$): more people → more demand" "\n"
            r"    - **Weather effect** ($\Delta E_{\text{weather}}$): warmer winters → less demand" "\n"
            r"    - **Intensity effect** ($\Delta E_{\text{int}}$): technology & behaviour (insulation, heat pumps, efficiency)"
        )
    mo.md(rf"""
    ---
    ## 14. LMDI-I Decomposition — {_n}-Factor Model

    **Method**: Logarithmic Mean Divisia Index (additive, Ang 2004)

    We decompose the change in **space-heating energy** (household total × SH share)
    into {_n} factors:

    {_formula}

    {_factors}

    The decomposition is *exact*: factor effects sum to $E^T - E^0$ (no residual).

    > **Toggle**: Set `USE_LMDI_4FACTOR = False` in the LMDI input cell below to revert to 3-factor.
    """)
    return


@app.cell
def _(df_floor_area, df_hdd, df_hh, df_pop_full, get_sh_share, pl):
    # ── Toggle: set to False to revert to 3-factor LMDI ──────────────
    USE_LMDI_4FACTOR = True

    # Build the LMDI input table
    _df_energy_total = (
        df_hh
        .group_by("Jahr").agg(pl.col("TJ").sum().alias("E_hh"))
        .rename({"Jahr": "year"}).sort("year")
        .filter(pl.col("year") >= 2000)
    )
    _sh = [get_sh_share(y) for y in _df_energy_total["year"].to_list()]
    _df_energy_total = _df_energy_total.with_columns(
        (pl.col("E_hh") * pl.Series("_sh", _sh)).alias("E"),
    )

    df_lmdi_input = (
        _df_energy_total
        .join(df_pop_full.select("year", "population"), on="year", how="inner")
        .join(df_hdd.select("year", "hdd"), on="year", how="inner")
        .sort("year")
        .with_columns(
            (pl.col("E") / (pl.col("population") * pl.col("hdd"))).alias("intensity"),
        )
    )

    # Optionally attach floor area for 4-factor decomposition
    if USE_LMDI_4FACTOR:
        _m2pp_2012 = df_floor_area.filter(pl.col("year") == 2012)["m2_per_person_avg"][0]
        _floor_records: list[dict] = []
        for _yr, _pop in zip(
            df_lmdi_input["year"].to_list(),
            df_lmdi_input["population"].to_list(),
        ):
            _fa_row = df_floor_area.filter(pl.col("year") == _yr)
            if len(_fa_row) > 0:
                _m2pp = _fa_row["m2_per_person_avg"][0]
            else:
                # Back-extrapolate using +0.3%/yr growth before 2012
                _m2pp = _m2pp_2012 * (1 - 0.003) ** (2012 - _yr)
            _floor_records.append({"year": _yr, "floor_area": _m2pp * _pop / 1e6})
        df_lmdi_input = df_lmdi_input.join(
            pl.DataFrame(_floor_records), on="year", how="left",
        )

    _label = "4-factor" if USE_LMDI_4FACTOR else "3-factor"
    print(f"LMDI input ({_label}): {df_lmdi_input.shape[0]} years ({df_lmdi_input['year'].min()}-{df_lmdi_input['year'].max()})")
    return (USE_LMDI_4FACTOR, df_lmdi_input)


@app.cell
def _(USE_LMDI_4FACTOR, compute_lmdi_3factor, compute_lmdi_4factor, df_lmdi_input, verify_decomposition):
    if USE_LMDI_4FACTOR:
        df_lmdi = compute_lmdi_4factor(df_lmdi_input)
        _residual = verify_decomposition(df_lmdi, n_factors=4)
        print(f"LMDI 4-factor residual: {_residual:.6f} TJ (should be ~0)")
    else:
        df_lmdi = compute_lmdi_3factor(df_lmdi_input)
        _residual = verify_decomposition(df_lmdi, n_factors=3)
        print(f"LMDI 3-factor residual: {_residual:.6f} TJ (should be ~0)")
    return (df_lmdi,)


@app.cell
def _(LMDI_COLORS, USE_LMDI_4FACTOR, apply_theme, df_lmdi, go):
    # Horizontal diverging bar chart (IPCC AR6 convention)
    _last = df_lmdi[-1]
    _factors: list[tuple[str, float, str]] = []
    if USE_LMDI_4FACTOR:
        _factors = [
            ("Intensity (tech.)", _last["cum_intensity"].item(), LMDI_COLORS["intensity"]),
            ("Weather (HDD)", _last["cum_weather"].item(), LMDI_COLORS["weather"]),
            ("Floor Area/cap", _last["cum_floor"].item(), LMDI_COLORS["floor_area"]),
            ("Population", _last["cum_pop"].item(), LMDI_COLORS["population"]),
        ]
    else:
        _factors = [
            ("Intensity (tech.)", _last["cum_intensity"].item(), LMDI_COLORS["intensity"]),
            ("Weather (HDD)", _last["cum_weather"].item(), LMDI_COLORS["weather"]),
            ("Population", _last["cum_pop"].item(), LMDI_COLORS["population"]),
        ]
    _net_val = _last["cum_total"].item()

    fig_lmdi_bar = go.Figure()
    for _label, _val, _color in _factors:
        fig_lmdi_bar.add_trace(go.Bar(
            y=[_label], x=[_val], orientation="h",
            marker_color=_color, showlegend=False,
            text=f"{_val:+,.0f} TJ",
            textposition="inside", insidetextanchor="end",
            textfont=dict(size=12, color="white"),
            constraintext="none",
        ))
    # Net change as a distinct marker
    fig_lmdi_bar.add_trace(go.Scatter(
        x=[_net_val], y=["Net Change"],
        mode="markers+text", marker=dict(symbol="diamond", size=14, color=LMDI_COLORS["net"]),
        text=[f"{_net_val:+,.0f} TJ"], textposition="middle right", textfont=dict(size=12),
        showlegend=False,
    ))
    fig_lmdi_bar.add_vline(x=0, line_width=1.5, line_color="black")
    _n = "4" if USE_LMDI_4FACTOR else "3"
    apply_theme(fig_lmdi_bar).update_layout(
        title=f"LMDI-I {_n}-Factor Decomposition — Cumulative Change (2000–{df_lmdi['year'][-1]}, TJ)",
        xaxis_title="Cumulative ΔE (TJ)", yaxis_title="",
        yaxis=dict(categoryorder="array", categoryarray=[f[0] for f in _factors] + ["Net Change"]),
        height=350 if not USE_LMDI_4FACTOR else 400,
        margin=dict(l=150),
    )
    return


@app.cell
def _(LMDI_COLORS, USE_LMDI_4FACTOR, apply_theme, df_lmdi, go):
    # Diverging stacked bar chart (Energy Policy / Applied Energy convention)
    _years = df_lmdi["year"].to_list()

    # Define factor series — positive factors first, then negative
    _bar_series: list[tuple[str, str, str]] = [
        ("dE_pop", "Population", LMDI_COLORS["population"]),
    ]
    if USE_LMDI_4FACTOR:
        _bar_series.append(("dE_floor", "Floor Area/cap", LMDI_COLORS["floor_area"]))
    _bar_series.extend([
        ("dE_weather", "Weather (HDD)", LMDI_COLORS["weather"]),
        ("dE_intensity", "Intensity (tech.)", LMDI_COLORS["intensity"]),
    ])

    fig_lmdi_ts = go.Figure()
    for _col, _name, _color in _bar_series:
        fig_lmdi_ts.add_trace(go.Bar(
            x=_years, y=df_lmdi[_col].to_list(),
            name=_name, marker_color=_color,
        ))
    # Net change overlay as line
    fig_lmdi_ts.add_trace(go.Scatter(
        x=_years, y=df_lmdi["dE_total"].to_list(),
        name="Net Change", mode="lines+markers",
        line=dict(color=LMDI_COLORS["net"], width=2.5, dash="dash"),
        marker=dict(size=5, color=LMDI_COLORS["net"]),
    ))
    fig_lmdi_ts.add_hline(y=0, line_width=1, line_color="black")
    _n = "4" if USE_LMDI_4FACTOR else "3"
    apply_theme(fig_lmdi_ts).update_layout(
        title=f"Annual LMDI-I {_n}-Factor Decomposition (TJ)",
        xaxis_title="Year", yaxis_title="Annual \u0394E (TJ)",
        barmode="relative",
        width=1150,
        margin=dict(b=110),
    )
    fig_lmdi_ts.add_annotation(
        text="Note: Population and Floor Area effects are small relative to Weather and Intensity.",
        xref="paper", yref="paper", x=0.5, y=-0.35,
        showarrow=False, font=dict(size=10, color="#888"),
        xanchor="center",
    )
    return


@app.cell
def _(USE_LMDI_4FACTOR, df_lmdi, mo):
    _last_row = df_lmdi[-1]
    _cum_p = _last_row["cum_pop"].item()
    _cum_w = _last_row["cum_weather"].item()
    _cum_i = _last_row["cum_intensity"].item()
    _cum_t = _last_row["cum_total"].item()

    _rows: list[str] = []
    if USE_LMDI_4FACTOR:
        _cum_f = _last_row["cum_floor"].item()
        _abs_sum = abs(_cum_p) + abs(_cum_f) + abs(_cum_w) + abs(_cum_i)
        _rows.append(f"| **Population** | {_cum_p:+,.0f} | {'Up' if _cum_p > 0 else 'Down'} | {abs(_cum_p)/_abs_sum*100:.0f}% |")
        _rows.append(f"| **Floor Area/cap** | {_cum_f:+,.0f} | {'Up' if _cum_f > 0 else 'Down'} | {abs(_cum_f)/_abs_sum*100:.0f}% |")
    else:
        _abs_sum = abs(_cum_p) + abs(_cum_w) + abs(_cum_i)
        _rows.append(f"| **Population** | {_cum_p:+,.0f} | {'Up' if _cum_p > 0 else 'Down'} | {abs(_cum_p)/_abs_sum*100:.0f}% |")
    _rows.append(f"| **Weather (HDD)** | {_cum_w:+,.0f} | {'Up' if _cum_w > 0 else 'Down'} | {abs(_cum_w)/_abs_sum*100:.0f}% |")
    _rows.append(f"| **Intensity (tech.)** | {_cum_i:+,.0f} | {'Up' if _cum_i > 0 else 'Down'} | {abs(_cum_i)/_abs_sum*100:.0f}% |")
    _rows.append(f"| **Net Change** | {_cum_t:+,.0f} | {'Up' if _cum_t > 0 else 'Down'} | — |")

    _n = "4" if USE_LMDI_4FACTOR else "3"
    _table = "\n        ".join(_rows)
    mo.md(
        f"""
        ### LMDI Summary — {_n}-Factor (2000 to {df_lmdi['year'][-1]})

        | Factor | Cumulative dE (TJ) | Direction | Share |
        |--------|--------------------:|-----------|------:|
        {_table}

        **Key insight**: The intensity effect alone ({_cum_i:+,.0f} TJ) is large enough to
        offset **both** population growth ({_cum_p:+,.0f} TJ) **and** would still yield a
        net decline even without the weather bonus ({_cum_w:+,.0f} TJ).
        """
    )
    return


# ═══════════════════════════════════════════════════════════════════════
# 15. HDD-NORMALIZED ENERGY
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(apply_theme, df_hdd, df_hh, get_sh_share, go, mo, pl):
    _hdd_ref = df_hdd.filter(pl.col("year").is_between(2000, 2024))["hdd"].mean()

    _df_e_yr = (
        df_hh.group_by("Jahr").agg(pl.col("TJ").sum().alias("E_hh"))
        .rename({"Jahr": "year"}).sort("year").filter(pl.col("year") >= 2000)
    )
    _sh = [get_sh_share(y) for y in _df_e_yr["year"].to_list()]
    _df_e_yr = _df_e_yr.with_columns((pl.col("E_hh") * pl.Series("_sh", _sh)).alias("E"))

    df_hdd_norm = (
        _df_e_yr
        .join(df_hdd.select("year", "hdd"), on="year", how="inner")
        .with_columns((pl.col("E") * _hdd_ref / pl.col("hdd")).round(0).alias("E_norm"))
    )

    fig_hdd_norm = go.Figure()
    fig_hdd_norm.add_trace(go.Scatter(
        x=df_hdd_norm["year"].to_list(), y=df_hdd_norm["E"].to_list(),
        name="Actual", mode="lines+markers", line=dict(color="#90CAF9", width=2), marker=dict(size=5),
    ))
    fig_hdd_norm.add_trace(go.Scatter(
        x=df_hdd_norm["year"].to_list(), y=df_hdd_norm["E_norm"].to_list(),
        name=f"HDD-Normalized (ref={_hdd_ref:.0f})", mode="lines+markers",
        line=dict(color="#1565C0", width=3), marker=dict(size=6),
    ))
    apply_theme(fig_hdd_norm).update_layout(
        title="Space-Heating Energy — Actual vs HDD-Normalized (TJ)",
        xaxis_title="Year", yaxis_title="Final Energy (TJ)",
    )
    fig_hdd_norm

    _e_first = df_hdd_norm.filter(pl.col("year") == df_hdd_norm["year"].min())["E_norm"][0]
    _e_last = df_hdd_norm.filter(pl.col("year") == df_hdd_norm["year"].max())["E_norm"][0]
    _pct = (_e_last - _e_first) / _e_first * 100
    mo.md(f"**HDD-normalized structural change: {_pct:+.1f}%** from {df_hdd_norm['year'].min()} to {df_hdd_norm['year'].max()}.")
    return df_hdd_norm, fig_hdd_norm


# ═══════════════════════════════════════════════════════════════════════
# 16. INTENSITY ATTRIBUTION (Qualitative)
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(apply_theme, df_lmdi, go):
    _total_intensity = df_lmdi[-1]["cum_intensity"].item()
    # Fixed indicative shares from literature (BFE/Prognos 2024, TEP Energy)
    _envelope_share = 0.45
    _fuel_switch_share = 0.35
    _other_share = 1.0 - _envelope_share - _fuel_switch_share
    _envelope_pct = round(_envelope_share * 100)
    _fuel_switch_pct = round(_fuel_switch_share * 100)
    _other_pct = round(_other_share * 100)
    _shares = {
        f"Building Envelope ({_envelope_pct}%)": _envelope_share,
        f"Fuel Switching ({_fuel_switch_pct}%)": _fuel_switch_share,
        f"Other ({_other_pct}%)": _other_share,
    }

    fig_intensity_attr = go.Figure(go.Bar(
        y=["Total Intensity Effect"] + list(_shares.keys()),
        x=[_total_intensity] + [_total_intensity * s for s in _shares.values()],
        orientation="h",
        marker_color=["#1565C0", "#4CAF50", "#FF9800", "#9E9E9E"],
        text=[f"{_total_intensity * s:,.0f} TJ" if i > 0 else f"{_total_intensity:,.0f} TJ"
              for i, s in enumerate([1.0] + list(_shares.values()))],
        textposition="auto",
    ))
    apply_theme(fig_intensity_attr).update_layout(
        title="Intensity Effect \u2014 Attribution (indicative)",
        xaxis_title="\u0394E (TJ, cumulative 2000\u2013latest)",
        yaxis=dict(autorange="reversed"), height=400,
        margin=dict(l=180),
    )
    fig_intensity_attr
    return (fig_intensity_attr,)


@app.cell
def _(mo):
    mo.md("""
    ## Building Envelope & Renovation Context

    The intensity effect is the dominant driver of space-heating
    energy reduction. We decompose it qualitatively into three channels:

    ### 1. Building Envelope Improvements (~45%)

    Switzerland's building renovation rate stands at approximately **1.1% per year**
    (TEP Energy, 2020), well below the **2.0--2.5%** needed to meet the 2050 net-zero
    target (BFE *Energieperspektiven 2050+*). At the current pace, full stock turnover
    would take roughly 90 years.

    Reference thermal performance by construction period (GEAK/CECB database):

    | Construction Period | Typical U-value (W/m\u00b2K) | Specific Heating Demand (kWh/m\u00b2) |
    |---|---|---|
    | Pre-1970 | 0.8--1.0 | 170--200 |
    | 1970--1990 | 0.5--0.8 | 100--150 |
    | 1990--2010 | 0.3--0.5 | 60--100 |
    | Post-2010 (MuKEn 2014) | 0.15--0.25 | 30--50 |
    | Minergie-P target | \u22640.15 | \u226416 (SIA 380/1) |

    **Why not a formal LMDI factor?** We investigated adding insulation as a 5th
    decomposition factor but concluded it would be methodologically unsound:

    - No consistent annual time series of stock-level U-values exists for Switzerland.
    - The *Energiebezugsfl\u00e4che* (EBF) definition changed with SIA 380/1 (2007),
      making pre/post comparisons unreliable.
    - The intensity factor in our 4-factor LMDI already captures envelope improvements
      implicitly -- adding a separate insulation factor would create multicollinearity.

    ### 2. Fuel Switching (~35%)

    The shift from oil/gas boilers (efficiency ~85--95%) to heat pumps (COP 3--4)
    reduces final energy consumption per unit of useful heat by a factor of roughly 3.
    This is captured in the heating mix transition (fig4) and the building-level
    analysis (fig15).

    ### 3. Other Efficiency Gains (~20%)

    Includes improved controls (thermostatic valves, weather-compensated heating curves),
    reduced distribution losses, and behavioral changes.

    ### Regulatory Timeline

    - **SIA 380/1 (2007 update)**: Standardized thermal energy calculation method;
      introduced the *Energiebezugsfl\u00e4che* (EBF) definition.
    - **MuKEn 2014**: Cantonal model energy codes -- now adopted in 22/26 cantons.
      Mandates roughly 10% renewable share on heating system replacement.
    - **MuKEn 2025**: Adopted August 2025 -- tighter envelope requirements,
      implementation 2025--2030.
    """)
    return


# ═══════════════════════════════════════════════════════════════════════
# 17. MONTE CARLO SCENARIOS
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 17. Monte Carlo Scenario Projections (2024-2050)

    Forward projection of household energy demand under uncertainty.
    Three named scenarios (BAU, Accelerated, Ambitious) with 1,000 Monte Carlo
    iterations providing uncertainty bands.

    **Parameters**: population growth (BFS reference +/- noise), HDD decline trend,
    renovation rate (drives intensity decline), HP adoption speed.
    """)
    return


@app.cell
def _(
    DEFAULT_SCENARIOS,
    apply_theme,
    compute_named_trajectories,
    compute_tornado_sensitivity,
    df_lmdi_input,
    df_pop_proj,
    extract_base_values,
    go,
    pl,
    run_monte_carlo,
):
    _base = extract_base_values(df_lmdi_input)
    _mc = run_monte_carlo(_base, pop_projections=df_pop_proj)
    _named = compute_named_trajectories(_base, pop_projections=df_pop_proj)

    # Fan chart
    fig_scenario_fan = go.Figure()
    fig_scenario_fan.add_trace(go.Scatter(
        x=_mc["years"] + _mc["years"][::-1],
        y=_mc["p90"].tolist() + _mc["p10"][::-1].tolist(),
        fill="toself", fillcolor="rgba(158,158,158,0.15)",
        line=dict(width=0), name="10th–90th pctile",
    ))
    fig_scenario_fan.add_trace(go.Scatter(
        x=_mc["years"] + _mc["years"][::-1],
        y=_mc["p75"].tolist() + _mc["p25"][::-1].tolist(),
        fill="toself", fillcolor="rgba(158,158,158,0.30)",
        line=dict(width=0), name="25th–75th pctile",
    ))
    for _sname, _traj in _named.items():
        _sdef = DEFAULT_SCENARIOS[_sname]
        fig_scenario_fan.add_trace(go.Scatter(
            x=_mc["years"], y=_traj,
            name=_sdef.label, mode="lines",
            line=dict(color=_sdef.color, width=3),
        ))

    # Historical energy — full series so the trend into projections is visible
    fig_scenario_fan.add_trace(go.Scatter(
        x=df_lmdi_input["year"].to_list(), y=df_lmdi_input["E"].to_list(),
        name="Historical", mode="lines+markers",
        line=dict(color="#212121", width=3), marker=dict(size=4),
    ))
    apply_theme(fig_scenario_fan).update_layout(
        title="Projected Space-Heating Energy Demand — Monte Carlo Scenarios (TJ)",
        xaxis_title="Year", yaxis_title="Final Energy (TJ)",
    )

    # Tornado sensitivity
    _median_2050 = float(_mc["p50"][-1])
    _sensitivities = compute_tornado_sensitivity(_base, _median_2050)

    fig_tornado = go.Figure(go.Bar(
        y=[s[0] for s in _sensitivities],
        x=[s[1] for s in _sensitivities],
        orientation="h",
        marker_color=["#F44336" if s[1] > 0 else "#4CAF50" for s in _sensitivities],
        text=[f"{s[1]:+,.0f} TJ" for s in _sensitivities],
        textposition="inside",
        insidetextanchor="end",
        textfont=dict(size=12, color="white"),
        constraintext="none",
    ))
    _tornado_max = max(abs(s[1]) for s in _sensitivities) * 1.15
    apply_theme(fig_tornado).update_layout(
        title="Tornado Sensitivity \u2014 2050 Energy Demand vs Median",
        xaxis_title="\u0394E vs Median (TJ)",
        xaxis=dict(range=[-_tornado_max, _tornado_max]),
        yaxis=dict(autorange="reversed"), height=450,
        margin=dict(l=180, t=80),
    )

    fig_scenario_fan
    return fig_scenario_fan, fig_tornado


# ═══════════════════════════════════════════════════════════════════════
# 18. HEATING SYSTEM ECONOMICS
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## 18. Heating System Economics — Operating + Investment Cost Comparison

    Annualized heating cost for a reference 150 m² unrenovated single-family house
    (120 kWh/m²/yr demand). Shows how the CO₂ levy shifts the economic calculus
    between fossil boilers and heat pumps.

    ### The Swiss CO₂ Levy Mechanism

    The CO₂ levy (*CO₂-Abgabe*) is a Pigouvian tax on **fossil heating fuels**
    (heating oil, natural gas) collected at the point of import or production.
    It does **not** apply to transport fuels or electricity — meaning heat pumps
    are structurally exempt on the operating-cost side.

    Revenue is recycled through two channels:
    - **~2/3** redistributed to the population via per-capita health-insurance
      premium reductions (lump-sum rebate), making it progressive.
    - **~1/3** channelled to the *Gebäudeprogramm*, which co-finances envelope
      retrofits and heating-system replacements (reflected in our CAPEX subsidies).

    ### Three Scenario Levels — Rationale

    We evaluate costs under three levy levels that span the plausible policy
    corridor from today's law through to full externality pricing:

    | Scenario | Level | Justification |
    |----------|-------|---------------|
    | **Status quo** | CHF 120/t | Current rate since 1 Jan 2022. Set by the CO₂ Act (SR 641.71) and CO₂ Ordinance (SR 641.711, Art. 94a). The levy has escalated stepwise from CHF 12/t in 2008 each time the buildings sector missed its interim CO₂ reduction targets. |
    | **Policy trajectory** | CHF 200/t | The revised CO₂ Act (2025–2030) authorises a ceiling of CHF 210/t, with automatic escalation if buildings miss the 2026/2028 interim targets. This is consistent with the EU ETS price trajectory under the Fit-for-55 package and is the mid-range assumption used by BFE *Energieperspektiven 2050+* and Prognos/TEP Energy. |
    | **Full externality** | CHF 300/t | Aligns with IPCC AR6 WGIII carbon prices for 1.5 °C-compatible pathways (median USD 220–350/t CO₂ by 2030, Table 3.6). Supported by the US EPA (2023) social cost of carbon estimates and Rennert et al. (2022, *Nature*). Represents the cost if the levy fully internalised the climate-damage externality. |

    This **status quo / policy trajectory / full cost internalisation** bracket is
    standard methodology in Swiss energy-policy analysis (BFE, BAFU, Prognos/TEP Energy)
    and allows the reader to assess how sensitive the fossil-vs-HP cost comparison is
    to the regulatory trajectory.
    """)
    return


@app.cell
def _(CO2_LEVY_SCENARIOS, DEFAULT_SYSTEMS, apply_theme, compute_opex, compute_totex, go, make_subplots):
    # TOTEX stacked bars across CO₂ levy scenarios
    _levies = list(CO2_LEVY_SCENARIOS.keys())
    _systems = list(DEFAULT_SYSTEMS.keys())
    _n_sys = len(_systems)

    fig_cost = make_subplots(
        rows=1, cols=len(_levies), shared_yaxes=True,
        subplot_titles=[f"CO\u2082 levy CHF {l}/t" for l in _levies],
        horizontal_spacing=0.08,
    )

    for _li, _levy in enumerate(_levies):
        _col = _li + 1
        _capex, _fuel, _co2, _totals = [], [], [], []
        for _sys in DEFAULT_SYSTEMS.values():
            _t = compute_totex(_sys, _levy)
            _o = compute_opex(_sys, _levy)
            _capex.append(_t["annual_capex"])
            _fuel.append(_o["fuel_cost"])
            _co2.append(_o["co2_cost"])
            _totals.append(_t["total_totex"])

        _show = _li == 0  # legend only on first subplot
        fig_cost.add_trace(go.Bar(
            x=_systems, y=_capex, name="CAPEX (annualized)",
            marker_color="#78909C", showlegend=_show,
            text=[f"{v:,.0f}" for v in _capex], textposition="inside",
            textfont=dict(color="white", size=10),
        ), row=1, col=_col)
        fig_cost.add_trace(go.Bar(
            x=_systems, y=_fuel, name="Fuel",
            marker_color="#FF9800", showlegend=_show,
            text=[f"{v:,.0f}" for v in _fuel], textposition="inside",
            textfont=dict(color="white", size=10),
        ), row=1, col=_col)
        fig_cost.add_trace(go.Bar(
            x=_systems, y=_co2, name="CO₂ levy",
            marker_color="#F44336", showlegend=_show,
            text=[f"{v:,.0f}" if v > 0 else "" for v in _co2], textposition="inside",
            textfont=dict(color="white", size=10),
        ), row=1, col=_col)
        for _i, (_s, _t) in enumerate(zip(_systems, _totals)):
            fig_cost.add_annotation(
                x=_s, y=_t, text=f"<b>{_t:,.0f}</b>",
                showarrow=False, yshift=12, font=dict(size=10),
                xref=f"x{_col}" if _col > 1 else "x",
                yref=f"y{_col}" if _col > 1 else "y",
            )

    apply_theme(fig_cost).update_layout(
        title=dict(
            text=(
                "Annual TOTEX \u2014 150 m\u00b2 Unrenovated House (CHF/yr)"
                "<br><sup style='color:#666'>CAPEX annualized over 20 yr at 3 %, "
                "net of Geb\u00e4udeprogramm subsidies</sup>"
            ),
            y=0.96,
            x=0.5,
            xanchor="center",
        ),
        barmode="stack", height=620, width=1350,
        margin=dict(l=70, r=50, t=110, b=80),
    )
    fig_cost.update_yaxes(title_text="Annual Cost (CHF/yr)", row=1, col=1)
    fig_cost.update_xaxes(tickangle=-25)
    fig_cost
    return (fig_cost,)


@app.cell
def _(CO2_LEVY_SCENARIOS, DEFAULT_SYSTEMS, annuity_factor, compute_opex, mo):
    _lifetime = 20
    _r = 0.03
    _af = annuity_factor(_r, _lifetime)

    _rows = []
    for _name, _sys in DEFAULT_SYSTEMS.items():
        _opex = compute_opex(_sys, 120)  # current levy
        _net_invest = _sys.invest_chf - _sys.subsidy_chf
        _annual_invest = round(_net_invest * _af)
        _total = _opex["total_opex"] + _annual_invest
        _rows.append(
            f"| {_name} | {_sys.invest_chf:,} | {_sys.subsidy_chf:,} "
            f"| {_net_invest:,} | {_annual_invest:,} | {_opex['total_opex']:,.0f} | **{_total:,.0f}** |"
        )

    mo.md(
        f"""
        ### Total Cost of Ownership (at current CO₂ levy CHF 120/t)

        | System | Investment (CHF) | Subsidy | Net invest | Annual invest | Annual operating | **Annual TCO** |
        |--------|--:|--:|--:|--:|--:|--:|
        {chr(10).join("        " + r for r in _rows)}

        Lifetime: {_lifetime} years, discount rate: {_r:.0%}. Operating costs = fuel + CO₂ levy.

        Even including the higher upfront cost, **heat pumps reach near-parity with fossil systems**
        on a total-cost-of-ownership basis thanks to their COP advantage (3–4× less final
        energy) and zero CO₂ levy exposure.
        """
    )
    return


# ═══════════════════════════════════════════════════════════════════════
# FIGURE EXPORT
# ═══════════════════════════════════════════════════════════════════════


@app.cell
def _(mo):
    mo.md("""
    ---
    ## Figure Export for Report
    """)
    return


@app.cell
def _(
    BUILDING_HEAT_COLORS,
    CARRIER_COLORS,
    CARRIER_MAP,
    DECOUPLE_SERIES,
    FIGURES_DIR,
    LMDI_COLORS,
    MIX_CARRIERS,
    MIX_COLORS,
    MIX_LABELS,
    USE_LMDI_4FACTOR,
    apply_theme,
    df_floor_area,
    df_hdd,
    df_heating_compare,
    df_hh,
    df_indexed,
    df_lmdi,
    df_mix,
    df_pop_full,
    df_pop_proj,
    export_fig,
    go,
    pl,
):
    # ── fig1: Energy by carrier ──
    _df_hh_plot = df_hh.with_columns(pl.col("Energietraeger").replace(CARRIER_MAP).alias("carrier_en"))
    _df_pivot = _df_hh_plot.group_by(["Jahr", "carrier_en"]).agg(pl.col("TJ").sum()).sort("Jahr")
    _ordered = _df_pivot.group_by("carrier_en").agg(pl.col("TJ").sum().alias("total")).sort("total", descending=True)["carrier_en"].to_list()

    _fig1 = go.Figure()
    for _c in _ordered:
        _sub = _df_pivot.filter(pl.col("carrier_en") == _c).sort("Jahr")
        _fig1.add_trace(go.Scatter(x=_sub["Jahr"].to_list(), y=_sub["TJ"].to_list(), name=_c, mode="lines", stackgroup="one", line=dict(width=0.5, color=CARRIER_COLORS.get(_c, "#999"))))
    apply_theme(_fig1).update_layout(title="Swiss Household Final Energy Consumption by Carrier (TJ)", xaxis_title="Year", yaxis_title="Final Energy (TJ)")
    export_fig(_fig1, "fig1_energy_by_carrier", FIGURES_DIR)

    # ── fig2: HDD trend ──
    _yrs = df_hdd["year"].to_list(); _hdds = df_hdd["hdd"].to_list()
    _n = len(_yrs); _sx = sum(_yrs); _sy = sum(_hdds); _sxy = sum(x*y for x,y in zip(_yrs,_hdds)); _sx2 = sum(x*x for x in _yrs)
    _sl = (_n*_sxy - _sx*_sy) / (_n*_sx2 - _sx*_sx); _ic = (_sy - _sl*_sx) / _n
    _fig2 = go.Figure()
    _fig2.add_trace(go.Scatter(x=_yrs, y=_hdds, name="HDD (actual)", mode="markers", marker=dict(size=8, color="#FF9800")))
    _fig2.add_trace(go.Scatter(x=_yrs, y=[_sl*yr+_ic for yr in _yrs], name=f"Trend ({_sl*10:.0f} HDD/decade)", mode="lines", line=dict(color="#F44336", width=2, dash="dash")))
    apply_theme(_fig2).update_layout(title="Heating Degree Days — Switzerland (base 20/12°C)", xaxis_title="Year", yaxis_title="HDD")
    export_fig(_fig2, "fig2_hdd_trend", FIGURES_DIR)

    # ── fig3: Population (with projections) ──
    _fig3 = go.Figure()
    _fig3.add_trace(go.Scatter(x=df_pop_full["year"].to_list(), y=[p/1e6 for p in df_pop_full["population"].to_list()], name="Historical", mode="lines+markers", line=dict(color="#9C27B0", width=3), marker=dict(size=3)))
    if df_pop_proj is not None:
        _pyr = df_pop_proj["year"].to_list()
        _lhy = df_pop_full["year"].max()
        _lhp = df_pop_full.filter(df_pop_full["year"]==_lhy)["population"][0]/1e6
        _fig3.add_trace(go.Scatter(x=[_lhy]+_pyr+_pyr[::-1]+[_lhy], y=[_lhp]+[p/1e6 for p in df_pop_proj["pop_high"].to_list()]+[p/1e6 for p in df_pop_proj["pop_low"].to_list()][::-1]+[_lhp], fill="toself", fillcolor="rgba(156,39,176,0.12)", line=dict(width=0), name="BFS high/low"))
        _fig3.add_trace(go.Scatter(x=[_lhy]+_pyr, y=[_lhp]+[p/1e6 for p in df_pop_proj["pop_reference"].to_list()], name="BFS Reference", mode="lines", line=dict(color="#9C27B0", width=2.5, dash="dash")))
    for _yr,_y,_txt in [(1964,5.6,"Guest workers"),(1974,6.3,"Oil crisis"),(2002,7.3,"EU free mvmt")]:
        _fig3.add_annotation(x=_yr, y=_y, text=_txt, showarrow=True, arrowhead=2, arrowsize=0.8, ax=40, ay=-30, font=dict(size=9, color="#666"))
    apply_theme(_fig3).update_layout(title="Swiss Population — History & BFS Projections (millions)", xaxis_title="Year", yaxis_title="Population (millions)")
    export_fig(_fig3, "fig3_population", FIGURES_DIR)

    # ── fig4: Heating mix ──
    _fig4 = go.Figure()
    for _mc in MIX_CARRIERS:
        _fig4.add_trace(go.Scatter(x=df_mix["year"].to_list(), y=df_mix[_mc].to_list(), name=MIX_LABELS[_mc], mode="lines", stackgroup="one", line=dict(width=0.5, color=MIX_COLORS[_mc]), fillcolor=MIX_COLORS[_mc]))
    apply_theme(_fig4).update_layout(title="Swiss Residential Heating — Floor Area Share by System (%)", xaxis_title="Year", yaxis_title="Share of Floor Area (%)", yaxis=dict(range=[0,100]))
    export_fig(_fig4, "fig4_heating_mix", FIGURES_DIR)

    # ── fig5: Decoupling ──
    _fig5 = go.Figure()
    for _col, _name, _color, _dash, _width in DECOUPLE_SERIES:
        _fig5.add_trace(go.Scatter(x=df_indexed["year"].to_list(), y=df_indexed[_col].to_list(), name=_name, mode="lines+markers", line=dict(color=_color, width=_width, dash=_dash), marker=dict(size=4)))
    _fig5.add_hline(y=100, line_dash="dot", line_color="gray", opacity=0.5)
    for _yr, _text, _ypos in [(2007,"SIA 380/1",1.02),(2008,"CO\u2082 levy",1.10),(2010,"Buildings Prog.",1.02),(2015,"MuKEn 2014",1.02),(2022,"CHF 120/t CO\u2082",1.02)]:
        _fig5.add_vline(x=_yr, line_dash="dot", line_color="rgba(0,0,0,0.12)")
        _fig5.add_annotation(x=_yr, y=_ypos, yref="paper", text=_text, showarrow=False, font=dict(size=8, color="#555"), textangle=-35, xanchor="left", yanchor="bottom")
    apply_theme(_fig5).update_layout(title="Decoupling: Space-Heating Energy vs Economic Growth (2000 = 100)", xaxis_title="Year", yaxis_title="Index (2000 = 100)", margin=dict(t=110))
    export_fig(_fig5, "fig5_decoupling", FIGURES_DIR)

    # ── fig6: Floor area ──
    _fig6 = go.Figure()
    _fig6.add_trace(go.Scatter(x=df_floor_area["year"].to_list(), y=df_floor_area["m2_per_person_sfh"].to_list(), name="Single-Family", mode="lines+markers", line=dict(color="#FF9800", width=2.5), marker=dict(size=6)))
    _fig6.add_trace(go.Scatter(x=df_floor_area["year"].to_list(), y=df_floor_area["m2_per_person_mfh"].to_list(), name="Multi-Family", mode="lines+markers", line=dict(color="#2196F3", width=2.5), marker=dict(size=6)))
    _fig6.add_trace(go.Scatter(x=df_floor_area["year"].to_list(), y=df_floor_area["m2_per_person_avg"].to_list(), name="Weighted Avg (~30/70)", mode="lines+markers", line=dict(color="#4CAF50", width=3, dash="dash"), marker=dict(size=5)))
    apply_theme(_fig6).update_layout(title="Average Floor Area per Person — Swiss Residential (BFS GWS)", xaxis_title="Year", yaxis_title="m² per person")
    export_fig(_fig6, "fig6_floor_area", FIGURES_DIR)

    # ── fig7: Buildings by heating source ──
    _src = df_heating_compare["source"].to_list()
    _fig7 = go.Figure()
    _fig7.add_trace(go.Bar(x=_src, y=[v/1000 for v in df_heating_compare["buildings_2000"].to_list()], name="2000", marker_color="#BDBDBD", marker_line=dict(color="#757575", width=1.5)))
    _fig7.add_trace(go.Bar(x=_src, y=[v/1000 for v in df_heating_compare["buildings_2021"].to_list()], name="2021", marker_color=[BUILDING_HEAT_COLORS.get(s,"#999") for s in _src]))
    apply_theme(_fig7).update_layout(title="Residential Buildings by Heating Source \u2014 2000 vs 2021", xaxis_title="Energy Source", yaxis_title="Buildings (thousands)", barmode="group")
    export_fig(_fig7, "fig7_buildings_heating", FIGURES_DIR)

    # ── fig8: LMDI horizontal diverging bar ──
    _last = df_lmdi[-1]
    _n8 = "4" if USE_LMDI_4FACTOR else "3"
    _factors8: list[tuple[str, float, str]] = []
    if USE_LMDI_4FACTOR:
        _factors8 = [
            ("Intensity (tech.)", _last["cum_intensity"].item(), LMDI_COLORS["intensity"]),
            ("Weather (HDD)", _last["cum_weather"].item(), LMDI_COLORS["weather"]),
            ("Floor Area/cap", _last["cum_floor"].item(), LMDI_COLORS["floor_area"]),
            ("Population", _last["cum_pop"].item(), LMDI_COLORS["population"]),
        ]
    else:
        _factors8 = [
            ("Intensity (tech.)", _last["cum_intensity"].item(), LMDI_COLORS["intensity"]),
            ("Weather (HDD)", _last["cum_weather"].item(), LMDI_COLORS["weather"]),
            ("Population", _last["cum_pop"].item(), LMDI_COLORS["population"]),
        ]
    _net8 = _last["cum_total"].item()
    _fig8 = go.Figure()
    for _label, _val, _color in _factors8:
        _fig8.add_trace(go.Bar(y=[_label], x=[_val], orientation="h", marker_color=_color, showlegend=False, text=f"{_val:+,.0f} TJ", textposition="inside", insidetextanchor="end", textfont=dict(size=12, color="white"), constraintext="none"))
    _fig8.add_trace(go.Scatter(x=[_net8], y=["Net Change"], mode="markers+text", marker=dict(symbol="diamond", size=14, color=LMDI_COLORS["net"]), text=[f"{_net8:+,.0f} TJ"], textposition="middle right", textfont=dict(size=12), showlegend=False))
    _fig8.add_vline(x=0, line_width=1.5, line_color="black")
    apply_theme(_fig8).update_layout(title=f"LMDI-I {_n8}-Factor Decomposition — Cumulative Change (2000–{df_lmdi['year'][-1]}, TJ)", xaxis_title="Cumulative ΔE (TJ)", yaxis_title="", yaxis=dict(categoryorder="array", categoryarray=[f[0] for f in _factors8] + ["Net Change"]), height=350 if not USE_LMDI_4FACTOR else 400, margin=dict(l=150))
    export_fig(_fig8, "fig8_lmdi_waterfall", FIGURES_DIR)

    # ── fig9: LMDI diverging stacked bar ──
    _years9 = df_lmdi["year"].to_list()
    _bar9: list[tuple[str, str, str]] = [("dE_pop", "Population", LMDI_COLORS["population"])]
    if USE_LMDI_4FACTOR:
        _bar9.append(("dE_floor", "Floor Area/cap", LMDI_COLORS["floor_area"]))
    _bar9.extend([("dE_weather", "Weather", LMDI_COLORS["weather"]), ("dE_intensity", "Intensity", LMDI_COLORS["intensity"])])
    _fig9 = go.Figure()
    for _col, _name, _color in _bar9:
        _fig9.add_trace(go.Bar(x=_years9, y=df_lmdi[_col].to_list(), name=_name, marker_color=_color))
    _fig9.add_trace(go.Scatter(x=_years9, y=df_lmdi["dE_total"].to_list(), name="Net", mode="lines+markers", line=dict(color=LMDI_COLORS["net"], width=2.5, dash="dash"), marker=dict(size=5, color=LMDI_COLORS["net"])))
    _fig9.add_hline(y=0, line_width=1, line_color="black")
    apply_theme(_fig9).update_layout(title=f"Annual LMDI-I {_n8}-Factor Decomposition (TJ)", xaxis_title="Year", yaxis_title="Annual \u0394E (TJ)", barmode="relative", width=1150, margin=dict(b=110))
    _fig9.add_annotation(text="Note: Population and Floor Area effects are small relative to Weather and Intensity.", xref="paper", yref="paper", x=0.5, y=-0.35, showarrow=False, font=dict(size=10, color="#888"), xanchor="center")
    export_fig(_fig9, "fig9_lmdi_timeseries", FIGURES_DIR)

    print(f"Exported fig1-fig9 to {FIGURES_DIR}")
    return


@app.cell
def _(FIGURES_DIR, export_fig, fig_canton_map, fig_cost, fig_floor_period, fig_hdd_norm, fig_heating_by_type, fig_intensity_attr, fig_scenario_fan, fig_tornado):
    _new_figs = [
        (fig_hdd_norm, "fig10_energy_hdd_normalized"),
        (fig_intensity_attr, "fig11_intensity_attribution"),
        (fig_scenario_fan, "fig12_scenario_fan"),
        (fig_tornado, "fig13_scenario_tornado"),
        (fig_cost, "fig14_cost_comparison"),
        (fig_heating_by_type, "fig15_heating_by_type"),
        (fig_floor_period, "fig16_floor_area_by_period"),
        (fig_canton_map, "fig17_canton_hp_map"),
    ]
    for _fig, _name in _new_figs:
        export_fig(_fig, _name, FIGURES_DIR)
    print(f"Exported fig10-fig17 to {FIGURES_DIR}")
    return


@app.cell
def _(mo):
    mo.md("""
    ### Exported Files

    | # | SVG | PDF |
    |---|-----|-----|
    | 1 | `fig1_energy_by_carrier.svg` | `fig1_energy_by_carrier.pdf` |
    | 2 | `fig2_hdd_trend.svg` | `fig2_hdd_trend.pdf` |
    | 3 | `fig3_population.svg` | `fig3_population.pdf` |
    | 4 | `fig4_heating_mix.svg` | `fig4_heating_mix.pdf` |
    | 5 | `fig5_decoupling.svg` | `fig5_decoupling.pdf` |
    | 6 | `fig6_floor_area.svg` | `fig6_floor_area.pdf` |
    | 7 | `fig7_buildings_heating.svg` | `fig7_buildings_heating.pdf` |
    | 8 | `fig8_lmdi_waterfall.svg` | `fig8_lmdi_waterfall.pdf` |
    | 9 | `fig9_lmdi_timeseries.svg` | `fig9_lmdi_timeseries.pdf` |
    | 10 | `fig10_energy_hdd_normalized.svg` | `fig10_energy_hdd_normalized.pdf` |
    | 11 | `fig11_intensity_attribution.svg` | `fig11_intensity_attribution.pdf` |
    | 12 | `fig12_scenario_fan.svg` | `fig12_scenario_fan.pdf` |
    | 13 | `fig13_scenario_tornado.svg` | `fig13_scenario_tornado.pdf` |
    | 14 | `fig14_cost_comparison.svg` | `fig14_cost_comparison.pdf` |
    | 15 | `fig15_heating_by_type.svg` | `fig15_heating_by_type.pdf` |
    | 16 | `fig16_floor_area_by_period.svg` | `fig16_floor_area_by_period.pdf` |
    | 17 | `fig17_canton_hp_map.svg` | `fig17_canton_hp_map.pdf` |

    All figures saved to `figures/` for inclusion in the Typst report.
    """)
    return


if __name__ == "__main__":
    app.run()
