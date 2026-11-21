"""Check the greeting and the command line entry point."""

import contextlib
import io
from pathlib import Path
import runpy
import unittest

from app import greet


class TestApp(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet("World"), "Hello, World from Ali Naji!")

    def test_another_name(self):
        self.assertEqual(greet("Jenkins"), "Hello, Jenkins from Ali Naji!")

    def test_empty_name(self):
        self.assertEqual(greet(""), "Hello,  from Ali Naji!")

    def test_command_line(self):
        output = io.StringIO()
        app_path = Path(__file__).resolve().parents[1] / "app.py"
        with contextlib.redirect_stdout(output):
            runpy.run_path(str(app_path), run_name="__main__")
        self.assertEqual(output.getvalue(), "Hello, World from Ali Naji!\n")


if __name__ == "__main__":
    unittest.main()
