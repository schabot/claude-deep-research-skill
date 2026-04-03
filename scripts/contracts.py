#!/usr/bin/env python3
"""Shared runtime contracts for the Codex research engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Set

MODES: tuple[str, ...] = ("quick", "standard", "deep", "ultradeep")

MODE_CONTRACTS: Dict[str, Dict[str, int]] = {
    "quick": {
        "min_words": 1500,
        "max_words": 3500,
        "min_unique_citations": 8,
        "max_cycles": 1,
    },
    "standard": {
        "min_words": 3500,
        "max_words": 7000,
        "min_unique_citations": 12,
        "max_cycles": 2,
    },
    "deep": {
        "min_words": 7500,
        "max_words": 14000,
        "min_unique_citations": 18,
        "max_cycles": 4,
    },
    "ultradeep": {
        "min_words": 11000,
        "max_words": 22000,
        "min_unique_citations": 24,
        "max_cycles": 6,
    },
}

REQUIRED_SECTIONS: Dict[str, Dict[str, int]] = {
    "Executive Summary": {
        "quick": 200,
        "standard": 200,
        "deep": 200,
        "ultradeep": 200,
    },
    "Introduction": {
        "quick": 300,
        "standard": 400,
        "deep": 400,
        "ultradeep": 400,
    },
    "Main Analysis": {
        "quick": 900,
        "standard": 1800,
        "deep": 2500,
        "ultradeep": 4000,
    },
    "Synthesis & Insights": {
        "quick": 250,
        "standard": 600,
        "deep": 900,
        "ultradeep": 1200,
    },
    "Limitations & Caveats": {
        "quick": 150,
        "standard": 250,
        "deep": 250,
        "ultradeep": 250,
    },
    "Recommendations": {
        "quick": 250,
        "standard": 500,
        "deep": 500,
        "ultradeep": 500,
    },
    "Bibliography": {
        "quick": 1,
        "standard": 1,
        "deep": 1,
        "ultradeep": 1,
    },
    "Methodology Appendix": {
        "quick": 200,
        "standard": 300,
        "deep": 300,
        "ultradeep": 300,
    },
}

GATE_NAMES: Dict[str, str] = {
    "section_minimums": "section_minimums_gate",
    "mode_length": "mode_length_gate",
    "citation": "citation_gate",
    "bibliography": "bibliography_gate",
    "markdown_validation": "markdown_validation_gate",
    "html_parity": "html_parity_gate",
}

CRITICAL_GATES: Set[str] = {
    GATE_NAMES["section_minimums"],
    GATE_NAMES["mode_length"],
    GATE_NAMES["citation"],
    GATE_NAMES["bibliography"],
    GATE_NAMES["markdown_validation"],
    GATE_NAMES["html_parity"],
}

ALLOW_BELOW_MINIMUM_OVERRIDES: Set[str] = {
    GATE_NAMES["section_minimums"],
    GATE_NAMES["mode_length"],
}

SKIP_HTML_OVERRIDES: Set[str] = {
    GATE_NAMES["html_parity"],
}


@dataclass(frozen=True)
class FinalizationPolicyInput:
    """Inputs required to evaluate whether packaging/finalization may proceed."""

    gate_results: Mapping[str, bool]
    allow_below_minimum: bool = False
    skip_html: bool = False
    critical_gates: Set[str] = field(default_factory=lambda: set(CRITICAL_GATES))


@dataclass(frozen=True)
class FinalizationPolicyDecision:
    """Decision payload for machine-readable finalization handling."""

    can_finalize: bool
    failed_critical_gates: List[str]
    ignored_gates: List[str]
    blocking_reasons: List[str]


def evaluate_finalization_policy(
    policy_input: FinalizationPolicyInput,
) -> FinalizationPolicyDecision:
    """Evaluate critical gate outcomes without needing full engine execution."""

    failed: List[str] = []
    ignored: List[str] = []

    for gate_name in sorted(policy_input.critical_gates):
        gate_passed = policy_input.gate_results.get(gate_name, False)
        if gate_passed:
            continue

        if policy_input.allow_below_minimum and gate_name in ALLOW_BELOW_MINIMUM_OVERRIDES:
            ignored.append(gate_name)
            continue

        if policy_input.skip_html and gate_name in SKIP_HTML_OVERRIDES:
            ignored.append(gate_name)
            continue

        failed.append(gate_name)

    reasons = [f"Critical gate failed: {gate}" for gate in failed]
    can_finalize = len(failed) == 0

    return FinalizationPolicyDecision(
        can_finalize=can_finalize,
        failed_critical_gates=failed,
        ignored_gates=ignored,
        blocking_reasons=reasons,
    )


__all__ = [
    "ALLOW_BELOW_MINIMUM_OVERRIDES",
    "CRITICAL_GATES",
    "FinalizationPolicyDecision",
    "FinalizationPolicyInput",
    "GATE_NAMES",
    "MODE_CONTRACTS",
    "MODES",
    "REQUIRED_SECTIONS",
    "SKIP_HTML_OVERRIDES",
    "evaluate_finalization_policy",
]
