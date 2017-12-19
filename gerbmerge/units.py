#!/usr/bin/env python2
"""
This module imports the Unum unit system, adds some new units and
a parser for numbers

--------------------------------------------------------------------

This program is licensed under the GNU General Public License (GPL)
Version 3.  See http://www.fsf.org for details of the license.

http://github.com/stertingen/gerbmerge
"""

from unum.units.si import *
from unum import Unum

unit = Unum.unit

mil     = MIL   = unit('mil',   25.4 * UM,  'mil')
inch    = INCH  = unit('inch',  25.4 * MM,  'inch')

class NumberParser:
    def __init__(self, unit = inch, integers = 2, decimals = 4,
            omitTrailing = False, omitLeading = False, decimalPoint = False):
        self.setUnit(unit)
        self.setFormat(integers, decimals)
        self.setOptions(omitTrailing, omitLeading, decimalPoint, incremental = False)

    def setUnit(self, unit):
        self.unit = unit

    def setFormat(self, integers, decimals):
        self.integers = int(integers)
        self.decimals = int(decimals)

    def setOptions(self, omitTrailing = None, omitLeading = None,
            decimalPoint = None, incremental = None):
        if (omitTrailing and omitLeading):
            raise RuntimeError, "Cannot omit both trailing and leading zeros!"
        if (omitTrailing and decimalPoint):
            raise RuntimeError, "Cannot omit trailing zeros with decimal point enabled!"
        if (decimalPoint and omitLeading):
            raise RuntimeError, "Cannot omit leading zeros with decimal point enabled!"
        if (incremental):
            raise RuntimeError, "Incremental positioning not yet supported!"
        
        # Only set explicitly passed options
        if (omitTrailing is not None):
            self.omitTrailing = omitTrailing
        if (omitLeading is not None):
            self.omitLeading = omitLeading
        if (decimalPoint is not None):
            self.decimalPoint = decimalPoint

    def parse(self, string):
        # TODO: Maybe add some sanity checks:
        # Check string length matches integers + decimals
        # Check if there is a decimal point
        # TODO: Better handling for None
        if (string is None):
            return None

        if (self.decimalPoint):
            return float(string) * self.unit
        else:
            if (self.omitTrailing):
                string = string.ljust(self.integers + self.decimals, '0')

            return (float(string) / 10.0**self.decimals) * self.unit

def formatNumber(number, unit, decimals):
    #assert isinstance(number, Unum)
    #assert isinstance(unit, Unum)
    #assert isinstance(decimals, int)
    return int(round(number.asNumber(unit) * 10**decimals))

del Unum
del unit

if __name__ == '__main__':
    print NumberParser(mm, 2, 4, omitTrailing = True).parse("1234")
    print NumberParser(mm, 2, 4, omitLeading = True).parse("1234")
    print NumberParser(mm, decimalPoint = True).parse(".1234")
    print NumberParser(mm, decimalPoint = True).parse("1234")
