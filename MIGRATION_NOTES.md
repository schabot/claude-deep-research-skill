# MIGRATION_NOTES

## 2026-04-03 - Plan comparison against external audit/spec

### Summary

The repository already contains a meaningful Codex-native migration effort. Compared with the original skill instance audited outside this repo, this repo is in a stronger state:

- `SKILL.md` is already Codex-oriented.
- `MIGRATION_PLAN.md` correctly identifies provider-specific wording, pathing, continuation examples, and documentation drift as key migration concerns.
- The repo already includes `sources.json` expectations, critique-loop concepts, and structured-evidence language.

However, the migration plan is still narrower than the broader improvement spec created during the audit. The current repo plan focuses mostly on **provider migration and documentation/runtime neutrality**. The external spec adds a second layer: **upgrading the research workflow itself into a more enforceable evidence-driven operating procedure**.

### Where the existing plan is already strong

1. **Migration framing is correct**
   - The repo plan correctly treats this as a Claude-to-Codex port with minimal unnecessary churn.
   - It explicitly calls out provider-specific paths, orchestration examples, and output assumptions.

2. **Preservation bias is appropriate**
   - The existing plan sensibly preserves scripts, templates, and methodology where practical.
   - This is the right stance for an initial migration.

3. **Codex-native shell-first orientation is already present**
   - `SKILL.md` now defines explicit artifact paths relative to the current working directory.
   - Validation calls are spelled out concretely.

4. **There is already some evidence-discipline groundwork**
   - `sources.json` is now part of the workflow.
   - Report structure and critique language are more developed than the original audited copy.

### Gaps relative to the improvement spec

The repo plan does **not yet fully cover** the following higher-value workflow upgrades:

1. **Environment detection as an explicit step**
   - The current migration plan removes Claude-specific assumptions.
   - It does not yet define a formal capability-detection step that branches behavior depending on available search, validation, network, and delegation support.

2. **Mandatory workstream decomposition**
   - The methodology talks about parallel retrieval.
   - It does not yet require named workstreams with ownership, source intent, and merge rules in deep/ultradeep mode.

3. **Evidence ledger as a first-class artifact**
   - `sources.json` exists, but the broader spec requires a stricter claim/evidence schema and direct traceability from report claims to evidence objects.

4. **Contradiction register before synthesis**
   - Contradictions are mentioned conceptually.
   - They are not yet enforced as a required intermediate artifact with disposition and impact on recommendations.

5. **Layered quality gates**
   - Current validation remains mostly structural.
   - The broader spec separates validation into:
     - structural quality
     - evidence trace quality
     - decision-quality / usability

6. **Offline-aware citation verification**
   - The current verifier still relies heavily on live URL/DOI resolution.
   - It should explicitly degrade to structural-only verification when network access is unavailable.

7. **Modular output modes**
   - Current outputs are still centered on a long-form report.
   - The broader spec adds multiple deliverable types: executive memo, workshop pack, strategy outline, architect brief.

8. **Mandatory critique artifact**
   - The methodology includes critique/refine concepts.
   - The broader spec requires a concrete critique artifact and blocks finalization in deep/ultradeep without it.

### Recommended interpretation

The current repo plan should be treated as **Phase 1: provider migration**.

The external improvement spec should be treated as **Phase 2: workflow hardening and quality-system upgrade**.

That sequencing is sensible:

1. First make the repo cleanly Codex-native and provider-neutral.
2. Then strengthen the underlying research system itself.

### Recommended next workstreams

#### Workstream A - Workflow contract hardening

Update:
- `SKILL.md`
- `reference/methodology.md`
- `reference/quality-gates.md`

Goals:
- add explicit environment adaptation
- require workstream decomposition in deep/ultradeep
- require evidence ledger before synthesis
- require critique artifact before finalization

#### Workstream B - Validator redesign

Update:
- `scripts/validate_report.py`
- `scripts/verify_citations.py`

Add:
- `scripts/check_evidence_trace.py`

Goals:
- reduce heading-name brittleness
- distinguish structural failures from substantive evidence failures
- support offline citation verification mode
- verify recommendation-to-evidence traceability

#### Workstream C - Artifact model expansion

Update:
- `templates/report_template.md`
- possibly add new templates

Goals:
- support multiple output modes
- add explicit uncertainty/contradiction placeholders
- support evidence-ledger-aware assembly

### Proposed implementation order

1. Finish migration cleanup and remove remaining provider-specific runtime language.
2. Add environment detection and evidence-ledger requirements to docs.
3. Redesign validators and add evidence-trace checking.
4. Expand templates/output modes.
5. Re-test end-to-end with one deep and one ultradeep scenario.

### Decision

No change to `MIGRATION_PLAN.md` yet. The current plan remains valid, but it should be understood as incomplete if the goal is not just migration, but also meaningful research-quality improvement.

## 2026-04-03 - Port divergence audit focused on report depth + HTML quality

### Context
Performed a targeted audit against the upstream repository to explain two failures observed in this port:
1) materially shorter reports in deep/ultradeep runs;
2) materially weaker rendered HTML quality.

### Key decisions/tradeoffs captured
- Treat this as an **orchestration-contract issue first**, not a styling-only issue.
- Preserve the existing converter/template path for now, but prioritize report-structure enforcement before visual tuning.
- Use a Codex-native redesign for continuation/runtime gates rather than literal Claude-runtime emulation.

### Open items requiring human decision
1. Should deep/ultradeep length gates be hard-fail defaults, or soft warnings with override flags?
2. Should this repo re-align to upstream template/converter contract, or intentionally maintain a forked HTML schema?
3. Should continuation be fully automated in `research_engine.py`, or split into a separate executable runner?

### Deferred implementation work
- Add deterministic continuation state machine with append-only section completion.
- Add per-section minimum enforcement and total-length target enforcement by mode.
- Add compatibility tests for markdown→HTML placeholders, bibliography parsing, and section parity.

## 2026-04-03 - Forensic execution audit (short-output + HTML degradation)

### Summary of verified execution reality
- `scripts/research_engine.py` is an instruction-printing scaffold; it does not execute retrieval/synthesis or write markdown report content.
- Continuation protocol is documentation-only (`reference/continuation.md`), not executable orchestration.
- Mode length targets are documentation-only (`reference/report-assembly.md`) and not enforced by validators (`scripts/validate_report.py` warns only when report is <500 words).
- HTML quality degradation is largely upstream-thinning, with additional converter brittleness around bibliography/citation parsing (`scripts/md_to_html.py`).

### Decisions/tradeoffs recorded
- Prioritize orchestration and contract enforcement ahead of visual styling changes.
- Treat HTML renderer quality issues as secondary until markdown depth and structure are enforced.
- Preserve current template while hardening converter behavior and parity checks.

### Open items requiring human decision
1. Whether mode length gates should hard-fail by default or allow explicit override flags.
2. Whether continuation should be built into `research_engine.py` or as a dedicated continuation runner script.
3. Whether to preserve the current HTML template style or converge to benchmark-style custom components.

## 2026-04-03 - Concrete implementation plan for executable Codex runtime

### Summary
Converted forensic diagnosis into an execution-ready implementation plan (`CODEX_PORT_IMPLEMENTATION_PLAN.md`) with explicit architecture, gating, continuation-state contract, execution order, and iteration sequencing.

### Decisions/tradeoffs recorded
- Prioritize an MVP "real runtime" (executable orchestration + continuation + gates) before advanced retrieval adapters.
- Keep existing HTML template styling with targeted compatibility changes; focus first on markdown depth and section/citation parity.
- Introduce hard mode gates by default with explicit override flag (`--allow-below-minimum`) to preserve operator control while preventing silent under-delivery.

### Open items requiring human decision
1. Confirm final per-mode minimum thresholds (especially deep vs ultradeep lower bounds).
2. Confirm whether HTML parity failures should always block packaging or be overridable in CI-only contexts.
3. Confirm whether continuation execution remains integrated in `research_engine.py` or delegated by default to a dedicated runner script.

## 2026-04-03 - Converted implementation plan into executable package checklist

### Summary
Reworked `CODEX_PORT_IMPLEMENTATION_PLAN.md` from narrative architecture text into a check-off to-do tracker composed of discrete implementation packages with deliverables and acceptance checks.

### Decisions/tradeoffs recorded
- Preserved the original implementation intent, but changed format to execution-tracking first.
- Kept package boundaries aligned to the previously prioritized roadmap (contracts → engine → continuation → gates → HTML parity → tests → docs → E2E smoke).
- Added explicit acceptance criteria per package so completion can be verified without subjective interpretation.

### Open items requiring human decision
1. Confirm whether package completion should be tracked in-place on the checklist file or mirrored into a project board.
2. Confirm whether deferred items should be promoted into MVP scope for this repo iteration.

## 2026-04-03 - Restored implementation plan and split checklist into separate file

### Summary
Addressed review feedback by restoring `CODEX_PORT_IMPLEMENTATION_PLAN.md` to its original narrative/reference form and moving the actionable checkbox tracker into a separate file: `CODEX_PORT_TODO.md`.

### Decisions/tradeoffs recorded
- Kept the long-form implementation plan intact to preserve architecture rationale and sequencing context.
- Retained the checklist format as an execution aid, but decoupled it from the reference plan to reduce document churn and preserve auditability.

### Open items requiring human decision
1. Confirm canonical filename preference for the execution checklist (`CODEX_PORT_TODO.md` vs `IMPLEMENTATION_TODO.md`).
2. Confirm whether completion tracking should occur only in-repo or be mirrored in external project tooling.

## 2026-04-04 - Architectural correction: execution model misdiagnosis

### Summary

The forensic audit (`FORENSIC_AUDIT_2026-04-03.md`) and subsequent implementation
plan (`CODEX_PORT_IMPLEMENTATION_PLAN.md`) were based on a fundamental
misunderstanding of how Codex skills execute. The entire Package 1 and Package 2
scope was built on a wrong premise and has been corrected.

### The misdiagnosis

The forensic audit identified `execute_phase()` returning
`{status: "instructions_displayed"}` as the **first point of failure**, concluding
that the engine "does not execute retrieval/synthesis or write markdown." It proposed
rewriting `research_engine.py` into an autonomous executor that calls LLM APIs,
manages a continuation state machine, and assembles sections programmatically.

This is wrong.

### Why it is wrong

In a Codex (or Claude Code) skill, the Python script is a **tool the LLM calls**.
The LLM is the orchestrator. `execute_phase()` printing phase instructions IS the
correct pattern: the script structures the prompts, the LLM reads them and does the
work using its native tools (web search, file writes, bash).

Making Python autonomous would:
1. Create a split-brain system — Python and the LLM both trying to orchestrate the
   same workflow with no clean authority boundary
2. Strip the LLM of cross-phase context it needs for coherent long-form output
3. Re-introduce provider coupling (Python calling LLM APIs directly)
4. Rebuild an agent framework that Codex already provides

### The real cause of the quality gap

The actual reason Codex produces ~4K words instead of 11K+ is that `SKILL.md` does
not give Codex explicit, hard requirements:
- Word targets for deep/ultradeep are in `scripts/contracts.py` — a file Codex does
  not read unless it explicitly fetches it
- Section minima live in Python code, not in the instructions Codex sees at run start
- Continuation is in `reference/continuation.md`, loaded lazily, with no hard signal
  that it is mandatory for deep/ultradeep runs
- Quality standards use soft preference language ("preferred", "recommended")
  instead of hard requirements

### Why Codex made the wrong diagnosis

The forensic audit was performed by a Codex session asked to find why output was
short. Several factors compounded into the wrong conclusion:

1. **Reasoned from code, not from architecture.** The script shows a function that
   doesn't produce output — from a conventional software perspective, that is a bug.
   The auditor didn't have access to the meta-level context that the LLM is the
   executor, not the script.

2. **Did not recognize its own execution model.** The LLM analyzed a skill designed
   to run inside an LLM agent without recognizing itself as the executor. It
   examined the code as if it were an external system, reaching the conclusion that
   "the engine doesn't run" — which is literally true of the Python, but misses that
   the engine IS the LLM.

3. **The comment was too subtle.** The code comment "In real usage, the agent
   executes these instructions" is easy to dismiss. The skill architecture was not
   explicitly documented anywhere in the repo, so the auditor had no authoritative
   source to consult.

4. **The prompt framed it as a code audit.** "Why does the engine produce short
   output?" naturally leads to "because the engine doesn't execute." The question
   didn't ask "is the skill execution pattern correct?" so the auditor didn't question
   it.

5. **The diagnosis fit the evidence.** State files with `"report": ""`, fabricated
   file paths, no real content written — these are real observations that look like
   failure symptoms. The causal inference was wrong, but the observations were
   accurate.

6. **Confirmation bias from the audit framing.** The forensic audit was specifically
   tasked with finding failure points. Finding "the executor doesn't execute" is a
   compelling answer. The auditor stopped there rather than asking whether a
   non-executing Python script might be intentional.

### Decisions recorded

- `research_engine.py` retains its current role as a prompt scaffolding helper and
  state manager. No autonomous LLM calls, no phase execution logic.
- Continuation and section assembly are enforced through LLM instruction quality
  (SKILL.md + reference docs), not Python control flow.
- `scripts/contracts.py` thresholds must be surfaced in `SKILL.md` directly so the
  LLM sees them at run start without requiring a fetch.
- `scripts/assemble_report.py` may be added as a pure file compositor (reads
  LLM-written section fragments, assembles report.md) — no content generation.
- No `continuation_runner.py` should be built.

### Updated package plan

See `CODEX_PORT_TODO.md` for the revised package list. The corrected order is:
1. Package 0 ✓
2. Package 1: SKILL.md contract hardening
3. Package 2: Reference doc alignment (LLM-driven discipline)
4. Package 3: Validator JSON outputs and gate runner
5. Package 4: HTML hardening
6. Package 5–7: Tests, docs, smoke

---

## 2026-04-03 - Package 0 implementation (contracts + finalization policy)

### What was implemented
- Added `scripts/contracts.py` as the canonical runtime contract module for modes, cycle limits, required section minima, citation minima, gate names, and override sets.
- Added `FinalizationPolicyInput`, `FinalizationPolicyDecision`, and `evaluate_finalization_policy(...)` so finalize decisions can be computed independently of full engine execution.
- Added `schemas/report_contract.schema.json` for mode/section/gate contract validation.
- Added `schemas/continuation_state.schema.json` for persisted continuation-state validation.
- Updated `CODEX_PORT_TODO.md` to mark both Package 0 tasks complete.

### Decisions and tradeoffs
- Kept contract values in Python for immediate runtime consumption and mirrored constraints in JSON Schema for machine-validation/tooling compatibility.
- Mode-aware section minima are centralized under one canonical structure (`REQUIRED_SECTIONS`) to avoid duplicated thresholds across scripts.
- Override semantics are explicit and narrow:
  - `--allow-below-minimum` can only ignore section-minimum and mode-length failures.
  - `--skip-html` can only ignore HTML parity gate failures.

### Open items
- Wire `scripts/research_engine.py` and forthcoming gate runners to consume `scripts/contracts.py` directly (Package 1+).
- Add automated schema-validation tests against representative sample artifacts (Package 5).

