from pathlib import Path

import pytest
from poetrify.api import build_poetry_init_command


def test_pipfile_not_found():
    with pytest.raises(FileNotFoundError):
        build_poetry_init_command(Path(".") / "NotPipfile")


def test_requirements_not_found():
    with pytest.raises(FileNotFoundError):
        build_poetry_init_command(Path(".") / "not_requirements.txt")
