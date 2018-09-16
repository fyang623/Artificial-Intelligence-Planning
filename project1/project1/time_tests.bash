#!/bin/bash

###############################################################################
# time_tests.bash -- Dana Nau <nau@cs.umd.edu>, Mar 5, 2018
# -- updated March 9 to remove the bogus line "problems=(wall8a wall8b)".
#
# This is a bash script to gather data for part (c) of your experiments.
# You'll need to make some modifications to use it.


# Change this to use the pathname for your python program
python=/usr/local/bin/python3.6    # python pathname


# The list of heuristic functions to test. It assumes your heuristic functions
# are in a file named p1.py
heuristics=(heuristics.h_walldist heuristics.h_esdist heuristics.h_ff1 heuristics.h_ff2)


# For part (c) of your experiments, use the following problems in the order given.
problems=(wall8a wall8b rectwall8 rhook16a rhook16b spiral16 rectwall16 lhook16 rect20a rect20b rect20c rect20d rect20e spiral24 pdes30 pdes30b rect50)

# You can modify the script for use in part (a) and (b) of your experiments, by making
# the following changes.
# (1) use maketracks.py to create a file of randomly generated problems;
# (2) replace the above list of problems with the names of the problems in your file;
# (3) below, replace "sample_probs" with the rootname of your file;
# (4) in the call to Python below, replace "verbose=0" with "verbose=1" so that
#     fsearch.main will print the number of nodes generated.
# problems=(problem0 problem1 problem2 problem3 problem4 problem5 problem6 problem7 problem8 problem9 problem10 problem11 problem12 problem13 problem14 problem15 problem16 problem17 problem18 problem19 problem20 problem21 problem22 problem23 problem24 problem25 problem26 problem27 problem28 problem29 problem30 problem31 problem32 problem33 problem34 problem35 problem36 problem37 problem38 problem39)

# Do a time test for every combination of sample problem and search strategy
for heur in ${heuristics[*]}
do
    for prob in ${problems[*]}
    do
        echo ''
        echo "Time test of $heur on $prob"
        # string for setting everything up
        setup="import racetrack, sample_probs, heuristics"
        # code for doing a time test
        time_test="racetrack.main(sample_probs.$prob, 'gbf', $heur, verbose=1, draw=1)"
		${python} -m timeit -n 1 -r 1 -s "$setup" "$time_test"
		# ${python} -m timeit -s "$setup" "$time_test"
    done
done
