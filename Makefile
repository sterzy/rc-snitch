.PHONY: all

PORT ?= /dev/ttyACM0
ARCH ?= arduino:avr:mega:cpu=atmega2560

all: arduino-verify rc-snitch

clean:
	pyb clean

arduino-upload: src/main/arduino/main.cpp
	arduino --upload --port $(PORT) --board $(ARCH) $^

arduino-verify: src/main/arduino/main.cpp
	arduino --verify --board $(ARCH) $^

rc-snitch: build.py
	pyb
