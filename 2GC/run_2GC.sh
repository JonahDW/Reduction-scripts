#!/bin/bash
set -e

MS=J2339-5523

casa --nogui -c SCRIPTS/flagging.py ${MS}.ms
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 1000 'init'

python /.aux_mnt/pc002a/wagenveld/MeerKAT/Image_processing/sourcefinding.py mask IMAGES/${MS}_init.image.tt0 --spectral_index
casa --nogui -c SCRIPTS/insert_lsm.py ${MS}.ms IMAGES/${MS}_init_bdsfcat.fits

casa --nogui -c SCRIPTS/pcal.py ${MS}.ms 'inf' 'GP0'
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 10000 'p0' IMAGES/${MS}_init_mask.crtf

python /.aux_mnt/pc002a/wagenveld/MeerKAT/Image_processing/sourcefinding.py mask IMAGES/${MS}_p0.image.tt0 -s 1.5 --spectral_index
casa --nogui -c SCRIPTS/insert_lsm.py ${MS}.ms IMAGES/${MS}_p0_bdsfcat.fits

casa --nogui -c SCRIPTS/pcal.py ${MS}.ms '256s' 'GP1'
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 50000 'p1' IMAGES/${MS}_p0_mask.crtf

python /.aux_mnt/pc002a/wagenveld/MeerKAT/Image_processing/sourcefinding.py mask IMAGES/${MS}_p1.image.tt0 -s 2.0 --spectral_index
casa --nogui -c SCRIPTS/insert_lsm.py ${MS}.ms IMAGES/${MS}_p1_bdsfcat.fits

casa --nogui -c SCRIPTS/pcal.py ${MS}.ms '64s' 'GP2'
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 100000 'p2' IMAGES/${MS}_p1_mask.crtf

python /.aux_mnt/pc002a/wagenveld/MeerKAT/Image_processing/sourcefinding.py mask IMAGES/${MS}_p2.image.tt0 -s 2.5 --spectral_index
casa --nogui -c SCRIPTS/insert_lsm.py ${MS}.ms IMAGES/${MS}_p2_bdsfcat.fits

casa --nogui -c SCRIPTS/apcal.py ${MS}.ms '256s' GAINTABLES/${MS}.GP2
casa --nogui -c SCRIPTS/clean.py ${MS}.ms 200000 'ap0' IMAGES/${MS}_p2_mask.crtf