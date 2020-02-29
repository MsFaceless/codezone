#!/bin/python
import numpy
import pandas
from matplotlib import pyplot
import scipy.interpolate

def pandas_interpolate(df, interp_column, method='cubic'):
    df = df.set_index(interp_column)
    df = df.reindex(numpy.arange(df.index.min(), df.index.max(), 0.0005))
    df = df.interpolate(method=method)
    df = df.reset_index()
    df = df.rename(columns={'index': interp_column})
    return df

def scipy_interpolate(df, interp_column, method='cubic'):
    series = {}
    new_x = numpy.arange(df[interp_column].min(), df[interp_column].max(), 0.0005)

    for column in df:
        if column == interp_column:
            series[column] = new_x
        else:
            interp_f = scipy.interpolate.interp1d(df[interp_column], df[column], kind=method)
            series[column] = interp_f(new_x)

    return pandas.DataFrame(series)


if __name__ == '__main__':
    #df = pandas.read_csv('pandas_interpolate_bug/interp_test.csv')

    #df = pandas.read_excel('input/Latest DWS Data Small.xlsx', dtype={'Reading' : numpy.float64, 'Date' : str, 'Time' : str})
    #df['DateTime'] = pandas.to_datetime(str(df['Date']) + ' ' + str(df['Time']), format='%Y/%m/%d %H:%M:%S %H:%M')
    #df = pandas.read_csv('input/Latest DWS Data Small.csv')
    #df['Reading'] = df['Reading'].replace(', ', '.')

    #pd_interp = pandas_interpolate(df, 'DateTime', 'cubic')
    #scipy_interp = scipy_interpolate(df, 'DateTime', 'cubic')

    #pyplot.plot(df['lon'], df['lat'], label='raw data')
    #pyplot.plot(pd_interp['Date'], pd_interp['Date'], label='pandas')
    #pyplot.plot(scipy_interp['Time'], scipy_interp['Time'], label='scipy interp1d')
    #pyplot.legend(loc='best')

    #pyplot.figure()
    #df2 = pandas.DataFrame({'x': numpy.arange(10), 'sin(x)': numpy.sin(numpy.arange(10))})
    #pd_interp2 = pandas_interpolate(df2, 'x', 'cubic')
    #scipy_interp2 = scipy_interpolate(df2, 'x', 'cubic')
    #pyplot.plot(pd_interp2['x'], pd_interp2['sin(x)'], label='pandas')
    #pyplot.plot(scipy_interp2['x'], scipy_interp2['sin(x)'], label='scipy interp1d')
    #pyplot.legend(loc='best')

    df = pandas.read_excel('input/Latest DWS Data Small.xlsx', usecols=['Reading', 'Gauge Plate', 'Date'])
    #df['DateTime'] = pandas.to_datetime(df['Date'], format='%Y/%m/%d %H:%M:%S')
    method = 'pad'
    #method = 'linear'
    #method = 'index'
    #method = 'values'
    #method = 'nearest'
    #method = 'zero'
    #method = 'slinear'
    #method = 'cubic'
    #method = 'quadratic'
    #method = 'barycentric'
    #method = 'polynomial'
    # axis must be same length
    #method = 'spline'

    interp_df = scipy_interpolate(df, 'Date', 'nearest')
    #interp_df = df.interpolate(method=method, limit_direction='forward')
    #interp_df = scipy.interpolate.interp1d(df['Reading'], df['Gauge Plate'], kind=method)

    #padded_df = df.interpolate(method='pad', limit_direction='forward')
    #df['Pad Adjusted'] = padded_df['Gauge Plate']

    #interp_df = df.interpolate(method=method, limit_direction='forward')
    df['Adjusted'] = interp_df['Gauge Plate']


    #reading = df['Reading']
    #thedate = df['Date']
    #control = df['Gauge Plate']

    #diff = numpy.interp(control, thedate, reading)
    #print(diff)
    #df['Adjusted'] = diff['Gauge Plate']
    #df['Adjusted'] = diff['Gauge Plate']
    #df['Adjusted'] = df['Reading']

    print('info start')
    print(df.info())
    print(df.tail())
    print('info done')

    # Horizontal
    x = df['Date']

    # Vertical
    y = df['Reading']
    z = df['Gauge Plate']
    v = df['Adjusted']

    pyplot.plot(x, y, label='Reading')
    pyplot.plot(x, z, label='Gauge Plate')
    pyplot.plot(x, v, label='Adjusted')
    pyplot.legend(loc='best')
    pyplot.show()
