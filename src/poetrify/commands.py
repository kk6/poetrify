import errno
import os
import subprocess
import sys
from pathlib import Path

from cleo import Command

from .api import build_poetry_init_command


class GenerateCommand(Command):
    """
    Generate pyproject.toml from the source file

    generate
        {--w|workspace= : Working space}
        {--s|src=Pipfile : source file}
        {--d|dry-run : Only display the generated command.}

    """

    def _determine_workspace(self, _workspace):
        if _workspace:
            workspace = Path(_workspace)
        else:
            workspace = Path(".")
        return workspace

    def handle(self):
        workspace = self._determine_workspace(self.option("workspace"))
        os.chdir(workspace)

        _src = self.option("src")
        src = workspace.cwd() / _src
        poetry_command = build_poetry_init_command(src)
        if not poetry_command:
            self.line_error("[ERROR] Source file not found.", style="error")
            sys.exit(errno.ENOENT)

        self.info("Generated init command:")
        self.line(f"\n{poetry_command}\n")
        self.line("")

        if self.option("dry-run"):
            sys.exit(os.EX_OK)

        self.info(
            "Execute the above command. Also, the following output is due to Poetry."
        )
        r = subprocess.run(poetry_command, shell=True)
        if r.returncode != os.EX_OK:
            sys.exit(r.returncode)

        if src.exists():
            if self.confirm(f"Do you wanna delete {src.name}?", False):
                os.remove(src)
                self.info(f"{src.name} deleted!")
        if src.name == "Pipfile":
            lock_file = src.parent / "Pipfile.lock"
            if lock_file.exists():
                if self.confirm("Do you wanna delete Pipfile.lock?", False):
                    os.remove(lock_file)
                    self.info("Pipfile.lock deleted!")
