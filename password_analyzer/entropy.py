"""Password entropy estimation."""

import math


def calculate_entropy(password: str) -> float:
    """Estimate password entropy in bits.

    Uses the formula: entropy = length * log2(pool_size)
    where pool_size is determined by which character classes are present.

    This assumes characters are chosen uniformly at random from the pool,
    so it overestimates entropy for non-random passwords. Other checks
    (common password, sequential characters) compensate for this.
    """
    if not password:
        return 0.0

    pool_size = 0
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    if has_lower:
        pool_size += 26
    if has_upper:
        pool_size += 26
    if has_digit:
        pool_size += 10
    if has_symbol:
        pool_size += 32

    if pool_size == 0:
        return 0.0

    return len(password) * math.log2(pool_size)
