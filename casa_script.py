from astropy import units as u
from astropy.coordinates import SkyCoord

from astropy.table import Table

#Global variables
sourcename = 'J1833'
ms = 'J1833chav32.ms'
uvrange = '>500lambda'
sourcefield = '0'

cat_ra = 'RA(2000)'
cat_dec = 'DEC(2000)'
cat_intensity = 'PEAK INT'
cat_majax = 'MAJOR AX'
cat_minax = 'MINOR AX'
cat_pa = 'POSANGLE'

catalog = Table.read('../NVSS/CATALOG.FIT', format='fits')
catalog = catalog[catalog[cat_intensity] > 0.3] #Jy

catalog[cat_ra].unit = u.deg
catalog[cat_dec].unit = u.deg
catalog_coords = SkyCoord(ra=catalog[cat_ra],dec=catalog[cat_dec])

tb.open(ms+'/FIELD')
ref_coords = tb.getcol('REFERENCE_DIR')

c = SkyCoord(ref_coords[0,0,sourcefield]*u.rad, ref_coords[1,0,sourcefield]*u.rad)
idx = catalog_coords.separation(c) < 1*u.deg

catalog_matches = catalog[idx]
print(catalog_matches)

with open(sourcename+'_mask.crtf', 'w+') as f:
	f.write('#CRTFv0 \n\n')
	for match in catalog_matches:
		f.write('ellipse[[{0}deg,{1}deg], [{2}deg,{3}deg], {4}deg]\n'.format(match[cat_ra], match[cat_dec], match[cat_majax], match[cat_minax], match[cat_pa]))

#First run of clean
tclean(vis=ms,
		imagename=sourcename+'_init',
		imsize=5120, #for 1 sq. degree field of view
		cell='1.5arcsec', #one fifth of the 6 arcsecond beam size
		uvrange = uvrange,
		gain=0.1,
		deconvolver='mtmfs',
		nterms=2,
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=-0.5,
		niter=10000,
		threshold='30mJy',
		mask = sourcename+'_mask.crtf',
		interactive=False)

exportfits(sourcename+'_init.image.tt0', sourcename+'_init.fits')

'''
#Add components to model

image_cat = Table.read(sourcename+'_init_cat.fits', format='fits')
bright_src = image_cat[image_cat['Peak_flux'] > 0.05]

cl.done()
for source in bright_src:
	print(source['Peak_flux'])
	direction = "J2000 "+str(source['RA'])+"deg "+str(source['DEC'])+"deg"
	cl.addcomponent(dir = direction, flux = source['Peak_flux'], fluxunit='Jy', shape='point', spectrumtype='constant', freq=['TOPO','1.3GHz'])

cl.rename('model_components.cl')
cl.close()

ft(vis=ms, complist='model_components.cl')
'''

#First phase calibration
gaincal(vis=ms,
		field=sourcefield,
		uvrange=uvrange,
		caltable='cal_'+sourcename+'.GP0',
		refant = 'm002',
		solint='60s',
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
		gaintable=['cal_'+sourcename+'.GP0'],
		calwt=False,
		parang=False,
		applymode='calonly',
		interp = ['nearest'])

image_cat = Table.read(sourcename+'_init_cat.fits', format='fits')
bright_src = image_cat[image_cat['Peak_flux'] > 0.05]

with open(sourcename+'_selfcal_mask.crtf', 'w+') as f:
	f.write('#CRTFv0 \n\n')
	for match in bright_src:
		f.write('ellipse[[{0}deg,{1}deg], [{2}deg,{3}deg], {4}deg]\n'.format(match['RA'], match['DEC'], match['Maj'], match['Min'], match['PA']))

#Clean again
tclean(vis=ms,
		imagename=sourcename+'_p0',
		imsize=5120, #for 1 sq. degree field of view
		cell='1.5arcsec', #one fifth of the 6 arcsecond beam size
		uvrange=uvrange,
		gain=0.1,
		deconvolver='mtmfs',
		nterms=2,
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=-0.5,
		niter=10000,
		threshold='5mJy',
		mask=sourcename+'_selfcal_mask.crtf',
		savemodel='modelcolumn',
		interactive=False)

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
		gain=0.1,
		deconvolver='mtmfs',
		nterms=2,
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=-0.5,
		niter=10000,
		threshold='1mJy',
		mask=sourcename+'_selfcal_mask.crtf',
		savemodel='modelcolumn',
		interactive=False)

#Amplitude & phase calibration
gaincal(vis=ms,
		field=sourcefield,
		uvrange=uvrange,
		caltable='cal_'+sourcename+'.GAP0',
		refant = 'm002',
		solint='180s',
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
		gaintable=['cal_'+sourcename+'.GP1','cal_'+sourcename+'.GAP0'],
		calwt=False,
		parang=False,
		applymode='calonly',
		interp = ['nearest', 'linear'])

#Clean again
tclean(vis=ms,
		imagename=sourcename+'_ap0',
		imsize=5120, #for 1 sq. degree field of view
		cell='1.5arcsec', #one fifth of the 6 arcsecond beam size
		uvrange=uvrange,
		gain=0.2,
		deconvolver='mtmfs',
		nterms=2,
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=-0.5,
		niter=100000,
		mask=sourcename+'_selfcal_mask.crtf',
		savemodel='modelcolumn',
		interactive=False)

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
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=-0.5,
		niter=100000,
		mask=sourcename+'_selfcal_mask.crtf',
		interactive=False)


#Subtract model and see what is left
uvsub(vis=ms)

tclean(vis=ms,
		imagename=sourcename+'_uvsub',
		imsize=5120, #for 1 sq. degree field of view
		cell='1.5arcsec', #one fifth of the 6 arcsecond beam size
		uvrange=uvrange,
		gain=0.2,
		deconvolver='mtmfs',
		nterms=2,
		gridder='wproject',
		wprojplanes=128,
		weighting='briggs',
		robust=-0.5,
		niter=0,
		interactive=False)