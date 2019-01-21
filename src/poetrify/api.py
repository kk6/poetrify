import shlex

import licensename

from .files import get_requires
from .files import Pipfile
from .files import RequirementsTxt


def generate_init_cmd(src):
    """
    Generate command string to pass to poetry

    :param str src: Source file name.
    :return: Generated command for 'poetry init' .
    :rtype: str

    """
    if src == "Pipfile":
        src = Pipfile(src)
    else:
        src = RequirementsTxt(src)
    try:
        packages, dev_packages = get_requires(src)
    except FileNotFoundError:
        return

    cmd = ["poetry", "init"]

    for package in packages:
        cmd.append(f"--dependency={shlex.quote(package)}")

    for package in dev_packages:
        cmd.append(f"--dev-dependency={shlex.quote(package)}")

    try:
        license_name = licensename.from_file("LICENSE")
    except FileNotFoundError:
        license_name = ""
    else:
        if license_name is None:
            license_name = ""
    if license_name:
        cmd.append(f"--license={license_name}")

    return " ".join(cmd)
