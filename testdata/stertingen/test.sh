#!/bin/sh
python2 ../../gerbmerge/gerbmerge.py --skipdisclaimer layout-inch.cfg layout.def
python2 ../../gerbmerge/gerbmerge.py --skipdisclaimer layout-mm.cfg layout.def

