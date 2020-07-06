
from arduino import Arduino, connection_handler
from argparse import Namespace
from commands.command import Command
from util import tint_yellow, tint_red, to_tri_state, tri_state_value
import signal, time

class Block(Command):
  """This class represents the 'block' subcommand."""

  def __init__(self):
    """Constructs a new instance."""
    super(Block, self).__init__()
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

  def __block_aggressive(self, a: Arduino):
    """Blocks a certain set of switches aggressively, by sending a specified set
    of codes continuously.

    :param      a:    he Arduino object that will be used as a blocker.
    :type       a:    Arduino
    """
    print("Blocking the following switches continuously: {}"
                              .format(tint_red(",".join(self.args.aggressive))))

    while not self.interrupted:
      for code in self.args.aggressive:
        a.send_tri_state(code)
        time.sleep(.5)

  def __block_reactive(self, a: Arduino):
    """Blocks a certain set of switches reactively by sending a specified
    tri-state code upon reception of another tri-state code.

    :param      a:    The Arduino object that will be used as a blocker.
    :type       a:    Arduino
    """
    blocking = dict(self.args.reactive)

    while not self.interrupted:
      received = a.sniff_single()

      if received is not None:
        code = to_tri_state(received);

        if code in blocking:
          print("Switch {} detected, blocking {}...".format(tint_red(code),
                                                    tint_yellow(blocking[code])))

          for i in range(5):
            a.send_tri_state(blocking[code])
            time.sleep(.5)

  def execute(self, args: Namespace):
    """Checks which type of blocker should be used an executes it.

    :param      args:  The arguments to the command
    :type       args:  Namespace
    """
    print(tint_yellow('Starting blocker...'))
    self.args = args

    # attach signal handler and start listening
    signal.signal(signal.SIGTERM, self.__signal_handler)
    signal.signal(signal.SIGINT, self.__signal_handler)

    # start blocking
    if args.aggressive is not None:
      connection_handler(self.__block_aggressive,
                         args.port,
                         args.baud_rate,
                         args.timeout)

    elif args.reactive is not None:
      connection_handler(self.__block_reactive,
                         args.port,
                         args.baud_rate,
                         args.timeout)

    print(tint_yellow('Stopping...'))
