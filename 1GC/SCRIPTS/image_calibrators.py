import sys

import casatasks as ct
from casaviewer import msview

msfile=sys.argv[1]
bpcal=sys.argv[2]
apcal=sys.argv[3]

fluximage = 'flux_calib_1GC'
apimage = 'ap_calib_1GC'

#Image flux calibrator
ct.tclean(vis=msfile,
          datacolumn='corrected',
          stokes='IQ',
          field=bpcal,
          spw='0',
          imagename='IMAGES/'+fluximage,
          imsize=5120,
          cell='0.5arcsec',
          specmode='mfs',
          deconvolver='hogbom',
          gridder='standard',
          weighting='briggs',
          robust=0.0,
          niter=0,
          interactive=False)

msview('IMAGES/'+fluximage+'.image',
       outfile=fluximage,
       outformat='png')

# Image amp/phase calibrator
ct.tclean(vis=msfile,
          datacolumn='corrected',
          stokes='IQ',
          field=apcal,
          spw='0',
          imagename='IMAGES/'+apimage,
          imsize=5120,
          cell='0.5arcsec',
          specmode='mfs',
          deconvolver='hogbom',
          gridder='standard',
          weighting='briggs',
          robust=0.0,
          niter=0,
          interactive=False)

msview('IMAGES/'+apimage+'.image',
       outfile=apimage,
       outformat='png')