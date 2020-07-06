
from arduino import Arduino, connection_handler
from argparse import Namespace
from commands.command import Command
from util import tint_yellow

class Send(Command):
  """This class represents the 'send' subcommand."""

  def __init__(self):
    """Constructs a new instance."""
    super(Send, self).__init__()

  def execute(self, args: Namespace):
    """Execute the 'send' command, parses the type of 'send' command and executes
    it.

    :param      args:  The arguments to the command
    :type       args:  Namespace
    """
    fn = None

    if args.binary is not None:
      print('''Sending binary code "{}"...'''
                                              .format(tint_yellow(args.binary)))
      fn = lambda a : a.send_binary(args.binary)

    elif args.tri_state is not None:
      print('''Sending tri-state code "{}"...'''.format(
                                                   tint_yellow(args.tri_state)))
      fn = lambda a : a.send_tri_state(args.tri_state)

    elif args.decimal is not None:
      print('''Sending decimal value {} with length {}...'''
            .format(tint_yellow(args.decimal[0]), tint_yellow(args.decimal[1])))
      fn = lambda a : a.send_decimal_value(args.decimal[0], args.decimal[1])

    if fn is not None:
      connection_handler(fn, args.port, args.baud_rate, args.timeout)
