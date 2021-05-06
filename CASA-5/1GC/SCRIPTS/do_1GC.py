from sys import argv
msfile=argv[3]

msname = os.path.basename(msfile).split('.')[0]

ktab0 = 'GAINTABLES/1GC_'+msname+'.K0'
gtab0 = 'GAINTABLES/1GC_'+msname+'.G0'
gtab1 = 'GAINTABLES/1GC_'+msname+'.G1'
gtab2 = 'GAINTABLES/1GC_'+msname+'.G2'

bptab = 'GAINTABLES/1GC_'+msname+'.B0'
fluxtab = 'GAINTABLES/1GC_'+msname+'.F0'

# Global parameters
refant = 'm001'
bpcal = argv[4]
apcal = argv[5]
target = argv[5]

calchan = '0:1250'

#------------------Primary calibrator------------

# Set the flux of the flux calibrator
setjy(vis=msfile,
       field=bpcal,
       scalebychan=True,
       standard='Stevens-Reynolds 2016',
       fluxdensity=-1)

# Do delay calibration
gaincal(vis=msfile,
       caltable=ktab0,
       field=bpcal,
       refant=refant,
       gaintype='K',
       solint='inf')

# Do gain calibration
gaincal(vis=msfile,
       caltable=gtab0,
       field=bpcal,
       spw=calchan,
       refant=refant,
       gaintype='G',
       calmode='p',
       solint='inf',
       gaintable=[ktab0],
       minsnr=2.0)

bandpass(vis=msfile,
         caltable=bptab,
         field=bpcal,
         refant=refant,
         solint='inf',
         solnorm=True,
         interp=['nearest','linear'],
         gaintable=[ktab0,gtab0])

# Apply calibration and image the flux calibrator
applycal(vis=msfile,
         gaintable=[ktab0,gtab0,bptab],
         field=bpcal,
         calwt=False)

#-----------------Secondary calibrator----------

gaincal(vis=msfile,
       caltable=gtab1,
       field=(',').join((bpcal,apcal)),
       spw=calchan,
       refant=refant,
       gaintype='G',
       calmode='p',
       solint='60s',
       minsnr=2.0,
       gaintable=[ktab0,bptab])

gaincal(vis=msfile,
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
fluxscale(vis=msfile,
       caltable=gtab2,
       fluxtable=fluxtab,
       reference=bpcal)

# Apply calibration to secondary
applycal(vis=msfile,
         gaintable=[ktab0, bptab, gtab1, fluxtab],
         field=apcal,
         gainfield=[bpcal,bpcal,apcal,apcal],
         interp=['nearest','nearest','linear','linear'],
         calwt=False)

#------------------Target----------

# Apply calibration to target
applycal(vis=msfile,
         gaintable=[ktab0, bptab, gtab1, fluxtab],
         field=target,
         gainfield=[bpcal,bpcal,apcal,apcal],
         interp=['nearest','nearest','linear','linear'],
         calwt=False)