# -- ipynb.py --

"""Jupyter ipynb document format filter."""

from .. import filters
import codecs
import markdown
import nbformat

class IpynbFilter(filters.Filter):
    """Spellchecking Jupyter notebook ipynb cells."""

    def __init__(self, options, default_encoding='utf-8'):
        """Initialization."""

        super().__init__(options, default_encoding)

    def get_default_config(self):
        """Get default configuration."""

        return {
            'cell_type': 'markdown', # Cell type to filter
            'language': '', # This is the code language for the notebook
            # Optionally specify whether code cell outputs should be spell checked
            'output': False, # TO DO
            # Allow tagged cells to be excluded
            'tags-exclude': ['code-fails']
        }

    def setup(self):
        """Setup."""

        self.cell_type = self.config['cell_type'] if self.config['cell_type'] in ['markdown', 'code'] else 'markdown'
        self.language = self.config['language'].upper()
        self.tags_exclude = set(self.config['tags-exclude'])

    def filter(self, source_file, encoding):  # noqa A001
        """Parse ipynb file."""

        nb = nbformat.read(source_file, as_version=4)
        self.lang = nb.metadata['language_info']['name'].upper() if 'language_info' in nb.metadata else None
        # Allow possibility to ignore code cells if language is set and
        # does not match parameter specified language? E.g. in extreme case:
        #if self.cell_type=='code' and self.config['language'] and self.config['language']!=self.lang:
        #    nb=nbformat.v4.new_notebook()
        # Or maybe better to just exclude code cells and retain other cells?

        encoding = 'utf-8'

        return [filters.SourceText(self._filter(nb), source_file, encoding, 'ipynb')]

    def _filter(self, nb):
        """Filter ipynb."""

        text_list = []
        for cell in nb.cells:
            if 'tags' in cell['metadata'] and \
                set(cell['metadata']['tags']).intersection(self.tags_exclude):
                continue
            if cell['cell_type']==self.cell_type:
                text_list.append(cell['source'])

        return '\n'.join(text_list)

    def sfilter(self, source):
        """Filter."""

        return [filters.SourceText(self._filter(source.text), source.context, source.encoding, 'ipynb')]


def get_plugin():
    """Return the filter."""

    return IpynbFilter
