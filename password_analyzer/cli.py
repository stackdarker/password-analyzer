"""Command-line interface for the password analyzer."""

import argparse
import getpass
import os
import sys

from .analyzer import AnalysisResult, PasswordAnalyzer
from .generator import DEFAULT_LENGTH, generate_password

COLORS = {
    "red": "\033[91m",
    "yellow": "\033[93m",
    "green": "\033[92m",
    "bright_green": "\033[92;1m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "reset": "\033[0m",
}

_use_color = True


def colorize(text: str, color: str) -> str:
    """Wrap text in ANSI color codes if color output is enabled."""
    if not _use_color or color not in COLORS:
        return text
    return f"{COLORS[color]}{text}{COLORS['reset']}"


def build_score_bar(score: int, width: int = 30) -> str:
    """Build a visual score bar like [========------] 80/100."""
    filled = round(score / 100 * width)
    empty = width - filled

    if score >= 76:
        bar_color = "bright_green"
    elif score >= 51:
        bar_color = "green"
    elif score >= 26:
        bar_color = "yellow"
    else:
        bar_color = "red"

    bar = colorize("=" * filled, bar_color) + colorize("-" * empty, "dim")
    return f"[{bar}] {score}/100"


def print_result(result: AnalysisResult, verbose: bool = False) -> None:
    """Print a formatted analysis result to stdout."""
    print()
    print(f"  {colorize('Password Strength Report', 'bold')}")
    print(f"  {'-' * 40}")
    print()
    print(f"  Score:    {build_score_bar(result.score)}")
    print(f"  Strength: {colorize(result.strength, result.strength_color)}")
    print(f"  Entropy:  {result.entropy_bits:.1f} bits")
    print(f"  Length:   {result.password_length} characters")
    print()

    if verbose:
        print(f"  {colorize('Check Breakdown:', 'bold')}")
        print(f"  {'Check':<22} {'Score':>7}  {'Details'}")
        print(f"  {'-' * 55}")
        for check in result.checks:
            score_str = f"{check.score:>4.0f}/{check.max_score:.0f}"
            detail = "; ".join(check.feedback) if check.feedback else "-"
            print(f"  {check.name:<22} {score_str:>7}  {detail}")
        print()

    suggestions = [f for f in result.feedback if any(
        word in f.lower() for word in ["add ", "too ", "low entropy", "extremely common",
                                        "common word", "contains repeated",
                                        "contains sequential", "contains reverse",
                                        "contains keyboard"]
    )]
    positives = [f for f in result.feedback if f not in suggestions]

    if positives:
        print(f"  {colorize('Strengths:', 'green')}")
        for item in positives:
            print(f"    {colorize('+', 'green')} {item}")
        print()

    if suggestions:
        print(f"  {colorize('Suggestions:', 'yellow')}")
        for item in suggestions:
            print(f"    {colorize('!', 'yellow')} {item}")
        print()


def main(argv: list[str] | None = None) -> None:
    """Entry point for the CLI."""
    # Enable ANSI colors on Windows
    if sys.platform == "win32":
        os.system("")

    global _use_color

    parser = argparse.ArgumentParser(
        prog="password-analyzer",
        description="Analyze password strength and get improvement suggestions.",
    )
    parser.add_argument(
        "password",
        nargs="?",
        help="Password to analyze (omit for interactive hidden input).",
    )
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Read password from stdin (for piping).",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output.",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed per-check score breakdown.",
    )
    parser.add_argument(
        "--generate", "-g",
        nargs="?",
        const=DEFAULT_LENGTH,
        type=int,
        metavar="LENGTH",
        help=f"Generate a strong random password (default: {DEFAULT_LENGTH} chars).",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude symbols from generated passwords.",
    )

    args = parser.parse_args(argv)

    if args.no_color or not sys.stdout.isatty():
        _use_color = False

    # Generate mode
    if args.generate is not None:
        password = generate_password(
            length=args.generate,
            use_symbols=not args.no_symbols,
        )
        print()
        print(f"  {colorize('Generated password:', 'bold')} {password}")

        analyzer = PasswordAnalyzer()
        result = analyzer.analyze(password)
        print_result(result, verbose=args.verbose)
        return

    # Analyze mode
    if args.stdin:
        password = sys.stdin.readline().rstrip("\n")
    elif args.password is not None:
        password = args.password
    else:
        password = getpass.getpass("Enter password to analyze: ")

    if not password:
        print("Error: empty password provided.", file=sys.stderr)
        sys.exit(1)

    analyzer = PasswordAnalyzer()
    result = analyzer.analyze(password)
    print_result(result, verbose=args.verbose)
