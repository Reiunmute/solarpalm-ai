# Data sources

The engine uses two public datasets, both free and neither needing an API key.
PVGIS is primary. NASA POWER is the fallback.

## PVGIS (primary)

- Provider: European Commission Joint Research Centre.
- Endpoint: `https://re.jrc.ec.europa.eu/api/v5_2/PVcalc`
- What it returns: modelled PV output in the plane of the panel, as a yearly
  total and twelve monthly totals.
- Why it is primary: PVGIS models the panel at its real tilt and orientation,
  applies the system loss, and returns energy already in kWh. The engine does
  no irradiance math on this path, so there is less to get wrong locally.

### Fiji coverage

PVGIS-ERA5 covers Fiji. The engine was tested live against Suva
(-18.14, 178.44) and PVGIS returned a full monthly and annual series. Coverage
was verified before PVGIS was made the primary source.

## NASA POWER (fallback)

- Provider: NASA Langley Research Center.
- Endpoint: `https://power.larc.nasa.gov/api/temporal/climatology/point`
- Parameter read: `ALLSKY_SFC_SW_DWN`, annual mean daily irradiance on a
  horizontal surface (kWh/m2/day).
- What the engine does with it: applies the generation formula in
  [`methodology.md`](methodology.md) with a performance ratio of 0.75.

### When the fallback triggers

The fallback runs only when the PVGIS call fails: a network error, a timeout, or
a response the parser does not recognise. The user can also force it with
`--source nasa`. When the fallback is used, the output source label reads
`NASA-POWER (fallback estimate)`, so the path is always visible.

## Cross-check: how far apart are the two paths

For Suva at 3 kWp, default tilt 10 degrees, the two paths give:

| Path | Annual generation | Payback |
|------|-------------------|---------|
| PVGIS-ERA5 | 3816.6 kWh | 7.37 years |
| NASA POWER (fallback) | 4049.3 kWh | 6.95 years |

The fallback reads about 6% higher here. That is expected. The fallback uses
horizontal irradiance and a single flat performance ratio, so it does not see
the loss from a tilted panel facing away from the optimum, and it does not
capture seasonal shape. Treat the fallback as a coarse upper-ish estimate, not a
substitute for the PVGIS number.

### Reproduce it

```bash
# PVGIS (primary)
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3

# NASA POWER (forced fallback)
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3 --source nasa
```

Both calls hit live public APIs, so the exact figures can move slightly as the
upstream datasets update. The roughly 6% gap between the paths is the stable
point, not the last decimal.

## Why two sources at all

A single source with no fallback fails closed: if PVGIS is down, the user gets
nothing. With a labelled fallback the user still gets a usable, clearly marked
estimate. The cost is that the two paths do not agree to the decimal, which is
why every result carries its source.
