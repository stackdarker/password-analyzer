import subprocess
import sys

from password_analyzer.cli import main


class TestCLIWithArgs:
    def test_analyze_weak_password(self, capsys):
        main(["--no-color", "abc"])
        output = capsys.readouterr().out
        assert "Weak" in output
        assert "Score:" in output

    def test_analyze_strong_password(self, capsys):
        main(["--no-color", "j8$Kp2!mX@nQ9vL#"])
        output = capsys.readouterr().out
        assert "Very Strong" in output

    def test_no_color_flag(self, capsys):
        main(["--no-color", "Hello123!"])
        output = capsys.readouterr().out
        assert "\033[" not in output

    def test_empty_password_exits(self):
        try:
            main(["--no-color", ""])
        except SystemExit as e:
            assert e.code == 1

    def test_stdin_mode(self, capsys, monkeypatch):
        import io
        monkeypatch.setattr("sys.stdin", io.StringIO("TestPassword1!\n"))
        main(["--no-color", "--stdin"])
        output = capsys.readouterr().out
        assert "Score:" in output


class TestCLISubprocess:
    def test_help_flag(self):
        result = subprocess.run(
            [sys.executable, "-m", "password_analyzer", "--help"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "password" in result.stdout.lower()

    def test_direct_invocation(self):
        result = subprocess.run(
            [sys.executable, "-m", "password_analyzer", "--no-color", "Hello123!"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Score:" in result.stdout
