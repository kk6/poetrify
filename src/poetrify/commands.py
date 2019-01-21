import errno
import os
import subprocess
import sys
from pathlib import Path

from cleo import Command

from .api import generate_init_cmd


class GenerateCommand(Command):
    """
    Generate pyproject.toml from the source file

    generate
        {--w|workspace= : Working space}
        {--s|src=Pipfile : source file}
        {--d|dry-run : Only display the generated command.}

    """

    def handle(self):
        _workspace = self.option("workspace")
        if _workspace:
            workspace = Path(_workspace)
            os.chdir(workspace)
        else:
            workspace = Path(".")

        src = self.option("src")
        cmd = generate_init_cmd(src)
        if not cmd:
            self.line_error("[ERROR] Pipfile not found.", style="error")
            sys.exit(errno.ENOENT)

        self.info("Generated init command:")
        self.line(f"\n{cmd}\n")
        self.line("")

        if self.option("dry-run"):
            sys.exit(os.EX_OK)

        self.info(
            "Execute the above command. Also, the following output is due to Poetry."
        )
        r = subprocess.run(cmd, shell=True)
        if r.returncode != os.EX_OK:
            sys.exit(r.returncode)

        pipfile = workspace / "Pipfile"
        pipfile_lock = workspace / "Pipfile.lock"

        if pipfile.exists():
            if self.confirm("Do you wanna delete Pipfile?", False):
                os.remove(pipfile)
                self.info("Pipfile deleted!")

        if pipfile_lock.exists():
            if self.confirm("Do you wanna delete Pipfile.lock?", False):
                os.remove(pipfile_lock)
                self.info("Pipfile.lock deleted!")
