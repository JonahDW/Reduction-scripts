#!/bin/bash
set -e

MS=J2339-5523
# Path to sourcefinding script
sf_script=/.aux_mnt/pc002a/wagenveld/MeerKAT/Image_processing/sourcefinding.py

# Create directories if they don't exist
mkdir -p IMAGES
mkdir -p GAINTABLES

# Initial imaging
casa --nogui -c SCRIPTS/flagging.py ${MS}.ms
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 1000 'init'

# First phase calibration
python $sf_script mask IMAGES/${MS}_init.image.tt0 --spectral_index
casa --nogui -c SCRIPTS/insert_lsm.py ${MS}.ms IMAGES/${MS}_init_bdsfcat.fits

casa --nogui -c SCRIPTS/pcal.py ${MS}.ms '120a' 'GP0'
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 10000 'p0' IMAGES/${MS}_init_mask.crtf

# Second phase calibration
python $sf_script mask IMAGES/${MS}_p0.image.tt0 -s 1.5 --spectral_index
casa --nogui -c SCRIPTS/insert_lsm.py ${MS}.ms IMAGES/${MS}_p0_bdsfcat.fits

casa --nogui -c SCRIPTS/pcal.py ${MS}.ms '120s' 'GP1'
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 50000 'p1' IMAGES/${MS}_p0_mask.crtf

# Amplitude calibration
python $sf_script mask IMAGES/${MS}_p1.image.tt0 -s 2.0 --spectral_index
casa --nogui -c SCRIPTS/insert_lsm.py ${MS}.ms IMAGES/${MS}_p1_bdsfcat.fits

casa --nogui -c SCRIPTS/apcal.py ${MS}.ms '600s' 'GAP0' GAINTABLES/${MS}.GP1
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 100000 'ap0' IMAGES/${MS}_p1_mask.crtf

# Second amplitude calibration
python $sf_script mask IMAGES/${MS}_ap0.image.tt0 -s 2.5 --spectral_index
casa --nogui -c SCRIPTS/insert_lsm.py ${MS}.ms IMAGES/${MS}_ap0_bdsfcat.fits

casa --nogui -c SCRIPTS/apcal.py ${MS}.ms '600s' 'GAP1' GAINTABLES/${MS}.GP1
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 200000 'ap1' IMAGES/${MS}_ap0_mask.crtf
