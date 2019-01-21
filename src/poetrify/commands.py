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

    def _determine_workspace(self, _workspace):
        if _workspace:
            workspace = Path(_workspace)
        else:
            workspace = Path(".")
        return workspace

    def _remove_source_files(self, workspace, src):
        # TODO: To clean up this dirty code
        source_file = workspace / src
        if src == "Pipfile":
            lock_file = workspace / "Pipfile.lock"

            if source_file.exists():
                if self.confirm("Do you wanna delete Pipfile?", False):
                    os.remove(source_file)
                    self.info("Pipfile deleted!")

            if lock_file.exists():
                if self.confirm("Do you wanna delete Pipfile.lock?", False):
                    os.remove(lock_file)
                    self.info("Pipfile.lock deleted!")
        else:
            if source_file.exists():
                if self.confirm("Do you wanna delete requirements.txt?", False):
                    os.remove(source_file)
                    self.info("requirements.txt deleted!")

    def handle(self):
        workspace = self._determine_workspace(self.option("workspace"))
        os.chdir(workspace)

        src = self.option("src")
        cmd = generate_init_cmd(src)
        if not cmd:
            self.line_error("[ERROR] Source file not found.", style="error")
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

        self._remove_source_files(workspace, src)
