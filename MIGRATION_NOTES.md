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
