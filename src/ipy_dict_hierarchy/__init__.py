from .hierarchical_pprint import plain_text
from .tab_completion_dict import enable_tab_completion as enable_tab_dict
from .tab_completion_benedict import enable_tab_completion as enable_tab_benedict

def load_ipython_extension(ipython=None):

    if ipython is None:
        from IPython import get_ipython
        ipython = get_ipython()

    enable_tab_benedict(ipython)
    enable_tab_dict(ipython)


    # plain text formatting
    formatter = ipython.display_formatter.formatters["text/plain"]
    formatter.for_type(dict, plain_text)
    formatter.for_type_by_name('benedict.dicts', 'benedict', plain_text)
    formatter.for_type_by_name('h5py._hl.files', 'File', plain_text)
    formatter.for_type_by_name('h5py._hl.group', 'Group', plain_text)
