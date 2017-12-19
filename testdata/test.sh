#!/bin/sh
set -e
GERBMERGE="python2 $(readlink -f ../gerbmerge/gerbmerge.py) --skipdisclaimer"
TESTROOT=$(pwd)
for CFG in $(find . -name "*.cfg"); do
    cd $(dirname $CFG)
    DEF=$(sed 's/\.cfg$/\.def/g' <<< $(basename $CFG))
    if [ -r $DEF ]; then
        echo "Running GerbMerge in $(dirname $CFG) with Config $(basename $CFG) and Layout $DEF ..."
        $GERBMERGE $(basename $CFG) $DEF
    fi
    echo "Running GerbMerge in $(dirname $CFG) with Config $CFG ..."
    $GERBMERGE $(basename $CFG)
    cd $TESTROOT
done
