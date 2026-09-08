# NJDOT Green-Time Anomaly Detection

Python-based ITS/SCATS operational data-validation project for screening abnormal traffic-signal Green Time and supporting batch review workflows.

## What it demonstrates

- Python automation
- Explainable rule-based anomaly detection
- Operational/traffic-data validation
- Batch processing and reporting
- Separation of Green-Time anomalies from phase/signal-group diagnostics
- Domain-driven engineering and auditability

## Core rule

`GT_Anomaly` is derived from MAIN `Green Time (Sec)` compared with MAIN `GT_mean`:

```text
Anomaly if Green Time < 0.50 * GT_mean
        or Green Time > 1.50 * GT_mean
```

The project intentionally keeps this separate from `Phase_Flag`, which represents independent phase/signal-group consistency logic.

## Run

```bash
pip install -r requirements.txt
python run_pipeline.py --main path/to/site.xlsx --output outputs
```

No live NJDOT/SCATS operational data or sensitive site configuration are included. See `PROVENANCE.md` for reconstruction details.
