#!/usr/bin/env python
import os
import subprocess
from pathlib import Path

from cleo import Command
from cleo import Application

from . import __version__
from .core import generate_init_cmd

application = Application("pipenv2poetry", __version__, complete=True)


class GenerateCommand(Command):
    """
    Generate pyproject.toml from Pipfile

    generate
        {--w|workspace= : Working space}
        {--d|dry-run : Only display the generated command.}

    """

    def handle(self):
        workspace = self.option("workspace")
        if workspace:
            os.chdir(Path(workspace))

        try:
            cmd = generate_init_cmd()
        except FileNotFoundError as e:
            self.line_error(f"<error>{e}</error>")
            return self.line_error("<error>[ERROR] Pipfile not found.</error>")

        self.info("Generated init command:")
        self.line(f"\n{cmd}\n")
        self.line("")

        if not self.option("dry-run"):
            self.info("Execute the above command. Also, the following output is due to Poetry.")
            subprocess.run(cmd, shell=True)


application.add(GenerateCommand())
