# ECE Data Visualisation — datasets (FR / EN)

**Purpose:** immutable teaching snapshots shared by the English and French ECE Data Visualisation notebooks. These are real historical records, not synthetic examples. Data is publicly accessible; avoid pushing student submissions here.

## Files

| Path | Provenance | Data structure |
| --- | --- | --- |
| `uber/uber_apr2014.csv` | FiveThirtyEight / NYC TLC FOIL, Uber NYC April 2014 | Recorded pickup timestamp, latitude, longitude, base |
| `nyc_trips/green_taxi_2025_01.csv` | NYC TLC Green Taxi Trip Records, Jan 2025 | Selected trip records: pickup/dropoff timestamp, distance in miles, fare total, zones, passenger count |

The Green Taxi CSV is a **column-preserving export** of the original NYC TLC Parquet file. It does not intentionally filter or clean records. Compare like with like: the two sources cover different months, years and populations; they cannot directly establish competitive market shares.

Sources:
- https://github.com/fivethirtyeight/uber-tlc-foil-response
- https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

Dataset construction and schema checks are in `scripts/prepare_data.py`. `MANIFEST.json`, generated at preparation time, records row counts, URLs and SHA-256 for the original downloaded asset and exported teaching CSV. Do not invent or manually edit hashes.

## Notebook usage

In a notebook, first download the desired CSV from the **raw.githubusercontent.com** file URL (ideally pin a commit SHA) to `Path.cwd() / "data"`, and on every later run use `pd.read_csv` on the local path. The shared notebook should not import `mobility_io.py`.

Data files are created by the `ECE Data Visualisation - snapshots` GitHub Actions job. If these files are not present, the workflow needs to complete successfully before this mirror may be used in notebooks. **Do not replace missing real files with fictional CSVs under the same filename.**

## Data quality and licensing

These are third-party public records, provided with attribution. Their existence does not imply accuracy, representativeness, or endorsement by the source organizations. Invalid times, zero distances, anomalous amounts and missing fields are retained for student analysis rather than silently removed. Check relevant source usage terms before redistribution.
