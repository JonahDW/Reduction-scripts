from sys import argv
msfile = argv[3]

# Bad frequencies
flagdata(vis=vis,
         mode='manual',
         spw="""*:856~890MHz,
                *:924~970MHz,
                *:1027~1033MHz,
                *:1039~1044MHz,
                *:1090~1095MHz,
                *:1139~1310MHz,
                *:1415~1425MHz,
                *:1510~1630MHz""")

# UVrange
flagdata(vis=vis,
         mode='manual',
         uvrange = '<600')

# Auto correlations
flagdata(vis=vis,
         mode='manual',
         autocorr=True)

# Zeros
flagdata(vis=vis,
         mode='clip',
         clipzeros=True)

# Clip
flagdata(vis=vis,
         mode='clip',
         clipminmax=[0.0,100.0])

flagmanager(vis=msfile,
            mode='save',
            versionname='basic')

flagdata(vis=msfile,
         mode='rflag',
         action='apply',
         display='')