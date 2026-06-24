# Examples

Every command below was run against the live public APIs. The output shown is
the recorded output of that run, not an illustration. The exact figures can move
slightly as PVGIS and NASA POWER update their datasets.

## 1. Suva, 3 kWp, human-readable

```bash
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3
```

```
Location:          -18.14, 178.44
System:            3.0 kWp, tilt 10.0 deg, azimuth 0.0
Data source:       PVGIS-ERA5
Annual generation: 3816.6 kWh
CapEx:             FJD 9000.0
Annual savings:    FJD 1221.32
Payback:           7.37 years
```

The source line reads `PVGIS-ERA5`, so this is the primary path.

## 2. Suva, 3 kWp, JSON with the monthly breakdown

```bash
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3 --json
```

```json
{
  "annual_kwh": 3816.6,
  "source": "PVGIS-ERA5",
  "capex_fjd": 9000.0,
  "annual_savings_fjd": 1221.32,
  "payback_years": 7.37,
  "monthly_kwh": [
    420.4,
    358.7,
    344.1,
    274.3,
    236.4,
    196.5,
    219.0,
    263.1,
    311.0,
    366.6,
    401.8,
    424.7
  ]
}
```

The monthly array runs January to December. Generation peaks in the Fijian
summer (December, 424.7 kWh) and dips in the cooler, cloudier middle of the year
(June, 196.5 kWh). The monthly breakdown is only present on the PVGIS path.

## 3. Suva, 3 kWp, forced NASA fallback

```bash
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 3 --source nasa
```

```
Location:          -18.14, 178.44
System:            3.0 kWp, tilt 10.0 deg, azimuth 0.0
Data source:       NASA-POWER (fallback estimate)
Annual generation: 4049.3 kWh
CapEx:             FJD 9000.0
Annual savings:    FJD 1295.76
Payback:           6.95 years
```

The source line reads `NASA-POWER (fallback estimate)`, and there is no monthly
array. This path reads about 6% higher than PVGIS for the same roof. The reason
is in [`../docs/data-sources.md`](../docs/data-sources.md).

## 4. Override tilt, azimuth, and economics

```bash
python3 -m solarpalm.cli --lat -18.14 --lon 178.44 --kwp 5 \
  --tilt 15 --azimuth 0 --tariff 0.34 --cost-per-kw 3200
```

```
Location:          -18.14, 178.44
System:            5.0 kWp, tilt 15.0 deg, azimuth 0.0
Data source:       PVGIS-ERA5
Annual generation: 6127.9 kWh
CapEx:             FJD 16000.0
Annual savings:    FJD 2083.48
Payback:           7.68 years
```

Every constant from the README table is overridable on the command line. Here a
5 kWp system at 15 degree tilt is priced at FJD 3200/kW against a FJD 0.34
tariff. Use `--source nasa` on any of these to force the fallback path.
