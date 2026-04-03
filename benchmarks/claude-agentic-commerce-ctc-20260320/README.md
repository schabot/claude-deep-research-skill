# Benchmark: Claude Agentic Commerce CTC Report

## Purpose

This folder contains a benchmark output produced in Claude Code for a similar, but not identical, deep-research request on agentic commerce and Canadian Tire Corporation.

These files were imported to serve as the primary quality reference for the Codex parity effort.

---

## Provenance

Original source folder on the local machine:

- `/Users/chabot/Documents/Agentic_Commerce_CTC_Research_20260320/`

Imported into this repository on:

- `2026-04-03`

---

## Files

- `research_report_20260320_agentic_commerce_ctc.md`
  - benchmark markdown report
- `research_report_20260320_agentic_commerce_ctc.html`
  - benchmark HTML rendering
- `Agentic AI in Commerce_ Use Cases and Implementation for Retail.docx`
  - companion document from the same benchmark run

---

## Why This Benchmark Matters

The benchmark demonstrates that a generic deep-research scaffold can still produce a much stronger deliverable when the execution behavior is stronger.

Key observed advantages over the current Codex output:

- stronger client adaptation
- stronger section architecture
- more consulting-grade framing
- more renderable markdown structure
- much better HTML presentation quality

This folder should be used when evaluating:

- report depth
- report structure
- semantic markdown patterns
- renderer parity
- deep/ultradeep execution quality

---

## Usage Guidance

When working on parity improvements, compare against this benchmark in both forms:

1. markdown-to-markdown
2. HTML-to-HTML

Do not assume the HTML quality gap is only a renderer issue. The markdown artifact itself is also structurally better and should inform changes to:

- `SKILL.md`
- `reference/report-assembly.md`
- `templates/report_template.md`
- `scripts/md_to_html.py`
