import os

import pytest


def test_foo_dry_run(command_tester_factory):
    print(os.getcwd())
    command_tester = command_tester_factory("generate")
    with pytest.raises(SystemExit) as pytest_wrapped_exit:
        command_tester.execute("-d -w repos/foo")
    assert pytest_wrapped_exit.type == SystemExit
    assert pytest_wrapped_exit.value.code == os.EX_OK
    assert (
        "poetry init --dependency=scrapy --dependency=beautifulsoup4 --license=MIT"
        in command_tester.io.fetch_output()
    )


def test_foo(command_tester_factory):
    print(os.getcwd())
    command_tester = command_tester_factory("generate")
    command_tester.execute("-w repos/foo")
    assert (
        "poetry init --dependency=scrapy --dependency=beautifulsoup4 --license=MIT"
        in command_tester.io.fetch_output()
    )
