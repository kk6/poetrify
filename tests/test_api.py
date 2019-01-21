import pytest
from poetrify.api import generate_init_cmd


def test_pipfile_not_found():
    with pytest.raises(FileNotFoundError):
        generate_init_cmd("Pipfile")


def test_requirements_not_found():
    with pytest.raises(FileNotFoundError):
        generate_init_cmd("requirements.txt")
