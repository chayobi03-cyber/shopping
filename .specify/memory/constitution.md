# Shopping Intelligence Constitution

Version: 1.0.0

1. User hard constraints are immutable unless explicitly changed by the user.
2. Product identity must be established before product data is combined.
3. Decision-critical claims must have source and evidence provenance.
4. UNKNOWN, CONFLICT, STALE, and DATA_NOT_READY remain explicit states.
5. Source reliability is distinct from field-level data quality.
6. Price and option availability are time-bound observations with timestamps and TTLs.
7. Deterministic code owns hard gates; agents may not override them.
8. Automatic approval applies only to artifacts that pass CI and independent review.
9. BUY means recommendation eligibility, never purchase execution permission.
10. Preserve decision snapshots, data lineage, and Git history.
11. Respect source terms, privacy, copyright, rate limits, and access controls.
12. Prefer the simplest architecture that satisfies verified operating needs.
