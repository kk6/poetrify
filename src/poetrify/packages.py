import re
from dataclasses import dataclass
from dataclasses import field
from typing import List


@dataclass
class Package:
    name: str
    extras: List[str] = field(default_factory=list)

    def __str__(self):
        if self.extras:
            extras = ",".join(self.extras)
            return "".join([self.name, f"[{extras}]"])
        return self.name


def setup_package(s):
    """Setup Package data

    Currently, only deal with name and extras.

    See: https://pip.pypa.io/en/stable/reference/pip_install/#examples

    """
    m = re.search(r"\[.*]", s)
    if m:
        package = Package(name=s[: m.start()], extras=m.group(0)[1:-1].split(","))
    else:
        package = Package(name=s)
    return package
