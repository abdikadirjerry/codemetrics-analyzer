"""
AST-based analyzer for Python source code files.
Extracts metrics such as lines of code, function definitions, class definitions,
and docstring presence without executing the target code.
"""

import ast
from pathlib import Path
from typing import Dict, Any


class ASTAnalyzer:
    """Analyzes a single Python file using Python's built-in AST module."""

    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)

    def analyze(self) -> Dict[str, Any]:
        """Reads and parses the Python file, returning a dictionary of metrics."""
        metrics = {
            "file_path": str(self.file_path),
            "total_lines": 0,
            "code_lines": 0,
            "comment_lines": 0,
            "blank_lines": 0,
            "functions": 0,
            "classes": 0,
            "async_functions": 0,
            "has_module_docstring": False,
        }

        if not self.file_path.exists():
            return metrics

        try:
            source_code = self.file_path.read_text(encoding="utf-8")
        except Exception:
            # Fallback for encoding issues or read errors
            return metrics

        # Line-by-line metrics calculation
        lines = source_code.splitlines()
        metrics["total_lines"] = len(lines)

        for line in lines:
            stripped = line.strip()
            if not stripped:
                metrics["blank_lines"] += 1
            elif stripped.startswith("#"):
                metrics["comment_lines"] += 1
            else:
                metrics["code_lines"] += 1

        # AST-based structural parsing
        try:
            tree = ast.parse(source_code, filename=str(self.file_path))
        except SyntaxError:
            # If the file has invalid syntax, return line counts only
            return metrics

        # Check for module-level docstring
        if (
            tree.body
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)
            and isinstance(tree.body[0].value.value, str)
        ):
            metrics["has_module_docstring"] = True

        # Walk the AST tree to count classes and functions
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                metrics["classes"] += 1
            elif isinstance(node, ast.FunctionDef):
                metrics["functions"] += 1
            elif isinstance(node, ast.AsyncFunctionDef):
                metrics["async_functions"] += 1

        return metrics