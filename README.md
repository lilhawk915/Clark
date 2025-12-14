# Clark Distress Data Collectors

This repository contains collection scripts for public records that help monitor property distress signals in Clark County, Ohio.

## Permit reports (Clark County, OH)

A new collector, `collectors/permit_reports.py`, handles weekly building permit reports for Clark County:

- Configuration lives in `configs/clark_county_oh.json`, which stores placeholder weekly PDF URLs and the output directory path.
- When executed, the collector will download each weekly permit PDF to `outputs/clark/permits/raw/`. The current implementation uses mocked URLs and placeholder PDF content; TODO comments mark where live endpoints and parsing logic will be added later.
- A parser stub is included to eventually extract permit records with the fields: permit_number, address, issue_date, permit_type, and status. Parsed data will later be saved in a structured format (e.g., CSV or JSON).

> Note: The collector intentionally avoids scraping live sites until real endpoints and selectors are confirmed.

## Recorder search plans

Generate a CSV plan for recorder search strategies:

```
python3 collectors/recorder_search_plan.py
```

The CSV is written to `outputs/clark/recorder/search_plan.csv`.
