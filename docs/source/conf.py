# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.

import sys
import os

sys.path.insert(0, os.path.abspath("../"))

# added these imports to work around the issue for autodoc_pydantic not working with multi-level inheritance
# This workaround was suggested here: https://github.com/pydantic/pydantic/discussions/7763
from ochra_common.storage.holder import Holder  # noqa: F401
from ochra_common.storage.vessel import Vessel  # noqa: F401
from ochra_common.equipment.robot import Robot  # noqa: F401
from ochra_common.equipment.mobile_robot import MobileRobot  # noqa: F401

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "OChRA_common"
copyright = "2025, ochra-lab"
author = "stoic-roboticist"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib.autodoc_pydantic"
]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

autoclass_content = "both"
autodoc_typehints = "description"
napoleon_google_docstring = True

autodoc_pydantic_model_show_config_summary = False
autodoc_pydantic_model_show_validator_summary = False
autodoc_pydantic_model_show_validator_members = False
autodoc_pydantic_model_undoc_members = False
autodoc_pydantic_model_show_json = False
