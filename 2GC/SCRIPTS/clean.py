import sys
import os

import casatasks as ct

msfile = sys.argv[1]
niters = int(sys.argv[2])
imname =  sys.argv[3]

try:
    mask_file = sys.argv[4]
except IndexError:
    mask_file = None

imagename = 'IMAGES/'+os.path.basename(msfile).split('.')[0]+'_'+imname

ct.tclean(vis=msfile,
          datacolumn='corrected',
          field='0',
          spw='0',
          imagename=imagename,
          imsize=5120,
          cell='1.5arcsec',
          deconvolver='mtmfs',
          scales=[0,2,3,5],
          nterms=2,
          gridder='wproject',
          wprojplanes=1024,
          weighting='briggs',
          robust=0.0,
          niter=niters,
          threshold='0.02mJy',
          mask=mask_file,
          interactive=False)
