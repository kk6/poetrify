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
$ pip install --user ./dist/poetrify-0.2.1-py3-none-any.whl
$ cd path/to/workspace
$ poetrify generate
```

## required

- `poetry` command (See: https://poetry.eustace.io/docs/#installation )

- Please delete the existing `.venv` directory. 
If `pipenv` command is still available, it should be deleted with `pipenv - rm`.


I found the following trouble with the latest poetry. If the venv directory already exists when the `init` command is executed, it seems that `JSONDecodeError` occurs when resolving Python version.

```
$ poetry init

This command will guide you through creating your pyproject.toml config.

Package name [foo]:
Version [0.1.0]:
Description []:
Author [kk6 <hiro.ashiya@gmail.com>, n to skip]:
License []:

[JSONDecodeError]
Expecting value: line 1 column 1 (char 0)

init [--name NAME] [--description DESCRIPTION] [--author AUTHOR] [--dependency DEPENDENCY] [--dev-dependency DEV-DEPENDENCY] [-l|--license LICENSE]
```