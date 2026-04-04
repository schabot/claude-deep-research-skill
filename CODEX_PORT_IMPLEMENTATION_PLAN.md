# Codex Port Implementation Plan

> **Architectural correction (2026-04-04):** Sections 1–5 of this document reflect
> a plan based on an incorrect diagnosis. The forensic audit identified
> `execute_phase()` returning `{status: "instructions_displayed"}` as a failure.
> That is not a failure — it is the correct pattern for a Codex skill. The Python
> script is a **tool the LLM calls**, not the executor. The LLM is the orchestrator.
> Rewriting `research_engine.py` to autonomously call LLM APIs and manage a
> continuation loop would create a split-brain system (Python and LLM both trying to
> orchestrate) and strip the LLM of the cross-phase context it needs to produce
> coherent long-form output. **The correct fix is to make the LLM's instructions
> more explicit and demanding — not to replace the LLM with Python.**
>
> The corrected plan is: harden `SKILL.md` with explicit thresholds and protocols
> (Package 1), align reference docs to enforce LLM-driven section discipline
> (Package 2), strengthen validator JSON feedback so the LLM can self-correct
> (Package 3), then harden the HTML tooling (Package 4). `research_engine.py` keeps
> its current role as a prompt scaffolder and state manager. No Python continuation
> runner or autonomous phase executor should be built.
>
> See `MIGRATION_NOTES.md` (2026-04-04) and `CODEX_PORT_TODO.md` for the corrected
> package list.

---

## 1. Executive summary (original — read with correction above)
- The current repo has strong documentation and validators, but the runtime path is still scaffold-heavy: `research_engine.py` does not execute a real multi-pass generation loop that can reliably produce benchmark-scale reports.
- ~~The minimum honest fix is to implement an executable orchestration loop with persisted continuation state, section-by-section assembly, and hard mode gates before packaging.~~ **Corrected:** The minimum honest fix is to surface mode thresholds and section minima explicitly in SKILL.md and tighten the reference docs so the LLM follows a strict section-by-section protocol.
- The first implementation should prioritize ~~deterministic markdown generation~~ **explicit LLM instruction quality** + strict gating + validation/HTML blocking logic, then harden evidence normalization and renderer robustness in iteration 2.
- ~~Documentation-only features (continuation, deep-length behavior, assembly loops) must be converted into code paths and testable artifacts.~~ **Corrected:** These features must be converted into explicit, prescriptive LLM instructions — not Python code paths. The LLM executes them; Python only validates and supports.

## 2. Engineering requirements

### 2.1 Failure-to-requirement translation

| Failure area | Required behavior | Missing mechanism now | Concrete implementation target |
|---|---|---|---|
| Non-generative engine scaffold | Engine must write full report sections from execution phases, not just instructions/state stubs | `research_engine.py` prints instructions and stores tiny state | Replace instruction-only phase runner with executable orchestration that produces `report.md`, `sources.json`, `continuation_state.json`, and section drafts |
| Missing continuation state machine | Deep/ultradeep runs must resume deterministically until gates pass or max cycles reached | No executable continuation loop; only reference docs | Add runtime continuation controller with phase pointer, per-section completion map, cycle counters, and finalize conditions |
| Missing per-section assembly loop | Report must be built section-by-section with explicit completeness checks before finalization | Single-pass packaging expectation; no assembly checkpoints | Add section assembler that iterates required sections, validates each section minimums, rewrites weak sections, and appends to markdown source of truth |
| Missing mode-based length/completeness gates | quick/standard/deep/ultradeep must enforce different minima and continuation behavior | Length and depth targets only in docs | Add mode contract module with hard thresholds and `--allow-below-minimum` override flag |
| Markdown→HTML brittleness | HTML generation must preserve all validated sections and bibliography fidelity | Converter relies on brittle regex assumptions and tolerant fallbacks | Harden markdown parser + strict section parity checks; block HTML generation unless markdown passes validation contract |
| Citation/bibliography fidelity issues | Every in-text citation must map to complete bibliography entry; bibliography must be machine-parseable | Citation parsing/format assumptions are weak; partial entries can pass downstream | Normalize citation ledger, enforce bibliography schema, and run citation gate before rendering/packaging |

### 2.2 Non-negotiable runtime requirements
1. **Executable phases**: scope/plan/retrieve/triangulate/synthesize/critique/refine/package must map to runnable functions with persisted outputs.
2. **Deterministic state**: every continuation cycle must update a single authoritative state file with monotonic cycle number and checkpoints.
3. **Assembly-first truth**: markdown file is built from section artifacts and is the only input to renderer/validators.
4. **Gate-controlled finalize**: packaging blocked unless section, length, and citation/bibliography gates pass.
5. **Observable artifacts**: every run emits run manifest with timestamps, mode, gates, and pass/fail reasons.

## 3. Target runtime architecture

### 3.1 Runtime boundaries and data flow
1. **Research / evidence collection**
   - Input: query + mode
   - Output: normalized source records and evidence objects
   - Files: `run/sources.normalized.json`, `run/evidence_ledger.json`
2. **Synthesis / outline**
   - Input: evidence ledger
   - Output: outline + claim map + unresolved gaps
   - Files: `run/outline.json`, `run/claim_map.json`
3. **Report assembly**
   - Input: outline + claim map
   - Output: section markdown fragments + assembled report markdown
   - Files: `run/sections/*.md`, `report.md`
4. **Packaging / rendering**
   - Input: validated markdown
   - Output: HTML and optional PDF
   - Files: `report.html`, optional `report.pdf`
5. **Verification**
   - Input: report markdown/html + source/evidence artifacts
   - Output: gate results + final manifest
   - Files: `run/validation_results.json`, `run/final_manifest.json`

### 3.2 Entrypoint behavior (proposed)
`python scripts/research_engine.py --query "..." --mode deep [flags]`

Engine behavior:
- initialize run folder (`research_output/<slug>-<date>/`)
- create baseline state files
- execute phase pipeline by mode
- iterate continuation cycles until finalize gates pass or cycle limit reached
- invoke validation gate runner
- invoke renderer only on validator success
- write final manifest and exit non-zero on blocked finalize

### 3.3 Proposed state files
- `run/engine_state.json` — phase pointer, mode, timestamps, errors, retries
- `run/continuation_state.json` — cycle counters, section status, gate status
- `run/evidence_ledger.json` — evidence rows with source ids + claim linkage
- `run/outline.json` — required sections with target word budgets
- `run/validation_results.json` — structured gate outcomes
- `run/final_manifest.json` — artifacts and final pass/fail summary

### 3.4 Continuation state contract
`continuation_state.json` should include:
- `mode`, `cycle_index`, `max_cycles`
- `sections`: `{name, min_words, target_words, status, attempts, citations_count}`
- `global_metrics`: `total_words`, `unique_citations`, `bibliography_entries`
- `gates`: section_gate, mode_length_gate, citation_gate, bibliography_gate, html_gate
- `can_finalize` boolean + blocking reasons list

### 3.5 Validator and packaging boundaries
- `run_validation_gate.py` (new) orchestrates:
  1) `validate_report.py`
  2) `verify_citations.py`
  3) optional HTML parity gate
- packaging is blocked if any **critical** gate fails
- HTML generation runs only after markdown gate success
- HTML verification runs immediately after render and can mark packaging failed if parity breaks

## 4. Minimum Viable Real Port

> **Architectural correction (2026-04-04):** The original "must build now" list
> assumed Python should execute phases and manage continuation. That is wrong. See
> the correction note at the top of this document. The corrected MVP is below.

The smallest set that makes this repo honestly produce benchmark-quality output:

### Must build now (corrected)
1. Surface all mode thresholds and section minima from `scripts/contracts.py` directly into `SKILL.md` as hard requirements visible to the LLM at run start.
2. Add explicit numbered section-by-section assembly protocol to `SKILL.md` and `reference/report-assembly.md`.
3. Rewrite `reference/continuation.md` as a prescriptive, numbered LLM instruction sequence (not pseudocode or narrative).
4. Add `--json-out` to validator scripts so they emit structured, machine-readable feedback the LLM can read and act on.
5. Block HTML generation until markdown + citation validators pass (enforced by updated SKILL.md workflow steps).

### Can remain simplified in MVP
- `research_engine.py` keeps its current role: print structured phase prompts, save state stubs. No autonomous LLM calls needed.
- Retrieval depth can remain a basic source normalization abstraction.
- Critique/refine loops can be single-iteration by default for standard mode.
- HTML style can remain current template so long as section parity and bibliography fidelity are enforced.

### Cannot remain doc-only (corrected framing)
- Mode thresholds must appear in SKILL.md (not just contracts.py) — the LLM must see them.
- Section assembly must be a numbered mandatory protocol the LLM follows, not background guidance.
- Continuation criteria must be explicit and tied to contracts.py thresholds.
- Packaging gating must be enforced by SKILL.md workflow steps, not Python control flow.

## 5. File-by-file plan

### Existing files
- **`scripts/research_engine.py` — replace (major rewrite)**
  - Implement executable phase functions and orchestration loop.
  - Persist/load state artifacts and continuation cycle data.
  - Add `--resume`, `--max-cycles`, `--allow-below-minimum` flags.
- **`scripts/validate_report.py` — modify**
  - Support mode-aware thresholds (from config/schema).
  - Promote current word-count warning into configurable fail gate.
  - Output structured JSON result (`--json-out`) for gate runner.
- **`scripts/md_to_html.py` — modify**
  - Enforce strict bibliography parsing and section mapping.
  - Fail fast on malformed required placeholders/sections.
  - Accept optional metadata manifest for deterministic header fields.
- **`scripts/verify_html.py` — modify**
  - Add strict markdown↔HTML section parity mode.
  - Verify citation counts and bibliography entry parity numerically.
  - Emit JSON output for gate orchestration.
- **`reference/report-assembly.md` — modify**
  - Convert guidance into explicit runtime contract table used by code.
- **`reference/continuation.md` — modify**
  - Replace provider-coupled narrative with executable state-machine protocol and schema examples.
- **`templates/mckinsey_report_template.html` — keep with targeted edits**
  - Preserve styling, but align required anchors/classes with stricter verifier expectations.

### New files (recommended)
- **`scripts/assemble_report.py` (add)**
  - Section-by-section writer and completeness evaluator.
- **`scripts/continuation_runner.py` (add)**
  - Standalone continuation cycle executor; reusable by engine and resume command.
- **`scripts/run_validation_gate.py` (add)**
  - Unified gate runner and packaging blocker.
- **`scripts/contracts.py` (add)**
  - Shared mode thresholds, section specs, and gate constants.
- **`schemas/continuation_state.schema.json` (add)**
  - Validation schema for continuation state.
- **`schemas/report_contract.schema.json` (add)**
  - Required sections and per-mode thresholds schema.
- **`tests/fixtures/deep_mode_minimal_pass.md` (add)**
  - Borderline passing fixture for deep mode.
- **`tests/fixtures/deep_mode_below_min_fail.md` (add)**
  - Expected-fail fixture for gate enforcement.
- **`tests/test_runtime_gates.py` (add)**
  - Unit tests for thresholds and finalize decisions.
- **`tests/test_html_parity.py` (add)**
  - Regression tests for markdown→HTML parity and bibliography integrity.

## 6. Runtime enforcement rules

### 6.1 Mode targets (enforced)
- **quick**: 1,500–3,500 words
- **standard**: 3,500–7,000 words
- **deep**: 7,500–14,000 words
- **ultradeep**: 11,000–22,000 words

Default behavior: fail finalization if below minimum. Override only via `--allow-below-minimum` (manifest records override).

### 6.2 Required sections and minimums
Required H2 sections (must all exist):
1. Executive Summary (>=200 words)
2. Introduction (>=400)
3. Main Analysis (>=2,500 deep / >=4,000 ultradeep)
4. Synthesis & Insights (>=900 deep / >=1,200 ultradeep)
5. Limitations & Caveats (>=250)
6. Recommendations (>=500)
7. Bibliography (machine-parseable entries)
8. Methodology Appendix (>=300)

### 6.3 Citation and bibliography gates
- Unique in-text citations:
  - quick >=8
  - standard >=12
  - deep >=18
  - ultradeep >=24
- Bibliography completeness:
  - Every citation id in body must exist in bibliography.
  - Bibliography numbering contiguous from `[1]..[N]`.
  - Minimum complete entries: 10 for standard, 15 deep, 20 ultradeep.
- Any truncation marker (`etc.`, ranges like `[8-75]`, placeholder phrases) = hard fail.

### 6.4 Continuation/finalization control
- Cycle limits:
  - quick: 1 cycle
  - standard: 2 cycles
  - deep: 4 cycles
  - ultradeep: 6 cycles
- Continue condition:
  - any required section below min words
  - total words below mode minimum
  - citation/bibliography gate failing
- Fail condition:
  - cycle limit reached and critical gates still failing
- Pass condition:
  - all critical gates pass + validator scripts return success

### 6.5 Packaging and HTML rules
- HTML generation allowed **only** when markdown + citation gates pass.
- HTML verification required before final success manifest.
- Packaging blocked if HTML parity gate fails (unless `--skip-html` explicitly set).

## 7. Execution sequence

1. User runs `scripts/research_engine.py` with query + mode.
2. Engine creates run workspace under `research_output/<slug>-<date>/` and writes `run/engine_state.json`.
3. Research phase functions collect/normalize evidence into `run/sources.normalized.json` and `run/evidence_ledger.json`.
4. Synthesis phase writes `run/outline.json` and `run/claim_map.json`.
5. Assembly phase (`assemble_report.py`) drafts section fragments in `run/sections/*.md`.
6. Engine composes `report.md` from ordered section fragments.
7. Gate runner evaluates section minima + mode word minimum + citation/bibliography requirements and updates `run/continuation_state.json`.
8. If gates fail and cycles remain, continuation runner rewrites weak sections and returns to step 5.
9. When markdown gates pass, engine calls `validate_report.py` and `verify_citations.py`; outputs into `run/validation_results.json`.
10. If validators pass, engine calls `md_to_html.py` to generate `report.html`.
11. Engine calls `verify_html.py --html report.html --md report.md` and records results.
12. If all pass, write `run/final_manifest.json` with artifact paths and success=true; otherwise success=false with blockers and non-zero exit.

## 8. Prioritized implementation roadmap

### Top 5 changes by leverage
1. Rewrite `research_engine.py` into executable orchestrator with persistence.
2. Add shared contract constants/schemas for mode + section gates.
3. Add continuation runner + section assembly loop.
4. Add unified validation gate runner that blocks packaging.
5. Harden markdown→HTML parity and bibliography parsing.

### Quick wins (high impact, low complexity)
- Add `--json-out` machine-readable outputs to existing validators.
- Promote word count warning to mode-configurable hard gate.
- Add strict "no packaging on failed validation" branch.

### Structural rewrites (higher effort)
- Split orchestration into modules (`research_engine.py`, `assemble_report.py`, `continuation_runner.py`).
- Introduce contracts/schemas consumed by validators and engine.
- Add regression tests for continuation decisions and HTML parity.

### Dependencies/order
1. Contracts/schemas first (source of truth for thresholds).
2. Engine + continuation + assembly loop next.
3. Validator JSON outputs and gate runner.
4. HTML converter/verifier hardening.
5. Fixtures/tests + documentation updates.

### Iteration plan
- **Iteration 1 (MVP real port):** contracts, engine rewrite, continuation loop, runtime gates, packaging blocker, minimal tests.
- **Iteration 2 (hardening):** citation/evidence ledger strictness, HTML parity robustness, expanded fixtures, better diagnostics.
- **Deferred:** advanced provider adapters, multi-deliverable output modes, richer visual template redesign.

## 9. Risks and tradeoffs
- **Claude parity vs Codex-native behavior:** literal parity may be impossible where upstream relied on implicit runtime continuation behavior; substitute explicit disk-backed continuation protocol.
- **Token/context differences:** Codex runs may need more deterministic multi-cycle assembly; tradeoff is more files and stricter gates, but better reproducibility.
- **Validator strictness transition risk:** raising warnings to hard failures may break existing short artifacts; mitigate with override flag + explicit manifest annotation.
- **HTML template stability:** preserving current style limits churn, but stricter parser assumptions can surface latent markdown formatting inconsistencies.

## 10. Appendix

### 10.1 Pseudocode (engine control loop)
```python
state = load_or_init_state(args)
while state.cycle_index < state.max_cycles:
    run_research_phases(state)
    assemble_sections(state)
    compose_markdown(state)

    gate_result = run_markdown_gates(state)
    save_continuation_state(state, gate_result)

    if gate_result.can_finalize:
        break
    state.cycle_index += 1

if not gate_result.can_finalize and not args.allow_below_minimum:
    fail("critical gates not met")

validate_md()
validate_citations()
if validations_pass:
    render_html()
    verify_html()
finalize_manifest()
```

### 10.2 Suggested CLI flags
- `--resume [run_dir]`
- `--max-cycles N`
- `--allow-below-minimum`
- `--skip-html`
- `--contracts schemas/report_contract.schema.json`
- `--json-logs`

### 10.3 Example continuation state (abridged)
```json
{
  "mode": "deep",
  "cycle_index": 2,
  "max_cycles": 4,
  "sections": [
    {"name": "Executive Summary", "min_words": 200, "actual_words": 238, "status": "pass"},
    {"name": "Main Analysis", "min_words": 2500, "actual_words": 2110, "status": "fail"}
  ],
  "global_metrics": {"total_words": 6920, "unique_citations": 17, "bibliography_entries": 17},
  "gates": {
    "section_gate": false,
    "mode_length_gate": false,
    "citation_gate": false,
    "bibliography_gate": true
  },
  "can_finalize": false,
  "blocking_reasons": [
    "Main Analysis below minimum words",
    "deep mode total words below 7500",
    "deep mode requires >=18 unique citations"
  ]
}
```
