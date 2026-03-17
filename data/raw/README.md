# Raw Data Inventory

Downloaded: 2026-03-12

These files are manually downloaded and **not** auto-fetched by the notebook.
The notebook reads them from `data/raw/`.

## Files

| File | Source | Years | Description |
|------|--------|-------|-------------|
| `bfe_hh_energy_by_use_2024.xlsx` | BFE/Prognos (pubdb.bfe.admin.ch) | 2000-2024 | Household energy by end use (Tabellen 1, 11, 13) |
| `floor_area_by_building_category.xlsx` | BFS (asset 36158296) | 2012-2024 | m2/person by building type & construction period |
| `floor_area_by_rooms_canton.csv` | BFS (asset 36158430) | 2012-2024 | m2/person by room count, by canton |
| `buildings_heating_source_2000_2021.xlsx` | BFS (asset 23524602) | 2000, 2021 | Buildings by heating system & energy source |
| `bau_wohnungswesen.csv` | BFS (asset 24885538) | 2020-2022 | Housing stats: dwellings by energy source, vacancy, floor area |
| `worldbank_gdp_ch.json` | World Bank WDI (NY.GDP.MKTP.KN) | 2000-2024 | Real GDP in constant CHF |
| `worldbank_pop_ch.json` | World Bank WDI (SP.POP.TOTL) | 2000-2024 | Total population (fills 2000-2009 gap) |

## Auto-downloaded by notebook (in `data/`)

These are fetched by `download_cached()` in `notebooks/analysis.py`:

| File | Source | Description |
|------|--------|-------------|
| `bfe_energy_balance.csv` | BFE ogd115 | Energy balance by sector & carrier (TJ) |
| `bfe_hdd_monthly.csv` | BFE ogd105 | Heating degree days (monthly, 1994+) |
| `zurich_hdd_annual.csv` | Stadt Zurich | HDD Zurich Fluntern (backfill 1980-1993) |
| `bfs_population.json` | BFS PxWeb | Permanent resident population (2010+) |
| `bfs_census_buildings_heating.json` | BFS PxWeb | Buildings by heating source (census) |

## Known Gaps

- Population 2000-2009: covered by `worldbank_pop_ch.json`
- HDD: not available from Eurostat for CH (non-EU); curated from BFE + Zurich Fluntern
- Annual buildings by heating source (2010-2024): requires STAT-TAB PxWeb interactive query
