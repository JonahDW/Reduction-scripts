import sys

msfile = sys.argv[3]
solint = sys.argv[4]
run = sys.argv[5]

gptab = sys.argv[6]

gaptab = 'GAINTABLES/'+os.path.splitext(msfile)[0]+'.'+run

gaincal(vis=msfile,
    field='0',
    caltable=gaptab,
    refant = 'm057,m059',
    solint=solint,
    solnorm=False,
    combine='',
    minsnr=3,
    calmode='ap',
    parang=False,
    gaintable=[gptab],
    append=False)

applycal(vis=msfile,
    gaintable=[gptab,gaptab],
    field='0',
    calwt=False,
    parang=False,
    applymode='calonly',
    gainfield=['',''],
    interp = ['nearest','linear'])