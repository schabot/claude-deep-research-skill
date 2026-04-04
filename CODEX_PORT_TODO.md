# Codex Port Implementation To-Do List

Use this checklist as the implementation tracker for the Codex runtime port. Each package is intentionally discrete, has a concrete deliverable, and includes clear acceptance checks so work can be completed and checked off incrementally.

## How to use this checklist
- Check a package only when all deliverables and acceptance checks in that package pass.
- Keep package order unless a dependency is explicitly marked optional.
- If scope changes, update `MIGRATION_PLAN.md` and append rationale to `MIGRATION_NOTES.md`.

---

## Package 0 — Contracts and schemas (foundational)
- [x] **Define shared runtime contracts in code/config**
  - **Deliverables**
    - `scripts/contracts.py` with mode thresholds, cycle limits, required section specs, citation minima, gate names.
    - `schemas/report_contract.schema.json` for mode + section requirements.
    - `schemas/continuation_state.schema.json` for persisted continuation state.
  - **Acceptance checks**
    - Mode constants include: `quick`, `standard`, `deep`, `ultradeep`.
    - Required sections + minima are represented in one canonical location (no duplicated hardcoded thresholds).
    - Schemas validate representative sample files.

- [x] **Codify finalization policy**
  - **Deliverables**
    - A contract-level definition of critical vs non-critical gates.
    - Override semantics for `--allow-below-minimum` and `--skip-html`.
  - **Acceptance checks**
    - Finalization logic can be evaluated without running full engine (unit-testable function).

---

## Package 1 — SKILL.md contract hardening (highest leverage)

> **Architectural note (2026-04-04):** The original Package 1 proposed rewriting
> `research_engine.py` into an autonomous LLM-calling executor. This was
> architecturally wrong. In a Codex skill, the Python script is a **tool** the LLM
> calls — not the executor. The LLM is the orchestrator. Making Python autonomous
> would create a split-brain system where two orchestrators compete for the same
> workflow. The correct fix is to make the LLM's operating instructions explicit and
> demanding enough that Codex produces quality output on its own. See
> `MIGRATION_NOTES.md` (2026-04-04) for the full diagnosis.

- [ ] **Surface mode thresholds and section minima directly in SKILL.md**
  - **Deliverables**
    - `SKILL.md` updated with explicit word targets per mode (quick: 1,500–3,500; standard: 3,500–7,000; deep: 7,500–14,000; ultradeep: 11,000–22,000).
    - Section minima (from `scripts/contracts.py`) visible in SKILL.md as a required quality table.
    - Citation minima per mode stated explicitly.
  - **Acceptance checks**
    - `SKILL.md` contains no soft-preference language ("preferred", "recommended") for quality thresholds — all are stated as hard requirements.
    - Thresholds in `SKILL.md` match `scripts/contracts.py` exactly.

- [ ] **Add mandatory section-by-section assembly protocol to SKILL.md**
  - **Deliverables**
    - Numbered section-drafting protocol in SKILL.md: draft → self-check word count → expand or proceed.
    - Explicit instruction that continuation is mandatory (not optional) for deep/ultradeep when any section or total word count falls below minimum.
  - **Acceptance checks**
    - Protocol is a numbered step sequence, not prose guidance.
    - Deep/ultradeep continuation trigger criteria match `scripts/contracts.py` cycle limits.

---

## Package 2 — Reference doc alignment (LLM-driven discipline)

> **Architectural note (2026-04-04):** The original Package 2 proposed a Python
> `continuation_runner.py` that would make continuation decisions programmatically.
> This was wrong. Continuation decisions require reading and judging content — that
> is the LLM's role. The correct deliverable is a prescriptive reference doc the LLM
> follows, not a Python loop that wraps LLM calls.

- [ ] **Rewrite `reference/continuation.md` as prescriptive LLM instruction protocol**
  - **Deliverables**
    - `reference/continuation.md` rewritten as a numbered, plaintext instruction set the LLM follows step-by-step.
    - Continuation trigger conditions and exit conditions stated explicitly, matching `scripts/contracts.py` thresholds.
    - No provider-coupled pseudocode or ambiguous narrative prose.
  - **Acceptance checks**
    - Document reads as a standalone instruction sequence (no external context required to follow it).
    - All numeric thresholds match `scripts/contracts.py` exactly.

- [ ] **Align `reference/report-assembly.md` with contracts.py section minima**
  - **Deliverables**
    - Section-by-section assembly stated as a mandatory numbered protocol, not guidance.
    - Per-section word targets by mode derived from `scripts/contracts.py`.
  - **Acceptance checks**
    - Section minima in `reference/report-assembly.md` match `scripts/contracts.py` exactly.
    - No remaining language that allows single-pass packaging without section-level completeness checks.

- [ ] **Add section compositor script (optional, non-generative)**
  - **Deliverables**
    - `scripts/assemble_report.py` as a pure file compositor: reads LLM-written `run/sections/*.md` fragments and composes ordered `report.md`. Does not generate content.
  - **Acceptance checks**
    - Script only reads and concatenates; no LLM calls, no content generation.
    - Composition order is stable and deterministic.

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
1. Package 0 ✓ (complete)
2. Package 1 — SKILL.md contract hardening (highest leverage; fixes the root cause)
3. Package 2 — Reference doc alignment (LLM-driven continuation discipline)
4. Package 3 — Validator JSON outputs and unified gate runner (actionable LLM feedback)
5. Package 4 — HTML hardening (tooling quality)
6. Package 5 — Test fixtures and regression coverage
7. Package 6 — Documentation contract alignment
8. Package 7 — End-to-end smoke and release readiness

## Deferred (explicitly out of MVP)
- [ ] Advanced multi-provider retrieval adapters beyond baseline normalization.
- [ ] Multiple deliverable output modes (memo/workshop pack/architect brief).
- [ ] Full visual redesign of HTML template beyond parity/stability fixes.
