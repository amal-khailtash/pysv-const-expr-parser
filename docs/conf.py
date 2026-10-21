"""Sphinx configuration for the SLY expression parser."""

from pathlib import Path
import tomllib

metadata = tomllib.loads((Path(__file__).resolve().parents[1] / "pyproject.toml").read_text())
project = "pysv-const-expr-parser"
author = "Amal Khailtash"
copyright = "2026, Amal Khailtash"
version = release = metadata["project"]["version"]
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.mathjax", "myst_parser"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
exclude_patterns = ["_build"]
html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 4, "collapse_navigation": False}
