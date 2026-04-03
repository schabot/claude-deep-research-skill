# Repo Port Audit: Claude Deep Research Skill → Codex

## Scope and method

This audit traces **actual execution behavior** of this repository and compares it to the imported benchmark artifact that represents expected high-depth output quality (`benchmarks/claude-agentic-commerce-ctc-20260320/*`).

Notes:
- Direct git clone/curl access to upstream source from this environment returned HTTP 403.
- Upstream files were inspected via browser fetch (raw GitHub endpoint) at a high level; the core engine shape appears materially the same scaffold pattern as this repo's `scripts/research_engine.py`.

## Mechanical findings

### 1) Entrypoint behavior is non-generative (hard fact)

`python scripts/research_engine.py --query "..."` does not perform retrieval, synthesis, or packaging. It only prints instruction text for each phase and writes tiny JSON state stubs.

Evidence in code:
- `execute_phase()` prints prompt text and returns `{status: "instructions_displayed"}`; no model call, no search, no markdown assembly. (`scripts/research_engine.py`, lines 442-459)
- `run_pipeline()` loops through phases and saves state only; it never mutates `state.report`, never writes markdown content. (`scripts/research_engine.py`, lines 461-493)
- Report path is fabricated and returned as a string without file creation. (`scripts/research_engine.py`, lines 485-493)
- On completion it explicitly tells the operator to execute instructions elsewhere. (`scripts/research_engine.py`, lines 580-581)

Observed run artifact:
- State files contain `"report": ""`.

### 2) There is no continuation engine in executable code

Continuation exists only as documentation prose and pseudocode. No script enforces continuation state transitions, section completeness, or recursive resume.

Evidence:
- Continuation mechanics live in `reference/continuation.md` only, including pseudo `delegated_workstream(...)`. (`reference/continuation.md`, lines 72-107)
- `scripts/research_engine.py` has no word-count threshold branch, no continuation state file creation, no recursive execution path.

### 3) Length targets are documentation-only; validators do not enforce mode minima

The repository states strong length targets by mode, but runtime checks do not enforce them.

Evidence:
- Target sizes are declared in docs (`Deep: 8,000-15,000`, `UltraDeep: 15,000-20,000+`). (`reference/report-assembly.md`, lines 5-10)
- Validator word-count check only warns if `<500` words and still passes. (`scripts/validate_report.py`, lines 247-255)
- No check ties report length to selected mode.

### 4) Single-pass packaging prompt invites truncation by design

The package phase instruction is a one-shot markdown skeleton with placeholders like `[Continue for all findings...]`. Without enforced section looping, this naturally collapses to one-pass, medium-length output.

Evidence:
- Package prompt includes static scaffold and continuation placeholder text. (`scripts/research_engine.py`, lines 373-437)
- Progressive section-by-section generation loop is only in docs, not code. (`reference/report-assembly.md`, lines 39-89)

### 5) HTML quality degradation is mainly upstream-thinning + rigid parser contract

The converter is deterministic but narrow. It assumes markdown structure quality and strict bibliography patterns; when upstream report is thin or structurally loose, rendered quality degrades sharply.

Evidence:
- Section/nav extraction only keys off `##` headings. (`scripts/md_to_html.py`, lines 143-150)
- Bibliography parser expects each entry on one line with trailing URL; otherwise it downgrades to plain paragraph block. (`scripts/md_to_html.py`, lines 228-250)
- Metrics dashboard extracts first 4 numeric-like strings only; shallow reports produce weak/empty dashboards. (`scripts/md_to_html.py`, lines 153-193)
- Converter passed benchmark markdown through verifier with warning that HTML retained far fewer citations than markdown (`18` vs `45`), showing markdown→HTML fidelity loss under realistic complex input.

### 6) Benchmark evidence confirms the target quality envelope

The imported benchmark markdown is ~11K words and structurally rich, matching expected deep/ultradeep behavior.

Evidence:
- `benchmarks/.../research_report_20260320_agentic_commerce_ctc.md` word count: 11,024 words.
- Benchmark README explicitly records this as quality reference and warns not to blame renderer alone. (`benchmarks/claude-agentic-commerce-ctc-20260320/README.md`)

## First point of failure (earliest executable fault)

**File:** `scripts/research_engine.py`  
**Function:** `execute_phase()`  
**Failure:** It terminates each phase at instruction display and returns status marker only; no phase work is executed.  
**Why this is first:** This is the earliest point where planned operations should dispatch into retrieval/synthesis/assembly but do not.

## Direct answer to “why ~4K instead of continuing?”

Because there is no executable continuation or section assembly loop. The system has:
1) no per-section append loop,
2) no mode-based minimum-length gate,
3) no continuation state machine tied to runtime,
4) no hard-fail on undersized output.

Therefore any one-pass response that “looks complete enough” ends execution.

## HTML pipeline impact model

### Case A: full report (ideal)
- Rich `##` section map populates nav and sidebar correctly.
- Dense numeric statements produce a populated metrics dashboard.
- Complete bibliography with strict `[N] ... URL` lines renders as styled `.bib-entry` blocks.
- Overall page appears coherent and information-dense.

### Case B: current thin report (~4K)
- Fewer `##` sections -> sparse nav/sidebar and low section count stat.
- Weak quantitative density -> empty/weak metrics dashboard.
- Short or malformed bibliography lines -> fallback paragraphs, reduced reference affordance.
- Less citation markup surviving content conversion -> reduced trust cues.

Net: renderer does not create depth; it exposes lack of depth and can amplify structural weakness.

## Classification

1. **Orchestration failure (primary, critical)**
   - Non-generative engine scaffold, single-pass instructions-only execution.
   - Missing executable continuation logic.

2. **Report contract failure (primary, critical)**
   - No hard enforcement of mode-based length targets.
   - No hard enforcement of section-by-section completion.
   - Validator allows short outputs (warn-only under 500 words).

3. **Rendering failure (secondary, moderate)**
   - Converter assumes strict markdown contracts; partial degradation on real-world complex markdown.
   - Bibliography parsing and citation preservation are brittle.

## Gap vs target architecture

1. Codex-native execution: **partial** (shell UX is codex-style; execution logic still scaffold-only)
2. Enforced multi-pass generation: **not aligned**
3. Section-by-section append-only assembly: **not aligned (docs only)**
4. Hard length/completeness gates: **not aligned**
5. Deterministic markdown→HTML pipeline: **partial** (deterministic but lossy on complex inputs)
6. Research vs assembly separation: **partial** (conceptual only)
7. Template+converter contract integrity: **partial** (works on strict input, degrades otherwise)

## Top 5 high-priority fixes

1. Implement real phase executors (retrieve/triangulate/synthesize/package) in `research_engine.py`.
2. Add append-only section assembly loop with persisted section state.
3. Add hard mode gates (`deep >= 8k`, `ultradeep >= 15k`) with fail/continue behavior.
4. Implement executable continuation state machine (not doc pseudocode).
5. Harden markdown→HTML conversion for bibliography and citation parity, then gate with `verify_html` in CI.

