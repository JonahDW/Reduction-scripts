import sys

ms = sys.argv[3]
sourcefield = sys.argv[4]
sourcename = sys.argv[5]

uvrange = '>500lambda'

#Initial imaging
tclean(vis=ms,
		imagename=sourcename+'_init',
		field = sourcefield,
		imsize=5120, #for 1 sq. degree field of view
		cell='1.5arcsec', #one fifth of the 6 arcsecond beam size
		uvrange = uvrange,
		gain=0.1,
		deconvolver='mtmfs',
		nterms=2,
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=0,
		niter=5000,
		mask = sourcename+'_mask.crtf',
		datacolumn = 'data',
		interactive=False)

exportfits(sourcename+'_init.image.tt0', sourcename+'_init.fits')