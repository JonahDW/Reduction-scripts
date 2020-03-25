import matplotlib
matplotlib.use('agg')

from argparse import ArgumentParser
import ShadeMS
from ShadeMS import shadeMS as sms
import time
import numpy
import daskms as xms
import pandas as pd
import colorcet
import holoviews as hv
import holoviews.operation.datashader as hd
import datashader as ds
import dask.dataframe as dd
from collections import OrderedDict as odict
import pkg_resources
import ast
import matplotlib.pyplot as plt

log = ShadeMS.log

try:
    __version__ = pkg_resources.require("shadems")[0].version
except pkg_resources.DistributionNotFound:
    __version__ = "dev"

def main():

    clock_start = time.time()


    parser = ArgumentParser(description='Rapid Measurement Set plotting with xarray-ms and datashader. Version {0:s}'.format(__version__))

    parser.add_argument('ms', 
                      help='Measurement set')
    parser.add_argument("-v", "--version", action='version',
                      version='{:s} version {:s}'.format(parser.prog, __version__))
    parser.add_argument('--xaxis', dest='xaxis',
                      help='[t]ime (default), [f]requency, [c]hannels, [u], [uv]distance, [r]eal, [a]mplitude', default='t')
    parser.add_argument('--yaxis', dest='yaxis',
                      help='[a]mplitude (default), [p]hase, [r]eal, [i]maginary, [v]', default='a')
    parser.add_argument('--field', dest='myfields',
                      help='Field ID(s) to plot (comma separated list, default = all)', default='all')
    parser.add_argument('--spws', dest='myspws',
                      help='Spectral windows (DDIDs) to plot (comma separated list, default = all)', default='all')
    parser.add_argument('--chans', dest='mychans',
                      help='Channels to plot (single int or tuple, default = all)', default='all')
    parser.add_argument('--baseline', dest='mybaselines',
                      help='Baselines to plot (list of tuples, default = all)', default='all')
    parser.add_argument('--corr', dest='corr',
                      help='Correlation index to plot (default = 0)', default=0)
    parser.add_argument('--noflags', dest='noflags',
                      help='Plot flagged data (default = False)', action='store_true', default=False)
    parser.add_argument('--noconj', dest='noconj',
                      help='Do not show conjugate points in u,v plots (default = plot conjugates)', action='store_true', default=False)
    parser.add_argument('--xmin', dest='xmin',
                      help='Minimum x-axis value (default = data min)', default='')
    parser.add_argument('--xmax', dest='xmax',
                      help='Maximum x-axis value (default = data max)', default='')
    parser.add_argument('--ymin', dest='ymin',
                      help='Minimum y-axis value (default = data min)', default='')
    parser.add_argument('--ymax', dest='ymax',
                      help='Maximum y-axis value (default = data max)', default='')
    parser.add_argument('--png', dest='pngname',
                      help='PNG name (default = something verbose)', default='')

    # Assign inputs

    options = parser.parse_args()

    xaxis = options.xaxis.lower()
    yaxis = options.yaxis.lower()
    myfields = options.myfields
    myspws = options.myspws
    mychans = int(options.mychans)
    mybaselines = ast.literal_eval(options.mybaselines)#[(10,30)]
    noflags = options.noflags
    pngname = options.pngname
    corr = options.corr

    # Trap no MS

    myms = options.ms

    # Check for allowed axes

    allowed = ['a', 'p', 'r', 'i', 't', 'f', 'c', 'uv', 'u', 'v']
    if xaxis not in allowed or yaxis not in allowed:
        raise ValueError('xaxis "%s" is unknown. Please check requested axes' % xaxis)

    xfullname, xunits = sms.fullname(xaxis)
    yfullname, yunits = sms.fullname(yaxis)

    log.info('Plotting %s vs %s' % (yfullname, xfullname))

    # Get MS metadata

    chan_freqs = sms.get_chan_freqs(myms)

    field_ids, field_names = sms.get_field_names(myms)
    antenna_ids = sms.get_antennas(myms)

    # Sort out field selection(s)

    if myfields == 'all':
        fields = field_ids
        # fields = []
        # for group in msdata:
        #   fields.append(group.FIELD_ID)
        # fields = numpy.unique(fields)
    else:
        fields = list(map(int, myfields.split(',')))

    sms.blank()
    log.info('FIELD_ID   NAME')
    for i in fields:
        log.info('%-10s %-16s' % (i, field_names[i]))

    # Sort out SPW selection(s)

    if myspws == 'all':
        spws = numpy.arange(len(chan_freqs))
    else:
        spws = list(map(int, myspws.split(',')))

    if numpy.isscalar(mychans):
        chan_low = int(mychans)
        chan_hi = int(mychans+1)
    else:
        chan_low = int(mychans[0])
        chan_hi = int(mychans[1])

    sms.blank()
    log.info('SPW_ID     NCHAN ')
    for i in spws:
        nchan = len(chan_freqs.values[i])
        log.info('%-10s %-16s' % (i, nchan))

    sms.blank()

    # Construct TaQL string based on FIELD and SPW selections

    field_taq = []
    for fld in fields:
        field_taq.append('FIELD_ID=='+str(fld))

    spw_taq = []
    for spw in spws:
        spw_taq.append('DATA_DESC_ID=='+str(spw))

    mytaql = '('+' || '.join(field_taq)+') && ('+' || '.join(spw_taq)+')'

    # Read the selected data

    log.info('Reading %s' % (myms))

    group_cols = ['ANTENNA1', 'ANTENNA2']

    corrected_data = xms.xds_from_ms(
        myms, columns=['CORRECTED_DATA', 'TIME', 'FLAG', 'FIELD_ID','DATA_DESC_ID', 'UVW'], group_cols=group_cols, taql_where=mytaql)

    model_data = xms.xds_from_ms(
        myms, columns=['MODEL_DATA', 'TIME', 'FLAG', 'FIELD_ID','DATA_DESC_ID', 'UVW'], group_cols=group_cols, taql_where=mytaql)

    # Replace xarray data with a,p,r,i in situ
    # And select only the baseline

    log.info('Rearranging the deck chairs')


    for baseline in mybaselines:

        antenna1 = baseline[0]
        antenna2 = baseline[1]

        new_corrected = []
        for i in range(0, len(corrected_data)):
            if corrected_data[i].ANTENNA1 == antenna1 and corrected_data[i].ANTENNA2 == antenna2:
                corrected_data[i] = corrected_data[i].rename({'CORRECTED_DATA': 'VISDATA'}) 
                new_corrected.append(corrected_data[i])

        new_model = []
        for i in range(0, len(model_data)):
            if model_data[i].ANTENNA1 == antenna1 and model_data[i].ANTENNA2 == antenna2:
                model_data[i] = model_data[i].rename({'MODEL_DATA': 'VISDATA'}) 
                new_model.append(model_data[i])

        # Initialise arrays for plot data

        ydata = numpy.array(())
        xdata = numpy.array(())
        model_ydata = numpy.array(())
        model_xdata = numpy.array(())
        flags = numpy.array(())

        # Get plot data into a pair of numpy arrays

        for group in new_corrected:
            visdata = group.VISDATA.values[:,chan_low:chan_hi,:]

            nrows = visdata.shape[0]
            nchan = visdata.shape[1]
            fld = group.FIELD_ID
            ddid = group.DATA_DESC_ID

            if fld in fields and ddid in spws:
                chans = chan_freqs.values[ddid, chan_low:chan_hi]
                flags = numpy.append(flags, group.FLAG.values[:,chan_low:chan_hi,corr])

                if xaxis == 'uv' or xaxis == 'u' or yaxis == 'v':
                    uu = group.UVW.values[:, 0]
                    vv = group.UVW.values[:, 1]
                    chans_wavel = sms.freq_to_wavel(chans)
                    uu_wavel = numpy.ravel(
                        uu / numpy.transpose(numpy.array([chans_wavel, ]*len(uu))))
                    vv_wavel = numpy.ravel(
                        vv / numpy.transpose(numpy.array([chans_wavel, ]*len(vv))))
                    uvdist_wavel = ((uu_wavel**2.0)+(vv_wavel**2.0))**0.5

                if yaxis == 'a':
                    ydata = numpy.append(ydata, numpy.abs(
                        visdata[:, :, corr]))
                elif yaxis == 'p':
                    ydata = numpy.append(ydata, numpy.angle(
                        visdata[:, :, corr]))
                elif yaxis == 'r':
                    ydata = numpy.append(ydata, numpy.real(
                        visdata[:, :, corr]))
                elif yaxis == 'i':
                    ydata = numpy.append(ydata, numpy.imag(
                        visdata[:, :, corr]))
                elif yaxis == 'v':
                    ydata = numpy.append(ydata, vv_wavel)

                if xaxis == 'f':
                    xdata = numpy.append(xdata, numpy.tile(chans, nrows))
                elif xaxis == 'c':
                    xdata = numpy.append(xdata, numpy.tile(
                        numpy.arange(nchan), nrows))
                elif xaxis == 't':
                    # Add t = t - t[0] and make it relative
                    xdata = numpy.append(
                        xdata, numpy.repeat(group.TIME.values, nchan))
                    xdata = xdata - xdata[0]
                elif xaxis == 'uv':
                    xdata = numpy.append(xdata, uvdist_wavel)
                elif xaxis == 'r':
                    xdata = numpy.append(xdata, numpy.real(
                        visdata[:, :, corr]))
                elif xaxis == 'u':
                    xdata = numpy.append(xdata, uu_wavel)
                elif xaxis == 'a':
                    xdata = numpy.append(xdata, numpy.abs(
                        visdata[:, :, corr]))

        for group in new_model:
            visdata = group.VISDATA.values[:,chan_low:chan_hi,:]

            nrows = visdata.shape[0]
            nchan = visdata.shape[1]
            fld = group.FIELD_ID
            ddid = group.DATA_DESC_ID

            if fld in fields and ddid in spws:
                model_chans = chan_freqs.values[ddid, chan_low:chan_hi]
                model_flags = numpy.append(flags, group.FLAG.values[:,chan_low:chan_hi,corr])

                if xaxis == 'uv' or xaxis == 'u' or yaxis == 'v':
                    uu = group.UVW.values[:, 0]
                    vv = group.UVW.values[:, 1]
                    chans_wavel = sms.freq_to_wavel(chans)
                    uu_wavel = numpy.ravel(
                        uu / numpy.transpose(numpy.array([chans_wavel, ]*len(uu))))
                    vv_wavel = numpy.ravel(
                        vv / numpy.transpose(numpy.array([chans_wavel, ]*len(vv))))
                    uvdist_wavel = ((uu_wavel**2.0)+(vv_wavel**2.0))**0.5

                if yaxis == 'a':
                    model_ydata = numpy.append(model_ydata, numpy.abs(
                        visdata[:, :, corr]))
                elif yaxis == 'p':
                    model_ydata = numpy.append(model_ydata, numpy.angle(
                        visdata[:, :, corr]))
                elif yaxis == 'r':
                    model_ydata = numpy.append(model_ydata, numpy.real(
                        visdata[:, :, corr]))
                elif yaxis == 'i':
                    model_ydata = numpy.append(model_ydata, numpy.imag(
                        visdata[:, :, corr]))
                elif yaxis == 'v':
                    model_ydata = numpy.append(model_ydata, vv_wavel)

                if xaxis == 'f':
                    model_xdata = numpy.append(model_xdata, numpy.tile(chans, nrows))
                elif xaxis == 'c':
                    model_xdata = numpy.append(model_xdata, numpy.tile(
                        numpy.arange(nchan), nrows))
                elif xaxis == 't':
                    # Add t = t - t[0] and make it relative
                    model_xdata = numpy.append(
                        model_xdata, numpy.repeat(group.TIME.values, nchan))
                    model_xdata = model_xdata - model_xdata[0]
                elif xaxis == 'uv':
                    model_xdata = numpy.append(model_xdata, uvdist_wavel)
                elif xaxis == 'r':
                    model_xdata = numpy.append(model_xdata, numpy.real(
                        visdata[:, :, corr]))
                elif xaxis == 'u':
                    model_xdata = numpy.append(model_xdata, uu_wavel)
                elif xaxis == 'a':
                    model_xdata = numpy.append(model_xdata, numpy.abs(
                        visdata[:, :, corr]))
        # Drop flagged data if required

        if not noflags:

            bool_flags = list(map(bool, flags))

            masked_ydata = numpy.ma.masked_array(data=ydata, mask=bool_flags)
            masked_xdata = numpy.ma.masked_array(data=xdata, mask=bool_flags)

            ydata = masked_ydata.compressed()
            xdata = masked_xdata.compressed()

        ylabel = yfullname+' '+yunits
        xlabel = xfullname+' '+xunits
        title = myms.split('/')[-1]+' '+str(antenna_ids[antenna1])+'&'+str(antenna_ids[antenna2])
        if pngname == '':
            pngname = 'plot_'+myms.split('/')[-1]+'_'
            pngname += str(antenna_ids[antenna1])+'&'+str(antenna_ids[antenna2])+'_'
            pngname += yfullname+'_vs_'+xfullname
            pngname += '.png'

        fig, ax = plt.subplots(figsize=(8,5))
        ax.scatter(xdata, ydata, s=10, color='k', label='Corrected')
        ax.plot(model_xdata[2:],model_ydata[2:], marker='o', markersize=5, color='b', label='Model')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.legend()
        fig.savefig(pngname, bbox_inches='tight')

        pngname = options.pngname

    # Stop the clock

    clock_stop = time.time()
    elapsed = str(round((clock_stop-clock_start), 2))

    log.info('Done. Elapsed time: %s seconds.' % (elapsed))

if __name__ == '__main__':
    main()