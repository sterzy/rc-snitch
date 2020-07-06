#include "src/rc-switch/RCSwitch.h"

/*<== Global Variables ==>*/

RCSwitch Transmitter  = RCSwitch(); /**< The 433MHz transmitter. */
RCSwitch Receiver     = RCSwitch(); /**< The 433MHz receiver. */

unsigned int messageBuffer[15]; /**< Buffer to store the current message. */
int ind = 0;                    /**< Index of the current message. */
int len = 0;                    /**< Length of the current message. */

/*<== Main Logic ==>*/

/**
 * @brief      Setups the rc receiver on pin 2, the transmitter on pin 10 and
 *             the serial connection.
 */
void setup(void) {

  Serial.begin(9600);
  Transmitter.enableTransmit(10);
  Receiver.enableReceive(0);

}

/**
 * @brief      Loops eternally, checks if the switch has received something and
 *             sends it. It checks and handles receiving message via the serial
 *             communication as well.
 */
void loop(void) {

  if (Receiver.available()) {

    // We received something via the 433MHz receiver, send it
    sendValue(Receiver.getReceivedValue());
    Receiver.resetAvailable();

  }

  if (Serial.available()) {

    unsigned int received = Serial.read();

    // if we receive a valid message header, start parsing it
    if (ind >= len && received >= 64 && received < 80) {

      len = received & 15;
      ind = 0;

    // keep parsing a message until we reach the end
    } else if (ind < len) {

      messageBuffer[ind++] = received;

      if (ind >= len) {

        // parse the message we received
        parseMessage(messageBuffer, len);

        // clear the buffer and the helper variables
        len = ind = 0;
        memset(messageBuffer, 0, sizeof(messageBuffer));

      }
    }
  }
}

/*<== Parse and Send Messages ==>*/

/**
 * @brief      Sends a given value via the serial connection.
 *
 * @param[in]  toSend  The message that will be send
 */
void sendValue(unsigned long toSend) {

  // divide the long up into 4 bytes
  uint8_t buf[4];
  buf[0] = toSend         & 255;
  buf[1] = (toSend >> 8)  & 255;
  buf[2] = (toSend >> 16) & 255;
  buf[3] = (toSend >> 24) & 255;

  // send everything
  Serial.write('R');
  Serial.write(buf, sizeof(buf));
  Serial.write('\n');

}

/**
 * @brief      This function parses the contents of a message buffer and
 *             executes a given command.
 *
 * @param      buffer  The buffer that will be parsed.
 * @param[in]  length  The length of the message.
 */
void parseMessage(unsigned int buffer[], int length) {

  // check if we are parsing a valid command and trigger the command
  if (length > 2) {

    switch (buffer[0]) {

      // send a code
      case 1:
        send(buffer, length);
        break;

      // activate or deactivate the receiver
      case 2:
        setReceiver((bool) buffer[1]);
        break;

    }
  }
}

/*<== Command Implementations ==>*/

/**
 * @brief      Sends a decimal value via the transmitter.
 *
 * @param      buffer  The buffer containing the value and length of the
 *                     transmission.
 * @param[in]  length  The length of the buffer.
 */
void send(unsigned int buffer[], unsigned int length) {

  if (length == 7) {

    // parse the value and length
    unsigned long value = (((unsigned long) buffer[1]) << 24) +
                          (((unsigned long) buffer[2]) << 16) +
                          (((unsigned long) buffer[3]) << 8) +
                          buffer[4];
    unsigned int l      = (buffer[5] << 8) + buffer[6];

    // send the value and stop the receiver from reporting our own values
    Transmitter.send(value, l);
    Receiver.resetAvailable();

  }
}

/**
 * @brief      Disables or enables the receiver.
 *
 * @param[in]  to    Whether the receiver should be turned on or off.
 */
void setReceiver(bool to) {

  if (to) {

    Receiver.enableReceive(0);

  } else {

    Receiver.disableReceive();

  }
}
