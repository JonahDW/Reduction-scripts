import sys
import os

import casatasks as ct

msfile = sys.argv[1]
solint = sys.argv[2]
run = sys.argv[3]

gptab = sys.argv[4]

gaptab = 'GAINTABLES/'+os.path.splitext(msfile)[0]+'.'+run

ct.gaincal(vis=msfile,
           field='0',
           caltable=gaptab,
           refant = 'm001',
           solint=solint,
           solnorm=False,
           combine='',
           minsnr=3,
           calmode='ap',
           parang=False,
           gaintable=[gptab],
           append=False)

ct.applycal(vis=msfile,
            gaintable=[gptab,gaptab],
            field='0',
            calwt=False,
            parang=False,
            applymode='calonly',
            gainfield=['',''],
            interp = ['nearest','linear'])