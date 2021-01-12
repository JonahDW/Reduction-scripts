from sys import argv
msfile = argv[3]

flagmanager(vis=msfile,
            mode='save',
            versionname='default')

flagdata(vis=msfile, 
         mode='tfcrop',
         action='apply',
         display='')