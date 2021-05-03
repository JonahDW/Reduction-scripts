### Reduction-scripts

This is the home of some scripts I've been using for the reduction of MeerKAT data. 

Optimal usage is to place the scripts in the same directory as your measurement set, it will NOT make a copy but operate on the measurement set specified.

#### 1GC

Currently limited to the calibration of a single target, with corresponding bandpass/gain calibrator specified by the user. In principle only required editing is in `run_1GC.sh`, everything else will be handled by running `./run_1GC.sh` (modifying permissions may be necessary).

#### 2GC

More complete implementation of self-calibration, operating on a measurement set containg only the target source. In principle only required editing is in `run_2GC.sh`, everything else will be handled by running `./run_2GC.sh` (modifying permissions may be necessary). The script makes use of my sourcefinding scripts, which can be found at https://github.com/JonahDW/Image-processing. Please see all the instructions for making it work there.