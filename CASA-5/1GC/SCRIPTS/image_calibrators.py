from sys import argv
msfile=argv[3]

bpcal=argv[4]
apcal=argv[5]

fluximage = 'flux_calib_1GC'
apimage = 'ap_calib_1GC'

#Image flux calibrator
tclean(vis=msfile,
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
       robust=-0.5,
       niter=0,
       interactive=False)

viewer('IMAGES/'+fluximage+'.image',
       outfile=fluximage,
       outformat='png')

# Image amp/phase calibrator
tclean(vis=msfile,
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
       robust=-0.5,
       niter=0,
       interactive=False)

viewer('IMAGES/'+apimage+'.image',
       outfile=apimage,
       outformat='png')