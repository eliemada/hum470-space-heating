"""Heating system economics — OPEX, CAPEX, and TOTEX calculations.

Reference building: 150 m², unrenovated single-family house
(120 kWh/m²/yr useful heating demand).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HeatingSystem:
    """Technical and economic parameters for a heating system."""

    name: str
    efficiency: float       # COP for HPs, thermal efficiency for boilers
    fuel_chf_kwh: float     # Fuel price (CHF/kWh delivered)
    co2_kg_kwh: float       # Direct CO2 emissions (kg/kWh fuel burned)
    color: str              # Chart color
    invest_chf: int         # Gross investment cost (CHF)
    subsidy_chf: int        # Gebäudeprogramm subsidy (CHF)


# ── Default system definitions ──────────────────────────────────────────
# Sources:
#   - EnergieSchweiz "Heizungsersatz: Kosten" (EFH reference case)
#   - hausinfo.ch "Kosten einer Wärmepumpe in der Schweiz"
#   - hausinfo.ch "Heizungsersatz: Finanzierung & Förderung"
DEFAULT_SYSTEMS: dict[str, HeatingSystem] = {
    "Oil Boiler": HeatingSystem(
        "Oil Boiler", 0.90, 0.12, 0.265, "#8B4513", 18_000, 0,
    ),
    "Gas Condensing": HeatingSystem(
        "Gas Condensing", 0.95, 0.11, 0.198, "#FF6B35", 20_000, 0,
    ),
    "Air-Source HP": HeatingSystem(
        "Air-Source HP", 3.2, 0.27, 0.0, "#2196F3", 42_000, 5_000,
    ),
    "Ground-Source HP": HeatingSystem(
        "Ground-Source HP", 4.0, 0.27, 0.0, "#1565C0", 60_000, 10_000,
    ),
}

# Reference building
DEFAULT_AREA_M2 = 150
DEFAULT_DEMAND_KWH_M2 = 120


def compute_opex(
    system: HeatingSystem,
    co2_levy_chf_per_ton: float,
    area_m2: float = DEFAULT_AREA_M2,
    demand_kwh_m2: float = DEFAULT_DEMAND_KWH_M2,
) -> dict:
    """Compute annual operating cost (fuel + CO2 levy).

    Returns dict with ``fuel_cost``, ``co2_cost``, ``total_opex``.
    """
    final_energy_kwh = area_m2 * demand_kwh_m2 / system.efficiency
    fuel_cost = final_energy_kwh * system.fuel_chf_kwh
    co2_cost = final_energy_kwh * system.co2_kg_kwh / 1000 * co2_levy_chf_per_ton
    return {
        "fuel_cost": round(fuel_cost, 0),
        "co2_cost": round(co2_cost, 0),
        "total_opex": round(fuel_cost + co2_cost, 0),
    }


def annuity_factor(rate: float, years: int) -> float:
    """Capital recovery factor: rate / (1 - (1+rate)^-years)."""
    if rate <= 0:
        return 1.0 / years
    return rate / (1 - (1 + rate) ** (-years))


def compute_totex(
    system: HeatingSystem,
    co2_levy_chf_per_ton: float,
    *,
    area_m2: float = DEFAULT_AREA_M2,
    demand_kwh_m2: float = DEFAULT_DEMAND_KWH_M2,
    lifetime_years: int = 20,
    discount_rate: float = 0.03,
) -> dict:
    """Compute total annualized cost of ownership (CAPEX + OPEX).

    Returns dict with ``annual_capex``, ``total_opex``, ``total_totex``,
    ``net_invest``.
    """
    opex = compute_opex(system, co2_levy_chf_per_ton, area_m2, demand_kwh_m2)
    net_invest = system.invest_chf - system.subsidy_chf
    annual_capex = round(net_invest * annuity_factor(discount_rate, lifetime_years))
    return {
        "net_invest": net_invest,
        "annual_capex": annual_capex,
        "total_opex": opex["total_opex"],
        "total_totex": annual_capex + opex["total_opex"],
    }


# CO2 levy scenario values with policy justification
CO2_LEVY_SCENARIOS = {
    120: "Status quo — current rate since 1 Jan 2022 (CO₂ Act SR 641.71, Ordinance SR 641.711 Art. 94a)",
    200: "Policy trajectory — revised CO₂ Act 2025-2030 ceiling CHF 210/t (consistent with EU ETS / BFE EP2050+)",
    300: "Full externality — IPCC AR6 WGIII 1.5°C pathway median (Rennert et al. 2022; US EPA 2023 SCC)",
}
