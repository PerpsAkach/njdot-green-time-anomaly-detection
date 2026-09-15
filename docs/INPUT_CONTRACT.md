# MAIN Input Contract

The public runner accepts a single MAIN export as `.xlsx` or `.csv`.

## Required columns

| Column | Required | Expected content | Validation behavior |
|---|---:|---|---|
| `Green Time (Sec)` | Yes | Numeric seconds, `>= 0` | Non-numeric, non-finite, or negative values become `Invalid` rows. |
| `GT_mean` | Yes | Numeric baseline, `> 0` | Non-numeric, non-finite, zero, or negative values become `Invalid` rows. |

If either required column is absent, processing stops with a schema error rather than guessing a replacement column.

## Optional columns used by the public runner

| Column | Purpose |
|---|---|
| `DateConverted Hierarchy - Date` | Parsed when present to create one output sheet per valid calendar date and to report missing date values. |
| `Time` | Used with date to report duplicated complete date/time keys and missing time values. |

Other columns are preserved in `PROCESSED` without being interpreted by the Green-Time classifier.

## Invalid-row policy

The public pipeline does not silently impute operational values. A row can therefore remain in the output with:

```text
GT_Anomaly = Invalid
GT_Severity = Invalid
GT_Reason = <deterministic reason code>
```

Current reason codes are:

- `non_numeric`
- `non_finite`
- `negative_green_time`
- `non_positive_baseline`

## Date handling

Date grouping is optional. If the configured date column is absent, Green-Time processing still succeeds but no daily sheets are generated. If some date values cannot be parsed, those rows remain in `PROCESSED` and are excluded from daily sheets rather than being assigned an invented date.

## Data sensitivity

The public repository must not contain live controller identifiers, production credentials, site-sensitive configuration, or raw operational exports. The checked-in sample is demonstration data created specifically for the portfolio.
