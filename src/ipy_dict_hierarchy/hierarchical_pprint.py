# ------------------------------------------------------------------------------ #
# @Author:        F. Paul Spitzner
# @Email:         paul.spitzner@ds.mpg.de
# @Created:       2022-07-26 20:45:38
# @Last Modified: 2022-08-02 14:00:52
# ------------------------------------------------------------------------------ #
# this provides a pretty print for nested dictionaries.
# ------------------------------------------------------------------------------ #

# TODO: check for numpy, then again, when has it ever not been installed?
from numbers import Number
from numpy import ndarray as np_ndarray
from numpy import bytes_ as np_bytes_

try:
    from h5py import Dataset as h5py_Dataset
    from h5py import Group as h5py_Group
    from h5py import File as h5py_File

    _h5_installed = True
except ImportError:
    _h5_installed = False


def plain_text(obj, p=None, cycle=False):
    """
    See https://ipython.readthedocs.io/en/stable/api/generated/IPython.lib.pretty.html

    # Example
    ```
    from .hierarchical_pprint import plain_text
    formatter = get_ipython().display_formatter.formatters["text/plain"]
    formatter.for_type(dict, plain_text)
    formatter.for_type_by_name('benedict.dicts', 'benedict', plain_text)
    formatter.for_type_by_name('h5py._hl.files', 'File', plain_text)
    formatter.for_type_by_name('h5py._hl.group', 'Group', plain_text)
    ```

    Then, printing a nested dict should look like this:
    ```
    └── profile
          ├── firstname ................. str  Fabio
          └── lastname .................. str  Caccamo
    ```
    """

    try:
        width = p.max_width - 3
    except:
        width = 79
    fill = "."

    if cycle:
        p.text(f"{type(obj)}")
    else:
        try:
            # first, get a decent one line description of the object
            try:
                if _h5_installed and "h5py" in str(type(obj)):
                    p.text(f"{obj}")
                else:
                    p.text(f"{type(obj)}")
            except:
                p.text(f"{type(obj)}")
            p.breakable()

            # this gets us the tree as a dict of equally long lists
            rt = _recursive_tree(obj)
            num_lines = len(rt["varname"])
            for l in range(0, num_lines):
                # pcs and scs are padding and split characters
                left = f"{rt['pcs'][l]}{rt['scs'][l]}{rt['varname'][l]}"
                right = f"{rt['vartype'][l]}"
                # dicts dont have a vartype, unfold, dont print fill characters
                ws = " " if rt["vartype"][l] == "" else fill
                p.text(f"{left} {ws*(width-len(left)-len(right))} {right}")
                if len(rt["varval"][l]) > 0:
                    p.text(f"  {rt['varval'][l]}")
                if l < num_lines - 1:
                    p.breakable()
        except AttributeError:
            pass


def _recursive_tree(d, t=None, depth=0):
    """
    helper to call recursively and build the tree structure of the content
    # Parameters
    d : dict, current dict level
    t : dict, current tree structure
    depth : int, current depth
    max_els : int, maximum number of elements per hierarchy level
    """

    if t is None:
        # these are all flat lists of the same length
        # scs are split characters
        # pcs are padding
        t = {key: [] for key in ["pcs", "scs", "varname", "varval", "vartype"]}
        t["prev_pc"] = ""

    for vdx, var in enumerate(d.keys()):
        # lets have a hard-coded limit so that this cannot blow up too much
        if len(t["pcs"]) > 5_000:
            return t

        if vdx < len(d.keys()) - 1:
            sc = "├── "
            pc = "│   "
        else:
            sc = "└── "
            pc = "    "

        t["pcs"].append(t["prev_pc"])
        t["scs"].append(sc)
        t["varname"].append(var)

        if isinstance(d[var], dict) or (
            _h5_installed
            # also expand hdf5 groups but not references to files
            and (isinstance(d[var], h5py_Group) and not isinstance(d[var], h5py_File))
        ):
            # get all content of the dict, while incrementing the padding `pc`
            t["vartype"].append("")
            t["varval"].append("")
            # further indent the prefix
            t["prev_pc"] += pc
            _recursive_tree(d[var], t, depth + 1)
            # unindent the prefix
            t["prev_pc"] = t["prev_pc"][0:-4]
        else:
            # extract type and certain variables
            t["vartype"].append(f"{d[var].__class__.__name__}")

            # number
            if isinstance(d[var], Number):
                t["varval"].append(str(d[var]))

            # numpy byte strings
            elif isinstance(d[var], np_bytes_):
                string = d[var].decode("UTF-8").replace("\n", " ")
                if len(string) > 14:
                    string = f"{string:.11s}..."
                t["varval"].append(string)

            # base strings
            elif isinstance(d[var], str):
                string = d[var].replace("\n", " ")
                if len(string) > 14:
                    string = f"{string:.11s}..."
                t["varval"].append(string)

            # numpy arrays, print shape
            elif isinstance(d[var], np_ndarray):
                t["varval"].append(f"{d[var].shape}")

            # list, print length
            elif isinstance(d[var], list):
                t["varval"].append(f"({len(d[var])})")

            # hdf5 datset
            elif _h5_installed and isinstance(d[var], h5py_Dataset):
                try:
                    # this will throw an exception if file is closed
                    d[var].file
                    t["varval"].append(f"{d[var].shape}")
                except ValueError:
                    t["varval"].append(f"(file closed)")

            # unknown
            else:
                t["varval"].append("")

    return t
