import sys

import casatasks as ct

msfile=sys.argv[1]

ct.flagdata(vis=msfile,
            mode='manual',
            autocorr=True)

ct.flagdata(vis=msfile,
            mode='clip',
            clipzeros=True)

#MeerKAT RFI regions
ct.flagdata(vis=msfile,
            mode='manual',
            spw="""0:935.0~960.0MHz ;
                1083~1095MHz ;
                1167.8~1185.6MHz ;
                1200.6~1213.0MHz ;
                1226.5~1228.8MHz ;
                1243.7~1249.2MHz ;
                1261.2~1293.7MHz ;
                1525~1563MHz ;
                1573~1578MHz ;
                1588.4~1593.3MHz ;
                1599~1606MHz""")

ct.flagmanager(vis=msfile,
               mode='save',
               versionname='basic')

ct.flagdata(vis=msfile,
            mode='tfcrop',
            action='apply',
            display='')