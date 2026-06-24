# Methodology

This document states every step the engine takes to turn a location and a
system size into generation, savings, and payback. It also states what each
number does not account for.

## Inputs

The engine needs a location and a system specification.

| Input | Required | Default | Meaning |
|-------|----------|---------|---------|
| latitude | yes | none | decimal degrees |
| longitude | yes | none | decimal degrees |
| capacity_kwp | yes | none | system size in kWp |
| tilt_deg | no | 10.0 | panel tilt from horizontal |
| azimuth_deg | no | 0.0 | PVGIS aspect: 0 equator-facing, -90 east, 90 west |
| system_loss_pct | no | 14.0 | DC system loss passed to PVGIS |
| cost_per_kw_fjd | no | 3000.0 | install cost, FJD per kW |
| tariff_fjd_per_kwh | no | 0.32 | grid tariff, FJD per kWh |

## Step 1: annual generation

There are two paths. The engine always tries PVGIS first.

### Primary path: PVGIS

PVGIS runs its own in-plane PV model. The engine sends location, capacity,
loss, tilt, and aspect, and reads back the yearly total `E_y` and the twelve
monthly totals `E_m`. The engine does no irradiance math of its own on this
path. It passes the system parameters in and reads the modelled kWh out. The
code is `fetch_pvgis` in `solarpalm/datasources.py`.

The data layer used is PVGIS-ERA5.

### Fallback path: NASA POWER

If the PVGIS call fails for any reason, the engine falls back to NASA POWER.
NASA POWER returns mean daily horizontal irradiance (`ALLSKY_SFC_SW_DWN`, annual
mean, kWh/m2/day). The engine then computes generation itself:

```
annual_kwh = capacity_kwp * daily_irradiance * 365 * performance_ratio
```

with `performance_ratio = 0.75`. This is `generation_from_irradiance` in
`solarpalm/core.py`.

This path is rougher than PVGIS for two reasons. It uses horizontal irradiance,
not the irradiance in the plane of a tilted panel, and it collapses a year into
one performance ratio. The output labels this path `NASA-POWER (fallback
estimate)` so a reader always knows which path produced the number. The two
paths are never mixed in one result.

## Step 2: annual bill savings

```
annual_savings_fjd = annual_kwh * tariff_fjd_per_kwh
```

This assumes every generated kWh displaces a kWh the household would otherwise
buy from the grid at the tariff. It does not model export tariffs, time-of-use
pricing, or self-consumption below 100%. For a household whose daytime load is
smaller than its generation, this overstates the bill saving, because surplus
energy may earn less than the retail tariff or nothing at all.

## Step 3: capital cost and payback

```
capex_fjd = capacity_kwp * cost_per_kw_fjd
payback_years = capex_fjd / annual_savings_fjd
```

Payback is simple and undiscounted. It is the install cost divided by the
first-year saving. It does not model:

- interest or the cost of financing
- panel degradation over time
- tariff changes over the system life
- inflation or the time value of money
- maintenance, inverter replacement, or insurance

If annual savings are zero or negative the engine raises an error rather than
returning an infinite or negative payback. See `payback_years` in
`solarpalm/core.py`.

## Worked example: Suva, 3 kWp

Command:

```bash
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3
```

PVGIS path, recorded output:

- annual generation: 3816.6 kWh
- CapEx: 3 kWp * FJD 3000 = FJD 9000.0
- annual savings: 3816.6 kWh * FJD 0.32 = FJD 1221.32
- payback: FJD 9000 / FJD 1221.32 = 7.37 years

The same location and size on the NASA fallback gives 4049.3 kWh and a 6.95 year
payback. The gap between the two paths is the subject of
[`data-sources.md`](data-sources.md).

## What the engine never does

- It never invents a number. Every output traces to PVGIS, to NASA POWER, or to
  a documented constant the user can override.
- It never silently mixes the two data paths.
- It never claims site-survey precision. Roof tilt and orientation come from the
  user or the AR layer, not from this core.
