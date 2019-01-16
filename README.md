# pipenv2poetry

```
$ git clone https://github.com/kk6/pipenv2poetry.git
$ cd pipenv2poetry
$ poetry install
$ poetry run pipenv2poetry generate -w /path/to/workspace
```

or

```
$ git clone https://github.com/kk6/pipenv2poetry.git
$ cd pipenv2poetry
$ poetry build
$ pip install --user ./dist/pipenv2poetry-0.1.0-py3-none-any.whl
$ cd path/to/workspace
$ pipenv2poetry generate
```

## required

`poetry` command

See: https://poetry.eustace.io/docs/#installation
