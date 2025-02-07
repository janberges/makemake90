# Configuration file for the Sphinx documentation builder.

# https://www.sphinx-doc.org/en/master/usage/configuration.html

project = 'makemake90'
copyright = '2015-%Y Jan Berges'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'numpydoc',
    'myst_parser',
    ]

html_theme = 'sphinx_rtd_theme'
html_logo = '../logo/makemake90.svg'
html_theme_options = {
    'logo_only': True,
    'style_nav_header_background': 'black',
    }
