#!/usr/bin/env python
import os
import subprocess
from pathlib import Path

from cleo import Command
from cleo import Application

from . import __version__
from .core import generate_init_cmd

application = Application("poetrify", __version__, complete=True)


class GenerateCommand(Command):
    """
    Generate pyproject.toml from Pipfile

    generate
        {--w|workspace= : Working space}
        {--d|dry-run : Only display the generated command.}

    """

    def handle(self):
        _workspace = self.option("workspace")
        if _workspace:
            workspace = Path(_workspace)
            os.chdir(workspace)
        else:
            workspace = Path(".")

        try:
            cmd = generate_init_cmd()
        except FileNotFoundError as e:
            self.line_error(f"<error>{e}</error>")
            return self.line_error("<error>[ERROR] Pipfile not found.</error>")

        self.info("Generated init command:")
        self.line(f"\n{cmd}\n")
        self.line("")

        if not self.option("dry-run"):
            self.info(
                "Execute the above command. Also, the following output is due to Poetry."
            )
            r = subprocess.run(cmd, shell=True)
            pyproject_toml = workspace / "pyproject.toml"
            if not r.returncode and pyproject_toml.exists():
                pipfile = workspace / "Pipfile"
                pipfile_lock = workspace / "Pipfile.lock"
                if pipfile.exists():
                    if self.confirm("Do you wanna delete Pipfile?", False):
                        os.remove(pipfile)
                        self.info("Pipfile deleted!")
                if pipfile_lock.exists():
                    if self.confirm("Do you wanna delete Pipfile.lock, too?", False):
                        os.remove(pipfile_lock)
                        self.info("Pipfile.lock deleted!")


application.add(GenerateCommand())
