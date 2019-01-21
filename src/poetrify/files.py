from dataclasses import dataclass
from functools import singledispatch

import tomlkit


@dataclass
class Pipfile:
    src: str
    body: dict = None

    def read(self):
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


@dataclass
class RequirementsTxt:
    src: str
    body: list = None

    def read(self):
        with open(self.src) as f:
            self.body = [l.strip() for l in f.readlines()]

    @property
    def packages(self):
        if self.body:
            packages = []
            for line in self.body:
                if "egg=" in line:
                    continue
                elif "==" in line:
                    package = line.split("==")[0]
                else:
                    package = line
                packages.append(package)
            return packages


@singledispatch
def get_requires(src):
    src.read()
    return src.packages, src.dev_packages


@get_requires.register(RequirementsTxt)
def get_requires_from_requirements_txt(src):
    src.read()
    return src.packages, []
