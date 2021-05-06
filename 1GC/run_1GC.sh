#!/bin/bash
set -e

# Set alias for using casa python
casa-python=/soft/astro/casa/casa-6.1.0-118/bin/python3

# Create output folders if not exist
mkdir -p PLOTS
mkdir -p IMAGES
mkdir -p GAINPLOTS
mkdir -p GAINTABLES

MS=LSB1chav16
bpcal='J1939-6342'
apcal='J2329-4730'
target='J2339-5523'

ragavi_img=/.aux_mnt/pc002a/wagenveld/MeerKAT/Software_Images/stimela_ragavi_1.4.6-1.img

casa-python SCRIPTS/diagnostic_plots.py ${MS}.ms
casa-python SCRIPTS/flagging.py ${MS}.ms
casa-python SCRIPTS/do_1GC.py ${MS}.ms $bpcal $apcal $target

singularity exec --bind $PWD $ragavi_img python3 SCRIPTS/plot_gains.py

casa-python SCRIPTS/image_calibrators.py ${MS}.ms $bpcal $apcal
casa-python SCRIPTS/image_target.py ${MS}.ms $target
