from password_analyzer.scoring import get_strength_label, normalize_score


class TestNormalizeScore:
    def test_full_score(self):
        assert normalize_score(10, 10) == 100

    def test_zero_score(self):
        assert normalize_score(0, 10) == 0

    def test_half_score(self):
        assert normalize_score(5, 10) == 50

    def test_negative_clamps_to_zero(self):
        assert normalize_score(-5, 10) == 0

    def test_over_max_clamps_to_100(self):
        assert normalize_score(15, 10) == 100

    def test_zero_max_returns_zero(self):
        assert normalize_score(5, 0) == 0

    def test_rounding(self):
        assert normalize_score(1, 3) == 33
        assert normalize_score(2, 3) == 67


class TestGetStrengthLabel:
    def test_weak(self):
        label, color = get_strength_label(0)
        assert label == "Weak"
        assert color == "red"

    def test_weak_boundary(self):
        label, _ = get_strength_label(25)
        assert label == "Weak"

    def test_fair(self):
        label, color = get_strength_label(26)
        assert label == "Fair"
        assert color == "yellow"

    def test_fair_boundary(self):
        label, _ = get_strength_label(50)
        assert label == "Fair"

    def test_strong(self):
        label, color = get_strength_label(51)
        assert label == "Strong"
        assert color == "green"

    def test_strong_boundary(self):
        label, _ = get_strength_label(75)
        assert label == "Strong"

    def test_very_strong(self):
        label, color = get_strength_label(76)
        assert label == "Very Strong"
        assert color == "bright_green"

    def test_perfect_score(self):
        label, _ = get_strength_label(100)
        assert label == "Very Strong"
