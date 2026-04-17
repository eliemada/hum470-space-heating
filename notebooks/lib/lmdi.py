"""LMDI-I (Logarithmic Mean Divisia Index) decomposition engine.

Implements both 3-factor and 4-factor additive LMDI following Ang (2004).
The decomposition is *exact*: the sum of all factor effects equals the
observed total change, with no residual.
"""

from __future__ import annotations

import numpy as np
import polars as pl


def _log_mean(a: float, b: float) -> float:
    """Logarithmic mean L(a, b) = (a - b) / ln(a/b), with L(a, a) = a."""
    if a <= 0 or b <= 0:
        return 0.0
    if abs(a - b) < 1e-12:
        return a
    return (a - b) / np.log(a / b)


# ────────────────────────────────────────────────────────────────────────
# 3-Factor LMDI: E = P × HDD × Intensity
# ────────────────────────────────────────────────────────────────────────

def compute_lmdi_3factor(df: pl.DataFrame) -> pl.DataFrame:
    """Three-factor additive LMDI decomposition.

    Parameters
    ----------
    df : DataFrame
        Must contain columns: ``year``, ``E`` (energy), ``population``,
        ``hdd``, ``intensity`` (= E / (P × HDD)).

    Returns
    -------
    DataFrame with annual and cumulative decomposition columns:
        ``year``, ``dE_pop``, ``dE_weather``, ``dE_intensity``, ``dE_total``,
        ``cum_pop``, ``cum_weather``, ``cum_intensity``, ``cum_total``.
    """
    years = df["year"].to_list()
    E = df["E"].to_list()
    P = df["population"].to_list()
    HDD = df["hdd"].to_list()
    I = df["intensity"].to_list()

    records: list[dict] = []
    for t in range(1, len(years)):
        L = _log_mean(E[t], E[t - 1])
        records.append({
            "year": years[t],
            "dE_pop": L * np.log(P[t] / P[t - 1]),
            "dE_weather": L * np.log(HDD[t] / HDD[t - 1]),
            "dE_intensity": L * np.log(I[t] / I[t - 1]),
            "dE_total": E[t] - E[t - 1],
        })

    return (
        pl.DataFrame(records)
        .with_columns(
            pl.col("dE_pop").cum_sum().alias("cum_pop"),
            pl.col("dE_weather").cum_sum().alias("cum_weather"),
            pl.col("dE_intensity").cum_sum().alias("cum_intensity"),
            pl.col("dE_total").cum_sum().alias("cum_total"),
        )
    )


# ────────────────────────────────────────────────────────────────────────
# 4-Factor LMDI: E = P × (A/P) × HDD × (E / (A × HDD))
# ────────────────────────────────────────────────────────────────────────

def compute_lmdi_4factor(df: pl.DataFrame) -> pl.DataFrame:
    """Four-factor additive LMDI decomposition.

    Parameters
    ----------
    df : DataFrame
        Must contain columns: ``year``, ``E`` (energy), ``population``,
        ``floor_area`` (total, e.g. Mio m²), ``hdd``.
        The function computes derived ratios internally.

    Returns
    -------
    DataFrame with annual and cumulative decomposition columns:
        ``year``, ``dE_pop``, ``dE_floor``, ``dE_weather``, ``dE_intensity``,
        ``dE_total``, ``cum_pop``, ``cum_floor``, ``cum_weather``,
        ``cum_intensity``, ``cum_total``.
    """
    years = df["year"].to_list()
    E = df["E"].to_list()
    P = df["population"].to_list()
    A = df["floor_area"].to_list()
    HDD = df["hdd"].to_list()

    # Derived factors
    floor_pc = [a / p for a, p in zip(A, P)]           # A/P
    intensity = [e / (a * h) for e, a, h in zip(E, A, HDD)]  # E/(A×HDD)

    records: list[dict] = []
    for t in range(1, len(years)):
        L = _log_mean(E[t], E[t - 1])
        records.append({
            "year": years[t],
            "dE_pop": L * np.log(P[t] / P[t - 1]),
            "dE_floor": L * np.log(floor_pc[t] / floor_pc[t - 1]),
            "dE_weather": L * np.log(HDD[t] / HDD[t - 1]),
            "dE_intensity": L * np.log(intensity[t] / intensity[t - 1]),
            "dE_total": E[t] - E[t - 1],
        })

    return (
        pl.DataFrame(records)
        .with_columns(
            pl.col("dE_pop").cum_sum().alias("cum_pop"),
            pl.col("dE_floor").cum_sum().alias("cum_floor"),
            pl.col("dE_weather").cum_sum().alias("cum_weather"),
            pl.col("dE_intensity").cum_sum().alias("cum_intensity"),
            pl.col("dE_total").cum_sum().alias("cum_total"),
        )
    )


def verify_decomposition(df_lmdi: pl.DataFrame, n_factors: int = 3) -> float:
    """Return the decomposition residual (should be ~0 for exact LMDI).

    Works for both 3-factor and 4-factor results.
    """
    last = df_lmdi[-1]
    factor_sum = last["cum_pop"].item() + last["cum_weather"].item() + last["cum_intensity"].item()
    if n_factors == 4:
        factor_sum += last["cum_floor"].item()
    return last["cum_total"].item() - factor_sum
