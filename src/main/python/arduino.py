
from serial import Serial
from typing import Callable
import time

class Arduino(object):

  def __init__(self, port: str = '/dev/ttyACM0',
               baud_rate: int = 9600,
               timeout: int = 5):
    """The Arduino class provides a convenient wrapper around the serial
    communication with the Arduino.

    :param      port:       The port that will be used to connect to the
                            Arduino. Default: "/dev/ttyACM0".
    :type       port:       str
    :param      baud_rate:  The baud rate that will be used for the connection.
                            Default: 9600
    :type       baud_rate:  int
    :param      timeout:    The timeout used for the connection in seconds.
                            Default 5
    :type       timeout:    int
    """
    super(Arduino, self).__init__()
    self.port = port
    self.baud_rate = baud_rate
    self.arduino = None
    self.timeout = timeout

  def __str__(self) -> str:
    """Returns a string representation of the object.

    :returns:   String representation of the object.
    :rtype:     str
    """
    toReturn = 'Arduino(connected={}, port="{}", baudrate={})'
    return toReturn.format(self.is_connected(), self.port, self.baud_rate)

  def connect(self):
    """Connects to the Arduino on the configured port with the configured baud
    rate. Note: after calling this method it might be necessary to wait for 1 or
    two seconds for the communication to be established properly.
    """
    self.arduino = Serial(self.port, self.baud_rate, timeout=self.timeout)

  def disconnect(self):
    """Disconnects from the Arduino."""
    self.arduino.close()
    self.arduino = None

  def is_connected(self) -> bool:
    """Checks if the Arduino is connected or not.

    :returns:   True if the Arduino is connected, False otherwise.
    :rtype:     bool
    """
    return self.arduino is not None

  def send_message(self, message: bytes):
    """Sends a message, to the Arduino, if the message is larger than 15 bytes
    nothing happens. If the Arduino is not connected, this function will connect
    to it.

    :param      message:  The message that will be send.
    :type       message:  bytes
    """
    if not self.is_connected():
      self.connect()

    if len(message) <= 15:
      header = (0x40 + len(message)).to_bytes(1, 'big')
      self.arduino.write(header + message)

  def set_receiver(self, to: bool):
    """Changes whether the receiver is active or not. If the Arduino is not
    connected, this function will connect to it.

    :param      to:   The new value the receiver will be set to. True to
                      activate it, False to deactivate it.
    :type       to:   bool
    """
    self.send_message(b'\x02' + int(to).to_bytes(1, 'big'))

  def enable_receiver(self):
    """Enables the receiver. If the Arduino is not connected, this function will
    connect to it.
    """
    self.set_receiver(True)

  def disable_receiver(self):
    """Disables the receiver. If the Arduino is not connected, this function
    will connect to it.
    """
    self.set_receiver(False)

  def send_decimal_value(self, value: int, length: int = 24):
    """Sends a value via the decimal send method of the Arduino transmitter. If
    the Arduino is not connected, this function will connect to it.

    :param      value:   The value that will be send
    :type       value:   int
    :param      length:  The length of the signal, defaults to 24
    :type       length:  int
    """
    self.send_message(b'\x01' +
                      value.to_bytes(4, 'big') +
                      length.to_bytes(2, 'big'))

  def send_tri_state(self, code: str):
    """Sends a TriState code. Note: this does not use the RCSwitch::sendTriState
    (@see https://github.com/sui77/rc-switch/blob/master/RCSwitch.cpp) method,
    but rather uses the same encoding scheme to create an equivalent decimal
    value. If the Arduino is not connected, this function will connect to it.

    :param      code:  The code that will be send
    :type       code:  str
    """
    value = 0;

    # for each 0 a bit pattern of '00' , for each 1 a bit pattern of '11' and
    # for F a bit patter of '11' is created
    for i in code:
      value <<= 2;

      if i == 'F':
        value += 1;
      elif i == '1':
        value += 3;

    self.send_decimal_value(value, len(code)*2)

  def send_binary(self, code: str):
    """Sends a binary code. Note: this does not use the RCSwitch::send (@see
    https://github.com/sui77/rc-switch/blob/master/RCSwitch.cpp) method, but
    rather uses the same encoding scheme to create an equivalent decimal value.
    If the Arduino is not connected, this function will connect to it.

    :param      code:  The code that will be send
    :type       code:  str
    """
    self.send_decimal_value(int(code, 2), len(code))

  def sniff_single(self) -> int:
    """Reads a multiple values from the receiver and parses them. Note: this
    call blocks and uses the timeout specified before.

    :returns:   A list of all values that have been received.
    :rtype:     int
    """
    data = self.arduino.readline()

    if data and data[0] == ord('R'):
      return int.from_bytes(data[1:4], 'little')

    return None

  def sniff_multiple(self) -> list:
    toReturn = []

    lines = self.arduino.readlines()

    for l in lines:
      if l and l[0] == ord('R'):
        toReturn.append(int.from_bytes(l[1:4], 'little'))

    return toReturn

def connection_handler(to_wrap: Callable[[Arduino], None],
                       port: str = '/dev/ttyACM0',
                       baud_rate: int = 9600,
                       timeout: int = 5):
  """Wraps a given function with the setup up and tear down code needed for
  proper communication with the Arduino.

  :param      to_wrap:    The function that will be wrapped
  :type       to_wrap:    Function
  :param      port:       The port that will be used to connect to the Arduino.
                          Default: "/dev/ttyACM0".
  :type       port:       str
  :param      baud_rate:  The baud rate that will be used for the connection.
                          Default: 9600
  :type       baud_rate:  int
  :param      timeout:    The timeout used for the connection in seconds.
                          Default: 5 seconds
  :type       timeout:    int
  """
  arduino = Arduino(port, baud_rate, timeout)
  arduino.connect()
  time.sleep(2)

  to_wrap(arduino)

  arduino.disconnect()
