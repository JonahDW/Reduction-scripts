import sys

ms = sys.argv[3]
sourcefield = sys.argv[4]
sourcename = sys.argv[5]

uvrange = '>500lambda'

uvsub(vis=ms)

#Initial imaging
tclean(vis=ms,
		imagename=sourcename+'_uvsub',
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
		niter=0,
		interactive=False)

uvsub(vis = ms, reverse = True)