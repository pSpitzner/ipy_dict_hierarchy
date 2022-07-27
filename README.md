# Utilities to work with hierarchical dictionaries

When working with simulation data or simply creating data visualizations, I often find myself wishing for a _readable_ representation of a nested structure. In python these are typically `dicts` containing `dicts` or something alike.

So, this is where this ipython extension comes in:

* Tab completion across levels for [benedicts](https://github.com/fabiocaccamo/python-benedict) (plain dicts asap)

![tab_completion](https://media.giphy.com/media/Ry3Zh1jH2fOVg9nbx9/giphy.gif)

* Pretty printing dictionaries and similar types in a tree-like structure.

```
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
```
pip install python-benedict
pip install h5py
```

Required
```
pip install ipy_dict_hierarchy
```

In jupyter or ipython, to load manually
```
%load_ext ipy_dict_hierarchy
```

