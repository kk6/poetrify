from pathlib import Path

import pytest
import requests
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
    for p in requires.all_packages:
        with open(pypi_json.with_name(f"{p.name}.json")) as f:
            responses.add(
                responses.GET,
                f"https://pypi.org/pypi/{p.name}/json",
                body=f.read(),
                status=200,
                content_type="application/json",
            )
    assert requires.path.name == "requirements.txt"
    assert requires.packages == ["adb-shell", "django", "pytest"]
    assert requires.dev_packages == []


@responses.activate
def test_requires_with_non_exists_package(fixture, pypi_json):
    responses.add(
        responses.GET,
        f"https://pypi.org/pypi/djangodjango/json",
        body="",
        status=404,
        content_type="text/html",
    )
    requires = RequirementsTxt(fixture.with_name("non_exists_requirements.txt"))
    with pytest.raises(requests.exceptions.HTTPError):
        requires.packages


def test_requirements_if_not_exists():
    with pytest.raises(FileNotFoundError):
        RequirementsTxt(Path("./bar"))


def test_various_symbols_with_versions(fixture):
    pipfile = RequirementsTxt(fixture.with_name("various_symbols.txt"))
    assert [str(p) for p in pipfile.all_packages] == [
        "nose",
        "nose-cov",
        "beautifulsoup4",
        "docopt",
        "keyring",
        "coverage",
        "mopidy-dirble",
        "rejected",
        "green",
    ]
