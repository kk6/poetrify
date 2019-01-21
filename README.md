# Poetrify

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/b6382d985bf745958b70832f6b356615)](https://app.codacy.com/app/hiro.ashiya/poetrify?utm_source=github.com&utm_medium=referral&utm_content=kk6/poetrify&utm_campaign=Badge_Grade_Settings)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://raw.githubusercontent.com/kk6/poetrify/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/poetrify.svg?style=flat-square)](https://pypi.python.org/pypi/poetrify)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Installation

Pipfile or requirements.txt(this is trial) to pyproject.toml for Poetry.

```bash
pip install poetrify
```

### required

`poetry` command (See: <https://poetry.eustace.io/docs/#installatio> )

## Usage

```bash
$ poetrify
Poetrify version 0.3.0

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
  generate               Generate pyproject.toml from the source file
  help                   Display the manual of a command
```

Example structure::

```bash
$ tree .
.
├── app.py
├── LICENSE
├── Pipfile
└── Pipfile.lock
```

The `generate` command sets the way for `poetry init`

```bash
$ poetrify generate
Generated init command:

poetry init --dependency=rauth --dependency=requests --dependency=requests-cache --dependency=furl --dependency=arrow --dependency=pytest --dependency=responses --dev-dependency=pytest --dev-dependency=pytest-cov --dev-dependency=pytest-flake8 --dev-dependency=responses --dev-dependency=pytest-runner --license=MIT

Execute the above command. Also, the following output is due to Poetry.

This command will guide you through creating your pyproject.toml config.

Package name [foo]:
...
```

### Trial

Also supported to requirements.txt on a trial basis.

Please specify `requirements.txt` for`--src` option. The default value of this option is Pipfile.

```bash
$ poetry run pip freeze > requirements.txt

$ cat requirements.txt
aspy.yaml==1.1.1
atomicwrites==1.2.1
attrs==18.2.0
certifi==2018.11.29
cfgv==1.4.0
chardet==3.0.4
cleo==0.7.2
Click==7.0
clikit==0.2.3
coverage==4.5.2
identify==1.1.8
idna==2.8
importlib-metadata==0.8
incremental==17.5.0
Jinja2==2.10
licensename==0.4.2
MarkupSafe==1.1.0
more-itertools==5.0.0
nodeenv==1.3.3
pastel==0.1.0
pluggy==0.8.1
-e git+https://github.com/kk6/poetrify.git@63a861cba868298c896888f5104230c4a00896bb#egg=poetrify
pre-commit==1.14.2
py==1.7.0
pylev==1.3.0
pytest==3.10.1
pytest-cov==2.6.1
PyYAML==3.13
requests==2.21.0
six==1.12.0
toml==0.10.0
tomlkit==0.5.3
towncrier==18.6.0
Unidecode==1.0.23
urllib3==1.24.1
virtualenv==16.2.0
zipp==0.3.3

$ poetry run poetrify generate -d -s requirements.txt
Generated init command:

poetry init --dependency=cleo --dependency=licensename --dependency=pre-commit --dependency=pytest-cov --dependency=requests --dependency=tomlkit --dependency=towncrier --license=MIT
```

As you can see, poetrify extract only descendants packages from all the packages listed in `requirements.txt` and pass only those to poetry. This is to prevent `pyproject.toml` from becoming full of package names.

## Autocompletion

### Description

One can generate a completion script for `poetrify` that is compatible with a given shell. The
script is output on `stdout` allowing one to re-direct the output to the file of their choosing.
Where you place the file will depend on which shell, and which operating system you are using. Your particular
configuration may also determine where these scripts need to be placed.

Here are some common set ups for the three supported shells under Unix and similar operating systems (such as
GNU/Linux).

### BASH

`bash`
Completion files are commonly stored in `/etc/bash_completion.d/`

Run the command:

`poetrify completions bash > /etc/bash_completion.d/poetrify.bash-completion`

This installs the completion script. You may have to log out and log back in to your shell session for the changes to
take effect.

### FISH

Fish completion files are commonly stored in`$HOME/.config/fish/completions`

Run the command:

`poetrify completions fish > ~/.config/fish/completions/poetrify.fish`

This installs the completion script. You may have to log out and log back in to your shell session for the changes to
take effect.

### ZSH

ZSH completions are commonly stored in any directory listed in your `$fpath` variable. To use these
completions, you must either add the generated script to one of those directories, or add your own to this list.

Adding a custom directory is often the safest best if you're unsure of which directory to use. First create the
directory, for this example we'll create a hidden directory inside our `$HOME` directory

`mkdir ~/.zfunc`

Then add the following lines to your `.zshrc` just before `compinit`

`fpath+=~/.zfunc`

Now you can install the completions script using the following command

`poetrify completions zsh > ~/.zfunc/_poetrify`

You must then either log out and log back in, or simply run

`exec zsh`

For the new completions to take affect.

### CUSTOM LOCATIONS

Alternatively, you could save these files to the place of your choosing, such as a custom directory inside your
\$HOME. Doing so will require you to add the proper directives, such as `source`ing inside your login script. Consult
your shells documentation for how to add such directives.
