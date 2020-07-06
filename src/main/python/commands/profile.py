
from argparse import Namespace
from commands.command import Command
from datetime import datetime
from util import tint_yellow, tint_red, tint_green, tint_blue
from util import tri_state_value, tri_state_device
import csv

class Profile(Command):
  """This class represents the 'profile' subcommand."""

  def __init__(self):
    """Constructs a new instance."""
    super(Profile, self).__init__()

  def execute(self, args: Namespace):
    """Execute the 'profile' command. It gives a nice overview of data captured
    with the sniff command

    :param      args:  The arguments to the command
    :type       args:  Namespace
    """
    data = {}

    with open(args.data, 'r') as file:
      reader = csv.reader(file, delimiter=';')

      for row in reader:
        if reader.line_num == 1:
          if 'Timestamp, Decimal, TriState, State' != ','.join(row):
            print('Not a valid CSV file!')
            return

        else:
          dt     = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
          value  = tri_state_value(row[2])
          device = data.setdefault(tri_state_device(row[2].strip()), {})
          device.setdefault(dt.date(),[]).append((dt.strftime('%H:%M'), value))

    for k in sorted(data.keys()):
      device = data[k]
      print('Device {}:'.format(tint_yellow(k)))

      for d in sorted(device.keys()):
        device[d].sort(key=lambda x: x[0])
        print('\t{}:'.format(tint_blue(d)))

        for (t, v) in device[d]:
          if v:
            print('\t\tAt {} the device was turned {}.'.format(tint_blue(t),
                                                              tint_green('ON')))
          else:
            print('\t\tAt {} the device was turned {}.'.format(tint_blue(t),
                                                               tint_red('OFF')))
