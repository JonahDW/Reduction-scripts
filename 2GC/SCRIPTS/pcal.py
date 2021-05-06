import sys

import casatasks as ct

msfile = sys.argv[1]
solint = sys.argv[2]
run = sys.argv[3]

gptab = 'GAINTABLES/'+os.path.splitext(msfile)[0]+'.'+run

ct.gaincal(vis=msfile,
           field='0',
           caltable=gptab,
           refant='m001',
           solint=solint,
           solnorm=False,
           combine='',
           minsnr=3,
           calmode='p',
           parang=False,
           gaintable=[],
           gainfield=[],
           interp=[],
           append=False)

ct.applycal(vis=msfile,
            gaintable=[gptab],
            field='0',
            calwt=False,
            parang=False,
            applymode='calonly',
            interp=['nearest'])
