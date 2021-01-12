from sys import argv

msfile = argv[3]
solint = argv[4]
gptab = argv[5]

gaptab = 'GAINTABLES/'+os.path.splitext(msfile)[0]+'.GAP0'

gaincal(vis=msfile,
    field='0',
    caltable=gaptab,
    refant = 'm001',
    solint=solint,
    solnorm=False,
    combine='',
    minsnr=3,
    calmode='a',
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