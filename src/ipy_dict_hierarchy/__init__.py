# from .tab_completion import enable_tab_completion
from .tab_completion_2 import enable_tab_completion
from .hierarchical_pprint import plain_text

def load_ipython_extension(ipython=None):

    if ipython is None:
        from IPython import get_ipython
        ipython = get_ipython()

    enable_tab_completion(ipython)

    # plain text formatting
    formatter = ipython.display_formatter.formatters["text/plain"]
    formatter.for_type(dict, plain_text)
    formatter.for_type_by_name('benedict.dicts', 'benedict', plain_text)
    formatter.for_type_by_name('h5py._hl.files', 'File', plain_text)
    formatter.for_type_by_name('h5py._hl.group', 'Group', plain_text)
