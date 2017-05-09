#!/usr/bin/env python
"""
Various utility functions

--------------------------------------------------------------------

This program is licensed under the GNU General Public License (GPL)
Version 3.  See http://www.fsf.org for details of the license.

Rugged Circuits LLC
http://ruggedcircuits.com/gerbmerge
"""

import config


def in2gerb(value):
# add metric support (1/1000 mm vs. 1/100,000 inch)
  #integerDigits = int(config.Config['coordinatesintegerdigits'])
  fractionalDigits = int(config.Config['gerberdecimals'])

  """Convert inches to n.m Gerber units"""
  return int(round(value*pow(10,fractionalDigits)))


def in2gerber_str(value):
# add metric support (1/1000 mm vs. 1/100,000 inch)
  #integerDigits = int(config.Config['coordinatesintegerdigits'])
  fractionalDigits = int(config.Config['gerberdecimals'])

  """Convert inches to n.m Gerber units"""
  return str(int(round(value*pow(10,fractionalDigits)))).zfill(config.ZeroFillCount)


def gerb2in(value):
# add metric support (1/1000 mm vs. 1/100,000 inch)
  #integerDigits = int(config.Config['inputcoordinatesintegerdigits'])
  fractionalDigits = int(config.Config['inputgerberdecimals'])
  
  """Convert n.m Gerber units to inches"""
  return float(value)*pow(10,-fractionalDigits)


def gerber_str(value):
  return str(value).zfill(config.ZeroFillCount)

def excellon_str(value):
  if config.ExcellonZeroFillCount == 0: # No leading zeros
    return str(value)
  else:
    return str(value).zfill(config.ExcellonZeroFillCount)#.rstrip('0') # Remove trailing zeros
