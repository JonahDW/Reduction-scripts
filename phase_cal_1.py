import sys

ms = sys.argv[3]
sourcefield = sys.argv[4]
sourcename = sys.argv[5]

uvrange = '>500lambda'

#Second phase calibration
gaincal(vis=ms,
		field=sourcefield,
		uvrange=uvrange,
		caltable='cal_'+sourcename+'.GP1',
		refant = 'm002',
		solint='20s',
		solnorm=False,
		combine='',
		minsnr=3,
		calmode='p',
		parang=False,
		gaintable=[],
		gainfield=[],
		interp=[],
		append=False)

applycal(vis=ms,
		field=sourcefield,
		gaintable=['cal_'+sourcename+'.GP1'],
		calwt=False,
		parang=False,
		applymode='calonly',
		interp = ['nearest'])

#Clean again
tclean(vis=ms,
		imagename=sourcename+'_p1',
		imsize=5120, #for 1 sq. degree field of view
		cell='1.5arcsec', #one fifth of the 6 arcsecond beam size
		uvrange=uvrange,
		gain=0.2,
		deconvolver='mtmfs',
		nterms=2,
		scales=[0,1,5,15],
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=0,
		niter=10000,
		mask=sourcename+'_selfcal_mask.crtf',
		savemodel='modelcolumn',
		interactive=False)
