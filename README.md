# QtMaterialSymbols
Python Qt wrapper for Material Design icons.

## Description
QtMaterialSymbols enables to use [Material Symbols](https://fonts.google.com/icons) font icons in PySide and PyQt applications.

This project is heavily based on [QtAwesome](https://github.com/spyder-ide/qtawesome).

## Installation
You can install QtMaterialSymbols using pip:

```bash
pip install qtmaterialsymbols
```

## Usage
To use Material Symbols in your PySide or PyQt application, you can simply import the `get_icon` function and use it to create icons for your widgets.:

```python
from qtmaterialsymbols import get_icon

icon = get_icon("settings", color="#ffffff")
button = QtWidgets.QPushButton(icon)
```

Please look into signature of `get_icon` function for more details on available parameters.

At this moment it is not possible to use font axis (outlined, rounded, fill etc.). It is available since Qt 6.7 which might limit the usage.
