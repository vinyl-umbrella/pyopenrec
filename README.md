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


openrec = Openrec("YOUR_EMAIL", "YOUR_PASSWORD")
user = openrec.me()
print(user.id)
```

<!-- python3 setup.py sdist; pip install dist/pyopenrec-0.0.5.tar.gz -->
### More Samples
There are more programs [here](https://github.com/vinyl-umbrella/pyopenrec/tree/main/sample)

[OPENREC.tv API LIST](https://futon.manuke.dev/openrecapi)

## Dev
```sh
# install dev dependencies
pipenv install --dev
# Spawns a shell within the virtualenv
pipenv shell
# If you add some packages, add it to the requirements.txt
pip freeze > requirements.txt
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
