#!/bin/sh
cd stertingen
#python2 ../../gerbmerge/gerbmerge.py --skipdisclaimer layout-inch.cfg layout.def
#python2 ../../gerbmerge/gerbmerge.py --skipdisclaimer layout-mm.cfg layout.def
cd ../DipTrace_Example
python2 ../../gerbmerge/gerbmerge.py --skipdisclaimer layout.cfg
cd ..
