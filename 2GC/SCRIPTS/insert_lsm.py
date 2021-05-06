import os
import sys

from astropy.table import Table
from casatools import componentlist as cl

msfile = sys.argv[1]
catalog = sys.argv[2]

# Add components to model
image_cat = Table.read(catalog)
bright_src = image_cat[image_cat['Peak_flux'] > 0.01]

cl.done()

for source in bright_src:
    print(source['Total_flux'],source['alpha'])
    direction = "J2000 "+str(source['RA'])+"deg "+str(source['DEC'])+"deg"
    if source['alpha'] < 100:
        cl.addcomponent(dir=direction,
                        flux=source['Total_flux'],
                        fluxunit='Jy',
                        shape='point',
                        spectrumtype='spectral index',
                        index=source['alpha'],
                        freq=['TOPO','1.3GHz'])
    else:
        cl.addcomponent(dir=direction,
                flux=source['Total_flux'],
                fluxunit='Jy',
                shape='point',
                spectrumtype='spectral index',
                index=-1.0,
                freq=['TOPO','1.3GHz'])

clname = os.path.basename(catalog).split('.')[0] + '.cl'
cl.rename(clname)
cl.close()

ft(vis=msfile, complist=clname)