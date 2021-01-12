from sys import argv
msfile=argv[3]

# Plot antennas
plotants(vis=msfile,
         figfile='PLOTS/'+msfile+'_ants.png')

# Plot elevation vs time
plotms(vis = msfile,
       field='',
       title='Source elevation',
       yaxis='elevation',
       xaxis='time',
       coloraxis='field',
       showgui=False,
       overwrite=True,
       plotfile='PLOTS/elevation_time.png')

# Plot amp vs time
plotms(vis = msfile,
       yaxis='amplitude',
       xaxis='time',
       coloraxis='baseline',
       showgui=False,
       antenna='1',
       avgchannel='8',
       overwrite=True,
       plotfile='PLOTS/antenna1_amptime.png')

# Plot amplitude vs frequency
plotms(vis = msfile,
       yaxis='amplitude',
       xaxis='frequency',
       coloraxis='baseline',
       showgui=False,
       antenna='1',
       avgtime='5000',
       highres=True,
       overwrite=True,
       plotfile='PLOTS/antenna1_ampfreq.png')

# Plot phase vs frequency
plotms(vis = msfile,
       yaxis='phase',
       xaxis='frequency',
       showgui=False,
       coloraxis='baseline',
       antenna='1',
       avgtime='5000',
       overwrite=True,
       plotfile='PLOTS/antenna1_phasefreq.png')

