# GerbMerge

## Warning!

Don't use version 1.10 in production environments. It is currently highly broken! Use the 1.9.5 or 1.9.4 version, which is considered kind of stable. (Branch 1.9.5-dev)

## What's New

In release 1.10.0 (mostly broken!)

* Auto-detect if a file is in metric or imperial units and convert measurements to target unit
* Better KiCAD support
* Some scoring features

In release 1.9.5 (stable-ish version, use this one!)

* Set interpreter to python2 for Archlinux compatibility

In release 1.9.4

* Metric support fixed and tested with Diptrace
* Support for Cygwin environment
* Fixed Windows installation
* Some Gerber parsing fixes

In release 1.9

* Added metric support
* Added default timeout for random tile placement
* Added DipTrace support
* Use boardoutline files (when present) to build cutlines in silkscreen layers instead of the default calculated algorithm. This change permits non-rectangular board outlines.

In release 1.8:

* Released under more recent GPL v3 license
* Summary statistics prints out smallest drill tool diameter
* Added [<tt>FiducialPoints</tt>](doc/cfgfile.md#FiducialPoints), [<tt>FiducialCopperDiameter</tt>](doc/cfgfile.md#FiducialCopperDiameter), and [<tt>FiducialMaskDiameter</tt>](doc/cfgfile.md#FiducialMaskDiameter) configuration options
* Added option to write fiducials to final panel
* Scoring lines now go all the way across a panel

In release 1.7:

* Added a new command-line option <tt>--search-timeout</tt> to time-limit the automatic placement process.
* Added preliminary support for a GUI controller interface.

## Introduction

GerbMerge is a program for combining (panelizing) the CAM data from multiple printed circuit board designs into a single set of CAM files. The purpose of doing so is to submit a single job to a board manufacturer, thereby saving on manufacturing costs.

GerbMerge currently works with:

* CAM data generated by the [Eagle](http://www.cadsoft.de), [DipTrace](http://www.diptrace.com) and [KiCAD](http://kicad-pcb.org/) circuit board design programs, with "best effort" support for Orcad, Protel, and [PCB](http://www.sourceforge.net/projects/pcb)
* Artwork in Gerber RS274-X format
* Drill files in Excellon format

Here are two samples of the program's output. These samples demonstrate panelizing multiple, different jobs, and also demonstrate board rotation.

<a href="doc/img/sample.jpg"><img src="doc/img/sample.jpg" alt="sample 1" height=300></img></a>
<a href="doc/img/sample2.jpg"><img src="doc/img/sample2.jpg" alt="sample 2" height=300></img></a>

## Requirements

GerbMerge is written in pure [Python](http://www.python.org). It depends upon the following packages for operation:

* [Python](http://www.python.org) version 2.4 or later, version 3.x is not supported!
* [SimpleParse](http://simpleparse.sourceforge.net) version 2.1.0 or later
* [Unum](http://home.scarlet.be/be052320/Unum.html) version 4.1.3 or later

All of the above packages come with easy installation programs for both Windows, Mac OS X, and Linux. ## Automatic Installation with PIP This repository can generate a tarball for installation with PIP. In the repository, run:

    $ python setup.py sdist
    $ pip install dist/gerbmerge-1.10.0.tar.gz
    
PIP will automatically resolve the dependencies. `-1.10.0` will change with the current tool version. To easily run the installed package without looking up your python path, use python's "run module as script" feature: ``` $ python -m gerbmerge <args>```</args>

## Installation

### Windows / Cygwin

Install Cygwin with _python_, _python-setuptools_, and _gcc_ packages (gcc is needed for simpleparse). Launch Cygwin shell and install _pip_, then _simpleparse_:

    easy_install-x.y pip
    pip install simpleparse

(x.y is the current Python version)

Download and unpack _gerbmerge_ sources, navigate to its folder in Cygwin shell and run:

    python setup.py sdist
    pip install dist/gerbmerge-1.9.4.tar.gz

Now you can use it by running _gerbmerge_ in Cygwin shell.

To uninstall gerbmerge, launch Cygwin shell and run:

    pip uninstall gerbmerge

### Windows (native)

[Download](https://www.python.org/downloads/release/python-2711/) and install Python-2.7, _pip_ will be installed too. Assuming Python installation folder is C:\Python27, open command propmt and run:

    cd c:\python27\
    scripts\pip.exe install simpleparse

Download and unpack _gerbmerge_ sources, navigate to its folder and run:

    c:\python27\python.exe setup.py sdist
    c:\python27\scripts\pip.exe istall dist\gerbmerge-1.9.4.zip

Now you can use it by running _c:\python27\gerbmerge.bat_ in command prompt.

To uninstall gerbmerge, launch command prompt and run:

    c:\python27\scripts\pip.exe uninstall gerbmerge

### Unix / Mac OS X

Install python, gcc (required to build simpleparse), and pip (recommended)

Launch shell and install _simpleparse_:

    sudo pip install simpleparse

Download and unpack _gerbmerge_ sources, navigate to its folder and run:

    python setup.py sdist
    sudo pip istall dist/gerbmerge-1.9.4.tar.gz

Now you can use it by running _gerbmerge_.

To uninstall gerbmerge, open shell and run:

    sudo pip uninstall gerbmerge

## Running GerbMerge

### Windows / Cygwin

Launch Cygwin shell and type

    gerbmerge

### Windows (native)

Open a DOS command prompt and laucnh gerberge.bat file:

    c:\python27\gerbmerge.bat

### Unix / Mac OS X

Open shell and type

    gerbmerge

### Operation

There are three ways to run GerbMerge:

1.  By manually specifying the relative placement of jobs
2.  By manually specifying the absolute placement of jobs
3.  By letting GerbMerge automatically search for a placement that minimizes total panel area

#### Manual Relative Placement

For the manual relative placement approach, GerbMerge needs two input text files:

* The _configuration file_ specifies global options and defines the jobs to be panelized

* The _layout file_ specifies how the jobs are to be laid out.

The names of these files are the two required parameters to GerbMerge:

    gerbmerge file.cfg file.def

The following links describe the contents of the [configuration file](doc/cfgfile.md) and [layout file](doc/layoutfile.md).

#### Manual Absolute Placement

For the manual absolute placement approach, GerbMerge also needs the configuration file as well as another text file that specifies where each job is located on the panel and whether or not it is rotated:

    gerbmerge --place-file=place.txt file.cfg

The <tt>place.txt</tt> file looks something like:

    job1 0.100 0.100
    cpu 0.756 0.100
    cpu*rotated 1.35 1.50

This method of placement is not meant for normal use. It can be used to recreate a previous invocation of GerbMerge, since GerbMerge saves its results in a text file (whose name is set in the [<tt>[MergeOutputFiles]</tt>](doc/cfgfile.#MergeOutputFiles) section of the configuration file) after every run. Thus, you can experiment with different parameters, save a placement you like, do some more experimentation, then return to the saved placement if necessary.

Alternatively, this method of placement can be used with third-party back ends that implement intelligent auto-placement algorithms, using GerbMerge only for doing the actual panelization.

#### Automatic Placement

For the [automatic placement](doc/autosearch.md) approach, GerbMerge only needs the configuration file:

    gerbmerge file.cfg

Command-line options can be used to modify the search algorithm. See the [Automatic Placement](doc/autosearch.md) page for more information.

### Input File Requirements

GerbMerge requires the following input CAM files:

* Each job must have a Gerber file describing the board outline, which is assumed rectangular. In Eagle, a board outline is usually generated from the Dimension layer. This board outline is a width-0 line describing the physical extents of the board. If you're not using Eagle, you don't have to generate a width-0 rectangle, but GerbMerge does need to use some Gerber layer to determine the extents of the board. GerbMerge will take the maximum extents of all drawn objects in this layer as the extents of the board.

* Each job must have an Excellon drill file.

* Each job can have any number of optional Gerber files describing copper layers, silkscreen, solder masks, etc.

* All files must have the same offset and must be shown looking from the top of the board, i.e., not mirrored.

* Each job may have an optional tool list file indicating the tool names used in the Excellon file and the diameter of each tool. This file is not necessary if tool sizes are embedded in the Excellon file. A typical tool list file looks like:

<pre>T01 0.025in
T02 0.032in
T03 0.045in</pre>
    
## Verifying the Output

Before sending your job to be manufactured, it is imperative that you verify the correctness of the output. Remember that GerbMerge comes with NO WARRANTY. Manufacturing circuit boards costs real money and a single mistake can render an entire lot of boards unusable.

I recommend the following programs for viewing the final output data. Take the time to become very familiar with at least one of these tools and to use it before every job you send out for manufacture.

<dl>

<dt>gerbv</dt>

<dd>

For Linux, the best option (currently) for viewing Gerber and Excellon files is the [gerbv](http://gerbv.sourceforge.net) program. Simply type in the names of all files generated by GerbMerge as parameters to <tt>gerbv</tt>:

    gerbv merged.*.ger merged.*.xln

</dd>

<dt>GC-Prevue</dt>

<dd>

For Windows, [GC-Prevue](http://www.graphicode.com) is a good program that I have used often. It is a free program. GraphiCode makes lots of other, more powerful Gerber manipulation and viewing programs but they are quite pricey ($495 and up).

</dd>

<dt>ViewMate</dt>

<dd>
    
Another free Windows program, [ViewMate](http://www.pentalogix.com) is similar to GC-Prevue. I have not used ViewMate much, but that is mostly due to familiarity with GC-Prevue. The two programs are comparable, although I'm sure that someone who is much more familiar with both could point out some differences.

</dd>

</dl>

## Limitations

* This program has mainly been tested with output from Eagle CAD and Diptrace programs. Limited testing has been performed with Orcad, Protel, and PCB. Other CAD programs will NOT WORK with a very high probability, as the input parser is quite primitive.

If you have the need/motivation to adapt GerbMerge to other CAD programs, have a look at the <tt>gerber2pdf</tt> program. It is written in Python and implements a much more complete RS274-X input file parser. Combining GerbMerge with <tt>gerber2pdf</tt> should be a fairly simple exercise. Also, feel free to send us samples of Gerber/Excellon output of your CAD tool and we'll see if we can add support for it.

* This program handles apertures that are rectangles, ovals, circles, macros without parameters or operators, and Eagle octagons (which are defined using a macro with a single parameter, hence currently handled as a special case).

* The panelizing capabilities of this program do not allow for arbitrary placement of jobs, although there is a fair amount of flexibility.

* All jobs are assumed to be rectangular in shape. Non-rectangular jobs can be handled but will lead to wasted space in the final panel.

* A maximum of 26 different drill sizes is supported for generating a fabrication drawing.

## Program Options

<dl>

<dt>--octagons=normal</dt>

<dt>--octagons=rotate</dt>

<dd>The <tt>--octagons</tt> option affects how the octagon aperture is defined in the output files. The parameter to this option must either be <tt>rotate</tt> or <tt>normal</tt>. Normally, octagons begin at an angle of 22.5 degrees, but some Gerber viewers have a problem with that (notably CircuitMaker from LPKF). These programs expect octagons to begin at 0.0 degrees.

The <tt>--octagons=normal</tt> option is the default (22.5 degrees) and need not be specified. A rotation of 0.0 degrees can be achieved by specifying <tt>--octagons=rotate</tt>.

</dd>

<dt>--random-search</dt>

<dd>This option is the default when only a configuration file is specified (see the documentation on [Automatic Placement](autosearch.html) for more information). It indicates that a randomized search of possible job tilings is to be performed. This option does not make sense when a layout file is specified.</dd>

<dt>--full-search</dt>

<dd>This option may be specified to indicate that all possible job tilings are to be searched (see the documentation on [Automatic Placement](autosearch.html) for more information). This option does not make sense when a layout file is specified.</dd>

<dt>--rs-fsjobs=N</dt>

<dd>This option is used with randomized search to indicate how many jobs are to undergo full search for each tiling. See the documentation on [Automatic Placement](autosearch.html) for more information.</dd>

<dt>--place-file=filename</dt>

<dd>This option performs a panel layout based upon absolute job positions in the given text file, rather than by random/full search or by a layout file. The placement file created by GerbMerge can be used as an input file to this option in order to recreate a previous layout.</dd>

<dt>--no-trim-gerber</dt>

<dd>This option prevents GerbMerge from trying to trim all Gerber data to lie within the extents of a given job's board outline. Normally, GerbMerge will try to do so to prevent one job's Gerber data (most notably, silkscreen lines for connectors that protrude from the board) from interfering with a neighboring job on the final panel. Specify this command-line option if you do not want this trimming to occur.</dd>

<dt>--no-trim-excellon</dt>

<dd>This option prevents GerbMerge from trying to trim all Excellon data to lie within the extents of a given job's board outline. Normally, GerbMerge will try to do so to prevent one job's drill holes from landing in the middle of a neighboring job on the final panel. Specify this command-line option if you do not want this trimming to occur.</dd>

<dt>--search-timeout=seconds</dt>

<dd>When random placements are used, this option can be used to automatically terminate the search process after the specified number of seconds. If the number of seconds is 0 or this option is not specified, then random placements are tried forever, until Ctrl-C is pressed to stop the process and keep the best placement so far.</dd>

<dt>-h, --help</dt>

<dd>The '<tt>-h</tt>' or '<tt>--help</tt>' option prints a brief summary of available options.</dd>

<dt>-v, --version</dt>

<dd>The '<tt>-v</tt>' or '<tt>--version</tt>' option prints the current program version and author contact information.</dd>

</dl>

## Examples

Example layout config files and gerber files (both original and merged) can be found in gerbmerge/examples folder

## Copyright & License

This repo is a fork of gerbmerge, version 1.9.4 from unwireddevices.com, with additional patches py Hermann

Copyright © 2016 [Unwired Devices LLC](http://www.unwireddevices.com).

This repo is a fork of gerbmerge, version 1.9 from ProvideYourOwn.com, with additional patches by Ian Hartwig and Paulo Henrique Silva

Copyright © 2013 [ProvideYourOwn.com](http://provideyourown.com). All Rights Reserved.

This repo is a fork of gerbmerge, version 1.8 from Rugged Circuits LLC:

Copyright © 2011 [Rugged Circuits LLC](http://ruggedcircuits.com). All Rights Reserved. mailto: [support@ruggedcircuits.com](mailto:support@ruggedcircuits.com?subject=GerbMerge)

GerbMerge comes with ABSOLUTELY NO WARRANTY. This is free software licensed under the terms of the [GNU General Public License](gpl.html) Version 3\. You are welcome to copy, modify and redistribute this software under certain conditions. For more details, see the LICENSE file or visit [The Free Software Foundation](http://www.fsf.org).

## To Do

1.  Proper metric/inch support: parse files with arbitrary units, output files with units specified in the config
2.  Accept outputs from more CAD programs
3.  A graphical interface for interactive placement
4.  Better reporting of parse errors in the layout and configuration files
5.  Implement simple primitive for panelizing a single job in an array
6.  More intelligent placement algorithms, possibly based on the fabric cutting problem.
7.  Accept aperture macro parameters and operators
8.  HPGL output for miling

## Credits

Thanks to Jace Browning for major contributions to this code. This help file is based on a template for the help file for mxTools by [M.A. Lemburg](http://starship.python.net/crew/lemburg). This software was created with [VIM](http://www.vim.org/); thanks to the authors of this program and special thanks for the Python syntax support. Thanks to M.A. Lemburg for his [mxBase](http://www.egenix.com/files/python/eGenix-mx-Extensions.html) package, Mike Fletcher for his [SimpleParse](http://simpleparse.sourceforge.net) package, and the authors of [gerbv](http://gerbv.sourceforge.net), a great Gerber file viewer for Linux/Mac OS X, and, of course, to the [Python](http://www.python.org) developers and support community.

Thanks to Joe Pighetti for making me start writing this program, and to the Grand Valley State University Firefighting Robot Team for making me finish it.

Thanks to Matt Kavalauskas for identifying Eagle's annulus and thermal macros and supporting the development of the aperture macro code.

* * *

Portions (versoin 1.9.4 & prior): Copyright © 2016 [Unwired Devices LLC](http://www.unwireddevices.com). All Rights Reserved.

Portions (version 1.9.3 & prior): Copyright © 2013 [ProvideYourOwn.com](http://provideyourown.com). All Rights Reserved.

Portions (version 1.8 & prior): Copyright © 2003-2011, Copyright by [Rugged Circuits LLC](http://ruggedcircuits.com); All Rights Reserved. mailto: [support@ruggedcircuits.com](mailto:support@ruggedcircuits.com?subject=GerbMerge)

