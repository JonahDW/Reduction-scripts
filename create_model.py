import sys
from astropy.table import Table

ms = sys.argv[3]
sourcename = sys.argv[4]

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

with open(sourcename+'_selfcal_mask.crtf', 'w+') as f:
	f.write('#CRTFv0 \n\n')
	for match in bright_src:
		f.write('ellipse[[{0}deg,{1}deg], [{2}deg,{3}deg], {4}deg]\n'.format(match['RA'], match['DEC'], match['Maj'], match['Min'], match['PA']))