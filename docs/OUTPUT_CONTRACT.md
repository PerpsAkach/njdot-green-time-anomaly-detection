# Output Workbook Contract

The command-line runner writes one timestamped `.xlsx` workbook per run.

## `RUN_REPORT`

One summary row containing:

- source file name;
- total row count;
- valid / invalid / anomalous / normal counts;
- counts for each Green-Time severity tier;
- anomaly rate over valid rows;
- missing Green Time / baseline counts;
- missing date / time counts when those columns are present;
- duplicated complete date/time-key count.

`GT_Anomaly_Rate` is defined as:

```text
GT_Anomalies / GT_Valid
```

and is `0.0` when no valid rows exist.

## `PROCESSED`

Contains every input row plus the classifier outputs:

| Output field | Meaning |
|---|---|
| `GT_Anomaly` | `Anomaly`, `No Anomaly`, or `Invalid` |
| `GT_Severity` | `Severe-Low`, `Anomaly-Low`, `Normal`, `Anomaly-High`, `Severe-High`, or `Invalid` |
| `GT_Ratio` | observed Green Time divided by `GT_mean` |
| `GT_Low_Threshold` | row-level low anomaly threshold |
| `GT_High_Threshold` | row-level high anomaly threshold |
| `GT_Reason` | deterministic explanation code |

Invalid rows retain the source fields and receive `NaN` for numerical derived fields where a valid ratio/threshold cannot be calculated.

## Daily sheets

When `DateConverted Hierarchy - Date` is present and parseable, the workbook also contains one sheet per date using `YYYY-MM-DD` naming. Daily sheets are subsets of `PROCESSED`; they do not alter classification logic.

Rows with invalid/unparseable dates remain in `PROCESSED` and are not placed into a fabricated daily bucket.

## Interpretation boundary

Workbook classifications are screening outputs. They are not controller-fault diagnoses, traffic-engineering directives, or autonomous control decisions.
