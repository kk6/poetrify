from pipenv2poetry import __version__
from cleo import Application, CommandTester


def test_version():
    assert __version__ == '0.1.0'


def test_foo():
    from pipenv2poetry.cli import GenerateCommand
    application = Application()
    application.add(GenerateCommand())
    command = application.find("generate")
    command_tester = CommandTester(command)
    command_tester.execute("-d -w tests/repos/foo")

    assert (
        "poetry init --dependency=scrapy --dependency=beautifulsoup4 --license=MIT"
        in
        command_tester.io.fetch_output()
    )
