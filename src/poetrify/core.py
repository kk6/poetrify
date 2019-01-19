import shlex

import licensename
import tomlkit


def generate_init_cmd():
    """

    :return: Generated command for 'poetry init' .
    :rtype: str

    """
    try:
        with open("Pipfile") as f:
            d = tomlkit.parse(f.read())
    except FileNotFoundError:
        return

    packages = list(d["packages"].keys())
    dev_packages = list(d["dev-packages"].keys())

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
