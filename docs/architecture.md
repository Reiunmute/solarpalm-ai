# Architecture and where this core fits

This repository is one layer of SolarPalm AI: the calculation core. It produces
the numbers. Two other layers sit on top of it. This document describes all
three and the boundary between them.

## The three layers

```
+-------------------------------------------------------------+
|  AR front-end (separate, planned)                           |
|  - phone camera + ARCore detects the roof plane             |
|  - estimates usable area, slope, orientation                |
|  - overlays panels so the user sees the layout              |
+----------------------------+--------------------------------+
                             | roof area, tilt, orientation, location
                             v
+-------------------------------------------------------------+
|  Calculation core  (THIS REPO)                              |
|  - PVGIS primary, NASA POWER fallback                       |
|  - generation -> savings -> payback                         |
|  - deterministic, traceable, offline-testable               |
+----------------------------+--------------------------------+
                             | generation, savings, payback
                             v
+-------------------------------------------------------------+
|  Financing-referral layer (separate, planned)               |
|  - compares install cost against finance routes             |
|  - produces a first eligibility signal, with consent        |
|  - refers to licensed local institutions                    |
+-------------------------------------------------------------+
```

## What each layer owns

### AR front-end

Owns measurement. It turns a camera view into a roof: usable area, slope, and
orientation. It is where the computer-vision model lives. It hands the core a
location and a system specification. It is a separate project and is not in this
repository.

### Calculation core (this repo)

Owns the numbers. Given a location and a system specification, it returns annual
generation, annual savings, and payback, each tagged with the data source that
produced it. It is deterministic physics and data lookups, not a model that
learns. It has no UI and no camera code. It is unit tested offline because the
network calls are isolated in `solarpalm/datasources.py`.

The public surface is small:

- `solarpalm/core.py`: the math and the `estimate` orchestration.
- `solarpalm/datasources.py`: the two API clients.
- `solarpalm/constants.py`: the Fiji default constants.
- `solarpalm/cli.py`: the command-line entry point.

### Financing-referral layer

Owns the connection to money, but not money itself. It takes the core's cost and
payback, compares finance routes (installment plans, credit-union loans, climate
fund programmes), and with the user's consent produces a first eligibility
signal and a referral. It is a separate project and is not in this repository.

## The boundary that does not move

SolarPalm AI diagnoses and connects. It does not lend and it does not decide
credit. The eligibility signal in the referral layer is a first filter, not an
approval. Licensed local institutions (for example the Fiji Development Bank,
credit unions, fund programmes) make every credit decision and move every
dollar. This boundary is a design rule and a regulatory one, and it holds across
all three layers.

## Why the core ships first and ships alone

The numbers have to be right before anything built on them can be trusted. A
roof scan that feeds a wrong generation figure, or a referral built on a wrong
payback, is worse than no tool. So the core is the first thing made public, on
its own, with its sources and its limits stated. The AR and referral layers
build on a core a stranger can already inspect and run.
