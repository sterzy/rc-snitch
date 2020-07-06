
from argparse import Namespace

class Command(object):
  """The command 'interface' describes the structure of a command."""

  def execute(self, args: Namespace):
    pass
