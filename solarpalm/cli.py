"""Command-line interface for the SolarPalm AI calculation core."""

import argparse
import json

from .core import Economics, SystemSpec, estimate


def main(argv=None):
    p = argparse.ArgumentParser(
        prog="solarpalm",
        description="SolarPalm AI: rooftop solar generation, savings and payback (Fiji)",
    )
    p.add_argument("--lat", type=float, required=True, help="latitude")
    p.add_argument("--lon", type=float, required=True, help="longitude")
    p.add_argument("--kwp", type=float, required=True, help="system capacity in kWp")
    p.add_argument("--tilt", type=float, default=10.0, help="panel tilt in degrees")
    p.add_argument(
        "--azimuth",
        type=float,
        default=0.0,
        help="PVGIS aspect: 0 = equator-facing, -90 = east, 90 = west",
    )
    p.add_argument("--loss", type=float, default=14.0, help="DC system loss in %%")
    p.add_argument("--cost-per-kw", type=float, default=None, help="install cost FJD/kW")
    p.add_argument("--tariff", type=float, default=None, help="tariff FJD/kWh")
    p.add_argument(
        "--source",
        choices=["pvgis", "nasa"],
        default="pvgis",
        help="primary data source (pvgis falls back to nasa on failure)",
    )
    p.add_argument("--json", action="store_true", help="emit JSON")
    args = p.parse_args(argv)

    spec = SystemSpec(
        latitude=args.lat,
        longitude=args.lon,
        capacity_kwp=args.kwp,
        tilt_deg=args.tilt,
        azimuth_deg=args.azimuth,
        system_loss_pct=args.loss,
    )
    econ = Economics()
    if args.cost_per_kw is not None:
        econ.cost_per_kw_fjd = args.cost_per_kw
    if args.tariff is not None:
        econ.tariff_fjd_per_kwh = args.tariff

    prefer = "pvgis" if args.source == "pvgis" else "nasa"
    est = estimate(spec, econ, prefer=prefer)

    if args.json:
        print(json.dumps(est.__dict__, indent=2))
        return

    print(f"Location:          {args.lat}, {args.lon}")
    print(f"System:            {args.kwp} kWp, tilt {args.tilt} deg, azimuth {args.azimuth}")
    print(f"Data source:       {est.source}")
    print(f"Annual generation: {est.annual_kwh} kWh")
    print(f"CapEx:             FJD {est.capex_fjd}")
    print(f"Annual savings:    FJD {est.annual_savings_fjd}")
    print(f"Payback:           {est.payback_years} years")


if __name__ == "__main__":
    main()
