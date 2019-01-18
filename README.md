# Poetrify

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/kk6/poetrify/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/poetrify.svg?style=flat-square)](https://pypi.python.org/pypi/poetrify)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Installation

Pipfile to pyproject.toml for Poetry.

```
$ pip install poetrify
```

### required

- `poetry` command (See: https://poetry.eustace.io/docs/#installation )

## Usage

```
$ poetrify
Poetrify version 0.2.1

USAGE
  poetrify [-h] [-q] [-v [<...>]] [-V] [--ansi] [--no-ansi] [-n] <command> [<arg1>] ... [<argN>]

ARGUMENTS
  <command>              The command to execute
  <arg>                  The arguments of the command

GLOBAL OPTIONS
  -h (--help)            Display this help message
  -q (--quiet)           Do not output any message
  -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and
                         "-vvv" for debug
  -V (--version)         Display this application version
  --ansi                 Force ANSI output
  --no-ansi              Disable ANSI output
  -n (--no-interaction)  Do not ask any interactive question

AVAILABLE COMMANDS
  completions            Generate completion scripts for your shell.
  generate               Generate pyproject.toml from Pipfile
  help                   Display the manual of a command
```

Example structure::
```
$ tree .
.
├── app.py
├── LICENSE
├── Pipfile
└── Pipfile.lock
```

The `generate` command sets the way for `poetry init`

```
$ poetrify generate
Generated init command:

poetry init --dependency=rauth --dependency=requests --dependency=requests-cache --dependency=furl --dependency=arrow --dependency=pytest --dependency=responses --dev-dependency=pytest --dev-dependency=pytest-cov --dev-dependency=pytest-flake8 --dev-dependency=responses --dev-dependency=pytest-runner --license=MIT

Execute the above command. Also, the following output is due to Poetry.

This command will guide you through creating your pyproject.toml config.

Package name [foo]:
...
```
