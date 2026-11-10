# Agent Execution Plan

## Orchestrator
- Parse request and freeze hard constraints.
- Create run manifest and tasks.
- Dispatch independent bounded tasks and preserve separate run IDs.
- Merge only atomic assertions with provenance.
- Invoke deterministic validators and decision engine.
- Publish immutable snapshots.

## Specialist lanes
1. Identity/source discovery: model, brand, SKU, season, source registry.
2. Material/design: composition by garment part, construction facts, design notes.
3. Price/deal: payable price, shipping, discount baseline, offer conditions.
4. Size/stock: brand size chart and exact option-level availability.
5. Independent reviewer: source reopening, adverse evidence, recomputed decision.

## Run separation
Each lane returns its own task_id/run_id. The reviewer uses a new run_id and must not consume only the orchestrator's summary.

## Data handoff
Agents write only their own output artifacts. Shared curated CSV/JSON updates are performed by the orchestrator sequentially after schema validation. Conflicting assertions coexist until resolved; they are never last-write-wins.
