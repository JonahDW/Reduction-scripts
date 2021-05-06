from sys import argv

msfile = argv[3]
solint = argv[4]
run = argv[5]

gptab = 'GAINTABLES/'+os.path.splitext(msfile)[0]+'.'+run

gaincal(vis=msfile,
    field='0',
    caltable=gptab,
    refant='m057,m059',
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

applycal(vis=msfile,
    gaintable=[gptab],
    field='0',
    calwt=False,
    parang=False,
    applymode='calonly',
    interp = ['nearest'])
