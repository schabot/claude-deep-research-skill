# Repo Port Audit: Claude Deep Research Skill → Codex

Date: 2026-04-03
Audited repo: `/workspace/claude-deep-research-skill`
External reference: `https://github.com/199-biotechnologies/claude-deep-research-skill`

## 1) Executive diagnosis

Primary diagnosis:
- The strongest drift is **runtime/orchestration drift**, not just prose prompt drift. This repo's executable entrypoint (`scripts/research_engine.py`) is primarily an instruction scaffold; it does not execute retrieval loops, section assembly loops, continuation thresholds, or validator-driven rewrite loops. That makes under-length outputs likely whenever users rely on engine defaults.
- HTML quality degradation is likely a **structure + pipeline contract problem** before styling: if markdown is shorter/thinner or missing expected sections/metrics/callouts, the template cannot produce a high-density executive-report result.
- The local converter/template pair has grown and changed significantly; this may be an improvement in some contexts, but it is now a different contract than the original and increases risk of mismatch with upstream report-shape assumptions.

## 2) Original repo: critical mechanisms (verified/partially verified)

Verified from externally accessible snapshots:
- Original skill contract expects deep mode and ultradeep mode to produce substantially longer, section-complete artifacts with continuation for long runs (>18K words).
- Original report assembly guidance is explicit about per-section generation and append-only file growth to avoid single-call output limits.
- Original contract includes deterministic artifacts: markdown + HTML + PDF + bibliography discipline.

Partially verified due network constraints:
- Upstream repo metadata indicates larger files for key mechanics than some local docs imply (e.g., scripts/template line counts in external snapshots differ from local versions).
- Could not fully diff every upstream script line-by-line in shell because direct GitHub clone/raw fetch was blocked in this environment.

## 3) Current repo vs original: divergence analysis

### A. Orchestration / execution contract

What is preserved:
- Documentation still describes the 8-phase methodology and rich retrieval/triangulation process.
- Documentation preserves progressive section assembly and continuation concepts.

Material drift:
- `scripts/research_engine.py` is a scaffold that prints phase instructions and stores state objects, but it does not implement real web retrieval execution, quality-gate retries, section append loops, or continuation handoff runtime.
- Default output path in engine is `./research_output`, not the topic/date folder contract emphasized elsewhere.
- The state object supports serialization, but no concrete code path enforces report-length targets or section-level minimums before finalization.

Impact:
- Users running the engine as if it were a full orchestration runtime can finish with under-developed outputs.

### B. Report assembly & continuation

What is preserved:
- Reference docs still require section-by-section progressive generation, source persistence (`sources.json`), and bibliography completeness.
- Continuation guidance still exists with state-file shape and quality targets.

Material drift:
- Continuation exists mostly as instruction text; local executable plumbing does not appear to instantiate continuation state transitions automatically.
- There is no explicit hard guard in engine code that blocks completion below deep/ultradeep word targets.
- Current template and validator expectations imply a full section structure, but operational enforcement is document-level, not runtime-level.

Impact:
- Early stop after one pass becomes common, producing ~4K outcomes instead of multi-pass 8K–20K outcomes.

### C. HTML rendering pipeline

What is preserved:
- `scripts/md_to_html.py` still uses deterministic placeholder replacement into `templates/mckinsey_report_template.html`.
- `scripts/verify_html.py` checks section parity, placeholder replacement, citation presence, and structure.

Material drift / risk points:
- Local converter has expanded considerably and now expects/injects additional placeholders (`{{SUBTITLE}}`, `{{MODE_LABEL}}`, `{{HEADER_TAG}}`, `{{SECTION_COUNT}}`, nav/sidebar links). This is a stronger but different contract.
- Local template style contradicts local reference doc in places (reference says no gradients/no rounded aesthetics, while template uses gradients and rounded corner treatments).
- Bibliography parsing is regex-shaped; malformed bibliography lines degrade into paragraph output and can weaken final visual hierarchy.

Impact:
- If markdown input is thin, converter outputs sparse metrics/dashboard/nav; template appears low quality even when technically valid HTML.

### D. Prompt/runtime adaptation quality

Preserved:
- Provider-neutral wording appears across many docs.

Drift or redesign gap:
- The repo partially removed Claude-specific language but did not fully replace Claude runtime affordances (Task delegation, long-context continuation behavior) with concrete Codex-native equivalents in executable orchestration.
- Result: docs promise capabilities that runtime scaffold does not enforce.

## 4) Root causes of short report output (ranked)

1. **Orchestration is instructional, not enforced runtime behavior**
   - Engine does not automatically execute retrieval depth, section loops, continuation thresholds, or rewrite loops.
2. **No hard completion gate tied to length targets**
   - No runtime fail/continue decision when deep/ultradeep output is below target range.
3. **Continuation is mostly documentary**
   - State schema exists in docs; automated chaining logic is not evident in engine flow.
4. **Section assembly is not guaranteed append-only in runtime path**
   - Docs specify append loops; scaffold flow can terminate without full assembly.
5. **Contract drift encourages summary-style completion**
   - Codex-native wording cleanup happened, but execution contract still under-specified for guaranteed long-form artifact completion.

## 5) Root causes of weak HTML output (ranked)

1. **Thin markdown in → weak HTML out**
   - Template cannot compensate for underdeveloped section content.
2. **Template/converter contract divergence from original assumptions**
   - Additional placeholders + expanded layout logic increase fragility when report shape varies.
3. **Reference/style inconsistency inside this repo**
   - `reference/html-generation.md` aesthetic principles and actual template CSS diverge.
4. **Bibliography/callout parsing sensitivity**
   - Slight markdown shape drift reduces semantic rendering quality.
5. **Potential bypass behavior in user workflows**
   - If users generate ad hoc HTML directly (outside `md_to_html.py`), quality and consistency drop immediately.

## 6) Gap analysis vs recommended architecture

### Recommendation 1: Don’t treat Codex as drop-in Claude runtime
- Status: **Partially aligned**
- Severity: **High**
- Evidence: docs neutralized; executable orchestration still lacks concrete Codex-native replacements for Claude-style delegation/continuation behavior.
- Change: implement explicit Codex runtime contract with deterministic local batching and stateful continuation.

### Recommendation 2: Preserve original artifact mechanics
- Status: **Partially aligned**
- Severity: **High**
- Evidence: docs preserve mechanics; runtime enforcement is weak.
- Change: enforce section checkpoints, citation state writes, continuation thresholds, validator loop blocking.

### Recommendation 3: Separate research from report assembly
- Status: **Partially aligned**
- Severity: **Medium-High**
- Evidence: conceptual separation exists; engine workflow does not enforce artifact boundaries strongly.
- Change: explicit phase artifacts (`retrieval.json`, `triangulation.json`, `outline.json`, then report assembly pass).

### Recommendation 4: Enforce section-level and total-length targets
- Status: **Not aligned (runtime)**
- Severity: **High**
- Evidence: targets in docs; no hard runtime gate.
- Change: add per-section minima + total range checks with mandatory continuation.

### Recommendation 5: Use original HTML pipeline unless justified
- Status: **Partially aligned**
- Severity: **Medium**
- Evidence: still template+converter; however local pipeline has diverged materially in structure and style.
- Change: either realign with upstream contract or document intentional fork + add compatibility tests.

### Recommendation 6: Fix structure before styling
- Status: **Not aligned operationally**
- Severity: **High**
- Evidence: short markdown remains primary issue; style tuning cannot recover missing depth.
- Change: enforce report contract upstream of HTML generation.

### Recommendation 7: Redesign Claude-specific prompting for Codex
- Status: **Partially aligned**
- Severity: **Medium-High**
- Evidence: wording is more neutral; execution still relies on assumed runtime behaviors not guaranteed in Codex.
- Change: remove ceremony/status text overhead; replace with actionable per-section write loops and explicit completion checks.

## 7) Top 5 high-priority fixes

1. Add hard runtime completion gates in `research_engine.py` for section minima and total-length per mode.
2. Implement explicit continuation runner that reads/writes continuation state and auto-resumes until contract met.
3. Split artifacts by phase and make report assembly a distinct deterministic pass.
4. Add regression fixture(s): deep-mode markdown expected word range + required-section checks + bibliography completeness.
5. Reconcile HTML contract: either strict upstream-compatible template/converter pair, or a documented fork with schema tests for placeholders and section mappings.

## 8) Quick wins vs structural rewrites

Quick wins:
- Add a post-generation gate: fail if deep <8K or ultradeep <15K unless user explicitly overrides.
- Add `--enforce-length` and `--min-section-words` flags.
- Add converter smoke test fixture covering callouts, tables, bibliography split.
- Align `reference/html-generation.md` style claims with actual template CSS.

Structural rewrites:
- True continuation pipeline with resume token/state and append-only assembly.
- Research/evidence ledger pipeline with explicit claim→evidence mapping files.
- Codex-native orchestration that emulates delegated workstreams deterministically when parallel agents are absent.

## 9) Suggested next-step implementation plan

Iteration 1 (stability):
1. Introduce length/section gating and fail-fast messages.
2. Add explicit `sources.json` + `assembly_state.json` write checkpoints.
3. Add one deep-mode end-to-end fixture and validator CI step.

Iteration 2 (continuation):
4. Implement continuation state machine (`pending_sections`, `next_citation`, `remaining_targets`).
5. Auto-resume until target met or max cycles reached.

Iteration 3 (HTML hardening):
6. Define markdown-to-html contract schema and tests.
7. Resolve template/style drift vs docs.
8. Add visual regression snapshots for a canonical fixture report.

## 10) Verification notes and constraints

External verification constraints:
- Direct shell `git clone` and raw `curl` to GitHub were blocked (403 CONNECT tunnel).
- Partial upstream visibility came via web snapshots, including:
  - skills listing page with output/continuation contract statements
  - at least one upstream raw reference file (`reference/methodology.md`) via web tool redirect
  - upstream file metadata views indicating differing sizes for key files

Confidence summary:
- **High confidence** on local drift diagnostics and runtime enforcement gaps.
- **Medium confidence** on exact line-level upstream script/template diffs due restricted direct fetch.
