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

<!-- python3 setup.py sdist; pip install dist/pyopenrec-0.0.4.tar.gz -->
### More Samples
There are more programs [here](https://github.com/vinyl-umbrella/pyopenrec/tree/main/sample)

[OPENREC.tv API LIST](https://futonchan-openchat.web.app/api)

## Dev
```sh
# install dev dependencies
pipenv install --dev
# Spawns a shell within the virtualenv
pipenv shell
# If you add some packages, add it to the requirements.txt
pipenv lock -r > requirements.txt
# install pyopenrec to virtual environment
pipenv install -e .
# lint & test
pipenv run lint
pipenv run test
```

## Contributing
1. Fork this repository
2. Clone your fork
3. Create your feature branch
4. Commit your changes
5. Push to the branch
6. Submit a pull request
