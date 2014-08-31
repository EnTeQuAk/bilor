# -*- coding: utf-8 -*-
import os
import pkg_resources

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bilor.conf.development")


try:
    import sphinx_rtd_theme
except ImportError:
    sphinx_rtd_theme = None


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage']

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = u'bilor'
copyright = u'2014, bilor'

dist = pkg_resources.get_distribution('bilor')
version = release = dist.version

exclude_patterns = []

pygments_style = 'sphinx'

if sphinx_rtd_theme:
    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
else:
    html_theme = "default"

html_static_path = ['_static']

htmlhelp_basename = 'bilordoc'

latex_elements = {}

latex_documents = [
    ('index', 'bilor.tex', u'bilor Documentation',
     u'bilor', 'manual'),
]

man_pages = [
    ('index', 'bilor', u'bilor Documentation',
     [u'bilor'], 1)
]

texinfo_documents = [
    ('index', 'bilor', u'bilor Documentation',
     u'bilor', 'bilor', 'Secure password storage',
     'Miscellaneous'),
]

epub_title = u'Bilor - Experimental exception/logging server.'
epub_author = u'Christopher Grebs'
epub_publisher = u'Christopher Grebs'
epub_copyright = u'2014, Christopher Grebs'

intersphinx_mapping = {'http://docs.python.org/': None}
