# ------------------------------------------------------------------------------ #
# @Author:        F. Paul Spitzner
# @Email:         paul.spitzner@ds.mpg.de
# @Created:       2022-07-26 20:10:12
# @Last Modified: 2022-08-02 22:46:43
# ------------------------------------------------------------------------------ #
# This implements tab completion for nested dictionaries
#
# TODOS:
# - make our hook invoke before the default. this is relevant when completing `foo[`
#   currently, in this case, shows at the end of a long list, so wont be seen.
# - add the type hint for currently selected completion. I do not know how to do this.
#   currently yields `<unknown>`. maybe infers type the returned list items?
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

from IPython.core.error import TryNext


_re_obj_match = re.compile(r"(?:.*\=)?(.+?)(?:\[)")
_re_item_match = re.compile(r"""(?:.*\=)?(.*)\[(?P<s>['|"])(?!.*(?P=s))(.*)$""")
_re_word_match = re.compile(r"\w+")
_re_closed_match = re.compile(r"\w+(\"|\')$")
_re_open_match = re.compile(r"\[")

def _completer(self, event) -> list[str]:
    """
    Completer function to be loaded into IPython.
    Needs to return a list of possible completions for the current line.
    Raise `TryNext` to try the next completer.
    """

    try:
        # lets use event.text_until_cursor instead of event.line
        # so completion works not just at the end of the line
        text = event.text_until_cursor
        # text = event.line

        # if the string is closed e.g. my_dict['search' we just want to close the brace
        if len(re.findall(_re_closed_match, text)) > 0:
            return [']']

        # depending on what we are completing, we need to prepend to all suggested keys
        prefix = ""

        # split the text into the base and the item
        re_split = _re_item_match.split(text)

        # workarounds:
        # our _re_item_match registers, but cannot split when ending in [ or ]
        if len(re_split) == 1:

            if re_split[0].endswith("]"):
                # completing another level of a dict
                base = re_split[0]
                item = ""
                prefix = '["'
            else:
                # get the last position of an opening bracket [. no index error
                # should not occur, 'cos our completer does not fire on `foo`, but `foo[`
                last_br_pos = [f.start() for f in re.finditer(_re_open_match, text)][-1]

                # everything before the last bracket
                base = text[:last_br_pos]
                try:
                    # assuming after the opening bracket there is a key
                    item = re.findall(_re_word_match, text[last_br_pos:])[0]
                except IndexError:
                    item = ''

                # the default closing suffix is "] so lets add the right prefix.
                prefix = '"'

        else:
            # default, foo["ba
            base, item = re_split[1:4:2]

    except Exception as e:
        return []

    # `base` should now contain all chars in the current line up to the
    # dict instance where tab completeion was invoked e.g.
    # some_func(my_dict["search    ->    some_func(my_dict["
    # my_dict["search              ->    my_dict
    # `item` is the part of the line after the last `["` -> "search"

    # we also want to be able to complete when passing a dict as an
    # argument to a function. then a "(" will be in `base`
    if "(" in base:
        try:
            base = base.split("(")[-1]
        except Exception as e:
            raise TryNext

    # Depending on opening chars, we have different closing and separation strings.
    cls_str = '"]'
    sep_str = '"]["'
    last_pos = -1

    for match in re.finditer('\["', text):
        pos = match.start()
        if pos > last_pos:
            last_pos = pos
    for match in re.finditer("\['", text):
        pos = match.start()
        if pos > last_pos:
            last_pos = pos
            cls_str = "']"
            sep_str = "']['"
            # maybe we have to update the prefix again :/
            if prefix == '["':
                prefix = "['"
            break

    # get the instance of the dict-like object
    try:
        # older versions of IPython:
        obj = eval(base, self.shell.user_ns)
    except AttributeError:
        # as of IPython-1.0:
        obj = eval(base, self.user_ns)


    keys = _get_keys(obj)
    if keys is None:
        # object we are completing is not dict-like
        raise TryNext

    # filter by the typed key we are trying to complete
    keys = [k for k in keys if k[0:len(item)] == item]

    # dict was empty
    if len(keys) == 0:
        return []

    # peek ahead one layer, but show top-level keys first
    peeked_top_level = []
    peeked_sec_level = []
    for key in keys:
        # suggest to close top level, and also have half-closed lower level.
        peeked_top_level.append(prefix + key + cls_str)
        extra_keys = _get_keys(obj[key])
        if extra_keys is not None:
            peeked_sec_level.extend([prefix + key + sep_str + ek for ek in extra_keys])

    return peeked_top_level + peeked_sec_level


def _get_keys(obj):
    """
    Return the _dict like_ keys if present, else returns an empty list.
    """
    try:
        return obj.keys()
    except AttributeError:
        return None

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
                "complete_command", _completer, re_key=r"(?:.*\=)?(.+?)\[",
            )

    raise RuntimeError("Completer must be enabled in active ipython session")
