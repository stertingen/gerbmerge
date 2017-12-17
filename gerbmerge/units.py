#!/usr/bin/env python2

from unum.units.si import *
from unum import Unum

unit = Unum.unit

mil     = MIL   = unit('mil',   25.4 * UM,  'mil')
inch    = INCH  = unit('inch',  25.4 * MM,  'inch')

class NumberParser:
    def __init__(self, unit = inch, integers = 2, decimals = 4,
            omitTrailing = False, omitLeading = False):
        if (omitTrailing and omitLeading):
            raise RuntimeError, "Cannot omit both trailing and leading zeros!"
        self.unit = unit
        self.integers = integers
        self.decimals = decimals
        self.omitTrailing = omitTrailing
        self.omitLeading = omitLeading

    def setUnit(self, unit):
        self.unit = unit

    def setFormat(self, integers, decimals):
        self.integers = integers
        self.decimals = decimals

    def setOptions(self, omitTrailing = False, omitLeading = False, incremental = False):
        if (omitTrailing and omitLeading):
            raise RuntimeError, "Cannot omit both trailing and leading zeros!"
        if (incremental):
            raise RuntimeError, "Incremental positioning not yet supported!"
        self.omitTrailing = omitTrailing
        self.omitLeading = omitLeading

    def parse(self, string):
        # TODO: Maybe add some sanity checks
        if (self.omitTrailing):
            string = string.ljust(self.integers + self.decimals, '0')

        return (float(string) / 10.0**self.decimals) * self.unit

del Unum
del unit

if __name__ == '__main__':
    print NumberParser(mm, 2, 4, omitTrailing = True).parse("1234")
    print NumberParser(mm, 2, 4, omitLeading = True).parse("1234")
