# CODEX_PARITY_PLAN

## Objective

Bring the Codex port of the deep-research skill to a quality level that is competitive with the original Claude workflow for **deep** and **ultradeep** research reports.

This plan does **not** assume the prompts are identical. It assumes the benchmark output reveals a higher-quality effective process. The goal is to reconstruct that process as closely as possible inside the Codex environment.

---

## 1. What Claude Appears To Be Doing Better

Based on the benchmark report and HTML artifact, the original Claude workflow appears to do more than follow a linear prompt. It likely executes a richer end-to-end research and packaging process with stronger report shaping.

### A. Better artifact ambition

Claude appears to target a **client-ready deliverable**, not just a research summary.

Observed benchmark characteristics:
- explicit audience framing
- strong title and positioning
- section architecture designed for decision-making
- roadmap, vendor map, risk framing, recommendations by audience
- client-specific narrative woven throughout

Inference:
- the system is optimizing for a consulting playbook, not just completeness

### B. Stronger progressive assembly discipline

The benchmark report appears to have been built section by section with deliberate structure, rather than generated as a single flowing answer.

Observed benchmark characteristics:
- highly structured section sequence
- consistent internal cadence
- deliberate expansion into subsections and sub-subsections
- strong consistency of tone and section density

Inference:
- Claude likely follows the progressive assembly protocol more faithfully
- each section likely gets its own localized drafting pass

### C. Better context carry-forward

The benchmark maintains stronger thread continuity across:
- market context
- CTC-specific implications
- technical architecture
- use-case prioritization
- roadmap and vendor choices

Inference:
- the workflow likely maintains a stronger persistent outline and section-level intent state
- continuation and synthesis are probably more tightly integrated than in the Codex run

### D. Better report-to-HTML coupling

The benchmark HTML is not a generic markdown conversion. It is a purpose-built rendered deliverable.

Observed benchmark characteristics:
- branded hero
- metric strip
- nav
- sticky sidebar
- structured cards
- roadmap visuals
- architecture visuals
- recommendation blocks
- visual hierarchy matched to report semantics

Inference:
- Claude’s effective process either:
  1. renders into a rich template directly, or
  2. produces markdown deliberately shaped for a richer renderer

### E. Better client-specific synthesis

The benchmark is much more deeply adapted to CTC.

Observed benchmark characteristics:
- CTC-specific asset framing
- CTC-specific competitive context
- explicit CTC use cases
- implementation sequencing tied to CTC

Inference:
- Claude likely spends more effort in synthesis and contextual adaptation before packaging

---

## 2. Why Codex Underperformed

The Codex port underperformed for two different classes of reasons:

### A. Process fidelity gap

The Codex execution did not reproduce the likely effective Claude process:
- less ambitious report structure
- weaker progressive assembly
- weaker synthesis density
- weaker client adaptation
- weaker packaging rigor

### B. Tooling and rendering gap

The Codex repo currently lacks equivalent output machinery:
- weak HTML renderer
- no semantic component mapping
- no dashboard/nav/sidebar generation
- no strong packaging orchestration
- limited evidence-trace enforcement

So even perfect markdown would still underperform visually.

---

## 3. Reconstructed “Claude-Like” Effective Process

This is the best inference of the process Claude appears to be executing in successful ultra-deep runs.

### Phase 0: Deliverable framing

Before retrieval, determine:
- exact audience
- artifact type
- report stance
- expected decisions enabled by the report

Required outputs:
- title
- subtitle
- report thesis
- target artifact type
- required section architecture

### Phase 1: Research decomposition

Split work into explicit streams:
- market and definitions
- architecture
- retailer/client context
- use cases
- vendors / ecosystem / protocols
- implementation and recommendations

Required outputs:
- workstream list
- coverage map
- retrieval targets per stream

### Phase 2: Evidence capture

Collect evidence into structured objects, not just loose notes.

Required outputs:
- evidence ledger
- source classification
- claim/source mapping

### Phase 3: Synthesis framing

Before drafting prose, determine:
- central thesis
- key argument structure
- section-level takeaways
- where client context must appear

Required outputs:
- report outline with subsection intent
- claim hierarchy
- strongest evidence per section

### Phase 4: Section-by-section drafting

Draft each major section independently but against the shared narrative.

Required behavior:
- dense, consultant-style sections
- section-specific evidence clusters
- explicit implications and transitions
- constant linkage back to client context

### Phase 5: Executive deliverable shaping

Turn the report into a product:
- hero/title framing
- dashboard metrics
- section navigation
- visual grouping of key constructs
- callouts, cards, roadmap, frameworks

### Phase 6: Critique and refinement

Evaluate the report against:
- strategic usefulness
- evidence sufficiency
- client specificity
- implementation usefulness
- presentation quality

### Phase 7: Final packaging

Produce:
- markdown report
- evidence ledger / sources state
- high-quality HTML
- optional PDF
- validation output

---

## 4. Parity Workstreams

To recreate this in Codex, the repo needs five concrete workstreams.

### Workstream A: Deep/UltraDeep Report Contract

Goal:
Force Codex to generate the right kind of artifact, not just a long answer.

Required changes:
- expand `SKILL.md`
- add explicit deliverable framing step
- require report type selection for `deep`/`ultradeep`
- require outline approval internally before drafting
- require section-level thesis statements

Deliverables:
- stronger output contract
- artifact mode definitions:
  - strategy brief
  - consulting playbook
  - workshop pack
  - architect briefing

### Workstream B: Evidence Operating System

Goal:
Make evidence capture and traceability much stricter.

Required changes:
- upgrade `sources.json` to a richer evidence ledger
- require claim-to-source mapping
- add contradiction register
- add uncertainty register
- add recommendation-to-evidence trace checks

Deliverables:
- `templates/evidence_ledger.json`
- `scripts/check_evidence_trace.py`
- updated validation docs

### Workstream C: Progressive Assembly Orchestrator

Goal:
Recreate the section-by-section discipline that Claude appears to follow.

Required changes:
- improve `report-assembly.md`
- improve `research_engine.py` so it manages section state better
- add section generation sequence metadata
- add narrative carry-forward fields
- add per-section completeness checks

Required behaviors:
- section intent
- section evidence pack
- section draft
- section critique
- append only when section passes checks

### Workstream D: Benchmark-Grade HTML Renderer

Goal:
Replace the current generic converter with a semantic renderer.

Required changes:
- rebuild `md_to_html.py`
- integrate `templates/mckinsey_report_template.html` as a true template
- support semantic block extraction from markdown
- support auto-generated:
  - header
  - subtitle
  - metrics strip
  - nav
  - sidebar
  - section labels
  - cards
  - callout boxes
  - roadmap blocks
  - vendor maps

Required design principle:
- HTML should be a designed report artifact, not a markdown dump

### Workstream E: Quality Gate Upgrade

Goal:
Evaluate the output the way a consultant or partner would, not just structurally.

Required changes:
- layered quality gates:
  - structure
  - evidence
  - decision quality
  - presentation quality
- mandatory critique artifact for deep/ultradeep
- benchmark-oriented scoring rubric

Possible scoring dimensions:
- client specificity
- evidence density
- implementation usefulness
- comparative rigor
- section completeness
- visual presentation readiness

---

## 5. Concrete Gaps vs Benchmark

This section maps current Codex behavior against what the benchmark demonstrates.

| Capability | Benchmark behavior | Current Codex state | Gap |
|---|---|---|---|
| Report ambition | consulting playbook | strong brief | high |
| Client specificity | deeply integrated | moderate | high |
| Section architecture | rich and nested | moderate | medium-high |
| Use-case structure | explicit and prioritized | present but lighter | medium |
| Roadmap and implementation plan | explicit | mostly absent | high |
| Vendor decision framing | strong | limited | high |
| Architecture explanation | layered and detailed | good but simpler | medium |
| Packaging | premium | basic | high |
| HTML rendering | designed artifact | converted markdown | very high |

---

## 6. Implementation Order

The work should be sequenced to maximize practical improvement quickly.

### Phase 1: Artifact quality contract

Update:
- `SKILL.md`
- `reference/report-assembly.md`
- `reference/quality-gates.md`

Goal:
- make deep/ultradeep outputs behave like consulting artifacts

### Phase 2: Renderer rebuild

Update:
- `scripts/md_to_html.py`
- `templates/mckinsey_report_template.html`
- possibly add semantic partial templates

Goal:
- close the most visible quality gap fast

### Phase 3: Evidence system

Update/add:
- richer `sources.json` schema
- `check_evidence_trace.py`
- validator enhancements

Goal:
- improve report correctness and depth

### Phase 4: Progressive assembly strengthening

Update:
- `research_engine.py`
- continuation and assembly docs

Goal:
- improve section quality and continuity

### Phase 5: Benchmark-based acceptance testing

Create a benchmark rubric and compare:
- structure
- density
- client specificity
- HTML quality

Goal:
- make “parity” measurable

---

## 7. Acceptance Criteria For “Claude-Level” Quality

The Codex port should be considered competitive only when it can produce a report that meets most of the following:

1. Reads like a consulting deliverable, not a generalized memo.
2. Shows strong client-specific adaptation.
3. Produces richer section structure with roadmap, use cases, risk, and vendor framing where relevant.
4. Maintains strong evidence density and explicit uncertainty.
5. Generates HTML that looks intentionally designed, not mechanically converted.
6. Passes structural validation and internal quality scoring.
7. Compares favorably to the benchmark on:
   - strategic usefulness
   - presentation quality
   - implementation usefulness
   - report architecture

---

## 8. Recommended Immediate Next Step

The highest leverage next move is:

### Rebuild the HTML pipeline first

Why:
- it is the largest visible gap
- it forces better semantic structure in the markdown
- it closes a major parity gap quickly
- it will improve how reports are authored as well as rendered

After that, implement:
- artifact contract hardening
- evidence-trace system
- progressive assembly improvements

---

## Final Diagnosis

The path to parity is not to “make Codex write more.”  
The path to parity is to recreate the **effective end-to-end report production system** Claude appears to be using:

- stronger artifact ambition
- stronger evidence discipline
- stronger section assembly
- stronger client shaping
- stronger HTML rendering

Codex can likely produce comparable results, but only if the repo encodes that process explicitly rather than assuming the model will infer it.
