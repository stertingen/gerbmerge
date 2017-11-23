#!/usr/bin/env python2
"""
Various utility functions

--------------------------------------------------------------------

This program is licensed under the GNU General Public License (GPL)
Version 3.  See http://www.fsf.org for details of the license.

Rugged Circuits LLC
http://ruggedcircuits.com/gerbmerge
"""

import config

def in2gerb(value, val_unit = ''):
    """Convert something in val_unit to 2.5(in) or 5.3(mm) Gerber units"""
    f = 1
    if config.Config['measurementunits'] != val_unit:
      if val_unit == 'inch':
        # Target: mm, value: inch
        f = 25.4
      elif val_unit == 'mm':
        # Target: inch, value: mm
        f = 1/25.4

    if config.Config['measurementunits'] == 'inch':
      return int(round(f*value*1e5))
    else: #convert mm to 5.3 Gerber units
      return int(round(f*value*1e3))

def gerb2in(value):
    """Convert 2.5(in) or 5.3(mm) Gerber units to target unit specified in config"""
    if config.Config['measurementunits'] == 'inch':
      return float(value)*1e-5
    else:
      return float(value)*1e-3
