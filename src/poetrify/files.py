from dataclasses import dataclass
from dataclasses import field
from functools import singledispatch

import requests
import tomlkit


@dataclass
class Pipfile:
    src: str
    body: dict = field(init=False)

    def __post_init__(self):
        with open(self.src) as f:
            self.body = tomlkit.parse(f.read())

    @property
    def packages(self):
        if self.body:
            return list(self.body["packages"].keys())

    @property
    def dev_packages(self):
        if self.body:
            return list(self.body["dev-packages"].keys())


def find_descendant_packages(package_names):
    requires = []
    for name in package_names:
        r = requests.get(f"https://pypi.org/pypi/{name}/json")
        r.raise_for_status()
        j = r.json()
        requires_dist = j["info"].get("requires_dist")
        if requires_dist:
            for dist in requires_dist:
                if "extra ==" in dist:
                    continue
                dist_name = dist.split(" ")[0]
                requires.append(dist_name)
    package_name_set = {p.lower() for p in package_names}
    requires_set = {r.lower() for r in requires}
    return sorted(package_name_set - requires_set)


@dataclass
class RequirementsTxt:
    src: str
    body: list = field(init=False)
    _decent_packages: list = None

    def __post_init__(self):
        with open(self.src) as f:
            self.body = [l.strip() for l in f.readlines()]

    @property
    def packages(self):
        packages = []
        for line in self.body:

            if "egg=" in line:
                continue

            if "==" in line:
                package = line.split("==")[0]
            else:
                package = line
            packages.append(package)
        return packages

    def get_decent_packages(self):
        if not self._decent_packages:
            self._decent_packages = find_descendant_packages(self.packages)
        return self._decent_packages


@singledispatch
def get_requires(src):
    raise TypeError(f"Unsupported type: {src}")


@get_requires.register(Pipfile)
def get_requires_from_pipfile(src):
    return src.packages, src.dev_packages


@get_requires.register(RequirementsTxt)
def get_requires_from_requirements_txt(src):
    return src.get_decent_packages(), []
