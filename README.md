# Utilities to work with hierarchical dictionaries

When working with simulation data or simply creating data visualizations, I often find myself wishing for a _readable_ representation of a nested structure. In python these are typically `dicts` containing `dicts` or something alike.

So, this is where this ipython extension comes in:

* Tab completion across levels for nested dicts and [benedicts](https://github.com/fabiocaccamo/python-benedict)

![tab_completion](https://media.giphy.com/media/Ry3Zh1jH2fOVg9nbx9/giphy.gif)

* Pretty printing dictionaries and similar types in a tree-like structure.

```python
dict(
    lorem = "ipsum",
    first_level = dict(
        second_level = dict(
            some_entry = 8.15,
            another_entry = [0, 1, 2, 3, 4],
        )

    )
)
```

```
<class 'dict'>
├── lorem .................................... str  ipsum
└── first_level
    └── second_level
        ├── some_entry ..................... float  8.15
        └── another_entry ................... list  (5)
```

## Install

Optional, but recommended
```bash
python -m pip install python-benedict
python -m pip install h5py
```

Required
```bash
python -m pip install ipy_dict_hierarchy
```

In jupyter or ipython, load manually
```ipython
%load_ext ipy_dict_hierarchy
```
or [load by default on startup](https://stackoverflow.com/questions/31872520/ipython-load-extension-automatically-upon-start)

## TODOs

- make our tabcompletion hook invoke before the default. this is relevant when completing `foo[` currently, in this case, our suggestions show at the end of a long list, so wont be seen.
- add the type hint for currently selected completion. I do not know how to do this. currently yields `<unknown>`. maybe infers type the returned list items?
