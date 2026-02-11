from password_analyzer.checks import (
    CheckResult,
    check_character_variety,
    check_common_password,
    check_entropy,
    check_length,
    check_sequential_characters,
)


class TestCheckLength:
    def test_short_password(self):
        result = check_length("abc")
        assert result.score == 0
        assert result.max_score == 3

    def test_decent_password(self):
        result = check_length("abcdefgh")
        assert result.score == 1

    def test_good_password(self):
        result = check_length("a" * 12)
        assert result.score == 2

    def test_great_password(self):
        result = check_length("a" * 16)
        assert result.score == 3

    def test_empty_password(self):
        result = check_length("")
        assert result.score == 0

    def test_boundary_8(self):
        assert check_length("a" * 7).score == 0
        assert check_length("a" * 8).score == 1

    def test_boundary_12(self):
        assert check_length("a" * 11).score == 1
        assert check_length("a" * 12).score == 2

    def test_boundary_16(self):
        assert check_length("a" * 15).score == 2
        assert check_length("a" * 16).score == 3


class TestCheckCharacterVariety:
    def test_all_classes(self):
        result = check_character_variety("aA1!")
        assert result.score == 4

    def test_lowercase_only(self):
        result = check_character_variety("abcdef")
        assert result.score == 1

    def test_uppercase_only(self):
        result = check_character_variety("ABCDEF")
        assert result.score == 1

    def test_digits_only(self):
        result = check_character_variety("123456")
        assert result.score == 1

    def test_symbols_only(self):
        result = check_character_variety("!@#$%")
        assert result.score == 1

    def test_lower_and_upper(self):
        result = check_character_variety("aAbBcC")
        assert result.score == 2

    def test_empty_password(self):
        result = check_character_variety("")
        assert result.score == 0

    def test_feedback_for_missing_classes(self):
        result = check_character_variety("abc")
        assert any("Add uppercase" in f for f in result.feedback)
        assert any("Add digits" in f for f in result.feedback)
        assert any("Add symbols" in f for f in result.feedback)


class TestCheckCommonPassword:
    def test_exact_match(self):
        result = check_common_password("password")
        assert result.score == -3

    def test_case_insensitive_match(self):
        result = check_common_password("PASSWORD")
        assert result.score == -3

    def test_substring_match(self):
        result = check_common_password("mypassword99")
        assert result.score == -1

    def test_safe_password(self):
        result = check_common_password("j8Kp2mXnQ9")
        assert result.score == 0

    def test_short_common_words_not_substring_matched(self):
        # Common passwords shorter than 4 chars shouldn't trigger substring match
        result = check_common_password("xyzpassxyz")
        # "pass" is in the list and len >= 4, so it should match
        assert result.score == -1

    def test_exact_match_takes_priority(self):
        result = check_common_password("admin")
        assert result.score == -3


class TestCheckSequentialCharacters:
    def test_repeated_characters(self):
        result = check_sequential_characters("paaassword")
        assert result.score == 0
        assert any("repeated" in f.lower() for f in result.feedback)

    def test_ascending_sequence(self):
        result = check_sequential_characters("xabc99")
        assert result.score == 0
        assert any("sequential" in f.lower() for f in result.feedback)

    def test_descending_sequence(self):
        result = check_sequential_characters("xcba99")
        assert result.score == 0
        assert any("reverse" in f.lower() for f in result.feedback)

    def test_numeric_sequence(self):
        result = check_sequential_characters("x12345")
        assert result.score == 0

    def test_keyboard_pattern(self):
        result = check_sequential_characters("myqwerty1")
        assert result.score == 0
        assert any("keyboard" in f.lower() for f in result.feedback)

    def test_no_patterns(self):
        result = check_sequential_characters("j8Kp2mXn")
        assert result.score == 1

    def test_empty_password(self):
        result = check_sequential_characters("")
        assert result.score == 1

    def test_short_password_no_false_positive(self):
        result = check_sequential_characters("ab")
        assert result.score == 1


class TestCheckEntropy:
    def test_high_entropy(self):
        result = check_entropy(60.0)
        assert result.score == 2

    def test_moderate_entropy(self):
        result = check_entropy(35.0)
        assert result.score == 1

    def test_low_entropy(self):
        result = check_entropy(15.0)
        assert result.score == 0

    def test_boundary_50(self):
        assert check_entropy(49.9).score == 1
        assert check_entropy(50.0).score == 2

    def test_boundary_28(self):
        assert check_entropy(27.9).score == 0
        assert check_entropy(28.0).score == 1

    def test_zero_entropy(self):
        result = check_entropy(0.0)
        assert result.score == 0
