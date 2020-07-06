
from arduino import Arduino, connection_handler
from argparse import Namespace
from datetime import datetime
from os import path, linesep
from util import tint_yellow, to_tri_state, tri_state_value, format_received
from commands.command import Command
import signal

class Sniff(Command):
  """This class represents the 'sniff' subcommand."""

  def __init__(self):
    """Constructs a new instance."""
    super(Sniff, self).__init__()
    self.interrupted = False
    self.args        = None

  def __signal_handler(self, signal: int, frame):
    """Handles SIGINT and SIGTERM signals to enable a graceful shutdown.

    :param      signal:  The signal that was triggered.
    :type       signal:  int
    :param      frame:   The last stack frame.
    :type       frame:   frame
    """
    self.interrupted = True

  def __log_lines(self, a: Arduino):
    """Logs the received information to the terminal and if a file has been
    provided the information is also store there in a csv format.

    :param      a:    The Arduino which will be used as a receiver.
    :type       a:    Arduino
    """
    while not self.interrupted:
      lines = a.sniff_multiple();
      now   = datetime.now()

      # if no out file has been provided, just print to the terminal
      if self.args.out is None:
        for l in list(dict.fromkeys(lines)):
          tri = to_tri_state(l);

          if self.args.allowed is None or tri in self.args.allowed:
            print(format_received(now, l))

      # if an out file has been provided, create a csv file as well
      else:
        if not path.exists(self.args.out):
          with open(self.args.out, 'w') as file:
            file.write("Timestamp; Decimal; TriState; State{}".format(linesep))

        with open(self.args.out, 'a') as file:
          for l in list(dict.fromkeys(lines)):
            tri = to_tri_state(l);

            if self.args.allowed is None or tri in self.args.allowed:
              val = tri_state_value(tri)
              file.write("{}; {}; {}; {}{}".format(now, l, tri, val, linesep))
              print(format_received(now, l))

  def execute(self, args: Namespace):
    """Handles the 'sniff' command.

    :param      args:  The arguments to the command
    :type       args:  Namespace
    """
    print(tint_yellow('Starting sniffer...'))
    self.args = args

    # attach signal handler and start listening
    signal.signal(signal.SIGTERM, self.__signal_handler)
    signal.signal(signal.SIGINT, self.__signal_handler)
    connection_handler(self.__log_lines, args.port, args.baud_rate, args.timeout)

    print(tint_yellow('Stopping...'))
