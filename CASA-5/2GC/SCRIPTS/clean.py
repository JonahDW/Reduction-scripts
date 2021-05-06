from sys import argv
import os

msfile = argv[3]
niters = int(argv[4])
imname =  argv[5]

try:
    mask_file = argv[6]
except IndexError:
    mask_file = "circle[[2560pix,2560pix],10pix]"

imagename = 'IMAGES/'+os.path.basename(msfile).split('.')[0]+'_'+imname

tclean(vis=msfile,
       datacolumn='corrected',
       field='0',
       spw='0',
       imagename=imagename,
       imsize=5120,
       cell='1.5arcsec',
       deconvolver='mtmfs',
       nterms=2,
       gridder='wproject',
       wprojplanes=1024,
       weighting='briggs',
       robust=0.0,
       niter=niters,
       threshold='0.02mJy',
       mask=mask_file,
       interactive=False)
