## Introduction

</a>As an alternative to manual placement, either using the [layout file](layoutfile.html) approach or using the <tt>--place-file</tt> command-line option, GerbMerge can automatically try to find the best arrangement of jobs on a panel that minimizes the total panel area. Using automatic placement can save you time since you don't have to construct and experiment with a layout file. The tradeoff, however, is that automatic placement may take a long time to execute, and for panels with many, small jobs, the run time may be prohibitive. On the other hand, experience suggests that good results can be obtained in just a few minutes, even when GerbMerge is not allowed to search all possibilities.<a name="Random">

## Randomized Search

</a>

### The Basics

The randomized search approach has GerbMerge repeatedly place jobs randomly on a panel, possibly rotated. After each placement, GerbMerge evaluates the total area of the panel, and if it's less than the smallest area encountered so far, the placement is memorized as the best so far.

This may not sound like a very efficient approach but experience shows that it can lead to nearly-optimal results fairly quickly. The reason is that although there can be a huge number of possible placements for a given set of jobs, many of them are equivalent with respect to total panel area.

The randomized search approach is the default automatic placement method. It is invoked simply by not specifying any layout file:

<pre>

<center>gerbmerge file.cfg</center>

</pre>

The [configuration file](cfgfile.html) must still be specified, of course. After GerbMerge starts, you may press Ctrl-C at any time to stop the process. In fact, you must press Ctrl-C at some point as GerbMerge will try random placements forever.

The best layout found when Ctrl-C is pressed will be used for panelization. Note that the layout is also saved in the file specified by the <tt>Placement</tt> assignment in the <tt>[MergeOutputFiles]</tt> section of the [configuration file](cfgfile.html). Thus, if you want to experiment, you can run different trials, save the best placements from each, then use the best one by using the saved placement file as the input to GerbMerge with the <tt>--place-file</tt> option.

### Random+Exhaustive

The default operation of GerbMerge is to actually perform a hybrid search, using both random search and exhaustive search. By default, GerbMerge will take a list of N jobs and randomly place N-2 of them (randomly chosen). Then, GerbMerge will exhaustively try to place the remaining 2 jobs on the panel to minimize the area. This approach has been found to improve panel usage at minimal cost since an exhaustive search of only 2 jobs is very quick.

You can change the number of jobs to exhaustively search for a given random placement with the <tt>--rs-fsjobs</tt> command-line option. For example,

<pre>

<center>gerbmerge --rs-fsjobs=2 file.cfg</center>

</pre>

The above example is the default behavior, i.e., exhaustively place 2 jobs and randomly place N-2 jobs. By using a number higher than 2, there is less randomness but fewer starting placements are tested per second.<a name="Exhaustive">

## Exhaustive Search

</a>The exhaustive search approach has GerbMerge try all possible placements for a given set of jobs, one by one. This sounds like it may be an exponentially long approach, and it is. For anything other than a few boards (less than 5 or so), exhaustive search is prohibitive.

The exhaustive search mode is invoked as follows:

<pre>

<center>gerbmerge --full-search file.cfg</center>

</pre>

You can stop the search at any time by pressing Ctrl-C. The best placement found so far will be used for panelization and saved in the placement file specified by the <tt>Placement</tt> value in the <tt>[MergeOutputFiles]</tt> section of the [configuration file](cfgfile.html).<a name="Repeats">

## Multiple Instances

</a>There is no need to repeat sections of a job in the configuration file if you want a job to appear multiple times on a panel. You can use the <tt>Repeat=N</tt> configuration option to indicate that a particular job is to have N copies on a panel. For example:

    [irtx]
    Prefix=%(projdir)s/IRTransmitter/irtx
    *TopLayer=%(prefix)s.cmp
    *BottomLayer=%(prefix)s.sol
    Drills=%(prefix)s.xln
    BoardOutline=%(prefix)s.bor
    *SolderMaskTop=%(prefix)s.stc
    *SolderMaskBottom=%(prefix)s.sts
    **Repeat=5**

This job specifies all the layers as usual, then the last line indicates that 5 such jobs are to appear on the final panel. They may appear in various positions and states of rotation, however.<a name="Usage">

## Usage Notes

</a>

### Area Estimates

GerbMerge will estimate and display the maximum possible panel usage as a percentage. This estimate is frequently too high, as GerbMerge simply takes the area of each job, adds in the area required by inter-job spacing, then adds all of these areas together. The amount of that area that is used by actual jobs (and not inter-job spacing) represents the best possible area usage. This usage will clearly not be achieved unless all jobs magically fit together perfectly.

In summary, it is pointless to wait for a random search for hours to hit an estimated area utilization of 91% because, unless the dimensions of all boards line up just so, that utilization is not achievable.

### Panel Width and Height

Note that the <tt>PanelWidth</tt> and <tt>PanelHeight</tt> options in the [configuration file](cfgfile.html) constrain the search process. GerbMerge will not allow any placement, either by random search or exhaustive search, to exceed the panel dimensions. You can, therefore, guide the search process by choosing a panel size that is not too large, thus preventing highly-unlikely placements (think all jobs in one row) from being considered.

Similarly, by choosing panels that are slightly wider than taller, or vice versa, different placements can be considered and may lead to different results. Consider these two configuration file options as a source of experimentation.

### Time vs. Money

How long should you wait for the best possible area utilization? It depends... how much is your time worth?

If you've achieved 85% utilization for a 30 sq. in. board, what will you save by waiting and hoping for 90% (i.e., 28.3 sq. in.)? Assuming 64 cents/sq. in. ([BareBonesPCB.com](http://www.barebonespcb.com) cost), you will save $1.09.

* * *

<center><font size="-1">© 2003-2011, Copyright by [Rugged Circuits LLC](http://ruggedcircuits.com); All Rights Reserved. mailto: [support@ruggedcircuits.com](mailto:support@ruggedcircuits.com?subject=GerbMerge)</font></center>
