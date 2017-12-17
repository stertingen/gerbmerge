## Introduction

The configuration file tells GerbMerge things like:

*   How much space to leave between jobs in the final panel
*   Whether or not to draw cut lines or crop marks, and on which layers
*   Whether or not to generate a fabrication drawing
*   The job names and files to be panelized
*   The output file names

Note that the configuration file does not specify layout of jobs on the panel. This layout is described by the [layout file](layoutfile.md). The layout of jobs on the panel may also be constructed automatically using the [automatic placement](autosearch.md) mode of operation.

## Help!

The rest of this document has a lot of information and it's easy to get overwhelmed. Users of GerbMerge complain that the configuration file is the biggest hurdle to overcome in using the program.

Don't panic. Start with a [sample configuration file](html/layout2.cfg) and modify it for your own jobs. The comments in the sample file will guide you through the process.

## Syntax Notes

The configuration file is a plain text file that can be created with any text editor. It is parsed using Python's [<tt>ConfigParser</tt>](http://docs.python.org/lib/module-ConfigParser.html) module. See the documentation for this module for a full description of supported syntax.

Note that comments in this file begin with a <tt>#</tt> character. Comments must occupy an entire line and must not have any characters before the '#' character, including blanks. Comments cannot be placed at the end of a line. For example:

    # This is correct...a comment occupies the entire line
        # Incorrect...comment preceded by blanks
    PanelWidth = 10.5   # This is INCORRECT...a comment cannot be placed at the end of a line

The configuration file has a standard "INI-style" syntax comprising:

* _Sections_ delimited by section names in square brackets (e.g., <tt>[Options]</tt>)
* _Assignments_ of the form '<tt>Name = Value</tt>'

The configuration file parser supports variable substitution. You can specify a common pathname prefix, for example, and substitute it in subsequent assignments, like this:

    [CPUBoard]
    Prefix = /home/user/eagle/cpuboard

    # Note the syntax '%(prefix)s' is a variable string substitution.
    # Even though we said 'Prefix = ...' we use LOWERCASE 'prefix' in the actual substitution!
    BoardOutline = %(prefix)s/cpu.bor
    Drills       = %(prefix)s/cpu.xln

* * *

**NOTE:** the parser converts all names you assign to into **lowercase letters only**.

* * *

In general, assignments are local to the section in which they reside, i.e., the names assigned to are not visible in the other sections. However, any assignments in the section named <tt>[DEFAULT]</tt> are visible in all sections. For example:

    [DEFAULT]
    EagleDir = /home/user/eagle

    [CPUBoard]
    Prefix = %(eagledir)s/cpuboard
    BoardOutline = %(prefix)s/cpu.bor
    Drills       = %(prefix)s/cpu.xln

    [IOBoard]
    Prefix = %(eagledir)s/ioboard
    BoardOutline = %(prefix)s/io.bor
    Drills       = %(prefix)s/io.xln

Have a look at the sample configuration files [<tt>layout1.cfg</tt>](layout1.cfg) and [<tt>layout2.cfg</tt>](layout2.cfg) for a quick overview of this file's syntax.

## Operating Parameters

The first section of the configuration file is called <tt>[Options]</tt>. This section specifies operating parameters for the job.

The following optional parameters are supported:

<dl>

<a name="ToolList"><dt>Tool List</dt></a>

<dd><tt>ToolList = /home/user/eagle/toollist.drl</tt>

**NOTE:** If you're using a recent version of Eagle or other modern PCB program, you can probably ignore this option. Try commenting it out and see what happens!

This parameter sets the default tool list (or "drill rack") in effect for jobs that (a) do not have embedded tool sizes in the Excellon file, and (b) do not have a tool list specified as part of the job description (see below).

As of Eagle version 4.11r2, tool sizes are embedded in the Excellon file, like this:

<pre>...
T01C0.032
T02C0.045
T03C0.115
...</pre>

For Excellon files with embedded tool sizes, no tool list file need be specified. Otherwise, a tool list file must be specified that contains something like:

<pre>T01 0.032in
T02 0.045in
T03 0.115in</pre>

Suffixes of 'mm' and 'mil' may be used instead of 'in' to indicate millimetres and mils.

Note that Eagle's CAM Processor uses two different forms of Excellon output devices, <tt>EXCELLON</tt> in which tool sizes are embedded in the drill file, and <tt>EXCELLON_RACK</tt> which requires an external tool list file, or drill rack. The latter may be desirable when you want to send your boards to a manufacturer with a limited set of drill sizes, or that charges by the number of different drill sizes used. In this case, do specify the <tt>ToolList</tt> option and set it to the drill rack you specified for the <tt>EXCELLON_RACK</tt> device.
</dd>

<a name="ExcellonDecimals"><dt>Excellon Decimals</dt></a>

<dd><tt>ExcellonDecimals = 4</tt>

This optional setting specifies the number of digits after the decimal point in the input Excellon drill files. These files contain (X,Y) drill locations specified as integers, but represent actual positions in the format <tt>M.N</tt> where there are <tt>M</tt> digits before the decimal point and <tt>N</tt> digits after. The default number of decimal digits is 4, hence a 2.4 integer format, so that the drill instruction <tt>X12300Y9400</tt> means to drill at (1.23", 0.94"). In 2.3 format (with <tt>ExcellonDecimals=3</tt>) the above would appear as <tt>X1230Y940</tt>. Note that it is assumed that leading 0's are omitted, or else no zeroes are omitted. Omitted trailing 0's are not yet supported.

As of this writing, older Eagle versions use a 2.3 format (prior to version 4.11r12), more recent Eagle versions use a 2.4 format, while Orcad and PCB use 2.4.

Note that each job may have its own <tt>ExcellonDecimals</tt> setting (see [below](#LocalExcellonDecimals)) to override this global setting.

Finally, note that the <tt>ExcellonDecimals</tt> option applies to the expected format for the **input** Excellon files, i.e., the drill files that GerbMerge reads in. The [<tt>ExcellonLeadingZeros</tt>](#ExcellonLeadingZeros) option below applies to the **output** Excellon file generated by GerbMerge.

<dt><a name="CutLineLayers">**Cut Line Layers**</a></dt>
<dd><tt>CutLineLayers = *toplayer,*bottomlayer</tt>

This parameter indicates which, if any, layers are to have cut lines drawn on them. Cut lines define the rectangular extents of each individual job on the panel. They are intended to help you in cutting out the individual jobs from the panel.

The value of this parameter is a list of layer names, which are defined for each job (see below). Layer names may be separated with commas or semicolons.

Note that **layer names must be written in lowercase letters**, even if they are defined with uppercase letters. Also note that all layer names except the board outline layer will begin with an asterisk '*'.

</dd>

This parameter may be omitted, or be set to <tt>None</tt> to indicate that no cut lines should be drawn.

<dt><a name="CropMarkLayers">Crop Mark Layers</a></dt>

<dd><tt>CropMarkLayers = *toplayer,*bottomlayer</tt>

This parameter indicates which, if any, layers are to have crop marks drawn on them. Crop marks are small L-shaped marks at the four corners of the final panel. Some board manufacturers require crop marks to ensure registration and to unambiguously define the extents of the job.

The value of this parameter is a list of layer names, which are defined for each job (see below). Layer names may be separated with commas or semicolons.

Note that **layer names must be written in lowercase letters**, even if they are defined with uppercase letters. Also note that all layer names except the board outline layer will begin with an asterisk '*'.

This parameter may be omitted, or be set to <tt>None</tt> to indicate that no crop marks should be drawn.

</dd>

<a name="FabricationDrawingFile"><dt>Fabrication Drawing File</dt></a>

<dd><tt>FabricationDrawingFile = fabdwg.ger</tt>

This optional parameter may be set to a filename, to 'none', or omitted entirely. When a valid filename is specified, GerbMerge will generate a Gerber RS274X file containing a fabrication drawing for the entire project. The drawing contains a box for the outline of the entire panel, dimension arrows for the panel, drill symbols for each drill hit, a drill tool legend, and optional user text. Some board manufacturers require a fabrication drawing.

The Fabrication Drawing Text option below allows you add user-defined text to this drawing.

Note that for generating a fabrication drawing, no more than 26 drill tools can appear in the merged output.

</dd>

<a name="FabricationDrawingText"><dt>Fabrication Drawing Text</dt></a>

<dd><tt>FabricationDrawingText = project/fabdwg.txt</tt>

This optional parameter may specify the name of a file containing plain text. Each line in the file is added to the fabrication drawing, if one is enabled.

</dd>

<a name="ExcellonLeadingZeros"><dt>ExcellonLeadingZeros</dt></a>

<dd><tt>ExcellonLeadingZeros = 0</tt>

This optional setting creates a merged Excellon output file with leading zeros. The default is to use leading-zero suppression. For example, with leading-zero suppression, a drill hit at location (1.23",4.56") would be written in the output Excellon file as:

    X12300Y45600

Without leading-zero suppression (i.e., with <tt>ExcellonLeadingZeros=1</tt>) it would appear as:

    X012300Y045600

Not using leading-zero suppression may make it easier for some Gerber viewers to properly interpret the Excellon file. Try setting <tt>ExcellonLeadingZeros=1</tt> if your drills appear in completely the wrong locations when viewing your merged output files in a Gerber viewer.

**DipTrace Users**

Try setting <tt>ExcellonLeadingZeros=diptrace</tt> if it looks like the holes are all at the wrong scale.

</dd>

Finally, note that the <tt>ExcellonLeadingZeros</tt> option applies to the format for the **output** Excellon file as generated by GerbMerge. The [<tt>ExcellonDecimals</tt>](#ExcellonDecimals) option described above applies to the **input** Excellon files read in by GerbMerge.<a name="OutlineLayerFile"></a>

<dt><a name="OutlineLayerFile">Outline Layer File</a></dt>

<dd><tt>OutlineLayerFile = project.oln</tt>

This optional parameter indicates that an additional output file (Gerber layer) is to be generated containing a rectangle that is drawn around the edges of the final panelized job. The value of this parameter is the name of the file. If 'none' is specified or this option is omitted, no outline file is generated.

This outline layer is useful in circuit board milling for defining the path extents of a contour router bit so that the entire panel may be cut out by the mill.

</dd>

<a name="ScoringFile"><dt>Scoring File</dt></a>

<dd><tt>ScoringFile = project.sco</tt>

This optional parameter indicates that an additional output file (Gerber layer) is to be generated containing scoring lines. These scoring lines describe the path for a scoring tool to make V-grooves in the board in between jobs, so that the jobs may be easily snapped apart. The value of this parameter is the name of the file. If 'none' is specified or this option is omitted, no scoring file is generated.

</dd>

<a name="ScoringStyle"><dt>Scoring Style</dt></a>
<dd><tt>ScoringStyle = edge-to-edge</tt>

The scoring lines can be drawn in two styles:

  # edge-to-edge - extends every scoring line to the board edges, this is appropriate if you are using a scoring machine which can only score right across a board, you must be careful with edge-to-edge if you are not using a strict grid of the same PCB in the same orientation for your panel, if you mix pcbs or orientations you can easily end up with a score line right through some of the PCBs on the panel.  Be sure to inspect your output gerber carefully!
  
  # surround - the scoring lines "surround" the indivudual boards, this is appropriate if you are manually cutting up your panel after manufacture and are not constrained to the limits of an automatic scoring machine.  Automatic scoring machines can almost certainly NOT score these lines, they can score only edge-to-edge.
</dd>

<a name="ScoringLineLayers"><dt>Scoring Line Layers</dt></a>
<dd><tt>ScoringLineLayers = *topsilkscreen,*bottomsilkscreen</tt></dd>

This optional parameter indicates that scoring lines (in addition to the ScoringFile if set) will be placed on the given layers, useful if your PCB fabricator isn't actually going to score the PCBs but you want to make silkscreen (or copper, or mask) lines to help you cut them up later.

The difference betweena "Scoring Line" and a "Cut Line" is that between two sub-pcbs there will be 1 scoring line right in the middle of the gap between them, but 2 cut lines excluding the gap in the middle.  In other words, a scoring line includes half the X/Y spacing in each pcb, a cut line excludes that spacing.

If you set the left/right/top/bottom margin to 1mm, and x/y spacing to 2mm plus the width of your saw blade, then using a scoring line will give you each pcb with 1mm border around all edges.
</dd>

<a name="ScoringLineWidth"><dt>Scoring Line Width</dt></a>
<dd><tt>ScoringLineWidth = 0.5</tt>

The width of the scoring line when drawn in the Scoring Line Layers, this does not affect the width of the line in the Scoring File.
</dd>

<a name="PanelWidthHeight"><dt>Panel Width/Height</dt></a>

<dd><tt>PanelWidth = 12.6</tt>  
<tt>PanelHeight = 7.8</tt>

These parameters set the dimensions of the board manufacturer's panels. An error message will be displayed if the panelized job exceeds these dimensions. You can change these settings to match the panel size of your board manufacturer, if you know it.

For [automatic placement](autosearch.html), the panel size defined by these settings constraint the random placements such that only placements that would fit on the panel are considered.

</dd>

<a name="Margins"><dt>Margins</dt></a>

<dd><tt>LeftMargin = 0.1</tt>  
<tt>RightMargin = 0.1</tt>  
<tt>TopMargin = 0.1</tt>  
<tt>BottomMargin = 0.1</tt>

These four parameters set the amount of extra space to leave around the edges of the panel to simplify tooling and handling. These margins default to 0" if not specified. These spacings will only be visible to the board manufacturer if you enable crop marks (see [CropMarkLayers](#CropMarkLayers) above) or use an [outline layer](#OutlineLayerFile).<a name="JobSpacing"></a>

</dd>

<dt><a name="JobSpacing">Job Spacing</a></dt>

<dd><tt>XSpacing = 0.125</tt>  
<tt>YSpacing = 0.125</tt>

These parameters set the job-to-job spacing in horizontal (X) and vertical (Y) directions. The default spacing is 0.125 inches if these parameters are not specified. Normally, both parameters will have the same value, but different values can be used to "tweak" a panel to exactly fit some dimensions.

</dd>

<a name="CutLineWidth"><dt>Cut Line Width</dt></a>

<dd><tt>CutLineWidth = 0.01</tt>

This optional parameter indicates the width of the line used to draw cut lines. If not specified, the default is 0.01".

</dd>

<a name="CropMarkWidth"><dt>Crop Mark Width</dt></a>

<dd><tt>CropMarkWidth = 0.01</tt>

This optional parameter indicates the width of the line used to draw crop marks. If not specified, the default is 0.01".

</dd>

<a name="AllowMissingLayers"><dt>Allow Missing Layers</dt></a>

<dd><tt>AllowMissingLayers = 0</tt>

This parameter may be set to either 0 or 1. When set to 0, all jobs must have the same layer names. This is the most common case. This parameter guards against misspelling of layer names and having them mistakenly placed on a different layer.

Some jobs, however, will have fewer or more layers. For example, mixing jobs that do and do not have surface-mount components may mean that some jobs will have solder mask layers and some will not. Setting <tt>AllowMissingLayers</tt> to 1 allows you to panelize such job mixtures. Take care, however, to [inspect the output carefully](index.html#Verifying) in this case to catch layer-name surprises.

</dd>

<a name="DrillClusterTolerance"><dt>DrillClusterTolerance</dt></a>

<dd><tt>DrillClusterTolerance = 0</tt>

This option is intended to reduce the number of drills in the output by eliminating drill sizes that are too close to make a difference. For example, it probably does not make sense to have two separate 0.031" and 0.0315" drills. The <tt>DrillClusterTolerance</tt> value specifies how much tolerance is allowed in drill sizes, in units of inches. Multiple drill tools that span twice this tolerance will be clustered into a single drill tool. For example, a set of 0.031", 0.0315", 0.032", and 0.034" drills will all be replaced by a single drill tool of diameter (0.031"+0.034")/2 = 0.0325". It is guaranteed that all original drill sizes will be no farther than <tt>DrillClusterTolerance</tt> from the drill tool size generated by clustering.

Setting <tt>DrillClusterTolerance</tt> to 0 (the default) disables clustering.

</dd>

<a name="MinimumFeatureSize"><dt>MinimumFeatureSize</dt></a>

<dd><tt>MinimumFeatureSize = None</tt>

Use this option to automatically thicken features on particular layers. This is intended for thickening silkscreen to some minimum width. The value of this option must be a comma-separated list of layer names followed by minimum feature sizes (in inches) for that layer. Comment this out to disable thickening. Example usage is:

    MinimumFeatureSize = *topsilkscreen,0.008,*bottomsilkscreen,0.008

</dd>

<a name="FiducialPoints"><dt>FiducialPoints</dt></a>

<dd><tt>FiducialPoints = None</tt>

Use this option to automatically add fiducials (little round markers used to aid in automatic component placement) to your final panel. This makes the most sense when you leave some [margins](#Margins) around your panel and place the fiducials on the margins.

The parameter to this option is a list of X,Y points at which to draw fiducials, relative to the edges of the final panel. Positive values are relative to the lower-left, while negative values are relative to the upper-right. For example:

    FiducialPoints = 0.125,0.125,-0.1,-0.1

would place one fiducial at (0.125,0.125) relative to the lower-left, and another fiducial a distance of (0.1,0.1) from the top-right of the final panel. To place a fiducial at the top-left of the final panel:

    FiducialPoints = 0.125,-0.125

The [<tt>FiducialCopperDiameter</tt>](#FiducialCopperDiameter) and [<tt>FiducialMaskDiameter</tt>](#FiducialMaskDiameter) options control the appearance of the fiducials.</dd>

<dt><a name="FiducialCopperDiameter">FiducialCopperDiameter</a></dt>

<dd><tt>FiducialCopperDiameter = 0.08</tt>

This option sets the diameter of fiducials. See the [<tt>FiducialPoints</tt>](#FiducialPoints) configuration option for more information.

</dd>

<a name="FiducialMaskDiameter"><dt>FiducialMaskDiameter</dt></a>

<dd><tt>FiducialMaskDiameter = 0.32</tt>

This option sets the diameter of the soldermask opening around fiducials. See the [<tt>FiducialPoints</tt>](#FiducialPoints) configuration option for more information.

</dd>

</dl>

<a name="Jobs"></a>
## Job Descriptions

Each input job is described in its own section. The job is described by providing file names for each layer. Layer names are up to you, but note the following:

* Layer names may be specified with lowercase and uppercase letters, but are converted to all-lowercase by GerbMerge. Note that this applies to layer names, not filenames.

* Each job must have at least a 'boardoutline' and 'drills' layer, specifying the Gerber board outline and Excellon drills layer, respectively.

* Each job may have an optional 'toollist' file specifying the tool list (or "drill rack") in effect for this job only. This setting overrides the global <tt>ToolList</tt> option, described above. If the Excellon file for the job has embedded tool sizes, this option is ignored.

* All layer names other than 'boardoutline' and 'drills' must begin with an asterisk '*' character.

Consider the following example:

    [CPUBoard]
    BoardOutline = /home/user/eagle/cpuboard/cpu.bor
    Drills       = /home/user/eagle/cpuboard/cpu.xln
    ToolList     = /home/user/eagle/cpuboard/tools.drl
    *TopLayer    = /home/user/eagle/cpuboard/cpu.cmp
    *BottomLayer = /home/user/eagle/cpuboard/cpu.sol
    *Silkscreen  = /home/user/eagle/cpuboard/cpu.plc

Job names (in square brackets) are fairly arbitrary and need not correspond to any file names. They must, however, comprise only letters, digits, and the underscore character. Furthermore, job names must begin with a letter. Job names, unlike layer names, are case sensitive.

Each assignment statement assigns a file name to a layer name. As mentioned above, the layer names 'boardoutline' and 'drills' are reserved and required. The optional 'toollist' layer is not an actual layer but an assignment that indicates the tool list in effect for this job. All other layer names are up to you and must begin with an asterisk '*'.

Make good use of variable substitutions (see the sample [<tt>layout1.cfg</tt>](layout1.cfg) and [<tt>layout2.cfg</tt>](layout2.cfg) files) to avoid typing the same pathname over and over.

In addition to specifying board layers, each job description can also have job-specific parameter assignments:

<dl>

<dt>Repeat</dt>

<dd><tt>Repeat = 3</tt>

This option is only used for [automatic placement](autosearch.md) and indicates the number of times this job is to appear in the final panel. For manual placement, this option is ignored. This option may be left unspecified in which case a repeat count of 1 is assumed.<a name="LocalExcellonDecimals"></a>

</dd>

<dt><a name="LocalExcellonDecimals">**ExcellonDecimals**</a></dt>

<dd><tt>ExcellonDecimals = 3</tt>

This option overrides the global [<tt>ExcellonDecimals</tt>](#ExcellonDecimals) setting in the <tt>[Options]</tt> section for this job only. This allows jobs with different Excellon decimal formats to be panelized. This option may be left unspecified in which case the global <tt>ExcellonDecimals</tt> setting is applied.

</dd>

</dl>

<a name="MergeOutputFiles"></a>
## Merge Output Files

GerbMerge combines data from multiple jobs grouped by layer. All of the "bottom copper" layers from all jobs, for example, will be combined into a single "bottom copper" file. The names of these combined output files can be set in the <tt>[MergeOutputFiles]</tt> section of the configuration file.

This section contains assignments of file names to layer names. The layer names must be the same as the ones specified in the [<tt>[Jobs]</tt>](#Jobs) section of the configuration file. All layer names must begin with an asterisk '*' except for the following four reserved layer names:

* <tt>BoardOutline</tt>
* <tt>Drills</tt>
* <tt>Placement</tt>
* <tt>ToolList</tt>

The first two reserved layer names are actual layers, while <tt>Placement</tt> refers to the placement file generated by GerbMerge containing positions of jobs on the final panel, and <tt>ToolList</tt> refers to the combined tool list file generated by GerbMerge.

Any assignment made in this section that does not begin with an asterisk or is not an assignment to one of the above four reserved names is considered a general variable assignment for future string substitution.

Here is an example:

    [MergeOutputFiles]
    Prefix = job1
    BoardOutline = %(prefix)s.bor
    Drills = %(prefix)s.xln
    *topcopper = %(prefix)s.cmp
    *bottomcopper = %(prefix)s.sol

If an assignment to a layer name is missing, GerbMerge will create the file <tt>merged.layername.ger</tt> where '<tt>layername</tt>' is the layer name. Default values for the four reserved names are <tt>merged.boardoutline.ger</tt> for the <tt>BoardOutline</tt> layer, <tt>merged.drills.xln</tt> for the <tt>Drills</tt> layer, <tt>merged.placement.txt</tt> for the <tt>Placement</tt> file, and <tt>merged.toollist.drl</tt> for the <tt>ToolList</tt> combined tool list file.

* * *

<center><font size="-1">© 2003-2011, Copyright by [Rugged Circuits LLC](http://ruggedcircuits.com); All Rights Reserved. mailto: [support@ruggedcircuits.com](mailto:support@ruggedcircuits.com?subject=GerbMerge)</font></center>
