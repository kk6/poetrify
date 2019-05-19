from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

import tomlkit

from .http import fetch_package_json


@dataclass
class Pipfile:
    path: Path
    body: dict = field(init=False)

    def __post_init__(self):
        with open(self.path) as f:
            self.body = tomlkit.parse(f.read())

    @property
    def packages(self):
        try:
            return list(self.body["packages"].keys())
        except tomlkit.exceptions.NonExistentKey:
            return []

    @property
    def dev_packages(self):
        try:
            return list(self.body["dev-packages"].keys())
        except tomlkit.exceptions.NonExistentKey:
            return []


@dataclass
class RequirementsTxt:
    path: Path
    body: list = field(init=False)
    _decent_packages: list = None

    def __post_init__(self):
        with open(self.path) as f:
            self.body = [l.strip() for l in f.readlines()]

    @property
    def all_packages(self):
        return find_packages(self.body)

    @property
    def packages(self):
        if self._decent_packages is None:
            self._decent_packages = find_descendant_packages(self.all_packages)
        return self._decent_packages

    @property
    def dev_packages(self):
        return []


def find_packages(requirements_txt_lines):
    version_specifiers = ["~=", "==", "!=", "<=", ">=", ">", "<", "==="]
    packages = []
    for line in requirements_txt_lines:

        if line.startswith("#"):
            continue

        if "egg=" in line:
            continue

        if "http" in line:
            continue

        if "-r" in line:
            continue

        if ".whl" in line:
            continue

        package = line
        for s in version_specifiers:
            if s in line:
                package = line.split(s)[0]
                break
        packages.append(package.lower().strip())
    return packages


def find_descendant_packages(package_names):
    def get_requires_dist(json_):
        parents = []
        requires_dist = json_["info"].get("requires_dist")

        if not requires_dist:
            return parents

        for dist in requires_dist:
            if "extra ==" in dist:
                continue
            dist_name = dist.split(" ")[0]
            parents.append(dist_name)

        return parents

    all_requires = []
    for name in package_names:
        j = fetch_package_json(name)
        requires = get_requires_dist(j)
        all_requires.extend(requires)

    package_name_set = {p.lower() for p in package_names}
    requires_set = {r.lower() for r in all_requires}
    return sorted(package_name_set - requires_set)
