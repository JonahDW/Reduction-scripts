ms = 'J1833chav32.ms'
sourcefield = 0
sourcename = 'J1833'

uvrange = '>500lambda'

#Clean again
tclean(vis=ms,
		imagename=sourcename+'_IQ',
		field = sourcefield,
		imsize=5120, #for 1 sq. degree field of view
		cell='1.5arcsec', #one fifth of the 6 arcsecond beam size
		stokes='IQ',
		uvrange=uvrange,
		gain=0.2,
		deconvolver='mtmfs',
		nterms=2,
		scales=[0,1,5,15],
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=-0.5,
		niter=100000,
		mask=sourcename+'_selfcal_mask.crtf',
		interactive=False)

exportfits(sourcename+'_IQ.image.tt0', sourcename+'_IQ.fits')