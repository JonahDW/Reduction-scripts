import bdsf
import sys

sourcename = sys.argv[1]

#Run PyBDSF
img = bdsf.process_image(sourcename+'_init.fits',
						psf_vary_do = True,
						rms_map = None,
						adaptive_rms_box = True,
						group_by_isl = True,
						ini_gausfit = 'simple',
						adaptive_thresh = 20.0,
						thresh_pix = 10.0,
						thresh_isl = 5.0)
img.show_fit()

img.write_catalog(outfile = sourcename+'_init_cat.fits', 
				  clobber = True, 
				  format = 'fits', 
				  catalog_type = 'srl')
