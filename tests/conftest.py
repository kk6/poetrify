import os
from pathlib import Path

import pytest
from cleo import Application, CommandTester

from poetrify.cli import GenerateCommand


@pytest.fixture(scope='function', autouse=True)
def setup_repos(request):
    """Reset current working directory and remove pyproject.toml"""
    starting_directory = Path.cwd()

    test_directory = starting_directory / "tests"
    os.chdir(test_directory)

    def return_to_saved_path():
        os.chdir(starting_directory)

    def remove_toml():
        cwd = Path.cwd()
        if cwd.name == "poetrify":
            f = cwd / "tests" / "repos" / "foo" / "pyproject.toml"
            if f.exists():
                os.remove(f)

    request.addfinalizer(remove_toml)
    request.addfinalizer(return_to_saved_path)


@pytest.fixture
def command_tester_factory():
    def get_command_tester(name):
        application = Application()
        application.add(GenerateCommand())
        command = application.find(name)
        command_tester = CommandTester(command)
        return command_tester
    return get_command_tester
