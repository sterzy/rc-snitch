# RC Snitch
This is a project for the course «Secure Mobile Systems» at TU Darmstadt. It attempts to demonstrate some implementation flaws with common radio controlled power outlets. It can:

- Send Codes to turn on or off radio controlled power outlets
- Detect whether such codes are send
- React to such codes

## Dependencies
- Hardware
    + Arduino Uno or Mega 2560 (other might work too, but have not been tested)
    + 433MHz Transmitter
    + 433MHz Receiver
- Software
    + Python 3.8+ and `pip`
    + Arduino IDE 1.8+

## Setup
### Hardware
Connect the transmitter and the receiver to the Arduino as follows:

- On both the transmitter and the receiver connect the pin labelled `VCC` or `5V+` to the `5V` outlet of the Arduino.
- On both the transmitter and the receiver connect `GND` to the same outlet on the Arduino.
- On the transmitter connect the `DATA` pin to pin 10 on the Arduino.
- On the receiver connect the `DATA` pin that is closer to the `GND` pin to pin 2 on the Arduino.

### Software
After installing the Arduino IDE make sure that the Arduino boards are correctly installed with `arduino --install-boards arduino:avr`. Then clone this repository with `git clone --recurse-submodules https://github.com/sterzy/rc-snitch.git` and set up the python project as follows:

```bash
pip3 install virtualenv --user
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

Then you should be able to execute the following commands:

- `make`: This will execute the `all` target which will just verify the project and create (but not install) the python utility.
- `make arduino-upload`: If everything works out, this command should upload the Arduino firmware to the board. Per default, `/dev/ttyACM0` as the port and the Arduino Mega as the board will be used. These values can be overwritten with the following environment variables:
    + `PORT` specifies the port that the Arduino is connected to.
    + `ARCH` specifies the board that is actually used. The following two boards have been tested: Arduino Mega 2560 (`"arduino:avr:mega:cpu=atmega2560"`) and Arduino Uno (`"arduino:avr:uno"`)
- `make rc-snitch`: This will create the python utility.

Note that at this point the python utility is not installed yet. After executing `make rc-snitch` install it with the following commands:

```bash
pip install --upgrade ./target/dist/rc-snitch-1.0.dev0/dist/rc_snitch-1.0.dev0-py3-none-any.whl
rc-snitch -h
```

To understand how it works `rc-snitch -h` can be executed, which display a helpful description of the utility. Every sub-command (`send`, `sniff`, `block` and `profile`) has its own help message. The utility can be removed with `pip uninstall rc-snitch`.

## Further Reading
- [SUI77 - Low cost RC power sockets (radio outlets)+arduino](https://sui77.wordpress.com/2011/04/12/163/)
- This project is based on the rc-switch library: [SUI77 - rc-switch](https://github.com/sui77/rc-switch)
- [Arduino IDE CLI Documentation](https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc)
