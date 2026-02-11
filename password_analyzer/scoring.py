"""Score normalization and strength labeling."""


def normalize_score(raw_score: float, max_raw_score: float) -> int:
    """Map a raw score to a 0-100 scale, clamped."""
    if max_raw_score <= 0:
        return 0
    return max(0, min(100, round(raw_score / max_raw_score * 100)))


def get_strength_label(score: int) -> tuple[str, str]:
    """Return a (label, color_name) tuple based on score.

    Color names are symbolic — the CLI module maps them to ANSI codes.
    """
    if score >= 76:
        return ("Very Strong", "bright_green")
    elif score >= 51:
        return ("Strong", "green")
    elif score >= 26:
        return ("Fair", "yellow")
    else:
        return ("Weak", "red")
