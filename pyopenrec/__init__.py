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
from datetime import datetime
import json
import pyopenrec

openrec = pyopenrec.Openrec()
dt = datetime(2021, 12, 21, 0, 0, 0)
j = openrec.get_comment("n9ze3m2w184", dt, 5)

with open("sample.json", "w") as f:
    json.dump(j, f, indent=2, ensure_ascii=False)
```

### More
There are more programs [here](https://github.com/vinyl-umbrella/pyopenrec/tree/main/sample)

[OPENREC.tv API LIST](https://futonchan-openchat.web.app/api)

"""

from .openrec import *

__version__ = '0.0.3'
