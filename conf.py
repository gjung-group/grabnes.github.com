# Configuration file for the Sphinx documentation builder.
#
# For the full list of options:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------

project = "GRABNES"
copyright = "2022-2026, Nicolas Leconte and the GRABNES developers"
author = "Nicolas Leconte"

# The full version, including alpha/beta/rc tags
release = "0.1"

# -- General configuration ---------------------------------------------------

extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
    "amsmath",
]

templates_path = []

# The repository root is the Sphinx source directory, so everything that is
# not website content must be excluded: build output, the README/AGENTS docs,
# and the old (2022) sphinx tree kept for reference until migration ends.
exclude_patterns = [
    "_build",
    "public",
    ".venv/*",
    "grabnes/*",
    "README.md",
    "AGENTS.md",
    # README.md files inside downloadable example folders are data, not pages
    "assets/downloads/**",
    "Thumbs.db",
    ".DS_Store",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "furo"
html_title = "GRABNES documentation"
# assets/ holds images, sample inputs and static files; its static/ subfolder
# is served under _static/ by Sphinx.
html_static_path = ["assets/static"]
html_css_files = ["grabnes.css"]
html_logo = "assets/static/logo1.png"
html_favicon = "assets/static/logo-icon.png"

html_theme_options = {}

# External links that should not be checked during builds
nitpick_ignore = []

# -- Custom directives ---------------------------------------------------------
# {task}  : exercise/exercise box used in the tutorials
# {todo}  : work-in-progress marker
# Both render as titled admonitions (styled in assets/static/grabnes.css).

from docutils import nodes
from docutils.parsers.rst import Directive


class _TitledAdmonition(Directive):
    has_content = True
    name = ""

    def run(self):
        node = nodes.admonition(classes=[self.name])
        node += nodes.title(self.name.title(), self.name.title())
        self.state.nested_parse(self.content, self.content_offset, node)
        return [node]


class Task(_TitledAdmonition):
    name = "task"


class Todo(_TitledAdmonition):
    name = "todo"


def setup(app):
    app.add_directive("task", Task)
    app.add_directive("todo", Todo)
