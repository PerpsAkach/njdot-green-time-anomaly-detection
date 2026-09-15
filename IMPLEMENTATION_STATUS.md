# Implementation Status

## Implemented and verified in the public repository

- MAIN `.xlsx` and `.csv` ingestion
- required Green-Time schema validation
- deterministic `Green Time (Sec)` vs `GT_mean` classification
- configurable low/high/severe thresholds
- absolute short-GT guard
- explicit invalid-input reason codes
- ratio and row-level threshold outputs
- run-level severity and anomaly counts
- non-destructive input data-quality metrics
- optional date grouping and one sheet per parseable date
- consolidated Excel workbook output
- sanitized public demonstration dataset
- separate `Phase_Flag` helper preserving the conceptual diagnostic boundary
- unit and integration tests
- GitHub Actions across Python 3.11, 3.12, and 3.13
- source-compilation validation
- end-to-end CLI smoke test on sanitized data

## Intentionally not implemented in the public runner

- live NJDOT or SCATS connectivity
- controller commands or automated remediation
- ingestion/join logic for production EVENTS, PHASES, STATISTICS, or SIGNAL GROUPS exports
- site-specific controller mappings or timing-plan configuration
- automatic root-cause diagnosis
- machine-learning anomaly detection
- threshold auto-tuning from live operational data

## Rationale

The public repository is an operator-support and portfolio demonstration. It preserves the supported Green-Time screening methodology while deliberately excluding sensitive production artifacts and avoiding claims that cannot be verified from recovered material.

The next technically meaningful extension would be a fully synthetic multi-export diagnostic adapter with an explicitly invented public schema. That would be an **ENHANCED** portfolio feature, not a recovered production implementation, and is therefore not required for the current repository to be considered complete.
