from .tab_completion import enable_tab_completion

def load_ipython_extension(ipython):
    print(ipython)
    enable_tab_completion(ipython)
