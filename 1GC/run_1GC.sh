#!/bin/bash
set -e

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

casa --nogui -c SCRIPTS/diagnostic_plots.py ${MS}.ms
casa --nogui -c SCRIPTS/flagging.py ${MS}.ms
casa --nogui -c SCRIPTS/do_1GC.py ${MS}.ms $bpcal $apcal $target

singularity exec --bind $PWD $ragavi_img python3 SCRIPTS/plot_gains.py

casa --nogui -c SCRIPTS/image_calibrators.py ${MS}.ms $bpcal $apcal
casa --nogui -c SCRIPTS/image_target.py ${MS}.ms $target