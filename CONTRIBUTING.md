# Contributing

Thanks for looking at the SolarPalm AI calculation core. This repository is the
numbers only. Three rules keep it trustworthy.

## 1. This repo is the core, not the app

No app code lands here. No UI, no AR or camera code, no financing or credit
logic. Those are separate layers, described in
[`docs/architecture.md`](docs/architecture.md). A pull request that adds them to
this repo is out of scope and will be declined. This repo computes generation,
savings, and payback, and nothing else.

## 2. Tests stay offline

The math is unit tested with no network access. Network calls live only in
`solarpalm/datasources.py`, and tests stub them out (see
`tests/test_core.py`). Any new test must run with no internet. Run the suite
with:

```bash
python3 -m unittest discover -s tests -v
```

All tests must pass before a change is merged.

## 3. No untraceable numbers

Every constant must trace to a named source or to a user input. If you add or
change a default, the same commit must add a source comment next to it, in the
style already used in `solarpalm/constants.py`. A number with no source does not
land. The engine's promise to the reader is that it never invents a figure, and
that promise is enforced here.

## How to make a change

1. Keep changes additive where you can. Do not rewrite working code to restyle
   it.
2. Match the existing style: standard library only, Python 3.9+, no third-party
   dependencies.
3. Run the tests offline and confirm they pass.
4. If you touched a default or a formula, update the relevant file in `docs/`.
5. Open a pull request that states what changed and what source backs any new
   number.

## Scope of dependencies

The core has zero runtime dependencies and targets the standard library. A pull
request that adds a dependency needs a clear reason in its description, because
the point of the core is that it runs anywhere Python does.
