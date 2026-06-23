"""Fiji baseline constants. All values are overridable via the CLI.

Sources are documented in README.md. These are defaults, not assertions of
precision. The engine never fabricates a number it cannot trace to a source
or a user input.
"""

# Rooftop PV installed cost, FJD per kW.
# Source: academia.edu, "Role of solar PV in future electricity generation in
# Fiji" (rooftop system around FJD 3,000/kW).
DEFAULT_COST_PER_KW_FJD = 3000.0

# MSME / domestic electricity tariff, FJD per kWh.
# Source: Fiji Government, MSME domestic rate around 32c per unit.
DEFAULT_TARIFF_FJD_PER_KWH = 0.32

# Default DC system loss (%) passed to PVGIS.
DEFAULT_SYSTEM_LOSS_PCT = 14.0

# Performance ratio for the NASA POWER fallback estimate (dimensionless).
# The fallback uses horizontal irradiance only, so this PR is deliberately
# conservative. It is a coarse estimate, flagged as such in the output.
DEFAULT_FALLBACK_PR = 0.75
