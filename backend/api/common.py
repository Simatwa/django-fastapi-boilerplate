"""Shared variables"""

from pathlib import Path

api_module_path = Path(__file__).parent

api_description = api_module_path.joinpath("README.md").read_text()
