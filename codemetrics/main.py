"""
Command-line interface entry point for CodeMetrics.
"""

import argparse
from pathlib import Path
from codemetrics.analyzers.directory_scanner import DirectoryScanner
from codemetrics.reports.formatter import ReportFormatter


def main() -> None:
    """Main CLI execution function."""
    parser = argparse.ArgumentParser(
        description="CodeMetrics: A Python static code analysis tool."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the Python project directory to analyze (default: current directory)",
    )

    args = parser.parse_args()
    target_path = Path(args.path)

    if not target_path.exists():
        print(f"Error: Path '{target_path}' does not exist.")
        return

    print(f"Scanning '{target_path.resolve()}' for Python files...")

    scanner = DirectoryScanner(target_path)
    file_metrics = scanner.scan()

    formatter = ReportFormatter(file_metrics, target_path)
    formatter.print_report()


if __name__ == "__main__":
    main()