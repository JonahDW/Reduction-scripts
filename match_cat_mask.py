from astropy import units as u
from astropy.coordinates import SkyCoord

from astropy.table import Table
import sys

#Global variables
ms = sys.argv[3]
sourcefield = sys.argv[4]
sourcename = sys.argv[5]

uvrange = '>500lambda'

cat_ra = 'RA(2000)'
cat_dec = 'DEC(2000)'
cat_intensity = 'PEAK INT'
cat_majax = 'MAJOR AX'
cat_minax = 'MINOR AX'
cat_pa = 'POSANGLE'

catalog = Table.read('/.aux_mnt/pc002a/wagenveld/MeerKAT/NVSS/CATALOG.FIT', format='fits')
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