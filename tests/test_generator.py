import pytest

from password_analyzer.generator import generate_password


class TestGeneratePassword:
    def test_default_length(self):
        password = generate_password()
        assert len(password) == 16

    def test_custom_length(self):
        password = generate_password(length=24)
        assert len(password) == 24

    def test_contains_all_classes_by_default(self):
        # Run multiple times to account for randomness
        for _ in range(10):
            password = generate_password(length=16)
            assert any(c.islower() for c in password)
            assert any(c.isupper() for c in password)
            assert any(c.isdigit() for c in password)
            assert any(not c.isalnum() for c in password)

    def test_no_symbols(self):
        for _ in range(10):
            password = generate_password(length=12, use_symbols=False)
            assert all(c.isalnum() for c in password)

    def test_no_uppercase(self):
        for _ in range(10):
            password = generate_password(length=12, use_uppercase=False)
            assert not any(c.isupper() for c in password)

    def test_no_digits(self):
        for _ in range(10):
            password = generate_password(length=12, use_digits=False)
            assert not any(c.isdigit() for c in password)

    def test_minimum_length(self):
        # 4 classes enabled = minimum length 4
        password = generate_password(length=4)
        assert len(password) == 4

    def test_length_too_short_raises(self):
        with pytest.raises(ValueError):
            generate_password(length=2)

    def test_uniqueness(self):
        # Two generated passwords should differ (astronomically unlikely to collide)
        p1 = generate_password()
        p2 = generate_password()
        assert p1 != p2

    def test_lowercase_only(self):
        for _ in range(10):
            password = generate_password(
                length=10,
                use_uppercase=False,
                use_digits=False,
                use_symbols=False,
            )
            assert password.islower()
            assert len(password) == 10
