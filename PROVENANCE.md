# Provenance

This repository separates historical evidence from current portfolio engineering so that operational and implementation claims remain defensible.

## RECOVERED

Supported by prior project/work artifacts or documented operational context:

- ITS / SCATS operational-monitoring context;
- Python-assisted Green-Time screening and repetitive validation work;
- use of MAIN `Green Time (Sec)` relative to row-level `GT_mean`;
- the 0.50 / 1.50 comparison band for Green-Time anomaly screening;
- conceptual separation of `GT_Anomaly` from `Phase_Flag`;
- date-oriented / batch-validation workflow concept;
- historical existence of related export categories such as EVENTS, PHASES, STATISTICS, and SIGNAL GROUPS.

Recovered context does **not** establish that the current public source tree is literal historical production code.

## RECONSTRUCTED

Current code rebuilt from the supported workflow where original source bytes or production artifacts were not available:

- modular Python classifier structure;
- MAIN DataFrame enrichment;
- command-line processing entry point;
- Excel run-report/output structure;
- small standalone `evaluate_phase_flag()` primitive preserving the anomaly/diagnostic distinction.

The public implementation is therefore a reconstruction of the supported methodology, not a claim of byte-for-byte recovery.

## ENHANCED

New portfolio-quality engineering added after reconstruction:

- validated threshold configuration;
- configurable CLI thresholds;
- explicit invalid-input reason codes;
- ratio and row-level threshold fields;
- severity labels;
- CSV as well as XLSX MAIN ingestion;
- safe handling of empty exports with the required schema;
- non-destructive data-quality metrics;
- duplicate date/time-key screening;
- parseable-date grouping and per-day workbook sheets;
- review-oriented workbook formatting with frozen headers, filters, bounded widths, and percentage formatting;
- UTC-stamped output filenames for unambiguous run traceability;
- sanitized demonstration data with stable expected-result tests;
- reusable processing/reporting functions;
- expanded unit and workbook integration tests;
- Python 3.11 / 3.12 / 3.13 GitHub Actions CI;
- source compilation checks;
- Ruff linting as a quality gate;
- `pip-audit` dependency-vulnerability scanning;
- sanitized end-to-end CLI smoke testing;
- bounded dependency ranges;
- explicit input/output contracts, operational-safety documentation, and implementation-status tracking.

## UNVERIFIED / NOT CLAIMED

This repository does not present the following as established historical or current production facts:

- an exact historical source tree or commit history;
- the exact production implementation of EVENTS / PHASES / STATISTICS / SIGNAL GROUPS joins;
- production controller identifiers, credentials, site mappings, timing plans, or live operational data;
- an autonomous traffic-control or remediation capability;
- a machine-learning model for anomaly detection;
- root-cause diagnosis from Green-Time thresholds alone;
- universal applicability of the default thresholds to every signal, plan, or operating condition.

## Data boundary

No live NJDOT/SCATS operational records, credentials, production-site configuration, or sensitive controller information are included. `sample_data/main_sanitized.csv` is demonstration data created for the public portfolio.
