# Password Analyzer

A command-line tool that evaluates password strength across multiple dimensions and provides actionable feedback.

## Features

- **Length analysis** — scores passwords on a tiered scale (8/12/16+ characters)
- **Character variety** — checks for uppercase, lowercase, digits, and symbols
- **Common password detection** — flags passwords from a top-100 dictionary (exact and substring matching)
- **Pattern detection** — catches repeated characters, sequential runs, and keyboard patterns (qwerty, asdf, etc.)
- **Entropy estimation** — calculates bits of entropy based on character pool size
- **0-100 scoring** with strength labels: Weak / Fair / Strong / Very Strong
- **Colored CLI output** with visual score bar

## Installation

```bash
git clone https://github.com/yourusername/password-analyzer.git
cd password-analyzer
pip install -e .
```

For development (includes pytest):

```bash
pip install -r requirements-dev.txt
```

## Usage

```bash
# Analyze a password directly
password-analyzer "MyP@ssw0rd"

# Interactive mode (hidden input)
password-analyzer

# Pipe from stdin
echo "MyP@ssw0rd" | password-analyzer --stdin

# Disable colors (for scripting)
password-analyzer --no-color "MyP@ssw0rd"

# Or run as a Python module
python -m password_analyzer "MyP@ssw0rd"
```

## How Scoring Works

The analyzer runs five independent checks, each contributing to a raw score that is normalized to 0-100:

| Check               | Points     | Description                                |
|---------------------|------------|--------------------------------------------|
| Length              | 0-3        | Tiered: <8 / 8-11 / 12-15 / 16+          |
| Character variety   | 0-4        | +1 per class: upper, lower, digit, symbol  |
| Common password     | -3 to 0    | Penalty for dictionary matches             |
| Patterns            | 0-1        | Bonus for avoiding sequences and repeats   |
| Entropy             | 0-2        | Based on bits of entropy: <28 / 28-50 / 50+|

**Strength tiers:**

| Score   | Label       |
|---------|-------------|
| 0-25    | Weak        |
| 26-50   | Fair        |
| 51-75   | Strong      |
| 76-100  | Very Strong |

## Using as a Library

```python
from password_analyzer import PasswordAnalyzer

analyzer = PasswordAnalyzer()
result = analyzer.analyze("MyP@ssw0rd")

print(result.score)        # 0-100
print(result.strength)     # "Weak" / "Fair" / "Strong" / "Very Strong"
print(result.entropy_bits) # float
print(result.feedback)     # list of suggestion strings
```

## Running Tests

```bash
pytest
```

## License

MIT
