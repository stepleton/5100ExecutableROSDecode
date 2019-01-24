#!/usr/bin/python3
"""Assemble screendump hex files into binary files.

Usage: 5100_display_undump.py file1 file2 ...

All files on the command line should be text files starting with twelve
nonempty lines of 64 characters in [0123456789ABCDEF]. These files are assumed
to be text transcriptions of the IBM 5x00 screen with the DISPLAY REGISTERS
switch in the on position.

This program will print binary data to stdout containing the same information
as was shown on the IBM 5x00 screen. Data from successive files listed on the
command line will be concatenated in the same order in the output.

The DISPLAY REGISTERS display presents 256 16-bit "halfwords". Each halfword is
shown as a 2x2 "square" of characters, e.g.

    AB
    CD

which is the 16-bit value 0xABCD. The display presents the 256 halfwords in
left-to-right, top-to-bottom order (or "row-major" order if you prefer). Refer
to page 3-71 of the IBM 5100 Maintenance Information Manual (found at e.g.
http://bitsavers.informatik.uni-stuttgart.de/pdf/ibm/5100/SY31-0405-3_5100maint_Oct79.pdf)
for more details on this display.

It's worth restating that this program will dump binary data directly to stdout.

Licensing:

This program and any supporting programs, software libraries, and documentation
distributed alongside it are released into the public domain without any
warranty. See the LICENSE file for details.
"""

import itertools
import logging
import sys


def validate(filename, data):
  """Check that input data meets validity requirements, or fail."""
  assert len(data) == 16, (
      'Screen transcription files must be 16 lines long, but {} has {} lines.'
      ''.format(filename, len(data)))
  assert all(len(d) == 64 for d in data), (
      'All lines in screen transcription files must contain exactly 64 '
      'characters, but {} deviates from this requirement.'.format(filename))
  assert all(c in '0123456789ABCDEF' for c in ''.join(data)), (
      'Screen transcription files may only contain the characters "0123456789A'
      'BCDEF", but {} has other characters.'.format(filename))


def decode(data):
  """Decode a DISPLAY REGISTERS screen dump as binary data."""
  top_rows = ''.join(data[::2])
  bot_rows = ''.join(data[1::2])
  all_hex = ''.join(itertools.chain.from_iterable(zip(top_rows, bot_rows)))
  return bytes.fromhex(all_hex)


def main(files):
  if not files: logging.warning(
    'No files listed on commandline: output is empty.')
  for filename in files:
    with open(filename, 'r') as f:
      data = [l.upper() for l in f.read().splitlines()]
      validate(filename, data)
      sys.stdout.buffer.write(decode(data))


if __name__ == '__main__':
  main(sys.argv[1:])
