# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys

sys.path.append("C:\\Users\\kanga\\OneDrive\\College\\RIT\\CAPSTONE\\ChatCSEC\\src")
project = 'ChatCSEC'
copyright = '2024, Brian McNulty, Kyri Christensen, Domenic Lo Iacano, Rich Kleinhenz'
author = 'Brian McNulty, Kyri Christensen, Domenic Lo Iacano, Rich Kleinhenz'
release = '0.2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
  'sphinx.ext.autodoc',
  'sphinx.ext.viewcode',
  'sphinx.ext.napoleon',
  'sphinx.ext.todo',
  "sphinx_rtd_dark_mode"
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv']

todo_include_todos = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output
default_dark_mode = True
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
