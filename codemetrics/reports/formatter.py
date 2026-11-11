"""
Report formatter to aggregate and present code metrics cleanly in the terminal.
"""

from typing import List, Dict, Any
from pathlib import Path


class ReportFormatter:
    """Aggregates individual file metrics and formats summary reports."""

    def __init__(self, file_metrics: List[Dict[str, Any]], root_dir: Path):
        self.file_metrics = file_metrics
        self.root_dir = Path(root_dir).resolve()

    def generate_summary(self) -> Dict[str, Any]:
        """Calculates totals and averages across all analyzed files."""
        summary = {
            "total_files": len(self.file_metrics),
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "functions": 0,
            "classes": 0,
            "async_functions": 0,
        }

        for metrics in self.file_metrics:
            summary["total_lines"] += metrics["total_lines"]
            summary["code_lines"] += metrics["code_lines"]
            summary["comment_lines"] += metrics["comment_lines"]
            summary["blank_lines"] += metrics["blank_lines"]
            summary["functions"] += metrics["functions"]
            summary["classes"] += metrics["classes"]
            summary["async_functions"] += metrics["async_functions"]

        return summary

    def print_report(self) -> None:
        """Prints a professional, human-readable summary report to the console."""
        summary = self.generate_summary()

        print("\n" + "=" * 50)
        print(" 📊 Codemetrics Project Analysis Report")
        print("=" * 50)
        print(f" Target Directory : {self.root_dir}")
        print(f" Analyzed Files   : {summary['total_files']}")
        print("-" * 50)
        print(" 📈 Line Counts:")
        print(f"   - Total Lines  : {summary['total_lines']:,}")
        print(f"   - Code Lines   : {summary['code_lines']:,}")
        print(f"   - Comments     : {summary['comment_lines']:,}")
        print(f"   - Blank Lines  : {summary['blank_lines']:,}")
        print("-" * 50)
        print(" 🏗️  Structural Metrics:")
        print(f"   - Classes      : {summary['classes']:,}")
        print(f"   - Functions    : {summary['functions']:,}")
        print(f"   - Async Funcs  : {summary['async_functions']:,}")
        print("=" * 50)

        if self.file_metrics:
            print("\n 📄 File Breakdown:")
            for m in self.file_metrics:
                rel_path = Path(m["file_path"]).relative_to(self.root_dir) if Path(m["file_path"]).is_relative_to(self.root_dir) else m["file_path"]
                print(f"   • {rel_path} -> {m['code_lines']} loc, {m['functions']} funcs, {m['classes']} classes")
        print()