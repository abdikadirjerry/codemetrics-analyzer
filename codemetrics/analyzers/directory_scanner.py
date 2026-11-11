"""
Directory scanner to recursively find and analyze Python files in a project.
"""

from pathlib import Path
from typing import List, Dict, Any
from codemetrics.analyzers.ast_analyzer import ASTAnalyzer


class DirectoryScanner:
    """Scans directories for Python files and aggregates code metrics."""

    IGNORED_DIRS = {
        "__pycache__",
        "venv",
        "env",
        ".env",
        ".git",
        ".pytest_cache",
        "build",
        "dist",
        ".idea",
        ".vscode",
    }

    def __init__(self, root_dir: Path):
        self.root_dir = Path(root_dir).resolve()

    def scan(self) -> List[Dict[str, Any]]:
        """Recursively scans the root directory for Python files and analyzes them."""
        results = []

        if not self.root_dir.exists() or not self.root_dir.is_dir():
            return results

        for path in self.root_dir.rglob("*.py"):
            # Skip if any parent folder is in the ignored list
            if any(part in self.IGNORED_DIRS for part in path.parts):
                continue

            analyzer = ASTAnalyzer(path)
            file_metrics = analyzer.analyze()
            results.append(file_metrics)

        return results