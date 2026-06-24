# SolarPalm AI: calculation core

This repository is the open-source calculation engine for SolarPalm AI, a
smartphone tool that helps people in Fiji work out whether rooftop solar is
worth it for them.

The engine answers one question with traceable numbers: if I put solar on this
roof, how much will it generate, how much will it save, and how long until it
pays for itself?

This repo is the numbers only. It has no app UI and no AR. The AR scanning
front-end and the financing-referral layer are separate, and both sit on top of
this core. The rest of this README explains the product they form together, then
documents the engine you can run today.

## The product this powers

SolarPalm AI is a one-stop phone tool for Fijian households and small
businesses. Fiji has about 92% electricity access, so the problem is not the
absence of power. It is high tariffs, diesel dependence, and unreliable supply,
plus a large amount of rooftop solar potential that no one has an easy way to
measure. Solar assessment today stays at utility and expert level, and existing
solar finance (credit-union savings collateral, payroll deduction) leaves out
informal workers, women, and outer-island residents.

The full app runs five steps:

1. Scan. The user points a phone at a roof. Computer vision detects the roof
   plane and estimates usable area, slope, and orientation.
2. Assess. The app overlays panels in AR and calls this engine to compute
   expected generation, bill and diesel savings, and payback period.
3. Size the investment. It estimates install cost and payback for that roof.
4. Show finance routes. It compares options such as installment plans,
   credit-union loans, and climate-fund programmes.
5. Refer. With the user's consent, it produces a first eligibility signal and
   points them to licensed local institutions (Fiji Development Bank, credit
   unions, fund programmes).

The boundary is fixed: SolarPalm AI diagnoses and connects. It does not lend
money and does not make credit decisions. Licensed local institutions do that.

This repository is step 2, the engine that produces the numbers the other steps
depend on. The numbers have to be right before anything built on them can be
trusted, so the core ships first and ships honest.

## What the engine does

Given a location and a system specification, it returns:

- Annual generation (kWh), with a monthly breakdown when PVGIS is used
- Annual bill savings (FJD)
- Simple payback period (years)

## Quickstart

Requires Python 3.9 or newer. Standard library only, nothing to install.

```bash
# Suva, 3 kWp rooftop system
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3
```

Real output from that command:

```
Location:          -18.14, 178.44
System:            3.0 kWp, tilt 10.0 deg, azimuth 0.0
Data source:       PVGIS-ERA5
Annual generation: 3816.6 kWh
CapEx:             FJD 9000.0
Annual savings:    FJD 1221.32
Payback:           7.37 years
```

More commands and recorded output are in [`examples/`](examples/README.md).

```bash
# JSON output, including the monthly breakdown
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3 --json

# Override tilt, azimuth, and economics
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 5 \
  --tilt 15 --azimuth 0 --tariff 0.34 --cost-per-kw 3200
```

## Data sources (public, no key)

| Source | Role | Notes |
|--------|------|-------|
| [PVGIS](https://re.jrc.ec.europa.eu/) (PVcalc, ERA5) | Primary | In-plane modelled PV output. Verified to cover Fiji. |
| [NASA POWER](https://power.larc.nasa.gov/) | Fallback | Horizontal irradiance only. Coarser estimate, flagged in output. |

If PVGIS fails, the engine falls back to NASA POWER and labels the result as a
fallback estimate. It never silently mixes the two. The detail is in
[`docs/data-sources.md`](docs/data-sources.md).

## Fiji baseline constants

All are overridable from the CLI. Defaults:

| Constant | Default | Source |
|----------|---------|--------|
| Install cost | FJD 3,000 / kW | academia.edu, "Role of solar PV in future electricity generation in Fiji" |
| Tariff | FJD 0.32 / kWh | Fiji Government MSME domestic rate (about 32c per unit) |
| System loss | 14% | PVGIS default |
| Fallback PR | 0.75 | conservative performance ratio for the NASA path |

These are documented defaults, not claims of precision. The engine does not
invent any number it cannot trace to a source or a user input.

## What this is not

- Not an app. No UI, no AR scanning, no mobile build in this repo.
- Not a lender. It makes no credit decision and moves no money.
- Not a precise site survey. It estimates potential; a real install still needs
  a professional check of the roof.

## How it works and where it fits

- The math is documented in [`docs/methodology.md`](docs/methodology.md).
- The data sources and Fiji coverage are in [`docs/data-sources.md`](docs/data-sources.md).
- How this core feeds the AR front-end and the referral layer is in
  [`docs/architecture.md`](docs/architecture.md).

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The math (generation, savings, payback) is unit tested offline. Network calls
are isolated in `solarpalm/datasources.py`, so the tests run without internet.

## Known limitations

- The NASA fallback uses horizontal irradiance, so it is rougher than the PVGIS
  in-plane model. For Suva at 3 kWp the two paths give 3,816.6 kWh (PVGIS) and
  4,049.3 kWh (NASA), which sets a sense of the spread.
- Payback is a simple, undiscounted figure (CapEx divided by annual savings). It
  does not model interest, panel degradation, or tariff changes.
- Roof slope and orientation come from the user or the AR layer. This core does
  not measure them.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). The short version: this repo is the
core only, tests must stay offline, and no constant lands without a traceable
source.

## License

MIT. An open core is the point: any Pacific operator should be able to inspect,
run, and extend these numbers.
