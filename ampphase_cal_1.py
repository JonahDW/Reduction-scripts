import sys

ms = sys.argv[3]
sourcefield = sys.argv[4]
sourcename = sys.argv[5]

uvrange = '>500lambda'

#Second amplitude & phase calibration
gaincal(vis=ms,
		field=sourcefield,
		uvrange=uvrange,
		caltable='cal_'+sourcename+'.GAP1',
		refant = 'm002',
		solint='60s',
		solnorm=False,
		combine='',
		minsnr=3,
		calmode='ap',
		parang=False,
		gaintable=['cal_'+sourcename+'.GP1'],
		gainfield=[],
		interp=[],
		append=False)

applycal(vis=ms,
		field=sourcefield,
		gaintable=['cal_'+sourcename+'.GP1','cal_'+sourcename+'.GAP1'],
		calwt=False,
		parang=False,
		applymode='calonly',
		interp = ['nearest', 'linear'])

#Clean again
tclean(vis=ms,
		imagename=sourcename+'_ap1',
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
		robust=-0.5,
		niter=100000,
		mask=sourcename+'_selfcal_mask.crtf',
		savemodel='modelcolumn',
		interactive=False)