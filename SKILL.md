---
name: deep-research
description: Codex-native deep research workflow for multi-source synthesis, citation tracking, and validated report generation with explicit file artifacts.
version: 3.0.0
owners:
  - repository-maintainers
triggers:
  - deep research
  - comprehensive analysis
  - research report
  - compare x vs y
  - analyze trends
  - state of the art
---

# Deep Research (Codex-Native)

## Purpose

Deliver citation-backed, verifiable research reports through a structured pipeline that preserves the existing methodology while using Codex shell-first execution and explicit artifact outputs.

---

## When to Use

Use this skill when the task requires:
- Multi-source research and synthesis (not a quick lookup)
- Evidence tracking and citation hygiene
- Structured report output (Markdown + HTML, optional PDF)
- Validation before delivery

## When NOT to Use

Do **not** use this skill for:
- Simple factual lookups answerable in 1-2 searches
- Pure debugging tasks
- Small edits that do not require full research workflow
- Time-critical requests where exhaustive validation cannot be completed

---

## Research Modes

| Mode | Phases | Typical Duration | Best For |
|------|--------|------------------|----------|
| quick | 3 | 2-5 min | Initial exploration |
| standard (default) | 6 | 5-10 min | Most research requests |
| deep | 8 | 10-20 min | High-stakes or complex decisions |
| ultradeep | 8+ | 20-45 min | Maximum rigor/comprehensive reviews |

Phase mapping and quality expectations remain defined in the reference docs.

---

## Methodology Sources (Keep Intact)

Load references progressively (only what is needed for the current phase):

1. Pipeline phases (1-7): `reference/methodology.md`
2. Packaging and section assembly: `reference/report-assembly.md`
3. HTML conversion and presentation: `reference/html-generation.md`
4. Quality checks and validation loop: `reference/quality-gates.md`
5. Continuation protocol for long reports: `reference/continuation.md`

Templates:
- Markdown report skeleton: `templates/report_template.md`
- HTML template: `templates/mckinsey_report_template.html`

---

## Codex Workflow (Explicit)

### Step 0 - Initialize workspace
1. Determine report topic slug and date (`YYYYMMDD`).
2. Create output folder:
   - `./[Topic]_Research_[YYYYMMDD]/` (relative to current working folder)
3. Define artifact paths:
   - Markdown: `research_report_[YYYYMMDD]_[topic].md`
   - HTML: `research_report_[YYYYMMDD]_[topic].html`
   - PDF (optional): `research_report_[YYYYMMDD]_[topic].pdf`
   - Source state: `sources.json`

### Step 1 - Scope and plan
- Execute SCOPE and PLAN phases from `reference/methodology.md`.
- Confirm boundaries, assumptions, query strategy, and quality gates.

### Step 2 - Retrieve and triangulate
- Run RETRIEVE phase with parallelizable search angles where possible.
- Capture source metadata and evidence snippets into `sources.json`.
- Run TRIANGULATE to verify major claims across independent sources.

### Step 3 - Synthesize and critique (mode-dependent)
- Generate findings and cross-source synthesis.
- In deep/ultradeep, run CRITIQUE and REFINE loops.

### Step 4 - Package output artifacts
- Build markdown report progressively using `templates/report_template.md` structure.
- Ensure bibliography is complete and numbered correctly.
- Convert markdown to HTML using script calls below.
- Generate PDF optionally (WeasyPrint guidance in `reference/weasyprint_guidelines.md`).

---

## Script Calls (Explicit)

From repository root:

```bash
python scripts/validate_report.py --report [markdown_report_path]
python scripts/verify_citations.py --report [markdown_report_path]
python scripts/md_to_html.py [markdown_report_path]
python scripts/verify_html.py --html [html_report_path] --md [markdown_report_path]
```

Optional engine scaffolding:

```bash
python scripts/research_engine.py --query "[research question]" --mode [quick|standard|deep|ultradeep]
```

---

## Output Artifacts (Required)

Each run must produce (at minimum):
1. **Markdown report** (source of truth)
2. **HTML report** (rendered presentation)
3. **`sources.json`** (durable source/citation tracking)

Optional:
4. **PDF report** (print-ready)

Report content requirements:
- Executive Summary
- Introduction (scope/methodology/assumptions)
- Main Analysis (evidence-backed findings)
- Synthesis & Insights
- Limitations & Caveats
- Recommendations
- Bibliography (complete; no placeholders)
- Methodology Appendix

---

## Validation Contract

Run validation loop before delivery:

1. `validate_report.py`
2. `verify_citations.py`
3. (if HTML generated) `verify_html.py`

If any validation fails:
- Fix the reported issue(s)
- Re-run all required validators
- Maximum 3 fix cycles

Do not deliver final output if critical checks still fail.

---

## Failure Handling

Stop and report clearly when any of the following occurs:
- Fewer than 5 credible sources after exhaustive retrieval
- Bibliography/citation mismatch that cannot be resolved after retries
- Repeated validation failure after 3 cycles
- Scope becomes ambiguous or incompatible with available evidence

Failure report format:
- **Issue:** what failed
- **Context:** what was attempted
- **Tried:** remediation steps already taken
- **Next options:** 1-2 concrete paths to proceed

---

## Quality Standards (Non-Negotiable)

- 10+ sources preferred (document shortfall if not achievable)
- Major claims supported by 3+ independent sources when possible
- Immediate claim-level citation placement `[N]`
- No fabricated citations, placeholders, or truncated bibliography entries
- Prose-first writing style with precise, evidence-rich statements
