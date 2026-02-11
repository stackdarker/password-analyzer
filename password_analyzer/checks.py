"""Individual password strength check functions."""

from __future__ import annotations

import dataclasses

from .common_passwords import COMMON_PASSWORDS

KEYBOARD_PATTERNS: list[str] = [
    "qwerty", "qwertz", "azerty",
    "asdf", "zxcv",
    "qazwsx", "1qaz2wsx",
]


@dataclasses.dataclass
class CheckResult:
    """Result from a single password check."""

    name: str
    score: float
    max_score: float
    feedback: list[str]


def check_length(password: str) -> CheckResult:
    """Score password based on length."""
    length = len(password)
    if length >= 16:
        return CheckResult("Length", 3, 3, ["Great length (16+ characters)."])
    elif length >= 12:
        return CheckResult("Length", 2, 3, ["Good length (12-15 characters)."])
    elif length >= 8:
        return CheckResult("Length", 1, 3, ["Decent length (8-11 characters)."])
    else:
        return CheckResult("Length", 0, 3, ["Too short — use at least 8 characters."])


def check_character_variety(password: str) -> CheckResult:
    """Score password based on character class diversity."""
    score = 0
    feedback: list[str] = []

    classes = [
        (any(c.isupper() for c in password), "uppercase letters"),
        (any(c.islower() for c in password), "lowercase letters"),
        (any(c.isdigit() for c in password), "digits"),
        (any(not c.isalnum() for c in password), "symbols"),
    ]

    for present, name in classes:
        if present:
            score += 1
            feedback.append(f"Contains {name}.")
        else:
            feedback.append(f"Add {name}.")

    return CheckResult("Character variety", score, 4, feedback)


def check_common_password(password: str) -> CheckResult:
    """Check if the password appears in a common password dictionary."""
    lower = password.lower()

    if lower in COMMON_PASSWORDS:
        return CheckResult(
            "Common password", -3, 0,
            ["This is an extremely common password — choose something unique."],
        )

    for common in COMMON_PASSWORDS:
        if len(common) >= 4 and common in lower:
            return CheckResult(
                "Common password", -1, 0,
                [f"Contains the common word '{common}' — avoid dictionary words."],
            )

    return CheckResult("Common password", 0, 0, [])


def check_sequential_characters(password: str) -> CheckResult:
    """Detect repeated, sequential, and keyboard-pattern characters."""
    issues: list[str] = []

    # Repeated characters (3+ identical in a row)
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            issues.append("Contains repeated characters (e.g., 'aaa').")
            break

    # Sequential runs (3+ ascending or descending ASCII)
    for i in range(len(password) - 2):
        a, b, c = ord(password[i]), ord(password[i + 1]), ord(password[i + 2])
        if b - a == 1 and c - b == 1:
            issues.append("Contains sequential characters (e.g., 'abc', '123').")
            break
        if a - b == 1 and b - c == 1:
            issues.append("Contains reverse sequential characters (e.g., 'cba', '321').")
            break

    # Keyboard patterns
    lower = password.lower()
    for pattern in KEYBOARD_PATTERNS:
        if pattern in lower:
            issues.append(f"Contains keyboard pattern '{pattern}'.")
            break

    if issues:
        return CheckResult("Patterns", 0, 1, issues)

    return CheckResult("Patterns", 1, 1, ["No common patterns detected."])


def check_entropy(entropy_bits: float) -> CheckResult:
    """Score based on pre-computed entropy value."""
    if entropy_bits >= 50:
        return CheckResult(
            "Entropy", 2, 2,
            [f"Good entropy ({entropy_bits:.1f} bits)."],
        )
    elif entropy_bits >= 28:
        return CheckResult(
            "Entropy", 1, 2,
            [f"Moderate entropy ({entropy_bits:.1f} bits)."],
        )
    else:
        return CheckResult(
            "Entropy", 0, 2,
            [f"Low entropy ({entropy_bits:.1f} bits) — use a longer, more varied password."],
        )
