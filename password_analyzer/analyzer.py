"""Core password analysis orchestrator."""

from __future__ import annotations

import dataclasses

from .checks import (
    CheckResult,
    check_character_variety,
    check_common_password,
    check_entropy,
    check_length,
    check_sequential_characters,
)
from .entropy import calculate_entropy
from .scoring import get_strength_label, normalize_score


@dataclasses.dataclass
class AnalysisResult:
    """Complete result of a password analysis."""

    password_length: int
    score: int
    strength: str
    strength_color: str
    entropy_bits: float
    checks: list[CheckResult]
    feedback: list[str]


class PasswordAnalyzer:
    """Analyzes password strength across multiple dimensions."""

    def analyze(self, password: str) -> AnalysisResult:
        """Run all checks and return an aggregated result."""
        entropy_bits = calculate_entropy(password)

        checks = [
            check_length(password),
            check_character_variety(password),
            check_common_password(password),
            check_sequential_characters(password),
            check_entropy(entropy_bits),
        ]

        raw_score = sum(c.score for c in checks)
        max_score = sum(c.max_score for c in checks)
        score = normalize_score(raw_score, max_score)
        strength, color = get_strength_label(score)

        feedback: list[str] = []
        for check in checks:
            feedback.extend(check.feedback)

        return AnalysisResult(
            password_length=len(password),
            score=score,
            strength=strength,
            strength_color=color,
            entropy_bits=entropy_bits,
            checks=checks,
            feedback=feedback,
        )
