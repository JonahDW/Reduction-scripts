import sys

import casatasks as ct

msfile=sys.argv[1]
target=sys.argv[2]

ct.tclean(vis=msfile,
          datacolumn='corrected',
          field=target,
          spw='0',
          imagename='IMAGES/'+targe'_1GC',
          imsize=5120,
          cell='1.5arcsec',
          specmode='mfs',
          deconvolver='hogbom',
          gridder='standard',
          weighting='briggs',
          robust=0.0,
          niter=1000,
          interactive=False)

'''
viewer('IMAGES/J2339-5523_1GC.image',
       outfile='J2339-5523_1GC',
       outformat='png')
'''