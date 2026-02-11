from password_analyzer.analyzer import AnalysisResult, PasswordAnalyzer


class TestPasswordAnalyzer:
    def setup_method(self):
        self.analyzer = PasswordAnalyzer()

    def test_returns_analysis_result(self):
        result = self.analyzer.analyze("test")
        assert isinstance(result, AnalysisResult)

    def test_weak_password(self):
        result = self.analyzer.analyze("a")
        assert result.strength == "Weak"
        assert result.score < 26

    def test_common_password_penalized(self):
        result = self.analyzer.analyze("password")
        assert result.strength == "Weak"
        assert result.score < 26

    def test_decent_password(self):
        result = self.analyzer.analyze("Hello123!")
        assert result.score > 0
        assert result.strength in ("Fair", "Strong")

    def test_strong_password(self):
        result = self.analyzer.analyze("j8$Kp2!mX@nQ9vL#")
        assert result.score >= 76
        assert result.strength == "Very Strong"

    def test_password_length_recorded(self):
        result = self.analyzer.analyze("abcdef")
        assert result.password_length == 6

    def test_entropy_recorded(self):
        result = self.analyzer.analyze("aA1!")
        assert result.entropy_bits > 0

    def test_feedback_populated(self):
        result = self.analyzer.analyze("abc")
        assert len(result.feedback) > 0

    def test_checks_populated(self):
        result = self.analyzer.analyze("abc")
        assert len(result.checks) == 5

    def test_empty_password(self):
        result = self.analyzer.analyze("")
        assert result.strength == "Weak"
        assert result.score < 26

    def test_common_password_with_extras(self):
        # "password" is common — substring penalty + sequential "123" should drag it down
        result = self.analyzer.analyze("password123!")
        assert result.score < 70
