"""Shared variables"""

from pathlib import Path

api_module_path = Path(__file__).parent

api_version = (api_module_path.joinpath("VERSION").read_text().strip(),)
api_description = (api_module_path.joinpath("README.md").read_text(),)
