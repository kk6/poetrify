import json
from pathlib import Path

import pytest
import responses
from poetrify.files import get_requires
from poetrify.files import Pipfile
from poetrify.files import RequirementsTxt


@pytest.fixture()
def fixture():
    return Path(__file__).parent / "fixtures" / "Pipfile"


def test_pipfile(fixture):
    src = Pipfile(fixture)
    packages, dev_packages = get_requires(src)
    assert packages == ["scrapy", "beautifulsoup4"]
    assert dev_packages == []


def test_pipfile_if_not_exists():
    with pytest.raises(FileNotFoundError):
        Pipfile("foo")


@responses.activate
def test_requirements(fixture):
    for name in ("django", "pytest"):
        with open(fixture.with_name(f"{name}.json")) as f:
            responses.add(
                responses.GET,
                f"https://pypi.org/pypi/{name}/json",
                body=f.read(),
                status=200,
                content_type="application/json",
            )
    src = RequirementsTxt(fixture.with_name("requirements.txt"))
    packages, dev_packages = get_requires(src)
    assert packages == ["django", "pytest"]
    assert dev_packages == []


def test_requirements_if_not_exists():
    with pytest.raises(FileNotFoundError):
        RequirementsTxt("bar")
