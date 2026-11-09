# Data Directory Contract

- requests/: immutable request JSON snapshots
- catalog/: product and variant JSON records
- evidence/: source and evidence registries
- offers/: append-only offer and availability observations
- decisions/: immutable decision snapshots
- fixtures/: synthetic and adjudicated test fixtures

CSV files are append-only observation ledgers where practical. Corrected records receive new observation IDs and supersedes references; historical observations are not silently overwritten. Do not commit credentials, personal data, copyrighted page dumps, or unlicensed review text.
