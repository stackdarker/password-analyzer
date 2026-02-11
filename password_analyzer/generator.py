"""Secure random password generator."""

import secrets
import string


DEFAULT_LENGTH = 16

CHARSETS = {
    "lowercase": string.ascii_lowercase,
    "uppercase": string.ascii_uppercase,
    "digits": string.digits,
    "symbols": "!@#$%^&*()-_=+[]{}|;:,.<>?",
}


def generate_password(
    length: int = DEFAULT_LENGTH,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """Generate a cryptographically secure random password.

    Guarantees at least one character from each enabled class,
    then fills the remaining length with random picks from the full pool.

    Args:
        length: Total password length (minimum 4).
        use_uppercase: Include uppercase letters.
        use_digits: Include digit characters.
        use_symbols: Include symbol characters.

    Returns:
        A random password string.

    Raises:
        ValueError: If length is less than the number of required character classes.
    """
    # Always include lowercase
    required: list[str] = [secrets.choice(CHARSETS["lowercase"])]
    pool = CHARSETS["lowercase"]

    if use_uppercase:
        required.append(secrets.choice(CHARSETS["uppercase"]))
        pool += CHARSETS["uppercase"]

    if use_digits:
        required.append(secrets.choice(CHARSETS["digits"]))
        pool += CHARSETS["digits"]

    if use_symbols:
        required.append(secrets.choice(CHARSETS["symbols"]))
        pool += CHARSETS["symbols"]

    if length < len(required):
        raise ValueError(
            f"Length must be at least {len(required)} to include all "
            f"requested character classes."
        )

    # Fill remaining slots from the full pool
    remaining = [secrets.choice(pool) for _ in range(length - len(required))]

    # Combine and shuffle so required chars aren't always at the start
    chars = required + remaining
    # Fisher-Yates shuffle using secrets for uniform randomness
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]

    return "".join(chars)
