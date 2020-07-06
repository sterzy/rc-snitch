
from argparse import ArgumentTypeError
from datetime import datetime
import re

def check_binary(code: str) -> str:
  """Checks if a string is a valid binary code

  :param      code:               The code that will be checked
  :type       code:               str

  :returns:   If the code is valid it will be returned
  :rtype:     str

  :raises     ArgumentTypeError:  If the code is not valid, this error will be
                                  raised
  """
  if not bool(re.match('^[10]+$', code)):
    raise ArgumentTypeError("{} is not a valid binary code".format(code))

  return code

def check_tri_state(code: str) -> str:
  """Checks if a string is a valid tri-state code

  :param      code:               The code that will be checked
  :type       code:               str

  :returns:   If the code is valid it will be returned
  :rtype:     str

  :raises     ArgumentTypeError:  If the code is not valid, this error will be
                                  raised
  """
  if not bool(re.match('^[10F]+$', code)):
    raise ArgumentTypeError("{} is not a valid tri-state code".format(code))

  return code

def check_tri_state_pair(pair: str) -> str:
  """Checks if a string is a valid tri-state code

  :param      pair:               The pair that will be checked
  :type       pair:               str

  :returns:   If the pair is valid it will be returned as a tuple
  :rtype:     str

  :raises     ArgumentTypeError:  If the pair is not valid, this error will be
                                  raised
  """
  codes = pair.split(':')

  if len(codes) != 2:
    raise ArgumentTypeError("{} is not a valid tri state pair".format(pair))

  return (check_tri_state(codes[0]), check_tri_state(codes[1]))

def to_tri_state(value: int) -> str:
  """Parses an integer value to a tri-state code

  :param      value:  The value to parse
  :type       value:  int

  :returns:   A string containing the tri-state code
  :rtype:     str
  """
  tri_state = ""
  string = "{:024b}".format(value)

  for i in range(0, len(string), 2):
    if string[i:i+2] == '01':
      tri_state += 'F';

    elif string[i:i+2] == '11':
      tri_state += '1';

    elif string[i:i+2] == '00':
      tri_state += '0';

    # would result in an invalid string arccording to the arduino library but
    # for completeness sake
    elif string[i:i+2] == '10':
      tri_state += 'S';

  return tri_state

def tri_state_value(tri_state: str) -> bool:
  """Returns whether a tri-state code turns a switch on or off.

  :param      tri_state:  The tri-state code.
  :type       tri_state:  str

  :returns:   True if the tri-state codes turns a switch on, False otherwise.
  :rtype:     str
  """
  return 'F' == tri_state[-1:]

def tri_state_device(tri_state: str) -> str:
  """Returns a more human readable description of the device in a tri-state c
  ode.

  :param      tri_state:  The tri-state code to parse
  :type       tri_state:  str

  :returns:   A string describing the devices group and place in the group.
  :rtype:     str
  """
  group  = tri_state_part_to_number(tri_state[0:4])
  device = tri_state_part_to_number(tri_state[4:8])

  return "G-{} D-{}".format(group, chr(ord('@')+device))

def tri_state_part_to_number(part: str) -> int:
  """Parses a tri state part to a number

  :param      part:  The part that will be parsed
  :type       part:  str

  :returns:   A number between 1 and 4 if a valid tri_state part is provided
              otherwise none
  :rtype:     int
  """
  if len(part) == 4:
    return (part.find('0') + 1)

  return None

def format_received(timestamp: datetime, val: int) -> str:
  """
  Formats a value that has been received in order to be able to print it nicely.

  :param      timestamp:  The timestamp when the value was received
  :type       timestamp:  datetime
  :param      val:        The value that was received
  :type       val:        int

  :returns:   The formatted string
  :rtype:     str
  """
  tri = to_tri_state(val);
  on  = tri_state_value(tri)

  if on:
    state = tint_green("ON")
  else:
    state = tint_red("OFF")

  return "{}: Switch {} ({}, {}) was turned {}.".format(tint_blue(timestamp),
                                             tint_yellow(tri_state_device(tri)),
                                             tint_yellow(tri),
                                             tint_yellow(val),
                                             state,
                                             tint_yellow(val))

def tint_green(text: str) -> str:
  """Tints a given text green.

  :param      text:  The text to be tinted
  :type       text:  str

  :returns:   The same text but tinted green
  :rtype:     str
  """
  return ("\x1b[32m%s\x1b[0m" % text)

def tint_blue(text: str) -> str:
  """Tints a given text blue.

  :param      text:  The text to be tinted
  :type       text:  str

  :returns:   The same text but tinted blue
  :rtype:     str
  """
  return ("\x1b[34m%s\x1b[0m" % text)

def tint_red(text: str) -> str:
  """Tints a given text red.

  :param      text:  The text to be tinted
  :type       text:  str

  :returns:   The same text but tinted red
  :rtype:     str
  """
  return ("\x1b[31m%s\x1b[0m" % text)

def tint_yellow(text: str) -> str:
  """Tints a given text yellow.

  :param      text:  The text to be tinted
  :type       text:  str

  :returns:   The same text but tinted yellow
  :rtype:     str
  """
  return ("\x1b[33m%s\x1b[0m" % text)
