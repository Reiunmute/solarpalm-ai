"""Open-data irradiance/PV sources: PVGIS (primary) and NASA POWER (fallback).

Both are public APIs requiring no key. Only stdlib is used so the core runs
anywhere with Python 3.9+.
"""

import json
import urllib.parse
import urllib.request

PVGIS_URL = "https://re.jrc.ec.europa.eu/api/v5_2/PVcalc"
NASA_POWER_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"


class DataSourceError(Exception):
    """Raised when an upstream API response cannot be parsed."""


def _get_json(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "SolarPalmAI/0.1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_pvgis(lat, lon, peakpower_kwp, loss_pct, tilt_deg, azimuth_deg, timeout=30):
    """Return (annual_kwh, monthly_kwh_list) from PVGIS PVcalc.

    PVGIS aspect convention: 0 = equator-facing, -90 = east, 90 = west.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "peakpower": peakpower_kwp,
        "loss": loss_pct,
        "angle": tilt_deg,
        "aspect": azimuth_deg,
        "outputformat": "json",
    }
    url = PVGIS_URL + "?" + urllib.parse.urlencode(params)
    data = _get_json(url, timeout=timeout)
    try:
        totals = data["outputs"]["totals"]["fixed"]
        monthly = data["outputs"]["monthly"]["fixed"]
    except (KeyError, TypeError) as exc:
        raise DataSourceError("unexpected PVGIS response shape") from exc
    annual_kwh = totals["E_y"]
    monthly_kwh = [m["E_m"] for m in monthly]
    return annual_kwh, monthly_kwh


def fetch_nasa_irradiance(lat, lon, timeout=30):
    """Return annual mean daily horizontal irradiance (kWh/m^2/day)."""
    params = {
        "parameters": "ALLSKY_SFC_SW_DWN",
        "community": "RE",
        "longitude": lon,
        "latitude": lat,
        "format": "JSON",
    }
    url = NASA_POWER_URL + "?" + urllib.parse.urlencode(params)
    data = _get_json(url, timeout=timeout)
    try:
        ann = data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]["ANN"]
    except (KeyError, TypeError) as exc:
        raise DataSourceError("unexpected NASA POWER response shape") from exc
    return ann
