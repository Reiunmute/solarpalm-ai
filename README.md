# SolarPalm AI: calculation core

Rooftop solar potential and savings estimator for Fiji. This is the open-source
calculation engine behind SolarPalm AI, an entry for the UNFCCC Technology
Mechanism AI for Climate Action (AICA) Award 2026 (Fiji, SIDS).

The engine answers one question with traceable numbers: **"If I put solar on
this roof, how much will it generate, how much will it save, and how long until
it pays for itself?"**

No app UI, no AR here. This repository is the trustworthy numeric core that the
AR front-end and the financing-referral layer both build on.

## What it does

Given a location and a system specification, it returns:

- Annual generation (kWh), with a monthly breakdown when PVGIS is used
- Annual bill savings (FJD)
- Simple payback period (years)

## Data sources (public, no key)

| Source | Role | Notes |
|--------|------|-------|
| [PVGIS](https://re.jrc.ec.europa.eu/) (PVcalc, ERA5) | Primary | In-plane modelled PV output. Verified to cover Fiji. |
| [NASA POWER](https://power.larc.nasa.gov/) | Fallback | Horizontal irradiance only. Coarser estimate, flagged in output. |

If PVGIS fails, the engine falls back to NASA POWER and labels the result as a
fallback estimate. It never silently mixes the two.

## Fiji baseline constants

All are overridable from the CLI. Defaults:

| Constant | Default | Source |
|----------|---------|--------|
| Install cost | FJD 3,000 / kW | academia.edu, "Role of solar PV in future electricity generation in Fiji" |
| Tariff | FJD 0.32 / kWh | Fiji Government MSME domestic rate (~32c per unit) |
| System loss | 14% | PVGIS default |
| Fallback PR | 0.75 | conservative performance ratio for the NASA path |

These are documented defaults, not claims of precision. The engine does not
invent any number it cannot trace to a source or a user input.

## Usage

Requires Python 3.9+. Standard library only, no dependencies to install.

```bash
# Suva, 3 kWp rooftop system
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3

# JSON output
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3 --json

# Override tilt, azimuth, and economics
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 5 \
  --tilt 15 --azimuth 0 --tariff 0.34 --cost-per-kw 3200
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The math (generation, savings, payback) is unit tested offline. Network calls
are isolated in `solarpalm/datasources.py`.

## Scope and honesty

This core computes potential and economics. It does **not** make credit
decisions or lend money. In the wider SolarPalm AI design, financing is handled
by licensed local institutions; this engine only produces the numbers a
household needs to understand its options.

Known limitations:

- The NASA fallback uses horizontal irradiance, so it is a rougher estimate than
  the PVGIS in-plane model.
- Payback is a simple, undiscounted figure (CapEx / annual savings).

## License

MIT. Open source is an eligibility requirement of the AICA Award, and an open
core is the point: any Pacific operator should be able to inspect, run, and
extend these numbers.
