#!/usr/bin/env python
from cleo import Application

from . import __version__
from .commands import GenerateCommand

application = Application("poetrify", __version__, complete=True)
application.add(GenerateCommand())
