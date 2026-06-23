"""Unit tests for the pure calculation math. No network access."""

import unittest

from solarpalm import constants
from solarpalm.core import (
    Economics,
    Estimate,
    SystemSpec,
    annual_savings,
    estimate,
    generation_from_irradiance,
    payback_years,
)


class TestCore(unittest.TestCase):
    def test_generation_from_irradiance(self):
        # 1 kWp, 5 kWh/m2/day, PR 0.75 -> 1 * 5 * 365 * 0.75 = 1368.75
        self.assertAlmostEqual(
            generation_from_irradiance(1.0, 5.0, 0.75), 1368.75, places=2
        )

    def test_annual_savings(self):
        self.assertAlmostEqual(annual_savings(1000.0, 0.32), 320.0, places=2)

    def test_payback(self):
        # 3 kWp * 3000 = 9000 capex; savings 1500/yr -> 6 years
        self.assertAlmostEqual(payback_years(9000.0, 1500.0), 6.0, places=2)

    def test_payback_zero_savings_raises(self):
        with self.assertRaises(ValueError):
            payback_years(1000.0, 0.0)

    def test_fiji_defaults(self):
        self.assertEqual(constants.DEFAULT_COST_PER_KW_FJD, 3000.0)
        self.assertEqual(constants.DEFAULT_TARIFF_FJD_PER_KWH, 0.32)

    def test_estimate_nasa_fallback_offline(self):
        # Force the NASA path but stub the network call to keep the test offline.
        from solarpalm import datasources

        original = datasources.fetch_nasa_irradiance
        datasources.fetch_nasa_irradiance = lambda lat, lon, timeout=30: 5.0
        try:
            spec = SystemSpec(latitude=-18.14, longitude=178.44, capacity_kwp=3.0)
            est = estimate(spec, Economics(), prefer="nasa")
        finally:
            datasources.fetch_nasa_irradiance = original

        self.assertIsInstance(est, Estimate)
        self.assertIn("NASA", est.source)
        # 3 kWp * 5 * 365 * 0.75 = 4106.25 kWh
        self.assertAlmostEqual(est.annual_kwh, 4106.2, places=1)
        # capex 3 * 3000 = 9000; savings 4106.25 * 0.32 = 1314.0
        self.assertAlmostEqual(est.capex_fjd, 9000.0, places=1)
        self.assertAlmostEqual(est.annual_savings_fjd, 1314.0, places=1)


if __name__ == "__main__":
    unittest.main()
