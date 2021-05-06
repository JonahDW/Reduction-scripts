import sys

import casatasks as ct

msfile = sys.argv[1]

# Bad frequencies
ct.flagdata(vis=msfile,
            mode='manual',
            spw="""*:856~890MHz,
                   *:924~970MHz,
                   *:1027~1033MHz,
                   *:1039~1044MHz,
                   *:1090~1095MHz,
                   *:1139~1310MHz,
                   *:1415~1425MHz,
                   *:1510~1630MHz""")

# Auto correlations
ct.flagdata(vis=msfile,
            mode='manual',
            autocorr=True)

# Zeros
ct.flagdata(vis=msfile,
            mode='clip',
            clipzeros=True)

# Clip
ct.flagdata(vis=msfile,
            mode='clip',
            clipminmax=[0.0,100.0])

ct.flagmanager(vis=msfile,
               mode='save',
               versionname='basic')

ct.flagdata(vis=msfile,
            mode='rflag',
            action='apply',
            display='')