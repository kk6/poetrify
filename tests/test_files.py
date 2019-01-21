from poetrify.files import get_requires
from poetrify.files import Pipfile
from poetrify.files import RequirementsTxt


def test_pipfile():
    src = Pipfile("repos/foo/Pipfile")
    packages, dev_packages = get_requires(src)
    assert packages == ["scrapy", "beautifulsoup4"]
    assert dev_packages == []


def test_requirements():
    src = RequirementsTxt("repos/requirements_txt/requirements.txt")
    packages, dev_packages = get_requires(src)
    assert packages == ["django", "pytest"]
    assert dev_packages == []
