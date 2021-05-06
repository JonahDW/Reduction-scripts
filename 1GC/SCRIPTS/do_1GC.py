import sys
import os

import casatasks as ct

msfile=sys.argv[1]

msname = os.path.basename(msfile).split('.')[0]

ktab0 = 'GAINTABLES/1GC_'+msname+'.K0'
gtab0 = 'GAINTABLES/1GC_'+msname+'.G0'
gtab1 = 'GAINTABLES/1GC_'+msname+'.G1'
gtab2 = 'GAINTABLES/1GC_'+msname+'.G2'

bptab = 'GAINTABLES/1GC_'+msname+'.B0'
fluxtab = 'GAINTABLES/1GC_'+msname+'.F0'

# Global parameters
refant = 'm001'
bpcal = sys.argv[2]
apcal = sys.argv[3]
target = sys.argv[4]

calchan = '0:1250'

#------------------Primary calibrator------------

# Set the flux of the flux calibrator
ct.setjy(vis=msfile,
         field=bpcal,
         scalebychan=True,
         standard='Stevens-Reynolds 2016',
         fluxdensity=-1)

# Do delay calibration
ct.gaincal(vis=msfile,
           caltable=ktab0,
           field=bpcal,
           refant=refant,
           gaintype='K',
           solint='inf')

# Do gain calibration
ct.gaincal(vis=msfile,
           caltable=gtab0,
           field=bpcal,
           spw=calchan,
           refant=refant,
           gaintype='G',
           calmode='p',
           solint='inf',
           gaintable=[ktab0],
           minsnr=2.0)

ct.bandpass(vis=msfile,
            caltable=bptab,
            field=bpcal,
            refant=refant,
            solint='inf',
            solnorm=True,
            interp=['nearest','linear'],
            gaintable=[ktab0,gtab0])

# Apply calibration and image the flux calibrator
ct.applycal(vis=msfile,
            gaintable=[ktab0,gtab0,bptab],
            field=bpcal,
            calwt=False)

#-----------------Secondary calibrator----------

ct.gaincal(vis=msfile,
           caltable=gtab1,
           field=(',').join((bpcal,apcal)),
           spw=calchan,
           refant=refant,
           gaintype='G',
           calmode='p',
           solint='60s',
           minsnr=2.0,
           gaintable=[ktab0,bptab])

ct.gaincal(vis=msfile,
           caltable=gtab2,
           field=(',').join((bpcal,apcal)),
           spw=calchan,
           refant=refant,
           gaintype='G',
           calmode='ap',
           solint='inf',
           minsnr=2.0,
           gaintable=[ktab0,bptab,gtab1],
           interp=['nearest','linear','linear'])

# Set flux scale of gain table to flux calibrator
ct.fluxscale(vis=msfile,
             caltable=gtab2,
             fluxtable=fluxtab,
             reference=bpcal)

# Apply calibration to secondary
ct.applycal(vis=msfile,
            gaintable=[ktab0, bptab, gtab1, fluxtab],
            field=apcal,
            gainfield=[bpcal,bpcal,apcal,apcal],
            interp=['nearest','nearest','linear','linear'],
            calwt=False)

#------------------Target----------

# Apply calibration to target
ct.applycal(vis=msfile,
            gaintable=[ktab0, bptab, gtab1, fluxtab],
            field=target,
            gainfield=[bpcal,bpcal,apcal,apcal],
            interp=['nearest','nearest','linear','linear'],
            calwt=False)