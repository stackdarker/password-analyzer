import math

import pytest

from password_analyzer.entropy import calculate_entropy


class TestCalculateEntropy:
    def test_empty_string(self):
        assert calculate_entropy("") == 0.0

    def test_lowercase_only(self):
        # 8 chars, pool = 26 -> 8 * log2(26)
        expected = 8 * math.log2(26)
        assert calculate_entropy("abcdefgh") == pytest.approx(expected)

    def test_uppercase_only(self):
        expected = 6 * math.log2(26)
        assert calculate_entropy("ABCDEF") == pytest.approx(expected)

    def test_digits_only(self):
        expected = 4 * math.log2(10)
        assert calculate_entropy("1234") == pytest.approx(expected)

    def test_symbols_only(self):
        expected = 3 * math.log2(32)
        assert calculate_entropy("!@#") == pytest.approx(expected)

    def test_mixed_lower_and_digits(self):
        # pool = 26 + 10 = 36
        expected = 6 * math.log2(36)
        assert calculate_entropy("abc123") == pytest.approx(expected)

    def test_all_character_classes(self):
        # pool = 26 + 26 + 10 + 32 = 94
        password = "aA1!"
        expected = 4 * math.log2(94)
        assert calculate_entropy(password) == pytest.approx(expected)

    def test_longer_password_has_more_entropy(self):
        short = calculate_entropy("aA1!")
        long = calculate_entropy("aA1!bB2@cC3#")
        assert long > short

    def test_single_character(self):
        expected = 1 * math.log2(26)
        assert calculate_entropy("a") == pytest.approx(expected)
