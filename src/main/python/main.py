#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from commands import block, send, sniff, profile
from pathlib import Path
from util import check_binary, check_tri_state, check_tri_state_pair
import argparse

def main():
  parser = argparse.ArgumentParser(description='''A utility to sniff and \
    transmit with a 433MHz transceiver using an Arduino.''')

  subparsers = parser.add_subparsers(title='sub-commands',
                                     metavar='COMMAND',
                                     help='')

  subparsers.required = True

  parser.add_argument('-p',
                      '--port',
                      metavar='PORT',
                      type=str,
                      default='/dev/ttyACM0',
                      help='''port the Arduino is connected to, defaults \
                      to "/dev/ttyACM0"''')

  parser.add_argument('-b',
                      '--baud-rate',
                      metavar='BAUDRATE',
                      type=int,
                      default=9600,
                      help='''baud rate that the Arduino uses, defaults to \
                      9600''')

  parser.add_argument('-t',
                      '--timeout',
                      metavar='TIMEOUT',
                      type=int,
                      default=5,
                      help='''timeout used for the connection to the \
                      arduino, defaults to 5 seconds''')

  send_parser = subparsers.add_parser('send', help='''send either a \
                              tri-state, binary or decimal value''')

  send_group = send_parser.add_mutually_exclusive_group(required=True)

  send_group.add_argument('-b',
                          '--binary',
                          metavar="BINARY",
                          type=check_binary,
                          help='the binary code to send')

  send_group.add_argument('-t',
                          '--tri-state',
                          metavar="TRISTATE",
                          type=check_tri_state,
                          help='the tri-state code to send')

  send_group.add_argument('-d',
                          '--decimal',
                          metavar="NUMBER",
                          type=int,
                          nargs=2,
                          help='the decimal code and length to send')

  send_parser.set_defaults(func=send.Send().execute)

  sniff_parser = subparsers.add_parser('sniff', help='''use the receiver to \
                                                        sniff for events''')

  sniff_parser.add_argument('-o',
                            '--out',
                            metavar='OUTFILE',
                            type=Path,
                            help='''write events to a file in addition to the \
                            terminal, data will be in a csv format''')

  sniff_parser.add_argument('-a',
                            '--allowed',
                            metavar='ALLOW',
                            type=check_tri_state,
                            nargs='+',
                            help='''a list of allowed codes that will be \
                            logged, only accepts tri-state codes''')

  sniff_parser.set_defaults(func=sniff.Sniff().execute)

  block_parser = subparsers.add_parser('block', help='''block a switch either \
              reactively or aggressively, only accepts tri-state codes''')

  block_group = block_parser.add_mutually_exclusive_group(required=True)

  block_group.add_argument('-r',
                          '--reactive',
                          metavar='ON:SEND',
                          type=check_tri_state_pair,
                          nargs='+',
                          help='''reactively block a switch, when the code ON is \
                          detected SEND will be transmitted''')

  block_group.add_argument('-a',
                          '--aggressive',
                          metavar='CODE',
                          type=check_tri_state,
                          nargs='+',
                          help='''aggressively block a switch i.e. send the \
                          provided code continously''')

  block_parser.set_defaults(func=block.Block().execute)

  profile_parser = subparsers.add_parser('profile', help='''take a csv file \
                create by the "sniff" sub-command and create a nice overview''')

  profile_parser.add_argument('data',
                              metavar='CSVFILE',
                              type=Path,
                              help='''the file containing the sniffing data''')

  profile_parser.set_defaults(func=profile.Profile().execute)

  args = parser.parse_args()
  args.func(args)

if __name__ == '__main__':
  main()
