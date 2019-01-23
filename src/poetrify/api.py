import shlex

import licensename

from .files import Pipfile
from .files import RequirementsTxt


def build_poetry_init_command(src):
    """
    Make a command for `poetry init`

    :param pathlib.Path src: Source file's Path object.
    :return: Generated command for 'poetry init' .
    :rtype: str

    """
    if src.name == "Pipfile":
        src = Pipfile(src)
    else:
        src = RequirementsTxt(src)

    cmd = ["poetry", "init"]

    for package in src.packages:
        cmd.append(f"--dependency={shlex.quote(package)}")

    for package in src.dev_packages:
        cmd.append(f"--dev-dependency={shlex.quote(package)}")

    try:
        license_name = licensename.from_file("LICENSE") or ""
    except FileNotFoundError:
        license_name = ""
    if license_name:
        cmd.append(f"--license={license_name}")

    return " ".join(cmd)
