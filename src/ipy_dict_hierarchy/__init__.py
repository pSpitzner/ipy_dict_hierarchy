from .tab_completion import enable_tab_completion
from .hierarchical_pprint import plain_text

def load_ipython_extension(ipython=None):

    # fallbacks for ipython
    if ipython is None:
        try:
            # >=ipython-1.0
            from IPython import get_ipython
        except ImportError:
            try:
                # support >=ipython-0.11, <ipython-1.0
                from IPython.core.ipapi import get as get_ipython
            except ImportError:
                # support <ipython-0.11
                from IPython.ipapi import get as get_ipython
        ipython = get_ipython()

    enable_tab_completion(ipython)

    # plain text formatting
    formatter = ipython.display_formatter.formatters["text/plain"]
    formatter.for_type(dict, plain_text)
    formatter.for_type_by_name('benedict.dicts', 'benedict', plain_text)
    formatter.for_type_by_name('h5py._hl.files', 'File', plain_text)
    formatter.for_type_by_name('h5py._hl.group', 'Group', plain_text)
