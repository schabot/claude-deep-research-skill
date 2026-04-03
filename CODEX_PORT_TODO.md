# Codex Port Implementation To-Do List

Use this checklist as the implementation tracker for the Codex runtime port. Each package is intentionally discrete, has a concrete deliverable, and includes clear acceptance checks so work can be completed and checked off incrementally.

## How to use this checklist
- Check a package only when all deliverables and acceptance checks in that package pass.
- Keep package order unless a dependency is explicitly marked optional.
- If scope changes, update `MIGRATION_PLAN.md` and append rationale to `MIGRATION_NOTES.md`.

---

## Package 0 — Contracts and schemas (foundational)
- [ ] **Define shared runtime contracts in code/config**
  - **Deliverables**
    - `scripts/contracts.py` with mode thresholds, cycle limits, required section specs, citation minima, gate names.
    - `schemas/report_contract.schema.json` for mode + section requirements.
    - `schemas/continuation_state.schema.json` for persisted continuation state.
  - **Acceptance checks**
    - Mode constants include: `quick`, `standard`, `deep`, `ultradeep`.
    - Required sections + minima are represented in one canonical location (no duplicated hardcoded thresholds).
    - Schemas validate representative sample files.

- [ ] **Codify finalization policy**
  - **Deliverables**
    - A contract-level definition of critical vs non-critical gates.
    - Override semantics for `--allow-below-minimum` and `--skip-html`.
  - **Acceptance checks**
    - Finalization logic can be evaluated without running full engine (unit-testable function).

---

## Package 1 — Engine rewrite to executable orchestration
- [ ] **Replace scaffold engine with runnable phase orchestration**
  - **Deliverables**
    - `scripts/research_engine.py` executes phases and writes artifacts, not instruction-only stubs.
    - Artifacts written under `research_output/<slug>-<date>/`.
  - **Acceptance checks**
    - A dry run produces: `run/engine_state.json`, `report.md`, `sources.json`, `run/final_manifest.json` (success or failure).
    - CLI supports: `--query`, `--mode`, `--resume`, `--max-cycles`, `--allow-below-minimum`, `--skip-html`.

- [ ] **Add deterministic state persistence**
  - **Deliverables**
    - `run/engine_state.json` with phase pointer, timestamps, retries/errors.
    - State load/save paths for resume behavior.
  - **Acceptance checks**
    - Resume mode continues from persisted state and does not overwrite completed checkpoints unexpectedly.

---

## Package 2 — Section assembly and continuation loop
- [ ] **Implement section-by-section assembly**
  - **Deliverables**
    - `scripts/assemble_report.py` to generate/evaluate section fragments.
    - `run/sections/*.md` plus deterministic ordered compose into `report.md`.
  - **Acceptance checks**
    - Missing/weak sections are detectable by name and word-count metrics.
    - `report.md` composition order is stable and reproducible.

- [ ] **Implement continuation runner**
  - **Deliverables**
    - `scripts/continuation_runner.py` for cycle-based rewrites of weak sections.
    - `run/continuation_state.json` with cycle index, per-section status, gate status, blockers.
  - **Acceptance checks**
    - Continuation stops on either pass condition or mode-specific cycle limit.
    - Blocking reasons are explicit and persisted.

---

## Package 3 — Unified gate orchestration (block packaging on failure)
- [ ] **Add unified validation gate runner**
  - **Deliverables**
    - `scripts/run_validation_gate.py` to orchestrate:
      1) `validate_report.py`
      2) `verify_citations.py`
      3) optional HTML parity verification
    - Structured gate output at `run/validation_results.json`.
  - **Acceptance checks**
    - Packaging cannot proceed when any critical gate fails.
    - Gate output captures pass/fail + machine-readable failure reasons.

- [ ] **Add JSON outputs to validators**
  - **Deliverables**
    - `validate_report.py --json-out <path>`
    - `verify_citations.py --json-out <path>`
    - `verify_html.py --json-out <path>`
  - **Acceptance checks**
    - JSON outputs are schema-consistent and consumed by gate runner.

---

## Package 4 — Markdown→HTML hardening and parity enforcement
- [ ] **Harden converter for bibliography/section fidelity**
  - **Deliverables**
    - `scripts/md_to_html.py` strict handling for required sections and bibliography parsing.
    - Deterministic metadata behavior for rendered headers/subtitles.
  - **Acceptance checks**
    - Converter fails fast on malformed bibliography or missing required sections.

- [ ] **Enforce markdown↔HTML parity checks**
  - **Deliverables**
    - `scripts/verify_html.py` strict section and citation/bibliography parity mode.
  - **Acceptance checks**
    - Packaging fails when parity fails (unless `--skip-html` is explicitly set).

---

## Package 5 — Test fixtures and regression coverage
- [ ] **Add mode-threshold fixtures**
  - **Deliverables**
    - `tests/fixtures/deep_mode_minimal_pass.md`
    - `tests/fixtures/deep_mode_below_min_fail.md`
  - **Acceptance checks**
    - Fixtures trigger expected gate outcomes deterministically.

- [ ] **Add runtime gate tests**
  - **Deliverables**
    - `tests/test_runtime_gates.py`
  - **Acceptance checks**
    - Tests cover mode minima, section minima, citation minima, cycle limit finalize behavior.

- [ ] **Add HTML parity regression tests**
  - **Deliverables**
    - `tests/test_html_parity.py`
  - **Acceptance checks**
    - Tests catch citation/bibliography count drift and missing section mapping.

---

## Package 6 — Documentation contract alignment
- [ ] **Align reference docs with executable runtime**
  - **Deliverables**
    - Update `reference/report-assembly.md` with contract tables matching `scripts/contracts.py`.
    - Update `reference/continuation.md` with executable state-machine protocol and JSON examples.
  - **Acceptance checks**
    - No provider-coupled orchestration language remains.
    - Docs and code thresholds are consistent.

- [ ] **Record migration decisions and open questions**
  - **Deliverables**
    - Append implementation decisions/tradeoffs/open items to `MIGRATION_NOTES.md` each milestone.
  - **Acceptance checks**
    - Notes reflect any threshold, gating, and continuation policy decisions.

---

## Package 7 — End-to-end smoke and release readiness
- [ ] **Run required smoke checks**
  - **Acceptance checks (must pass)**
    - `python scripts/research_engine.py --help`
    - `python scripts/validate_report.py --help`
    - `python scripts/verify_citations.py --help`
    - `python scripts/md_to_html.py --help`
    - `python scripts/verify_html.py --help`

- [ ] **Run representative end-to-end scenarios**
  - **Deliverables**
    - One `deep` scenario run artifact set.
    - One `ultradeep` scenario run artifact set.
  - **Acceptance checks**
    - `run/final_manifest.json` present and accurately records blocked/pass outcomes.
    - Validation and parity outcomes are reflected in manifest.

---

## Suggested implementation order (checklist sequence)
1. Package 0
2. Package 1
3. Package 2
4. Package 3
5. Package 4
6. Package 5
7. Package 6
8. Package 7

## Deferred (explicitly out of MVP)
- [ ] Advanced multi-provider retrieval adapters beyond baseline normalization.
- [ ] Multiple deliverable output modes (memo/workshop pack/architect brief).
- [ ] Full visual redesign of HTML template beyond parity/stability fixes.
