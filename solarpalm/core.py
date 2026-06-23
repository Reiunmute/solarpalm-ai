"""Calculation core: location + system -> generation -> savings -> payback.

Pure math functions are kept separate from network calls so they can be unit
tested without hitting any API.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from . import constants, datasources


@dataclass
class SystemSpec:
    latitude: float
    longitude: float
    capacity_kwp: float
    tilt_deg: float = 10.0
    azimuth_deg: float = 0.0
    system_loss_pct: float = constants.DEFAULT_SYSTEM_LOSS_PCT


@dataclass
class Economics:
    cost_per_kw_fjd: float = constants.DEFAULT_COST_PER_KW_FJD
    tariff_fjd_per_kwh: float = constants.DEFAULT_TARIFF_FJD_PER_KWH


@dataclass
class Estimate:
    annual_kwh: float
    source: str
    capex_fjd: float
    annual_savings_fjd: float
    payback_years: float
    monthly_kwh: List[float] = field(default_factory=list)


def generation_from_irradiance(capacity_kwp, daily_irradiance, performance_ratio):
    """Annual kWh from mean daily horizontal irradiance.

    annual = capacity * irradiance(kWh/m2/day) * 365 * PR
    """
    return capacity_kwp * daily_irradiance * 365.0 * performance_ratio


def annual_savings(annual_kwh, tariff_fjd_per_kwh):
    """Annual bill offset, assuming generated energy displaces grid purchase."""
    return annual_kwh * tariff_fjd_per_kwh


def payback_years(capex_fjd, annual_savings_fjd):
    if annual_savings_fjd <= 0:
        raise ValueError("annual savings must be positive to compute payback")
    return capex_fjd / annual_savings_fjd


def estimate(spec, economics=None, prefer="pvgis", timeout=30):
    """Run the full estimate. Falls back to NASA POWER if PVGIS is unavailable."""
    economics = economics or Economics()
    source = None
    monthly: List[float] = []
    annual: Optional[float] = None

    if prefer == "pvgis":
        try:
            annual, monthly = datasources.fetch_pvgis(
                spec.latitude,
                spec.longitude,
                spec.capacity_kwp,
                spec.system_loss_pct,
                spec.tilt_deg,
                spec.azimuth_deg,
                timeout=timeout,
            )
            source = "PVGIS-ERA5"
        except Exception:
            annual = None

    if annual is None:
        daily = datasources.fetch_nasa_irradiance(
            spec.latitude, spec.longitude, timeout=timeout
        )
        annual = generation_from_irradiance(
            spec.capacity_kwp, daily, constants.DEFAULT_FALLBACK_PR
        )
        source = "NASA-POWER (fallback estimate)"

    capex = spec.capacity_kwp * economics.cost_per_kw_fjd
    savings = annual_savings(annual, economics.tariff_fjd_per_kwh)
    payback = payback_years(capex, savings)

    return Estimate(
        annual_kwh=round(annual, 1),
        source=source,
        capex_fjd=round(capex, 2),
        annual_savings_fjd=round(savings, 2),
        payback_years=round(payback, 2),
        monthly_kwh=[round(m, 1) for m in monthly],
    )
