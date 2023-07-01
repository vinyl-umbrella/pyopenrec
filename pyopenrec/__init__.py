"""
# pyopenrec
[OPENREC.tv](https://www.openrec.tv) API wrapper for Python.

## Installation
```sh
pip install git+https://github.com/vinyl-umbrella/pyopenrec
```

## Usage
### Basic
```py
from pyopenrec import Openrec


openrec = Openrec("EMAIL", "PASSWORD")
user = openrec.me()
print(user.id)
```

### More
There are more programs [here](https://github.com/vinyl-umbrella/pyopenrec/tree/main/sample)

[OPENREC.tv API LIST](https://futon.manuke.dev/openrecapi)
"""

__title__ = "pyopenrec"
__author__ = "vinyl-umbrella"
__license__ = "MIT"
__version__ = "1.0.0"


from .openrec import Openrec
from .util.enums import *
