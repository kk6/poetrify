from pathlib import Path

import pytest
import responses
from poetrify.files import Pipfile
from poetrify.files import RequirementsTxt


@pytest.fixture()
def fixture():
    return Path(__file__).parent / "fixtures" / "Pipfile"


@pytest.fixture()
def pypi_json():
    return Path(__file__).parent / "fixtures" / "pypi" / "pytest.json"


def test_pipfile(fixture):
    pipfile = Pipfile(fixture)
    assert pipfile.path.name == "Pipfile"
    assert pipfile.packages == ["scrapy", "beautifulsoup4"]
    assert pipfile.dev_packages == ["pytest"]


def test_pipfile_if_not_exists():
    with pytest.raises(FileNotFoundError):
        Pipfile(Path("./foo"))


def test_empty_pipfile(fixture):
    pipfile = Pipfile(fixture.with_name("EmptyPipfile"))
    assert pipfile.packages == []
    assert pipfile.dev_packages == []


@responses.activate
def test_requires(fixture, pypi_json):
    requires = RequirementsTxt(fixture.with_name("requirements.txt"))
    for name in requires.all_packages:
        with open(pypi_json.with_name(f"{name}.json")) as f:
            responses.add(
                responses.GET,
                f"https://pypi.org/pypi/{name}/json",
                body=f.read(),
                status=200,
                content_type="application/json",
            )
    assert requires.path.name == "requirements.txt"
    assert requires.packages == ["django", "pytest"]
    assert requires.dev_packages == []


def test_requirements_if_not_exists():
    with pytest.raises(FileNotFoundError):
        RequirementsTxt(Path("./bar"))
