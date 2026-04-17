"""Monte Carlo scenario projection engine.

Simulates future Swiss residential space-heating energy demand under
parameter uncertainty using configurable distributions.
"""

from __future__ import annotations

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import polars as pl


@dataclass(frozen=True)
class ScenarioDef:
    """Deterministic scenario definition for overlay on the MC fan chart."""

    name: str
    reno_rate: float
    label: str
    color: str


# ── Default named scenarios ──────────────────────────────────────────
DEFAULT_SCENARIOS: dict[str, ScenarioDef] = {
    "BAU": ScenarioDef("BAU", 0.010, "BAU (1% reno)", "#FF9800"),
    "Accelerated": ScenarioDef("Accelerated", 0.020, "Accelerated (2% reno)", "#2196F3"),
    "Ambitious": ScenarioDef("Ambitious", 0.030, "Ambitious (3% reno)", "#4CAF50"),
}


@dataclass(frozen=True)
class MCBaseValues:
    """Observed values for the last historical year (launch point for MC)."""

    E: float           # Space-heating energy (TJ)
    population: float  # Total population
    hdd: float         # Heating degree days
    intensity: float   # E / (P × HDD)
    last_year: int     # Last observed year


def extract_base_values(df_lmdi_input: pl.DataFrame) -> MCBaseValues:
    """Extract MC base values from the last row of the LMDI input table."""
    last = df_lmdi_input.filter(
        pl.col("year") == df_lmdi_input["year"].max()
    )
    return MCBaseValues(
        E=last["E"].item(),
        population=last["population"].item(),
        hdd=last["hdd"].item(),
        intensity=last["intensity"].item(),
        last_year=int(last["year"].item()),
    )


def _interpolate_pop_projection(
    years: list[int],
    proj_years: list[int],
    proj_ref: list[float],
    proj_hi: list[float],
    proj_lo: list[float],
    base_pop: float,
    base_year: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Linearly interpolate BFS projection scenarios onto target years.

    Returns (ref, hi, lo) arrays of length len(years).
    """
    ref = np.interp(years, [base_year] + proj_years, [base_pop] + proj_ref)
    hi = np.interp(years, [base_year] + proj_years, [base_pop] + proj_hi)
    lo = np.interp(years, [base_year] + proj_years, [base_pop] + proj_lo)
    return ref, hi, lo


def run_monte_carlo(
    base: MCBaseValues,
    *,
    n_sims: int = 1000,
    target_year: int = 2050,
    pop_projections: pl.DataFrame | None = None,
    rng_seed: int = 42,
) -> dict:
    """Run Monte Carlo simulation and return trajectories + percentiles.

    Parameters
    ----------
    pop_projections : DataFrame, optional
        BFS population projections with columns ``year``, ``pop_reference``,
        ``pop_high``, ``pop_low``.  If provided, population uncertainty is
        sampled uniformly between the high/low BFS scenarios instead of using
        a naive linear extrapolation with Gaussian noise.

    Returns
    -------
    dict with keys:
        ``years``: list[int],
        ``trajectories``: ndarray (n_sims × n_years),
        ``p10``, ``p25``, ``p50``, ``p75``, ``p90``: ndarray (n_years,),
    """
    rng = np.random.default_rng(rng_seed)
    years = list(range(base.last_year + 1, target_year + 1))
    n_years = len(years)

    # Population projection: BFS scenarios or fallback linear
    if pop_projections is not None:
        _py = pop_projections["year"].to_list()
        _pr = pop_projections["pop_reference"].to_list()
        _ph = [float(v) for v in pop_projections["pop_high"].to_list()]
        _pl = [float(v) for v in pop_projections["pop_low"].to_list()]
        pop_ref, pop_hi, pop_lo = _interpolate_pop_projection(
            years, _py, _pr, _ph, _pl, base.population, base.last_year,
        )
        use_bfs = True
    else:
        pop_slope = (10_500_000 - base.population) / (2055 - base.last_year)
        use_bfs = False

    trajectories = np.zeros((n_sims, n_years))

    for sim in range(n_sims):
        reno = rng.uniform(0.008, 0.032)
        hdd_decline = rng.normal(-0.0025, 0.001)
        intensity_decline = 0.010 + reno * 0.5

        if use_bfs:
            # Sample between BFS low and high uniformly
            _alpha = rng.uniform(0.0, 1.0)
            pop_sim = pop_lo + _alpha * (pop_hi - pop_lo)
        else:
            pop_noise = rng.normal(0, 100_000)

        for yi, yr in enumerate(years):
            dt = yr - base.last_year
            if use_bfs:
                P_t = pop_sim[yi]
            else:
                P_t = base.population + pop_slope * dt + pop_noise
            HDD_t = base.hdd * (1 + hdd_decline) ** dt
            I_t = base.intensity * (1 - intensity_decline) ** dt
            trajectories[sim, yi] = P_t * HDD_t * I_t

    return {
        "years": years,
        "trajectories": trajectories,
        "p10": np.percentile(trajectories, 10, axis=0),
        "p25": np.percentile(trajectories, 25, axis=0),
        "p50": np.percentile(trajectories, 50, axis=0),
        "p75": np.percentile(trajectories, 75, axis=0),
        "p90": np.percentile(trajectories, 90, axis=0),
    }


def compute_named_trajectories(
    base: MCBaseValues,
    scenarios: dict[str, ScenarioDef] | None = None,
    *,
    target_year: int = 2050,
    pop_projections: pl.DataFrame | None = None,
    hdd_decline_rate: float = -0.0025,
) -> dict[str, list[float]]:
    """Compute deterministic trajectories for named scenarios.

    Uses BFS reference population projection if available, otherwise
    falls back to linear extrapolation toward 10.5M by 2055.

    Returns dict mapping scenario name → list of E values per year.
    """
    if scenarios is None:
        scenarios = DEFAULT_SCENARIOS

    years = list(range(base.last_year + 1, target_year + 1))

    if pop_projections is not None:
        _py = pop_projections["year"].to_list()
        _pr = pop_projections["pop_reference"].to_list()
        pop_ref, _, _ = _interpolate_pop_projection(
            years, _py, _pr, _pr, _pr, base.population, base.last_year,
        )
    else:
        pop_slope = (10_500_000 - base.population) / (2055 - base.last_year)
        pop_ref = np.array([base.population + pop_slope * (yr - base.last_year) for yr in years])

    result: dict[str, list[float]] = {}
    for name, sdef in scenarios.items():
        traj: list[float] = []
        for yi, yr in enumerate(years):
            dt = yr - base.last_year
            P = pop_ref[yi]
            HDD = base.hdd * (1 + hdd_decline_rate) ** dt
            I = base.intensity * (1 - (0.010 + sdef.reno_rate * 0.5)) ** dt
            traj.append(P * HDD * I)
        result[name] = traj
    return result


def compute_tornado_sensitivity(
    base: MCBaseValues,
    median_2050: float,
    *,
    pop_target_2055: float = 10_500_000,
) -> list[tuple[str, float]]:
    """One-at-a-time sensitivity analysis for 2050 energy demand.

    Returns list of (label, delta_E) tuples sorted by |delta_E| descending.
    """
    pop_slope = (pop_target_2055 - base.population) / (2055 - base.last_year)
    dt = 2050 - base.last_year

    def _E(pop_delta: float = 0, hdd_rate: float = -0.0025, reno: float = 0.020) -> float:
        P = base.population + pop_slope * dt + pop_delta
        H = base.hdd * (1 + hdd_rate) ** dt
        I = base.intensity * (1 - (0.010 + reno * 0.5)) ** dt
        return P * H * I

    sensitivities = [
        ("Population +500k", _E(pop_delta=500_000) - median_2050),
        ("Population \u2212500k", _E(pop_delta=-500_000) - median_2050),
        ("HDD decline \u22121.5%/dec", _E(hdd_rate=-0.0015) - median_2050),
        ("HDD decline \u22123.5%/dec", _E(hdd_rate=-0.0035) - median_2050),
        ("Reno rate 1.0%/yr", _E(reno=0.010) - median_2050),
        ("Reno rate 3.0%/yr", _E(reno=0.030) - median_2050),
    ]

    sensitivities.sort(key=lambda x: abs(x[1]), reverse=True)
    return sensitivities
