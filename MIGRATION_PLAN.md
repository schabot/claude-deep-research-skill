# MIGRATION_PLAN

## Scope
Port this repository from a Claude-oriented deep-research skill to a Codex-native skill repository while preserving the research methodology, validation rigor, and helper tooling.

---

## 1) Current Repository Structure

```text
.
├── AGENTS.md
├── README.md
├── SKILL.md
├── requirements.txt
├── reference/
│   ├── continuation.md
│   ├── html-generation.md
│   ├── methodology.md
│   ├── quality-gates.md
│   ├── report-assembly.md
│   └── weasyprint_guidelines.md
├── scripts/
│   ├── citation_manager.py
│   ├── md_to_html.py
│   ├── research_engine.py
│   ├── source_evaluator.py
│   ├── validate_report.py
│   ├── verify_citations.py
│   └── verify_html.py
├── templates/
│   ├── mckinsey_report_template.html
│   └── report_template.md
└── tests/
    └── fixtures/
        ├── invalid_report.md
        └── valid_report.md
```

### Functional groupings
- **Entrypoint/UX:** `SKILL.md`, `README.md`
- **Methodology references:** `reference/*.md`
- **Automation and validation scripts:** `scripts/*.py`
- **Report and HTML templates:** `templates/*`
- **Validation fixtures:** `tests/fixtures/*`

---

## 2) Claude-Specific Constructs (to migrate)

### A. Branding and runtime wording
- "Claude Code" phrasing appears in script docstrings/help text and reference docs.
- Some instructions assume Claude-specific execution behavior/tooling language.

### B. Claude-specific filesystem paths
- Hardcoded/explicit references to `~/.claude/...` in:
  - state/output storage guidance
  - installation and command examples

### C. Provider-specific orchestration examples
- `Task(...)`-style continuation examples and provider-coupled orchestration snippets in reference docs.

### D. Provider-specific output constraints
- Token-limit language tied to Claude defaults rather than neutral budgeting guidance.

### E. Mixed-positioning documentation
- Repository presents as Codex-native, but some README and reference sections still instruct Claude-specific setup/usage.

---

## 3) Reusable Scripts and Assets (retain with minimal change)

### Scripts that are already reusable
- `scripts/validate_report.py` — report structure and quality gate checks.
- `scripts/verify_citations.py` — citation verification and hallucination-pattern detection.
- `scripts/source_evaluator.py` — source credibility scoring.
- `scripts/citation_manager.py` — citation/state management helpers.
- `scripts/md_to_html.py` — markdown to HTML conversion.
- `scripts/verify_html.py` — HTML/report parity and structure checks.

### Script requiring adaptation (not replacement)
- `scripts/research_engine.py`:
  - update branding/help text
  - remove Claude-only output path defaults
  - add/standardize Codex-neutral output directory behavior

### Reusable assets/templates
- `templates/mckinsey_report_template.html` — reusable visual layout.
- `templates/report_template.md` — reusable report skeleton with wording cleanup.
- `tests/fixtures/*.md` — reusable validator fixture inputs.
- Most methodology guidance in `reference/methodology.md` and `reference/quality-gates.md` is reusable with runtime-language normalization.

---

## 4) Target Codex-Native Structure

```text
.
├── AGENTS.md
├── README.md                        # Codex-native install/use docs
├── SKILL.md                         # Codex-native execution contract
├── MIGRATION_PLAN.md                # this plan
├── MIGRATION_NOTES.md               # implementation notes and decisions
├── requirements.txt
├── reference/
│   ├── continuation.md              # provider-neutral continuation protocol
│   ├── html-generation.md           # repo-relative shell commands
│   ├── methodology.md               # preserved core pipeline
│   ├── quality-gates.md             # preserved validation standards
│   ├── report-assembly.md           # neutral output budgeting/pathing
│   └── weasyprint_guidelines.md
├── scripts/
│   ├── citation_manager.py
│   ├── md_to_html.py
│   ├── research_engine.py           # Codex-native defaults/messages
│   ├── source_evaluator.py
│   ├── validate_report.py
│   ├── verify_citations.py
│   └── verify_html.py
├── templates/
│   ├── mckinsey_report_template.html
│   └── report_template.md           # wording updated for neutral/Codex runtime
├── tests/
│   └── fixtures/
│       ├── invalid_report.md
│       └── valid_report.md
└── archive/                         # only if superseded docs are moved
    └── README.md
```

### Structural intent
- Preserve file layout and helper scripts unless change is necessary.
- Normalize docs/instructions to Codex shell execution.
- Keep explicit, deterministic file outputs and validation flow.
- Use `archive/` only when full-file supersession is needed.

---

## 5) Risks and Unknowns

### Technical risks
1. **Behavior drift risk:** wording cleanups in methodology docs may accidentally alter workflow guarantees.
2. **Pathing regressions:** changing default output locations can break implicit assumptions in existing user workflows.
3. **Continuation ambiguity:** replacing provider-specific `Task(...)` examples may reduce clarity unless equivalent Codex guidance is explicit.
4. **Template-validator coupling:** edits to `templates/report_template.md` may conflict with `validate_report.py` required section expectations.
5. **Cross-doc inconsistency:** SKILL/README/reference docs can diverge unless updated together.

### Operational unknowns
1. Preferred long-term Codex output root (repo-local vs `~/Documents/...` vs configurable-only).
2. Whether continuation should remain instruction-only or gain an executable helper script.
3. Degree of backward-compatibility desired for users migrating from Claude folder conventions.
4. Whether to keep upstream-oriented Claude attribution in README as historical context or reduce it further.

### Mitigations
- Apply changes in small, reviewable steps.
- Run smoke checks after edits:
  - `python scripts/research_engine.py --help`
  - `python scripts/validate_report.py --help`
  - `python scripts/verify_citations.py --help`
  - `python scripts/md_to_html.py --help`
  - `python scripts/verify_html.py --help`
- Record final decisions and any deferred follow-ups in `MIGRATION_NOTES.md`.
