# ------------------------------------------------------------------------------ #
# @Author:        F. Paul Spitzner
# @Email:         paul.spitzner@ds.mpg.de
# @Created:       2022-07-26 20:10:12
# @Last Modified: 2022-08-02 13:43:34
# ------------------------------------------------------------------------------ #
# This implements tab completion for nested dictionaries (for now only benedict)
# https://github.com/fabiocaccamo/python-benedict
# ------------------------------------------------------------------------------ #
# This file is reworked from h5py, a low-level Python interface to the HDF5 library.
#
# Originally contributed by Darren Dale under BSD license.
# Copyright (C) 2009 Darren Dale
# http://h5py.org
# ------------------------------------------------------------------------------ #


import re
import readline
import re

try:
    from benedict import benedict
except ImportError:
    # this only makes sense if benedict is installed.
    # we again check below
    pass

from IPython.core.error import TryNext


_re_item_match = re.compile(r"""(?:.*\=)?(.*)\[(?P<s>['|"])(?!.*(?P=s))(.*)$""")


def _completer(self, event):
    """Completer function to be loaded into IPython"""
    try:
        base, item = _re_item_match.split(event.line)[1:4:2]
    except ValueError:
        raise TryNext

    # `base` should now contain all chars in the current line up to the
    # benedict instance where tab completeion was invoked
    # we also want to be able to complete when passing a benedict as an
    # argument to a function. then a "(" will be in `base`
    if "(" in base:
        try:
            base = base.split("(")[-1]
            if not isinstance(self._ofind(base).get("obj"), benedict):
                raise ValueError
        except Exception as e:
            return []

    # if completing a benedict, get the separator to split paths, else skip completion
    if isinstance(self._ofind(base).get("obj"), benedict):
        try:
            # older versions of IPython:
            obj = eval(base, self.shell.user_ns)
        except AttributeError:
            # as of IPython-1.0:
            obj = eval(base, self.user_ns)
        sep = obj.keypath_separator
    else:
        raise TryNext

    # per default, posixpath uses '/' as a sperator
    # path, _ = posixpath.split(item)
    # we want: empty string when no sep, else everything before the last sep.
    path = ""
    if len(item) >= 1 and item[0] == sep:
        # this is not great, keys without a name are problematic
        return []
    elif len(item) > 1:
        if item[-1] == sep:
            path = item[:-1]
        else:
            path = sep.join(item.split(sep)[:-1])

    # maybe it is convenient to close the brackets.
    # ideally this would not be shown in the preview, but no clue how to do this
    term = ""
    if re.search('\["', event.line):
        term = '"]'
    elif re.search("\['", event.line):
        term = "']"

    try:
        if len(path) > 0:
            try:
                items = (sep.join([path, name]) for name in obj[path].keys())
            except KeyError:
                return []
        else:
            items = obj.keys()
    except AttributeError:
        return []

    items = [
        item + sep if isinstance(obj[item], benedict) else item + term for item in items
    ]
    items = list(items)
    readline.set_completer_delims(" \t\n`!@#$^&*()=+[{]}\\|;:'\",<>?")

    return [i for i in items if i[: len(item)] == item]




def enable_tab_completion(ipython):
    """
    Call this from an interactive IPython session to enable tab-completion
    of nested benedict keys.
    """
    import sys

    # if benedict is not installed, the current implementation is useless.
    if not "benedict" in sys.modules:
        return

    if "IPython" in sys.modules:
        ip_running = False
        try:
            from IPython.core.interactiveshell import InteractiveShell

            ip_running = InteractiveShell.initialized()
        except ImportError:
            # support <ipython-0.11
            from IPython import ipapi as _ipapi

            ip_running = _ipapi.get() is not None
        except Exception:
            pass
        if ip_running:
            return ipython.set_hook(
                "complete_command", _completer, re_key=r"(?:.*\=)?(.+?)\["
            )

    raise RuntimeError("Completer must be enabled in active ipython session")
