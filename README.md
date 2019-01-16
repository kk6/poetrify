# Poetrify

Pipfile to pyproject.toml for Poetry.

```
$ git clone https://github.com/kk6/poetrify.git
$ cd poetrify
$ poetry install
$ poetry run poetrify generate -w /path/to/workspace
```

or

```
$ git clone https://github.com/kk6/poetrify.git
$ cd poetrify
$ poetry build
$ pip install --user ./dist/poetrify-0.2.0-py3-none-any.whl
$ cd path/to/workspace
$ poetrify generate
```

## required

`poetry` command

See: https://poetry.eustace.io/docs/#installation
