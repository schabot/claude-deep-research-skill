# AGENTS.md

## Repository mission
Port this repository from a Claude-oriented deep-research skill to a **Codex-native skill** while preserving methodology, evidence quality, and validation rigor.

## Primary objectives
- Preserve the research pipeline and helper scripts where practical.
- Remove Claude-specific wording, paths, and runtime assumptions.
- Keep instructions shell-first and explicit for Codex execution.
- Favor deterministic file outputs and validation loops.

## Working rules for contributors/agents
1. **Read before editing**
   - Start with: `SKILL.md`, `README.md`, `MIGRATION_PLAN.md`, `MIGRATION_NOTES.md` (if present), and `reference/*.md` relevant to your change.
2. **Minimize unnecessary churn**
   - Keep existing methodology intact unless explicitly asked to change it.
   - Prefer targeted edits over broad rewrites.
3. **Preserve reusable components**
   - Reuse and keep `scripts/*.py`, `templates/*`, and `tests/fixtures/*` unless a change is necessary.
4. **Provider neutrality**
   - Do not introduce Claude-only pathing (`~/.claude/...`) or provider-coupled execution language.
   - Use current-working-directory or explicit user-configurable paths.
5. **File lifecycle policy**
   - Do not delete original files outright.
   - If a file is fully superseded, move it to `archive/` and document why.

## Required documentation updates during migration
When making migration-related changes:
- Update `MIGRATION_PLAN.md` if scope or sequence changes.
- Append implementation decisions, tradeoffs, and open items to `MIGRATION_NOTES.md`.

## Validation and smoke checks
After editing instructions/scripts/templates, run applicable checks:

```bash
python scripts/research_engine.py --help
python scripts/validate_report.py --help
python scripts/verify_citations.py --help
python scripts/md_to_html.py --help
python scripts/verify_html.py --help
```

If report artifacts are changed/generated, also run:

```bash
python scripts/validate_report.py --report [markdown_report_path]
python scripts/verify_citations.py --report [markdown_report_path]
python scripts/verify_html.py --html [html_report_path] --md [markdown_report_path]
```

## Manual review checklist (must summarize in final response)
- Any remaining Claude-specific wording or assumptions.
- Any pathing defaults that are not current-working-directory based.
- Any script/template coupling risks (e.g., report sections expected by validators).
- Any deferred work requiring human decision.

## Commit/PR expectations
- Keep commits scoped and descriptive.
- Mention modified files and why.
- Include test/smoke-check commands and outcomes.
